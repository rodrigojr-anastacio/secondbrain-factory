"""Bancada de modelos de imagem do fal.ai para o historia-ptbr (003-ira, youtube.videos id 5).

Uso (a partir de ~/workspace/fabrica-youtube/tools):
  .venv/bin/python ../canais/historia-ptbr/videos/003-ira/v2-amostras/imagens/bench.py [--so slug1,slug2] [--reserva 0.85] [--teto 4.0]

Gera 2 cenas (I002 caravana com pessoa / I007 Persépolis) por modelo, em ordem de prioridade, em amostras/<slug>-<cena>.jpg.
Antes de cada modelo confere o saldo AO VIVO do fal (api.fal.ai/v1/account/billing) e pula se o saldo depois do modelo
ficaria abaixo da --reserva (dinheiro de outro agente) ou se o total da bancada passaria do --teto.
Registra o custo previsto de cada modelo em financas.consumo (ref youtube.video 5) e grava prompts.json e resultados.json.
Rodar de novo pula as imagens que já existem (não paga duas vezes).
"""
import argparse
import base64
import io
import json
import os
import subprocess
import sys
import time
import urllib.request

sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
import yaml  # noqa: E402
from PIL import Image, ImageStat  # noqa: E402

from db import tentar  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
VIDEOS = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
CANAL = os.path.abspath(os.path.join(VIDEOS, ".."))
AMOSTRAS = os.path.join(AQUI, "amostras")
VIDEO_ID = 5
W, H = 1536, 864
CENAS = ["I002", "I007"]
REFS = [os.path.join(VIDEOS, "001-egito/imagens/I041.jpg"), os.path.join(VIDEOS, "002-india/imagens/I041.jpg")]
REF_INSTR = ("Use the attached reference images ONLY as a style guide: draw in exactly the same art style as the reference "
             "images (simple cartoon people with round white heads, dot eyes, simple expressive faces, thick black outlines, "
             "flat bright colors, soft cel shading). Do not copy their content or composition. New scene: ")
SZ = {"width": W, "height": H}

# (slug, endpoint, tipo, preco previsto US$/img a ~1536x864, usa refs, corpo extra)
MODELOS = [
    ("gpt-image-2-low", "openai/gpt-image-2", "t2i", 0.006, False, {"image_size": SZ, "quality": "low", "output_format": "jpeg"}),
    ("gpt-image-2-medium", "openai/gpt-image-2", "t2i", 0.040, False, {"image_size": SZ, "quality": "medium", "output_format": "jpeg"}),
    ("gpt-image-2-edit-low", "openai/gpt-image-2/edit", "edit", 0.020, True, {"image_size": SZ, "quality": "low", "output_format": "jpeg"}),
    ("nano-banana-edit", "fal-ai/nano-banana/edit", "edit", 0.0398, True, {"aspect_ratio": "16:9", "output_format": "jpeg"}),
    ("nano-banana-2.1-edit", "google/nano-banana-2.1/edit", "edit", 0.044, True, {"aspect_ratio": "16:9", "resolution": "1K", "output_format": "jpeg"}),
    ("seedream-4.5-edit", "fal-ai/bytedance/seedream/v4.5/edit", "edit", 0.04, True, {"image_size": SZ}),
    ("kontext-pro-multi", "fal-ai/flux-pro/kontext/multi", "edit", 0.04, True, {"aspect_ratio": "16:9", "output_format": "jpeg"}),
    ("recraft-v4-style", "recraft/v4/style/text-to-image", "t2i+style", 0.0375, True, {"image_size": SZ}),
    ("ideogram-v3-turbo-styleref", "fal-ai/ideogram/v3", "t2i+style", 0.03, True, {"image_size": SZ, "rendering_speed": "TURBO", "enable_prompt_expansion": False}),
    ("z-image-turbo", "fal-ai/z-image/turbo", "t2i", 0.007, False, {"image_size": SZ}),
    ("gpt-image-1-mini-medium", "fal-ai/gpt-image-1-mini", "t2i", 0.015, False, {"image_size": "1536x1024", "quality": "medium", "output_format": "jpeg"}),
    ("seedream-4-t2i", "fal-ai/bytedance/seedream/v4/text-to-image", "t2i", 0.03, False, {"image_size": SZ}),
    ("flux-2-klein-9b-edit", "fal-ai/flux-2/klein/9b/edit", "edit", 0.04, True, {"image_size": SZ}),
    ("qwen-image-edit-2511", "fal-ai/qwen-image-edit-2511", "edit", 0.06, True, {"image_size": SZ}),
]


def chave():
    for linha in open(os.path.expanduser("~/.segredos/fal.env")):
        if linha.startswith("FAL_KEY="):
            return linha.split("=", 1)[1].strip()
    sys.exit("FAL_KEY não encontrada")


def saldo(key):
    req = urllib.request.Request("https://api.fal.ai/v1/account/billing?expand=credits", headers={"Authorization": f"Key {key}"})
    return float(json.load(urllib.request.urlopen(req, timeout=30))["credits"]["current_balance"])


def data_uri(p):
    im = Image.open(p).convert("RGB")
    im.thumbnail((1024, 1024))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def chamar(key, endpoint, corpo):
    req = urllib.request.Request(f"https://fal.run/{endpoint}", data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=400) as r:
        return json.load(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so")
    ap.add_argument("--reserva", type=float, default=0.85)
    ap.add_argument("--teto", type=float, default=4.0)
    a = ap.parse_args()
    key = chave()
    try:
        estilo = yaml.safe_load(open(os.path.join(CANAL, "canal.yaml")))["visual"]["estilo_prompt"]
    except yaml.YAMLError:  # canal.yaml em edição por outro job: usa a versão commitada
        txt = subprocess.run(["git", "show", "HEAD:canais/historia-ptbr/canal.yaml"], cwd=CANAL, capture_output=True, text=True).stdout
        estilo = yaml.safe_load(txt)["visual"]["estilo_prompt"]
    cenas = {c["id"]: c["prompt"] for c in json.load(open(os.path.join(VIDEOS, "003-ira/cenas.json")))}
    refs = [data_uri(p) for p in REFS]
    os.makedirs(AMOSTRAS, exist_ok=True)
    pj, rj = os.path.join(AQUI, "prompts.json"), os.path.join(AQUI, "resultados.json")
    prompts = json.load(open(pj)) if os.path.exists(pj) else {}
    res = json.load(open(rj)) if os.path.exists(rj) else {}
    gasto_total = sum(v.get("custo_usd", 0) for v in res.values())
    so = set(a.so.split(",")) if a.so else None
    for slug, endpoint, tipo, preco, usa_refs, extra in MODELOS:
        if so and slug not in so:
            continue
        faltam = [c for c in CENAS if not os.path.exists(os.path.join(AMOSTRAS, f"{slug}-{c}.jpg"))]
        if not faltam:
            print(f"{slug}: já feito")
            continue
        prev = preco * len(faltam)
        s = saldo(key)
        if s - prev < a.reserva or gasto_total + prev > a.teto:
            print(f"{slug}: PULADO (saldo fal US$ {s:.2f}, previsto {prev:.3f}, reserva {a.reserva}, gasto {gasto_total:.3f})")
            res.setdefault(slug, {}).update({"endpoint": endpoint, "status": f"não testado: saldo US$ {s:.2f} / reserva"})
            json.dump(res, open(rj, "w"), indent=1, ensure_ascii=False)
            continue
        ok = 0
        info = res.setdefault(slug, {"endpoint": endpoint, "tipo": tipo, "preco_img": preco, "cenas": {}})
        info.update({"endpoint": endpoint, "tipo": tipo, "preco_img": preco})
        info.setdefault("cenas", {})
        for c in faltam:
            prompt = f"{cenas[c]}. {estilo}"
            if usa_refs and tipo == "edit":
                prompt = REF_INSTR + prompt
            corpo = {"prompt": prompt, "num_images": 1, **extra}
            if usa_refs:
                corpo["image_urls"] = refs
            if "enable_safety_checker" not in corpo and not endpoint.startswith(("fal-ai/nano", "google/", "fal-ai/flux-pro/kontext")):
                corpo["enable_safety_checker"] = True
            prompts.setdefault(slug, {"endpoint": endpoint, "parametros": {k: v for k, v in corpo.items() if k not in ("prompt", "image_urls")},
                                      "refs": [os.path.relpath(p, VIDEOS) for p in REFS] if usa_refs else [], "prompts": {}})
            prompts[slug]["prompts"][c] = prompt
            t0 = time.time()
            try:
                r = chamar(key, endpoint, corpo)
            except Exception as e:  # noqa: BLE001
                det = e.read().decode()[:300] if hasattr(e, "read") else ""
                print(f"{slug} {c}: ERRO {e} {det}")
                info["cenas"][c] = {"erro": f"{e} {det}"[:400]}
                continue
            dt = time.time() - t0
            img = r["images"][0]
            nsfw = (r.get("has_nsfw_concepts") or [False])[0]
            raw = urllib.request.urlopen(img["url"], timeout=120).read()
            im = Image.open(io.BytesIO(raw)).convert("RGB")
            media = sum(ImageStat.Stat(im).mean) / 3
            destino = os.path.join(AMOSTRAS, f"{slug}-{c}.jpg")
            im.save(destino, "JPEG", quality=90)
            ok += 1  # cobrado mesmo se sair preto/nsfw
            falha = bool(nsfw) or media < 8
            info["cenas"][c] = {"resolucao": f"{im.width}x{im.height}", "segundos": round(dt, 1), "nsfw": bool(nsfw),
                                "media_brilho": round(media, 1), "falha": falha}
            print(f"{slug} {c}: ok {im.width}x{im.height} {dt:.0f}s{' FALHA(nsfw/preta)' if falha else ''}")
        custo = round(ok * preco, 4)
        info["custo_usd"] = round(info.get("custo_usd", 0) + custo, 4)
        info["status"] = "testado"
        gasto_total += custo
        if ok:
            def registrar(con, n=ok, usd=custo, ep=endpoint):
                cam = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='fal.ai'").fetchone()
                con.execute(
                    "INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
                    " VALUES ('youtube','historia-ptbr','fal.ai',%s,%s,'imagens',%s,'USD',%s,'youtube.video',%s,'v2 bancada de modelos')",
                    (f"imagem {ep}", n, usd, usd * float(cam[0]) if cam else None, VIDEO_ID))
                return True
            info["db"] = bool(tentar(registrar))
        json.dump(prompts, open(pj, "w"), indent=1, ensure_ascii=False)
        json.dump(res, open(rj, "w"), indent=1, ensure_ascii=False)
    print(f"\nTotal previsto da bancada: US$ {gasto_total:.3f} · saldo fal agora US$ {saldo(key):.2f}")


if __name__ == "__main__":
    main()
