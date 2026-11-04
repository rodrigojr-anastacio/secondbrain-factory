"""Concorrência: canais com título na fórmula (qualquer idioma) achados nas buscas + canais es/pt/fr/de do dados.json anterior.
API (só leitura): channels.list (1 un/50), playlistItems (1 un/página de 50, até MAX_PAGES), videos.list (1 un/50).
Saída: dados/canais_api.json"""
import json, os, sys, collections, statistics, datetime as dt
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from trends import yt_client, segundos, chunks
from comum import FORMULA_RE, temas, em_minutos, idioma, formula
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BASE)
MAX_PAGES = int(os.environ.get("MAX_PAGES", "2"))
cand = set()
for fn in ("busca.jsonl", "busca_clones.jsonl"):
    for l in open(os.path.join(BASE, "dados", fn)):
        b = json.loads(l); t = b.get("title") or ""
        if b.get("channel_id") and (b.get("duration") or 0) >= 240 and any(r.search(t) for r in FORMULA_RE.values()) and (temas(t) or em_minutos(t)):
            cand.add(b["channel_id"])
ant = json.load(open(os.path.join(ROOT, "dados.json")))["canais"]
for c in ant.values():
    cand.add(c["id"])
yt = yt_client(); un = 0
chs = {}
for g in chunks(sorted(cand)):
    for it in yt.channels().list(part="snippet,statistics,contentDetails", id=",".join(g), maxResults=50).execute().get("items", []):
        sn, st = it["snippet"], it["statistics"]
        chs[it["id"]] = {"id": it["id"], "nome": sn["title"], "handle": sn.get("customUrl"), "criado": sn["publishedAt"][:10], "pais": sn.get("country"),
                         "lang_canal": sn.get("defaultLanguage"), "views": int(st.get("viewCount", 0)), "inscritos": int(st.get("subscriberCount", 0)),
                         "n_videos": int(st.get("videoCount", 0)), "uploads": it["contentDetails"]["relatedPlaylists"]["uploads"], "antigo": it["id"] in ant}
    un += 1
hoje = dt.date(2026, 11, 4)
for c in chs.values():
    ids, tok, pages = [], None, 0
    while pages < MAX_PAGES:
        try:
            r = yt.playlistItems().list(part="contentDetails", playlistId=c["uploads"], maxResults=50, pageToken=tok).execute()
        except Exception as e:
            print("erro uploads", c["nome"], str(e)[:80], file=sys.stderr); break
        un += 1; pages += 1
        ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
        tok = r.get("nextPageToken")
        if not tok: break
    vids = []
    for g in chunks(ids):
        for it in yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(g)).execute().get("items", []):
            d = it["contentDetails"].get("duration")
            vids.append({"id": it["id"], "titulo": it["snippet"]["title"], "pub": it["snippet"]["publishedAt"][:10], "views": int(it["statistics"].get("viewCount", 0)),
                         "dur_s": segundos(d) if d else 0, "audio": it["snippet"].get("defaultAudioLanguage"), "lang": it["snippet"].get("defaultLanguage")})
        un += 1
    c["lista_completa"] = tok is None
    c["videos"] = vids
print("canais:", len(chs), "unidades:", un, file=sys.stderr)
json.dump(chs, open(os.path.join(BASE, "dados/canais_api.json"), "w"), ensure_ascii=False)
