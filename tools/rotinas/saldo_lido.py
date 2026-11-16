#!/usr/bin/env python3
"""Lê o saldo real dos fornecedores que têm API de saldo e grava em financas.saldo_lido (16/11/2026).

Hoje: Runpod (GraphQL `myself.clientBalance`, a mesma leitura do tools/render_runpod.sh).
A view financas.saldo_pre_pago passa a mostrar esse valor (leitura ≤ 3 dias) no lugar de recarregado − consumido.
Nunca imprime nem grava a chave ou a resposta crua. Falha de leitura não derruba quem chamou (sai 0, avisa no stderr).

Uso: tools/.venv/bin/python tools/rotinas/saldo_lido.py [--sem-gravar]
Chamado por: rotinas/diaria.sh (06:30) e noturna.py planejar (pré-voo, 20:00).
"""
import argparse
import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

FONTE_RUNPOD = "api graphql myself.clientBalance (tools/rotinas/saldo_lido.py)"


def ler_runpod(timeout=30):
    chave = (Path.home() / ".segredos/runpod/api_key").read_text().strip()
    req = urllib.request.Request("https://api.runpod.io/graphql", method="POST",
                                 data=json.dumps({"query": "query { myself { clientBalance } }"}).encode(),
                                 headers={"Authorization": f"Bearer {chave}", "Content-Type": "application/json",
                                          "User-Agent": "fabrica-saldo/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return round(float(json.load(r)["data"]["myself"]["clientBalance"]), 4)


def ler_e_gravar(con=None, gravar=True):
    """→ {fornecedor: saldo} das leituras que deram certo; grava em financas.saldo_lido se gravar."""
    out = {}
    try:
        out["Runpod"] = (ler_runpod(), FONTE_RUNPOD)
    except Exception as e:  # noqa: BLE001  (sem detalhes da requisição: nada de chave em log)
        print(f"saldo_lido: Runpod não leu ({type(e).__name__})", file=sys.stderr)
    if gravar and out:
        fechar = con is None
        if con is None:
            import psycopg
            con = psycopg.connect("dbname=vida")
        for forn, (saldo, fonte) in out.items():
            con.execute("INSERT INTO financas.saldo_lido (fornecedor, moeda, saldo, fonte) VALUES (%s,'USD',%s,%s)", (forn, saldo, fonte))
        con.commit()
        if fechar:
            con.close()
    return {k: v[0] for k, v in out.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sem-gravar", action="store_true")
    a = ap.parse_args()
    for forn, s in ler_e_gravar(gravar=not a.sem_gravar).items():
        print(f"{forn}: US$ {s:.2f}")


if __name__ == "__main__":
    main()
