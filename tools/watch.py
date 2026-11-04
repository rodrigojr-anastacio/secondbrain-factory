""""Assiste" vídeos de referência: hook transcrito, frames de edição, ritmo de cortes e anúncios.

Uso:
  ~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/tools/watch.py <VIDEO_ID> [<VIDEO_ID> ...]
  ~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/tools/watch.py --garimpo pesquisa/tendencias/AAAA-MM-DD.json [--top 6]
      (pega o vídeo de maior views de cada um dos N primeiros candidatos)

Tudo passa pelo Cloudflare WARP (SOCKS5 127.0.0.1:40000), porque o YouTube bloqueia o IP da VPS.
Saída por vídeo em pesquisa/tendencias/assets/<data>/<id>/:
  hook.txt (transcrição dos primeiros 90 s), hook_sheet.jpg (1 frame a cada 3 s nos primeiros 60 s),
  video_sheet.jpg (12 frames do vídeo inteiro), thumb.jpg e info.json (duração, cortes por minuto, anúncios…).
O vídeo baixado é apagado no fim.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import tempfile
import wave

from _paths import TENDENCIAS, VENV_BIN
from db import Jsonb, tentar

PROXY = "socks5://127.0.0.1:40000"
NODE = os.path.expanduser("~/.hermes/tools/node-26.12.1-linux-x64/bin/node")
OUT = os.path.join(TENDENCIAS, "assets")
_model = None


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def anuncios(video_id):
    """Sinal de anúncios na página. Atenção: o YouTube exibe anúncios até em canais fora do YPP,
    então isso é indício, não prova, de monetização."""
    r = run(["curl", "-s", "--max-time", "40", "--socks5-hostname", "127.0.0.1:40000", "-A", "Mozilla/5.0",
             "-H", "Accept-Language: en-US", f"https://www.youtube.com/watch?v={video_id}"])
    html = r.stdout
    status = re.search(r'playabilityStatus":\{"status":"([A-Z_]+)"', html)
    return {
        "pagina_status": status.group(1) if status else "desconhecido",
        "anuncios_na_pagina": bool(re.search(r'"(adPlacements|playerAds|adSlots)"', html)),
    }


def baixar(video_id, pasta):
    r = run([f"{VENV_BIN}/yt-dlp", "-q", "--no-warnings", "--proxy", PROXY, "--js-runtimes", f"node:{NODE}",
             "-f", "bv*[height<=360]+ba/b[height<=360]/18", "--write-thumbnail", "--convert-thumbnails", "jpg",
             "--print-json", "-o", os.path.join(pasta, "v.%(ext)s"), f"https://www.youtube.com/watch?v={video_id}"],
            timeout=600)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[-300:])
    meta = json.loads(r.stdout.strip().splitlines()[-1])
    video = next(os.path.join(pasta, f) for f in os.listdir(pasta) if f.startswith("v.") and not f.endswith(".jpg"))
    thumb = next((os.path.join(pasta, f) for f in os.listdir(pasta) if f.endswith(".jpg")), None)
    return meta, video, thumb


def transcrever(video, pasta, segundos=90):
    global _model
    from faster_whisper import WhisperModel
    import numpy as np
    wav = os.path.join(pasta, "hook.wav")
    run(["ffmpeg", "-v", "error", "-y", "-t", str(segundos), "-i", video, "-ac", "1", "-ar", "16000", wav])
    w = wave.open(wav)
    audio = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    _model = _model or WhisperModel("base", device="cpu", compute_type="int8")
    segs, info = _model.transcribe(audio)
    linhas = [f"[{int(s.start)//60}:{int(s.start)%60:02d}] {s.text.strip()}" for s in segs]
    return info.language, "\n".join(linhas)


def cortes_por_minuto(video, ate=60):
    r = run(["ffmpeg", "-v", "info", "-t", str(ate), "-i", video, "-vf", "select='gt(scene,0.3)',showinfo",
             "-f", "null", "-"])
    return round(len(re.findall(r"pts_time:", r.stderr)) * 60 / ate, 1)


def sheets(video, destino, duracao):
    run(["ffmpeg", "-v", "error", "-y", "-t", "60", "-i", video, "-vf",
         "fps=1/3,scale=320:-1,tile=5x4:padding=4", "-frames:v", "1", "-q:v", "4", os.path.join(destino, "hook_sheet.jpg")])
    passo = max(duracao / 12, 1)
    run(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf",
         f"fps=1/{passo:.2f},scale=320:-1,tile=4x3:padding=4", "-frames:v", "1", "-q:v", "4",
         os.path.join(destino, "video_sheet.jpg")])


def assistir(video_id, destino_base, canal=None):
    destino = os.path.join(destino_base, video_id)
    os.makedirs(destino, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="watch_")
    info = {"video_id": video_id, "url": f"https://www.youtube.com/watch?v={video_id}", "canal": canal}
    try:
        info.update(anuncios(video_id))
        meta, video, thumb = baixar(video_id, tmp)
        info.update({"titulo": meta.get("title"), "duracao_s": meta.get("duration"), "views": meta.get("view_count"),
                     "canal_nome": meta.get("channel"), "capitulos": [c.get("title") for c in meta.get("chapters") or []],
                     "descricao": (meta.get("description") or "")[:600]})
        if thumb:
            shutil.copy(thumb, os.path.join(destino, "thumb.jpg"))
        info["idioma"], hook = transcrever(video, tmp)
        open(os.path.join(destino, "hook.txt"), "w").write(hook)
        info["cortes_por_min_inicio"] = cortes_por_minuto(video)
        sheets(video, destino, meta.get("duration") or 600)
        info["ok"] = True
    except Exception as e:
        info["ok"] = False
        info["erro"] = str(e)[:300]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    json.dump(info, open(os.path.join(destino, "info.json"), "w"), ensure_ascii=False, indent=1)
    if info.get("ok"):
        hook_txt = open(os.path.join(destino, "hook.txt")).read()
        tentar(lambda con: con.execute(
            "INSERT INTO assistidos(video_id, titulo, canal, idioma, duracao_s, cortes_por_min, anuncios, hook, capitulos, assets)"
            " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (video_id) DO UPDATE SET"
            " titulo=EXCLUDED.titulo, cortes_por_min=EXCLUDED.cortes_por_min, anuncios=EXCLUDED.anuncios,"
            " hook=EXCLUDED.hook, capitulos=EXCLUDED.capitulos, assets=EXCLUDED.assets, analisado_em=now()",
            (video_id, info.get("titulo"), info.get("canal_nome"), info.get("idioma"), info.get("duracao_s"),
             info.get("cortes_por_min_inicio"), info.get("anuncios_na_pagina"), hook_txt, Jsonb(info.get("capitulos")), destino)))
    print(f"{'OK ' if info['ok'] else 'ERRO'} {video_id} · {info.get('titulo', '')} · "
          f"cortes/min={info.get('cortes_por_min_inicio')} · anúncios={info.get('anuncios_na_pagina')} → {destino}")
    return info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--garimpo")
    ap.add_argument("--top", type=int, default=6)
    a = ap.parse_args()
    destino_base = os.path.join(OUT, dt.date.today().isoformat())
    alvos = [(i, None) for i in a.ids]
    if a.garimpo:
        dados = json.load(open(a.garimpo))
        for c in dados["candidatos"][: a.top]:
            if c.get("videos_lista"):
                alvos.append((c["videos_lista"][0]["id"], c["titulo"]))
    if not alvos:
        ap.error("informe IDs de vídeo ou --garimpo")
    resultados = [assistir(v, destino_base, canal) for v, canal in alvos]
    json.dump(resultados, open(os.path.join(destino_base, "resumo.json"), "w"), ensure_ascii=False, indent=1)
    print(f"\nResumo: {os.path.join(destino_base, 'resumo.json')}")


if __name__ == "__main__":
    main()
