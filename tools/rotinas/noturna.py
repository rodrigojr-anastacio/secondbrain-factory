#!/usr/bin/env python
"""Fábrica noturna (14/11/2026, decisão do Rodrigo): 4 vídeos por canal por semana, produzidos de noite.

Calendário: publica seg, qua, sex + 1 no fim de semana (sábado numa semana, domingo na outra; tools/rotinas/backlog.py).
A produção roda na NOITE ANTERIOR a cada publicação (20:00): o timer fabrica-noturna dispara dom/ter/qui/sex/sáb e
o script só trabalha se amanhã for dia de publicação (sex só na semana de sábado; sáb só na semana de domingo).

Subcomandos (tools/rotinas/noturna.sh <sub> …):
  planejar [--noite AAAA-MM-DD] [--dry-run] [--forcar] [--sem-telegram] [--canal X]
        20:00. Pré-voo (fal/Fish/Runpod, Max semanal, Drive, disco) → pauta: por canal, o 1º item do backlog vivo
        para a 1ª vaga do calendário (amanhã ou, se amanhã já tem vídeo pronto, a próxima vaga em até 7 dias) →
        youtube.videos + pasta + briefs ETAPA1/2 (modelos BRIEF-lote-MODELO-*) → fila (e1 Opus, e2 Sonnet
        --depende-de, prazo 07:00) → backlog em_producao. Falta de recurso: produz o que couber, na ordem do
        calendário, e avisa no Telegram.
  vigia [--sem-telegram]
        a cada 10 min (timer fabrica-noturna-vigia): sincroniza status; embalagem reprovada no crivo (BLOQUEIO.md)
        → descarta o tema e põe o próximo do backlog NA MESMA NOITE (1×, até LIMITE_SUBSTITUTO); vídeo pronto →
        entrega no Drive (tools/entregar_drive.sh; Em Relevo por rclone direto) se houver espaço, senão fica na
        fila de entrega e avisa 1× no Telegram.
  manha [--noite AAAA-MM-DD] [--sem-telegram] [--dry-run]
        07:30 (timer fabrica-noturna-manha): resumo curto por canal no Telegram (pronto?, título aprovado,
        data de publicação, Drive, custo da noite, falhas).
Tabelas: youtube.backlog, youtube.calendario_semanas, youtube.producao_noturna, youtube.noites (tools/db/schema_backlog.sql).
Config opcional: ~/.config/fabrica/noturna.env (chaves abaixo em PADRAO).
"""
import argparse
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import backlog as B  # noqa: E402
from psycopg.types.json import Jsonb  # noqa: E402

REPO, TZ = B.REPO, B.TZ
REF = Path.home() / "workspace/referencias"
FILA = REPO / "tools/fila.sh"
LOGDIR = Path.home() / "workspace/relatorios/noturna"
PADRAO = {
    "CANAIS": "historia-ptbr,dossie-es,lugares-guerra-en,em-relevo",  # ordem = prioridade no corte
    "INICIO": "2026-11-15",         # 1ª noite de produção (Rodrigo: começa dom 15/11 20:00); antes disso o timer não faz nada
    "HORIZONTE_VAGA": "7",          # dias à frente para achar a vaga a produzir
    "PRAZO_HORA": "07:00",
    "LIMITE_SUBSTITUTO": "03:30",   # depois disso, embalagem reprovada não ganha substituto na mesma noite
    "FOLGA_FAL": "5", "FOLGA_FISH": "2", "FOLGA_RUNPOD": "1",
    "DISCO_MIN_GB": "8", "DISCO_POR_VIDEO_GB": "4",
    "MAX_SEMANA_CORTE": "90",       # % semanal do Max: acima disso produz no máx. MAX_SEMANA_CORTE_N vídeos
    "MAX_SEMANA_CORTE_N": "2", "MAX_SEMANA_PARAR": "97",
    "MAX_LEITURA_VELHA_H": "24",
}
# Necessidade estimada por vídeo (US$), de financas.consumo (média dos vídeos 013+ em 14/11/2026) + reserva.
NECESSIDADE = {
    "historia-ptbr": {"fal.ai": 2.0, "Fish Audio": 0.8, "Runpod": 0.5},   # Codex US$ 0; fal = reserva do fallback
    "dossie-es": {"fal.ai": 9.5, "Fish Audio": 0.4, "Runpod": 0.5},
    "lugares-guerra-en": {"fal.ai": 1.0, "Fish Audio": 0.5, "Runpod": 0.5},  # IA só na thumb
    "em-relevo": {"Runpod": 0.6},                                           # sem IA de cena; voz ElevenLabs
}
TETO = {"historia-ptbr": 8, "dossie-es": 12, "lugares-guerra-en": 4, "em-relevo": 3}
FOLGA_DE = {"fal.ai": "FOLGA_FAL", "Fish Audio": "FOLGA_FISH", "Runpod": "FOLGA_RUNPOD"}

REGRAS_CANAL = {
    "historia-ptbr": """- Canal **História em minutos** (pt-BR), molde **History in Minutes, bíblia v2**: narrativa contínua, eras ligadas por causa→consequência ("mas… então…"), fio condutor, "guarde isso" pagos depois; bonequinhos de cabeça redonda. Bíblia: `canais/historia-ptbr/biblia/` (prevalece).
- **Não leia `canais/dossie-es/`** nem copie nada de outro canal. Referência de código/estrutura: SOMENTE os últimos vídeos deste canal (`videos/007-russia` em diante, checklist v2 com nota).
- Imagens **pelo Codex** (`canal.yaml` `visual.gerador: codex`, fallback fal automático; outro job cuida do gerador: **não edite** `canal.yaml`, `tools/img_*`, `skills/imagens`, `skills/thumbnail`). Nos prompts de época, diga o que **não** pode aparecer (o Codex inventa marcos fora de época; `conhecimento/anti-padroes.md` §3d). Voz Fish drama-3 (`canal.yaml`).
- Feche no presente com 1 frase neutra. Guerra/regimes: seriedade e neutralidade factual, sem imagens gráficas (política de anúncios).""",
    "dossie-es": """- Canal **Dossier en Minutos** (espanhol), molde **Archive in Minutes**: capítulos "EXPEDIENTE N", hook por anedota, carimbos e SFX nas transições; graphic novel em tinta. Bíblia: `canais/dossie-es/biblia/` (prevalece).
- **Não leia `canais/historia-ptbr/`** nem copie nada de outro canal. Referência de código/estrutura: SOMENTE os últimos vídeos deste canal (`videos/007-ss`, `008-inquisicion`).
- Imagens pela fal conforme `canal.yaml` (nano-banana; tamanho máximo do modelo; cobra por megapixel; filtro devolve preta sem erro; moldura em ~25%: detector do 001-cia). Voz Fish (`canal.yaml`).
- Organizações nazistas/temas sensíveis: sem runas, suástica ou símbolos na thumb e nas imagens; tom de vítimas e julgamento. Organização viva: atribua toda acusação ("según X").""",
    "lugares-guerra-en": """- Canal **Clearance Required** (inglês): lugares militares famosos que não se pode visitar + os documentos públicos que explicam por quê. Bíblia: `canais/lugares-guerra-en/biblia/` (prevalece).
- Não leia nem copie os canais `historia-ptbr`/`dossie-es`. Referência de código/estrutura: SOMENTE `videos/002-bikini` e `003-gettysburg`.
- **Acervo real** (NARA, DoD/DVIDS, LOC, Wikimedia PD/CC com licença conferida por arquivo); **IA só na base da thumb** (fal conforme `canal.yaml`). Créditos só na descrição. Voz conforme `canal.yaml`.
- Restos humanos/vítimas: nada de ossadas ou corpos na tela, nada de "dead/death" no título.""",
    "em-relevo": """- Canal **Em Relevo** (pt-BR): clima e geografia do Brasil em mapa 3D/satélite + fotos reais grandes. **Sem IA de cena.** O canal não tem pasta `canais/`: as regras moram em `pesquisa/canal-clima-2026-11/` (`RELATORIO.md`, `biblia-titulo.md` = bíblia de título/thumb, `IDEIAS-A-DISCUTIR.md`) e `pesquisa/estilo-mapa-relevo-3d/PADRAO.md`; as regras de lote de `~/workspace/referencias/BRIEF-lote-fds-COMUM.md` valem, **exceto a seção Entrega** (aqui quem entrega é a rotina noturna).
- Pipeline/código: copie de `pesquisa/canal-clima-2026-11/longo-04/` (e `longo-03/`), sem `node_modules`. Escreva só na sua pasta `longo-NN/`.
- Imagens: Landsat/USGS, NOAA, INMET, Wikimedia com licença conferida por arquivo, arquivos públicos com licença clara. **Nenhuma imagem da Globo/TV.** Créditos só na descrição. Voz ElevenLabs (a mesma do 002; confira o saldo de caracteres).
- Números com fonte primária (sem fonte vira "segundo X" ou sai). Sem alarmismo em previsão: probabilidades com fonte.""",
}


def cfg():
    c = dict(PADRAO)
    f = Path.home() / ".config/fabrica/noturna.env"
    if f.exists():
        for ln in f.read_text().splitlines():
            if "=" in ln and not ln.strip().startswith("#"):
                k, v = ln.split("=", 1)
                c[k.strip()] = v.strip()
    return c


def log(msg):
    linha = f"{datetime.now(TZ):%Y-%m-%d %H:%M:%S} {msg}"
    print(linha)
    try:
        LOGDIR.mkdir(parents=True, exist_ok=True)
        with open(LOGDIR / "noturna.log", "a") as f:
            f.write(linha + "\n")
    except OSError:
        pass


def evento(tipo, sev, msg, ref=None):
    try:
        sys.path.insert(0, str(REPO / "tools"))
        from event_log import registrar
        registrar("noturna", tipo, sev, msg, ref=ref)
    except Exception as e:  # noqa: BLE001
        print(f"[evento] aviso: {e}")


def telegram(assunto, texto, enviar=True):
    print(f"--- Telegram: {assunto}\n{texto}\n---")
    if not enviar:
        return False
    try:
        r = subprocess.run([str(Path.home() / ".local/bin/hermes"), "send", "--to", "telegram", "--subject", assunto, "--quiet"],
                           input=texto, text=True, capture_output=True, timeout=120)
        ok = r.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        ok = False
    log(f"telegram {'ok' if ok else 'FALHOU'}: {assunto}")
    return ok


# ---------------- pré-voo ----------------
def drive_livre_mb():
    try:
        r = subprocess.run(["rclone", "about", "gdrive:", "--json"], capture_output=True, text=True, timeout=90)
        return int(json.loads(r.stdout).get("free", 0)) / 1048576
    except Exception:  # noqa: BLE001
        return None


def preflight(con, c):
    pf = {"saldos": {}, "avisos": []}
    for forn, saldo in con.execute("SELECT fornecedor, saldo FROM financas.saldo_pre_pago").fetchall():
        pf["saldos"][forn] = float(saldo)
    r = con.execute("SELECT lido_em, pct_semana, reseta_semana, pct_5h, reseta_5h FROM ops.max_leituras ORDER BY lido_em DESC LIMIT 1").fetchone()
    agora = datetime.now(TZ)
    if r:
        idade_h = (agora - r[0]).total_seconds() / 3600
        reset_passou = bool(r[2] and r[2] <= agora)
        pf["max"] = {"lido_em": r[0].astimezone(TZ).isoformat(timespec="minutes"), "pct_semana": float(r[1]) if r[1] is not None else None,
                     "reseta_semana": r[2].astimezone(TZ).isoformat(timespec="minutes") if r[2] else None, "idade_h": round(idade_h, 1),
                     "reset_passou": reset_passou}
        if reset_passou:
            pf["max"]["pct_semana_efetivo"] = 0.0
        if idade_h > float(c["MAX_LEITURA_VELHA_H"]) and not reset_passou:
            pf["avisos"].append(f"leitura do Max semanal velha ({idade_h:.0f} h, {r[1]}%): sigo com cautela")
    else:
        pf["max"] = None
        pf["avisos"].append("sem leitura do Max semanal (ops.max_leituras): sigo com cautela")
    pf["drive_livre_mb"] = drive_livre_mb()
    st = os.statvfs(Path.home())
    pf["disco_livre_gb"] = round(st.f_bavail * st.f_frsize / 1e9, 1)
    return pf


def cortar(pf, candidatos, c):
    """candidatos em ordem de prioridade → (aprovados, cortes[{canal, motivo}]). Greedy: entra se couber."""
    sald = dict(pf["saldos"])
    aprov, cortes = [], []
    mx = pf.get("max") or {}
    pct = mx.get("pct_semana_efetivo", mx.get("pct_semana"))
    limite_n = len(candidatos)
    if pct is not None and pct >= float(c["MAX_SEMANA_PARAR"]):
        limite_n = 0
    elif pct is not None and pct >= float(c["MAX_SEMANA_CORTE"]):
        limite_n = int(c["MAX_SEMANA_CORTE_N"])
    disco = pf["disco_livre_gb"] - float(c["DISCO_MIN_GB"])
    for cand in candidatos:
        canal = cand["canal"]
        if len(aprov) >= limite_n:
            cortes.append({"canal": canal, "motivo": f"Max semanal em {pct:.0f}% (corte ≥ {c['MAX_SEMANA_CORTE']}%: no máx. {limite_n} vídeo(s))"})
            continue
        if disco < float(c["DISCO_POR_VIDEO_GB"]):
            cortes.append({"canal": canal, "motivo": f"disco local com {pf['disco_livre_gb']:.0f} GB livres"})
            continue
        falta = []
        for forn, v in NECESSIDADE[canal].items():
            folga = float(c[FOLGA_DE[forn]])
            if forn in sald and sald[forn] - v < folga:
                falta.append(f"{forn.split()[0].replace('.ai', '')} com US$ {sald[forn]:.0f}, recarregue")
        if falta:
            cortes.append({"canal": canal, "motivo": "; ".join(falta)})
            continue
        for forn, v in NECESSIDADE[canal].items():
            if forn in sald:
                sald[forn] -= v
        disco -= float(c["DISCO_POR_VIDEO_GB"])
        aprov.append(cand)
    return aprov, cortes


# ---------------- pauta ----------------
def vaga_e_item(con, canal, noite, horizonte, excluir=()):
    """1ª vaga do calendário (de amanhã até amanhã+horizonte) e o item do backlog para ela."""
    amanha = noite + timedelta(days=1)
    ocup = {r[0] for r in con.execute("SELECT data_prevista FROM youtube.backlog WHERE canal_slug=%s AND status IN ('em_producao','pronto','publicado') "
                                      "AND data_prevista >= %s", (canal, amanha)).fetchall()}
    vagas = [d for d in B.slots(con, amanha, amanha + timedelta(days=horizonte)) if d not in ocup]
    if not vagas:
        return None, None
    vaga = vagas[0]
    ex = tuple(excluir) or (0,)
    it = B.itens(con, "canal_slug=%s AND status='agendado' AND data_prevista=%s AND NOT (id = ANY(%s))", (canal, vaga, list(ex)))
    if not it:
        it = B.itens(con, "canal_slug=%s AND status IN ('agendado','proposto') AND NOT (id = ANY(%s))", (canal, list(ex)))
    return vaga, (it[0] if it else None)


def nome_canal_curto(canal):
    return B.CANAIS[canal]["curto"]


def gerar_briefs(canal, it, vid_id, numero, pasta, vaga, noite, prazo, destino=REF):
    cfgc = B.CANAIS[canal]
    curto = cfgc["curto"]
    pasta_nome = Path(pasta).name
    nnn = f"{numero:03d}"
    base = f"BRIEF-lote-{curto}-{nnn}-{it['slug']}"
    destino.mkdir(parents=True, exist_ok=True)
    principal = destino / f"{base}.md"
    e1, e2 = destino / f"{base}-ETAPA1.md", destino / f"{base}-ETAPA2.md"
    biblia = {"em-relevo": "pesquisa/canal-clima-2026-11/ (RELATORIO.md, biblia-titulo.md) + pesquisa/estilo-mapa-relevo-3d/PADRAO.md"}.get(canal, f"canais/{canal}/biblia/")
    evid = "\n".join(f"  - [{e.get('tipo', '')}] {e.get('fonte', '')}: {e.get('numero', '')} ({e.get('data', '')}) {e.get('link', '')}".rstrip()
                     for e in (it["evidencias"] or []))
    entrega_drive = ("**Não rode `entregar_drive.sh` nem `rclone`.** Deixe tudo em `" + pasta + "/entrega/` (video.mp4, legendas.srt, "
                     "thumb-A/B/C.jpg, thumbnail.jpg, pacote/youtube.txt com os 3 títulos pareados às thumbs). A rotina noturna "
                     "(`noturna.py vigia`) sobe ao Drive se houver espaço e avisa o Rodrigo se não houver.")
    txt = f"""# BRIEF lote noturno: {cfgc['nome']} {nnn} — {it['tema']} (publica {B.fmt_d(vaga)}/{vaga:%Y})
<!-- Gerado por tools/rotinas/noturna.py em {datetime.now(TZ):%d/%m/%Y %H:%M} (noite de {noite:%d/%m}) a partir do backlog vivo
     (youtube.backlog id {it['id']}). Etapas: {e1.name} (Opus) e {e2.name} (Sonnet, --depende-de). -->

Repo `~/workspace/fabrica-youtube`. Leia `~/.claude/CLAUDE.md` (headless), `MAPA.md`, `AGENTS.md`, a **bíblia do canal** `{biblia}` (prevalece), `conhecimento/` (regras gerais, `titulos.md`, `erros-qa.md`, `politicas-youtube.md`) e as skills de etapa. **Tudo em primeiro plano** (Task também). **Não pare por pendência menor: contorne e registre.** Só encerre com tudo pronto, commitado e com push, ou com `BLOQUEIO.md` na pasta do vídeo.

## O vídeo
- Canal `{canal}`. Pasta **já criada**: `{pasta}/`. Linha **já criada** em `youtube.videos`: **id {vid_id}** (número {numero}): use-a (não crie outra), atualize `titulo` com o T1 aprovado e avance `status` a cada etapa até `pronto`.
- Tema (backlog vivo, nota {it['nota']}: demanda {it['demanda']} × encaixe {it['encaixe']} × urgência {it['urgencia']}): **{it['tema']}**.
- Ângulo/hook candidato (ponto de partida; confira os fatos): {it['angulo'] or '-'}
- Título candidato (ponto de partida; a **embalagem + crivo** decide): {it['titulo_candidato'] or '-'}
- Evidências da pauta (fonte `{it['fonte'] or 'youtube.backlog'}`):
{evid or '  - (sem evidência registrada)'}
- Riscos: {it['riscos'] or '-'}
- Publicação: **{B.fmt_d(vaga)}/{vaga:%Y}** (upload manual do Rodrigo de manhã). **Prazo: tudo pronto até {prazo:%d/%m %H:%M}.**
- Teto em dinheiro do vídeo (etapa 2): **US$ {TETO[canal]}**. Toda geração paga com `--video {vid_id}`.

## Regras do canal
{REGRAS_CANAL[canal]}

## Regras gerais do lote noturno
- Outros vídeos rodam antes/depois/em paralelo: `git add` só da sua pasta (+ bíblia do seu canal para aprendizados); **não edite a seção "Backlog vivo" do `backlog.md`** (é gerada pelo `backlog.py`). `index.lock` → espere e tente de novo. `git pull --rebase` antes do push.
- Memória da VPS: nunca grave em `/tmp` (é RAM): use `$TMPDIR` (= `~/cache/tmp`). Render só no Runpod (`tools/render_runpod.sh`, skill `montagem-render`), em partes. Pré-QA visual (`tools/preqa_visual.py`) antes do render.
- **3 títulos + 3 thumbs** pareadas (A = T1, B = T2, C = variação) para o "Testar e comparar". Sem gancho de próximo vídeo (nunca anuncie o próximo; puxar sessão para vídeo já publicado pode). Pauta proibida: `conhecimento/politicas-youtube.md` e a lista "evitar" da bíblia.
- Embalagem reprovada no crivo (3 rodadas) → `BLOQUEIO.md` na pasta com a palavra "crivo" e **pare**: a rotina noturna põe o próximo tema do backlog na mesma noite.
- **Entrega:** {entrega_drive}
- Custos em `financas.consumo` com o id {vid_id}. Confira saldos antes (outros jobs gastam ao mesmo tempo).
- `git grep` atrás de segredos antes do push. Resposta final curta (pt-BR) conforme a etapa.
"""
    principal.write_text(txt)
    m1 = (REF / "BRIEF-lote-MODELO-ETAPA1.md").read_text()
    m2 = (REF / "BRIEF-lote-MODELO-ETAPA2.md").read_text()

    def sub(m):
        m = re.sub(r"<!--.*?-->\n?", "", m, flags=re.S)
        m = m.replace(f"BRIEF-lote-<canal>-<NNN>-<slug>.md", principal.name)
        m = m.replace("<pasta do vídeo>", pasta)
        m = m.replace("canais/<slug>/biblia/", biblia)
        m = m.replace("<com ou sem Drive, conforme o brief do lote>", "sem Drive: deixe em `entrega/`; a rotina noturna sobe")
        return m
    hdr = f"<!-- Gerado por tools/rotinas/noturna.py (noite de {noite:%d/%m}); vídeo id {vid_id}, pasta {pasta}, publica {vaga:%d/%m}. -->\n"
    e1.write_text(hdr + sub(m1) + f"\n- Pasta e linha em `youtube.videos` (id {vid_id}) **já existem**: o passo 1 completa o `BRIEF.md`, não cria outra linha.\n")
    e2.write_text(hdr + sub(m2) + f"\n- Prazo: pronto até {prazo:%d/%m %H:%M}. Teto US$ {TETO[canal]}. Entrega: só `entrega/` (a rotina noturna sobe ao Drive).\n")
    return principal, e1, e2


def enfileirar(con, canal, it, vaga, noite, c, dry, tentativa=1, prioridade=3):
    numero = B.proximo_numero(con, canal)
    pasta = f"{B.CANAIS[canal]['videos']}/{B.CANAIS[canal]['pasta_fmt'].format(n=numero, slug=it['slug'])}"
    h, mi = map(int, c["PRAZO_HORA"].split(":"))
    prazo = datetime.combine(noite + timedelta(days=1), datetime.min.time()).replace(hour=h, minute=mi, tzinfo=TZ)
    nome = f"lote-{B.CANAIS[canal]['curto']}-{numero:03d}-{it['slug']}"
    res = {"canal": canal, "tema": it["tema"], "backlog_id": it["id"], "vaga": str(vaga), "numero": numero, "pasta": pasta,
           "jobs": [f"{nome}-e1", f"{nome}-e2"], "tentativa": tentativa}
    if dry:  # prévia dos briefs (fora da fila e fora de referencias/): referencias/previa-noturna-<noite>/
        prev = REF / f"previa-noturna-{noite:%Y-%m-%d}"
        p, e1, e2 = gerar_briefs(canal, it, "<id na hora>", numero, pasta, vaga, noite, prazo, destino=prev)
        res["briefs"] = [str(x.relative_to(REF)) for x in (p, e1, e2)]
        return res
    titulo = it["titulo_candidato"] or it["tema"]
    vid = con.execute("INSERT INTO youtube.videos (canal_slug, numero, titulo, status, pasta, notas, biblia_versao) VALUES (%s,%s,%s,'roteiro',%s,%s,%s) RETURNING id",
                      (canal, numero, titulo, pasta, f"fábrica noturna {noite:%d/%m}: backlog id {it['id']}, publica {vaga:%d/%m}",
                       "v2" if canal == "historia-ptbr" else None)).fetchone()[0]
    (REPO / pasta).mkdir(parents=True, exist_ok=True)
    p, e1, e2 = gerar_briefs(canal, it, vid, numero, pasta, vaga, noite, prazo)
    res["briefs"] = [p.name, e1.name, e2.name]
    res["video_id"] = vid
    pz = f"{prazo:%Y-%m-%d %H:%M}"
    for args in ([f"{nome}-e1", str(e1), "--modelo", "opus", "--prioridade", str(prioridade), "--prazo", pz],
                 [f"{nome}-e2", str(e2), "--modelo", "sonnet", "--prioridade", str(prioridade + 1), "--prazo", pz, "--depende-de", f"{nome}-e1"]):
        r = subprocess.run([str(FILA), "add", *args], capture_output=True, text=True)
        log(f"fila add {args[0]}: {(r.stdout or r.stderr).strip()}")
    B.mudar(con, it["id"], f"produção noturna {noite:%d/%m} (tentativa {tentativa}) para {B.fmt_d(vaga)}",
            status="em_producao", data_prevista=vaga, video_id=vid, pasta=pasta)
    con.execute("INSERT INTO youtube.producao_noturna (noite, canal_slug, tentativa, backlog_id, video_id, data_publicacao, job_e1, job_e2) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (noite, canal_slug, tentativa) DO NOTHING",
                (noite, canal, tentativa, it["id"], vid, vaga, f"{nome}-e1", f"{nome}-e2"))
    return res


def planejar(a):
    c = cfg()
    noite = date.fromisoformat(a.noite) if a.noite else B.hoje()
    canais = [x for x in c["CANAIS"].split(",") if x] if not a.canal else [a.canal]
    if noite < date.fromisoformat(c["INICIO"]) and not a.forcar:
        log(f"noite {noite:%d/%m}: antes do início da fábrica noturna ({c['INICIO']}); nada a fazer")
        return
    con = B.conectar(autocommit=False)
    try:
        amanha = noite + timedelta(days=1)
        if not B.eh_slot(con, amanha) and not a.forcar:
            log(f"noite {noite:%d/%m}: amanhã ({B.fmt_d(amanha)}) não é dia de publicação; nada a fazer")
            con.rollback() if a.dry_run else con.commit()
            return
        B.sync(con)
        B.agendar(con, ref=noite)
        pf = preflight(con, c)
        cands, sem = [], []
        for canal in canais:
            if con.execute("SELECT 1 FROM youtube.producao_noturna WHERE noite=%s AND canal_slug=%s", (noite, canal)).fetchone():
                sem.append({"canal": canal, "motivo": "já enfileirado nesta noite"})
                continue
            vaga, it = vaga_e_item(con, canal, noite, int(c["HORIZONTE_VAGA"]))
            if not vaga:
                sem.append({"canal": canal, "motivo": f"calendário coberto até {amanha + timedelta(days=int(c['HORIZONTE_VAGA'])):%d/%m}"})
            elif not it:
                sem.append({"canal": canal, "motivo": "backlog vazio (rode a rotina backlog)"})
            else:
                cands.append({"canal": canal, "vaga": vaga, "item": it})
        ordem = {k: i for i, k in enumerate(canais)}
        cands.sort(key=lambda x: (x["vaga"], ordem[x["canal"]]))
        aprov, cortes = cortar(pf, cands, c)
        feitos = [enfileirar(con, x["canal"], x["item"], x["vaga"], noite, c, a.dry_run, prioridade=3 + 2 * i) for i, x in enumerate(aprov)]
        for x in cortes:
            cc = next(k for k in cands if k["canal"] == x["canal"])
            x.update({"tema": cc["item"]["tema"], "vaga": str(cc["vaga"])})
            if not a.dry_run:
                con.execute("INSERT INTO youtube.producao_noturna (noite, canal_slug, backlog_id, data_publicacao, status, obs) VALUES (%s,%s,%s,%s,'adiado',%s) "
                            "ON CONFLICT DO NOTHING", (noite, x["canal"], cc["item"]["id"], cc["vaga"], x["motivo"]))
        if not a.dry_run:
            con.execute("INSERT INTO youtube.noites (noite, preflight, cortes) VALUES (%s,%s,%s) ON CONFLICT (noite) DO UPDATE SET preflight=EXCLUDED.preflight, "
                        "cortes=youtube.noites.cortes || EXCLUDED.cortes", (noite, Jsonb(pf), Jsonb(cortes)))
        # relatório
        L = [f"Fábrica noturna {noite:%d/%m} ({'DRY-RUN, nada enfileirado' if a.dry_run else 'enfileirado'})", "",
             "Pré-voo: " + ", ".join(f"{k} US$ {v:.2f}" for k, v in pf["saldos"].items() if k in ("fal.ai", "Fish Audio", "Runpod"))
             + ((f"; Max semanal {pf['max']['pct_semana']}% (lido {datetime.fromisoformat(pf['max']['lido_em']):%d/%m %H:%M}, {pf['max']['idade_h']:.0f} h"
                 + (", reset já passou" if pf['max'].get('reset_passou') else "") + ")") if pf.get("max") else "; Max semanal sem leitura")
             + ((f"; Drive {pf['drive_livre_mb'] / 1024:.1f} GB livres") if pf["drive_livre_mb"] is not None else "; Drive: não consegui ler"),
             f"Disco local {pf['disco_livre_gb']:.0f} GB livres." + (" Avisos: " + " | ".join(pf["avisos"]) if pf["avisos"] else ""), ""]
        for f in feitos:
            L.append(f"+ {f['canal']}: {f['tema']} → publica {B.fmt_d(date.fromisoformat(f['vaga']))} · pasta {f['pasta']} · jobs {', '.join(f['jobs'])}")
            L.append(f"    briefs: {', '.join(f['briefs'])}")
        for x in cortes:
            L.append(f"- {x['canal']}: ADIADO {x['tema']} ({B.fmt_d(date.fromisoformat(x['vaga']))}): {x['motivo']}")
        for x in sem:
            L.append(f"· {x['canal']}: nada a produzir ({x['motivo']})")
        rel = "\n".join(L)
        print(rel)
        if a.dry_run:
            con.rollback()
        else:
            con.commit()
            log(f"planejar {noite:%d/%m}: {len(feitos)} enfileirado(s), {len(cortes)} adiado(s)")
            for f in feitos:
                evento("noturna_enfileirado", "info", f"{f['canal']} {f['tema']} → {f['vaga']}", ref=f["jobs"][0])
            if cortes or pf["avisos"]:
                msg = [f"Noite {noite:%d/%m}: {len(feitos)} vídeo(s) na fila."]
                msg += [f"⚠ {x['canal']}: {x['tema']} ({B.fmt_d(date.fromisoformat(x['vaga']))}) adiado: {x['motivo']}." for x in cortes]
                msg += [f"⚠ {w}" for w in pf["avisos"]]
                if pf["drive_livre_mb"] is not None and pf["drive_livre_mb"] < 1500:
                    msg.append(f"⚠ Drive com {pf['drive_livre_mb'] / 1024:.1f} GB: os vídeos ficam na fila de entrega se não couberem.")
                telegram(f"[fábrica] noite {noite:%d/%m}", "\n".join(msg), not a.sem_telegram)
            # espelho do backlog nos backlog.md (commit pela rotina diária/git-diario)
            for canal in B.CANAIS:
                with B.conectar() as c2:
                    B.gerar_md(c2, canal)
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()


# ---------------- vigia ----------------
def ler(p):
    try:
        return Path(p).read_text(errors="replace")
    except OSError:
        return ""


def status_job(con, nome):
    r = con.execute("SELECT status FROM ops.fila_jobs WHERE nome=%s", (nome,)).fetchone() if nome else None
    return r[0] if r else None


def entregar(con, row, canal, pasta, enviar_tg):
    """Sobe <pasta>/entrega ao Drive. Devolve 'entregue' | 'sem_espaco' | 'erro'."""
    item = Path(pasta).name
    src = REPO / pasta / "entrega"
    if not src.is_dir() or not any(src.iterdir()):
        return "erro"
    if canal != "em-relevo":
        r = subprocess.run([str(REPO / "tools/entregar_drive.sh"), canal, item], capture_output=True, text=True, timeout=3600)
        rc = r.returncode
    else:  # Em Relevo não tem canais/<slug>/canal.yaml: mesmo critério do entregar_drive.sh (folga de 300 MB), rclone direto
        precisa = sum(f.stat().st_size for f in src.rglob("*") if f.is_file()) / 1048576
        livre = drive_livre_mb()
        if livre is None or livre < precisa + 300:
            rc = 3
        else:
            r = subprocess.run(["rclone", "copy", str(src), f"gdrive:Youtube/Em Relevo/{item}", "--drive-chunk-size", "64M", "--transfers", "2"],
                               capture_output=True, text=True, timeout=3600)
            rc = r.returncode
    st = "entregue" if rc == 0 else ("sem_espaco" if rc == 3 else "erro")
    con.execute("UPDATE youtube.producao_noturna SET entrega=%s, entregue_em=CASE WHEN %s='entregue' THEN now() END, atualizado_em=now() WHERE id=%s",
                (st, st, row["id"]))
    log(f"entrega {canal}/{item}: {st} (rc {rc})")
    if st == "sem_espaco" and not row["avisado_em"]:
        telegram("[fábrica] Drive sem espaço", f"{B.CANAIS[canal]['nome']} {item} pronto, mas o Drive não tem espaço: ficou na fila de entrega "
                 f"({pasta}/entrega). Libere espaço (pastas vazias = já subiu) e eu tento de novo sozinho.", enviar_tg)
        con.execute("UPDATE youtube.producao_noturna SET avisado_em=now() WHERE id=%s", (row["id"],))
    return st


def vigia(a):
    c = cfg()
    lock = open(Path(os.environ.get("TMPDIR", Path.home() / "cache/tmp")) / "fabrica-noturna-vigia.lock", "w")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("outra vigia em andamento")
        return
    enviar = not a.sem_telegram
    with B.conectar() as con:
        B.sync(con)
        cur = con.execute("SELECT * FROM youtube.producao_noturna WHERE status='enfileirado' OR (status='pronto' AND entrega IS DISTINCT FROM 'entregue') ORDER BY id")
        names = [d.name for d in cur.description]
        rows = [dict(zip(names, r)) for r in cur.fetchall()]
        agora = datetime.now(TZ)
        for row in rows:
            canal = row["canal_slug"]
            it = B.itens(con, "id=%s", (row["backlog_id"],))[0] if row["backlog_id"] else None
            pasta = it["pasta"] if it else None
            if not pasta:
                continue
            s1, s2 = status_job(con, row["job_e1"]), status_job(con, row["job_e2"])
            pdir = REPO / pasta
            bloq = ler(pdir / "BLOQUEIO.md")
            if row["status"] == "enfileirado":
                e1_fim = s1 in ("concluido", "bloqueado", "falhou")
                if e1_fim and bloq and not (pdir / "ETAPA1-PRONTA.md").exists() and re.search(r"crivo|embalagem", bloq, re.I):
                    # embalagem reprovada: descarta e põe o próximo tema na mesma noite (1×)
                    con.execute("UPDATE youtube.producao_noturna SET status='embalagem_reprovada', obs=%s, atualizado_em=now() WHERE id=%s",
                                ("BLOQUEIO.md do crivo", row["id"]))
                    if s2 == "fila":
                        subprocess.run([str(FILA), "cancel", row["job_e2"]], capture_output=True)
                    con.execute("UPDATE youtube.videos SET status='arquivado', notas=coalesce(notas,'')||' | embalagem reprovada no crivo (noite)', atualizado_em=now() WHERE id=%s",
                                (row["video_id"],))
                    B.mudar(con, it["id"], f"embalagem reprovada no crivo (noite {row['noite']:%d/%m}); ver {pasta}/BLOQUEIO.md",
                            status="descartado", data_prevista=None)
                    evento("noturna_embalagem_reprovada", "aviso", f"{canal} {it['tema']}", ref=row["job_e1"])
                    h, mi = map(int, c["LIMITE_SUBSTITUTO"].split(":"))
                    limite = datetime.combine(row["noite"] + timedelta(days=1), datetime.min.time()).replace(hour=h, minute=mi, tzinfo=TZ)
                    if row["tentativa"] == 1 and agora < limite:
                        tentados = [r[0] for r in con.execute("SELECT backlog_id FROM youtube.producao_noturna WHERE noite=%s AND canal_slug=%s", (row["noite"], canal)).fetchall()]
                        B.agendar(con, canal, ref=row["noite"])
                        vaga, novo = vaga_e_item(con, canal, row["noite"], int(c["HORIZONTE_VAGA"]), excluir=tentados)
                        if novo:
                            f = enfileirar(con, canal, novo, row["data_publicacao"] or vaga, row["noite"], c, False, tentativa=2, prioridade=2)
                            log(f"vigia: {canal} embalagem reprovada ({it['tema']}) → substituto {novo['tema']} ({', '.join(f['jobs'])})")
                            telegram("[fábrica] embalagem reprovada", f"{B.CANAIS[canal]['nome']}: o crivo reprovou \"{it['tema']}\"; entrou \"{novo['tema']}\" na mesma noite.", enviar)
                        else:
                            log(f"vigia: {canal} embalagem reprovada e backlog sem substituto")
                    else:
                        log(f"vigia: {canal} embalagem reprovada ({it['tema']}); sem substituto (tentativa {row['tentativa']}, limite {c['LIMITE_SUBSTITUTO']})")
                    continue
                if s1 in ("bloqueado", "falhou", "cancelado"):
                    if s2 == "fila":
                        subprocess.run([str(FILA), "cancel", row["job_e2"]], capture_output=True)
                    con.execute("UPDATE youtube.producao_noturna SET status=%s, obs=%s, atualizado_em=now() WHERE id=%s",
                                ("bloqueado" if s1 == "bloqueado" else ("cancelado" if s1 == "cancelado" else "falhou"), f"e1 {s1}" + (": " + bloq[:200] if bloq else ""), row["id"]))
                    continue
                if s2 in ("bloqueado", "falhou", "cancelado"):
                    con.execute("UPDATE youtube.producao_noturna SET status=%s, obs=%s, atualizado_em=now() WHERE id=%s",
                                ("bloqueado" if s2 == "bloqueado" else ("cancelado" if s2 == "cancelado" else "falhou"), f"e2 {s2}" + (": " + bloq[:200] if bloq else ""), row["id"]))
                    continue
                vst = con.execute("SELECT status FROM youtube.videos WHERE id=%s", (row["video_id"],)).fetchone()
                pronto = s2 == "concluido" and ((vst and vst[0] in ("pronto", "publicado")) or (pdir / "entrega").is_dir())
                if pronto:
                    con.execute("UPDATE youtube.producao_noturna SET status='pronto', entrega='pendente', atualizado_em=now() WHERE id=%s", (row["id"],))
                    if it["status"] == "em_producao":
                        B.mudar(con, it["id"], "vídeo pronto (produção noturna)", status="pronto")
                    row["status"], row["entrega"] = "pronto", "pendente"
                elif s2 == "concluido" and bloq:
                    con.execute("UPDATE youtube.producao_noturna SET status='bloqueado', obs=%s, atualizado_em=now() WHERE id=%s", ("e2: " + bloq[:200], row["id"]))
                    continue
            if row["status"] == "pronto" and row["entrega"] != "entregue":
                # sem espaço: tenta de novo a cada 60 min
                if row["entrega"] in ("sem_espaco", "erro") and row["atualizado_em"] and agora - row["atualizado_em"] < timedelta(minutes=60):
                    continue
                entregar(con, row, canal, pasta, enviar)


# ---------------- manhã ----------------
def titulo_aprovado(pasta, fallback):
    for nome in ("ETAPA1-PRONTA.md", "EMBALAGEM.md"):
        t = ler(REPO / pasta / nome)
        m = re.search(r"T1[^\n]{0,40}?[\"“«]([^\"”»\n]{8,140})[\"”»]", t)
        if m:
            return m.group(1).strip()
    return fallback


def manha(a):
    noite = date.fromisoformat(a.noite) if a.noite else B.hoje() - timedelta(days=1)
    if not a.dry_run:
        try:
            vigia(argparse.Namespace(sem_telegram=a.sem_telegram))
        except Exception as e:  # noqa: BLE001
            log(f"manha: vigia falhou ({e})")
    with B.conectar() as con:
        cur = con.execute("SELECT * FROM youtube.producao_noturna WHERE noite=%s ORDER BY canal_slug, tentativa", (noite,))
        names = [d.name for d in cur.description]
        rows = [dict(zip(names, r)) for r in cur.fetchall()]
        nt = con.execute("SELECT cortes FROM youtube.noites WHERE noite=%s", (noite,)).fetchone()
        if not rows and not (nt and nt[0]):
            print(f"noite {noite:%d/%m}: sem produção registrada; nada a mandar")
            return
        L = [f"Fábrica noturna {noite:%d/%m} → manhã {noite + timedelta(days=1):%d/%m}"]
        total_usd = total_eq = 0.0
        icone = {"pronto": "✅", "enfileirado": "⏳", "embalagem_reprovada": "♻", "bloqueado": "⛔", "falhou": "❌", "adiado": "⏸", "cancelado": "✖"}
        for r in rows:
            it = B.itens(con, "id=%s", (r["backlog_id"],))[0] if r["backlog_id"] else None
            nome = B.CANAIS[r["canal_slug"]]["nome"]
            tema = it["tema"] if it else "?"
            if r["status"] == "adiado":
                L.append(f"{icone['adiado']} {nome}: {tema} adiado ({r['obs']})")
                continue
            vt = con.execute("SELECT titulo FROM youtube.videos WHERE id=%s", (r["video_id"],)).fetchone() if r["video_id"] else None
            tit = titulo_aprovado(it["pasta"], vt[0] if vt else tema) if it and it["pasta"] else tema
            usd = float(con.execute("SELECT COALESCE(sum(custo),0) FROM financas.consumo WHERE ref_id=%s", (r["video_id"],)).fetchone()[0]) if r["video_id"] else 0
            eq = float(con.execute("SELECT COALESCE(sum(custo_equivalente_usd),0) FROM ops.fila_jobs WHERE nome IN (%s,%s)", (r["job_e1"], r["job_e2"])).fetchone()[0])
            total_usd += usd
            total_eq += eq
            if r["status"] == "pronto":
                drive = {"entregue": f"Drive: Youtube/{nome}/{Path(it['pasta']).name}", "sem_espaco": "Drive SEM ESPAÇO (fila de entrega)",
                         "pendente": "Drive: subindo", "erro": "Drive: erro na entrega (tento de novo)"}.get(r["entrega"], "Drive: ?")
                L.append(f"{icone['pronto']} {nome}: \"{tit}\" · publica {B.fmt_d(r['data_publicacao'])} · {drive} · US$ {usd:.2f}")
            elif r["status"] == "embalagem_reprovada":
                L.append(f"{icone['embalagem_reprovada']} {nome}: crivo reprovou \"{tema}\" (substituto abaixo, se houver)")
            else:
                s1, s2 = status_job(con, r["job_e1"]), status_job(con, r["job_e2"])
                det = r["obs"] or f"e1 {s1}, e2 {s2}"
                L.append(f"{icone.get(r['status'], '?')} {nome}: {tema} · {r['status']} ({det[:120]}) · publica {B.fmt_d(r['data_publicacao'])}")
        L.append(f"Custo da noite: US$ {total_usd:.2f} pago" + (f" · Max ~US$ {total_eq:.0f} equivalente" if total_eq else ""))
        txt = "\n".join(L)
        if a.dry_run:
            print(txt)
            return
        con.execute("UPDATE youtube.noites SET resumo_manha=%s, manha_em=now() WHERE noite=%s", (txt, noite))
        telegram(f"[fábrica] manhã {noite + timedelta(days=1):%d/%m}", txt, not a.sem_telegram)
        for canal in B.CANAIS:
            B.gerar_md(con, canal)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="c", required=True)
    p = sp.add_parser("planejar"); p.add_argument("--noite"); p.add_argument("--dry-run", action="store_true")
    p.add_argument("--forcar", action="store_true", help="roda mesmo se amanhã não for dia de publicação"); p.add_argument("--sem-telegram", action="store_true")
    p.add_argument("--canal")
    p = sp.add_parser("vigia"); p.add_argument("--sem-telegram", action="store_true")
    p = sp.add_parser("manha"); p.add_argument("--noite"); p.add_argument("--sem-telegram", action="store_true"); p.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    {"planejar": planejar, "vigia": vigia, "manha": manha}[a.c](a)


if __name__ == "__main__":
    main()
