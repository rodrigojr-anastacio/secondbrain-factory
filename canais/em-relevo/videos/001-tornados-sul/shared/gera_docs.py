# Gera ROTEIRO.md (texto com tempos) e o rascunho do STORYBOARD (transições e mídias) a partir dos JSONs.
import json
from pathlib import Path
A = Path(__file__).parent; R = A.parent
bl = json.load(open(A / "blocos.json")); tp = {b["id"]: b for b in json.load(open(A / "tempos.json"))["blocos"]}
c = json.load(open(A / "cues.json"))
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
L = ["| Bloco | Tempo | Aba | Atempo | Texto (tela) |", "|---|---|---|---|---|"]
for b in bl:
    t = tp[b["id"]]
    L.append(f"| {b['id']} | {mmss(t['s'])}–{mmss(t['e'])} | {b['cap']} | {t.get("atempo", b["marcha"])} | {b["tela"].replace('|', '/')} |")
open(R / "work/roteiro-tabela.md", "w").write("\n".join(L))
S = ["| # | Tempo | Transição | SFX |", "|---|---|---|---|"]
sfx = {"nuvem": "whoosh longo", "whip": "swish + whoosh curto", "luz": "whoosh médio baixo", "corte": "impacto grave", "orbital": "whoosh longo",
       "rack": "whoosh médio", "match": "impacto suave + whoosh", "whip_v": "swish + whoosh curto", "match_funil": "impacto suave", "zoomout": "whoosh longo"}
for i, x in enumerate(c["transicoes"], 1): S.append(f"| T{i} | {mmss(x['t'])} | {x['desc']} | {sfx[x['tipo']]} |")
M = ["| Tempo | Tipo | Quadro | Legenda na tela | Crédito na tela |", "|---|---|---|---|---|"]
for m in c["midia"]: M.append(f"| {mmss(m['t0'])}–{mmss(m['t1'])} | {'vídeo' if m['tipo']=='video' else 'imagem'} | {m['fmt']} ({m['lado']}) | {m['legenda']} | {m['credito']} |")
for it in c["cortica"]["itens"]:
    if it["tipo"] == "foto": M.append(f"| {mmss(it['t'])}–{mmss(c['cortica']['t1'])} | vídeo | polaroid no quadro de cortiça | {it['legenda']} | VÍDEO: {it['credito']} |")
for s in c["sats"]:
    o = s["op"]; M.append(f"| {mmss(o[1][0])}–{mmss(o[-1][0])} | satélite (folha sobre o mapa) | translúcida | — | barra de fontes: NOAA/NASA |")
open(R / "work/storyboard-tabelas.md", "w").write("\n".join(S) + "\n\n" + "\n".join(M))
tela_real = sum(m["t1"] - m["t0"] for m in c["midia"]) + sum(c["cortica"]["t1"] - it["t"] for it in c["cortica"]["itens"] if it["tipo"] == "foto") * 0 + sum((s["op"][-2][0] - s["op"][1][0]) for s in c["sats"])
# tempo com pelo menos 1 material real na tela (união dos intervalos)
iv = [(m["t0"], m["t1"]) for m in c["midia"]] + [(it["t"], c["cortica"]["t1"]) for it in c["cortica"]["itens"] if it["tipo"] == "foto"] + [(s["op"][1][0], s["op"][-1][0]) for s in c["sats"]]
iv.sort(); tot, cur = 0, None
for a, b in iv:
    if cur and a <= cur[1]: cur[1] = max(cur[1], b)
    else:
        if cur: tot += cur[1] - cur[0]
        cur = [a, b]
tot += cur[1] - cur[0]
nv = sum(1 for m in c["midia"] if m["tipo"] == "video") + sum(1 for it in c["cortica"]["itens"] if it["tipo"] == "foto")
ni = sum(1 for m in c["midia"] if m["tipo"] == "img")
print(f"tempo com material real na tela: {tot:.0f} s de {c['duracao']:.0f} s = {100*tot/c['duracao']:.0f}%; trechos de vídeo: {nv}; imagens: {ni}; folhas de satélite: {len(c['sats'])}")
