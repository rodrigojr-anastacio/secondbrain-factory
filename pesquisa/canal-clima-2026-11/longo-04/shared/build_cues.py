# Storyboard em código do longo 04 (Em Relevo, 1983: o El Niño que partiu o Brasil ao meio): gera shared/cues.json e shared/estilo_v2.json
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
def cartao(t0, t1, rotulo, texto, carimbo=None, t_carimbo=None, top=300):
    c = {"t0": round(t0, 3), "t1": round(t1, 3), "rotulo": rotulo, "texto": texto, "top": top}
    if carimbo: c["carimbo"] = {"texto": carimbo, "t": round(t_carimbo, 3)}
    cartoes.append(c)
def trans(t, tipo, dur=1.0, desc=""): transicoes.append({"t": round(t, 3), "tipo": tipo, "dur": dur, "desc": desc})
def papel(b0, b1, itens, pre=0.0, topo=False): papeis.append({"t0": round(S(b0) - pre, 3), "t1": round(E(b1) + 0.25, 3), "itens": itens, "topo": topo})
def meio(b1, b2): return (E(b1) + S(b2)) / 2
luz = [[0, 1]]; noite = [[0, 0]]; quente = [[0, 0]]; amazonia = [[0, 0]]; andes_t = [[0, 0]]; arquivo = [[0, 0]]; tremor = [[0, 0]]; desfoque = [[0, 0]]
def tab(lista, t, v, dur=0.6): lista.append([round(t, 3), lista[-1][1]]); lista.append([round(t + dur, 3), v])
ESTILO = []   # (t, 'A'|'B')
def est(b, e): ESTILO.append((max(0, S(b) - 0.4) if b != "b01" else 0, e))

# ======================= Em Relevo 004 (1983): dados e lugares =======================
FOTOS = {
    "landsat4-uv-19830703-par.jpg": {"legenda_tela": "UNIÃO DA VITÓRIA · LANDSAT 4 · 3 JUL 1983"},
    "blumenau-aerea-2010.jpg": {"legenda_tela": "BLUMENAU · CENTRO E RIO ITAJAÍ-AÇU · 2010"},
    "acude-seco-santa-quiteria-ce-2018.jpg": {"legenda_tela": "AÇUDE SECO · SANTA QUITÉRIA (CE) · 2018"},
    "retirantes-pernambuco-slide-janjao-sem-data.jpg": {"legenda_tela": "RETIRANTES · PERNAMBUCO · FOTO DE ACERVO (SEM DATA)"},
    "uniao-da-vitoria-vista-aerea-2009.jpg": {"legenda_tela": "UNIÃO DA VITÓRIA · RIO IGUAÇU · 2009"},
    "porto-uniao-centro-2014.jpg": {"legenda_tela": "UNIÃO DA VITÓRIA E PORTO UNIÃO · 2014"},
    "blumenau-rio-itajai-acu-2006.jpg": {"legenda_tela": "BLUMENAU · RIO ITAJAÍ-AÇU EM ESTIAGEM · 2006"},
    "blumenau-enchente-2008-exercito-NAO-1983.jpg": {"legenda_tela": "BLUMENAU · ENCHENTE DE 2008"},
    "acude-coremas-seco-2017.jpg": {"legenda_tela": "AÇUDE DE COREMAS (PB) · SECA · 2017"},
    "sertao-caatinga-arido-2013.jpg": {"legenda_tela": "SERTÃO · CAATINGA NA ESTIAGEM · 2013"},
    "elnino-1982-83-anomalia-temp-pacifico-jan1983.jpg": {"legenda_tela": "PACÍFICO · JAN 1983"},
    "noaa-cpc-elnino-impactos-globais-jun-ago.jpg": {"legenda_tela": "NOAA · IMPACTOS DO EL NIÑO · JUN–AGO"},
    "uniao-da-vitoria-rio-iguacu-helicoptero-2016.jpg": {"legenda_tela": "UNIÃO DA VITÓRIA · RIO IGUAÇU · 2016"},
    "sobradinho-represa-seca-2015.jpg": {"legenda_tela": "SOBRADINHO (BA) · RESERVATÓRIO BAIXO · 2015"},
}
IGU = json.load(open(R / "dados/iguacu-uv-1982-83.json"))
DIAS = sorted(IGU["dias"]); IDX = {d: i for i, d in enumerate(DIAS)}; NDIA = len(DIAS)
def di(d): return IDX[d]
MOMB = json.load(open(R / "dados/mombaca-anual.json"))
roni = {}
for ln in open(R / "dados/roni.txt").read().split("\n")[1:]:
    p = ln.split()
    if len(p) == 3: roni[(p[0], int(p[1]))] = float(p[2])
def rmax(a, b): return max(v for (s, y), v in roni.items() if a <= y <= b)
MES_SEAS = {"DJF": 1, "JFM": 2, "FMA": 3, "MAM": 4, "AMJ": 5, "MJJ": 6, "JJA": 7, "JAS": 8, "ASO": 9, "SON": 10, "OND": 11, "NDJ": 12}
# RONI sazonal -> índice de dia (centro do trimestre), de out/1982 a set/1983
RONI_DIA = []
for (s, y), v in sorted(roni.items(), key=lambda kv: (kv[0][1], MES_SEAS[kv[0][0]])):
    m = MES_SEAS[s]; ano = y if s != "NDJ" else y
    ano_c = y + (1 if s == "NDJ" else 0) if False else y
    d = f"{ano_c}-{m:02d}-15"
    if d in IDX: RONI_DIA.append([IDX[d], round(v, 2)])
UV = P(-51.09, -26.23); BLU = P(-49.07, -26.92); MOM = P(-39.63, -5.75); CAN = P(-39.32, -4.35); FOR = P(-38.54, -3.72)
CE = P(-39.4, -5.3); NE = P(-40.5, -8.0); BRC = [0.8, -17.5]; SUL_C = P(-51.5, -27.0); CUR = P(-49.27, -25.43)
IGUACU = [P(-49.27, -25.45), P(-49.9, -25.55), P(-50.38, -25.87), P(-51.09, -26.23), P(-51.7, -26.0), P(-52.6, -25.6), P(-53.2, -25.55), P(-54.0, -25.6), P(-54.43, -25.69)]
VARZEA = [P(-51.20 - 0.14, -26.12 + 0.08), P(-50.95 + 0.12, -26.12 + 0.1), P(-50.90 + 0.16, -26.28 - 0.02), P(-51.10, -26.36 - 0.12), P(-51.25 - 0.14, -26.28 - 0.02)]
SULUF = ["41", "42", "43"]; NEUF = ["21", "22", "23", "24", "25", "26", "27", "28", "29"]
AZUL = "#39B0F5"; CORAL = "#E8505B"
PACC = P2(195, 0); MONT = [PAC["x0"], 34.0]
def grade_xy(lon0, lon1, lat0, lat1):
    i0, i1 = int(lon0 - SST["lon0"]), int(lon1 - SST["lon0"]); j0, j1 = int(lat0 - SST["lat0"]), int(lat1 - SST["lat0"])
    xs = [P2(SST["lon0"] + i, 0)[0] for i in range(i0, i1 + 1)]; zs = [P2(200, SST["lat0"] + j)[1] for j in range(j0, j1 + 1)]
    return {"i0": i0, "i1": i1, "j0": j0, "j1": j1, "xs": xs, "zs": zs}
def partida(t0, t1, fade=0.8):
    tintas.append({"ufs": SULUF, "cor": AZUL, "op": janela_op(t0, t1, 1, fade, fade), "max": 1.0})
    tintas.append({"ufs": NEUF, "cor": CORAL, "op": janela_op(t0, t1, 1, fade, fade), "max": 0.8})
def g4(**k): graficos4.append({**k, "t0": round(k["t0"], 3), "t1": round(k["t1"], 3)})
graficos4 = []
cobre = []
def ts_idx(d): return di(d)

# ======================= HOOK =======================
est("b01", "A"); tab(luz, 0, 0.8, 0.1); tab(quente, 0, 0.0, 0.1)
cam(0.0, [UV[0] + 2.0, UV[1] - 2.5], 12, 24, -20, y=0.3); cam(F("b01", 1), [UV[0] + 0.3, UV[1] - 0.3], 7.0, 32, -6); cam(F("b01", 3), [UV[0], UV[1]], 5.2, 38, 8); cam(E("b01") - 0.2, [UV[0], UV[1]], 4.6, 40, 14)
pino("uv", "UNIÃO DA VITÓRIA (PR)", "JULHO DE 1983", 0.5, t2=E("b01") + 0.6, xz=UV, y0=0.1, ate=E("b01") + 0.2)
foto("landsat4-uv-19830703-par.jpg", 0.4, 3.4, lado="dir")
seta(AZUL, IGUACU, 3.4, 5.5, E("b01") + 3, y=0.14, r=0.05, fluxo=True, vel=0.16, semCabeca=True)
t_rg = F("b01", 1)
cilindros.append({"x": UV[0] + 0.55, "z": UV[1] - 0.25, "r": 0.08, "h": 1.1, "cor": "#3D7FB8", "cor_marca": "#E8505B", "marca": 6.0 / 12.0, "t_marca": t_rg,
    "op": janela_op(t_rg - 0.2, S("b02") + 0.3, 1, 0.5, 0.5), "nivel": [[0, 0.2], [t_rg, 2.5 / 12], [tw("dezoito|18", "b01", n=0, apos=F("b01", 2), alt=F("b01", 2) + 1.0) - 0.8, 2.5 / 12], [tw("dezoito|18", "b01", n=0, apos=F("b01", 2), alt=F("b01", 2) + 1.0) + 1.2, 10.42 / 12]]})
t_ag = tw("cobriu", "b01", alt=F("b01", 3))
regioes.append({"anel": VARZEA, "cor": AZUL, "op": janela_op(t_ag - 0.5, E("b02") + 0.3, 1, 0.9, 0.7), "max": 0.55, "y": 0.12})
num(t_rg + 0.2, valor="2,5", faixa="UNIÃO DA VITÓRIA · NÍVEL NORMAL DO IGUAÇU", unidade="m")
t_dz = tw("dezoito|18", "b01", n=0, apos=F("b01", 2), alt=F("b01", 2) + 1.0)
num(t_dz - 0.2, de=2.5, para=10.42, dur=1.6, faixa="18 JUL 1983 · COTA DO RIO IGUAÇU · ANA", unidade="m", dec=2)
num_off(E("b01") + 0.1)
# b02 Blumenau
est("b02", "A"); trans(S("b02") - 0.15, "whip", 0.6, "whip pan para leste")
cam(S("b02") - 0.1, [BLU[0] - 0.4, BLU[1] - 0.2], 6.0, 34, -50, corte=True); cam(F("b02", 1), [BLU[0], BLU[1]], 4.6, 30, -20); cam(E("b02"), [BLU[0] + 0.1, BLU[1]], 4.0, 34, 10)
pino("blu", "BLUMENAU (SC)", "JULHO DE 1983", S("b02") + 0.3, xz=BLU, ate=E("b02") + 0.2)
cilindros.append({"x": BLU[0] + 0.45, "z": BLU[1] - 0.2, "r": 0.08, "h": 1.2, "cor": "#3D7FB8", "cor_marca": "#E8505B", "marca": 10.0 / 16, "t_marca": S("b02"),
    "op": janela_op(S("b02"), E("b02") + 0.4, 1, 0.5, 0.5), "nivel": [[0, 0.1], [S("b02") + 0.3, 0.1], [tw("quinze|15", "b02", alt=F("b02", 0) + 2.5), 15.34 / 16]]})
foto("blumenau-aerea-2010.jpg", tw("Blumenau", "b02", alt=S("b02") + 0.2) + 0.3, tw("Blumenau", "b02", alt=S("b02") + 0.2) + 3.6, lado="esq")
num(tw("quinze|15", "b02", alt=F("b02", 0) + 2.0), de=10, para=15.34, dur=1.4, faixa="BLUMENAU · 9 JUL 1983 · RIO ITAJAÍ-AÇU", unidade="m", dec=2)
num_off(F("b02", 2) - 0.2)
cartao(F("b02", 1) + 0.3, E("b02") + 0.2, "ITAJAÍ-AÇU · 1983", "3ª CHEIA DO ANO · FALTAVA A 4ª", top=650)
# b03 Mombaça
est("b03", "A"); trans(S("b03") - 0.2, "nuvem", 1.3, "zoom-out do Sul até o Brasil e mergulho no Ceará")
cam(S("b03") - 0.2, BRC, 64, 54, 0, corte=True); cam(F("b03", 1), NE, 34, 50, 4); cam(F("b03", 2) - 0.1, [MOM[0], MOM[1]], 8.5, 34, 12); cam(E("b03"), [MOM[0] + 0.3, MOM[1]], 6.5, 38, -4)
tab(quente, S("b03") + 1.5, 0.55, 0.8)
tg = tw("quilômetros|quilometros", "b03", alt=S("b03") + 1.0)
seta("#FFFFFF", [UV, [P(-46, -16)[0], P(-46, -16)[1]], MOM], tg, tg + 2.0, F("b03", 2) + 0.5, y=0.6, r=0.08, fluxo=True, vel=0.1, semCabeca=True)
rot("2.500 KM", P(-46, -16), tg + 0.8, F("b03", 2) + 0.5, "seta")
pino("mom", "MOMBAÇA (CE)", "1983", F("b03", 2), xz=MOM, ate=E("b03") + 0.2)
cilindros.append({"x": MOM[0] + 0.5, "z": MOM[1] + 0.2, "r": 0.12, "h": 1.0, "cor": "#3D7FB8", "cor_marca": "#E8505B", "marca": 1.0, "t_marca": F("b03", 2),
    "op": janela_op(F("b03", 2) + 0.3, E("b03") + 0.4, 1, 0.5, 0.5), "nivel": [[0, 0.95], [F("b03", 2) + 0.6, 0.95], [tw("metade|menos", "b03", alt=F("b03", 2) + 2.0), 0.47]]})
num(tw("metade", "b03", alt=F("b03", 2) + 2.0), valor="47%", faixa="MOMBAÇA · CHUVA DE 1983 EM RELAÇÃO À MÉDIA (366 DE 783 MM)")
num_off(F("b03", 3))
foto("acude-seco-santa-quiteria-ce-2018.jpg", F("b03", 3) + 0.2, E("b03") + 0.2, lado="dir")
rot("5º ANO DE SECA · DESDE 1979", [MOM[0] - 1.6, MOM[1] + 1.4], F("b03", 3) + 0.3, E("b03") + 0.4, "quente")
# b04 arquivo
trans(S("b04") - 0.1, "corte", 0.5, "corte seco para o papel (impacto grave)")
tab(arquivo, S("b04") - 0.2, 0.7, 0.1); tab(arquivo, E("b04") + 0.3, 0.0, 0.2)
cam(S("b04"), CAN, 7, 40, 0, corte=True); est("b04", "B")
papel("b04", "b04", [{"tipo": "data", "texto": "CANINDÉ (CE) · AGOSTO DE 1983", "t": S("b04") + 0.2},
    {"tipo": "titulo", "texto": "FLAGELADOS INVADEM ARMAZÉM DE COMIDA", "t": S("b04") + 0.6, "tam": 84},
    {"tipo": "numero", "de": 0, "para": 5000, "t": tw("cinco|5", "b04", alt=F("b04", 0) + 1.5), "dur": 1.2, "tam": 220},
    {"tipo": "rotulo", "texto": "FLAGELADOS · SEGUNDO O MEMORIAL DA DEMOCRACIA", "t": tw("flagelados", "b04", n=0, alt=F("b04", 0) + 2.0)},
    {"tipo": "carimbo", "texto": "10 MILHÕES NO NORDESTE", "t": tw("milhões|milhoes|10", "b04", apos=F("b04", 1), alt=F("b04", 1) + 1.0), "tam": 60}], pre=0.15, topo=True)
# b05 TELA PARTIDA
est("b05", "B"); tab(arquivo, S("b05") - 0.1, 0.0, 0.1); trans(S("b05") - 0.1, "corte", 0.5, "corte seco de volta ao mapa (impacto suave)")
cam(S("b05"), BRC, 78, 62, 0, corte=True); cam(E("b05"), BRC, 74, 60, 4)
partida(S("b05") + 0.2, E("b07") + 0.5)
g4(tipo="relogio", t0=S("b05") + 0.4, t1=E("b05") + 0.3, texto="1983", sub="O MESMO ANO", top=60)
rot("ÁGUA DEMAIS", P(-50.5, -25.0), tw("demais", "b05", alt=F("b05", 1) + 0.8), E("b06"), "fria")
rot("ÁGUA NENHUMA", P(-39.5, -8.5), tw("nenhuma", "b05", alt=F("b05", 1) + 2.0), E("b06"), "quente")
cartao(tw("pergunta", "b05", alt=F("b05", 2) + 2.0) - 0.6, E("b05") + 0.2, "EL NIÑO 2026", "ISSO PODE ACONTECER DE NOVO?", top=640)
# b06 4 perguntas
cx_itens = [{"n": 1, "texto": "O QUE ACONTECEU NO SUL?", "t": F("b06", 1)}, {"n": 2, "texto": "O QUE ACONTECEU NO SERTÃO?", "t": F("b06", 2)},
            {"n": 3, "texto": "POR QUE OS DOIS AO MESMO TEMPO?", "t": F("b06", 3)}, {"n": 4, "texto": "E EM 2026?", "t": F("b06", 4)}]
cx_estados = [{"t": cx_itens[0]["t"], "modo": "grande", "ativa": 0, "feitas": []}, {"t": S("b07") + 0.3, "modo": "compacta", "ativa": 0, "feitas": []}, {"t": S("b08") - 0.5, "modo": "oculto"}]
cam(S("b06"), BRC, 74, 60, 4); cam(E("b06"), BRC, 72, 58, -4)
# b07 meses
cam(S("b07") + 0.3, CE, 24, 52, 8); cam(E("b07"), BRC, 64, 56, 0)
g4(tipo="anel24", t0=S("b07") + 0.5, t1=E("b07") + 0.8, titulo="QUANDO CHOVE · SUL × SERTÃO", centro=["SUL: O ANO TODO", "SERTÃO: FEV–MAI"], fonte="INMET · FUNCEME", left=1230, top=290,
   acende=[{"i0": 0, "i1": 11, "t": tw("Sul", "b07", n=0, alt=F("b07", 1)), "cor": AZUL}, {"i0": 1, "i1": 4, "t": tw("fevereiro", "b07", alt=F("b07", 2) + 1.5), "cor": CORAL}],
   legenda=[[AZUL, "SUL: CHUVA O ANO INTEIRO (FRENTES FRIAS)", tw("Sul", "b07", n=0, alt=F("b07", 1))], [CORAL, "SERTÃO: SÓ DE FEVEREIRO A MAIO", tw("fevereiro", "b07", alt=F("b07", 2) + 1.5)]])
rot("EXTREMOS OPOSTOS", P(-45, -15), tw("extremos", "b07", alt=F("b07", 3) + 2.0), E("b07"), "seta")

# ======================= 1/4 O QUE ACONTECEU NO SUL =======================
est("b08", "A"); tab(quente, S("b08"), 0.0, 0.5); trans(meio("b07", "b08"), "nuvem", 1.3, "push-in atravessando nuvens de chuva")
cx_estados += [{"t": S("b08") - 0.3, "modo": "grande", "ativa": 0, "feitas": [], "volta": True}, {"t": F("b08", 1), "modo": "compacta", "ativa": 0, "feitas": []}]
cam(meio("b07", "b08") + 0.2, CUR, 12, 28, -30, corte=True); cam(F("b08", 1), [(CUR[0] + UV[0]) / 2, (CUR[1] + UV[1]) / 2], 11, 34, -10); cam(F("b08", 2), UV, 6.0, 40, 0); cam(E("b08"), [UV[0], UV[1]], 4.4, 44, 14)
seta(AZUL, IGUACU, S("b08") + 0.3, S("b08") + 3.0, E("b09") + 2, y=0.14, r=0.06, fluxo=True, vel=0.14, semCabeca=True)
rot("CURITIBA", [CUR[0] - 0.2, CUR[1] - 0.2], tw("Curitiba", "b08", alt=F("b08", 1) + 0.4), F("b08", 2), "seta"); rot("CATARATAS", P(-54.43, -25.69), tw("Cataratas", "b08", alt=F("b08", 1) + 2.0), F("b08", 2) + 0.3, "seta")
pino("uv3", "UNIÃO DA VITÓRIA", "", F("b08", 2), xz=UV, ate=E("b08") + 0.1)
regioes.append({"anel": VARZEA, "cor": "#FFFFFF", "op": janela_op(tw("curvas", "b08", alt=F("b08", 2) + 1.5), E("b08") + 0.2, 1, 0.6, 0.6), "max": 0.35, "y": 0.12})
foto("uniao-da-vitoria-vista-aerea-2009.jpg", tw("cresceu", "b08", alt=F("b08", 3)) - 0.3, E("b08") + 0.2, lado="dir")
# b09 hidrograma
est("b09", "B"); trans(S("b09") - 0.2, "whip", 0.6, "whip pan para o gráfico")
cam(S("b09") - 0.1, UV, 10, 50, 0, corte=True); cam(E("b11"), [UV[0] + 0.5, UV[1]], 12, 52, 10)
HI = di("1983-07-03"); HP = di("1983-07-18"); H11 = di("1983-08-10")
t_nov = tw("novembro", "b09", alt=F("b09", 1)); t_mai = tw("maio", "b09", alt=F("b09", 2)); t_jul = tw("julho", "b09", alt=F("b09", 3))
prog = [[0, 0], [S("b09") + 0.4, 0], [t_nov + 1.0, di("1982-12-31") / (NDIA - 1)], [t_mai + 1.2, di("1983-06-10") / (NDIA - 1)], [t_jul + 0.8, HI / (NDIA - 1)],
        [S("b11") + 0.3, HI / (NDIA - 1)], [S("b11") + 3.4, HP / (NDIA - 1)], [S("b11") + 6.5, di("1983-09-30") / (NDIA - 1)]]
HM = [{"t": t_nov, "i": di("1982-11-27"), "v": 6.45, "texto": "NOV/82 · 6,45 M"}, {"t": t_mai, "i": di("1983-06-01"), "v": 6.65, "texto": "MAI–JUN/83 · 6,65 M", "dx": -120},
      {"t": t_jul, "i": HI, "v": 4.94, "texto": "3 JUL · 4,94 M", "cor": "#1F2A44", "dx": -40, "dy": 64}, {"t": S("b11") + 3.2, "i": HP, "v": 10.42, "texto": "18 JUL · 10,42 M", "tam": 38}]
EIXO = [[di("1982-10-01"), "OUT/82"], [di("1983-01-01"), "JAN/83"], [di("1983-04-01"), "ABR"], [di("1983-07-01"), "JUL"], [di("1983-09-30"), "SET"]]
g4(tipo="hidro", t0=S("b09") + 0.2, t1=E("b11") + 1.5, titulo="RIO IGUAÇU EM UNIÃO DA VITÓRIA · COTA DIÁRIA (M) · OUT/1982–SET/1983", fonte="ANA (HIDROWEB, ESTAÇÃO 65310000)",
   n=NDIA, ymax=11, dias=[[i, IGUACU_V] for i, IGUACU_V in [(IDX[d], IGU["dias"][d]) for d in DIAS]], prog=prog, marcas=HM, eixo=EIXO,
   faixa={"t": S("b11") + 5.0, "i0": HP - 3, "i1": H11, "texto": "+1 MÊS ACIMA DE 6 M"}, roni=None, vertical=None, left=50, top=250)
cartao(F("b09", 3) + 1.2, E("b09") + 0.2, "3 DE JULHO", "CHEIO, MAS SOB CONTROLE", top=650)
# b10 pluviômetros
est("b10", "B")
g4(tipo="colunas", t0=S("b10") + 0.3, t1=E("b10") + 0.8, titulo="CHUVA EM MM · PARANÁ", fonte="DEFESA CIVIL DO PARANÁ", w=560, left=1330, top=240, max=850,
   itens=[["MÉDIA DE JUN + JUL JUNTOS", 138, tw("cento|138", "b10", alt=F("b10", 2)), "#7FA2C9", "138"], ["UMA SEMANA EM JUL/83", 800, tw("oitocentos|800", "b10", alt=F("b10", 1) + 0.5), CORAL, "~800"]],
   selo={"t": tw("seis|6", "b10", n=0, apos=F("b10", 3), alt=F("b10", 3) + 0.6), "texto": "QUASE 6 VEZES"})
cam(S("b10"), UV, 10, 46, 20, corte=False)
# b11
est("b11", "B")
num(tw("quinze|15", "b11", alt=F("b11", 1)), de=4.94, para=10.42, dur=2.6, faixa="IGUAÇU · EM 15 DIAS · 3 A 18 JUL 1983", unidade="m", dec=2)
num_off(F("b11", 2) + 0.2)
cartao(F("b11", 2) + 0.5, E("b11") + 0.4, "ACIMA DE 6 METROS", "POR MAIS DE UM MÊS", top=650)
# b12 inundação
est("b12", "A"); trans(S("b12") - 0.1, "corte", 0.5, "corte seco de volta ao mapa")
cam(S("b12"), [UV[0], UV[1]], 6.4, 44, -30, corte=True); cam(E("b12"), [UV[0], UV[1]], 5.4, 48, 40)
regioes.append({"anel": VARZEA, "cor": AZUL, "op": janela_op(S("b12") - 0.1, E("b13") + 0.1, 1, 0.5, 0.5), "max": 0.7, "y": 0.2})
cilindros.append({"x": UV[0] + 0.55, "z": UV[1] - 0.25, "r": 0.08, "h": 1.1, "cor": "#3D7FB8", "cor_marca": "#E8505B", "marca": 6.0 / 12, "t_marca": S("b12"),
    "op": janela_op(S("b12"), E("b12") + 0.3, 1, 0.4, 0.4), "nivel": [[0, 10.42 / 12], [E("b12"), 10.42 / 12]]})
for k, (txt, w) in enumerate([("SEM LUZ", "luz"), ("SEM ÁGUA POTÁVEL", "água|agua"), ("SEM COMIDA", "comida")]):
    rot(txt, [UV[0] - 1.2 + 1.2 * k, UV[1] - 1.1 + 0.45 * (k % 2)], tw(w, "b12", n=0, alt=S("b12") + 0.6 + 0.6 * k), F("b12", 1) + 0.3, "quente")
num(tw("quatrocentas|2.400|400", "b12", alt=F("b12", 1) + 0.6), de=0, para=2400, dur=1.4, faixa="FAMÍLIAS DESAMPARADAS · UNIÃO DA VITÓRIA · DEFESA CIVIL DO PR", unidade="+")
num_off(E("b12"))
foto("porto-uniao-centro-2014.jpg", tw("abrigos|parentes", "b12", alt=F("b12", 2)), E("b12") + 0.2, lado="dir")
# b13 antes x depois (tela cheia)
est("b13", "A")
t13 = F("b13", 1) - 0.2; t_ag4 = tw("agosto", "b13", alt=F("b13", 3) - 0.3)
g4(tipo="cortina", t0=t13, t1=E("b13") + 0.4, t_cortina=t_ag4 - 0.4, antes="fotos/landsat4-uv-19830703-par.jpg", depois="fotos/landsat4-uv-19830804-par.jpg", origem="70% 70%",
   rotA="3 JUL 1983 · RIO 4,94 M", rotB="4 AGO 1983 · RIO 7,42 M", t_seta=tw("lago|vars|varz", "b13", alt=F("b13", 5)) , seta={"x": 520, "y": 640, "texto": "A VÁRZEA VIROU UM LAGO"})
cobre.append([round(t13 - 0.5, 3), round(E("b13") + 0.5, 3)])
cam(t13, UV, 5.0, 40, 0)
# b14 Itajaí
est("b14", "A"); trans(S("b14") - 0.15, "whip", 0.6, "whip pan para leste")
cam(S("b14") - 0.1, [BLU[0] - 0.3, BLU[1] - 0.2], 5.0, 24, -35, corte=True); cam(F("b14", 2), [BLU[0], BLU[1]], 3.8, 22, 10); cam(E("b14"), [BLU[0] + 0.2, BLU[1]], 3.4, 30, 40)
rot("VALE ESTREITO · ITAJAÍ-AÇU", [BLU[0] - 0.8, BLU[1] - 0.7], tw("apertado", "b14", alt=F("b14", 1) + 0.6), E("b14"), "corredor")
rot("IGUAÇU: ESPALHA · ITAJAÍ: SOBE", [BLU[0] + 0.2, BLU[1] + 0.6], tw("Sobe", "b14", alt=F("b14", 2) + 1.0), E("b14") + 0.3, "seta")
foto("blumenau-rio-itajai-acu-2006.jpg", tw("apertado", "b14", alt=F("b14", 1) + 0.4), tw("apertado", "b14", alt=F("b14", 1) + 0.4) + 3.6, lado="dir")
# b15 régua de Blumenau
est("b15", "B"); trans(S("b15") - 0.15, "whip", 0.6, "whip pan")
cam(S("b15") - 0.1, [BLU[0], BLU[1]], 6.0, 44, 10, corte=True); cam(E("b15"), [BLU[0] + 0.5, BLU[1]], 7.0, 48, -10)
t_mar = tw("março|marco", "b15", alt=S("b15") + 0.8); t_maio = tw("maio", "b15", n=0, apos=F("b15", 1), alt=F("b15", 1) + 0.4); t_jul9 = tw("quinze|15", "b15", alt=F("b15", 2) + 0.8); t_set = tw("setembro", "b15", alt=F("b15", 3) + 0.5)
g4(tipo="regua", t0=S("b15") + 0.2, t1=E("b15") + 0.8, titulo="BLUMENAU · RIO ITAJAÍ-AÇU · 1983", fonte="DEFESA CIVIL DE BLUMENAU", max=16, linha=10, linha_txt="10 M", left=130, top=230, w=620,
   niveis=[[t_mar, 10.60, "04/03", None], [t_maio, 12.52, "20/05", None], [t_jul9, 15.34, "09/07", CORAL], [t_set, 11.75, "24/09", None]])
num(t_jul9, valor="15,34", faixa="BLUMENAU · 9 JUL 1983 · COTA DO ITAJAÍ-AÇU", unidade="m"); num_off(t_set - 0.3)
# b16 SC
est("b16", "B")
cam(S("b16"), [BLU[0] - 0.5, BLU[1] - 1.0], 18, 52, 0, corte=True); cam(E("b16"), [BLU[0] - 0.5, BLU[1] - 1.0], 15, 54, 12)
tintas.append({"ufs": ["42"], "cor": CORAL, "op": janela_op(S("b16") + 0.3, E("b16") + 1.0, 1, 0.9, 0.8), "max": 0.55})
num(tw("setenta|78", "b16", alt=F("b16", 1) + 1.0), de=0, para=78, dur=1.2, faixa="MUNICÍPIOS EM CALAMIDADE · JULHO DE 1983 · SC", unidade="")
num(tw("quarenta|49", "b16", alt=F("b16", 2)), de=0, para=49, dur=1.0, faixa="MORTOS · SANTA CATARINA", unidade="")
num(tw("duzentos|200", "b16", alt=F("b16", 2) + 1.3), de=0, para=200000, dur=1.4, faixa="DESABRIGADOS (QUASE) · SEGUNDO HERRMANN, UFSC", unidade="")
num_off(E("b16") + 0.2)
foto("blumenau-enchente-2008-exercito-NAO-1983.jpg", F("b16", 0) + 0.5, F("b16", 0) + 3.8, lado="esq")

# ======================= 2/4 O QUE ACONTECEU NO SERTÃO =======================
est("b17", "A"); trans(S("b17") - 0.3, "nuvem", 1.3, "zoom-out orbital do Sul e voo para o sertão")
cx_estados += [{"t": S("b17") - 0.3, "modo": "grande", "ativa": 1, "feitas": [1], "volta": True}, {"t": F("b17", 1) + 0.2, "modo": "compacta", "ativa": 1, "feitas": [1]}]
cam(S("b17") - 0.3, BRC, 68, 54, 0, corte=True); cam(F("b17", 1), NE, 30, 50, 6); cam(E("b17"), CE, 16, 40, -10)
tab(quente, S("b17") + 0.5, 0.6, 0.8)
tintas.append({"ufs": NEUF, "cor": CORAL, "op": janela_op(S("b17"), E("b17") + 1.0, 1, 0.8, 0.8), "max": 0.5})
for k, ano in enumerate([1979, 1980, 1981, 1982, 1983]):
    rot(str(ano), [CE[0] - 1.6 + 0.8 * k, CE[1] + 1.4 - 0.1 * k], F("b17", 2) + 0.35 * k, E("b17") + 0.3, "quente")
# b18 Mombaça
est("b18", "B"); trans(S("b18") - 0.2, "whip", 0.6, "whip pan para o gráfico")
cam(S("b18") - 0.1, MOM, 10, 50, 0, corte=True); cam(E("b18"), [MOM[0] + 0.5, MOM[1]], 12, 52, 10)
anos = [[int(a), v] for a, v in sorted(MOMB["anos"].items(), key=lambda kv: int(kv[0])) if int(a) >= 1911]
t81 = tw("oitenta|81", "b18", n=0, apos=F("b18", 2) - 0.1, alt=F("b18", 2) + 0.2); t82 = tw("oitenta|82", "b18", n=0, apos=F("b18", 3) - 0.1, alt=F("b18", 3) + 0.2); t83 = tw("oitenta|83", "b18", n=0, apos=F("b18", 4) - 0.1, alt=F("b18", 4) + 0.2)
g4(tipo="anuais", t0=S("b18") + 0.5, t1=E("b18") + 0.8, titulo="CHUVA ANUAL EM MOMBAÇA (CE) · PLUVIÔMETRO DO DNOCS", fonte="ANA (HIDROWEB, ESTAÇÃO 00539001) · SÓ ANOS COMPLETOS", anos=anos, max=1700, media=783,
   t_ini=tw("desde|dez", "b18", alt=S("b18") + 1.5), dur=3.5, dest=[[1981, t81, "1981 · 472"], [1982, t82, "1982 · 407"], [1983, t83, "1983 · 366"]])
pino("mom2", "MOMBAÇA (CE)", "PLUVIÔMETRO · DESDE 1910", S("b18") + 0.3, xz=MOM, ate=F("b18", 2))
cartao(tw("metade", "b18", alt=E("b18") - 1.5), E("b18") + 0.3, "1983 EM MOMBAÇA", "47% DA MÉDIA", top=650)
# b19 três anos
est("b19", "B"); cam(S("b19"), CE, 14, 48, 0, corte=True); cam(E("b19"), CE, 11, 50, 10)
for k, (rt, tx, w) in enumerate([("ANO 1", "A ROÇA FALHA", "primeiro"), ("ANO 2", "ACABA O GUARDADO", "segundo"), ("ANO 3", "AÇUDES SECAM · O GADO MORRE", "terceiro")]):
    cartao(tw(w, "b19", alt=F("b19", 2) + 0.6 * k) - 0.2, E("b19") + 0.3 if k == 2 else tw(["segundo", "terceiro"][k], "b19", alt=F("b19", 3) + 0.4 * k) - 0.2, rt, tx, top=300 + k * 0)
foto("acude-coremas-seco-2017.jpg", tw("açudes|acudes", "b19", alt=F("b19", 3) + 0.8), E("b19") + 0.2, lado="dir")
# b20 frentes de emergência
est("b20", "B"); cam(S("b20"), NE, 26, 52, 6, corte=True); cam(E("b20"), NE, 22, 54, -6)
tintas.append({"ufs": NEUF, "cor": CORAL, "op": janela_op(S("b20"), E("b20") + 0.6, 1, 0.8, 0.8), "max": 0.35})
foto("retirantes-pernambuco-slide-janjao-sem-data.jpg", S("b20") + 0.4, S("b20") + 3.6, lado="esq", estatica=True)
foto("sertao-caatinga-arido-2013.jpg", tw("estrada", "b20", alt=F("b20", 0) + 2.0), tw("estrada", "b20", alt=F("b20", 0) + 2.0) + 3.4, lado="esq")
g4(tipo="colunas", t0=F("b20", 1) + 0.2, t1=E("b20") + 0.8, titulo="ALISTADOS NAS FRENTES DE EMERGÊNCIA", fonte="SUDENE (VIA LITERATURA ACADÊMICA)", w=640, left=1230, top=240, max=3400,
   itens=[["1979", 460, tw("setenta|79", "b20", n=0, apos=F("b20", 2) - 0.1, alt=F("b20", 2) + 0.3), "#7FA2C9", "~460 MIL"], ["1983", 3130, tw("milhões|milhoes|3", "b20", n=0, apos=F("b20", 1), alt=F("b20", 1) + 1.0), CORAL, "3,13 MILHÕES"]], selo=None)
# b21 arquivo (fome vira revolta)
trans(S("b21") - 0.1, "corte", 0.5, "corte seco para o papel (impacto grave)")
tab(arquivo, S("b21") - 0.2, 0.7, 0.1); tab(arquivo, E("b21") + 0.3, 0.0, 0.2); est("b21", "B")
cam(S("b21"), FOR, 7, 40, 0, corte=True)
papel("b21", "b21", [{"tipo": "data", "texto": "CEARÁ · AGOSTO DE 1983", "t": S("b21") + 0.2},
    {"tipo": "titulo", "texto": "A FOME VIROU REVOLTA", "t": S("b21") + 0.5, "tam": 110},
    {"tipo": "rotulo", "texto": "FORTALEZA · SEDE DO GOVERNO OCUPADA", "t": tw("Fortaleza", "b21", alt=F("b21", 1) + 0.5)},
    {"tipo": "rotulo", "texto": "↓ DOIS DIAS DEPOIS ↓", "t": tw("depois", "b21", alt=F("b21", 2))},
    {"tipo": "rotulo", "texto": "CANINDÉ · ARMAZÉM DA COBAL INVADIDO", "t": tw("Canindé|Caninde", "b21", alt=F("b21", 2) + 0.8)},
    {"tipo": "carimbo", "texto": "AGOSTO DE 1983", "t": tw("alimentos", "b21", alt=E("b21") - 0.8), "tam": 60}], pre=0.15, topo=True)
# b22 número que ninguém contou
est("b22", "B")
papel("b22", "b22", [{"tipo": "data", "texto": "QUANTOS MORRERAM?", "t": S("b22") + 0.2},
    {"tipo": "titulo", "texto": "MORTOS: ?", "t": S("b22") + 0.7, "tam": 240},
    {"tipo": "rotulo", "texto": "NENHUM NÚMERO OFICIAL CONFIÁVEL", "t": tw("oficial", "b22", alt=F("b22", 2) + 0.8)},
    {"tipo": "rotulo", "texto": "OS RELATOS FALAM DE MUITAS CRIANÇAS · FOME E DESNUTRIÇÃO", "t": tw("crianças|criancas", "b22", alt=F("b22", 3) + 0.8), "tam": 28}], pre=0.15, topo=True)
# b23 volta ao mapa
est("b23", "B"); tab(arquivo, S("b23") - 0.1, 0.0, 0.1); trans(S("b23") - 0.1, "corte", 0.5, "corte seco de volta ao mapa")
cam(S("b23"), NE, 26, 54, 0, corte=True); cam(E("b23"), CE, 18, 50, 12)
tintas.append({"ufs": NEUF, "cor": CORAL, "op": janela_op(S("b23"), E("b23") + 0.6, 1, 0.8, 0.8), "max": 0.45})
cartao(F("b23", 0) + 0.4, F("b23", 1) - 0.1, "SECA DE 1979–1983", "UMA DAS MAIORES DO SÉCULO 20", top=330)
cartao(F("b23", 1) + 0.2, E("b23") + 0.4, "1984", "A CHUVA VOLTA AO NORMAL", top=650)

# ======================= 3/4 POR QUE OS DOIS AO MESMO TEMPO =======================
est("b24", "A"); tab(quente, S("b24"), 0.0, 0.5); trans(S("b24") - 0.3, "nuvem", 1.3, "zoom-out orbital do Brasil até o Pacífico")
cx_estados += [{"t": S("b24") - 0.3, "modo": "grande", "ativa": 2, "feitas": [1, 2], "volta": True}, {"t": F("b24", 1) + 0.2, "modo": "compacta", "ativa": 2, "feitas": [1, 2]}]
cam(S("b24") - 0.3, BRC, 68, 54, 0, corte=True); cam(F("b24", 1), P(-80, -8), 56, 50, -20); cam(F("b24", 2) - 0.2, PACC, 70, 56, -6); cam(E("b24"), PACC, 62, 56, -2)
rot("PACÍFICO", P2(215, 0), tw("Pacífico|Pacifico", "b24", alt=F("b24", 2) + 0.4), E("b24") + 0.3, "corredor")
# b25 Pacífico 82-83 + montanhas RONI
est("b25", "A"); gpac = grade_xy(100, 290, -30, 30)
cam(S("b25"), PACC, 60, 56, -6, corte=True)
relevos.append({**gpac, "y0": 0.03, "k": 0.45, "mostra_data": False, "idx": [[0, 1]], "op": janela_op(S("b25") - 0.2, F("b25", 1) - 0.1, 1, 0.8, 0.5), "cresce": [[0, 0], [S("b25"), 0], [S("b25") + 3.0, 1]]})
rot("PACÍFICO · DEZ/1982", P2(215, 12), S("b25") + 1.0, F("b25", 1), "corredor")
foto("elnino-1982-83-anomalia-temp-pacifico-jan1983.jpg", tw("Pacífico|Pacifico", "b25", n=0, alt=S("b25") + 1.0) + 0.5, tw("Pacífico|Pacifico", "b25", n=0, alt=S("b25") + 1.0) + 4.0, lado="esq")
tmt = F("b25", 1) - 0.1; KH = 1.15
ANOSM = [("1982-83", rmax(1982, 1983)), ("1997-98", rmax(1997, 1998)), ("2015-16", rmax(2015, 2016)), ("2026", rmax(2026, 2026))]
fim_m = E("b25") + 0.6
tks = [F("b25", 1) + 0.6, F("b25", 1) + 1.6, F("b25", 1) + 2.4, F("b25", 1) + 3.2]
for k, (ano, v) in enumerate(ANOSM):
    x = MONT[0] + (k - 1.5) * 4.6
    montanhas.append({"nome": ano + f" · +{v:.1f}".replace(".", ","), "x": x, "z": MONT[1], "r": 1.55, "kh": KH, "cor": CORAL if k == 0 else "#DCCDB0", "h": [[0, 0], [tks[k] - 0.2, 0], [tks[k] + 1.0, v]], "op": janela_op(tmt, fim_m, 1, 0.5, 0.6), "acende": [[0, 0], [tks[k], 1], [tks[k] + 1.2, 0.2]]})
cam(tmt + 0.1, MONT, 30, 14, -6, y=2.0, corte=True); cam(E("b25"), [MONT[0] + 3, MONT[1]], 28, 14, 6, y=2.2)
num(tw("recorde", "b25", alt=E("b25") - 0.8), valor=f"+{ANOSM[0][1]:.1f}".replace(".", ","), faixa="1982-83 · MAIOR EL NIÑO DESDE 1950 · ÍNDICE RONI · NOAA", unidade="°C")
num_off(E("b25") + 0.9)
# b26 Walker
est("b26", "A"); trans(S("b26") - 0.3, "whip", 0.6, "whip pan para a circulação de Walker")
WX0, WX1 = P2(128, 0)[0], P2(262, 0)[0]
cam(S("b26"), [PACC[0], 4.0], 66, 14, 4, y=4.0, corte=True); cam(E("b26"), [PACC[0], 4.0], 62, 16, -4, y=4.0)
t_w = tw("sobe", "b26", alt=F("b26", 1)); t_d = tw("desce", "b26", n=0, alt=F("b26", 2))
seta("#E07A3A", [[WX0, 0, 5.4], [WX0, 0, 7.0], [WX0 + 0.5, 0, 8.6]], t_w, t_w + 1.0, E("b26"), r=0.3)
seta("#E07A3A", [[WX0 + 1, 0, 9.0], [PACC[0], 0, 9.4], [WX1 - 1, 0, 9.0]], t_w + 1.0, t_w + 2.6, E("b26"), r=0.3)
seta("#4C7FB8", [[WX1, 0, 8.6], [WX1, 0, 7.2], [WX1, 0, 5.6]], t_d, t_d + 1.0, E("b26"), r=0.3)
rot("AR SOBE: NUVENS E CHUVA", [WX0 + 4, 0], t_w + 0.4, E("b26"), "quente", y=10.6); rot("AR DESCE: SEM NUVEM", [WX1 - 2, 0], t_d + 0.4, E("b26"), "fria", y=10.0)
cartao(S("b26") + 0.2, F("b26", 1) - 0.1, "ASSISTA: EL NIÑO 2026", "O NOSSO VÍDEO ANTERIOR, AQUI NO CANAL", top=200)
# b27 calendário
est("b27", "B"); trans(S("b27") - 0.2, "whip", 0.6, "whip pan para o calendário")
cam(S("b27") - 0.1, CE, 16, 50, 0, corte=True); cam(E("b27"), CE, 13, 52, 8)
tintas.append({"ufs": ["23"], "cor": CORAL, "op": janela_op(S("b27"), E("b27") + 0.6, 1, 0.7, 0.8), "max": 0.5})
t_pico = tw("dezembro", "b27", alt=F("b27", 1) + 0.5); t_chu = tw("fevereiro", "b27", alt=F("b27", 2) + 1.0)
g4(tipo="anel24", t0=S("b27") + 0.5, t1=E("b27") + 0.8, titulo="CALENDÁRIO · EL NIÑO × CHUVA DO SERTÃO", centro=["PICO DO EL NIÑO", "DEZ–JAN"], fonte="NOAA/CPC (RONI) · FUNCEME", left=1230, top=290,
   acende=[{"i0": 11, "i1": 11, "t": t_pico, "cor": CORAL}, {"i0": 1, "i1": 4, "t": t_chu, "cor": "#5B86B8"}],
   legenda=[[CORAL, "PICO DO EL NIÑO: DEZEMBRO E JANEIRO", t_pico], ["#5B86B8", "CHUVA DO SERTÃO: FEVEREIRO A MAIO", t_chu]])
cartao(tw("terceiro", "b27", alt=E("b27") - 1.5) - 0.2, E("b27") + 0.3, "O INVERNO DO SERTANEJO", "FRACO PELO 3º ANO SEGUIDO", top=650)
# b28 jato subtropical
est("b28", "A"); trans(S("b28") - 0.2, "whip", 0.6, "whip pan para o Sul")
cam(S("b28") - 0.1, P(-55, -27), 32, 44, 10, corte=True); cam(F("b28", 2), P(-52, -27), 24, 40, -6); cam(E("b28"), P(-50, -27), 22, 40, 10)
tj = tw("jato", "b28", alt=F("b28", 1) + 1.0)
seta("#FFFFFF", [P(-78, -30), P(-65, -28.5), P(-55, -29), P(-45, -30.5), P(-34, -30)], tj, tj + 2.2, E("b28") + 1, y=1.6, r=0.14, fluxo=True, vel=0.14, semCabeca=True)
rot("JATO SUBTROPICAL", P(-62, -28.5), tj + 0.4, E("b28"), "seta", y=2.4)
t_seg = tw("segura", "b28", alt=F("b28", 2) + 0.3)
for k, lon in enumerate([-58, -53, -48]):
    seta("#7FB4DE", [P(lon - 3, -36), P(lon - 1, -32), P(lon, -28.2)], t_seg + 0.25 * k, t_seg + 0.25 * k + 1.2, E("b28") + 1, y=0.5, r=0.12)
rot("FRENTES FRIAS PRESAS", P(-52, -24.8), t_seg + 0.4, E("b28"), "fria")
t_bl = tw("bloqueios|bloqueio", "b28", alt=F("b28", 3))
rot("BLOQUEIO · TEMPO TRAVADO", P(-36, -26), t_bl, E("b28") + 0.3, "quente")
foto("noaa-cpc-elnino-impactos-globais-jun-ago.jpg", tw("contrário|contrario", "b28", alt=F("b28", 0) + 0.8), tw("contrário|contrario", "b28", alt=F("b28", 0) + 0.8) + 3.6, lado="esq")
cartao(F("b28", 3) + 0.5, E("b28") + 0.3, "ESTUDO DO INPE", "1983: O TEMPO TRAVADO CHOVENDO POR DIAS", top=650)
# b29 hidrograma + RONI
est("b29", "B"); trans(S("b29") - 0.1, "corte", 0.5, "corte seco de volta ao hidrograma")
cam(S("b29"), UV, 10, 50, 0, corte=True); cam(E("b29"), [UV[0] + 0.5, UV[1]], 12, 52, 10)
tp = tw("esfriando", "b29", alt=F("b29", 1) + 1.5)
g4(tipo="hidro", t0=S("b29") + 0.1, t1=E("b29") + 0.8, titulo="IGUAÇU (COTA, M) × PACÍFICO (RONI × 3, °C) · 1982–83", fonte="ANA · NOAA/CPC", n=NDIA, ymax=11,
   dias=[[IDX[d], IGU["dias"][d]] for d in DIAS], prog=[[0, 1], [E("b29"), 1]], marcas=[{"t": S("b29") + 0.4, "i": HP, "v": 10.42, "texto": "18 JUL · 10,42 M", "tam": 34}], eixo=EIXO,
   faixa=None, roni={"t": S("b29") + 0.8, "k": 3.0, "serie": RONI_DIA}, vertical={"t": tw("julho", "b29", alt=F("b29", 1) + 0.3), "i": HP, "texto": "18 JUL 1983"},
   rotulos=[{"t": tp, "x": 620, "y": 120, "cor": CORAL, "texto": "PACÍFICO ESFRIANDO ↘"}, {"t": tw("pior", "b29", alt=F("b29", 3) + 1.0), "x": 820, "y": 90, "cor": "#3D7FB8", "texto": "RIO NO PICO ↗"}], left=50, top=250)
# b30 anel 24 meses
est("b30", "B")
cam(S("b30"), SUL_C, 22, 54, 0, corte=True); cam(E("b30"), [SUL_C[0], SUL_C[1]], 18, 56, 10)
tintas.append({"ufs": SULUF, "cor": AZUL, "op": janela_op(S("b30"), E("b30") + 0.8, 1, 0.8, 0.8), "max": 0.5})
t_pri = tw("primavera", "b30", alt=F("b30", 1) + 1.0); t_out = tw("outono", "b30", alt=F("b30", 1) + 2.8)
g4(tipo="anel24", t0=S("b30") + 0.5, t1=E("b30") + 0.8, titulo="EL NIÑO NO SUL · 2 ANOS (ANO 1 FORA · ANO 2 DENTRO)", centro=["ANO 1 → ANO 2", "CHUVA A MAIS"], fonte="NOAA/CPC · ANA", left=1230, top=290,
   acende=[{"i0": 8, "i1": 10, "t": t_pri, "cor": AZUL}, {"i0": 14, "i1": 20, "t": t_out, "cor": AZUL}],
   marcas=[{"t": tw("novembro", "b30", alt=F("b30", 2) + 0.5), "i": 10}, {"t": tw("maio", "b30", alt=F("b30", 2) + 1.5), "i": 16}, {"t": tw("julho", "b30", alt=F("b30", 2) + 2.3), "i": 18}],
   legenda=[[AZUL, "PRIMAVERA DO ANO 1 (NOV/82: CHEIA)", t_pri], [AZUL, "OUTONO–INVERNO DO ANO 2 (MAI E JUL/83: CHEIAS)", t_out]])
cartao(tw("Guarde", "b30", alt=E("b30") - 1.8) - 0.1, E("b30") + 0.4, "GUARDE ISSO", "VAI IMPORTAR EM 2026", top=560, carimbo="GUARDE ISSO", t_carimbo=tw("Guarde", "b30", alt=E("b30") - 1.8) + 0.7)
# b31 tela partida + fios do Pacífico
est("b31", "B"); trans(S("b31") - 0.2, "luz", 1.0, "zoom-out para a tela partida")
cam(S("b31") - 0.1, BRC, 72, 58, -20, corte=True); cam(E("b31"), BRC, 68, 58, 6)
partida(S("b31"), E("b32") + 0.2)
t_des = tw("desligou", "b31", alt=F("b31", 0) + 1.5); t_lig = tw("ligou", "b31", alt=F("b31", 0) + 2.8)
seta(CORAL, [P(-86, -6), P(-62, -8), NE], t_des, t_des + 1.6, E("b31") + 1, y=0.9, r=0.16, fluxo=True, vel=0.14, semCabeca=False)
seta(AZUL, [P(-86, -8), P(-68, -18), SUL_C], t_lig, t_lig + 1.6, E("b31") + 1, y=0.9, r=0.16, fluxo=True, vel=0.14, semCabeca=False)
rot("DESLIGA A CHUVA", [NE[0] - 2.0, NE[1] + 1.0], t_des + 0.6, E("b31"), "quente"); rot("LIGA A CHUVA", [SUL_C[0] - 2.0, SUL_C[1] - 1.0], t_lig + 0.6, E("b31"), "fria")
tg2 = tw("quilômetros|quilometros", "b31", alt=F("b31", 1) + 1.0)
rot("2.500 KM", P(-45, -16), tg2, E("b31") + 0.3, "seta")
cartao(F("b31", 1) - 0.2, E("b31") + 0.3, "O MESMO FENÔMENO", "DUAS PONTAS DO EL NIÑO", top=650)
# b32 lugares escolhidos
est("b32", "A")
cam(S("b32"), [UV[0], UV[1]], 5.2, 32, -20, corte=True); cam(tw("sertão|sertao", "b32", alt=F("b32", 1)) - 0.3, [MOM[0], MOM[1]], 7.0, 34, 10, corte=True); cam(F("b32", 2) - 0.3, [UV[0], UV[1]], 5.2, 34, 30, corte=True); cam(E("b32"), [UV[0] + 0.2, UV[1]], 4.8, 36, 50)
pino("uv5", "UNIÃO DA VITÓRIA", "VÁRZEA OCUPADA", F("b32", 2), xz=UV, ate=E("b32")); pino("mom5", "SERTÃO", "SEM ÁGUA GUARDADA", tw("sertão|sertao", "b32", alt=F("b32", 1)), xz=MOM, ate=F("b32", 2) - 0.4)
tab(quente, tw("sertão|sertao", "b32", alt=F("b32", 1)) - 0.3, 0.5, 0.5); tab(quente, F("b32", 2) - 0.3, 0.0, 0.5)
foto("uniao-da-vitoria-rio-iguacu-helicoptero-2016.jpg", tw("vars|varz", "b32", alt=F("b32", 2) + 0.4), F("b32", 3) - 0.2, lado="dir")
cartao(tw("escolheu", "b32", n=0, alt=F("b32", 3) + 0.2) - 0.2, E("b32") + 0.3, "O EL NIÑO ESCOLHEU OS LUGARES", "A OCUPAÇÃO ESCOLHEU QUEM SOFRERIA MAIS", top=300)

# ======================= 4/4 E EM 2026? =======================
est("b33", "A"); tab(quente, S("b33"), 0.0, 0.3); trans(S("b33") - 0.3, "nuvem", 1.3, "zoom-out orbital até o Pacífico de hoje")
cx_estados += [{"t": S("b33") - 0.3, "modo": "grande", "ativa": 3, "feitas": [1, 2, 3], "volta": True}, {"t": E("b33") + 0.3, "modo": "compacta", "ativa": 3, "feitas": [1, 2, 3]}]
cam(S("b33") - 0.3, BRC, 70, 54, 0, corte=True); cam(F("b33", 1), PACC, 66, 56, -6); cam(E("b33"), PACC, 60, 56, -2)
relevos.append({**gpac, "y0": 0.03, "k": 0.45, "mostra_data": False, "idx": [[0, 5]], "op": janela_op(S("b33") + 0.5, E("b34") + 0.6, 1, 0.8, 0.8), "cresce": [[0, 0], [S("b33") + 0.5, 0], [S("b33") + 3.0, 1]]})
rot("PACÍFICO · OUT/2026", P2(215, 12), S("b33") + 1.0, F("b34", 1), "corredor")
# b34 NOAA
est("b34", "A"); cam(S("b34"), PACC, 58, 54, 4, corte=False); cam(E("b34"), P2(215, 0), 44, 50, -4)
t_25 = tw("meio|2", "b34", n=0, apos=F("b34", 1) + 0.3, alt=F("b34", 1) + 2.0)
num(t_25, valor="+2,5", faixa="NIÑO 3.4 · BOLETIM DA NOAA · 12/11/2026", unidade="°C")
t_60 = tw("sessenta|60", "b34", alt=F("b34", 2) + 0.5)
num(t_60 + 0.2, valor="~60%", faixa="CHANCE DE VIRAR O MAIS FORTE DESDE 1950 · NOAA/CPC", unidade="")
g4(tipo="gauge", t0=t_60 - 0.2, t1=E("b34") + 0.6, titulo="CHANCE DE EL NIÑO HISTÓRICO", fonte="NOAA/CPC · 12/11/2026", t_gira=t_60, valor=60, selo={"t": tw("certeza", "b34", alt=E("b34") - 0.8), "texto": "PROVÁVEL ≠ CERTO"})
num_off(E("b34") + 0.2)
LAR = P(-52.41, -25.42); DIO = P(-53.64, -26.27)
# b35 Sul já sentiu
est("b35", "B"); trans(S("b35") - 0.2, "whip", 0.6, "whip pan para o Sul")
MID35 = [(LAR[0] + DIO[0] + BLU[0]) / 3, (LAR[1] + DIO[1] + BLU[1]) / 3]
cam(S("b35") - 0.1, SUL_C, 20, 54, 0, corte=True); cam(F("b35", 1), MID35, 13, 52, 8); cam(E("b35"), [MID35[0] + 0.5, MID35[1]], 11, 52, -6)
tintas.append({"ufs": SULUF, "cor": AZUL, "op": janela_op(S("b35"), E("b35") + 0.8, 1, 0.8, 0.8), "max": 0.45})
pino("lar", "LARANJEIRAS DO SUL (PR)", "577,6 MM · OUT/2026", tw("Laranjeiras", "b35", alt=F("b35", 1) + 1.0), xz=LAR, ate=E("b35"))
pino("dio", "DIONÍSIO CERQUEIRA (SC)", "581,6 MM · OUT/2026", tw("Dionísio|Dionisio", "b35", alt=F("b35", 1) + 3.0), xz=DIO, ate=E("b35"))
num(tw("recorde", "b35", alt=F("b35", 1) + 0.3), valor="~580", faixa="CHUVA EM OUTUBRO DE 2026 · INMET", unidade="mm"); num_off(F("b35", 2) - 0.2)
num(tw("cinquenta|54", "b35", alt=F("b35", 2) + 1.0), de=0, para=54, dur=1.0, faixa="CIDADES CATARINENSES COM ESTRAGOS · 7–8 NOV/2026", unidade=""); num_off(E("b35") + 0.2)
# b36 atenção outono-inverno 2027
est("b36", "B"); cam(S("b36"), SUL_C, 22, 54, 0, corte=True); cam(E("b36"), SUL_C, 18, 56, 10)
tintas.append({"ufs": SULUF, "cor": AZUL, "op": janela_op(S("b36"), E("b36") + 0.8, 1, 0.8, 0.8), "max": 0.4})
g4(tipo="anel24", t0=S("b36") + 0.4, t1=E("b36") + 0.8, titulo="2026–2027 · O MESMO CALENDÁRIO DE 83", centro=["2026 → 2027", "ATENÇÃO"], fonte="NOAA/CPC (BOLETIM DE 12/11/2026)", left=1230, top=290,
   acende=[{"i0": 8, "i1": 10, "t": S("b36") + 0.6, "cor": AZUL}, {"i0": 14, "i1": 20, "t": tw("outono", "b36", alt=F("b36", 3) + 1.5), "cor": AZUL, "pontilhado": True}],
   legenda=[[AZUL, "PRIMAVERA DE 2026: JÁ ACONTECEU", S("b36") + 0.6], [CORAL, "OUTONO E INVERNO DE 2027: ATENÇÃO (NÃO É PREVISÃO)", tw("outono", "b36", alt=F("b36", 3) + 1.5)]])
cartao(F("b36", 3) - 0.2, E("b36") + 0.3, "ISSO NÃO É PREVISÃO DE ENCHENTE", "É ATENÇÃO", top=650)
# b37 sertão 2027
est("b37", "B"); trans(S("b37") - 0.2, "whip", 0.6, "whip pan para o norte")
cam(S("b37") - 0.1, NE, 28, 54, 0, corte=True); cam(E("b37"), CE, 20, 52, 8)
tintas.append({"ufs": ["23", "22", "24", "25", "21"], "cor": CORAL, "op": janela_op(F("b37", 1), E("b37") + 0.8, 1, 0.9, 0.8), "max": 0.35})
cartao(F("b37", 1) + 0.3, F("b37", 2) - 0.1, "PREVISÃO NOV–JAN (INMET)", "CHUVA ABAIXO DA MÉDIA EM ÁREAS DO NORDESTE", top=300)
cartao(F("b37", 3) - 0.1, E("b37") + 0.3, "FUNCEME", "AINDA É CEDO PARA PREVER FEV–MAI DE 2027", top=650)
# b38 Brasil de hoje (cisternas)
est("b38", "A"); cam(S("b38"), CE, 18, 40, 10, corte=True); cam(E("b38"), NE, 26, 46, -10)
tab(quente, S("b38"), 0.0, 0.5)
rng = [[CE[0] + math.cos(i * 2.4) * (0.4 + (i % 9) * 0.5), CE[1] + math.sin(i * 1.7) * (0.3 + (i % 7) * 0.5)] for i in range(110)]
pontos.append({"lista": rng, "t0": tw("cisternas", "b38", alt=F("b38", 1) + 1.0), "t1": tw("cisternas", "b38", alt=F("b38", 1) + 1.0) + 2.6, "t2": E("b38") + 1})
num(tw("milhão|milhao", "b38", alt=F("b38", 1) + 0.5), valor="1,2 MILHÃO", faixa="CISTERNAS NO SEMIÁRIDO · ASA / P1MC", unidade=""); num_off(F("b38", 2))
foto("sobradinho-represa-seca-2015.jpg", tw("doze|2012", "b38", alt=F("b38", 2) + 0.5), E("b38") + 0.3, lado="dir")
# b39 alerta Sul
est("b39", "A"); cam(S("b39"), [(UV[0] + BLU[0]) / 2, (UV[1] + BLU[1]) / 2], 11, 40, -10, corte=True); cam(E("b39"), [(UV[0] + BLU[0]) / 2, UV[1]], 8, 44, 12)
pino("uv4", "UNIÃO DA VITÓRIA", "ALERTA NO CELULAR · DEFESA CIVIL", tw("alerta", "b39", alt=S("b39") + 0.8), xz=UV, ate=F("b39", 1)); pino("blu4", "BLUMENAU", "SISTEMA DE ALERTA DE CHEIA", tw("alerta", "b39", alt=S("b39") + 0.8) + 0.6, xz=BLU, ate=F("b39", 1))
cilindros.append({"x": UV[0] + 0.4, "z": UV[1] - 0.1, "r": 0.08, "h": 1.1, "cor": "#3D7FB8", "cor_marca": "#E8505B", "marca": 10.42 / 12, "t_marca": F("b39", 1),
    "op": janela_op(F("b39", 1), E("b39") + 0.5, 0.55, 0.5, 0.5), "nivel": [[0, 0.0], [F("b39", 1), 0.0], [F("b39", 1) + 1.0, 10.42 / 12]]})
rot("1983 · 10,42 M", [UV[0] + 0.9, UV[1] - 0.5], F("b39", 1) + 0.3, E("b39") + 0.3, "corredor")
cartao(tw("vars|varz", "b39", alt=F("b39", 2)) - 0.1, E("b39") + 0.3, "AS VÁRZEAS CONTINUAM OCUPADAS", "UM RIO QUE JÁ SUBIU 10 METROS PODE SUBIR DE NOVO", top=650)

# ======================= A RESPOSTA =======================
est("b40", "B"); trans(S("b40") - 0.3, "nuvem", 1.3, "zoom-out até a tela partida")
cam(S("b40") - 0.3, BRC, 74, 58, -10, corte=True); cam(E("b40"), BRC, 68, 58, 8)
partida(S("b40") - 0.1, E("b41") + 0.5)
g4(tipo="relogio", t0=S("b40") + 0.2, t1=E("b40") + 0.4, texto="JULHO 1983", sub="O MESMO EL NIÑO", top=60)
seta(CORAL, [P(-86, -6), P(-62, -8), NE], F("b40", 3), F("b40", 3) + 1.4, E("b41"), y=0.9, r=0.16, fluxo=True, vel=0.14)
seta(AZUL, [P(-86, -8), P(-68, -18), SUL_C], F("b40", 3) + 0.3, F("b40", 3) + 1.7, E("b41"), y=0.9, r=0.16, fluxo=True, vel=0.14)
cartao(tw("mesmo", "b40", n=0, alt=F("b40", 4) + 0.1) - 0.2, E("b40") + 0.3, "O MESMO EL NIÑO", "PUXANDO O BRASIL PARA OS DOIS LADOS", top=650)
# b41
est("b41", "A"); trans(S("b41") - 0.2, "nuvem", 1.3, "zoom-out orbital até o Pacífico")
cam(S("b41") - 0.2, PACC, 64, 56, -6, corte=True); cam(E("b41"), PACC, 58, 54, 6)
relevos.append({**gpac, "y0": 0.03, "k": 0.45, "mostra_data": False, "idx": [[0, 5]], "op": janela_op(S("b41"), E("b41") + 0.6, 1, 0.8, 0.8), "cresce": [[0, 1], [E("b41"), 0.5]]})
cartao(F("b41", 2) - 0.1, E("b41") + 0.4, "A LIÇÃO DE 1983", "O PERIGO NÃO ACABA QUANDO O PACÍFICO ESFRIA", top=300)
# b42 fecho
est("b42", "B"); cam(S("b42"), BRC, 70, 58, 0, corte=True); cam(E("b42"), BRC, 64, 58, 10)
partida(S("b42"), E("b42") + 0.5)
cta = {"t0": S("b42") + 0.1, "t_inscreve": tw("inscreve", "b42", alt=F("b42", 2) + 0.3) - 0.2, "texto": "MANDA PRA QUEM TEM FAMÍLIA NO SUL OU NO SERTÃO", "inscreve": "INSCREVA-SE · EM RELEVO"}

fontes = [
    {"t": 0, "texto": "FONTES: ANA (COTA DO IGUAÇU) · DEFESA CIVIL DO PR E DE BLUMENAU · HERRMANN (UFSC) · LANDSAT 4 (USGS)"},
    {"t": S("b17") - 0.5, "texto": "FONTES: ANA/DNOCS (MOMBAÇA) · SUDENE · MEMORIAL DA DEMOCRACIA · MAPA: IBGE / NATURAL EARTH"},
    {"t": S("b25") - 0.5, "texto": "FONTES: NOAA ERSSTV5 · NOAA/CPC (RONI) · INPE"},
    {"t": S("b34") - 0.5, "texto": "FONTES: NOAA/CPC (12/11/2026) · INMET · FUNCEME · ASA"},
]
texturas = []
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
    "midia": midia, "manchetes": manchetes, "cartoes": cartoes, "graficos": graficos, "graficos3": graficos3, "graficos4": graficos4, "papeis": papeis, "checklists": [], "calendario": None,
    "pergunta": {"t0": 9999, "t1": 9999, "texto": ""}, "caixas": {"itens": cx_itens, "estados": cx_estados}, "cortica": {"t0": 9999, "t1": 9999, "itens": []}, "cobre3d": cobre,
    "thumbs": {"A": round(S("b06") + 0.5, 3), "B": round(S("b03") - 0.3, 3), "C0": round(S("b12") + 2.5, 3), "C1": round(S("b33") + 4.0, 3)},
    "transicoes": sorted(transicoes, key=lambda x: x["t"]), "cta": cta, "fontes": fontes, "texturas": texturas,
}
cues["camera"].sort(key=lambda k: k["t"]); cues["rotulos_mapa"] = rotulos
cues["rotulos"] = rotulos
json.dump(cues, open(A / "cues.json", "w"), ensure_ascii=False, separators=(",", ":"))
tr = []; ant = None
for t_, e_ in sorted(ESTILO):
    if e_ != ant: tr.append({"t": round(t_, 3), "e": e_}); ant = e_
json.dump({"_doc": "A/B do longo-04 (build_cues.py): troca no corte de câmera", "trechos": tr}, open(A / "estilo_v2.json", "w"), ensure_ascii=False, indent=1)
(R / "work").mkdir(exist_ok=True)
with open(R / "work/storyboard.txt", "w") as f:
    for tr_ in cues["transicoes"]: f.write(f"TRANSIÇÃO {tr_['t']:7.2f}s {tr_['tipo']}: {tr_['desc']}\n")
    for m in midia: f.write(f"MÍDIA {m['t0']:7.2f}–{m['t1']:7.2f}s {m['id']} ({m['lado']})\n")
    f.write("\n".join(avisos))
print(f"ok: {len(palavras)} palavras, {len(camera)} chaves de câmera, {len(midia)} mídias, {len(transicoes)} transições, {len(relevos)} relevos, {len(papeis)} papéis, {len(graficos4)} g4")
print("avisos:", *avisos, sep="\n  ")
