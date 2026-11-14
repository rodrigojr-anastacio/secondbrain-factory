"""Garimpo em escala com a Batch API da Anthropic (50% mais barata): analisa em lote título, thumb, hook transcrito
e frames de muitos vídeos de concorrentes por rodada e acumula os padrões.

Uso (a partir do repo; a rotina de tendências chama sozinha depois do agente):
  tools/.venv/bin/python tools/garimpo_batch.py [--max 300] [--espera 40] [--modelo sonnet|haiku] [--so-coletar]
      [--sem-sintese] [--sem-commit] [--dry-run]

O que faz:
1. Coleta lotes pendentes de rodadas anteriores (pesquisa/tendencias/batch/pendente.json).
2. Escolhe até --max vídeos ainda não analisados de youtube.garimpo_videos (canais não descartados, sem Shorts,
   ordem de views) e monta 1 pedido por vídeo: título, canal (idade, inscritos, nº de vídeos), views, duração,
   thumb (URL hqdefault do i.ytimg.com) e, se o watch.py já assistiu o vídeo (pesquisa/tendencias/assets/*/<id>/),
   hook.txt, capítulos, cortes/min e o hook_sheet.jpg. Saída estruturada (output_config json_schema: com fórmula, gatilho,
   thumb, hook, edição, modelável…).
3. Envia o lote (Messages Batches) e espera até --espera minutos (consulta a cada 30 s). Se não terminar, grava em
   pendente.json e a próxima rodada coleta.
4. Resultados em pesquisa/tendencias/batch/<data>-<lote>.jsonl (estado: vídeo analisado não volta ao lote).
5. Síntese (1 chamada Sonnet, sem lote): agrupa por fórmula com números e escreve pesquisa/tendencias/<data>-batch.md
   e uma seção datada em conhecimento/padroes-garimpo.md (com fonte).
6. Custo real (tokens × preço; lote com 50%) em financas.consumo: 'batch:garimpo' e 'batch:garimpo-sintese'
   (chave ~/.segredos/anthropic/rotinas.env; teto mensal do grupo rotinas, tools/anthropic_api.py).
7. Commit só dos próprios arquivos (sem push). Códigos: 0 ok (ou lote pendente), 1 erro, 4 teto.
8. Teto do grupo rotinas ou API fora (14/11/2026): a Batch API não existe no Max, então a rodada cai 1× para o plano Max em
   modo reduzido (até --max-max vídeos, padrão 40, em claude -p de 20 vídeos; mesmo prompt/esquema, mesmo jsonl/banco/síntese;
   lote 'max-<data>-<hhmm>', modelo 'max:<modelo>'). Os vídeos que não couberem não são perdidos: continuam sem análise e
   entram na próxima rodada. Se o Max também falhar, só registra (ops.event_log) e segue.
"""
import argparse
import base64
import datetime as dt
import glob
import io
import json
import os
import statistics
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anthropic_api as A  # noqa: E402
import fallback_max as F  # noqa: E402
from db import conectar  # noqa: E402

FAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEND = os.path.join(FAB, "pesquisa", "tendencias")
BDIR = os.path.join(TEND, "batch")
PENDENTE = os.path.join(BDIR, "pendente.json")
PADROES = os.path.join(FAB, "conhecimento", "padroes-garimpo.md")

SISTEMA = """Você é analista de formatos do YouTube de uma fábrica de canais faceless (narração + imagens/mapas/animação, sem rosto).
Para cada vídeo de concorrente, analise o que foi observado (título, números, thumb, hook transcrito, frames) e responda só com o JSON
do esquema pedido. Seja concreto e curto. Separe o observado do inferido: se não houver hook/frames, deixe os campos de hook/edição
como "sem dado". Escreva em português do Brasil; cite trechos de título/hook no idioma original. A `formula` é a estrutura reutilizável
do título com variáveis (ex.: "The ENTIRE History of [PAÍS] in [N] Minutes", "Why Can't You Visit [LUGAR]?", "What's Still Under [LUGAR]?")."""

ESQUEMA = {
        "type": "object",
        "properties": {
            "formula": {"type": "string", "description": "estrutura reutilizável do título com [VARIÁVEIS], no idioma original"},
            "gatilho_titulo": {"type": "string", "description": "gatilho psicológico (curiosidade, proibido, escala, mistério, contagem…)"},
            "nicho": {"type": "string", "description": "nicho/tema em 2-5 palavras (ex.: história militar, geografia de lugares proibidos)"},
            "idioma": {"type": "string"},
            "thumb": {"type": "object", "properties": {
                "elementos": {"type": "string"}, "texto": {"type": "string", "description": "texto escrito na thumb (literal) ou 'nenhum'"},
                "cores": {"type": "string"}, "personagem": {"type": "string"}, "composicao": {"type": "string"}},
                "required": ["elementos", "texto", "cores", "personagem", "composicao"], "additionalProperties": False},
            "hook": {"type": "object", "properties": {
                "primeiras_frases": {"type": "string"}, "tecnica": {"type": "string"}},
                "required": ["primeiras_frases", "tecnica"], "additionalProperties": False},
            "edicao": {"type": "string", "description": "estilo visual (mapa 3D, IA ilustrada, stock, animação 2D…), ritmo de cortes, texto na tela"},
            "modelavel_faceless": {"type": "boolean"},
            "motivo_modelavel": {"type": "string"},
            "por_que_funciona": {"type": "string", "description": "1-2 frases"},
            "nota_formato": {"type": "integer", "description": "1 a 5: potencial de replicar o formato em canal novo (5 = muito)"},
        },
        "required": ["formula", "gatilho_titulo", "nicho", "idioma", "thumb", "hook", "edicao", "modelavel_faceless",
                     "motivo_modelavel", "por_que_funciona", "nota_formato"],
    "additionalProperties": False,
}


def log(*a):
    print("[garimpo_batch]", *a, file=sys.stderr, flush=True)


def sem_thumb():
    """Vídeos cujo pedido falhou ao baixar a thumb (URL): vão sem a imagem da URL na próxima rodada."""
    ids = set()
    for f in glob.glob(os.path.join(BDIR, "*.jsonl")):
        for linha in open(f, encoding="utf-8"):
            if '"ok": false' in linha and "download" in linha:
                try:
                    ids.add(json.loads(linha)["video_id"])
                except (json.JSONDecodeError, KeyError):
                    pass
    return ids


def ja_analisados():
    ids = set()
    for f in glob.glob(os.path.join(BDIR, "*.jsonl")):
        with open(f, encoding="utf-8") as fh:
            for linha in fh:
                try:
                    j = json.loads(linha)
                    if j.get("ok"):
                        ids.add(j["video_id"])
                except json.JSONDecodeError:
                    pass
    if os.path.exists(PENDENTE):
        for p in json.load(open(PENDENTE)):
            ids.update(p.get("ids", []))
    return ids


def candidatos(limite, excluir):
    sql = """
    WITH snap AS (
      SELECT DISTINCT ON (channel_id) channel_id, videos, inscritos, idade_dias, media_views
      FROM youtube.garimpo_snapshots ORDER BY channel_id, execucao_id DESC)
    SELECT v.video_id, v.titulo, v.publicado, v.duracao_min, v.views, c.titulo, c.channel_id, c.decisao, c.formula,
           c.primeiro_video, s.videos, s.inscritos, s.idade_dias, s.media_views
    FROM youtube.garimpo_videos v JOIN youtube.garimpo_canais c USING (channel_id) LEFT JOIN snap s USING (channel_id)
    WHERE COALESCE(c.decisao,'') <> 'descartar' AND COALESCE(v.duracao_min, 0) >= 3
      AND v.titulo NOT ILIKE '%%#shorts%%'
    ORDER BY v.views DESC NULLS LAST"""
    with conectar() as con:
        rows = con.execute(sql).fetchall()
    out = []
    for r in rows:
        if r[0] in excluir:
            continue
        out.append(dict(video_id=r[0], titulo=r[1], publicado=str(r[2]) if r[2] else None,
                        duracao_min=float(r[3]) if r[3] is not None else None, views=r[4], canal=r[5], channel_id=r[6],
                        decisao=r[7], formula_canal=r[8], primeiro_video=str(r[9]) if r[9] else None, n_videos=r[10],
                        inscritos=r[11], idade_dias=r[12], media_views=r[13]))
        if len(out) >= limite:
            break
    return out


def assets(video_id):
    pastas = sorted(glob.glob(os.path.join(TEND, "assets", "*", video_id)))
    return pastas[-1] if pastas else None


def img_b64(caminho, lado=1568):
    from PIL import Image
    im = Image.open(caminho).convert("RGB")
    im.thumbnail((lado, lado))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=82)
    return base64.b64encode(b.getvalue()).decode()


def montar_pedido(v, modelo, thumb_url=True):
    txt = [f"Vídeo {v['video_id']}: \"{v['titulo']}\"",
           f"Canal: {v['canal']} · 1º vídeo {v['primeiro_video'] or '?'} · {v['n_videos'] or '?'} vídeos · {v['inscritos'] or '?'} inscritos"
           f" · média {v['media_views'] or '?'} views/vídeo · decisão do garimpo: {v['decisao'] or 'sem'}"
           + (f" · fórmula anotada: {v['formula_canal']}" if v['formula_canal'] else ""),
           f"Views: {v['views']} · publicado {v['publicado']} · duração {v['duracao_min']} min"]
    conteudo = ([{"type": "image", "source": {"type": "url", "url": f"https://i.ytimg.com/vi/{v['video_id']}/hqdefault.jpg"}}]
                if thumb_url else [])
    pasta = assets(v["video_id"])
    if not thumb_url and pasta and os.path.exists(os.path.join(pasta, "thumb.jpg")):
        conteudo = [{"type": "image", "source": {"type": "base64", "media_type": "image/jpeg",
                                                 "data": img_b64(os.path.join(pasta, "thumb.jpg"), 800)}}]
    if pasta:
        try:
            info = json.load(open(os.path.join(pasta, "info.json"), encoding="utf-8"))
            caps = info.get("capitulos") or []
            caps = [c.get("title", c) if isinstance(c, dict) else c for c in caps][:20]
            txt.append(f"Capítulos: {caps}" if caps else "Capítulos: nenhum")
            txt.append(f"Cortes por minuto no início: {info.get('cortes_por_min_inicio')} · anúncios na página: {info.get('anuncios_na_pagina')}")
            if info.get("descricao"):
                txt.append("Descrição (início): " + str(info["descricao"])[:400])
        except Exception:  # noqa: BLE001
            pass
        hk = os.path.join(pasta, "hook.txt")
        if os.path.exists(hk):
            txt.append("Hook transcrito (primeiros 90 s):\n" + open(hk, encoding="utf-8").read()[:2500])
        hs = os.path.join(pasta, "hook_sheet.jpg")
        if os.path.exists(hs):
            conteudo.append({"type": "text", "text": "Frames do 1º minuto (1 a cada 3 s):"})
            conteudo.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64(hs)}})
    else:
        txt.append("Sem transcrição nem frames (só título, números e thumb).")
    conteudo.insert(0, {"type": "text", "text": "\n".join(txt)})
    return {"custom_id": f"v_{v['video_id']}", "params": {
        "model": A.modelo_id(modelo), "max_tokens": 4000,
        "system": [{"type": "text", "text": SISTEMA, "cache_control": {"type": "ephemeral"}}],
        "output_config": {"effort": "low", "format": {"type": "json_schema", "schema": ESQUEMA}},
        "messages": [{"role": "user", "content": conteudo}]}}


def salvar_pendente(lst):
    os.makedirs(BDIR, exist_ok=True)
    if lst:
        json.dump(lst, open(PENDENTE, "w"), ensure_ascii=False, indent=1)
    elif os.path.exists(PENDENTE):
        os.remove(PENDENTE)


def coletar(cli, pend, meta_por_id):
    """Baixa os resultados de um lote terminado; grava jsonl e o custo. Devolve a lista de análises ok."""
    b = cli.messages.batches.retrieve(pend["batch_id"])
    if b.processing_status != "ended":
        return None
    saida = os.path.join(BDIR, f"{pend['data']}-{pend['batch_id'][-8:]}.jsonl")
    ok, custo, tokens, erros = [], 0.0, 0, 0
    with open(saida, "w", encoding="utf-8") as fh:
        for r in cli.messages.batches.results(pend["batch_id"]):
            vid = r.custom_id[2:]
            linha = {"video_id": vid, "lote": pend["batch_id"], "data": pend["data"], "ok": False, **meta_por_id.get(vid, {})}
            if r.result.type == "succeeded":
                m = r.result.message
                custo += A.custo_usd(m.model, m.usage, batch=True)
                tokens += A.tokens_total(m.usage)
                txt = "".join(c.text for c in m.content if c.type == "text")
                try:
                    linha.update(ok=True, modelo=m.model, analise=json.loads(txt))
                    ok.append(linha)
                except json.JSONDecodeError:
                    erros += 1
                    linha["erro"] = f"json inválido ({m.stop_reason}): {txt[:200]}"
            else:
                erros += 1
                linha["erro"] = r.result.type + ": " + str(getattr(getattr(r.result, "error", None), "error", ""))[:300]
            fh.write(json.dumps(linha, ensure_ascii=False) + "\n")
    try:
        log(f"banco: {gravar_banco(ok)} análises novas em youtube.garimpo_analises")
    except Exception as e:  # noqa: BLE001
        log(f"AVISO: não gravei no banco ({type(e).__name__}: {str(e)[:200]}); o jsonl segue e `--importar` refaz")
    A.registrar_consumo(custo, "batch:garimpo", tokens, "tokens",
                        notas=f"garimpo_batch.py lote {pend['batch_id']} ({pend['data']}): {len(ok)} ok, {erros} erros; preço de lote (50%)")
    log(f"lote {pend['batch_id']}: {len(ok)} ok, {erros} erros, {tokens} tokens, US$ {custo:.4f} → {os.path.relpath(saida, FAB)}")
    return ok, saida, custo


SCHEMA_SQL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db", "schema_garimpo_analises.sql")


def gravar_banco(linhas):
    """Grava as análises (linhas dos jsonl com ok=True) em youtube.garimpo_analises. Idempotente (video_id+lote)."""
    from psycopg.types.json import Jsonb
    n = 0
    with conectar() as con:
        con.execute(open(SCHEMA_SQL, encoding="utf-8").read())
        for l in linhas:
            if not l.get("ok"):
                continue
            an = l["analise"]
            th, hk = an.get("thumb") or {}, an.get("hook") or {}
            r = con.execute(
                "INSERT INTO youtube.garimpo_analises (video_id, lote, channel_id, analisado_em, modelo, titulo, canal,"
                " formula, gatilho_titulo, nicho, idioma, thumb_elementos, thumb_texto, thumb_cores, thumb_personagem,"
                " thumb_composicao, hook_frases, hook_tecnica, edicao, modelavel_faceless, motivo_modelavel,"
                " por_que_funciona, nota_formato, views, duracao_min, json_completo)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                " ON CONFLICT (video_id, lote) DO NOTHING",
                (l["video_id"], l["lote"], l.get("channel_id"), l.get("data"), l.get("modelo"), l.get("titulo"),
                 l.get("canal"), an.get("formula"), an.get("gatilho_titulo"), an.get("nicho"), an.get("idioma"),
                 th.get("elementos"), th.get("texto"), th.get("cores"), th.get("personagem"), th.get("composicao"),
                 hk.get("primeiras_frases"), hk.get("tecnica"), an.get("edicao"), an.get("modelavel_faceless"),
                 an.get("motivo_modelavel"), an.get("por_que_funciona"), an.get("nota_formato"), l.get("views"),
                 l.get("duracao_min"), Jsonb(l)))
            n += r.rowcount
    return n


def agregar(analises):
    grupos = {}
    for a in analises:
        f = (a["analise"].get("formula") or "?").strip()
        chave = f.lower()
        g = grupos.setdefault(chave, {"formula": f, "videos": [], "canais": set()})
        g["videos"].append(a)
        g["canais"].add(a.get("canal") or "?")
    linhas = []
    for g in grupos.values():
        views = [x.get("views") or 0 for x in g["videos"]]
        linhas.append({"formula": g["formula"], "n_videos": len(views), "n_canais": len(g["canais"]),
                       "canais": sorted(g["canais"])[:6], "views_mediana": int(statistics.median(views)) if views else 0,
                       "views_max": max(views) if views else 0,
                       "modelavel": sum(1 for x in g["videos"] if x["analise"].get("modelavel_faceless")),
                       "nota_media": round(statistics.mean([x["analise"].get("nota_formato") or 0 for x in g["videos"]]), 1)})
    linhas.sort(key=lambda x: (x["n_canais"], x["views_mediana"]), reverse=True)
    return linhas


def pedido_sintese(analises, data, lotes, via="Batch API"):
    agreg = agregar(analises)
    compacto = []
    for a in sorted(analises, key=lambda x: -(x.get("views") or 0)):
        an = a["analise"]
        compacto.append({"id": a["video_id"], "t": a.get("titulo"), "canal": a.get("canal"), "views": a.get("views"),
                         "min": a.get("duracao_min"), "idade_canal_d": a.get("idade_dias"), "insc": a.get("inscritos"),
                         "formula": an.get("formula"), "gatilho": an.get("gatilho_titulo"), "nicho": an.get("nicho"),
                         "thumb": an.get("thumb"), "hook": an.get("hook"), "edicao": an.get("edicao"),
                         "modelavel": an.get("modelavel_faceless"), "nota": an.get("nota_formato"),
                         "porque": an.get("por_que_funciona")})
    pedido = f"""Data: {data}. Lotes: {', '.join(lotes)}. {len(analises)} vídeos de concorrentes analisados em lote ({via}) nesta rodada.

Agregado por fórmula (calculado em Python, números observados):
{json.dumps(agreg[:40], ensure_ascii=False)}

Análises por vídeo (ordem de views):
{json.dumps(compacto, ensure_ascii=False)}

Escreva em português do Brasil, em markdown, curto e com números:
## Resumo (3 linhas)
## Fórmulas que mais rendem (tabela: fórmula | canais | vídeos | views mediana | modelável faceless? | nota)  — até 10
## Padrões de título (estruturas e gatilhos que se repetem em ≥ 2 canais, com nº de canais/vídeos e exemplo literal)
## Padrões de thumb (o que se repete nas thumbs dos vídeos de mais views; texto, cores, composição)
## Técnicas de hook (só dos vídeos com transcrição; cite a frase real e o vídeo)
## Edição (estilos visuais e ritmo observados nos frames)
## Para a fábrica (até 5 bullets: o que testar, em qual canal nosso ou canal novo; marque Hipótese quando for inferência)
Depois, uma linha só com `---PADROES---` e, abaixo, de 5 a 8 bullets curtos (1 linha cada) com os padrões mais fortes desta rodada para o
arquivo acumulado, cada um com o número que o sustenta (ex.: "Títulos 'What's Still Under X?' — 3 canais, mediana 210 mil views")."""
    return pedido, agreg


def sintese(cli, analises, data, lotes, modelo="sonnet"):
    pedido, agreg = pedido_sintese(analises, data, lotes)
    with cli.messages.stream(model=A.modelo_id(modelo), max_tokens=24000, output_config={"effort": "medium"},
                             messages=[{"role": "user", "content": pedido}]) as st:
        m = st.get_final_message()
    custo = A.custo_usd(m.model, m.usage)
    A.registrar_consumo(custo, "batch:garimpo-sintese", A.tokens_total(m.usage), "tokens",
                        notas=f"garimpo_batch.py síntese {data} ({len(analises)} vídeos; {m.model})")
    texto = "".join(c.text for c in m.content if c.type == "text")
    log(f"síntese {m.model}: US$ {custo:.4f} · stop={m.stop_reason} · blocos={[c.type for c in m.content]} · saída {m.usage.output_tokens} tokens")
    if not texto.strip():
        raise RuntimeError(f"síntese sem texto (stop_reason={m.stop_reason})")
    corpo, _, padroes = texto.partition("---PADROES---")
    return corpo.strip(), padroes.strip(), agreg, custo


def escrever(data, corpo, padroes, analises, lotes, custo_total, jsonls):
    md = os.path.join(TEND, f"{data}-batch.md")
    cab = (f"# Garimpo em lote (Batch API) — {data}\n\n"
           f"{len(analises)} vídeos de concorrentes (youtube.garimpo_videos, canais não descartados, sem Shorts) analisados por "
           f"{analises[0].get('modelo', '?') if analises else '?'} em lote; lotes {', '.join(lotes)}; custo US$ {custo_total:.3f}. "
           f"Dados por vídeo: {', '.join(os.path.relpath(j, FAB) for j in jsonls)}. Gerado por `tools/garimpo_batch.py`.\n\n")
    with open(md, "w", encoding="utf-8") as f:
        f.write(cab + corpo + "\n")
    novo = not os.path.exists(PADROES)
    with open(PADROES, "a", encoding="utf-8") as f:
        if novo:
            f.write("# Padrões do garimpo em lote (acumulado)\n\n"
                    "> **Observação de concorrentes, não regra de canal.** Regra de canal está em `canais/<slug>/biblia/` e sempre prevalece. "
                    "Cada seção é uma rodada do `tools/garimpo_batch.py` (Batch API, rotina de tendências seg/qui), com data e fonte; "
                    "o que é inferência fica como **Hipótese**. Padrão que se repete em várias rodadas pode virar regra (em `conhecimento/` "
                    "se for geral, na bíblia se for de um formato nosso).\n")
        f.write(f"\n## {data} — {len(analises)} vídeos\n{padroes}\n- Fonte: `pesquisa/tendencias/{data}-batch.md`.\n")
    return md


def commit(caminhos, msg):
    rel = [os.path.relpath(c, FAB) for c in caminhos if c and os.path.exists(c)]
    if os.path.exists(PENDENTE):
        rel.append(os.path.relpath(PENDENTE, FAB))
    for _ in range(10):
        p = subprocess.run(["git", "add", "--", *rel], cwd=FAB, capture_output=True, text=True)
        if p.returncode == 0:
            break
        if "index.lock" in p.stderr:
            time.sleep(5)
            continue
        log("git add falhou:", p.stderr.strip()[:300])
        return False
    for _ in range(10):
        p = subprocess.run(["git", "commit", "-m", msg, "--", *rel], cwd=FAB, capture_output=True, text=True)
        if p.returncode == 0 or "nothing to commit" in p.stdout + p.stderr:
            return True
        if "index.lock" in p.stderr:
            time.sleep(5)
            continue
        log("git commit falhou:", (p.stdout + p.stderr).strip()[:300])
        return False
    return False


MAX_LOTE = 20  # vídeos por claude -p no fallback


def pedido_max(v, modelo, d):
    """Texto do pedido de um vídeo para o Max: o mesmo conteúdo do pedido da Batch API; imagens viram arquivos (Read)."""
    import urllib.request
    p = montar_pedido(v, modelo, thumb_url=True)
    partes, n = [], 0
    for c in p["params"]["messages"][0]["content"]:
        if c["type"] == "text":
            partes.append(c["text"])
            continue
        n += 1
        arq = os.path.join(d, f"{v['video_id']}-{n}.jpg")
        try:
            if c["source"]["type"] == "url":
                urllib.request.urlretrieve(c["source"]["url"], arq)
            else:
                open(arq, "wb").write(base64.b64decode(c["source"]["data"]))
            partes.append(f"[imagem {n} (thumb ou frames): {arq}]")
        except Exception as e:  # noqa: BLE001
            partes.append(f"[imagem {n} indisponível ({type(e).__name__})]")
    return "\n".join(partes)


def rodada_max(a, data, motivo):
    """Fallback para o plano Max (modo reduzido). Devolve o dict de resumo da rodada ou None se nada foi analisado."""
    log(f"caindo para o Max ({motivo}): até {a.max_max} vídeos, {MAX_LOTE} por claude -p")
    novos = [] if a.so_coletar else candidatos(a.max_max, ja_analisados())
    if not novos:
        log("Max: nada novo para analisar")
        return None
    d = F.tmp_dir("garimpo-max")
    hora = dt.datetime.now().strftime("%H%M")
    lote_id = f"max-{data}-{hora}"
    ok, erros = [], 0
    for k in range(0, len(novos), MAX_LOTE):
        parte = novos[k:k + MAX_LOTE]
        saida = os.path.join(d, f"analises-{os.getpid()}-{k}.jsonl")
        pedidos = "\n\n=====\n\n".join(pedido_max(v, a.modelo, d) for v in parte)
        prompt = (SISTEMA + "\n\n# Tarefa (modo Max)\nAnalise os " + str(len(parte)) + " vídeos abaixo, um a um. Para as imagens indicadas, use a ferramenta Read no "
                  "caminho. Não leia nem altere mais nada. Grave com a ferramenta Write, em " + saida + ", um JSON por linha (JSONL, sem markdown), "
                  'cada linha {"video_id": "<id>", "analise": <objeto no esquema abaixo>}. Esquema de "analise":\n'
                  + json.dumps(ESQUEMA, ensure_ascii=False) + "\nResponda no chat apenas 'ok'.\n\n# Vídeos\n\n" + pedidos)
        txt = F.rodar_max_json("batch", "job-garimpo-fallback", prompt, saida, a.modelo, timeout=3600, ref=lote_id, max_turns=150,
                               motivo=motivo, detalhes={"videos": len(parte)})
        por_id = {v["video_id"]: v for v in parte}
        achou = set()
        for linha in (txt or "").splitlines():
            try:
                j = json.loads(linha)
                an = j["analise"]
                v = por_id[j["video_id"]]
                if not all(c in an for c in ESQUEMA["required"]):
                    raise KeyError("campos faltando")
            except (json.JSONDecodeError, KeyError, TypeError):
                continue
            achou.add(v["video_id"])
            meta = {c: v[c] for c in ("titulo", "canal", "channel_id", "views", "duracao_min", "publicado", "idade_dias", "inscritos", "n_videos")}
            ok.append({"video_id": v["video_id"], "lote": lote_id, "data": data, "ok": True, **meta, "modelo": f"max:{a.modelo}", "analise": an})
        erros += len(parte) - len(achou)
    if not ok:
        return None
    os.makedirs(BDIR, exist_ok=True)
    jsonl = os.path.join(BDIR, f"{data}-max{hora}.jsonl")
    with open(jsonl, "w", encoding="utf-8") as fh:
        for l in ok:
            fh.write(json.dumps(l, ensure_ascii=False) + "\n")
    try:
        log(f"banco: {gravar_banco(ok)} análises novas em youtube.garimpo_analises")
    except Exception as e:  # noqa: BLE001
        log(f"AVISO: não gravei no banco ({type(e).__name__}: {str(e)[:200]}); `--importar` refaz")
    log(f"Max: {len(ok)} ok, {erros} sem análise (voltam na próxima rodada) → {os.path.relpath(jsonl, FAB)}")
    md = None
    if not a.sem_sintese:
        saida = os.path.join(d, f"sintese-{os.getpid()}.md")
        pedido, _ = pedido_sintese(ok, data, [lote_id], via="plano Max, modo reduzido")
        prompt = (pedido + "\n\nGrave o texto completo (markdown, incluindo a linha ---PADROES---) com a ferramenta Write em " + saida
                  + ". Não use outras ferramentas. Responda no chat apenas 'ok'.")
        txt = F.rodar_max_json("batch", "job-garimpo-fallback", prompt, saida, "sonnet", timeout=2400, ref=lote_id, max_turns=20,
                               motivo=motivo, detalhes={"fase": "sintese"})
        if txt and txt.strip():
            corpo, _, padroes = txt.partition("---PADROES---")
            md = escrever(data, corpo.strip(), padroes.strip(), ok, [lote_id], 0.0, [jsonl])
            log(f"relatório (Max) → {os.path.relpath(md, FAB)}")
        else:
            log("síntese pelo Max falhou; análises ficam no jsonl")
    if not a.sem_commit:
        commit([jsonl] + ([md, PADROES] if md else []),
               f"garimpo em lote {data}: {len(ok)} vídeos analisados pelo plano Max (fallback, modo reduzido)")
    return {"analisados": len(ok), "lotes": [lote_id], "pendentes": [], "custo_usd": 0, "fallback": "max",
            "relatorio": os.path.relpath(md, FAB) if md else None}


def sem_bloqueio(a, data, tipo, texto):
    """Teto/API fora: tenta o Max; se também falhar, registra e segue sem bloquear."""
    res = None
    try:
        res = rodada_max(a, data, tipo)
    except Exception as e:  # noqa: BLE001
        F.registrar("batch", "fallback_falhou", "erro", f"fallback do garimpo falhou: {type(e).__name__}: {str(e)[:200]}", {"motivo": tipo})
    if res is None:
        F.registrar("batch", "info", "aviso", f"garimpo em lote não rodou ({tipo}); Max também sem análise", {"motivo": texto[:200]})
        res = {"analisados": 0, "lotes": [], "pendentes": [], "custo_usd": 0, "relatorio": None, "erro": tipo}
    print(json.dumps(res, ensure_ascii=False))


def main():
    """Falha da API (chave, crédito, 5xx/overload) ou teto: registra em ops.event_log e cai 1× para o Max em modo reduzido
    (rodada_max); só se o Max também falhar segue sem bloquear (a próxima rodada tenta de novo)."""
    try:
        _main()
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001
        texto = f"{type(e).__name__}: {str(e)[:300]}"
        tipo = F.classificar(texto)
        if tipo is None and type(e).__module__.startswith("anthropic"):
            tipo = "api_erro"
        if tipo is None:
            raise
        F.registrar_falha("batch", tipo, texto, "rotinas", None)
        log(f"API falhou ({tipo}): {texto}")
        sem_bloqueio(_ARGS[0], dt.date.today().isoformat(), tipo, texto)


_ARGS = [None]


def _main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--max", type=int, default=300)
    ap.add_argument("--max-max", type=int, default=40, help="vídeos por rodada no fallback para o plano Max (modo reduzido)")
    ap.add_argument("--espera", type=int, default=40, help="minutos esperando o lote terminar (depois fica pendente)")
    ap.add_argument("--modelo", default="sonnet")
    ap.add_argument("--so-coletar", action="store_true", help="só coleta lotes pendentes")
    ap.add_argument("--sem-sintese", action="store_true")
    ap.add_argument("--sem-commit", action="store_true")
    ap.add_argument("--sintese-de", nargs="+", metavar="JSONL", help="refaz só a síntese a partir de jsonl já coletados")
    ap.add_argument("--importar", action="store_true", help="importa para o banco todos os jsonl já coletados (sem duplicar)")
    ap.add_argument("--dry-run", action="store_true", help="mostra quantos vídeos iriam e o 1º pedido (sem imagem), sem gastar")
    a = ap.parse_args()
    _ARGS[0] = a
    os.makedirs(BDIR, exist_ok=True)
    data = dt.date.today().isoformat()

    if a.importar:
        linhas = [json.loads(l) for f in sorted(glob.glob(os.path.join(BDIR, "*.jsonl"))) for l in open(f, encoding="utf-8") if l.strip()]
        print(json.dumps({"jsonl_ok": sum(1 for x in linhas if x.get("ok")), "novas_no_banco": gravar_banco(linhas)}))
        return

    if a.sintese_de:
        analises = [json.loads(l) for f in a.sintese_de for l in open(f, encoding="utf-8") if l.strip()]
        analises = [x for x in analises if x.get("ok")]
        lotes = sorted({x["lote"] for x in analises})
        corpo, padroes, _, c = sintese(A.cliente("rotinas"), analises, data, lotes)
        md = escrever(data, corpo, padroes, analises, lotes, c, [os.path.abspath(f) for f in a.sintese_de])
        if not a.sem_commit:
            commit([md, PADROES], f"garimpo em lote {data}: síntese de {len(analises)} vídeos (Batch API)")
        print(json.dumps({"analisados": len(analises), "lotes": lotes, "pendentes": [], "custo_usd": round(c, 4),
                          "relatorio": os.path.relpath(md, FAB)}, ensure_ascii=False))
        return

    excluir = ja_analisados()
    novos = [] if a.so_coletar else candidatos(a.max, excluir)
    if a.dry_run:
        print(f"{len(novos)} vídeos novos (já analisados: {len(excluir)})")
        if novos:
            p = montar_pedido(novos[0], a.modelo)
            print(json.dumps([c if c["type"] == "text" else {"type": "image"} for c in p["params"]["messages"][0]["content"]], ensure_ascii=False, indent=1)[:3000])
        return

    # previsão conservadora: ~US$ 0,01 por vídeo no Sonnet em lote (+ síntese ~US$ 0,15)
    try:
        A.checar_teto("rotinas", previsto=len(novos) * (0.01 if "sonnet" in a.modelo else 0.002) + 0.2)
    except A.TetoExcedido as e:
        log("AVISO: teto mensal do grupo rotinas; caindo para o Max (modo reduzido):", e)
        sem_bloqueio(a, data, "teto_atingido", str(e))
        return
    cli = A.cliente("rotinas")
    pendentes = json.load(open(PENDENTE)) if os.path.exists(PENDENTE) else []
    if novos:
        falhou_thumb = sem_thumb()
        reqs = [montar_pedido(v, a.modelo, thumb_url=v["video_id"] not in falhou_thumb) for v in novos]
        b = cli.messages.batches.create(requests=reqs)
        log(f"lote {b.id} enviado: {len(reqs)} vídeos ({A.modelo_id(a.modelo)})")
        meta = {v["video_id"]: {k: v[k] for k in ("titulo", "canal", "channel_id", "views", "duracao_min", "publicado",
                                                    "idade_dias", "inscritos", "n_videos")} for v in novos}
        pendentes.append({"batch_id": b.id, "data": data, "ids": [v["video_id"] for v in novos], "meta": meta})
        salvar_pendente(pendentes)
    if not pendentes:
        log("nada novo para analisar e nenhum lote pendente")
        return

    limite = time.monotonic() + a.espera * 60
    analises, lotes, jsonls, custo_total = [], [], [], 0.0
    while pendentes and time.monotonic() < limite:
        for p in list(pendentes):
            r = coletar(cli, p, p.get("meta", {}))
            if r is not None:
                ok, saida, custo = r
                analises += ok
                lotes.append(p["batch_id"])
                jsonls.append(saida)
                custo_total += custo
                pendentes.remove(p)
                salvar_pendente(pendentes)
        if pendentes:
            time.sleep(30)
    if pendentes:
        log(f"{len(pendentes)} lote(s) ainda processando; ficam em {os.path.relpath(PENDENTE, FAB)} para a próxima rodada")

    md = None
    if analises and not a.sem_sintese:
        try:
            corpo, padroes, _, c = sintese(cli, analises, data, lotes)
            custo_total += c
            md = escrever(data, corpo, padroes, analises, lotes, custo_total, jsonls)
            log(f"relatório → {os.path.relpath(md, FAB)}")
        except Exception as e:  # noqa: BLE001
            log(f"síntese falhou ({type(e).__name__}: {str(e)[:300]}); análises ficam nos jsonl")
    if not a.sem_commit and (jsonls or md or os.path.exists(PENDENTE)):
        commit(jsonls + ([md, PADROES] if md else []),
               f"garimpo em lote {data}: {len(analises)} vídeos analisados (Batch API), padrões em conhecimento/padroes-garimpo.md")
    print(json.dumps({"analisados": len(analises), "lotes": lotes, "pendentes": [p["batch_id"] for p in pendentes],
                      "custo_usd": round(custo_total, 4), "relatorio": os.path.relpath(md, FAB) if md else None}, ensure_ascii=False))


if __name__ == "__main__":
    main()
