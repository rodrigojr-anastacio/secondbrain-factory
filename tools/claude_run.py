"""Roda uma etapa curta do Claude Code (claude -p) para um vídeo, com trava anti-duplicação e registro de custo.

Uso:
  tools/.venv/bin/python tools/claude_run.py --video <id> --etapa <etapa> --cwd <pasta do vídeo> \
      (--prompt "..." | --prompt-file BRIEF-ETAPA.md) [--modelo opus|sonnet|<id>] [--timeout 3600] \
      [--max-turns N] [--permission-mode bypassPermissions] [--dry-run] [-- <args extras do claude>]

- Modelo por etapa: opus em roteiro e storyboard (e roteiro-storyboard); sonnet no resto. --modelo sobrescreve.
- Trava: ~/.cache/fabrica/locks/claude-<video>-<etapa>.lock (flock não bloqueante). Se já houver outra execução
  do mesmo vídeo+etapa, avisa e sai com código 3 sem chamar o claude.
- Chama `claude -p --output-format json --model <m>` (prompt pelo stdin), grava uma linha em
  youtube.execucoes_claude e o JSON bruto em <cwd>/logs/claude-<etapa>-<data>.json (logs/ fica fora do git).
- Saída: o texto final do Claude no stdout; o resumo (modelo, turnos, tokens, custo) no stderr.
  Código de saída: 0 ok, 1 erro do claude/timeout, 2 argumento inválido, 3 trava ocupada.
- custo_usd_equivalente = total_cost_usd (preço de lista). No plano Max não é cobrança: serve para comparar.
Etapas sem vídeo (sem --video): `teste` (testes) e as rotinas `tendencias` e `metricas` (tools/rotinas/*.sh). A view
youtube.custo_claude_por_video ignora essas linhas (só conta linhas com video_id).
"""
import argparse
import datetime as dt
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from db import conectar, tentar  # noqa: E402

OPUS = {"roteiro", "storyboard", "roteiro-storyboard"}
ETAPAS = ["pesquisa-referencia", "roteiro", "storyboard", "roteiro-storyboard", "producao", "voz", "imagens",
          "montagem-render", "thumbnail", "pacote-youtube", "qa", "teste", "tendencias", "metricas", "palavras-chave"]
SEM_VIDEO = {"teste", "tendencias", "metricas", "palavras-chave"}  # etapas que não pertencem a um vídeo
LOCKS = os.path.expanduser(os.environ.get("FABRICA_LOCKS", "~/.cache/fabrica/locks"))


def modelo_da_etapa(etapa):
    return "opus" if etapa in OPUS else "sonnet"


def travar(video, etapa):
    """Retorna o arquivo travado (mantenha aberto) ou None se outra execução já segura a trava."""
    os.makedirs(LOCKS, exist_ok=True)
    caminho = os.path.join(LOCKS, f"claude-{video if video is not None else 'sem-video'}-{etapa}.lock")
    f = open(caminho, "a+")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        f.seek(0)
        dono = f.read().strip() or "?"
        f.close()
        print(f"[claude_run] AVISO: já existe execução do vídeo {video if video is not None else '(sem vídeo)'} etapa '{etapa}' em andamento ({dono}). "
              f"Nada foi chamado. Trava: {caminho}", file=sys.stderr)
        return None
    f.seek(0)
    f.truncate()
    f.write(f"pid={os.getpid()} desde={dt.datetime.now().isoformat(timespec='seconds')}\n")
    f.flush()
    return f


def video_existe(video):
    try:
        with conectar() as con:
            return con.execute("SELECT 1 FROM youtube.videos WHERE id=%s", (video,)).fetchone() is not None
    except Exception as e:  # noqa: BLE001
        print(f"[claude_run] aviso: não consegui conferir o vídeo no banco ({type(e).__name__}); sigo.", file=sys.stderr)
        return True


def n(d, *chaves):
    for k in chaves:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", type=int, help="id em youtube.videos (obrigatório, exceto nas etapas " + ", ".join(sorted(SEM_VIDEO)) + ")")
    ap.add_argument("--etapa", required=True, help=" | ".join(ETAPAS) + " (outras etapas: letras, números e '-')")
    ap.add_argument("--cwd", default=".", help="pasta onde o claude roda (a pasta do vídeo)")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--prompt")
    g.add_argument("--prompt-file")
    ap.add_argument("--modelo", help="sobrescreve o modelo da etapa (opus, sonnet ou id completo)")
    ap.add_argument("--timeout", type=int, default=3600, help="segundos (padrão 3600)")
    ap.add_argument("--max-turns", type=int)
    ap.add_argument("--permission-mode", help="repassado ao claude (ex.: bypassPermissions, acceptEdits)")
    ap.add_argument("--dry-run", action="store_true", help="mostra o comando e confere a trava, sem chamar o claude")
    ap.add_argument("extras", nargs=argparse.REMAINDER, help="depois de --: argumentos extras do claude")
    a = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", a.etapa):
        ap.error("etapa inválida (use letras minúsculas, números e '-')")
    if a.video is None and a.etapa not in SEM_VIDEO:
        ap.error("--video é obrigatório (só as etapas " + ", ".join(sorted(SEM_VIDEO)) + " rodam sem vídeo)")
    cwd = os.path.abspath(os.path.expanduser(a.cwd))
    if not os.path.isdir(cwd):
        ap.error(f"--cwd não existe: {cwd}")
    prompt = a.prompt if a.prompt is not None else open(os.path.expanduser(a.prompt_file), encoding="utf-8").read()
    if not prompt.strip():
        ap.error("prompt vazio")
    if a.video is not None and not video_existe(a.video):
        ap.error(f"vídeo {a.video} não existe em youtube.videos (crie a linha antes)")
    modelo = a.modelo or modelo_da_etapa(a.etapa)
    extras = a.extras[1:] if a.extras[:1] == ["--"] else a.extras
    claude = shutil.which("claude") or os.path.expanduser("~/.local/bin/claude")
    cmd = [claude, "-p", "--output-format", "json", "--model", modelo]
    if a.max_turns:
        cmd += ["--max-turns", str(a.max_turns)]
    if a.permission_mode:
        cmd += ["--permission-mode", a.permission_mode]
    cmd += extras

    trava = travar(a.video, a.etapa)
    if trava is None:
        sys.exit(3)

    if a.dry_run:
        print(f"[dry-run] trava ok ({trava.name})")
        print(f"[dry-run] cwd: {cwd}")
        print(f"[dry-run] modelo: {modelo} (etapa {a.etapa}) · timeout {a.timeout}s")
        print(f"[dry-run] comando: {' '.join(cmd)}  < prompt ({len(prompt)} caracteres)")
        print(f"[dry-run] prompt (início): {prompt[:200]!r}")
        return

    inicio = dt.datetime.now(dt.timezone.utc)
    t0 = time.monotonic()
    saida, erro_txt, subtype = "", "", None
    try:
        p = subprocess.run(cmd, cwd=cwd, env={**os.environ, "CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS": "0"}, input=prompt, capture_output=True, text=True, timeout=a.timeout)
        saida, erro_txt, rc = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired as e:
        saida = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        rc, subtype = -1, "timeout"
    fim = dt.datetime.now(dt.timezone.utc)
    duracao_ms = int((time.monotonic() - t0) * 1000)

    try:
        j = json.loads(saida) if saida.strip() else {}
        if isinstance(j, list):  # formato antigo/alternativo: lista de eventos; o último "result" vale
            j = next((x for x in reversed(j) if isinstance(x, dict) and x.get("type") == "result"), {})
    except json.JSONDecodeError:
        j = {}
    resultado = j.get("result")
    if resultado is None:
        resultado = (saida or erro_txt or "").strip()[-2000:] or "(sem saída)"
    is_error = bool(j.get("is_error")) or rc != 0 or not j
    subtype = subtype or j.get("subtype") or ("sem_json" if not j else None)
    u = j.get("usage") or {}
    modelos_reais = ",".join(sorted((j.get("modelUsage") or {}).keys())) or None
    custo = j.get("total_cost_usd", j.get("cost_usd"))

    os.makedirs(os.path.join(cwd, "logs"), exist_ok=True)
    log = os.path.join(cwd, "logs", f"claude-{a.etapa}-{inicio.astimezone():%Y%m%d-%H%M%S}.json")
    with open(log, "w", encoding="utf-8") as f:
        json.dump(j or {"stdout": saida[-5000:], "stderr": erro_txt[-5000:], "rc": rc}, f, ensure_ascii=False, indent=1)

    def registrar(con):
        return con.execute(
            "INSERT INTO youtube.execucoes_claude (video_id, etapa, modelo, modelo_real, session_id, inicio, fim,"
            " duracao_ms, num_turns, input_tokens, output_tokens, cache_read_tokens, cache_creation_tokens,"
            " custo_usd_equivalente, is_error, subtype, resultado, cwd, prompt_resumo)"
            " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id",
            (a.video, a.etapa, modelo, modelos_reais, j.get("session_id"), inicio, fim,
             duracao_ms, j.get("num_turns"), u.get("input_tokens"), u.get("output_tokens"),
             u.get("cache_read_input_tokens"), u.get("cache_creation_input_tokens"), custo, is_error, subtype,
             str(resultado)[:2000], cwd, prompt[:300])).fetchone()[0]
    reg = tentar(registrar)

    print(resultado)
    custo_txt = f"US$ {custo:.4f}" if isinstance(custo, (int, float)) else "US$ ?"
    print(f"\n[claude_run] vídeo {a.video if a.video is not None else '-'} · {a.etapa} · {modelos_reais or modelo} · {duracao_ms / 1000:.0f}s · "
          f"{j.get('num_turns', '?')} turnos · in {u.get('input_tokens', '?')} / out {u.get('output_tokens', '?')} / "
          f"cache r {u.get('cache_read_input_tokens', '?')} c {u.get('cache_creation_input_tokens', '?')} · "
          f"{custo_txt} equivalente · {'ERRO ' + str(subtype) if is_error else 'ok'} · "
          f"execucoes_claude id {reg} · log {log}", file=sys.stderr)
    sys.exit(1 if is_error else 0)


if __name__ == "__main__":
    main()
