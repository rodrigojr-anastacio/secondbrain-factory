#!/usr/bin/env python3
"""Montagem do 001-midway (Clearance Required): voz real + storyboard.json → timeline do Remotion, trilha com ducking, .srt e capítulos.

Uso (na pasta do vídeo): ~/workspace/fabrica-youtube/tools/.venv/bin/python tools/build.py [--sem-midia]
Entradas: blocos.json, storyboard.json, audio/<bloco>.mp3, qa/whisper.json (tools/compara_voz.py), midia/, midia.csv, SCRIPT.md
Saídas:   audio/final/{voz,trilha,mix}.wav (fora do public/: não vai no bundle), public/img/*.jpg (reduzidas), public/clips/<plano>.mp4 (trechos de filme cortados,
          sem áudio, já na velocidade), src/timeline.json, out/legendas.srt, qa/capitulos.json, qa/tempos.json
Regras do Rodrigo (12/11/2026): filme do John Ford só em trechos SEM áudio e < 7 s cada (FILME_MAX); sem 3D.
Cortes: cada plano começa na 1ª palavra do seu "em" (tempo do Whisper), 0,12 s antes; o 1º plano de um bloco começa no meio da pausa.
"""
import csv, json, math, re, subprocess, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
V = Path(__file__).resolve().parent.parent
SR, FPS, W, H = 48000, 30, 1920, 1080
GAP, GAP_IDEIA, GAP_CAP, HEAD, TAIL = 0.35, 0.9, 1.5, 0.3, 2.5
FILME_MAX, VEL_MIN = 6.9, 0.52
LEAD = 0.12
SEM_MIDIA = "--sem-midia" in sys.argv


# ───────────── áudio ─────────────
def ler_mp3(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def aparar(x, lim_db=-45, cab=0.04, cauda=0.15):
    w = int(0.01 * SR); n = len(x) // w
    rms = np.sqrt(np.mean(x[: n * w].reshape(n, w) ** 2, axis=1) + 1e-12)
    voz = np.where(20 * np.log10(rms) > lim_db)[0]
    if not len(voz):
        return x, 0
    a = max(0, voz[0] * w - int(cab * SR)); z = min(len(x), (voz[-1] + 1) * w + int(cauda * SR))
    y = x[a:z].copy(); f = int(0.008 * SR)
    y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y, a / SR


def salvar(p, x, canais=1):
    x = np.clip(x, -1, 1)
    with wave.open(str(p), "wb") as w:
        w.setnchannels(canais); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def trilha(dur):
    """Trilha documental sóbria, sintetizada aqui (nada de terceiros): pad de cordas lento em Ré (Ré–Si♭–Fá–Dó, modal),
    baixo longo e um piano suave e raro. Sem percussão: o canal é calmo, documental."""
    rng = np.random.default_rng(11)
    N = int(dur * SR); t = np.arange(N) / SR
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    out = np.zeros(N)
    prog = [[50, 57, 62, 65], [46, 53, 58, 62], [41, 48, 57, 60], [48, 55, 60, 64]]   # Rém, Si♭, Fá, Dó
    CH = 12.0
    for c in range(int(dur / CH) + 2):
        s0 = int((c * CH - 3) * SR); L = int((CH + 6) * SR)
        a_, b_ = max(0, s0), min(N, s0 + L)
        if a_ >= b_: continue
        tt = np.arange(a_, b_) / SR - (c * CH - 3)
        env = (np.clip(tt / 4.5, 0, 1) * np.clip((CH + 6 - tt) / 4.5, 0, 1)) ** 1.4
        seg = np.zeros(b_ - a_)
        notas = prog[c % len(prog)]
        for k, m in enumerate(notas):
            for det in (-0.06, 0.0, 0.05):
                fr = hz(m) * 2 ** (det / 12); ph = rng.uniform(0, 6.3)
                vib = 1 + 0.002 * np.sin(2 * np.pi * 5.2 * tt + ph)
                seg += (np.sin(2 * np.pi * fr * tt * vib + ph) + 0.25 * np.sin(4 * np.pi * fr * tt + ph) + 0.08 * np.sin(6 * np.pi * fr * tt)) * (0.6 if k == 0 else 1)
        bx = np.sin(2 * np.pi * hz(notas[0] - 12) * tt) * 2.2
        out[a_:b_] += 0.008 * (seg + bx) * env
    # piano suave: uma nota da escala a cada ~6–9 s
    escala = [62, 65, 69, 70, 72, 74, 77]
    p = 4.0
    while p < dur - 4:
        n = int(4 * SR); tt = np.arange(n) / SR; m = escala[int(rng.integers(len(escala)))]
        nota = sum(np.sin(2 * np.pi * hz(m) * h * tt) * np.exp(-tt * (1.2 + 0.9 * h)) / h for h in (1, 2, 3, 4))
        nota *= np.clip(tt / 0.006, 0, 1)
        i0 = int(p * SR); i1 = min(N, i0 + n); out[i0:i1] += 0.05 * nota[: i1 - i0]
        p += rng.uniform(6, 9)
    fi = int(2.5 * SR); out[:fi] *= np.linspace(0, 1, fi); out[-int(4 * SR):] *= np.linspace(1, 0, int(4 * SR))
    return out / (np.max(np.abs(out)) + 1e-9) * 0.5


def sfx(dur, papeis, grifos):
    """Papel (folha virando: ruído filtrado com envelope) no começo de cada DocGrifo novo e tecla de máquina de escrever,
    bem baixa, enquanto o grifo corre (biblia/visual.md: SFX mínimos, máquina só no grifo)."""
    rng = np.random.default_rng(5)
    N = int(dur * SR); out = np.zeros(N)
    n = int(0.45 * SR); tt = np.arange(n) / SR
    for t0 in papeis:
        r = rng.uniform(-1, 1, n)
        r = np.convolve(r, np.ones(6) / 6, "same") - np.convolve(r, np.ones(40) / 40, "same")
        env = np.clip(tt / 0.05, 0, 1) * np.exp(-tt * 7) * (1 + 0.6 * np.sin(2 * np.pi * 9 * tt))
        i0 = int(t0 * SR); i1 = min(N, i0 + n)
        if i0 < N: out[i0:i1] += 0.16 * (r * env)[: i1 - i0]
    k = int(0.025 * SR); kt = np.arange(k) / SR
    for t0, t1 in grifos:
        t = t0
        while t < min(t1, t0 + 1.4):
            clic = rng.uniform(-1, 1, k) * np.exp(-kt * 300); clic = np.convolve(clic, np.ones(3) / 3, "same")
            i0 = int(t * SR); i1 = min(N, i0 + k)
            if i0 < N: out[i0:i1] += 0.05 * clic[: i1 - i0] * rng.uniform(0.6, 1)
            t += rng.uniform(0.07, 0.13)
    return out


def ducking(voz, musica, base_db=-19, sob_voz_db=-31):
    w = int(0.02 * SR); n = len(voz) // w + 1
    pad = np.zeros(n * w); pad[: len(voz)] = voz
    rms = np.sqrt(np.mean(pad.reshape(n, w) ** 2, axis=1))
    alvo = np.where(20 * np.log10(rms + 1e-9) > -38, sob_voz_db, base_db).astype(float)
    g = np.empty(n); g[0] = alvo[0]
    at, rel = 1 - math.exp(-0.02 / 0.05), 1 - math.exp(-0.02 / 0.6)
    for i in range(1, n):
        k = at if alvo[i] < g[i - 1] else rel
        g[i] = g[i - 1] + k * (alvo[i] - g[i - 1])
    return musica * np.repeat(10 ** (g / 20), w)[: len(musica)]


# ───────────── texto / tempos ─────────────
sys.path.insert(0, str(Path(__file__).resolve().parent))
from compara_voz import norm  # mesma normalização do QA de voz (números por extenso, sem "and/the/a")


def toks(t):
    return norm(t.replace("Ah-kah-gee", "Akagi"))


def acha_em(em, palavras, desde):
    """Índice da palavra do Whisper onde começa a frase 'em' (≥ desde). Casa as 3 primeiras palavras normalizadas."""
    alvo = toks(em)[:3]
    flat, dono = [], []
    for i, w in enumerate(palavras):
        for tk in toks(w[0]):
            flat.append(tk); dono.append(i)
    import difflib
    T = "".join(alvo)
    melhor, mi = 0.0, None
    for k in range(len(flat)):
        if dono[k] < desde: continue
        S = "".join(flat[k:k + 6])[:len(T)]
        r = difflib.SequenceMatcher(None, T, S).ratio()
        if r > melhor + 1e-9:
            melhor, mi = r, dono[k]
        if r == 1.0:
            break
    return mi if melhor >= 0.75 else None


def ts(s):
    ms = int(round(s * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def fmt(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def legendas(blocos, whisper):
    """Até ~84 caracteres por legenda (2 linhas), tempo pelas palavras do Whisper (proporção de palavras)."""
    itens = []
    for b in blocos:
        txt = re.sub(r"\s+", " ", b["texto"].replace("*", "")).strip()
        ref = txt.split()
        wp = whisper[b["id"]]["palavras"]
        frases = re.split(r"(?<=[.?!])\s+", txt)
        pedacos = []
        for fr in frases:
            cur = ""
            for p in fr.split():
                if len(cur) + len(p) + 1 > 84 and cur:
                    pedacos.append(cur); cur = p
                else:
                    cur = f"{cur} {p}".strip()
            if cur: pedacos.append(cur)
        i = 0
        k = len(wp) / max(1, len(ref))
        for p in pedacos:
            n = len(p.split())
            wi = min(len(wp) - 1, int(i * k)); wf = min(len(wp) - 1, max(wi, int((i + n) * k) - 1))
            a = b["ini"] + wp[wi][1] - b["off"]; z = b["ini"] + wp[wf][2] - b["off"]
            if len(p) > 42:
                ws = p.split(); best = min(range(1, len(ws)), key=lambda j: abs(len(" ".join(ws[:j])) - len(" ".join(ws[j:]))))
                p = " ".join(ws[:best]) + "\n" + " ".join(ws[best:])
            itens.append([max(a, b["ini"]), min(max(z, a + 0.8), b["fim"] + 0.3), p]); i += n
    for j in range(len(itens) - 1):
        itens[j][1] = min(itens[j][1], itens[j + 1][0] - 0.02)
    return "\n".join(f"{i}\n{ts(a)} --> {ts(z)}\n{p}\n" for i, (a, z, p) in enumerate(itens, 1))


# ───────────── mídia ─────────────
def img_publica(arq, crop=None):
    """Cópia reduzida em public/img (docs até 5.600 px no lado maior, fotos até 3.400 px), JPEG q90. Devolve (nome, w, h)."""
    src = V / "midia" / arq
    dst_nome = re.sub(r"\.(png|jpg|jpeg)$", "", arq) + ".jpg"
    dst = V / "public/img" / dst_nome
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        im = Image.open(src)
        im = im.convert("RGB") if im.mode not in ("L", "RGB") else im
        lim = 5600 if arq.startswith("doc_") else 3400
        if max(im.size) > lim:
            f = lim / max(im.size); im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, quality=90)
    with Image.open(dst) as im:
        return dst_nome, im.width, im.height


def clip(p, dur):
    """Corta o trecho do filme (sem áudio), na velocidade do plano, 30 fps, com folga de 0,3 s."""
    dst = V / "public/clips" / f"{p['id']}.mp4"
    precisa = (dur + 0.3) * p["vel"]
    chave = f"{p['arq']}|{p['tin']}|{p['vel']:.3f}|{dur:.2f}"
    marca = dst.with_suffix(".txt")
    if dst.exists() and marca.exists() and marca.read_text() == chave:
        return dst.name
    dst.parent.mkdir(parents=True, exist_ok=True)
    vf = f"yadif=deint=interlaced,setpts=PTS/{p['vel']:.4f},fps={FPS},scale=1440:-2:flags=lanczos"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{p['tin']:.3f}", "-t", f"{precisa:.3f}", "-i", str(V / "midia" / p["arq"]),
                    "-an", "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", str(dst)], check=True)
    marca.write_text(chave)
    return dst.name


# ───────────── mapa 2D (Natural Earth 50m, PD) ─────────────
GEO = None


def simplifica(pts, tol=1.5):
    out = [pts[0]]
    for x, y in pts[1:]:
        if abs(x - out[-1][0]) + abs(y - out[-1][1]) >= tol:
            out.append((x, y))
    return out


def mapa(p, pontos):
    global GEO
    if GEO is None:
        GEO = json.load(open(V / "midia/mapa_base_ne50m_land.geojson"))["features"]
    pts = [pontos[n] for n in p["pontos"]]
    lons = [x for x, _ in pts]; lats = [y for _, y in pts]
    naufr = any("WRECK" in n for n in p["pontos"])
    mn = 6 if naufr else 12
    span = max(max(lons) - min(lons), (max(lats) - min(lats)) * W / H, mn) * (1.35 if len(pts) > 3 else 1.6)
    clon, clat = (max(lons) + min(lons)) / 2, (max(lats) + min(lats)) / 2
    lon0, lat_top = clon - span / 2, clat + span * H / W / 2
    sc = W / span
    pr = lambda lo, la: (round((lo - lon0) * sc, 1), round((lat_top - la) * sc, 1))
    paths = []
    for f in GEO:
        gm = f["geometry"]
        aneis = [gm["coordinates"][0]] if gm["type"] == "Polygon" else [pl[0] for pl in gm["coordinates"]]
        for ring in aneis:
            for off in (0, 360):
                xy = [pr(c[0] + off, c[1]) for c in ring]
                if max(x for x, _ in xy) < -50 or min(x for x, _ in xy) > W + 50 or max(y for _, y in xy) < -50 or min(y for _, y in xy) > H + 50:
                    continue
                xy = simplifica(xy)
                if len(xy) > 2:
                    paths.append("M" + "L".join(f"{x:.0f},{y:.0f}" for x, y in xy) + "Z")
    P = {n: pr(*pontos[n]) for n in p["pontos"]}
    linhas = [[*P[a], *P[b], rot] for a, b, rot in p.get("linhas", [])]
    num = None
    m = re.search(r"«(.+?)»", p.get("nota", ""))
    if m:
        v, _, r = m.group(1).partition(" ")
        num = [v, r]
    return dict(paths=paths, pts=[[n, *P[n]] for n in p["pontos"]], linhas=linhas, naufr=naufr, num=num)


# ───────────── DocGrifo: câmera ─────────────
def cam_doc(p, iw, ih):
    """Câmera (cx, cy em px da imagem, s = px de tela por px da imagem). 'pag' = página inteira; 'alvo' = zoom na linha
    (a linha grifada ocupa ~78% da largura, no máx. 4,2x a página, e fica a 42% da altura), como o pré-QA (preqa/gerar_grades.py)."""
    s_pag = min((H - 90) / ih, (W - 200) / iw)
    pag = [iw / 2, ih / 2, s_pag]
    g = p.get("grifo")
    if not g and p.get("regiao"):
        x, y, w, h = p["regiao"]
        s = min((W - 160) / (w * iw), (H - 100) / (h * ih))   # região inteira na tela (contain), sem cortar o texto
        return pag, [(x + w / 2) * iw, (y + h / 2) * ih, s]
    if not g:
        return pag, None
    x0 = min(r[0] for r in g) * iw; x1 = max(r[0] + r[2] for r in g) * iw
    y0 = min(r[1] for r in g) * ih; y1 = max(r[1] + r[3] for r in g) * ih
    with Image.open(V / "midia" / p["arq"]) as im0:
        fator = iw / im0.width  # a imagem pública pode ter sido reduzida; 1.100 px vale na original
    vw = min(max((x1 - x0) / 0.78, iw / 4.2, 1100 * fator), iw)
    vh = vw * H / W
    cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
    bx = min(max(cx - vw / 2, 0), iw - vw); by = min(max(cy - 0.42 * vh, 0), max(ih - vh, 0))
    return pag, [bx + vw / 2, by + vh / 2, W / vw]


def main():
    blocos = json.load(open(V / "blocos.json"))
    sb = json.load(open(V / "storyboard.json"))
    planos, pontos = sb["planos"], {k: tuple(v) for k, v in sb["pontos"].items()}
    whisper = json.load(open(V / "qa/whisper.json"))
    creditos = {r["arquivo"]: r["credito"] for r in csv.DictReader(open(V / "midia.csv"))}
    caps_txt = re.search(r"## Capítulos.*?```\n(.*?)```", (V / "SCRIPT.md").read_text(), re.S).group(1).strip().splitlines()
    titulos = re.findall(r"^### (B\d\d) \[[^\]]*\] (.+)$", (V / "SCRIPT.md").read_text(), re.M)
    cap_titulo = {bid: caps_txt[i].split(" ", 1)[1] for i, (bid, _) in enumerate(titulos) if i < len(caps_txt)}

    def gap(i, b):
        if i == 0: return 0
        if b["id"][:3] != blocos[i - 1]["id"][:3]: return GAP_CAP if b["id"][:3] in cap_titulo else GAP_IDEIA
        return GAP_IDEIA if b.get("ideia") else GAP

    # 1) voz
    partes, t = [np.zeros(int(HEAD * SR))], HEAD
    for i, b in enumerate(blocos):
        g = gap(i, b)
        if g: partes.append(np.zeros(int(g * SR))); t += g
        x, off = aparar(ler_mp3(V / "audio" / f"{b['id']}.mp3"))
        b["gap"] = g; b["off"] = off; b["ini"] = round(t, 3); t += len(x) / SR; b["fim"] = round(t, 3)
        partes.append(x)
    partes.append(np.zeros(int(TAIL * SR)))
    voz = np.concatenate(partes)
    dur = len(voz) / SR
    voz *= 10 ** (-3 / 20) / (np.max(np.abs(voz)) + 1e-9)
    por_id = {b["id"]: b for b in blocos}

    # 2) tempos dos planos
    erros, avisos = [], []
    for bid in [b["id"] for b in blocos]:
        ps = [p for p in planos if p["bloco"] == bid]
        b = por_id[bid]; wp = whisper[bid]["palavras"]; desde = 0
        for k, p in enumerate(ps):
            if k == 0:
                p["t0"] = 0.0 if bid == blocos[0]["id"] else b["ini"] - max(0.15, b["gap"] * 0.5)
                continue
            i = acha_em(p["em"], wp, desde)
            if i is None:
                pos = b["texto"].find(p["em"]) / max(1, len(b["texto"]))
                p["t0"] = b["ini"] + pos * (b["fim"] - b["ini"]) - LEAD
                avisos.append(f"{p['id']}: 'em' não achado no Whisper ({p['em']!r}); tempo proporcional")
            else:
                p["t0"] = b["ini"] + wp[i][1] - b["off"] - LEAD; desde = i + 1
        # grifo literal: quando a narração lê a frase do documento
        for p in ps:
            if p["tipo"] == "DocGrifo" and p.get("frase_doc"):
                i = acha_em(p["frase_doc"], wp, 0)
                if i is not None:
                    n = len(toks(p["frase_doc"]))
                    j = min(len(wp) - 1, i + max(0, n - 1))
                    p["g_ini"] = b["ini"] + wp[i][1] - b["off"]; p["g_fim"] = b["ini"] + wp[j][2] - b["off"]
    fim_total = math.ceil(dur * FPS) / FPS
    for k, p in enumerate(planos):
        p["t1"] = planos[k + 1]["t0"] if k + 1 < len(planos) else fim_total
        p["from"] = round(p["t0"] * FPS); p["fim_q"] = round(p["t1"] * FPS)
    for k, p in enumerate(planos):
        p["durq"] = (planos[k + 1]["from"] if k + 1 < len(planos) else round(fim_total * FPS)) - p["from"]
        p["d"] = p["durq"] / FPS
        if p["durq"] < 30: avisos.append(f"{p['id']}: plano curto ({p['d']:.2f} s)")

    # 3) checagens de filme (regra Ford < 7 s) e velocidade
    for p in planos:
        if p["tipo"] != "Filme": continue
        if p["d"] > FILME_MAX:
            erros.append(f"{p['id']} {p['bloco']}: trecho de filme com {p['d']:.2f} s (> {FILME_MAX} s, regra do Rodrigo)")
        disp = p["tout"] - p["tin"]
        if disp < p["d"] * p["vel"]:
            v = disp / p["d"]
            if v < VEL_MIN:
                erros.append(f"{p['id']} {p['bloco']}: trecho {p['tin']}–{p['tout']} ({disp:.1f} s) curto para {p['d']:.2f} s mesmo a {VEL_MIN}")
            p["vel"] = round(max(v, VEL_MIN), 3)
            avisos.append(f"{p['id']}: velocidade ajustada para {p['vel']}")
    if erros:
        print("\n".join("ERRO: " + e for e in erros)); print("\n".join("aviso: " + a for a in avisos))
        json.dump([dict(id=p["id"], bloco=p["bloco"], tipo=p["tipo"], t0=round(p["t0"], 2), d=round(p["d"], 2), em=p["em"]) for p in planos],
                  open(V / "qa/tempos.json", "w"), ensure_ascii=False, indent=0)
        sys.exit(1)

    # 4) mídia + timeline
    # SEM CRÉDITO EM TELA (Rodrigo, 12/11/2026): a Ficha mostra só data/lugar ou quem aparece; acervo e créditos vão só na descrição.
    FICHA_ARQ = {"foto_nimitz_midway1942.jpg": "ADM. CHESTER NIMITZ · MIDWAY, 1942", "foto_rochefort1934.jpg": "JOSEPH ROCHEFORT · 1934",
                 "foto_yamamoto.jpg": "ADM. ISOROKU YAMAMOTO", "foto_george_gay1942_rot.jpg": "ENSIGN GEORGE GAY · JUNE 1942",
                 "foto_robbins.jpg": "CHANDLER ROBBINS", "foto_robbins1948.jpg": "CHANDLER ROBBINS"}
    FICHA_TXT = {"AUG 15 2023 · USFWS": "AUG 15 2023 · MIDWAY ATOLL", "JAN 18 2022 · USFWS": "JAN 18 2022 · MIDWAY ATOLL",
                 "NHHC · H-GRAM 006": "NAVY HISTORY · THE \"AF\" TRICK", "NHHC · ORAL HISTORY": "JOHN FORD · IN HIS OWN WORDS",
                 "USGS · PATUXENT": "CHANDLER ROBBINS", "MIDWAY ATOLL NWR": "MIDWAY ATOLL", "JUNE 1942 · CINCPAC": "JUNE 4–7, 1942 · TRACK CHART",
                 "JUN 2 2016 · GAO-16-382": "JUN 2 2016 · FEDERAL AUDIT"}

    def ficha_tela(p):
        f = p.get("ficha")
        if not f: return None
        return [FICHA_ARQ.get(p.get("arq"), FICHA_TXT.get(f[0], f[0]))]

    tl = []
    papeis, grifos_sfx = [], []
    prev = None
    for p in planos:
        q = dict(id=p["id"], bloco=p["bloco"], tipo=p["tipo"], from_=p["from"], dur=p["durq"], ficha=ficha_tela(p), num=p.get("num"))
        tp = p["tipo"]
        if tp == "KenBurns":
            nome, iw, ih = img_publica(p["arq"]) if not SEM_MIDIA else (p["arq"], 1, 1)
            q.update(img=nome, iw=iw, ih=ih, de=p["de"], para=p["para"], crop=p.get("crop"))
        elif tp == "Filme":
            q.update(clip=clip(p, p["d"]) if not SEM_MIDIA else "", tin=p["tin"], vel=p["vel"])
        elif tp == "DocGrifo":
            nome, iw, ih = img_publica(p["arq"]) if not SEM_MIDIA else (p["arq"], 1, 1)
            pag, alvo = cam_doc(p, iw, ih)
            mesmo = prev is not None and prev["tipo"] == "DocGrifo" and prev.get("arq") == p["arq"]
            gi = p.get("g_ini"); gf = p.get("g_fim")
            q.update(img=nome, iw=iw, ih=ih, pag=pag, alvo=alvo, grifo=p.get("grifo"), cont=mesmo and not p.get("regiao"), regiao=p.get("regiao"),
                     cam_ant=(prev.get("_cam") if mesmo else None),
                     g_ini=None if gi is None else round((gi - p["t0"]) * FPS), g_fim=None if gf is None else round((gf - p["t0"]) * FPS))
            p["_cam"] = alvo or pag
            if not mesmo: papeis.append(p["t0"] + 0.05)
            if p.get("grifo"):
                a = gi if gi is not None else p["t0"] + 1.4
                grifos_sfx.append((a, (gf if gf is not None else a + 1.0)))
        elif tp == "Número":
            q.update(valor=p["valor"], rotulo=p.get("rotulo", ""))
        elif tp == "Mapa2D":
            q.update(mapa(p, pontos), selo=p.get("selo"), nome=p.get("nome"))
        elif tp == "Cartela":
            q.update(linhas=p["linhas"], selo=p.get("selo"))
        elif tp == "EntaoAgora":
            n1, w1, h1 = img_publica(p["arq"]) if not SEM_MIDIA else (p["arq"], 1, 1)
            n2, w2, h2 = img_publica(p["arq2"]) if not SEM_MIDIA else (p["arq2"], 1, 1)
            q.update(img=n1, iw=w1, ih=h1, img2=n2, iw2=w2, ih2=h2, rot1=p["rot1"], rot2=p["rot2"],
                     cred1="", cred2="")   # sem crédito em tela
        q["arq"] = p.get("arq")
        tl.append(q)
        p["_tl"] = q
        prev = p
    total_q = round(fim_total * FPS)
    (V / "src").mkdir(exist_ok=True)
    json.dump(dict(fps=FPS, durationInFrames=total_q, planos=tl), open(V / "src/timeline.json", "w"), ensure_ascii=False)

    # 5) áudio final
    (V / "audio/final").mkdir(parents=True, exist_ok=True)
    musica = ducking(voz, trilha(dur)) + sfx(dur, papeis, grifos_sfx)
    salvar(V / "audio/final/voz.wav", voz)
    salvar(V / "audio/final/trilha.wav", musica)
    salvar(V / "audio/final/mix_pre.wav", voz + musica)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(V / "audio/final/mix_pre.wav"), "-af", "loudnorm=I=-15:TP=-1.5:LRA=11",
                    "-ar", str(SR), "-ac", "2", str(V / "audio/final/mix.wav")], check=True)

    # 6) legendas e capítulos
    (V / "out").mkdir(exist_ok=True); (V / "qa").mkdir(exist_ok=True)
    (V / "out/legendas.srt").write_text(legendas(blocos, whisper))
    caps = []
    for bid, titulo in cap_titulo.items():
        b0 = next(b for b in blocos if b["id"].startswith(bid))
        caps.append(dict(t=0 if not caps else math.floor(b0["ini"] - b0["gap"] * 0.5), titulo=titulo, bloco=bid))
    json.dump(caps, open(V / "qa/capitulos.json", "w"), ensure_ascii=False, indent=1)
    json.dump([dict(id=b["id"], ini=b["ini"], fim=b["fim"]) for b in blocos], open(V / "qa/blocos_tempos.json", "w"), indent=0)
    json.dump([dict(id=p["id"], bloco=p["bloco"], tipo=p["tipo"], t0=round(p["t0"], 2), d=round(p["d"], 2), em=p["em"]) for p in planos],
              open(V / "qa/tempos.json", "w"), ensure_ascii=False, indent=0)
    filmes = [p["d"] for p in planos if p["tipo"] == "Filme"]
    print(json.dumps(dict(duracao=fmt(dur), duracao_s=round(dur, 2), quadros=total_q, planos=len(planos),
                          plano_min_s=round(min(p["d"] for p in planos), 2), plano_max_s=round(max(p["d"] for p in planos), 2),
                          filme_max_s=round(max(filmes), 2), capitulos=[f"{fmt(c['t'])} {c['titulo']}" for c in caps]), ensure_ascii=False, indent=1))
    for a in avisos: print("aviso:", a)


if __name__ == "__main__":
    main()
