#!/usr/bin/env python3
"""Experimento A/B da narração (vídeo 003, feedback "narração robótica" do Rodrigo, 04/11/2026).

Uso (na raiz do repo): tools/.venv/bin/python canais/historia-ptbr/videos/003-ira/amostras-voz/ab.py [gerar|medir]
Gera as variações do hook em amostras-voz/<VAR>.wav e mede: duração, palavras/min de articulação, pausas,
variação de entonação (desvio-padrão do F0 em semitons, Praat/parselmouth) e concordância do Whisper.
Custo: registrado em financas.consumo (ref_id=5).
"""
import difflib, json, os, re, subprocess, sys, unicodedata, wave
from pathlib import Path
import numpy as np

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[4] / "tools"))
import yaml  # noqa: E402
from tts_fish import chave, gerar, PRECO_POR_MI_BYTES  # noqa: E402
from db import tentar  # noqa: E402

SR = 44100
VIDEO_ID = 5
CFG = yaml.safe_load(open(AQUI.parents[4] / "canais/historia-ptbr/canal.yaml"))["voz"]
TAG = re.compile(r"\[[^\]]*\]\s*")

# ── Texto A: como o 002 foi escrito (blocos curtos, [break] dentro do bloco, tag de tom por bloco) ──
TEXTO_A = [
    ("[slightly dramatic] Pérsia, quinhentos e vinte e dois antes de Cristo. Seis nobres precisam decidir quem vai governar o maior império do mundo. [break] A regra é estranha: ao nascer do sol, o cavalo que relinchar primeiro escolhe o rei.", False),
    ("[curious] Um deles, Dario, tem um cavalariço esperto. Na noite anterior, ele leva o cavalo até aquele lugar exato, junto com uma égua. [break] De manhã, o cavalo passa por ali, sente o cheiro e relincha.", False),
    ("[amazed] Dario vira rei de um império que ia do Egito até a Índia. [break] Um império escolhido por um cavalo. Pelo menos, é assim que Heródoto conta.", False),
    ("[serious] Essa é a história inteira do Irã. Um país invadido por gregos, árabes, mongóis e turcos, [break] e que, toda vez, acabou ensinando os invasores a viver como persas.", True),
    ("Como? E o que esse cavalo tem a ver com o Irã de hoje? [long-break] Guarde esse cavalo. Ele volta no final.", False),
]
# ── Texto B: reescrito para a fala (frases curtas, vírgula de respiração, reticências na virada, sem [break]) ──
TEXTO_B = [
    "Pérsia. Quinhentos e vinte e dois antes de Cristo. Seis nobres têm um problema: quem vai governar o maior império do mundo? A solução é… estranha. Ao nascer do sol, eles vão sair a cavalo. E o cavalo que relinchar primeiro, escolhe o rei.",
    "Um deles se chama Dario. E Dario tem um cavalariço esperto. Na noite anterior, ele leva o cavalo até aquele lugar exato, junto com uma égua. De manhã, o cavalo passa por ali, sente o cheiro… e relincha.",
    "Dario vira rei. Rei de um império que ia do Egito até a Índia. Um império escolhido, literalmente, por um cavalo. Pelo menos, é assim que Heródoto conta.",
    "Essa é a história inteira do Irã. Um país invadido por gregos, árabes, mongóis e turcos. E que, toda vez, acabou ensinando os invasores a viver como persas. Como? E o que esse cavalo tem a ver com o Irã de hoje? Guarde esse cavalo. Ele volta no final.",
]
# ── Texto F: B + tags livres de direção de narrador (s2 aceita descrição em linguagem natural), 1 por parágrafo ──
TAGS_F = ["[storyteller voice, intrigued]", "[low voice, conspiratorial]", "[amazed]", "[serious, calm]"]
TEXTO_F = [f"{t} {p}" for t, p in zip(TAGS_F, TEXTO_B)]

FRASE = re.compile(r"(?<=[.?!])\s+(?=[A-ZÀ-Ú])")

VARS = {
    # nome: (lista de (texto, gap_antes_s), parâmetros extras da API, pós-processamento)
    "A-atual": ([(t, 0.9 if i else 0.0) if ideia else (t, 0.35 if i else 0.0) for i, (t, ideia) in enumerate(TEXTO_A)], {}, None),
    "B-texto-falado": ([(p, 0.9 if i else 0.0) for i, p in enumerate(TEXTO_B)], {}, None),
    "C-por-frase-silencio": ([(f, (0.75 if j == 0 else 0.32) if (i or j) else 0.0) for i, p in enumerate(TEXTO_B)
                              for j, f in enumerate(FRASE.split(p))], {}, None),
    "D-temp-0.9": ([(p, 0.9 if i else 0.0) for i, p in enumerate(TEXTO_B)], {"temperature": 0.9, "top_p": 0.9}, None),
    "E-B+pausas-alongadas": ("B-texto-falado", {}, "alongar"),
    "F-tags-narrador": ([(p, 0.9 if i else 0.0) for i, p in enumerate(TEXTO_F)], {}, "alongar"),
    # 2ª rodada: tomadas repetidas (ruído entre gerações) e combinações
    "B-take2": ([(p, 0.9 if i else 0.0) for i, p in enumerate(TEXTO_B)], {}, None),
    "C-take2": ([(f, (0.75 if j == 0 else 0.32) if (i or j) else 0.0) for i, p in enumerate(TEXTO_B)
                 for j, f in enumerate(FRASE.split(p))], {}, None),
    "F-take2": ([(p, 0.9 if i else 0.0) for i, p in enumerate(TEXTO_F)], {}, "alongar"),
    "G-por-frase+tags": ([(f"{TAGS_F[i]} {f}" if j == 0 else f, (0.75 if j == 0 else 0.32) if (i or j) else 0.0)
                          for i, p in enumerate(TEXTO_B) for j, f in enumerate(FRASE.split(p))], {}, None),
    "H-tags-vel-0.97": ([(p, 0.9 if i else 0.0) for i, p in enumerate(TEXTO_F)], {"prosody": {"speed": 0.97}}, "alongar"),
}


def mp3_para_np(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def salvar(p, x):
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def aparar(x, lim_db=-45, cauda=0.15):
    w = int(0.01 * SR); n = len(x) // w
    rms = 20 * np.log10(np.sqrt(np.mean(x[: n * w].reshape(n, w) ** 2, axis=1) + 1e-12))
    v = np.where(rms > lim_db)[0]
    return x if not len(v) else x[max(0, v[0] * w - int(0.05 * SR)): min(len(x), (v[-1] + 1) * w + int(cauda * SR))]


def silencios(x, lim_db=-40, minimo=0.12):
    """Intervalos (ini, fim) em s de silêncio interno ≥ minimo."""
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
                out.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    return out


def alongar(x, alvo=0.34, minimo=0.15):
    """Pausa natural ≥ minimo (fim de frase) vira pelo menos `alvo` s; vírgulas curtas ficam como estão."""
    partes, ult = [], 0
    for a, b in silencios(x, minimo=minimo):
        ia, ib = int(a * SR), int(b * SR)
        partes.append(x[ult:ib])
        falta = alvo - (b - a)
        if falta > 0:
            partes.append(np.zeros(int(falta * SR)))
        ult = ib
    partes.append(x[ult:])
    return np.concatenate(partes)


def gerar_var(nome, key, total):
    seg, extra, pos = VARS[nome]
    pasta = AQUI / "trechos" / nome
    pasta.mkdir(parents=True, exist_ok=True)
    if isinstance(seg, str):  # reaproveita os trechos de outra variação (sem custo)
        seg, src = VARS[seg][0], AQUI / "trechos" / seg
    else:
        src = pasta
    for i, (t, _) in enumerate(seg):
        mp3 = src / f"{i:02d}.mp3"
        if not mp3.exists():
            gerar(key, CFG["voz"], CFG["modelo"], CFG.get("velocidade"), t, mp3, extra)
            total[0] += len(t.encode())
    audio = []
    for i, (t, gap) in enumerate(seg):
        x = aparar(mp3_para_np(src / f"{i:02d}.mp3"))
        if pos == "alongar":
            x = alongar(x)
        audio += [np.zeros(int(gap * SR)), x]
    salvar(AQUI / f"{nome}.wav", np.concatenate([np.zeros(int(0.25 * SR))] + audio + [np.zeros(int(0.5 * SR))]))


def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    return re.findall(r"[a-z0-9]+", "".join(c for c in t if not unicodedata.combining(c)))


_m = None


def whisper(x):
    global _m
    from faster_whisper import WhisperModel
    _m = _m or WhisperModel("small", device="cpu", compute_type="int8")
    y = x[:: 1].astype(np.float32)
    # reamostra 44,1 kHz → 16 kHz
    idx = np.arange(0, len(y), SR / 16000)
    y16 = np.interp(idx, np.arange(len(y)), y).astype(np.float32)
    segs, _ = _m.transcribe(y16, language="pt", vad_filter=False)
    return " ".join(s.text for s in segs)


def medir(nome):
    import parselmouth
    p = AQUI / f"{nome}.wav"
    x = mp3_para_np(p)
    dur = len(x) / SR
    sil = silencios(x, minimo=0.12)
    pausas = [b - a for a, b in sil]
    snd = parselmouth.Sound(str(p))
    f0 = snd.to_pitch(time_step=0.01, pitch_floor=65, pitch_ceiling=350).selected_array["frequency"]
    f0 = f0[f0 > 0]
    st = 12 * np.log2(f0 / np.median(f0))
    # monotonia dentro da frase: desvio do F0 (st) em cada trecho falado entre pausas ≥ 0,25 s, em média
    cortes = [0.0] + [b for a, b in sil if b - a >= 0.25] + [dur]
    pitch_t = snd.to_pitch(time_step=0.01, pitch_floor=65, pitch_ceiling=350)
    ff = pitch_t.selected_array["frequency"]; tt = pitch_t.xs()
    intra, durs = [], []
    for a, b in zip(cortes, cortes[1:]):
        v = ff[(tt >= a) & (tt < b) & (ff > 0)]
        if len(v) > 30:
            intra.append(np.std(12 * np.log2(v / np.median(f0))))
            durs.append(b - a)
    pz = [d for d in pausas if d >= 0.25]
    texto = " ".join(TAG.sub("", t) for t, _ in (VARS[nome][0] if not isinstance(VARS[nome][0], str) else VARS[VARS[nome][0]][0]))
    ref = norm(texto)
    hyp_txt = whisper(x)
    hyp = norm(hyp_txt)
    sim = difflib.SequenceMatcher(None, ref, hyp, autojunk=False).ratio()
    falado = dur - 0.75 - sum(pausas)
    tags = [w for w in hyp if w in {"break", "curious", "serious", "amazed", "dramatic", "storyteller", "voice", "conspiratorial", "calm", "intrigued"}]
    return {"var": nome, "dur_s": round(dur, 1), "palavras": len(ref), "ppm_total": round(len(ref) / dur * 60),
            "ppm_articulacao": round(len(ref) / falado * 60), "pausas_>=0.25s": sum(d >= 0.25 for d in pausas),
            "pausa_media_s": round(float(np.mean(pausas)), 2) if pausas else 0, "pct_silencio": round(100 * sum(pausas) / dur),
            "f0_desvio_st": round(float(np.std(st)), 2), "f0_faixa_p10_p90_st": round(float(np.percentile(st, 90) - np.percentile(st, 10)), 2),
            "f0_intra_frase_st": round(float(np.mean(intra)), 2), "cv_trechos": round(float(np.std(durs) / np.mean(durs)), 2),
            "cv_pausas": round(float(np.std(pz) / np.mean(pz)), 2) if pz else 0,
            "whisper_pct": round(100 * sim, 1), "tags_faladas": tags, "whisper": hyp_txt.strip()}


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "gerar"
    so = sys.argv[2:] or list(VARS)
    if modo == "gerar":
        key, total = chave(), [0]
        for n in so:
            gerar_var(n, key, total)
            print(n, "ok")
        custo = total[0] * PRECO_POR_MI_BYTES[CFG["modelo"]] / 1e6
        if total[0]:
            def reg(con):
                c = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='Fish Audio'").fetchone()
                con.execute("INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
                            " VALUES ('youtube','historia-ptbr','Fish Audio',%s,%s,'bytes',%s,'USD',%s,'youtube.video',%s,'A/B de voz do hook (amostras-voz/ab.py)')",
                            (f"tts {CFG['modelo']}", total[0], custo, custo * float(c[0]) if c else None, VIDEO_ID))
            tentar(reg)
        print(f"{total[0]} bytes · US$ {custo:.4f}")
    else:
        res = [medir(n) for n in so]
        json.dump(res, open(AQUI / "medidas.json", "w"), ensure_ascii=False, indent=1)
        for r in res:
            print({k: v for k, v in r.items() if k != "whisper"})


if __name__ == "__main__":
    main()
