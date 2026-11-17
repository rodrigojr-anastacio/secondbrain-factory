# Em Relevo 006 (17/11/2026): storyboard em código -> shared/cues.json (tudo amarrado à palavra falada, via whisper.json).
# Motor 2D do 006 (mapa litoral norte A/B + peças React, remotion/src/Longo6.jsx), não o 3D do 005: ver ETAPA2-PRONTA.md.
# Uso: python3 build_cues6.py  (precisa de tempos.json + whisper.json: monta_audio_v2.py antes; dados/blocos3d via gera_assets6.py)
import json, math, re, unicodedata
from pathlib import Path
import numpy as np

A = Path(__file__).parent; R = A.parent
blocos = json.load(open(A / "blocos.json")); tempos = json.load(open(A / "tempos.json")); wh = json.load(open(A / "whisper.json"))
G = json.load(open(R / "remotion/public/v6/geo6.json")); LON0, LON1, LAT0, LAT1 = G["bbox"]; IW, IH = G["w"], G["h"]
T = {b["id"]: b for b in tempos["blocos"]}
S = lambda b: T[b]["s"]; E = lambda b: T[b]["e"]
avisos = []
def norm(w):
    w = unicodedata.normalize("NFD", w.lower()); w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", w)
def tw(palavra, b, n=0, apos=None, alt=None):
    t0 = apos if apos is not None else S(b) - 0.3; t1 = E(b) + 0.2; alvos = [norm(x) for x in palavra.split("|")]; k = 0
    for w in wh:
        if t0 <= w["s"] <= t1 and any(norm(w["w"]).startswith(a) for a in alvos):
            if k == n: return round(w["s"], 3)
            k += 1
    avisos.append(f"palavra '{palavra}' (n={n}) não achada em {b}")
    return round(alt if alt is not None else (S(b) + E(b)) / 2, 3)
def XY(lon, lat): return [round((lon - LON0) / (LON1 - LON0) * IW, 1), round((LAT1 - lat) / (LAT1 - LAT0) * IH, 1)]

# ---------------- legenda (máquina de escrever, igual ao 005) ----------------
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

# ---------------- lugares ----------------
BERT = (-46.139, -23.853); SSEB = (-45.50, -23.78); CARA = (-45.41, -23.625); UBAT = (-45.07, -23.436)
SAHY = (-45.69, -23.772); CRUZ = (-45.42, -23.63); JUQ = (-45.44, -23.50); JUQY = (-45.70, -23.78)
CRISTA = (-45.47, -23.54)

# ---------------- câmera ----------------
camera = []
def cam(t, ll, z, corte=False):
    x, y = XY(*ll)
    if corte and camera: camera.append({"t": round(t - 0.001, 3), **{k: camera[-1][k] for k in ("x", "y", "z")}})
    camera.append({"t": round(t, 3), "x": x, "y": y, "z": z})
ESTILO = []     # (t, 1 = B editorial / 0 = A satélite, fade)
def est(t, v, fade=0.0): ESTILO.append((round(t, 3), v, fade))
ESCURO = []     # (t, v)
def esc(t, v): ESCURO.append([round(t, 3), v])
mapa, anc, cenas, hud, numero = [], [], [], [], []
def add(lista, k, t0, t1, **kw): lista.append({"k": k, "t0": round(t0, 3), "t1": round(t1, 3), **kw})
def num(t, valor=None, faixa="", de=None, para=None, dur=1.0, unidade=None, dec=0):
    n = {"t": round(t, 3), "faixa": faixa, "unidade": unidade, "dec": dec}
    if valor is not None: n["valor"] = valor
    else: n.update({"de": de, "para": para, "ate": round(t + dur, 3)})
    numero.append(n)
def num_off(t): numero.append({"t": round(t, 3), "oculto": True})
def seg(ids): return S(ids[0]), E(ids[-1])
def meio(a, b): return (E(a) + S(b)) / 2
def ficha(k, t0, t1, num_, txt, pulsos=()): add(hud, "ficha", t0, t1, nome=k, num=num_, txt=txt, pulsos=[round(p, 3) for p in pulsos])
def coluna(ll, valor, rot, t0, t1, cor="#3FD8FF", maxv=700, altmax=340, n=None): add(anc, "coluna", t0, t1, ll=XY(*ll), valor=valor, rot=rot, cor=cor, maxv=maxv, altmax=altmax)
def pino(ll, nome, t0, t1, sub=None): add(anc, "pino", t0, t1, ll=XY(*ll), nome=nome, sub=sub)
def rotulo(ll, texto, t0, t1, estilo="seta"): add(anc, "rotulo", t0, t1, ll=XY(*ll), texto=texto, estilo=estilo)
def selo(texto, t0, t1): add(hud, "selo", t0, t1, texto=texto)
def cartao(texto, t0, t1): add(hud, "cartao", t0, t1, texto=texto)

# ---------------- cicatrizes (posições ILUSTRATIVAS sobre encostas > 40 %) ----------------
dem = np.load(R / "work/v6/dem.npy"); mpp = 111320.0 / G["k"]
gy, gx = np.gradient(dem, mpp); decliv = np.hypot(gx, gy) * 100
rng = np.random.default_rng(1967)
def sorteia(box, n, lim=40, seed=0):
    r = np.random.default_rng(seed); x0, y0 = XY(box[0], box[3]); x1, y1 = XY(box[1], box[2]); out = []
    ys, xs = np.where(decliv[int(y0):int(y1), int(x0):int(x1)] > lim)
    if len(xs) == 0: return out
    for i in r.choice(len(xs), min(n, len(xs)), replace=False): out.append([round(float(xs[i] + x0), 1), round(float(ys[i] + y0), 1)])
    return out
CIC67 = sorteia((-45.56, -45.28, -23.70, -23.50), 640, 40, 1)
CIC23 = sorteia((-45.80, -45.58, -23.80, -23.70), 180, 40, 2)

# ======================= HOOK =======================
# b01: A à noite, câmera corre de Bertioga a Caraguatatuba
est(S("b01") - 0.1, 0); esc(0, 0.45); esc(E("b02"), 0.0)
cam(0, (-46.10, -23.78), 0.62); cam(E("b01") - 0.5, (-45.55, -23.70), 0.78);
add(mapa, "luzes", 0, E("b01"))
cartao("BERTIOGA (SP) · 18–19 FEV 2023", 0.3, E("b01") + 0.3)
coluna(BERT, 683, "BERTIOGA", tw("683", "b01"), E("b02") + 0.5, maxv=700, altmax=420)
coluna(CARA, 234, "CARAGUATATUBA", tw("234", "b01"), E("b02") + 0.5, maxv=700, altmax=420)
add(hud, "etiqueta", 0.6, E("b02") + 0.5, texto="24 HORAS · CEMADEN", pos=[60, 1022])
# b02: SS 627, depois Landsat grande
cam(S("b02"), (-45.62, -23.70), 0.9); cam(E("b02") + 0.4, (-45.55, -23.72), 1.0)
coluna(SSEB, 627, "SÃO SEBASTIÃO", tw("627", "b02"), E("b02") + 0.5, maxv=700, altmax=420)
t_sat = tw("satelite|satélite", "b02")
add(cenas, "foto", t_sat, E("b02") + 0.5, arq="satelite/nasa-eo-landsat8-sao-sebastiao-depois-2023-02-26.jpg", fmt="grande", legenda="SÃO SEBASTIÃO · LANDSAT 8 · 26 FEV 2023", kb=[0.5, 0.5, 1.0, 0.45, 0.62, 1.22])
# b03: dois blocos
est(S("b03") - 0.2, 1, 0.0); esc(S("b03") - 0.2, 0.0)
add(cenas, "bloco", S("b03") - 0.15, E("b03") + 0.3, modo="dois", fichas=False)
add(hud, "selo", S("b03") + 1.0, E("b03"), texto="ILUSTRATIVO · ALTURA EXAGERADA 2,5×")
# b04: recuo e pergunta
cam(S("b04") - 0.2, (-45.55, -23.64), 0.52, corte=True)
add(hud, "pergunta", S("b04"), E("b04") + 0.4, texto="POR QUE A SERRA DO MAR DESABA SOBRE O LITORAL?", sub="E POR QUE ELA REPETE?", t_sub=tw("repete", "b04"))
# b05: A, foto da serra + etiquetas
est(S("b05") - 0.3, 0, 0.5)
cam(S("b05") - 0.3, (-45.42, -23.64), 1.0); cam(E("b05") + 0.5, (-45.44, -23.58), 1.5)
add(cenas, "foto", S("b05") + 0.1, E("b05") + 0.4, arq="video/serra-do-mar-vista-da-tamoios-caraguatatuba.jpg", fmt="grande", legenda="SERRA DO MAR · CARAGUATATUBA", kb=[0.5, 0.55, 1.0, 0.5, 0.45, 1.12])
# b06: bloco Cruzeiro + 3 fichas
est(S("b06") - 0.3, 1, 0.0); esc(S("b06") - 0.3, 0.0)
add(cenas, "bloco", S("b06") - 0.2, E("b06") + 0.4, modo="cruzeiro", fichas=False, casca_t=tw("casca", "b06"))
tP, tC, tK = tw("700", "b06"), tw("400", "b06"), tw("casca", "b06")
ficha("PAREDE", tP, E("b06") + 0.7, "700 M", "EM < 6 KM"); ficha("CHUVA", tC, E("b06") + 0.7, "400 MM", "EM 6 H"); ficha("CASCA", tK, E("b06") + 0.7, "1 A 2,5 M", "SOBRE A ROCHA")
# b07: carta de Olga Cruz + Landsat lado a lado
est(S("b07") - 0.3, 1, 0.0)
t7 = tw("satell|satel", "b07", n=0)
add(cenas, "doc", S("b07") - 0.2, t7 + 0.1, arq="doc/cruz1975-fig7-carta-declividade-santo-antonio.png", legenda="CARTA DE DECLIVIDADES · OLGA CRUZ · 1975", rot="OLGA CRUZ · GEÓGRAFA (USP)", kb=[0.5, 0.35, 1.0, 0.5, 0.65, 1.08], inclina=True)
add(cenas, "dupla", t7 + 0.1, E("b07") + 0.4, arqs=["doc/cruz1975-fig7-carta-declividade-santo-antonio.png", "satelite/nasa-eo-landsat8-sao-sebastiao-depois-2023-02-26.jpg"],
    leg=["CARTA DE DECLIVIDADES · OLGA CRUZ · 1975", "SÃO SEBASTIÃO · LANDSAT 8 · 26 FEV 2023"], rots=["OLGA CRUZ · 1975", "LANDSAT · 2023"])

# ======================= 1 · A PAREDE =======================
est(S("b08") - 0.4, 0, 0.9)
cam(S("b08") - 0.4, (-45.42, -23.60), 0.62, corte=True); cam(E("b08"), (-45.43, -23.60), 1.15)
rotulo((-45.45, -23.545), "BORDA DO PLANALTO · 750–900 M", tw("700", "b08"), E("b08") + 0.4, "corredor")
add(mapa, "linha", tw("planalto", "b08") - 0.5, E("b09"), pts=[XY(-45.62, -23.575), XY(-45.50, -23.53), XY(-45.36, -23.54), XY(-45.28, -23.56)], cor="#FFE9A8", largura=7, dash=False)
add(hud, "regua_h", S("b08") + 3.0, E("b08") + 0.3, texto="PRAIA → CRISTA · 7,5 KM", pos=[1180, 150])
# b09: sobe o vale (perfil 1)
prf = json.load(open(R / "dados/perfis.json"))["perfis"][0]; pts = [XY(p["lon"], p["lat"]) for p in prf["pontos"][::20]]
cam(S("b09"), (-45.40, -23.62), 1.3); cam(E("b09") - 1.5, (-45.45, -23.55), 1.6); cam(E("b09"), (-45.42, -23.64), 1.5)
add(mapa, "linha", S("b09") + 0.2, E("b09"), pts=pts, cor="#3FD8FF", largura=6, dash=False, cresce=True)
pino((-45.40, -23.625), "CENTRO · RIO SANTO ANTÔNIO", S("b09") + 0.3, E("b09"))
add(hud, "altimetro", S("b09") + 0.4, E("b09") - 1.2, de=0, para=750, km=7.5, t_fim=tw("750", "b09"))
tCr = tw("Cruzeiro", "b09"); add(mapa, "img", tCr, E("b10") + 0.2, src="v6/decliv30g.png", op=0.95)
rotulo((-45.465, -23.585), "MORRO DO CRUZEIRO · > 30°", tCr, E("b09") + 0.2, "corredor")
# b10: bacia, declive > 40 %
est(S("b10") - 0.2, 1, 0.8)
cam(S("b10") - 0.2, (-45.44, -23.60), 1.4); cam(E("b10"), (-45.44, -23.59), 1.7)
add(mapa, "img", S("b10") + 0.2, E("b10") + 0.8, src="v6/decliv40.png", op=0.95)
rotulo((-45.47, -23.56), "BACIA DO SANTO ANTÔNIO · ~30 KM²", S("b10") + 0.2, E("b10") + 0.6, "seta")
num(tw("40", "b10") - 2.5, valor="MAIS DE 50%", faixa="COM DECLIVE ACIMA DE 40%")
num_off(E("b10") + 0.1)
add(mapa, "linha", tw("nasce", "b10") - 0.2, E("b10") + 0.3, pts=[XY(-45.47, -23.55), XY(-45.43, -23.60), XY(-45.40, -23.625), XY(-45.39, -23.64)], cor="#E8505B", largura=9, dash=False, cresce=True)
add(hud, "etiqueta", tw("minutos", "b10") - 0.3, E("b10") + 0.4, texto="MINUTOS, NÃO DIAS", pos=[60, 1022])
# b11: Juqueriquerê e fratura
est(S("b11") - 0.3, 0, 0.9)
cam(S("b11") - 0.3, (-45.43, -23.58), 0.9, corte=False); cam(E("b11"), (-45.40, -23.45), 0.75)
rotulo(JUQ, "SERRA DE JUQUERIQUERÊ · > 1.300 M", tw("Juquere", "b11"), E("b11") + 0.2, "corredor")
add(mapa, "linha", tw("fratura|partiu", "b11") - 0.3, E("b11") + 0.4, pts=[XY(-45.80, -23.78), XY(-45.60, -23.70), XY(-45.40, -23.60), XY(-45.20, -23.50)], cor="#FFFFFF", largura=5, dash=True)
selo("FRATURA · BORDA DO BLOCO (ESQUEMA ILUSTRATIVO)", tw("fratura|partiu", "b11") - 0.3, E("b11") + 0.3)
# b12: dolly a Sahy, bloco Sahy
est(S("b12") - 0.2, 1, 0.0); esc(S("b12") - 0.2, 0.0)
cam(S("b12") - 0.2, CARA, 0.8, corte=True); cam(S("b12") + 4.5, SAHY, 0.9)
add(mapa, "linha", S("b12"), S("b12") + 4.6, pts=[XY(*CARA), XY(*SAHY)], cor="#FFD23F", largura=6, dash=True)
add(hud, "regua_h", S("b12") + 0.8, S("b12") + 5.0, texto="CARAGUATATUBA ↔ BARRA DO SAHY · ~35 KM", pos=[560, 120])
add(cenas, "bloco", S("b12") + 5.0, E("b12") + 0.4, modo="sahy", fichas=False)
pino(SAHY, "GUARDE ESTE LUGAR", tw("Guarde", "b12"), E("b12") + 0.2)

# ======================= 2 · A CHUVA QUE A SERRA FABRICA =======================
est(S("b13") - 0.2, 1, 0.0); esc(S("b13") - 0.2, 0.55)
cam(S("b13") - 0.2, (-45.62, -23.68), 0.56, corte=True); cam(E("b13"), (-45.60, -23.66), 0.6)
cartao("18–19 FEV 2023 · 24 H · CEMADEN", S("b13") + 0.3, E("b13") - 4)
for lug, nome, v, w in ((BERT, "BERTIOGA", 683, "Bertioga"), (SSEB, "SÃO SEBASTIÃO", 627, "Sebasti"), (CARA, "CARAGUATATUBA", 234, "Caraguatatuba"), (UBAT, "UBATUBA", 335, "Ubatuba")):
    coluna(lug, v, nome, tw(w, "b13", n=0 if nome != "BERTIOGA" else 0, apos=tw("Bertioga", "b13") - 0.3 if nome != "BERTIOGA" else None) + 0.5, E("b14") + 0.2, maxv=700, altmax=380)
esc(E("b13") + 0.5, 0.0)
# b14: A, faixa de chuva + ar úmido
est(S("b14") - 0.3, 0, 0.6)
cam(S("b14") - 0.3, (-45.80, -23.78), 1.25); cam(E("b14"), (-45.55, -23.72), 1.05)
add(mapa, "chuva", S("b14") + 0.8, E("b14") + 0.3, poly=[XY(-46.18, -23.85), XY(-45.45, -23.70), XY(-45.45, -23.62), XY(-46.18, -23.76)])
add(mapa, "setas_ar", tw("ar", "b14", n=0, apos=tw("oceano|úmido", "b14") - 0.8), E("b14") + 0.3, de=[XY(-45.9, -23.92), XY(-45.7, -23.90), XY(-45.5, -23.84)], para=[XY(-45.86, -23.80), XY(-45.66, -23.77), XY(-45.46, -23.69)])
rotulo((-45.85, -23.745), "FAIXA DE POUCOS KM", tw("faixa", "b14"), E("b14") + 0.3, "corredor")
rotulo((-45.62, -23.905), "AR ÚMIDO DO MAR → SOBE · ESFRIA · CHOVE", tw("oceano|úmido", "b14"), E("b14") + 0.3, "seta")
selo("ESQUEMA ILUSTRATIVO", S("b14") + 0.3, E("b14"))
# b15: IMERG
est(S("b15") - 0.2, 1, 0.0)
cam(S("b15") - 0.2, (-45.62, -23.68), 0.56, corte=True); cam(E("b15"), (-45.60, -23.67), 0.6)
add(mapa, "img", S("b15") + 0.2, E("b15") + 0.5, src="v6/imerg.png", op=0.6)
rotulo((-45.35, -23.86), "SATÉLITE DE CHUVA (NASA) · QUADRADOS DE 10 KM", S("b15") + 0.3, E("b15") + 0.3, "seta")
coluna(BERT, 683, "PLUVIÔMETRO · BERTIOGA", S("b15") + 0.3, E("b15") + 0.5, maxv=700, altmax=360)
num(tw("110", "b15") - 0.2, valor="~110 MM", faixa="ESTIMATIVA DO SATÉLITE DA NASA")
num_off(E("b15") + 0.1)
add(hud, "etiqueta", tw("pico", "b15"), E("b15") + 0.3, texto="O PICO NÃO CABIA NO QUADRADO", pos=[60, 1022])
# b16: A, regional
est(S("b16") - 0.3, 0, 0.9)
cam(S("b16") - 0.3, (-45.6, -23.62), 0.6); cam(E("b16"), (-45.4, -23.55), 0.52)
rotulo((-45.5, -23.43), "FRENTE FRIA", tw("fria", "b16"), E("b16") + 0.3, "fria")
rotulo((-45.25, -23.74), "CICLONE PEQUENO", tw("ciclone", "b16"), E("b16") + 0.3, "seta")
rotulo((-45.62, -23.88), "OCEANO MAIS QUENTE (+~1 °C)", tw("quente", "b16"), E("b16") + 0.3, "quente")
add(mapa, "ciclone", tw("ciclone", "b16"), E("b16") + 0.3, ll=XY(-45.15, -23.80))
add(hud, "etiqueta", S("b16") + 0.4, E("b16") + 0.3, texto="SEGUNDO O IAG-USP", pos=[60, 1022]); selo("ESQUEMA ILUSTRATIVO", S("b16") + 0.4, E("b16"))
# b17: pluviômetro gigante
est(S("b17") - 0.2, 1, 0.0)
add(cenas, "pluv", S("b17") - 0.1, E("b17") + 0.3, t_ini=tw("400", "b17") - 0.6, t_fim=tw("400", "b17") + 2.2, maxv=400, marca=225, marca_t=tw("225", "b17"), recorde_t=tw("maior", "b17"))
# b18: ficha de 1967
est(S("b18") - 0.2, 1, 0.0)
add(cenas, "ficha1967", S("b18") - 0.1, E("b18") + 0.3, t17=tw("17", "b18"), t18=tw("18", "b18", apos=tw("17", "b18") + 0.4), t_trans=tw("transbordou", "b18"))
# b19: dois postos
add(cenas, "postos", S("b19") - 0.1, E("b19") + 0.3, t_poucos=tw("poucos", "b19"), t_valer=tw("vale", "b19"), t_terceiro=tw("terceiro", "b19"))
ficha("CASCA", tw("terceiro", "b19"), E("b19") + 0.3, "1 A 2,5 M", "SOBRE A ROCHA", pulsos=[tw("terceiro", "b19")])

# ======================= 3 · A CASCA DA SERRA =======================
add(cenas, "bloco", S("b20") - 0.15, E("b21") + 0.3, modo="face", fichas=False, t_zoom=S("b20") + 0.2, t_recua=S("b21") - 0.3, t_planta=tw("floresta", "b21"), t_comp=tw("700", "b21"))
selo("ILUSTRATIVO · CASCA EXAGERADA", S("b20") + 0.5, E("b21"))
add(hud, "etiqueta", tw("plantada", "b21") - 0.2, E("b21") + 0.3, texto="CONTATO COM A ROCHA", pos=[60, 1022])
# b22: esquema do escorregamento
add(cenas, "casca_esq", S("b22") - 0.15, E("b22") + 0.3, t_gotas=S("b22") + 0.3, t_cola=tw("coes", "b22"), t_desliza=tw("Encharcado", "b22"), t_sa=tw("sa|rocha", "b22", n=0, apos=tw("raspou", "b22") - 0.2))
# b23: carta Olga Cruz tela cheia
est(S("b23") - 0.2, 1, 0.0)
add(cenas, "doc", S("b23") - 0.15, E("b23") + 0.3, arq="doc/cruz1975-fig7-carta-declividade-santo-antonio.png", legenda="CARTA DE DECLIVIDADES · OLGA CRUZ · 1975", rot=None, kb=[0.5, 0.3, 1.05, 0.5, 0.7, 1.25], inclina=False,
    tags=[[tw("40", "b23"), "> 40% · MAIS ATINGIDAS", 0], [tw("topos", "b23"), "TOPOS PLANOS · FICARAM DE PÉ", 1]])
# b24: granito
est(S("b24") - 0.2, 1, 0.0)
cam(S("b24") - 0.2, (-45.44, -23.60), 1.5, corte=True); cam(E("b24"), (-45.43, -23.60), 1.3)
add(mapa, "img", S("b24"), E("b24") + 0.4, src="v6/decliv40.png", op=0.55)
add(mapa, "cic", tw("cicatri", "b24") - 0.2, E("b24") + 0.4, pts=CIC67[:260], cor="#FFE9A8", r=9, ritmo=3.5)
rotulo((-45.47, -23.57), "GRANITO DE CARAGUATATUBA", tw("granito", "b24", n=0, apos=tw("rocha", "b24")), E("b24") + 0.3, "seta")
num(tw("oito", "b24") - 0.3, valor="8 EM CADA 10", faixa="NO MESMO GRANITO · USP, 2017"); num_off(E("b24") + 0.2)
selo("POSIÇÕES ILUSTRATIVAS", tw("cicatri", "b24"), E("b24"))
# b25: foto de Ubatuba, depois cascas multiplicadas
t25 = tw("Ubatuba", "b25")
add(cenas, "foto", S("b25") - 0.15, tw("Agora", "b25", apos=tw("estrada", "b25")) , arq="video/ubatuba-encosta-arrancada-estrada-2023-02-19.jpg", fmt="grande", legenda="UBATUBA (SP) · 19 FEV 2023", kb=[0.5, 0.75, 1.0, 0.5, 0.45, 1.18])
est(tw("Agora", "b25", apos=tw("estrada", "b25")) - 0.2, 0, 0.0)
cam(tw("Agora", "b25", apos=tw("estrada", "b25")) - 0.2, (-45.68, -23.74), 1.3, corte=True); cam(E("b25") + 0.4, (-45.62, -23.72), 1.0)
add(mapa, "cic", tw("centenas", "b25") - 1.4, E("b25") + 0.5, pts=CIC23, cor="#C98B52", r=7, ritmo=3.0)

# ======================= 4 · 1967: O CAMINHO ATÉ A CIDADE =======================
est(S("b26") - 0.4, 0, 0.9)
cam(S("b26") - 0.4, (-45.42, -23.60), 0.9, corte=True); cam(E("b26"), (-45.43, -23.60), 1.25)
add(mapa, "img", S("b26") + 1.0, E("b27") + 0.5, src="v6/decliv40.png", op=0.7)
cartao("CARAGUATATUBA · 18 MAR 1967", S("b26") + 0.2, E("b26"))
rotulo((-45.40, -23.56), "TODOS OS VALES", tw("todos", "b26"), E("b26") + 0.3, "corredor")
add(mapa, "vales", tw("escorregar", "b26") - 0.3, E("b28") + 0.3)
# b27: contadores
est(S("b27") - 0.2, 1, 0.0)
cam(S("b27") - 0.2, (-45.42, -23.60), 0.75, corte=True); cam(E("b27"), (-45.42, -23.60), 0.88)
t640 = tw("640", "b27"); add(mapa, "cic", t640 - 0.2, t640 + 4.0, pts=CIC67, cor="#E8505B", r=4.5, ritmo=4.2)
add(mapa, "circulo", t640, E("b27") + 0.5, ll=XY(*CARA), r_km=15)
num(t640 - 0.1, de=0, para=640, dur=4.0, unidade="cicatrizes", faixa="FOTOS AÉREAS · RAIO DE ATÉ 15 KM")
num(tw("2", "b27", n=0, apos=tw("Cerca", "b27")) - 0.2, valor="~2 MILHÕES", faixa="DE TONELADAS DE TERRA, ROCHA E ÁRVORES");
num(tw("quinto", "b27") - 0.2, valor="1/5", faixa="DA FLORESTA DA ÁREA ESTUDADA"); num_off(E("b27") + 0.2)
selo("POSIÇÕES ILUSTRATIVAS", t640, E("b27"))
# b28: avalanche
est(S("b28") - 0.2, 0, 0.8)
cam(S("b28") - 0.2, (-45.46, -23.56), 1.5, corte=True); cam(tw("planic|planíc", "b28") - 1.0, (-45.42, -23.60), 1.45); cam(E("b28"), (-45.40, -23.63), 1.0)
add(mapa, "fluxo", S("b28") + 0.2, E("b28") + 0.3, vias=[[XY(-45.50, -23.55), XY(-45.45, -23.58), XY(-45.41, -23.62)], [XY(-45.44, -23.53), XY(-45.42, -23.58), XY(-45.40, -23.622)], [XY(-45.35, -23.55), XY(-45.38, -23.59), XY(-45.395, -23.62)], [XY(-45.52, -23.60), XY(-45.46, -23.61), XY(-45.415, -23.63)]])
rotulo((-45.47, -23.545), "AVALANCHE DE DETRITOS (OLGA CRUZ)", tw("avalanche", "b28"), E("b28") + 0.2, "corredor")
add(hud, "aspas", tw("morro", "b28", n=0, apos=tw("moradores", "b28")), E("b28") - 3.0, texto="“O MORRO RODOU”", sub="MORADORES")
rotulo((-45.40, -23.655), "A PLANÍCIE · A CIDADE", tw("planic|planíc", "b28"), E("b28") + 0.3, "seta")
# b29: 4 fases
est(S("b29") - 0.2, 1, 0.0)
add(cenas, "fases", S("b29") - 0.1, E("b29") + 0.3, ts=[tw("Primeiro", "b29"), tw("escorregamentos", "b29"), tw("corridas", "b29"), tw("represaram|nova", "b29")],
    nomes=["ENCHENTE DOS RIOS", "ESCORREGAMENTOS", "CORRIDAS DE DETRITOS", "ENCHENTE POR BLOQUEIO"])
# b30: rio e lama
est(S("b30") - 0.2, 0, 0.0)
add(cenas, "lama", S("b30") - 0.1, E("b30") + 0.3, t_rio=tw("abriu", "b30"), t_lama=tw("80", "b30", n=0, apos=tw("ruas", "b30")), t_troncos=tw("troncos", "b30"))
# b31: vítimas, sóbrio
est(S("b31") - 0.2, 1, 0.0); esc(S("b31") - 0.2, 0.35)
cam(S("b31") - 0.2, (-45.40, -23.62), 1.0, corte=True); cam(E("b31"), (-45.40, -23.62), 1.15)
add(cenas, "card", S("b31") + 0.0, tw("segundo", "b31") - 0.3, titulo="VÍTIMAS DE 1967", linhas=[["120", "ESTIMATIVA DE OLGA CRUZ", tw("120", "b31")], ["~500", "CONTAGENS DA ÉPOCA", tw("500", "b31")]], fundo=False)
rotulo((-45.40, -23.65), "PLANÍCIE EM 1967 · FAZENDAS (ESQUEMA)", tw("fazenda", "b31"), E("b31") + 0.3, "seta")
# b32: carta SGB (declive como base) + moradores
est(S("b32") - 0.2, 1, 0.0); esc(S("b32") - 0.2, 0.0)
cam(S("b32") - 0.2, (-45.42, -23.60), 0.95, corte=True); cam(E("b32"), (-45.42, -23.62), 1.2)
add(mapa, "img", S("b32") + 0.5, E("b32") + 0.5, src="v6/decliv40.png", op=0.85)
add(hud, "etiqueta", S("b32") + 0.5, E("b32") + 0.3, texto="ENCOSTAS > 40% DE DECLIVE · SRTM (BASE DA CARTA DO SGB, NÃO REPRODUZIDA)", pos=[60, 1022])
pino(CARA, "CARAGUATATUBA · PLANÍCIE", tw("planic|planíc", "b32"), E("b32") + 0.2)
num(tw("censo", "b32") - 0.3, valor="~135 MIL", faixa="MORADORES · CENSO 2022"); num_off(E("b32") + 0.3)

# ======================= 5 · 2023: A MESMA RECEITA =======================
est(S("b33") - 0.3, 0, 0.9); esc(S("b33") - 0.3, 0.0)
cam(S("b33") - 0.3, CARA, 0.9, corte=True); cam(S("b33") + 4.0, SAHY, 1.15); cam(E("b33"), (-45.68, -23.76), 1.5)
add(mapa, "ret", S("b33") + 3.5, E("b33") + 0.4, box=[-45.78, -45.60, -23.80, -23.72], texto="ÁREA DA IMAGEM LANDSAT")
# b34: cortina antes x depois
add(cenas, "cortina", S("b34") - 0.15, E("b34") + 0.3, antes="satelite/nasa-eo-landsat9-sao-sebastiao-antes-2022-10-29.jpg", depois="satelite/nasa-eo-landsat8-sao-sebastiao-depois-2023-02-26.jpg", t_faixa=tw("faixa", "b34", n=0, apos=tw("Cada", "b34") - 0.6))
# b35: bloco Sahy + fichas
est(S("b35") - 0.2, 1, 0.0)
add(cenas, "bloco", S("b35") - 0.15, E("b35") + 0.3, modo="sahy", fichas=False)
ficha("PAREDE", tw("parede", "b35"), E("b35") + 0.2, "685 M", "EM 5,4 KM"); ficha("CHUVA", tw("627", "b35"), E("b35") + 0.2, "627 MM", "EM 24 H"); ficha("CASCA", tw("casca", "b35"), E("b35") + 0.2, "1 A 2,5 M", "SOBRE A ROCHA")
# b36: citação
add(cenas, "citacao", S("b36") - 0.15, E("b36") + 0.3, arq="satelite/nasa-eo-landsat8-sao-sebastiao-depois-2023-02-26.jpg", texto="BEM INCOMUNS, MAS NÃO SEM PRECEDENTE", fonte="ESPECIALISTA EM DESLIZAMENTOS DA NASA", t_prec=tw("precedente", "b36", n=1))
# b37: card 2023
add(cenas, "card", S("b37") - 0.15, E("b37") + 0.3, titulo="2023 · SÃO SEBASTIÃO E UBATUBA", linhas=[["65", "VIDAS", tw("65", "b37")], ["1.815", "DESABRIGADOS", tw("desabrigadas", "b37") - 0.6], ["2.251", "DESALOJADOS", tw("sair", "b37") - 1.2]],
    fundo="video/sao-sebastiao-encosta-aereo-2023-02-23.jpg")

# ======================= A RESPOSTA =======================
est(S("b38") - 0.3, 1, 0.9); esc(S("b38") - 0.3, 0.0)
cam(S("b38") - 0.3, (-45.55, -23.64), 0.6, corte=True); cam(E("b38"), (-45.55, -23.64), 0.52)
add(cenas, "resposta", S("b38") + 0.5, E("b38") + 0.4, ts=[tw("700", "b38"), tw("faixa", "b38"), tw("casca", "b38")], itens=[["700 M", "A MENOS DE 6 KM DO MAR"], ["400 MM", "EM 6 H, NUMA FAIXA ESTREITA"], ["CASCA DE 1 A 2,5 M", "QUASE SEM COLA"]])
# b39: reprise
est(S("b39") - 0.3, 0, 0.8)
cam(S("b39") - 0.3, (-45.44, -23.60), 1.3, corte=True); cam(tw("planic|planíc", "b39") - 0.3, (-45.40, -23.63), 1.2); cam(tw("Cruzeiro", "b39") - 0.5, (-45.55, -23.70), 0.8)
add(mapa, "cic", S("b39") + 0.1, tw("Cruzeiro", "b39"), pts=CIC67[:300], cor="#E8505B", r=5, ritmo=3.0)
add(mapa, "fluxo", S("b39") + 5.0, tw("Cruzeiro", "b39") - 0.2, vias=[[XY(-45.50, -23.55), XY(-45.45, -23.58), XY(-45.41, -23.62)], [XY(-45.35, -23.55), XY(-45.38, -23.59), XY(-45.395, -23.62)]])
est(tw("Cruzeiro", "b39") - 0.5, 1, 0.0)
add(cenas, "bloco", tw("Cruzeiro", "b39") - 0.45, E("b39") + 0.3, modo="dois", fichas=False)
# b40
est(S("b40") - 0.3, 1, 0.9)
cam(S("b40") - 0.3, (-45.55, -23.66), 0.58, corte=True); cam(E("b40"), (-45.50, -23.66), 0.8)
add(mapa, "img", S("b40") + 0.2, E("b40") + 0.5, src="v6/decliv40.png", op=0.9)
add(hud, "selo_grande", S("b40") + 0.4, E("b40"), texto="NÃO É PREVISÃO")
add(hud, "etiqueta", tw("geografia", "b40"), E("b40") + 0.3, texto="A GEOGRAFIA NÃO MUDA", pos=[60, 1022])
# b41
cam(S("b41") - 0.2, (-45.41, -23.625), 1.4, corte=True); cam(E("b41"), (-45.41, -23.625), 1.7)
add(mapa, "img", S("b41"), E("b41") + 0.4, src="v6/decliv40.png", op=0.75)
num(tw("3", "b41") - 0.3, valor="~3 MIL", faixa="MORADORES EM ÁREAS DE RISCO · IBGE, CENSO 2010"); num_off(E("b41") + 0.2)
selo("ESQUEMA · SEM POLÍGONOS DE RISCO REPRODUZIDOS", S("b41") + 0.5, E("b41"))
# b42
add(cenas, "cortica", S("b42") - 0.15, E("b42") + 0.3, ts1=tw("SMS", "b42", alt=S("b42") + 1.0), ts2=tw("saia", "b42", alt=E("b42") - 2.0))
# b43
add(cenas, "final", S("b43") - 0.15, tempos["duracao"], t_card=tw("seca", "b43"), t_logo=tw("inscreve", "b43"), t_btn=tw("inscreve", "b43") + 0.3)

# ---------------- estilo A/B (1 = B), com fade ----------------
tab = []; ant = 1
ESTILO.sort()
tab.append([0, 0])
for t_, v, f in ESTILO:
    cur = tab[-1][1]
    if v == cur: continue
    if f > 0: tab += [[t_, cur], [t_ + f, v]]
    else: tab += [[round(t_ - 0.001, 3), cur], [t_, v]]
ESC = [[0, 0.45]] + sorted(ESCURO)
cues = {
    "_doc": "Gerado por shared/build_cues6.py (não editar à mão). Tempos em segundos de audio/narracao.wav.",
    "fps": 30, "duracao": tempos["duracao"], "fim_fala": tempos["blocos"][-1]["e"], "voz": tempos.get("voz"),
    "geo": G, "paleta": {"papel": "#E9DCC3", "coral": "#E8505B", "navy": "#1F2A44", "tinta": "#2B2622", "branco": "#FBF8F1", "amarelo": "#FFD23F", "ciano": "#3FD8FF", "terra": "#B9A47F"},
    "palavras": palavras, "capitulos": capitulos, "numero": sorted(numero, key=lambda n: n["t"]),
    "camera": sorted(camera, key=lambda k: k["t"]), "estilo": tab, "escuro": ESC, "mapa": mapa, "anc": anc, "cenas": cenas, "hud": hud,
    "fotos": sorted({c.get("arq") for c in cenas if c.get("arq")} | {a for c in cenas for a in c.get("arqs", [])} | {c.get(k) for c in cenas for k in ("antes", "depois", "fundo") if isinstance(c.get(k), str)}),
    "thumbs": {},
}
json.dump(cues, open(A / "cues.json", "w"), ensure_ascii=False, separators=(",", ":"))
json.dump({"_doc": "A/B (1 = B) do 006", "tab": tab}, open(A / "estilo_v2.json", "w"))
print(f"ok: {len(palavras)} palavras, {len(camera)} câmeras, {len(mapa)} mapa, {len(anc)} ancorados, {len(cenas)} cenas, {len(hud)} hud, {len(numero)} números; cicatrizes {len(CIC67)}+{len(CIC23)}")
print("avisos:", *avisos, sep="\n  ")
