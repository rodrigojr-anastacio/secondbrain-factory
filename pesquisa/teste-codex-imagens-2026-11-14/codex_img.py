"""Protótipo: gera imagens pelo Codex CLI (ChatGPT Plus, ferramenta interna image_gen), SEM chave de API.

Teste de 14/11/2026 (pesquisa/teste-codex-imagens-2026-11-14). Não substitui tools/img_fal.py ainda.

Uso (da raiz do repo):
  tools/.venv/bin/python pesquisa/teste-codex-imagens-2026-11-14/codex_img.py <canal> <cenas.json> <saida/> \
      [--ids I001,I013] [--paralelo 3] [--estilo-extra "..."] [--sem-refs]

Como funciona (1 imagem = 1 `codex exec`, mapeamento determinístico):
  - monta o prompt como o img_fal.py: ref_instrucao (se o canal usa refs) + prompt da cena + estilo_prompt do canal.yaml;
  - roda `codex exec --json -s read-only` numa pasta vazia em $HOME/cache/tmp, pedindo 1 chamada do image_gen com o
    prompt literal (e as refs do canal em referenced_image_paths, se houver);
  - o Codex grava a imagem em ~/.codex/generated_images/<thread_id>/*.png (thread_id vem do evento thread.started);
  - lê o rollout da sessão (~/.codex/sessions/**/rollout-*<thread_id>.jsonl) para status/recusa/prompt revisado;
  - converte para JPEG 1536x864 (recorte central para 16:9 + reescala) em <saida>/<id>.jpg;
  - grava <saida>/codex_log.jsonl (id, segundos, tamanho original, tokens, status, falha).
Pula ids que já existem. Trava a pasta de saída (.codex.lock). Não lê nem imprime credenciais.
"""
import argparse, concurrent.futures as cf, glob, json, os, subprocess, sys, time
from pathlib import Path

import yaml
from PIL import Image

REPO = Path(__file__).resolve().parents[2]
CODEX = os.path.expanduser("~/.local/bin/codex")
CODEX_HOME = Path(os.environ.get("CODEX_HOME", os.path.expanduser("~/.codex")))
TMP = Path(os.environ.get("TMPDIR", os.path.expanduser("~/cache/tmp")))
FINAL = (1536, 864)

INSTR = ("Call the built-in image generation tool (tools.image_gen__imagegen) EXACTLY ONCE and do nothing else: "
         "no shell commands, no skills, no files, no other tools. Use transparent_background=false. "
         "Pass the prompt below VERBATIM (do not rewrite, shorten or add to it). The image must be a wide 16:9 landscape. "
         "{refs}After the image is generated, reply only with the word OK.\n\nPROMPT:\n{prompt}")
REFS = ("Pass referenced_image_paths={paths} (style references only). ")


def carregar_canal(canal):
    y = REPO / "canais" / canal / "canal.yaml"
    if not y.exists():
        return {}, REPO / "canais" / canal
    return yaml.safe_load(open(y)).get("visual", {}), y.parent


def rollout(thread):
    fs = glob.glob(str(CODEX_HOME / "sessions" / "**" / f"rollout-*{thread}.jsonl"), recursive=True)
    info = {"status": None, "falha": None, "prompt_revisado": None, "salvo": None, "tokens": None}
    if not fs:
        return info
    for l in open(fs[0]):
        try:
            d = json.loads(l)
        except Exception:
            continue
        p = d.get("payload", {})
        it = p.get("item") or {}
        if isinstance(it, dict) and it.get("kind") == "image_gen.generation":
            info.update(status=it.get("status"), falha=it.get("failure"), prompt_revisado=it.get("revisedPrompt"),
                        salvo=it.get("savedPath"))
    return info


def uma(cena, prompt, refs, saida, log):
    cid = cena["id"]
    destino = saida / f"{cid}.jpg"
    if destino.exists():
        return cid, "existe"
    trab = TMP / "codex-img" / cid
    trab.mkdir(parents=True, exist_ok=True)
    msg = INSTR.format(prompt=prompt, refs=REFS.format(paths=json.dumps(refs)) if refs else "")
    cmd = [CODEX, "exec", "--skip-git-repo-check", "-s", "read-only", "--json", "-C", str(trab), "-"]
    t0 = time.time()
    try:
        r = subprocess.run(cmd, input=msg, capture_output=True, text=True, timeout=420,
                           env={**os.environ, "OPENAI_API_KEY": ""})
        out = r.stdout
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
    dt = round(time.time() - t0, 1)
    thread, tokens, erros = None, None, []
    for l in out.splitlines():
        try:
            ev = json.loads(l)
        except Exception:
            continue
        if ev.get("type") == "thread.started":
            thread = ev.get("thread_id")
        elif ev.get("type") == "turn.completed":
            tokens = ev.get("usage")
        elif ev.get("type") in ("error", "turn.failed") or (ev.get("item") or {}).get("type") == "error":
            erros.append(str(ev)[:300])
    info = rollout(thread) if thread else {}
    pngs = sorted(glob.glob(str(CODEX_HOME / "generated_images" / str(thread) / "*.png")), key=os.path.getmtime) if thread else []
    reg = {"id": cid, "seg": dt, "thread": thread, "tokens": tokens, "n_png": len(pngs), **{k: info.get(k) for k in ("status", "falha")},
           "prompt_igual": (info.get("prompt_revisado") or "").strip() == prompt.strip() if info.get("prompt_revisado") else None,
           "erros": erros[:3]}
    if pngs:
        im = Image.open(pngs[-1]).convert("RGB")
        reg["tam_orig"] = im.size
        w, h = im.size
        alvo = FINAL[0] / FINAL[1]
        if w / h > alvo:
            nw = round(h * alvo); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        elif w / h < alvo:
            nh = round(w / alvo); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im.resize(FINAL, Image.LANCZOS).save(destino, "JPEG", quality=90)
    with open(log, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    return cid, f"{'ok' if pngs else 'FALHOU'} {dt}s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("canal"); ap.add_argument("cenas"); ap.add_argument("saida")
    ap.add_argument("--ids", default=""); ap.add_argument("--paralelo", type=int, default=1)
    ap.add_argument("--estilo", default=None, help="sobrescreve o estilo_prompt do canal.yaml")
    ap.add_argument("--sem-refs", action="store_true")
    a = ap.parse_args()
    visual, pasta_canal = carregar_canal(a.canal)
    estilo = a.estilo if a.estilo is not None else visual.get("estilo_prompt", "")
    refs = [] if a.sem_refs else [str(pasta_canal / r) for r in visual.get("refs", [])]
    instr = visual.get("ref_instrucao", "") if refs else ""
    cenas = json.load(open(a.cenas))
    cenas = cenas["cenas"] if isinstance(cenas, dict) else cenas
    if a.ids:
        q = a.ids.split(","); cenas = [c for c in cenas if c["id"] in q]
    saida = Path(a.saida); saida.mkdir(parents=True, exist_ok=True)
    trava = saida / ".codex.lock"
    try:
        fd = os.open(trava, os.O_CREAT | os.O_EXCL | os.O_WRONLY); os.write(fd, str(os.getpid()).encode()); os.close(fd)
    except FileExistsError:
        sys.exit(3)
    try:
        log = saida / "codex_log.jsonl"
        t0 = time.time()
        with cf.ThreadPoolExecutor(a.paralelo) as ex:
            fut = [ex.submit(uma, c, (instr + f"{c['prompt']}. {estilo}".strip(". ")) if estilo else instr + c["prompt"], refs, saida, log)
                   for c in cenas]
            for f in cf.as_completed(fut):
                print(*f.result(), flush=True)
        print(f"total {round(time.time() - t0)}s para {len(cenas)} cenas, paralelo {a.paralelo}")
    finally:
        trava.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
