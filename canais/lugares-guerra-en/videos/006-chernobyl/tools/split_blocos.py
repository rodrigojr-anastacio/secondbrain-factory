#!/usr/bin/env python3
"""Divide a narração do SCRIPT.md em blocos de áudio (≤ 48 palavras, ≤ 4 frases) → qa/split_blocos.json + blocos-voz.json (grafia da voz).
006: marcadores [[A1]]…[[A6]] no texto = áudio de época (não narrado) inserido naquele ponto; o parágrafo é cortado ali
e o bloco seguinte leva "arquivo_antes": "A3" (o roteiro.py e o build.py põem o áudio de época antes dele)."""
import re, json
from pathlib import Path
V = Path(__file__).resolve().parent.parent
VOZ_SUBS = [
    # 006: grafias da voz (conferir no Whisper): Pripyat ("PRIP-yat"), Bryukhanov, Khodemchuk, Shashenok, Kibenok, Pravik, Masik, Dymer,
    # Ivankov, Forsmark, Chebrikov, Gromyko, Dobrynin, Vremya ("VREM-ya"), INSAG ("IN-sag"), RCPS, EPS-5, germanium.
    ("EPS-5", "E.P.S. five"), ("INSAG-7", "Insag seven"), ("RCPS", "R.C.P.S."), ("Pripyat'", "Pripyat"),
    ("at 2000 26 April 1986", "at twenty hundred, twenty-six April nineteen eighty-six"), ("1125 buses and 250 trucks", "eleven twenty-five buses and two hundred fifty trucks"),
    ("1:30 a.m.", "one thirty a.m."), ("1991", "nineteen ninety-one"), ("1992", "nineteen ninety-two"), ("1986", "nineteen eighty-six"),

    # 005: grafia da voz (o texto da tela/legenda continua o do SCRIPT.md). Conferir no Whisper: Betio ("BAY-shoh"), Kiribati ("KEER-ih-bahss"),
    # Tarawa, Sasebo, Shibasaki, Masatoshi/Sadayuki Nomura, Choi Byeong-yeon ("CHWAY byung-yun"), Scovill, Roecker, Rush (Kentucky).
    ("POW/MIA", "P.O.W. M.I.A."), ("Kiribati", "Kiribass"), ("Betio", "Bay-sho"),
    ("124 of the 243 (~50%) unique Sanger-generated mtDNA sequences are consistent with Asian haplogroups",
     "one hundred twenty-four of the two hundred forty-three, about fifty percent, unique Sanger-generated M.T. D.N.A. sequences are consistent with Asian haplogroups"),
    ("From 1943-1946", "From nineteen forty-three to nineteen forty-six"), ("SeaBee", "Seabee"),
    ("3,301", "thirty-three hundred and one"), ("4,836", "forty-eight thirty-six"), ("4,690", "forty-six ninety"),
    ("Choi Byeong-yeon", "Choi Byung-yun"),
]
def voz(t):
    for a, b in VOZ_SUBS: t = t.replace(a, b)
    return t
def main():
    s = (V / "SCRIPT.md").read_text()
    paras0 = {m.group(1): m.group(2).strip() for m in re.finditer(r"^### (B\d\d) .*\n(.+)$", s, re.M)}
    sents = lambda t: [p for p in re.split(r'(?:(?<=[.?!]")|(?<=[.?!]))\s+(?=["A-Z])', t) if p]
    blocos = []
    for bid, t0 in paras0.items():
      partes = re.split(r"\s*\[\[(A\d)\]\]\s*", t0)
      arq = [None] + partes[1::2]
      for k, t in enumerate(partes[0::2]):
        if not t:
            pend = arq[k]; continue
        ant = arq[k] if k < len(arq) else None
        if k and not ant: ant = pend
        chunks, cur = [], []
        for x in sents(t):
            if cur and (sum(len(y.split()) for y in cur) + len(x.split()) > 48 or len(cur) >= 4):
                chunks.append(cur); cur = []
            cur.append(x)
        if cur:
            if chunks and sum(len(y.split()) for y in cur) < 12: chunks[-1] += cur
            else: chunks.append(cur)
        n0 = sum(1 for b in blocos if b["id"][:3] == bid)
        for i, c in enumerate(chunks):
            d = dict(id=f"{bid}{'abcdefghijkl'[n0 + i]}", texto=" ".join(c))
            if i == 0 and ant: d["arquivo_antes"] = ant
            blocos.append(d)
        pend = None
    json.dump(blocos, open(V / "qa/split_blocos.json", "w"), ensure_ascii=False, indent=1)
    assert all(b["texto"] for b in blocos)
    json.dump([dict(id=b["id"], texto=voz(b["texto"])) for b in blocos], open(V / "blocos-voz.json", "w"), ensure_ascii=False, indent=1)
    print(len(blocos), "blocos,", sum(len(b["texto"].split()) for b in blocos), "palavras")
if __name__ == "__main__":
    main()
