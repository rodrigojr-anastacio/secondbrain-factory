"""Conexão com o banco "vida" (Postgres local, esquema youtube). Autenticação peer pelo usuário do SO."""
import os
import sys

import psycopg
from psycopg.types.json import Jsonb

DSN = os.environ.get("FABRICA_DB", "dbname=vida")


def conectar():
    con = psycopg.connect(DSN, autocommit=True)
    con.execute("SET search_path = youtube")
    return con


def tentar(func, *args, **kw):
    """Grava no banco sem derrubar o script se o banco falhar (o arquivo continua sendo a saída principal)."""
    try:
        with conectar() as con:
            return func(con, *args, **kw)
    except Exception as e:  # noqa: BLE001
        print(f"[db] aviso: não gravou no banco ({type(e).__name__}: {e})", file=sys.stderr)


__all__ = ["conectar", "tentar", "Jsonb"]
