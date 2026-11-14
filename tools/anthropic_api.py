"""Base comum dos scripts que usam os créditos da API Anthropic (US$ 100/mês incluídos no Max).

- Chaves em ~/.segredos/anthropic/<nome>.env (formato ANTHROPIC_API_KEY=...): `rotinas` (rotinas + garimpo em lote)
  e `qa` (pré-QA visual). A chave é lida só no processo que usa, nunca impressa, nunca exportada para o ambiente
  global. ATENÇÃO: não deixe ANTHROPIC_API_KEY no ambiente de um `claude -p` da esteira (faria o Claude Code cobrar
  pela API, e esses créditos não cobrem sessões do Claude Code). O Agent SDK (tools/rotinas/rotina_api.py) recebe a
  chave só no `env` do processo filho.
- Preços (USD por milhão de tokens; https://platform.claude.com/docs/en/about-claude/pricing, lido em 12/11/2026).
  Batch API = 50% do preço normal.
- Todo custo vai para financas.consumo (fornecedor 'Anthropic API'); o crédito do mês está em financas.lancamentos
  (pre_pago), então financas.saldo_pre_pago mostra o saldo.
- Teto mensal por grupo (brief 12/11/2026): rotinas+garimpo ≤ US$ 50 (era 30; Rodrigo 14/11), qa ≤ US$ 25, dev (desenvolvimento e
  pesquisas pela API, servico 'dev:<nome>', tools/job_api.py) ≤ US$ 25. Total 100. `checar_teto()` levanta
  TetoExcedido antes de gastar.
"""
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

FORNECEDOR = "Anthropic API"
SEGREDOS = os.path.expanduser("~/.segredos/anthropic")

# USD / MTok: entrada, escrita de cache 5 min, escrita 1 h, leitura de cache, saída
PRECOS = {
    "claude-opus-5-5": (4.0, 5.0, 8.0, 0.20, 20.0),
    "claude-sonnet-5-5": (2.0, 2.5, 4.0, 0.10, 10.0),
    "claude-haiku-5-5": (0.10, 0.125, 0.20, 0.01, 0.50),       # prompt ≤ 100 mil tokens
    "claude-haiku-5-5>100k": (0.50, 0.625, 1.0, 0.05, 2.50),   # prompt > 100 mil tokens
    "claude-fable-5-2": (8.0, 10.0, 16.0, 0.20, 40.0),
}
APELIDOS = {"opus": "claude-opus-5-5", "sonnet": "claude-sonnet-5-5", "haiku": "claude-haiku-5-5",
            "fable": "claude-fable-5-2"}

# grupos de teto: servico em financas.consumo começa com um destes prefixos
TETOS = {"rotinas": (50.0, ("rotina:", "batch:")), "qa": (25.0, ("preqa",)),
         "dev": (25.0, ("dev:",))}


class TetoExcedido(RuntimeError):
    pass


def modelo_id(m):
    return APELIDOS.get(m, m)


def carregar_chave(nome):
    """Lê ANTHROPIC_API_KEY de ~/.segredos/anthropic/<nome>.env e devolve a string (nunca imprime).
    Teste: FABRICA_CHAVE_ARQUIVO=<arquivo .env falso> troca o arquivo (sem tocar nas chaves reais)."""
    caminho = os.environ.get("FABRICA_CHAVE_ARQUIVO") or os.path.join(SEGREDOS, f"{nome}.env")
    with open(caminho, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha.startswith("ANTHROPIC_API_KEY="):
                v = linha.split("=", 1)[1].strip().strip('"').strip("'")
                if v:
                    return v
    raise RuntimeError(f"ANTHROPIC_API_KEY não encontrada em {caminho}")


def cliente(nome_chave):
    import anthropic
    return anthropic.Anthropic(api_key=carregar_chave(nome_chave), max_retries=4)


def _u(usage, campo):
    if usage is None:
        return 0
    v = usage.get(campo) if isinstance(usage, dict) else getattr(usage, campo, None)
    return int(v or 0)


def custo_usd(modelo, usage, batch=False):
    """Custo de uma resposta (usage do Messages API, objeto ou dict). Escrita de cache contada como 5 min."""
    m = modelo_id(modelo)
    ent, cw, cw1h, cr = (_u(usage, "input_tokens"), _u(usage, "cache_creation_input_tokens"), 0,
                         _u(usage, "cache_read_input_tokens"))
    cc = usage.get("cache_creation") if isinstance(usage, dict) else getattr(usage, "cache_creation", None)
    if cc:
        e1h = cc.get("ephemeral_1h_input_tokens") if isinstance(cc, dict) else getattr(cc, "ephemeral_1h_input_tokens", 0)
        cw1h = int(e1h or 0)
        cw = max(cw - cw1h, 0)
    sai = _u(usage, "output_tokens")
    base = next((k for k in PRECOS if m.startswith(k)), None)
    if base == "claude-haiku-5-5" and ent + cw + cw1h + cr > 100_000:
        base = "claude-haiku-5-5>100k"
    if base is None:
        base = "claude-opus-5-5"  # desconhecido: preço mais alto da família (conservador)
    p_in, p_cw, p_cw1h, p_cr, p_out = PRECOS[base]
    c = (ent * p_in + cw * p_cw + cw1h * p_cw1h + cr * p_cr + sai * p_out) / 1e6
    return c * (0.5 if batch else 1.0)


def gasto_mes(grupo, quando=None):
    """US$ já gastos no mês corrente pelo grupo (rotinas | qa | dev)."""
    from db import conectar
    _, prefixos = TETOS[grupo]
    quando = quando or dt.date.today()
    ini = quando.replace(day=1)
    fim = (ini + dt.timedelta(days=32)).replace(day=1)
    filtro = " OR ".join(["servico LIKE %s"] * len(prefixos))
    with conectar() as con:
        r = con.execute(f"SELECT COALESCE(SUM(custo),0) FROM financas.consumo WHERE fornecedor=%s AND ocorrido_em>=%s"
                        f" AND ocorrido_em<%s AND ({filtro})", (FORNECEDOR, ini, fim, *[p + "%" for p in prefixos])).fetchone()
    return float(r[0])


def checar_teto(grupo, previsto=0.0):
    """Levanta TetoExcedido se gasto do mês + previsto passar do teto do grupo. Se o banco falhar, avisa e deixa seguir."""
    teto, _ = TETOS[grupo]
    if os.environ.get("FABRICA_TETO_TESTE"):  # só para teste do fallback: teto artificial em US$
        teto = float(os.environ["FABRICA_TETO_TESTE"])
    try:
        g = gasto_mes(grupo)
    except Exception as e:  # noqa: BLE001
        print(f"[anthropic_api] aviso: não consegui ler o gasto do mês ({type(e).__name__}); sigo.", file=sys.stderr)
        return None
    if g >= 0.8 * teto and not os.environ.get("FABRICA_TETO_TESTE"):
        from event_log import existe, registrar
        if not existe("teto:%", "teto_aviso", filtro_detalhes={"grupo": grupo}):
            registrar(f"teto:{grupo}", "teto_aviso", "aviso",
                      f"grupo '{grupo}' em {g / teto:.0%} do teto mensal (US$ {g:.2f} de {teto:.0f})",
                      {"grupo": grupo, "gasto_mes_usd": round(g, 2), "teto_usd": teto})
    if g + previsto > teto:
        from event_log import registrar
        registrar(f"teto:{grupo}", "teto_atingido", "erro", f"teto mensal do grupo '{grupo}' atingido",
                  {"grupo": grupo, "gasto_mes_usd": round(g, 2), "previsto_usd": round(previsto, 2), "teto_usd": teto})
        raise TetoExcedido(f"teto mensal do grupo '{grupo}' (US$ {teto:.0f}): gasto US$ {g:.2f} + previsto US$ {previsto:.2f}")
    return teto - g


def registrar_consumo(custo, servico, quantidade, unidade="tokens", notas=None, video=None, projeto="fabrica"):
    """Grava uma linha em financas.consumo (custo em USD; custo_brl 0 porque o crédito vem incluído no Max)."""
    from db import tentar

    def ins(con):
        return con.execute(
            "INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda,"
            " custo_brl, ref_tipo, ref_id, notas) VALUES ('youtube',%s,%s,%s,%s,%s,%s,'USD',0,%s,%s,%s) RETURNING id",
            (projeto, FORNECEDOR, servico[:200], round(float(quantidade), 2), unidade, round(float(custo), 6),
             "youtube.video" if video else None, video, notas)).fetchone()[0]
    return tentar(ins)


def tokens_total(usage):
    return sum(_u(usage, k) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens",
                                      "output_tokens"))
