# Tabela de trechos reais para FONTES-E-LICENCAS.md (de clipes.json + cues.json): onde aparece, URL, autor, segundos do original.
import json
from pathlib import Path
A = Path(__file__).parent; R = A.parent
CL = json.load(open(A / "clipes.json")); c = json.load(open(A / "cues.json"))
def mmss(t): return f"{int(t // 60)}:{t % 60:04.1f}"
usos = [(m["t0"], m["t1"], m["id"], m.get("rate", 1)) for m in c["midia"] if m["tipo"] == "video"]
usos += [(it["t"], c["cortica"]["t1"], it["src"].split("/")[-1][:-4], 1) for it in c["cortica"]["itens"] if it["tipo"] == "foto"]
L = ["| # | No vídeo | Trecho (legenda na tela) | Fonte (URL) | Autor / canal | Segundos do original | Crédito na tela |", "|---|---|---|---|---|---|---|"]
for k, (t0, t1, nome, rate) in enumerate(sorted(usos), 1):
    x = CL[nome]; d = min(x["duracao"], (t1 - t0) * rate)
    ini = x["ss"] if x["ss"] else x["ini"]
    autor = x["credito"].replace("VÍDEO: ", "").split(" · ")[0]
    L.append(f"| {k} | {mmss(t0)}–{mmss(t1)} | {x['legenda']} | {x['url']} | {autor} | {ini:.1f}–{ini + d:.1f} s{' (em loop)' if t1 - t0 > x['duracao'] + 1 else ''} | {x['credito']} |")
open(R / "work/licencas-videos.md", "w").write("\n".join(L))
I = ["| No vídeo | Imagem | Arquivo | Crédito na tela |", "|---|---|---|---|"]
for m in c["midia"]:
    if m["tipo"] == "img": I.append(f"| {mmss(m['t0'])}–{mmss(m['t1'])} | {m['legenda']} | {m['src']} | {m['credito']} |")
open(R / "work/licencas-imagens.md", "w").write("\n".join(I))
print(len(usos), "usos de vídeo;", len(I) - 2, "imagens")
