"""Roda uma rotina da fábrica pelo Agent SDK do Claude com a chave da API (créditos de US$ 100/mês do Max),
fora da cota do Claude Max. Substitui o `claude_run.sh` nas rotinas automáticas (tendências, métricas,
palavras-chave) desde 12/11/2026.

Uso (normalmente chamado por _rotina_claude.sh):
  tools/.venv/bin/python tools/rotinas/rotina_api.py --rotina <tendencias|metricas|palavras-chave> \
      --prompt-file <arquivo> [--modelo sonnet|haiku|opus|<id>] [--orcamento 3.0] [--timeout 5400] [--max-turns 150]

- Mesmas ferramentas do Claude Code (Bash, Read com visão, Write, Edit, Glob, Grep), mesmo prompt de
  prompts/<rotina>.md, mesmo cwd (o repo), `bypassPermissions`. O CLAUDE.md do projeto é carregado
  (setting_sources=["project"]); as configurações do usuário (plugins, MCP) não.
- A chave (~/.segredos/anthropic/rotinas.env) vai só no env do processo filho. O script confere no evento `init` que
  a autenticação é a chave (apiKeySource=ANTHROPIC_API_KEY); se não for, aborta (não roda na cota do Max por engano).
- Teto: `--orcamento` (max_budget_usd por execução) e o teto mensal do grupo `rotinas` (US$ 65, tools/anthropic_api.py).
- Trava: a mesma do claude_run (~/.cache/fabrica/locks/claude-sem-video-<rotina>.lock): duas execuções da mesma
  rotina nunca rodam juntas, seja pela API ou pelo claude -p.
- Registro: custo real em financas.consumo (servico 'rotina:<rotina>') e uma linha em youtube.execucoes_claude
  (modelo 'api:<modelo>'; custo_usd_equivalente = custo real cobrado nos créditos).
- Falha da API (rede, 401, 429, 5xx/overload, crédito esgotado) ou teto mensal do grupo: registra em ops.event_log e
  **cai 1× para o plano Max** (`claude -p` via claude_run.sh, sem ANTHROPIC_API_KEY; fallback_max.py) com o mesmo prompt.
  Orçamento da execução estourado e timeout NÃO acionam fallback. Códigos: 0 ok, 1 erro/timeout (ou fallback falhou),
  2 argumento, 3 trava ocupada.
"""
import argparse
import asyncio
import datetime as dt
import fcntl
import os
import sys
import time

TOOLS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, TOOLS)
import anthropic_api as A  # noqa: E402
import fallback_max as F  # noqa: E402
from db import tentar  # noqa: E402

FAB = os.path.dirname(TOOLS)
LOCKS = os.path.expanduser(os.environ.get("FABRICA_LOCKS", "~/.cache/fabrica/locks"))
MODELO_PADRAO = {"tendencias": "sonnet", "palavras-chave": "sonnet", "metricas": "sonnet", "reembalagem": "sonnet"}
ORCAMENTO_PADRAO = {"tendencias": 4.0, "palavras-chave": 3.0, "metricas": 1.5, "reembalagem": 4.0}
REGRAS_HEADLESS = (
    "\n\n# Execução automática (rotina da fábrica pela API)\n"
    "- Ninguém vai responder perguntas: decida e siga; não pare por pendência menor.\n"
    "- Rode tudo em primeiro plano. Nunca use run_in_background nem '&'; nunca termine com processo pendente.\n"
    "- Responda em português do Brasil. Segredos ficam em ~/.segredos/: nunca imprima, copie nem commite.\n"
    "- Nunca rode `claude` (Claude Code) de dentro desta execução.\n"
    "- `git add` só dos caminhos que você mudou; se houver .git/index.lock, espere e tente de novo. Não faça push.\n")


CLI_ERR = []  # últimas linhas do stderr do CLI do Agent SDK (para classificar a falha da API)


def travar(rotina):
    os.makedirs(LOCKS, exist_ok=True)
    f = open(os.path.join(LOCKS, f"claude-sem-video-{rotina}.lock"), "a+")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        f.close()
        return None
    f.seek(0)
    f.truncate()
    f.write(f"pid={os.getpid()} desde={dt.datetime.now().isoformat(timespec='seconds')} motor=api\n")
    f.flush()
    return f


def resumo_ferramenta(bloco):
    nome = getattr(bloco, "name", "?")
    ent = getattr(bloco, "input", {}) or {}
    alvo = ent.get("command") or ent.get("file_path") or ent.get("pattern") or ent.get("description") or ""
    return f"[tool] {nome}: {str(alvo)[:200]}"


async def rodar(a, prompt, chave):
    from claude_agent_sdk import (AssistantMessage, ClaudeAgentOptions, ResultMessage, SystemMessage, TextBlock,
                                  ToolUseBlock, query)
    env = {"ANTHROPIC_API_KEY": chave, "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0",
           "CLAUDE_CODE_OAUTH_TOKEN": "", "DISABLE_AUTOUPDATER": "1"}
    opts = ClaudeAgentOptions(
        model=A.modelo_id(a.modelo), cwd=FAB, permission_mode="bypassPermissions",
        setting_sources=["project"], max_turns=a.max_turns, max_budget_usd=a.orcamento, env=env,
        system_prompt={"type": "preset", "preset": "claude_code", "append": REGRAS_HEADLESS},
        stderr=lambda s: (CLI_ERR.append(s.rstrip()[:500]), print(f"[cli] {s.rstrip()}", file=sys.stderr)))
    resultado = None
    async for msg in query(prompt=prompt, options=opts):
        if isinstance(msg, SystemMessage) and msg.subtype == "init":
            fonte = (msg.data or {}).get("apiKeySource")
            print(f"[init] modelo={msg.data.get('model')} apiKeySource={fonte}", flush=True)
            if fonte != "ANTHROPIC_API_KEY":
                raise RuntimeError(f"autenticação não é a chave da API (apiKeySource={fonte}); abortado para não "
                                   "usar a cota do Max")
        elif isinstance(msg, AssistantMessage):
            for b in msg.content:
                if isinstance(b, TextBlock) and b.text.strip():
                    print(f"[claude] {b.text.strip()[:1500]}", flush=True)
                elif isinstance(b, ToolUseBlock):
                    print(resumo_ferramenta(b), flush=True)
        elif isinstance(msg, ResultMessage):
            resultado = msg
    return resultado


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rotina", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--modelo")
    ap.add_argument("--orcamento", type=float, help="US$ máximo desta execução (max_budget_usd)")
    ap.add_argument("--timeout", type=int, default=5400)
    ap.add_argument("--max-turns", type=int, default=150)
    a = ap.parse_args()
    a.modelo = a.modelo or MODELO_PADRAO.get(a.rotina, "sonnet")
    a.orcamento = a.orcamento or ORCAMENTO_PADRAO.get(a.rotina, 2.0)
    prompt = open(a.prompt_file, encoding="utf-8").read()
    if not prompt.strip():
        ap.error("prompt vazio")

    trava = travar(a.rotina)
    if trava is None:
        print(f"[rotina_api] AVISO: rotina '{a.rotina}' já em andamento; nada foi chamado.", file=sys.stderr)
        sys.exit(3)
    origem = f"rotina:{a.rotina}"

    def cair_para_max(tipo, texto):
        if tipo != "teto_atingido":  # o teto já foi registrado por A.checar_teto
            F.registrar_falha(origem, tipo, texto, "rotinas", A.modelo_id(a.modelo), a.rotina)
        trava.close()  # libera a trava: o claude_run usa a mesma
        sys.exit(F.rodar_no_max(origem, a.rotina, a.prompt_file, a.modelo, a.timeout, ref=a.rotina,
                                max_turns=a.max_turns, motivo=tipo, detalhes={"texto": texto[:200]}))

    try:
        A.checar_teto("rotinas", previsto=a.orcamento)
    except A.TetoExcedido as e:
        print(f"[rotina_api] AVISO: {e}.", file=sys.stderr)
        cair_para_max("teto_atingido", str(e))

    inicio = dt.datetime.now(dt.timezone.utc)
    t0 = time.monotonic()
    res, erro = None, None
    try:
        res = asyncio.run(asyncio.wait_for(rodar(a, prompt, A.carregar_chave("rotinas")), timeout=a.timeout))
    except asyncio.TimeoutError:
        erro = f"timeout de {a.timeout}s"
    except Exception as e:  # noqa: BLE001
        erro = f"{type(e).__name__}: {str(e)[:500]}"
    fim = dt.datetime.now(dt.timezone.utc)
    dur = int((time.monotonic() - t0) * 1000)

    u = (res.usage if res else None) or {}
    custo = float(res.total_cost_usd or 0) if res else 0.0
    modelos = ",".join(sorted((res.model_usage or {}).keys())) if res and res.model_usage else A.modelo_id(a.modelo)
    is_error = bool(erro) or res is None or bool(res.is_error)
    subtype = "erro_api" if erro else (res.subtype if res else "sem_resultado")
    texto = (res.result if res and res.result else erro) or "(sem saída)"
    tokens = A.tokens_total(u)
    falha_api = F.classificar(" ".join([erro or "", str(res.result) if res and res.is_error and res.result else "",
                                        " ".join(CLI_ERR[-10:])])) if is_error and subtype != "error_max_budget_usd" and not (erro or "").startswith("timeout") else None

    if custo > 0 or tokens:
        A.registrar_consumo(custo, f"rotina:{a.rotina}", tokens, "tokens",
                            notas=f"rotina_api.py {modelos}; {res.num_turns if res else '?'} turnos; {dur // 1000}s; "
                                  f"{'ERRO ' + str(subtype) if is_error else 'ok'}")

    def reg(con):
        return con.execute(
            "INSERT INTO youtube.execucoes_claude (video_id, etapa, modelo, modelo_real, session_id, inicio, fim,"
            " duracao_ms, num_turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens,"
            " custo_usd_equivalente, is_error, subtype, resultado, cwd, prompt_resumo)"
            " VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id",
            (a.rotina, f"api:{a.modelo}", modelos, res.session_id if res else None, inicio, fim, dur,
             res.num_turns if res else None, u.get("input_tokens"), u.get("output_tokens"),
             u.get("cache_read_input_tokens"), u.get("cache_creation_input_tokens"), custo, is_error, subtype,
             str(texto)[:2000], FAB, "[API] " + prompt[:290])).fetchone()[0]
    rid = tentar(reg)

    if falha_api:
        print(f"[rotina_api] falha da API ({falha_api}): {str(texto)[:300]}", file=sys.stderr)
        cair_para_max(falha_api, " ".join([str(texto), " ".join(CLI_ERR[-10:])]))

    print(texto)
    print(f"\n[rotina_api] {a.rotina} · {modelos} · {dur / 1000:.0f}s · {res.num_turns if res else '?'} turnos · "
          f"{tokens} tokens · US$ {custo:.4f} (créditos da API) · {'ERRO ' + str(subtype) if is_error else 'ok'} · "
          f"execucoes_claude id {rid}", file=sys.stderr)
    sys.exit(1 if is_error else 0)


if __name__ == "__main__":
    main()
