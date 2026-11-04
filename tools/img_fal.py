"""Gera imagens em lote no fal.ai, no estilo visual do canal, com o custo registrado no banco (financas.consumo).

Uso:
  tools/.venv/bin/python tools/img_fal.py <canal> <cenas.json> <pasta_saida> [--video <id>] [--modelo fal-ai/flux/dev] [--paralelo 4]
  <cenas.json>: lista de {"id": "S001", "prompt": "descrição da cena"} (o estilo do canal é adicionado sozinho).
O estilo e o modelo padrão vêm de canais/<canal>/canal.yaml (seção visual: modelo, estilo_prompt, tamanho).
As imagens que já existem na pasta são puladas, então dá para rodar de novo depois de uma falha.
A chave vem de ~/.segredos/fal.env (FAL_KEY).
"""
import argparse
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import yaml

from _paths import FABRICA
from db import tentar

# US$ por imagem (~1 MP, 16:9) segundo as páginas dos modelos no fal.ai. Atualize se mudar.
PRECO_POR_IMAGEM = {
    "fal-ai/flux/schnell": 0.003,
    "fal-ai/flux/dev": 0.025,
    "fal-ai/flux-pro/v1.1": 0.04,
    "fal-ai/recraft/v3/text-to-image": 0.04,
    "fal-ai/imagen4/preview/fast": 0.02,
    "fal-ai/nano-banana": 0.039,
}


def chave():
    for linha in open(os.path.expanduser("~/.segredos/fal.env")):
        if linha.startswith("FAL_KEY="):
            return linha.split("=", 1)[1].strip()
    sys.exit("FAL_KEY não encontrada em ~/.segredos/fal.env")


def gerar(key, modelo, prompt, tamanho, destino, seed=None):
    corpo = {"prompt": prompt, "image_size": tamanho, "num_images": 1, "enable_safety_checker": True}
    if seed is not None:
        corpo["seed"] = seed
    req = urllib.request.Request(f"https://fal.run/{modelo}", data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        url = json.load(r)["images"][0]["url"]
    urllib.request.urlretrieve(url, destino)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canal")
    ap.add_argument("cenas")
    ap.add_argument("saida")
    ap.add_argument("--video", type=int, help="id em youtube.videos, para atribuir o custo ao vídeo")
    ap.add_argument("--modelo")
    ap.add_argument("--paralelo", type=int, default=4)
    a = ap.parse_args()
    visual = (yaml.safe_load(open(os.path.join(FABRICA, "canais", a.canal, "canal.yaml"))) or {}).get("visual", {})
    modelo = a.modelo or visual.get("modelo", "fal-ai/flux/dev")
    estilo = visual.get("estilo_prompt", "")
    tamanho = visual.get("tamanho", "landscape_16_9")
    if modelo not in PRECO_POR_IMAGEM:
        sys.exit(f"Modelo {modelo} sem preço em PRECO_POR_IMAGEM; cadastre antes de usar.")
    key = chave()
    os.makedirs(a.saida, exist_ok=True)
    cenas = json.load(open(a.cenas))
    pendentes = [c for c in cenas if not os.path.exists(os.path.join(a.saida, f"{c['id']}.jpg"))]
    ok, falhas = 0, []

    def uma(c):
        prompt = f"{c['prompt']}. {estilo}".strip(". ") if estilo else c["prompt"]
        gerar(key, modelo, prompt, tamanho, os.path.join(a.saida, f"{c['id']}.jpg"), c.get("seed"))
        return c["id"]

    with ThreadPoolExecutor(max_workers=a.paralelo) as ex:
        for c, fut in [(c, ex.submit(uma, c)) for c in pendentes]:
            try:
                fut.result()
                ok += 1
                print(f"{c['id']}: ok")
            except Exception as e:  # noqa: BLE001
                falhas.append(c["id"])
                print(f"{c['id']}: ERRO {str(e)[:160]}")
    custo = ok * PRECO_POR_IMAGEM[modelo]

    def registrar(con):
        cambio = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='fal.ai'").fetchone()
        con.execute(
            "INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
            " VALUES ('youtube', %s, 'fal.ai', %s, %s, 'imagens', %s, 'USD', %s, %s, %s, %s)",
            (a.canal, f"imagem {modelo}", ok, custo, custo * float(cambio[0]) if cambio else None,
             "youtube.video" if a.video else None, a.video, os.path.basename(a.cenas)))
    if ok:
        tentar(registrar)
    print(f"\n{ok} geradas, {len(cenas) - len(pendentes)} já existiam, {len(falhas)} falhas · US$ {custo:.3f} ({modelo})")
    if falhas:
        print("Falharam (rode de novo para tentar só estas):", ", ".join(falhas))


if __name__ == "__main__":
    main()
