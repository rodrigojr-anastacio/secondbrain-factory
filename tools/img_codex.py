"""Gera imagens em lote pelo Codex CLI (login ChatGPT Plus, ferramenta interna image_gen), SEM chave de API, com
fallback automático para o tools/img_fal.py.

Decisão do Rodrigo (14/11/2026): historia-ptbr gera cenas e thumb pelo Codex; o fal fica de reserva. Outros canais: fal.
Origem: protótipo pesquisa/teste-codex-imagens-2026-11-14/codex_img.py (30/30 imagens, US$ 0).

Uso (da raiz do repo; mesma interface útil do img_fal.py):
  tools/.venv/bin/python tools/img_codex.py <canal> <cenas.json> <pasta_saida> [--video <id>] [--paralelo 3]
        [--so I001,I002] [--teto 10.0] [--notas "v2"] [--tamanho 1536x864] [--sem-fallback] [--sem-refs]
  <cenas.json>: lista de {"id": "I001", "prompt": "..."} (ou {"cenas": [...]}); o estilo do canal entra sozinho.

Como funciona
- 1 imagem = 1 `codex exec --json -s read-only` numa pasta vazia em $TMPDIR/codex-img/, pedindo 1 chamada do image_gen
  com o prompt literal (ref_instrucao + prompt da cena + estilo_prompt do canal.yaml) e as `visual.refs` do canal como
  referenced_image_paths. O Codex grava ~/.codex/generated_images/<thread>/*.png (1672x941); a tool reescala para
  --tamanho (padrão visual.tamanho do canal, 1536x864) e salva <saida>/<id>.jpg. O PNG original é apagado depois.
- Falha de uma imagem (sem PNG, recusa, erro, timeout, imagem preta/vazia, moldura) → aquela imagem vai para o fal.
  Limite de cota do Codex (rate_limit_reached_type ou "usage limit") ou 3 falhas seguidas → o RESTO do lote vai para o fal.
- O fallback chama o tools/img_fal.py (sem alterá-lo) numa subpasta <saida>/.fal-fallback/ com --so <ids>, --video,
  --teto e notas "fallback codex"; depois move os .jpg para <saida>/. O img_fal.py registra o custo do fal como sempre.
- Trava a pasta (<saida>/.img.lock, a mesma do img_fal.py/img_openai.py: 2º processo sai com código 3). Pula ids
  que já existem (retomada sem duplicar).
- Registro: <saida>/codex_log.jsonl (1 linha por imagem: gerador codex|fal-fallback, seg, erro, cota 5 h/semanal);
  financas.consumo com custo 0 (fornecedor 'OpenAI ChatGPT Plus', para contar o volume); ops.event_log
  (codex_lote no fim; codex_limite, codex_erro, codex_fallback quando acontecem). Resumo: tools/codex_uso.sh.
- Nunca usa OPENAI_API_KEY (zerada no ambiente do codex). Não lê nem imprime ~/.codex/auth.json.

Variáveis de teste: IMG_CODEX_BIN (outro binário), IMG_CODEX_FORCAR_FALHA=I001,I003 (esses ids rodam com binário
inexistente), IMG_CODEX_SIMULAR_LIMITE=I002 (esse id finge limite de cota).
Códigos de saída: 0 tudo gerado; 1 faltou alguma imagem; 3 pasta travada por outro processo.
"""
import argparse
import concurrent.futures as cf
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

import yaml
from PIL import Image, ImageStat

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _paths import FABRICA  # noqa: E402
from _trava import travar_pasta  # noqa: E402
from db import Jsonb, tentar  # noqa: E402

CODEX = os.environ.get("IMG_CODEX_BIN", os.path.expanduser("~/.local/bin/codex"))
CODEX_HOME = Path(os.environ.get("CODEX_HOME", os.path.expanduser("~/.codex")))
TMP = Path(os.environ.get("TMPDIR") or os.path.expanduser("~/cache/tmp"))
if str(TMP).startswith("/tmp"):  # /tmp é tmpfs (RAM) nesta VPS
    TMP = Path(os.path.expanduser("~/cache/tmp"))
PY = os.path.join(FABRICA, "tools", ".venv", "bin", "python")
IMG_FAL = os.path.join(FABRICA, "tools", "img_fal.py")
FORNECEDOR = "OpenAI ChatGPT Plus"
TIMEOUT = 420
FALHAS_SEGUIDAS_MAX = 3
RE_LIMITE = re.compile(r"usage limit|rate.?limit|too many requests|\b429\b|quota|limit reached", re.I)

INSTR = ("Call the built-in image generation tool (image_gen) EXACTLY ONCE and do nothing else: "
         "no shell commands, no skills, no files, no other tools. Use transparent_background=false. "
         "Pass the prompt below VERBATIM (do not rewrite, shorten or add to it). The image must be a wide 16:9 landscape. "
         "{refs}After the image is generated, reply only with the word OK.\n\nPROMPT:\n{prompt}")
REFS = "Pass referenced_image_paths={paths} (style references only). "

trava_estado = threading.Lock()
estado = {"parar": None, "seguidas": 0, "cota": None}


def evento(tipo, sev, msg, det, ref=None):
    tentar(lambda con: con.execute(
        "INSERT INTO ops.event_log (origem, tipo, severidade, mensagem, detalhes, ref) VALUES ('img_codex', %s, %s, %s, %s, %s)",
        (tipo, sev, msg, Jsonb(det), ref)))


def ler_rollout(thread):
    """Status do image_gen e a cota (rate_limits) que o Codex grava no rollout da sessão."""
    info = {"status": None, "falha": None, "prompt_revisado": None, "cota": None}
    fs = glob.glob(str(CODEX_HOME / "sessions" / "**" / f"rollout-*{thread}.jsonl"), recursive=True)
    if not fs:
        return info
    for linha in open(fs[0], errors="replace"):
        try:
            d = json.loads(linha)
        except Exception:  # noqa: BLE001
            continue
        p = d.get("payload") or {}
        it = p.get("item") or {}
        if isinstance(it, dict) and it.get("kind") == "image_gen.generation":
            info.update(status=it.get("status"), falha=it.get("failure"), prompt_revisado=it.get("revisedPrompt"))
        rl = p.get("rate_limits") or (p.get("info") or {}).get("rate_limits") if isinstance(p, dict) else None
        if isinstance(rl, dict):
            pri, sec = rl.get("primary") or {}, rl.get("secondary") or {}
            info["cota"] = {"pct_5h": pri.get("used_percent"), "reset_5h": pri.get("resets_at"),
                            "pct_semana": sec.get("used_percent"), "reset_semana": sec.get("resets_at"),
                            "plano": rl.get("plan_type"), "limite_atingido": rl.get("rate_limit_reached_type")}
    return info


def imagem_ruim(im):
    """Preta/vazia ou com moldura (as 4 bordas lisas e da mesma cor). Devolve o motivo ou None."""
    g = im.convert("L")
    st = ImageStat.Stat(g)
    if st.mean[0] < 15 or st.stddev[0] < 6:
        return f"imagem preta/vazia (média {st.mean[0]:.0f}, desvio {st.stddev[0]:.0f})"
    w, h = g.size
    m = max(4, round(min(w, h) * 0.012))
    faixas = [g.crop((0, 0, w, m)), g.crop((0, h - m, w, h)), g.crop((0, 0, m, h)), g.crop((w - m, 0, w, h))]
    dentro = [g.crop((m * 2, m * 2, w - m * 2, m * 4)), g.crop((m * 2, h - m * 4, w - m * 2, h - m * 2)),
              g.crop((m * 2, m * 2, m * 4, h - m * 2)), g.crop((w - m * 4, m * 2, w - m * 2, h - m * 2))]
    sts = [ImageStat.Stat(f) for f in faixas]
    medias = [s.mean[0] for s in sts]
    contraste = sum(abs(ImageStat.Stat(d).mean[0] - mm) > 15 for d, mm in zip(dentro, medias))
    # moldura = 4 bordas lisas, da mesma cor e diferentes do que vem logo dentro (fundo branco liso não conta)
    if all(s.stddev[0] < 7 for s in sts) and max(medias) - min(medias) < 12 and contraste >= 3:
        return f"moldura (bordas lisas, média {sum(medias) / 4:.0f})"
    return None


def salvar(png, destino, tam):
    im = Image.open(png).convert("RGB")
    orig = im.size
    motivo = imagem_ruim(im)
    if motivo:
        return orig, motivo
    w, h = im.size
    alvo = tam[0] / tam[1]
    if w / h > alvo:
        nw = round(h * alvo)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    elif w / h < alvo:
        nh = round(w / alvo)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    tmp = str(destino) + ".tmp.jpg"
    im.resize(tam, Image.LANCZOS).save(tmp, "JPEG", quality=92)
    os.replace(tmp, destino)
    return orig, None


def uma(cena, prompt, refs, saida, tam, log, forcar, simular):
    cid = cena["id"]
    destino = saida / f"{cid}.jpg"
    if destino.exists():
        return {"id": cid, "gerador": "existe"}
    with trava_estado:
        if estado["parar"]:
            return {"id": cid, "gerador": "pendente-fal", "erro": f"codex parado: {estado['parar']}"}
    trab = TMP / "codex-img" / f"{os.getpid()}-{cid}"
    trab.mkdir(parents=True, exist_ok=True)
    msg = INSTR.format(prompt=prompt, refs=REFS.format(paths=json.dumps(refs)) if refs else "")
    binario = "/nonexistent/codex-forcado" if cid in forcar else CODEX
    cmd = [binario, "exec", "--skip-git-repo-check", "-s", "read-only", "--json", "-C", str(trab), "-"]
    env = {k: v for k, v in os.environ.items() if k not in ("OPENAI_API_KEY", "OPENAI_BASE_URL")}
    t0 = time.time()
    out, err, rc = "", "", None
    try:
        if cid in simular:
            raise OSError("limite simulado (IMG_CODEX_SIMULAR_LIMITE), codex não chamado")
        r = subprocess.run(cmd, input=msg, capture_output=True, text=True, timeout=TIMEOUT, env=env)
        out, err, rc = r.stdout, r.stderr, r.returncode
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode(errors="replace") if isinstance(e.stdout, bytes) else (e.stdout or "")
        err = f"timeout {TIMEOUT}s"
    except OSError as e:
        err = f"binário: {e}"
    dt = round(time.time() - t0, 1)
    thread, erros = None, []
    for linha in out.splitlines():
        try:
            ev = json.loads(linha)
        except Exception:  # noqa: BLE001
            continue
        t = ev.get("type")
        if t == "thread.started":
            thread = ev.get("thread_id")
        elif t in ("error", "turn.failed") or (ev.get("item") or {}).get("type") == "error":
            erros.append(json.dumps(ev, ensure_ascii=False)[:300])
    info = ler_rollout(thread) if thread else {}
    cota = info.get("cota")
    pngs = sorted(glob.glob(str(CODEX_HOME / "generated_images" / str(thread) / "*.png")), key=os.path.getmtime) if thread else []
    reg = {"id": cid, "gerador": "codex", "seg": dt, "thread": thread, "rc": rc, "status": info.get("status"),
           "falha_gen": info.get("falha"), "cota": cota, "erro": None,
           "prompt_igual": ((info.get("prompt_revisado") or "").strip() == prompt.strip()) if info.get("prompt_revisado") else None}
    texto_erro = " | ".join(erros + ([err.strip()[-300:]] if err and err.strip() else []))
    limite = bool(cota and cota.get("limite_atingido")) or (not pngs and bool(RE_LIMITE.search(texto_erro)))
    if cid in simular:
        limite, texto_erro = True, "limite simulado (IMG_CODEX_SIMULAR_LIMITE)"
    if pngs:
        try:
            orig, motivo = salvar(pngs[-1], destino, tam)
            reg["tam_orig"] = list(orig)
            if motivo:
                reg["erro"] = motivo
        except Exception as e:  # noqa: BLE001
            reg["erro"] = f"conversão: {e}"
        for p in pngs:  # o PNG original (≈2 MB) não fica acumulando em ~/.codex
            Path(p).unlink(missing_ok=True)
    else:
        reg["erro"] = texto_erro or (f"sem imagem (status {info.get('status')}, falha {info.get('falha')})")
    shutil.rmtree(trab, ignore_errors=True)
    if limite:
        reg["erro"] = f"LIMITE: {reg['erro']}"
    ok = destino.exists() and not reg["erro"]
    if not ok:
        reg["gerador"] = "pendente-fal"
        destino.unlink(missing_ok=True)
    with trava_estado:
        if cota:
            estado["cota"] = cota
        if ok:
            estado["seguidas"] = 0
        else:
            estado["seguidas"] += 1
            if limite and not estado["parar"]:
                estado["parar"] = "limite de cota"
                evento("codex_limite", "aviso", f"Codex acusou limite de cota em {cid}; resto do lote vai para o fal",
                       {"id": cid, "cota": cota, "erro": reg["erro"][:300]}, str(saida))
            elif estado["seguidas"] >= FALHAS_SEGUIDAS_MAX and not estado["parar"]:
                estado["parar"] = f"{FALHAS_SEGUIDAS_MAX} falhas seguidas"
            if not limite:
                evento("codex_erro", "aviso", f"Codex falhou em {cid}: {reg['erro'][:160]}",
                       {"id": cid, "seg": dt, "erro": reg["erro"][:500], "status": info.get("status")}, str(saida))
    with open(log, "a") as f:
        f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), **reg}, ensure_ascii=False) + "\n")
    return reg


def fallback_fal(a, ids, saida, log, cenas_path):
    """Gera `ids` no img_fal.py (sem alterá-lo) numa subpasta e move para a saída. Devolve os ids que ficaram prontos."""
    sub = saida / ".fal-fallback"
    sub.mkdir(exist_ok=True)
    cmd = [PY, IMG_FAL, a.canal, str(cenas_path), str(sub), "--so", ",".join(ids), "--paralelo", str(min(4, max(1, len(ids)))),
           "--notas", f"fallback codex {a.notas}".strip()]
    if a.video:
        cmd += ["--video", str(a.video)]
    if a.teto:
        cmd += ["--teto", str(a.teto)]
    if a.modelo_fal:
        cmd += ["--modelo", a.modelo_fal]
    print(f"\nfallback fal: {len(ids)} imagens ({','.join(ids)})", flush=True)
    t0 = time.time()
    r = subprocess.run(cmd, cwd=os.path.join(FABRICA, "tools"), capture_output=True, text=True, timeout=3600)
    print(r.stdout[-1500:], r.stderr[-800:], sep="\n", flush=True)
    feitos = []
    for cid in ids:
        src = sub / f"{cid}.jpg"
        if src.exists():
            if a.tamanho_explicito:
                im = Image.open(src).convert("RGB")
                if im.size != a.tam:
                    im.resize(a.tam, Image.LANCZOS).save(src, "JPEG", quality=92)
            os.replace(src, saida / f"{cid}.jpg")
            feitos.append(cid)
    with open(log, "a") as f:
        for cid in ids:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "id": cid, "gerador": "fal-fallback",
                                "seg": round((time.time() - t0) / max(1, len(ids)), 1),
                                "erro": None if cid in feitos else "fal também falhou"}, ensure_ascii=False) + "\n")
    shutil.rmtree(sub, ignore_errors=True)
    return feitos


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canal")
    ap.add_argument("cenas")
    ap.add_argument("saida")
    ap.add_argument("--video", type=int, help="id em youtube.videos (custo/volume atribuído ao vídeo)")
    ap.add_argument("--paralelo", type=int, default=3, help="processos codex ao mesmo tempo (3 testado em 14/11/2026)")
    ap.add_argument("--so", help="só estes ids (vírgula)")
    ap.add_argument("--teto", type=float, help="teto em US$ repassado ao img_fal.py no fallback")
    ap.add_argument("--notas", default="")
    ap.add_argument("--tamanho", help="WxH final (padrão: visual.tamanho do canal ou 1536x864; thumb pode usar 1280x720)")
    ap.add_argument("--modelo-fal", help="modelo do fal no fallback (padrão: visual.modelo do canal.yaml)")
    ap.add_argument("--sem-fallback", action="store_true", help="não chama o fal (as falhas ficam faltando)")
    ap.add_argument("--sem-refs", action="store_true")
    a = ap.parse_args()

    pasta_canal = Path(FABRICA) / "canais" / a.canal
    visual = (yaml.safe_load(open(pasta_canal / "canal.yaml")) or {}).get("visual", {})
    if a.tamanho:
        a.tam = tuple(int(x) for x in a.tamanho.lower().split("x"))
    else:
        t = visual.get("tamanho")
        a.tam = (t["width"], t["height"]) if isinstance(t, dict) else (1536, 864)
    a.tamanho_explicito = bool(a.tamanho)
    estilo = visual.get("estilo_prompt", "")
    refs = [] if a.sem_refs else [str(pasta_canal / r) for r in visual.get("refs", []) if (pasta_canal / r).exists()]
    instr = visual.get("ref_instrucao", "") if refs else ""
    raw = json.load(open(a.cenas))
    cenas = raw["cenas"] if isinstance(raw, dict) else raw
    if a.so:
        so = set(a.so.split(","))
        cenas = [c for c in cenas if c["id"] in so]
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    trava = travar_pasta(str(saida))  # noqa: F841  (mesma trava do img_fal/img_openai)
    TMP.mkdir(parents=True, exist_ok=True)
    log = saida / "codex_log.jsonl"
    forcar = set(filter(None, os.environ.get("IMG_CODEX_FORCAR_FALHA", "").split(",")))
    simular = set(filter(None, os.environ.get("IMG_CODEX_SIMULAR_LIMITE", "").split(",")))
    pendentes = [c for c in cenas if not (saida / f"{c['id']}.jpg").exists()]
    print(f"codex · {len(pendentes)} pendentes de {len(cenas)} · refs {len(refs)} · paralelo {a.paralelo} · {a.tam[0]}x{a.tam[1]}"
          f"{' · TESTE forçar falha ' + ','.join(sorted(forcar)) if forcar else ''}"
          f"{' · TESTE simular limite ' + ','.join(sorted(simular)) if simular else ''}", flush=True)

    t0 = time.time()
    regs = []
    with cf.ThreadPoolExecutor(max(1, a.paralelo)) as ex:
        futs = {ex.submit(uma, c, instr + (f"{c['prompt']}. {estilo}".strip(". ") if estilo else c["prompt"]),
                          refs, saida, a.tam, log, forcar, simular): c["id"] for c in pendentes}
        for f in cf.as_completed(futs):
            try:
                r = f.result()
            except Exception as e:  # noqa: BLE001
                r = {"id": futs[f], "gerador": "pendente-fal", "erro": f"exceção: {e}"}
            regs.append(r)
            if r["gerador"] == "codex":
                print(f"{r['id']}: ok codex {r['seg']}s", flush=True)
            elif r["gerador"] == "pendente-fal":
                print(f"{r['id']}: codex FALHOU → fal ({(r.get('erro') or '')[:140]})", flush=True)
    t_codex = round(time.time() - t0)
    ok_codex = [r["id"] for r in regs if r["gerador"] == "codex"]
    falhas = [r["id"] for r in regs if r["gerador"] == "pendente-fal"]

    feitos_fal = []
    if falhas and not a.sem_fallback:
        evento("codex_fallback", "aviso", f"{len(falhas)} imagens do Codex foram para o fal ({estado['parar'] or 'falha pontual'})",
               {"ids": falhas, "motivo": estado["parar"] or "falha pontual", "canal": a.canal, "video": a.video}, str(saida))
        feitos_fal = fallback_fal(a, falhas, saida, log, Path(a.cenas).resolve())

    cota = estado["cota"] or {}
    if ok_codex:
        tentar(lambda con: con.execute(
            "INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
            " VALUES ('youtube', %s, %s, 'imagem codex image_gen (cota Plus)', %s, 'imagens', 0, 'USD', 0, %s, %s, %s)",
            (a.canal, FORNECEDOR, len(ok_codex), "youtube.video" if a.video else None, a.video,
             f"{a.notas} {os.path.basename(a.cenas)}; cota 5h {cota.get('pct_5h')}% semana {cota.get('pct_semana')}%; "
             f"{len(falhas)} no fallback fal".strip())))
    resumo = {"canal": a.canal, "video": a.video, "cenas": os.path.basename(a.cenas), "pedidas": len(pendentes),
              "codex_ok": len(ok_codex), "fallback_pedidas": len(falhas), "fallback_ok": len(feitos_fal),
              "faltando": len(falhas) - len(feitos_fal), "parou": estado["parar"], "seg_codex": t_codex, "cota": cota}
    if pendentes:
        evento("codex_lote", "info" if resumo["faltando"] == 0 else "erro",
               f"img_codex {a.canal}: {len(ok_codex)} codex, {len(feitos_fal)} fal, {resumo['faltando']} faltando", resumo, str(saida))
    print(f"\n{len(ok_codex)} codex + {len(feitos_fal)} fal-fallback · {len(cenas) - len(pendentes)} já existiam · "
          f"{resumo['faltando']} faltando · codex {t_codex}s · cota 5h {cota.get('pct_5h')}% semana {cota.get('pct_semana')}%"
          f"{' · PAROU: ' + estado['parar'] if estado['parar'] else ''}")
    faltam = [c["id"] for c in cenas if not (saida / f"{c['id']}.jpg").exists()]
    if faltam:
        print("Faltando (rode de novo para tentar só estas):", ",".join(faltam))
        sys.exit(1)


if __name__ == "__main__":
    main()
