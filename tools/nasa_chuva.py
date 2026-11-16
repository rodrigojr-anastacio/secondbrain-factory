"""Chuva real da NASA (GPM IMERG V07, GES DISC) para o mapa do Em Relevo (e qualquer canal): acumulado no período,
anomalia opcional e 3 saídas prontas para compor.

Uso (rode de tools/ ou com caminho absoluto):
  tools/.venv/bin/python tools/nasa_chuva.py --inicio 2024-04-27 --fim 2024-05-05 --regiao RS --saida <pasta> [--nome enchente-rs]
  tools/.venv/bin/python tools/nasa_chuva.py --data 2024-05-02 --bbox -54,-31,-50,-28 --saida <pasta>
  ... --anomalia            # também: anomalia × climatologia mensal IMERG (padrão 2001–2020; +20–40 requisições pequenas)
  ... --mascara             # zera fora do Brasil/UF da região (camada só sobre terra brasileira; útil em UF)
  ... --fundo claro         # PNG de tela em papel claro (thumb documento-evidencia: a regra do canal permite só 1 thumb com mapa escuro)
  ... --vmax 500            # topo fixo da escala de cor (mm); padrão: automático (percentil 99,5 arredondado)
  tools/.venv/bin/python tools/nasa_chuva.py --regioes   # lista as regiões prontas

Saídas em <saida>/ (prefixo = --nome ou chuva-<regiao>-<inicio>_<fim>):
  1. <prefixo>-camada.png   RGBA transparente, sem texto, georreferenciado em lon/lat (plate carrée) no bbox do JSON:
                            pixel (x, y) ↔ lon = oeste + (x + 0,5)·(leste − oeste)/largura; lat = norte − (y + 0,5)·(norte − sul)/altura.
                            Linha 0 = norte. Vira textura/camada sobre o terreno 3D (mesmo bbox) ou sobre o mapa 2D.
     <prefixo>-camada.pgw   world file (para conferir em GIS).
  2. <prefixo>-tela.png     1920×1080 pronto para tela/thumb: fundo navy, UFs (IBGE) e países vizinhos (Natural Earth), chuva, legenda mínima em pt-BR (mm) e período.
                            Sem crédito na tela (regra do canal: crédito só na descrição).
  3. <prefixo>.json         bbox, período, produto e arquivos usados, mm máx (e onde; max_terra = só dentro das UFs da região), mm médio (bbox e área mascarada/UF),
                            escala de cor (para o código desenhar a legenda), anomalia (se pedida) e a linha de crédito.
  Com --anomalia: também <prefixo>-anomalia-camada.png e <prefixo>-anomalia-tela.png (marrom = abaixo, azul = acima da média).

Dados: GPM_3IMERGDF.07 (Final, diário, 0,1°, jun/2000 em diante, ~3,5 meses de atraso); dias mais recentes caem no
GPM_3IMERGDL.07 (Late, ~1 dia de atraso) e o JSON diz qual foi usado. Climatologia: GPM_3IMERGM.07 (mensal).
Antes de 01/06/2000 não há IMERG: a ferramenta para e sugere a alternativa já usada no canal.
Acesso: OPeNDAP do GES DISC só com o recorte (poucos KB por dia), token Earthdata de ~/.segredos/nasa/earthdata.env
(EARTHDATA_TOKEN, header Authorization: Bearer). O token nunca é impresso nem gravado. Cache em $HOME/cache/nasa/.
Licença: dados da NASA, domínio público; crédito na descrição: "Chuva: NASA GPM IMERG (GES DISC), domínio público".
"""
import argparse
import datetime as dt
import json
import math
import os
import re
import struct
import sys
import time

import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFont

CACHE = os.path.join(os.path.expanduser("~"), "cache", "nasa")
OPENDAP = "https://gpm1.gesdisc.eosdis.nasa.gov/opendap/GPM_L3"
PROD_FINAL, PROD_LATE, PROD_MES = "GPM_3IMERGDF.07", "GPM_3IMERGDL.07", "GPM_3IMERGM.07"
INICIO_IMERG = dt.date(2000, 6, 1)
CREDITO = "Chuva: NASA GPM IMERG (GES DISC), domínio público"
FAB = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
FONTES = os.path.join(FAB, "pesquisa/canal-clima-2026-11/identidade/fontes")
NAVY, BRANCO = (31, 42, 68), (251, 248, 241)

# bbox = (oeste, sul, leste, norte), graus; folga de ~0,3° em volta dos limites IBGE
REGIOES = {
    "BRASIL": (-74.5, -34.2, -34.3, 5.6), "SUL": (-58.0, -34.2, -47.8, -22.2), "SUDESTE": (-53.4, -25.6, -38.8, -14.0),
    "NORDESTE": (-48.9, -18.6, -34.4, -0.7), "NORTE": (-74.5, -13.9, -45.7, 5.6), "CENTRO-OESTE": (-61.9, -24.4, -45.7, -7.1),
    "RS": (-57.9, -34.0, -49.4, -26.8), "SC": (-54.0, -29.6, -48.1, -25.7), "PR": (-55.0, -26.9, -47.8, -22.3),
    "SP": (-53.4, -25.6, -44.0, -19.5), "RJ": (-45.1, -23.6, -40.7, -20.5), "MG": (-51.3, -23.1, -39.6, -14.0),
    "ES": (-41.9, -21.6, -39.4, -17.6), "BA": (-46.9, -18.6, -37.1, -8.3), "PE": (-41.6, -9.8, -34.6, -7.0),
    "CE": (-41.7, -8.1, -37.0, -2.5), "AM": (-73.9, -9.9, -56.0, 2.5), "PA": (-59.0, -10.2, -45.9, 2.9),
    "MT": (-61.9, -18.3, -50.0, -7.1), "MS": (-58.4, -24.4, -50.7, -17.0), "GO": (-53.5, -19.8, -45.7, -12.1),
}
UF_COD = {"11": "RO", "12": "AC", "13": "AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO", "21": "MA", "22": "PI", "23": "CE",
          "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE", "29": "BA", "31": "MG", "32": "ES", "33": "RJ", "35": "SP",
          "41": "PR", "42": "SC", "43": "RS", "50": "MS", "51": "MT", "52": "GO", "53": "DF"}
REGIAO_UFS = {"SUL": ["PR", "SC", "RS"], "SUDESTE": ["SP", "RJ", "MG", "ES"], "NORTE": ["RO", "AC", "AM", "RR", "PA", "AP", "TO"],
              "NORDESTE": ["MA", "PI", "CE", "RN", "PB", "PE", "AL", "SE", "BA"], "CENTRO-OESTE": ["MS", "MT", "GO", "DF"]}

# escala de chuva acumulada (fração do vmax → cor, alfa); abaixo de 3% do vmax fica transparente
ESCALA = [(0.00, (159, 232, 255), 0), (0.03, (159, 232, 255), 90), (0.15, (63, 216, 255), 170), (0.35, (47, 123, 255), 205),
          (0.60, (124, 58, 237), 225), (0.82, (232, 64, 160), 238), (1.00, (255, 210, 63), 245)]
ESCALA_ANOM = [(0.0, (140, 81, 10), 230), (0.3, (216, 179, 101), 170), (0.45, (246, 232, 195), 0), (0.55, (199, 234, 229), 0),
               (0.7, (90, 180, 172), 170), (1.0, (1, 102, 94), 230)]


# ---------------------------------------------------------------- acesso
def token():
    p = os.path.expanduser("~/.segredos/nasa/earthdata.env")
    for linha in open(p):
        if linha.strip().startswith("EARTHDATA_TOKEN="):
            return linha.split("=", 1)[1].strip().strip("'\"")
    sys.exit("EARTHDATA_TOKEN não encontrado em ~/.segredos/nasa/earthdata.env (peça ao Rodrigo; nunca cole o token aqui)")


SESS = requests.Session()


def baixar(url, tentativas=4):
    if "Authorization" not in SESS.headers:
        SESS.headers["Authorization"] = f"Bearer {token()}"
    for i in range(tentativas):
        try:
            r = SESS.get(url, timeout=120)
            if r.status_code == 200:
                return r.content
            if r.status_code in (401, 403):
                sys.exit(f"GES DISC recusou o acesso (HTTP {r.status_code}): token vencido (vale até 15/01/2027) ou app "
                         "'NASA GESDISC DATA ARCHIVE' desautorizado na conta Earthdata. Peça ao Rodrigo para renovar.")
            if r.status_code == 404:
                return None
        except requests.RequestException:
            pass
        time.sleep(3 * (i + 1))
    sys.exit(f"Falha ao baixar do GES DISC depois de {tentativas} tentativas: {url.split('?')[0]}")


def listagem(prod, ano, mes=None):
    """Nomes dos arquivos de um mês (diário) ou ano (mensal). Cache de 1 dia para meses recentes, permanente para antigos."""
    sub = f"{ano}/{mes:02d}/" if mes else f"{ano}/"
    cp = os.path.join(CACHE, "listas", prod, sub.replace("/", "_") + "lista.json")
    antigo = dt.date(ano, mes or 12, 1) < dt.date.today() - dt.timedelta(days=150)
    if os.path.exists(cp) and (antigo or time.time() - os.path.getmtime(cp) < 86400):
        return json.load(open(cp))
    html = baixar(f"{OPENDAP}/{prod}/{sub}contents.html")
    nomes = sorted(set(re.findall(r"3B-[^\"<>/ ]+?\.(?:nc4|HDF5)", html.decode("utf-8", "ignore")))) if html else []
    os.makedirs(os.path.dirname(cp), exist_ok=True)
    json.dump(nomes, open(cp, "w"))
    return nomes


def ler_dods(raw, n_esperado):
    """DAP2 binário (.dods) de UM array Float32: DDS em texto, 'Data:\\n', 2× uint32 (n), n float32 big-endian."""
    i = raw.find(b"\nData:\n")
    if i < 0:
        raise ValueError("resposta OPeNDAP sem bloco Data")
    corpo = raw[i + 7:]
    n, n2 = struct.unpack(">II", corpo[:8])
    if n != n_esperado or n2 != n_esperado:
        raise ValueError(f"tamanho inesperado no OPeNDAP: {n} (esperado {n_esperado})")
    return np.frombuffer(corpo[8:8 + 4 * n], dtype=">f4").astype(np.float32)


def indices(bbox):
    o, s, l, n = bbox
    i0, i1 = int(math.floor((o + 180) / 0.1)), int(math.ceil((l + 180) / 0.1)) - 1
    j0, j1 = int(math.floor((s + 90) / 0.1)), int(math.ceil((n + 90) / 0.1)) - 1
    return max(0, i0), min(3599, i1), max(0, j0), min(1799, j1)


def grade(prod, caminho, idx, cache_nome):
    """Recorte de precipitation [lon][lat] → array (nlat, nlon) com linha 0 = SUL (ordem do IMERG). NaN = sem dado."""
    i0, i1, j0, j1 = idx
    cp = os.path.join(CACHE, "imerg", prod, f"{cache_nome}_{i0}_{i1}_{j0}_{j1}.npy")
    if os.path.exists(cp):
        return np.load(cp)
    q = f"precipitation[0:1:0][{i0}:1:{i1}][{j0}:1:{j1}]"
    raw = baixar(f"{OPENDAP}/{prod}/{caminho}.dods?{q}")
    if raw is None:
        return None
    nlon, nlat = i1 - i0 + 1, j1 - j0 + 1
    v = ler_dods(raw, nlon * nlat).reshape(nlon, nlat).T.copy()
    v[v < -9000] = np.nan
    os.makedirs(os.path.dirname(cp), exist_ok=True)
    np.save(cp, v)
    return v


def dia(d, idx):
    """mm no dia d (Final; se ainda não saiu, Late). Devolve (array, produto, arquivo)."""
    for prod in (PROD_FINAL, PROD_LATE):
        nomes = [x for x in listagem(prod, d.year, d.month) if f".{d:%Y%m%d}-" in x]
        if nomes:
            v = grade(prod, f"{d.year}/{d.month:02d}/{nomes[-1]}", idx, f"{d:%Y%m%d}")
            if v is not None:
                return v, prod, nomes[-1]
    return None, None, None


def climatologia_mes(ano_ini, ano_fim, mes, idx):
    """Média de mm/dia no mês `mes` em ano_ini..ano_fim (IMERG mensal, mm/h × 24)."""
    pilha = []
    for ano in range(ano_ini, ano_fim + 1):
        nomes = [x for x in listagem(PROD_MES, ano) if f".{ano}{mes:02d}01-" in x]
        if not nomes:
            continue
        v = grade(PROD_MES, f"{ano}/{nomes[-1]}", idx, f"mes{ano}{mes:02d}")
        if v is not None:
            pilha.append(v * 24.0)
    if not pilha:
        sys.exit(f"Sem IMERG mensal para o mês {mes} em {ano_ini}–{ano_fim}")
    return np.nanmean(np.stack(pilha), axis=0), len(pilha)


# ---------------------------------------------------------------- geografia (IBGE)
def ufs_geo():
    """Polígonos das UFs (IBGE malhas v3, qualidade mínima), em cache. Devolve {sigla: [anéis [(lon, lat)…]]}."""
    cp = os.path.join(CACHE, "ibge-ufs.geojson")
    if not os.path.exists(cp):
        url = ("https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo%2Bjson"
               "&intrarregiao=UF&qualidade=minima")
        try:
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            os.makedirs(CACHE, exist_ok=True)
            open(cp, "wb").write(r.content)
        except requests.RequestException:
            return {}
    out = {}
    for f in json.load(open(cp))["features"]:
        sig = UF_COD.get(str(f["properties"].get("codarea")), "?")
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        out[sig] = [ring for poly in polys for ring in poly[:1]]
    return out


def paises_geo(bbox):
    """Contornos de países (Natural Earth 1:50m, domínio público) que tocam o bbox, menos o Brasil (o Brasil vem do IBGE)."""
    cp = os.path.join(CACHE, "ne_50m_admin_0_countries.geojson")
    if not os.path.exists(cp):
        try:
            r = requests.get("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
                             "ne_50m_admin_0_countries.geojson", timeout=120)
            r.raise_for_status()
            os.makedirs(CACHE, exist_ok=True)
            open(cp, "wb").write(r.content)
        except requests.RequestException:
            return []
    o, s, l, n = bbox
    out = []
    for f in json.load(open(cp))["features"]:
        if f["properties"].get("ADM0_A3") == "BRA":
            continue
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            ring = poly[0]
            xs, ys = [p[0] for p in ring], [p[1] for p in ring]
            if max(xs) >= o and min(xs) <= l and max(ys) >= s and min(ys) <= n:
                out.append(ring)
    return out


def mascara(ufs, siglas, bbox, shape):
    """Máscara booleana (linha 0 = norte) das UFs `siglas` na grade (shape) do bbox."""
    h, w = shape
    o, s, l, n = bbox
    im = Image.new("L", (w * 4, h * 4), 0)
    d = ImageDraw.Draw(im)
    for sig in siglas:
        for ring in ufs.get(sig, []):
            d.polygon([((x - o) / (l - o) * w * 4, (n - y) / (n - s) * h * 4) for x, y in ring], fill=255)
    return np.asarray(im.resize((w, h), Image.BILINEAR)) > 127


# ---------------------------------------------------------------- cor e imagens
def colorir(v, vmin, vmax, escala):
    t = np.clip((v - vmin) / (vmax - vmin), 0, 1)
    rgba = np.zeros(v.shape + (4,), dtype=np.float32)
    pos = [e[0] for e in escala]
    for c in range(3):
        rgba[..., c] = np.interp(t, pos, [e[1][c] for e in escala])
    rgba[..., 3] = np.interp(t, pos, [e[2] for e in escala])
    rgba[np.isnan(v)] = 0
    return Image.fromarray(rgba.astype(np.uint8), "RGBA")


def ampliar(v_norte, largura):
    """Interpola a grade 0,1° (linha 0 = norte) para `largura` px mantendo o aspecto em graus (bicúbica)."""
    h, w = v_norte.shape
    alt = max(1, round(largura * h / w))
    vv = np.where(np.isnan(v_norte), 0, v_norte).astype(np.float32)
    im = Image.fromarray(vv, "F").resize((largura, alt), Image.BICUBIC)
    out = np.asarray(im).copy()
    nan = Image.fromarray(np.isnan(v_norte).astype(np.uint8) * 255).resize((largura, alt), Image.NEAREST)
    out[np.asarray(nan) > 0] = np.nan
    return np.clip(out, 0, None) if np.nanmin(v_norte) >= 0 else out


def topo_auto(v):
    p = float(np.nanpercentile(v, 99.5))
    for passo in (10, 25, 50, 100, 250, 500, 1000):
        if p / passo <= 8:
            return max(passo, math.ceil(p / passo) * passo)
    return math.ceil(p / 1000) * 1000


def fonte(nome, tam):
    try:
        return ImageFont.truetype(os.path.join(FONTES, nome), tam)
    except OSError:
        return ImageFont.load_default()


MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]


def periodo_pt(a, b):
    f = lambda d, ano=True: f"{d.day} {MESES[d.month - 1]}" + (f" {d.year}" if ano else "")
    return f(a) if a == b else f"{f(a, a.year != b.year)} – {f(b)}"


def tela(v_norte, bbox, escala, vmin, vmax, titulo, periodo, ufs, destaque, destino, ticks, unidade="mm", fundo="navy"):
    W, H = 1920, 1080
    if fundo == "claro":  # papel (#E9DCC3) e terra branco-papel; texto e linhas em tinta (#2B2622)
        MAR, TERRA, LINHA, TXT, DATA = (233, 220, 195), (251, 248, 241), (43, 38, 34), (43, 38, 34), (232, 80, 91)
    else:
        MAR, TERRA, LINHA, TXT, DATA = NAVY, (44, 57, 88), BRANCO, BRANCO, (255, 210, 63)
    o, s, l, n = bbox
    cosl = math.cos(math.radians((s + n) / 2))
    larg_g, alt_g = (l - o) * cosl, (n - s)
    area = (60, 60, 1480, 1020)  # caixa do mapa
    k = min((area[2] - area[0]) / larg_g, (area[3] - area[1]) / alt_g)
    mw, mh = int(larg_g * k), int(alt_g * k)
    x0, y0 = area[0] + (area[2] - area[0] - mw) // 2, area[1] + (area[3] - area[1] - mh) // 2
    im = Image.new("RGBA", (W, H), MAR + (255,))
    camada = colorir(ampliar(v_norte, mw), vmin, vmax, escala).resize((mw, mh), Image.BILINEAR)
    xy = lambda lon, lat: (x0 + (lon - o) / (l - o) * mw, y0 + (n - lat) / (n - s) * mh)
    fundo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(fundo)
    vizinhos = paises_geo(bbox)
    for ring in vizinhos + [r for rings in ufs.values() for r in rings]:  # terra um pouco mais clara que o mar
        d.polygon([xy(*p) for p in ring], fill=TERRA + (255,))
    im.alpha_composite(fundo)
    im.alpha_composite(camada, (x0, y0))
    lin = ImageDraw.Draw(im)
    for ring in vizinhos:
        pts = [xy(*p) for p in ring]
        lin.line(pts + pts[:1], fill=LINHA + (80,), width=1)
    for sig, rings in ufs.items():
        for ring in rings:
            pts = [xy(*p) for p in ring]
            lin.line(pts + pts[:1], fill=LINHA + ((235,) if sig in destaque else (110,)), width=3 if sig in destaque else 1)
    # recorta o que vazou para fora da caixa do mapa
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).rectangle((x0, y0, x0 + mw, y0 + mh), fill=255)
    im = Image.composite(im, Image.new("RGBA", (W, H), MAR + (255,)), m)
    # legenda: barra vertical + rótulos em mm + período
    d = ImageDraw.Draw(im)
    bx, by, bw, bh = 1590, 300, 46, 560
    grad = np.linspace(vmax, vmin, bh)[:, None].repeat(bw, 1)
    barra = colorir(grad, vmin, vmax, [(p, c, max(a, 255 if p > 0 else a)) for p, c, a in escala])
    fundo_barra = Image.new("RGBA", (bw, bh), TERRA + (255,))
    fundo_barra.alpha_composite(barra)
    im.alpha_composite(fundo_barra, (bx, by))
    d.rectangle((bx, by, bx + bw, by + bh), outline=TXT + (200,), width=2)
    f_t, f_n, f_p = fonte("IBMPlexMono-Bold.ttf", 24), fonte("IBMPlexMono-Medium.ttf", 28), fonte("Anton-Regular.ttf", 54)
    for t in ticks:
        y = by + (vmax - t) / (vmax - vmin) * bh
        d.line((bx + bw, y, bx + bw + 14, y), fill=TXT, width=2)
        d.text((bx + bw + 22, y), f"{t:+g}" if vmin < 0 else f"{t:g}", font=f_n, fill=TXT, anchor="lm")
    d.text((bx, by - 24), unidade, font=f_t, fill=TXT, anchor="ls")
    d.text((bx, by - 70), titulo, font=f_t, fill=TXT, anchor="ls")
    d.text((W - 60, H - 60), periodo.upper(), font=f_p, fill=DATA, anchor="rs")
    im.convert("RGB").save(destino, optimize=True)


def ticks_de(vmin, vmax):
    span = vmax - vmin
    passo = next(p for p in (5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000) if span / p <= 6)
    t0 = math.ceil(vmin / passo) * passo
    return [round(t0 + i * passo, 6) for i in range(int((vmax - t0) / passo) + 1)]


def salvar_camada(v_norte, bbox, escala, vmin, vmax, destino, largura):
    img = colorir(ampliar(v_norte, largura), vmin, vmax, escala)
    img.save(destino, optimize=True)
    o, s, l, n = bbox
    w, h = img.size
    dx, dy = (l - o) / w, (n - s) / h
    open(destino[:-4] + ".pgw", "w").write(f"{dx:.10f}\n0\n0\n{-dy:.10f}\n{o + dx / 2:.10f}\n{n - dy / 2:.10f}\n")
    return w, h


# ---------------------------------------------------------------- principal
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--data", help="um dia (AAAA-MM-DD)")
    ap.add_argument("--inicio")
    ap.add_argument("--fim")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--regiao", help="região pronta (--regioes lista): BRASIL, SUL, NORDESTE, RS, SC…")
    g.add_argument("--bbox", help="oeste,sul,leste,norte em graus (ex.: -54,-31,-50,-28)")
    ap.add_argument("--saida", help="pasta de saída")
    ap.add_argument("--nome", help="prefixo dos arquivos")
    ap.add_argument("--anomalia", action="store_true", help="anomalia × climatologia mensal IMERG")
    ap.add_argument("--clima", default="2001-2020", help="anos da climatologia (padrão 2001-2020)")
    ap.add_argument("--mascara", action="store_true", help="zera fora das UFs da região (ou do Brasil, com --bbox)")
    ap.add_argument("--vmax", type=float, help="topo da escala de cor em mm (padrão automático)")
    ap.add_argument("--fundo", choices=["navy", "claro"], default="navy",
                    help="fundo do PNG de tela: navy (padrão, dentro do vídeo) ou claro (papel; thumb documento-evidencia sem mapa escuro)")
    ap.add_argument("--largura", type=int, default=2048, help="largura da camada PNG em px (padrão 2048)")
    ap.add_argument("--regioes", action="store_true", help="lista as regiões prontas e sai")
    a = ap.parse_args()
    if a.regioes:
        for k, v in REGIOES.items():
            print(f"{k:13s} {v}")
        return
    if not a.saida or not (a.data or a.inicio):
        ap.error("informe --saida e --data ou --inicio/--fim")
    ini = dt.date.fromisoformat(a.data or a.inicio)
    fim = dt.date.fromisoformat(a.data or a.fim or a.inicio)
    if fim < ini:
        ap.error("--fim antes de --inicio")
    if ini < INICIO_IMERG:
        sys.exit(f"Sem dado IMERG antes de {INICIO_IMERG:%d/%m/%Y} (pedido: {ini:%d/%m/%Y}). Para 1983, 1967, 1877 etc., use o que o "
                 "canal já usou: chuva de pluviômetro e cota de rio da ANA HidroWeb (videos/005-*/shared/baixa_ana.py; 004 usou "
                 "as estações 00539001 e 65310000), régua/gráfico de chuva em código, Landsat MSS (desde 1972; antes × depois do "
                 "004) e jornal/arquivo público de época com licença. Grade mensal global antiga (GPCC/CRU) só como Hipótese, "
                 "ainda não usada no canal.")
    if fim > dt.date.today() - dt.timedelta(days=1):
        sys.exit("O IMERG Late tem ~1 dia de atraso: use datas até anteontem/ontem.")
    if a.bbox:
        bbox = tuple(float(x) for x in a.bbox.split(","))
        regiao = "bbox"
    else:
        regiao = (a.regiao or "BRASIL").upper()
        if regiao not in REGIOES:
            sys.exit(f"Região desconhecida: {regiao}. Use --regioes ou --bbox.")
        bbox = REGIOES[regiao]
    idx = indices(bbox)
    i0, i1, j0, j1 = idx
    bbox_g = (-180 + i0 * 0.1, -90 + j0 * 0.1, -180 + (i1 + 1) * 0.1, -90 + (j1 + 1) * 0.1)  # bordas reais das células
    os.makedirs(a.saida, exist_ok=True)
    pref = os.path.join(a.saida, a.nome or f"chuva-{regiao.lower()}-{ini:%Y%m%d}_{fim:%Y%m%d}")

    soma, usados, prods, faltas = None, [], set(), []
    d = ini
    while d <= fim:
        v, prod, arq = dia(d, idx)
        if v is None:
            faltas.append(d.isoformat())
        else:
            soma = v.copy() if soma is None else soma + v
            usados.append(arq)
            prods.add(prod)
        print(f"{d}: {'ok ' + prod if v is not None else 'SEM ARQUIVO'}", flush=True)
        d += dt.timedelta(days=1)
    if soma is None:
        sys.exit("Nenhum dia encontrado no GES DISC para o período.")
    acum = soma[::-1].copy()  # linha 0 = norte

    ufs = ufs_geo()
    siglas = ([regiao] if regiao in UF_COD.values() else REGIAO_UFS.get(regiao, list(UF_COD.values())))
    msk = mascara(ufs, siglas, bbox_g, acum.shape) if ufs else None
    if a.mascara and msk is not None:
        acum = np.where(msk, acum, np.nan)

    jmax = np.unravel_index(np.nanargmax(acum), acum.shape)
    lat_max = bbox_g[3] - (jmax[0] + 0.5) * 0.1
    lon_max = bbox_g[0] + (jmax[1] + 0.5) * 0.1
    vmax = a.vmax or topo_auto(acum)
    titulo = "CHUVA ACUMULADA" if ini != fim else "CHUVA NO DIA"
    periodo = periodo_pt(ini, fim)
    wc, hc = salvar_camada(acum, bbox_g, ESCALA, 0, vmax, pref + "-camada.png", a.largura)
    tela(acum, bbox_g, ESCALA, 0, vmax, titulo, periodo, ufs, siglas if regiao != "BRASIL" else [], pref + "-tela.png",
         ticks_de(0, vmax), fundo=a.fundo)
    info = {
        "fonte": "NASA GPM IMERG V07 (GES DISC)", "credito": CREDITO, "licenca": "domínio público (dados da NASA)",
        "produtos": sorted(prods), "arquivos": usados, "dias_sem_arquivo": faltas,
        "periodo": {"inicio": ini.isoformat(), "fim": fim.isoformat(), "dias": (fim - ini).days + 1, "texto_tela": periodo},
        "regiao": regiao, "bbox_pedido": list(bbox), "bbox": [round(x, 4) for x in bbox_g],
        "grade": {"resolucao_graus": 0.1, "linhas": int(acum.shape[0]), "colunas": int(acum.shape[1])},
        "mm": {"max": round(float(np.nanmax(acum)), 1), "max_lat": round(lat_max, 2), "max_lon": round(lon_max, 2),
               "medio_bbox": round(float(np.nanmean(acum)), 1)},
        "escala": {"vmin": 0, "vmax": vmax, "unidade": "mm", "transparente_abaixo_mm": round(0.03 * vmax, 1),
                   "paradas": [{"frac": p, "mm": round(p * vmax, 1), "rgb": c, "alfa": al} for p, c, al in ESCALA]},
        "arquivos_saida": {"camada": os.path.basename(pref + "-camada.png"), "camada_px": [wc, hc],
                           "world_file": os.path.basename(pref + "-camada.pgw"), "tela": os.path.basename(pref + "-tela.png")},
        "georreferencia": "plate carrée: lon = oeste + (x+0,5)·(leste−oeste)/largura; lat = norte − (y+0,5)·(norte−sul)/altura",
        "mascara": bool(a.mascara and msk is not None),
    }
    if msk is not None:
        terra = np.where(msk, acum, np.nan)
        jt = np.unravel_index(np.nanargmax(terra), terra.shape)
        info["mm"]["max_terra"] = round(float(np.nanmax(terra)), 1)
        info["mm"]["max_terra_lat"] = round(bbox_g[3] - (jt[0] + 0.5) * 0.1, 2)
        info["mm"]["max_terra_lon"] = round(bbox_g[0] + (jt[1] + 0.5) * 0.1, 2)
        info["mm"][f"medio_{'+'.join(siglas) if len(siglas) <= 9 else 'brasil'}"] = round(float(np.nanmean(np.where(msk, acum, np.nan))), 1)
    if a.anomalia:
        a0, a1 = (int(x) for x in a.clima.split("-"))
        esperado = np.zeros_like(soma)
        anos_usados = {}
        d = ini
        cache_clima = {}
        while d <= fim:
            if d.month not in cache_clima:
                cache_clima[d.month] = climatologia_mes(a0, a1, d.month, idx)
            esperado += cache_clima[d.month][0]
            anos_usados[d.month] = cache_clima[d.month][1]
            d += dt.timedelta(days=1)
        esperado = esperado[::-1]
        anom = acum - esperado
        pct = np.where(esperado > 1, acum / np.maximum(esperado, 1e-6) * 100, np.nan)
        lim = a.vmax or topo_auto(np.abs(anom))
        salvar_camada(anom, bbox_g, ESCALA_ANOM, -lim, lim, pref + "-anomalia-camada.png", a.largura)
        tela(anom, bbox_g, ESCALA_ANOM, -lim, lim, "DIFERENÇA DA MÉDIA", periodo, ufs, siglas if regiao != "BRASIL" else [],
             pref + "-anomalia-tela.png", ticks_de(-lim, lim), fundo=a.fundo)
        info["anomalia"] = {
            "climatologia": f"IMERG mensal {PROD_MES}, {a0}–{a1} (anos com dado por mês: {anos_usados})",
            "metodo": "esperado = soma, dia a dia, da média diária do mês na climatologia; anomalia = acumulado − esperado",
            "mm_esperado_medio_bbox": round(float(np.nanmean(esperado)), 1),
            "mm_anomalia_max": round(float(np.nanmax(anom)), 1), "mm_anomalia_media_bbox": round(float(np.nanmean(anom)), 1),
            "pct_da_media_max": round(float(np.nanmax(pct)), 0), "escala_mm": [-lim, lim],
            "arquivos": [os.path.basename(pref + "-anomalia-camada.png"), os.path.basename(pref + "-anomalia-tela.png")],
        }
        if msk is not None:
            info["anomalia"]["pct_da_media_area"] = round(float(np.nansum(np.where(msk, acum, 0)) / np.nansum(np.where(msk, esperado, 0)) * 100), 0)
    json.dump(info, open(pref + ".json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: info[k] for k in ("produtos", "bbox", "mm")}, ensure_ascii=False))
    print(f"→ {pref}-camada.png · {pref}-tela.png · {pref}.json" + (" · anomalia" if a.anomalia else ""))


if __name__ == "__main__":
    main()
