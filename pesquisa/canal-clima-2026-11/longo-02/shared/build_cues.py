# Storyboard em código do longo 02 (Em Relevo, Super El Niño 2026): gera shared/cues.json (fonte única da Composition "Longo")
# a partir de blocos.json, tempos.json, whisper.json, geo.json e sst_pacifico.json. Eventos amarrados à palavra falada
# (Whisper) ou ao início da frase. Base: longo-01/shared/build_cues.py (mesmos helpers).
# Os blocos do SLOT [ATUALIZAR 12/11] (b19–b21) só têm eventos dentro da janela fixa (tempos["slot"]), para que a troca
# desses blocos em 12/11 não mexa em nada antes nem depois.
import json, math, re, unicodedata
from pathlib import Path

A = Path(__file__).parent; R = A.parent
blocos = json.load(open(A / "blocos.json"))
tempos = json.load(open(A / "tempos.json"))
wh = json.load(open(A / "whisper.json"))
geo = json.load(open(A / "geo.json"))
SST = json.load(open(A / "sst_pacifico.json"))
FOTOS = {f["arquivo"]: f for f in json.load(open(R / "dl/fotos/fotos.json"))}
pj = geo["proj"]; PAC = geo["pac"]
def P(lon, lat): return [round((lon - pj["lon0"]) * pj["cos"] * pj["k"], 3), round(-(lat - pj["lat0"]) * pj["k"], 3)]
def P2(lon, lat): l = lon % 360; return [round(PAC["x0"] + (l - PAC["lonc"]) * PAC["k"], 3), round(PAC["z0"] - lat * PAC["k"], 3)]
C = geo["cidades"]
T = {b["id"]: b for b in tempos["blocos"]}
SLOT = tempos.get("slot")
S = lambda b: T[b]["s"]
E = lambda b: T[b]["e"]
def F(b, k): return T[b]["frases"][min(k, len(T[b]["frases"]) - 1)]["s"]
def FE(b, k): return T[b]["frases"][min(k, len(T[b]["frases"]) - 1)]["e"]
avisos = []

def norm(w):
    w = unicodedata.normalize("NFD", w.lower()); w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", w)
def tw(palavra, b, apos=None, n=0, alt=None):
    """tempo da (n+1)-ésima palavra falada que começa com <palavra> no bloco b (depois de <apos>); senão alt (ou meio do bloco)"""
    t0 = (apos if apos is not None else S(b) - 0.35); t1 = E(b) + 0.2; alvos = [norm(x) for x in palavra.split("|")]; k = 0
    for w in wh:
        if t0 <= w["s"] <= t1 and any(norm(w["w"]).startswith(a) for a in alvos):
            if k == n: return w["s"]
            k += 1
    avisos.append(f"palavra '{palavra}' não achada em {b}")
    return round(alt if alt is not None else (max(t0, S(b)) + E(b)) / 2, 3)

# ---------------- legenda (palavras da tela com o tempo da palavra falada) ----------------
palavras = []
for b in blocos:
    tb = T[b["id"]]
    ws = [w for w in wh if tb["s"] - 0.35 <= w["s"] <= tb["e"] + 0.1]
    linhas = [l.split() for l in b["tela"].split("|")]
    toks = [w for l in linhas for w in l]
    n, m = len(toks), len(ws)
    tt, j = [None] * n, 0
    for i, tk in enumerate(toks):
        for k in range(j, min(m, j + 5)):
            a, c = norm(tk), norm(ws[k]["w"])
            if a and c and (a == c or a.startswith(c) or c.startswith(a)):
                tt[i] = ws[k]["s"]; j = k + 1; break
    for i in range(n):
        if tt[i] is None:
            ant = next((tt[k] for k in range(i - 1, -1, -1) if tt[k] is not None), tb["s"])
            prox = next((tt[k] for k in range(i + 1, n) if tt[k] is not None), tb["e"])
            tt[i] = ant + (prox - ant) * 0.5
    i = 0
    for li, l in enumerate(linhas):
        if palavras: palavras.append("|")
        for w in l:
            palavras.append([w, round(max(tt[i], tb["s"] - 0.05), 3)]); i += 1
capitulos = []
for b in blocos:
    if not capitulos or capitulos[-1]["nome"] != b["cap"]:
        capitulos.append({"t": max(0, S(b["id"]) - 0.4), "nome": b["cap"]})

# ---------------- helpers de cena ----------------
camera = []
def cam(t, alvo, dist, el, az, y=0.3, corte=False):
    el, az = math.radians(el), math.radians(az); x, z = alvo
    k = {"t": round(t, 3), "alvo": [x, y, z], "pos": [round(x + dist * math.sin(az) * math.cos(el), 3), round(y + dist * math.sin(el), 3), round(z + dist * math.cos(az) * math.cos(el), 3)]}
    if corte: k["corte"] = True
    camera.append(k)
def off(c, dx=0, dz=0): return [c[0] + dx, c[1] + dz]
pinos, destaques, fios, funis, setas, nuvens, regioes, rastros, sats, ciclones, aneis, rotulos = [], [], [], [], [], [], [], [], [], [], [], []
relevos, montanhas, barras3d, globos, fumacas, chuvas, cilindros, pontos, tintas = [], [], [], [], [], [], [], [], []
def pino(id, nome, sub, t, t2=None, pequeno=False, cor=None, ate=None, xz=None, cid=None, y0=None):
    x, z = xz or C[cid]
    p = {"id": id, "nome": nome, "sub": sub, "x": x, "z": z, "t": round(t, 3), "pequeno": pequeno}
    if t2: p["t2"] = round(t2, 3)
    if cor: p["cor"] = cor
    if y0 is not None: p["y0"] = y0
    p["ate"] = round(ate if ate else (t2 if t2 else t + 6), 3)
    pinos.append(p)
def dest(nome, t, t2=None, cor=None):
    d = {"nome": nome, "t": round(t, 3)}
    if t2: d["t2"] = round(t2, 3)
    if cor: d["cor"] = cor
    destaques.append(d)
def rot(nome, xz, t0, t1, tipo="seta", y=None):
    r = {"nome": nome, "x": xz[0], "z": xz[1], "t0": round(t0, 3), "t1": round(t1, 3), "tipo": tipo}
    if y is not None: r["y"] = y
    rotulos.append(r)
def seta(cor, pts, t0, t1, t2, y=0.95, r=0.16, fluxo=False, vel=0.18, semCabeca=False):
    """pts: lista de [x, z] ou [x, z, y] em coordenadas da cena"""
    s = {"cor": cor, "pontos": [list(q) for q in pts], "t0": round(t0, 3), "t1": round(t1, 3), "t2": round(t2, 3), "y": y, "r": r, "fluxo": fluxo, "vel": vel}
    if semCabeca: s["semCabeca"] = True
    setas.append(s)
def janela_op(t0, t1, v=1.0, din=0.7, dout=0.7): return [[0, 0], [round(t0, 3), 0], [round(t0 + din, 3), v], [round(t1, 3), v], [round(t1 + dout, 3), 0]]
def anel_elipse(c0, ang, a_, b_, n=48, proj=P):
    ang = math.radians(ang)
    return [proj(c0[0] + a_ * math.cos(u) * math.cos(ang) - b_ * math.sin(u) * math.sin(ang), c0[1] + a_ * math.cos(u) * math.sin(ang) + b_ * math.sin(u) * math.cos(ang))
            for u in [2 * math.pi * i / n for i in range(n)]]
def retangulo(lon0, lon1, lat0, lat1, proj=P2, n=10):
    pts = [(lon0 + (lon1 - lon0) * i / n, lat1) for i in range(n)] + [(lon1, lat1 + (lat0 - lat1) * i / n) for i in range(n)] + \
          [(lon1 + (lon0 - lon1) * i / n, lat0) for i in range(n)] + [(lon0, lat0 + (lat1 - lat0) * i / n) for i in range(n)]
    return [proj(*q) for q in pts]

midia, numero, manchetes, cartoes, graficos, checklists, transicoes = [], [], [], [], [], [], []
def foto(arq, t0, t1, lado="dir", fmt="pol", pino=None, legenda=None, credito=None):
    """arq: fotos/<x>.jpg (metadados de dl/fotos/fotos.json) ou sat/<x>.jpg / img/<x> (legenda e crédito dados aqui)"""
    if arq.startswith("fotos/"):
        f = FOTOS[arq.split("/")[-1]]; legenda = legenda or f["legenda_tela"]; credito = credito or f["credito_tela"]
    midia.append({"id": arq, "tipo": "img", "src": arq, "fmt": fmt, "t0": round(t0, 3), "t1": round(t1, 3), "lado": lado, "legenda": legenda, "credito": credito, "pino": pino})
def num(t, valor=None, faixa="", de=None, para=None, dur=1.0, unidade=None, dec=0):
    if valor is not None: numero.append({"t": round(t, 3), "valor": valor, "faixa": faixa, "unidade": unidade})
    else: numero.append({"t": round(t, 3), "de": de, "para": para, "ate": round(t + dur, 3), "unidade": unidade, "faixa": faixa, "dec": dec})
def num_off(t): numero.append({"t": round(t, 3), "oculto": True})
def manchete(t0, t1, veiculo, texto, destaque, lado="esq"):
    manchetes.append({"t0": round(t0, 3), "t1": round(t1, 3), "veiculo": veiculo, "texto": texto, "destaque": destaque, "lado": lado})
def cartao(t0, t1, rotulo, texto, carimbo=None, t_carimbo=None, top=300):
    c = {"t0": round(t0, 3), "t1": round(t1, 3), "rotulo": rotulo, "texto": texto, "top": top}
    if carimbo: c["carimbo"] = {"texto": carimbo, "t": round(t_carimbo, 3)}
    cartoes.append(c)
def trans(t, tipo, dur=1.0, desc=""): transicoes.append({"t": round(t, 3), "tipo": tipo, "dur": dur, "desc": desc})
def meio(b1, b2): return (E(b1) + S(b2)) / 2

luz = [[0, 1]]; noite = [[0, 0]]; quente = [[0, 0]]; amazonia = [[0, 0]]; andes_t = [[0, 0]]; arquivo = [[0, 0]]; tremor = [[0, 0]]; desfoque = [[0, 0]]
def tab(lista, t, v, dur=0.6): lista.append([round(t, 3), lista[-1][1]]); lista.append([round(t + dur, 3), v])

# ---------------- lugares ----------------
MAN, DC, BV, MCP = C["MANAUS"], C["DIONÍSIO CERQUEIRA"], C["BOA VISTA"], C["MACAPÁ"]
PERU = P(-80.9, -6.2)                      # costa do Peru (Niño 1+2)
CONT = P(-58, -16)                         # continente
BR = P(-53, -17)
SUL = [-0.9, 0.7]
PACC = P2(195, 0)                          # centro da maquete do Pacífico
MONT = [PAC["x0"], 34.0]                   # palco das montanhas (ao sul da maquete do Pacífico)
GLOBO = [PAC["x0"], -48.0]                 # palco do globo (ao norte)
def grade_xy(lon0, lon1, lat0, lat1, proj):
    i0, i1 = int(lon0 - SST["lon0"]), int(lon1 - SST["lon0"]); j0, j1 = int(lat0 - SST["lat0"]), int(lat1 - SST["lat0"])
    xs = [proj(SST["lon0"] + i if proj is P2 else (SST["lon0"] + i) - 360 if SST["lon0"] + i > 180 else SST["lon0"] + i, 0)[0] for i in range(i0, i1 + 1)]
    zs = [proj(200 if proj is P2 else -80, SST["lat0"] + j)[1] for j in range(j0, j1 + 1)]
    return {"i0": i0, "i1": i1, "j0": j0, "j1": j1, "xs": xs, "zs": zs}
IDX_0411 = SST["datas"].index("2026-11-04"); NDAT = len(SST["datas"])

# ======================= HOOK =======================
# b01 Manaus (noite azulada, fumaça)
tab(noite, 0, 0.35, 0.1)
cam(0.0, MAN, 12, 44, -14); cam(F("b01", 2), MAN, 10.5, 40, 0); cam(E("b01") - 0.3, MAN, 11.5, 46, 12)
pino("man", "MANAUS · AM", "09/10/2026", 0.3, t2=E("b07") - 1.0, ate=S("b02") - 0.1, cid="MANAUS", y0=0.1)
fumacas.append({"x": MAN[0] + 0.3, "z": MAN[1] - 0.2, "t0": 0.2, "t1": S("b02") + 0.8, "r": 0.7, "h": 3.0, "s": 0.75, "n": 70, "vento": 1.6})
foto("sat/manaus-fumaca-2026-10-09-terra.jpg", F("b01", 1) + 0.2, F("b01", 3) - 0.1, legenda="MANAUS · 09/10/2026 · VISTA DO ESPAÇO", credito="IMAGEM: NASA MODIS TERRA (GIBS) · DOMÍNIO PÚBLICO", pino="man")
num(tw("quase", "b01", apos=F("b01", 2), alt=F("b01", 2)), de=0, para=196, dur=1.2, unidade="µg/m³", faixa="FUMAÇA FINA (PM2,5) · MANHÃ DE 09/10 · DEFESA CIVIL DE MANAUS")
num(F("b01", 3) + 0.2, "15", "OMS · MÁXIMO RECOMENDADO (MÉDIA DE 24 H)", unidade="µg/m³")
num_off(S("b02"))
# b02 desliza ~2.700 km até Dionísio Cerqueira: chuva + pluviômetro
tab(noite, S("b02") - 0.6, 0.0, 1.2)
cam(S("b02") + 0.9, DC, 10, 46, -8); cam(E("b02"), DC, 8.4, 40, 6)
pino("dc", "DIONÍSIO CERQUEIRA · SC", "OUTUBRO/2026", tw("Dionísio|Dionisio", "b02", alt=S("b02") + 1.5), t2=E("b07") - 1.0, ate=S("b03") - 0.1, cid="DIONÍSIO CERQUEIRA")
dest("DIONÍSIO CERQUEIRA", tw("Dionísio|Dionisio", "b02", alt=S("b02") + 1.5) + 0.2, t2=E("b04") + 0.5)
nuvens.append({"x": DC[0] - 0.2, "z": DC[1] - 0.2, "s": 1.1, "t": S("b02") + 0.4, "t2": E("b02") + 0.2, "y": 2.4})
chuvas.append({"x": DC[0] - 0.2, "z": DC[1] - 0.2, "t0": S("b02") + 0.6, "t1": E("b02") + 0.1, "r": 0.8, "h": 2.2, "n": 80})
t581 = tw("581|quinhentos", "b02", alt=F("b02", 0) + 3)
cilindros.append({"x": DC[0] + 0.9, "z": DC[1] + 0.2, "r": 0.28, "h": 2.0, "cor": "#3D6A9E", "op": janela_op(S("b02") + 0.8, E("b02") + 0.3, 1, 0.4, 0.5), "nivel": [[0, 0], [t581 - 0.3, 0], [t581 + 1.4, 1.0]]})
num(t581, de=0, para=581, dur=1.2, unidade="mm", faixa="CHUVA EM OUTUBRO/2026 · DIONÍSIO CERQUEIRA (SC) · INMET")
num(F("b02", 1) + 0.1, "MEIO METRO", "DE ÁGUA EM UM MÊS")
num_off(S("b03"))
# b03 sobe pelos Andes e sai sobre o Pacífico: relevo de calor real (OISST, semana de 04/11)
tab(andes_t, S("b03") - 0.3, 1.0, 0.8); tab(andes_t, E("b04"), 0.0, 1.0)
cam(S("b03") + 0.4, P(-68, -12), 34, 44, 40); cam(S("b03") + 2.6, P(-80, -7), 32, 42, 26); cam(E("b03") + 0.4, P(-82, -6), 30, 44, 18)
gp = grade_xy(265, 285, -16, 4, P)
relevos.append({**gp, "y0": 0.02, "k": 0.2, "idx": [[0, IDX_0411]], "op": janela_op(S("b03") + 0.3, E("b04") + 0.6, 1, 0.6, 0.8),
                "cresce": [[0, 0], [S("b03") + 0.4, 0], [S("b03") + 2.6, 1]], "mostra_data": False})
relevos.append({**gp, "y0": 0.02, "k": 0.2, "idx": [[0, IDX_0411]], "op": janela_op(S("b47") + 0.5, E("b48") + 3, 0.9, 1.0, 0.8), "mostra_data": False})
pino("peru", "COSTA DO PERU", "SEMANA DE 04/11", tw("Peru", "b03", alt=S("b03") + 2.0), t2=E("b07") - 1.0, ate=E("b03") + 0.2, xz=PERU, y0=0.05)
num(tw("cinco|5", "b03", alt=S("b03") + 3), "+5,6 °C", "MAR ACIMA DO NORMAL · NIÑO 1+2 (COSTA DO PERU) · SEMANA DE 04/11 · NOAA/CPC")
foto("sat/pacifico-anomalia-nasa-2026-11-08.jpg", S("b03") + 1.2, E("b03") + 0.4, legenda="PACÍFICO · TEMPERATURA DO MAR ACIMA DO NORMAL · 08/11/2026", credito="IMAGEM: NASA JPL (MUR, GIBS) · DOMÍNIO PÚBLICO", lado="esq")
num_off(S("b04"))
# b04 fio liga os 3 pinos
cam(S("b04") + 0.8, P(-62, -20), 64, 62, -4); cam(E("b04"), P(-62, -20), 62, 64, 4)
fios += [{"pontos": [MAN, DC], "t0": S("b04") + 0.6, "t1": S("b04") + 1.8, "t2": E("b07") - 1.0, "grosso": 4},
         {"pontos": [DC, PERU], "t0": S("b04") + 1.4, "t1": S("b04") + 2.6, "t2": E("b07") - 1.0, "grosso": 4},
         {"pontos": [PERU, MAN], "t0": S("b04") + 2.2, "t1": S("b04") + 3.4, "t2": E("b07") - 1.0, "grosso": 4}]
rot("FUMAÇA", off(MAN, 0, -3.5), tw("Fumaça", "b04", alt=S("b04")), E("b05"), "quente")
rot("ÁGUA DEMAIS", off(DC, 3, 2.5), tw("Água", "b04", alt=S("b04") + 1), E("b05"), "fria")
rot("MAR QUENTE", off(PERU, -2, 3.5), tw("Mar", "b04", alt=S("b04") + 2), E("b05"), "corredor")
cen = [(MAN[0] + DC[0] + PERU[0]) / 3, (MAN[1] + DC[1] + PERU[1]) / 3]
rot("?", cen, F("b04", 2), E("b06"), "corredor")
pergunta = {"t0": S("b05") - 0.1, "t1": F("b06", 1) - 0.15, "texto": "É mesmo um SUPER El Niño? O que ele vai fazer com o Brasil neste verão?"}
tab(luz, S("b05") - 0.3, 0.55, 0.8); tab(luz, S("b07") - 0.4, 1.0, 0.8)
cx_itens = [{"n": 1, "texto": "O QUE É O EL NIÑO?", "t": F("b06", 1)}, {"n": 2, "texto": "É SUPER?", "t": F("b06", 2)},
            {"n": 3, "texto": "O QUE MUDA NA MINHA REGIÃO?", "t": F("b06", 3)}, {"n": 4, "texto": "ATÉ QUANDO?", "t": F("b06", 4)}]
cx_estados = [{"t": cx_itens[0]["t"], "modo": "grande", "ativa": 0, "feitas": []}, {"t": S("b07") + 0.3, "modo": "compacta", "ativa": 0, "feitas": []},
              {"t": S("b08") - 0.5, "modo": "oculto"}]
cam(S("b07") + 1.5, P(-66, -14), 70, 66, 10); cam(E("b07") - 0.2, P(-74, -6), 78, 70, 30)
num(F("b07", 2), "+10 MIL KM", "DAQUI ATÉ O MEIO DO PACÍFICO")
num_off(E("b07"))

# T1 nuvem -> maquete do Pacífico
t_T1 = meio("b07", "b08")
trans(t_T1, "nuvem", 1.3, "push-in que atravessa uma nuvem: do continente para a maquete do Pacífico inteiro")

# ======================= 1/4 O QUE É (b08–b14) =======================
cx_estados += [{"t": S("b08") - 0.3, "modo": "grande", "ativa": 1, "feitas": [], "volta": True}, {"t": F("b08", 1), "modo": "compacta", "ativa": 1, "feitas": []}]
cam(t_T1 + 0.2, PACC, 58, 56, -6, corte=True); cam(E("b08"), PACC, 52, 54, 4)
for nome, ll, tipo in [("INDONÉSIA", (118, -1), "mapa"), ("AUSTRÁLIA", (134, -24), "mapa"), ("AMÉRICA DO SUL", (293, -12), "mapa"), ("OCEANO PACÍFICO", (205, 14), "mapa_grande")]:
    rot(nome, P2(*ll), S("b08"), E("b14"), tipo)
rot("EQUADOR (LINHA)", P2(160, 1.5), S("b08") + 1, E("b08"), "mapa")
alis = [P2(lo, 6.5) + [1.0] for lo in (276, 250, 220, 190, 160, 138)]
alis2 = [P2(lo, -6.5) + [1.0] for lo in (278, 252, 222, 192, 162, 140)]
t_alis = tw("alísios|alisios|ventos", "b08", alt=F("b08", 1))
seta("#EDE6D6", alis, t_alis, t_alis + 2.2, tw("enfraquecem", "b11", alt=F("b11", 1)) + 0.6, r=0.32, fluxo=True, vel=0.16)
seta("#EDE6D6", alis2, t_alis + 0.3, t_alis + 2.5, S("b09") + 0.2, r=0.32, fluxo=True, vel=0.16)
rot("ALÍSIOS: LESTE → OESTE", P2(205, 8.5), t_alis + 0.5, E("b10"), "seta")
# diorama (b09–b12)
D0, D1 = P2(122, 0)[0], P2(279, 0)[0]
diorama = {"x0": D0, "x1": D1, "z": 0.0, "prof": 3.2, "alt": 4.6, "y": 0.05, "op": janela_op(S("b09") + 0.2, E("b12") - 1.5, 1, 1.2, 1.0),
           "gangorra": [[0, 0], [tw("escorre", "b11", alt=F("b11", 2)) - 0.4, 0], [tw("escorre", "b11", alt=F("b11", 2)) + 3.5, 1.0]]}
cam(S("b09") + 0.6, [PACC[0], 1.0], 48, 20, -4, y=2.0); cam(F("b09", 2), [D0 + 12, 1.0], 30, 14, -12, y=2.4); cam(F("b09", 3) + 0.5, [D1 - 10, 1.0], 28, 14, 10, y=2.0)
cam(E("b09"), [PACC[0], 1.5], 50, 16, 0, y=3.0)
rot("ÁGUA QUENTE", [D0 + 8, 2.0], tw("quente", "b09", alt=F("b09", 0)) + 0.3, F("b11", 2), "quente", y=6.0)
rot("+50 CM (EXAGERADO)", [D0 + 3, 1.6], F("b09", 2), F("b09", 3) + 1.5, "seta", y=7.0)
rot("ÁGUA FRIA SOBE", [D1 - 5, 1.6], F("b09", 3) + 0.4, E("b10"), "fria", y=0.8)
seta("#3D6A9E", [[D1 - 10, 1.7, 0.4], [D1 - 6, 1.7, 0.8], [D1 - 3, 1.7, 2.4], [D1 - 2, 1.7, 4.0]], F("b09", 3) + 0.2, F("b09", 3) + 1.6, F("b11", 2), r=0.18)
# b10 circulação de Walker
cam(S("b10") + 0.4, [PACC[0], 4.0], 66, 14, 4, y=4.0); cam(E("b10"), [PACC[0], 4.0], 62, 16, -4, y=4.0)
for k in range(4):
    x, z = P2(124 + 7 * k, 0.5 * (k % 2))
    nuvens.append({"x": x, "z": z, "s": 2.6, "t": tw("nuvens", "b10", alt=F("b10", 0)) + 0.2 * k, "t2": E("b12"), "y": 6.6 + 0.4 * (k % 2),
                   "x2": P2(186 + 6 * k, 0.5 * (k % 2))[0], "z2": z, "tm0": tw("chuva", "b12", alt=F("b12", 0)), "tm1": tw("chuva", "b12", alt=F("b12", 0)) + 4})
WX0, WX1 = P2(128, 0)[0], P2(262, 0)[0]
t_w = tw("ar|sobe", "b10", alt=F("b10", 0))
seta("#E07A3A", [[WX0, 0, 5.4], [WX0, 0, 7.0], [WX0 + 0.5, 0, 8.6]], t_w, t_w + 1.0, F("b11", 1), r=0.3)
seta("#E07A3A", [[WX0 + 1, 0, 9.0], [PACC[0], 0, 9.4], [WX1 - 1, 0, 9.0]], t_w + 1.0, t_w + 2.6, F("b11", 1), r=0.3)
t_desce = tw("desce", "b10", alt=F("b10", 2))
seta("#4C7FB8", [[WX1, 0, 8.6], [WX1, 0, 7.2], [WX1, 0, 5.6]], t_desce, t_desce + 1.0, F("b11", 1), r=0.3)
rot("AR SOBE: NUVENS E CHUVA", [WX0 + 4, 0], t_w + 0.4, F("b11", 0), "quente", y=10.6)
rot("AR DESCE: SECO", [WX1 - 2, 0], t_desce + 0.4, F("b11", 0), "fria", y=10.0)
rot("CIRCULAÇÃO DE WALKER", [PACC[0], 0], F("b10", 3), F("b11", 0) + 0.5, "seta", y=10.8)
# b11 gangorra
cam(S("b11") + 0.3, [PACC[0], 1.5], 52, 16, 0, y=2.6); cam(F("b11", 3), [PACC[0], 1.5], 46, 14, 8, y=2.6); cam(E("b11"), [PACC[0] + 6, 1.5], 44, 18, 14, y=2.6)
num(F("b11", 1), "A CADA 2 A 7 ANOS", "OS ALÍSIOS ENFRAQUECEM")
rot("A GANGORRA", [PACC[0], 1.6], tw("gangorra", "b11", alt=F("b11", 3)) - 0.2, E("b11") + 0.5, "corredor", y=7.4)
num_off(F("b11", 3))
# b12 a chuva migra; corte para o globo
cam(S("b12") + 0.3, [PACC[0], 2.5], 50, 22, -2, y=3.0); cam(F("b12", 2) - 0.2, [PACC[0], 2.5], 56, 26, 4, y=3.0)
rot("A CHUVA VAI JUNTO", P2(196, 6), F("b12", 0) + 0.5, F("b12", 2), "quente", y=8.5)
t_glo = F("b12", 2)
cam(t_glo, GLOBO, 34, 8, 0, y=7.0, corte=True); cam(E("b12") + 0.5, GLOBO, 28, 10, 6, y=7.0)
globos.append({"img": "sat/globo-anomalia.jpg", "x": GLOBO[0], "y": 7.0, "z": GLOBO[1], "r": 7.0, "rot0": 0, "vel": 0.0,
               "op": janela_op(t_glo - 0.2, E("b12") + 0.6, 1, 0.3, 0.3), "rot": [[0, 0.87], [t_glo, 0.87], [E("b12"), -0.45]]})
trans(t_glo, "whip", 0.6, "whip pan: da maquete do Pacífico para o globo, que gira até o Brasil")
rot("BRASIL", [GLOBO[0] + 1.5, GLOBO[1] + 6.8], F("b12", 3), E("b12") + 0.4, "corredor", y=5.0)
# b13 o nome: arquivo sépia na costa do Peru
t13 = meio("b12", "b13")
trans(t13, "corte", 0.5, "corte seco para o 'arquivo' (sépia): pescadores do Peru no século 19")
tab(arquivo, t13, 0.75, 0.05); tab(arquivo, E("b13") - 0.2, 0.0, 0.6)
PC2 = P2(279.5, -6)
cam(t13, PC2, 14, 40, -10, corte=True); cam(E("b13"), PC2, 12, 38, 8)
pino("menino", "COSTA DO PERU", "SÉCULO 19", S("b13") + 0.3, t2=E("b13"), xz=PC2, y0=0.1)
foto("fotos/pesca-cabo-blanco-2024-1.jpg", S("b13") + 0.8, F("b13", 2) + 0.3, lado="dir", pino="menino")
cartao(F("b13", 2), E("b13") + 0.3, "PESCADORES DO PERU · PERTO DO NATAL", "El Niño = o Menino (Jesus)", top=320)
# b14 o retângulo Niño 3.4 + termômetro
cam(S("b14") + 0.3, P2(212, 0), 40, 52, -4); cam(E("b14"), P2(212, 0), 36, 54, 6)
n34 = retangulo(190, 240, -5, 5)
regioes.append({"anel": n34, "cor": "#E8505B", "op": janela_op(tw("retângulo|retangulo", "b14", alt=F("b14", 0)), E("b15") + 0.5, 1.0), "max": 0.55, "pulsa": True, "y": 0.15})
rot("NIÑO 3.4", P2(215, 9), tw("retângulo|retangulo", "b14", alt=F("b14", 0)) + 0.5, E("b14"), "corredor")
graficos.append({"tipo": "termometro", "t0": F("b14", 1) - 0.2, "t1": E("b14") + 0.4,
                 "faixas": [[0.5, "EL NIÑO", F("b14", 1)], [1.5, "FORTE", F("b14", 2)], [2.0, "MUITO FORTE", F("b14", 3)]], "t_super": tw("super", "b14", apos=F("b14", 4), alt=F("b14", 4) + 1.5),
                 "fonte": "NOAA/CPC · ÍNDICE OFICIAL (RONI), MÉDIA DE 3 MESES"})

# ======================= 2/4 É SUPER? (b15–b22) =======================
t_T2 = meio("b14", "b15")
trans(t_T2, "rack", 1.4, "rack focus: o termômetro desfoca e entra o Pacífico real")
tab(desfoque, t_T2 - 0.4, 1.0, 0.6); tab(desfoque, S("b15") + 0.6, 0.0, 0.8)
cx_estados += [{"t": S("b15") - 0.3, "modo": "grande", "ativa": 2, "feitas": [1], "volta": True}, {"t": E("b15") + 0.3, "modo": "compacta", "ativa": 2, "feitas": [1]}]
cam(S("b15"), PACC, 60, 58, -4, corte=True); cam(E("b15"), PACC, 58, 58, 2)
gpac = grade_xy(100, 290, -30, 30, P2)
t16a, t16b = F("b16", 1), F("b16", 5)
relevos.append({**gpac, "y0": 0.03, "k": 0.45, "mostra_data": True,
                "idx": [[0, 0], [t16a, 0], [F("b16", 2) + 1.0, 13], [t16b - 0.3, IDX_0411], [E("b16"), NDAT - 1]],
                "op": janela_op(S("b16") - 0.2, t17 if False else E("b16") + 0.3, 1, 0.6, 0.3)})
relevos.append({**gpac, "y0": 0.03, "k": 0.45, "mostra_data": False, "idx": [[0, NDAT - 1]], "op": janela_op(meio("b17", "b18") - 0.1, E("b18") + 0.6, 1, 0.3, 0.6),
                "sub": [[0, 0], [tw("desconta", "b18", alt=F("b18", 4)) - 0.2, 0], [tw("desconta", "b18", alt=F("b18", 4)) + 1.6, 0.5]]})
cam(S("b16") + 0.5, PACC, 56, 50, -6); cam(F("b16", 3), P2(210, 0), 46, 46, 0); cam(F("b16", 5), P2(262, -2), 30, 40, 16); cam(E("b16"), P2(250, 0), 40, 46, 10)
manchete(F("b16", 3) - 0.1, F("b16", 5) - 0.3, "INMET · 03/11/2026", "El Niño atinge anomalia recorde para outubro", "recorde para outubro", lado="esq")
num(F("b16", 5), "+5 °C", "COSTA DO PERU · SEMANA DE 04/11 · NOAA/CPC")
foto("fotos/enchente-norte-peru-2023-1.jpg", F("b16", 5) + 0.4, E("b16") + 0.4, lado="dir", legenda="NORTE DO PERU · CHUVAS DO EL NIÑO COSTEIRO · MAR/2023")
num_off(E("b16"))
# b17 régua de montanhas (ONI)
t17 = meio("b16", "b17")
trans(t17, "whip", 0.6, "whip pan: do Pacífico para a régua de montanhas de papel")
ANOS = [("1982-83", 2.14, 2.40), ("1997-98", 2.37, 2.28), ("2015-16", 2.59, 2.25), ("2023-24", 1.99, 1.42), ("2026", 2.46, 1.97)]
KH = 2.3
t_oni = [tw("82|oitenta", "b17", alt=F("b17", 1)), tw("97|noventa", "b17", alt=F("b17", 1) + 1.5), tw("2015|quinze", "b17", alt=F("b17", 1) + 3),
         tw("recente", "b17", alt=F("b17", 2)), F("b17", 3)]
t_roni = [tw("recorde", "b19", alt=F("b19", 1)), tw("recorde", "b19", alt=F("b19", 1)) + 0.4, tw("recorde", "b19", alt=F("b19", 1)) + 0.8,
          tw("recorde", "b19", alt=F("b19", 1)) + 1.2, F("b19", 2)]
fim_m = E("b21") + 0.6
for k, (ano, oni, roni) in enumerate(ANOS):
    x = MONT[0] + (k - 2) * 4.6
    eh26 = ano == "2026"
    h = [[0, 0], [t_oni[k] - 0.2, 0], [t_oni[k] + (2.8 if eh26 else 0.9), oni], [t_roni[k] - 0.1, oni], [t_roni[k] + (2.2 if eh26 else 0.9), roni]]
    montanhas.append({"nome": ano, "x": x, "z": MONT[1], "r": 1.55, "kh": KH, "cor": "#E8505B" if eh26 else "#DCCDB0",
                      "h": h, "op": janela_op(t17, fim_m, 1, 0.5, 0.6), "acende": [[0, 0], [t_oni[k], 1], [t_oni[k] + 1.2, 0.2]]})
cam(t17 + 0.1, [MONT[0], MONT[1]], 30, 14, -6, y=2.6, corte=True); cam(F("b17", 3), [MONT[0] + 3, MONT[1]], 26, 12, 6, y=3.0); cam(E("b17"), [MONT[0], MONT[1]], 28, 14, 0, y=3.0)
num(F("b17", 2) + 0.2, "2,46 °C", "EL NIÑO 2026 · TERMÔMETRO TRADICIONAL (ONI) · AGO–OUT · NOAA/CPC")
num(F("b17", 3) + 0.5, "2,59 °C", "O RECORDE NO ONI: 2015-16")
num_off(E("b17"))
# b18 véu do aquecimento: volta ao Pacífico
t18 = meio("b17", "b18")
trans(t18, "whip", 0.6, "whip pan: de volta ao Pacífico, que ganha um véu coral (o planeta mais quente)")
cam(t18 + 0.1, PACC, 60, 56, 4, corte=True); cam(F("b18", 3), PACC, 56, 54, -4); cam(E("b18"), PACC, 54, 56, 2)
veu = retangulo(100, 290, -20, 20)
regioes.append({"anel": veu, "cor": "#E8505B", "op": [[0, 0], [F("b18", 1), 0], [F("b18", 1) + 0.8, 1], [tw("desconta", "b18", alt=F("b18", 4)), 1], [tw("desconta", "b18", alt=F("b18", 4)) + 1.4, 0]], "max": 0.3, "y": 2.6})
rot("O PLANETA INTEIRO MAIS QUENTE", P2(205, 21), F("b18", 1) + 0.3, tw("desconta", "b18", alt=F("b18", 4)) + 0.6, "quente")
cartao(F("b18", 3) + 0.2, F("b18", 5) - 0.1, "TERMÔMETRO NOVO · NOAA, 2026", "RONI = Pacífico menos o resto dos trópicos", top=150)
rot("SÓ O QUE SOBRA: O EL NIÑO", P2(215, 9), tw("desconta", "b18", alt=F("b18", 4)) + 1.2, E("b18") + 0.4, "corredor")
# b19 (SLOT) montanhas redesenhadas com o RONI
sl0, sl1 = (SLOT["s"], SLOT["e"]) if SLOT else (S("b19"), E("b21"))
trans(sl0 - 0.35, "whip", 0.6, "whip pan: de volta à régua; as montanhas se redesenham com o termômetro novo (RONI)")
cam(sl0 - 0.3, [MONT[0], MONT[1]], 34, 14, 4, y=3.0, corte=True); cam(F("b19", 2), [MONT[0] + 3, MONT[1]], 31, 12, 8, y=2.8); cam(E("b19"), [MONT[0], MONT[1]], 33, 15, -2, y=2.8)
barras3d.append({"x0": MONT[0] - 11.5, "x1": MONT[0] + 11.5, "z": MONT[1], "y": 2.40 * KH, "cor": "#E8505B", "op": janela_op(F("b19", 1) + 0.6, fim_m, 1, 0.6, 0.6)})
barras3d.append({"x0": MONT[0] - 11.5, "x1": MONT[0] + 11.5, "z": MONT[1], "y": 2.5 * KH, "cor": "#1F2A44", "op": janela_op(S("b20") + 0.2, fim_m, 1, 0.6, 0.6)})
rot("RECORDE NO RONI: 2,40 (1982-83)", [MONT[0] + 13.5, MONT[1]], F("b19", 1) + 0.8, fim_m, "corredor", y=2.40 * KH)
rot("\"HISTÓRICO\": 2,5", [MONT[0] - 9.0, MONT[1]], S("b20") + 0.4, fim_m, "seta", y=2.5 * KH + 0.2)
num(F("b19", 2) + 0.2, "2,0 °C", "EL NIÑO 2026 · ÍNDICE OFICIAL (RONI) · AGO–OUT · NOAA/CPC")
num(F("b19", 3) + 0.2, "MUITO FORTE", "JÁ PASSOU O DE 2023-24 · AINDA NÃO É O MAIOR")
num_off(E("b19"))
# b20 (SLOT) mostrador + 27 modelos
graficos.append({"tipo": "mostrador", "t0": F("b20", 2) - 0.2, "t1": F("b20", 3) + 0.2, "de": 70, "ate": 83, "t_gira": F("b20", 2) + 0.3,
                 "titulo": "CHANCE DE SER O MAIS FORTE DESDE 1950", "fonte": "NOAA/CPC · BOLETIM DE 08/10/2026 · OUT–DEZ E NOV–JAN"})
graficos.append({"tipo": "modelos", "t0": F("b20", 3), "t1": E("b20") + 0.4, "n": 27, "t_acende": F("b20", 3) + 0.4,
                 "titulo": "27 DE 27 MODELOS: MUITO FORTE ATÉ FEVEREIRO", "fonte": "IRI · UNIVERSIDADE COLUMBIA · 19/10/2026"})
# b21 (SLOT) carimbo
manchete(S("b21") + 0.6, F("b21", 3) - 0.1, "CARBON BRIEF · 06/11/2026", "“Super El Niño” em desenvolvimento rápido deve chegar ao pico em dezembro", "“Super El Niño”", lado="dir")
cartao(F("b21", 3) - 0.1, sl1 - 0.2, "É SUPER?", "“Super” é apelido. Termo oficial:", carimbo="MUITO FORTE", t_carimbo=F("b21", 4), top=300)
cam(S("b21") + 0.3, [MONT[0], MONT[1]], 34, 16, 6, y=3.0); cam(sl1, [MONT[0], MONT[1]], 36, 18, 0, y=3.0)
# b22 não é causado pelo aquecimento
t22 = meio("b21", "b22")
trans(t22, "rack", 1.2, "rack focus: da régua para o Pacífico de hoje, com a prancha do que a ciência diz")
tab(desfoque, t22 - 0.3, 0.6, 0.5); tab(desfoque, E("b22"), 0.0, 0.6)
cam(t22 + 0.1, PACC, 58, 58, -6, corte=True); cam(E("b22"), PACC, 56, 58, 4)
relevos.append({**gpac, "y0": 0.03, "k": 0.45, "idx": [[0, NDAT - 1]], "op": janela_op(t22, E("b22") + 0.5, 1, 0.4, 0.6), "mostra_data": False})
graficos.append({"tipo": "ciencia", "t0": S("b22") + 0.3, "t1": E("b22") + 0.4, "fonte": "NOAA CLIMATE.GOV · OMM", "itens": [
    ["O EL NIÑO É CAUSADO PELO AQUECIMENTO GLOBAL", False, F("b22", 1)], ["ELE EXISTE HÁ MILHARES DE ANOS (CORAIS: ~7 MIL ANOS)", True, F("b22", 2)],
    ["AGORA ACONTECE NUM PLANETA MAIS QUENTE", True, F("b22", 3)]]})

# ======================= 3/4 MINHA REGIÃO (b23–b38) =======================
t_T3 = meio("b22", "b23")
trans(t_T3, "orbital", 1.4, "zoom-out orbital: do Pacífico para a América do Sul inteira")
cx_estados += [{"t": S("b23") - 0.3, "modo": "grande", "ativa": 3, "feitas": [1, 2], "volta": True}, {"t": E("b23") + 0.3, "modo": "compacta", "ativa": 3, "feitas": [1, 2]}]
cam(t_T3 + 0.3, P(-70, -12), 90, 66, 30, corte=True); cam(E("b23"), CONT, 74, 64, 6)
# b24 ar descendo sobre a Amazônia; jato subtropical segura as frentes no Sul
cam(S("b24") + 0.5, CONT, 72, 62, -4); cam(F("b24", 3), P(-56, -24), 54, 58, 4); cam(E("b24"), P(-56, -24), 52, 58, 8)
AMZ = P(-62, -5)
for k, ll in enumerate([(-64, -4), (-59, -6), (-55, -3), (-67, -7)]):
    x, z = P(*ll); nuvens.append({"x": x, "z": z, "s": 2.4, "t": S("b24") + 0.3 + 0.2 * k, "t2": tw("forma", "b24", alt=F("b24", 2)), "y": 2.0})
t_desc = tw("descer", "b24", alt=F("b24", 1))
for ll in [(-62, -5), (-48, -6)]:
    x, z = P(*ll); seta("#4C7FB8", [[x, z, 9.0], [x, z, 6.0], [x, z, 2.4]], t_desc, t_desc + 1.2, F("b24", 4), r=0.7)
rot("AR DESCE: MENOS CHUVA", off(AMZ, 8, -2), t_desc + 0.6, F("b24", 4), "fria", y=6)
jato = [P(*q) for q in [(-72, -31), (-64, -30), (-56, -28.5), (-48, -27.5), (-40, -27.5)]]
t_jato = tw("jato", "b24", alt=F("b24", 4))
seta("#E07A3A", [q + [3.0] for q in jato], t_jato, t_jato + 2.0, E("b25"), r=0.55, fluxo=True, vel=0.14)
rot("JATO SUBTROPICAL", P(-60, -33), t_jato + 0.5, E("b24") + 0.5, "quente", y=3.0)
seta("#4C7FB8", [P(*q) + [1.2] for q in [(-66, -42), (-61, -37), (-57, -33), (-54, -30.5)]], t_jato + 1.0, t_jato + 2.6, E("b24") + 0.8, r=0.45)
rot("MAIS CHUVA", P(-50, -30), F("b24", 5), E("b24") + 0.6, "fria")
for k, ll in enumerate([(-53.5, -27.0), (-51.0, -26.2), (-55.0, -29.2), (-50.0, -29.0)]):
    x, z = P(*ll); nuvens.append({"x": x, "z": z, "s": 1.8, "t": F("b24", 5) + 0.3 * k, "t2": E("b24") + 1.0, "y": 1.6})
# b25 o Brasil pinta por cor (previsão nov–jan)
cam(S("b25") + 0.4, BR, 88, 74, -4); cam(E("b25"), BR, 86, 76, 4)
NNE = ["11", "12", "13", "14", "15", "16", "17", "21", "22", "23", "24", "25", "26", "27", "28", "29"]
SULU = ["41", "42", "43"]; CSUL = ["31", "32", "33", "35", "50", "51", "52", "53"]
t_s, t_n, t_c = tw("Chuva", "b25", apos=F("b25", 3), alt=F("b25", 3)), F("b25", 4), F("b25", 5)
tintas.append({"ufs": SULU, "cor": "#5B86B8", "op": janela_op(t_s, E("b25") + 0.5, 1, 0.6, 0.8)})
tintas.append({"ufs": NNE, "cor": "#D9894A", "op": janela_op(t_n, E("b25") + 0.5, 1, 0.6, 0.8), "max": 0.75})
tintas.append({"ufs": CSUL, "cor": "#E8806E", "op": janela_op(t_c, E("b25") + 0.5, 1, 0.6, 0.8), "max": 0.6})
graficos.append({"tipo": "legenda", "t0": F("b25", 1), "t1": E("b25") + 0.5, "titulo": "PREVISÃO NOV–JAN", "fonte": "PAINEL EL NIÑO · BOLETIM Nº 05 · OUT/2026",
                 "itens": [["#5B86B8", "SUL: CHUVA ACIMA DA MÉDIA", t_s], ["#D9894A", "NORTE E NORDESTE: CHUVA ABAIXO", t_n], ["#E8806E", "QUASE TODO O PAÍS: MAIS CALOR", t_c]]})
num(F("b25", 1) + 0.3, "7 ÓRGÃOS", "INMET · INPE · ANA · CEMADEN · SGB · SEDEC · CENSIPAM")
num_off(F("b25", 3))
# NORTE b26 rio Branco em Boa Vista
cam(S("b26"), off(BV, 0, 1.0), 14, 50, -6, corte=True); cam(E("b26"), BV, 11, 46, 6)
t_T4n = S("b26") - 0.3
trans(t_T4n, "whip_v", 0.6, "whip pan vertical: do Brasil inteiro para Roraima")
pino("bv", "BOA VISTA · RR", "RIO BRANCO · 04/09/2026", tw("Boa", "b26", alt=F("b26", 1)), t2=E("b26") + 0.3, cid="BOA VISTA")
foto("sat/boavista-rio-branco-2025-09-21.jpg", F("b26", 1) - 0.1, E("b26") + 0.4, lado="esq", legenda="RIO BRANCO · BOA VISTA · 21/09/2025",
     credito="IMAGEM: NASA HLS · CONTÉM DADOS COPERNICUS SENTINEL MODIFICADOS [2025]")
foto("sat/boavista-rio-branco-2026-09-16.jpg", F("b26", 1) + 0.9, E("b26") + 0.4, lado="dir", legenda="RIO BRANCO · BOA VISTA · 16/09/2026",
     credito="IMAGEM: NASA HLS · CONTÉM DADOS COPERNICUS SENTINEL MODIFICADOS [2026]")
num(tw("mínimos|minimos", "b26", alt=F("b26", 1) + 2), "1,24 M", "RIO BRANCO · 04/09 · ABAIXO DO MÍNIMO PARA A ÉPOCA · SGB")
num_off(E("b26"))
# b27 focos de calor no Amazonas
cam(S("b27") + 0.2, off(MAN, -2, -1), 26, 58, -4); cam(E("b27"), off(MAN, 0, 0), 20, 52, 6)
am = next(v["anel"] for v in geo["vizinhos"] if v["nome"] == "13")
def dentro(pt, anel):
    x, z = pt; c = False
    for i in range(len(anel)):
        x1, z1 = anel[i - 1]; x2, z2 = anel[i]
        if (z1 > z) != (z2 > z) and x < (x2 - x1) * (z - z1) / (z2 - z1 + 1e-12) + x1: c = not c
    return c
xs_am = [p[0] for p in am]; zs_am = [p[1] for p in am]
pts_am, k = [], 0
while len(pts_am) < 124 and k < 20000:
    u = (math.sin(k * 12.9898) * 43758.5453) % 1; v = (math.sin(k * 78.233 + 1.3) * 12345.6789) % 1; k += 1
    q = [min(xs_am) + u * (max(xs_am) - min(xs_am)), min(zs_am) + v * (max(zs_am) - min(zs_am))]
    if dentro(q, am): pts_am.append([round(q[0], 3), round(q[1], 3)])
t_focos = F("b27", 0) + 0.8
pontos.append({"lista": pts_am, "t0": t_focos, "t1": F("b27", 1) + 1.5, "t2": E("b27") + 0.3})
rot("FOCOS DE CALOR NO AM · SET/2026 (POSIÇÕES ILUSTRATIVAS)", off(MAN, -2, 6), t_focos + 0.3, E("b27"), "quente")
num(F("b27", 1), de=942, para=3726, dur=1.6, faixa="FOCOS DE QUEIMADA NO AMAZONAS · SET/2025 → SET/2026 · INPE")
foto("fotos/queimada-apui-2020-1.jpg", F("b27", 0) + 1.2, F("b27", 2) - 0.2, lado="dir")
fumacas.append({"x": MAN[0] + 0.3, "z": MAN[1] - 0.2, "t0": F("b27", 2) - 0.3, "t1": E("b27"), "r": 0.7, "h": 3.0, "s": 0.75, "n": 70, "vento": 1.6})
num_off(E("b27"))
# b28 rio Negro (régua) e o norte da Amazônia
cam(S("b28") + 0.2, MAN, 11, 40, -8); cam(F("b28", 2) + 1, MAN, 9.5, 34, 6)
pino("man28", "MANAUS · RIO NEGRO", "05/11/2026", S("b28") + 0.4, t2=F("b28", 3) + 0.2, cid="MANAUS", y0=0.1)
t_rn = F("b28", 2)
cilindros.append({"x": MAN[0] + 1.2, "z": MAN[1] + 0.3, "y": 0.1, "r": 0.34, "h": 2.6, "cor": "#3D6A9E", "op": janela_op(t_rn - 0.3, F("b28", 3) + 0.3, 1, 0.4, 0.5),
                  "nivel": [[0, 0], [t_rn, 0], [t_rn + 1.2, 16.43 / 20]], "marca": 12.16 / 20, "t_marca": t_rn + 1.4})
rot("2024: 12,2 M", [MAN[0] + 2.4, MAN[1] + 0.3], t_rn + 1.4, F("b28", 3) + 0.2, "seta", y=0.1 + 2.6 * 12.16 / 20)
rot("HOJE: 16,4 M", [MAN[0] + 2.4, MAN[1] + 0.3], t_rn + 1.0, F("b28", 3) + 0.2, "fria", y=0.1 + 2.6 * 16.43 / 20 + 0.25)
num(t_rn + 0.4, "+4 M", "RIO NEGRO EM MANAUS · 05/11 · 2024: 12,2 M · 2026: 16,4 M · ANA")
foto("fotos/seca-manaus-2023-1.jpg", F("b28", 1) - 0.2, F("b28", 2) - 0.1, lado="dir", legenda="MANAUS · A SECA DO RIO NEGRO · 2023")
num_off(F("b28", 3))
cam(F("b28", 3) + 0.4, P(-58, 0), 42, 60, -4); cam(E("b28"), P(-58, 0), 40, 60, 6)
tintas.append({"ufs": ["14", "16"], "cor": "#E8505B", "op": janela_op(F("b28", 4) - 0.2, E("b28") + 0.4, 1, 0.5, 0.6), "max": 0.7})
rot("RORAIMA", P(-61.3, 2.0), F("b28", 4), E("b28"), "corredor"); rot("AMAPÁ", P(-52, 1.3), F("b28", 4) + 0.4, E("b28"), "corredor")
rot("ALTO RIO NEGRO", P(-67.5, -0.5), F("b28", 4) + 0.8, E("b28"), "corredor")
num(F("b28", 5), "DEZ → ABR", "O PIOR PERÍODO DE FOGO EM RORAIMA · PAINEL EL NIÑO")
num_off(E("b28") + 0.2)
# NORDESTE b29
t_T4 = meio("b28", "b29")
trans(t_T4, "whip", 0.6, "whip pan para o semiárido")
NE = P(-40.5, -8.5)
cam(t_T4 + 0.25, NE, 34, 56, -6, corte=True); cam(E("b29"), NE, 30, 54, 8)
for r_ in geo["secas"]["08"]:
    regioes.append({"anel": r_, "cor": "#C9612A", "op": [[0, 0], [S("b29") + 0.4, 0], [S("b29") + 1.0, 1], [F("b29", 1) + 1.6, 1], [F("b29", 1) + 2.4, 0]], "max": 0.55, "y": 0.2})
for r_ in geo["secas"]["09"]:
    regioes.append({"anel": r_, "cor": "#B8323D", "op": janela_op(F("b29", 1) + 1.6, E("b29") + 0.3, 1, 0.8, 0.6), "max": 0.55, "y": 0.21})
rot("SECA GRAVE · AGO/2026", P(-40, -4.5), S("b29") + 0.8, F("b29", 1) + 1.8, "quente")
rot("SECA GRAVE · SET/2026", P(-40, -4.5), F("b29", 1) + 2.0, E("b29"), "corredor")
num(F("b29", 1) + 0.3, "16% → 28%", "DO NORDESTE EM SECA GRAVE · AGO → SET · MONITOR DE SECAS (ANA)")
num(F("b29", 2), de=4, para=68, dur=1.4, faixa="MUNICÍPIOS EM SECA EXTREMA NO PAÍS · EM 2 MESES · PAINEL EL NIÑO")
foto("fotos/seca-santa-quiteria-2016-1.jpg", F("b29", 2) + 0.6, E("b29") + 0.4, lado="esq", legenda="SANTA QUITÉRIA (CE) · AÇUDE SECO · FEV/2016 (EL NIÑO 2015-16)")
num_off(E("b29"))
# CENTRO-OESTE E SUDESTE b30–b31
CS = P(-47, -19)
cam(S("b30") - 0.2, CS, 40, 58, -6, corte=True); cam(E("b30"), CS, 36, 56, 6)
trans(S("b30") - 0.45, "whip", 0.6, "whip pan para o Centro-Sul")
tab(quente, S("b30") + 0.3, 0.7, 1.0); tab(quente, E("b30") + 0.2, 0.0, 1.0)
tintas.append({"ufs": ["50", "51", "52", "53", "31", "35", "32", "33"], "cor": "#E8806E", "op": janela_op(S("b30") + 0.4, F("b30", 3), 1, 0.6, 0.6), "max": 0.55})
tintas.append({"ufs": ["35", "50"], "cor": "#5B86B8", "op": janela_op(F("b30", 3), F("b30", 5), 1, 0.6, 0.6), "max": 0.7})
rot("CHUVA ACIMA: SP · TRIÂNGULO MINEIRO · MS", P(-50.5, -22.8), F("b30", 3), F("b30", 5), "fria")
rot("ABAIXO: NORTE DE MG E DO ES", P(-42.5, -16.0), F("b30", 4), F("b30", 5) + 0.5, "quente")
num(F("b30", 0) + 0.8, "CALOR", "ACIMA DO NORMAL NO VERÃO · CENTRO-OESTE E SUDESTE · PAINEL EL NIÑO")
num_off(F("b30", 3))
doce = [P(*q) + [0.16] for q in [(-43.1, -20.4), (-42.6, -19.6), (-41.95, -19.4), (-40.9, -19.45), (-39.85, -19.6)]]
paraiba = [P(*q) + [0.16] for q in [(-45.6, -23.35), (-45.4, -23.0), (-44.9, -22.75), (-44.1, -22.5), (-43.2, -22.15), (-42.3, -21.85), (-41.3, -21.75), (-41.05, -21.6)]]
t_rios = F("b30", 5)
seta("#2F527E", doce, t_rios, t_rios + 1.4, E("b30") + 0.5, r=0.12, semCabeca=True)
seta("#2F527E", paraiba, t_rios + 0.4, t_rios + 1.8, E("b30") + 0.5, r=0.12, semCabeca=True)
cam(t_rios, P(-42.5, -21), 16, 54, -4); cam(E("b30") + 0.3, P(-42.5, -21), 15, 52, 6)
rot("RIO DOCE", P(-41.0, -18.8), t_rios + 0.8, E("b30") + 0.3, "fria"); rot("RIO PARAÍBA DO SUL", P(-43.0, -23.1), t_rios + 1.0, E("b30") + 0.3, "fria")
num(t_rios + 0.4, "JANEIRO", "RISCO DE CHEIA NOS RIOS DOCE E PARAÍBA DO SUL · PAINEL EL NIÑO")
num_off(E("b30") + 0.3)
cam(S("b31") + 0.4, P(-48, -20), 30, 50, -6); cam(E("b31"), P(-48, -20), 28, 48, 6)
t_res = tw("reservatórios|reservatorios", "b31", alt=F("b31", 2))
for k, ll in enumerate([(-51.0, -20.2), (-47.6, -21.6), (-45.2, -17.6), (-49.6, -18.0)]):
    x, z = P(*ll)
    cilindros.append({"x": x, "z": z, "y": 0.1, "r": 0.95, "h": 3.4, "cor": "#5B86B8", "op": janela_op(t_res - 0.4 + 0.15 * k, E("b31") + 0.3, 1, 0.4, 0.5),
                      "nivel": [[0, 0], [t_res + 0.1 * k, 0], [t_res + 1.5 + 0.1 * k, 0.659]]})
num(t_res + 0.3, "65,9%", "RESERVATÓRIOS DAS HIDRELÉTRICAS · OUTUBRO · 2º MAIOR PARA A DATA DESDE 2015 · PAINEL EL NIÑO")
num_off(E("b31") + 0.2)
# SUL b32–b37
t_T5 = meio("b31", "b32")
trans(t_T5, "luz", 1.4, "a luz escurece (céu de chuva) enquanto a câmera desce para o Sul")
tab(luz, t_T5 - 0.3, 0.62, 1.2); tab(luz, E("b35") + 0.3, 1.0, 1.0)
TAQ = C["LAJEADO"]
cam(t_T5 + 0.5, SUL, 20, 58, -6); cam(F("b32", 1) + 0.3, off(TAQ, 0, -0.3), 8.5, 46, -6); cam(F("b32", 2), off(TAQ, 0.1, -0.2), 8.0, 44, 6)
taquari = [P(*q) + [0.36] for q in [(-50.9, -28.75), (-51.5, -28.95), (-51.88, -29.15), (-51.96, -29.45), (-51.85, -29.75), (-51.72, -29.95)]]
seta("#2F527E", taquari, F("b32", 1), F("b32", 1) + 1.4, F("b32", 3), r=0.06, semCabeca=True)
rot("RIO TAQUARI", P(-51.2, -28.65), F("b32", 1) + 0.5, F("b32", 3), "fria")
for k, (nm, w) in enumerate([("MUÇUM", "Muçum|Mussum|Muçu"), ("ENCANTADO", "Encant"), ("ESTRELA", "Estrel"), ("LAJEADO", "Lajea|Lagia|Lajia")]): dest(nm, tw(w, "b32", alt=F("b32", 1) + 1 + 0.5 * k), t2=F("b32", 3))
foto("fotos/enchente-mucum-2023-1.jpg", F("b32", 1) + 0.8, F("b32", 2) + 0.2, lado="dir", legenda="MUÇUM (RS) · ENCHENTE DO TAQUARI · SET/2023")
cam(F("b32", 2) + 0.4, P(-52.5, -26.3), 16, 52, -6)
for k, ll in enumerate([(-53.6, -26.4), (-52.4, -25.6), (-53.0, -27.0), (-51.6, -25.3)]):
    x, z = P(*ll)
    nuvens.append({"x": x, "z": z, "s": 1.3, "t": F("b32", 2) + 0.2 * k, "t2": F("b32", 3) + 0.5, "y": 2.4})
    chuvas.append({"x": x, "z": z, "t0": F("b32", 2) + 0.3 + 0.2 * k, "t1": F("b32", 3) + 0.4, "r": 0.8, "h": 2.2, "n": 50})
num(F("b32", 2) + 0.3, "RECORDE", "CHUVA DE OUTUBRO NO SUL · INMET")
cam(F("b32", 3), SUL, 19, 60, -4); cam(E("b32"), SUL, 18, 60, 6)
todos = ["MARINGÁ", "CHAPECÓ", "XANXERÊ", "RIO NEGRINHO", "ERVAL GRANDE", "SANTO AUGUSTO", "PALMEIRA DAS MISSÕES"]
for k, cid in enumerate(todos): pino(f"t{k}", cid, "", F("b32", 3) + 0.3 + 0.25 * k, pequeno=True, t2=E("b32") + 0.4, cid=cid)
num(F("b32", 3) + 0.3, de=0, para=7, dur=1.8, unidade="tornados", faixa="2 A 7/11 · SIMEPAR + DEFESAS CIVIS (LEVANTAMENTO CLIMATEMPO)")
num_off(E("b32") + 0.3)
cam(S("b33"), SUL, 18, 62, -6); cam(E("b33"), SUL, 17, 62, 4)
tintas.append({"ufs": ["42", "43"], "cor": "#E8505B", "op": janela_op(S("b33") + 0.3, E("b33") + 0.4, 1, 0.5, 0.6), "max": 0.55})
num(tw("260|duzentos", "b33", alt=S("b33") + 2), de=0, para=262, dur=1.6, unidade="municípios", faixa="ATINGIDOS DE 1º A 6/11 · DEFESAS CIVIS RS (136) E SC (126)")
foto("sat/sul-tempestade-2026-11-04-terra.jpg", S("b33") + 0.4, E("b33") + 0.5, lado="dir", legenda="SUL DO BRASIL · 04/11/2026 · TEMPESTADES", credito="IMAGEM: NASA MODIS TERRA (GIBS) · DOMÍNIO PÚBLICO")
num_off(E("b33") + 0.3)
graficos.append({"tipo": "ciencia", "t0": S("b34") + 0.2, "t1": F("b34", 3) - 0.1, "fonte": "CLIMATEMPO · PAINEL EL NIÑO", "itens": [
    ["O EL NIÑO CAUSA CADA TEMPESTADE", False, S("b34") + 0.3], ["ELE AUMENTA AS CHANCES", True, F("b34", 1)], ["MAIS CHUVA · SOLO ENCHARCADO · RIOS CHEIOS", True, F("b34", 2)]]})
foto("img/thumb-video1.jpg", F("b34", 3), E("b34") + 0.6, lado="dir", legenda="ASSISTA: 7 TORNADOS EM 6 DIAS", credito="EM RELEVO · O VÍDEO ANTERIOR")
cam(S("b35"), off(C["PORTO ALEGRE"], -1.2, -1.0), 22, 60, -6); cam(E("b35"), off(C["PORTO ALEGRE"], -1.2, -1.0), 21, 60, 6)
tintas.append({"ufs": ["43"], "cor": "#9CC3E4", "op": janela_op(F("b35", 1), E("b35") + 0.3, 1, 0.6, 0.6), "max": 0.9})
num(F("b35", 1) + 0.3, "ABAIXO DO NORMAL", "TEMPERATURA NO RIO GRANDE DO SUL · NOV–JAN · PAINEL EL NIÑO")
num_off(E("b35") + 0.3)
# b36 arquivo 1983
t36 = meio("b35", "b36")
trans(t36, "corte", 0.5, "corte seco no impacto para o 'arquivo' (sépia): a enchente de 1983")
tab(tremor, t36, 1.0, 0.05); tab(tremor, t36 + 0.3, 0.0, 0.5)
tab(arquivo, t36, 0.85, 0.05); tab(arquivo, E("b36") - 0.1, 0.0, 0.7)
UV, BLU = C["UNIÃO DA VITÓRIA"], C["BLUMENAU"]
cam(t36, off(UV, 0, 0.2), 9, 44, -10, corte=True); cam(F("b36", 3) - 0.3, off(UV, 0.4, 0.1), 9.5, 46, 6)
pino("uv", "UNIÃO DA VITÓRIA · PR", "JULHO DE 1983", tw("União|Uniao", "b36", alt=F("b36", 2)), t2=F("b36", 4), cid="UNIÃO DA VITÓRIA", cor="#1F2A44")
dest("UNIÃO DA VITÓRIA", tw("União|Uniao", "b36", alt=F("b36", 2)) + 0.2, t2=F("b36", 4), cor="#B98B5A")
t_ig = F("b36", 3)
cilindros.append({"x": UV[0] + 0.9, "z": UV[1] + 0.2, "r": 0.3, "h": 2.4, "cor": "#5E6E7E", "op": janela_op(t_ig - 0.4, F("b36", 4) + 0.2, 1, 0.4, 0.5),
                  "nivel": [[0, 2.5 / 12], [t_ig, 2.5 / 12], [t_ig + 1.6, 10.42 / 12]]})
num(t_ig, de=2.5, para=10.42, dur=1.6, unidade="m", faixa="RIO IGUAÇU · UNIÃO DA VITÓRIA · 1983 · DEFESA CIVIL DO PR", dec=2)
num(F("b36", 4), "18", "MORTES · ENCHENTE DE 1983 NO PARANÁ · DEFESA CIVIL DO PR", unidade="mortes")
cam(F("b36", 5) - 0.2, off(BLU, 0, 0.2), 9, 44, -6); cam(E("b36") + 0.3, BLU, 8.5, 42, 6)
pino("blu", "BLUMENAU · SC", "09/07/1983", F("b36", 5), t2=E("b36") + 0.3, cid="BLUMENAU", cor="#1F2A44")
dest("BLUMENAU", F("b36", 5) + 0.2, t2=E("b36") + 0.3, cor="#B98B5A")
num(F("b36", 5) + 0.3, "15,34 M", "ITAJAÍ-AÇU EM BLUMENAU · 09/07/1983 · DEFESA CIVIL DE BLUMENAU")
num_off(E("b36") + 0.3)
# b37 enchente de 2024
t37 = meio("b36", "b37")
trans(t37, "corte", 0.5, "corte seco de volta ao mapa colorido: a enchente de 2024")
POA = C["PORTO ALEGRE"]
cam(t37, off(POA, -0.6, -0.6), 12, 52, -6, corte=True); cam(E("b37"), off(POA, -0.4, -0.4), 11, 50, 6)
regioes.append({"anel": anel_elipse((-51.5, -29.75), 20, 1.0, 0.45, 40), "cor": "#3D6A9E", "op": janela_op(S("b37") + 0.3, E("b37") + 0.3, 1.0), "max": 0.55, "pulsa": True})
rot("ENCHENTE · MAIO/2024", P(-51.2, -29.0), S("b37") + 0.6, F("b37", 1) + 0.5, "fria")
foto("fotos/enchente-rmpa-2024-1.jpg", S("b37") + 0.5, F("b37", 2) - 0.1, lado="dir")
rot("EL NIÑO + AQUECIMENTO · WWA", P(-53.0, -30.8), F("b37", 1), E("b37") + 0.3, "corredor")
num(F("b37", 2), "MAIO/2024", "O EL NIÑO JÁ ESTAVA PERDENDO FORÇA")
foto("fotos/enchente-rmpa-2024-2.jpg", F("b37", 2) + 0.2, E("b37") + 0.4, lado="esq")
num_off(E("b37") + 0.3)
# O MUNDO b38 globo
t38 = meio("b37", "b38")
trans(t38, "orbital", 1.4, "zoom-out orbital até o globo inteiro, com o mar quente")
cam(t38 + 0.2, GLOBO, 36, 12, -10, y=7.0, corte=True); cam(E("b38"), GLOBO, 30, 10, 8, y=7.0)
globos.append({"img": "sat/globo-anomalia.jpg", "x": GLOBO[0], "y": 7.0, "z": GLOBO[1], "r": 7.0, "rot0": 0, "vel": 0.0,
               "op": janela_op(t38, E("b38") + 0.6, 1, 0.4, 0.4), "rot": [[0, 0.9], [t38, 0.9], [E("b38"), -1.3]]})
rot("DADOS: NOAA OISST · 08/11/2026", [GLOBO[0], GLOBO[1] + 7.5], t38 + 0.8, E("b38"), "mapa", y=0.3)
num(F("b38", 2), "OUTUBRO MAIS QUENTE", "OUT/2026 · +1,75 °C ACIMA DO PRÉ-INDUSTRIAL · COPERNICUS")
num(F("b38", 3) + 0.3, "96%", "CHANCE DE 2027 SER O ANO MAIS QUENTE · CARBON BRIEF")
foto("fotos/coral-florida-2023-1.jpg", F("b38", 1) - 0.2, F("b38", 3) - 0.2, lado="esq", legenda="MAR QUENTE: CORAL BRANQUEADO · FLÓRIDA (EUA) · JUL/2023")
num_off(E("b38") + 0.3)

# ======================= 4/4 ATÉ QUANDO (b39–b43) =======================
t_T6 = meio("b38", "b39")
trans(t_T6, "match", 1.2, "match cut: o globo vira o disco do calendário")
cx_estados += [{"t": S("b39") - 0.3, "modo": "grande", "ativa": 4, "feitas": [1, 2, 3], "volta": True}, {"t": E("b39") + 0.3, "modo": "compacta", "ativa": 4, "feitas": [1, 2, 3]}]
cam(t_T6 + 0.05, PACC, 64, 60, -6, corte=True); cam(E("b41"), PACC, 60, 58, 4)
relevos.append({**gpac, "y0": 0.03, "k": 0.45, "idx": [[0, NDAT - 1]], "op": janela_op(t_T6, E("b42") + 0.4, 1, 0.5, 0.6), "mostra_data": False,
                "cresce": [[0, 1], [F("b41", 0), 1], [F("b41", 2) + 1.5, 0.35], [F("b42", 1), 0.35], [F("b42", 2) + 1.5, 0.0]]})
TRI = ["OND", "NDJ", "DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ"]
graficos.append({"tipo": "prob", "t0": S("b40") + 0.2, "t1": E("b41") + 0.5, "tri": TRI, "titulo": "PROBABILIDADE POR TRIMESTRE", "fonte": "NOAA/CPC · OUT/2026",
                 "barras": [{"i": i, "v": v, "cor": "#E8505B", "t": S("b40") + 0.6 + 0.25 * i} for i, v in enumerate([100, 96, 81, 46])] +
                           [{"i": 6, "v": 54, "cor": "#7FA6C9", "t": F("b41", 2)}, {"i": 7, "v": 70, "cor": "#7FA6C9", "t": F("b41", 2) + 0.3}],
                 "legendas": [["#E8505B", "EL NIÑO MUITO FORTE", S("b40") + 0.6], ["#7FA6C9", "PACÍFICO NEUTRO", F("b41", 2)]],
                 "hoje": {"i": 0, "t": S("b40") + 0.4, "texto": "ESTAMOS AQUI"}, "pico": {"de": 0.5, "ate": 1.7, "t": F("b40", 0) + 0.8, "texto": "PICO: DEZ–JAN"}})
rot("LA NIÑA?", P2(220, 0), F("b42", 2), E("b42"), "fria")
regioes.append({"anel": retangulo(160, 280, -6, 6), "cor": "#3D6A9E", "op": janela_op(F("b42", 2), E("b42"), 1.0, 1.0, 0.6), "max": 0.4, "y": 0.6})
graficos.append({"tipo": "depois", "t0": F("b42", 1) - 0.2, "t1": F("b42", 4) + 0.3, "titulo": "O ANO SEGUINTE (ONI, °C)", "fonte": "NOAA/CPC",
                 "itens": [["1983", -0.96, F("b42", 1) + 0.3], ["1998", -1.47, F("b42", 1) + 0.7], ["2016", -0.51, F("b42", 1) + 1.1]]})
t43 = meio("b42", "b43")
trans(t43, "whip", 0.6, "whip pan de volta ao Brasil")
cam(t43 + 0.25, BR, 66, 66, -4, corte=True); cam(E("b43"), BR, 64, 66, 4)
cartao(S("b43") + 0.4, E("b43") + 0.3, "PAINEL EL NIÑO · OUT/2026", "Os efeitos podem continuar depois do pico.", top=300)

# ======================= O QUE FAZER (b44–b46): quadro de cortiça =======================
t_T9 = meio("b43", "b44")
trans(t_T9, "corte", 0.6, "corte para o quadro de cortiça (o 3D sai de cena)")
cx_estados.append({"t": t_T9, "modo": "oculto"})
cortica = {"t0": t_T9, "t1": S("b47") - 0.2, "itens": []}
def it(tipo, t, x, y, w, rot_, **kw): cortica["itens"].append({"tipo": tipo, "t": round(t, 3), "x": x, "y": y, "w": w, "rot": rot_, **kw})
it("titulo", t_T9 + 0.3, 640, 60, 640, -1, texto="O QUE FAZER")
it("postit", S("b45") - 0.1, 110, 230, 340, -4, cor="#9AD1D4", titulo="NO SUL", texto="alertas da Defesa Civil\nSMS: seu CEP\npara 40199 (grátis)")
it("celular", F("b45", 1), 490, 210, 270, 3, texto="DEFESA CIVIL ALERTA\nAlerta de temporal na sua região. Fique longe de rios, encostas e árvores.")
it("postit", F("b45", 2), 110, 640, 340, 3, cor="#F4D35E", titulo="TEMPORAL", texto="longe de rios,\nencostas e árvores")
it("fotoimg", F("b45", 2) + 0.4, 820, 560, 380, -3, src="fotos/enchente-rio-do-sul-2023-1.jpg", legenda=FOTOS["enchente-rio-do-sul-2023-1.jpg"]["legenda_tela"], credito=FOTOS["enchente-rio-do-sul-2023-1.jpg"]["credito_tela"])
it("postit", S("b46") - 0.1, 1180, 200, 330, 2, cor="#F7C59F", titulo="FUMAÇA", texto="portas e janelas\nfechadas\nmáscara PFF2")
it("fotoimg", S("b46") + 0.6, 1530, 190, 340, 4, src="fotos/fumaca-brasilia-2024-1.jpg", legenda=FOTOS["fumaca-brasilia-2024-1.jpg"]["legenda_tela"], credito=FOTOS["fumaca-brasilia-2024-1.jpg"]["credito_tela"])
it("postit", F("b46", 1), 1300, 600, 360, -3, cor="#B8E0A0", titulo="CALOR", texto="água mesmo sem sede\nfuja do sol forte\nidosos e crianças")
cobre3d = [[t_T9 + 0.6, S("b47") - 1.0]]
t_T10 = S("b47") - 0.6
trans(t_T10, "zoomout", 1.2, "zoom-out: o quadro encolhe e revela o continente ao entardecer")

# ======================= A RESPOSTA (b47–b48) =======================
tab(quente, t_T10, 0.6, 1.2)
cam(t_T10, P(-62, -18), 72, 62, -8, corte=True); cam(F("b47", 3), P(-62, -18), 66, 62, 0); cam(E("b48") + 2.5, P(-62, -18), 60, 60, 10)
cartao(S("b47"), F("b47", 1) + 0.2, "A RESPOSTA", "É mesmo um super El Niño?", top=240)
for k, (pid, nome, xz) in enumerate([("f1", "MANAUS · FUMAÇA", MAN), ("f2", "DIONÍSIO CERQUEIRA · CHUVA", DC), ("f3", "COSTA DO PERU · MAR QUENTE", PERU)]):
    pino(pid, nome, "", F("b47", 1) + 0.4 * k, xz=xz, ate=F("b47", 3))
fios += [{"pontos": [MAN, DC], "t0": F("b47", 2), "t1": F("b47", 2) + 1.0, "grosso": 4}, {"pontos": [DC, PERU], "t0": F("b47", 2) + 0.5, "t1": F("b47", 2) + 1.5, "grosso": 4},
         {"pontos": [PERU, MAN], "t0": F("b47", 2) + 1.0, "t1": F("b47", 2) + 2.0, "grosso": 4}]
num(F("b47", 4), "MUITO FORTE", "EL NIÑO 2026 · NOAA/CPC · PICO: DEZ–JAN")
num_off(E("b47"))
cx_estados += [{"t": F("b47", 4), "modo": "final", "ativa": 0, "feitas": [1, 2, 3, 4]}]
cta = {"t0": S("b48") + 0.1, "t_inscreve": tw("inscreve", "b48", alt=F("b48", 1)) - 0.2,
       "texto": "MANDA PRA QUEM VAI PASSAR O VERÃO NO SUL, NO NORTE OU NO NORDESTE", "inscreve": "INSCREVA-SE · A GENTE VOLTA QUANDO OS NÚMEROS MUDAREM"}

fontes = [
    {"t": 0, "texto": "FONTES: DEFESA CIVIL DE MANAUS · INMET · NOAA/CPC · SATÉLITE: NASA (GIBS) · MAPA: IBGE / NATURAL EARTH"},
    {"t": S("b08") - 0.5, "texto": "FONTES: NOAA PMEL · NOAA CLIMATE.GOV · NOAA/CPC · MAPA: NATURAL EARTH"},
    {"t": S("b15") - 0.5, "texto": "FONTES: NOAA OISST (RELEVO: DADOS NOAA, ARTE EM RELEVO) · INMET (03/11) · NOAA/CPC (ONI)"},
    {"t": sl0 - 0.3, "texto": "FONTES: NOAA/CPC (RONI, BOLETIM DE 08/10/2026) · IRI/COLUMBIA (19/10) · OMM · CARBON BRIEF"},
    {"t": S("b22") - 0.5, "texto": "FONTES: NOAA CLIMATE.GOV · OMM · RELEVO: DADOS NOAA OISST"},
    {"t": S("b23") - 0.5, "texto": "FONTES: PAINEL EL NIÑO 2026-27 (BOLETIM Nº 05) · INMET · INPE · MAPA: IBGE"},
    {"t": S("b26") - 0.5, "texto": "FONTES: SGB · ANA · INPE · DEFESA CIVIL DE MANAUS · PAINEL EL NIÑO · SATÉLITE: NASA HLS / COPERNICUS SENTINEL"},
    {"t": S("b29") - 0.5, "texto": "FONTES: MONITOR DE SECAS (ANA) · PAINEL EL NIÑO · MAPA: IBGE"},
    {"t": S("b30") - 0.5, "texto": "FONTES: PAINEL EL NIÑO (PREVISÃO NOV–JAN) · MAPA: IBGE"},
    {"t": S("b32") - 0.5, "texto": "FONTES: PAINEL EL NIÑO · INMET · CLIMATEMPO · DEFESAS CIVIS RS E SC · SIMEPAR"},
    {"t": S("b36") - 0.5, "texto": "FONTES: DEFESA CIVIL DO PR · DEFESA CIVIL DE BLUMENAU · WORLD WEATHER ATTRIBUTION"},
    {"t": S("b38") - 0.5, "texto": "FONTES: COPERNICUS C3S · CARBON BRIEF · GLOBO: DADOS NOAA OISST, ARTE EM RELEVO"},
    {"t": S("b39") - 0.5, "texto": "FONTES: NOAA/CPC (08/10/2026) · BUREAU OF METEOROLOGY (27/10) · CARBON BRIEF · PAINEL EL NIÑO"},
    {"t": S("b44") - 0.5, "texto": "FONTES: MINISTÉRIO DA INTEGRAÇÃO (SMS 40199) · MINISTÉRIO DA SAÚDE"},
    {"t": S("b47") - 0.5, "texto": "FONTES: NOAA/CPC · INMET · DEFESA CIVIL DE MANAUS · PAINEL EL NIÑO"},
]

texturas = sorted({g["img"] for g in globos})
# a caixa compacta (canto superior direito) fica só ~5 s depois de cada abertura de pergunta (evita poluir a tela)
extra = []
for e in cx_estados:
    if e["modo"] == "compacta": extra.append({"t": round(e["t"] + 5.0, 3), "modo": "oculto"})
cx_estados = sorted(cx_estados + extra, key=lambda e: e["t"])
cues = {
    "_doc": "Gerado por shared/build_cues.py (não editar à mão). Tempos em segundos de audio/narracao.wav.",
    "fps": 30, "duracao": tempos["duracao"], "fim_fala": tempos["blocos"][-1]["e"], "slot": SLOT, "voz": tempos.get("voz"),
    "paleta": {"papel": "#E9DCC3", "coral": "#E8505B", "navy": "#1F2A44", "tinta": "#2B2622", "branco": "#FBF8F1"},
    "palavras": palavras, "capitulos": capitulos, "numero": sorted(numero, key=lambda n: n["t"]), "camera": camera,
    "luz": sorted(luz), "noite": noite, "quente": quente, "amazonia": amazonia, "andes": andes_t, "arquivo": arquivo, "tremor": tremor, "desfoque": desfoque,
    "pinos": pinos, "destaques": destaques, "fios": fios, "funis": funis, "setas": setas, "nuvens": nuvens, "regioes": regioes, "rastros": rastros,
    "sats": sats, "ciclones": ciclones, "aneis": aneis, "supercelula": None, "rotulos_mapa": rotulos,
    "relevos": relevos, "diorama": diorama, "montanhas": montanhas, "barras3d": barras3d, "globos": globos, "fumacas": fumacas, "chuvas": chuvas,
    "cilindros": cilindros, "pontos": pontos, "tintas": tintas, "sst_datas": SST["datas"],
    "midia": midia, "manchetes": manchetes, "cartoes": cartoes, "graficos": graficos, "checklists": checklists, "calendario": None,
    "pergunta": pergunta, "caixas": {"itens": cx_itens, "estados": cx_estados}, "cortica": cortica, "cobre3d": cobre3d,
    "thumbs": {"1": round(E("b17") - 0.5, 3), "2": round(E("b25") - 0.3, 3), "3": round(F("b47", 3) + 1.0, 3)},
    "transicoes": sorted(transicoes, key=lambda x: x["t"]), "cta": cta, "fontes": fontes, "texturas": texturas,
}
cues["camera"].sort(key=lambda k: k["t"])
json.dump(cues, open(A / "cues.json", "w"), ensure_ascii=False, separators=(",", ":"))
(R / "work").mkdir(exist_ok=True)
with open(R / "work/storyboard.txt", "w") as f:
    for tr in cues["transicoes"]: f.write(f"TRANSIÇÃO {tr['t']:7.2f}s {tr['tipo']}: {tr['desc']}\n")
    for m in midia: f.write(f"MÍDIA {m['t0']:7.2f}–{m['t1']:7.2f}s {m['id']} ({m['lado']})\n")
    f.write("\n".join(avisos))
# conferência do slot: nenhum evento de b19–b21 pode vazar da janela
if SLOT:
    vaz = [m for m in midia + manchetes + cartoes + graficos if (SLOT["s"] - 0.5 < m["t0"] < SLOT["e"]) and m["t1"] > SLOT["e"] + 0.7]
    if vaz: avisos.append(f"ATENÇÃO: {len(vaz)} eventos começam no slot e passam do fim: {[v.get('id', v.get('tipo', v.get('rotulo'))) for v in vaz]}")
print(f"ok: {len(palavras)} palavras, {len(camera)} chaves de câmera, {len(midia)} mídias, {len(transicoes)} transições, {len(relevos)} relevos")
print("avisos:", *avisos, sep="\n  ")
