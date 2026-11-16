# Storyboard em código do longo 03 (Em Relevo, A Grande Seca de 1877): gera shared/cues.json (fonte única da composição LongoV3)
# e shared/estilo_v2.json (linha do tempo A/B) a partir de blocos.json, tempos.json, whisper.json, storyboard.json, geo.json e dados/.
# Mesmo método do longo-02/shared/build_cues.py: cada evento amarrado à palavra falada (Whisper) ou ao início da frase.
import json, math, re, unicodedata
from pathlib import Path

A = Path(__file__).parent; R = A.parent
blocos = json.load(open(A / "blocos.json")); tempos = json.load(open(A / "tempos.json")); wh = json.load(open(A / "whisper.json"))
geo = json.load(open(A / "geo.json")); SST = json.load(open(A / "sst_pacifico.json"))
HIST = json.load(open(R / "dados/historia.json")); RIOS = json.load(open(R / "dados/rios-ce.json"))
SEMI = json.load(open(R / "dados/semiarido.json")); MON = json.load(open(R / "dados/monitor-secas-2026-09.json"))
CHUVA = json.load(open(R / "dados/chuva-fortaleza-resumo.json"))
FOTOS = {f["arquivo"].replace("ê", "e").replace("ç", "c"): f for f in json.load(open(R / "dl/fotos/fotos.json"))}
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
def cartao(t0, t1, rotulo, texto, carimbo=None, t_carimbo=None, top=300):
    c = {"t0": round(t0, 3), "t1": round(t1, 3), "rotulo": rotulo, "texto": texto, "top": top}
    if carimbo: c["carimbo"] = {"texto": carimbo, "t": round(t_carimbo, 3)}
    cartoes.append(c)
def trans(t, tipo, dur=1.0, desc=""): transicoes.append({"t": round(t, 3), "tipo": tipo, "dur": dur, "desc": desc})
def papel(b0, b1, itens, pre=0.0, topo=False): papeis.append({"t0": round(S(b0) - pre, 3), "t1": round(E(b1) + 0.25, 3), "itens": itens, "topo": topo})
def meio(b1, b2): return (E(b1) + S(b2)) / 2
luz = [[0, 1]]; noite = [[0, 0]]; quente = [[0, 0]]; amazonia = [[0, 0]]; andes_t = [[0, 0]]; arquivo = [[0, 0]]; tremor = [[0, 0]]; desfoque = [[0, 0]]
def tab(lista, t, v, dur=0.6): lista.append([round(t, 3), lista[-1][1]]); lista.append([round(t + dur, 3), v])
CID = {c["nome"]: c for c in HIST["cidades"]}
def cid(n): c = CID[n]; return P(c["lon"], c["lat"])
FOR, QUI, CRA, ICO, SOB, BAT, ARA, CAM = cid("Fortaleza"), cid("Quixadá"), cid("Crato"), cid("Icó"), cid("Sobral"), cid("Baturité"), cid("Aracati"), cid("Camocim")
CEDRO = P(-39.06293, -4.97825); BEL, MAN, RBR = cid("Belém"), cid("Manaus"), cid("Rio Branco")
CE = P(-39.4, -5.3); NE = P(-40.5, -8.0); BRC = P(-52, -14)
ACRE = P(-70.5, -9.2)
def L(lon, lat): return P(lon, lat)
SUL = [P2(195, 0)]; PACC = P2(195, 0); GLOBO = [PAC["x0"], -48.0]; MONT = [PAC["x0"], 34.0]
def grade_xy(lon0, lon1, lat0, lat1):
    i0, i1 = int(lon0 - SST["lon0"]), int(lon1 - SST["lon0"]); j0, j1 = int(lat0 - SST["lat0"]), int(lat1 - SST["lat0"])
    xs = [P2(SST["lon0"] + i, 0)[0] for i in range(i0, i1 + 1)]; zs = [P2(200, SST["lat0"] + j)[1] for j in range(j0, j1 + 1)]
    return {"i0": i0, "i1": i1, "j0": j0, "j1": j1, "xs": xs, "zs": zs}
NDAT = len(SST["datas"]); I1877, I2026 = 0, NDAT - 1
def ring(f):
    g = f["geometry"]; polys = [g["coordinates"]] if g["type"] == "Polygon" else [p for p in g["coordinates"]]
    return [p[0] for p in polys]
def linha_trilho(nome): return [P(lo, la) for lo, la in HIST["linhas_ferroviarias"][nome]["pontos"]]
def trecho(nome): return [P(lo, la) for lo, la in HIST["rota_migracao"]["trechos"][nome]]
RETIR = [(QUI, "Quixadá"), (CRA, "Crato"), (ICO, "Icó"), (SOB, "Sobral")]
def rios_retirantes(t0, tfim, vis=True):
    # ilustrativo: direção e destino reais (todos para Fortaleza), quantidade não é dado
    for k, (o, nome) in enumerate(RETIR):
        meio_ = [(o[0] + FOR[0]) / 2 + (0.5 if k % 2 else -0.5), (o[1] + FOR[1]) / 2 + 0.3]
        seta("#FFE9C7", [o, meio_, FOR], t0 + 0.35 * k, t0 + 0.35 * k + 2.6, tfim, y=0.35, r=0.07, fluxo=True, vel=0.14, semCabeca=True)
ESTILO = []   # (t, 'A'|'B')
def est(b, e): ESTILO.append((max(0, S(b) - 0.4) if b != "b01" else 0, e))

# ======================= HOOK =======================
est("b01", "A"); tab(luz, 0, 0.8, 0.1); tab(quente, 0, 0.55, 0.1)
cam(0.0, [CE[0] + 1, CE[1] + 1.5], 11, 22, -8, y=0.3); cam(F("b01", 1), [FOR[0] - 0.6, FOR[1] + 1.8], 9, 30, 4); cam(E("b01") - 0.2, [FOR[0] + 0.3, FOR[1] + 0.4], 6.5, 38, 10)
pino("for", "FORTALEZA · 1878", "", 0.4, t2=E("b02"), xz=FOR, y0=0.1, ate=S("b03") - 0.1)
num(0.5, "25 MIL", "FORTALEZA · 1878 · HABITANTES (ESTIMATIVA)")
t_ch = tw("chegam", "b01", alt=F("b01", 2) + 0.5)
rios_retirantes(t_ch, E("b05"))
num(t_ch + 0.4, de=25000, para=100000, dur=2.2, unidade="", faixa="MAIS DE 100 MIL CHEGAM · A PÉ · DO SERTÃO")
foto("fortaleza-planta-1875.jpg", F("b01", 1) + 0.4, F("b01", 1) + 3.6, lado="dir", pino="for")
num_off(S("b02"))
tt = tw("Theophilo", "b02", alt=F("b02", 0) + 0.3)
num(tt + 0.1, de=25000, para=160000, dur=2.0, faixa="SEGUNDO RODOLPHO THEOPHILO, QUE VIVEU AQUILO")
foto("teofilo-vacinando-1907.jpg", tt + 0.4, tt + 4.4, lado="esq")
graficos3.append({"tipo": "populacao", "t0": F("b02", 3) - 0.2, "t1": E("b02") + 0.5, "t_ini": F("b02", 3), "a": 25, "b": 160, "rotA": "25 MIL", "rotB": "160 MIL · 6×", "titulo": "FORTALEZA: ANTES E DEPOIS", "fonte": "RODOLPHO THEOPHILO; CENSO"})
num_off(E("b02"))
# b03 arquivo
papel("b03", "b03", [{"tipo": "data", "texto": "FORTALEZA · 10 DE DEZEMBRO DE 1878", "t": S("b03") + 0.2}, {"tipo": "numero", "de": 0, "para": 1004, "t": S("b03") + 0.6, "dur": 1.5, "tam": 280},
    {"tipo": "rotulo", "texto": "MORTOS DE VARÍOLA EM 1 DIA", "t": tw("mil|quatro", "b03", alt=F("b03", 1))}], pre=0.15)
tab(arquivo, S("b03") - 0.2, 0.7, 0.1); tab(arquivo, E("b03") + 0.3, 0.0, 0.2)
trans(S("b03") - 0.1, "corte", 0.5, "corte seco para o papel (impacto grave)")
cam(S("b03"), FOR, 7, 40, 0, corte=True)

# b04 Brasil
est("b04", "B"); tab(arquivo, S("b04") - 0.1, 0.0, 0.1); tab(quente, S("b04") - 0.2, 0.0, 0.3)
cam(S("b04"), CE, 14, 50, 0, corte=True); cam(F("b04", 1), NE, 34, 56, 0); cam(F("b04", 2), BRC, 66, 62, 4); cam(E("b04"), BRC, 68, 64, 0)
NORTE1877 = ["23", "24", "25", "26", "22", "27", "28", "29"]
tintas.append({"ufs": NORTE1877, "cor": "#E8505B", "op": janela_op(S("b04") + 0.5, E("b04") + 14, 1, 0.7, 0.8), "max": 0.8})
rot("O IMPÉRIO · 1877", L(-52, -10), S("b04") + 0.5, E("b04"), "mapa_grande")
num(tw("quinhentos|500", "b04", alt=F("b04", 1)), "500 MIL", "ESTIMATIVAS DE MORTOS · ATÉ", unidade="")
cartao(F("b04", 2) + 0.3, E("b04") + 0.2, "PELAS CONTAS MAIS ALTAS", "5% DA POPULAÇÃO DO IMPÉRIO", top=700)
cartao(S("b04") + 0.2, F("b04", 1) - 0.2, "A GRANDE SECA", "1877–1879", top=360)
num_off(E("b04") + 0.3)
# b05 
cam(S("b05"), NE, 36, 56, 2); cam(E("b05"), NE, 34, 54, -2)
cartao(S("b05") + 0.3, F("b05", 1) - 0.1, "QUASE NINGUÉM FALA DELA", "E EM 2026?", top=360)
trans(S("b05"), "luz", 1.0, "luz")
# b06 4 perguntas
cx_itens = [{"n": 1, "texto": "O QUE ACONTECEU?", "t": F("b06", 1)}, {"n": 2, "texto": "POR QUE NÃO CHOVEU?", "t": F("b06", 2)},
            {"n": 3, "texto": "O QUE MUDOU NO MAPA?", "t": F("b06", 3)}, {"n": 4, "texto": "E EM 2026?", "t": F("b06", 4)}]
cx_estados = [{"t": cx_itens[0]["t"], "modo": "grande", "ativa": 0, "feitas": []}, {"t": S("b07") + 0.3, "modo": "compacta", "ativa": 0, "feitas": []}, {"t": S("b08") - 0.5, "modo": "oculto"}]
cam(S("b06"), BRC, 70, 62, 0); cam(E("b06"), [CE[0] + 4, CE[1] + 4], 52, 58, 0)
# b07 anel de meses
cam(S("b07") + 0.3, CE, 15, 52, 6); cam(E("b07"), CE, 13, 54, 0)
tintas.append({"ufs": ["23"], "cor": "#E8505B", "op": janela_op(S("b07"), E("b07"), 1, 0.7, 0.8), "max": 0.55})
graficos3.append({"tipo": "meses", "t0": S("b07") + 0.8, "t1": E("b07") + 0.6, "t_chuva": tw("fevereiro", "b07", alt=F("b07", 2)), "titulo": "A CHUVA DO CEARÁ", "centro": "FEV–MAI", "fonte": "FUNCEME", "duvida": False})
rot("O 'INVERNO' DO SERTÃO", [CE[0] - 1.4, CE[1] + 0.6], tw("inverno", "b07", alt=F("b07", 3)), E("b07"), "corredor")

# ======================= 1/4 O QUE ACONTECEU =======================
est("b08", "A"); tab(quente, S("b08"), 0.35, 0.5)
trans(meio("b07", "b08"), "nuvem", 1.3, "push-in atravessando nuvens secas")
cx_estados += [{"t": S("b08") - 0.3, "modo": "grande", "ativa": 0, "feitas": [], "volta": True}, {"t": F("b08", 1), "modo": "compacta", "ativa": 0, "feitas": []}]
cam(meio("b07", "b08") + 0.2, CE, 16, 28, -10, corte=True); cam(E("b08"), CE, 12, 34, 8)
foto("hoje-santa-quiteria-2018.jpg", F("b08", 3) + 0.2, E("b08") + 0.2, lado="dir")
cartao(F("b08", 1) + 0.4, F("b08", 3) - 0.1, "19 DE MARÇO · SÃO JOSÉ", "SE CHOVER ATÉ AQUI, O INVERNO É BOM", top=330)
# b09 régua de chuva
est("b09", "B"); trans(S("b09") - 0.2, "whip", 0.6, "whip pan para o gráfico")
cam(S("b09") - 0.1, FOR, 12, 50, 0, corte=True); cam(E("b09"), [FOR[0] + 1, FOR[1] + 1], 13, 52, 10)
anos = []
for ln in open(R / "dados/chuva-fortaleza-anual.csv").read().strip().split("\n")[1:]:
    p = ln.split(",")
    if p[1] and float(p[1]) > 0 and (p[2] in ("0", "")): anos.append([int(p[0]), float(p[1])])
anos = [a for a in anos if a[0] <= 2018]
graficos3.append({"tipo": "chuva", "t0": S("b09") + 0.4, "t1": E("b09") + 0.6, "t_ini": tw("medida|desde", "b09", alt=S("b09") + 1), "dur": 5.0, "anos": anos, "max": 2800, "media": round(CHUVA["media_1849_2018_mm"]),
    "t_1877": tw("quatrocentos|468", "b09", alt=F("b09", 3)), "t_1878": tw("1878|setenta", "b09", n=0, alt=F("b09", 5)), "mm1877": 468, "titulo": "CHUVA ANUAL EM FORTALEZA · 1849–2018 (153 ANOS)", "fonte": "GHCN V2 (NOAA)"})
num(tw("quatrocentos|468", "b09", alt=F("b09", 3)) + 0.2, "468 MM", "EM 1877 · UM TERÇO DO NORMAL (1.450 MM)")
num_off(F("b09", 5))
# b10
est("b10", "A"); trans(S("b10") - 0.3, "whip", 0.6, "whip pan de volta ao mapa")
cam(S("b10"), [CE[0], CE[1] + 0.5], 14, 30, -20, corte=True); cam(E("b10"), [CE[0] + 1, CE[1] + 0.5], 12, 32, 20)
tab(quente, S("b10"), 0.2, 0.5)
foto("hoje-coremas-seca-2017.jpg", tw("pasto", "b10", alt=F("b10", 1)), tw("pasto", "b10", alt=F("b10", 1)) + 4.0, lado="esq")
for k, (txt, w) in enumerate([("PASTO SECOU", "pasto"), ("O GADO MORREU", "gado"), ("ROÇA: MILHO · FEIJÃO · MANDIOCA", "roças|rocas")]):
    rot(txt, [CE[0] + (1.5 if k % 2 else -1.5), CE[1] + 1.2 + k * 0.8], tw(w, "b10", alt=F("b10", 1) + k), E("b10"), "quente")
# b11
est("b11", "B"); cam(S("b11"), CE, 16, 52, 0, corte=True); cam(E("b11"), CE, 12, 56, 0)
tintas.append({"ufs": ["23"], "cor": "#E8505B", "op": janela_op(S("b11"), E("b13") + 6, 1, 0.7, 0.8), "max": 0.45})
rot("CEARÁ · 1872 · 721 MIL HABITANTES", [CE[0], CE[1] - 2.0], S("b11") + 0.3, F("b11", 2), "corredor")
pts_ce = [[CE[0] + math.cos(i * 2.4) * (0.4 + (i % 9) * 0.22), CE[1] + math.sin(i * 1.7) * (0.3 + (i % 7) * 0.2)] for i in range(120)]
pontos.append({"lista": pts_ce, "t0": S("b11") + 0.3, "t1": F("b11", 1) + 1.5, "t2": F("b11", 2)})
foto("mapa-seca-1877-rebouças.jpg".replace("ç", "c"), F("b11", 0) + 1.0, F("b11", 1) + 0.5, lado="dir")
# b12 plano-assinatura
est("b12", "A"); cam(S("b12"), [CE[0], CE[1] + 0.3], 18, 62, 0, corte=True); cam(E("b12"), [CE[0], CE[1] + 0.3], 15, 66, 6)
t_r = tw("escorresse|escorre", "b12", alt=S("b12") + 0.4)
for rio in RIOS["features"]:
    pass
rios_retirantes(t_r, E("b13") + 3)
rot("RETIRANTES", [CE[0] - 0.5, CE[1] - 1.6], tw("retirantes", "b12", alt=F("b12", 2)), F("b12", 2) + 4, "corredor")
foto("retirantes-1878-grupo.jpg", tw("retirantes", "b12", alt=F("b12", 2)) + 0.1, tw("retirantes", "b12", alt=F("b12", 2)) + 3.6, lado="dir", fmt="carte", estatica=True)
# b13 abarracados
est("b13", "B"); trans(S("b13") - 0.2, "rack", 1.0, "rack focus para Fortaleza"); tab(desfoque, S("b13") - 0.4, 1.0, 0.4); tab(desfoque, S("b13") + 0.4, 0.0, 0.5)
cam(S("b13") - 0.1, FOR, 6, 54, 0, corte=True); cam(E("b13"), [FOR[0], FOR[1] + 0.3], 5.0, 56, 6)
pts_b = [[FOR[0] + 0.15 * math.cos(i * 2.3) * (1 + i % 5) * 0.5, FOR[1] + 0.12 * math.sin(i * 1.9) * (1 + i % 4) * 0.5] for i in range(90)]
pontos.append({"lista": pts_b, "t0": S("b13") + 1.5, "t1": tw("agosto", "b13", alt=F("b13", 3)) + 2, "t2": E("b14")})
rot("ABARRACAMENTOS", [FOR[0] - 1.1, FOR[1] - 0.6], F("b13", 1), E("b13"), "corredor")
num(tw("agosto", "b13", alt=F("b13", 3)), de=0, para=113900, dur=2.0, faixa="ABARRACADOS · AGO/1878 · QUASE 114 MIL")
num_off(E("b13") + 0.2)
# b14
est("b14", "A"); cam(S("b14"), [FOR[0] + 1, FOR[1] - 0.6], 9, 36, 20, corte=True); cam(E("b14"), [FOR[0] + 0.6, FOR[1] - 0.2], 8, 38, -10)
seta("#FFFFFF", [[FOR[0] + 7, FOR[1] - 4.5], [FOR[0] + 3.2, FOR[1] - 2.0], [FOR[0] + 0.3, FOR[1] - 0.15]], S("b14") + 0.4, S("b14") + 2.4, E("b14"), y=0.3, r=0.1, fluxo=True, vel=0.12)
rot("A COMIDA VINHA POR MAR", [FOR[0] + 3.2, FOR[1] - 2.2], S("b14") + 0.6, F("b14", 2), "seta")
cartao(tw("carne", "b14", alt=F("b14", 2)), E("b14") + 0.1, "DENÚNCIAS · 1878", "CARNE ESTRAGADA · FARINHA COM CAL", top=330)
foto("mapa-seca-1878-ferrovias.jpg", F("b14", 1) - 0.2, F("b14", 2) + 0.4, lado="dir")
# b15/b16 arquivo
trans(S("b15") - 0.1, "corte", 0.5, "corte seco para o papel")
tab(arquivo, S("b15") - 0.2, 0.7, 0.1); tab(arquivo, E("b16") + 0.3, 0.0, 0.2); cam(S("b15"), FOR, 7, 40, 0, corte=True)
papel("b15", "b15", [{"tipo": "data", "texto": "FORTALEZA · 1878 · MORTES POR MÊS", "t": S("b15") + 0.3},
    {"tipo": "barras", "max": 16000, "t": F("b15", 2), "itens": [["NOV", 9844, F("b15", 3) + 0.2, "#6b3b2a"], ["DEZ", 15352, F("b15", 4) + 0.2, "#E8505B"]]},
    {"tipo": "rotulo", "texto": "DEZEMBRO: 14.491 DE VARÍOLA", "t": F("b15", 4) + 1.8}], pre=0.15, topo=True)
foto("retirante-correa-1877-a.jpg", F("b15", 2) + 0.2, F("b15", 2) + 4.0, lado="esq", fmt="carte", estatica=True)
papel("b16", "b16", [{"tipo": "data", "texto": "10 DE DEZEMBRO DE 1878", "t": S("b16") + 0.2}, {"tipo": "numero", "de": 0, "para": 1004, "t": S("b16") + 0.5, "dur": 1.2, "tam": 260},
    {"tipo": "rotulo", "texto": "MORTOS EM UM DIA", "t": S("b16") + 1.8}, {"tipo": "titulo", "texto": "O DIA DOS MIL MORTOS", "t": tw("Dia", "b16", n=0, apos=F("b16", 3), alt=F("b16", 3)), "tam": 110}], pre=0.15)
# b17 estimativas
est("b17", "B"); tab(arquivo, S("b17") - 0.1, 0.0, 0.1); trans(S("b17") - 0.1, "corte", 0.5, "corte seco de volta ao mapa")
cam(S("b17"), NE, 30, 56, 0, corte=True); cam(E("b17"), NE, 26, 56, 6)
tintas.append({"ufs": NORTE1877, "cor": "#E8505B", "op": janela_op(S("b17"), E("b17"), 1, 0.7, 0.8), "max": 0.6})
graficos3.append({"tipo": "estimativas", "t0": F("b17", 2) - 0.3, "t1": E("b17") + 0.6, "t_ini": F("b17", 2), "max": 550, "de": 150, "para": 500,
    "marcas": [[150, "150 MIL", tw("cento|150", "b17", alt=F("b17", 2) + 0.5)], [500, "500 MIL", tw("quinhentos|500", "b17", alt=F("b17", 2) + 1.7)]], "titulo": "MORTOS (MIL): NINGUÉM CONTOU DIREITO", "fonte": "ESTIMATIVAS DE HISTORIADORES; AGÊNCIA SENADO"})
cartao(tw("chuva", "b17", n=0, alt=F("b17", 3)), E("b17") + 0.2, "A CHUVA SÓ VOLTOU DE VERDADE EM", "1880", top=340)
# b18 O Besouro
trans(S("b18") - 0.1, "match", 1.0, "match cut: o mapa vira a página de jornal")
tab(arquivo, S("b18") - 0.2, 0.7, 0.1); tab(arquivo, E("b18") + 0.3, 0.0, 0.2); cam(S("b18"), FOR, 7, 40, 0, corte=True)
papel("b18", "b18", [{"tipo": "data", "texto": "RIO DE JANEIRO · 1878 · O BESOURO", "t": tw("Besouro", "b18", alt=F("b18", 1))},
    {"tipo": "carimbo", "texto": "PRIMEIRO FOTOJORNALISMO DO BRASIL?", "t": tw("fotojornalismo", "b18", alt=F("b18", 3)), "tam": 58}], pre=0.15, topo=True)
foto("retirante-correa-1878-b.jpg", F("b18", 1) + 0.8, F("b18", 1) + 4.6, lado="esq", fmt="carte", estatica=True)
foto("retirantes-1878-grupo.jpg", F("b18", 1) + 1.4, F("b18", 1) + 5.2, lado="dir", fmt="carte", estatica=True)
foto("patrocinio-1879.jpg", F("b18", 3) + 0.3, F("b18", 3) + 3.8, lado="centro", fmt="carte", estatica=True)

# ======================= 2/4 POR QUE NÃO CHOVEU =======================
est("b19", "A"); tab(arquivo, S("b19") - 0.1, 0.0, 0.1)
trans(meio("b18", "b19"), "nuvem", 1.3, "zoom-out orbital do Ceará até o globo")
cx_estados += [{"t": S("b19") - 0.3, "modo": "grande", "ativa": 1, "feitas": [1], "volta": True}, {"t": E("b19") + 0.3, "modo": "compacta", "ativa": 1, "feitas": [1]}]
cam(meio("b18", "b19") + 0.2, GLOBO, 30, 8, 0, y=7.0, corte=True); cam(E("b19"), GLOBO, 26, 10, 6, y=7.0)
globos.append({"img": "sat/globo-1877.jpg", "x": GLOBO[0], "y": 7.0, "z": GLOBO[1], "r": 7.0, "rot0": 0, "vel": 0.0, "op": janela_op(S("b19") - 0.3, E("b19") + 0.6, 1, 0.3, 0.3), "rot": [[0, -0.9], [S("b19"), -0.9], [E("b19"), 0.87]]})
rot("DO OUTRO LADO DO PLANETA", [GLOBO[0] + 1.5, GLOBO[1] + 6.8], tw("outro", "b19", alt=F("b19", 2)), E("b19") + 0.4, "corredor", y=5.0)
# b20 Pacífico 1877 + montanhas
est("b20", "A"); t20 = S("b20") - 0.4
cam(t20, PACC, 58, 56, -6, corte=True); cam(F("b20", 3), P2(215, 0), 44, 48, 4); cam(F("b20", 4) - 0.2, P2(215, 0), 40, 50, 0)
gpac = grade_xy(100, 290, -30, 30)
relevos.append({**gpac, "y0": 0.03, "k": 0.45, "mostra_data": False, "idx": [[0, I1877]], "op": janela_op(S("b20") - 0.2, F("b20", 4) - 0.1, 1, 0.8, 0.5), "cresce": [[0, 0], [S("b20"), 0], [S("b20") + 3.0, 1]]})
rot("PACÍFICO · DEZ/1877 · RECONSTRUÇÃO", P2(215, 12), S("b20") + 1.0, F("b20", 4), "corredor")
t_mt = F("b20", 4) - 0.1
KH = 2.3; fim_m = E("b20") + 0.6
ANOS = [("1877-78", 2.53), ("1982-83", 2.33), ("1997-98", 2.40), ("2015-16", 2.71)]
for k, (ano, v) in enumerate(ANOS):
    x = MONT[0] + (k - 1.5) * 4.6; ts = tw(ano[:4][2:] if ano[:4] != "1877" else "mil|1877", "b20", apos=F("b20", 4) - 0.3, alt=F("b20", 5) + k * 0.8)
    tk = [F("b20", 4) + 0.2, F("b20", 5) + 0.3, F("b20", 5) + 1.0, F("b20", 5) + 1.7][k]
    montanhas.append({"nome": ano, "x": x, "z": MONT[1], "r": 1.55, "kh": KH, "cor": "#E8505B" if k == 0 else "#DCCDB0", "h": [[0, 0], [tk - 0.2, 0], [tk + 1.0, v]], "op": janela_op(t_mt, fim_m, 1, 0.5, 0.6), "acende": [[0, 0], [tk, 1], [tk + 1.2, 0.2]]})
cam(t_mt + 0.1, MONT, 30, 14, -6, y=2.6, corte=True); cam(E("b20"), [MONT[0] + 3, MONT[1]], 28, 14, 6, y=3.0)
num(tk, "NO NÍVEL DE 82, 97 E 2015", "NIÑO 3.4 · MÁXIMO MENSAL · NOAA ERSSTV5 (RECONSTRUÇÃO)") if False else None
# b21 Walker
est("b21", "A"); trans(S("b21") - 0.3, "whip", 0.6, "whip pan para a circulação de Walker")
WX0, WX1 = P2(128, 0)[0], P2(262, 0)[0]
cam(S("b21"), [PACC[0], 4.0], 66, 14, 4, y=4.0, corte=True); cam(E("b21"), [PACC[0], 4.0], 62, 16, -4, y=4.0)
t_w = tw("sobe", "b21", alt=F("b21", 1)); t_d = tw("desce", "b21", n=0, alt=F("b21", 2))
seta("#E07A3A", [[WX0, 0, 5.4], [WX0, 0, 7.0], [WX0 + 0.5, 0, 8.6]], t_w, t_w + 1.0, E("b21"), r=0.3)
seta("#E07A3A", [[WX0 + 1, 0, 9.0], [PACC[0], 0, 9.4], [WX1 - 1, 0, 9.0]], t_w + 1.0, t_w + 2.6, E("b21"), r=0.3)
seta("#4C7FB8", [[WX1, 0, 8.6], [WX1, 0, 7.2], [WX1, 0, 5.6]], t_d, t_d + 1.0, E("b21"), r=0.3)
rot("AR SOBE: NUVENS E CHUVA", [WX0 + 4, 0], t_w + 0.4, E("b21"), "quente", y=10.6); rot("AR DESCE: SEM NUVEM", [WX1 - 2, 0], t_d + 0.4, E("b21"), "fria", y=10.0)
cartao(S("b21") + 0.2, F("b21", 1) - 0.1, "ASSISTA: EL NIÑO 2026", "O NOSSO VÍDEO ANTERIOR", top=200)
# b22 Atlântico
est("b22", "B"); trans(S("b22") - 0.2, "whip", 0.6, "whip pan para o Atlântico")
AT = P(-30, 2); cam(S("b22"), AT, 46, 54, 0, corte=True); cam(F("b22", 3), [AT[0] + 4, AT[1] + 2], 34, 54, 6); cam(E("b22"), [CE[0] + 4, CE[1] - 2], 32, 54, 0)
t_z = tw("faixa", "b22", alt=F("b22", 1))
seta("#FFFFFF", [P(-50, 0.5), P(-40, 0.8), P(-30, 0.5), P(-20, 0.3)], t_z, t_z + 2, F("b22", 3), y=0.6, r=0.35, fluxo=True, vel=0.12, semCabeca=True)
seta("#FFFFFF", [P(-50, 4.5), P(-40, 5.0), P(-30, 5.2), P(-20, 4.8)], F("b22", 3), F("b22", 3) + 2, E("b22"), y=0.6, r=0.35, fluxo=True, vel=0.12, semCabeca=True)
regioes.append({"anel": [P(-50, 8), P(-15, 8), P(-15, 25), P(-50, 25)], "cor": "#E8505B", "op": janela_op(tw("Norte", "b22", alt=F("b22", 2)), E("b22"), 1, 0.8, 0.8), "max": 0.35, "y": 0.5})
rot("ATLÂNTICO NORTE MAIS QUENTE", P(-32, 14), tw("Norte", "b22", alt=F("b22", 2)), E("b22"), "quente"); rot("FAIXA DE NUVENS (ZCIT)", P(-36, -1.2), t_z + 0.3, F("b22", 3), "seta")
rot("CEARÁ SEM CHUVA", [CE[0] + 0.5, CE[1] - 1.2], F("b22", 3) + 0.5, E("b22"), "corredor")
# b23 / b24 globo com 3 pinos
est("b23", "A"); trans(meio("b22", "b23"), "nuvem", 1.3, "zoom-out orbital até o globo")
cam(meio("b22", "b23") + 0.2, GLOBO, 30, 8, 0, y=7.0, corte=True); cam(E("b24"), GLOBO, 26, 10, 6, y=7.0)
globos.append({"img": "sat/globo-1877.jpg", "x": GLOBO[0], "y": 7.0, "z": GLOBO[1], "r": 7.0, "rot0": 0, "vel": 0.0, "op": janela_op(S("b23") - 0.3, E("b24") + 0.6, 1, 0.3, 0.3), "rot": [[0, 0.87], [S("b23"), 0.87], [tw("India|Índia", "b23", n=1, alt=F("b23", 1)), -2.6], [tw("China", "b23", n=1, alt=F("b23", 2)), -3.2], [E("b24"), -2.9]]})
num(tw("India|Índia", "b23", n=1, alt=F("b23", 1)) + 0.3, "5,5–9,6 MI", "ÍNDIA · MORTOS ESTIMADOS NA FOME DE 1876–78")
num(tw("China", "b23", n=1, alt=F("b23", 2)) + 0.3, "9–13 MI", "NORTE DA CHINA · MORTOS ESTIMADOS")
num_off(E("b23"))
foto("india-1877-graphic-bellary.jpg", tw("India|Índia", "b23", n=1, alt=F("b23", 1)) + 0.3, tw("India|Índia", "b23", n=1, alt=F("b23", 1)) + 3.8, lado="dir")
cam(S("b24"), GLOBO, 26, 10, 6, y=7.0)
num(tw("cinquenta", "b24", alt=F("b24", 2) + 1), "+50 MILHÕES", "ESTIMATIVAS DE MORTOS NO MUNDO · ESTUDO DE 2018 (J. CLIMATE)")
num_off(E("b24") + 0.3)
# b25 Ceará sem açude
est("b25", "B"); trans(S("b25") - 0.2, "rack", 1.2, "rack focus de volta ao Ceará"); tab(desfoque, S("b25") - 0.5, 1.0, 0.5); tab(desfoque, S("b25") + 0.6, 0.0, 0.6)
cam(S("b25") - 0.1, CE, 14, 54, 0, corte=True); cam(E("b25"), CE, 12, 56, 8)
tintas.append({"ufs": ["23"], "cor": "#E8505B", "op": janela_op(S("b25"), E("b26"), 1, 0.7, 0.8), "max": 0.35})
trilho0 = linha_trilho("EF Baturité: Fortaleza–Baturité")[:6]
seta("#E8505B", trilho0, tw("ferrovia", "b25", alt=F("b25", 2)), tw("ferrovia", "b25", alt=F("b25", 2)) + 1.5, E("b25"), y=0.3, r=0.05, semCabeca=True)
rot("0 GRANDES AÇUDES", [CE[0] - 1.0, CE[1] + 1.0], tw("açude|acude", "b25", alt=F("b25", 2)), E("b25"), "corredor")
rot("FERROVIA: SÓ ATÉ PACATUBA (1873)", [FOR[0] + 1.7, FOR[1] + 0.8], tw("ferrovia", "b25", alt=F("b25", 2)) + 0.3, E("b25"), "seta")
# b26 Sinimbu
trans(S("b26") - 0.1, "corte", 0.5, "corte seco para o papel do Senado")
tab(arquivo, S("b26") - 0.2, 0.7, 0.1); tab(arquivo, E("b26") + 0.3, 0.0, 0.2); cam(S("b26"), FOR, 7, 40, 0, corte=True)
papel("b26", "b26", [{"tipo": "citacao", "texto": "A SOLUÇÃO DEPENDE DA DIVINA PROVIDÊNCIA, E NÃO DE NÓS.", "autor": "SENADOR SINIMBU, CHEFE DO GOVERNO · 1878", "t": tw("solução|solucao", "b26", alt=F("b26", 1))},
    {"tipo": "carimbo", "texto": "INVESTIGAÇÃO NÃO APROVADA", "t": tw("aprovado", "b26", alt=F("b26", 2) + 1), "tam": 64}], pre=0.15)

# ======================= 3/4 MAPA =======================
est("b27", "A"); tab(arquivo, S("b27") - 0.1, 0.0, 0.1); trans(S("b27") - 0.1, "corte", 0.5, "corte seco de volta ao mapa"); tab(luz, S("b27"), 1.0, 0.3); tab(quente, S("b27"), 0.0, 0.3)
cx_estados += [{"t": S("b27") - 0.3, "modo": "grande", "ativa": 2, "feitas": [1, 2], "volta": True}, {"t": E("b27") + 0.3, "modo": "compacta", "ativa": 2, "feitas": [1, 2]}]
cam(S("b27"), CE, 16, 40, 0, corte=True); cam(E("b27"), CE, 14, 42, 10)
# b28 ferrovia de Baturité
est("b28", "B"); cam(S("b28"), [FOR[0] + 1.2, FOR[1] + 1.2], 11, 54, 0, corte=True); cam(F("b28", 2), [QUI[0] - 1.5, QUI[1] - 2.0], 11, 54, 6); cam(E("b28"), [QUI[0] - 1.2, QUI[1] - 1.8], 9, 50, 10)
tr = linha_trilho("EF Baturité: Fortaleza–Quixadá"); trb = linha_trilho("EF Baturité: Fortaleza–Baturité")
tb_ = tw("Baturité|Baturite", "b28", n=0, apos=F("b28", 1), alt=F("b28", 1))
seta("#E8505B", trb, S("b28") + 0.5, tb_ + 2.0, E("b30"), y=0.3, r=0.06, semCabeca=True)
seta("#E8505B", tr, tw("Quixadá|Quixada", "b28", alt=F("b28", 3)), tw("Quixadá|Quixada", "b28", alt=F("b28", 3)) + 2.5, E("b30"), y=0.3, r=0.06, semCabeca=True)
pino("bat", "BATURITÉ · 1882", "", tb_ + 1.8, xz=BAT, ate=E("b28"), pequeno=False); pino("qui", "QUIXADÁ · 1891", "", tw("Quixadá|Quixada", "b28", alt=F("b28", 3)) + 2.2, xz=QUI, ate=E("b30"))
rot("1878 · OBRA DE SOCORRO", [FOR[0] + 0.9, FOR[1] - 0.7], S("b28") + 1.0, F("b28", 1) + 3, "corredor")
foto("ferrovia-baturite-estacao.jpg", tb_ + 0.3, tb_ + 4.0, lado="esq"); foto("ferrovia-quixada-estacao.jpg", tw("Quixadá|Quixada", "b28", alt=F("b28", 3)) + 0.3, E("b28") + 0.3, lado="dir")
# b29 Camocim-Sobral
est("b29", "B"); trans(S("b29") - 0.2, "whip", 0.6, "whip pan para o norte")
cam(S("b29") - 0.1, [SOB[0] - 1.5, SOB[1] - 0.6], 12, 54, 0, corte=True); cam(E("b29"), [SOB[0] - 1.8, SOB[1] - 0.4], 10, 52, 8)
trs = linha_trilho("EF Sobral: Camocim–Granja")[::-1] + linha_trilho("EF Sobral: Granja–Sobral")[::-1] if False else linha_trilho("EF Sobral: Camocim–Granja") + linha_trilho("EF Sobral: Granja–Sobral")
seta("#E8505B", trs, tw("Camocim", "b29", alt=F("b29", 1)), tw("Camocim", "b29", alt=F("b29", 1)) + 3.0, E("b30"), y=0.3, r=0.06, semCabeca=True)
pino("sob", "SOBRAL · 31/12/1882", "", tw("Sobral", "b29", alt=F("b29", 1) + 1), xz=SOB, ate=E("b29") + 0.5)
foto("mapa-seca-1878-ferrovias.jpg", F("b29", 1), E("b29") + 0.2, lado="dir")
# b30 Cedro
est("b30", "A"); trans(S("b30") - 0.2, "whip", 0.6, "whip pan para Quixadá")
cam(S("b30") - 0.1, CEDRO, 6, 34, -20, corte=True); cam(F("b30", 3), CEDRO, 3.6, 30, 10); cam(E("b30"), CEDRO, 3.8, 32, 40)
pino("ced", "AÇUDE DO CEDRO", "1884 → 1906", S("b30") + 0.6, xz=CEDRO, ate=E("b30"))
cilindros.append({"x": CEDRO[0] + 0.15, "z": CEDRO[1] + 0.1, "r": 0.55, "h": 0.12, "cor": "#3D6A9E", "op": janela_op(tw("represar", "b30", alt=F("b30", 1)), E("b30") + 0.5, 1, 0.5, 0.5), "nivel": [[0, 0.1], [tw("represar", "b30", alt=F("b30", 1)), 0.1], [tw("Levou|22", "b30", alt=F("b30", 5)), 1.0]]})
foto("cedro-galinha-choca-pd.jpg", tw("Galinha", "b30", alt=F("b30", 2) + 1.2) - 0.2, tw("Galinha", "b30", alt=F("b30", 2) + 1.2) + 5.0, lado="esq")
foto("cedro-barragem-detalhe.jpg", tw("primeiro", "b30", alt=F("b30", 4)), tw("primeiro", "b30", alt=F("b30", 4)) + 4.0, lado="dir")
num(tw("Levou|22", "b30", alt=F("b30", 5)), "22 ANOS", "PARA FICAR PRONTO · 1884 → 1906")
num_off(E("b30") + 0.3)
# b31 lenda
trans(S("b31") - 0.1, "corte", 0.5, "corte seco para o papel"); tab(arquivo, S("b31") - 0.2, 0.7, 0.1); tab(arquivo, E("b31") + 0.3, 0.0, 0.2); cam(S("b31"), FOR, 7, 40, 0, corte=True)
papel("b31", "b31", [{"tipo": "rotulo", "texto": "FRASE ATRIBUÍDA A DOM PEDRO II", "t": S("b31") + 0.3},
    {"tipo": "citacao", "texto": "VENDEREI ATÉ A ÚLTIMA JOIA DA COROA PARA QUE NENHUM CEARENSE MORRA DE FOME.", "t": tw("joia", "b31", alt=F("b31", 1)) - 0.5},
    {"tipo": "carimbo", "texto": "SEM DOCUMENTO", "t": tw("documento", "b31", alt=F("b31", 2) + 0.5), "tam": 84}], pre=0.15)
# b32 rota
est("b32", "A"); tab(arquivo, S("b32") - 0.1, 0.0, 0.1); trans(S("b32") - 0.1, "nuvem", 1.3, "zoom-out orbital do Ceará para a América do Sul"); tab(luz, S("b32"), 1.0, 0.2)
cam(S("b32"), P(-48, -3.5), 32, 52, 0, corte=True); cam(E("b32"), P(-54, -3), 36, 52, 6)
r1, r2, r3 = trecho("Fortaleza→Belém (cabotagem)"), trecho("Belém→Manaus (rio Amazonas)"), trecho("Manaus→Rio Branco (Solimões/Purus)")
seta("#FFE9C7", r1, tw("embarcaram", "b32", alt=F("b32", 1)), tw("embarcaram", "b32", alt=F("b32", 1)) + 2.2, E("b34") + 4, y=0.4, r=0.1, fluxo=True, vel=0.1)
seta("#FFE9C7", r2, tw("Amaz", "b32", alt=F("b32", 1) + 1), tw("Amaz", "b32", alt=F("b32", 1) + 3.5), E("b34") + 4, y=0.4, r=0.1, fluxo=True, vel=0.1)
for nm, xz, tp in [("FORTALEZA", FOR, S("b32") + 0.3), ("BELÉM", BEL, tw("Amaz", "b32", alt=F("b32", 1) + 1)), ("MANAUS", MAN, tw("Amaz", "b32", alt=F("b32", 1) + 3))]:
    rot(nm, [xz[0], xz[1] - 0.8], tp, E("b32"), "mapa")
num(tw("cinco", "b32", alt=F("b32", 2) + 1), de=0, para=4963, dur=1.5, faixa="PARA O AMAZONAS · JUN/1877 → AGO/1878 · PASSAGEM PAGA PELO GOVERNO")
num_off(E("b32") + 0.4)
foto("seringal-acre-1910.jpg", F("b32", 2) + 0.3, E("b32") + 0.4, lado="dir")
# b33 Acre
est("b33", "B"); tab(quente, S("b33"), 0.0, 0.3)
cam(S("b33"), P(-64, -8), 30, 54, 0, corte=True); cam(E("b33"), ACRE, 22, 56, 8)
seta("#FFE9C7", r3, S("b33"), S("b33") + 2.5, E("b34") + 4, y=0.4, r=0.1, fluxo=True, vel=0.1)
t_ac = tw("Acre", "b33", alt=F("b33", 1) + 0.5); t_1903 = tw("três|tres|1903", "b33", apos=F("b33", 2) - 0.3, alt=F("b33", 3))
tintas.append({"ufs": ["12"], "cor": "#9CC3E4", "op": janela_op(t_ac, t_1903, 1, 0.6, 0.3), "max": 0.8})
tintas.append({"ufs": ["12"], "cor": "#E8505B", "op": janela_op(t_1903, E("b34") + 5, 1, 0.6, 0.8), "max": 0.85})
rot("ACRE · BOLÍVIA", [ACRE[0], ACRE[1] - 1.0], t_ac, t_1903, "fria"); rot("ACRE · BRASIL · 1903", [ACRE[0], ACRE[1] - 1.0], t_1903, E("b34") + 4, "corredor")
rot("SERINGUEIROS NORDESTINOS", [ACRE[0] + 3, ACRE[1] + 1.5], S("b33") + 0.5, F("b33", 2), "seta")
cartao(t_1903 + 0.2, t_1903 + 3.2, "TRATADO DE PETRÓPOLIS", "1903", top=330)
foto("seringueiro-acre-2010.jpg", F("b33", 1) + 0.3, F("b33", 1) + 4.0, lado="esq", fmt="pol")
# b34
cam(S("b34"), BRC, 56, 56, 0); cam(E("b34"), BRC, 60, 60, 4)
fios += [{"pontos": [FOR, ACRE], "t0": S("b34") + 0.4, "t1": S("b34") + 2.4, "t2": E("b34") + 4, "grosso": 4}]
pino("f_ce", "CEARÁ", "", S("b34") + 0.1, xz=FOR, ate=E("b34") + 4); pino("f_ac", "ACRE", "", S("b34") + 0.8, xz=ACRE, ate=E("b34") + 4)
rot("A SECA AJUDOU A DESENHAR A FRONTEIRA", [P(-58, -3)[0], P(-58, -3)[1]], S("b34") + 1.0, E("b34"), "corredor")
# b35 campos
trans(S("b35") - 0.1, "corte", 0.5, "corte seco para o mapa sépia"); tab(arquivo, S("b35") - 0.2, 0.7, 0.1); tab(arquivo, E("b35") + 0.3, 0.0, 0.2)
est("b35", "B"); cam(S("b35"), CE, 14, 58, 0, corte=True); cam(E("b35"), CE, 12, 56, 6)
tintas.append({"ufs": ["23"], "cor": "#6b3b2a", "op": janela_op(S("b35"), E("b35"), 1, 0.5, 0.5), "max": 0.7})
campos = [("FORTALEZA", FOR), ("FORTALEZA ", [FOR[0] + 0.25, FOR[1] - 0.2]), ("SENADOR POMPEU", P(-39.37, -5.59)), ("CRATO", CRA), ("QUIXERAMOBIM", P(-39.29, -5.2)), ("CARIÚS", P(-39.49, -6.53)), ("IPU", P(-40.71, -4.32))]
for k, (nm, xz) in enumerate(campos[:7]):
    pino(f"c{k}", nm.strip() + " · 1932", "", tw("sete|7", "b35", alt=F("b35", 2)) + 0.2 * k, xz=xz, ate=E("b35"), pequeno=True, cor="#6b3b2a")
pino("c15", "ALAGADIÇO · 1915", "", tw("1915|quinze", "b35", alt=F("b35", 0) + 1), xz=P(-38.6, -3.8), ate=E("b35"), cor="#6b3b2a")
rot("CURRAIS DO GOVERNO", [CE[0], CE[1] - 1.8], tw("currais", "b35", alt=F("b35", 1)), E("b35"), "corredor")
num(tw("sete|7", "b35", alt=F("b35", 2)), "+70 MIL", "7 CAMPOS EM 1932 · CERCADOS PARA NÃO CHEGAR A FORTALEZA")
num_off(E("b35") + 0.3)
# b36 semiárido
est("b36", "B"); tab(arquivo, S("b36") - 0.1, 0.0, 0.1); trans(S("b36") - 0.1, "corte", 0.5, "corte seco de volta ao mapa")
cam(S("b36"), NE, 34, 56, 0, corte=True); cam(E("b36"), NE, 30, 56, 6)
for r_ in ring(SEMI["features"][0]):
    regioes.append({"anel": [P(lo, la) for lo, la in r_], "cor": "#E9C46A", "op": janela_op(S("b36") + 0.3, E("b37") + 4, 1, 0.8, 0.8), "max": 0.45, "y": 0.45})
cartao(tw("1909", "b36", alt=F("b36", 0) + 0.3) - 0.1, E("b36") + 0.1, "1909 · INSPETORIA DE OBRAS CONTRA AS SECAS", "VIROU O DNOCS", top=700)
rot("SEMIÁRIDO", L(-41, -8.5), S("b36") + 0.6, E("b36") + 4, "mapa_grande")
# b37 fichas
cam(S("b37"), CE, 22, 54, 0); cam(E("b37"), CE, 20, 56, 8)
graficos.append({"tipo": "legenda", "t0": 0, "t1": 0, "titulo": "", "fonte": "", "itens": []})
papel("b37", "b37", [] , pre=-2) if False else None
checklists = [{"t0": round(F("b37", 2) + 0.2, 3), "t1": round(tw("secas", "b37", n=1, alt=F("b37", 5)) - 0.3, 3), "titulo": "POR QUE QUASE NINGUÉM FALA", "itens": [["Os mortos eram pobres do sertão", tw("pobres", "b37", alt=F("b37", 2))], ["Longe da capital", tw("longe", "b37", alt=F("b37", 2) + 1)], ["Corpos sem contagem", tw("corpos", "b37", alt=F("b37", 3))], ["Investigação barrada", tw("barrada", "b37", alt=F("b37", 4))]]}]
graficos3.append({"tipo": "secas", "t0": tw("secas", "b37", n=1, alt=F("b37", 5)) - 0.2, "t1": E("b37") + 0.6, "a0": 1870, "a1": 2020, "titulo": "AS SECAS SEGUINTES REPETIRAM O ROTEIRO", "fonte": "HISTORIOGRAFIA; DNOCS",
    "eventos": [[1877, "1877", tw("secas", "b37", n=1, alt=F("b37", 5)), True], [1915, "1915", tw("secas", "b37", n=1, alt=F("b37", 5)) + 0.7, False], [1932, "1932", tw("secas", "b37", n=1, alt=F("b37", 5)) + 1.4, False], [1958, "1958", tw("secas", "b37", n=1, alt=F("b37", 5)) + 2.1, False], [1983, "1983", tw("secas", "b37", n=1, alt=F("b37", 5)) + 2.8, False], [2012, "2012", tw("secas", "b37", n=1, alt=F("b37", 5)) + 3.5, False]]})

# ======================= 4/4 E EM 2026 =======================
est("b38", "A"); trans(meio("b37", "b38"), "nuvem", 1.3, "zoom-out orbital até o globo de hoje")
cx_estados += [{"t": S("b38") - 0.3, "modo": "grande", "ativa": 3, "feitas": [1, 2, 3], "volta": True}, {"t": E("b38") + 0.3, "modo": "compacta", "ativa": 3, "feitas": [1, 2, 3]}]
cam(meio("b37", "b38") + 0.2, GLOBO, 30, 8, 0, y=7.0, corte=True); cam(E("b38"), GLOBO, 26, 10, 6, y=7.0)
globos.append({"img": "sat/globo-2026.jpg", "x": GLOBO[0], "y": 7.0, "z": GLOBO[1], "r": 7.0, "rot0": 0, "vel": 0.0, "op": janela_op(S("b38") - 0.3, E("b38") + 0.6, 1, 0.3, 0.3), "rot": [[0, 1.13], [S("b38"), 1.13], [E("b38"), 1.0]]})
# b39 Pacífico 1877 x 2026
est("b39", "A"); cam(S("b39") - 0.1, PACC, 58, 56, -6, corte=True); cam(F("b39", 2), P2(215, 0), 44, 48, 4); cam(E("b39") - 3.0, MONT, 32, 14, 0, y=2.8)
t_26 = tw("nível|nivel", "b39", alt=F("b39", 2))
relevos.append({**gpac, "y0": 0.03, "k": 0.45, "mostra_data": False, "idx": [[0, I1877]], "op": janela_op(S("b39") - 0.2, t_26 + 0.5, 1, 0.8, 0.5)})
relevos.append({**gpac, "y0": 0.03, "k": 0.45, "mostra_data": False, "idx": [[0, I2026]], "op": janela_op(t_26, F("b39", 3) + 0.5, 1, 0.8, 0.5), "cresce": [[0, 0], [t_26, 0], [t_26 + 2.5, 1]]})
rot("PACÍFICO · DEZ/1877", P2(215, 12), S("b39") + 0.8, t_26 + 0.3, "corredor"); rot("PACÍFICO · OUT/2026", P2(215, 12), t_26 + 0.5, F("b39", 3), "quente")
t_mt2 = F("b39", 3) - 0.3
for k, (ano, v) in enumerate([("1877-78", 2.53), ("OUT/2026", 3.06)]):
    montanhas.append({"nome": ano, "x": MONT[0] + (k - 0.5) * 6.0, "z": MONT[1], "r": 1.8, "kh": KH, "cor": "#E8505B" if k else "#DCCDB0", "h": [[0, 0], [t_mt2 + 0.6 * k, 0], [t_mt2 + 1.4 + 1.8 * k, v]], "op": janela_op(t_mt2, E("b39") + 0.4, 1, 0.5, 0.6), "acende": [[0, 0], [t_mt2 + 0.6 * k, 1], [t_mt2 + 2 + k, 0.2]]})
cartao(tw("previsão|previsao", "b39", alt=F("b39", 3)) + 0.3, E("b39") + 0.3, "PREVISÃO NOV–DEZ–JAN · INMET", "CHUVA ABAIXO DA MÉDIA EM ÁREAS DO NORDESTE", top=200)
# b40 
est("b40", "B"); trans(S("b40") - 0.2, "whip", 0.6, "whip pan para o Ceará e o Atlântico")
cam(S("b40") - 0.1, [CE[0] + 3, CE[1]], 30, 54, 0, corte=True); cam(E("b40"), CE, 20, 54, 6)
graficos3.append({"tipo": "meses", "t0": S("b40") + 0.5, "t1": E("b40") + 0.4, "t_chuva": tw("fevereiro", "b40", alt=F("b40", 1)), "titulo": "2027: AINDA É CEDO", "centro": "FEV–MAI ?", "fonte": "FUNCEME", "duvida": True})
seta("#FFFFFF", [P(-45, 0.5), P(-38, 1.0), P(-30, 0.8)], S("b40") + 0.5, S("b40") + 2.5, E("b40"), y=0.6, r=0.3, fluxo=True, vel=0.1, semCabeca=True)
rot("O QUE DECIDE: FEV–MAI 2027", [CE[0] - 2.0, CE[1] - 1.8], F("b40", 1), E("b40"), "corredor"); rot("FUNCEME: AINDA É CEDO", [CE[0] + 0.3, CE[1] + 1.8], tw("Funceme", "b40", alt=F("b40", 3)), E("b40"), "seta")
# b41 Monitor
est("b41", "B"); cam(S("b41"), NE, 34, 56, 0, corte=True); cam(E("b41"), NE, 30, 56, 6)
feat = {f["properties"]["categoria"]: f for f in MON["features"]}
for cat, cor in [("S0", "#F2D16B"), ("S1", "#E9A23B"), ("S2", "#D9642A")]:
    if cat in feat:
        for r_ in [p[0] for p in ([feat[cat]["geometry"]["coordinates"]] if feat[cat]["geometry"]["type"] == "Polygon" else feat[cat]["geometry"]["coordinates"])]:
            if r_ and -48 < r_[0][0] < -34 and -18 < r_[0][1] < -1:
                regioes.append({"anel": [P(lo, la) for lo, la in r_], "cor": cor, "op": janela_op(S("b41") + 0.3, E("b41") + 0.5, 1, 0.7, 0.6), "max": 0.55, "y": 0.5})
num(tw("noventa|96", "b41", alt=F("b41", 2)), "96%", "DO TERRITÓRIO DO NORDESTE COM SECA · SET/2026 · MONITOR DE SECAS")
num_off(E("b41") + 0.3)
# b42 hoje
est("b42", "A"); cam(S("b42"), CE, 20, 38, 0, corte=True); cam(E("b42"), [CE[0] + 1, CE[1]], 15, 36, 10)
cist = [[CE[0] + math.cos(i * 2.1) * (0.3 + (i % 11) * 0.28), CE[1] + math.sin(i * 1.3) * (0.3 + (i % 9) * 0.22)] for i in range(110)]
pontos.append({"lista": cist, "t0": tw("cisternas", "b42", alt=F("b42", 3)), "t1": tw("cisternas", "b42", alt=F("b42", 3)) + 3.0, "t2": E("b43")})
num(tw("milhão|milhao|1,2", "b42", alt=F("b42", 3)), "1,2 MILHÃO", "DE CISTERNAS DE ÁGUA DA CHUVA · ASA/P1MC")
num_off(F("b42", 5))
CAST = P(-38.47, -5.52); rot("CASTANHÃO", CAST, tw("Castanhão", "b42", alt=F("b42", 5)), E("b42"), "corredor"); rot("TRANSPOSIÇÃO · 2020", P(-38.9, -7.0), tw("transposição|transposicao", "b42", alt=F("b42", 6)), E("b43"), "seta")
foto("hoje-castanhao.jpg", tw("Castanhão", "b42", alt=F("b42", 5)) + 0.2, tw("Castanhão", "b42", alt=F("b42", 5)) + 4.2, lado="esq"); foto("hoje-transposicao-jati.jpg", tw("transposição|transposicao", "b42", alt=F("b42", 6)) + 0.2, E("b42") + 0.2, lado="dir")
# b43 linha do tempo
est("b43", "B"); cam(S("b43"), CE, 22, 54, 0, corte=True); cam(E("b43"), CE, 20, 56, 8)
graficos3.append({"tipo": "secas", "t0": S("b43") + 2.0, "t1": tw("pipa|carro", "b43", alt=F("b43", 2)) - 0.1, "a0": 1870, "a1": 2020, "titulo": "SECAS DO NORDESTE · SÓ EM 1877 MORTES EM MASSA", "fonte": "HISTORIOGRAFIA",
    "eventos": [[1877, "1877", S("b43") + 2.2, True], [1915, "1915", S("b43") + 2.7, False], [1932, "1932", S("b43") + 3.2, False], [2012, "2012–17", tw("2012|dois", "b43", alt=F("b43", 1)) + 0.2, False]]})
foto("hoje-pipa-caninde-2026.jpg", tw("pipa|carro", "b43", alt=F("b43", 2)), tw("pipa|carro", "b43", alt=F("b43", 2)) + 4.2, lado="dir")
# b44
est("b44", "A"); cam(S("b44"), CE, 18, 30, -20, corte=True); cam(E("b44"), CE, 14, 32, 20); tab(quente, S("b44"), 0.5, 0.8)
for k, (txt, w) in enumerate([("ÁGUA RACIONADA", "racionada"), ("COLHEITA PERDIDA", "colheita"), ("GADO VENDIDO ÀS PRESSAS", "gado"), ("CALOR", "calor")]):
    rot(txt, [CE[0] + (-1.6 if k % 2 == 0 else 1.6), CE[1] - 0.8 + k * 0.7], tw(w, "b44", alt=F("b44", 1) + 0.3 * k), E("b44"), "quente")
# b45 reprise
est("b45", "A"); trans(S("b45") - 0.3, "nuvem", 1.3, "zoom-out para o plano do hook"); tab(quente, S("b45"), 0.55, 0.5)
cx_estados += [{"t": F("b45", 2), "modo": "final", "ativa": 0, "feitas": [1, 2, 3, 4]}]
cam(S("b45") - 0.2, NE, 30, 50, 0, corte=True); cam(F("b45", 1), [FOR[0] - 0.4, FOR[1] + 1.0], 9, 36, 6); cam(E("b45"), [FOR[0] + 0.5, FOR[1] + 0.5], 8, 40, 12)
rios_retirantes(F("b45", 1) - 0.4, E("b46"))
pino("for2", "FORTALEZA · 1878", "", S("b45") + 0.5, xz=FOR, ate=E("b45"))
num(F("b45", 1) + 0.5, de=25000, para=100000, dur=2.0, faixa="25 MIL → MAIS DE 100 MIL")
num_off(F("b45", 2))
for k, (nm, xz, w) in enumerate([("PACÍFICO", P(-60, -2), "El|Niño|Nino"), ("ATLÂNTICO", P(-30, 4), "Atlântico|Atlantico"), ("GOVERNO", P(-47, -15.8), "governo|país|pais")]):
    pino(f"r{k}", nm, "", tw(w, "b45", n=0, alt=F("b45", 3) + 0.7 * k), xz=xz, ate=E("b45") + 0.5)
fios += [{"pontos": [P(-60, -2), P(-30, 4)], "t0": F("b45", 4), "t1": F("b45", 4) + 1.0, "t2": E("b45") + 0.5, "grosso": 3}, {"pontos": [P(-30, 4), P(-47, -15.8)], "t0": F("b45", 4) + 0.5, "t1": F("b45", 4) + 1.5, "t2": E("b45") + 0.5, "grosso": 3}]
# b46
est("b46", "A"); cam(S("b46") - 0.1, [P(-50, -7)[0], P(-50, -7)[1]], 60, 50, 0, corte=True); cam(E("b46"), P(-52, -8), 58, 52, 6)
seta("#E8505B", linha_trilho("EF Baturité: Fortaleza–Quixadá"), tw("trilhos", "b46", alt=S("b46") + 0.3), tw("trilhos", "b46", alt=S("b46") + 0.3) + 1.5, E("b46") + 3, y=0.3, r=0.12, semCabeca=True)
pino("cedro2", "AÇUDE DO CEDRO", "", tw("açude|acude", "b46", alt=F("b46", 1)), xz=CEDRO, ate=E("b46")); pino("acre2", "ACRE", "", tw("Acre", "b46", alt=F("b46", 2)), xz=ACRE, ate=E("b46"))
seta("#FFE9C7", r1 + r2 + r3, tw("empurrou", "b46", alt=F("b46", 2)), tw("empurrou", "b46", alt=F("b46", 2)) + 2.0, E("b46") + 3, y=0.4, r=0.1, fluxo=True, vel=0.1, semCabeca=True)
cartao(tw("Mas", "b46", alt=F("b46", 4)) - 0.1, E("b46") + 0.2, "O QUE TRANSFORMA SECA EM TRAGÉDIA", "É O QUE SE FAZ ANTES DELA", top=300)
# b47 fecho
est("b47", "B"); cam(S("b47"), [FOR[0], FOR[1]], 14, 46, 0, corte=True); cam(E("b47"), CE, 22, 52, 10)
cta = {"t0": S("b47") + 0.1, "t_inscreve": tw("inscreve", "b47", alt=F("b47", 1)) - 0.2, "texto": "MANDA PRA QUEM TEM FAMÍLIA NO SERTÃO", "inscreve": "INSCREVA-SE · EM RELEVO"}

fontes = [
    {"t": 0, "texto": "FONTES: THEOPHILO · CENSO DE 1872 · ESTIMATIVAS DE HISTORIADORES · MAPA: IBGE / NATURAL EARTH"},
    {"t": S("b09") - 0.5, "texto": "FONTES: GHCN V2 (NOAA) · FUNCEME · RELEVO: NOAA ETOPO 2022"},
    {"t": S("b19") - 0.5, "texto": "FONTES: NOAA ERSSTV5 (RECONSTRUÇÃO ANTES DE 1900: PADRÃO DE GRANDE ESCALA) · NOAA/CPC"},
    {"t": S("b25") - 0.5, "texto": "FONTES: HISTORIOGRAFIA · AGÊNCIA SENADO · OPENSTREETMAP (RIOS E TRILHOS, TRAÇADO APROXIMADO)"},
    {"t": S("b36") - 0.5, "texto": "FONTES: IBGE / SUDENE (SEMIÁRIDO, 2022) · HISTORIOGRAFIA"},
    {"t": S("b38") - 0.5, "texto": "FONTES: NOAA ERSSTV5 · INMET · FUNCEME · MONITOR DE SECAS (ANA, SET/2026) · ASA"},
]
texturas = sorted({g["img"] for g in globos})
extra = [{"t": round(e["t"] + 5.0, 3), "modo": "oculto"} for e in cx_estados if e["modo"] == "compacta"]
cx_estados = sorted(cx_estados + extra, key=lambda e: e["t"])
cues = {
    "_doc": "Gerado por shared/build_cues.py (não editar à mão). Tempos em segundos de audio/narracao.wav.",
    "fps": 30, "duracao": tempos["duracao"], "fim_fala": tempos["blocos"][-1]["e"], "slot": None, "voz": tempos.get("voz"),
    "paleta": {"papel": "#E9DCC3", "coral": "#E8505B", "navy": "#1F2A44", "tinta": "#2B2622", "branco": "#FBF8F1"},
    "palavras": palavras, "capitulos": capitulos, "numero": sorted(numero, key=lambda n: n["t"]), "camera": camera,
    "luz": sorted(luz), "noite": noite, "quente": quente, "amazonia": amazonia, "andes": andes_t, "arquivo": arquivo, "tremor": tremor, "desfoque": desfoque,
    "pinos": pinos, "destaques": destaques, "fios": fios, "funis": [], "setas": setas, "nuvens": nuvens, "regioes": regioes, "rastros": [],
    "sats": [], "ciclones": [], "aneis": [], "supercelula": None, "rotulos_mapa": rotulos,
    "relevos": relevos, "diorama": None, "montanhas": montanhas, "barras3d": [], "globos": globos, "fumacas": [], "chuvas": [],
    "cilindros": cilindros, "pontos": pontos, "tintas": tintas, "sst_datas": SST["datas"],
    "midia": midia, "manchetes": manchetes, "cartoes": cartoes, "graficos": graficos, "graficos3": graficos3, "papeis": papeis, "checklists": checklists, "calendario": None,
    "pergunta": {"t0": 9999, "t1": 9999, "texto": ""}, "caixas": {"itens": cx_itens, "estados": cx_estados}, "cortica": {"t0": 9999, "t1": 9999, "itens": []}, "cobre3d": [],
    "thumbs": {"A": round(F("b04", 1), 3), "B": round(F("b34", 1) + 2.0, 3), "C0": round(S("b39") + 3.5, 3), "C1": round(t_26 + 3.8, 3)},
    "transicoes": sorted(transicoes, key=lambda x: x["t"]), "cta": cta, "fontes": fontes, "texturas": texturas,
}
cues["camera"].sort(key=lambda k: k["t"]); cues["rotulos_mapa"] = rotulos
cues["rotulos"] = rotulos
json.dump(cues, open(A / "cues.json", "w"), ensure_ascii=False, separators=(",", ":"))
tr = []; ant = None
for t_, e_ in sorted(ESTILO):
    if e_ != ant: tr.append({"t": round(t_, 3), "e": e_}); ant = e_
json.dump({"_doc": "A/B do longo-03 (build_cues.py): troca no corte de câmera", "trechos": tr}, open(A / "estilo_v2.json", "w"), ensure_ascii=False, indent=1)
(R / "work").mkdir(exist_ok=True)
with open(R / "work/storyboard.txt", "w") as f:
    for tr_ in cues["transicoes"]: f.write(f"TRANSIÇÃO {tr_['t']:7.2f}s {tr_['tipo']}: {tr_['desc']}\n")
    for m in midia: f.write(f"MÍDIA {m['t0']:7.2f}–{m['t1']:7.2f}s {m['id']} ({m['lado']})\n")
    f.write("\n".join(avisos))
print(f"ok: {len(palavras)} palavras, {len(camera)} chaves de câmera, {len(midia)} mídias, {len(transicoes)} transições, {len(relevos)} relevos, {len(papeis)} papéis")
print("avisos:", *avisos, sep="\n  ")
