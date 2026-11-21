#!/usr/bin/env python3
"""Montagem do 006-chernobyl (Clearance Required, "relógio de 67 h"): voz real + áudios de época + storyboard.json → timeline do Remotion,
trilha com ducking (muda sob áudio de época, no botão e no silêncio do log), .srt (voz + legendas dos áudios de época) e capítulos.

Uso (na pasta do vídeo): ~/workspace/fabrica-youtube/tools/.venv/bin/python tools/build.py [--sem-midia]
Entradas: blocos.json (+ arquivo_antes), storyboard.json, audio/<bloco>.mp3, audio/epoca/{A1..A6.wav,epoca.json} (tools/epoca.py), qa/whisper.json, midia/, midia.csv, SCRIPT.md
Saídas:   audio/final/{voz,trilha,mix}.wav, public/img, public/clips (trechos de filme sem áudio + fundos dos áudios de época), src/timeline.json
          (cada plano leva `rl` = estado do relógio persistente: régua + contador), out/legendas.srt, qa/capitulos.json, qa/tempos.json, qa/epoca_tempos.json
Crédito na tela: coluna `credito` do midia.csv (filmes/fotos) e DOC_CRED (documentos); o do áudio de época vai no plano Arquivo.
"""
import csv, json, math, os, re, subprocess, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
V = Path(__file__).resolve().parent.parent
SR, FPS, W, H = 48000, 30, 1920, 1080
GAP, GAP_IDEIA, GAP_CAP, HEAD, TAIL = 0.35, 0.9, 1.5, 0.15, 2.5
FILME_MAX, VEL_MIN = 8.6, 0.52   # 002: bíblia pede clipes de 4–8 s (o < 7 s era regra do filme do Ford, 001)
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


def ler_wav(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


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
    doc = arq.startswith("doc_")
    # docs: contraste 1,06 "assado" no arquivo (= CSS contrast(1.06)); filter em elemento de ~7.000 px estourava a memória do render (12/11)
    dst_nome = re.sub(r"\.(png|jpg|jpeg)$", "", arq) + (".c106.jpg" if doc else ".jpg")
    dst = V / "public/img" / dst_nome
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        im = Image.open(src)
        im = im.convert("RGB") if im.mode not in ("L", "RGB") else im
        lim = 5600 if arq.startswith("doc_") else 3400
        if max(im.size) > lim:
            f = lim / max(im.size); im = im.resize((round(im.width * f), round(im.height * f)), Image.LANCZOS)
        if doc:
            import numpy as np
            a8 = np.asarray(im).astype(np.float32)
            im = Image.fromarray(np.clip((a8 - 127.5) * 1.06 + 127.5, 0, 255).round().astype(np.uint8), mode=im.mode)
        dst.parent.mkdir(parents=True, exist_ok=True)
        im.save(dst, quality=90)
    with Image.open(dst) as im:
        return dst_nome, im.width, im.height


def clip(p, dur):
    """Corta o trecho do filme (sem áudio), na velocidade do plano, 30 fps, com folga de 0,3 s."""
    dst = V / "public/clips" / f"{p['id']}.mp4"
    precisa = (dur + 0.3) * p["vel"]
    base = f"{p['arq']}|{p['tin']}|{p['vel']:.3f}"
    marca = dst.with_suffix(".txt")
    if dst.exists() and marca.exists():   # 006: reaproveita o corte se a base é a mesma e ele cobre a duração (o plano só mudou 1–2 quadros)
        b0, _, l0 = marca.read_text().rpartition("|")
        try:
            if b0 == base and float(l0) >= precisa - 0.25 * p["vel"]: return dst.name
        except ValueError:
            pass
    dst.parent.mkdir(parents=True, exist_ok=True)
    recorte = "crop=iw*0.90:ih*0.90:0:0" if "voa" in p["arq"].lower() else "crop=iw*0.96:ih*0.96"   # 006: logo VOA no canto inferior direito
    vf = f"yadif=deint=interlaced,setpts=PTS/{p['vel']:.4f},fps={FPS},{recorte},scale=1440:-2:flags=lanczos"   # 002: corta 2% de cada borda (margens claras do telecine)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{p['tin']:.3f}", "-t", f"{precisa:.3f}", "-i", str(V / "midia" / p["arq"]),
                    "-an", "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", str(dst)], check=True)
    marca.write_text(f"{base}|{precisa:.3f}")
    return dst.name


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


# ───────────── 006: mapa 2D por código (Natural Earth 50m países, PD) ─────────────
GEO = None
LABELS_LAT = 1.0


def simplifica(pts, tol=1.2):
    out = [pts[0]]
    for x, y in pts[1:]:
        if abs(x - out[-1][0]) + abs(y - out[-1][1]) >= tol:
            out.append((x, y))
    return out


def mapa(p, pontos):
    """Projeção equirretangular com correção de cos(lat); caminhos por país (para destacar a Suécia na pluma)."""
    global GEO
    if GEO is None:
        GEO = json.load(open(V / "midia/ne50_countries.geojson"))["features"]
    pts = [pontos[n] for n in p["pontos"]]
    lons = [x for x, _ in pts]; lats = [y for _, y in pts]
    clat = (max(lats) + min(lats)) / 2; k = math.cos(math.radians(clat))
    mn = {"zona": 1.5, "despacho": 1.4, "rota": 1.6, "zona30": 1.5, "2022": 3.0}.get(p.get("nome"), 6.0)
    span_lat = max((max(lats) - min(lats)) * 1.9, (max(lons) - min(lons)) * k * H / W * 1.9, mn)   # altura do quadro em graus de latitude
    span_x = span_lat * W / H                                                                      # largura em "graus de latitude"
    clon = (max(lons) + min(lons)) / 2
    top = clat + span_lat / 2; sc = H / span_lat
    pr = lambda lo, la: (round(W / 2 + (lo - clon) * k * sc, 1), round((top - la) * sc, 1))
    paths = []
    for f in GEO:
        gm = f["geometry"]; nome = f["properties"].get("ADMIN", "")
        aneis = [gm["coordinates"][0]] if gm["type"] == "Polygon" else [pl[0] for pl in gm["coordinates"]]
        for ring in aneis:
            xy = [pr(c[0], c[1]) for c in ring]
            if max(x for x, _ in xy) < -50 or min(x for x, _ in xy) > W + 50 or max(y for _, y in xy) < -50 or min(y for _, y in xy) > H + 50:
                continue
            xy = simplifica(xy)
            if len(xy) > 2:
                paths.append(dict(d="M" + "L".join(f"{x:.0f},{y:.0f}" for x, y in xy) + "Z", pais=nome))
    P = {n: pr(*pontos[n]) for n in p["pontos"]}
    linhas = [[*P[a], *P[b], rot] for a, b, rot in p.get("linhas", [])]
    raio30 = round(30 / 111.0 * sc, 1) if p.get("nome") in ("zona30", "zona") else 0
    return dict(paths=paths, pts=[[n, *P[n]] for n in p["pontos"]], linhas=linhas, pluma=bool(p.get("pluma")), nome=p.get("nome"), raio30=raio30)


# ───────────── 006: relógio (régua + contador) ─────────────
BTN = 1 * 3600 + 23 * 60 + 40   # 26/04 01:23:40, em segundos desde 26/04 00:00


def parse_rel(lab):
    """'26.04 01:23:40' / '27.04 ~12:00' / '28.04 MON' → (segundos desde 26/04 00:00, aprox, tem_seg, so_dia); None se fora da régua."""
    m = re.match(r"^(\d\d)\.(\d\d) ~?(\d\d):(\d\d)(?::(\d\d))?$", lab or "")
    if m:
        d, _, h, mi, s = m.groups()
        return ((int(d) - 26) * 86400 + int(h) * 3600 + int(mi) * 60 + int(s or 0), "~" in lab, bool(s), False)
    if lab == "28.04 MON": return (2 * 86400 + 9 * 3600, True, False, True)
    if lab == "29.04 TUE": return (3 * 86400 + 12 * 3600, True, False, True)
    return None


def tod_para_s(t):
    """'01:23:40' | '25.04 01:06' | '28.04 21:00:00' | '+67:36:20' → ('tod', s desde 26/04 00:00) | ('dec', s)"""
    if t.startswith("+"):
        h, m, s = (int(x) for x in t[1:].split(":")); return "dec", h * 3600 + m * 60 + s
    m = re.match(r"^(?:(\d\d)\.(\d\d)(?:\.\d{4})? )?(\d\d):(\d\d)(?::(\d\d))?$", t)
    d = int(m.group(1)) if m and m.group(1) else 26
    if m and m.group(1) and re.match(r"^\d\d\.\d\d\.\d{4} ", t): d = 26   # 14.02.2025: só a hora
    return "tod", (d - 26) * 86400 + int(m.group(3)) * 3600 + int(m.group(4)) * 60 + int(m.group(5) or 0)


# ───────────── 006: áudio de época, fundos e imagens extraídas ─────────────
EPOCA = json.load(open(V / "audio/epoca/epoca.json"))
FUNDOS = {   # filmes de fundo (concatenados até cobrir a duração do áudio de época); A1/A6: tela escura com onda
    "A2": ["filme_pripyat_rua_vazia_1986.mp4"],
    "A3": ["filme_aerea_pb_usina_1986.mp4", "filme_helicoptero_chamine_pb_1986.mp4", "filme_parede_usina_chamine_1986.mp4"],
    "A4": ["filme_pripyat_sacadas_playground_1986.mp4", "filme_pripyat_predios_rua_1986.mp4", "filme_palacio_cultura_pripyat_1986.mp4",
           "filme_centro_comercial_pripyat_1986.mp4", "filme_aerea_pripyat_horizonte_1986.mp4", "filme_pripyat_panorama_aerea_1986.mp4",
           "filme_pripyat_rua_vazia_1986.mp4"],
    "A5": ["filme_vremya_locutora_28abr1986.mp4", "filme_cbs_vremya_locutor.mp4", "filme_abc_vremya_locutora.mp4"],
}
CRED_AUDIO = {
    "A1": "Audio: fire-service dispatch calls, 26 Apr 1986 · via pripyat.com / Wikimedia Commons",
    "A2": "Audio: Pripyat city radio, 27 Apr 1986 · via pripyat.com / Wikimedia Commons",
    "A3": "Audio: fire-service dispatch calls, 26 Apr 1986 · via pripyat.com / Wikimedia Commons",
    "A4": "Audio: Pripyat city radio, 27 Apr 1986 · via pripyat.com / Wikimedia Commons",
    "A5": "Synthetic voice reading the TASS text of 28 Apr 1986 · not the original broadcast",
    "A6": "Audio: fire-service dispatch calls, 26 Apr 1986 · via pripyat.com / Wikimedia Commons",
}
DOC_CRED = [
    ("doc_insag7", "Source: IAEA, INSAG-7 (1992)"),
    ("doc_wilson208406", "Order of the Ministry of Motor Transport · Wilson Center Digital Archive, doc. 208406"),
    ("doc_wilson208405", "V. P. Bryukhanov, report of 26 Apr 1986 · Wilson Center Digital Archive, doc. 208405"),
    ("doc_politburo-28abr_ru", "Politburo, 28 April 1986 (original text, gorby.ru)"),
    ("doc_politburo", "Politburo session, 28 Apr 1986 (APRF; trans. S. Savranskaya, National Security Archive)"),
    ("doc_frus", "CIA, 'Spot Commentary', 29 Apr 1986 · FRUS 1981-88, vol. V, doc. 220"),
    ("doc_upi", "UPI Archives, 28 April 1986"),
    ("doc_lei791a", "Law of Ukraine No. 791a-XII, 27 Feb 1991"),
]


def cred_doc(arq):
    for pre, c in DOC_CRED:
        if arq.startswith(pre): return c
    return None


def dur_arq(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout)


def fundo_clip(aid, dur):
    """Concatena os filmes de fundo (sem áudio, 30 fps, 1440 px) até cobrir dur; devolve (nome, ar)."""
    dst = V / "public/clips" / f"fundo_{aid}.mp4"
    chave = f"{FUNDOS[aid]}|{dur:.2f}"; marca = dst.with_suffix(".txt")
    if not (dst.exists() and marca.exists() and marca.read_text() == chave):
        dst.parent.mkdir(parents=True, exist_ok=True)
        tmp = Path(os.environ.get("TMPDIR", "/tmp")) / f"fundo_{aid}"; tmp.mkdir(parents=True, exist_ok=True)
        lista, tot, i = [], 0.0, 0
        while tot < dur + 0.5:
            f = FUNDOS[aid][i % len(FUNDOS[aid])]; i += 1
            o = tmp / f"{i:02d}.mp4"
            vf = f"yadif=deint=interlaced,fps={FPS},crop=iw*0.96:ih*0.96,scale=1440:1080:flags=lanczos"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(V / "midia" / f), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                            "-pix_fmt", "yuv420p", str(o)], check=True)
            lista.append(o); tot += dur_arq(o)
        (tmp / "l.txt").write_text("".join(f"file '{o}'\n" for o in lista))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "l.txt"), "-t", f"{dur + 0.3:.3f}", "-c:v", "libx264",
                        "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(dst)], check=True)
        marca.write_text(chave)
    return dst.name


def arq_img(arq):
    """'filme:<arq>.mp4@<s>' = still do clipe naquele segundo → public/img; senão a imagem da mídia."""
    if arq.startswith("filme:"):
        f, _, s = arq[6:].partition("@")
        nome = f"still_{Path(f).stem}_{s.replace('.', '_')}.jpg"
        dst = V / "public/img" / nome
        if not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", s, "-i", str(V / "midia" / f), "-frames:v", "1", "-vf", "yadif=deint=interlaced,crop=iw*0.96:ih*0.96,scale=1440:-2:flags=lanczos",
                            "-q:v", "2", str(dst)], check=True)
        with Image.open(dst) as im:
            return nome, im.width, im.height
    return img_publica(arq)


def estatica(rng, d, g=1.0):
    n = rng.uniform(-1, 1, int(d * SR)); k = int(0.0006 * SR)
    x = n - np.convolve(n, np.ones(40) / 40, "same")
    x *= (0.6 + 0.4 * np.sign(np.sin(np.linspace(0, 90, len(n)))))
    y = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * 10 ** (-30 / 20) * g
    f = int(0.05 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f)
    return y


def main():
    blocos = json.load(open(V / "blocos.json"))
    sb = json.load(open(V / "storyboard.json"))
    planos, pontos = sb["planos"], {k: tuple(v) for k, v in sb["pontos"].items()}
    arqs = sb["arquivos"]
    whisper = json.load(open(V / "qa/whisper.json"))
    creditos = {r["arquivo"]: r["credito"] for r in csv.DictReader(open(V / "midia.csv"))}
    titulos = re.findall(r"^### (B\d\d) \[[^\]]*\] (.+)$", (V / "SCRIPT.md").read_text(), re.M)
    cap_titulo = {bid: t.strip() for bid, t in titulos}

    def gap(i, b):
        if i == 0: return 0
        if b.get("arquivo_antes"): return 0.3
        if b["id"][:3] != blocos[i - 1]["id"][:3]: return GAP_CAP if b["id"][:3] in cap_titulo else GAP_IDEIA
        return GAP_IDEIA if b.get("ideia") else GAP

    # 1) voz + áudios de época
    n_max = int(1200 * SR)
    voz_a = np.zeros(n_max); epo_a = np.zeros(n_max)
    t = HEAD
    epoca_t = {}                      # A# → (início, fim) na timeline
    for i, b in enumerate(blocos):
        a_id = b.get("arquivo_antes")
        if a_id:
            t += 0.3 if i else 0.0
            d = EPOCA[a_id]["dur"]
            w = ler_wav(V / "audio/epoca" / f"{a_id}.wav")
            epo_a[int(t * SR):int(t * SR) + len(w)] += w
            epoca_t[a_id] = (round(t, 3), round(t + d, 3)); t += d
        g = gap(i, b)
        t += g
        x, off = aparar(ler_mp3(V / "audio" / f"{b['id']}.mp3"))
        b["gap"] = g; b["off"] = off; b["ini"] = round(t, 3)
        voz_a[int(t * SR):int(t * SR) + len(x)] += x
        t += len(x) / SR; b["fim"] = round(t, 3)
    t += TAIL
    dur = t
    voz = voz_a[: int(dur * SR)]; epo = epo_a[: int(dur * SR)]
    voz *= 10 ** (-3 / 20) / (np.max(np.abs(voz)) + 1e-9)
    por_id = {b["id"]: b for b in blocos}

    # 2) tempos dos planos
    erros, avisos = [], []
    for k, p in enumerate(planos):
        if p["tipo"] == "Arquivo":
            p["t0"] = 0.0 if p["id"] == planos[0]["id"] else max(0.0, epoca_t[p["bloco"]][0] - 0.05)
    for bid in [b["id"] for b in blocos]:
        ps = [p for p in planos if p["bloco"] == bid]
        b = por_id[bid]; wp = whisper[bid]["palavras"]; desde = 0
        for k, p in enumerate(ps):
            if k == 0:
                p["t0"] = 0.0 if p["id"] == planos[0]["id"] else b["ini"] - max(0.15, b["gap"] * 0.5)
                continue
            i = acha_em(p["em"], wp, desde)
            if i is None:
                pos = b["texto"].find(p["em"]) / max(1, len(b["texto"]))
                p["t0"] = b["ini"] + pos * (b["fim"] - b["ini"]) - LEAD
                avisos.append(f"{p['id']}: 'em' não achado no Whisper ({p['em']!r}); tempo proporcional")
            else:
                p["t0"] = b["ini"] + wp[i][1] - b["off"] - LEAD; desde = i + 1
        for p in ps:
            if p["tipo"] == "DocGrifo" and p.get("frase_doc"):
                i = acha_em(p["frase_doc"], wp, 0)
                if i is not None:
                    n = len(toks(p["frase_doc"])); j = min(len(wp) - 1, i + max(0, n - 1))
                    p["g_ini"] = b["ini"] + wp[i][1] - b["off"]; p["g_fim"] = b["ini"] + wp[j][2] - b["off"]
    fim_total = math.ceil(dur * FPS) / FPS
    for k, p in enumerate(planos):
        p["from"] = round(p["t0"] * FPS)
    for k, p in enumerate(planos):
        p["durq"] = (planos[k + 1]["from"] if k + 1 < len(planos) else round(fim_total * FPS)) - p["from"]
        p["d"] = p["durq"] / FPS
        if p["durq"] < 30: avisos.append(f"{p['id']}: plano curto ({p['d']:.2f} s)")
        if p["durq"] <= 0: erros.append(f"{p['id']}: duração {p['durq']} (ordem dos tempos)")

    # 3) checagens de filme e velocidade
    for p in planos:
        if p["tipo"] != "Filme": continue
        if p["d"] > FILME_MAX:
            erros.append(f"{p['id']} {p['bloco']}: trecho de filme com {p['d']:.2f} s (> {FILME_MAX} s)")
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
    tl = []
    papeis, grifos_sfx, mudo, estaticas, datilos = [], [], [], [], []
    prev = None
    est = (False, None)
    for p in planos:
        tp = p["tipo"]
        q = dict(id=p["id"], bloco=p["bloco"], tipo=tp, from_=p["from"], dur=p["durq"], num=p.get("num"),
                 ficha=[p["ficha"]] if p.get("ficha") else None, cred=p.get("credito") or None, selo=p.get("selo"))
        if tp == "KenBurns":
            nome, iw, ih = img_publica(p["arq"]) if not SEM_MIDIA else (p["arq"], 1, 1)
            q.update(img=nome, iw=iw, ih=ih, de=p["de"], para=p["para"], crop=p.get("crop"))
        elif tp == "Filme":
            cn = clip(p, p["d"]) if not SEM_MIDIA else ""
            ar = 1.33
            if cn and (V / "public/clips" / cn).exists():
                o = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(V / "public/clips" / cn)],
                                   capture_output=True, text=True).stdout.strip().split(",")
                ar = int(o[0]) / int(o[1])
            q.update(clip=cn, tin=p["tin"], vel=p["vel"], ar=round(ar, 3))
        elif tp == "DocGrifo":
            nome, iw, ih = img_publica(p["arq"]) if not SEM_MIDIA else (p["arq"], 1, 1)
            pag, alvo = cam_doc(p, iw, ih)
            mesmo = prev is not None and prev["tipo"] == "DocGrifo" and prev.get("arq") == p["arq"]
            gi = p.get("g_ini"); gf = p.get("g_fim")
            q.update(img=nome, iw=iw, ih=ih, pag=pag, alvo=alvo, grifo=p.get("grifo"), cont=mesmo and not p.get("regiao"), regiao=p.get("regiao"),
                     cam_ant=(prev.get("_cam") if mesmo else None), cred=cred_doc(p["arq"]),
                     g_ini=None if gi is None else round((gi - p["t0"]) * FPS), g_fim=None if gf is None else round((gf - p["t0"]) * FPS))
            p["_cam"] = alvo or pag
            if not mesmo: papeis.append(p["t0"] + 0.05)
            if p.get("grifo"):
                a = gi if gi is not None else p["t0"] + 1.4
                grifos_sfx.append((a, (gf if gf is not None else a + 1.0)))
        elif tp == "Número":
            q.update(valor=p["valor"], rotulo=p.get("rotulo", ""))
        elif tp == "Mapa2D":
            q.update(mapa(p, pontos))
        elif tp in ("Dupla", "EntaoAgora"):
            n1, w1, h1 = arq_img(p["arq"]) if not SEM_MIDIA else (p["arq"], 1, 1)
            n2, w2, h2 = arq_img(p["arq2"]) if not SEM_MIDIA else (p["arq2"], 1, 1)
            q.update(img=n1, iw=w1, ih=h1, img2=n2, iw2=w2, ih2=h2, rot1=p["rot1"], rot2=p["rot2"],
                     cred1=p.get("credito") or "", cred2=creditos.get(p["arq2"], ""))
            if tp == "EntaoAgora": q["cred"] = None
        elif tp == "Cartela":
            q.update(linhas=p["linhas"])
        elif tp in ("Datilo", "Teletipo"):
            q.update(linhas=p["linhas"]); datilos.append((p["t0"], p["t0"] + min(p["d"] * 0.7, 3.2)))
        elif tp == "Contador":
            q.update(rotulo=p.get("rotulo", ""), de_t=p["de_t"], ate_t=p["ate_t"])
        elif tp == "TresRelogios":
            q.update(valores=p["valores"], rotulos=p["rotulos"])
        elif tp == "Arquivo":
            a = p["bloco"]; E = EPOCA[a]; a0 = epoca_t[a][0]
            leg = [[round(x0 * FPS), round(x1 * FPS), o, en] for x0, x1, o, en in E["leg"]]
            fundo = fundo_clip(a, p["d"]) if (a in FUNDOS and not SEM_MIDIA) else None
            cred = [CRED_AUDIO[a]]
            if a in FUNDOS and creditos.get(FUNDOS[a][0]): cred.append("Film: " + creditos[FUNDOS[a][0]].replace("Film: ", "").replace("Soviet newsreel footage", "newsreel footage"))
            ini_q = round((a0 - p["t0"]) * FPS)    # o plano começa 0,05 s antes do áudio
            q.update(selo=arqs[a]["selo"], rotulo=arqs[a].get("rotulo"), leg=leg, onda=E["onda"], onda_ini=ini_q, fundo=fundo, creds=cred, aid=a, cred=None)
            mudo.append((a0 - 0.3, a0 + E["dur"] + 0.3))
            if a in ("A1", "A6"): estaticas.append((p["t0"], 0.7, 0.8)); estaticas.append((a0 + E["dur"] - 0.5, 0.6, 0.8))
        elif tp == "Glitch":
            estaticas.append((p["t0"], min(p["d"], 2.6), 1.0)); mudo.append((p["t0"] - 0.1, p["t0"] + p["d"]))
        elif tp == "Mural":
            q.update(cards=[
                ("doc_insag7_p65_tabela-I-I-0123-40.png", "01:23:40", "INSAG-7 · LOG"),
                ("doc_wilson208405_bryukhanov-0125.png", "01:25", "DIRECTOR'S REPORT"),
                ("doc_wilson208406_p3_1125-onibus-250-caminhoes.png", "SAT 20:00", "BUS ORDER"),
                ("doc_politburo-28abr_p1_dolgikh-0130.png", "MON 28 APR", "POLITBURO"),
                ("doc_upi-28abr1986_p2_tass-announcement.png", "MON 21:00", "TASS · UPI"),
                ("doc_frus-v05-d220_cia-29abr.png", "TUE 29 APR", "CIA · SPOT COMMENTARY"),
            ])
            q["mural_imgs"] = [[img_publica(a)[0], *img_publica(a)[1:], h, r] for a, h, r in q.pop("cards")]
        # relógio persistente (régua + contador): plano sem `relogio` herda o estado do anterior
        rel = p.get("relogio")
        if rel is not None:
            r = parse_rel(rel[0]) if rel[1] != "oculto" else None
            est = (r is not None, r)
        else:
            est = est if prev is not None else (False, None)
        vis, cur = est
        modo = rel[1] if rel else "parado"
        pv = prev["_rl"] if prev is not None else None
        q["rl"] = dict(vis=bool(vis), v1=cur[0] if cur else None, aprox=bool(cur[1]) if cur else False, seg=bool(cur[2]) if cur else False,
                       dia=bool(cur[3]) if cur else False, modo=modo, v0=(pv["v1"] if pv and pv["vis"] else None), oc=bool(pv and pv["vis"]),
                       sem_cont=tp in ("Contador", "TresRelogios", "DocGrifo"))
        p["_rl"] = q["rl"]
        q["arq"] = p.get("arq")
        tl.append(q)
        prev = p
    total_q = round(fim_total * FPS)
    (V / "src").mkdir(exist_ok=True)
    json.dump(dict(fps=FPS, durationInFrames=total_q, planos=tl), open(V / "src/timeline.json", "w"), ensure_ascii=False)

    # 5) áudio final
    (V / "audio/final").mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(3)
    mus = trilha(dur)
    # trilha para: sob cada áudio de época, no botão (Contador "parado" do B01a) e no silêncio do log (Glitch)
    p005 = next(p for p in planos if p["id"] == "P005"); mudo.append((p005["t0"] - 0.1, p005["t0"] + p005["d"]))
    g = np.ones(len(mus))
    for a, b_ in mudo:
        i0, i1 = max(0, int((a - 0.4) * SR)), min(len(g), int((b_ + 0.5) * SR))
        env = np.ones(i1 - i0)
        f = int(0.4 * SR); env[:f] = np.linspace(1, 0.0, f); env[f:-f] = 0.0; env[-f:] = np.linspace(0.0, 1, f)
        g[i0:i1] = np.minimum(g[i0:i1], env)
    musica = ducking(voz, mus) * g + sfx(dur, papeis, grifos_sfx + datilos)
    st = np.zeros(len(musica))
    for t0, d, gg in estaticas:
        x = estatica(rng, d, gg); i0 = int(t0 * SR); st[i0:i0 + len(x)] += x[: len(st) - i0]
    epo_n = epo
    salvar(V / "audio/final/voz.wav", voz)
    salvar(V / "audio/final/trilha.wav", musica + st)
    salvar(V / "audio/final/mix_pre.wav", voz + epo_n + musica + st)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(V / "audio/final/mix_pre.wav"), "-af", "loudnorm=I=-15:TP=-1.5:LRA=11",
                    "-ar", str(SR), "-ac", "2", str(V / "audio/final/mix.wav")], check=True)

    # 6) legendas e capítulos
    (V / "out").mkdir(exist_ok=True); (V / "qa").mkdir(exist_ok=True)
    srt = legendas(blocos, whisper)
    itens = []
    for bl in srt.strip().split("\n\n"):
        ln = bl.split("\n"); a_, z_ = ln[1].split(" --> "); itens.append((a_, z_, "\n".join(ln[2:])))
    for a, (a0, _) in epoca_t.items():
        for x0, x1, o, en in EPOCA[a]["leg"]:
            itens.append((ts(a0 + x0), ts(a0 + x1), ("[ARCHIVE AUDIO] " if a != "A5" else "[RECONSTRUCTION] ") + en))
    itens.sort(key=lambda z: z[0])
    (V / "out/legendas.srt").write_text("\n".join(f"{i}\n{a} --> {z}\n{p}\n" for i, (a, z, p) in enumerate(itens, 1)))
    caps = []
    for bid, titulo in cap_titulo.items():
        b0 = next(b for b in blocos if b["id"].startswith(bid))
        caps.append(dict(t=0 if not caps else math.floor(b0["ini"] - b0["gap"] * 0.5), titulo=titulo, bloco=bid))
    json.dump(caps, open(V / "qa/capitulos.json", "w"), ensure_ascii=False, indent=1)
    json.dump([dict(id=b["id"], ini=b["ini"], fim=b["fim"]) for b in blocos], open(V / "qa/blocos_tempos.json", "w"), indent=0)
    json.dump([dict(id=p["id"], bloco=p["bloco"], tipo=p["tipo"], t0=round(p["t0"], 2), d=round(p["d"], 2), em=p.get("em", "")) for p in planos],
              open(V / "qa/tempos.json", "w"), ensure_ascii=False, indent=0)
    json.dump(epoca_t, open(V / "qa/epoca_tempos.json", "w"))
    filmes = [p["d"] for p in planos if p["tipo"] == "Filme"]
    print(json.dumps(dict(duracao=fmt(dur), duracao_s=round(dur, 2), quadros=total_q, planos=len(planos),
                          plano_min_s=round(min(p["d"] for p in planos), 2), plano_max_s=round(max(p["d"] for p in planos), 2),
                          filme_max_s=round(max(filmes), 2) if filmes else 0, epoca=epoca_t, capitulos=[f"{fmt(c['t'])} {c['titulo']}" for c in caps]), ensure_ascii=False, indent=1))
    for a in avisos: print("aviso:", a)


if __name__ == "__main__":
    main()
