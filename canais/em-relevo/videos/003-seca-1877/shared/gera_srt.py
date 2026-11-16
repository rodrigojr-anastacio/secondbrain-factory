# out/legendas.srt (longo 02) a partir dos cartões da legenda (cues.palavras: "|" separa cartões) + capítulos do YouTube.
import json
from pathlib import Path
A = Path(__file__).parent; R = A.parent
c = json.load(open(A / "cues.json")); tp = json.load(open(A / "tempos.json"))["blocos"]
cartoes, cur = [], []
for p in c["palavras"]:
    if p == "|":
        if cur: cartoes.append(cur); cur = []
    else: cur.append(p)
if cur: cartoes.append(cur)
fins = [f["e"] for b in tp for f in b["frases"]]
def fim_frase(t):
    return min((e for e in fins if e >= t - 0.05), default=t + 2)
def ts(t): h, r = divmod(t, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
out = []; fim_ant = 0
for i, cd in enumerate(cartoes):
    t0 = cd[0][1]; prox = cartoes[i + 1][0][1] if i + 1 < len(cartoes) else t0 + 3
    t1 = min(prox - 0.02, fim_frase(cd[-1][1]) + 0.25)
    a = max(fim_ant + 0.01, t0 - 0.05); b = max(t1, a + 0.6); fim_ant = b
    out.append(f"{i+1}\n{ts(a)} --> {ts(b)}\n{' '.join(w for w, _ in cd)}\n")
(R / "out").mkdir(exist_ok=True)
open(R / "out/legendas.srt", "w").write("\n".join(out))
mapa = {"FORTALEZA · 1878": "Fortaleza, 1878", "A PERGUNTA": "A pergunta: a seca que quase ninguém conta", "PERGUNTA 1/4 · O QUE ACONTECEU": "O que aconteceu em 1877-78",
        "PERGUNTA 2/4 · POR QUE NÃO CHOVEU": "Por que não choveu (El Niño e Atlântico)", "PERGUNTA 3/4 · O QUE MUDOU NO MAPA": "O que a seca mudou no mapa do Brasil",
        "PERGUNTA 4/4 · E EM 2026": "Pode se repetir em 2026?", "A RESPOSTA": "A resposta"}
caps = []
for cp in c["capitulos"]:
    nome = next((v for k, v in mapa.items() if cp["nome"].startswith(k)), None)
    if nome and nome not in [x[1] for x in caps]:
        t = 0 if not caps else cp["t"]; caps.append((f"{int(t // 60)}:{int(t % 60):02d}", nome))
open(R / "work/capitulos.txt", "w").write("\n".join(f"{a} {b}" for a, b in caps))
print(len(out), "legendas;", *[f"{a} {b}" for a, b in caps], sep="\n")
