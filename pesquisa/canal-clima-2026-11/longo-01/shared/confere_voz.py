# Voz × roteiro: compara o texto falado (blocos.json) com o Whisper (whisper.json) por bloco. Saída: work/confere_voz.txt
import json, re, unicodedata, difflib
from pathlib import Path
A = Path(__file__).parent
def n(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", " ", s).split()
bl = json.load(open(A / "blocos.json")); tp = {b["id"]: b for b in json.load(open(A / "tempos.json"))["blocos"]}
wh = json.load(open(A / "whisper.json"))
out = []; rs = []
for b in bl:
    t = tp[b["id"]]; ws = [w for w in wh if t["s"] - 0.3 <= w["s"] <= t["e"] + 0.1]
    a, c = n(b["fala"]), n(" ".join(w["w"] for w in ws))
    r = difflib.SequenceMatcher(None, a, c).ratio(); rs.append(r)
    pm = sum(w["p"] for w in ws) / max(1, len(ws))
    out.append(f"{b['id']} {t['s']:7.1f}s ratio={r:.2f} prob={pm:.2f}\n  ROTEIRO: {' '.join(a)}\n  WHISPER: {' '.join(c)}")
open(A.parent / "work/confere_voz.txt", "w").write("\n".join(out))
print(f"média ratio {sum(rs)/len(rs):.3f}; piores:", sorted(zip(rs, [b['id'] for b in bl]))[:8])
