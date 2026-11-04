#!/usr/bin/env python3
"""QA da voz por bloco: transcreve audio/N###.mp3 (Whisper small, int8) e compara com o texto do bloco sem tags.
Rodar de dentro da pasta do vídeo:  <venv>/python tools/qa_voz_blocos.py [N001 N002 ...]   (sem args = todos)
Saída: qa/voz_blocos.json (por bloco: razão, tags faladas, trechos diferentes) + resumo. Critério: >= 93% por bloco (es: números por extenso, siglas unificadas)."""
import difflib, json, re, subprocess, sys, unicodedata
import numpy as np
from faster_whisper import WhisperModel

TAG = re.compile(r"\[[a-z][a-z ,-]*\]\s*")
TAGS_FALADAS = {"break", "curious", "serious", "amazed", "warm", "dramatic", "emphasis", "sad", "long", "slightly"}
MINIMO = 0.93


U = ("cero uno dos tres cuatro cinco seis siete ocho nueve diez once doce trece catorce quince dieciseis diecisiete "
     "dieciocho diecinueve veinte veintiuno veintidos veintitres veinticuatro veinticinco veintiseis veintisiete veintiocho veintinueve").split()
D = "_ _ _ treinta cuarenta cincuenta sesenta setenta ochenta noventa".split()
C = "_ ciento doscientos trescientos cuatrocientos quinientos seiscientos setecientos ochocientos novecientos".split()


def por_extenso(n):
    """0..999999 em espanhol, sem acento e sem o 'y' (a norm() descarta 'y' dos dois lados)."""
    if n < 30:
        return U[n]
    if n < 100:
        return D[n // 10] + ("" if n % 10 == 0 else " " + U[n % 10])
    if n < 1000:
        return "cien" if n == 100 else C[n // 100] + ("" if n % 100 == 0 else " " + por_extenso(n % 100))
    m = n // 1000
    return ("mil" if m == 1 else por_extenso(m) + " mil") + ("" if n % 1000 == 0 else " " + por_extenso(n % 1000))


def norm(t):
    """Minúsculas, sem acento; algarismos viram palavras; 'y' descartado; grafias de siglas unificadas."""
    t = t.lower()
    t = re.sub(r"(?<=\d)[.\s](?=\d{3}\b)", "", t)
    t = re.sub(r"\bu-?2\b", "u dos", t)
    t = re.sub(r"\d+", lambda m: " " + por_extenso(int(m.group())) + " ", t)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r"\bmk[- ]?ultra\b", "mk ultra", t).replace("pbsuccess", "pb success").replace("p b success", "pb success")
    return [w for w in re.findall(r"[a-z]+", t) if w != "y"]


def audio(caminho):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", caminho, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def main():
    ids = set(a for a in sys.argv[1:] if not a.endswith(".json"))
    blocos = [b for b in json.load(open(sys.argv[1] if sys.argv[1:] and sys.argv[1].endswith(".json") else "blocos.json")) if not ids or b["id"] in ids]
    try:
        res = json.load(open("qa/voz_blocos.json"))
    except Exception:
        res = {}
    m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=2)
    for b in blocos:
        ref = norm(TAG.sub("", b["texto"]))
        segs, _ = m.transcribe(audio(f"audio/{b['id']}.mp3"), language="es", beam_size=1, vad_filter=False)
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
