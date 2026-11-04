#!/usr/bin/env python3
"""QA da v2: compara v1 × v2 em duração, pausas reais entre blocos e nitidez no zoom máximo.

Uso (na pasta do vídeo, depois do render da v2): ~/workspace/fabrica-youtube/tools/.venv/bin/python tools/compara_v1v2.py
Entradas: out-v1/video.mp4 + qa-v1/{voz.wav,blocos.json,timeline.json} (v1) e out/video.mp4 + public/audio/voz.wav,
          qa/blocos.json, src/timeline.json, blocos.json (v2).
Saídas:   qa/v1v2.json e qa/nitidez.jpg (recortes 1:1 do mesmo plano com zoom máximo, v1 em cima e v2 embaixo).
"""
import json, subprocess, wave
from pathlib import Path
import numpy as np

V = Path(__file__).resolve().parent.parent
SR, FPS, XF = 48000, 30, 5


def dur(mp4):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                                capture_output=True, text=True, check=True).stdout)


def voz(p):
    with wave.open(str(p)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float64) / 32768


def pausas(wav, blocos, lim_db=-45):
    """Silêncio real entre o fim da voz de um bloco e o começo da voz do seguinte (janelas de 10 ms)."""
    x = voz(wav); w = int(0.01 * SR); n = len(x) // w
    on = 20 * np.log10(np.sqrt(np.mean(x[: n * w].reshape(n, w) ** 2, axis=1)) + 1e-12) > lim_db
    res = []
    for a, b in zip(blocos, blocos[1:]):
        i0, i1, i2 = int(a["ini"] * 100), int(a["fim"] * 100), int(b["fim"] * 100)
        va = np.where(on[i0:i1])[0]; vb = np.where(on[i1:i2])[0]
        if len(va) and len(vb):
            res.append(((i1 + vb[0]) - (i0 + va[-1] + 1)) / 100)
    return np.array(res)


def nitidez(mp4, t, crop):
    """Variância do Laplaciano num recorte 1:1 do frame (quanto maior, mais nítido)."""
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(mp4), "-frames:v", "1", "-vf", f"crop={crop},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    cw, ch = map(int, crop.split(":")[:2])
    g = np.frombuffer(png, dtype=np.uint8)[: cw * ch].reshape(ch, cw).astype(np.float64)
    lap = g[1:-1, 1:-1] * -4 + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:]
    return float(lap.var())


def main():
    tl1, tl2 = json.load(open(V / "qa-v1/timeline.json")), json.load(open(V / "src/timeline.json"))
    b1, b2 = json.load(open(V / "qa-v1/blocos.json")), json.load(open(V / "qa/blocos.json"))
    ideia = {b["id"]: b.get("ideia", False) for b in json.load(open(V / "blocos.json"))}
    caps = {c["bloco"] for c in tl2["chapters"]}
    p1, p2 = pausas(V / "qa-v1/voz.wav", b1), pausas(V / "public/audio/voz.wav", b2)
    tipo = ["capítulo" if b["id"] in caps else "ideia" if ideia[b["id"]] else "mesmo" for b in b2[1:]]
    por_tipo = {k: {"v1": round(float(p1[[i for i, t in enumerate(tipo) if t == k]].mean()), 2),
                    "v2": round(float(p2[[i for i, t in enumerate(tipo) if t == k]].mean()), 2),
                    "n": tipo.count(k)} for k in ("mesmo", "ideia", "capítulo")}

    # nitidez: planos reenquadrados (detalhe-* = 1,6–1,68x, o zoom máximo do vídeo; médio-* = ~1,4x) com a mesma imagem
    # nas duas versões; frame no fim do plano (zoom máximo dele), antes do crossfade
    def fim(tl, img):
        s = max((s for s in tl["shots"] if s["img"] == img and s["enq"] != "aberto"), key=lambda s: s["enq"].startswith("detalhe"))
        return (s["from"] + s["dur"] - XF - 2) / FPS, s["enq"]
    det = lambda tl: {s["img"] for s in tl["shots"] if s["enq"] != "aberto"}
    zoom = lambda img: any(s["img"] == img and s["enq"].startswith("detalhe") for s in tl2["shots"])
    pares = sorted(det(tl1) & det(tl2), key=lambda i: (not zoom(i), i))   # o plano de zoom máximo (detalhe) primeiro
    pares = pares[:1] + pares[1:][:: max(1, len(pares) // 7)][:7]
    crop = "480:270:720:405"   # centro da tela, 1:1
    nit = []
    for img in pares:
        (t1, e1), (t2, e2) = fim(tl1, img), fim(tl2, img)
        nit.append({"img": img, "enq": f"{e1} / {e2}", "t_v1": round(t1, 2), "t_v2": round(t2, 2),
                    "v1": round(nitidez(V / "out-v1/video.mp4", t1, crop), 1), "v2": round(nitidez(V / "out/video.mp4", t2, crop), 1)})
    # recortes lado a lado das 3 primeiras imagens
    tmp = V / "qa/nit"; tmp.mkdir(parents=True, exist_ok=True)
    for k, n in enumerate(nit[:3]):
        for ver, mp4, t in (("v1", V / "out-v1/video.mp4", n["t_v1"]), ("v2", V / "out/video.mp4", n["t_v2"])):
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(mp4), "-frames:v", "1", "-vf", f"crop={crop}",
                            str(tmp / f"{ver}_{k}.png")], check=True)
    ins = sum((["-i", str(tmp / f"{v}_{k}.png")] for v in ("v1", "v2") for k in range(min(3, len(nit)))), [])
    m = min(3, len(nit))
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex",
                    f"xstack=inputs={2 * m}:grid={m}x2", "-q:v", "2", str(V / "qa/nitidez.jpg")], check=True)

    res = {"duracao_s": {"v1": round(dur(V / "out-v1/video.mp4"), 1), "v2": round(dur(V / "out/video.mp4"), 1)},
           "pausa_media_s": {"v1": round(float(p1.mean()), 2), "v2": round(float(p2.mean()), 2)},
           "pausa_por_tipo_v2": por_tipo,
           "nitidez_laplaciano": {"planos": nit, "media_v1": round(np.mean([n["v1"] for n in nit]), 1),
                                  "media_v2": round(np.mean([n["v2"] for n in nit]), 1)}}
    json.dump(res, open(V / "qa/v1v2.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
