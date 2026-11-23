"""Gera imagens em lote na Gemini API (Google AI Studio), no estilo visual do canal, com o custo REAL registrado no banco.

Mesmo contrato do tools/img_fal.py (23/11/2026; fallback do img_codex.py desde que a fal ficou sem saldo):
  tools/.venv/bin/python tools/img_gemini.py <canal> <cenas.json> <pasta_saida> [--video <id>] [--modelo gemini-nano-banana-2.1]
        [--paralelo 4] [--so I001,I002] [--teto 10.0] [--notas "v2"] [--sem-refs] [--visual teste.yaml]
  <cenas.json>: lista de {"id": "I001", "prompt": "..."} (ou {"cenas": [...]}); o estilo do canal entra sozinho.

- Lê canais/<canal>/canal.yaml (bloco visual): `modelo_gemini` (padrão gemini-nano-banana-2.1, o único que passou 6/6
  no teste de 23/11/2026, canais/dossie-es/testes/gemini-2026-11-23/TESTE.md), `estilo_prompt`, `tamanho` (padrão
  1536x864), `refs` + `ref_instrucao` (refs de ESTILO, inline, até 3; instrução antes do prompt), `parametros_gemini`
  (ex.: {imageSize: 1K, thinkingLevel: minimal}). Modo padrão (generateContent), nunca Batch (bloqueou 4/6 no teste).
- 16:9 (imageConfig.aspectRatio), saída reescalada/cortada para visual.tamanho em JPEG.
- Falha = HTTP de erro, bloqueio (promptFeedback.blockReason, finishReason IMAGE_SAFETY/SAFETY/PROHIBITED…), resposta sem
  imagem, ou imagem preta/vazia. Em bloqueio: 1 nova tentativa com "resembling <Nome>" removido do prompt (nome de pessoa
  real é o gatilho típico); se bloquear de novo, a imagem fica faltando (o storyboard cobre com reuso ou o Codex refaz).
  429/5xx: até 3 novas tentativas com espera.
- Custo REAL por imagem = usageMetadata × preço oficial (aistudio.google.com/docs/pricing, lido em 23/11/2026), somado e
  gravado em financas.consumo (fornecedor 'Google Gemini API', ref_id = youtube.videos.id com --video). Bloqueio também
  entra (custa só o prompt). --teto: para de disparar quando o gasto da execução passar disso (US$).
- Trava a pasta (<saida>/.img.lock, a mesma do img_fal/img_codex: 2º processo sai com código 3); pula ids prontos e re-checa
  cada id logo antes da chamada paga.
- Chave: ~/.segredos/gemini.env (GEMINI_API_KEY), enviada só no header x-goog-api-key; nunca é impressa nem gravada.
Log por imagem: <saida>/gemini_log.jsonl. Códigos de saída: 0 tudo gerado; 1 faltou alguma; 3 pasta travada.
"""
import argparse
import base64
import io
import json
import os
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests
import yaml
from PIL import Image, ImageStat

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import FABRICA  # noqa: E402
from _trava import travar_pasta  # noqa: E402
from db import tentar  # noqa: E402

BASE = "https://generativelanguage.googleapis.com/v1beta"
FORNECEDOR = "Google Gemini API"
MODELO_PADRAO = "gemini-nano-banana-2.1"
# US$ por 1M tokens: entrada (texto/imagem), saída texto+thinking, saída imagem (preço oficial, 23/11/2026)
PRECOS = {
    "gemini-nano-banana-2.1": (1.50, 7.50, 30.0),
    "gemini-2.5-flash-image": (0.30, 2.50, 30.0),
    "gemini-3.1-flash-image": (0.50, 3.00, 60.0),
    "gemini-3.1-flash-lite-image": (0.25, 1.50, 30.0),
}
SEM_IMAGESIZE = {"gemini-2.5-flash-image"}
RE_RESEMBLING = re.compile(r",?\s*resembling\s+(?:[A-Z][\w'.\-]*\s*){1,4}", re.U)
BLOQUEIOS = {"IMAGE_SAFETY", "SAFETY", "PROHIBITED_CONTENT", "BLOCKLIST", "SPII", "IMAGE_PROHIBITED_CONTENT",
             "IMAGE_RECITATION", "RECITATION", "OTHER", "IMAGE_OTHER", "NO_IMAGE"}


class Bloqueio(RuntimeError):
    pass


def chave():
    f = os.path.expanduser("~/.segredos/gemini.env")
    k = os.environ.get("GEMINI_API_KEY")
    if not k and os.path.exists(f):
        for linha in open(f):
            linha = linha.strip()
            if linha.startswith(("GEMINI_API_KEY=", "export GEMINI_API_KEY=")):
                k = linha.split("=", 1)[1].strip().strip('"').strip("'")
    if not k:
        sys.exit("GEMINI_API_KEY não encontrada em ~/.segredos/gemini.env")
    return k


def inline(caminho):
    im = Image.open(caminho).convert("RGB")
    im.thumbnail((1024, 1024))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=88)
    return {"inlineData": {"mimeType": "image/jpeg", "data": base64.b64encode(b.getvalue()).decode()}}


def corpo(modelo, texto, refs_inline, params):
    img_cfg = {"aspectRatio": "16:9"}
    size = params.get("imageSize", "1K")
    if modelo not in SEM_IMAGESIZE and size:
        img_cfg["imageSize"] = size
    gen = {"responseModalities": ["IMAGE"], "imageConfig": img_cfg}
    if params.get("thinkingLevel"):
        gen["thinkingConfig"] = {"thinkingLevel": params["thinkingLevel"]}
    return {"contents": [{"role": "user", "parts": [{"text": texto}] + refs_inline}], "generationConfig": gen}


def custo(modelo, uso):
    pin, ptxt, pimg = PRECOS[modelo]
    entrada = uso.get("promptTokenCount", 0)
    det = uso.get("candidatesTokensDetails") or []
    img_out = sum(d.get("tokenCount", 0) for d in det if d.get("modality") == "IMAGE")
    txt_out = uso.get("candidatesTokenCount", 0) - img_out + uso.get("thoughtsTokenCount", 0)
    if not det:
        img_out, txt_out = uso.get("candidatesTokenCount", 0), uso.get("thoughtsTokenCount", 0)
    return round((entrada * pin + txt_out * ptxt + img_out * pimg) / 1e6, 5)


def extrair(resp):
    """Imagem PIL da resposta; Bloqueio se o filtro barrou; RuntimeError se veio sem imagem por outro motivo."""
    pf = resp.get("promptFeedback") or {}
    if pf.get("blockReason"):
        raise Bloqueio(f"bloqueio do prompt: {pf['blockReason']}")
    cands = resp.get("candidates") or []
    if not cands:
        raise Bloqueio("sem candidates")
    partes = (cands[0].get("content") or {}).get("parts") or []
    dados = next((p["inlineData"]["data"] for p in partes if "inlineData" in p), None)
    fr = cands[0].get("finishReason")
    if not dados:
        txt = " ".join(p.get("text", "") for p in partes)[:120]
        msg = f"sem imagem (finishReason {fr}; {txt})"
        raise (Bloqueio if (fr in BLOQUEIOS or not fr) else RuntimeError)(msg)
    im = Image.open(io.BytesIO(base64.b64decode(dados))).convert("RGB")
    st = ImageStat.Stat(im.convert("L"))
    if st.mean[0] < 15 or st.stddev[0] < 6:
        raise RuntimeError(f"imagem preta/vazia (média {st.mean[0]:.0f}, desvio {st.stddev[0]:.0f})")
    return im


def salvar(im, destino, tam):
    w, h = im.size
    alvo = tam[0] / tam[1]
    if w / h > alvo + 0.01:
        nw = round(h * alvo)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    elif w / h < alvo - 0.01:
        nh = round(w / alvo)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    tmp = destino + ".tmp.jpg"
    im.resize(tam, Image.LANCZOS).save(tmp, "JPEG", quality=92)
    os.replace(tmp, destino)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canal")
    ap.add_argument("cenas")
    ap.add_argument("saida")
    ap.add_argument("--video", type=int, help="id em youtube.videos, para atribuir o custo ao vídeo")
    ap.add_argument("--modelo", help=f"padrão: visual.modelo_gemini ou {MODELO_PADRAO}")
    ap.add_argument("--paralelo", type=int, default=4)
    ap.add_argument("--so", help="só estes ids (vírgula)")
    ap.add_argument("--teto", type=float, help="para de disparar se o gasto desta execução passar disto (US$)")
    ap.add_argument("--notas", default="")
    ap.add_argument("--tamanho", help="WxH final (padrão visual.tamanho ou 1536x864)")
    ap.add_argument("--sem-refs", action="store_true")
    ap.add_argument("--visual", help="yaml que sobrepõe chaves de visual (testes)")
    a = ap.parse_args()

    pasta_canal = os.path.join(FABRICA, "canais", a.canal)
    visual = (yaml.safe_load(open(os.path.join(pasta_canal, "canal.yaml"))) or {}).get("visual", {})
    if a.visual:
        visual.update(yaml.safe_load(open(a.visual)) or {})
    modelo = a.modelo or visual.get("modelo_gemini") or MODELO_PADRAO
    if modelo not in PRECOS:
        sys.exit(f"Modelo {modelo} sem preço em PRECOS; cadastre antes de usar.")
    estilo = visual.get("estilo_prompt", "")
    if a.tamanho:
        tam = tuple(int(x) for x in a.tamanho.lower().split("x"))
    else:
        t = visual.get("tamanho")
        tam = (t["width"], t["height"]) if isinstance(t, dict) else (1536, 864)
    params = visual.get("parametros_gemini") or {}
    refs_arq = [] if a.sem_refs else [os.path.join(pasta_canal, r) for r in (visual.get("refs") or [])[:3]
                                       if os.path.exists(os.path.join(pasta_canal, r))]
    refs_inline = [inline(r) for r in refs_arq]
    instr = visual.get("ref_instrucao", "") if refs_inline else ""
    key = chave()
    hdr = {"x-goog-api-key": key, "Content-Type": "application/json"}

    os.makedirs(a.saida, exist_ok=True)
    trava = travar_pasta(a.saida)  # noqa: F841
    raw = json.load(open(a.cenas))
    cenas = raw["cenas"] if isinstance(raw, dict) else raw
    if a.so:
        so = set(a.so.split(","))
        cenas = [c for c in cenas if c["id"] in so]
    pendentes = [c for c in cenas if not os.path.exists(os.path.join(a.saida, f"{c['id']}.jpg"))]
    print(f"gemini {modelo} · {len(pendentes)} pendentes de {len(cenas)} · refs {len(refs_inline)} · paralelo {a.paralelo} · "
          f"{tam[0]}x{tam[1]}", flush=True)
    log = os.path.join(a.saida, "gemini_log.jsonl")
    tl = threading.Lock()
    tot = {"custo": 0.0, "chamadas": 0, "bloqueios": 0, "parou": False}

    def chamar(texto):
        r = None
        for tent in range(4):
            r = requests.post(f"{BASE}/models/{modelo}:generateContent", headers=hdr, json=corpo(modelo, texto, refs_inline, params),
                              timeout=300)
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(15 * (tent + 1))
                continue
            break
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
        resp = r.json()
        c = custo(modelo, resp.get("usageMetadata") or {})
        with tl:
            tot["custo"] += c
            tot["chamadas"] += 1
        return resp, c

    def uma(cena):
        cid = cena["id"]
        destino = os.path.join(a.saida, f"{cid}.jpg")
        if os.path.exists(destino):
            return {"id": cid, "ok": None}
        if tot["parou"]:
            return {"id": cid, "ok": False, "erro": "teto atingido; não disparado"}
        base = f"{cena['prompt']}. {estilo}".strip(". ") if estilo else cena["prompt"]
        reg = {"id": cid, "modelo": modelo, "refs": len(refs_inline), "custo_usd": 0.0, "tentativas": []}
        t0 = time.time()
        prompts = [base]
        sem_nome = RE_RESEMBLING.sub("", base)
        prompts.append(sem_nome)  # 1 nova tentativa só em bloqueio (sem "resembling <Nome>"; se não houver, o mesmo)
        for i, p in enumerate(prompts):
            try:
                resp, c = chamar(instr + p)
                reg["custo_usd"] += c
                salvar(extrair(resp), destino, tam)
                reg["tentativas"].append("ok" if i == 0 else "ok sem nome")
                reg["ok"] = True
                break
            except Bloqueio as e:
                with tl:
                    tot["bloqueios"] += 1
                reg["tentativas"].append(f"bloqueio: {e}"[:160])
                reg["ok"], reg["erro"] = False, str(e)[:200]
                continue
            except Exception as e:  # noqa: BLE001  (HTTP, rede, imagem preta: não insiste para não pagar em dobro)
                reg["tentativas"].append(f"erro: {e}"[:160])
                reg["ok"], reg["erro"] = False, str(e)[:200]
                break
        reg["seg"] = round(time.time() - t0, 1)
        reg["custo_usd"] = round(reg["custo_usd"], 5)
        with tl:
            if a.teto and tot["custo"] > a.teto:
                tot["parou"] = True
            with open(log, "a") as f:
                f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), **reg}, ensure_ascii=False) + "\n")
        return reg

    regs = []
    with ThreadPoolExecutor(max_workers=max(1, a.paralelo)) as ex:
        for r in ex.map(uma, pendentes):
            regs.append(r)
            if r["ok"] is None:
                print(f"{r['id']}: já existe (pulada)", flush=True)
            elif r["ok"]:
                print(f"{r['id']}: ok gemini {r['seg']}s US$ {r['custo_usd']:.4f}"
                      + (" (sem nome, após bloqueio)" if r["tentativas"][-1] == "ok sem nome" else ""), flush=True)
            else:
                print(f"{r['id']}: FALHOU ({(r.get('erro') or '')[:140]})", flush=True)
    ok = sum(1 for r in regs if r["ok"])
    falhas = [r["id"] for r in regs if r["ok"] is False]
    custo_tot = round(tot["custo"], 5)

    def registrar(con):
        cambio = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor=%s", (FORNECEDOR,)).fetchone()
        con.execute(
            "INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
            " VALUES ('youtube', %s, %s, %s, %s, 'imagens', %s, 'USD', %s, %s, %s, %s)",
            (a.canal, FORNECEDOR, f"imagem {modelo} {params.get('imageSize', '1K')}", ok, custo_tot,
             custo_tot * float(cambio[0]) if cambio else None, "youtube.video" if a.video else None, a.video,
             f"{a.notas} {os.path.basename(a.cenas)}; {tot['chamadas']} chamadas, {tot['bloqueios']} bloqueios, {len(falhas)} falhas; "
             f"custo real pelo usageMetadata × preço oficial".strip()))
    if tot["chamadas"]:
        tentar(registrar)
    print(f"\n{ok} geradas, {len(cenas) - len(pendentes)} já existiam, {len(falhas)} falhas, {tot['bloqueios']} bloqueios · "
          f"US$ {custo_tot:.4f} ({tot['chamadas']} chamadas)" + (" · PAROU no teto" if tot["parou"] else ""))
    if falhas:
        print("Falharam (rode de novo para tentar só estas):", ",".join(falhas))
    faltam = [c["id"] for c in cenas if not os.path.exists(os.path.join(a.saida, f"{c['id']}.jpg"))]
    sys.exit(1 if faltam else 0)


if __name__ == "__main__":
    main()
