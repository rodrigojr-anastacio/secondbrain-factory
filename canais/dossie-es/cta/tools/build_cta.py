#!/usr/bin/env python3
"""CTA genérico da HQ "Expedientes Secretos" (Dossier en Minutos, 24/11/2026): áudio, tempos e links do bloco de 16,4 s.

Uso (na pasta cta/): ~/workspace/fabrica-youtube/tools/.venv/bin/python tools/build_cta.py
Entradas: voz/CTA.mp3 (Fish, voz do canal, 1,0× + ffmpeg atempo 1,25) e voz/palavras.json (tempos de palavra do Whisper),
          capas/páginas/wallpaper de ../produtos/hq/ (hard links em public/img; o Remotion não serve symlink).
Saídas:   cta-hq.wav (só a voz, 48 kHz mono, começa em VOZ_OFF dentro do bloco), cta-sfx.wav (só os SFX, para o encaixe
          num vídeo, onde a trilha do vídeo continua com ducking), public/audio/mix.wav (voz + trilha + SFX, -15 LUFS,
          o áudio do cta-hq.mp4 avulso), src/tempos.json (eventos sincronizados com a fala) e cta.json.
A trilha e os SFX são os do canal (mesmas funções do tools/build.py dos vídeos 016/017: drone + pulso, carimbo, teclas).
"""
import json, math, subprocess, wave
from pathlib import Path
import numpy as np

C = Path(__file__).resolve().parent.parent
HQ = C.parent / "produtos" / "hq"
SR, FPS = 48000, 30
DUR = 16.4            # bloco inteiro (s): Rodrigo aceitou ~16 s (24/11, v2: voz 15,66 s + entrada 0,25 s + respiro; alvo <= 16,5 s)
VOZ_OFF = 0.25        # a voz começa 0,25 s depois do início do bloco
TEXTO = ("Si te están gustando estos expedientes, hay otros que nunca llegaron al canal: los guardamos para un cómic. "
         "Expedientes Secretos. Historias reales de espionaje y, de regalo, póster y fondos de pantalla para tu celular y tu computadora. "
         "El enlace está en la descripción y en el comentario fijado.")
LINKS = {"capa-1.jpg": "capa.jpg", "capa-2.jpg": "capa-2.jpg", "capa-3.jpg": "capa-3.jpg", "pagina-1.jpg": "pagina-1.jpg",
         "pagina-2.jpg": "pagina-2.jpg", "wallpaper-celular.jpg": "wallpaper-celular.jpg", "P203.jpg": "arte/P203.jpg",
         }
# artes reduzidas (jpg) dos pôsteres novos e do wallpaper desktop da HQ #1 (v2, 24/11/2026)
REDUZIDAS = {"poster-C.jpg": ("001/pacote/poster-C-com-titulo.png", 1100), "poster-A.jpg": ("001/pacote/poster-A-com-titulo.png", 1100),
             "desktop.jpg": ("001/pacote/wallpaper-1-desktop-3840x2160.jpg", 1600)}   # (origem, maior lado em px)


def ler_mp3(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def salvar(p, x, canais=1):
    x = np.clip(x, -1, 1)
    with wave.open(str(p), "wb") as w:
        w.setnchannels(canais); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def trilha(dur):
    """Mesma trilha do canal (build.py 016/017): drone Ré+Lá, pads menores, pulso 'tum-tum' a cada 1,6 s."""
    rng = np.random.default_rng(7)
    N = int(dur * SR); t = np.arange(N) / SR
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    out = np.zeros(N)
    out += 0.06 * np.sin(2 * np.pi * hz(38) * t) * (0.75 + 0.25 * np.sin(2 * np.pi * t / 23))
    out += 0.03 * np.sin(2 * np.pi * hz(45) * t + 1) * (0.7 + 0.3 * np.sin(2 * np.pi * t / 31 + 2))
    prog = [[50, 53, 57, 62], [46, 50, 53, 58]]
    CH = 7.5
    for c in range(int(dur / CH) + 2):
        s0 = int((c * CH - 3) * SR); L = int((CH + 6) * SR)
        a_, b_ = max(0, s0), min(N, s0 + L)
        if a_ >= b_: continue
        tt = np.arange(a_, b_) / SR - (c * CH - 3)
        env = (np.clip(tt / 3, 0, 1) * np.clip((CH + 6 - tt) / 3, 0, 1)) ** 1.5
        seg = np.zeros(b_ - a_)
        for m in prog[c % len(prog)]:
            for det in (-0.07, 0.0, 0.06):
                fr = hz(m) * 2 ** (det / 12); ph = rng.uniform(0, 6.3)
                seg += np.sin(2 * np.pi * fr * tt + ph) + 0.1 * np.sin(4 * np.pi * fr * tt + ph)
        out[a_:b_] += 0.010 * seg * env
    k = int(0.35 * SR); kt = np.arange(k) / SR
    kick = np.sin(2 * np.pi * (45 * kt + 25 * (1 - np.exp(-kt * 18)) / 18)) * np.exp(-kt * 9)
    p = 0.4
    while p < dur - 0.5:
        for dp, g in ((0, 1.0), (0.28, 0.6)):
            i0 = int((p + dp) * SR); i1 = min(N, i0 + k)
            out[i0:i1] += 0.16 * g * kick[: i1 - i0]
        p += 1.6
    fi = int(0.4 * SR); out[:fi] *= np.linspace(0, 1, fi); out[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))
    return out / (np.max(np.abs(out)) + 1e-9) * 0.5


def ducking(voz, musica, base_db=-21, sob_voz_db=-33):
    w = int(0.02 * SR); n = len(voz) // w + 1
    pad = np.zeros(n * w); pad[: len(voz)] = voz
    rms = np.sqrt(np.mean(pad.reshape(n, w) ** 2, axis=1))
    alvo = np.where(20 * np.log10(rms + 1e-9) > -38, sob_voz_db, base_db).astype(float)
    g = np.empty(n); g[0] = alvo[0]
    at, rel = 1 - math.exp(-0.02 / 0.04), 1 - math.exp(-0.02 / 0.4)
    for i in range(1, n):
        k = at if alvo[i] < g[i - 1] else rel
        g[i] = g[i - 1] + k * (alvo[i] - g[i - 1])
    return musica * np.repeat(10 ** (g / 20), w)[: len(musica)]


def sfx(dur, ev):
    """Carimbo do canal (baque grave + estalo), folha virando (sopro de ruído filtrado que sobe e desce) e 'whoosh'."""
    rng = np.random.default_rng(3)
    N = int(dur * SR); out = np.zeros(N)
    m = int(0.5 * SR); mt = np.arange(m) / SR
    baque = np.sin(2 * np.pi * (60 * mt + 60 * (1 - np.exp(-mt * 25)) / 25)) * np.exp(-mt * 14) + 0.5 * rng.uniform(-1, 1, m) * np.exp(-mt * 90)

    def por(t0, x, g):
        i0 = int(t0 * SR); i1 = min(N, i0 + len(x))
        if 0 <= i0 < N: out[i0:i1] += g * x[: i1 - i0]

    for t0 in ev["carimbos"]:
        por(t0, baque, 0.35)
    for t0, d in ev["folhas"]:   # folha: ruído passa-banda com envelope em sino + leve estalo do papel no fim
        n = int(d * SR); tt = np.arange(n) / SR
        r = rng.uniform(-1, 1, n)
        r = np.convolve(r, np.ones(6) / 6, "same") - np.convolve(r, np.ones(40) / 40, "same")
        env = np.sin(np.pi * np.clip(tt / d, 0, 1)) ** 1.6
        x = r * env * 1.6
        k = int(0.04 * SR); x[-k:] += rng.uniform(-1, 1, k) * np.exp(-np.arange(k) / SR * 120) * 0.5
        por(t0, x, 0.22)
    for t0 in ev["whoosh"]:
        n = int(0.45 * SR); tt = np.arange(n) / SR
        r = np.convolve(rng.uniform(-1, 1, n), np.ones(12) / 12, "same")
        por(t0, r * np.sin(np.pi * tt / 0.45) ** 2, 0.18)
    return out


def main():
    # 1) links das artes (refaça depois de trocar uma capa: as capas saem de ../produtos/hq/src/hq.py --capa)
    (C / "public/img").mkdir(parents=True, exist_ok=True); (C / "public/audio").mkdir(parents=True, exist_ok=True)
    for dst, src in LINKS.items():
        d, s = C / "public/img" / dst, HQ / src
        if d.exists() or d.is_symlink(): d.unlink()
        d.hardlink_to(s)

    from PIL import Image
    for dst, (src, mx) in REDUZIDAS.items():
        im = Image.open(HQ / src).convert("RGB"); im.thumbnail((mx, mx), Image.LANCZOS)
        im.save(C / "public/img" / dst, quality=88)

    # 2) voz no bloco
    v = ler_mp3(C / "voz/CTA.mp3")
    v *= 10 ** (-3 / 20) / (np.max(np.abs(v)) + 1e-9)
    salvar(C / "cta-hq.wav", v)
    N = int(DUR * SR)
    voz = np.zeros(N); i0 = int(VOZ_OFF * SR); voz[i0:i0 + len(v)] = v[: N - i0]
    fim_voz = VOZ_OFF + len(v) / SR
    assert fim_voz <= DUR - 0.2, f"voz passa do bloco: {fim_voz:.2f} s"

    # 3) eventos sincronizados com as palavras reais (Whisper)
    pal = [(w, a + VOZ_OFF, z + VOZ_OFF) for w, a, z in json.load(open(C / "voz/palavras.json"))]
    def t(palavra, n=1):
        achadas = [p for p in pal if p[0].strip(".,:").lower() == palavra]
        return achadas[n - 1]
    ev = {
        "dur": DUR, "fps": FPS, "voz_off": VOZ_OFF, "voz_fim": round(fim_voz, 3),
        "carimbo2": round(t("otros")[1], 2),                 # CLASIFICADO na capa #2
        "carimbo3": round(t("llegaron")[1], 2),              # CLASIFICADO na capa #3
        "zoom": round(t("canal")[2] + 0.05, 2),              # #1 vai ao centro e cresce
        "abre": round(t("guardamos")[1], 2),                 # a capa abre
        "folheia": round(t("expedientes", 2)[1] + 0.1, 2),   # vira a pág. 1 (aparece a 2)
        "cena2": round(t("historias")[1] - 0.3, 2),          # parede: pôster
        "poster": round(t("póster")[1] - 0.1, 2),            # 2º pôster (A) ao lado do C
        "celular": round(t("celular")[1] - 0.2, 2),          # celular com o wallpaper
        "notebook": round(t("computadora")[1] - 0.2, 2),     # notebook com o wallpaper desktop
        "regalo": round(t("regalo")[1], 2),                  # carimbo DE REGALO
        "banner": round(t("el", 1)[1] - 0.15, 2),            # banner do link
    }
    ev["carimbos"] = [ev["carimbo2"] + 0.2, ev["carimbo3"] + 0.2, ev["regalo"] + 0.2]   # o carimbo bate 6 quadros depois de surgir
    ev["folhas"] = [(ev["abre"] + 0.05, 0.75), (ev["folheia"] + 0.05, 0.7)]
    ev["whoosh"] = [0.05, ev["zoom"], ev["cena2"], ev["banner"]]
    ev["palavras"] = [[w, round(a, 2), round(z, 2)] for w, a, z in pal]
    json.dump(ev, open(C / "src/tempos.json", "w"), ensure_ascii=False, indent=1)

    # 4) trilha com ducking + SFX → mix do mp4 avulso; SFX sozinho para o encaixe
    efeitos = sfx(DUR, ev)
    salvar(C / "cta-sfx.wav", efeitos)
    mix = voz + ducking(voz, trilha(DUR)) + efeitos
    salvar(C / "public/audio/mix_pre.wav", mix)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(C / "public/audio/mix_pre.wav"), "-af", "loudnorm=I=-15:TP=-1.5:LRA=11",
                    "-ar", str(SR), "-ac", "2", str(C / "public/audio/mix.wav")], check=True)
    (C / "public/audio/mix_pre.wav").unlink()

    # 5) cta.json: o que o build.py de um vídeo precisa para encaixar o bloco
    json.dump({
        "versao": "2026-11-24-v2",
        "duracao_s": DUR, "frames": int(DUR * FPS), "fps": FPS,
        "voz_off_s": VOZ_OFF, "voz_fim_s": round(fim_voz, 3),
        "texto": TEXTO,
        "legenda": [  # linhas do .srt (tempos relativos ao início do bloco), cortadas nas pausas reais da fala
            {"ini": VOZ_OFF, "fim": round(t("cómic")[2], 2), "texto": "Si te están gustando estos expedientes, hay otros que nunca\nllegaron al canal: los guardamos para un cómic."},
            {"ini": round(t("expedientes", 2)[1], 2), "fim": round(t("computadora")[2], 2), "texto": "Expedientes Secretos. Historias reales de espionaje y, de regalo,\npóster y fondos de pantalla para tu celular y tu computadora."},
            {"ini": round(t("el", 1)[1], 2), "fim": round(fim_voz, 2), "texto": "El enlace está en la descripción\ny en el comentario fijado."},
        ],
        "arquivos": {"video": "cta-hq.mp4", "voz": "cta-hq.wav", "sfx": "cta-sfx.wav"},
        "interruptor": "ATIVO (1ª linha = link da Hotmart); sem ele o build.py ignora o CTA",
        "voz": {"motor": "fish", "modelo": "s2.1-pro", "voz": "ac594943984a47e7a827416eb263c7b1", "velocidade": 1.0, "atempo": 1.25, "pausa_frase_s": 0.25},
    }, open(C / "cta.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: ev[k] for k in ("voz_fim", "carimbo2", "carimbo3", "zoom", "abre", "folheia", "cena2", "poster", "celular", "notebook", "regalo", "banner")}))


if __name__ == "__main__":
    main()
