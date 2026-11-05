"""Gera imagens em lote no fal.ai, no estilo visual do canal, com o custo registrado no banco (financas.consumo).

Uso:
  tools/.venv/bin/python tools/img_fal.py <canal> <cenas.json> <pasta_saida> [--video <id>] [--modelo <endpoint>] [--paralelo 4]
        [--so I001,I002] [--teto 10.0] [--notas "v2"]
  <cenas.json>: lista de {"id": "S001", "prompt": "descrição da cena"} (o estilo do canal é adicionado sozinho).
O estilo, o modelo e os parâmetros vêm de canais/<canal>/canal.yaml (seção visual: modelo, estilo_prompt, tamanho, refs,
ref_instrucao, parametros).
- Modelos de edição (endpoint terminando em /edit): recebem as `refs` do canal.yaml (caminhos relativos à pasta do canal)
  como referência de ESTILO, com a `ref_instrucao` antes do prompt (historia-ptbr, 05/11/2026: nano-banana-2.1/edit + 3 imagens
  gpt-image-2 do Egito e da Índia, para manter os bonequinhos de cabeça redonda).
- A saída é sempre reescalada para visual.tamanho (padrão 1536x864) e salva em JPEG.
- Imagem preta/vazia (filtro de segurança do fal devolve preto SEM erro; 003 v1) conta como FALHA e é apagada.
- Custo REAL: lê o gasto do endpoint no fal (api.fal.ai/v1/models/usage) antes e depois e registra a diferença (o preço do fal
  é por megapixel/token e varia; o preço fixo antigo subestimava). Isso isola o custo de outro job em OUTRO endpoint; no mesmo
  endpoint ao mesmo tempo, mistura. Plano B: diferença do saldo (account/billing); plano C: PRECO_POR_IMAGEM.
As imagens que já existem na pasta são puladas, então dá para rodar de novo depois de uma falha.
Trava anti-duplicação: um processo por pasta de saída (<pasta>/.img.lock); um 2º processo na mesma pasta sai com
aviso (código 3). Cada id é re-checado logo antes da chamada paga.
A chave vem de ~/.segredos/fal.env (FAL_KEY).
"""
import argparse
import base64
import io
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import yaml
from PIL import Image, ImageStat

from _paths import FABRICA
from _trava import travar_pasta
from db import tentar

# Estimativa de US$ por imagem (~1–1,3 MP, 16:9), usada só se o saldo do fal não puder ser lido.
PRECO_POR_IMAGEM = {
    "fal-ai/flux/schnell": 0.003,
    "fal-ai/flux/dev": 0.033,          # 1536x864 ≈ 1,33 MP × US$ 0,025/MP
    "fal-ai/flux-pro/v1.1": 0.04,
    "fal-ai/recraft/v3/text-to-image": 0.04,
    "fal-ai/imagen4/preview/fast": 0.02,
    "fal-ai/nano-banana": 0.039,
    "fal-ai/nano-banana/edit": 0.039,
    "google/nano-banana-2.1/edit": 0.044,   # bancada do 003 (04/11/2026), 1K
    "openai/gpt-image-2": 0.04,             # medium 1536x864
    "openai/gpt-image-2/edit": 0.02,        # low
}


def chave():
    for linha in open(os.path.expanduser("~/.segredos/fal.env")):
        if linha.startswith("FAL_KEY="):
            return linha.split("=", 1)[1].strip()
    sys.exit("FAL_KEY não encontrada em ~/.segredos/fal.env")


def saldo(key):
    try:
        req = urllib.request.Request("https://api.fal.ai/v1/account/billing?expand=credits", headers={"Authorization": f"Key {key}"})
        return float(json.load(urllib.request.urlopen(req, timeout=30))["credits"]["current_balance"])
    except Exception:  # noqa: BLE001
        return None


def uso_endpoint(key, modelo, desde="2026-11-01T00:00:00Z"):
    """Gasto acumulado (US$) do endpoint desde `desde` (api.fal.ai/v1/models/usage, buckets por hora). Isola o custo deste
    modelo mesmo com outro job usando OUTRO endpoint do fal ao mesmo tempo (05/11/2026)."""
    try:
        u = (f"https://api.fal.ai/v1/models/usage?endpoint_id={modelo}&start={desde}&expand=time_series")
        d = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": f"Key {key}"}), timeout=60))
        return sum(float(r.get("cost_total", r.get("cost", 0)) or 0) for b in d.get("time_series", []) for r in b.get("results", []))
    except Exception:  # noqa: BLE001
        return None


def data_uri(caminho):
    im = Image.open(caminho).convert("RGB")
    im.thumbnail((1024, 1024))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def corpo_para(modelo, prompt, tamanho, params, refs, seed=None):
    corpo = {"prompt": prompt, "num_images": 1}
    if modelo.startswith(("fal-ai/flux", "fal-ai/recraft", "fal-ai/imagen")):
        corpo["image_size"] = tamanho
        corpo["enable_safety_checker"] = True
    if tamanho == "landscape_16_9":  # nano-banana ignora image_size e sai 1:1; ele lê aspect_ratio (teste dossie-ptbr, 2026-11-04)
        corpo["aspect_ratio"] = "16:9"
    corpo.update(params or {})
    if refs:
        corpo["image_urls"] = refs
    if seed is not None:
        corpo["seed"] = seed
    return corpo


def gerar(key, modelo, corpo, destino, tam_final):
    req = urllib.request.Request(f"https://fal.run/{modelo}", data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=400) as r:
        resp = json.load(r)
    if any(resp.get("has_nsfw_concepts") or []):
        raise RuntimeError("filtro de segurança (has_nsfw_concepts)")
    url = resp["images"][0]["url"]
    with urllib.request.urlopen(url, timeout=120) as r:
        im = Image.open(io.BytesIO(r.read())).convert("RGB")
    st = ImageStat.Stat(im.convert("L"))
    if st.mean[0] < 15 or st.stddev[0] < 6:
        raise RuntimeError(f"imagem preta/vazia (média {st.mean[0]:.0f}, desvio {st.stddev[0]:.0f})")
    orig = im.size
    if tam_final and im.size != tam_final:
        im = im.resize(tam_final, Image.LANCZOS)
    tmp = destino + ".tmp.jpg"
    im.save(tmp, "JPEG", quality=92)
    os.replace(tmp, destino)
    return orig


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canal")
    ap.add_argument("cenas")
    ap.add_argument("saida")
    ap.add_argument("--video", type=int, help="id em youtube.videos, para atribuir o custo ao vídeo")
    ap.add_argument("--modelo")
    ap.add_argument("--paralelo", type=int, default=4)
    ap.add_argument("--so", help="só estes ids (vírgula)")
    ap.add_argument("--teto", type=float, help="para de disparar se o gasto real (saldo) passar disto, em US$")
    ap.add_argument("--notas", default="", help="texto extra nas notas de financas.consumo")
    a = ap.parse_args()
    pasta_canal = os.path.join(FABRICA, "canais", a.canal)
    visual = (yaml.safe_load(open(os.path.join(pasta_canal, "canal.yaml"))) or {}).get("visual", {})
    modelo = a.modelo or visual.get("modelo", "fal-ai/flux/dev")
    estilo = visual.get("estilo_prompt", "")
    tamanho = visual.get("tamanho", "landscape_16_9")
    tam_final = (tamanho["width"], tamanho["height"]) if isinstance(tamanho, dict) else None
    params = visual.get("parametros") or {}
    edicao = modelo.endswith("/edit")
    refs = [data_uri(os.path.join(pasta_canal, r)) for r in visual.get("refs", [])] if edicao else []
    if edicao and not refs:
        sys.exit(f"{modelo} é de edição e o canal.yaml não tem visual.refs.")
    instr = visual.get("ref_instrucao", "") if edicao else ""
    if modelo not in PRECO_POR_IMAGEM:
        sys.exit(f"Modelo {modelo} sem preço em PRECO_POR_IMAGEM; cadastre antes de usar.")
    key = chave()
    os.makedirs(a.saida, exist_ok=True)
    trava = travar_pasta(a.saida)  # noqa: F841  (um processo por pasta; sai com aviso se já houver outro)
    cenas = json.load(open(a.cenas))
    if a.so:
        so = set(a.so.split(","))
        cenas = [c for c in cenas if c["id"] in so]
    pendentes = [c for c in cenas if not os.path.exists(os.path.join(a.saida, f"{c['id']}.jpg"))]
    s0, u0 = saldo(key), uso_endpoint(key, modelo)
    print(f"{modelo} · {len(pendentes)} pendentes · refs {len(refs)} · saldo fal antes: {s0} · uso do endpoint: {u0}")
    ok, falhas, puladas, parou = 0, [], 0, False

    def uma(c):
        nonlocal parou
        if os.path.exists(os.path.join(a.saida, f"{c['id']}.jpg")):  # re-checa logo antes da chamada paga
            return None
        if parou:
            raise RuntimeError("teto atingido; não disparado")
        prompt = f"{c['prompt']}. {estilo}".strip(". ") if estilo else c["prompt"]
        corpo = corpo_para(modelo, instr + prompt, tamanho, params, refs, c.get("seed"))
        ultimo = None
        for tentativa in range(2):  # 1 nova tentativa em erro de rede/imagem preta (cobra de novo, mas evita buraco)
            try:
                return gerar(key, modelo, corpo, os.path.join(a.saida, f"{c['id']}.jpg"), tam_final)
            except Exception as e:  # noqa: BLE001
                ultimo = e
                time.sleep(2)
        raise ultimo

    with ThreadPoolExecutor(max_workers=a.paralelo) as ex:
        for c, fut in [(c, ex.submit(uma, c)) for c in pendentes]:
            try:
                r = fut.result()
                if r is None:
                    puladas += 1
                    print(f"{c['id']}: já existe (pulada)")
                    continue
                ok += 1
                print(f"{c['id']}: ok ({r[0]}x{r[1]})", flush=True)
                if a.teto and s0 is not None and ok % 10 == 0:
                    s = saldo(key)
                    if s is not None and s0 - s > a.teto:
                        parou = True
                        print(f"TETO: gasto real US$ {s0 - s:.2f} > {a.teto}; parando")
            except Exception as e:  # noqa: BLE001
                falhas.append(c["id"])
                print(f"{c['id']}: ERRO {str(e)[:160]}", flush=True)
    u1 = None
    for _ in range(6):  # o uso por endpoint entra com alguns segundos de atraso
        time.sleep(10)
        u1 = uso_endpoint(key, modelo)
        if u0 is not None and u1 is not None and (u1 - u0 > 0 or not ok):
            break
    s1 = saldo(key)
    if u0 is not None and u1 is not None and u1 - u0 > 0:
        real, custo, fonte = True, round(u1 - u0, 4), f"real pelo uso do endpoint no fal ({u0:.3f} → {u1:.3f}); saldo {s0} → {s1}"
    elif s0 is not None and s1 is not None and s0 - s1 > 0:
        real, custo, fonte = True, round(s0 - s1, 4), f"real pelo saldo do fal ({s0:.2f} → {s1:.2f}; inclui outros jobs no período)"
    else:
        real, custo, fonte = False, ok * PRECO_POR_IMAGEM[modelo], "estimado (preço fixo)"

    def registrar(con):
        cambio = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='fal.ai'").fetchone()
        con.execute(
            "INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
            " VALUES ('youtube', %s, 'fal.ai', %s, %s, 'imagens', %s, 'USD', %s, %s, %s, %s)",
            (a.canal, f"imagem {modelo}", ok, custo, custo * float(cambio[0]) if cambio else None,
             "youtube.video" if a.video else None, a.video,
             f"{a.notas} {os.path.basename(a.cenas)}; custo {fonte}; {len(falhas)} falhas".strip()))
    if ok or (real and custo > 0):
        tentar(registrar)
    print(f"\n{ok} geradas, {len(cenas) - len(pendentes) + puladas} já existiam, {len(falhas)} falhas · US$ {custo:.3f} ({fonte})")
    if ok:
        print(f"US$ {custo / ok:.4f} por imagem")
    if falhas:
        print("Falharam (rode de novo para tentar só estas):", ", ".join(falhas))


if __name__ == "__main__":
    main()
