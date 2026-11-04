"""Narração com Fish Audio usando a voz do canal, com o custo registrado no banco (financas.consumo).

Uso:
  tools/.venv/bin/python tools/tts_fish.py <canal> <entrada> <pasta_saida> [--video <youtube.videos.id>]
  <entrada>: .json (lista de {"id": "P01", "texto": "..."}) ou .txt (parágrafos separados por linha em branco).
Lê motor, voz, modelo e velocidade de canais/<canal>/canal.yaml (seção voz). Gera <pasta_saida>/<id>.mp3.
O texto pode levar marcações do Fish: [break], [long-break], [emphasis], [determined], [soft tone]…
A chave vem de ~/.segredos/fish.env (FISH_API_KEY).
"""
import argparse
import json
import os
import sys
import urllib.request

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


def gerar(key, voz, modelo, velocidade, texto, destino):
    corpo = {"text": texto, "reference_id": voz, "format": "mp3", "mp3_bitrate": 192}
    if velocidade and float(velocidade) != 1.0:
        corpo["prosody"] = {"speed": float(velocidade)}
    req = urllib.request.Request("https://api.fish.audio/v1/tts", data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "model": modelo})
    with urllib.request.urlopen(req, timeout=300) as r, open(destino, "wb") as f:
        f.write(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canal")
    ap.add_argument("entrada")
    ap.add_argument("saida")
    ap.add_argument("--video", type=int, help="id em youtube.videos, para atribuir o custo ao vídeo")
    a = ap.parse_args()
    cfg = yaml.safe_load(open(os.path.join(FABRICA, "canais", a.canal, "canal.yaml")))["voz"]
    if cfg.get("motor") != "fish":
        sys.exit(f"O canal {a.canal} não usa Fish (motor={cfg.get('motor')}).")
    modelo = cfg.get("modelo", "s2.1-pro")
    if modelo not in PRECO_POR_MI_BYTES:
        sys.exit(f"Modelo {modelo} sem preço cadastrado em PRECO_POR_MI_BYTES.")
    key = chave()
    os.makedirs(a.saida, exist_ok=True)
    total_bytes = 0
    for bid, texto in blocos(a.entrada):
        destino = os.path.join(a.saida, f"{bid}.mp3")
        gerar(key, cfg["voz"], modelo, cfg.get("velocidade"), texto, destino)
        total_bytes += len(texto.encode("utf-8"))
        print(f"{bid}: ok ({len(texto.encode('utf-8'))} bytes) → {destino}")
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
