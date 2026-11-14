"""YouTube Reporting API: jobs, download e gravação de impressões/CTR e origem de tráfego.

Uso (a partir de tools/):
  .venv/bin/python reporting.py --criar-jobs     # cria (idempotente) os jobs que faltam e registra no banco os que já existem na API
  .venv/bin/python reporting.py --baixar         # baixa relatórios novos (paginado) e grava em youtube.alcance_diario
  .venv/bin/python reporting.py --baixar --rebaixar   # baixa de novo TODOS os relatórios ainda disponíveis (corrige gravações antigas)
  .venv/bin/python reporting.py --status         # jobs, relatórios baixados e cobertura de dias por canal
  .venv/bin/python reporting.py --canal X        # limita a um canal
Download diário: tools/rotinas/diaria.sh (06:30) roda `--criar-jobs --baixar`; o fabrica-analytics.timer também chama baixar()
(sem duplicar: cada relatório é gravado 1× por report_id).

Como a API funciona (diagnóstico de 14/11/2026):
- 1 relatório por dia e por job, gerado ~48–72 h depois do dia; o 1º só aparece ~2 dias depois de criar o job e começa no
  dia anterior à criação (jobs de 11/11 → 1º relatório = dia 10/11, gerado na madrugada de 14/11). Não há histórico anterior.
- Cada CSV tem várias linhas por (vídeo, dia, origem): o combined_a1 quebra por aparelho/SO/detalhe da origem e o
  traffic_source_a3 por país/inscrito/detalhe. Até 14/11/2026 o upsert gravava só a ÚLTIMA linha de cada chave (impressões
  e views subcontadas). Agora as linhas são agregadas antes de gravar: impressões somadas, CTR = cliques/impressões
  (cliques = impressões × CTR de cada linha), views e minutos somados.
- `reports.list` é paginado (o código antigo lia só a 1ª página: quebraria depois de ~uns meses de relatórios).
- Total por vídeo/dia: use fonte 'channel_reach_basic_a1' (origem ''); por origem: 'channel_reach_combined_a1'.
Nunca imprime token.
"""
import argparse
import csv
import io
import os
from collections import defaultdict

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


def criar_jobs(con, so=None, verboso=True):
    for slug in canais_com_token(con, so):
        try:
            api = build("youtubereporting", "v1", credentials=creds_for(slug))
            existentes = {j["reportTypeId"]: j["id"] for j in api.jobs().list().execute().get("jobs", [])}
        except Exception as e:  # noqa: BLE001
            print(f"- {slug}: [aviso] jobs.list falhou: {type(e).__name__}: {str(e)[:160]}")
            continue
        for tipo in TIPOS:
            if tipo in existentes:
                jid, novo = existentes[tipo], False
            else:
                jid, novo = api.jobs().create(body={"reportTypeId": tipo, "name": f"fabrica-{slug}-{tipo}"}).execute()["id"], True
            ja = con.execute("SELECT job_id FROM reporting_jobs WHERE canal_slug=%s AND tipo=%s", (slug, tipo)).fetchone()
            con.execute("INSERT INTO reporting_jobs (canal_slug,tipo,job_id) VALUES (%s,%s,%s)"
                        " ON CONFLICT (canal_slug,tipo) DO UPDATE SET job_id=EXCLUDED.job_id", (slug, tipo, jid))
            if verboso or novo or not ja or ja[0] != jid:
                estado = "CRIADO" if novo else ("já existia (registrado agora no banco)" if not ja or ja[0] != jid else "já existia")
                print(f"- {slug}: {tipo} {estado}")


def num(x, f=float):
    return f(x) if x not in ("", None) else None


def agregar(tipo, texto):
    """CSV → {(video, data, origem): {...}} somando as linhas de cada chave."""
    acc = defaultdict(lambda: {"imp": 0, "cliques": 0.0, "views": 0, "min": 0.0, "tem_imp": False, "tem_views": False})
    for r in csv.DictReader(io.StringIO(texto)):
        data = f"{r['date'][:4]}-{r['date'][4:6]}-{r['date'][6:]}"
        a = acc[(r.get("video_id") or "", data, r.get("traffic_source_type") or "")]
        if tipo.startswith("channel_reach"):
            imp, ctr = num(r.get("video_thumbnail_impressions"), int), num(r.get("video_thumbnail_impressions_ctr"))
            if imp is not None:
                a["imp"] += imp
                a["cliques"] += imp * (ctr or 0)
                a["tem_imp"] = True
        else:
            v, m = num(r.get("views"), int), num(r.get("watch_time_minutes"))
            a["views"] += v or 0
            a["min"] += m or 0
            a["tem_views"] = True
    return acc


def gravar(con, slug, tipo, texto):
    acc = agregar(tipo, texto)
    datas = sorted({k[1] for k in acc})
    if datas:  # regravação limpa do(s) dia(s) do relatório nesta fonte
        con.execute("DELETE FROM alcance_diario WHERE canal_slug=%s AND fonte=%s AND data = ANY(%s::date[])", (slug, tipo, datas))
    for (vid, data, origem), a in acc.items():
        if tipo.startswith("channel_reach"):
            imp = a["imp"] if a["tem_imp"] else None
            ctr = (a["cliques"] / a["imp"]) if a["imp"] else (0 if a["tem_imp"] else None)
            views = mins = None
        else:
            imp = ctr = None
            views, mins = (a["views"], round(a["min"], 2)) if a["tem_views"] else (None, None)
        con.execute(
            "INSERT INTO alcance_diario (canal_slug,video_id,data,origem,impressoes,ctr,views,minutos,fonte)"
            " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (canal_slug,video_id,data,origem,fonte) DO UPDATE SET"
            " impressoes=EXCLUDED.impressoes, ctr=EXCLUDED.ctr, views=EXCLUDED.views, minutos=EXCLUDED.minutos, baixado_em=now()",
            (slug, vid, data, origem, imp, ctr, views, mins, tipo))
    return len(acc)


def listar_relatorios(api, jid):
    reps, tok = [], None
    while True:
        r = api.jobs().reports().list(jobId=jid, pageSize=100, pageToken=tok).execute()
        reps += r.get("reports", [])
        tok = r.get("nextPageToken")
        if not tok:
            return reps


def baixar(con, so=None, rebaixar=False):
    for slug in canais_com_token(con, so):
        try:
            creds = creds_for(slug)
            api = build("youtubereporting", "v1", credentials=creds)
        except Exception as e:  # noqa: BLE001
            print(f"- {slug}: [aviso] sem acesso à Reporting API: {type(e).__name__}: {str(e)[:160]}")
            continue
        for tipo, jid in con.execute("SELECT tipo,job_id FROM reporting_jobs WHERE canal_slug=%s", (slug,)).fetchall():
            vistos = set() if rebaixar else {r[0] for r in con.execute(
                "SELECT report_id FROM reporting_relatorios WHERE canal_slug=%s AND tipo=%s", (slug, tipo))}
            reps = listar_relatorios(api, jid)
            novos = [r for r in reps if r["id"] not in vistos]
            for r in sorted(novos, key=lambda r: (r["startTime"], r.get("createTime", ""))):
                resp = requests.get(r["downloadUrl"], headers={"Authorization": f"Bearer {creds.token}"}, timeout=120)
                resp.raise_for_status()
                n = gravar(con, slug, tipo, resp.text)
                con.execute("INSERT INTO reporting_relatorios (report_id,canal_slug,tipo,inicio,fim,linhas) VALUES (%s,%s,%s,%s,%s,%s)"
                            " ON CONFLICT (report_id) DO UPDATE SET linhas=EXCLUDED.linhas, baixado_em=now()",
                            (r["id"], slug, tipo, r["startTime"][:10], r["endTime"][:10], n))
            print(f"- {slug}: {tipo}: {len(reps)} relatórios no job, {len(novos)} {'rebaixados' if rebaixar else 'novos'}")


def status(con, so=None):
    for r in con.execute("SELECT canal_slug,tipo,job_id,criado_em::date FROM reporting_jobs ORDER BY 1,2"):
        print(r)
    print("relatórios baixados / último dia:", con.execute("SELECT count(*), max(inicio) FROM reporting_relatorios").fetchone())
    for r in con.execute("SELECT canal_slug, count(DISTINCT data), min(data), max(data), sum(impressoes) FROM alcance_diario"
                         " WHERE fonte='channel_reach_basic_a1' GROUP BY 1 ORDER BY 1"):
        print("cobertura (basic_a1):", r)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--criar-jobs", action="store_true")
    p.add_argument("--baixar", action="store_true")
    p.add_argument("--rebaixar", action="store_true", help="com --baixar: baixa de novo todos os relatórios disponíveis")
    p.add_argument("--status", action="store_true")
    p.add_argument("--canal")
    a = p.parse_args()
    with conectar() as con:
        migrar(con)
        if a.criar_jobs:
            criar_jobs(con, a.canal, verboso=not a.baixar)
        if a.baixar:
            baixar(con, a.canal, a.rebaixar)
        if a.status:
            status(con, a.canal)
        if not (a.criar_jobs or a.baixar or a.status):
            p.print_help()


if __name__ == "__main__":
    main()
