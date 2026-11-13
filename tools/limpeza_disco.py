#!/usr/bin/env python3
"""Limpeza de disco da VPS (só classe A: regenerável). Uso: limpeza_disco.py [--dry-run]

Regras (brief 13/11/2026):
- node_modules e out/partes (com out/video.mp4 presente) e imagens-orig (com imagens/ presente)
  de vídeos com status publicado/arquivado em youtube.videos;
- ~/cache/tmp, ~/cache/mwraw-*, ~/cache/rcl-* (> 2 dias), ~/render-midway;
- ~/.npm/_cacache, ~/.cache/pip, `uv cache prune`; logs de referencias/ e relatorios/ > 30 dias.
Nunca toca: pastas ativas na fila (ops.fila_jobs), pastas protegidas, classe B (video.mp4, áudios,
~/.hermes, jsonl do Claude), entrega/, ~/.segredos, repositórios git versionados.
"""
import argparse, datetime as dt, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

HOME = Path.home().resolve()
FAB = HOME / "workspace" / "fabrica-youtube"
REL = HOME / "workspace" / "relatorios" / "limpeza"
DIAS_TMP = 2
DIAS_LOG = 30
RECENTE_H = 6  # pasta de vídeo mexida há menos que isso = em uso, não toca

# Classe C fixa (brief). Dinâmica: pastas citadas por jobs ativos da fila.
PROTEGIDOS_FIXOS = [
    "canais/dossie-es/videos/007-ss", "canais/dossie-es/videos/008-",
    "canais/lugares-guerra-en/videos/002-", "canais/lugares-guerra-en/videos/003-",
    "canais/historia-ptbr/videos/008-", "canais/historia-ptbr/videos/009-",
    "pesquisa/canal-clima-2026-11/longo-03", "pesquisa/canal-clima-2026-11/longo-04",
]


def psql(sql):
    r = subprocess.run(["psql", "-d", "vida", "-At", "-F", "\t", "-c", sql], capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr.strip())
    return [l.split("\t") for l in r.stdout.splitlines() if l]


def du(p):
    r = subprocess.run(["du", "-sb", str(p)], capture_output=True, text=True)
    try:
        return int(r.stdout.split()[0])
    except Exception:
        return 0


def seguro(p: Path):
    """Só caminhos dentro de ~ (e fora do próprio ~, .segredos, .claude, .git)."""
    try:
        rp = p.resolve()
    except Exception:
        return False
    if rp == HOME or HOME not in rp.parents:
        return False
    partes = rp.relative_to(HOME).parts
    return not (partes[0] in (".segredos", ".claude", ".ssh", ".hermes") or ".git" in partes)


def idade_dias(p: Path):
    return (time.time() - p.stat().st_mtime) / 86400


def recente(d: Path):
    """Algo na pasta (nível 1 e out/) mexido nas últimas RECENTE_H horas."""
    lim = time.time() - RECENTE_H * 3600
    for base in (d, d / "out"):
        if not base.is_dir():
            continue
        for e in base.iterdir():
            if e.name == "node_modules":
                continue
            try:
                if e.stat().st_mtime > lim:
                    return True
            except OSError:
                pass
    return False


def protegidos():
    pats = list(PROTEGIDOS_FIXOS)
    # jobs ativos: nome tipo lote-historia-008-franca-e1 -> canal-palavra + NNN
    try:
        for nome, brief in psql("select nome, brief from ops.fila_jobs where status not in ('concluido','cancelado','ok','falhou','erro')"):
            m = re.search(r"-(\d{3})-([a-z0-9-]+?)(?:-e[12])?$", nome)
            if m:
                pats.append(f"{m.group(1)}-{m.group(2)}")
                pats.append(f"{m.group(1)}-")  # conservador: qualquer pasta com mesmo número
            for mm in re.findall(r"canais/[\w-]+/videos/[\w-]+|pesquisa/[\w/-]+", brief or ""):
                pats.append(mm)
    except Exception as e:
        print("aviso: fila indisponível:", e, file=sys.stderr)
        return None
    return pats


def eh_protegido(d: Path, pats):
    rel = str(d.relative_to(FAB))
    base = d.name
    for p in pats:
        if rel.startswith(p) or base.startswith(p) or (re.fullmatch(r"\d{3}-", p) and base.startswith(p)):
            return True
    return False


class Limpeza:
    def __init__(self, dry):
        self.dry = dry
        self.vistos = set()
        self.itens = []  # (tipo, caminho, bytes)

    def apagar(self, tipo, p: Path):
        if not seguro(p) or not p.exists() or str(p) in self.vistos:
            return
        self.vistos.add(str(p))
        n = du(p)
        if not self.dry:
            if p.is_dir() and not p.is_symlink():
                shutil.rmtree(p, ignore_errors=True)
            else:
                p.unlink(missing_ok=True)
        self.itens.append((tipo, str(p), n))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    antes = shutil.disk_usage(HOME)
    L = Limpeza(a.dry_run)
    pats = protegidos()

    # --- vídeos publicados/arquivados
    if pats is None:
        print("sem acesso à fila: pulando regras por vídeo", file=sys.stderr)
    else:
        for pasta, status in psql("select pasta, status from youtube.videos where pasta is not null and status in ('publicado','arquivado')"):
            d = (FAB / pasta)
            if not d.is_dir() or not seguro(d) or eh_protegido(d, pats) or recente(d):
                continue
            L.apagar("node_modules", d / "node_modules")
            if (d / "out" / "video.mp4").is_file():
                L.apagar("out/partes", d / "out" / "partes")
            if (d / "imagens").is_dir() and any((d / "imagens").iterdir()):
                L.apagar("imagens-orig", d / "imagens-orig")

    # --- ~/cache
    c = HOME / "cache"
    if c.is_dir():
        for e in c.glob("mwraw-*"):
            L.apagar("cache mwraw/rcl", e)
        for e in c.glob("rcl-*"):
            if idade_dias(e) > DIAS_TMP:
                L.apagar("cache mwraw/rcl", e)
        t = c / "tmp"
        if t.is_dir():
            for e in t.iterdir():
                if idade_dias(e) > DIAS_TMP:
                    L.apagar("cache/tmp", e)
    L.apagar("render-midway", HOME / "render-midway")

    # --- caches de ferramentas
    for p in (HOME / ".npm" / "_cacache", HOME / ".npm" / "_npx", HOME / ".cache" / "pip"):
        L.apagar("caches (npm/pip)", p)
    uv = shutil.which("uv") or str(HOME / ".local/bin/uv")
    if os.path.exists(uv):
        antes_uv = du(HOME / ".cache" / "uv")
        if not a.dry_run:
            subprocess.run([uv, "cache", "prune"], capture_output=True)
        L.itens.append(("uv cache prune", str(HOME / ".cache/uv"), 0 if a.dry_run else max(0, antes_uv - du(HOME / ".cache" / "uv"))))

    # --- logs antigos
    for base in (HOME / "workspace" / "referencias", HOME / "workspace" / "relatorios", FAB / "tools" / "rotinas"):
        if base.is_dir():
            for f in base.rglob("*.log"):
                if f.is_file() and idade_dias(f) > DIAS_LOG:
                    L.apagar("logs > 30 dias", f)

    depois = shutil.disk_usage(HOME)
    pct = round(100 * depois.used / depois.total, 1)
    por_tipo = {}
    for t, _, n in L.itens:
        por_tipo[t] = por_tipo.get(t, 0) + n
    total = sum(por_tipo.values())
    gb = lambda n: f"{n/1e9:.2f} GB"
    hoje = dt.date.today().isoformat()
    alerta = pct > 85 and not a.dry_run
    rel = [f"# Limpeza de disco {hoje}" + (" (dry-run)" if a.dry_run else ""), "",
           f"Disco antes: {gb(antes.used)} usados de {gb(antes.total)} ({100*antes.used/antes.total:.1f}%)",
           f"Disco depois: {gb(depois.used)} ({pct}%)",
           f"{'Apagaria' if a.dry_run else 'Liberado'}: {gb(total)}", ""]
    if alerta:
        rel += [f"**ALERTA: disco em {pct}% depois da limpeza (> 85%).** Classe B precisa de decisão do Rodrigo.", ""]
    rel += ["| Tipo | GB |", "|---|---|"] + [f"| {t} | {n/1e9:.2f} |" for t, n in sorted(por_tipo.items(), key=lambda x: -x[1])]
    rel += ["", "## Itens"] + [f"- {t}: `{p}` ({n/1e6:.0f} MB)" for t, p, n in L.itens]
    REL.mkdir(parents=True, exist_ok=True)
    out = REL / (hoje + ("-dry" if a.dry_run else "") + ".md")
    out.write_text("\n".join(rel) + "\n")
    print("\n".join(rel[:14]))
    print("relatório:", out)

    if not a.dry_run:
        det = json.dumps({"liberado_bytes": total, "disco_pct": pct, "por_tipo": por_tipo})
        sev = "erro" if alerta else "info"
        msg = (f"ALERTA disco {pct}% após limpeza" if alerta else f"limpeza de disco: {gb(total)} liberados, disco {pct}%")
        try:
            tipo = "disco_alto" if alerta else "limpeza"
            sql = (f"insert into ops.event_log(origem,tipo,severidade,mensagem,detalhes) "
                   f"values ('limpeza_disco','{tipo}','{sev}',$m${msg}$m$,$d${det}$d$::jsonb)")
            subprocess.run(["psql", "-d", "vida", "-v", "ON_ERROR_STOP=1", "-c", sql], check=True, capture_output=True)
        except Exception as e:
            print("aviso: event_log falhou:", e, file=sys.stderr)


if __name__ == "__main__":
    main()
