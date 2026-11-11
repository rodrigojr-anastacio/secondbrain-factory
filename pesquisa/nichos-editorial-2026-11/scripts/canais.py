"""Uploads dos canais do nicho (Data API, só leitura): views/mês, mediana, cadência, 1º vídeo, % shorts.
Saída: dados/canais_nicho.json"""
import json, os, sys, statistics as stt, datetime as dt
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client, segundos, chunks
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEL = {  # id: (idioma, nicho)
 "UCmGSJVG3mCRXVOP4yZrU1Dw": ("en","geo"), "UC9RM-iSvTu1uPJb8X5yp3EQ": ("en","mega"), "UCP5tjEmvPItGyLhmjdwP7Ww": ("en","geo"),
 "UC7-Z34pbJ0ZAOJRmUCEz0Cg": ("en","cidades"), "UCcWOL02JEjNmxcU6UVDqEPg": ("es","cidades"), "UC6n8I1UDTKP1IWjQMg6_TwA": ("en","mega"),
 "UC0woBco6Dgcxt0h8SwyyOmw": ("en","mega"), "UCR1IuLEqb6UEA_zQ81kwXfg": ("en","mega"), "UCwpHKudUkP5tNgmMdexB3ow": ("en","acidentes"),
 "UCoftW9U27KfkNz5jFES7htg": ("en","acidentes"), "UCXIkr0SRTnZO4_QpZozvCCA": ("en","acidentes"), "UCK9xNYXhp2zL4_SIkd1AIEA": ("en","economia"),
 "UC-9b7aDP6ZN0coj9-xFnrtw": ("en","espaco"), "UC-2A6Z4k5-AJBLO_wDA-ZUg": ("es","espaco"), "UCQVKHQydcoIVN6Xfx3-72MQ": ("es","espaco"),
 "UCBMpOoAvVl9T2V6ZavXl9vw": ("en","historia20"), "UCI0YUL57yQ03GmfBYmIw5Ng": ("en","militar"), "UCO4gtSa3rpOutrZ45-OjYyA": ("en","militar"),
 "UC7t63g5TYdhbE8t1Ti-Wa6g": ("en","militar"), "UCTngalO3jl5I3Op885eurfw": ("en","oceano"), "UCqXlPGw_s8Mr7YOSVZYjWOg": ("en","oceano"),
 "UCrGua2D39Yktjh9b7jINuOw": ("es","oceano"), "UCdZhRs4wM7SgVXoP9WSW2yA": ("en","acidentes"), "UCfDPwaVu8uF1_C4_uy6ntVw": ("en","acidentes"),
 "UCoZ6gJoTzo1ptnhrbFtWTSw": ("es","acidentes"), "UCILe99sw_kJ4NvcFrnrlq9w": ("es","mega"), "UCZXwKwfLqAtL97b_b_fGWiQ": ("es","mega"),
 "UCsGmo5M9LX8GJ-6CsT8xDpw": ("es","cidades"), "UCdyNZcgs1ZcFFM1cy4g04og": ("en","economia"), "UCEPS4Oc-5EqlOp8IlfUhUZQ": ("en","geo"),
 "UC850JkAjgLpH4MuPzd2yawQ": ("en","geo"), "UCdYuVMwhxFLc-87sulUbIBg": ("en","geo"), "UC51z1Rn0zevAK9xWpfMg_ZA": ("en","guerrafria"),
 "UCh0CBgDE49V88YG61HcTlBg": ("es","desastre"), "UCG76lqEyDxxARvenKCoOAvQ": ("es","mega"), "UC8DBRONy1P9jw-pHjnwRChQ": ("es","economia"),
 "UCu2Swk671inpyXO6kmZ-ajQ": ("en","escala"), "UCJw3_4gpD9dicj1ZGr5wdHQ": ("en","oceano"), "UCB389sx-L4Jiy79-K0kGUiA": ("en","acidentes"),
 "UCMOqf8ab-42UUQIdVoKwjlQ": ("en","mega"), "UCgNg3vwj3xt7QOrcIDaHdFg": ("en","economia"), "UCZ4AMrDcNrfy3X6nsU8-rPg": ("en","economia"),
 "UCfCNU6LWB66VR48V58d2KOg": ("en","acidentes"), "UC1ZBQ-F-yktYD4m5AzM6pww": ("en","militar"), "UC1pACXxUjIWNDuU-kY1OX0Q": ("en","espaco"),
 "UClZbmi9JzfnB2CEb0fG8iew": ("en","espaco"), "UC5q902RpdLkzhzmm8kGvQXg": ("es","espaco"), "UCD9UIa4WDqVmJiMsQ4UMM0A": ("en","espaco"),
 "UCK6geQoP0RNg9G2KQB1JlAg": ("en","espaco"), "UCWwCEHGxwFkf2Zf36mlEAug": ("en","historia20"), "UCeMcDx6-rOq_RlKSPehk2tQ": ("en","espaco"),
 "UCAVxoa11gRHcit9_onvTkMQ": ("en","oceano"), "UCwvpTmocCcxuXX1_XbB34Tg": ("es","oceano"), "UCjKZXiXPwIhkz5trHANMgXw": ("es","oceano"),
 "UCBodi-kVExpIOrEaVbPIS0g": ("es","acidentes"), "UCXaTgv15SFzrrks_sPLMdhg": ("es","mega"), "UCfM8cvYaVCsz9NgyKMRVFNw": ("pt","geo"),
 "UCLNUQhd4SfWog0b4TAqtjkw": ("pt","geo"), "UCQfm2EMu9H6lXtUxkqKV7Kw": ("en","militar"), "UCe9imMhDp6Kn3dn75mzUUZw": ("en","natureza"),
 "UCpw_I21AoF3N6Dqm3LLY9bw": ("en","natureza"), "UCKjRbFbTtetc-bQ5sztC4aA": ("en","natureza"), "UCnIpkOAIMk5pfhHxIIuwa1g": ("es","natureza"),
 "UCSt2qok-JJLVi_jOdn-AjGw": ("en","geo"), "UCJBtZsbKrhEJh09pnqYAB-g": ("en","historia20"), "UCZXShYiBJlahi8mCNiU3XBg": ("en","historia20"),
 "UCnvv-sfvCb0gBkb0LwpjDog": ("en","acidentes"), "UC_9A1c12YJXjADklUU2MVug": ("en","acidentes"), "UCZd9f77kiWs7m3uH3Y3NzNA": ("en","espaco"),
 "UCN6XxorahzAiDNyRnI1of2g": ("en","desastre"), "UCUq1B_mpEgWiNujdZkY0x5w": ("en","desastre"), "UC1dXACOtLPqYnGUmaSo2e8g": ("en","escala"),
}
hoje = dt.date(2026, 11, 11)
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
    print(f'{c["lang"]} {c["guarda"][:10]:10} {c["nome"][:24]:24} 1º {c["primeiro_video"] or "~"+c["criado"]} insc {c["inscritos"]:>8,} v/mês {c["views_mes"]:>10,} L90 {c["longos_90d"]:>3} S90 {c["shorts_90d"]:>3} medL {c["mediana_longos"]:>8,} medL90 {c["mediana_longos_90d"]:>8,} dur {c["dur_media_longos_min"]:>4} | {c["top"][0]["views"]:>9,} {c["top"][0]["t"][:55]}')
