#!/usr/bin/env python3
"""Mede as amostras v2: duração, ppm, pausas, F0 (mediana/desvio/faixa), repetição melódica e queda no fim
(mesma conta do amostras-voz/melodia.py) e Whisper small (concordância com o texto e tags faladas).
Uso: ~/workspace/fabrica-youtube/tools/.venv/bin/python medir.py <amostra.mp3>... [--sem-whisper]
O texto de referência vem do <amostra>.json gerado pelo gerar.py. Resultado em medidas.json (acumula por arquivo)."""
import difflib, json, re, subprocess, sys, unicodedata
from pathlib import Path
import numpy as np
import parselmouth

AQUI = Path(__file__).resolve().parent
SR = 16000
TAG = re.compile(r"\[[^\]]*\]|<[^>]*>")


def ler(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return re.findall(r"[a-z0-9]+", "".join(c for c in t if not unicodedata.combining(c)))


def pausas(x, lim_db=-40, minimo=0.25):
    w = int(0.01 * SR); n = len(x) // w
    rms = 20 * np.log10(np.sqrt(np.mean(x[: n * w].reshape(n, w) ** 2, axis=1) + 1e-12))
    sil = rms < lim_db
    out, i = [], 0
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]:
                j += 1
            if i > 0 and j < n and (j - i) * 0.01 >= minimo:
                out.append((j - i) * 0.01)
            i = j
        else:
            i += 1
    return out


def melodia(p):
    """Cópia da conta de amostras-voz/melodia.py (para não depender do print)."""
    s = parselmouth.Sound(str(p)); pt = s.to_pitch(time_step=0.01, pitch_floor=65, pitch_ceiling=350)
    f0, t = pt.selected_array["frequency"], pt.xs()
    it = s.to_intensity(time_step=0.01); I, ti = it.values[0], it.xs()
    sil = np.interp(t, ti, I) < (np.percentile(I, 95) - 25)
    tr, cur, gap = [], [], 0
    for k in range(len(t)):
        if sil[k]:
            gap += 1
            if gap >= 25 and cur: tr.append(cur); cur = []
        else:
            gap = 0; cur.append(k)
    if cur: tr.append(cur)
    med = np.median(f0[f0 > 0]); cont = []
    for c in tr:
        v = f0[c]; ok = v > 0
        if ok.sum() < 40: continue
        x = np.arange(len(v))[ok]; y = 12 * np.log2(v[ok] / med)
        cont.append(np.interp(np.linspace(x[0], x[-1], 20), x, y))
    C = np.corrcoef(np.array(cont)); n = len(cont)
    st = 12 * np.log2(f0[f0 > 0] / med)
    return {"trechos": n, "repeticao_melodica": round(float((C.sum() - n) / (n * (n - 1))), 2),
            "queda_media_st": round(float(np.mean([c[-4:].mean() - c[:4].mean() for c in cont])), 2),
            "f0_mediana_hz": round(float(med), 1), "f0_desvio_st": round(float(np.std(st)), 2),
            "f0_faixa_p10_p90_st": round(float(np.percentile(st, 90) - np.percentile(st, 10)), 2)}


_m = None


def whisper(x):
    global _m
    from faster_whisper import WhisperModel
    _m = _m or WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = _m.transcribe(x, language="pt", vad_filter=False)
    return " ".join(s.text for s in segs).strip()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    usa_w = "--sem-whisper" not in sys.argv
    arq = AQUI / "medidas.json"
    res = json.load(open(arq)) if arq.exists() else {}
    for a in args:
        p = Path(a).resolve()
        info = json.load(open(p.with_suffix(".json")))
        direcao = info.get("direcao") or ""
        texto = " ".join(c["texto"] for c in info["chamadas"])
        if direcao:
            texto = texto.replace(direcao, " ")
        ref = norm(TAG.sub(" ", texto))
        x = ler(p)
        dur = len(x) / SR
        pz = pausas(x)
        r = {"dur_s": round(dur, 1), "palavras": len(ref), "ppm": round(len(ref) / dur * 60),
             "pausas_>=0.25s": len(pz), "silencio_pct": round(100 * sum(pz) / dur)}
        r.update(melodia(p))
        if usa_w:
            hyp_txt = whisper(x)
            hyp = norm(hyp_txt)
            r["whisper_pct"] = round(100 * difflib.SequenceMatcher(None, ref, hyp, autojunk=False).ratio(), 1)
            palavras_tag = set(norm(" ".join(TAG.findall(texto)))) - set(ref)
            r["tags_faladas"] = sorted({w for w in hyp if w in palavras_tag})
            r["whisper"] = hyp_txt
        res[p.name] = r
        print(p.name, {k: v for k, v in r.items() if k != "whisper"})
    json.dump(res, open(arq, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
