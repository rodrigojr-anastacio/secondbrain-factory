#!/usr/bin/env python3
"""QA voz × roteiro: compara qa/transcricao.json (Whisper) com blocos.json, sem tags. Salva qa/voz_diff.txt."""
import difflib, json, re, unicodedata
TAG = re.compile(r"\[[^\]]*\]\s*")
U = "zero um dois três quatro cinco seis sete oito nove dez onze doze treze catorze quinze dezesseis dezessete dezoito dezenove".split()
D = "_ _ vinte trinta quarenta cinquenta sessenta setenta oitenta noventa".split()
C = "_ cento duzentos trezentos quatrocentos quinhentos seiscentos setecentos oitocentos novecentos".split()


def por_extenso(n):
    """0..999999 em pt-BR (sem o 'e': a norm() descarta 'e' dos dois lados, então a conjunção não importa)."""
    if n < 20:
        return U[n]
    if n < 100:
        return D[n // 10] + ("" if n % 10 == 0 else " " + U[n % 10])
    if n < 1000:
        return "cem" if n == 100 else C[n // 100] + ("" if n % 100 == 0 else " " + por_extenso(n % 100))
    m = n // 1000
    return ("mil" if m == 1 else por_extenso(m) + " mil") + ("" if n % 1000 == 0 else " " + por_extenso(n % 1000))


def norm(t):
    """Minúsculas, sem acento; algarismos viram palavras; 'a.C.' = antes de cristo; 'e' descartado; xá/shah = xa."""
    t = t.lower()
    t = re.sub(r"(?<=\d)[.\s](?=\d{3}\b)", "", t)
    t = re.sub(r"\ba\.?\s?c\.?(?=\W|$)", "antes de cristo", t)
    t = re.sub(r"\bd\.?\s?c\.?(?=\W|$)", "depois de cristo", t)
    t = re.sub(r"\d+", lambda m: " " + por_extenso(int(m.group())) + " ", t)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    return [{"shah": "xa", "ira": "ira", "iran": "ira"}.get(w, w) for w in re.findall(r"[a-z]+", t) if w != "e"]


ref = norm(" ".join(TAG.sub("", b["texto"]) for b in json.load(open("blocos.json"))))
hyp = norm(" ".join(s["texto"] for s in json.load(open("qa/transcricao.json"))))
sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
linhas = []
for op, a, b, c, d in sm.get_opcodes():
    if op != "equal":
        linhas.append(f"{op:8s} roteiro: {' '.join(ref[a:b])[:90]!r} | voz: {' '.join(hyp[c:d])[:90]!r}")
open("qa/voz_diff.txt", "w").write("\n".join(linhas) + "\n")
tags = [w for w in hyp if w in {"break", "curious", "serious", "amazed", "warm", "dramatic", "emphasis", "sad"}]
print(f"concordância {100 * sm.ratio():.1f}% · {len(ref)} palavras no roteiro, {len(hyp)} na voz · {len(linhas)} trechos diferentes · tags faladas: {tags}")
big = [l for l in linhas if len(l.split("|")[0]) > 60]
print("\n".join(big[:40]))
