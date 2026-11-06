#!/usr/bin/env python3
"""(Cópia do 003-ira/v2-voz, adaptada ao 004-china: compara também com a grafia de tela.) Rescore do QA de voz por bloco (qa/voz_blocos.json) com chave fonética, para não reprovar bloco por grafia de nome persa
no Whisper ("cha" = xá, "canats" = qanats, "Nasser" = Naser). Uso (pasta do vídeo): python3 v2-voz/qa_fonetico.py [--min 0.95]"""
import difflib, json, re, sys, unicodedata
sys.path.insert(0, "tools")
from qa_voz_blocos import norm, TAG  # noqa: E402

def fon(w):
    w = w.replace("tch", "x").replace("dj", "j").replace("zh", "j").replace("sh", "x").replace("ch", "x").replace("kh", "k").replace("q", "k").replace("ph", "f")
    w = re.sub(r"c(?=[aou])", "k", w); w = re.sub(r"c(?=[ei])", "s", w).replace("z", "s").replace("ss", "s").replace("w", "u").replace("y", "i")
    w = w.replace("h", "").replace("j", "i").replace("g", "k")
    w = re.sub(r"(.)\1+", r"\1", w)
    return w[:-1] if len(w) > 3 and w[-1] in "aeiou" else w   # vogal final átona varia no Whisper (persa/perso)

def chave(ws):
    return list("".join(fon(w) for w in ws))   # compara por caractere: "pai de daesa" ≈ "pairidaeza"

mn = float(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 0.95
bl = json.load(open("blocos.json")); r = json.load(open("qa/voz_blocos.json"))
out = {}
for b in bl:
    x = r[b["id"]]
    hyp = chave(norm(x["transcricao"]))
    # 004-china: o Whisper escreve os nomes em pinyin (Qin, Zhou) e o Fish recebe a grafia fonética (Tchin, Djou):
    # vale a melhor das duas comparações (texto falado × grafia de tela)
    out[b["id"]] = round(max(difflib.SequenceMatcher(None, chave(norm(TAG.sub("", b[c]))), hyp, autojunk=False).ratio()
                             for c in ("texto", "tela") if c in b), 4)
v = list(out.values())
ruins = {k: s for k, s in out.items() if s < mn or r[k]["tags_faladas"]}
print(f"{len(v)} blocos · mín {100*min(v):.1f}% · média {100*sum(v)/len(v):.1f}% · abaixo de {100*mn:.0f}%: {len(ruins)}")
for k, s in ruins.items():
    print(k, f"{100*s:.1f}%", r[k]["diferencas"][:5])
json.dump(out, open("qa/voz_blocos_fonetico.json", "w"), indent=0)
