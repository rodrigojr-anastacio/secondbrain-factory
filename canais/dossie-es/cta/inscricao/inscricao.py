#!/usr/bin/env python3
"""CTA de inscrição do Dossier en Minutos (27/11/2026, decisão do Rodrigo). Regra em canais/dossie-es/biblia/roteiro.md.

A frase (texto fixo, palavra por palavra) é um BLOCO NORMAL do roteiro, falado pelo narrador do canal (mesma voz e config
de produção), no fim de um capítulo forte por volta de 60% do vídeo (aceitável 55–70%), a ≥ 2 min do CTA da HQ (~37,5%,
cta/encaixe.py). Enquanto a frase toca, um botão "SUSCRÍBETE" desenhado no estilo do canal entra no canto superior
direito, recebe o clique (vira "SUSCRITO"), o sininho toca e ele sai (BotonSuscribete.jsx).

Uso (raiz do repo; P = canais/dossie-es/cta/inscricao/inscricao.py; V = pasta do vídeo):
  tools/.venv/bin/python P roteiro V   depois do roteiro.py: confere texto, posição estimada (55–70%), fim de capítulo,
                                       distância do CTA da HQ e CTA antigo; sugere o capítulo certo. Código 1 = reprovado.
  tools/.venv/bin/python P montar V    depois do tools/build.py e ANTES do render: põe o botão na src/timeline.json,
                                       copia o componente para src/, liga o Video.jsx (idempotente), põe o clique e o
                                       sininho no public/audio/mix.wav e grava qa/cta-inscricao.json. Código 1 = fora da regra.
  tools/.venv/bin/python P qa V        no out/video.mp4: Whisper da frase (≥ 85% do texto), posição 55–70%, ≥ 120 s do
                                       CTA da HQ e botão visível (frame + pixels). Grava qa/cta-inscricao-qa.json e
                                       qa/cta-inscricao.jpg. Código 1 = reprovado. --sem-posicao: só texto e botão (amostra).
No roteiro.py, use o texto daqui (nunca redigite):
  import sys; sys.path.insert(0, str(Path.home() / "workspace/fabrica-youtube/canais/dossie-es/cta/inscricao"))
  from inscricao import TEXTO as CTA_INSCRICAO
  ...
  b("<re-hook que abre o próximo expediente>")
  b(CTA_INSCRICAO, "<2–3 planos de reuso do capítulo>", ideia=True)   # último bloco do capítulo
  cap("9. ...")
"""
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
import wave
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent
CTA_DIR = AQUI.parent
sys.path.insert(0, str(CTA_DIR))
import encaixe  # noqa: E402  (CTA da HQ: posição e interruptor ATIVO)

TEXTO = ("Si te está gustando este expediente, suscríbete. "
         "Así nos ayudas a seguir investigando y contando historias como esta.")
FAIXA = (55.0, 70.0)        # % da duração em que o bloco começa
ALVO = 60.0
DIST_HQ = 120.0             # s mínimos entre os dois CTAs (fim de um → início do outro)
MARGEM_EST = 10.0           # s de folga na checagem do roteiro (estimativa de tempo erra 1–3%)
WPS, BREAK, LONG = 2.38, 0.35, 0.8   # mesmos do roteiro.py do canal
FPS, SR = 30, 48000
COMPONENTE = "BotonSuscribete.jsx"
# área do botão no quadro 1920×1080 (canto superior direito, espelho da ficha LUGAR Y FECHA): usada no QA de pixels
CAIXA = (1920 - 64 - 520, 50, 1920 - 40, 50 + 150)   # x0, y0, x1, y1 com folga para a rotação e a sombra

TAG = re.compile(r"\[[^\]]*\]\s*")
PEDE_INSCRICAO = {"suscribete", "suscribirte", "suscribanse", "suscribase"}   # CTA antigo/redigitado ("suscribir el empréstito" não conta)


def limpo(t):
    return re.sub(r"\s+", " ", TAG.sub("", t)).strip()


def norm(t):
    t = unicodedata.normalize("NFD", limpo(t).lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]+", " ", t).split()


def e_cta(texto):
    return norm(texto) == norm(TEXTO)


def falado(t):
    n = 0
    for w in limpo(t).split():
        d = re.sub(r"\D", "", w)
        n += (5 if len(d) == 4 else 3 if len(d) == 3 else 2 if d else 1) if d and d == w.strip(".,:;?!") else 1
    return n


def dur_est(t):
    return falado(t) / WPS + t.count("[break]") * BREAK + t.count("[long-break]") * LONG + 0.1


def fmt(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


def capitulos_do_script(V):
    """{id_do_bloco: título do capítulo} e a lista ordenada de (título, primeiro_bloco), lidos do SCRIPT.md."""
    cap, de, inicios = None, {}, []
    for linha in (V / "SCRIPT.md").read_text().splitlines():
        m = re.match(r"^##\s+(.*\S)", linha)
        if m:
            cap = m.group(1); inicios.append([cap, None]); continue
        m = re.match(r"^\*\*\[(N\d+)\]\*\*", linha)
        if m and cap:
            de[m.group(1)] = cap
            if inicios[-1][1] is None: inicios[-1][1] = m.group(1)
    return de, [tuple(x) for x in inicios if x[1]]


def _hq_info():
    cfg = None
    try:
        cfg = json.load(open(CTA_DIR / "cta.json"))
    except Exception:
        pass
    dur = (cfg or {}).get("duracao_s", 16.4) + encaixe.GAP_ANTES
    return encaixe.ativo_path().exists(), dur


# ───────────────────────── roteiro ─────────────────────────
def cmd_roteiro(V):
    blocos = json.load(open(V / "blocos.json"))
    cap_de, inicios = capitulos_do_script(V)
    abre = {b for _, b in inicios}
    t, ini = 0.0, {}
    for b in blocos:
        ini[b["id"]] = t; t += dur_est(b["texto"])
    total = t
    ativo, hq_dur = _hq_info()
    hq_bloco = encaixe.escolher([(b, ini[b]) for _, b in inicios if b in ini], total)
    hq_ini = ini.get(hq_bloco)
    def real(s):   # tempo com o CTA da HQ encaixado (se ATIVO)
        return s + hq_dur if (ativo and hq_ini is not None and s >= hq_ini) else s
    total_r = total + (hq_dur if ativo and hq_ini is not None else 0)
    ids = [b["id"] for b in blocos]
    fim_de_cap = {ids[i]: (i + 1 < len(ids) and ids[i + 1] in abre) for i in range(len(ids))}

    def avalia(bid):
        i = ids.index(bid)
        a = real(ini[bid]); z = a + dur_est(blocos[i]["texto"])
        pct = 100 * a / total_r
        if hq_ini is None: dist = None
        else:
            h0 = real(hq_ini) - (hq_dur if ativo else 0); h1 = h0 + (hq_dur if ativo else 0)
            dist = a - h1 if a >= h1 else h0 - z
        return a, pct, dist

    candidatos = []
    for i, bid in enumerate(ids):
        cap = cap_de.get(bid, "")
        if not fim_de_cap[bid] or cap.startswith(("Hook", "Cierre")) or e_cta(blocos[i]["texto"]): continue
        a, pct, dist = avalia(bid)
        # o CTA entraria DEPOIS deste bloco (último do capítulo): início = fim deste bloco
        a2 = a + dur_est(blocos[i]["texto"]); pct2 = 100 * a2 / total_r
        d2 = None if dist is None else dist + dur_est(blocos[i]["texto"])
        if FAIXA[0] <= pct2 <= FAIXA[1] and (d2 is None or d2 >= DIST_HQ + MARGEM_EST):
            candidatos.append((abs(pct2 - ALVO), cap, bid, pct2, a2))
    candidatos.sort()

    erros, avisos, info = [], [], {}
    achados = [b["id"] for b in blocos if e_cta(b["texto"])]
    antigos = [b["id"] for b in blocos if PEDE_INSCRICAO & set(norm(b["texto"])) and not e_cta(b["texto"])]
    if antigos:
        erros.append(f"CTA de inscrição fora do texto aprovado em {', '.join(antigos)} (o texto é fixo; apague o CTA antigo "
                     f"'Si te interesan estos expedientes…')")
    if len(achados) != 1:
        erros.append(f"{len(achados)} blocos com a frase exata do CTA de inscrição (precisa de 1)")
    for bid in achados[:1]:
        a, pct, dist = avalia(bid)
        cap = cap_de.get(bid, "?")
        info = {"bloco": bid, "capitulo": cap, "ini_est": fmt(a), "pct_est": round(pct, 1),
                "dist_hq_est_s": None if dist is None else round(dist, 1), "duracao_est": fmt(total_r)}
        if not fim_de_cap[bid]: erros.append(f"{bid} não é o último bloco do capítulo '{cap}' (o próximo bloco tem de abrir capítulo)")
        if cap.startswith(("Hook", "Cierre")): erros.append(f"{bid} está no {cap}: vai no fim de um expediente do miolo")
        if not FAIXA[0] <= pct <= FAIXA[1]: erros.append(f"{bid} começa em ~{pct:.1f}% (faixa {FAIXA[0]:.0f}–{FAIXA[1]:.0f}%)")
        elif abs(pct - ALVO) > 6: avisos.append(f"{bid} em ~{pct:.1f}%: aceitável, mas o alvo é ~60%")
        if dist is not None and dist < DIST_HQ + MARGEM_EST:
            erros.append(f"{bid} a ~{dist:.0f} s do CTA da HQ (mínimo {DIST_HQ:.0f} s + {MARGEM_EST:.0f} s de margem da estimativa)")
    print(f"CTA de inscrição · duração estimada {fmt(total_r)} (CTA da HQ {'ATIVO' if ativo else 'inativo, posição hipotética'}"
          f" antes de {hq_bloco} em ~{fmt(real(hq_ini)) if hq_ini is not None else '?'})")
    if info: print("  frase:", json.dumps(info, ensure_ascii=False))
    print("  lugares válidos (fim de capítulo → CTA):", "; ".join(f"depois de {b} ({c}) ~{p:.1f}% {fmt(a)}" for _, c, b, p, a in candidatos[:4]) or "nenhum")
    for x in avisos: print("  AVISO:", x)
    for x in erros: print("  ERRO:", x)
    print("  APROVADO" if not erros else "  REPROVADO")
    return 0 if not erros else 1


# ───────────────────────── montar ─────────────────────────
def ler_audio(p, canais=1):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-ac", str(canais), "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    return x.reshape(-1, canais) if canais > 1 else x


def momento_clique(mp3):
    """s (contados do início da fala, como no build.py, que apara o silêncio inicial) em que soa o "-críbe-": Whisper com
    tempo por palavra no áudio do bloco, 45% da palavra "suscríbete". (A pausa da vírgula depois de "expediente" tem o
    mesmo tamanho da pausa entre frases do --por-frase: detecção de silêncio erra, 27/11/2026.) None se não achar."""
    from faster_whisper import WhisperModel
    x = ler_audio(mp3)
    w = int(0.01 * SR); n = len(x) // w
    db = 20 * np.log10(np.sqrt(np.mean(x[: n * w].reshape(n, w) ** 2, axis=1)) + 1e-12)
    voz = np.where(db > -45)[0]
    lead = max(0.0, voz[0] * 0.01 - 0.05) if len(voz) else 0.0      # o aparar() do build.py deixa 0,05 s antes da fala
    x16 = x[:: SR // 16000].astype(np.float32)
    segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(x16, language="es", beam_size=5, word_timestamps=True)
    for s in segs:
        for p in s.words or []:
            ws = norm(p.word)
            if ws and ws[0].startswith("suscr"):
                return max(0.5, p.start + 0.45 * (p.end - p.start) - lead)
    return None


def sfx_clique_sino():
    """Clique de mouse seco + sininho curto (dois parciais), sintetizados aqui. Devolve (clique, sino) mono 48 kHz."""
    rng = np.random.default_rng(11)
    n = int(0.05 * SR); t = np.arange(n) / SR
    clique = (rng.uniform(-1, 1, n) * np.exp(-t * 400) + 0.6 * np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 300))
    clique = np.convolve(clique, np.ones(4) / 4, "same") * 0.22
    m = int(1.1 * SR); t = np.arange(m) / SR
    sino = np.zeros(m)
    for k, (f0, a) in enumerate(((1568, 1.0), (2093, 0.7))):   # sol6 e dó7, o 2º 0,12 s depois
        o = int(0.12 * k * SR); tt = t[: m - o]
        sino[o:] += a * (np.sin(2 * np.pi * f0 * tt) + 0.35 * np.sin(2 * np.pi * f0 * 2.76 * tt) * np.exp(-tt * 6)) * np.exp(-tt * 4.5)
    return clique, sino * 0.05


def mix_sfx(mix_path, eventos):
    """Soma SFX ao mix.wav final (estéreo, pós-loudnorm). eventos = [(t_s, array mono)]."""
    with wave.open(str(mix_path)) as w:
        ch, sw, sr, nf = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        assert sw == 2 and sr == SR, f"mix.wav inesperado ({sw * 8} bits, {sr} Hz)"
        x = np.frombuffer(w.readframes(nf), dtype="<i2").astype(np.float64).reshape(-1, ch) / 32767
    for t0, s in eventos:
        i0 = int(t0 * SR); i1 = min(len(x), i0 + len(s))
        if 0 <= i0 < len(x): x[i0:i1] += s[: i1 - i0, None]
    x = np.clip(x, -0.98, 0.98)
    with wave.open(str(mix_path), "wb") as w:
        w.setnchannels(ch); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


IMPORT_JSX = "import { BotonSuscribete } from './BotonSuscribete.jsx';"
RENDER_JSX = ("      {timeline.inscricao && <Sequence from={timeline.inscricao.from} durationInFrames={timeline.inscricao.dur}>"
              "<BotonSuscribete dur={timeline.inscricao.dur} clique={timeline.inscricao.clique} /></Sequence>}\n")


def ligar_video_jsx(src):
    """Garante no Video.jsx o import e o <Sequence> do botão (idempotente; âncoras do template 016/017)."""
    p = src / "Video.jsx"; s = p.read_text()
    mudou = False
    if "BotonSuscribete" not in s:
        m = re.search(r"^import timeline from '\./timeline\.json';\n", s, re.M)
        if not m: raise SystemExit("Video.jsx sem a linha \"import timeline from './timeline.json';\": ligue o botão à mão (ver LEIA.md)")
        s = s[: m.end()] + IMPORT_JSX + "\n" + s[m.end():]
        k = s.find("      <Audio src={staticFile('audio/mix.wav')} />")
        if k < 0: raise SystemExit("Video.jsx sem a linha do <Audio … mix.wav>: ligue o botão à mão (ver LEIA.md)")
        s = s[:k] + RENDER_JSX + s[k:]
        mudou = True
    if mudou: p.write_text(s)
    return mudou


def achar_bloco(V):
    blocos = json.load(open(V / "blocos.json"))
    ach = [b for b in blocos if e_cta(b["texto"])]
    if len(ach) != 1:
        raise SystemExit(f"{len(ach)} blocos com a frase do CTA de inscrição em blocos.json (precisa de 1): rode o checador do roteiro")
    return ach[0]["id"]


def cmd_montar(V):
    bid = achar_bloco(V)
    q = {b["id"]: b for b in json.load(open(V / "qa/blocos.json"))}[bid]
    tl_p = V / "src/timeline.json"; tl = json.load(open(tl_p))
    dur = tl["frames"] / FPS
    mp3 = V / "audio" / f"{bid}.mp3"
    c = momento_clique(mp3) if mp3.exists() else None
    voz = q["fim"] - q["ini"]
    if c is None or c > voz - 1.5: c = voz * len("Si te está gustando este expediente, suscríbe") / len(TEXTO)
    f0 = round(q["ini"] * FPS) - 6                       # entra 0,2 s antes da fala
    fz = round((q["fim"] + 0.4) * FPS)                   # sai logo depois da frase (antes do cartão do capítulo)
    clique = round(q["ini"] * FPS + c * FPS) - f0
    tl["inscricao"] = {"from": f0, "dur": fz - f0, "clique": clique, "bloco": bid}
    json.dump(tl, open(tl_p, "w"), ensure_ascii=False, indent=0)
    shutil.copyfile(AQUI / COMPONENTE, V / "src" / COMPONENTE)
    ligou = ligar_video_jsx(V / "src")

    # SFX: clique no botão e sininho (idempotente: só se o mix.wav mudou desde a última montagem)
    mix = V / "public/audio/mix.wav"; reg_p = V / "qa/cta-inscricao.json"
    reg = json.load(open(reg_p)) if reg_p.exists() else {}
    t_clique = (f0 + clique) / FPS; t_sino = (f0 + min(clique + 24, fz - f0 - 24)) / FPS
    sfx = "sem mix.wav"
    if mix.exists():
        if reg.get("mix_mtime_ns") == mix.stat().st_mtime_ns and reg.get("t_clique") == round(t_clique, 3):
            sfx = "já aplicado"
        else:
            cl, si = sfx_clique_sino(); mix_sfx(mix, [(t_clique, cl), (t_sino + 0.05, si)]); sfx = "aplicado"

    hq = json.load(open(V / "qa/cta.json")) if (V / "qa/cta.json").exists() else None
    pct = 100 * q["ini"] / dur
    dist = None
    if hq: dist = q["ini"] - hq["fim_s"] if q["ini"] >= hq["fim_s"] else hq["ini_s"] - q["fim"]
    ok = FAIXA[0] <= pct <= FAIXA[1] and (dist is None or dist >= DIST_HQ)
    reg = {"bloco": bid, "ini_s": q["ini"], "fim_s": q["fim"], "pct": round(pct, 1), "dist_hq_s": None if dist is None else round(dist, 1),
           "from": f0, "dur": fz - f0, "clique": clique, "t_clique": round(t_clique, 3), "t_sino": round(t_sino, 3), "ok": ok,
           "mix_mtime_ns": mix.stat().st_mtime_ns if mix.exists() else None}
    json.dump(reg, open(reg_p, "w"), ensure_ascii=False, indent=1)
    print(f"CTA de inscrição: {bid} {fmt(q['ini'])}–{fmt(q['fim'])} ({pct:.1f}%), "
          f"{'sem CTA da HQ' if dist is None else f'{dist:.0f} s do CTA da HQ'}; botão {f0}+{fz - f0} quadros, clique em {fmt(t_clique)}; "
          f"Video.jsx {'ligado agora' if ligou else 'já ligado'}; SFX {sfx}; {'OK' if ok else 'FORA DA REGRA (55–70% e ≥ 120 s da HQ)'}")
    return 0 if ok else 1


# ───────────────────────── qa ─────────────────────────
def whisper_trecho(video, a, z):
    from faster_whisper import WhisperModel
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.2f}", "-t", f"{z - a:.2f}", "-i", str(video), "-vn", "-ac", "1",
                          "-ar", "16000", "-f", "f32le", "-"], capture_output=True, check=True).stdout
    audio = np.frombuffer(raw, dtype=np.float32)
    m = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio, language="es", beam_size=5, vad_filter=False)
    return " ".join(s.text.strip() for s in segs)


def cobertura(ouvido):
    """Fração das palavras do TEXTO achadas em ordem no que o Whisper ouviu (tolera palavras a mais nas bordas)."""
    alvo, o = norm(TEXTO), norm(ouvido)
    sm = SequenceMatcher(None, alvo, o, autojunk=False)
    return sum(b.size for b in sm.get_matching_blocks()) / len(alvo)


def botao_visivel(frame_jpg):
    """Na CAIXA: vermelho do botão (#B3261E) e papel da ficha (#E9DFC9). Devolve (ok, %vermelho, %papel)."""
    from PIL import Image
    im = np.asarray(Image.open(frame_jpg).convert("RGB").crop(CAIXA)).astype(int)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    verm = (r > 130) & (r - g > 70) & (r - b > 60)
    papel = (abs(r - 0xE9) < 28) & (abs(g - 0xDF) < 28) & (abs(b - 0xC9) < 32)
    pv, pp = verm.mean() * 100, papel.mean() * 100
    return bool(pv > 8 and pp > 8), round(float(pv), 1), round(float(pp), 1)


def cmd_qa(V, sem_posicao=False):
    video = V / "out/video.mp4"
    reg = json.load(open(V / "qa/cta-inscricao.json"))
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                               capture_output=True, text=True, check=True).stdout)
    ouvido = whisper_trecho(video, max(0, reg["ini_s"] - 0.6), min(dur, reg["fim_s"] + 0.8))
    cob = cobertura(ouvido)
    t_frame = (reg["from"] + max(14, reg["clique"] - 10)) / FPS     # botão já entrou e ainda não foi clicado
    jpg = V / "qa/cta-inscricao.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t_frame:.2f}", "-i", str(video), "-frames:v", "1", "-q:v", "3", str(jpg)], check=True)
    vis, pv, pp = botao_visivel(jpg)
    pct = 100 * reg["ini_s"] / dur
    hq = json.load(open(V / "qa/cta.json")) if (V / "qa/cta.json").exists() else None
    dist = reg.get("dist_hq_s")
    itens = {"frase_whisper": bool(cob >= 0.85), "botao_visivel": bool(vis)}
    if not sem_posicao:
        itens["posicao_55_70"] = bool(FAIXA[0] <= pct <= FAIXA[1])
        itens["dist_hq_120s"] = bool(dist is None or dist >= DIST_HQ)
    out = {"bloco": reg["bloco"], "ini": fmt(reg["ini_s"]), "pct": round(pct, 1), "dist_hq_s": dist, "cta_hq": bool(hq),
           "whisper": ouvido, "cobertura": round(cob * 100, 1), "frame_s": round(t_frame, 2), "vermelho_pct": pv, "papel_pct": pp,
           "itens": itens, "aprovado": all(itens.values())}
    json.dump(out, open(V / "qa/cta-inscricao-qa.json", "w"), ensure_ascii=False, indent=1)
    print(f"CTA de inscrição (QA): {reg['bloco']} em {fmt(reg['ini_s'])} ({pct:.1f}%), "
          f"{'sem CTA da HQ' if dist is None else f'{dist:.0f} s do CTA da HQ'}; Whisper {cob * 100:.0f}% \"{ouvido}\"; "
          f"botão no frame {fmt(t_frame)} (vermelho {pv}%, papel {pp}%) → qa/cta-inscricao.jpg")
    for k, v in itens.items(): print(f"  [{'x' if v else ' '}] {k}")
    print("  APROVADO" if out["aprovado"] else "  REPROVADO")
    return 0 if out["aprovado"] else 1


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("roteiro", "montar", "qa"):
        print(__doc__); return 2
    V = Path(sys.argv[2]).resolve()
    if sys.argv[1] == "roteiro": return cmd_roteiro(V)
    if sys.argv[1] == "montar": return cmd_montar(V)
    return cmd_qa(V, "--sem-posicao" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
