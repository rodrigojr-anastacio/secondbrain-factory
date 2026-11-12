"""Roda um brief como "job" pelo Agent SDK com a chave da API (créditos de US$ 100/mês do Max, grupo `dev`),
fora da cota do Claude Max. Mesmo comportamento de `claude -p "Execute o brief …"`: lê o brief, trabalha no repo com
Bash/Read/Write/Edit/Glob/Grep/WebFetch/WebSearch, commita e escreve a resposta final no log.

Uso (normalmente via tools/job_api.sh):
  tools/.venv/bin/python tools/job_api.py <brief.md> [--modelo opus|sonnet|haiku|<id>] [--orcamento 5.0]
                                          [--timeout 7200] [--max-turns 400] [--nome <slug>]

Motor e registros são os de rotina_api.py (chave só no env do processo filho, confere apiKeySource, trava por nome),
mas o custo vai para financas.consumo com servico 'dev:<nome>' e conta no teto mensal do grupo `dev` (US$ 40).
Falha da API ou teto mensal: registra em ops.event_log e cai 1× para o plano Max (claude -p, fallback_max.py).
Códigos: 0 ok, 1 erro/timeout (ou fallback falhou), 2 argumento, 3 trava ocupada.
"""
import argparse
import asyncio
import datetime as dt
import os
import re
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "rotinas"))
import rotina_api as R  # noqa: E402  (também põe tools/ no path)
import anthropic_api as A  # noqa: E402
import fallback_max as F  # noqa: E402
import tempfile  # noqa: E402
from db import tentar  # noqa: E402

R.REGRAS_HEADLESS = R.REGRAS_HEADLESS.replace("Não faça push.", "Commit só dos seus caminhos; push só se o brief mandar.") \
    .replace("(rotina da fábrica pela API)", "(job pela API, grupo dev)") \
    + "- Ferramentas: Bash, Read, Write, Edit, Glob, Grep, WebFetch, WebSearch (sem subagentes).\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("brief")
    ap.add_argument("--modelo", default="sonnet")
    ap.add_argument("--orcamento", type=float, default=5.0, help="US$ máximo deste job")
    ap.add_argument("--timeout", type=int, default=7200)
    ap.add_argument("--max-turns", type=int, default=400)
    ap.add_argument("--nome")
    a = ap.parse_args()
    brief = os.path.abspath(os.path.expanduser(a.brief))
    if not os.path.isfile(brief):
        ap.error(f"brief não encontrado: {brief}")
    nome = re.sub(r"[^a-z0-9-]+", "-", (a.nome or os.path.basename(brief).removesuffix(".md").removeprefix("BRIEF-")).lower()).strip("-")[:60]
    prompt = f"Execute o brief em {brief}"

    trava = R.travar(f"job-{nome}")
    if trava is None:
        print(f"[job_api] AVISO: job '{nome}' já em andamento; nada foi chamado.", file=sys.stderr)
        sys.exit(3)
    origem = "job_api"

    def cair_para_max(tipo, texto):
        if tipo != "teto_atingido":  # o teto já foi registrado por A.checar_teto
            F.registrar_falha(origem, tipo, texto, "dev", A.modelo_id(a.modelo), nome)
        trava.close()  # libera a trava: o claude_run usa a mesma (etapa job-<nome>)
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as tf:
            tf.write(prompt)
        try:
            rc = F.rodar_no_max(origem, f"job-{nome}", tf.name, a.modelo, a.timeout, ref=nome, max_turns=a.max_turns,
                                motivo=tipo, detalhes={"texto": texto[:200]})
        finally:
            os.unlink(tf.name)
        sys.exit(rc)

    try:
        A.checar_teto("dev", previsto=a.orcamento)
    except A.TetoExcedido as e:
        print(f"[job_api] AVISO: {e}.", file=sys.stderr)
        cair_para_max("teto_atingido", str(e))

    inicio = dt.datetime.now(dt.timezone.utc)
    t0 = time.monotonic()
    res, erro = None, None
    try:
        res = asyncio.run(asyncio.wait_for(R.rodar(a, prompt, A.carregar_chave("rotinas")), timeout=a.timeout))
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
                                        " ".join(R.CLI_ERR[-10:])])) if is_error and subtype != "error_max_budget_usd" and not (erro or "").startswith("timeout") else None

    if custo > 0 or tokens:
        A.registrar_consumo(custo, f"dev:{nome}", tokens, "tokens",
                            notas=f"job_api.py {modelos}; {res.num_turns if res else '?'} turnos; {dur // 1000}s; "
                                  f"{'ERRO ' + str(subtype) if is_error else 'ok'}")

    def reg(con):
        return con.execute(
            "INSERT INTO youtube.execucoes_claude (video_id, etapa, modelo, modelo_real, session_id, inicio, fim,"
            " duracao_ms, num_turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens,"
            " custo_usd_equivalente, is_error, subtype, resultado, cwd, prompt_resumo)"
            " VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id",
            (f"job:{nome}", f"api:{a.modelo}", modelos, res.session_id if res else None, inicio, fim, dur,
             res.num_turns if res else None, u.get("input_tokens"), u.get("output_tokens"),
             u.get("cache_read_input_tokens"), u.get("cache_creation_input_tokens"), custo, is_error, subtype,
             str(texto)[:2000], R.FAB, "[API job] " + prompt[:280])).fetchone()[0]
    rid = tentar(reg)

    if falha_api:
        print(f"[job_api] falha da API ({falha_api}): {str(texto)[:300]}", file=sys.stderr)
        cair_para_max(falha_api, " ".join([str(texto), " ".join(R.CLI_ERR[-10:])]))

    print(texto)
    print(f"\n[job_api] {nome} · {modelos} · {dur / 1000:.0f}s · {res.num_turns if res else '?'} turnos · {tokens} tokens · "
          f"US$ {custo:.4f} (créditos da API, grupo dev) · {'ERRO ' + str(subtype) if is_error else 'ok'} · "
          f"execucoes_claude id {rid}", file=sys.stderr)
    sys.exit(1 if is_error else 0)


if __name__ == "__main__":
    main()
