"""Registro de eventos operacionais em ops.event_log (schema db/schema_ops.sql). Nunca derruba o chamador.

Python:  from event_log import registrar;  registrar("job_api", "api_erro", "erro", "mensagem", {"status": 401}, ref="x")
Bash:    tools/evento.sh <origem> <tipo> <info|aviso|erro> "<mensagem>" [ref]
Consulta: psql -d vida -c "select ts, origem, tipo, severidade, mensagem from ops.event_log order by ts desc limit 20"
Os detalhes passam por um filtro que troca qualquer coisa parecida com chave (sk-ant-…, tokens longos) por [oculto].
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg  # noqa: E402
from psycopg.types.json import Jsonb  # noqa: E402

SEVERIDADES = ("info", "aviso", "erro")
_SEGREDO = re.compile(r"sk-[A-Za-z0-9_\-]{8,}|[A-Za-z0-9_\-]{40,}")


def limpar(v):
    """Remove segredos de textos/estruturas antes de gravar."""
    if isinstance(v, str):
        return _SEGREDO.sub("[oculto]", v)
    if isinstance(v, dict):
        return {str(k): limpar(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [limpar(x) for x in v]
    return v


def registrar(origem, tipo, severidade="info", mensagem="", detalhes=None, ref=None):
    """Grava um evento; devolve o id (ou None se o banco falhou: só avisa no stderr)."""
    if severidade not in SEVERIDADES:
        severidade = "info"
    try:
        with psycopg.connect(os.environ.get("FABRICA_DB", "dbname=vida"), autocommit=True) as con:
            return con.execute(
                "INSERT INTO ops.event_log (origem, tipo, severidade, mensagem, detalhes, ref) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id",
                (origem, tipo, severidade, limpar(str(mensagem))[:2000], Jsonb(limpar(detalhes or {})), ref)).fetchone()[0]
    except Exception as e:  # noqa: BLE001
        print(f"[event_log] aviso: não gravou ({type(e).__name__})", file=sys.stderr)
        return None


def existe(origem_like, tipo, desde_mes=True, filtro_detalhes=None):
    """True se já há evento do tipo neste mês (para avisos 1× por grupo/mês)."""
    try:
        with psycopg.connect(os.environ.get("FABRICA_DB", "dbname=vida"), autocommit=True) as con:
            q = "SELECT 1 FROM ops.event_log WHERE origem LIKE %s AND tipo=%s AND ts >= date_trunc('month', now())"
            p = [origem_like, tipo]
            if filtro_detalhes:
                q += " AND detalhes @> %s"
                p.append(Jsonb(filtro_detalhes))
            return con.execute(q + " LIMIT 1", p).fetchone() is not None
    except Exception:  # noqa: BLE001
        return False


def recentes(horas=48, tipos=None, minimo="aviso"):
    """Eventos recentes com severidade ≥ minimo, mais novos primeiro (lista de tuplas ts, origem, tipo, sev, msg)."""
    sevs = SEVERIDADES[SEVERIDADES.index(minimo):]
    try:
        with psycopg.connect(os.environ.get("FABRICA_DB", "dbname=vida"), autocommit=True) as con:
            q = ("SELECT ts, origem, tipo, severidade, mensagem FROM ops.event_log WHERE ts > now() - make_interval(hours => %s)"
                 " AND severidade = ANY(%s)")
            p = [horas, list(sevs)]
            if tipos:
                q += " AND tipo = ANY(%s)"
                p.append(list(tipos))
            return con.execute(q + " ORDER BY ts DESC LIMIT 20", p).fetchall()
    except Exception:  # noqa: BLE001
        return []


def main():
    a = sys.argv[1:]
    if a[:1] == ["--resumo"]:  # linha para o resumo das rotinas; vazio se nada
        horas = int(a[1]) if len(a) > 1 else 48
        r = recentes(horas, minimo="aviso")
        if r:
            n_fb = sum(1 for x in r if x[2].startswith("fallback"))
            n_err = sum(1 for x in r if x[3] == "erro")
            ult = r[0]
            print(f"⚠ Últimas {horas} h: {len(r)} evento(s) de API/operação ({n_err} erro, {n_fb} de fallback). "
                  f"Último: {ult[2]} em {ult[1]} — {ult[4][:140]}")
        return
    if len(a) < 4:
        sys.exit("uso: event_log.py <origem> <tipo> <info|aviso|erro> <mensagem> [ref]  |  --resumo [horas]")
    i = registrar(a[0], a[1], a[2], a[3], ref=a[4] if len(a) > 4 else None)
    sys.exit(0 if i else 1)


if __name__ == "__main__":
    main()
