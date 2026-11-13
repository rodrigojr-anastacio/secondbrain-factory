#!/usr/bin/env python
"""Fila de jobs `claude -p` em ops.fila_jobs: dispara, acompanha e retoma sozinho (tick a cada 3 min pelo timer fabrica-fila).

Uso:
  fila.sh add <nome> <brief> [--modelo opus|sonnet] [--motor max|api] [--prioridade N] [--prazo 'YYYY-MM-DD HH:MM'] [--depende-de nome] [--log caminho]
  fila.sh list | tick [--dry-run] | cancel <nome> | retomar <nome>
Config opcional: ~/.config/fabrica/fila.env (MAX_CONCORRENCIA=2, MEM_MIN_GB=2.5).
Nunca mata processos. Lock (flock) impede dois ticks juntos.
"""
import argparse
import fcntl
import glob
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import psycopg  # noqa: E402
from event_log import registrar  # noqa: E402

HOME = Path.home()
REPO = HOME / "workspace/fabrica-youtube"
REF = HOME / "workspace/referencias"
FILA_LOG = REF / "fila.log"
STATUS_MD = REF / "fila-status.md"
SESS_DIR = HOME / ".claude/projects/-home-hermes-workspace-fabrica-youtube"
TZ = ZoneInfo("America/Sao_Paulo")
TOOLS = ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Task", "WebFetch", "WebSearch"]
DB = os.environ.get("FABRICA_DB", "dbname=vida")
COLS = "id,nome,brief,log,modelo,motor,prioridade,prazo,depende_de,status,unit,session_id,retomar_em,tentativas,iniciado_em,terminado_em,obs"
LIMIT_RE = re.compile(r"hit your[^\n]*?limit[^\n]*?resets\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", re.I)


def cfg():
    c = {"MAX_CONCORRENCIA": "2", "MEM_MIN_GB": "2.5"}
    f = HOME / ".config/fabrica/fila.env"
    if f.exists():
        for ln in f.read_text().splitlines():
            if "=" in ln and not ln.strip().startswith("#"):
                k, v = ln.split("=", 1)
                c[k.strip()] = v.strip()
    return c


def logar(msg, nome=None, tipo="info", sev="info", dry=False):
    linha = f"{datetime.now(TZ):%Y-%m-%d %H:%M:%S} {'[dry] ' if dry else ''}{nome or '-'}: {msg}"
    print(linha)
    if dry:
        return
    with open(FILA_LOG, "a") as f:
        f.write(linha + "\n")
    registrar("fila", tipo, sev, f"{nome}: {msg}", ref=nome)


def mem_disp_gb():
    for ln in open("/proc/meminfo"):
        if ln.startswith("MemAvailable"):
            return int(ln.split()[1]) / 1048576
    return 0


def unit_ativa(unit):
    return subprocess.run(["systemctl", "--user", "is-active", f"{unit}.scope"], capture_output=True, text=True).stdout.strip() == "active"


def ler_log(path, n=4000):
    try:
        with open(path, "rb") as f:
            f.seek(0, 2)
            f.seek(max(0, f.tell() - n))
            return f.read().decode("utf-8", "replace")
    except OSError:
        return ""


def parse_reset(texto, agora=None):
    """'You've hit your 5-hour limit · resets 7:50pm (America/Sao_Paulo)' → datetime do reset + 2 min (ou +60 min se não ler)."""
    agora = agora or datetime.now(TZ)
    m = None
    for m in LIMIT_RE.finditer(texto):
        pass
    if not m:
        return agora + timedelta(minutes=60)
    h, mi, ap = int(m.group(1)), int(m.group(2) or 0), (m.group(3) or "").lower()
    if ap == "pm" and h < 12:
        h += 12
    if ap == "am" and h == 12:
        h = 0
    try:
        r = agora.replace(hour=h, minute=mi, second=0, microsecond=0)
    except ValueError:
        return agora + timedelta(minutes=60)
    if r <= agora - timedelta(hours=1):
        r += timedelta(days=1)
    return r + timedelta(minutes=2)


def classificar(job, agora=None):
    """Devolve (status, retomar_em|None, motivo) para um job cuja unit terminou."""
    texto = ler_log(job["log"])
    cauda = texto[-1500:]
    if not texto.strip():
        return "falhou", None, "log vazio"
    if LIMIT_RE.search(cauda) or re.search(r"hit your[^\n]*limit", cauda, re.I):
        return "pausado_limite", parse_reset(cauda, agora), "limite do Claude Max"
    ini = job["iniciado_em"]
    brief_txt = ""
    try:
        brief_txt = Path(os.path.expanduser(job["brief"])).read_text()
    except OSError:
        pass
    for b in glob.glob(str(REPO / "canais/**/BLOQUEIO.md"), recursive=True):
        p = Path(b)
        if ini and datetime.fromtimestamp(p.stat().st_mtime, timezone.utc) >= ini and (p.parent.name in brief_txt or p.parent.parent.name in brief_txt and p.parent.name in job["nome"]):
            return "bloqueado", None, f"BLOQUEIO.md em {p.parent.relative_to(REPO)}"
    if re.search(r"(?m)^(Error|API Error|Execution error)|Reached max turns|credit balance is too low", cauda):
        return "falhou", None, "erro no log"
    return "concluido", None, "saída normal"


def achar_session(job):
    base = os.path.basename(job["brief"])
    ini = job["iniciado_em"].timestamp() - 120 if job["iniciado_em"] else 0
    cands = sorted(SESS_DIR.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    for p in cands:
        if p.stat().st_mtime < ini:
            break
        try:
            with open(p, "rb") as f:
                if base.encode() in f.read(30000):
                    return p.stem
        except OSError:
            pass
    return None


def disparar(con, job, dry, retomada=False):
    nome = job["nome"]
    n = job["tentativas"] + 1
    unit = f"job-{nome}" if n == 1 else f"job-{nome}-r{n - 1}"
    brief = os.path.expanduser(job["brief"])
    if job["motor"] == "api":
        cmd = [str(REPO / "tools/job_api.sh"), brief, job["log"], "--modelo", job["modelo"]]
    else:
        prompt = (f"Continue o brief {brief} de onde parou; tudo em primeiro plano" if retomada else f"Execute o brief em {brief}")
        cmd = ["claude", "-p", prompt, "--model", job["modelo"], "--max-turns", "400", "--allowedTools", ",".join(TOOLS)]
        if retomada:
            cmd += ["--resume", job["session_id"]]
    full = ["systemd-run", "--user", "--scope", f"--unit={unit}", "-p", "MemoryMax=3500M", "-p", "MemorySwapMax=512M", "-q"] + cmd
    logar(f"{'retomar' if retomada else 'iniciar'} → {unit} ({job['motor']}/{job['modelo']})", nome, "job_inicio", dry=dry)
    if dry:
        return
    env = dict(os.environ, TMPDIR=str(HOME / "cache/tmp"), CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS="0")
    env.pop("ANTHROPIC_API_KEY", None) if job["motor"] == "max" else None
    os.makedirs(env["TMPDIR"], exist_ok=True)
    lg = open(job["log"], "ab")
    subprocess.Popen(full, cwd=REPO, env=env, stdout=lg, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
    con.execute("UPDATE ops.fila_jobs SET status='rodando', unit=%s, tentativas=%s, iniciado_em=now(), retomar_em=NULL, terminado_em=NULL WHERE id=%s", (unit, n, job["id"]))
    # oom_score_adj=800 nos PIDs do cgroup (OOMScoreAdjust não vale em scope)
    import time
    for _ in range(20):
        time.sleep(0.5)
        cg = subprocess.run(["systemctl", "--user", "show", f"{unit}.scope", "-p", "ControlGroup", "--value"], capture_output=True, text=True).stdout.strip()
        pf = Path(f"/sys/fs/cgroup{cg}/cgroup.procs") if cg else None
        if pf and pf.exists() and pf.read_text().split():
            for pid in pf.read_text().split():
                try:
                    Path(f"/proc/{pid}/oom_score_adj").write_text("800")
                except OSError:
                    pass
            break


def jobs(con, where="true", args=()):
    cur = con.execute(f"SELECT {COLS} FROM ops.fila_jobs WHERE {where} ORDER BY prioridade, prazo NULLS LAST, id", args)
    names = [d.name for d in cur.description]
    return [dict(zip(names, r)) for r in cur.fetchall()]


def tick(dry):
    lock = open("/tmp/fabrica-fila.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("outro tick em andamento")
        return
    c = cfg()
    agora = datetime.now(TZ)
    with psycopg.connect(DB, autocommit=True) as con:
        # 1. reconciliar
        for j in jobs(con, "status='rodando'"):
            if j["unit"] and unit_ativa(j["unit"]):
                continue
            st, ret, motivo = classificar(j, agora)
            sid = j["session_id"] or achar_session(j)
            if st == "falhou" and j["tentativas"] < 2 and sid and j["motor"] == "max":
                logar(f"falhou ({motivo}); retentativa com --resume", j["nome"], "job_retry", "aviso", dry)
                if not dry:
                    con.execute("UPDATE ops.fila_jobs SET session_id=%s WHERE id=%s", (sid, j["id"]))
                j["session_id"] = sid
                disparar(con, j, dry, retomada=True)
                continue
            resumo = ler_log(j["log"], 600).strip()
            logar(f"{j['status']} → {st} ({motivo})" + (f", retoma {ret:%d/%m %H:%M}" if ret else ""), j["nome"], f"job_{st}", "aviso" if st in ("falhou", "bloqueado", "pausado_limite") else "info", dry)
            if not dry:
                con.execute("UPDATE ops.fila_jobs SET status=%s, session_id=%s, retomar_em=%s, terminado_em=now(), resumo=%s, obs=%s WHERE id=%s", (st, sid, ret, resumo, motivo, j["id"]))
        # 2. retomar pausados cujo reset passou
        for j in jobs(con, "status='pausado_limite' AND retomar_em <= now()"):
            if not j["session_id"]:
                j["session_id"] = achar_session(j)
            if not j["session_id"]:
                logar("sem session_id para retomar; volta para a fila", j["nome"], "job_sem_sessao", "aviso", dry)
                if not dry:
                    con.execute("UPDATE ops.fila_jobs SET status='fila' WHERE id=%s", (j["id"],))
                continue
            disparar(con, j, dry, retomada=True)
        # 3. iniciar novos
        bloqueio_limite = con.execute("SELECT 1 FROM ops.fila_jobs WHERE status='pausado_limite' AND retomar_em > now() LIMIT 1").fetchone()
        if bloqueio_limite:
            logar("limite do Max ativo: não inicio novos", None, dry=dry) if jobs(con, "status='fila'") else None
        else:
            rodando = jobs(con, "status='rodando'")
            n_max = sum(1 for r in rodando if r["motor"] == "max")
            for j in jobs(con, "status='fila'"):
                if j["motor"] == "max" and n_max >= int(c["MAX_CONCORRENCIA"]):
                    continue
                if j["depende_de"]:
                    d = con.execute("SELECT status FROM ops.fila_jobs WHERE nome=%s", (j["depende_de"],)).fetchone()
                    if not d or d[0] != "concluido":
                        continue
                if mem_disp_gb() < float(c["MEM_MIN_GB"]):
                    logar(f"memória baixa ({mem_disp_gb():.1f} GB): espero", None, dry=dry)
                    break
                disparar(con, j, dry)
                if j["motor"] == "max":
                    n_max += 1
                if dry:
                    continue
                break  # um por tick: a memória só aparece depois que o job sobe
        if not dry:
            escrever_status(con)


def escrever_status(con):
    rows = jobs(con, "true")
    L = [f"# Fila de jobs ({datetime.now(TZ):%d/%m %H:%M})", "", "| pri | nome | status | prazo | detalhe |", "|---|---|---|---|---|"]
    for j in rows:
        det = j["obs"] or ""
        if j["status"] == "pausado_limite" and j["retomar_em"]:
            det = f"retoma {j['retomar_em'].astimezone(TZ):%d/%m %H:%M}"
        if j["status"] == "fila" and j["depende_de"]:
            det = f"depende de {j['depende_de']}"
        pz = j["prazo"].astimezone(TZ).strftime("%d/%m %H:%M") if j["prazo"] else "-"
        L.append(f"| {j['prioridade']} | {j['nome']} | {j['status']} | {pz} | {det} |")
    STATUS_MD.write_text("\n".join(L) + "\n")


def cmd_add(a):
    with psycopg.connect(DB, autocommit=True) as con:
        brief = a.brief
        log = a.log or str(REF / (a.nome + ".log"))
        con.execute("INSERT INTO ops.fila_jobs (nome,brief,log,modelo,motor,prioridade,prazo,depende_de) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                    (a.nome, brief, log, a.modelo, a.motor, a.prioridade, (a.prazo + " -03") if a.prazo else None, a.depende_de))
    print("ok:", a.nome)


def cmd_list(_):
    with psycopg.connect(DB, autocommit=True) as con:
        for j in jobs(con, "true"):
            extra = f" retoma {j['retomar_em'].astimezone(TZ):%d/%m %H:%M}" if j["retomar_em"] else ""
            pz = j["prazo"].astimezone(TZ).strftime("%d/%m %H:%M") if j["prazo"] else "-"
            print(f"{j['prioridade']} {j['nome']:<34} {j['status']:<15} prazo {pz} {('dep:' + j['depende_de']) if j['depende_de'] else ''}{extra}")


def cmd_set(a, status, extra=""):
    with psycopg.connect(DB, autocommit=True) as con:
        r = con.execute(f"UPDATE ops.fila_jobs SET status=%s{extra} WHERE nome=%s RETURNING id", (status, a.nome)).fetchone()
        print("ok" if r else "não achei", a.nome)
        if r:
            registrar("fila", f"job_{status}", "info", f"{a.nome}: {status} (manual)", ref=a.nome)


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="c", required=True)
    p = sp.add_parser("add")
    p.add_argument("nome"); p.add_argument("brief")
    p.add_argument("--modelo", default="opus"); p.add_argument("--motor", default="max")
    p.add_argument("--prioridade", type=int, default=5); p.add_argument("--prazo"); p.add_argument("--depende-de"); p.add_argument("--log")
    sp.add_parser("list")
    p = sp.add_parser("tick"); p.add_argument("--dry-run", action="store_true")
    for n in ("cancel", "retomar"):
        sp.add_parser(n).add_argument("nome")
    a = ap.parse_args()
    if a.c == "add":
        cmd_add(a)
    elif a.c == "list":
        cmd_list(a)
    elif a.c == "tick":
        tick(a.dry_run)
    elif a.c == "cancel":
        cmd_set(a, "cancelado")
    else:  # retomar: volta a 'pausado_limite' com reset vencido (ou 'fila' se não tem sessão)
        cmd_set(a, "pausado_limite", ", retomar_em=now()")


if __name__ == "__main__":
    main()
