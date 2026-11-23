"""Protótipo (TESTE, 23/11/2026): cenas do Dossier direto na Gemini API (AI Studio), modo padrão ou Batch.

Uso (a partir de qualquer pasta; Python do tools/.venv):
  set -a; . ~/.segredos/gemini.env; set +a
  python gemini_img.py padrao <modelo> <cenas.json> <saida> [--size 1K] [--refs a.jpg,b.jpg] [--paralelo 2] [--thinking minimal]
  python gemini_img.py batch  <modelo> <cenas.json> <saida> [--size 1K] [--refs ...] [--espera-min 40]
- Prompt = prompt da cena + ". " + visual.estilo_prompt do canais/dossie-es/canal.yaml (mesmo contrato do tools/img_fal.py).
- Refs (opcional, até 3): imagens inline como referência de ESTILO, com instrução antes do prompt.
- imageConfig.aspectRatio 16:9 (+ imageSize quando o modelo aceita); saída reescalada para 1536x864 JPEG.
- Falha = sem imagem (bloqueio: promptFeedback.blockReason / finishReason), ou imagem preta/vazia.
- Custo por imagem calculado do usageMetadata × preço oficial (aistudio.google.com/docs/pricing, 23/11/2026).
- A chave vem só do ambiente (GEMINI_API_KEY), vai no header x-goog-api-key e nunca é impressa nem gravada.
Log por imagem: <saida>/gemini_log.jsonl.
"""
import argparse
import base64
import io
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import requests
import yaml
from PIL import Image, ImageStat

BASE = "https://generativelanguage.googleapis.com/v1beta"
AQUI = os.path.dirname(os.path.abspath(__file__))
CANAL = os.path.abspath(os.path.join(AQUI, "..", ".."))
TAM_FINAL = (1536, 864)

# US$ por 1M tokens: entrada (texto/imagem), saída texto+thinking, saída imagem. Batch = metade.
PRECOS = {
    "gemini-2.5-flash-image": (0.30, 2.50, 30.0),
    "gemini-3.1-flash-image": (0.50, 3.00, 60.0),
    "gemini-nano-banana-2.1": (1.50, 7.50, 30.0),
    "gemini-3.1-flash-lite-image": (0.25, 1.50, 30.0),
}
SEM_IMAGESIZE = {"gemini-2.5-flash-image"}
REF_INSTR = ("Use the attached reference images ONLY as a style reference (ink line weight, muted desaturated palette, "
             "lighting, level of detail); do not copy their content, people or composition. Draw this scene: ")


def chave():
    k = os.environ.get("GEMINI_API_KEY")
    if not k:
        sys.exit("GEMINI_API_KEY ausente (carregue ~/.segredos/gemini.env)")
    return k


def hdr():
    return {"x-goog-api-key": chave(), "Content-Type": "application/json"}


def estilo():
    return (yaml.safe_load(open(os.path.join(CANAL, "canal.yaml"))).get("visual") or {}).get("estilo_prompt", "")


def inline(caminho):
    im = Image.open(caminho).convert("RGB")
    im.thumbnail((1024, 1024))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=88)
    return {"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(b.getvalue()).decode()}}


def requisicao(modelo, cena, est, refs, size, thinking):
    texto = f"{cena['prompt']}. {est}".strip(". ")
    partes = [{"text": (REF_INSTR if refs else "") + texto}] + [inline(r) for r in refs]
    img_cfg = {"aspectRatio": "16:9"}
    if modelo not in SEM_IMAGESIZE and size:
        img_cfg["imageSize"] = size
    gen = {"responseModalities": ["IMAGE"], "imageConfig": img_cfg}
    if thinking:
        gen["thinkingConfig"] = {"thinkingLevel": thinking}
    return {"contents": [{"role": "user", "parts": partes}], "generationConfig": gen}


def custo(modelo, uso, batch=False):
    pin, ptxt, pimg = PRECOS[modelo]
    entrada = uso.get("promptTokenCount", 0)
    img_out = sum(d.get("tokenCount", 0) for d in uso.get("candidatesTokensDetails", []) if d.get("modality") == "IMAGE")
    txt_out = uso.get("candidatesTokenCount", 0) - img_out + uso.get("thoughtsTokenCount", 0)
    if not uso.get("candidatesTokensDetails"):
        img_out, txt_out = uso.get("candidatesTokenCount", 0), uso.get("thoughtsTokenCount", 0)
    c = (entrada * pin + txt_out * ptxt + img_out * pimg) / 1e6
    return round(c / 2 if batch else c, 5)


def salvar(resp, destino):
    """Extrai a imagem da resposta; levanta RuntimeError com o motivo se não houver."""
    pf = resp.get("promptFeedback") or {}
    if pf.get("blockReason"):
        raise RuntimeError(f"bloqueio do prompt: {pf['blockReason']}")
    cands = resp.get("candidates") or []
    if not cands:
        raise RuntimeError("sem candidates")
    partes = (cands[0].get("content") or {}).get("parts") or []
    dados = next((p["inlineData"]["data"] for p in partes if "inlineData" in p), None)
    if not dados:
        txt = " ".join(p.get("text", "") for p in partes)[:120]
        raise RuntimeError(f"sem imagem (finishReason {cands[0].get('finishReason')}; {txt})")
    im = Image.open(io.BytesIO(base64.b64decode(dados))).convert("RGB")
    st = ImageStat.Stat(im.convert("L"))
    if st.mean[0] < 15 or st.stddev[0] < 6:
        raise RuntimeError(f"imagem preta/vazia (média {st.mean[0]:.0f})")
    orig = im.size
    im.resize(TAM_FINAL, Image.LANCZOS).save(destino, "JPEG", quality=92)
    return orig


def padrao(a, cenas, est, refs):
    n429 = [0]

    def uma(c):
        destino = os.path.join(a.saida, f"{c['id']}.jpg")
        if os.path.exists(destino):
            return None
        corpo = requisicao(a.modelo, c, est, refs, a.size, a.thinking)
        t0 = time.time()
        reg = {"id": c["id"], "modelo": a.modelo, "modo": "padrao", "refs": len(refs)}
        for tent in range(4):
            r = requests.post(f"{BASE}/models/{a.modelo}:generateContent", headers=hdr(), json=corpo, timeout=300)
            if r.status_code == 429 or r.status_code >= 500:
                n429[0] += r.status_code == 429
                reg.setdefault("http_retry", []).append(r.status_code)
                time.sleep(15 * (tent + 1))
                continue
            break
        reg["segundos"] = round(time.time() - t0, 1)
        if r.status_code != 200:
            reg["erro"] = f"HTTP {r.status_code}: {r.text[:200]}"
        else:
            resp = r.json()
            uso = resp.get("usageMetadata") or {}
            reg["uso"] = uso
            reg["custo_usd"] = custo(a.modelo, uso)
            try:
                reg["tamanho_orig"] = salvar(resp, destino)
            except RuntimeError as e:
                reg["erro"] = str(e)
        with open(os.path.join(a.saida, "gemini_log.jsonl"), "a") as f:
            f.write(json.dumps(reg, ensure_ascii=False) + "\n")
        return reg

    with ThreadPoolExecutor(max_workers=a.paralelo) as ex:
        regs = [r for r in ex.map(uma, cenas) if r]
    for r in regs:
        print(r["id"], f"{r['segundos']}s", f"US$ {r.get('custo_usd')}", r.get("tamanho_orig"), r.get("erro", "ok"), flush=True)
    tot = sum(r.get("custo_usd") or 0 for r in regs)
    print(f"{a.modelo}: {sum('erro' not in r for r in regs)}/{len(regs)} ok · US$ {tot:.4f} · 429: {n429[0]}")


def batch(a, cenas, est, refs):
    reqs = [{"request": requisicao(a.modelo, c, est, refs, a.size, a.thinking), "metadata": {"key": c["id"]}} for c in cenas]
    corpo = {"batch": {"display_name": f"dossie-teste-{int(time.time())}", "input_config": {"requests": {"requests": reqs}}}}
    t0 = time.time()
    if a.nome:  # retoma um lote já criado (t0 = createTime do lote)
        nome = a.nome
        g = requests.get(f"{BASE}/{nome}", headers=hdr(), timeout=60).json()
        ct = (g.get("metadata") or {}).get("createTime", "")
        if ct:
            from datetime import datetime
            t0 = datetime.fromisoformat(ct[:19] + "+00:00").timestamp()
    else:
        r = requests.post(f"{BASE}/models/{a.modelo}:batchGenerateContent", headers=hdr(), json=corpo, timeout=300)
        if r.status_code != 200:
            sys.exit(f"batch: HTTP {r.status_code}: {r.text[:300]}")
        nome = r.json()["name"]
    print("batch:", nome, flush=True)
    estado, op = None, {}
    primeiro = True
    while time.time() - t0 < a.espera_min * 60:
        if not primeiro:
            time.sleep(60)
        primeiro = False
        g = requests.get(f"{BASE}/{nome}", headers=hdr(), timeout=60)
        if g.status_code != 200:
            print("poll HTTP", g.status_code, flush=True)
            continue
        op = g.json()
        estado = op.get("metadata", {}).get("state") or op.get("state")
        print(f"{(time.time() - t0) / 60:.1f} min: {estado}", flush=True)
        if estado in ("JOB_STATE_SUCCEEDED", "BATCH_STATE_SUCCEEDED", "JOB_STATE_FAILED", "BATCH_STATE_FAILED",
                      "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED") or op.get("done"):
            break
    minutos = round((time.time() - t0) / 60, 1)
    resumo = {"modo": "batch", "modelo": a.modelo, "batch": nome, "estado": estado, "minutos": minutos, "refs": len(refs)}
    resp = op.get("response") or {}
    inl = (resp.get("inlinedResponses") or {})
    inl = inl.get("inlinedResponses", inl) if isinstance(inl, dict) else inl
    if not inl:
        inl = ((op.get("metadata") or {}).get("output") or {}).get("inlinedResponses", {})
        inl = inl.get("inlinedResponses", inl) if isinstance(inl, dict) else inl
    tot, ok = 0.0, 0
    for i, item in enumerate(inl or []):
        cid = (item.get("metadata") or {}).get("key") or cenas[i]["id"]
        reg = {"id": cid, "modelo": a.modelo, "modo": "batch", "refs": len(refs)}
        if "error" in item:
            reg["erro"] = str(item["error"])[:200]
        else:
            rr = item.get("response") or {}
            reg["uso"] = rr.get("usageMetadata") or {}
            reg["custo_usd"] = custo(a.modelo, reg["uso"], batch=True)
            tot += reg["custo_usd"]
            try:
                reg["tamanho_orig"] = salvar(rr, os.path.join(a.saida, f"{cid}.jpg"))
                ok += 1
            except RuntimeError as e:
                reg["erro"] = str(e)
        with open(os.path.join(a.saida, "gemini_log.jsonl"), "a") as f:
            f.write(json.dumps(reg, ensure_ascii=False) + "\n")
        print(cid, reg.get("custo_usd"), reg.get("erro", "ok"))
    resumo.update({"ok": ok, "custo_usd": round(tot, 4)})
    if not inl and estado and "SUCCEEDED" in estado:
        resumo["chaves_resposta"] = list(op.keys()) + list(resp.keys())
    with open(os.path.join(a.saida, "batch_resumo.json"), "w") as f:
        json.dump(resumo, f, ensure_ascii=False, indent=1)
    print(json.dumps(resumo, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("modo", choices=["padrao", "batch"])
    ap.add_argument("modelo", choices=sorted(PRECOS))
    ap.add_argument("cenas")
    ap.add_argument("saida")
    ap.add_argument("--size", default="1K")
    ap.add_argument("--refs", default="")
    ap.add_argument("--paralelo", type=int, default=2)
    ap.add_argument("--thinking", default=None)
    ap.add_argument("--espera-min", type=float, default=40)
    ap.add_argument("--nome", default=None, help="batches/<id> já criado: só acompanha e coleta")
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    refs = [r for r in a.refs.split(",") if r][:3]
    cenas = json.load(open(a.cenas))
    (padrao if a.modo == "padrao" else batch)(a, cenas, estilo(), refs)


if __name__ == "__main__":
    main()
