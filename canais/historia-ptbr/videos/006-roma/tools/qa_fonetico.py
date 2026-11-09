#!/usr/bin/env python3
"""006-roma: nota fonética por bloco a partir de qa/voz_blocos.json — compara roteiro × Whisper por letras, sem espaços,
sem 'h' e com u/l finais equivalentes (o Whisper corta "acorrentada" em "a correntada", "Danúbio" em "da Núvio", "Aníbal" em "a Nibau").
Uso (pasta do vídeo): python3 tools/qa_fonetico.py"""
import difflib, json, re, sys
sys.path.insert(0, "tools")
from qa_voz_blocos import norm, TAG
r = json.load(open("qa/voz_blocos.json")); bl = {b["id"]: b for b in json.load(open("blocos.json"))}
def chave(ws): return re.sub(r"l(?=\W|$)", "u", " ".join(ws)).replace(" ", "").replace("h", "")
out = {}
for k, v in r.items():
    a, z = chave(norm(TAG.sub("", bl[k]["tela"]))), chave(norm(v["transcricao"]))
    out[k] = round(100 * difflib.SequenceMatcher(None, a, z, autojunk=False).ratio(), 1)
vals = list(out.values()); ruins = {k: x for k, x in out.items() if x < 95}
print(f"{len(vals)} blocos · mín {min(vals)}% · média {sum(vals)/len(vals):.1f}% · < 95%: {ruins}")
json.dump(out, open("qa/voz_fonetico.json", "w"), indent=0)
