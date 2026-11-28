"""Scanner de oportunidades (28/11/2026): canais NOVOS com tração, qualquer nicho/idioma.

Descoberta grátis: busca do YouTube via yt-dlp + WARP (filtro "este mês", ordenado por views).
Enriquecimento barato: Data API videos.list/channels.list/playlistItems (1 unidade por chamada).
Regra de ouro: 1º vídeo >= 2026-07-28, <= 25 vídeos (marca >20), tração.

Uso: python scan.py <arquivo_queries.tsv> <saida.json> [--fim 120] [--min-views 40000]
TSV: idioma<TAB>nicho<TAB>query
"""
import argparse, json, os, re, statistics, subprocess, sys, datetime as dt
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks  # noqa

PROXY = "socks5://127.0.0.1:40000"
NODE = os.path.expanduser("~/.hermes/tools/node-26.12.1-linux-x64/bin/node")
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
CORTE = dt.date(2026, 7, 28)
SP = {"mes": "CAMSBAgEEAE%3D", "ano": "CAMSBAgFEAE%3D", "semana": "CAMSBAgDEAE%3D"}
CACHE = os.path.expanduser("~/cache/oport/canais_cache.json")


def busca(q, fim, janela):
    url = "https://www.youtube.com/results?search_query=" + q.replace(" ", "+") + "&sp=" + SP[janela]
    cmd = [YTDLP, "--proxy", PROXY, "--js-runtimes", f"node:{NODE}", "--no-warnings",
           "--flat-playlist", "--playlist-end", str(fim), "-J", url]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        d = json.loads(r.stdout)
        return [(e["id"], e.get("view_count") or 0, e.get("duration") or 0, e.get("title"))
                for e in d.get("entries", []) if e.get("id")]
    except Exception as ex:  # noqa
        print("falha busca", q, ex, file=sys.stderr)
        return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("queries"); ap.add_argument("saida")
    ap.add_argument("--fim", type=int, default=100)
    ap.add_argument("--min-views", type=int, default=40000)
    ap.add_argument("--janela", default="mes")
    a = ap.parse_args()
    linhas = [l.rstrip("\n").split("\t") for l in open(a.queries) if l.strip() and not l.startswith("#")]
    vids = {}  # id -> (views, dur, title, [(lang,nicho,q)])
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(lambda l: (l, busca(l[2], a.fim, a.janela)), linhas))
    for l, es in res:
        print(f"{l[0]} | {l[2]} -> {len(es)}", file=sys.stderr)
        for vid, v, d, t in es:
            if v >= a.min_views and (d or 999) > 180:
                vids.setdefault(vid, [v, d, t, []])[3].append(tuple(l))
    yt = yt_client()
    # canal de cada vídeo
    vid2ch = {}
    for ch in chunks(list(vids)):
        r = yt.videos().list(part="snippet", id=",".join(ch), maxResults=50).execute()
        for it in r["items"]:
            vid2ch[it["id"]] = it["snippet"]["channelId"]
    canais = {}
    for vid, ch in vid2ch.items():
        canais.setdefault(ch, []).append(vid)
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    info = {}
    novos = [c for c in canais if c not in cache]
    for ch in chunks(novos):
        r = yt.channels().list(part="snippet,statistics,contentDetails", id=",".join(ch), maxResults=50).execute()
        for it in r["items"]:
            st = it["statistics"]
            cache[it["id"]] = {"titulo": it["snippet"]["title"], "criado": it["snippet"]["publishedAt"][:10],
                               "pais": it["snippet"].get("country"), "handle": it["snippet"].get("customUrl"),
                               "videos": int(st.get("videoCount", 0)), "views": int(st.get("viewCount", 0)),
                               "inscritos": int(st.get("subscriberCount", 0) or 0),
                               "uploads": it["contentDetails"]["relatedPlaylists"]["uploads"]}
    cands = []
    for c in canais:
        i = cache.get(c)
        if not i:
            continue
        if i["videos"] <= 30 and i["views"] >= 200000:
            cands.append(c)
    out = []
    for c in cands:
        i = cache[c]
        if "lista" not in i:
            try:
                r = yt.playlistItems().list(part="contentDetails", playlistId=i["uploads"], maxResults=50).execute()
                ids = [x["contentDetails"]["videoId"] for x in r["items"]]
                vs = []
                for ch in chunks(ids):
                    rr = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ch)).execute()
                    for it in rr["items"]:
                        vs.append({"id": it["id"], "t": it["snippet"]["title"], "pub": it["snippet"]["publishedAt"][:10],
                                   "views": int(it["statistics"].get("viewCount", 0)),
                                   "dur": segundos(it["contentDetails"]["duration"]),
                                   "lang": it["snippet"].get("defaultAudioLanguage") or it["snippet"].get("defaultLanguage")})
                i["lista"] = vs
            except Exception as ex:  # noqa
                print("falha lista", c, ex, file=sys.stderr); continue
        vs = i["lista"]
        if not vs:
            continue
        primeiro = min(v["pub"] for v in vs)
        longos = [v for v in vs if v["dur"] > 180]
        base = longos or vs
        views = sorted(v["views"] for v in base)
        melhor = max(base, key=lambda v: v["views"])
        idade = max(1, (dt.date(2026, 11, 28) - dt.date.fromisoformat(primeiro)).days)
        tot = sum(v["views"] for v in vs)
        out.append({"channel_id": c, **{k: i[k] for k in ("titulo", "handle", "criado", "pais", "videos", "views", "inscritos")},
                    "primeiro_video": primeiro, "idade_dias": idade, "n_longos": len(longos), "n_curtos": len(vs) - len(longos),
                    "mediana": int(statistics.median(views)), "melhor": {k: melhor[k] for k in ("id", "t", "views", "dur", "pub")},
                    "views_mes": int(tot / idade * 30), "dur_media_min": round(statistics.mean(v["dur"] for v in base) / 60, 1),
                    "lang": statistics.mode([v["lang"] for v in vs if v["lang"]] or ["?"]),
                    "titulos": [v["t"] for v in sorted(base, key=lambda v: -v["views"])[:6]],
                    "ok_regra": primeiro >= CORTE.isoformat() and i["videos"] <= 20,
                    "achado_por": sorted({x for vid in canais[c] for x in [f"{q[0]}:{q[1]}" for q in vids[vid][3]]})})
    json.dump(cache, open(CACHE, "w"))
    out.sort(key=lambda x: -x["views"])
    json.dump(out, open(a.saida, "w"), ensure_ascii=False, indent=1)
    print(f"videos>=min: {len(vids)} canais: {len(canais)} cands: {len(cands)} regra_ok: {sum(o['ok_regra'] for o in out)}", file=sys.stderr)


if __name__ == "__main__":
    main()
