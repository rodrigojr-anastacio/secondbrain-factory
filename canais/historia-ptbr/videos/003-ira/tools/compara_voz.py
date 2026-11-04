#!/usr/bin/env python3
"""QA voz × roteiro: compara qa/transcricao.json (Whisper) com blocos.json, sem tags. Salva qa/voz_diff.txt."""
import difflib, json, re, unicodedata
TAG = re.compile(r"\[[^\]]*\]\s*")
def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", t)
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
