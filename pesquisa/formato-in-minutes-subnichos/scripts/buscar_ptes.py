"""Concorrência no idioma-alvo (pt-BR e es) para os subnichos candidatos, via yt-dlp + WARP (0 cota). Saída: dados/busca_ptes.jsonl"""
import json, os, sys, subprocess, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
Q = {
 "empresas_negocios": ["a história inteira da coca-cola", "a história inteira da apple em minutos", "a história completa da empresa em minutos",
    "a história inteira da nvidia", "a história inteira do mcdonald's", "história completa da marca", "ascensão e queda da empresa",
    "la historia completa de la empresa en minutos", "toda la historia de coca cola en minutos", "la historia entera de apple"],
 "guerras_especificas": ["a história inteira da guerra do vietnã", "a história inteira da segunda guerra mundial em minutos",
    "a história completa da guerra fria em minutos", "a história inteira da primeira guerra mundial", "a história completa das cruzadas",
    "toda la historia de la guerra de vietnam", "la historia completa de la segunda guerra mundial en minutos"],
 "cidades_regioes": ["a história inteira do rio de janeiro", "a história completa de são paulo em minutos", "a história inteira de lisboa",
    "história completa da cidade em minutos reconstrução ia", "a história inteira de salvador", "toda la historia de madrid en minutos",
    "la historia completa de buenos aires", "la historia completa de la ciudad de méxico"],
 "tecnologia_ciencia": ["a história inteira da inteligência artificial", "a história inteira da internet em minutos", "a história inteira do universo em minutos",
    "a história completa da terra em minutos", "toda la historia de la inteligencia artificial", "la historia completa del universo en minutos"],
 "religioes": ["a história inteira da bíblia", "a história completa do cristianismo em minutos", "a história inteira da igreja católica",
    "a história completa do islã", "toda la historia de la biblia en minutos"],
 "crime_drogas": ["a história inteira da máfia", "a história completa do pcc", "a história inteira de pablo escobar", "a história completa do cartel de medellín",
    "toda la historia del cartel de sinaloa"],
 "esportes": ["a história inteira do futebol", "a história completa da copa do mundo em minutos", "a história inteira da fórmula 1", "toda la historia del futbol en minutos"],
 "comida_commodities": ["a história inteira do café", "a história completa do açúcar", "a história inteira do chocolate", "la historia completa del café"],
 "financas_economia": ["a história inteira do dinheiro", "a história completa do bitcoin", "a história inteira da bolsa de valores", "la historia completa del dinero"],
}
def rodar(item):
    sub, q, ordem = item
    alvo = f"ytsearch25:{q}" if ordem == "relevancia" else "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=CAMSAggF"
    r = subprocess.run([YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--flat-playlist", "-J", "--playlist-end", "25", alvo], capture_output=True, text=True, timeout=120)
    if r.returncode: return item, None
    return item, [{k: e.get(k) for k in ("id", "title", "channel", "channel_id", "view_count", "duration")} for e in json.loads(r.stdout).get("entries") or []]
qs = [(s, q, o) for s, l in Q.items() for q in l for o in ("relevancia", "ano_views")]
with open(os.path.join(BASE, "dados/busca_ptes.jsonl"), "w") as f, ThreadPoolExecutor(4) as ex:
    for (s, q, o), vs in ex.map(rodar, qs):
        if vs is None: print("ERRO", q, file=sys.stderr); continue
        for i, v in enumerate(vs): f.write(json.dumps({"subnicho": s, "q": q, "ordem": o, "pos": i, **v}, ensure_ascii=False) + "\n")
