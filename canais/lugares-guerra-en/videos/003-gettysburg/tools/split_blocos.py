#!/usr/bin/env python3
"""Divide a narração do SCRIPT.md em blocos de áudio (≤ 48 palavras, ≤ 4 frases) → qa/split_blocos.json + blocos-voz.json (grafia da voz)."""
import re, json
from pathlib import Path
V = Path(__file__).resolve().parent.parent
VOZ_SUBS = [
    # 003: nenhuma troca por enquanto; conferir no Whisper Frassanito, O'Sullivan, Lamon, Reynolds, Devil's Den
]
def voz(t):
    for a, b in VOZ_SUBS: t = t.replace(a, b)
    return t
def main():
    s = (V / "SCRIPT.md").read_text()
    paras = {m.group(1): m.group(2).strip() for m in re.finditer(r"^### (B\d\d) .*\n(.+)$", s, re.M)}
    sents = lambda t: [p for p in re.split(r'(?:(?<=[.?!]")|(?<=[.?!]))\s+(?=["A-Z])', t) if p]
    blocos = []
    for bid, t in paras.items():
        chunks, cur = [], []
        for x in sents(t):
            if cur and (sum(len(y.split()) for y in cur) + len(x.split()) > 48 or len(cur) >= 4):
                chunks.append(cur); cur = []
            cur.append(x)
        if cur:
            if chunks and sum(len(y.split()) for y in cur) < 12: chunks[-1] += cur
            else: chunks.append(cur)
        for i, c in enumerate(chunks):
            blocos.append(dict(id=f"{bid}{'abcdefgh'[i]}", texto=" ".join(c)))
        assert " ".join(b["texto"] for b in blocos if b["id"][:3] == bid) == t, bid
    json.dump(blocos, open(V / "qa/split_blocos.json", "w"), ensure_ascii=False, indent=1)
    json.dump([dict(id=b["id"], texto=voz(b["texto"])) for b in blocos], open(V / "blocos-voz.json", "w"), ensure_ascii=False, indent=1)
    print(len(blocos), "blocos,", sum(len(b["texto"].split()) for b in blocos), "palavras")
if __name__ == "__main__":
    main()
