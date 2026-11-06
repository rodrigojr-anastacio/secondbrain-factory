"""Rotina semanal de palavras-chave (quarta 09:30): termos e padrões de busca em alta no YouTube → sugestões.

Uso: ~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/tools/keywords.py
       [--termos 20] [--max-cota 2500] [--teste] [--sem-validar] [--sem-banco]

1. Descoberta (grátis): autocomplete do YouTube (suggestqueries, via WARP socks5://127.0.0.1:40000, com pausa)
   a partir de pesquisa/keyword_seeds.yaml (sementes por idioma, expandidas com " a" … " z", + temas do backlog).
2. Padrões de título: n-gramas de 2–4 palavras (dígitos viram N) dos títulos de youtube.garimpo_videos, do último
   garimpo (pesquisa/tendencias/<data>.json) e dos resultados da validação, por idioma, pesados por views/dia de vida.
3. Validação (cota): para os ~20 melhores termos, search.list (100 un.) + videos.list (1 un.): mediana de views do
   top-10 (12 meses), vídeos < 90 dias com > 100 mil e vídeos que já usam um molde nosso. Para no teto de cota.
4. Grava em youtube.palavras_chave (tools/db/schema_palavras_chave.sql) com a tendência contra a execução anterior
   e salva pesquisa/palavras-chave/<data>.json e .md.
--teste: só sementes "simples" e do backlog (sem a–z), valida no máximo 3 termos, não grava no banco, sufixo -teste.
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
CUSTO_SEARCH, CUSTO_VIDEOS = 100, 1

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


def descobrir(cfg, teste, log):
    termos = {}  # (idioma, termo) -> dict
    chamadas, falhas = 0, []
    for lang, grupos in cfg["idiomas"].items():
        consultas = []  # (q, é_base)
        if not teste:
            for s in grupos.get("expandir", []):
                consultas.append((s, True))
                consultas += [(f"{s} {c}", False) for c in "abcdefghijklmnopqrstuvwxyz"]
        consultas += [(s, True) for s in grupos.get("simples", [])]
        consultas += [(s, True) for s in cfg.get("backlog", {}).get(lang, [])]
        for q, base in consultas:
            if len(falhas) >= 10 and chamadas <= len(falhas) * 2:
                log.append(f"autocomplete abortado em {lang}: {len(falhas)} falhas (WARP fora?)")
                return termos, chamadas, falhas
            sugestoes = autocomplete(q, lang, falhas)
            chamadas += 1
            time.sleep(0.35 + random.random() * 0.3)
            if not sugestoes:
                continue
            n = max(len(sugestoes), 10)
            for pos, s in enumerate(sugestoes):
                s = re.sub(r"\s+", " ", s.strip().lower())
                if len(s) < 4:
                    continue
                t = termos.setdefault((lang, s), {"idioma": lang, "termo": s, "origem": "autocomplete", "aparicoes": 0,
                                                  "melhor_posicao": 99, "bruto": 0.0, "sementes": set()})
                t["aparicoes"] += 1
                t["melhor_posicao"] = min(t["melhor_posicao"], pos + 1)
                t["bruto"] += (1 - pos / n) * (2 if base else 1)
                t["sementes"].add(q)
    return termos, chamadas, falhas


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


def escolher_para_validar(itens, cfg, n):
    sementes = {norm(x) for g in cfg["idiomas"].values() for k in ("expandir", "simples") for x in g.get(k, [])}
    cotas = {"dossie-es": 5, "historia-ptbr": 5, "lotr-fr": 4, "novo-canal": 6}
    fator = n / sum(cotas.values())
    cotas = {k: max(1, round(v * fator)) for k, v in cotas.items()}
    escolhidos, por_lang_novo = [], defaultdict(int)
    for dest, q in cotas.items():
        cand = sorted((t for t in itens if t["destino"] == dest and t["origem"] == "autocomplete"),
                      key=lambda t: (-t["score_descoberta"], -t["aparicoes"]))
        pegos = []
        for t in cand:
            if dest == "novo-canal" and (len(t["termo"].split()) < 3 or por_lang_novo[t["idioma"]] >= 2 or norm(t["termo"]) in sementes):
                continue
            toks = set(norm(t["termo"]).split())
            if any(p["idioma"] == t["idioma"] and (toks <= set(norm(p["termo"]).split()) or set(norm(p["termo"]).split()) <= toks) for p in pegos):
                continue
            pegos.append(t)
            if dest == "novo-canal":
                por_lang_novo[t["idioma"]] += 1
            if len(pegos) >= q:
                break
        escolhidos += pegos
    return escolhidos[:n]


def validar(yt, alvos, cfg, max_cota, hoje_dt, log):
    cota, extras = 0, {}
    desde = (hoje_dt - dt.timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
    moldes = [norm(m) for m in cfg.get("moldes", [])]
    for t in alvos:
        if cota + CUSTO_SEARCH + CUSTO_VIDEOS > max_cota:
            log.append(f"teto de cota ({max_cota}) atingido; {t['termo']!r} e os seguintes ficaram sem validação")
            break
        try:
            r = yt.search().list(part="snippet", q=t["termo"], type="video", order="viewCount", publishedAfter=desde,
                                 relevanceLanguage=t["idioma"], maxResults=50).execute()
            cota += CUSTO_SEARCH
            ids = [i["id"]["videoId"] for i in r.get("items", []) if i["id"].get("videoId")]
            vids = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids)).execute().get("items", []) if ids else []
            cota += CUSTO_VIDEOS if ids else 0
        except Exception as e:  # noqa: BLE001
            log.append(f"validação de {t['termo']!r} falhou: {type(e).__name__}: {str(e)[:200]}")
            if "quotaExceeded" in str(e):
                break
            continue
        lst, toks, fora = [], tokens_conteudo(t["termo"], t["idioma"]), 0
        for v in vids:
            if segundos(v.get("contentDetails", {}).get("duration")) <= 75:  # sem Shorts (nossos vídeos são longos)
                fora += 1
                continue
            decl = (v["snippet"].get("defaultAudioLanguage") or v["snippet"].get("defaultLanguage") or "")[:2]
            if (decl and decl != t["idioma"]) or not relevante(v["snippet"]["title"], toks, t["termo"], t["idioma"]):
                fora += 1
                continue
            views = int(v["statistics"].get("viewCount", 0))
            pub = v["snippet"]["publishedAt"]
            idade = (hoje_dt - dt.datetime.fromisoformat(pub.replace("Z", "+00:00"))).days
            lst.append({"id": v["id"], "titulo": v["snippet"]["title"], "canal": v["snippet"]["channelTitle"],
                        "canal_id": v["snippet"]["channelId"], "views": views, "publicado": pub[:10], "idade": idade})
            extras[v["id"]] = {"titulo": v["snippet"]["title"], "canal": v["snippet"]["channelId"], "publicado": pub[:10],
                               "views": views}
        lst.sort(key=lambda x: -x["views"])
        top10 = [x["views"] for x in lst[:10]]
        t["validado"] = True
        t["mediana_top10"] = int(statistics.median(top10)) if top10 else 0
        t["recentes_100k"] = sum(x["idade"] < 90 and x["views"] > 100_000 for x in lst)
        t["no_molde"] = sum(any(m in norm(x["titulo"]) for m in moldes) for x in lst)
        t["amostra"] = len(lst)
        t["fora_do_tema"] = fora
        t["exemplos"] = [{k: x[k] for k in ("id", "titulo", "canal", "views", "publicado")} for x in lst[:3]]
    return cota, extras


def pontuar(t):
    """Validado: demanda (10·log10 mediana) + tração (4 por vídeo recente > 100 mil, máx. 10) − concorrência no molde
    (3 por vídeo, máx. 5) + descoberta (0–10). Não validado: só a descoberta (0–10)."""
    if t.get("validado"):
        return round(10 * math.log10(1 + t["mediana_top10"]) + 4 * min(t["recentes_100k"], 10)
                     - 3 * min(t["no_molde"], 5) + t["score_descoberta"], 2)
    return t["score_descoberta"]


# ---------- 4. tendência e gravação ----------
def anterior(hoje):
    try:
        with conectar() as con:
            d = con.execute("SELECT max(data) FROM palavras_chave WHERE data < %s", (hoje,)).fetchone()[0]
            if not d:
                return None, {}
            rows = con.execute("SELECT idioma, termo, origem, score_descoberta, destino, validado, mediana_top10 "
                               "FROM palavras_chave WHERE data = %s", (d,)).fetchall()
            return d, {(r[0], r[1], r[2]): r for r in rows}
    except Exception as e:  # noqa: BLE001
        print(f"[db] aviso: sem execução anterior ({e})", file=sys.stderr)
        return None, {}


def tendencia(t, ant):
    a = ant.get((t["idioma"], t["termo"], t["origem"]))
    if not a:
        return "novo"
    prev = float(a[3] or 0)
    if t["score_descoberta"] > prev * 1.2 + 0.2:
        return "subindo"
    if t["score_descoberta"] < prev * 0.8 - 0.2:
        return "caindo"
    return "estavel"


def gravar(itens, hoje):
    with conectar() as con:
        for t in itens:
            con.execute(
                "INSERT INTO palavras_chave (data, idioma, termo, origem, destino, aparicoes, melhor_posicao, score_descoberta,"
                " validado, mediana_top10, recentes_100k, no_molde, amostra, exemplos, score, tendencia)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                " ON CONFLICT (data, idioma, termo, origem) DO UPDATE SET destino=EXCLUDED.destino, aparicoes=EXCLUDED.aparicoes,"
                " melhor_posicao=EXCLUDED.melhor_posicao, score_descoberta=EXCLUDED.score_descoberta, validado=EXCLUDED.validado,"
                " mediana_top10=EXCLUDED.mediana_top10, recentes_100k=EXCLUDED.recentes_100k, no_molde=EXCLUDED.no_molde,"
                " amostra=EXCLUDED.amostra, exemplos=EXCLUDED.exemplos, score=EXCLUDED.score, tendencia=EXCLUDED.tendencia,"
                " criado_em=now()",
                (hoje, t["idioma"], t["termo"], t["origem"], t["destino"], t["aparicoes"], t.get("melhor_posicao"),
                 t["score_descoberta"], t.get("validado", False), t.get("mediana_top10"), t.get("recentes_100k"),
                 t.get("no_molde"), t.get("amostra"), Jsonb(t["exemplos"]) if t.get("exemplos") else None, t["score"],
                 t["tendencia"]))
    return len(itens)


def fmt(n):
    return "—" if n is None else f"{n:,}".replace(",", ".")


def escrever_md(path, r):
    L = [f"# Palavras-chave — {r['data']}{' (teste)' if r['teste'] else ''}", "",
         f"Autocomplete: {r['chamadas_autocomplete']} chamadas ({len(r['falhas_autocomplete'])} falhas), "
         f"{r['n_autocomplete']} termos. Padrões de título: {r['n_titulo']} n-gramas ({r['titulos_corpus']} títulos; garimpo {r['garimpo']}). "
         f"Validação: {r['n_validados']} termos, **{r['cota_gasta']} unidades de cota** (teto {r['max_cota']}). "
         f"Execução anterior: {r['anterior'] or 'nenhuma'}.", ""]
    for l in r["avisos"]:
        L.append(f"- ⚠ {l}")
    itens = r["itens"]
    L += ["", "## Termos validados (YouTube Data API: 50 mais vistos dos últimos 12 meses (order=viewCount), só vídeos longos com as palavras do termo no título e no idioma)", "",
          "| Destino | Idioma | Termo | Med. top-10 | Recentes >100 mil (<90 d) | No molde | Score | Tendência | Top vídeo |",
          "|---|---|---|---|---|---|---|---|---|"]
    for t in sorted((t for t in itens if t.get("validado")), key=lambda t: (t["destino"], -t["score"])):
        ex = t["exemplos"][0] if t.get("exemplos") else None
        top = f"{ex['titulo'][:60]} ({fmt(ex['views'])}, {ex['canal'][:25]})" if ex else "—"
        L.append(f"| {t['destino']} | {t['idioma']} | {t['termo']} | {fmt(t['mediana_top10'])} | {t['recentes_100k']} | "
                 f"{t['no_molde']}/{t['amostra']} | {t['score']} | {t['tendencia']} | {top.replace('|', '/')} |")
    L += ["", "## Autocomplete por destino (top 15, não validados)", ""]
    for dest in ("dossie-es", "historia-ptbr", "lotr-fr", "novo-canal"):
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--termos", type=int, default=20, help="quantos termos validar com a API")
    ap.add_argument("--max-cota", type=int, default=2500)
    ap.add_argument("--teste", action="store_true")
    ap.add_argument("--sem-validar", action="store_true")
    ap.add_argument("--sem-banco", action="store_true")
    ap.add_argument("--seeds", default=SEEDS)
    a = ap.parse_args()
    if a.teste:
        a.termos, a.max_cota, a.sem_banco = min(a.termos, 3), min(a.max_cota, 3 * (CUSTO_SEARCH + CUSTO_VIDEOS)), True
    cfg = yaml.safe_load(open(a.seeds))
    agora = dt.datetime.now(dt.timezone.utc)
    hoje = dt.date.today()
    avisos = []
    t0 = time.time()

    termos, chamadas, falhas = descobrir(cfg, a.teste, avisos)
    itens = list(termos.values())
    for t in itens:
        t["destino"] = destino(t["idioma"], t["termo"], cfg)
    normalizar_score(itens)

    cota, extras = 0, {}
    if not a.sem_validar:
        alvos = escolher_para_validar(itens, cfg, a.termos)
        try:
            cota, extras = validar(yt_client(), alvos, cfg, a.max_cota, agora, avisos)
        except Exception as e:  # noqa: BLE001
            avisos.append(f"validação não rodou: {type(e).__name__}: {str(e)[:200]}")

    vids, garimpo = corpus_titulos(extras)
    pads = padroes_titulo(vids, hoje)
    for p in pads:
        p["destino"] = destino(p["idioma"], p["termo"], cfg)
    normalizar_score(pads)
    itens += pads

    data_ant, ant = (None, {}) if a.sem_banco and a.teste else anterior(hoje)
    for t in itens:
        t["score"] = pontuar(t)
        t["tendencia"] = tendencia(t, ant)
    atuais = {(t["idioma"], t["termo"], t["origem"]) for t in itens}
    sumiram = [f"{k[1]} [{k[0]}]" for k, r in sorted(ant.items(), key=lambda kv: -float(kv[1][3] or 0)) if k not in atuais][:20]

    gravados = None
    if not a.sem_banco:
        try:
            gravados = gravar(itens, hoje)
        except Exception as e:  # noqa: BLE001
            avisos.append(f"não gravou no banco: {type(e).__name__}: {e}")

    os.makedirs(OUT, exist_ok=True)
    base = os.path.join(OUT, f"{hoje.isoformat()}{'-teste' if a.teste else ''}")
    for t in itens:
        t.pop("sementes", None)
        t.pop("titulos_set", None)
    r = {"data": hoje.isoformat(), "teste": a.teste, "gerado_em": agora.isoformat(), "segundos": round(time.time() - t0),
         "chamadas_autocomplete": chamadas, "falhas_autocomplete": falhas, "cota_gasta": cota, "max_cota": a.max_cota,
         "n_autocomplete": len(termos), "n_titulo": len(pads), "titulos_corpus": len(vids), "garimpo": garimpo,
         "n_validados": sum(bool(t.get("validado")) for t in itens), "anterior": str(data_ant) if data_ant else None,
         "gravados_no_banco": gravados, "avisos": avisos, "sumiram": sumiram,
         "itens": sorted(itens, key=lambda t: (not t.get("validado"), -t["score"]))}
    json.dump(r, open(base + ".json", "w"), ensure_ascii=False, indent=1, default=str)
    escrever_md(base + ".md", r)
    print(open(base + ".md").read())
    print(f"(json: {base}.json · banco: {gravados if gravados is not None else 'não gravado'} linhas · cota {cota} · {r['segundos']} s)")


if __name__ == "__main__":
    main()
