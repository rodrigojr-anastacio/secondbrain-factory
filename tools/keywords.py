"""Rotina semanal de palavras-chave (quarta 09:30): termos e padrões de busca em alta no YouTube → sugestões.

Uso: ~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/tools/keywords.py
       [--termos 10] [--termos-exploracao 10] [--max-cota 2500] [--teste] [--sem-validar] [--sem-banco]
       [--sem-exploracao] [--categorias a,b] [--sufixo v2]

1. Descoberta (grátis): autocomplete do YouTube (suggestqueries, via WARP socks5://127.0.0.1:40000, com pausa)
   a partir de pesquisa/keyword_seeds.yaml (sementes por idioma, expandidas com " a" … " z", + temas do backlog).
2. Padrões de título: n-gramas de 2–4 palavras (dígitos viram N) dos títulos de youtube.garimpo_videos, do último
   garimpo (pesquisa/tendencias/<data>.json) e dos resultados da validação, por idioma, pesados por views/dia de vida.
3. Validação (cota): 10 termos nossos (+ 10 da exploração, item 3b), search.list (100 un.) + videos.list (1 un.): mediana de views do
   top-10 (12 meses), vídeos < 90 dias com > 100 mil e vídeos que já usam um molde nosso. Para no teto de cota.
   Idade do canal = data do 1º vídeo público (playlist de uploads, playlistItems.list 1 un./página; cache em
   youtube.canais_idade); canal com > 200 vídeos não é novo; erro/teto → data de criação (idade_fonte = 'criacao').
3b. EXPLORAÇÃO (fora do nosso nicho; Rodrigo, 06/11/2026): em alta por país (videos.list chart=mostPopular, só longos
   > 4 min, + Google Trends diário por RSS), sementes genéricas que giram por semana (keyword_seeds.yaml: exploracao) e
   caça a outliers: os 10 melhores termos de exploração passam por search.list com publishedAfter = 30 dias; vídeo de
   canal novo (1º vídeo < 90 dias) com ≥ 30 mil views e views/inscritos ≥ 3 = outlier (origem exploracao_outlier).
4. Grava em youtube.palavras_chave (tools/db/schema_palavras_chave.sql) com a tendência contra a execução anterior
   e salva pesquisa/palavras-chave/<data>.json e .md.
--teste: só sementes "simples", do backlog e das categorias (sem a–z), valida 2 + 2 termos (≤ 600 un.), não grava no
banco, sufixo -teste. Em 2 partes (cada comando do Bash do Claude tem teto de 10 min): --so-descoberta (autocomplete,
~6 min, grátis) e depois --descoberta <data>-descoberta.json (em alta + validação + banco + relatório, ~1 min).
Só leitura no YouTube. O token é o mesmo do garimpo (trends.py).
"""
import argparse
import datetime as dt
import json
import math
import os
import random
import re
import statistics
import subprocess
import sys
import time
import unicodedata
import urllib.parse
from collections import defaultdict

import yaml

from _paths import PESQUISA, TENDENCIAS
from db import Jsonb, conectar

PROXY = "127.0.0.1:40000"  # WARP (o YouTube bloqueia o IP da VPS)
SEEDS = os.path.join(PESQUISA, "keyword_seeds.yaml")
OUT = os.path.join(PESQUISA, "palavras-chave")
GL = {"en": "US", "es": "MX", "pt": "BR", "fr": "FR"}
CUSTO_SEARCH, CUSTO_VIDEOS, CUSTO_CANAIS = 100, 1, 1
CUSTO_TERMO = CUSTO_SEARCH + CUSTO_VIDEOS + CUSTO_CANAIS
NOVO_DIAS = 90  # canal "novo" = 1º vídeo público há menos de 90 dias (Rodrigo, 06/11/2026; era criação < 12 meses)
MAX_VIDEOS_NOVO = 200  # canal com mais vídeos que isso não é novo: não pagina o playlist de uploads
JANELA_NOSSOS, JANELA_EXPLORACAO = 365, 30  # dias da busca de validação (exploração = "em alta agora")
LONGO_EXPLORACAO = 240  # exploração: só vídeos > 4 min (Shorts vão até 3 min)
OUTLIER_VIEWS, OUTLIER_VPI = 30_000, 3  # outlier = canal novo com ≥ 30 mil views e views/inscritos ≥ 3
DESTINOS = ("dossie-es", "historia-ptbr", "lotr-fr", "novo-canal")


class Cota:
    """Conta as unidades da YouTube Data API gastas nesta execução (search 100, o resto 1) contra o teto."""
    def __init__(self, teto):
        self.teto, self.gasto, self.por_tipo, self.avisou = teto, 0, defaultdict(int), False

    def cabe(self, n, reserva=0):
        return self.gasto + n + reserva <= self.teto

    def gastar(self, n, tipo):
        self.gasto += n
        self.por_tipo[tipo] += n

STOP = {
    "en": "the a an of in on to and or is was were be for with how why what who when did does do you your it its this that "
          "from at by as are they them their his her he she we our i my me if not no all every".split(),
    "es": "el la los las un una de del en y o que es se por para con como su sus al lo le les qué cómo por qué fue "
          "este esta ese esa son era más muy tu te mi si no".split(),
    "pt": "o a os as um uma de do da dos das em no na nos nas e ou que é se por para com como seu sua ao à foi "
          "este esta esse essa são era mais muito você te meu se não".split(),
    "fr": "le la les un une de du des en et ou que qui est se par pour avec comme son sa ses au aux l d il elle "
          "ce cette sont était plus très tu te mon si ne pas".split(),
}
# palavras que só existem (quase) num idioma: usadas para adivinhar o idioma de um título
MARCAS = {
    "en": "the of and how why what history entire every explained story world was who".split(),
    "es": "la del los las historia cómo qué por toda completa mundo fue cuando su más".split(),
    "pt": "do da dos das história como que por toda inteira mundo foi quando você não".split(),
    "fr": "le du des les histoire comment pourquoi toute complète monde était quand vous".split(),
}


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def tem_palavra(texto_norm, palavras):
    """Palavra inteira, aceitando plural simples (templario → templarios)."""
    return any(re.search(r"(?<![a-z0-9])" + re.escape(norm(p).strip()) + r"(?:e?s)?(?![a-z0-9])", texto_norm)
               for p in palavras if p.strip())


GENERICAS = set("historia history histoire story toda entire complete completa complète completo inteira whole minutos minutes "
                "minutes explained explicado explique documentary documental documentaire".split())


def tokens_conteudo(termo, lang):
    stop = {norm(w) for w in STOP.get(lang, [])}
    return [w for w in re.findall(r"[a-z0-9']+", norm(termo)) if w not in stop and norm(w) not in GENERICAS and len(w) > 1]


HISTORICAS = ("histor", "documental", "documentar", "documentaire", "origen", "origem", "origine", "lore", "explained",
              "explicad", "explique", "minutos", "minutes")


def relevante(titulo, toks, termo, lang):
    """O título tem as palavras do termo, não está claramente em outro idioma e, se o termo é de "história de X",
    é vídeo de história/documentário (tira jogo da Copa em "história do Egito")."""
    tn = norm(titulo)
    if not all(re.search(r"(?<![a-z0-9])" + re.escape(w), tn) for w in toks):
        return False
    il = idioma_titulo(titulo)
    if il and il != lang:
        return False
    if "histor" in norm(termo) and not any(h in tn for h in HISTORICAS):
        return False
    return True


def segundos(iso):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    d, h, mi, se = (int(x) if x else 0 for x in m.groups()) if m else (0, 0, 0, 0)
    return d * 86400 + h * 3600 + mi * 60 + se


# ---------- 1. autocomplete ----------
def autocomplete(q, hl, falhas):
    url = "https://suggestqueries.google.com/complete/search?" + urllib.parse.urlencode(
        {"client": "youtube", "ds": "yt", "hl": hl, "gl": GL.get(hl, "US"), "oe": "utf-8", "q": q})
    for tentativa in range(2):
        r = subprocess.run(["curl", "-s", "-m", "20", "--socks5-hostname", PROXY, url], capture_output=True)
        txt = r.stdout.decode("utf-8", "replace")
        m = re.search(r"\((\[.*\])\)\s*$", txt, re.S)
        if r.returncode == 0 and m:
            try:
                return [s[0] for s in json.loads(m.group(1))[1]]
            except (ValueError, IndexError, TypeError):
                pass
        time.sleep(2 + tentativa * 3)
    falhas.append(q)
    return None


AZ = "abcdefghijklmnopqrstuvwxyz"


WORKERS = 3  # chamadas de autocomplete em paralelo (cada uma com pausa de 0,35–0,65 s): ~4/s em vez de ~1,4/s


def coletar(consultas, origem, termos, est, log):
    """consultas = [(idioma, q, é_base, categoria)]; acumula as sugestões em termos[(idioma, termo)].
    est = {"chamadas": n, "falhas": [...]}; devolve False se abortou (WARP fora). Busca em paralelo (WORKERS), em lotes
    de 30 para poder abortar cedo; a agregação é na ordem das consultas (determinística)."""
    from concurrent.futures import ThreadPoolExecutor

    def uma(c):
        r = autocomplete(c[1], c[0], est["falhas"])
        time.sleep(0.35 + random.random() * 0.3)
        return r

    resultados = []
    with ThreadPoolExecutor(WORKERS) as pool:
        for i in range(0, len(consultas), 30):
            if len(est["falhas"]) >= 10 and est["chamadas"] <= len(est["falhas"]) * 2:
                log.append(f"autocomplete abortado ({origem}): {len(est['falhas'])} falhas (WARP fora?)")
                break
            lote = consultas[i:i + 30]
            resultados += zip(lote, pool.map(uma, lote))
            est["chamadas"] += len(lote)
    for (lang, q, base, cat), sugestoes in resultados:
        if not sugestoes:
            continue
        n = max(len(sugestoes), 10)
        for pos, s in enumerate(sugestoes):
            s = re.sub(r"\s+", " ", s.strip().lower())
            if len(s) < 4:
                continue
            t = termos.setdefault((lang, s), {"idioma": lang, "termo": s, "origem": origem, "aparicoes": 0,
                                              "melhor_posicao": 99, "bruto": 0.0, "sementes": set(), "categoria": cat})
            if cat and (not t.get("categoria") or str(t["categoria"]).startswith("formato:")) and not cat.startswith("formato:"):
                t["categoria"] = cat  # categoria temática vence o formato aberto
            t["aparicoes"] += 1
            t["melhor_posicao"] = min(t["melhor_posicao"], pos + 1)
            t["bruto"] += (1 - pos / n) * (2 if base else 1)
            t["sementes"].add(q)
    return len(resultados) == len(consultas)


def descobrir(cfg, teste, log):
    termos, est = {}, {"chamadas": 0, "falhas": []}
    for lang, grupos in cfg["idiomas"].items():
        consultas = []
        if not teste:
            for s in grupos.get("expandir", []):
                consultas.append((lang, s, True, None))
                consultas += [(lang, f"{s} {c}", False, None) for c in AZ]
        consultas += [(lang, s, True, None) for s in grupos.get("simples", [])]
        consultas += [(lang, s, True, None) for s in cfg.get("backlog", {}).get(lang, [])]
        if not coletar(consultas, "autocomplete", termos, est, log):
            break
    for t in termos.values():
        t["categoria"] = None
    return termos, est["chamadas"], est["falhas"]


def rodizio(cfg, hoje, categorias=None):
    """Categorias e formatos da exploração desta semana (semana ISO % ciclos; formatos em 2 metades)."""
    ex = cfg.get("exploracao") or {}
    todas = list(ex.get("categorias", {}))
    k = int(ex.get("categorias_por_semana", 4))
    semana = hoje.isocalendar()[1]
    ciclos = max(1, math.ceil(len(todas) / k))
    b = semana % ciclos
    ativas = categorias or todas[b * k:(b + 1) * k]
    return {"semana": semana, "bloco": b, "ciclos": ciclos, "categorias": ativas, "metade_formatos": semana % 2}


def descobrir_exploracao(cfg, rod, teste, log):
    """Autocomplete das sementes genéricas (fora do nosso nicho): formatos abertos a–z (metade da semana) + sementes das
    categorias ativas, sozinhas e prefixadas pelos formatos de "combinar". Origem exploracao_semente."""
    ex = cfg.get("exploracao") or {}
    termos, est, consultas = {}, {"chamadas": 0, "falhas": []}, []
    for lang, f in ex.get("formatos", {}).items():
        if not teste:
            for s in f.get("expandir", [])[rod["metade_formatos"]::2]:
                consultas.append((lang, s, True, "formato:" + s))
                consultas += [(lang, f"{s} {c}", False, "formato:" + s) for c in AZ]
        for cat in rod["categorias"]:
            for s in ex["categorias"].get(cat, {}).get(lang, []):
                consultas.append((lang, s, True, cat))
                consultas += [(lang, f"{p} {s}", True, cat) for p in f.get("combinar", [])]
    coletar(consultas, "exploracao_semente", termos, est, log)
    return termos, est["chamadas"], est["falhas"]


def efemero_texto(texto, cfg):
    tn = " " + norm(texto) + " "
    return any(norm(w) in tn for w in (cfg.get("exploracao") or {}).get("efemeros", []))


# ---------- 1b. em alta agora (exploração) ----------
def google_trends(geo, log):
    """Google Trends diário (RSS grátis): [{termo, trafego, noticias}]. Direto; se falhar, via WARP."""
    import xml.etree.ElementTree as ET
    url = f"https://trends.google.com/trending/rss?geo={geo}"
    ns = {"ht": "https://trends.google.com/trending/rss"}
    for extra in ([], ["--socks5-hostname", PROXY]):
        r = subprocess.run(["curl", "-s", "-m", "25", *extra, url], capture_output=True)
        try:
            root = ET.fromstring(r.stdout)
        except ET.ParseError:
            continue
        out = []
        for it in root.iter("item"):
            tr = (it.findtext("ht:approx_traffic", default="", namespaces=ns) or "").replace(",", "").replace("+", "")
            mult = 1000 if tr.upper().endswith("K") else 1
            try:
                trafego = int(float(tr.rstrip("Kk") or 0) * mult)
            except ValueError:
                trafego = 0
            noticias = [n.findtext("ht:news_item_title", default="", namespaces=ns) for n in it.findall("ht:news_item", ns)][:2]
            out.append({"termo": (it.findtext("title") or "").strip().lower(), "trafego": trafego, "noticias": noticias})
        return out
    log.append(f"Google Trends {geo}: falhou (direto e via WARP)")
    return []


def em_alta(yt, cfg, cota, log, paginas=2):
    """mostPopular por região (1 un./página, só longos > 4 min) + Google Trends diário."""
    ex = cfg.get("exploracao") or {}
    efcat = {str(c) for c in ex.get("categorias_efemeras", [])}
    populares, trends = {}, {}
    for reg, lang in (ex.get("regioes") or {}).items():
        populares[reg], token = [], None
        for _ in range(paginas):
            if yt is None or not cota.cabe(1):
                break
            try:
                r = yt.videos().list(part="snippet,statistics,contentDetails", chart="mostPopular", regionCode=reg,
                                     maxResults=50, pageToken=token).execute()
            except Exception as e:  # noqa: BLE001
                log.append(f"mostPopular {reg} falhou: {type(e).__name__}: {str(e)[:150]}")
                break
            finally:
                cota.gastar(1, "mostPopular")
            for v in r.get("items", []):
                dur = segundos(v.get("contentDetails", {}).get("duration"))
                if dur <= LONGO_EXPLORACAO:
                    continue
                sn = v["snippet"]
                cat = str(sn.get("categoryId", ""))
                populares[reg].append({"id": v["id"], "titulo": sn["title"], "canal": sn["channelTitle"],
                                       "canal_id": sn["channelId"], "views": int(v["statistics"].get("viewCount", 0)),
                                       "publicado": sn["publishedAt"][:10], "duracao_min": round(dur / 60, 1),
                                       "categoria_yt": cat, "idioma": lang,
                                       "efemero": cat in efcat or efemero_texto(sn["title"], cfg)})
            token = r.get("nextPageToken")
            if not token:
                break
        trends[reg] = google_trends(reg, log)
    return populares, trends


def itens_em_alta(populares, trends, cfg, hoje):
    """Linhas exploracao_alta: n-gramas dos títulos longos e não efêmeros do mostPopular (≥ 2 canais) e assuntos do
    Google Trends (somados entre países do mesmo idioma)."""
    regioes = (cfg.get("exploracao") or {}).get("regioes") or {}
    facel = {str(c) for c in (cfg.get("exploracao") or {}).get("categorias_faceless", [])}
    vids = {v["id"]: {"titulo": v["titulo"], "canal": v["canal_id"], "publicado": v["publicado"], "views": v["views"],
                      "idioma": v["idioma"]} for vs in populares.values() for v in vs
            if not v["efemero"] and (not facel or v["categoria_yt"] in facel)}
    grams = padroes_titulo(vids, hoje, top=15)
    for g in grams:
        g.update(origem="exploracao_alta", categoria="mostPopular", efemero=efemero_texto(g["termo"], cfg))
    assuntos = {}
    for reg, xs in trends.items():
        lang = regioes.get(reg)
        for x in xs:
            if not x["termo"]:
                continue
            a = assuntos.setdefault((lang, x["termo"]), {"idioma": lang, "termo": x["termo"], "origem": "exploracao_alta",
                                                         "categoria": "trends", "aparicoes": 0, "bruto": 0.0, "regioes": [],
                                                         "noticias": [], "efemero": False})
            a["aparicoes"] += 1
            a["bruto"] += x["trafego"]
            a["regioes"].append(reg)
            a["noticias"] += x["noticias"]
            a["efemero"] = a["efemero"] or efemero_texto(x["termo"] + " " + " ".join(x["noticias"]), cfg)
    for a in assuntos.values():
        a["categoria"] = "trends:" + ",".join(a["regioes"])
    return grams + list(assuntos.values())


# ---------- destino ----------
def destino(lang, termo, cfg):
    tn = norm(termo)
    for slug, d in cfg["destinos"].items():
        if d["idioma"] != lang:
            continue
        if d.get("exigir_historia") and "historia" not in tn:
            continue
        if tem_palavra(tn, d["palavras"]):
            return slug
    return "novo-canal"


# ---------- 2. padrões de título ----------
def idioma_titulo(t):
    toks = re.findall(r"[a-zà-ÿ']+", t.lower())
    pts = {l: sum(w in MARCAS[l] for w in toks) for l in MARCAS}
    best = max(pts, key=pts.get)
    ordenado = sorted(pts.values(), reverse=True)
    return best if ordenado[0] >= 2 and ordenado[0] > ordenado[1] else None


def corpus_titulos(extras):
    """Títulos com views e data: garimpo_videos (banco) + último garimpo (json) + resultados da validação."""
    vids = {}
    try:
        with conectar() as con:
            for vid, ch, tit, pub, views in con.execute(
                    "SELECT video_id, channel_id, titulo, publicado, views FROM garimpo_videos WHERE titulo IS NOT NULL"):
                vids[vid] = {"titulo": tit, "canal": ch, "publicado": str(pub), "views": views or 0}
    except Exception as e:  # noqa: BLE001
        print(f"[db] aviso: sem garimpo_videos ({e})", file=sys.stderr)
    jsons = sorted(f for f in os.listdir(TENDENCIAS) if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.json", f)) if os.path.isdir(TENDENCIAS) else []
    if jsons:
        for c in json.load(open(os.path.join(TENDENCIAS, jsons[-1])))["candidatos"]:
            for v in c["videos_lista"]:
                vids[v["id"]] = {"titulo": v["titulo"], "canal": c["id"], "publicado": v["publicado"], "views": v["views"]}
    vids.update(extras)
    return vids, (jsons[-1] if jsons else None)


def padroes_titulo(vids, hoje, top=25):
    grams = defaultdict(lambda: {"peso": 0.0, "titulos": set(), "canais": set()})
    for vid, v in vids.items():
        lang = v.get("idioma") or idioma_titulo(v["titulo"])
        if lang not in STOP:
            continue
        try:
            idade = max((hoje - dt.date.fromisoformat(v["publicado"][:10])).days, 7)
        except ValueError:
            idade = 365
        peso = v["views"] / idade
        t = re.sub(r"\d+", "N", v["titulo"].lower())
        toks = re.findall(r"[a-zà-ÿ'N]+", t)
        vistos = set()
        for n in (2, 3, 4):
            for i in range(len(toks) - n + 1):
                g = toks[i:i + n]
                if (all(w in STOP[lang] or w == "N" for w in g) or g[0] in ("and", "y", "e", "et", "x", "vs")
                        or not any(len(w) >= 4 and w not in STOP[lang] for w in g)):
                    continue
                k = (lang, " ".join(g))
                if k in vistos:
                    continue
                vistos.add(k)
                grams[k]["peso"] += peso
                grams[k]["titulos"].add(vid)
                grams[k]["canais"].add(v["canal"])
    por_lang = defaultdict(list)
    for (lang, g), d in grams.items():
        if len(d["canais"]) >= 2 and len(d["titulos"]) >= 2:
            por_lang[lang].append({"idioma": lang, "termo": g, "origem": "titulo", "aparicoes": len(d["titulos"]),
                                   "canais": len(d["canais"]), "bruto": d["peso"], "titulos_set": d["titulos"]})
    saida = []
    for lang, xs in por_lang.items():
        xs.sort(key=lambda x: (-x["bruto"], -len(x["termo"])))
        escolhidos = []
        for x in xs:  # tira n-grama contido num mais longo que cobre os mesmos títulos
            if any(x["termo"] in y["termo"] and x["titulos_set"] <= y["titulos_set"] for y in xs if y is not x and len(y["termo"]) > len(x["termo"])):
                continue
            escolhidos.append(x)
            if len(escolhidos) >= top:
                break
        saida += escolhidos
    return saida


def normalizar_score(itens):
    """score_descoberta 0–10 dentro de cada (idioma, origem), em escala log."""
    grupos = defaultdict(list)
    for t in itens:
        grupos[(t["idioma"], t["origem"])].append(t)
    for xs in grupos.values():
        mx = max(math.log1p(x["bruto"]) for x in xs) or 1
        for x in xs:
            x["score_descoberta"] = round(10 * math.log1p(x["bruto"]) / mx, 2)


# ---------- 3. validação ----------
def yt_client():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from trends import yt_client as _yt  # mesmo token do garimpo
    return _yt()


def amostra_zero():
    """Termos que já foram validados com amostra 0 (nenhum vídeo útil) nas últimas 8 semanas: não regastar 100 un."""
    try:
        with conectar() as con:
            return {(r[0], r[1]) for r in con.execute(
                "SELECT DISTINCT idioma, termo FROM palavras_chave WHERE validado AND amostra = 0 AND data > current_date - 56")}
    except Exception:  # noqa: BLE001
        return set()


def escolher_para_validar(itens, cfg, n, pular=frozenset()):
    """Termos dos NOSSOS canais (10 por semana desde 06/11/2026; as vagas de "novo-canal" foram para a Exploração).
    Pula lixo (música, tutorial…: exploracao.lixo) e termos que já deram amostra 0."""
    lixo = [norm(w) for w in (cfg.get("exploracao") or {}).get("lixo", [])]
    cotas = {"dossie-es": 4, "historia-ptbr": 3, "lotr-fr": 3}
    fator = n / sum(cotas.values())
    cotas = {k: max(1, round(v * fator)) for k, v in cotas.items()}
    escolhidos = []
    for dest, q in cotas.items():
        cand = sorted((t for t in itens if t["destino"] == dest and t["origem"] == "autocomplete"),
                      key=lambda t: (-t["score_descoberta"], -t["aparicoes"]))
        pegos = []
        for t in cand:
            tn = norm(t["termo"])
            if (t["idioma"], t["termo"]) in pular or any(re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", tn) for w in lixo):
                continue
            toks = set(norm(t["termo"]).split())
            if any(p["idioma"] == t["idioma"] and (toks <= set(norm(p["termo"]).split()) or set(norm(p["termo"]).split()) <= toks) for p in pegos):
                continue
            pegos.append(t)
            if len(pegos) >= q:
                break
        escolhidos += pegos
    return escolhidos[:n]


def escolher_exploracao(itens, cfg, n, ativas=None, offset=0):
    """Exploração: até n termos, rodízio en → es → pt → fr (ordem da matriz), dos de maior descoberta; ≥ 3 palavras, não é
    semente, não é efêmero nem lixo (tutorial, música…), máx. 2 por categoria, sem sobreposição; até 2 vagas para
    n-gramas do mostPopular (em alta agora)."""
    ex = cfg.get("exploracao") or {}
    sementes = {norm(x) for f in ex.get("formatos", {}).values() for k in ("expandir", "combinar") for x in f.get(k, [])}
    sementes |= {norm(x) for c in ex.get("categorias", {}).values() for xs in c.values() for x in xs}
    lixo = [norm(w) for w in ex.get("lixo", [])]

    def ok(t):
        tn = norm(t["termo"])
        return (t["destino"] == "novo-canal" and not t.get("efemero") and len(tn.split()) >= 3 and tn not in sementes
                and not any(re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", tn) for w in lixo))

    pegos, por_cat = [], defaultdict(int)

    def cabe(t):
        toks = set(tokens_conteudo(t["termo"], t["idioma"]))
        if len(toks) < 1 or por_cat[t.get("categoria")] >= 2:
            return False
        return not any(p["idioma"] == t["idioma"] and (toks <= set(tokens_conteudo(p["termo"], p["idioma"]))
                                                       or set(tokens_conteudo(p["termo"], p["idioma"])) <= toks) for p in pegos)

    # 0) uma busca AMPLA por categoria ativa (a 1ª semente da categoria; idioma em rodízio en → es → pt → fr): sem filtro
    #    de título, é a rede para pegar canal novo estourando na categoria (outlier).
    langs = ("en", "es", "pt", "fr")
    por_chave = {(t["idioma"], t["termo"]): t for t in itens if t["origem"] == "exploracao_semente"}
    for k, cat in enumerate((ativas or [])[:(n + 1) // 2]):
        lang = langs[(k + (offset or 0)) % 4]
        sem = (ex.get("categorias", {}).get(cat, {}).get(lang) or [None])[0]
        if not sem:
            continue
        t = por_chave.get((lang, sem.lower())) or {"idioma": lang, "termo": sem.lower(), "origem": "exploracao_semente",
                                                   "aparicoes": 1, "melhor_posicao": None, "score_descoberta": 0.0,
                                                   "destino": "novo-canal", "efemero": False}
        if t not in itens:
            itens.append(t)
        t.update(categoria=cat, toks_relevancia=[], topico=f"categoria: {cat}", familias=["categoria"])
        pegos.append(t)
        por_cat[cat] += 1
    # 1) até 1 n-grama do mostPopular (só categorias faceless do YouTube)
    alta = sorted((t for t in itens if t["origem"] == "exploracao_alta" and t.get("categoria") == "mostPopular" and ok(t)),
                  key=lambda t: -t["score_descoberta"])
    n_alta = 0
    for t in alta:
        if n_alta >= 1 or len(pegos) >= n:
            break
        if cabe(t):
            pegos.append(t)
            n_alta += 1
    # 2) Tópicos: tira o prefixo do formato/semente ("what happened to", "secrets of", "why"…) e soma o mesmo assunto entre
    # formatos diferentes. Assunto que aparece em ≥ 2 famílias = interesse durável (não um vídeo só); o termo
    # representante (maior descoberta) vai para a busca, e a relevância usa só as palavras do tópico.
    stop_all = {norm(w) for ws in STOP.values() for w in ws}
    prefixos = sorted({norm(x) for f in ex.get("formatos", {}).values() for k in ("expandir", "combinar") for x in f.get(k, [])}
                      # sementes de categoria que são frase-prefixo ("who was", "la historia no contada de")
                      | {norm(x) for c in ex.get("categorias", {}).values() for xs in c.values() for x in xs
                         if len(x.split()) >= 2 and norm(x).split()[-1] in stop_all},
                      key=len, reverse=True)
    vagos = {norm(w) for w in ex.get("genericos", [])}
    toks_sementes = {w for c in ex.get("categorias", {}).values() for xs in c.values() for x in xs for w in norm(x).split()}
    topicos = {}
    for t in itens:
        if t["origem"] != "exploracao_semente" or t["destino"] != "novo-canal" or t.get("efemero"):
            continue
        tn = norm(t["termo"])
        if any(re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", tn) for w in lixo):
            continue
        fam = next((p for p in prefixos if tn.startswith(p + " ")), None)
        resto = tn[len(fam) + 1:] if fam else tn
        if fam and any(resto.startswith(p + " ") or resto == p for p in prefixos):
            continue  # "why why why…", "pourquoi pourquoi"
        toks = [w for w in tokens_conteudo(resto, t["idioma"]) if len(w) >= 3]
        if not toks or len(toks) > 4 or all(w in vagos or w in toks_sementes for w in toks):
            continue
        chave = (t["idioma"], " ".join(toks[:3]))
        tp = topicos.setdefault(chave, {"familias": set(), "soma": 0.0, "rep": None, "toks": toks[:3], "cats": set()})
        tp["familias"].add(fam or "semente")
        if t.get("categoria") and not str(t["categoria"]).startswith("formato:"):
            tp["cats"].add(t["categoria"])
        tp["soma"] += t["score_descoberta"]
        if tp["rep"] is None or t["score_descoberta"] > tp["rep"]["score_descoberta"]:
            tp["rep"] = t
    fila = {l: [] for l in ("en", "es", "pt", "fr")}
    ordem = sorted(((k, tp) for k, tp in topicos.items() if len(tp["familias"]) >= 2),
                   key=lambda kv: (-len(kv[1]["familias"]), -kv[1]["soma"]))
    for (lang, tema), tp in ordem:
        tp["rep"]["topico"], tp["rep"]["familias"], tp["rep"]["toks_relevancia"] = tema, sorted(tp["familias"]), tp["toks"]
        tp["rep"]["consulta"] = tema  # busca pelo assunto (a frase do autocomplete quase não tem vídeo em 30 dias)
        if tp["cats"]:
            tp["rep"]["categoria"] = sorted(tp["cats"])[0]
        if lang in fila:
            fila[lang].append(tp["rep"])

    def sobrepoe(t):
        return any(p["idioma"] == t["idioma"] and set(p.get("toks_relevancia") or []) & set(t["toks_relevancia"]) for p in pegos)

    # 1ª passada: o melhor tópico de cada categoria ativa da semana (a ordem en → es → pt → fr desempata)
    for cat in (ativas or []) if len(pegos) < n else []:
        for l in ("en", "es", "pt", "fr"):
            c = next((t for t in fila[l] if t.get("categoria") == cat and not sobrepoe(t)), None)
            if c and len(pegos) < n:
                pegos.append(c)
                fila[l].remove(c)
                por_cat[cat] += 1
                break
    while len(pegos) < n and any(fila.values()):
        for l in ("en", "es", "pt", "fr"):
            while fila[l] and len(pegos) < n:
                t = fila[l].pop(0)
                if por_cat[t.get("categoria")] < 2 and not sobrepoe(t):
                    pegos.append(t)
                    por_cat[t.get("categoria")] += 1
                    break
    return pegos


def validar(yt, alvos, cfg, cota, hoje_dt, log):
    """Valida cada termo (search.list + videos.list + channels.list + playlistItems). Termos de exploração usam a
    janela de 30 dias e caçam outliers. Reserva cota para os termos que faltam. Devolve (extras para o corpus de
    títulos, outliers)."""
    extras, outliers = {}, []
    moldes = [norm(m) for m in cfg.get("moldes", [])]
    for k, t in enumerate(alvos):
        reserva = CUSTO_TERMO * (len(alvos) - k - 1)
        if not cota.cabe(CUSTO_TERMO):
            log.append(f"teto de cota ({cota.teto}) atingido; {t['termo']!r} e os seguintes ficaram sem validação")
            break
        expl = t["origem"].startswith("exploracao")
        janela = JANELA_EXPLORACAO if expl else JANELA_NOSSOS
        min_seg = LONGO_EXPLORACAO if expl else 75  # nossos: > 75 s (critério da 1ª semana, para comparar semanas)
        desde = (hoje_dt - dt.timedelta(days=janela)).strftime("%Y-%m-%dT%H:%M:%SZ")
        try:
            r = yt.search().list(part="snippet", q=t.get("consulta") or t["termo"], type="video", order="viewCount", publishedAfter=desde,
                                 relevanceLanguage=t["idioma"], maxResults=50).execute()
            cota.gastar(CUSTO_SEARCH, "search")
            ids = [i["id"]["videoId"] for i in r.get("items", []) if i["id"].get("videoId")]
            vids = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids)).execute().get("items", []) if ids else []
            if ids:
                cota.gastar(CUSTO_VIDEOS, "videos")
        except Exception as e:  # noqa: BLE001
            log.append(f"validação de {t['termo']!r} falhou: {type(e).__name__}: {str(e)[:200]}")
            if "quotaExceeded" in str(e):
                break
            continue
        toks = t.get("toks_relevancia")
        toks = toks if toks is not None else tokens_conteudo(t["termo"], t["idioma"])
        lst, fora, longos = [], 0, []  # longos = todos os longos no idioma (exploração: base dos outliers)
        for v in vids:
            if segundos(v.get("contentDetails", {}).get("duration")) <= min_seg:  # sem Shorts (nossos vídeos são longos)
                fora += 1
                continue
            decl = (v["snippet"].get("defaultAudioLanguage") or v["snippet"].get("defaultLanguage") or "")[:2]
            il = idioma_titulo(v["snippet"]["title"])
            views = int(v["statistics"].get("viewCount", 0))
            pub = v["snippet"]["publishedAt"]
            idade = (hoje_dt - dt.datetime.fromisoformat(pub.replace("Z", "+00:00"))).days
            x = {"id": v["id"], "titulo": v["snippet"]["title"], "canal": v["snippet"]["channelTitle"],
                 "canal_id": v["snippet"]["channelId"], "views": views, "publicado": pub[:10], "idade": idade,
                 "duracao_min": round(segundos(v["contentDetails"].get("duration")) / 60, 1)}
            if not (decl and decl != t["idioma"]) and not (il and il != t["idioma"]):
                longos.append(x)
            if (decl and decl != t["idioma"]) or not relevante(v["snippet"]["title"], toks, t["termo"], t["idioma"]):
                fora += 1
                continue
            lst.append(x)
            if not expl:
                extras[v["id"]] = {"titulo": v["snippet"]["title"], "canal": v["snippet"]["channelId"], "publicado": pub[:10],
                                   "views": views}
        lst.sort(key=lambda x: -x["views"])
        top10 = [x["views"] for x in lst[:10]]
        t["validado"] = True
        t["janela_dias"] = janela
        t["mediana_top10"] = int(statistics.median(top10)) if top10 else 0
        t["recentes_100k"] = sum(x["idade"] < 90 and x["views"] > 100_000 for x in lst)
        t["no_molde"] = sum(any(m in norm(x["titulo"]) for m in moldes) for x in lst)
        t["amostra"] = len(lst)
        t["fora_do_tema"] = fora
        canais_do_top10(yt, t, lst, hoje_dt, cota, reserva, log, expl, longos)
        if expl:
            for x in longos:
                if x.get("canal_novo") and x["views"] >= OUTLIER_VIEWS and (
                        x.get("canal_inscritos") is None or x["views"] / max(x["canal_inscritos"], 1) >= OUTLIER_VPI):
                    outliers.append(dict(x, termo_busca=t["termo"], idioma=t["idioma"], categoria=t.get("categoria")))
            t["n_outliers"] = sum(o["termo_busca"] == t["termo"] for o in outliers)
        t["exemplos"] = [{k: x[k] for k in ("id", "titulo", "canal", "views", "publicado", "canal_idade_meses",
                                            "canal_criado_meses", "canal_idade_fonte", "canal_inscritos") if k in x}
                         for x in lst[:3]]
    return extras, outliers


# ---------- idade do canal pelo 1º vídeo ----------
def cache_idade(ids):
    try:
        with conectar() as con:
            rows = con.execute("SELECT channel_id, primeiro_video_em FROM canais_idade WHERE channel_id = ANY(%s)"
                               " AND primeiro_video_em IS NOT NULL", (list(ids),)).fetchall()
        return {r[0]: r[1] for r in rows}
    except Exception as e:  # noqa: BLE001
        print(f"[db] aviso: sem cache de idade ({e})", file=sys.stderr)
        return {}


def salvar_cache(info):
    try:
        with conectar() as con:
            for cid, i in info.items():
                con.execute(
                    "INSERT INTO canais_idade (channel_id, titulo, criado_em, primeiro_video_em, video_count, inscritos,"
                    " idade_fonte) VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (channel_id) DO UPDATE SET"
                    " titulo=EXCLUDED.titulo, criado_em=EXCLUDED.criado_em,"
                    " primeiro_video_em=COALESCE(EXCLUDED.primeiro_video_em, canais_idade.primeiro_video_em),"
                    " video_count=EXCLUDED.video_count, inscritos=EXCLUDED.inscritos,"
                    " idade_fonte=CASE WHEN EXCLUDED.primeiro_video_em IS NULL AND canais_idade.primeiro_video_em IS NOT NULL"
                    " THEN canais_idade.idade_fonte ELSE EXCLUDED.idade_fonte END, atualizado_em=now()",
                    (cid, i["titulo"], i["criado"], i["primeiro"], i["videos"], i["subs"], i["fonte"]))
    except Exception as e:  # noqa: BLE001
        print(f"[db] aviso: não salvou o cache de idade ({e})", file=sys.stderr)


def primeiro_video(yt, uploads, cota, reserva, log):
    """publishedAt mais antigo do playlist de uploads (pagina até o fim; 1 unidade por página de 50). None se não deu."""
    menor, token = None, None
    for _ in range(math.ceil(MAX_VIDEOS_NOVO / 50) + 1):
        if not cota.cabe(1, reserva):
            if not cota.avisou:
                log.append("teto de cota: parte dos canais ficou com a idade pela data de criação (idade_fonte = criacao)")
                cota.avisou = True
            return None
        try:
            r = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=token).execute()
        except Exception as e:  # noqa: BLE001
            cota.gastar(1, "playlistItems")
            print(f"[yt] playlistItems {uploads}: {type(e).__name__}: {str(e)[:120]}", file=sys.stderr)
            return None
        cota.gastar(1, "playlistItems")
        for it in r.get("items", []):
            p = it.get("contentDetails", {}).get("videoPublishedAt")
            if p:
                d = dt.date.fromisoformat(p[:10])
                menor = d if menor is None or d < menor else menor
        token = r.get("nextPageToken")
        if not token:
            return menor
    return None


def idade_canais(yt, ids, hoje_dt, cota, reserva, log, paginar):
    """channels.list (1 un. para até 50 ids) + 1º vídeo de cada canal em `paginar` com ≤ 200 vídeos (cache no banco).
    info[id] = {titulo, criado, dias_criacao, subs, videos, primeiro, fonte, dias, novo}."""
    ids = list(dict.fromkeys(ids))[:50]
    if not ids or not cota.cabe(CUSTO_CANAIS, reserva):
        return {}
    try:
        chs = yt.channels().list(part="snippet,statistics,contentDetails", id=",".join(ids)).execute().get("items", [])
    except Exception as e:  # noqa: BLE001
        log.append(f"channels.list falhou: {type(e).__name__}: {str(e)[:150]}")
        return {}
    finally:
        cota.gastar(CUSTO_CANAIS, "channels")
    cache = cache_idade([c["id"] for c in chs])
    info, hoje = {}, hoje_dt.date()
    for c in chs:
        cid, st = c["id"], c["statistics"]
        criado = dt.date.fromisoformat(c["snippet"]["publishedAt"][:10])
        i = {"titulo": c["snippet"]["title"], "criado": criado, "dias_criacao": (hoje - criado).days,
             "subs": None if st.get("hiddenSubscriberCount") else int(st.get("subscriberCount", 0) or 0),
             "videos": int(st.get("videoCount", 0) or 0), "primeiro": None, "fonte": "criacao"}
        if i["videos"] > MAX_VIDEOS_NOVO:
            i["fonte"] = "muitos_videos"
        elif cache.get(cid):
            i["primeiro"], i["fonte"] = cache[cid], "primeiro_video"
        elif cid in paginar:
            up = c.get("contentDetails", {}).get("relatedPlaylists", {}).get("uploads")
            p = primeiro_video(yt, up, cota, reserva, log) if up else None
            if p:
                i["primeiro"], i["fonte"] = p, "primeiro_video"
        i["dias"] = (hoje - i["primeiro"]).days if i["primeiro"] else i["dias_criacao"]
        i["novo"] = i["fonte"] != "muitos_videos" and i["dias"] < NOVO_DIAS
        info[cid] = i
    salvar_cache(info)
    return info


def canais_do_top10(yt, t, lst, hoje_dt, cota, reserva, log, expl=False, longos=()):
    """Idade (pelo 1º vídeo) e tamanho dos canais do top-10 útil. Na exploração, também os canais de qualquer vídeo longo
    no idioma com ≥ 30 mil views, mesmo sem as palavras do termo no título (candidatos a outlier)."""
    top = lst[:10]
    ids_top = [x["canal_id"] for x in top]
    extra = [x["canal_id"] for x in (longos if expl else []) if x["views"] >= OUTLIER_VIEWS]
    info = idade_canais(yt, ids_top + extra, hoje_dt, cota, reserva, log, set(ids_top) | set(extra))
    if not info:
        return
    for x in list(lst) + list(longos):
        i = info.get(x["canal_id"])
        if i:
            x["canal_idade_meses"] = round(i["dias"] / 30.4, 1)
            x["canal_criado_meses"] = round(i["dias_criacao"] / 30.4, 1)
            x["canal_idade_fonte"] = i["fonte"]
            x["canal_primeiro_video"] = str(i["primeiro"]) if i["primeiro"] else None
            x["canal_inscritos"] = i["subs"]
            x["canal_videos"] = i["videos"]
            x["canal_novo"] = i["novo"]
    tinfo = {cid: info[cid] for cid in dict.fromkeys(ids_top) if cid in info}
    idades = [i["dias"] / 30.4 for i in tinfo.values()]
    subs = [i["subs"] for i in tinfo.values() if i["subs"] is not None]
    novos = {cid for cid, i in tinfo.items() if i["novo"]}
    vpi = [x["views"] / max(x["canal_inscritos"], 1) for x in top
           if x["canal_id"] in novos and x.get("canal_inscritos") is not None]
    t["canais_top10"] = len(tinfo)
    t["n_canais_novos"] = len(novos)
    t["idade_mediana_meses"] = round(statistics.median(idades), 1) if idades else None
    t["inscritos_mediana"] = int(statistics.median(subs)) if subs else None
    t["vpi_novos"] = round(statistics.median(vpi), 2) if vpi else None
    primeiros = [i["primeiro"] for i in tinfo.values() if i["primeiro"]]
    t["primeiro_video_em"] = str(max(primeiros)) if primeiros else None
    fontes = {"criacao" if i["fonte"] == "criacao" else "primeiro_video" for i in tinfo.values()}
    t["idade_fonte"] = fontes.pop() if len(fontes) == 1 else "misto"
    # PORTA ABERTA: um canal com 1º vídeo < 90 dias no top-10 com vídeo de ≥ 50 mil views e ≥ metade da mediana do termo
    corte = max(50_000, 0.5 * (t.get("mediana_top10") or 0))
    t["porta_aberta"] = any(x["canal_id"] in novos and x["views"] >= corte for x in top)
    t["novos_exemplos"] = [{"titulo": x["titulo"], "canal": x["canal"], "views": x["views"],
                            "canal_idade_meses": x.get("canal_idade_meses"), "canal_criado_meses": x.get("canal_criado_meses"),
                            "canal_primeiro_video": x.get("canal_primeiro_video"), "canal_inscritos": x.get("canal_inscritos")}
                           for x in top if x["canal_id"] in novos][:3]


def bonus_canais(t):
    """Porta de entrada (dados de canais do top-10; 0 se não houver):
    + 4 por canal novo (1º vídeo < 90 dias, máx. 3 → 12) + 4·log10(1 + views/inscritos dos vídeos de canais novos) (VPI 10 → 4,2;
    100 → 8) + 5 se PORTA ABERTA; − se nenhum canal novo: idade mediana em anos (máx. 10) + 2·log10(inscritos medianos/100 mil)
    quando a mediana passa de 100 mil (1 mi → 2; 10 mi → 4)."""
    if t.get("canais_top10") is None:
        return 0.0
    b = 4 * min(t["n_canais_novos"] or 0, 3) + 4 * math.log10(1 + float(t["vpi_novos"] or 0)) + (5 if t["porta_aberta"] else 0)
    if not t["n_canais_novos"]:
        b -= min(float(t["idade_mediana_meses"] or 0) / 12, 10)
        if (t["inscritos_mediana"] or 0) > 100_000:
            b -= 2 * math.log10(t["inscritos_mediana"] / 100_000)
    return b


def pontuar(t):
    """Validado: demanda (10·log10 mediana) + tração (4 por vídeo recente > 100 mil, máx. 10) − concorrência no molde
    (3 por vídeo, máx. 5) + descoberta (0–10) + bonus_canais (idade/tamanho dos canais do top-10) + 5 por outlier
    (exploração, máx. 3). Exploração usa a janela de 30 dias: compare só com exploração.
    Outlier (linha própria): 10·log10(views) + 4·log10(1 + views/inscritos). Não validado: só a descoberta (0–10)."""
    if t["origem"] == "exploracao_outlier":
        ex = t["exemplos"][0]
        return round(10 * math.log10(1 + ex["views"]) + 4 * math.log10(1 + float(t.get("vpi_novos") or 0)), 2)
    if t.get("validado"):
        return round(10 * math.log10(1 + t["mediana_top10"]) + 4 * min(t["recentes_100k"], 10)
                     - 3 * min(t["no_molde"], 5) + t["score_descoberta"] + bonus_canais(t)
                     + 5 * min(t.get("n_outliers") or 0, 3), 2)
    return t["score_descoberta"]


# ---------- 4. tendência e gravação ----------
def anterior(hoje):
    """(data da execução anterior, linhas dela, histórico = última linha de cada termo em QUALQUER semana anterior)."""
    try:
        with conectar() as con:
            d = con.execute("SELECT max(data) FROM palavras_chave WHERE data < %s", (hoje,)).fetchone()[0]
            if not d:
                return None, {}, {}
            cols = "idioma, termo, origem, score_descoberta, destino, validado, mediana_top10, data"
            rows = con.execute(f"SELECT {cols} FROM palavras_chave WHERE data = %s", (d,)).fetchall()
            hist = con.execute(f"SELECT DISTINCT ON (idioma, termo, origem) {cols} FROM palavras_chave WHERE data < %s"
                               " ORDER BY idioma, termo, origem, data DESC", (hoje,)).fetchall()
            return d, {(r[0], r[1], r[2]): r for r in rows}, {(r[0], r[1], r[2]): r for r in hist}
    except Exception as e:  # noqa: BLE001
        print(f"[db] aviso: sem execução anterior ({e})", file=sys.stderr)
        return None, {}, {}


def tendencia(t, hist):
    """novo = nunca visto em semana anterior; subindo/caindo = descoberta ±20% ou, se validado nas duas, mediana ±30%."""
    if t["origem"] == "exploracao_outlier":
        return "novo" if (t["idioma"], t["termo"], t["origem"]) not in hist else "estavel"
    a = hist.get((t["idioma"], t["termo"], t["origem"]))
    if not a:
        return "novo"
    if t.get("validado") and a[5] and a[6]:
        if (t["mediana_top10"] or 0) > a[6] * 1.3:
            return "subindo"
        if (t["mediana_top10"] or 0) < a[6] * 0.7:
            return "caindo"
    prev = float(a[3] or 0)
    if t["score_descoberta"] > prev * 1.2 + 0.2:
        return "subindo"
    if t["score_descoberta"] < prev * 0.8 - 0.2:
        return "caindo"
    return "estavel"


COLS = ("destino", "aparicoes", "melhor_posicao", "score_descoberta", "validado", "mediana_top10", "recentes_100k", "no_molde",
        "amostra", "exemplos", "score", "tendencia", "canais_top10", "n_canais_novos", "idade_mediana_meses",
        "inscritos_mediana", "vpi_novos", "porta_aberta", "primeiro_video_em", "idade_fonte", "categoria", "janela_dias",
        "n_outliers", "efemero")


def gravar(itens, hoje):
    sql = ("INSERT INTO palavras_chave (data, idioma, termo, origem, " + ", ".join(COLS) + ") VALUES ("
           + ",".join(["%s"] * (4 + len(COLS))) + ") ON CONFLICT (data, idioma, termo, origem) DO UPDATE SET "
           + ", ".join(f"{c}=EXCLUDED.{c}" for c in COLS) + ", criado_em=now()"
           # 2ª execução no mesmo dia nunca apaga uma validação já feita
           + " WHERE EXCLUDED.validado OR NOT palavras_chave.validado")
    with conectar() as con:
        for t in itens:
            vals = []
            for c in COLS:
                v = t.get(c)
                if c == "exemplos":
                    v = Jsonb(v) if v else None
                elif c == "validado":
                    v = bool(v)
                elif c == "categoria" and v is not None:
                    v = str(v)[:120]
                vals.append(v)
            con.execute(sql, (hoje, t["idioma"], t["termo"], t["origem"], *vals))
    return len(itens)


def fmt(n):
    return "—" if n is None else f"{n:,}".replace(",", ".")


def _canais(t):
    if t.get("canais_top10") is None:
        return "— | — | — | — | — | "
    return (f"{t['n_canais_novos']}/{t['canais_top10']} | {t['idade_mediana_meses']} | {fmt(t['inscritos_mediana'])} | "
            f"{t['vpi_novos'] if t['vpi_novos'] is not None else '—'} | {'**PORTA ABERTA**' if t['porta_aberta'] else '—'} | ")


def _ex_novo(e):
    return (f"{e['canal'][:30]} (1º vídeo há {e['canal_idade_meses']} meses"
            + (f", canal criado há {e['canal_criado_meses']}" if e.get("canal_criado_meses") not in (None, e.get("canal_idade_meses")) else "")
            + f", {fmt(e['canal_inscritos'])} inscritos): {e['titulo'][:50]} ({fmt(e['views'])})")


def escrever_md(path, r):
    L = [f"# Palavras-chave — {r['data']}{' (teste)' if r['teste'] else ''}", "",
         f"Autocomplete: {r['chamadas_autocomplete']} chamadas ({len(r['falhas_autocomplete'])} falhas), "
         f"{r['n_autocomplete']} termos dos nossos nichos + {r['n_exploracao']} da exploração. Padrões de título: {r['n_titulo']} n-gramas "
         f"({r['titulos_corpus']} títulos; garimpo {r['garimpo']}). Validação: {r['n_validados']} termos, "
         f"**{r['cota_gasta']} unidades de cota** (teto {r['max_cota']}; {', '.join(f'{k} {v}' for k, v in r['cota_por_tipo'].items())}). "
         f"Execução anterior: {r['anterior'] or 'nenhuma'}.", "",
         "Idade do canal = **1º vídeo público** (playlist de uploads); canal novo = 1º vídeo há < 90 dias; > 200 vídeos = não é novo. "
         f"Fonte da idade nos termos validados: {r['fontes_idade']}.", ""]
    for l in r["avisos"]:
        L.append(f"- ⚠ {l}")
    itens = r["itens"]
    L += ["", "## Termos validados dos nossos canais (50 mais vistos dos últimos 12 meses, order=viewCount; só vídeos longos com as palavras do termo no título e no idioma)", "",
          "Canais = do top-10 útil: novos (1º vídeo < 90 dias)/total, idade mediana em meses (pelo 1º vídeo), inscritos medianos; VPI = mediana de "
          "views/inscritos dos vídeos de canais novos (alto = o algoritmo entrega para não inscritos).", "",
          "| Destino | Idioma | Termo | Med. top-10 | Recentes >100 mil (<90 d) | No molde | Canais novos | Idade med. (meses) | Inscritos med. | VPI novos | Porta | Score | Tendência | Top vídeo |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in sorted((t for t in itens if t.get("validado") and not t["origem"].startswith("exploracao")),
                    key=lambda t: (t["destino"], -t["score"])):
        ex = t["exemplos"][0] if t.get("exemplos") else None
        top = f"{ex['titulo'][:60]} ({fmt(ex['views'])}, {ex['canal'][:25]})" if ex else "—"
        L.append(f"| {t['destino']} | {t['idioma']} | {t['termo']} | {fmt(t['mediana_top10'])} | {t['recentes_100k']} | "
                 f"{t['no_molde']}/{t['amostra']} | " + _canais(t) + f"{t['score']} | {t['tendencia']} | {top.replace('|', '/')} |")
    portas = [t for t in itens if t.get("porta_aberta") and not t["origem"].startswith("exploracao")]
    if portas:
        L += ["", "**PORTA ABERTA** (canal com 1º vídeo < 90 dias no top-10 com vídeo ≥ 50 mil views e ≥ metade da mediana):", ""]
        for t in sorted(portas, key=lambda t: -t["score"]):
            ex = "; ".join(_ex_novo(e) for e in t.get("novos_exemplos", []))
            L.append(f"- {t['destino']} · {t['idioma']} · **{t['termo']}**: {ex.replace('|', '/')}")

    # ---------- exploração ----------
    rod = r.get("rodizio") or {}
    L += ["", "## Exploração (fora do nosso radar)", "",
          f"Semana ISO {rod.get('semana')}: categorias **{', '.join(rod.get('categorias', []))}** (bloco {rod.get('bloco')} de {rod.get('ciclos')}); "
          f"formatos a–z: metade {rod.get('metade_formatos')}.", "",
          "### Termos validados da exploração (busca dos **últimos 30 dias**, order=viewCount, só vídeos > 4 min)", "",
          "| Idioma | Categoria | Origem | Termo | Med. top-10 (30 d) | Amostra | Canais novos | Idade med. (meses) | Inscritos med. | VPI novos | Porta | Outliers | Score | Tendência | Top vídeo |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in sorted((t for t in itens if t.get("validado") and t["origem"].startswith("exploracao")), key=lambda t: -t["score"]):
        ex = t["exemplos"][0] if t.get("exemplos") else None
        top = f"{ex['titulo'][:55]} ({fmt(ex['views'])}, {ex['canal'][:22]})" if ex else "—"
        L.append(f"| {t['idioma']} | {t.get('categoria') or '—'} | {t['origem'].replace('exploracao_', '')} | {t['termo']} | "
                 f"{fmt(t['mediana_top10'])} | {t['amostra']} | " + _canais(t)
                 + f"{t.get('n_outliers') or 0} | {t['score']} | {t['tendencia']} | {top.replace('|', '/')} |")
    outs = sorted((t for t in itens if t["origem"] == "exploracao_outlier"), key=lambda t: -t["score"])
    L += ["", f"### Outliers de canal novo ({len(outs)}): 1º vídeo < 90 dias, ≥ {fmt(OUTLIER_VIEWS)} views, views/inscritos ≥ {OUTLIER_VPI}", ""]
    for t in outs[:25]:
        e = t["exemplos"][0]
        L.append(f"- [{t['idioma']}] **{e['canal'][:40]}** — {e['titulo'][:80].replace('|', '/')} · {fmt(e['views'])} views em "
                 f"{e.get('idade')} d · {fmt(e.get('canal_inscritos'))} inscritos (VPI {t.get('vpi_novos')}) · 1º vídeo {e.get('canal_primeiro_video') or '?'} "
                 f"({e.get('canal_idade_fonte')}; canal criado há {e.get('canal_criado_meses')} meses; {e.get('canal_videos')} vídeos) · "
                 f"{e.get('duracao_min')} min · busca \"{t['categoria_busca']}\" · https://youtu.be/{e['id']}")
    if not outs:
        L.append("Nenhum nesta semana.")
    L += ["", "### Em alta agora por país (mostPopular, só longos > 4 min; ⚡ = efêmero: categoria Música/Esportes/Notícias ou palavra de evento)", ""]
    for reg, vs in (r.get("populares") or {}).items():
        xs = sorted(vs, key=lambda v: -v["views"])[:8]
        L.append(f"**{reg}** ({len(vs)} longos): " + ("; ".join(f"{'⚡' if v['efemero'] else ''}{v['titulo'][:55]} ({fmt(v['views'])}, {v['canal'][:20]}, cat {v['categoria_yt']})".replace('|', '/') for v in xs) or "—"))
        L.append("")
    L += ["### Google Trends diário (top 10 por país; ⚡ = efêmero pela notícia)", ""]
    for reg, xs in (r.get("trends") or {}).items():
        L.append(f"**{reg}:** " + ("; ".join(f"{x['termo']} ({fmt(x['trafego'])}+)" for x in xs[:10]) or "—"))
        L.append("")
    alta = sorted((t for t in itens if t["origem"] == "exploracao_alta" and t.get("categoria") == "mostPopular"), key=lambda t: -t["score"])
    L.append("**Padrões dos títulos em alta (n-gramas em ≥ 2 canais, não efêmeros):** "
             + ("; ".join(f"\"{t['termo']}\" [{t['idioma']}, {t['aparicoes']} títulos]" for t in alta[:20]) or "—"))
    L += ["", "### Autocomplete da exploração por idioma (top 15 não validados, sem lixo)", ""]
    for lang in ("en", "es", "pt", "fr"):
        xs = sorted((t for t in itens if t["origem"] == "exploracao_semente" and t["idioma"] == lang and not t.get("validado")),
                    key=lambda t: -t["score"])[:15]
        L.append(f"**{lang}:** " + ("; ".join(f"{t['termo']} [{t.get('categoria')}, {t['score_descoberta']}, {t['tendencia']}{', ⚡' if t.get('efemero') else ''}]" for t in xs) or "—"))
        L.append("")

    L += ["## Autocomplete por destino (top 15, não validados)", ""]
    for dest in DESTINOS:
        xs = sorted((t for t in itens if t["destino"] == dest and t["origem"] == "autocomplete" and not t.get("validado")),
                    key=lambda t: -t["score"])[:15]
        L.append(f"**{dest}:** " + ("; ".join(f"{t['termo']} [{t['idioma']} {t['score_descoberta']}, {t['tendencia']}]" for t in xs) or "—"))
        L.append("")
    L += ["## Padrões de título (n-gramas em ≥ 2 canais, pesados por views/dia)", ""]
    for lang in ("en", "es", "pt", "fr"):
        xs = sorted((t for t in itens if t["origem"] == "titulo" and t["idioma"] == lang), key=lambda t: -t["score"])[:12]
        if xs:
            L.append(f"**{lang}:** " + "; ".join(f"\"{t['termo']}\" ({t['aparicoes']} títulos/{t['canais']} canais, {t['tendencia']})" for t in xs))
            L.append("")
    if r["sumiram"]:
        L += ["## Sumiram desde a execução anterior (top 20 por score de então)", "", "; ".join(r["sumiram"]), ""]
    open(path, "w").write("\n".join(L) + "\n")


def linhas_outlier(outliers, hoje):
    """Uma linha exploracao_outlier por vídeo (o melhor termo que o achou); termo = título normalizado."""
    por_id = {}
    for o in sorted(outliers, key=lambda o: -o["views"]):
        por_id.setdefault(o["id"], o)
    out = []
    for o in por_id.values():
        vpi = round(o["views"] / max(o["canal_inscritos"], 1), 2) if o.get("canal_inscritos") is not None else None
        out.append({"idioma": o["idioma"], "termo": re.sub(r"\s+", " ", o["titulo"].lower())[:150], "origem": "exploracao_outlier",
                    "destino": "novo-canal", "categoria": o.get("categoria"), "categoria_busca": o["termo_busca"],
                    "aparicoes": 1, "score_descoberta": 0, "validado": False, "n_canais_novos": 1, "vpi_novos": vpi,
                    "primeiro_video_em": o.get("canal_primeiro_video"), "idade_fonte": o.get("canal_idade_fonte"),
                    "janela_dias": JANELA_EXPLORACAO, "n_outliers": 1,
                    "exemplos": [{k: o.get(k) for k in ("id", "titulo", "canal", "canal_id", "views", "publicado", "idade",
                                                         "duracao_min", "canal_idade_meses", "canal_criado_meses",
                                                         "canal_primeiro_video", "canal_idade_fonte", "canal_inscritos",
                                                         "canal_videos", "termo_busca")}]})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--termos", type=int, default=10, help="quantos termos dos nossos canais validar com a API")
    ap.add_argument("--termos-exploracao", type=int, default=10, help="quantos termos da exploração validar (janela de 30 dias)")
    ap.add_argument("--max-cota", type=int, default=2500)
    ap.add_argument("--teste", action="store_true")
    ap.add_argument("--sem-validar", action="store_true")
    ap.add_argument("--sem-banco", action="store_true")
    ap.add_argument("--sem-exploracao", action="store_true")
    ap.add_argument("--categorias", help="força as categorias da exploração (vírgula), em vez do rodízio da semana")
    ap.add_argument("--sufixo", help="sufixo dos arquivos de saída (ex.: v2 → <data>-v2.json), para não sobrescrever a execução do dia")
    ap.add_argument("--so-descoberta", action="store_true", help="parte 1: só o autocomplete (nossos + exploração, grátis); "
                    "salva <data>[-sufixo]-descoberta.json e sai (para caber no limite de 10 min por comando)")
    ap.add_argument("--descoberta", metavar="JSON", help="parte 2: carrega o autocomplete salvo pela parte 1 e segue "
                    "(em alta, validação, padrões, banco, relatório)")
    ap.add_argument("--seeds", default=SEEDS)
    ap.add_argument("--reusar", metavar="JSON", help="reaproveita a descoberta (autocomplete) e a validação de um .json "
                    "desta rotina; só revalida (com canais) os --termos melhores que ainda não têm dados de canais, "
                    "pulando os que deram amostra 0 (sem exploração)")
    a = ap.parse_args()
    if a.teste:
        a.termos, a.termos_exploracao, a.sem_banco = min(a.termos, 2), min(a.termos_exploracao, 2), True
        a.max_cota = min(a.max_cota, 600)
    cfg = yaml.safe_load(open(a.seeds))
    agora = dt.datetime.now(dt.timezone.utc)
    hoje = dt.date.today()
    avisos = []
    t0 = time.time()
    cota = Cota(a.max_cota)
    rod = rodizio(cfg, hoje, a.categorias.split(",") if a.categorias else None)

    sufixo = f"{'-teste' if a.teste else ''}{'-' + a.sufixo if a.sufixo else ''}"
    expl = []
    if a.descoberta:
        d = json.load(open(a.descoberta))
        itens, expl = d["itens"], d["expl"]
        termos, chamadas, falhas = {(t["idioma"], t["termo"]): t for t in itens}, d["chamadas"], d["falhas"]
        rod = d["rodizio"]
        avisos += d["avisos"] + [f"autocomplete carregado de {os.path.basename(a.descoberta)} (parte 1, {d['segundos']} s)"]
    elif a.reusar:
        velho = json.load(open(a.reusar))
        itens = [t for t in velho["itens"] if t["origem"] == "autocomplete"]
        termos, chamadas, falhas = {(t["idioma"], t["termo"]): t for t in itens}, 0, []
        avisos.append(f"descoberta reaproveitada de {os.path.basename(a.reusar)} ({len(itens)} termos; 0 chamadas de autocomplete)")
        a.sem_exploracao = True
    else:
        termos, chamadas, falhas = descobrir(cfg, a.teste, avisos)
        itens = list(termos.values())
        for t in itens:
            t["destino"] = destino(t["idioma"], t["termo"], cfg)
        normalizar_score(itens)

    if not a.descoberta and not a.reusar and not a.sem_exploracao and cfg.get("exploracao"):
        t_expl, c2, f2 = descobrir_exploracao(cfg, rod, a.teste, avisos)
        chamadas += c2
        falhas += f2
        expl = list(t_expl.values())
        for t in expl:
            t["destino"] = destino(t["idioma"], t["termo"], cfg)
            t["efemero"] = efemero_texto(t["termo"], cfg)
        normalizar_score(expl)
    if a.so_descoberta:
        os.makedirs(OUT, exist_ok=True)
        path = os.path.join(OUT, f"{hoje.isoformat()}{sufixo}-descoberta.json")
        for t in itens + expl:
            t["sementes"] = sorted(t.get("sementes", []))
        json.dump({"itens": itens, "expl": expl, "chamadas": chamadas, "falhas": falhas, "rodizio": rod, "avisos": avisos,
                   "segundos": round(time.time() - t0)}, open(path, "w"), ensure_ascii=False, default=str)
        print(f"parte 1 ok: {chamadas} chamadas, {len(falhas)} falhas, {len(itens)} + {len(expl)} termos, "
              f"{round(time.time() - t0)} s → {path}")
        return

    yt = None
    if not a.sem_validar:
        try:
            yt = yt_client()
        except Exception as e:  # noqa: BLE001
            avisos.append(f"sem cliente da API: {type(e).__name__}: {str(e)[:200]}")

    populares, trends = {}, {}
    if not a.sem_exploracao and cfg.get("exploracao"):
        populares, trends = em_alta(yt, cfg, cota, avisos, paginas=1 if a.teste else 2)
        alta = itens_em_alta(populares, trends, cfg, hoje)
        for t in alta:
            t["destino"] = destino(t["idioma"], t["termo"], cfg)
        normalizar_score(alta)
        expl += alta

    extras, outliers = {}, []
    if yt is not None:
        if a.reusar:  # só os já validados sem dados de canais, melhores primeiro, sem os de amostra 0
            fila = defaultdict(list)
            for t in sorted((t for t in itens if t.get("validado") and t.get("amostra") and t.get("canais_top10") is None),
                            key=lambda t: -(t.get("score") or 0)):
                fila[t["destino"]].append(t)
            alvos = []  # rodízio entre destinos para não deixar um canal sem dado
            while len(alvos) < a.termos and any(fila.values()):
                for d in DESTINOS:
                    if fila[d] and len(alvos) < a.termos:
                        alvos.append(fila[d].pop(0))
        else:
            nossos = escolher_para_validar(itens, cfg, a.termos, amostra_zero())
            de_fora = escolher_exploracao(expl, cfg, a.termos_exploracao, rod["categorias"], rod["semana"]) if expl else []
            alvos = []  # intercalados: se o teto de cota bater, os dois lados perdem igual
            for k in range(max(len(nossos), len(de_fora))):
                alvos += nossos[k:k + 1] + de_fora[k:k + 1]
        try:
            extras, outliers = validar(yt, alvos, cfg, cota, agora, avisos)
        except Exception as e:  # noqa: BLE001
            avisos.append(f"validação não rodou: {type(e).__name__}: {str(e)[:200]}")

    vids, garimpo = corpus_titulos(extras)
    pads = padroes_titulo(vids, hoje)
    for p in pads:
        p["destino"] = destino(p["idioma"], p["termo"], cfg)
    normalizar_score(pads)
    itens += pads + expl + linhas_outlier(outliers, hoje)

    data_ant, ant, hist = (None, {}, {}) if a.sem_banco and a.teste else anterior(hoje)
    for t in itens:
        t["score"] = pontuar(t)
        t["tendencia"] = tendencia(t, hist)
    atuais = {(t["idioma"], t["termo"], t["origem"]) for t in itens}
    sumiram = [f"{k[1]} [{k[0]}]" for k, r in sorted(ant.items(), key=lambda kv: -float(kv[1][3] or 0))
               if k not in atuais and k[2] in ("autocomplete", "titulo")][:20]

    gravados = None
    if not a.sem_banco:
        try:
            gravados = gravar(itens, hoje)
        except Exception as e:  # noqa: BLE001
            avisos.append(f"não gravou no banco: {type(e).__name__}: {e}")

    os.makedirs(OUT, exist_ok=True)
    base = os.path.join(OUT, f"{hoje.isoformat()}{sufixo}")
    for t in itens:
        t.pop("sementes", None)
        t.pop("titulos_set", None)
    fontes = defaultdict(int)
    for t in itens:
        if t.get("validado") and t.get("idade_fonte"):
            fontes[t["idade_fonte"]] += 1
    r = {"data": hoje.isoformat(), "teste": a.teste, "gerado_em": agora.isoformat(), "segundos": round(time.time() - t0),
         "chamadas_autocomplete": chamadas, "falhas_autocomplete": falhas, "cota_gasta": cota.gasto, "max_cota": a.max_cota,
         "cota_por_tipo": dict(cota.por_tipo), "rodizio": rod,
         "n_autocomplete": len(termos), "n_exploracao": sum(t["origem"] == "exploracao_semente" for t in expl),
         "n_titulo": len(pads), "titulos_corpus": len(vids), "garimpo": garimpo,
         "n_validados": sum(bool(t.get("validado")) for t in itens), "anterior": str(data_ant) if data_ant else None,
         "fontes_idade": ", ".join(f"{k} {v}" for k, v in fontes.items()) or "—",
         "gravados_no_banco": gravados, "avisos": avisos, "sumiram": sumiram, "populares": populares, "trends": trends,
         "itens": sorted(itens, key=lambda t: (not t.get("validado"), -t["score"]))}
    json.dump(r, open(base + ".json", "w"), ensure_ascii=False, separators=(",", ":"), default=str)  # compacto (vai para o git)
    escrever_md(base + ".md", r)
    print(open(base + ".md").read())
    print(f"(json: {base}.json · banco: {gravados if gravados is not None else 'não gravado'} linhas · cota {cota.gasto} · {r['segundos']} s)")


if __name__ == "__main__":
    main()
