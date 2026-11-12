"""YouTube Reporting API: jobs, download e gravação de impressões/CTR e origem de tráfego.

Uso (a partir de tools/):
  .venv/bin/python reporting.py --criar-jobs     # cria (idempotente) os jobs de todos os canais com token
  .venv/bin/python reporting.py --baixar         # baixa relatórios novos e grava em youtube.alcance_diario
  .venv/bin/python reporting.py --status         # jobs e relatórios já baixados
  .venv/bin/python reporting.py --canal X        # limita a um canal
Impressões/CTR chegam com 1–2 dias de atraso; os relatórios só existem a partir da criação do job.
Nunca imprime token.
"""
import argparse
import csv
import io
import os
import sys

import requests
from googleapiclient.discovery import build

from _paths import TOKENS, TOOLS
from db import conectar
from report import creds_for

TIPOS = ["channel_reach_combined_a1", "channel_reach_basic_a1", "channel_traffic_source_a3"]


def migrar(con):
    con.execute(open(os.path.join(TOOLS, "db", "schema_alcance.sql")).read())


def canais_com_token(con, so=None):
    slugs = [r[0] for r in con.execute("SELECT slug FROM canais WHERE status <> 'arquivado' ORDER BY slug")]
    return [s for s in slugs if os.path.exists(os.path.join(TOKENS, f"{s}.json")) and (not so or s == so)]


def criar_jobs(con, so=None):
    for slug in canais_com_token(con, so):
        api = build("youtubereporting", "v1", credentials=creds_for(slug))
        existentes = {j["reportTypeId"]: j["id"] for j in api.jobs().list().execute().get("jobs", [])}
        for tipo in TIPOS:
            if tipo in existentes:
                jid, novo = existentes[tipo], False
            else:
                jid, novo = api.jobs().create(body={"reportTypeId": tipo, "name": f"fabrica-{slug}-{tipo}"}).execute()["id"], True
            con.execute("INSERT INTO reporting_jobs (canal_slug,tipo,job_id) VALUES (%s,%s,%s)"
                        " ON CONFLICT (canal_slug,tipo) DO UPDATE SET job_id=EXCLUDED.job_id", (slug, tipo, jid))
            print(f"- {slug}: {tipo} {'CRIADO' if novo else 'já existia'}")


def num(x, f=float):
    return f(x) if x not in ("", None) else None


def gravar(con, slug, tipo, texto):
    rows = list(csv.DictReader(io.StringIO(texto)))
    n = 0
    for r in rows:
        data = f"{r['date'][:4]}-{r['date'][4:6]}-{r['date'][6:]}"
        vid = r.get("video_id") or ""
        if tipo.startswith("channel_reach"):
            origem = r.get("traffic_source_type") or ""
            imp, ctr = num(r.get("video_thumbnail_impressions"), int), num(r.get("video_thumbnail_impressions_ctr"))
            views = mins = None
        else:
            origem = r.get("traffic_source_type") or ""
            imp = ctr = None
            views, mins = num(r.get("views"), int), num(r.get("watch_time_minutes"))
        con.execute(
            "INSERT INTO alcance_diario (canal_slug,video_id,data,origem,impressoes,ctr,views,minutos,fonte)"
            " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (canal_slug,video_id,data,origem,fonte) DO UPDATE SET"
            " impressoes=EXCLUDED.impressoes, ctr=EXCLUDED.ctr, views=EXCLUDED.views, minutos=EXCLUDED.minutos, baixado_em=now()",
            (slug, vid, data, origem, imp, ctr, views, mins, tipo))
        n += 1
    return n


def baixar(con, so=None):
    for slug in canais_com_token(con, so):
        creds = creds_for(slug)
        api = build("youtubereporting", "v1", credentials=creds)
        for tipo, jid in con.execute("SELECT tipo,job_id FROM reporting_jobs WHERE canal_slug=%s", (slug,)).fetchall():
            vistos = {r[0] for r in con.execute("SELECT report_id FROM reporting_relatorios WHERE canal_slug=%s AND tipo=%s", (slug, tipo))}
            reps = api.jobs().reports().list(jobId=jid).execute().get("reports", [])
            novos = [r for r in reps if r["id"] not in vistos]
            for r in sorted(novos, key=lambda r: r["startTime"]):
                resp = requests.get(r["downloadUrl"], headers={"Authorization": f"Bearer {creds.token}"}, timeout=120)
                resp.raise_for_status()
                n = gravar(con, slug, tipo, resp.text)
                con.execute("INSERT INTO reporting_relatorios (report_id,canal_slug,tipo,inicio,fim,linhas) VALUES (%s,%s,%s,%s,%s,%s)",
                            (r["id"], slug, tipo, r["startTime"][:10], r["endTime"][:10], n))
            print(f"- {slug}: {tipo}: {len(reps)} relatórios no job, {len(novos)} novos")


def status(con, so=None):
    for r in con.execute("SELECT canal_slug,tipo,job_id,criado_em::date FROM reporting_jobs ORDER BY 1,2"):
        print(r)
    print(con.execute("SELECT count(*), max(fim) FROM reporting_relatorios").fetchone())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--criar-jobs", action="store_true")
    p.add_argument("--baixar", action="store_true")
    p.add_argument("--status", action="store_true")
    p.add_argument("--canal")
    a = p.parse_args()
    with conectar() as con:
        migrar(con)
        if a.criar_jobs:
            criar_jobs(con, a.canal)
        if a.baixar:
            baixar(con, a.canal)
        if a.status:
            status(con, a.canal)
        if not (a.criar_jobs or a.baixar or a.status):
            p.print_help()


if __name__ == "__main__":
    main()
