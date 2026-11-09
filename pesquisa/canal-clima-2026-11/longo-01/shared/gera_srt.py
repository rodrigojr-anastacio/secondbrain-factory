# out/legendas-v2.srt (v2; a v1 ficou em out/legendas.srt) a partir dos cartões da legenda (cues.palavras: "|" separa cartões) + capítulos do YouTube.
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
open(R / "out/legendas-v2.srt", "w").write("\n".join(out))
caps = [("0:00", "7 tornados em 6 dias: a pergunta")]
mapa = {"DIA 1 · 2/11": "Dia a dia: Maringá (2/11)", "DIA 3 · 4/11": "4/11: Chapecó, Xanxerê, Erval Grande, Rio Negrinho", "DIA 6 · 7/11": "7/11: Santo Augusto e Palmeira das Missões",
        "É INÉDITO?": "Isso é inédito?", "PERGUNTA 1/3 · POR QUÊ": "Pergunta 1: por que acontece aqui", "EL NIÑO": "El Niño 2026: o que a ciência diz",
        "PERGUNTA 2/3 · RISCO": "Pergunta 2: vai voltar a acontecer?", "PERGUNTA 3/3 · ATÉ ONDE": "Pergunta 3: até onde pode chegar", "O QUE FAZER": "O que fazer", "A RESPOSTA": "A resposta"}
for cp in c["capitulos"]:
    if cp["nome"] in mapa and mapa[cp["nome"]] not in [x[1] for x in caps]:
        t = cp["t"]; caps.append((f"{int(t // 60)}:{int(t % 60):02d}", mapa[cp["nome"]]))
open(R / "work/capitulos.txt", "w").write("\n".join(f"{a} {b}" for a, b in caps))
print(len(out), "legendas;", *[f"{a} {b}" for a, b in caps], sep="\n")
