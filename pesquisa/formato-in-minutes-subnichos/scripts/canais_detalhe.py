"""Detalhe dos canais curados: uploads (playlistItems + videos.list, ~1 unidade por 50), idade real, ritmo, % no formato.
Só leitura; não grava no banco. Saída: dados/canais_detalhe.json e dados/canais_detalhe.csv"""
import csv, json, os, statistics, sys, datetime as dt
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "scripts"))
from trends import yt_client, segundos, chunks
from classificar import forca
MAX_PAGES = 6
yt = yt_client(); un = 0
ch = json.load(open(os.path.join(BASE, "dados/canais_api.json")))
byname = {}
for c in sorted(ch.values(), key=lambda c: c["views"]):
    byname[c["nome"].strip().lower()] = c  # nome repetido: fica o de mais views
hoje = dt.datetime(2026, 11, 4, tzinfo=dt.timezone.utc)
out = []
for r in csv.DictReader(open(os.path.join(BASE, "dados/curadoria.tsv")), delimiter="\t"):
    n = r["nome"].strip().lower()
    c = byname.get(n) or next((c for k, c in byname.items() if k.startswith(n[:12])), None)
    if not c: print("sem id:", r["nome"]); continue
    ids, tok, pages = [], None, 0
    while pages < MAX_PAGES:
        resp = yt.playlistItems().list(part="contentDetails", playlistId=c["uploads"], maxResults=50, pageToken=tok).execute(); un += 1; pages += 1
        ids += [it["contentDetails"]["videoId"] for it in resp.get("items", [])]
        tok = resp.get("nextPageToken")
        if not tok: break
    completo = tok is None
    vids = []
    for g in chunks(ids):
        for it in yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(g)).execute().get("items", []):
            d = it["contentDetails"].get("duration"); s = segundos(d) if d else 0
            vids.append({"id": it["id"], "titulo": it["snippet"]["title"], "pub": it["snippet"]["publishedAt"], "views": int(it["statistics"].get("viewCount", 0)),
                         "dur_s": s, "lang": it["snippet"].get("defaultAudioLanguage"), "forca": forca(it["snippet"]["title"])})
        un += 1
    longos = [v for v in vids if v["dur_s"] > 180]
    for v in vids: v["idade"] = (hoje - dt.datetime.fromisoformat(v["pub"].replace("Z", "+00:00"))).days
    primeiro = max((v["idade"] for v in vids), default=None) if completo else None
    idade_canal = primeiro or (hoje - dt.datetime.fromisoformat(c["criado"].replace("Z", "+00:00"))).days
    fmt = [v for v in longos if v["forca"] in ("alto", "medio")]
    rec30 = [v for v in vids if v["idade"] <= 30]; rec90 = [v for v in vids if v["idade"] <= 90]
    ult10 = sorted(longos, key=lambda v: v["idade"])[:10]
    dur_med = statistics.median([v["dur_s"] for v in longos]) if longos else 0
    vpm = c["views"] / max(idade_canal, 1) * 30
    # views/mês recentes: views dos vídeos publicados nos últimos 90 dias ÷ 3 (subestima a cauda dos antigos)
    vpm_rec = sum(v["views"] for v in rec90) / (min(90, max(idade_canal, 1)) / 30)
    horas_12m = sum(v["views"] * v["dur_s"] for v in longos if v["idade"] <= 365) * 0.4 / 3600
    out.append({**c, "subnicho": r["subnicho"], "lista_completa": completo, "idade_dias": idade_canal, "primeiro_video_dias": primeiro,
                "n_longos": len(longos), "n_formato": len(fmt), "pct_formato": round(100 * len(fmt) / max(len(longos), 1)),
                "mediana_views_formato": int(statistics.median([v["views"] for v in fmt])) if fmt else 0,
                "mediana_views_ult10": int(statistics.median([v["views"] for v in ult10])) if ult10 else 0,
                "videos_30d": len(rec30), "views_videos_30d": sum(v["views"] for v in rec30),
                "videos_90d": len(rec90), "views_mes_vida": int(vpm), "views_mes_recente_90d": int(vpm_rec),
                "dur_mediana_min": round(dur_med / 60, 1), "horas_12m_estim": int(horas_12m),
                "top3": [(v["views"], v["idade"], round(v["dur_s"]/60), v["titulo"][:70], v["id"]) for v in sorted(longos, key=lambda v: -v["views"])[:3]],
                "videos": vids})
    print(f"{c['nome'][:24]:24} idade={idade_canal}d longos={len(longos)} fmt={len(fmt)} vpm={int(vpm)} vpm90={int(vpm_rec)}", file=sys.stderr)
json.dump(out, open(os.path.join(BASE, "dados/canais_detalhe.json"), "w"), ensure_ascii=False, indent=0)
cols = ["subnicho", "nome", "id", "pais", "idade_dias", "primeiro_video_dias", "lista_completa", "n_videos", "n_longos", "n_formato", "pct_formato", "views", "inscritos",
        "views_mes_vida", "views_mes_recente_90d", "videos_30d", "views_videos_30d", "mediana_views_formato", "mediana_views_ult10", "dur_mediana_min", "horas_12m_estim"]
with open(os.path.join(BASE, "dados/canais_detalhe.csv"), "w") as f:
    w = csv.writer(f); w.writerow(cols + ["top3"])
    for o in out: w.writerow([o.get(k) for k in cols] + [" | ".join(f"{t[0]} views, {t[1]}d, {t[2]}min: {t[3]} ({t[4]})" for t in o["top3"])])
print("unidades:", un)
