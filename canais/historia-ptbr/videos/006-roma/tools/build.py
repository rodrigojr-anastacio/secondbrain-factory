#!/usr/bin/env python3
"""Etapa 2: junta a narração, gera a trilha, reescala o storyboard e escreve a timeline do Remotion.

Uso (na pasta do vídeo): ~/workspace/fabrica-youtube/tools/.venv/bin/python tools/build.py
Entradas: blocos.json, storyboard.json, audio/N###.mp3, imagens/I###.jpg
Saídas:   public/audio/{voz,trilha,mix}.wav, public/img/ (links), src/timeline.json,
          out/legendas.srt, qa/blocos.json (tempos reais por bloco), qa/capitulos.json
"""
import json, math, re, subprocess, wave
from pathlib import Path
import numpy as np

V = Path(__file__).resolve().parent.parent
SR, FPS = 48000, 30
# s de silêncio entre blocos do mesmo assunto / antes de bloco que abre ideia nova ("ideia": true) / antes de capítulo / início / fim
GAP, GAP_IDEIA, GAP_CAP, HEAD, TAIL = 0.35, 0.9, 1.5, 0.25, 2.0
TAG = re.compile(r"\[[^\]]*\]\s*")   # pausas, ênfase e tags de tom do Fish


def ler_mp3(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def aparar(x, lim_db=-45, cab=0.05, cauda=0.15):
    """Corta o silêncio do começo e do fim, deixando uma folga curta (cauda de 0,15 s para a frase respirar)."""
    w = int(0.01 * SR)
    n = len(x) // w
    rms = np.sqrt(np.mean(x[: n * w].reshape(n, w) ** 2, axis=1) + 1e-12)
    voz = np.where(20 * np.log10(rms) > lim_db)[0]
    if not len(voz):
        return x
    a = max(0, voz[0] * w - int(cab * SR))
    z = min(len(x), (voz[-1] + 1) * w + int(cauda * SR))
    y = x[a:z].copy()
    f = int(0.008 * SR)
    y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y


def salvar(p, x):
    x = np.clip(x, -1, 1)
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


# ───────────── trilha original gerada no código (sem samples) ─────────────
def trilha(dur):
    """005-brasil: pad, drone de Sol + Ré e dedilhado (timbre de cordas dedilhadas, tipo viola) no modo mixolídio de Sol (Sol Lá Si Dó Ré Mi Fá), o modo da música nordestina. Sons sintetizados aqui; nada de terceiros. (003: Hijaz persa; 004: pentatônica chinesa.)"""
    rng = np.random.default_rng(42)
    N = int(dur * SR); t = np.arange(N) / SR
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    out = np.zeros(N)
    # drone Ré + Lá, respirando devagar
    out += 0.05 * np.sin(2 * np.pi * hz(43) * t) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 19))
    out += 0.03 * np.sin(2 * np.pi * hz(50) * t + 1) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 27 + 2))
    # pads: acordes de 12 s com envelope lento
    prog = [[43, 50, 55, 59], [41, 48, 53, 57], [48, 55, 60, 64], [43, 50, 55, 59], [40, 47, 52, 55], [41, 48, 53, 57]]   # Sol, Fá, Dó, Sol, Mi menor, Fá (mixolídio de Sol: o Fá natural)
    CH = 12.0
    for c in range(int(dur / CH) + 2):
        s0 = int((c * CH - 3) * SR); L = int((CH + 6) * SR)
        a, b = max(0, s0), min(N, s0 + L)
        if a >= b: continue
        tt = np.arange(a, b) / SR - (c * CH - 3)
        env = (np.clip(tt / 4, 0, 1) * np.clip((CH + 6 - tt) / 4, 0, 1)) ** 1.5
        seg = np.zeros(b - a)
        for m in prog[c % len(prog)]:
            for det in (-0.08, 0.0, 0.07):
                fr = hz(m) * 2 ** (det / 12); ph = rng.uniform(0, 6.3)
                seg += np.sin(2 * np.pi * fr * tt + ph) + 0.15 * np.sin(4 * np.pi * fr * tt + ph)
        out[a:b] += 0.012 * seg * env
    # dedilhado (Karplus-Strong, timbre de guzheng) na pentatônica de Ré: Ré Mi Fá♯ Lá Si Ré Mi
    escala = [55, 57, 59, 60, 62, 64, 65, 67]   # Sol Lá Si Dó Ré Mi Fá Sol
    cordas = {}
    for m in escala:
        L = int(SR / hz(m)); n = int(1.8 * SR)
        buf = list(rng.uniform(-1, 1, L)); y = np.empty(n)
        for i in range(n):
            y[i] = buf[i % L]
            buf[i % L] = 0.996 * 0.5 * (buf[i % L] + buf[(i + 1) % L])
        cordas[m] = y
    passo = 0.0
    while passo < dur - 2:
        passo += rng.choice([1.5, 2.25, 3.0, 4.5])
        if passo >= dur - 1: break
        y = cordas[int(rng.choice(escala))] * rng.uniform(0.6, 1.0)
        i0 = int(passo * SR); i1 = min(N, i0 + len(y))
        out[i0:i1] += 0.035 * y[: i1 - i0]
    # fade in/out
    fi = int(2 * SR); out[:fi] *= np.linspace(0, 1, fi); out[-int(3 * SR):] *= np.linspace(1, 0, int(3 * SR))
    return out / (np.max(np.abs(out)) + 1e-9) * 0.5


def ducking(voz, musica, base_db=-21, sob_voz_db=-33):
    """Ganho da trilha: base_db nas pausas, sob_voz_db quando há voz (ataque 40 ms, soltura 400 ms)."""
    w = int(0.02 * SR); n = len(voz) // w + 1
    pad = np.zeros(n * w); pad[: len(voz)] = voz
    rms = np.sqrt(np.mean(pad.reshape(n, w) ** 2, axis=1))
    alvo = np.where(20 * np.log10(rms + 1e-9) > -38, sob_voz_db, base_db).astype(float)
    g = np.empty(n); g[0] = alvo[0]
    at, rel = 1 - math.exp(-0.02 / 0.04), 1 - math.exp(-0.02 / 0.4)
    for i in range(1, n):
        k = at if alvo[i] < g[i - 1] else rel
        g[i] = g[i - 1] + k * (alvo[i] - g[i - 1])
    ganho = np.repeat(10 ** (g / 20), w)[: len(musica)]
    return musica * ganho


def srt_ts(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def legendas(blocos):
    """Quebra cada bloco em legendas de até ~84 caracteres (2 linhas), com tempo proporcional ao texto."""
    itens = []
    for b in blocos:
        txt = re.sub(r"\s+", " ", TAG.sub("", b.get("tela", b["texto"]))).strip()   # "tela" = grafia correta (o "texto" é a grafia para a voz)
        frases = re.split(r"(?<=[.?!:])\s+", txt)
        pedacos = []
        for fr in frases:
            palavras, cur = fr.split(), ""
            for p in palavras:
                if len(cur) + len(p) + 1 > 84 and cur:
                    pedacos.append(cur); cur = p
                else:
                    cur = f"{cur} {p}".strip()
            if cur: pedacos.append(cur)
        tot = sum(len(p) for p in pedacos)
        t = b["ini"]; span = b["fim"] - b["ini"]
        for p in pedacos:
            d = span * len(p) / tot
            if len(p) > 42:   # 2 linhas equilibradas
                ws = p.split(); best = min(range(1, len(ws)), key=lambda i: abs(len(" ".join(ws[:i])) - len(" ".join(ws[i:]))))
                p = " ".join(ws[:best]) + "\n" + " ".join(ws[best:])
            itens.append((t, t + d, p)); t += d
    return "\n".join(f"{i}\n{srt_ts(a)} --> {srt_ts(z - 0.02)}\n{p}\n" for i, (a, z, p) in enumerate(itens, 1))


def main():
    blocos = json.load(open(V / "blocos.json"))
    sb = json.load(open(V / "storyboard.json"))["planos"]
    caps_ini = {p["bloco"] for p in sb if "capítulo:" in p["nota"]}

    gap = lambda b: GAP_CAP if b["id"] in caps_ini else GAP_IDEIA if b.get("ideia") else GAP   # silêncio antes do bloco

    # 1) voz: blocos aparados e encadeados
    partes, t = [np.zeros(int(HEAD * SR))], HEAD
    for i, b in enumerate(blocos):
        if i:
            partes.append(np.zeros(int(gap(b) * SR))); t += gap(b)
        x = aparar(ler_mp3(V / "audio" / f"{b['id']}.mp3"))
        b["ini"] = round(t, 3); t += len(x) / SR; b["fim"] = round(t, 3)
        partes.append(x)
    partes.append(np.zeros(int(TAIL * SR)))
    voz = np.concatenate(partes)
    voz *= 10 ** (-3 / 20) / (np.max(np.abs(voz)) + 1e-9)   # pico em -3 dBFS; o loudnorm acerta o volume final
    dur = len(voz) / SR
    (V / "public/audio").mkdir(parents=True, exist_ok=True)
    salvar(V / "public/audio/voz.wav", voz)
    tr = trilha(dur); tr = np.pad(tr, (0, max(0, len(voz) - len(tr))))[: len(voz)]   # arredondamento de amostras
    musica = ducking(voz, tr)
    salvar(V / "public/audio/trilha.wav", musica)
    salvar(V / "public/audio/mix_pre.wav", voz + musica)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(V / "public/audio/mix_pre.wav"),
                    "-af", "loudnorm=I=-15:TP=-1.5:LRA=11", "-ar", str(SR), "-ac", "2", str(V / "public/audio/mix.wav")], check=True)
    (V / "public/audio/mix_pre.wav").unlink()

    # 2) planos reescalados: cada bloco ocupa do início dele ao início do próximo
    por_bloco = {}
    for p in sb: por_bloco.setdefault(p["bloco"], []).append(p)
    total_frames = int(math.ceil(dur * FPS))
    shots, cards, caps = [], [], []
    for i, b in enumerate(blocos):
        a = 0 if i == 0 else b["ini"] - gap(b) / 2
        z = dur if i == len(blocos) - 1 else blocos[i + 1]["ini"] - gap(blocos[i + 1]) / 2
        ps = por_bloco[b["id"]]
        est = sum(p["fim"] - p["ini"] for p in ps)
        acc = a
        for p in ps:
            ini = acc; acc += (p["fim"] - p["ini"]) / est * (z - a)
            shots.append({"from": round(ini * FPS), "img": p["imagem"], "chave": p["chave"], "enq": p["enq"], "mov": p["mov"],
                          "nova": p["nova"], "bloco": p["bloco"], "trecho": p["trecho"], "rot": p.get("rot")})
            m = re.search(r"cartão de data: ([^;]+)", p["nota"])
            if m: cards.append({"from": round(b["ini"] * FPS), "text": m.group(1).strip()})
            m = re.search(r"capítulo: ([^;]+)", p["nota"])
            if m: caps.append({"from": round(ini * FPS), "t": round(ini, 2), "title": m.group(1).strip(), "bloco": b["id"]})
    for k, s in enumerate(shots):
        nxt = shots[k + 1]["from"] if k + 1 < len(shots) else total_frames
        s["dur"] = nxt - s["from"]
    (V / "src").mkdir(exist_ok=True)
    json.dump({"fps": FPS, "frames": total_frames, "shots": shots, "cards": cards, "chapters": caps},
              open(V / "src/timeline.json", "w"), ensure_ascii=False, indent=0)

    # 3) imagens no public/ (hard links)
    (V / "public/img").mkdir(parents=True, exist_ok=True)
    for f in (V / "imagens").glob("*.jpg"):
        dst = V / "public/img" / f.name
        if dst.is_symlink() or (dst.exists() and not dst.samefile(f)): dst.unlink()   # refaz links de outra versão
        if not dst.exists(): dst.hardlink_to(f)

    # 4) legendas (.srt separado) e tempos reais
    (V / "out").mkdir(exist_ok=True); (V / "qa").mkdir(exist_ok=True)
    (V / "out/legendas.srt").write_text(legendas(blocos))
    json.dump([{k: b[k] for k in ("id", "ini", "fim")} for b in blocos], open(V / "qa/blocos.json", "w"), indent=0)
    json.dump(caps, open(V / "qa/capitulos.json", "w"), ensure_ascii=False, indent=1)
    durs = [s["dur"] / FPS for s in shots]
    print(json.dumps({"duracao_s": round(dur, 1), "planos": len(shots), "plano_min_s": round(min(durs), 2),
                      "plano_max_s": round(max(durs), 2), "plano_medio_s": round(sum(durs) / len(durs), 2),
                      "cortes_por_min": round(len(shots) / dur * 60, 1), "cartoes": len(cards), "rotulos": sum(1 for s in shots if s.get("rot"))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
