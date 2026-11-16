#!/usr/bin/env python3
"""Registra os 3 pares título+thumb (A/B/C) de um vídeo e o resultado do "Testar e comparar" (16/11/2026).

Tabela youtube.embalagem_variantes (DDL tools/db/schema_embalagem_variantes.sql); placar em youtube.padrao_thumb_placar.

  registrar --video <id> --json <pasta do vídeo>/embalagem/variantes.json [--origem embalagem|reembalagem]
      variantes.json = [{"letra":"A","titulo":"…","padrao_titulo":"…","padrao_thumb":"rosto-emocao",
                         "thumb_conceito":"…","thumb_texto":"…","thumb_arquivo":"entrega/thumb-A.jpg"}, …]  (3 itens)
      Regrava (upsert) por (vídeo, origem, letra): a embalagem grava a proposta; o pacote-youtube regrava com títulos finais e arquivos.
  vencedora --video <id> --letra B [--share A=31,B=45,C=24] [--origem embalagem]
  placar [--canal <slug>]       → tabela por canal × padrão de thumb
  pendentes                     → publicados sem vencedora (o Métricas pede ao Rodrigo)
"""
import argparse
import json
import sys

import psycopg

EIXOS = {"rosto-emocao", "objeto-simbolo", "conflito-xvy", "numero-estatistica", "mapa-lugar", "antes-depois",
         "cena-acao", "documento-evidencia"}
CAMPOS = ("titulo", "padrao_titulo", "padrao_thumb", "thumb_conceito", "thumb_texto", "thumb_arquivo")


def registrar(con, a):
    vs = json.load(open(a.json))
    letras = sorted(v["letra"] for v in vs)
    if letras != ["A", "B", "C"]:
        sys.exit(f"variantes.json precisa de A, B e C (veio {letras})")
    eixos = [v["padrao_thumb"] for v in vs]
    fora = [e for e in eixos if e not in EIXOS]
    if fora:
        print(f"aviso: padrão de thumb fora do vocabulário {sorted(EIXOS)}: {fora} (o placar agrupa pelo texto exato)", file=sys.stderr)
    if len(set(eixos)) < 3:
        sys.exit(f"as 3 thumbs precisam de padrões diferentes (veio {eixos})")
    for v in vs:
        vals = [v.get(k) for k in CAMPOS]
        con.execute(f"""INSERT INTO youtube.embalagem_variantes (video_id, letra, origem, {', '.join(CAMPOS)})
                        VALUES (%s,%s,%s,{', '.join(['%s'] * len(CAMPOS))})
                        ON CONFLICT (video_id, origem, letra) DO UPDATE SET
                        {', '.join(f'{k}=coalesce(EXCLUDED.{k}, youtube.embalagem_variantes.{k})' for k in CAMPOS)}, atualizado_em=now()""",
                    [a.video, v["letra"], a.origem, *vals])
    con.commit()
    print(f"vídeo {a.video}: A/B/C registradas ({', '.join(eixos)})")


def vencedora(con, a):
    share = dict(x.split("=") for x in a.share.split(",")) if a.share else {}
    n = con.execute("UPDATE youtube.embalagem_variantes SET vencedora=(letra=%s), resultado_em=current_date, atualizado_em=now() "
                    "WHERE video_id=%s AND origem=%s", (a.letra, a.video, a.origem)).rowcount
    for l, p in share.items():
        con.execute("UPDATE youtube.embalagem_variantes SET share_pct=%s WHERE video_id=%s AND origem=%s AND letra=%s", (float(p), a.video, a.origem, l))
    con.commit()
    print(f"vídeo {a.video}: vencedora {a.letra} ({n} linhas)")


def tabela(con, sql, args=()):
    cur = con.execute(sql, args)
    cols = [d.name for d in cur.description]
    print(" | ".join(cols))
    for r in cur.fetchall():
        print(" | ".join("" if x is None else str(x) for x in r))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="c", required=True)
    p = sp.add_parser("registrar"); p.add_argument("--video", type=int, required=True); p.add_argument("--json", required=True)
    p.add_argument("--origem", default="embalagem")
    p = sp.add_parser("vencedora"); p.add_argument("--video", type=int, required=True); p.add_argument("--letra", required=True, choices="ABC")
    p.add_argument("--share"); p.add_argument("--origem", default="embalagem")
    p = sp.add_parser("placar"); p.add_argument("--canal")
    sp.add_parser("pendentes")
    a = ap.parse_args()
    with psycopg.connect("dbname=vida") as con:
        if a.c == "registrar":
            registrar(con, a)
        elif a.c == "vencedora":
            vencedora(con, a)
        elif a.c == "placar":
            tabela(con, "SELECT * FROM youtube.padrao_thumb_placar" + (" WHERE canal_slug=%s" if a.canal else "") + " ORDER BY canal_slug, vitorias DESC, testes DESC",
                   (a.canal,) if a.canal else ())
        else:
            tabela(con, "SELECT * FROM youtube.embalagem_sem_resultado ORDER BY publicado_em")


if __name__ == "__main__":
    main()
