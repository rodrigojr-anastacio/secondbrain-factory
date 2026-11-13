#!/usr/bin/env python
"""Fila de jobs `claude -p` em ops.fila_jobs: dispara, acompanha e retoma sozinho (tick a cada 3 min pelo timer fabrica-fila).

Uso:
  fila.sh add <nome> <brief> [--modelo opus|sonnet] [--motor max|api] [--prioridade N] [--prazo 'YYYY-MM-DD HH:MM'] [--depende-de nome] [--log caminho]
  fila.sh list | tick [--dry-run] | cancel <nome> | retomar <nome> | capacidade [--backfill]
Config opcional: ~/.config/fabrica/fila.env (MAX_CONCORRENCIA=2, MEM_MIN_GB=2.5).
Nunca mata processos. Lock (flock) impede dois ticks juntos.
"""
import argparse
from decimal import Decimal
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
PROJ = HOME / ".claude/projects"
CAP_MD = REPO / "conhecimento/capacidade-fila.md"
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
        cmd = [str(Path.home() / ".local/bin/claude"), "-p", prompt, "--model", job["modelo"], "--max-turns", "400", "--allowedTools", ",".join(TOOLS)]
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


# ---------- capacidade: amostras, tokens, janelas do Max ----------
def cg_dir(unit):
    cg = subprocess.run(["systemctl", "--user", "show", f"{unit}.scope", "-p", "ControlGroup", "--value"], capture_output=True, text=True).stdout.strip()
    d = Path(f"/sys/fs/cgroup{cg}") if cg else None
    return d if d and d.exists() else None


def _num(path):
    try:
        return float(Path(path).read_text().split()[0])
    except (OSError, ValueError, IndexError):
        return None


def cg_medidas(unit):
    """(mem_mb, pico_mb, cpu_seg, anon_mb, oom_kill) do scope; None onde não existe."""
    d = cg_dir(unit)
    if not d:
        return None, None, None, None, None
    mem, pico = _num(d / "memory.current"), _num(d / "memory.peak")
    anon, oom = None, None
    try:
        for ln in (d / "memory.stat").read_text().splitlines():
            if ln.startswith("anon "):
                anon = int(ln.split()[1]) / 1048576
        for ln in (d / "memory.events").read_text().splitlines():
            if ln.startswith("oom_kill "):
                oom = int(ln.split()[1])
    except (OSError, ValueError):
        pass
    cpu = None
    try:
        for ln in (d / "cpu.stat").read_text().splitlines():
            if ln.startswith("usage_usec"):
                cpu = int(ln.split()[1]) / 1e6
    except OSError:
        pass
    return (mem / 1048576 if mem is not None else None, pico / 1048576 if pico is not None else None, cpu, anon, oom)


def meminfo_mb():
    m = {}
    for ln in open("/proc/meminfo"):
        k, v = ln.split(":", 1)
        m[k] = int(v.split()[0]) / 1024
    return m


def amostrar(con, rodando):
    """Uma linha por job rodando + uma da VPS. Nunca derruba o tick."""
    try:
        mi = meminfo_mb()
        st = os.statvfs(HOME)
        livre = st.f_bavail * st.f_frsize / 1e9
        con.execute("INSERT INTO ops.fila_amostras (job_nome,mem_disponivel_mb,swap_usado_mb,load1,jobs_rodando,disco_livre_gb) VALUES (NULL,%s,%s,%s,%s,%s)",
                    (mi["MemAvailable"], mi["SwapTotal"] - mi["SwapFree"], os.getloadavg()[0], len(rodando), livre))
        for j in rodando:
            if not j["unit"]:
                continue
            mem, pico, cpu, anon, oom = cg_medidas(j["unit"])
            if mem is None:
                continue
            con.execute("INSERT INTO ops.fila_amostras (job_nome,mem_mb,mem_pico_mb,cpu_seg,mem_anon_mb,oom_kill) VALUES (%s,%s,%s,%s,%s,%s)", (j["nome"], mem, pico, cpu, anon, oom))
            # pico/cpu do scope são cumulativos desde a criação: guarda o maior já visto no job
            con.execute("UPDATE ops.fila_jobs SET mem_pico_mb=GREATEST(COALESCE(mem_pico_mb,0),%s), cpu_seg=GREATEST(COALESCE(cpu_seg,0),%s), mem_anon_pico_mb=GREATEST(COALESCE(mem_anon_pico_mb,0),%s), oom_kill=GREATEST(COALESCE(oom_kill,0),%s) WHERE id=%s",
                        (int(pico or mem), cpu or 0, int(anon or 0), int(oom or 0), j["id"]))
    except Exception as e:  # noqa: BLE001
        print(f"[amostrar] aviso: {type(e).__name__}: {e}")


def _preco():
    from anthropic_api import custo_usd
    return custo_usd


def achar_jsonl(session_id):
    if not session_id:
        return None
    r = list(PROJ.glob(f"*/{session_id}.jsonl"))
    return r[0] if r else None


def somar_jsonl(path, ini=None, fim=None):
    """Soma usage das respostas do assistente (dedup por message.id; a última linha do id vale). → dict com tokens, custo, t0, t1."""
    import json
    custo_usd = _preco()
    msgs = {}
    t0 = t1 = None
    try:
        with open(path, errors="replace") as f:
            for ln in f:
                if '"usage"' not in ln:
                    continue
                try:
                    o = json.loads(ln)
                except ValueError:
                    continue
                m = o.get("message")
                if not isinstance(m, dict) or not m.get("usage") or o.get("type") != "assistant":
                    continue
                ts = o.get("timestamp")
                try:
                    t = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except (AttributeError, ValueError):
                    continue
                if (ini and t < ini) or (fim and t > fim):
                    continue
                msgs[m.get("id") or o.get("uuid")] = (m.get("model") or "opus", m["usage"], t)
    except OSError:
        pass
    r = dict(ent=0, sai=0, cl=0, ce=0, custo=0.0, n=len(msgs), t0=None, t1=None)
    for mod, u, t in msgs.values():
        if mod.startswith("<") or mod == "synthetic":
            continue
        r["ent"] += u.get("input_tokens") or 0
        r["sai"] += u.get("output_tokens") or 0
        r["cl"] += u.get("cache_read_input_tokens") or 0
        r["ce"] += u.get("cache_creation_input_tokens") or 0
        r["custo"] += custo_usd(mod, u)
        r["t0"] = t if r["t0"] is None or t < r["t0"] else r["t0"]
        r["t1"] = t if r["t1"] is None or t > r["t1"] else r["t1"]
    return r


def atualizar_tokens(con, job_id, session_id):
    p = achar_jsonl(session_id)
    if not p:
        return
    r = somar_jsonl(p)
    con.execute("UPDATE ops.fila_jobs SET tokens_entrada=%s,tokens_saida=%s,tokens_cache_leitura=%s,tokens_cache_escrita=%s,custo_equivalente_usd=%s WHERE id=%s",
                (r["ent"], r["sai"], r["cl"], r["ce"], round(r["custo"], 4), job_id))


def fechar_metricas(con, j, sid, st, ret, cauda):
    """Ao terminar/pausar: duração rodando, tokens e, se limite, janela do Max."""
    try:
        con.execute("UPDATE ops.fila_jobs SET duracao_seg=duracao_seg+COALESCE(EXTRACT(EPOCH FROM now()-iniciado_em),0) WHERE id=%s", (j["id"],))
        atualizar_tokens(con, j["id"], sid)
        if st == "pausado_limite":
            con.execute("UPDATE ops.fila_jobs SET limites_batidos=limites_batidos+1 WHERE id=%s", (j["id"],))
            registrar_janela(con, j["nome"], ret, cauda)
    except Exception as e:  # noqa: BLE001
        print(f"[metricas] aviso: {type(e).__name__}: {e}")


def registrar_janela(con, nome, reseta, cauda):
    """Soma tudo que os `claude` da VPS gastaram na janela que acabou de estourar."""
    agora = datetime.now(timezone.utc)
    semanal = bool(re.search(r"weekly|week", cauda or "", re.I))
    reset_real = (reseta - timedelta(minutes=2)) if reseta else agora
    ini = reset_real - (timedelta(days=7) if semanal else timedelta(hours=5))
    tot = dict(ent=0, sai=0, cl=0, ce=0, custo=0.0)
    n = 0
    for p in PROJ.rglob("*.jsonl"):
        try:
            if p.stat().st_mtime < ini.timestamp():
                continue
        except OSError:
            continue
        r = somar_jsonl(p, ini, agora)
        if r["n"]:
            n += 1
            for k in tot:
                tot[k] += r[k]
    con.execute("INSERT INTO ops.max_janelas (detectado_em,reseta_em,tipo,job_nome,janela_ini,tokens_entrada,tokens_saida,tokens_cache_leitura,tokens_cache_escrita,custo_equivalente_usd,sessoes)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                (agora, reseta, "semanal" if semanal else "5h", nome, ini, tot["ent"], tot["sai"], tot["cl"], tot["ce"], round(tot["custo"], 4), n))


def tipo_job(nome):
    return "produção de vídeo" if nome.startswith(("lote-", "producao", "video")) or re.search(r"\d{3}", nome) else "pesquisa/outros"


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
        if not dry:
            amostrar(con, jobs(con, "status='rodando'"))
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
                if not dry:
                    fechar_metricas(con, j, sid, st, None, "")
                disparar(con, j, dry, retomada=True)
                continue
            resumo = ler_log(j["log"], 600).strip()
            if not dry:
                fechar_metricas(con, j, sid, st, ret, ler_log(j["log"], 1500))
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



# ---------- relatório de capacidade ----------
def historico_sessoes():
    """Sessões `claude -p Execute o brief …` (jsonl) → lista de dicts com nome do brief, tokens, custo, duração."""
    import json
    out = []
    for p in PROJ.rglob("*.jsonl"):
        try:
            with open(p, errors="replace") as f:
                prim = ""
                for ln in f:
                    if '"type":"user"' in ln:
                        o = json.loads(ln)
                        c = o.get("message", {}).get("content")
                        prim = c if isinstance(c, str) else json.dumps(c)
                        break
        except (OSError, ValueError):
            continue
        m = re.search(r"brief (?:em )?(\S*?BRIEF-([^\s/]+?)\.md)", prim) or re.search(r"Execute o brief em (\S+)", prim)
        if not m:
            continue
        brief = m.group(2) if m.lastindex and m.lastindex >= 2 else os.path.basename(m.group(1))
        r = somar_jsonl(p)
        if not r["n"]:
            continue
        r["nome"] = brief
        r["sid"] = p.stem
        r["dur_min"] = (r["t1"] - r["t0"]).total_seconds() / 60
        out.append(r)
    return sorted(out, key=lambda r: r["t0"])


def backfill(con):
    n = 0
    for j in jobs(con, "status IN ('concluido','pausado_limite','bloqueado','falhou') AND tokens_entrada IS NULL"):
        sid = j["session_id"] or achar_session(j)
        if sid:
            con.execute("UPDATE ops.fila_jobs SET session_id=%s WHERE id=%s", (sid, j["id"]))
            atualizar_tokens(con, j["id"], sid)
            if j["iniciado_em"] and j["terminado_em"]:
                con.execute("UPDATE ops.fila_jobs SET duracao_seg=GREATEST(duracao_seg,%s) WHERE id=%s", ((j["terminado_em"] - j["iniciado_em"]).total_seconds(), j["id"]))
            n += 1
    return n


def fmt_tok(n):
    n = n or 0
    return f"{n / 1e6:.1f}M" if n >= 1e6 else f"{n / 1e3:.0f}k"


def fmb(x):
    return "-" if x is None else f"{float(x):.0f} MB"


def cmd_capacidade(a):
    ago = datetime.now(TZ)
    L = [f"# Capacidade da fila ({ago:%d/%m/%Y %H:%M})", "", "Gerado por `tools/fila.sh capacidade` (medições de `ops.fila_amostras`, `ops.fila_jobs`, `ops.max_janelas`). Custo-equivalente = preço de lista da API (`anthropic_api.PRECOS`), não o que o Max cobra.", ""]
    with psycopg.connect(DB, autocommit=True) as con:
        bf = backfill(con) if a.backfill else 0
        if a.backfill:
            L.append(f"_Backfill: {bf} job(s) da fila preenchidos a partir dos jsonl._\n")
        mi = meminfo_mb()
        total = mi["MemTotal"]
        # --- VPS
        L += ["## VPS (RAM / CPU)", ""]
        v = [float(x) if isinstance(x, Decimal) else x for x in con.execute("SELECT count(*),min(ts),max(jobs_rodando),min(mem_disponivel_mb),max(swap_usado_mb),max(load1),avg(load1),min(disco_livre_gb) FROM ops.fila_amostras WHERE job_nome IS NULL").fetchone()]
        L.append(f"RAM total {total / 1024:.1f} GB, 2 vCPU. Amostras da VPS: {v[0]}" + (f" desde {v[1].astimezone(TZ):%d/%m %H:%M}" if v[1] else "") + ".")
        if v[0]:
            L.append(f"Pico com {v[2]} job(s) simultâneo(s): RAM disponível mínima {v[3] / 1024:.1f} GB, swap máx {v[4] / 1024:.1f} GB, load1 máx {v[5]:.1f} (média {v[6]:.1f}), disco livre mín {v[7]:.0f} GB.")
        rows = con.execute("""SELECT job_nome, count(*), avg(mem_mb), max(GREATEST(mem_mb,COALESCE(mem_pico_mb,0))), max(cpu_seg), min(ts), max(ts), avg(mem_anon_mb), max(mem_anon_mb), max(oom_kill)
                              FROM ops.fila_amostras WHERE job_nome IS NOT NULL GROUP BY 1 ORDER BY 1""").fetchall()
        medias, picos = [], []
        if rows:
            L += ["", "| job | amostras | anon média | anon pico | RAM total pico (c/ cache) | oom_kill | CPU (s) | CPU média (núcleos) |", "|---|---|---|---|---|---|---|---|"]
            for n, c, mm, mp, cpu, t0, t1, am, ap, ok in rows:
                dt = max((t1 - t0).total_seconds(), 1)
                # CPU média: delta do cumulativo / tempo amostrado
                c0 = con.execute("SELECT cpu_seg FROM ops.fila_amostras WHERE job_nome=%s ORDER BY ts LIMIT 1", (n,)).fetchone()[0] or 0
                nuc = f"{(float(cpu or 0) - float(c0)) / dt:.2f}" if c > 1 else "-"
                L.append(f"| {n} | {c} | {fmb(am)} | {fmb(ap)} | {mp:.0f} MB | {ok if ok is not None else '-'} | {cpu or 0:.0f} | {nuc} |")
                if ap is not None:  # dimensiona pelo anon (cache é recuperável); sem anon, cai no total
                    medias.append(float(am)); picos.append(float(ap))
                else:
                    medias.append(float(mm)); picos.append(float(mp))
        if picos:
            pico_medio = sum(picos) / len(picos)
            base = max(total - (v[3] if v[0] and v[2] else mi["MemAvailable"]) - sum(m for m in medias[-int(v[2] or 1):]), 0) if v[0] else 0
            cabem = int(max(total - 1536 - base, 0) // pico_medio)
            L += ["", f"Pico médio por job {pico_medio:.0f} MB (anon = memória não recuperável; o cache de arquivo do scope, que infla `memory.current`/`peak`, o kernel libera sob pressão). Base da VPS fora dos jobs ≈ {base / 1024:.1f} GB. **Cabem ~{cabem} job(s) com folga de 1,5 GB** (limite técnico: `MemoryMax=3500M` por job; CPU de 2 vCPU limita render a 1 por vez)."]
        else:
            L += ["", "Sem amostras por job ainda (próximos ticks preenchem)."]
        # --- Max
        L += ["", "## Claude Max (limite de 5 h / semanal)", ""]
        jw = con.execute("SELECT detectado_em,reseta_em,tipo,job_nome,tokens_entrada,tokens_saida,tokens_cache_leitura,tokens_cache_escrita,custo_equivalente_usd,sessoes FROM ops.max_janelas ORDER BY detectado_em").fetchall()
        if jw:
            L += ["| detectado | reseta | tipo | por | tokens in/out/cache | custo-eq. US$ | sessões |", "|---|---|---|---|---|---|---|"]
            for d, r, t, jn, e, s_, cl, ce, c, ns in jw:
                L.append(f"| {d.astimezone(TZ):%d/%m %H:%M} | {r.astimezone(TZ):%d/%m %H:%M} | {t} | {jn} | {fmt_tok(e)}/{fmt_tok(s_)}/{fmt_tok(cl)}+{fmt_tok(ce)} | {c:.0f} | {ns} |")
            c5 = [float(x[8]) for x in jw if x[2] == "5h"]
            if c5:
                L.append(f"\nCapacidade medida por janela de 5 h: ~US$ {sum(c5) / len(c5):.0f} custo-equivalente (n={len(c5)}, mín {min(c5):.0f}, máx {max(c5):.0f}).")
        else:
            L.append("Nenhum limite batido desde o início da medição (a coleta registra cada \"hit your … limit\"); capacidade ainda desconhecida.")
        hist = historico_sessoes()
        fj = jobs(con, "true")
        L += ["", "Consumo por job da fila (preço de lista equivalente):", "", "| job | tipo | status | duração | tokens in/out/cache | custo-eq. US$ | limites |", "|---|---|---|---|---|---|---|"]
        tipos = {}
        for j in fj:
            c = con.execute("SELECT custo_equivalente_usd,duracao_seg,tokens_entrada,tokens_saida,tokens_cache_leitura,tokens_cache_escrita,limites_batidos,mem_pico_mb FROM ops.fila_jobs WHERE id=%s", (j["id"],)).fetchone()
            if c[0] is None:
                continue
            L.append(f"| {j['nome']} | {tipo_job(j['nome'])} | {j['status']} | {float(c[1]) / 60:.0f} min | {fmt_tok(c[2])}/{fmt_tok(c[3])}/{fmt_tok(c[4])}+{fmt_tok(c[5])} | {float(c[0]):.1f} | {c[6]} |")
            if j["status"] == "concluido":
                tipos.setdefault(tipo_job(j["nome"]), []).append(float(c[0]))
        L += ["", "Histórico dos jobs `claude -p` anteriores (jsonl; backfill; duração = 1ª a última mensagem, inclui pausas):", "", "| brief | tokens in/out/cache | custo-eq. US$ | duração |", "|---|---|---|---|"]
        for r in hist:
            L.append(f"| {r['nome']} | {fmt_tok(r['ent'])}/{fmt_tok(r['sai'])}/{fmt_tok(r['cl'])}+{fmt_tok(r['ce'])} | {r['custo']:.1f} | {r['dur_min']:.0f} min |")
            if not any(x == r["nome"] for x in [j["nome"] for j in fj]):
                tipos.setdefault(tipo_job(r["nome"].lower()) if re.search(r"\d{3}|historia|dossie|lote|video", r["nome"].lower()) else "pesquisa/outros", []).append(r["custo"])
        if tipos:
            L += ["", "Consumo médio por tipo de job: " + "; ".join(f"{k}: US$ {sum(v_) / len(v_):.1f} (n={len(v_)})" for k, v_ in tipos.items()) + "."]
            if jw and c5 and "produção de vídeo" in tipos:
                m = sum(tipos["produção de vídeo"]) / len(tipos["produção de vídeo"])
                L.append(f"Vídeos completos por janela de 5 h ≈ {sum(c5) / len(c5) / m:.1f} (capacidade média ÷ custo médio de produção).")
        # --- API
        L += ["", "## API Anthropic (mês)", ""]
        try:
            from anthropic_api import TETOS, gasto_mes
            for g, (teto, _) in TETOS.items():
                gm = gasto_mes(g)
                L.append(f"- {g}: US$ {gm:.2f} / {teto:.0f} ({gm / teto * 100:.0f}%)")
        except Exception as e:  # noqa: BLE001
            L.append(f"(não consegui ler: {type(e).__name__})")
        # --- custo por vídeo
        L += ["", "## Custo por vídeo (financas.consumo, direto, US$)", ""]
        cv = con.execute("""SELECT c.fornecedor, count(DISTINCT c.ref_id), sum(c.custo), sum(c.custo)/NULLIF(count(DISTINCT c.ref_id),0)
                            FROM financas.consumo c WHERE c.ref_tipo='video' AND c.fornecedor IN ('Runpod','fal.ai','Fish Audio','OpenAI') GROUP BY 1 ORDER BY 1""").fetchall()
        if not cv:
            cv = con.execute("""SELECT fornecedor, count(DISTINCT ref_id), sum(custo), sum(custo)/NULLIF(count(DISTINCT ref_id),0)
                                FROM financas.consumo WHERE ref_id IS NOT NULL AND fornecedor IN ('Runpod','fal.ai','Fish Audio','OpenAI') GROUP BY 1 ORDER BY 1""").fetchall()
        L += ["| fornecedor | vídeos | total | por vídeo |", "|---|---|---|---|"] + [f"| {f} | {n} | {float(t):.2f} | {float(pv or 0):.2f} |" for f, n, t, pv in cv]
        # --- recomendação
        L += ["", "## Recomendação", ""]
        nmed = len(rows)
        hip = " **Hipótese** (menos de 4 jobs medidos)." if nmed < 4 else ""
        atual = cfg()["MAX_CONCORRENCIA"]
        if picos:
            sug = max(1, min(cabem, 3))
            L.append(f"- `MAX_CONCORRENCIA`: manter {atual}; RAM comporta ~{cabem}, mas o Max (cota) e o render limitam antes. Subir para {sug} só se não houver `pausado_limite` nas janelas.{hip}")
        else:
            L.append(f"- `MAX_CONCORRENCIA`: manter {atual} até haver amostras.{hip}")
        L.append("- Enviar à API (`--motor api`, grupo dev/rotinas) o que é curto e barato por job (pesquisa, garimpo, QA); manter no Max os jobs longos de produção, que têm cache alto e custo-equivalente grande." + hip)
        L.append("- Se uma janela de 5 h estourar com 2 jobs, o fila.py já pausa e retoma; o sinal de que há folga é a ausência de `pausado_limite` por 24 h.")
    CAP_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="c", required=True)
    p = sp.add_parser("add")
    p.add_argument("nome"); p.add_argument("brief")
    p.add_argument("--modelo", default="opus"); p.add_argument("--motor", default="max")
    p.add_argument("--prioridade", type=int, default=5); p.add_argument("--prazo"); p.add_argument("--depende-de"); p.add_argument("--log")
    sp.add_parser("list")
    p = sp.add_parser("capacidade"); p.add_argument("--backfill", action="store_true")
    p = sp.add_parser("tick"); p.add_argument("--dry-run", action="store_true")
    for n in ("cancel", "retomar"):
        sp.add_parser(n).add_argument("nome")
    a = ap.parse_args()
    if a.c == "add":
        cmd_add(a)
    elif a.c == "list":
        cmd_list(a)
    elif a.c == "capacidade":
        cmd_capacidade(a)
    elif a.c == "tick":
        tick(a.dry_run)
    elif a.c == "cancel":
        cmd_set(a, "cancelado")
    else:  # retomar: volta a 'pausado_limite' com reset vencido (ou 'fila' se não tem sessão)
        cmd_set(a, "pausado_limite", ", retomar_em=now()")


if __name__ == "__main__":
    main()
