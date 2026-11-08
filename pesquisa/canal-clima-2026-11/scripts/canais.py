"""Uploads dos canais do nicho (Data API, só leitura): views/mês, mediana, cadência, 1º vídeo, % shorts.
Saída: dados/canais_nicho.json"""
import json, os, sys, statistics as stt, datetime as dt
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEL = {  # id: (idioma, guarda-chuva)
 "UCfwuvBi-qNhYTeYg-zAtR-g": ("pt", "noticia-clima"), "UCfM8cvYaVCsz9NgyKMRVFNw": ("pt", "explicado"), "UCQZJSIL-0P-eL25pwLLbJFg": ("pt", "brasil-mapas"),
 "UCKMAIDE14obWuMayCz98ecA": ("pt", "noticia-clima"), "UCcK9yDz5INb1Q9Tw82ICeVQ": ("pt", "desastre-reconstruido"), "UC3M1FG__5Lb4i0R_ykhsZlQ": ("pt", "desastre-reconstruido"),
 "UCb2Jwl0gpeSq4bN1MyaiopA": ("pt", "compilado"), "UCyEr1_3pP7tkD-XNddOnN0w": ("pt", "fenomenos"), "UC2qnXFBVIlWOyHBHkn23_Bw": ("pt", "noticia-clima"),
 "UCg7fLHKsksWKtl-zOprMAeQ": ("pt", "noticia-clima"), "UCSTfMn3kpQ8dhirVVsecJfQ": ("pt", "meteorologia"), "UCB_Gxy3rG-REFVowVbjkulQ": ("pt", "fenomenos"),
 "UC734965gYfz7LPY2QQ66cVg": ("pt", "brasil-mapas"), "UCLNUQhd4SfWog0b4TAqtjkw": ("pt", "brasil-mapas"), "UCE7V35xEIapyI9guYtALHYg": ("pt", "brasil-mapas"),
 "UCIIrkrx9g0a0mmZEgUYearg": ("pt", "noticia-clima"), "UCvYEtxFZ8dCPwu6sxuonFdA": ("pt", "noticia-clima"), "UCf6K03zCykuTKYsu56iFC0w": ("pt", "noticia-clima"),
 "UCqcXds5a4BGxCPBfJjE806g": ("pt", "noticia-clima"), "UCX06w7siSbDfixndVolFlbQ": ("pt", "fenomenos"), "UCluo4IOs5C5ybSGWEf4XsMw": ("pt", "storm-chaser"),
 "UCUq1B_mpEgWiNujdZkY0x5w": ("en", "explicado"), "UCN6XxorahzAiDNyRnI1of2g": ("en", "desastre-reconstruido"), "UCqWxNlxcSBoM-cf1VOaG3UA": ("en", "desastre-reconstruido"),
 "UCvv0Zy25K_9wj_YyP4nDX3g": ("en", "desastre-reconstruido"), "UClEH97oWJjrm1PX6ZCEcafQ": ("en", "desastre-reconstruido"), "UCWBtLCE-BnzZx3DneqDiXWQ": ("en", "explicado"),
 "UC3lv_rnB5LgXW8t9sUH3hXw": ("en", "desastre-reconstruido"), "UCSn-jzJf_LMbT8bAfHj92_Q": ("en", "noticia-clima"), "UCCtYdNBm-8C_wZk0n6u8VnQ": ("en", "tornado-reconstruido"),
 "UCuer9Sw2UAD5LWZpVXbgKTA": ("en", "tornado-reconstruido"), "UCLfN3U2O0sEYabjo2lxIttw": ("en", "tornado-reconstruido"), "UCp9eTbnNSBFIFEdCSmPTrtw": ("en", "explicado"),
 "UCD9UIa4WDqVmJiMsQ4UMM0A": ("en", "desastre-reconstruido"), "UCvQxzqlRkeBX_jEFMjlLSAA": ("en", "noticia-clima"), "UCRPO5TnyXFk99NMfxFy_AZw": ("en", "explicado"),
 "UCNXvxXpDJXp-mZu3pFMzYHQ": ("en", "clima-ciencia"), "UCZTme3vf6kXmXfSsIr06lvQ": ("en", "desastre-reconstruido"), "UCpxYSWgxVt3Pyn1ovXsGQ0g": ("en", "clima-ciencia"),
 "UCrkONla60pQPsppl7PPDHyQ": ("es", "explicado"), "UCO6osb24LgRFhBIkAWEZdEQ": ("es", "explicado"), "UCL6UGqm6qEmQPa4TMngYENg": ("es", "meteorologia"),
 "UCRJuF3MHwrilm3coZcRRyIg": ("es", "meteorologia"), "UCcWOL02JEjNmxcU6UVDqEPg": ("es", "brasil-mapas"), "UC8OtZ6Q1Y7EtMyI6UVDaGww": ("es", "noticia-clima"),
 "UCyJxucjlRm1fxTi9Un2V2-g": ("hi", "desastre-reconstruido"), "UCXoi9MAKmS_T4Z6UUDGS-Ug": ("hi", "desastre-reconstruido"), "UCqgJ5kAAFspmgUB6zW27rNQ": ("hi", "desastre-reconstruido"),
}
hoje = dt.date(2026, 11, 8)
yt = yt_client(); un = 0; out = {}
info = {}
for g in chunks(list(SEL)):
    for it in yt.channels().list(part="snippet,statistics,contentDetails", id=",".join(g)).execute().get("items", []):
        info[it["id"]] = it
    un += 1
for cid, (lang, guarda) in SEL.items():
    it = info.get(cid)
    if not it: continue
    sn, st = it["snippet"], it["statistics"]; nv = int(st.get("videoCount", 0))
    maxp = 4 if nv <= 200 else 2
    ids, tok, p = [], None, 0
    while p < maxp:
        r = yt.playlistItems().list(part="contentDetails", playlistId=it["contentDetails"]["relatedPlaylists"]["uploads"], maxResults=50, pageToken=tok).execute()
        un += 1; p += 1; ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]; tok = r.get("nextPageToken")
        if not tok: break
    vs = []
    for g in chunks(ids):
        for v in yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(g)).execute().get("items", []):
            d = v["contentDetails"].get("duration") or "PT0S"
            vs.append({"id": v["id"], "t": v["snippet"]["title"], "pub": v["snippet"]["publishedAt"][:10], "views": int(v["statistics"].get("viewCount", 0)),
                       "dur": segundos(d) if "D" not in d else 99999})
        un += 1
    completo = tok is None
    longos = [v for v in vs if v["dur"] > 180]; shorts = [v for v in vs if v["dur"] <= 180]
    l90 = [v for v in longos if (hoje - dt.date.fromisoformat(v["pub"])).days <= 90]
    s90 = [v for v in shorts if (hoje - dt.date.fromisoformat(v["pub"])).days <= 90]
    primeiro = min((v["pub"] for v in vs), default=None) if completo else None
    idade = (hoje - dt.date.fromisoformat(primeiro or sn["publishedAt"][:10])).days
    views = int(st.get("viewCount", 0))
    vpm = views / max(idade, 1) * 30 if idade < 365 else (sum(v["views"] for v in l90 + s90) / 3)
    out[cid] = {"nome": sn["title"], "handle": sn.get("customUrl"), "lang": lang, "guarda": guarda, "pais": sn.get("country"), "criado": sn["publishedAt"][:10],
                "primeiro_video": primeiro, "idade_dias": idade, "inscritos": int(st.get("subscriberCount", 0) or 0), "views": views, "n_videos": nv,
                "views_mes": int(vpm), "longos_90d": len(l90), "shorts_90d": len(s90), "mediana_longos": int(stt.median([v["views"] for v in longos])) if longos else 0,
                "mediana_longos_90d": int(stt.median([v["views"] for v in l90])) if l90 else 0, "dur_media_longos_min": round(stt.mean([v["dur"] for v in longos]) / 60, 1) if longos else 0,
                "top": sorted(vs, key=lambda v: -v["views"])[:5], "flops": sorted(longos, key=lambda v: v["views"])[:3]}
json.dump(out, open(os.path.join(BASE, "dados", "canais_nicho.json"), "w"), ensure_ascii=False, indent=1)
print(len(out), "canais,", un, "unidades")
for c in sorted(out.values(), key=lambda c: (c["lang"], -c["views_mes"])):
    print(f'{c["lang"]} {c["guarda"][:14]:14} {c["nome"][:24]:24} 1º {c["primeiro_video"] or "~"+c["criado"]} insc {c["inscritos"]:>8,} v/mês {c["views_mes"]:>10,} L90 {c["longos_90d"]:>3} S90 {c["shorts_90d"]:>3} medL {c["mediana_longos"]:>8,} medL90 {c["mediana_longos_90d"]:>8,} dur {c["dur_media_longos_min"]:>4} | {c["top"][0]["views"]:>9,} {c["top"][0]["t"][:55]}')
