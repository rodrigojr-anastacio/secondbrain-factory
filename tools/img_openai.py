"""Gera imagens em lote na OpenAI (gpt-image), no estilo do canal, com o custo registrado no banco (financas.consumo).

Uso:
  tools/.venv/bin/python tools/img_openai.py <canal> <cenas.json> <pasta_saida> [--video <id>] [--qualidade low|medium|high] [--paralelo 4]
  <cenas.json>: lista de {"id": "S001", "prompt": "descrição da cena", "qualidade": "low"} (o campo qualidade é opcional, por cena).
Estilo, modelo e qualidade padrão vêm de canais/<canal>/canal.yaml (seção visual: modelo_openai, estilo_prompt, qualidade).
Gera JPG 1536x1024. As imagens que já existem são puladas, então dá para rodar de novo depois de falhas.
Trava anti-duplicação: um processo por pasta de saída (<pasta>/.img.lock); um 2º processo na mesma pasta sai com
aviso (código 3). Cada id é re-checado logo antes da chamada paga.
A chave vem de ~/.segredos/openai.env (linha OPENAI=...).
"""
import argparse
import base64
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import yaml

from _paths import FABRICA
from _trava import travar_pasta
from db import tentar

# US$ por milhão de tokens de imagem gerados (preço oficial: developers.openai.com/api/docs/guides/image-generation#cost-and-latency; bate com o saldo real em 02/11/2026).
PRECO_SAIDA_POR_MI = {"gpt-image-2": 30.0, "gpt-image-2.5-flare": 30.0, "gpt-image-2.5-sunburst": 30.0, "gpt-image-1-mini": 8.0}
PRECO_ENTRADA_TEXTO_POR_MI = 5.0


def chave():
    for linha in open(os.path.expanduser("~/.segredos/openai.env")):
        if linha.startswith("OPENAI="):
            return linha.split("=", 1)[1].strip()
    sys.exit("Linha OPENAI= não encontrada em ~/.segredos/openai.env")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canal")
    ap.add_argument("cenas")
    ap.add_argument("saida")
    ap.add_argument("--video", type=int)
    ap.add_argument("--qualidade")
    ap.add_argument("--paralelo", type=int, default=4)
    a = ap.parse_args()
    visual = (yaml.safe_load(open(os.path.join(FABRICA, "canais", a.canal, "canal.yaml"))) or {}).get("visual", {})
    modelo = visual.get("modelo_openai", "gpt-image-2")
    estilo = visual.get("estilo_prompt", "")
    qual_padrao = a.qualidade or visual.get("qualidade", "medium")
    key = chave()
    os.makedirs(a.saida, exist_ok=True)
    trava = travar_pasta(a.saida)  # noqa: F841  (um processo por pasta; sai com aviso se já houver outro)
    cenas = json.load(open(a.cenas))
    pendentes = [c for c in cenas if not os.path.exists(os.path.join(a.saida, f"{c['id']}.jpg"))]
    tok_in = tok_out = 0
    ok, falhas, puladas = 0, [], 0

    def uma(c):
        if os.path.exists(os.path.join(a.saida, f"{c['id']}.jpg")):  # re-checa logo antes da chamada paga
            return None
        corpo = {"model": modelo, "prompt": f"{c['prompt']}. {estilo}", "size": "1536x1024",
                 "quality": c.get("qualidade", qual_padrao), "n": 1}
        req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=json.dumps(corpo).encode(),
                                     headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=300))
        except urllib.error.HTTPError as e:
            raise RuntimeError(e.read().decode()[:200]) from None
        png = base64.b64decode(r["data"][0]["b64_json"])
        destino = os.path.join(a.saida, f"{c['id']}.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "pipe:0", "-q:v", "3", destino], input=png, check=True)
        u = r.get("usage", {})
        return u.get("input_tokens", 0), u.get("output_tokens", 0)

    with ThreadPoolExecutor(max_workers=a.paralelo) as ex:
        for c, fut in [(c, ex.submit(uma, c)) for c in pendentes]:
            try:
                r = fut.result()
                if r is None:
                    puladas += 1
                    print(f"{c['id']}: já existe (pulada)")
                    continue
                ti, to = r
                tok_in += ti
                tok_out += to
                ok += 1
                print(f"{c['id']}: ok")
            except Exception as e:  # noqa: BLE001
                falhas.append(c["id"])
                print(f"{c['id']}: ERRO {str(e)[:160]}")
    custo = tok_out * PRECO_SAIDA_POR_MI.get(modelo, 40.0) / 1e6 + tok_in * PRECO_ENTRADA_TEXTO_POR_MI / 1e6

    def registrar(con):
        cambio = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='OpenAI'").fetchone()
        con.execute(
            "INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
            " VALUES ('youtube', %s, 'OpenAI', %s, %s, 'imagens', %s, 'USD', %s, %s, %s, %s)",
            (a.canal, f"imagem {modelo} {qual_padrao}", ok, custo, custo * float(cambio[0]) if cambio else None,
             "youtube.video" if a.video else None, a.video,
             f"{os.path.basename(a.cenas)}; {tok_out} tokens de saída; custo estimado"))
    if ok:
        tentar(registrar)
    print(f"\n{ok} geradas, {len(cenas) - len(pendentes) + puladas} já existiam, {len(falhas)} falhas · ~US$ {custo:.3f} (estimado, {modelo})")
    if falhas:
        print("Falharam (rode de novo para tentar só estas):", ", ".join(falhas))


if __name__ == "__main__":
    main()
