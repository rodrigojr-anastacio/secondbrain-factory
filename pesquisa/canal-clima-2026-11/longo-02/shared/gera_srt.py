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
caps = [("0:00", "Fumaça no Norte, chuva no Sul, mar quente: a pergunta")]
mapa = {"PERGUNTA 1/4 · O QUE É": "O que é o El Niño (a gangorra do Pacífico)", "PERGUNTA 2/4 · É SUPER?": "É mesmo um Super El Niño? O recorde e o termômetro novo",
        "PERGUNTA 3/4 · MINHA REGIÃO": "O que muda na sua região", "NORTE": "Norte: seca, fogo e fumaça", "NORDESTE": "Nordeste: seca no semiárido",
        "CENTRO-OESTE E SUDESTE": "Centro-Oeste e Sudeste: calor e reservatórios", "SUL": "Sul: chuva, enchentes e tornados", "O MUNDO": "O mundo: 2027 pode ser o ano mais quente",
        "PERGUNTA 4/4 · ATÉ QUANDO": "Até quando vai o El Niño?", "O QUE FAZER": "O que fazer na sua região", "A RESPOSTA": "A resposta"}
for cp in c["capitulos"]:
    if cp["nome"] in mapa and mapa[cp["nome"]] not in [x[1] for x in caps]:
        t = cp["t"]; caps.append((f"{int(t // 60)}:{int(t % 60):02d}", mapa[cp["nome"]]))
open(R / "work/capitulos.txt", "w").write("\n".join(f"{a} {b}" for a, b in caps))
print(len(out), "legendas;", *[f"{a} {b}" for a, b in caps], sep="\n")
