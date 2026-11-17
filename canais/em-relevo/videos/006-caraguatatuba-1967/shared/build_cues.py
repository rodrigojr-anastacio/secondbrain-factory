# Storyboard em código do longo 05 (Em Relevo, enchente de 2024: por que a chuva da serra alagou Porto Alegre): gera shared/cues.json e shared/estilo_v2.json
# a partir de blocos.json, tempos.json, whisper.json, geo.json e dados/. Base: longo-03/shared/build_cues.py (cada evento amarrado à palavra falada).
# Uso: python3 build_cues.py (precisa de audio/narracao.wav + tempos.json + whisper.json: rode monta_audio_v2.py antes).
import json, math, re, unicodedata
from pathlib import Path

A = Path(__file__).parent; R = A.parent
blocos = json.load(open(A / "blocos.json")); tempos = json.load(open(A / "tempos.json")); wh = json.load(open(A / "whisper.json"))
geo = json.load(open(A / "geo.json")); SST = json.load(open(A / "sst_pacifico.json"))
pj = geo["proj"]; PAC = geo["pac"]
def P(lon, lat): return [round((lon - pj["lon0"]) * pj["cos"] * pj["k"], 3), round(-(lat - pj["lat0"]) * pj["k"], 3)]
def P2(lon, lat): l = lon % 360; return [round(PAC["x0"] + (l - PAC["lonc"]) * PAC["k"], 3), round(PAC["z0"] - lat * PAC["k"], 3)]
T = {b["id"]: b for b in tempos["blocos"]}
S = lambda b: T[b]["s"]; E = lambda b: T[b]["e"]
def F(b, k): return T[b]["frases"][min(k, len(T[b]["frases"]) - 1)]["s"]
def FE(b, k): return T[b]["frases"][min(k, len(T[b]["frases"]) - 1)]["e"]
avisos = []
def norm(w):
    w = unicodedata.normalize("NFD", w.lower()); w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", w)
def tw(palavra, b, apos=None, n=0, alt=None):
    t0 = (apos if apos is not None else S(b) - 0.35); t1 = E(b) + 0.2; alvos = [norm(x) for x in palavra.split("|")]; k = 0
    for w in wh:
        if t0 <= w["s"] <= t1 and any(norm(w["w"]).startswith(a) for a in alvos):
            if k == n: return w["s"]
            k += 1
    avisos.append(f"palavra '{palavra}' não achada em {b}")
    return round(alt if alt is not None else (max(t0, S(b)) + E(b)) / 2, 3)

# ---------------- legenda ----------------
palavras = []
for b in blocos:
    tb = T[b["id"]]; ws = [w for w in wh if tb["s"] - 0.35 <= w["s"] <= tb["e"] + 0.1]
    linhas = [l.split() for l in b["tela"].split("|")]; toks = [w for l in linhas for w in l]; n, m = len(toks), len(ws); tt, j = [None] * n, 0
    for i, tk in enumerate(toks):
        for k in range(j, min(m, j + 5)):
            a, c = norm(tk), norm(ws[k]["w"])
            if a and c and (a == c or a.startswith(c) or c.startswith(a)): tt[i] = ws[k]["s"]; j = k + 1; break
    for i in range(n):
        if tt[i] is None:
            ant = next((tt[k] for k in range(i - 1, -1, -1) if tt[k] is not None), tb["s"]); prox = next((tt[k] for k in range(i + 1, n) if tt[k] is not None), tb["e"])
            tt[i] = ant + (prox - ant) * 0.5
    i = 0
    for li, l in enumerate(linhas):
        if palavras: palavras.append("|")
        for w in l: palavras.append([w, round(max(tt[i], tb["s"] - 0.05), 3)]); i += 1
capitulos = []
for b in blocos:
    if not capitulos or capitulos[-1]["nome"] != b["cap"]: capitulos.append({"t": max(0, S(b["id"]) - 0.4), "nome": b["cap"]})

# ---------------- helpers ----------------
camera = []
def cam(t, alvo, dist, el, az, y=0.3, corte=False):
    el, az = math.radians(el), math.radians(az); x, z = alvo
    k = {"t": round(t, 3), "alvo": [x, y, z], "pos": [round(x + dist * math.sin(az) * math.cos(el), 3), round(y + dist * math.sin(el), 3), round(z + dist * math.cos(az) * math.cos(el), 3)]}
    if corte: k["corte"] = True
    camera.append(k)
pinos, destaques, fios, setas, nuvens, regioes, pontos, tintas, relevos, montanhas, globos, cilindros, rotulos = [], [], [], [], [], [], [], [], [], [], [], [], []
def pino(id, nome, sub, t, t2=None, pequeno=False, cor=None, ate=None, xz=None, y0=None):
    p = {"id": id, "nome": nome, "sub": sub, "x": xz[0], "z": xz[1], "t": round(t, 3), "pequeno": pequeno}
    if t2: p["t2"] = round(t2, 3)
    if cor: p["cor"] = cor
    if y0 is not None: p["y0"] = y0
    p["ate"] = round(ate if ate else (t2 if t2 else t + 6), 3)
    if not t2: p["t2"] = round(p["ate"] + 0.4, 3)
    pinos.append(p)
def rot(nome, xz, t0, t1, tipo="seta", y=None):
    r = {"nome": nome, "x": xz[0], "z": xz[1], "t0": round(t0, 3), "t1": round(t1, 3), "tipo": tipo}
    if y is not None: r["y"] = y
    rotulos.append(r)
def seta(cor, pts, t0, t1, t2, y=0.95, r=0.16, fluxo=False, vel=0.18, semCabeca=False):
    s = {"cor": cor, "pontos": [list(q) for q in pts], "t0": round(t0, 3), "t1": round(t1, 3), "t2": round(t2, 3), "y": y, "r": r, "fluxo": fluxo, "vel": vel}
    if semCabeca: s["semCabeca"] = True
    setas.append(s)
def janela_op(t0, t1, v=1.0, din=0.7, dout=0.7): return [[0, 0], [round(t0, 3), 0], [round(t0 + din, 3), v], [round(t1, 3), v], [round(t1 + dout, 3), 0]]
midia, numero, manchetes, cartoes, graficos, graficos3, papeis, transicoes = [], [], [], [], [], [], [], []
def foto(arq, t0, t1, lado="dir", fmt="grande", pino=None, estatica=False):
    f = FOTOS[arq]
    midia.append({"id": "fotos/" + arq, "tipo": "img", "src": "fotos/" + arq, "fmt": fmt, "t0": round(t0, 3), "t1": round(t1, 3), "lado": lado, "legenda": f["legenda_tela"], "credito": "", "pino": pino, "estatica": estatica})
def num(t, valor=None, faixa="", de=None, para=None, dur=1.0, unidade=None, dec=0):
    if valor is not None: numero.append({"t": round(t, 3), "valor": valor, "faixa": faixa, "unidade": unidade})
    else: numero.append({"t": round(t, 3), "de": de, "para": para, "ate": round(t + dur, 3), "unidade": unidade, "faixa": faixa, "dec": dec})
def num_off(t): numero.append({"t": round(t, 3), "oculto": True})
def cartao(t0, t1, rotulo, texto, carimbo=None, t_carimbo=None, top=300, left=None, w=None):
    c = {"t0": round(t0, 3), "t1": round(t1, 3), "rotulo": rotulo, "texto": texto, "top": top}
    if left: c["left"] = left
    if w: c["w"] = w
    if carimbo: c["carimbo"] = {"texto": carimbo, "t": round(t_carimbo, 3)}
    cartoes.append(c)
def trans(t, tipo, dur=1.0, desc=""): transicoes.append({"t": round(t, 3), "tipo": tipo, "dur": dur, "desc": desc})
def papel(b0, b1, itens, pre=0.0, topo=False): papeis.append({"t0": round(S(b0) - pre, 3), "t1": round(E(b1) + 0.25, 3), "itens": itens, "topo": topo})
def meio(b1, b2): return (E(b1) + S(b2)) / 2
luz = [[0, 1]]; noite = [[0, 0]]; quente = [[0, 0]]; amazonia = [[0, 0]]; andes_t = [[0, 0]]; arquivo = [[0, 0]]; tremor = [[0, 0]]; desfoque = [[0, 0]]
def tab(lista, t, v, dur=0.6): lista.append([round(t, 3), lista[-1][1]]); lista.append([round(t + dur, 3), v])
ESTILO = []   # (t, 'A'|'B')
def est(b, e): ESTILO.append((max(0, S(b) - 0.4) if b != "b01" else 0, e))

# ======================= Em Relevo 005 (enchente de maio/2024): dados e lugares =======================
RIOS = json.load(open(A / "rios.json"))
CX = P(-51.18, -29.17); PA = P(-51.23, -30.03); LAJ = P(-51.97, -29.47); SM = P(-53.81, -29.69); AM = P(-51.95, -29.40)
FOZ = P(-51.27, -30.05); GUA = P(-51.30, -30.15)
RG = P(-52.10, -32.03); PEL = P(-52.34, -31.77); SLS = P(-51.97, -31.37); BARRA = P(-52.07, -32.16)
LAGOA = [P(-51.12, -30.35), P(-51.40, -30.80), P(-51.85, -31.30), P(-52.18, -31.78), P(-52.10, -32.10)]
RSC = P(-53.2, -30.0); BAC = P(-52.6, -29.6); BAC2 = P(-52.5, -29.5)
AZUL = "#39B0F5"; CORAL = "#E8505B"; CIANO = "#3FD8FF"
graficos4, graficos5, checklists, rios_l, gotas, cobre, chuvas = [], [], [], [], [], [], []
def g5(**k): graficos5.append({**k, "t0": round(k["t0"], 3), "t1": round(k["t1"], 3)})
def chuva(xz, t0, t1, r=0.45, h=1.6, n=70, y=0.12, vel=1.3): chuvas.append({"x": xz[0], "z": xz[1], "r": r, "h": h, "n": n, "t0": round(t0, 3), "t1": round(t1, 3), "y": y, "vel": vel})
def cil(xz, t_ini, t_fim, nivel, marca=None, t_marca=None, r=0.09, h=1.2, cor="#3D7FB8", cor_marca="#C9A46A", y=0.2, dx=0.5, dz=-0.2):
    c = {"x": xz[0] + dx, "z": xz[1] + dz, "r": r, "h": h, "cor": cor, "y": y, "op": janela_op(t_ini, t_fim, 1, 0.5, 0.5), "nivel": [[round(a, 3), b] for a, b in nivel]}
    if marca is not None: c.update({"marca": marca, "t_marca": round(t_marca if t_marca is not None else t_ini, 3), "cor_marca": cor_marca})
    cilindros.append(c)
def nuvem(xz, t, t2, s=1.6, y=1.5, dest=None, tm=None):
    n = {"x": xz[0], "z": xz[1], "t": round(t, 3), "t2": round(t2, 3), "s": s, "y": y}
    if dest: n.update({"x2": dest[0], "z2": dest[1], "tm0": round(tm[0], 3), "tm1": round(tm[1], 3)})
    nuvens.append(n)
def arvore(sel, t0, t1, op_t0, op_t1, larg=1.0, cor=CIANO, pico=None, fade=0.8):
    L = {"sel": sel, "t0": round(t0, 3), "t1": round(t1, 3), "cor": cor, "larg": larg, "op": janela_op(op_t0, op_t1, 1, 0.3, fade)}
    if pico: L["pico"] = pico
    rios_l.append(L)
def pulso(t, dur=2.0, v=1.0): return [[0, 0], [round(t - 0.1, 3), 0], [round(t + 0.25, 3), v], [round(t + dur, 3), 0.15 * v]]
def pulsos(lista):   # lista de (t, dur)
    out = [[0, 0]]
    for t_, d_ in lista: out += [[round(t_ - 0.1, 3), out[-1][1]], [round(t_ + 0.25, 3), 1.0], [round(t_ + d_, 3), 0.1]]
    return out
def gota(path, t_vis0, t_vis1, t_mov0, t_mov1, esc=0.07, alto=0.12, cauda=1.0, prog_extra=None):
    prog = [[0, 0], [round(t_mov0, 3), 0], [round(t_mov1, 3), 1], [99999, 1]] if prog_extra is None else prog_extra
    gotas.append({"pontos": path, "prog": prog, "op": janela_op(t_vis0, t_vis1, 1, 0.4, 0.5), "esc": esc, "alto": alto, "cauda": cauda})
def foto_sat(arq, t0, t1, lado="dir", fmt="grande"): foto(arq, t0, t1, lado=lado, fmt=fmt, estatica=True)
def mm(t): return t
FOTOS = {
    "nasa-landsat8-porto-alegre-alagado-2024-05-08.jpg": "PORTO ALEGRE · LANDSAT 8 · 8 MAI 2024",
    "centro-historico-rodoviaria-cais-mauah-alagados-aereo-2024-05-05.jpg": "CENTRO HISTÓRICO · PORTO ALEGRE · 5 MAI 2024",
    "rodoviaria-viaduto-cais-maua-alagados-aereo-2024-05-05.jpg": "RODOVIÁRIA · PORTO ALEGRE · 5 MAI 2024",
    "aeroporto-salgado-filho-pista-alagada-aereo-2024-05-05.jpg": "AEROPORTO SALGADO FILHO · 5 MAI 2024",
    "arroio-do-meio-navegantes-destruicao-aereo-2024-06-06.jpg": "ARROIO DO MEIO · VALE DO TAQUARI · JUN 2024",
    "hls-sentinel2-porto-alegre-guaiba-antes-2024-04-01-recorte.jpg": "GUAÍBA · SENTINEL-2 · 1 ABR 2024",
    "nasa-modis-sul-do-rs-durante-2024-05-06.jpg": "LAGOA DOS PATOS · MODIS · 6 MAI 2024",
    "rio-grande-fragata-f44-canal-da-barra-molhes-2023-08-15.jpg": "CANAL DA BARRA · RIO GRANDE · 2023",
    "pelotas-bairros-alagados-aereo-2024-05-18.jpg": "PELOTAS · 18 MAI 2024",
    "mercado-publico-fachada-alagado-enchente-1941-05-recorte.jpg": "MERCADO PÚBLICO · MAIO DE 1941",
    "muro-da-maua-grafite-dia-normal-2016-04-23.jpg": "MURO DA MAUÁ · DIA NORMAL · 2016",
    "comporta-cais-maua-fechamento-2024-05-02.jpg": "COMPORTA DO CAIS MAUÁ · 2 MAI 2024",
    "mercado-publico-ilhado-aereo-2024-05-05.jpg": "MERCADO PÚBLICO · 5 MAI 2024",
    "centro-historico-edificios-historicos-alagados-aereo-2024-05-05.jpg": "CENTRO HISTÓRICO · 5 MAI 2024",
    "cais-maua-galpao-marcas-da-enchente-2026-03-12.jpg": "CAIS MAUÁ · MARCAS DA ENCHENTE · 2026",
}
_foto0 = foto
def foto(arq, t0, t1, lado="dir", fmt="grande", pino=None, estatica=False):
    midia.append({"id": "fotos/" + arq, "tipo": "img", "src": "fotos/" + arq, "fmt": fmt, "t0": round(t0, 3), "t1": round(t1, 3), "lado": lado, "legenda": FOTOS[arq], "credito": "", "pino": pino, "estatica": estatica})
# municípios (pontinhos que piscam ao longo da rede): vértices dos afluentes, determinístico
_pts = [p for o in RIOS if not o["c"] for p in o["p"][1:-1:3]]
MUNS = [P(*_pts[(i * 37) % len(_pts)]) for i in range(250)]
RIOCL = {"jacui": P(-53.28, -29.2), "taquari": P(-51.35, -29.0), "cai": P(-51.12, -29.38), "sinos": P(-50.9, -29.72), "gravatai": P(-50.78, -30.0)}

# ======================= HOOK (b01–b06) =======================
est("b01", "A"); tab(luz, 0, 0.9, 0.1); tab(quente, 0, 0.0, 0.1)
cam(0.0, [CX[0] + 1.6, CX[1] - 1.6], 11, 22, -20, y=0.1); cam(F("b01", 1), [CX[0] + 0.3, CX[1]], 5.6, 33, -8, y=0.1); cam(E("b01") - 0.2, [CX[0] + 0.15, CX[1] - 0.1], 4.4, 38, 8, y=0.1)
nuvem([CX[0] - 1.5, CX[1] - 0.6], 0.0, E("b01") + 0.5, 0.8, y=1.6); nuvem([CX[0] + 1.7, CX[1] + 0.2], 0.2, E("b01") + 0.5, 0.7, y=1.5); nuvem([CX[0] - 1.1, CX[1] + 1.3], 0.4, E("b01") + 0.5, 0.8, y=1.7)
chuva(CX, 0.6, E("b01") + 0.4, r=0.5, h=1.7, n=90)
pino("cx", "CAXIAS DO SUL (RS)", "2 DE MAIO DE 2024", 0.5, t2=E("b01") + 0.6, xz=CX, y0=0.1, ate=E("b01") + 0.2)
t_duz = tw("266|duzentos", "b01", alt=F("b01", 1) + 0.6)
cil(CX, F("b01", 1) - 0.4, E("b02") + 0.3, [[0, 0.0], [t_duz - 0.3, 0.0], [t_duz + 1.5, 266 / 300]], marca=94.4 / 300, t_marca=F("b01", 1) - 0.2, h=1.25, r=0.1)
rot("RECORDE ANTERIOR · 94 MM (2017)", [CX[0] + 0.5, CX[1] - 0.2], t_duz + 1.4, E("b01") + 1.5, "seta", y=0.2 + 1.25 * 94.4 / 300 + 0.15)
num(t_duz - 0.3, de=0, para=266, dur=1.5, faixa="CAXIAS DO SUL · 2 MAI 2024 · INMET", unidade="mm"); num_off(F("b01", 2) - 0.1)
g5(tipo="selo", t0=tw("três", "b01", alt=F("b01", 2) + 0.4) - 0.1, t1=E("b01") + 0.6, texto="QUASE 3× O RECORDE", top=190, left=1150, rot=-5)
gota([[CX[0] + 0.5, CX[1] - 0.2], [CX[0] + 0.1, CX[1] + 0.25], [P(-51.25, -29.40)[0], P(-51.25, -29.40)[1]], [P(-51.36, -29.65)[0], P(-51.36, -29.65)[1]], [P(-51.33, -29.88)[0], P(-51.33, -29.88)[1]], [FOZ[0] + 0.05, FOZ[1] - 0.08]],
     t_duz + 1.2, E("b02") + 0.4, S("b02") + 0.3, S("b02") + 7.0, esc=0.07, alto=0.14)
# b02 Porto Alegre
est("b02", "A"); trans(S("b02") - 0.15, "whip", 0.6, "dolly longo para o sul seguindo a gota")
cam(S("b02") - 0.1, [CX[0] + 0.2, CX[1] + 0.2], 5.2, 30, -10, corte=False, y=0.1); cam(S("b02") + 3.3, [P(-51.3, -29.6)[0], P(-51.3, -29.6)[1]], 7.5, 36, -6, y=0.1); cam(F("b02", 1) - 1.0, [PA[0] - 0.15, PA[1] - 0.2], 4.6, 36, 4, y=0.1); cam(E("b02"), [PA[0] - 0.15, PA[1] - 0.15], 3.9, 40, 10, y=0.1)
pino("pa", "PORTO ALEGRE (RS)", "5 DE MAIO DE 2024", S("b02") + 6.6, t2=E("b03") + 1.0, xz=PA, y0=0.1, ate=E("b03"))
rot("100 KM", [(CX[0] + PA[0]) / 2 + 0.3, (CX[1] + PA[1]) / 2], S("b02") + 3.0, S("b02") + 7.5, "seta", y=0.3)
t_cinco = tw("cinco|5", "b02", alt=F("b02", 0) + 1.2)
cil(PA, S("b02") + 6.4, E("b03") + 0.6, [[0, 0.0], [t_cinco + 0.2, 0.0], [t_cinco + 2.3, 5.35 / 6]], marca=4.76 / 6, t_marca=t_cinco + 2.4, h=1.1, r=0.09, dx=-0.75, dz=-0.1, cor="#3D7FB8", cor_marca="#C9A46A")
num(t_cinco, de=0, para=5.35, dur=1.8, faixa="GUAÍBA · PORTO ALEGRE · 5 MAI 2024", unidade="m", dec=2); num_off(F("b02", 1) + 1.7)
rot("1941 · 4,76 M", [PA[0] - 0.2, PA[1] - 0.2], t_cinco + 2.6, F("b02", 2) - 0.5, "seta", y=0.2 + 1.1 * 4.76 / 6 + 0.12)
foto_sat("nasa-landsat8-porto-alegre-alagado-2024-05-08.jpg", tw("Porto", "b02", alt=F("b02", 0) + 1.0) + 0.2, tw("Porto", "b02", alt=F("b02", 0) + 1.0) + 3.4, lado="dir")
g5(tipo="frase", t0=F("b02", 2), t1=E("b02") + 0.5, linhas=["A CHUVA MAIS PESADA CAIU NA SERRA.", "QUEM AFUNDOU FOI PORTO ALEGRE."], destaque=1, top=640, left=90, tam=64, dur=3.0)
# b03 impacto
est("b03", "A"); trans(S("b03") - 0.1, "corte", 0.5, "corte seco para foto (impacto grave)")
cam(S("b03"), [PA[0] - 0.1, PA[1] - 0.15], 3.8, 42, 10, corte=True, y=0.1); cam(E("b03"), [PA[0] - 0.05, PA[1] - 0.1], 3.2, 44, -8, y=0.1)
t_cap = tw("capital", "b03", alt=S("b03") + 3.0); t_rod = tw("rodoviária|rodoviaria", "b03", alt=F("b03", 1)); t_aer = tw("aeroporto", "b03", alt=F("b03", 1) + 1.5)
foto("centro-historico-rodoviaria-cais-mauah-alagados-aereo-2024-05-05.jpg", t_cap - 3.0, t_cap + 1.2, lado="esq")
foto("rodoviaria-viaduto-cais-maua-alagados-aereo-2024-05-05.jpg", t_rod - 0.1, t_rod + 1.9, lado="dir")
foto("aeroporto-salgado-filho-pista-alagada-aereo-2024-05-05.jpg", t_aer - 0.1, t_aer + 2.2, lado="esq")
t_160 = tw("160|cento", "b03", alt=S("b03") + 0.6)
num(t_160, valor="~160 MIL", faixa="PESSOAS ATINGIDAS · PORTO ALEGRE · SEGUNDO A PREFEITURA"); num_off(F("b03", 1) - 0.1)
cartao(tw("Defesa", "b03", alt=F("b03", 2)) - 0.1, E("b03") + 0.2, "RIO GRANDE DO SUL · BALANÇO DA DEFESA CIVIL (24/04/2025)", "184 MORTES", top=620)
# b04 o mapa
est("b04", "B"); trans(S("b04") - 0.2, "corte", 0.5, "corte seco de volta ao mapa")
cam(S("b04"), [-0.4, 2.9], 9.5, 52, 0, corte=True, y=0.1); cam(F("b04", 2) - 0.2, [0.1, 2.8], 8.0, 54, 4, y=0.1); cam(E("b04"), [-0.2, 2.9], 12.5, 58, 4, y=0.1)
t_cp = tw("capital", "b04", alt=S("b04") + 0.5)
cil(PA, S("b04") + 0.1, E("b04") + 0.4, [[0, 0], [t_cp, 0.0], [t_cp + 1.5, 564.8 / 1000]], r=0.12, h=1.7, dx=-0.15, dz=0.2, y=0.1, cor="#3D7FB8")
cil(CX, S("b04") + 0.1, E("b04") + 0.4, [[0, 0], [t_cp + 0.3, 0.0], [t_cp + 2.4, 919.1 / 1000]], r=0.12, h=1.7, dx=0.15, dz=-0.15, y=0.1, cor="#3D7FB8")
rot("PORTO ALEGRE · 565 MM", [PA[0] - 0.25, PA[1] + 0.55], t_cp + 1.3, F("b04", 2), "seta", y=0.1 + 1.7 * 0.5648 + 0.2)
rot("CAXIAS DO SUL · 919 MM", [CX[0] + 0.45, CX[1] - 0.15], t_cp + 2.3, F("b04", 2), "seta", y=0.1 + 1.7 * 0.919 + 0.2)
pergunta = {"t0": round(F("b04", 2) + 0.1, 3), "t1": round(E("b04") + 0.3, 3), "texto": "COMO A CHUVA DA SERRA FOI PARAR DENTRO DE PORTO ALEGRE?"}
# b05 árvore de rios
est("b05", "A"); trans(S("b05") - 0.3, "nuvem", 1.2, "câmera sobe até ver o centro-nordeste do RS")
cam(S("b05") - 0.3, [PA[0] - 0.4, PA[1] - 0.6], 9.0, 46, 6, corte=True, y=0.1); cam(F("b05", 1), BAC, 15.5, 56, 6, y=0.1); cam(E("b05"), [BAC[0] + 0.2, BAC[1] + 0.2], 14.0, 55, -4, y=0.1)
T_RIO = {c: tw({"jacui": "Jacuí", "taquari": "Taquari", "cai": "Caí", "sinos": "Sinos", "gravatai": "grava"}[c], "b05", alt=F("b05", 1) + 0.5 * k) for k, c in enumerate(["jacui", "taquari", "cai", "sinos", "gravatai"])}
for c in T_RIO: arvore(c, T_RIO[c] - 0.3, T_RIO[c] + 2.6, T_RIO[c] - 0.3, S("b14") - 0.3, larg=1.0)
for c, nome in (("jacui", "JACUÍ"), ("taquari", "TAQUARI"), ("cai", "CAÍ"), ("sinos", "SINOS"), ("gravatai", "GRAVATAÍ")): rot(nome, RIOCL[c], T_RIO[c] + 0.3, S("b07") - 0.5, "seta", y=0.3)
gotas.append({"pontos": [[FOZ[0] - 0.02, FOZ[1]], [FOZ[0], FOZ[1] + 0.01]], "prog": [[0, 0], [99999, 0]], "op": janela_op(T_RIO["gravatai"] + 0.8, E("b19") + 3.5, 1, 0.8, 0.6), "esc": 0.11, "alto": 0.15, "cauda": 0.0})
pino("pa2", "PORTO ALEGRE", "GUAÍBA", F("b05", 2), t2=S("b07") - 0.3, xz=PA, y0=0.1, ate=S("b07") - 0.5, pequeno=True)
rot("GUAÍBA", [FOZ[0] - 0.9, FOZ[1] + 0.5], F("b05", 2), S("b07") - 0.4, "corredor", y=0.3)
# b06 lago + um terço
est("b06", "B"); cam(S("b06"), [BAC[0] + 0.1, BAC[1] + 0.2], 14.0, 55, -4, corte=True, y=0.1); cam(F("b06", 2) - 0.3, [BAC[0] - 0.3, BAC[1] + 0.1], 13.0, 52, 10, y=0.1); cam(E("b06"), [CX[0] - 0.2, CX[1] - 0.4], 7.5, 40, 4, y=0.1)
arvore("afluentes", S("b06") + 0.2, S("b06") + 5.5, S("b06") + 0.2, S("b14") - 0.3, larg=1.0, cor="#7FDDF5")
g5(tipo="selo", t0=tw("lago", "b06", alt=S("b06") + 0.9) - 0.1, t1=F("b06", 1), texto="LAGO GUAÍBA (OFICIAL)", top=190, left=110, rot=-3, cor="#1F2A44", tam=52)
g5(tipo="selo", t0=tw("rio", "b06", n=0, alt=S("b06") + 4.0), t1=F("b06", 1), texto="RIO?", top=300, left=110, rot=3, cor="#7a7066", tam=36)
num(tw("terço|tercio", "b06", alt=F("b06", 1) + 1.0) - 0.3, valor="QUASE 1/3", faixa="DO RIO GRANDE DO SUL · ÁREA QUE DRENA PARA O GUAÍBA"); num_off(tw("saída|saida", "b06", alt=F("b06", 1) + 3.5) - 0.3)
t_said = tw("saída|saida", "b06", alt=F("b06", 1) + 3.5)
seta(CIANO, [[FOZ[0], FOZ[1]], P(-51.15, -30.3), P(-51.2, -30.55)], t_said, t_said + 1.2, F("b06", 2) - 0.2, y=0.5, r=0.045, fluxo=True, vel=0.2)
rot("1 SAÍDA", P(-51.0, -30.4), t_said + 0.6, F("b06", 2) - 0.2, "seta", y=0.55)
gota([[CX[0] + 0.4, CX[1] - 0.15], [CX[0] + 0.45, CX[1] - 0.12]], tw("caminho", "b06", alt=F("b06", 2) + 3.0) - 0.4, E("b07") + 3.0, 0, 0, esc=0.09, alto=0.18, cauda=0.0, prog_extra=[[0, 0], [99999, 0]])

# ======================= 1 · A CHUVA DA SERRA (b07–b13) =======================
est("b07", "A"); trans(S("b07") - 0.3, "nuvem", 1.2, "abertura do cap. 1: céu 3D sobre o RS")
cam(S("b07") - 0.3, RSC, 17, 28, -12, corte=True, y=0.3); cam(E("b07"), [RSC[0] + 1.0, RSC[1] - 0.3], 15, 30, 12, y=0.3)
tab(luz, S("b07"), 0.55, 0.8); tab(luz, E("b07") + 0.4, 0.9, 0.8)
for k, (dx, dz) in enumerate([(-0.5, 0.2), (0.3, -0.3), (1.0, 0.3), (1.6, -0.2), (2.2, 0.2), (2.8, -0.3)]):
    nuvem([RSC[0] - 6.0 + dx, RSC[1] + 3.0 + dz], S("b07") + 0.6 + 0.1 * k, E("b07") + 0.8, 1.35, y=1.5, dest=[RSC[0] + 0.3 + dx, RSC[1] - 0.2 + dz * 1.5], tm=(S("b07") + 1.0, F("b07", 1) + 0.5))
regioes.append({"anel": [P(-54.5, -26.2), P(-52.5, -25.2), P(-50.2, -25.6), P(-49.6, -26.8), P(-51.5, -27.3), P(-53.6, -27.2)], "cor": "#FF9A62", "op": janela_op(F("b07", 2) - 0.3, E("b07") + 1.0, 1, 0.9, 0.7), "max": 0.38, "y": 0.9, "pulsa": True})
seta("#7FB4DE", [P(-52.0, -23.5), P(-52.6, -25.8), P(-52.4, -28.2)], F("b07", 2) + 0.2, F("b07", 2) + 2.2, E("b07") + 1.2, y=1.1, r=0.05, fluxo=True, vel=0.16)
rot("FRENTE FRIA (PARADA)", P(-53.0, -29.8), F("b07", 1) + 0.8, E("b07") + 1.0, "fria", y=1.9)
rot("BLOQUEIO DE AR QUENTE", P(-52.0, -26.3), F("b07", 2) + 0.2, E("b07") + 1.0, "quente", y=1.2)
rot("UMIDADE DO NORTE", P(-51.2, -24.7), F("b07", 2) + 1.6, E("b07") + 1.0, "seta", y=1.2)
g5(tipo="selo", t0=F("b07", 1) + 0.3, t1=E("b07") + 0.8, texto="ESQUEMA · SEM NÚMERO", top=190, left=110, rot=-3, cor="#1F2A44", tam=40)
# b08 420 mm
est("b08", "B"); trans(S("b08") - 0.2, "corte", 0.4, "mapa editorial")
tab(luz, S("b08") - 0.2, 1.0, 0.2)
cam(S("b08"), [RSC[0] + 0.2, RSC[1]], 17, 56, 0, corte=True, y=0.1); cam(E("b08"), [RSC[0] + 0.2, RSC[1]], 15.5, 58, 6, y=0.1)
tintas.append({"ufs": ["43"], "cor": "#2D7FD0", "op": [[0, 0], [S("b08") + 0.5, 0], [E("b08") - 1.0, 1.0], [E("b08") + 0.6, 1.0], [E("b08") + 1.6, 0]], "max": 0.75})
t_420 = tw("420|quatrocentos", "b08", alt=S("b08") + 1.0)
num(t_420 - 0.4, de=0, para=420, dur=2.2, faixa="MÉDIA NO ESTADO · 24/04 A 04/05 · WORLD WEATHER ATTRIBUTION", unidade="mm"); num_off(F("b08", 2) - 0.2)
g5(tipo="chuva3m", t0=tw("3|três|tres", "b08", alt=F("b08", 2)) - 0.8, t1=E("b08") + 0.3)
# b09 serra e planalto
est("b09", "B"); cam(S("b09"), [CX[0] - 0.2, CX[1] + 0.1], 7.0, 38, -14, corte=True, y=0.1); cam(F("b09", 1) + 0.5, [(CX[0] + SM[0]) / 2 + 0.6, CX[1] + 0.3], 10.5, 42, 6, y=0.1); cam(E("b09"), [SM[0] + 0.8, SM[1] - 0.1], 7.5, 38, 14, y=0.1)
chuva(CX, S("b09") + 0.2, F("b09", 2), r=0.5, h=1.8, n=90); chuva(SM, F("b09", 2) - 0.3, E("b09") + 0.6, r=0.5, h=1.8, n=90)
t_707 = tw("707|setecentos", "b09", alt=F("b09", 1) + 1.0)
cil(CX, S("b09") + 0.2, F("b09", 2), [[0, 0], [t_707 - 0.4, 0.0], [t_707 + 1.4, 707.2 / 1000]], r=0.1, h=1.5, dx=0.5, dz=-0.2, y=0.1)
pino("cx9", "CAXIAS DO SUL", "707 MM · 1 A 13 DE MAIO", S("b09") + 0.4, t2=F("b09", 2), xz=CX, y0=0.1, ate=F("b09", 2) - 0.2)
pino("sm9", "SANTA MARIA", "MAIOR CHUVA DIÁRIA EM 112 ANOS · 1 MAI", F("b09", 2) - 0.2, t2=E("b09") + 0.8, xz=SM, y0=0.1, ate=E("b09") + 0.5)
rot("ONDE NASCEM OS RIOS", P(-51.3, -29.75), S("b09") + 0.5, F("b09", 2) - 0.4, "corredor", y=0.3)
num(t_707 - 0.3, de=0, para=707, dur=1.6, faixa="CAXIAS DO SUL · 1 A 13 MAI 2024 · INMET", unidade="mm"); num_off(F("b09", 2) - 0.2)
# b10 3 cheias
est("b10", "B"); cam(S("b10"), [RSC[0] + 0.5, RSC[1]], 16, 56, 0, corte=True, y=0.1); cam(E("b10"), [RSC[0] + 0.5, RSC[1]], 14.5, 58, 6, y=0.1)
t_set = tw("setembro", "b10", alt=F("b10", 1) - 0.5); t_nov = tw("novembro", "b10", alt=F("b10", 2) - 0.5); t_ter = tw("terceira", "b10", alt=F("b10", 3) - 0.5)
g5(tipo="cheias3", t0=S("b10") + 0.2, t1=E("b10") + 0.4, t=[t_set + 0.3, t_nov + 0.2, t_ter + 0.2])
num(t_ter + 0.3, valor="3", faixa="GRANDES CHEIAS EM 8 MESES"); num_off(E("b10") + 0.2)
# b11 perfil
est("b11", "A"); trans(S("b11") - 0.2, "match", 0.7, "gota")
cam(S("b11") - 0.1, [CX[0] + 0.2, CX[1] + 0.1], 5.4, 20, 100, corte=True, y=0.1); cam(F("b11", 1), [(CX[0] + PA[0]) / 2, (CX[1] + PA[1]) / 2], 8.5, 30, 100, y=0.1); cam(E("b11"), [PA[0] - 0.1, PA[1] - 0.3], 6.0, 34, 100, y=0.1)
t_des = tw("desce", "b11", alt=F("b11", 2) + 0.2)
g5(tipo="perfil", t0=S("b11") + 0.4, t1=E("b11") + 0.4, t_vales=tw("vales", "b11", alt=F("b11", 2) + 2.0), prog=[[0, 0], [t_des, 0], [E("b11") - 0.2, 1.0]], top=430)
# b12 Taquari / Lajeado
est("b12", "A"); trans(S("b12") - 0.2, "whip", 0.6, "voo pelo vale do Taquari")
cam(S("b12") - 0.1, [LAJ[0] + 0.8, LAJ[1] - 1.0], 6.0, 32, -40, corte=True, y=0.1); cam(F("b12", 1), [LAJ[0] + 0.1, LAJ[1] - 0.55], 4.3, 34, -8, y=0.1); cam(E("b12"), [LAJ[0] + 0.2, LAJ[1] - 0.55], 3.8, 38, 10, y=0.1)
pino("laj", "LAJEADO (RS)", "RIO TAQUARI · 2 DE MAIO", S("b12") + 0.4, t2=E("b13") - 0.5, xz=LAJ, y0=0.1, ate=E("b12") + 0.2)
t_3370 = tw("33|trinta", "b12", alt=F("b12", 1) + 1.0)
cil(LAJ, F("b12", 1) - 0.5, E("b12") + 0.4, [[0, 0.0], [t_3370 - 0.2, 0.0], [t_3370 + 2.0, 33.7 / 36]], marca=29.92 / 36, t_marca=t_3370 + 2.1, h=1.0, r=0.08, dx=0.95, dz=-0.1, cor="#3D7FB8", cor_marca="#C9A46A")
num(t_3370 - 0.2, de=20, para=33.7, dur=2.0, faixa="RIO TAQUARI · LAJEADO · 2 MAI 2024 · SGB/ANA", unidade="m", dec=1); num_off(F("b12", 3) - 0.3)
rot("1941 · 29,92 M", [LAJ[0] + 0.25, LAJ[1] - 0.3], t_3370 + 2.2, F("b12", 2) + 1.5, "seta", y=0.2 + 1.0 * 29.92 / 36 + 0.1)
g5(tipo="selo", t0=tw("acima", "b12", alt=F("b12", 2) + 0.3), t1=F("b12", 3), texto="+3 M ACIMA DE 1941", top=300, left=1150, rot=-4)
foto("arroio-do-meio-navegantes-destruicao-aereo-2024-06-06.jpg", tw("Cidades", "b12", alt=F("b12", 3)) - 0.2, E("b12") + 0.4, lado="esq")
# b13 gota até Porto Alegre
est("b13", "A"); cam(S("b13") - 0.1, [LAJ[0] + 0.2, LAJ[1] - 0.05], 4.8, 38, 0, corte=False, y=0.1); cam(F("b13", 1) - 0.2, [P(-51.7, -29.9)[0], P(-51.7, -29.9)[1]], 6.5, 46, 0, y=0.1); cam(E("b13"), [PA[0] - 0.4, PA[1] - 0.2], 7.0, 48, 4, y=0.1)
arvore(["taquari", "jacui"], S("b13"), S("b13") + 0.4, S("b13") - 0.2, E("b13") + 0.5, larg=1.35, pico=[[0, 0.0], [S("b13") + 0.3, 0.9], [E("b13"), 0.3]])
gota([[LAJ[0] + 0.1, LAJ[1] + 0.0], P(-51.93, -29.68), P(-51.78, -29.88), P(-51.55, -29.97), P(-51.36, -30.0), [FOZ[0], FOZ[1]]], S("b13") + 0.3, E("b13") + 0.3, F("b13", 1) - 0.1, E("b13") - 0.2, esc=0.075, alto=0.15)
rot("TAQUARI", P(-51.75, -29.5), S("b13") + 0.3, F("b13", 1), "seta", y=0.3); rot("JACUÍ", P(-51.6, -30.1), F("b13", 1) + 0.4, E("b13") + 0.2, "seta", y=0.3); rot("PORTO ALEGRE", [PA[0] + 0.1, PA[1] + 0.2], E("b13") - 1.3, E("b13") + 0.4, "seta", y=0.3)

# ======================= 2 · O LAGO QUE RECEBE TUDO (b14–b19) =======================
est("b14", "A"); trans(S("b14") - 0.3, "nuvem", 1.2, "suba a câmera e olhe o mapa inteiro")
cam(S("b14") - 0.3, [PA[0] - 0.4, PA[1] - 0.2], 8.5, 46, 4, corte=True, y=0.1); cam(F("b14", 1), BAC2, 16.5, 58, 4, y=0.1); cam(E("b14"), [BAC2[0] + 0.1, BAC2[1] + 0.1], 15.0, 56, -4, y=0.1)
arvore("todos", S("b14") + 0.1, S("b14") + 6.5, S("b14") - 0.2, S("b20") - 0.4, larg=1.0)
pontos.append({"lista": MUNS, "cor": "#FFFFFF", "r": 1.0, "y": 0.13, "t0": tw("duzentos|250", "b14", alt=F("b14", 1) + 0.3) - 0.2, "t1": tw("duzentos|250", "b14", alt=F("b14", 1) + 0.3) + 2.6, "t2": E("b14") + 0.5})
t_250 = tw("250|duzentos", "b14", alt=F("b14", 1) + 0.5)
num(t_250 - 0.2, de=0, para=250, dur=1.6, faixa="MUNICÍPIOS NA BACIA DO GUAÍBA", unidade="+"); num_off(F("b14", 2) - 0.2)
num(F("b14", 2) + 0.9, valor="~85 MIL km²", faixa="UNS 30% DO RIO GRANDE DO SUL"); num_off(E("b14") + 0.3)
# b15 rios engrossam
est("b15", "B"); cam(S("b15"), BAC2, 15.0, 56, -4, corte=True, y=0.1); cam(E("b15"), [BAC2[0] + 0.1, BAC2[1] + 0.2], 13.0, 54, 6, y=0.1)
tp = {"jacui": tw("Jacuí", "b15", alt=S("b15") + 0.5), "taquari": tw("Taquari", "b15", alt=F("b15", 1) + 0.3), "cai": tw("Caí", "b15", alt=F("b15", 2) + 0.3), "sinos": tw("Sinos", "b15", alt=F("b15", 2) + 1.2), "gravatai": tw("grava", "b15", alt=F("b15", 2) + 1.9)}
for c, tt in tp.items(): arvore(c, S("b15") - 5, S("b15") - 4, tt - 0.4, F("b15", 3) + 1.0, larg=1.5, pico=pulso(tt, 2.4, 1.0))
for c, nome in (("jacui", "JACUÍ"), ("taquari", "TAQUARI"), ("cai", "CAÍ"), ("sinos", "SINOS"), ("gravatai", "GRAVATAÍ")): rot(nome, RIOCL[c], tp[c], F("b15", 3) + 0.8, "seta", y=0.3)
rot("O MESMO LAGO: GUAÍBA", P(-51.1, -30.35), F("b15", 3) + 0.2, E("b15") + 0.8, "corredor", y=0.35)
# b16 lago largo e raso
est("b16", "A"); trans(S("b16") - 0.2, "corte", 0.4, "câmera baixa sobre o Guaíba")
cam(S("b16"), [FOZ[0] - 0.1, FOZ[1] + 0.2], 3.8, 24, -30, corte=True, y=0.1); cam(F("b16", 1), [FOZ[0] - 0.1, FOZ[1] + 0.15], 3.2, 22, 10, y=0.1); cam(E("b16"), [FOZ[0] - 0.05, FOZ[1] + 0.1], 2.8, 26, 40, y=0.1)
foto_sat("hls-sentinel2-porto-alegre-guaiba-antes-2024-04-01-recorte.jpg", tw("baiba|guaiba", "b16", alt=S("b16") + 0.5) + 0.2, tw("baiba|guaiba", "b16", alt=S("b16") + 0.5) + 4.6, lado="dir")
t_500 = tw("500|quinhentos", "b16", alt=F("b16", 1) + 0.2)
num(t_500 - 0.2, de=0, para=500, dur=1.4, faixa="ÁREA DO LAGO GUAÍBA · POUCOS METROS DE FUNDURA", unidade="km²"); num_off(F("b16", 2) - 0.2)
rot("LARGO E RASO", [FOZ[0] - 0.55, FOZ[1] - 0.1], F("b16", 2) - 0.2, E("b16") + 0.5, "corredor", y=0.3)
# b17 vazão
est("b17", "B"); trans(S("b17") - 0.2, "corte", 0.4, "mapa editorial")
cam(S("b17"), [FOZ[0] - 0.3, FOZ[1] - 0.3], 8.5, 50, 0, corte=True, y=0.1); cam(E("b17"), [FOZ[0] - 0.5, FOZ[1] - 0.3], 9.5, 52, 6, y=0.1)
t_b = tw("Jacuí", "b17", alt=S("b17") + 0.5); t_mil = tw("1|mil", "b17", alt=F("b17", 1) + 0.5); t_mai = tw("maio", "b17", alt=F("b17", 2) + 0.2)
g5(tipo="vazao", t0=S("b17") + 0.2, t1=E("b17") + 0.4, t_barra=t_b - 0.3, agulha=[[0, 0.0], [t_mil, 0.0], [t_mil + 1.2, 0.5], [t_mai + 0.3, 0.5], [t_mai + 1.6, 1.0]], t_selo=t_mai + 1.7)
# b18 tempo da água
est("b18", "B"); cam(S("b18"), BAC2, 14.0, 56, 0, corte=True, y=0.1); cam(E("b18"), [BAC2[0] + 0.1, BAC2[1] + 0.2], 12.5, 54, 8, y=0.1)
t_qui = tw("quinta", "b18", n=0, alt=S("b18") + 2.0); t_cai = tw("Caí", "b18", alt=t_qui + 0.4); t_sab = tw("sábado|sabado", "b18", alt=F("b18", 1) + 2.0); t_dom = tw("domingo", "b18", n=0, alt=F("b18", 1) + 3.5); t_gdom = tw("domingo", "b18", n=1, alt=F("b18", 3) + 2.0)
g5(tipo="calendario", modo="picos", t0=S("b18") + 0.3, t1=E("b18") + 0.4, tp=[t_qui, t_cai + 0.1, t_sab, t_dom, t_gdom])
for c, tt in (("taquari", t_qui), ("cai", t_cai), ("sinos", t_sab), ("jacui", t_dom)): arvore(c, S("b18") - 5, S("b18") - 4, S("b18") - 0.3, E("b18") + 0.8, larg=1.4, pico=pulso(tt, 2.2, 1.0))
# b19 o lago recebe tudo
est("b19", "A"); cam(S("b19"), BAC2, 14.0, 54, 0, corte=True, y=0.1); cam(F("b19", 2) - 0.3, [PA[0] - 0.7, PA[1] - 0.4], 9.0, 46, 6, y=0.1); cam(E("b19"), [PA[0] - 0.4, PA[1] - 0.2], 6.5, 42, 10, y=0.1)
gotas.append({"pontos": [[FOZ[0] - 0.02, FOZ[1]], [FOZ[0], FOZ[1] + 0.01]], "prog": [[0, 0], [99999, 0]], "op": janela_op(F("b19", 2) + 0.2, E("b19") + 1.5, 1, 0.7, 0.8), "esc": 0.2, "alto": 0.15, "cauda": 0.0})
pino("pa19", "PORTO ALEGRE", "NA FRENTE DO LAGO", F("b19", 2) + 0.2, t2=E("b19") + 1.0, xz=PA, y0=0.1, ate=E("b19") + 0.6)
g5(tipo="frase", t0=F("b19", 2), t1=E("b19") + 0.6, linhas=["O LAGO NA FRENTE DA CIDADE", "RECEBE TUDO."], destaque=1, top=700, left=90, tam=64, dur=2.2)

# ======================= 3 · A SAÍDA (b20–b24) =======================
est("b20", "A"); trans(S("b20") - 0.3, "whip", 0.6, "câmera desce do Guaíba para o sul")
cam(S("b20") - 0.2, [FOZ[0], FOZ[1] + 0.1], 5.0, 34, 0, corte=True, y=0.1); cam(F("b20", 1) + 0.5, [P(-51.5, -31.0)[0], P(-51.5, -31.0)[1]], 11.5, 48, 6, y=0.1); cam(E("b20"), [P(-51.7, -31.3)[0], P(-51.7, -31.3)[1]], 14.0, 52, 0, y=0.1)
rot("LAGOA DOS PATOS", P(-51.55, -31.15), tw("Lagoa", "b20", alt=F("b20", 2)) - 0.1, E("b20") + 1.0, "mapa_grande", y=0.2)
foto_sat("nasa-modis-sul-do-rs-durante-2024-05-06.jpg", tw("Lagoa", "b20", alt=F("b20", 2)) + 0.3, tw("Lagoa", "b20", alt=F("b20", 2)) + 3.7, lado="esq")
tab(arquivo, 0, 0.0, 0.1)
# b21 laguna até Rio Grande
est("b21", "A"); cam(S("b21") - 0.1, [P(-51.35, -30.7)[0], P(-51.35, -30.7)[1]], 8.0, 44, -10, corte=False, y=0.1); cam(F("b21", 1), [P(-51.9, -31.4)[0], P(-51.9, -31.4)[1]], 8.0, 46, 0, y=0.1); cam(F("b21", 2) - 0.3, [BARRA[0] + 0.1, BARRA[1] - 0.2], 5.0, 40, 10, y=0.1); cam(E("b21"), [BARRA[0] + 0.1, BARRA[1] - 0.1], 3.6, 40, 20, y=0.1)
seta(CIANO, [[FOZ[0], FOZ[1]]] + LAGOA + [[BARRA[0], BARRA[1]]], S("b21") + 0.2, F("b21", 1) + 2.0, E("b22") + 1.0, y=0.45, r=0.05, fluxo=True, vel=0.1)
rot("250 KM", P(-51.7, -31.1), S("b21") + 1.0, F("b21", 2) - 0.2, "seta", y=0.55); rot("LAGUNA · LIGADA AO MAR", P(-51.2, -31.55), F("b21", 1) + 0.2, F("b21", 2) - 0.3, "corredor", y=0.4)
pino("rg", "RIO GRANDE (RS)", "BARRA · DOIS MOLHES DE PEDRA", F("b21", 2) - 0.2, t2=E("b22") + 0.5, xz=RG, y0=0.1, ate=E("b21") + 1.0)
rot("SAÍDA ESTREITA", [BARRA[0] + 0.55, BARRA[1] + 0.15], tw("mole|molhe", "b21", alt=F("b21", 2) + 1.0), E("b21") + 1.0, "corredor", y=0.35)
foto("rio-grande-fragata-f44-canal-da-barra-molhes-2023-08-15.jpg", tw("mole|molhe", "b21", alt=F("b21", 2) + 1.0) - 0.2, E("b21") + 0.5, lado="esq")
# b22 caminho inteiro
est("b22", "B"); trans(S("b22") - 0.2, "corte", 0.4, "esquema em relevo editorial")
cam(S("b22"), [RSC[0] + 1.4, RSC[1] + 0.8], 17.0, 56, 0, corte=True, y=0.1); cam(E("b22"), [RSC[0] + 1.4, RSC[1] + 0.8], 15.0, 58, 6, y=0.1)
t_e = [S("b22") + 0.6, tw("lago", "b22", alt=F("b22", 0) + 1.5), tw("duzentos|250", "b22", alt=F("b22", 1) + 0.5), tw("gargalo", "b22", alt=F("b22", 2) + 1.2)]
g5(tipo="etapas", t0=S("b22") + 0.2, t1=E("b22") + 0.5, t=t_e, top=250)
# b23 vento
est("b23", "A"); trans(S("b23") - 0.2, "corte", 0.4, "")
cam(S("b23"), [P(-51.7, -31.3)[0], P(-51.7, -31.3)[1]], 13.0, 52, 0, corte=True, y=0.1); cam(E("b23"), [P(-51.6, -31.1)[0], P(-51.6, -31.1)[1]], 11.5, 50, 10, y=0.1)
t_v = tw("vento", "b23", alt=S("b23") + 0.5)
for k, dx in enumerate((-0.6, 0.0, 0.6)):
    seta("#FFFFFF", [[P(-52.5, -32.7)[0] + dx, P(-52.5, -32.7)[1]], [P(-52.0, -31.9)[0] + dx, P(-52.0, -31.9)[1]], [P(-51.5, -31.2)[0] + dx, P(-51.5, -31.2)[1]], [P(-51.1, -30.5)[0] + dx, P(-51.1, -30.5)[1]]], t_v + 0.3 * k, t_v + 1.8 + 0.3 * k, E("b23") + 0.6, y=0.7, r=0.045, fluxo=True, vel=0.12)
rot("VENTO SUL", P(-52.3, -32.1), t_v + 0.5, E("b23") + 0.5, "seta", y=0.8)
rot("ATÉ ~50 CM A MAIS (IPH/UFRGS)", P(-50.9, -30.5), tw("cinquenta|50", "b23", alt=F("b23", 2) + 1.5), E("b23") + 0.8, "corredor", y=0.5)
g5(tipo="selo", t0=tw("cinquenta|50", "b23", alt=F("b23", 2) + 1.5) + 1.0, t1=E("b23") + 0.6, texto="AGRAVANTE, NÃO A CAUSA PRINCIPAL", top=190, left=110, rot=-3, cor="#1F2A44", tam=40)
# b24 maio
est("b24", "B"); trans(S("b24") - 0.2, "corte", 0.4, "")
cam(S("b24"), [P(-51.7, -31.3)[0], P(-51.7, -31.3)[1]], 14.0, 56, 0, corte=True, y=0.1); cam(E("b24"), [P(-51.8, -31.2)[0], P(-51.8, -31.2)[1]], 13.0, 56, 8, y=0.1)
t_pat = tw("Patos", "b24", alt=S("b24") + 1.5); t_pel = tw("Pelotas", "b24", alt=F("b24", 1) + 3.0); t_slo = tw("Lourenço|Lourenco", "b24", alt=t_pel + 0.6); t_rgx = tw("Grande", "b24", n=0, alt=t_slo + 0.8)
g5(tipo="calendario", modo="maio", t0=S("b24") + 0.3, t1=E("b24") + 0.4, t_banda=tw("mês|mes", "b24", alt=F("b24", 2) + 2.0) - 1.0, tm=[S("b24") + 0.8, t_pat, t_pat + 2.6])
pino("pel", "PELOTAS", "LAGOA · MAIO DE 2024", t_pel, t2=E("b24") + 0.6, xz=PEL, y0=0.1, ate=E("b24")); pino("sls", "SÃO LOURENÇO DO SUL", "", t_slo, t2=E("b24") + 0.6, xz=SLS, y0=0.1, ate=E("b24")); pino("rg24", "RIO GRANDE", "", t_rgx, t2=E("b24") + 0.6, xz=RG, y0=0.1, ate=E("b24"))
foto("pelotas-bairros-alagados-aereo-2024-05-18.jpg", t_pel + 0.3, t_pel + 3.7, lado="dir")
num(tw("mês|mes", "b24", alt=F("b24", 2) + 2.0), valor="~1 MÊS", faixa="GUAÍBA ACIMA DA COTA DE INUNDAÇÃO · PORTO ALEGRE"); num_off(E("b24") + 0.3)

# ======================= 4 · O QUE CEDEU (b25–b33) =======================
est("b25", "B"); trans(S("b25") - 0.2, "corte", 0.5, "corte seco para o papel sépia"); tab(arquivo, S("b25") - 0.2, 0.7, 0.1); tab(arquivo, E("b25") + 0.3, 0.0, 0.2)
cam(S("b25"), [PA[0] - 0.1, PA[1] - 0.1], 5.0, 42, 0, corte=True, y=0.1); cam(E("b25"), [PA[0], PA[1]], 4.4, 44, 8, y=0.1)
cobre.append([round(S("b25") - 0.15, 3), round(E("b25") + 0.35, 3)])
papel("b25", "b25", [{"tipo": "data", "texto": "PORTO ALEGRE · MAIO DE 1941", "t": S("b25") + 0.2},
    {"tipo": "titulo", "texto": "GUAÍBA: 4,7 METROS", "t": tw("4|quatro", "b25", alt=F("b25", 2) + 1.0) - 0.3, "tam": 96},
    {"tipo": "rotulo", "texto": "UM MÊS ATÉ VOLTAR AOS 3 M", "t": tw("mês|mes", "b25", alt=F("b25", 2) + 3.5)},
    {"tipo": "carimbo", "texto": "1941", "t": tw("quarenta|1941", "b25", alt=F("b25", 2) + 0.2), "tam": 90}], pre=0.15, topo=True)
foto("mercado-publico-fachada-alagado-enchente-1941-05-recorte.jpg", S("b25") + 1.0, E("b25") + 0.2, lado="dir", fmt="cartep")
est("b26", "B"); trans(S("b26") - 0.2, "corte", 0.5, "maquete da orla")
cam(S("b26"), [PA[0] - 0.4, PA[1] - 0.3], 6.0, 44, 0, corte=True, y=0.1); cam(E("b26"), [PA[0] - 0.4, PA[1] - 0.2], 5.0, 46, 8, y=0.1)
t_muro = tw("muro", "b26", alt=F("b26", 2) + 0.3); t_dq = tw("Sessenta|68", "b26", alt=t_muro + 1.8); t_cp2 = tw("Quatorze|14", "b26", alt=t_dq + 1.5); t_bb = tw("vinte|23", "b26", alt=t_cp2 + 1.5)
MAQ = {"t_muro": t_muro, "t_dique": t_dq, "t_comp": t_cp2, "t_bomb": t_bb}
g5(tipo="maquete", t0=S("b26") + 0.3, t1=E("b31") + 0.4, titulo="O SISTEMA DE PROTEÇÃO CONTRA CHEIAS", ocultar=[[S("b27") - 0.1, E("b27") + 0.1]], **MAQ,
   t_falha=tw("rompeu", "b28", alt=F("b28", 1) + 1.0), t_agua=tw("entrou", "b28", alt=F("b28", 2) + 0.5), t_apaga=tw("dezenove|19", "b29", alt=F("b29", 1) + 1.0), t_sarandi=tw("saran", "b30", alt=S("b30") + 0.5),
   rotulos=[["COMPORTA · AV. SERTÓRIO · 3 MAI", 330, 360, tw("rompeu", "b28", alt=F("b28", 1) + 1.0), CORAL], ["NAVEGANTES", 130, 388, tw("Navegantes", "b28", alt=F("b28", 2) + 1.0), CORAL],
            ["SEM ENERGIA · INUNDADAS", 700, 385, tw("energia", "b29", alt=S("b29") + 0.8), CORAL], ["SARANDI", 150, 330, tw("saran", "b30", alt=S("b30") + 0.5), CORAL], ["CASA DE BOMBAS Nº 10", 380, 392, tw("10|dez", "b30", alt=S("b30") + 3.0), CORAL]])
cartao(tw("projeto", "b26", alt=F("b26", 1)) - 0.2, F("b26", 2) - 0.2, "PORTO ALEGRE", "PROJETO DE 1943 · OBRAS DOS ANOS 70", top=730)
foto("muro-da-maua-grafite-dia-normal-2016-04-23.jpg", t_muro + 0.1, t_muro + 3.1, lado="dir")
num(t_dq - 0.2, valor="68 KM", faixa="DE DIQUES"); num_off(t_cp2 - 0.2); num(t_cp2 - 0.1, valor="14", faixa="COMPORTAS"); num_off(t_bb - 0.2); num(t_bb - 0.1, valor="23", faixa="CASAS DE BOMBAS"); num_off(E("b26") + 0.2)
# b27 corte esquemático
est("b27", "B"); cam(S("b27"), [PA[0] - 0.4, PA[1] - 0.3], 5.4, 44, 0, corte=True, y=0.1); cam(E("b27"), [PA[0] - 0.4, PA[1] - 0.3], 5.0, 46, 8, y=0.1)
g5(tipo="corte", t0=S("b27") + 0.1, t1=E("b27") + 0.2, t_muro=S("b27") + 0.5, t_comp=tw("comportas", "b27", alt=F("b27", 2) + 0.2), t_bomba=tw("bomba", "b27", alt=F("b27", 3) + 0.2), t_falha=tw("falha", "b27", alt=F("b27", 4) + 0.3))
foto("comporta-cais-maua-fechamento-2024-05-02.jpg", tw("comportas", "b27", alt=F("b27", 2) + 0.2) - 0.1, tw("comportas", "b27", alt=F("b27", 2) + 0.2) + 3.0, lado="esq")
cartao(F("b27", 4) - 0.1, E("b27") + 0.3, "O RISCO DO SISTEMA", "SE UMA PEÇA FALHA, A ÁGUA ACHA O CAMINHO", top=730)
# b28–b31 maquete continua (g5 acima cobre b26–b31)
est("b28", "A"); cam(S("b28"), [PA[0] - 0.2, PA[1] - 0.2], 4.0, 44, 0, corte=True, y=0.1); cam(E("b28"), [PA[0] - 0.1, PA[1] - 0.15], 3.4, 46, 10, y=0.1)
est("b29", "B"); cam(S("b29"), [PA[0] - 0.4, PA[1] - 0.3], 5.0, 46, 0, corte=True, y=0.1); cam(E("b29"), [PA[0] - 0.4, PA[1] - 0.2], 4.6, 46, 8, y=0.1)
num(tw("dezenove|19", "b29", alt=F("b29", 1) + 1.0) - 0.2, de=0, para=19, dur=1.2, faixa="DE 23 CASAS DE BOMBAS PARADAS · NO DIA SEGUINTE AO PICO · PREFEITURA"); num_off(E("b29") + 0.2)
est("b30", "A"); cam(S("b30"), [PA[0] - 0.1, PA[1] - 0.3], 4.0, 44, 0, corte=True, y=0.1); cam(E("b30"), [PA[0] - 0.05, PA[1] - 0.25], 3.4, 46, 10, y=0.1)
num(tw("vinte|26", "b30", n=0, alt=F("b30", 1) + 1.0) - 0.2, valor="~26 MIL", faixa="PESSOAS ATINGIDAS · SARANDI · SEGUNDO A PREFEITURA"); num_off(E("b30") + 0.2)
est("b31", "B"); cam(S("b31"), [PA[0] - 0.4, PA[1] - 0.3], 5.0, 46, 0, corte=True, y=0.1); cam(E("b31"), [PA[0] - 0.4, PA[1] - 0.2], 4.6, 46, 8, y=0.1)
g5(tipo="selo", t0=tw("passou", "b31", alt=S("b31") + 1.5), t1=F("b31", 1) + 1.5, texto="A ÁGUA NÃO PASSOU POR CIMA DO MURO", top=100, left=520, rot=-3, tam=50)
cartao(F("b31", 2) - 0.2, E("b31") + 0.3, "WORLD WEATHER ATTRIBUTION", "FALHA DESDE ~4,5 M · DECLARADA: 6 M", top=330, left=1240, w=640)
# b32 arquivo: três explicações
est("b32", "B"); trans(S("b32") - 0.2, "corte", 0.5, "papel"); tab(arquivo, S("b32") - 0.2, 0.7, 0.1); tab(arquivo, E("b32") + 0.3, 0.0, 0.2)
cam(S("b32"), [PA[0] - 0.1, PA[1] - 0.1], 5.0, 42, 0, corte=True, y=0.1); cam(E("b32"), [PA[0], PA[1]], 4.4, 44, 8, y=0.1)
cobre.append([round(S("b32") - 0.15, 3), round(E("b32") + 0.35, 3)])
papel("b32", "b32", [{"tipo": "titulo", "texto": "POR QUE FALHOU? AINDA SE DISCUTE", "t": S("b32") + 0.2, "tam": 78},
    {"tipo": "fichas", "itens": [["MANUTENÇÃO · EX-DIRETORES DO DMAE", tw("manutenção|manutencao", "b32", alt=F("b32", 1) + 1.0) - 0.3], ["CONCEPÇÃO · PREFEITURA", tw("concepção|concepcao", "b32", alt=F("b32", 1) + 3.0) - 0.3], ["GESTÃO · PESQUISADORES", tw("gestão|gestao", "b32", alt=F("b32", 1) + 5.5) - 0.3]], "t": S("b32") + 0.8},
    {"tipo": "carimbo", "texto": "EM DISCUSSÃO", "t": F("b32", 1) + 0.3, "tam": 70},
    {"tipo": "rotulo", "texto": "NÃO SEGUROU ESSA CHEIA · 5,35 M", "t": F("b32", 2) + 0.6}], pre=0.15, topo=True)
# b33 a cidade
est("b33", "A"); trans(S("b33") - 0.2, "corte", 0.4, "")
cam(S("b33"), [PA[0] - 0.2, PA[1] - 0.2], 4.4, 44, -10, corte=True, y=0.1); cam(F("b33", 2) - 0.3, [PA[0] - 0.05, PA[1] - 0.05], 3.0, 46, 10, y=0.1); cam(E("b33"), [PA[0] - 0.05, PA[1]], 4.8, 44, 20, y=0.1)
gota([[FOZ[0] + 0.15, FOZ[1] - 0.05], [PA[0] - 0.03, PA[1] + 0.03]], S("b33"), F("b33", 1) + 0.5, S("b33") + 0.2, F("b33", 1), esc=0.07, alto=0.14)
t_mp = tw("Mercado", "b33", alt=F("b33", 1) + 0.3)
foto("mercado-publico-ilhado-aereo-2024-05-05.jpg", t_mp + 0.1, t_mp + 3.0, lado="esq")
cartao(tw("metro", "b33", alt=t_mp + 1.0) - 0.2, tw("metro", "b33", alt=t_mp + 1.0) + 2.6, "MERCADO PÚBLICO · 5 MAI 2024", "ÁGUA A 1,5 M", top=730)
for nome, (lo, la), tt in (("MENINO DEUS", (-51.225, -30.055), 0), ("FARRAPOS", (-51.205, -30.0), 1), ("HUMAITÁ", (-51.19, -29.98), 2), ("ILHAS", (-51.25, -30.01), 3)):
    rot(nome, P(lo, la), tw(nome.split()[0], "b33", alt=F("b33", 2) + 0.3 * tt), E("b33") + 0.5, "corredor", y=0.35)
t_tr = tw("30|trinta", "b33", alt=F("b33", 3) + 0.3)
foto("centro-historico-edificios-historicos-alagados-aereo-2024-05-05.jpg", t_tr + 0.3, E("b33") + 0.4, lado="dir")
num(t_tr - 0.2, valor="~30%", faixa="DO TERRITÓRIO DA CAPITAL · SEGUNDO A PREFEITURA"); num_off(E("b33") + 0.3)

# ======================= A RESPOSTA (b34–b40) =======================
est("b34", "A"); trans(S("b34") - 0.3, "whip", 0.7, "volta à serra")
cam(S("b34") - 0.2, [CX[0] + 1.0, CX[1] - 1.0], 9.0, 28, -20, corte=True, y=0.1); cam(E("b34"), [CX[0] + 0.3, CX[1] - 0.2], 5.2, 34, 6, y=0.1)
chuva(CX, S("b34"), E("b34") + 0.5, r=0.45, h=1.6, n=60)
cil(CX, S("b34") - 0.2, E("b34") + 0.6, [[0, 266 / 300], [99999, 266 / 300]], marca=94.4 / 300, t_marca=0, h=1.25, r=0.1)
g5(tipo="frase", t0=F("b34", 1), t1=E("b34") + 0.6, linhas=["POR QUE A CHUVA DA SERRA", "ALAGOU PORTO ALEGRE?"], destaque=1, top=640, left=90, tam=68, dur=2.4)
est("b35", "A"); cam(S("b35"), BAC2, 15.5, 56, 0, corte=True, y=0.1); cam(E("b36"), [BAC2[0] + 0.1, BAC2[1] + 0.1], 14.0, 54, 8, y=0.1)
arvore("todos", S("b35") + 0.2, S("b35") + 6.0, S("b35") - 0.2, S("b37") + 0.3, larg=1.0)
t_p1, t_p2, t_p3 = [tw("Porque", "b35", n=k, alt=F("b35", k)) for k in range(3)]; t_p4, t_p5 = [tw("Porque", "b36", n=k, alt=F("b36", k)) for k in range(2)]
checklists.append({"t0": round(S("b35") + 0.3, 3), "t1": round(E("b36") + 0.5, 3), "titulo": "A RESPOSTA, EM CINCO PORQUÊS", "itens": [["3 MESES DE CHUVA EM 11 DIAS", round(t_p1 + 1.0, 3)], ["RIOS JÁ CHEIOS: 3ª CHEIA EM 8 MESES", round(t_p2 + 1.0, 3)], ["1/3 DO ESTADO PARA UM LAGO RASO", round(t_p3 + 1.0, 3)], ["SAÍDA LENTA, ESTREITA E LONGA", round(t_p4 + 1.0, 3)], ["DEFESA CEDEU NOS PONTOS FRACOS", round(t_p5 + 1.0, 3)]]})
est("b36", "A")
est("b37", "B"); trans(S("b37") - 0.2, "corte", 0.4, "")
cam(S("b37"), [RSC[0] + 0.5, RSC[1]], 16.0, 56, 0, corte=True, y=0.1); cam(E("b37"), [RSC[0] + 0.5, RSC[1]], 14.5, 58, 6, y=0.1)
g5(tipo="wwa", t0=S("b37") + 0.3, t1=E("b37") + 0.4, t=[tw("dobrou", "b37", alt=F("b37", 1) + 2.0), tw("seis|6", "b37", alt=F("b37", 1) + 4.5), tw("Niño|Nino|elninho", "b37", alt=F("b37", 2) + 1.5)])
est("b38", "A"); cam(S("b38"), BAC2, 15.0, 56, -6, corte=True, y=0.1); cam(E("b38"), [BAC2[0] + 0.1, BAC2[1] + 0.1], 13.0, 54, 10, y=0.1)
arvore("todos", S("b38") - 6, S("b38") - 5, S("b38") - 0.3, S("b40") + 6, larg=1.0)
g5(tipo="selo", t0=tw("prever|previsão|previsao", "b38", alt=S("b38") + 1.5) - 0.3, t1=F("b38", 1) + 1.0, texto="NÃO É PREVISÃO", top=190, left=110, rot=-3, cor="#1F2A44", tam=52)
g5(tipo="frase", t0=tw("geografia", "b38", alt=F("b38", 1) + 0.5) - 0.2, t1=E("b38") + 0.6, linhas=["A GEOGRAFIA NÃO MUDA."], destaque=0, top=760, left=90, tam=76, dur=1.4)
est("b39", "B"); trans(S("b39") - 0.2, "corte", 0.4, "")
cam(S("b39"), [PA[0] - 0.4, PA[1] - 0.3], 6.0, 46, 0, corte=True, y=0.1); cam(E("b39"), [PA[0] - 0.4, PA[1] - 0.2], 5.4, 46, 8, y=0.1)
t_conc = tw("concreto", "b39", alt=S("b39") + 2.5)
g5(tipo="maquete", t0=S("b39") + 0.2, t1=F("b39", 1) + 0.2, titulo="OBRAS ANUNCIADAS PELA PREFEITURA", ocultar=[], t_muro=S("b39") - 10, t_dique=S("b39") - 10, t_comp=S("b39") - 10, t_bomb=S("b39") - 10, t_concreto=t_conc, left=70, w=1140,
   rotulos=[["8 DE 14 COMPORTAS VIRAM CONCRETO", 330, 290, t_conc, "#444"]])
foto("cais-maua-galpao-marcas-da-enchente-2026-03-12.jpg", t_conc + 0.4, t_conc + 3.4, lado="dir")
g5(tipo="sms", t0=tw("SMS|alerta", "b39", alt=F("b39", 1) + 0.3) - 0.3, t1=E("b39") + 0.6, t_msg=tw("SMS|alerta", "b39", alt=F("b39", 1) + 0.3) + 0.2)
est("b40", "B"); cam(S("b40"), [BAC2[0] + 0.3, BAC2[1]], 15.5, 56, 0, corte=True, y=0.1); cam(E("b40"), [BAC2[0] + 0.3, BAC2[1]], 14.5, 56, 10, y=0.1)
cartao(S("b40") + 0.4, F("b40", 1) - 0.2, "NO CANAL", "POR QUE O SUL TEM UM CLIMA TÃO DIFERENTE", top=300)
cta = {"t0": F("b40", 1) + 0.2, "t_inscreve": tw("inscreve", "b40", alt=F("b40", 2) + 0.3) - 0.2, "texto": "MANDA PRA QUEM TEM FAMÍLIA NO RIO GRANDE DO SUL", "inscreve": "INSCREVA-SE · EM RELEVO"}

fontes = [
    {"t": 0, "texto": "FONTES: INMET (CHUVA) · SEMA/ANA (GUAÍBA) · SGB/ANA (LAJEADO) · PREFEITURA DE PORTO ALEGRE · DEFESA CIVIL RS"},
    {"t": S("b07") - 0.5, "texto": "FONTES: WORLD WEATHER ATTRIBUTION · INMET · SGB/ANA · IPH/UFRGS · MAPA: IBGE · RIOS: OPENSTREETMAP"},
    {"t": S("b14") - 0.5, "texto": "FONTES: IPH/UFRGS (RBRH) · GOVERNO DO RS · DMAE · SENTINEL-2 / COPERNICUS · NASA"},
    {"t": S("b25") - 0.5, "texto": "FONTES: DMAE · PREFEITURA DE PORTO ALEGRE · WORLD WEATHER ATTRIBUTION · IPH/UFRGS"},
]

# ----- palco das thumbs: tempos DEPOIS do fim do vídeo (a composição não os renderiza; Thumb.jsx usa tempo=cues.thumbs.*): mapa escuro (noite) + árvore grossa
DUR = tempos["duracao"]; T_A, T_B = round(DUR + 8, 3), round(DUR + 20, 3)
for T_, (cx_, cz_, dist_, el_, az_, esc_) in ((T_A, (-0.37 - 0.75, 2.78, 8.6, 58, 2, 0.07)), (T_B, (-0.15, 3.2, 5.4, 27, 8, 0.2))):
    ESTILO.append((T_ - 0.5, "B")); tab(noite, T_ - 0.6, 1.0, 0.2); tab(noite, T_ + 5, 0.0, 0.2); tab(luz, T_ - 0.6, 1.0, 0.2)
    cam(T_ - 0.5, [cx_, cz_], dist_, el_, az_, corte=True, y=0.1)
    arvore("todos", T_ - 8, T_ - 7, T_ - 6, T_ + 4, larg=1.5, cor="#3FD8FF")
    arvore("principais", T_ - 8, T_ - 7, T_ - 6, T_ + 4, larg=2.6 if T_ == T_A else 2.2, cor="#3FD8FF", pico=[[0, 0.25], [99999, 0.25]])
    gotas.append({"pontos": [[FOZ[0] - 0.02, FOZ[1]], [FOZ[0], FOZ[1] + 0.01]], "prog": [[0, 0], [99999, 0]], "op": janela_op(T_ - 6, T_ + 4, 1, 0.1, 0.1), "esc": esc_, "alto": 0.15, "cauda": 0.0})
thumbs_t = {"A": T_A, "B": T_B}
cx_itens = [{"n": 1, "texto": "", "t": 99999}]
cues = {
    "_doc": "Gerado por shared/build_cues.py (não editar à mão). Tempos em segundos de audio/narracao.wav.",
    "fps": 30, "duracao": tempos["duracao"], "fim_fala": tempos["blocos"][-1]["e"], "slot": None, "voz": tempos.get("voz"),
    "paleta": {"papel": "#E9DCC3", "coral": "#E8505B", "navy": "#1F2A44", "tinta": "#2B2622", "branco": "#FBF8F1"},
    "palavras": palavras, "capitulos": capitulos, "numero": sorted(numero, key=lambda n: n["t"]), "camera": camera,
    "luz": sorted(luz), "noite": noite, "quente": quente, "amazonia": amazonia, "andes": andes_t, "arquivo": arquivo, "tremor": tremor, "desfoque": desfoque,
    "pinos": pinos, "destaques": [], "fios": [], "funis": [], "setas": setas, "nuvens": nuvens, "regioes": regioes, "rastros": [],
    "sats": [], "ciclones": [], "aneis": [], "supercelula": None, "rotulos_mapa": rotulos,
    "relevos": [], "diorama": None, "montanhas": [], "barras3d": [], "globos": [], "fumacas": [], "chuvas": chuvas,
    "cilindros": cilindros, "pontos": pontos, "tintas": tintas, "sst_datas": SST["datas"], "rios": rios_l, "gotas": gotas,
    "midia": midia, "manchetes": [], "cartoes": cartoes, "graficos": [], "graficos3": [], "graficos4": [], "graficos5": graficos5, "papeis": papeis, "checklists": checklists, "calendario": None,
    "pergunta": pergunta, "caixas": {"itens": cx_itens, "estados": []}, "cortica": {"t0": 9999, "t1": 9999, "itens": []}, "cobre3d": cobre,
    "thumbs": thumbs_t, "transicoes": sorted(transicoes, key=lambda x: x["t"]), "cta": cta, "fontes": fontes, "texturas": [],
}
cues["camera"].sort(key=lambda k: k["t"]); cues["rotulos"] = rotulos
json.dump(cues, open(A / "cues.json", "w"), ensure_ascii=False, separators=(",", ":"))
tr = []; ant = None
for t_, e_ in sorted(ESTILO):
    if e_ != ant: tr.append({"t": round(t_, 3), "e": e_}); ant = e_
json.dump({"_doc": "A/B do longo-05 (build_cues.py)", "trechos": tr}, open(A / "estilo_v2.json", "w"), ensure_ascii=False, indent=1)
(R / "work").mkdir(exist_ok=True)
with open(R / "work/storyboard.txt", "w") as f:
    for tr_ in cues["transicoes"]: f.write(f"TRANSIÇÃO {tr_['t']:7.2f}s {tr_['tipo']}: {tr_['desc']}\n")
    for m in midia: f.write(f"MÍDIA {m['t0']:7.2f}–{m['t1']:7.2f}s {m['id']} ({m['lado']})\n")
    f.write("\n".join(avisos))
print(f"ok: {len(palavras)} palavras, {len(camera)} chaves de câmera, {len(midia)} mídias, {len(transicoes)} transições, {len(rios_l)} camadas de rio, {len(gotas)} gotas, {len(graficos5)} g5, {len(papeis)} papéis")
print("avisos:", *avisos, sep="\n  ")
