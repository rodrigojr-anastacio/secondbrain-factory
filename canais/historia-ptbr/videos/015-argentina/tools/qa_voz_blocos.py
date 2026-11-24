#!/usr/bin/env python3
"""QA da voz por bloco: transcreve audio/N###.mp3 (Whisper small, int8) e compara com o texto do bloco sem tags.
Rodar de dentro da pasta do vídeo:  <venv>/python tools/qa_voz_blocos.py [N001 N002 ...]   (sem args = todos)
Saída: qa/voz_blocos.json (por bloco: razão, tags faladas, trechos diferentes) + resumo. Critério: >= 93% por bloco."""
import difflib, json, re, subprocess, sys, unicodedata
import numpy as np
from faster_whisper import WhisperModel

TAG = re.compile(r"\[[a-z][a-z ,-]*\]\s*")
TAGS_FALADAS = {"break", "curious", "serious", "amazed", "warm", "dramatic", "emphasis", "sad", "long"}
MINIMO = 0.93


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


def audio(caminho):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", caminho, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def main():
    ids = set(sys.argv[1:])
    blocos = [b for b in json.load(open("blocos.json")) if not ids or b["id"] in ids]
    try:
        res = json.load(open("qa/voz_blocos.json"))
    except Exception:
        res = {}
    m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
    for b in blocos:
        ref = norm(TAG.sub("", b["texto"]))
        segs, _ = m.transcribe(audio(f"audio/{b['id']}.mp3"), language="pt", beam_size=1, vad_filter=False)
        txt = " ".join(s.text.strip() for s in segs)
        hyp = norm(txt)
        sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
        difs = [f"{op}: roteiro {' '.join(ref[a:b_])!r} | voz {' '.join(hyp[c:d])!r}"
                for op, a, b_, c, d in sm.get_opcodes() if op != "equal"]
        falou = sorted(set(hyp) & TAGS_FALADAS - set(ref))
        res[b["id"]] = {"razao": round(sm.ratio(), 4), "palavras_roteiro": len(ref), "palavras_voz": len(hyp),
                        "tags_faladas": falou, "diferencas": difs, "transcricao": txt}
        print(f"{b['id']} {100 * sm.ratio():5.1f}%" + (f"  TAGS {falou}" if falou else "") + ("  <93" if sm.ratio() < MINIMO else ""), flush=True)
        json.dump(res, open("qa/voz_blocos.json", "w"), ensure_ascii=False, indent=1)
    r = [v["razao"] for v in res.values()]
    ruins = sorted(k for k, v in res.items() if v["razao"] < MINIMO or v["tags_faladas"])
    print(f"\n{len(r)} blocos · mín {100 * min(r):.1f}% · média {100 * sum(r) / len(r):.1f}% · abaixo de 93% ou com tag: {len(ruins)} {ruins}")


if __name__ == "__main__":
    main()
