"""Narração com Fish Audio usando a voz do canal, com o custo registrado no banco (financas.consumo).

Uso:
  tools/.venv/bin/python tools/tts_fish.py <canal> <entrada> <pasta_saida> [--video <youtube.videos.id>]
  <entrada>: .json (lista de {"id": "P01", "texto": "..."}) ou .txt (parágrafos separados por linha em branco).
Lê motor, voz, modelo e velocidade de canais/<canal>/canal.yaml (seção voz). Gera <pasta_saida>/<id>.mp3.
O texto pode levar marcações do Fish: [break], [long-break], [emphasis], [determined], [soft tone]…
A chave vem de ~/.segredos/fish.env (FISH_API_KEY).

--por-frase (padrão do historia-ptbr desde o A/B do 003, 04/11/2026; ver canais/historia-ptbr/videos/003-ira/amostras-voz/LEIA.md):
  gera cada frase do bloco numa chamada, apara o silêncio e junta com --pausa-frase s de silêncio (padrão 0,32).
  A pausa vira controlada (não depende de [break]) e a entonação repete menos entre frases.
  Cache por frase em <saida>/frases/<hash>.mp3: rodar de novo só gera (e cobra) as frases novas ou alteradas;
  para regerar uma frase ruim, apague o mp3 dela (o mapa bloco → frases fica em <saida>/frases/mapa.json).
  A tag de tom no início do bloco vale só para a 1ª frase; frase de 1–2 palavras ("Como?") é gerada junto com a seguinte.
--temperature/--top-p repassam à API (padrão do Fish: 0,7/0,7).
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request

import numpy as np

import yaml

from _paths import FABRICA
from db import tentar

# US$ por milhão de bytes UTF-8 (docs.fish.audio, "Pricing and Rate Limits"). Atualize se o Fish mudar o preço.
PRECO_POR_MI_BYTES = {"s2.1-pro": 15.0, "s2.1-pro-free": 0.0, "drama-3": 50.0}


def chave():
    for linha in open(os.path.expanduser("~/.segredos/fish.env")):
        if linha.startswith("FISH_API_KEY="):
            return linha.split("=", 1)[1].strip()
    sys.exit("FISH_API_KEY não encontrada em ~/.segredos/fish.env")


def blocos(entrada):
    if entrada.endswith(".json"):
        return [(b["id"], b["texto"]) for b in json.load(open(entrada))]
    partes = [p.strip() for p in open(entrada).read().split("\n\n") if p.strip()]
    return [(f"P{i:02d}", p) for i, p in enumerate(partes, 1)]


def gerar(key, voz, modelo, velocidade, texto, destino, extra=None):
    """extra: parâmetros opcionais da API (temperature, top_p, language, chunk_length...; docs.fish.audio, TTS)."""
    corpo = {"text": texto, "reference_id": voz, "format": "mp3", "mp3_bitrate": 192}
    if velocidade and float(velocidade) != 1.0:
        corpo["prosody"] = {"speed": float(velocidade)}
    corpo.update(extra or {})
    req = urllib.request.Request("https://api.fish.audio/v1/tts", data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "model": modelo})
    with urllib.request.urlopen(req, timeout=300) as r, open(destino, "wb") as f:
        f.write(r.read())


FRASE = re.compile(r"(?<=[.?!…])\s+(?=[\[A-ZÀ-Ú\"“])")
TAG = re.compile(r"\[[^\]]*\]")


def frases(texto):
    """Divide o bloco em frases; junta frase de 1–2 palavras faladas à seguinte (sozinha, o Fish a entoa mal ou corta)."""
    fs = [f.strip() for f in FRASE.split(texto) if f.strip()]
    out = []
    for f in fs:
        if out and len(TAG.sub("", out[-1]).split()) <= 2:
            out[-1] = f"{out[-1]} {f}"
        else:
            out.append(f)
    if len(out) > 1 and len(TAG.sub("", out[-1]).split()) <= 2:
        out[-2:] = [f"{out[-2]} {out[-1]}"]
    return out


SR = 44100


def ler(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32)


def aparar(x, lim_db=-45, cab=0.03, cauda=0.12):
    w = int(0.01 * SR); n = len(x) // w
    if n == 0:
        return x
    rms = 20 * np.log10(np.sqrt(np.mean(x[: n * w].reshape(n, w) ** 2, axis=1) + 1e-12))
    v = np.where(rms > lim_db)[0]
    return x if not len(v) else x[max(0, v[0] * w - int(cab * SR)): min(len(x), (v[-1] + 1) * w + int(cauda * SR))]


def juntar(partes, pausa, destino):
    sil = np.zeros(int(pausa * SR), dtype=np.float32)
    seq = []
    for i, x in enumerate(partes):
        seq += ([sil] if i else []) + [aparar(x)]
    y = np.concatenate(seq)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "pipe:0",
                    "-b:a", "192k", destino], input=y.astype(np.float32).tobytes(), check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canal")
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--video", type=int, help="id em youtube.videos, para atribuir o custo ao vídeo")
    ap.add_argument("--por-frase", action="store_true", help="uma chamada por frase + silêncio inserido (ver doc)")
    ap.add_argument("--pausa-frase", type=float, default=0.32, help="s de silêncio entre frases no modo --por-frase")
    ap.add_argument("--temperature", type=float)
    ap.add_argument("--top-p", type=float)
    a = ap.parse_args()
    cfg = yaml.safe_load(open(os.path.join(FABRICA, "canais", a.canal, "canal.yaml")))["voz"]
    if cfg.get("motor") != "fish":
        sys.exit(f"O canal {a.canal} não usa Fish (motor={cfg.get('motor')}).")
    modelo = cfg.get("modelo", "s2.1-pro")
    if modelo not in PRECO_POR_MI_BYTES:
        sys.exit(f"Modelo {modelo} sem preço cadastrado em PRECO_POR_MI_BYTES.")
    key = chave()
    os.makedirs(a.saida, exist_ok=True)
    extra = {k: v for k, v in (("temperature", a.temperature), ("top_p", a.top_p)) if v is not None}
    total_bytes = 0
    try:  # registra o custo do que foi gerado mesmo se cair no meio
        if a.por_frase:
            cache = os.path.join(a.saida, "frases")
            os.makedirs(cache, exist_ok=True)
            mapa_p = os.path.join(cache, "mapa.json")
            mapa = json.load(open(mapa_p)) if os.path.exists(mapa_p) else {}
            assin = json.dumps([cfg["voz"], modelo, cfg.get("velocidade"), extra], sort_keys=True)
            for bid, texto in blocos(a.entrada):
                fs, partes, novas = frases(texto), [], 0
                mapa[bid] = []
                for f in fs:
                    h = hashlib.sha1((assin + f).encode()).hexdigest()[:12]
                    p = os.path.join(cache, f"{h}.mp3")
                    mapa[bid].append({"frase": f, "mp3": f"{h}.mp3"})
                    if not os.path.exists(p):
                        gerar(key, cfg["voz"], modelo, cfg.get("velocidade"), f, p, extra)
                        total_bytes += len(f.encode("utf-8")); novas += 1
                    partes.append(ler(p))
                destino = os.path.join(a.saida, f"{bid}.mp3")
                juntar(partes, a.pausa_frase, destino)
                json.dump(mapa, open(mapa_p, "w"), ensure_ascii=False, indent=0)
                print(f"{bid}: ok ({len(fs)} frases, {novas} geradas agora) → {destino}")
        else:
            for bid, texto in blocos(a.entrada):
                destino = os.path.join(a.saida, f"{bid}.mp3")
                gerar(key, cfg["voz"], modelo, cfg.get("velocidade"), texto, destino, extra)
                total_bytes += len(texto.encode("utf-8"))
                print(f"{bid}: ok ({len(texto.encode('utf-8'))} bytes) → {destino}")
    finally:
        if total_bytes:
            registrar_custo(a, modelo, total_bytes)
    if not total_bytes:
        print("Nada novo gerado (tudo em cache); nenhum custo.")


def registrar_custo(a, modelo, total_bytes):
    custo = total_bytes * PRECO_POR_MI_BYTES[modelo] / 1_000_000

    def registrar(con):
        cambio = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='Fish Audio'").fetchone()
        con.execute(
            "INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
            " VALUES ('youtube', %s, 'Fish Audio', %s, %s, 'bytes', %s, 'USD', %s, %s, %s, %s)",
            (a.canal, f"tts {modelo}", total_bytes, custo, custo * float(cambio[0]) if cambio else None,
             "youtube.video" if a.video else None, a.video, os.path.basename(a.entrada)))
    tentar(registrar)
    print(f"\nTotal: {total_bytes} bytes · US$ {custo:.4f} ({modelo}) · registrado em financas.consumo")


if __name__ == "__main__":
    main()
