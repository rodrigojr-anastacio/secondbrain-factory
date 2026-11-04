"""Garimpo semanal: canais NOVOS, com poucos vídeos e muita tração (demanda comprovada).

Uso: ~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/tools/trends.py [--dias 30] [--top 15]
Lê as buscas de pesquisa/trend_seeds.txt (uma por linha; edite à vontade).
Salva em pesquisa/tendencias/AAAA-MM-DD.json e .md e mantém o histórico em pesquisa/trends_state.json.
Cota: cada busca custa 100 unidades (limite de 10 mil por dia no projeto); o resto custa ~1 unidade.
"""
import argparse
import datetime as dt
import json
import os
import re

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from _paths import PESQUISA, TENDENCIAS, TOKENS
from db import Jsonb, tentar

OUT = TENDENCIAS
STATE = os.path.join(PESQUISA, "trends_state.json")

# Critérios calibrados no "History in Minutes" (7 semanas, 8 vídeos, ~175 mil views por vídeo)
MAX_IDADE_DIAS = 120
MAX_VIDEOS = 20
MIN_MEDIA_VIEWS = 20_000


def yt_client():
    path = os.path.join(TOKENS, "lotr-fr.json")
    creds = Credentials.from_authorized_user_file(path)
    if not creds.valid:
        creds.refresh(Request())
        with open(path, "w") as f:
            f.write(creds.to_json())
    return build("youtube", "v3", credentials=creds)


def segundos(iso):
    h, m, s = (int(x) if x else 0 for x in re.match(r"P(?:\d+D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso).groups())
    return h * 3600 + m * 60 + s


def chunks(xs, n=50):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=30, help="janela de publicação dos vídeos buscados")
    ap.add_argument("--top", type=int, default=15)
    ap.add_argument("--seeds", default=os.path.join(PESQUISA, "trend_seeds.txt"))
    a = ap.parse_args()
    yt = yt_client()
    hoje = dt.datetime.now(dt.timezone.utc)
    desde = (hoje - dt.timedelta(days=a.dias)).strftime("%Y-%m-%dT%H:%M:%SZ")

    seeds = [l.strip() for l in open(a.seeds) if l.strip() and not l.startswith("#")]
    achados = {}  # channelId -> lista de buscas que o trouxeram
    for q in seeds:
        for dur in ("medium", "long"):  # sem Shorts
            r = yt.search().list(part="snippet", q=q, type="video", order="viewCount", publishedAfter=desde,
                                 relevanceLanguage="en", videoDuration=dur, maxResults=50).execute()
            for it in r.get("items", []):
                achados.setdefault(it["snippet"]["channelId"], set()).add(q)

    # 1) filtro barato pelos números do canal
    pre = []
    for grupo in chunks(list(achados)):
        for ch in yt.channels().list(part="snippet,statistics,contentDetails", id=",".join(grupo)).execute().get("items", []):
            st = ch["statistics"]
            n, views = int(st.get("videoCount", 0)), int(st.get("viewCount", 0))
            if n and n <= MAX_VIDEOS and views / n >= MIN_MEDIA_VIEWS:
                pre.append(ch)

    # 2) vídeos de cada um: idade real (1º upload), idioma e proporção de Shorts
    cand = []
    for ch in pre:
        st, sn = ch["statistics"], ch["snippet"]
        ids = [i["contentDetails"]["videoId"] for i in yt.playlistItems().list(
            part="contentDetails", playlistId=ch["contentDetails"]["relatedPlaylists"]["uploads"], maxResults=50).execute()["items"]]
        vids = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids)).execute()["items"] if ids else []
        if not vids:
            continue
        primeiro = min(v["snippet"]["publishedAt"] for v in vids)
        idade = (hoje - dt.datetime.fromisoformat(primeiro.replace("Z", "+00:00"))).days
        titulos = [v["snippet"]["title"] for v in vids]
        nao_latino = sum(bool(re.search(r"[^\x00-\u024F\u2000-\u2BFF\U0001F000-\U0001FAFF]", t)) for t in titulos) / len(titulos)
        audio = [v["snippet"].get("defaultAudioLanguage", "") for v in vids if v["snippet"].get("defaultAudioLanguage")]
        nao_en = audio and sum(not a.startswith("en") for a in audio) / len(audio) > 0.5
        shorts = sum(segundos(v["contentDetails"]["duration"]) <= 75 for v in vids) / len(vids)
        if idade > MAX_IDADE_DIAS or nao_latino > 0.3 or nao_en or shorts > 0.5:
            continue
        n, views = int(st.get("videoCount", 0)), int(st.get("viewCount", 0))
        subs = int(st.get("subscriberCount", 0) or 0)
        cand.append({
            "id": ch["id"], "titulo": sn["title"], "url": f"https://www.youtube.com/channel/{ch['id']}",
            "pais": sn.get("country"), "criado": sn["publishedAt"][:10], "primeiro_video": primeiro[:10], "idade_dias": idade,
            "videos": n, "views": views, "inscritos": subs, "media_views": views // n,
            "views_por_inscrito": round(views / subs, 1) if subs else None,
            "descricao": sn.get("description", "")[:300], "buscas": sorted(achados[ch["id"]]),
            "videos_lista": sorted(({
                "id": v["id"], "titulo": v["snippet"]["title"], "publicado": v["snippet"]["publishedAt"][:10],
                "duracao_min": round(segundos(v["contentDetails"]["duration"]) / 60, 1),
                "views": int(v["statistics"].get("viewCount", 0)),
                "thumb": v["snippet"]["thumbnails"].get("maxres", v["snippet"]["thumbnails"].get("high", {})).get("url"),
                "url": f"https://www.youtube.com/watch?v={v['id']}",
            } for v in vids), key=lambda v: v["views"], reverse=True),
        })

    # tração por dia de vida (desde o 1º vídeo): favorece quem cresce rápido
    for c in cand:
        c["score"] = round(c["views"] / max(c["idade_dias"], 7))
    cand.sort(key=lambda c: c["score"], reverse=True)
    cand = cand[: a.top]

    estado = json.load(open(STATE)) if os.path.exists(STATE) else {}
    for c in cand:
        ant = estado.get(c["id"])
        c["novo_no_radar"] = ant is None
        c["crescimento_views_desde_ultimo"] = c["views"] - ant["views"] if ant else None
        estado[c["id"]] = {"titulo": c["titulo"], "views": c["views"], "inscritos": c["inscritos"], "visto_em": hoje.date().isoformat()}
    json.dump(estado, open(STATE, "w"), ensure_ascii=False, indent=1)

    os.makedirs(OUT, exist_ok=True)
    base = os.path.join(OUT, hoje.date().isoformat())
    json.dump({"gerado_em": hoje.isoformat(), "buscas": seeds, "criterios": {
        "max_idade_dias": MAX_IDADE_DIAS, "max_videos": MAX_VIDEOS, "min_media_views": MIN_MEDIA_VIEWS},
        "candidatos": cand}, open(base + ".json", "w"), ensure_ascii=False, indent=1)
    with open(base + ".md", "w") as f:
        f.write(f"# Garimpo de canais novos — {hoje.date()}\n\n{len(achados)} canais vistos em {len(seeds)} buscas; {len(cand)} passaram no filtro.\n\n")
        for c in cand:
            tag = "NOVO" if c["novo_no_radar"] else f"+{c['crescimento_views_desde_ultimo']:,} views desde a última semana"
            f.write(f"## {c['titulo']} ({tag})\n{c['url']} · 1º vídeo {c['primeiro_video']} ({c['idade_dias']} dias) · {c['videos']} vídeos · "
                    f"{c['views']:,} views · {c['inscritos']:,} inscritos · média {c['media_views']:,}/vídeo\n")
            for v in c["videos_lista"][:5]:
                f.write(f"- {v['views']:,} views · {v['duracao_min']} min · {v['titulo']}\n")
            f.write("\n")
    def gravar(con):
        ex = con.execute(
            "INSERT INTO garimpo_execucoes(buscas, criterios, canais_vistos, candidatos, relatorio_md)"
            " VALUES (%s,%s,%s,%s,%s) RETURNING id",
            (Jsonb(seeds), Jsonb({"max_idade_dias": MAX_IDADE_DIAS, "max_videos": MAX_VIDEOS, "min_media_views": MIN_MEDIA_VIEWS}),
             len(achados), len(cand), base + ".md")).fetchone()[0]
        for c in cand:
            con.execute(
                "INSERT INTO garimpo_canais(channel_id, titulo, url, pais, criado, primeiro_video) VALUES (%s,%s,%s,%s,%s,%s)"
                " ON CONFLICT (channel_id) DO UPDATE SET titulo=EXCLUDED.titulo, ultima_vez=now()",
                (c["id"], c["titulo"], c["url"], c["pais"], c["criado"], c["primeiro_video"]))
            con.execute("INSERT INTO garimpo_snapshots VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                        (ex, c["id"], c["videos"], c["views"], c["inscritos"], c["media_views"], c["score"], c["idade_dias"]))
            for v in c["videos_lista"]:
                con.execute(
                    "INSERT INTO garimpo_videos VALUES (%s,%s,%s,%s,%s,%s,%s, now())"
                    " ON CONFLICT (video_id) DO UPDATE SET views=EXCLUDED.views, titulo=EXCLUDED.titulo, atualizado_em=now()",
                    (v["id"], c["id"], v["titulo"], v["publicado"], v["duracao_min"], v["views"], v["thumb"]))
        return ex
    ex = tentar(gravar)
    print(open(base + ".md").read())
    if ex:
        print(f"(gravado no banco: youtube.garimpo_execucoes id={ex})")
    print(f"(json completo: {base}.json)")


if __name__ == "__main__":
    main()
