"""Fallback API → plano Max (12/11/2026). Quando a API Anthropic falha (HTTP 4xx/5xx/overload persistente, chave inválida,
crédito esgotado, teto mensal do grupo), a rotina/job conclui o trabalho com `claude -p` via tools/claude_run.sh, com
ANTHROPIC_API_KEY removida do ambiente (cobra do plano Max). No máximo 1 fallback por execução (quem chama chama 1×).
Todo passo vai para ops.event_log (event_log.py). Nunca grava segredo.
"""
import calendar
import datetime as dt
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from event_log import registrar  # noqa: E402

FAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PADROES = [  # (tipo, regex) — a ordem importa: teto e crédito antes do genérico
    ("teto_atingido", r"teto mensal"),
    ("api_credito", r"credit balance|billing|insufficient (funds|credit)|purchase credits|payment required|\b402\b"),
    ("api_erro", r"invalid.{0,10}api.?key|x-api-key|authentication_error|unauthorized|\b401\b|\b403\b|permission_error|"
                 r"ANTHROPIC_API_KEY não encontrada|No such file|apiKeySource|overloaded|\b529\b|\b50[0234]\b|api_error|"
                 r"internal.?server|rate.?limit|\b429\b|connection error|APIConnectionError|APIStatusError|"
                 r"service unavailable|bad gateway"),
]


def classificar(texto):
    """Tipo de evento se o texto indica falha da API (api_erro | api_credito | teto_atingido); senão None."""
    t = texto or ""
    for tipo, rx in _PADROES:
        if re.search(rx, t, re.I):
            return tipo
    return None


def status_http(texto):
    m = re.search(r"\b(4\d\d|5\d\d)\b", texto or "")
    return int(m.group(1)) if m else None


def registrar_falha(origem, tipo, texto, grupo=None, modelo=None, ref=None, extra=None):
    """Grava api_erro/api_credito/teto_atingido; em crédito, avisa se acabou antes do fim do mês. Devolve o tipo."""
    det = {"status_http": status_http(texto), "modelo": modelo, "grupo": grupo, **(extra or {})}
    msg = {"teto_atingido": "teto mensal do grupo atingido", "api_credito": "crédito/billing da API esgotado",
           "api_erro": "erro da API Anthropic"}.get(tipo, tipo)
    hoje = dt.date.today()
    if tipo == "api_credito" and hoje.day < calendar.monthrange(hoje.year, hoje.month)[1]:
        msg = f"crédito da API acabou antes do fim do mês (dia {hoje.day}/{calendar.monthrange(hoje.year, hoje.month)[1]})"
        try:
            import anthropic_api as A
            if grupo in A.TETOS:
                det["gasto_mes_usd"] = round(A.gasto_mes(grupo), 2)
                det["teto_usd"] = A.TETOS[grupo][0]
        except Exception:  # noqa: BLE001
            pass
    registrar(origem, tipo, "erro", f"{msg}: {(texto or '')[:300]}", det, ref)
    return tipo


def rodar_no_max(origem, etapa, prompt_file, modelo, timeout, ref=None, max_turns=None, motivo=None, detalhes=None):
    """Roda o mesmo prompt com claude -p (plano Max) via claude_run.sh. Devolve o código de saída (0 = ok)."""
    det = {"modelo": modelo, "motivo": motivo, **(detalhes or {})}
    registrar(origem, "fallback_max", "aviso", f"API indisponível ({motivo}); caindo para o plano Max (claude -p)", det, ref)
    cmd = [os.path.join(FAB, "tools", "claude_run.sh"), "--etapa", etapa, "--cwd", FAB, "--prompt-file", prompt_file,
           "--modelo", modelo, "--timeout", str(timeout), "--permission-mode", "bypassPermissions"]
    if max_turns:
        cmd += ["--max-turns", str(max_turns)]
    env = {k: v for k, v in os.environ.items() if k not in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")}
    env["CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS"] = "0"
    print(f"[fallback_max] {origem}: API falhou ({motivo}); rodando no plano Max.", file=sys.stderr, flush=True)
    t0 = time.monotonic()
    try:
        rc = subprocess.run(cmd, cwd=FAB, env=env).returncode
    except Exception as e:  # noqa: BLE001
        registrar(origem, "fallback_falhou", "erro", f"fallback não rodou: {type(e).__name__}", det, ref)
        return 1
    det["duracao_s"] = int(time.monotonic() - t0)
    if rc == 0:
        registrar(origem, "fallback_ok", "info", "fallback no plano Max concluído", det, ref)
    else:
        registrar(origem, "fallback_falhou", "erro", f"fallback no plano Max terminou com código {rc}", {**det, "codigo": rc}, ref)
    return rc
