# Storyboard em código do longo 01: gera shared/cues.json (fonte única da Composition "Longo") a partir de
# blocos.json, tempos.json, whisper.json, geo.json e clipes.json. Cada evento é amarrado à palavra falada (Whisper small).
# A tabela de transições e o resumo por bloco também vão para work/storyboard.txt (base do STORYBOARD.md).
import json, math, re, unicodedata
from pathlib import Path

A = Path(__file__).parent
blocos = json.load(open(A / "blocos.json"))
tempos = json.load(open(A / "tempos.json"))
wh = json.load(open(A / "whisper.json"))
geo = json.load(open(A / "geo.json"))
CL = json.load(open(A / "clipes.json"))
pj = geo["proj"]
def P(lon, lat): return [round((lon - pj["lon0"]) * pj["cos"] * pj["k"], 3), round(-(lat - pj["lat0"]) * pj["k"], 3)]
C = geo["cidades"]
T = {b["id"]: b for b in tempos["blocos"]}
BL = {b["id"]: b for b in blocos}
S = lambda b: T[b]["s"]
E = lambda b: T[b]["e"]
def F(b, k): return T[b]["frases"][k]["s"]
def FE(b, k): return T[b]["frases"][k]["e"]
avisos = []

def norm(w):
    w = unicodedata.normalize("NFD", w.lower()); w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", w)
def tw(palavra, b, apos=None, n=0):
    """tempo da (n+1)-ésima palavra falada que começa com <palavra> dentro do bloco b (depois de <apos>)"""
    t0 = (apos if apos is not None else S(b) - 0.35); t1 = E(b) + 0.2; alvos = [norm(x) for x in palavra.split("|")]; k = 0
    for w in wh:
        if t0 <= w["s"] <= t1 and any(norm(w["w"]).startswith(a) for a in alvos):
            if k == n: return w["s"]
            k += 1
    avisos.append(f"palavra '{palavra}' não achada em {b}; usei o meio do bloco")
    return round((max(t0, S(b)) + E(b)) / 2, 3)

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

# ---------------- câmera ----------------
camera = []
def cam(t, alvo, dist, el, az, y=0.3, corte=False):
    el, az = math.radians(el), math.radians(az); x, z = alvo
    k = {"t": round(t, 3), "alvo": [x, y, z], "pos": [round(x + dist * math.sin(az) * math.cos(el), 3), round(y + dist * math.sin(el), 3), round(z + dist * math.cos(az) * math.cos(el), 3)]}
    if corte: k["corte"] = True
    camera.append(k)
def off(c, dx=0, dz=0): return [c[0] + dx, c[1] + dz]

MA, CH, SA, XA, EG, RN, PM = C["MARINGÁ"], C["CHAPECÓ"], C["SANTO AUGUSTO"], C["XANXERÊ"], C["ERVAL GRANDE"], C["RIO NEGRINHO"], C["PALMEIRA DAS MISSÕES"]
GUA, RBI, QI, PIR, SJ = C["GUARACIABA"], C["RIO BONITO DO IGUAÇU"], C["QUEDAS DO IGUAÇU"], C["PIRAÍ DO SUL"], C["SAN JUSTO"]
BRA, ITA = C["BARRA DO RIO AZUL"], C["ITATIBA DO SUL"]
SUL = [-0.9, 0.7]
CONT = P(-60, -18)          # visão do continente (Amazônia → Sul)
OESTE = [-1.0, -0.8]

pinos, destaques, fios, funis, setas, nuvens, regioes, rastros, sats, ciclones, aneis, rotulos = [], [], [], [], [], [], [], [], [], [], [], []
def pino(id, cid, nome, sub, t, t2=None, pequeno=False, cor=None, ate=None, xz=None):
    x, z = xz or C[cid]
    p = {"id": id, "nome": nome, "sub": sub, "x": x, "z": z, "t": round(t, 3), "pequeno": pequeno}
    if t2: p["t2"] = round(t2, 3)
    if cor: p["cor"] = cor
    p["ate"] = round(ate if ate else (t2 if t2 else t + 6), 3)
    pinos.append(p)
def dest(nome, t, t2=None, cor=None):
    d = {"nome": nome, "t": round(t, 3)}
    if t2: d["t2"] = round(t2, 3)
    if cor: d["cor"] = cor
    destaques.append(d)
def rot(nome, lonlat, t0, t1, tipo="seta", xz=None):
    x, z = xz or P(*lonlat); rotulos.append({"nome": nome, "x": x, "z": z, "t0": round(t0, 3), "t1": round(t1, 3), "tipo": tipo})
def seta(cor, lonlats, t0, t1, t2, y=0.95, r=0.16, fluxo=False, engrossa=None, vel=0.18, xz=False):
    pts = [list(q) if xz else P(*q) for q in lonlats]
    s = {"cor": cor, "pontos": pts, "t0": round(t0, 3), "t1": round(t1, 3), "t2": round(t2, 3), "y": y, "r": r, "fluxo": fluxo, "vel": vel}
    if engrossa: s["engrossa"] = engrossa
    setas.append(s)
def janela_op(t0, t1, v=1.0, din=0.7, dout=0.7): return [[0, 0], [t0, 0], [t0 + din, v], [t1, v], [t1 + dout, 0]]
def anel_elipse(c0, ang, a_, b_, n=48):
    ang = math.radians(ang)
    return [P(c0[0] + a_ * math.cos(u) * math.cos(ang) - b_ * math.sin(u) * math.sin(ang), c0[1] + a_ * math.cos(u) * math.sin(ang) + b_ * math.sin(u) * math.cos(ang))
            for u in [2 * math.pi * i / n for i in range(n)]]
def caixa_sat(lon0, lon1, lat0, lat1): x0, z0 = P(lon0, lat1); x1, z1 = P(lon1, lat0); return [x0, z0, x1, z1]
SUL_BOX = caixa_sat(-66, -42, -38, -18)

midia, numero, manchetes, cartoes, graficos, checklists, transicoes = [], [], [], [], [], [], []
def clip(nome, t0, t1, lado="dir", pino=None):
    k = CL[nome]; d = t1 - t0; rate = 1.0
    if d > k["duracao"] - 0.1:
        rate = max(0.62, (k["duracao"] - 0.15) / d)
        if d * rate > k["duracao"] - 0.1: t1 = t0 + (k["duracao"] - 0.15) / rate; avisos.append(f"clipe {nome} encurtado para {t1 - t0:.1f}s")
    midia.append({"id": nome, "tipo": "video", "src": f"clips/{nome}.mp4", "fmt": k["fmt"], "t0": round(t0, 3), "t1": round(t1, 3), "lado": lado,
                  "legenda": k["legenda"], "credito": k["credito"], "pino": pino, "rate": round(rate, 3)})
def foto(img, t0, t1, legenda, credito, lado="dir", fmt="pol", pino=None):
    midia.append({"id": img, "tipo": "img", "src": f"img/{img}", "fmt": fmt, "t0": round(t0, 3), "t1": round(t1, 3), "lado": lado,
                  "legenda": legenda, "credito": credito, "pino": pino})
def num(t, valor=None, faixa="", de=None, para=None, dur=1.0, unidade=None):
    if valor is not None: numero.append({"t": round(t, 3), "valor": valor, "faixa": faixa, "unidade": unidade})
    else: numero.append({"t": round(t, 3), "de": de, "para": para, "ate": round(t + dur, 3), "unidade": unidade, "faixa": faixa})
def num_off(t): numero.append({"t": round(t, 3), "oculto": True})
def manchete(t0, t1, veiculo, texto, destaque, lado="esq"):
    manchetes.append({"t0": round(t0, 3), "t1": round(t1, 3), "veiculo": veiculo, "texto": texto, "destaque": destaque, "lado": lado})
def cartao(t0, t1, rotulo, texto, carimbo=None, t_carimbo=None, top=300):
    c = {"t0": round(t0, 3), "t1": round(t1, 3), "rotulo": rotulo, "texto": texto, "top": top}
    if carimbo: c["carimbo"] = {"texto": carimbo, "t": round(t_carimbo, 3)}
    cartoes.append(c)
def trans(t, tipo, dur=1.0, desc=""): transicoes.append({"t": round(t, 3), "tipo": tipo, "dur": dur, "desc": desc})
def meio(b1, b2): return (E(b1) + S(b2)) / 2

# luz/clima por tabelas
luz = [[0, 1]]; noite = [[0, 0]]; quente = [[0, 0]]; amazonia = [[0, 0]]; andes_t = [[0, 0]]; arquivo = [[0, 0]]; tremor = [[0, 0]]; desfoque = [[0, 0]]
def tab(lista, t, v, dur=0.6): lista.append([round(t, 3), lista[-1][1]]); lista.append([round(t + dur, 3), v])

# ======================= HOOK (b01–b07): o do piloto =======================
t_cha, t_sa, t7 = tw("Chapecó", "b02"), tw("Santo", "b03"), tw("Sete", "b04")
cam(0.0, MA, 6.2, 40, -16); cam(3.2, MA, 7.0, 45, -2); cam(E("b01") - 0.3, MA, 7.8, 50, 14)
cam(t_cha - 0.1, CH, 6.8, 44, -10); cam(t_cha + 3.5, CH, 7.4, 47, 4); cam(E("b02"), CH, 7.8, 50, 14)
cam(t_sa + 0.1, SA, 6.6, 44, -6); cam(E("b03"), SA, 7.4, 48, 10)
cam(S("b04") + 0.6, SUL, 20.5, 58, 0); cam(S("b05") + 1.5, SUL, 19.5, 62, 6); cam(S("b06"), [-1.0, 0.5], 19.0, 60, -3); cam(E("b06"), [-1.0, 0.5], 18.5, 58, 4)
cam(S("b07") + 2, SUL, 17.5, 55, 12); cam(E("b07") - 0.2, off(MA, 0, 0.5), 13.0, 62, 6)
pino("ma", "MARINGÁ", "MARINGÁ · PR", "02/11 · TORNADO F2", 0.25, ate=S("b04") - 0.1, t2=E("b07") - 1.0)
pino("ch", "CHAPECÓ", "CHAPECÓ · SC", "04/11 · 10H30", t_cha, ate=S("b04") - 0.1, t2=E("b07") - 1.0)
pino("sa", "SANTO AUGUSTO", "SANTO AUGUSTO · RS", "07/11 · MADRUGADA", t_sa, ate=S("b04") - 0.1, t2=E("b07") - 1.0)
for k, (cid, nome) in enumerate([("XANXERÊ", "XANXERÊ · SC"), ("ERVAL GRANDE", "ERVAL GRANDE · RS"), ("PALMEIRA DAS MISSÕES", "PALMEIRA DAS MISSÕES · RS"), ("RIO NEGRINHO", "RIO NEGRINHO · SC")]):
    pino("x" + str(k), cid, nome, "", t7 + 0.3 + 0.38 * k, pequeno=True, t2=E("b07") - 1.0)
    dest(cid, t7 + 0.4 + 0.38 * k, t2=E("b07") - 1.0)
dest("MARINGÁ", 0.6, t2=E("b07") - 1.0); dest("CHAPECÓ", t_cha + 0.25, t2=E("b07") - 1.0); dest("SANTO AUGUSTO", t_sa + 0.25, t2=E("b07") - 1.0)
fios += [{"pontos": [MA, CH], "t0": S("b02") + 0.1, "t1": t_cha, "t2": E("b07") - 1.0}, {"pontos": [CH, SA], "t0": S("b03") + 0.1, "t1": t_sa, "t2": E("b07") - 1.0}]
funis += [{"x": MA[0] + 0.15, "z": MA[1] - 0.1, "t0": 0.5, "t1": E("b01") - 0.2}, {"x": CH[0] + 0.15, "z": CH[1] - 0.1, "t0": t_cha + 0.1, "t1": E("b02") - 0.2},
          {"x": SA[0] + 0.15, "z": SA[1] - 0.1, "t0": t_sa + 0.05, "t1": E("b03") - 0.1}]
clip("maringa-drone", E("b01") - 5.6, E("b01") + 0.15, pino="ma")
clip("chapeco-centro", t_cha + 0.4, E("b02") + 0.2, pino="ch")
clip("santo-augusto-rua", t_sa + 0.35, E("b03") + 0.15, pino="sa")
num(tw("tornado", "b01"), "F2", "TORNADO · MARINGÁ · 02/11")
num(tw("250", "b01"), de=0, para=250, dur=1.1, unidade="km/h", faixa="VENTOS ESTIMADOS · SIMEPAR")
num(tw("40", "b01"), "40%", "DA CIDADE ATINGIDA · 1ªS ESTIMATIVAS")
num_off(S("b02")); num(tw("16", "b02"), de=0, para=16, dur=0.8, unidade="km", faixa="DE DESTRUIÇÃO · CHAPECÓ · 04/11")
num(tw("maior", "b02"), "50 ANOS", "MAIOR EVENTO CLIMÁTICO · DEFESA CIVIL")
num_off(S("b03")); num(tw("50", "b03"), de=0, para=50, dur=0.8, unidade="casas", faixa="DESTELHADAS · SANTO AUGUSTO · 07/11")
num(t7, de=3, para=7, dur=1.8, unidade="tornados", faixa="CONFIRMADOS EM 6 DIAS · 2 A 7/11"); num_off(S("b05") - 0.1)
tab(luz, S("b05") - 0.3, 0.5, 0.8); tab(luz, S("b07") - 0.4, 1.0, 0.8)
pergunta = {"t0": S("b05") - 0.1, "t1": S("b06") - 0.1, "texto": "O que está acontecendo no Sul do Brasil para ter tantos eventos dessa magnitude?"}
cx_itens = [{"n": 1, "texto": "POR QUE ISSO ESTÁ ACONTECENDO?", "t": tw("Por", "b06")}, {"n": 2, "texto": "QUAL O RISCO DE VOLTAR?", "t": tw("Qual", "b06")},
            {"n": 3, "texto": "ATÉ QUE PROPORÇÃO PODE CHEGAR?", "t": tw("proporção", "b06") - 0.5}]
cx_estados = [{"t": cx_itens[0]["t"], "modo": "grande", "ativa": 0, "feitas": []}, {"t": tw("caixinhas", "b07") + 0.3, "modo": "compacta", "ativa": 0, "feitas": []},
              {"t": S("b08") - 0.5, "modo": "oculto"}]

# T1: push-in que atravessa a nuvem → Maringá de madrugada
t_T1 = meio("b07", "b08")
trans(t_T1, "nuvem", 1.3, "push-in que atravessa uma nuvem: sai do Sul inteiro e cai sobre o norte do PR de madrugada")
tab(noite, t_T1 - 0.2, 0.75, 0.6)

# ======================= DIA 1 (b08–b10): Maringá =======================
cal = {"t0": S("b08") - 0.2, "t1": E("b18") + 0.8, "dias": [2, 3, 4, 5, 6, 7], "eventos": []}
cal["eventos"].append({"t": tw("primeiro", "b08"), "dia": 1, "tipo": "foco"})
cam(t_T1 + 0.25, P(-50.5, -28.5), 9.0, 50, -4, corte=True)
CIC = P(-48.6, -31.9)
cam(F("b08", 1) + 1.5, P(-50.0, -29.5), 15.0, 55, 4)
cam(F("b08", 2), off(MA, 0, 0.6), 11.0, 55, -6); cam(E("b08"), MA, 8.0, 50, 2)
ciclones.append({"x": CIC[0], "z": CIC[1], "t0": tw("ciclone", "b08") - 0.3, "t1": F("b08", 2) + 1.0, "s": 0.9})
rot("CICLONE", None, tw("ciclone", "b08") + 0.2, F("b08", 2), xz=off(CIC, 0, -1.6))
seta("#4C7FB8", [(-53.5, -31.5), (-52.5, -29.5), (-51.6, -27.3), (-51.4, -25.2), (-51.6, -23.8)], tw("frente", "b08"), tw("frente", "b08") + 2.2, F("b08", 2) + 1.5, y=0.55, r=0.11)
rot("FRENTE FRIA", (-50.6, -26.4), tw("frente", "b08") + 0.5, F("b08", 2) + 1, tipo="fria")
sats.append({"img": "img/sat-maringa-ir.jpg", "caixa": SUL_BOX, "op": janela_op(tw("supercélula", "b08") - 0.2, F("b09", 1), 0.5)})
foto("sat-maringa-ir.jpg", tw("supercélula", "b08") + 0.3, F("b09", 0) + 1.0, "SATÉLITE · 02/11 · 3H (APROX.)", "IMAGEM: GOES-19 · NOAA/NASA (GIBS)", lado="dir")
pino("ma1", "MARINGÁ", "MARINGÁ · PR", "02/11 · ~3H", tw("Maringá", "b08"), t2=E("b10") + 0.5)
dest("MARINGÁ", tw("Maringá", "b08") + 0.2, t2=E("b10") + 0.5)
funis.append({"x": MA[0] + 0.15, "z": MA[1] - 0.1, "t0": tw("Maringá", "b08") + 0.2, "t1": F("b09", 1) + 1, "s": 1.0})
num(tw("rajadas", "b09"), de=0, para=97, dur=1.0, unidade="km/h", faixa="RAJADA NO AEROPORTO · 3H11–3H17")
cam(F("b09", 1), MA, 6.5, 42, -14); cam(F("b09", 2), MA, 6.8, 46, 2)
tab(noite, F("b09", 2) - 0.5, 0.0, 1.0)
clip("maringa-arvore", F("b09", 2) + 0.2, F("b09", 2) + 5.6, pino="ma1")
num(tw("F2", "b09"), "F2", "SIMEPAR · VISTORIA DE CAMPO")
num(tw("180", "b09") - 0.1, "180–253", "VENTOS ESTIMADOS · ESCALA FUJITA", unidade="km/h")
rastros.append({"pontos": [off(MA, -0.13, 0.08), off(MA, 0.08, -0.06)], "largura": 0.035, "t0": tw("rastro", "b09"), "t1": tw("rastro", "b09") + 1.6, "t2": E("b10")})
num(tw("15", "b09"), "~15 km", "RASTRO EM LINHA RETA · SIMEPAR")
cam(E("b09"), MA, 6.0, 52, 10); cam(E("b10"), MA, 7.2, 50, 22)
num(tw("Ninguém", "b10"), "0", "MORTES · MARINGÁ")
clip("maringa-posto", tw("900", "b10") - 0.6, tw("219", "b10") + 1.6, pino="ma1")
num(tw("900", "b10"), de=0, para=900, dur=1.0, faixa="ÁRVORES NO CHÃO · 04/11")
num(tw("219", "b10"), de=0, para=219, dur=0.8, faixa="POSTES QUEBRADOS · 04/11")
num(tw("35", "b10"), "35 MIL", "IMÓVEIS AINDA SEM LUZ · 04/11")
clip("maringa-limpeza", tw("219", "b10") + 1.7, E("b10") + 0.6, pino="ma1")
num_off(E("b10") + 0.3)

# T2: whip pan Maringá → oeste de SC
t_T2 = meio("b10", "b11")
trans(t_T2, "whip", 0.6, "whip pan (chicote) com motion blur: de Maringá para o oeste de SC")
cam(t_T2 - 0.25, MA, 7.4, 50, 30); cam(t_T2 + 0.25, OESTE, 18, 58, -40, corte=True)

# ======================= DIA 3 (b11–b16): 4/11 =======================
cal["eventos"].append({"t": tw("Dois", "b11") , "dia": 3, "tipo": "foco"})
cal["eventos"].append({"t": tw("quarta", "b11"), "dia": 4, "tipo": "foco"})
cam(S("b11") + 1.5, OESTE, 17, 58, -10); cam(F("b11", 2) + 1.0, OESTE, 16, 56, 6)
sats.append({"imgs": [f"img/seq/{i:02d}.jpg" for i in range(1, 14)], "caixa": SUL_BOX, "seq": [F("b11", 1), FE("b11", 2) + 1.5],
             "op": janela_op(F("b11", 1) - 0.3, FE("b11", 2) + 1.2, 0.5)})
foto("seq/09.jpg", F("b11", 2) - 0.2, FE("b11", 2) + 0.8, "SATÉLITE · 04/11 · 07H → 13H", "IMAGEM: GOES-19 · NOAA/NASA (GIBS)", lado="dir")
seta("#1F2A44", [(-56.0, -29.6), (-54.6, -28.4), (-53.4, -27.1), (-52.2, -26.0), (-50.6, -25.6)], tw("linha", "b11"), tw("linha", "b11") + 2.5, E("b11") - 0.2, y=0.6, r=0.09)
rot("LINHA DE TEMPESTADES", (-55.6, -28.2), tw("linha", "b11") + 0.6, E("b11") + 0.5)
t_ch4 = tw("Chapecó", "b12")
cam(t_ch4, CH, 7.0, 46, -12); cam(F("b12", 2), CH, 6.4, 44, 0); cam(F("b12", 3), CH, 6.8, 48, 12); cam(E("b13"), CH, 7.2, 50, 24)
pino("ch4", "CHAPECÓ", "CHAPECÓ · SC", "04/11 · 10H30", t_ch4, t2=E("b14") + 0.3)
dest("CHAPECÓ", t_ch4 + 0.2, t2=E("b16"))
clip("chapeco-predios", t_ch4 + 0.3, F("b12", 2) + 0.4, pino="ch4")
aneis.append({"x": CH[0], "z": CH[1], "r": 0.55, "t0": tw("radar", "b12"), "t1": FE("b12", 1) + 1.5})
rot("ROTAÇÃO NO RADAR", None, tw("radar", "b12") + 0.4, FE("b12", 1) + 1.2, xz=off(CH, 0, 0.9))
num(tw("126", "b12"), de=0, para=126, dur=1.0, unidade="km/h", faixa="RAJADA · ESTAÇÃO DO INMET · CHAPECÓ")
clip("chapeco-aeroporto", F("b12", 3), FE("b12", 3) + 1.0, pino="ch4")
manchete(tw("tripulação", "b12") - 0.3, E("b12") + 1.4, "ESTADÃO/DGABC · 05/11/2026", "Tripulação: “o avião está chacoalhando muito.”", "chacoalhando muito")
num_off(F("b12", 3))
clip("chapeco-palmeiras", S("b13"), F("b13", 1) - 0.1, pino="ch4")
num(tw("2400", "b13") if False else tw("cerca", "b13"), de=0, para=2400, dur=1.2, faixa="CASAS E INDÚSTRIAS DESTELHADAS · BALANÇO DE 05/11")
clip("chapeco-telhas", F("b13", 1), E("b13") + 0.4, lado="esq")
num(tw("15", "b13"), "15 MIN", "AVISO DE TEMPORAL ANTES DO TORNADO · DEFESA CIVIL")
t_xa = tw("Xanxerê|Chanch|Xanx", "b14")
cam(S("b14") + 0.5, off(CH, 0.2, -0.2), 7.5, 50, 0); cam(t_xa + 0.5, XA, 6.6, 46, -10); cam(E("b14"), XA, 7.0, 50, 6)
num(tw("18|Dezoito", "b14"), "18 MIN", "DEPOIS · MESMA LINHA DE TEMPESTADES")
fios.append({"pontos": [CH, XA], "t0": tw("18|Dezoito", "b14"), "t1": t_xa, "t2": E("b16")})
pino("xa4", "XANXERÊ", "XANXERÊ · SC", "04/11 · 10H48", t_xa, t2=E("b16"))
dest("XANXERÊ", t_xa + 0.2, t2=E("b16"))
funis.append({"x": XA[0] + 0.1, "z": XA[1] - 0.1, "t0": t_xa + 0.1, "t1": E("b14")})
num(tw("40", "b14"), "~40 km", "DE CHAPECÓ")
clip("xanxere-rodovia", tw("Caminhões", "b14") - 0.3, E("b14") + 0.7, pino="xa4")
num_off(F("b14", 1))
t_eg, t_rn = tw("Erval", "b15"), tw("Negrinho", "b15")
cam(S("b15") + 1.0, EG, 6.8, 48, -6); cam(F("b15", 1) - 0.3, EG, 6.4, 46, 8)
clip("xanxere-drone", S("b15") - 0.6, t_eg - 0.2, lado="esq")
pino("eg4", "ERVAL GRANDE", "ERVAL GRANDE · RS", "04/11 · MANHÃ", t_eg, t2=E("b16"))
for nm, tt in [("ERVAL GRANDE", t_eg + 0.2), ("ITATIBA DO SUL", t_eg + 0.5), ("BARRA DO RIO AZUL", tw("Barra", "b15"))]: dest(nm, tt, t2=E("b16"))
funis.append({"x": EG[0] + 0.1, "z": EG[1] + 0.05, "t0": t_eg, "t1": F("b15", 1)})
clip("erval-eucalipto", t_eg + 0.3, F("b15", 1) - 0.2, pino="eg4")
rot("RIO URUGUAI", (-52.3, -27.35), S("b15") + 0.5, F("b15", 1), tipo="mapa")
cam(F("b15", 1) + 1.2, off(RN, -0.6, 0.2), 9.0, 52, 0); cam(t_rn + 0.3, RN, 6.6, 46, -8); cam(E("b15"), RN, 7.0, 50, 6)
pino("rn4", "RIO NEGRINHO", "RIO NEGRINHO · SC", "04/11 · 13H30", t_rn, t2=E("b16"))
dest("RIO NEGRINHO", t_rn + 0.2, t2=E("b16"))
clip("rionegrinho-casas", t_rn + 0.2, E("b15") + 0.5, pino="rn4")
num(tw("82", "b15"), de=0, para=82, dur=0.8, unidade="casas", faixa="ATINGIDAS · RIO NEGRINHO")
cam(S("b16") + 0.6, [0.6, -0.8], 13, 56, -4); cam(E("b16"), [0.6, -0.8], 12.5, 58, 6)
num(tw("4", "b16") if False else tw("Quatro", "b16"), de=1, para=4, dur=1.0, unidade="tornados", faixa="NUM ÚNICO DIA · 04/11")
clip("rionegrinho-telhado", F("b16", 1) - 0.3, E("b16") + 0.5, lado="dir")
num(tw("duas", "b16"), "2 MORTES", "DURANTE OS TEMPORAIS · SC · 04/11")
cal["eventos"] += [{"t": t_ch4, "dia": 4, "tipo": "tornado"}, {"t": t_xa, "dia": 4, "tipo": "tornado"}, {"t": t_eg, "dia": 4, "tipo": "tornado"}, {"t": t_rn, "dia": 4, "tipo": "tornado"}]
cal["eventos"].insert(1, {"t": tw("Maringá", "b08"), "dia": 2, "tipo": "tornado"})
num_off(E("b16") + 0.3)

# T3: luz que muda (dia → noite) + zoom para o noroeste gaúcho
t_T3 = meio("b16", "b17")
trans(t_T3, "luz", 1.4, "a luz muda: o dia vira madrugada enquanto a câmera desliza para o noroeste gaúcho")
tab(noite, t_T3 - 0.6, 0.8, 1.4)

# ======================= DIA 6 (b17–b18): 7/11 =======================
cal["eventos"].append({"t": tw("Sábado", "b17"), "dia": 7, "tipo": "foco"})
cam(t_T3 + 0.7, [-1.9, 0.4], 10, 54, -10); cam(F("b17", 1) + 1, [-1.9, 0.4], 9, 52, 0)
sats.append({"img": "img/sat-sa-ir.jpg", "caixa": SUL_BOX, "op": janela_op(F("b17", 1) - 0.2, F("b17", 2) + 0.5, 0.5)})
foto("sat-sa-ir.jpg", F("b17", 1) + 0.3, F("b17", 2) + 0.3, "SATÉLITE · 07/11 · MADRUGADA", "IMAGEM: GOES-19 · NOAA/NASA (GIBS)", lado="dir")
t_sa7, t_pm = tw("Santo", "b17"), tw("Palmeira", "b17")
cam(t_sa7, SA, 6.4, 44, -8); cam(F("b17", 3), off(SA, 0.25, 0.05), 6.8, 48, 4); cam(t_pm + 0.3, PM, 6.6, 46, 10)
pino("sa7", "SANTO AUGUSTO", "SANTO AUGUSTO · RS", "07/11 · 1H18", t_sa7, t2=E("b17") + 0.5)
pino("pm7", "PALMEIRA DAS MISSÕES", "PALMEIRA DAS MISSÕES · RS", "07/11 · 1H54", t_pm, t2=E("b17") + 0.5)
dest("SANTO AUGUSTO", t_sa7 + 0.2, t2=E("b17") + 0.5); dest("PALMEIRA DAS MISSÕES", t_pm + 0.2, t2=E("b17") + 0.5)
funis += [{"x": SA[0] + 0.1, "z": SA[1] - 0.1, "t0": t_sa7, "t1": F("b17", 3) + 0.5}, {"x": PM[0] + 0.1, "z": PM[1] - 0.1, "t0": t_pm, "t1": E("b17")}]
nuvens.append({"x": SA[0] + 0.2, "z": SA[1] - 0.3, "s": 0.9, "t": F("b17", 1), "t2": E("b17")})
num(tw("50", "b17"), de=0, para=50, dur=0.8, unidade="casas", faixa="DESTELHADAS · SANTO AUGUSTO · BALANÇO PRELIMINAR")
num(tw("36|Trinta", "b17"), "36 MIN", "DEPOIS · A MESMA SUPERCÉLULA")
fios.append({"pontos": [SA, PM], "t0": tw("36|Trinta", "b17"), "t1": t_pm, "t2": E("b17")})
num_off(E("b17"))
cal["eventos"] += [{"t": t_sa7, "dia": 7, "tipo": "tornado"}, {"t": t_pm, "dia": 7, "tipo": "tornado"}]
tab(noite, S("b18") - 0.6, 0.0, 1.0)
cam(S("b18") + 0.8, SUL, 19.5, 60, -4); cam(E("b18") + 0.3, SUL, 18.5, 60, 8)
todos = [("MARINGÁ", "MARINGÁ · PR"), ("CHAPECÓ", "CHAPECÓ · SC"), ("XANXERÊ", "XANXERÊ · SC"), ("RIO NEGRINHO", "RIO NEGRINHO · SC"),
         ("ERVAL GRANDE", "ERVAL GRANDE · RS"), ("SANTO AUGUSTO", "SANTO AUGUSTO · RS"), ("PALMEIRA DAS MISSÕES", "PALMEIRA DAS MISSÕES · RS")]
for k, (cid, nome) in enumerate(todos):
    pino(f"t{k}", cid, nome, "", S("b18") + 0.2 + 0.3 * k, pequeno=True, t2=E("b18") + 0.4)
for k, nm in enumerate(["MARINGÁ", "CHAPECÓ", "XANXERÊ", "RIO NEGRINHO", "ERVAL GRANDE", "ITATIBA DO SUL", "BARRA DO RIO AZUL", "SANTO AUGUSTO", "PALMEIRA DAS MISSÕES"]):
    dest(nm, tw("Nove", "b18") + 0.12 * k, t2=E("b18") + 0.4)
num(S("b18"), de=0, para=7, dur=2.0, unidade="tornados", faixa="CONFIRMADOS PELAS DEFESAS CIVIS · 2 A 7/11")
graficos.append({"tipo": "placar", "t0": F("b18", 1), "t1": E("b18") + 0.4, "itens": [["RS", 3, tw("Três", "b18")], ["SC", 3, tw("três", "b18", n=1) if True else 0], ["PR", 1, tw("um", "b18", apos=F("b18", 1) + 1.5)]]})
num(tw("Nove", "b18"), "9", "MUNICÍPIOS ATINGIDOS", unidade="municípios")
clip("chapeco-claroes", S("b18") + 0.4, F("b18", 1) + 0.8, lado="dir")
num_off(E("b18") + 0.4)

# T4: corte seco no impacto → arquivo
t_T4 = meio("b18", "b19")
trans(t_T4, "corte", 0.5, "corte seco no impacto (boom + flash + tremor) para o 'arquivo' (tom sépia)")
tab(tremor, t_T4, 1.0, 0.05); tab(tremor, t_T4 + 0.3, 0.0, 0.5)
tab(arquivo, t_T4, 0.85, 0.05); tab(arquivo, F("b22", 0) - 0.4, 0.0, 0.8)

# ======================= É INÉDITO? (b19–b24) =======================
cam(t_T4, off(XA, -0.6, -0.2), 9, 56, 20, corte=True); cam(E("b19"), off(XA, -0.6, -0.3), 8, 52, 8)
cartao(S("b19") + 0.5, E("b19") + 0.2, "A PERGUNTA", "Isso é inédito?", carimbo="NÃO.", t_carimbo=tw("não", "b19", apos=F("b19", 2)))
foto("modis-xanxere2015.jpg", F("b19", 1) + 0.2, E("b19") + 1.0, "SATÉLITE · 20/04/2015 · O DIA DO TORNADO DE XANXERÊ", "IMAGEM: NASA (MODIS TERRA, GIBS) · DOMÍNIO PÚBLICO", lado="dir")
t_x15 = tw("Xanxerê|Chanch|Xanx", "b20")
cam(t_x15, XA, 6.6, 46, -6); cam(F("b20", 1) - 0.4, XA, 7.0, 48, 6)
pino("x15", "XANXERÊ", "XANXERÊ · SC", "20/04/2015", tw("abril", "b20"), t2=E("b21") + 0.4, cor="#1F2A44")
dest("XANXERÊ", tw("abril", "b20") + 0.3, t2=F("b20", 1), cor="#B98B5A")
clip("xanxere2015-funil", tw("abril", "b20") + 0.4, tw("mais", "b20", apos=t_x15 + 1) - 0.2, pino="x15")
num(tw("2", "b20", apos=t_x15 + 1) if False else tw("mais", "b20", apos=t_x15 + 1), "+2 MIL", "CASAS ATINGIDAS · XANXERÊ · 2015")
clip("xanxere2015-cctv", tw("mais", "b20", apos=t_x15 + 1), F("b20", 1) + 0.6, lado="esq")
t_gua = tw("Guaraciaba", "b20")
cam(t_gua, GUA, 6.4, 44, -10); cam(E("b20"), GUA, 6.8, 48, 4)
pino("gua", "GUARACIABA", "GUARACIABA · SC", "07/09/2009 · F3", t_gua, t2=E("b21") + 0.4, cor="#1F2A44")
dest("GUARACIABA", t_gua + 0.2, t2=F("b21", 0) + 1, cor="#B98B5A")
clip("guaraciaba2009", t_gua + 0.3, E("b20") + 0.6, pino="gua")
num(tw("F3", "b20"), "F3", "GUARACIABA · 2009 · 4 MORTOS")
num_off(E("b20") + 0.4)
t_rbi = tw("Rio", "b21")
cam(S("b21") + 0.8, off(RBI, 0.1, 0.0), 8, 50, -8); cam(F("b21", 1), RBI, 6.0, 46, 4); cam(E("b21"), RBI, 6.6, 52, 16)
pino("rbi", "RIO BONITO DO IGUAÇU", "RIO BONITO DO IGUAÇU · PR", "07/11/2025 · F4", t_rbi, t2=E("b21") + 0.4, cor="#1F2A44")
dest("RIO BONITO DO IGUAÇU", t_rbi + 0.2, t2=E("b21") + 0.4, cor="#B98B5A"); dest("QUEDAS DO IGUAÇU", t_rbi + 0.4, t2=E("b21") + 0.4, cor="#B98B5A")
rbi_ini = off(QI, -0.15, -0.05); rbi_fim = [RBI[0] + (RBI[0] - QI[0]) * 1.15, RBI[1] + (RBI[1] - QI[1]) * 1.15]
rastros.append({"pontos": [rbi_ini, rbi_fim], "largura": 0.04, "t0": F("b21", 1) - 0.2, "t1": F("b21", 1) + 2.4, "t2": E("b21") + 0.3})
num(tw("F4", "b21"), "F4", "LAUDO FINAL DO SIMEPAR · 26/11/2025")
num(tw("75", "b21"), de=0, para=75, dur=1.0, unidade="km", faixa="DE RASTRO · ATÉ 3,2 KM DE LARGURA")
clip("rbi-comercio", tw("F4", "b21") + 0.3, F("b21", 2) - 0.1, pino="rbi")
clip("rbi-rastro", F("b21", 2), E("b21") + 0.6, lado="esq")
num(tw("90", "b21"), "90%", "DA ÁREA URBANA ATINGIDA · SIMEPAR")
num(tw("Sete", "b21", apos=F("b21", 2) + 1), "7", "MORTES NO PARANÁ", unidade="mortes")
num_off(E("b21") + 0.3)
cam(S("b22") + 0.5, SUL, 16, 62, -6); cam(E("b23"), SUL, 15, 64, 8)
tab(luz, S("b22") - 0.3, 0.6, 0.6); tab(luz, E("b23") + 0.2, 1.0, 0.8)
graficos.append({"tipo": "barras", "t0": S("b22") + 0.3, "t1": E("b22") + 0.5, "titulo": "TORNADOS REGISTRADOS NO BRASIL · PREVOTS",
                 "barras": [["2025", 92, tw("92", "b22"), "RECORDE"], ["2026 (ATÉ JULHO)", 81, tw("81", "b22"), ""]], "max": 100})
clip("celular-nuvem", tw("câmera", "b23") - 0.4, tw("câmera", "b23") + 4.3, lado="dir")
cartao(tw("2018", "b23") - 0.2, F("b23", 2) + 0.2, "DESDE 2018", "PREVOTS: uma plataforma reúne cada relato de tempestade severa.", top=330)
graficos.append({"tipo": "x10", "t0": F("b23", 2) - 0.1, "t1": F("b23", 3) - 0.1, "t_n": tw("10", "b23"), "rotulo": "RELATOS DE TORNADO NO BRASIL EM 30 ANOS", "fonte": "SILVA DIAS (2011), WEATHER, CLIMATE, AND SOCIETY"})
cartao(F("b23", 3) - 0.1, E("b23") + 0.4, "ESPECIALISTAS", "Detecção melhor ou mais tornados?", carimbo="SEM CONSENSO", t_carimbo=tw("consenso", "b23") - 0.2)
# corredor
cam(F("b24", 1) - 0.4, [-4.0, 1.0], 30, 58, -4); cam(F("b24", 2), [-4.0, 1.5], 31, 60, 6)
corr = anel_elipse((-57.0, -28.6), 38, 8.5, 2.7)
regioes.append({"anel": corr, "cor": "#E8505B", "op": janela_op(tw("faixa", "b24"), E("b24") + 0.6, 1.0, 0.8, 0.8), "max": 0.34})
rot("CORREDOR DE TEMPESTADES", (-58.6, -30.2), tw("faixa", "b24") + 0.4, E("b24") + 0.5, tipo="corredor")
for nome, ll in [("ARGENTINA", (-61.5, -29.5)), ("PARAGUAI", (-58.0, -23.2)), ("URUGUAI", (-56.0, -32.9))]:
    rot(nome, ll, tw("faixa", "b24") - 0.2, E("b24") + 0.5, tipo="mapa")
num(tw("segunda", "b24"), "2ª", "REGIÃO MAIS PROPÍCIA A TORNADOS · DEPOIS DOS EUA (PESQUISADORES)")
clip("dolores2016", tw("Uruguai", "b24") + 0.2, tw("Uruguai", "b24") + 5.4, lado="dir")
num_off(F("b24", 2) - 0.2)
manchete(F("b24", 2) - 0.1, E("b24") + 0.5, "ZIPSER ET AL. · BAMS · 2006 (SATÉLITE TRMM/NASA)", "As tempestades mais intensas da Terra: centro-sul dos EUA e sudeste da América do Sul.", "sudeste da América do Sul")

# T5: zoom-out orbital → continente
t_T5 = meio("b24", "b25")
trans(t_T5, "orbital", 1.4, "zoom-out orbital: a câmera gira e sobe até revelar o continente, da Amazônia aos Andes")
cam(t_T5 + 0.5, P(-58, -22), 52, 64, 30); cam(E("b25"), CONT, 70, 66, 6)

# ======================= CAIXA 1: POR QUÊ (b25–b33) =======================
cx_estados += [{"t": S("b25") - 0.3, "modo": "grande", "ativa": 1, "feitas": [], "volta": True}, {"t": E("b25") + 0.3, "modo": "compacta", "ativa": 1, "feitas": []}]
AMZ = P(-62, -6)
cam(F("b26", 1), P(-61, -10), 52, 60, -6); cam(F("b26", 2), P(-60, -16), 56, 58, 4); cam(E("b26"), P(-60, -20), 58, 56, 10)
tab(amazonia, tw("Amazônia", "b26") - 0.2, 1.0, 1.0); tab(amazonia, E("b33") + 0.5, 0.0, 1.2)
rot("AMAZÔNIA", (-62, -5), tw("Amazônia", "b26") + 0.2, E("b27"), tipo="mapa_grande")
for k, ll in enumerate([(-64, -5), (-59, -7), (-55, -4), (-67, -8), (-61, -10)]):
    x, z = P(*ll); nuvens.append({"x": x, "z": z, "s": 2.2, "t": F("b26", 1) + 0.25 * k, "t2": F("b27", 0), "y": 1.6})
jato = [(-63.0, -8.0), (-64.0, -13.0), (-63.6, -17.5), (-62.4, -21.5), (-60.0, -25.0), (-56.5, -27.0), (-53.0, -27.4)]
seta("#E07A3A", jato, tw("jato", "b26"), tw("jato", "b26") + 3.0, E("b28") + 0.6, y=1.6, r=0.5, fluxo=True, vel=0.12)
seta("#E07A3A", jato, S("b35") - 0.4, S("b35") + 1.0, E("b35") + 0.5, y=1.6, r=0.62, fluxo=True, vel=0.2,
     engrossa=[[0, 0], [S("b35") - 0.2, 0], [S("b35") + 0.8, 1], [E("b35"), 1], [E("b35") + 0.6, 0]])
rot("JATO DE BAIXOS NÍVEIS · ~1.500 M", (-58.5, -14.0), tw("jato", "b26") + 0.6, E("b28"), tipo="quente")
foto("sat-geocolor-larga.jpg", F("b26", 1) + 0.2, F("b26", 2) + 0.3, "SATÉLITE · 04/11 · AMAZÔNIA AO SUL", "IMAGEM: GOES-19 · NOAA/NASA (GIBS)", lado="dir")
cam(tw("parede", "b27"), P(-63, -22), 34, 30, 62); cam(F("b27", 1) + 1, P(-62, -24), 36, 34, 52); cam(E("b27"), P(-60, -24), 44, 48, 36)
tab(andes_t, tw("Cordilheira", "b27") - 0.2, 1.0, 0.8); tab(andes_t, E("b28"), 0.0, 1.0)
rot("CORDILHEIRA DOS ANDES", (-70.5, -24.0), tw("Cordilheira", "b27") + 0.2, E("b28"), tipo="seta")
rot("RIO INVISÍVEL DE UMIDADE", (-59.5, -21.0), tw("rio", "b27") - 0.1, E("b27") + 1.0, tipo="quente")
cam(F("b28", 0) + 0.5, P(-57, -29), 34, 56, 0); cam(F("b28", 1), P(-54, -28), 28, 54, 8); cam(E("b28"), P(-53, -27.5), 26, 50, 12)
seta("#4C7FB8", [(-64.0, -39.0), (-61.5, -35.5), (-58.8, -32.0), (-56.0, -29.4), (-53.8, -28.2)], tw("frentes", "b28"), tw("frentes", "b28") + 2.2, E("b28") + 1.0, y=1.2, r=0.45)
rot("FRENTE FRIA · DA ARGENTINA", (-60.5, -36.5), tw("frentes", "b28") + 0.5, E("b28") + 0.8, tipo="fria")
seta("#E07A3A", [P(-53.2, -27.4) + [0.6], P(-53.2, -27.4) + [2.0], P(-53.2, -27.4) + [3.6]], tw("empurrado", "b28"), tw("empurrado", "b28") + 1.0, E("b28") + 0.6, r=0.3, xz=True)
rot("GATILHO", (-52.0, -26.0), tw("gatilho", "b28") - 0.1, E("b28") + 0.6, tipo="seta")
clip("prateleira-timelapse", tw("encontra", "b28") - 0.2, E("b28") + 0.5, lado="dir")

# supercélula didática (b29–b31) sobre o oeste de SC
SCX = off(CH, -0.9, 0.2)
supercelula = {"x": SCX[0], "z": SCX[1], "escala": 0.85, "t0": S("b29") - 0.6, "t_fim": E("b31") + 0.4,
               "t_baixo": tw("chão", "b29") - 0.2, "t_alto": tw("cima", "b29") - 0.2, "t_rolo": tw("rolar", "b29") - 0.3,
               "t_sobe": tw("corrente", "b30") - 0.2, "t_ergue": tw("pé", "b30") - 0.9, "t_gira": tw("gira", "b30") - 0.3,
               "t_meso": tw("mesociclone", "b30") - 0.3, "t_descida": tw("descida", "b31") - 0.3, "t_funil": tw("estreita", "b31") - 0.3}
cam(S("b29") - 0.2, off(SCX, 0, 0.4), 10.7, 22, 30, y=1.5); cam(F("b29", 2), off(SCX, 0, 0.3), 9.9, 18, 12, y=1.5); cam(F("b29", 3) + 0.5, off(SCX, 0, 0.2), 9.2, 16, -8, y=1.5)
cam(E("b29"), off(SCX, 0, 0.2), 8.9, 15, -16, y=1.5); cam(F("b30", 1), off(SCX, 0, 0.0), 9.9, 20, -2, y=1.5); cam(F("b30", 2) + 1, off(SCX, 0, 0.0), 9.4, 24, 18, y=1.5)
cam(F("b31", 0) + 1, off(SCX, -0.2, 0.2), 8.9, 18, 40, y=1.5); cam(F("b31", 1) + 1, off(SCX, 0, 0.1), 8.2, 12, 24, y=1.5); cam(E("b31"), off(SCX, 0, 0.1), 9.6, 16, 6, y=1.5)
YS = 0.32  # altura do papel; rótulos 3D da supercélula
def rot_sc(nome, dx, dy, dz, t0, t1, tipo="seta"):
    rotulos.append({"nome": nome, "x": SCX[0] + dx * 0.85, "y": YS + dy * 0.85, "z": SCX[1] + dz * 0.85, "t0": round(t0, 3), "t1": round(t1, 3), "tipo": tipo})
rot_sc("VENTO PERTO DO CHÃO", 1.0, 0.3, -2.4, supercelula["t_baixo"] + 0.4, F("b30", 0), "quente")
rot_sc("LÁ EM CIMA: MAIS FORTE", -2.6, 3.4, 0.6, supercelula["t_alto"] + 0.4, F("b30", 0), "fria")
rot_sc("O AR ROLA, DEITADO", 0.3, 2.1, 0, supercelula["t_rolo"] + 0.4, supercelula["t_ergue"] + 0.6)
rot_sc("SUPERCÉLULA", 0.4, 4.0, 0, tw("supercélula", "b30") - 0.1, FE("b31", 2) + 0.4, "corredor")
rot_sc("MESOCICLONE", 1.5, 2.3, 0.4, supercelula["t_meso"] + 0.4, F("b31", 0) + 0.5)
rot_sc("DESCIDA DE AR FRIO", -1.7, 1.6, 1.6, supercelula["t_descida"] + 0.4, E("b31"), "fria")
clip("mesociclone", tw("supercélula", "b30") + 0.2, tw("mesociclone", "b30") + 0.8, lado="dir")
foto("us-moore-2013-radar-ktlx.jpg", tw("radar", "b30") - 0.6, F("b31", 1) - 0.4, "O GIRO NO RADAR · OKLAHOMA, 2013", "IMAGEM: NWS/NOAA · DOMÍNIO PÚBLICO", lado="esq")
clip("tail-cloud", F("b31", 1) - 0.2, tw("toca", "b31") - 0.1, lado="dir")
clip("tornado-nssl1973", tw("toca", "b31"), E("b31") + 1.6, lado="esq")
# b32–b33
cam(S("b32") + 0.5, OESTE, 12, 50, 10); cam(E("b32"), OESTE, 11, 52, 20)
num(tw("maioria", "b32"), "A MAIORIA", "DAS SUPERCÉLULAS NÃO GERA TORNADO · NOAA/NSSL")
foto("br-piracicaba-2026-supercelula.jpg", tw("maioria", "b32") + 0.2, F("b32", 1) + 0.5, "SUPERCÉLULA SEM TORNADO · SP · 2026", "FOTO: A.O MAPPING · WIKIMEDIA COMMONS · CC BY 4.0", lado="dir")
num_off(F("b32", 1))
foto("us-nuvem-funil-descendo-noaa.jpg", F("b32", 1) + 0.6, E("b32") + 1.2, "NUVEM-FUNIL DESCENDO · EUA", "FOTO: NOAA PHOTO LIBRARY · DOMÍNIO PÚBLICO", lado="dir")
manchete(F("b32", 1) + 0.2, E("b32") + 0.8, "NOAA/NSSL · SEVERE WEATHER 101", "“A verdade é que não entendemos totalmente.”", "não entendemos totalmente")
cam(S("b33") + 0.3, CONT, 62, 64, -4); cam(E("b33") + 0.6, CONT, 64, 66, 6)
checklists.append({"t0": S("b33") - 0.1, "t1": E("b33") + 0.9, "titulo": "OS 4 INGREDIENTES", "itens": [
    ["UMIDADE DA AMAZÔNIA", tw("Umidade", "b33")], ["A PAREDE DOS ANDES", tw("parede", "b33")], ["FRENTES FRIAS", tw("frentes", "b33")], ["VENTO QUE MUDA COM A ALTURA", tw("vento", "b33")]]})
tab(andes_t, tw("parede", "b33"), 0.7, 0.5); tab(andes_t, E("b33") + 0.5, 0.0, 0.8)
seta("#E07A3A", jato, tw("Umidade", "b33"), tw("Umidade", "b33") + 1.2, E("b33") + 0.4, y=1.6, r=0.5) if False else None
seta("#4C7FB8", [(-64.0, -39.0), (-61.5, -35.5), (-58.8, -32.0), (-56.0, -29.4), (-53.8, -28.2)], tw("frentes", "b33"), tw("frentes", "b33") + 1.2, E("b33") + 0.4, y=1.2, r=0.45)

# T6: rack focus → El Niño
t_T6 = meio("b33", "b34")
trans(t_T6, "rack", 1.4, "rack focus: o mapa desfoca e o painel do Pacífico entra em foco")
tab(desfoque, t_T6 - 0.4, 1.0, 0.6); tab(desfoque, S("b35") - 0.3, 0.0, 0.8)

# ======================= EL NIÑO (b34–b36) =======================
cam(t_T6 + 0.2, P(-75, -12), 75, 70, -10); cam(E("b34"), P(-72, -14), 72, 68, 0)
tab(quente, S("b34"), 0.75, 1.2); tab(quente, E("b36") + 0.6, 0.0, 1.0)
foto("sst-anom.jpg", S("b34") + 0.1, F("b34", 3) - 0.2, "TEMPERATURA DO MAR ACIMA DO NORMAL · 05/11/2026", "IMAGEM: NASA JPL (MUR SST, GIBS) · DOMÍNIO PÚBLICO", lado="centro", fmt="grande")
num(tw("dois", "b34") - 0.2, "+2 °C", "PACÍFICO EQUATORIAL · ACIMA DO NORMAL · NOAA")
num(tw("muito", "b34"), "MUITO FORTE", "EL NIÑO · E AINDA SE FORTALECENDO")
oni = [l.split() for l in open(A.parent / "dl/dados/oni.ascii.txt").read().split("\n")[1:] if l.strip()]
anual = {}
for s, ano, _, an in oni: anual[int(ano)] = max(anual.get(int(ano), -9), float(an))
graficos.append({"tipo": "oni", "t0": F("b34", 3) - 0.1, "t1": E("b34") + 0.6, "serie": [[a, round(v, 2)] for a, v in sorted(anual.items())],
                 "destaques": [1982, 1997, 2015, 2026], "titulo": "EL NIÑO MAIS FORTE DE CADA ANO (ONI, °C) · NOAA/CPC", "t_fim": tw("1950", "b34") - 0.5})
num(tw("83|80", "b34"), "83%", "CHANCE DE SER O MAIS FORTE DESDE 1950 · NOAA/CPC (OUT–DEZ)")
num_off(E("b34") + 0.4)
cam(S("b35") + 0.4, P(-60, -20), 56, 58, 4); cam(E("b35"), P(-57, -24), 44, 56, 10)
foto("sat-chapeco-ir.jpg", F("b35", 0) + 1.0, E("b35") + 0.6, "SATÉLITE · 04/11 · TEMPESTADES SOBRE O SUL", "IMAGEM: GOES-19 · NOAA/NASA (GIBS)", lado="dir")
rot("EL NIÑO: JATO MAIS FREQUENTE E FORTE", (-57.5, -17.0), S("b35") + 0.6, E("b35") + 0.4, tipo="quente")
for k, ll in enumerate([(-53.5, -27.0), (-51.8, -26.2), (-55.0, -28.8), (-52.5, -28.6)]):
    x, z = P(*ll); nuvens.append({"x": x, "z": z, "s": 1.3, "t": F("b35", 1) + 0.4 * k, "t2": E("b35") + 1.5, "y": 1.3})
cam(S("b36") + 0.5, SUL, 18, 62, -6); cam(E("b36"), SUL, 17, 62, 6)
tab(luz, S("b36") - 0.2, 0.6, 0.6); tab(luz, E("b36") + 0.3, 1.0, 0.6)
graficos.append({"tipo": "ciencia", "t0": S("b36") + 0.2, "t1": F("b36", 3) + 0.5, "itens": [
    ["O EL NIÑO CAUSA CADA TORNADO", False, tw("causa", "b36") - 0.2], ["HÁ ESTUDO QUE LIGA SÓ O EL NIÑO AO Nº DE TORNADOS", False, tw("estudo", "b36") - 0.2],
    ["ELE AUMENTA AS CHANCES", True, tw("aumenta", "b36") - 0.2]], "fonte": "CLIMATEMPO · AGROLINK · 2026"})
foto("us-supercelula-corrente-ascendente-sino.jpg", F("b36", 3) + 0.4, E("b36") + 0.4, "SUPERCÉLULA · EUA", "FOTO: ROLLINGSKYPHOTO · WIKIMEDIA COMMONS · CC BY 4.0", lado="dir")
cartao(F("b36", 3) - 0.1, E("b36") + 0.6, "IPCC · 6º RELATÓRIO (2021)", "Tendência de tornados: baixa confiança. Os registros são curtos demais.", carimbo="BAIXA CONFIANÇA", t_carimbo=tw("curtos", "b36") - 0.2, top=300)

# T7: match cut (círculo do selo → zona de risco no mapa)
t_T7 = meio("b36", "b37")
trans(t_T7, "match", 1.2, "match cut: o círculo coral do selo vira a zona de risco acesa no mapa (mesma posição e forma)")
RISK_C = P(-53.3, -27.0)
cam(t_T7 + 0.05, RISK_C, 11, 62, 4, corte=True)
regioes.append({"anel": anel_elipse((-53.3, -27.0), 0, 1.9, 1.6, 40), "cor": "#E8505B", "op": janela_op(t_T7, E("b37") + 0.3, 1.0, 0.3, 0.9), "max": 0.4, "pulsa": True}); cam(E("b37"), RISK_C, 12, 62, 10)

# ======================= CAIXA 2: RISCO (b37–b41) =======================
cx_estados += [{"t": S("b37") - 0.3, "modo": "grande", "ativa": 2, "feitas": [1], "volta": True}, {"t": E("b37") + 0.3, "modo": "compacta", "ativa": 2, "feitas": [1]}]
num(tw("Alto", "b37"), "ALTO", "RISCO DE NOVOS TEMPORAIS SEVEROS · ATÉ O VERÃO")
num_off(E("b37") + 0.3)
graficos.append({"tipo": "meses", "t0": S("b38") + 0.2, "t1": F("b39", 1) + 0.4, "meses": ["JUL", "AGO", "SET", "OUT", "NOV", "DEZ", "JAN", "FEV", "MAR"],
                 "marcas": [{"de": 5, "ate": 6, "texto": "PICO DO EL NIÑO", "cor": "#E07A3A", "t": tw("pico", "b38")},
                            {"de": 4, "ate": 6, "texto": "CHUVA ACIMA DA MÉDIA", "cor": "#4C7FB8", "t": F("b38", 1) + 0.4},
                            {"de": 1, "ate": 4, "texto": "TEMPORADA DE TORNADOS", "cor": "#E8505B", "t": S("b39") + 0.3}],
                 "hoje": {"i": 4, "t": tw("meio", "b39") - 0.3, "texto": "ESTAMOS AQUI"}})
cam(S("b38") + 0.6, P(-53.0, -27.0), 12, 60, -4); cam(E("b38"), P(-52.6, -27.0), 11, 60, 6)
oeste_sc = anel_elipse((-52.6, -26.9), 5, 1.4, 0.6, 32)
regioes.append({"anel": oeste_sc, "cor": "#4C7FB8", "op": janela_op(tw("destaque", "b38") - 0.2, E("b38") + 0.5, 1.0), "max": 0.4, "pulsa": True})
rot("CHUVA ACIMA DA MÉDIA · OESTE DE SC", (-52.6, -26.0), tw("destaque", "b38"), E("b38") + 0.4, tipo="fria")
manchete(F("b38", 1) + 0.3, F("b38", 2) + 1.2, "EPAGRI/CIRAM · 29/10/2026", "Chuva acima da média em SC, com destaque para o Oeste.", "destaque para o Oeste", lado="esq")
clip("prateleira-baixa", F("b38", 2) - 0.2, F("b38", 2) + 4.6, lado="dir")
manchete(F("b39", 1) - 0.1, E("b39") + 0.6, "METSUL · 2026", "Risco de eventos extremos também no verão.", "também no verão", lado="esq")
cam(S("b40") + 0.3, [-0.2, -1.8], 17, 62, -6); cam(E("b40"), [0.6, -3.0], 19, 64, 8)
arco = [P(*q) for q in [(-55.5, -28.0), (-54.6, -29.3), (-53.2, -29.4), (-52.0, -28.4), (-51.4, -27.2), (-51.6, -25.6), (-52.4, -24.9), (-53.6, -25.2), (-54.0, -26.4), (-55.0, -27.2)]]
regioes.append({"anel": arco, "cor": "#E8505B", "op": janela_op(tw("arco", "b40") - 0.2, E("b41") + 0.5, 1.0), "max": 0.45, "pulsa": True})
rot("REGIÕES MAIS EXPOSTAS", (-53.2, -24.4), tw("arco", "b40") + 0.3, E("b40") + 0.4, tipo="corredor")
pino("ma26", "MARINGÁ", "NORTE DO PARANÁ", "MARINGÁ · 02/11/2026", tw("norte", "b40", apos=F("b40", 1)), t2=E("b41"), ate=FE("b40", 1) + 1.5)
pino("pir26", "PIRAÍ DO SUL", "CAMPOS GERAIS", "PIRAÍ DO SUL · 08/08/2026 · F3", tw("Campos", "b40"), t2=E("b41"), ate=FE("b40", 1) + 1.5)
num(tw("dias", "b41", apos=F("b41", 1)), "1–2 DIAS", "DE ANTECEDÊNCIA PARA PREVER OS DIAS DE RISCO")
num(tw("minutos", "b41"), "MINUTOS", "DE ANTECEDÊNCIA DO ALERTA DE TORNADO")
foto("us-wall-cloud-raios-noaa.jpg", F("b41", 1) - 0.2, E("b41") + 0.6, "NUVEM-PAREDE · O SINAL DE ROTAÇÃO", "FOTO: NOAA/NSSL · DOMÍNIO PÚBLICO", lado="dir")
num_off(E("b41") + 0.3)

# T8: whip pan vertical → escala
t_T8 = meio("b41", "b42")
trans(t_T8, "whip_v", 0.6, "whip pan vertical (tilt rápido) com motion blur para a caixinha 3")
cam(t_T8 - 0.25, [0.6, -3.0], 19, 64, 12); cam(t_T8 + 0.25, SUL, 22, 70, -8, corte=True)

# ======================= CAIXA 3: ATÉ ONDE (b42–b46) =======================
cx_estados += [{"t": S("b42") - 0.3, "modo": "grande", "ativa": 3, "feitas": [1, 2], "volta": True}, {"t": E("b42") + 0.3, "modo": "compacta", "ativa": 3, "feitas": [1, 2]}]
cam(E("b43"), SUL, 21, 70, 6)
tab(luz, S("b43") - 0.2, 0.6, 0.6); tab(luz, E("b43") + 0.2, 1.0, 0.6)
foto("us-moore-2013-dano-ef5-nws.jpg", F("b43", 3) - 0.1, E("b43") + 0.8, "O QUE SOBRA DEPOIS DE UM EF5 · MOORE, EUA, 2013", "FOTO: NWS NORMAN/NOAA · DOMÍNIO PÚBLICO", lado="dir")
graficos.append({"tipo": "escala", "t0": S("b43") + 0.2, "t1": E("b43") + 0.5, "titulo": "ESCALA FUJITA (F) · VENTO ESTIMADO PELO ESTRAGO",
                 "faixas": [["F0", 64, 116], ["F1", 117, 180], ["F2", 182, 253], ["F3", 254, 332], ["F4", 333, 418], ["F5", 419, 512]],
                 "marcas": [["F2", "MARINGÁ 2026", tw("Maringá", "b43")], ["F4", "RIO BONITO DO IGUAÇU 2025", tw("Rio", "b43")], ["F5", "?", tw("F5|cinco", "b43", apos=F("b43", 3) + 1.0)]],
                 "t_barras": S("b43") + 0.4, "fonte": "NOAA/NWS"})
t_sj = tw("San", "b44")
UGA = P(-57.08, -29.76)
cam(S("b44") + 0.6, P(-57, -29.5), 14, 56, -4); cam(t_sj + 0.5, P(-58.8, -30.2), 12, 54, 6); cam(E("b44"), SJ, 8.5, 50, 10)
pino("sj", "SAN JUSTO", "SAN JUSTO · ARGENTINA", "10/01/1973 · F5", t_sj, t2=E("b44") + 0.5, cor="#1F2A44", xz=SJ)
fios.append({"pontos": [UGA, SJ], "t0": tw("300", "b44") - 0.4, "t1": tw("300", "b44") + 1.0, "t2": E("b44") + 0.5, "grosso": 2})
rot("~300 KM", None, tw("300", "b44") + 0.5, E("b44") + 0.4, xz=[(UGA[0] + SJ[0]) / 2, (UGA[1] + SJ[1]) / 2 - 0.6])
funis.append({"x": SJ[0] + 0.1, "z": SJ[1] - 0.1, "t0": t_sj + 0.2, "t1": E("b44") + 0.3, "s": 1.5})
num(tw("F5", "b44"), "0", "F5 CONFIRMADOS NO BRASIL")
num(t_sj + 0.2, "F5", "SAN JUSTO · ARGENTINA · 10/01/1973")
num(tw("63", "b44"), "63", "MORTOS · O ÚNICO F5 DA AMÉRICA DO SUL", unidade="mortos")
num_off(E("b44") + 0.4)
cam(S("b45") + 0.5, SUL, 22, 70, -4); cam(E("b45"), SUL, 21, 70, 6)
tab(luz, S("b45") - 0.2, 0.6, 0.6); tab(luz, E("b45") + 0.2, 1.0, 0.6)
graficos.append({"tipo": "comparacao", "t0": S("b45") - 0.1, "t1": E("b45") + 0.5,
                 "linhas": [["TORNADOS POR ANO", "92", "2025, RECORDE", "~1.200", "MÉDIA, NOAA", S("b45") + 0.3],
                            ["O MAIS FORTE", "F4", "PR, 2025", "EF5", "MOORE, JOPLIN…", tw("largo", "b45") - 1.0],
                            ["O MAIS LARGO", "3,2 KM", "RIO BONITO DO IGUAÇU", "4,2 KM", "EL RENO, 2013", tw("largo", "b45")]],
                 "barras": [3.2, 4.2, F("b45", 2) - 0.2]})
foto("us-el-reno-2013-tornado-cunha.jpg", tw("Reno", "b45") - 0.3, F("b45", 2) + 0.2, "EL RENO · EUA · 31/05/2013", "FOTO: DANIEL RODRIGUEZ · WIKIMEDIA COMMONS · CC BY 2.0", lado="dir")
clip("rbi-galpao", F("b45", 2), E("b45") + 0.8, lado="dir")
CH_C = CH
cam(S("b46") + 0.6, off(CH, 0, -0.3), 9, 52, -10); cam(F("b46", 2), off(CH, 0, -0.3), 7.5, 46, 4); cam(E("b46") - 0.3, [CH[0] + 0.35, CH[1] + 0.1], 8.0, 14, 10, y=1.3)
funis.append({"x": CH[0] + 0.35, "z": CH[1] + 0.1, "t0": tw("forte", "b46") - 0.3, "t1": E("b46") + 0.6, "s": 2.2})
pino("ch46", "CHAPECÓ", "CHAPECÓ", "~250 MIL HABITANTES", tw("Chapecó", "b46"), t2=E("b46"))
pino("ma46", "MARINGÁ", "MARINGÁ", "~410 MIL HABITANTES", tw("Maringá", "b46"), t2=E("b46"), pequeno=True)
clip("rbi-bombeiros", F("b46", 1) + 0.2, F("b46", 2) + 1.2, lado="dir")

# T9: match cut funil 3D → funil desenhado no post-it
t_T9 = meio("b46", "b47")
trans(t_T9, "match_funil", 1.0, "match cut: o funil 3D no centro vira o funil desenhado no post-it do quadro de cortiça")

# ======================= O QUE FAZER (b47–b49): quadro de cortiça (cobre o 3D) =======================
cx_estados.append({"t": t_T9, "modo": "oculto"})
cortica = {"t0": t_T9, "t1": S("b50") - 0.2, "itens": []}
def it(tipo, t, x, y, w, rot_, **kw): cortica["itens"].append({"tipo": tipo, "t": round(t, 3), "x": x, "y": y, "w": w, "rot": rot_, **kw})
it("titulo", t_T9 + 0.3, 640, 70, 640, -1, texto="O QUE FAZER")
it("postit", t_T9 + 0.05, 800, 330, 300, -3, cor="#F4D35E", titulo="", texto="", icone="funil")
it("postit", tw("receba", "b47") - 0.2, 120, 210, 330, -4, cor="#F7C59F", titulo="1 · ALERTA", texto="SMS 40199\ncom o seu CEP\n(de graça)")
it("celular", tw("Defesa", "b47") - 0.2, 470, 190, 270, 3, texto="DEFESA CIVIL ALERTA\nAlerta extremo: risco de tornado na sua região. Procure abrigo.")
it("postit", S("b48") - 0.2, 1180, 180, 330, 2, cor="#9AD1D4", titulo="2 · SINAIS", texto="nuvem baixa girando\nfunil · granizo grande\nronco de trem")
it("foto", tw("nuvem", "b48"), 1530, 160, 330, 4, src="clips/sinal-nuvem.mp4", legenda="NUVEM BAIXA E ESCURA", credito="NOAA/NSSL · CC BY")
it("foto", tw("funil", "b48") - 0.1, 1500, 470, 330, -3, src="clips/sinal-funil.mp4", legenda="NUVEM DE TEMPESTADE", credito="DE OLHO NO CÉU · YOUTUBE")
it("foto", tw("Granizo", "b48") - 0.1, 1180, 560, 300, 3, src="clips/sinal-granizo.mp4", legenda="GRANIZO GRANDE", credito="NOAA/NSSL · CC BY")
it("postit", S("b49") - 0.2, 150, 600, 330, 3, cor="#B8E0A0", titulo="3 · ABRIGO", texto="cômodo pequeno\nandar mais baixo\nsem janelas\nproteja a cabeça")
it("postit", tw("Longe", "b49") - 0.1, 520, 640, 300, -2, cor="#F4D35E", titulo="LONGE DE", texto="vidro · galpões\nárvores")
it("postit", tw("livre", "b49") - 0.3, 860, 690, 280, 4, cor="#F7C59F", titulo="AO AR LIVRE", texto="deite numa vala")
it("postit", tw("nunca", "b49") - 0.1, 800, 330, 300, -3, cor="#E8505B", titulo="NUNCA", texto="embaixo de\nviaduto", claro=True)
cobre3d = [[t_T9 + 0.9, S("b50") - 1.0]]

# T10: zoom-out do quadro → mapa ao entardecer
t_T10 = S("b50") - 0.6
trans(t_T10, "zoomout", 1.2, "zoom-out: o quadro de cortiça encolhe e revela o mapa do continente ao entardecer")
tab(quente, t_T10, 0.6, 1.2)

# ======================= A RESPOSTA (b50–b51) =======================
cam(t_T10, CONT, 66, 64, -8, corte=True); cam(F("b50", 2), P(-58, -22), 48, 58, 0); cam(F("b50", 3), SUL, 22, 60, 6); cam(E("b51") + 2.5, SUL, 19, 58, 14)
cartao(S("b50"), F("b50", 1) + 0.2, "A RESPOSTA", "O que está acontecendo no Sul?", top=260)
tab(amazonia, tw("Amazônia", "b50") - 0.2, 0.8, 0.8); tab(amazonia, F("b50", 3), 0.0, 1.0)
tab(andes_t, tw("Andes", "b50") - 0.2, 0.8, 0.6); tab(andes_t, F("b50", 3), 0.0, 1.0)
seta("#E07A3A", jato, tw("Amazônia", "b50"), tw("Amazônia", "b50") + 1.5, F("b50", 3) + 1, y=1.6, r=0.5, fluxo=True, vel=0.12)
seta("#4C7FB8", [(-64.0, -39.0), (-61.5, -35.5), (-58.8, -32.0), (-56.0, -29.4), (-53.8, -28.2)], tw("frio", "b50"), tw("frio", "b50") + 1.2, F("b50", 3) + 1, y=1.2, r=0.45)
regioes.append({"anel": corr, "cor": "#E8505B", "op": janela_op(tw("cantos", "b50"), E("b51") + 3, 1.0), "max": 0.3})
rot("EL NIÑO MUITO FORTE", (-60.0, -16.0), tw("turbinado", "b50"), F("b50", 3) + 0.6, tipo="quente")
for k, (cid, nome) in enumerate(todos):
    pino(f"f{k}", cid, nome, "", tw("cada", "b50") + 0.15 * k, pequeno=True)
cx_estados += [{"t": F("b50", 3), "modo": "final", "ativa": 0, "feitas": [1, 2, 3]}]
cta = {"t0": S("b51") + 0.1, "t_inscreve": tw("inscreve", "b51") - 0.2}

# fontes (barra do rodapé por capítulo)
fontes = [
    {"t": 0, "texto": "FONTES: SIMEPAR · DEFESA CIVIL SC/RS · CLIMATEMPO · ND MAIS · MAPA: IBGE · SATÉLITE: NOAA/NASA"},
    {"t": S("b08") - 0.5, "texto": "FONTES: SIMEPAR · BAND · GAZETA DO POVO · BRASIL DE FATO · SATÉLITE: GOES-19 NOAA/NASA · MAPA: IBGE"},
    {"t": S("b11") - 0.5, "texto": "FONTES: DEFESA CIVIL SC E RS · INMET · DIÁRIO DO SUDOESTE · ND MAIS · ESTADÃO · SATÉLITE: GOES-19 NOAA/NASA"},
    {"t": S("b17") - 0.5, "texto": "FONTES: DEFESA CIVIL RS · REVISTA OESTE · INFOBAE · CLIMATEMPO (7 TORNADOS, 07/11) · SATÉLITE: NOAA/NASA"},
    {"t": S("b19") - 0.5, "texto": "FONTES: CÂMARA DOS DEPUTADOS · UFRJ · GAZETA DO POVO · SIMEPAR (LAUDO 26/11/2025) · PREVOTS · AGÊNCIA BRASIL"},
    {"t": S("b24") - 0.3, "texto": "FONTES: BROOKS ET AL. 2003 · ZIPSER ET AL. 2006 (BAMS) · BBC BRASIL · MAPA: IBGE / NATURAL EARTH"},
    {"t": S("b25") - 0.5, "texto": "FONTES: CLIMATEMPO · MARENGO ET AL. 2004 · NOAA/NSSL · SALLJEX · MAPA: IBGE / NATURAL EARTH"},
    {"t": S("b34") - 0.5, "texto": "FONTES: NOAA/CPC (08/10/2026) · NASA JPL · CLIMATEMPO · AGROLINK · IPCC AR6"},
    {"t": S("b37") - 0.5, "texto": "FONTES: EPAGRI/CIRAM · CLIMATEMPO · METSUL · INPE · AGROLINK · MAPA: IBGE"},
    {"t": S("b42") - 0.5, "texto": "FONTES: NOAA/NWS (ESCALAS F/EF) · SIMEPAR · METEORED · NOAA/NSSL"},
    {"t": S("b47") - 0.5, "texto": "FONTES: DEFESA CIVIL (40199) · GOV. RS · DEFESA CIVIL DE CURITIBA · NWS"},
    {"t": S("b50") - 0.5, "texto": "FONTES: SIMEPAR · DEFESA CIVIL · CLIMATEMPO · NOAA · INPE · IPCC · MAPA: IBGE"},
]

cues = {
    "_doc": "Gerado por shared/build_cues.py (não editar à mão). Tempos em segundos de audio/narracao.wav.",
    "fps": 30, "duracao": tempos["duracao"], "fim_fala": tempos["blocos"][-1]["e"],
    "paleta": {"papel": "#E9DCC3", "coral": "#E8505B", "navy": "#1F2A44", "tinta": "#2B2622", "branco": "#FBF8F1"},
    "palavras": palavras, "capitulos": capitulos, "numero": sorted(numero, key=lambda n: n["t"]), "camera": camera,
    "luz": sorted(luz), "noite": noite, "quente": quente, "amazonia": amazonia, "andes": andes_t, "arquivo": arquivo, "tremor": tremor, "desfoque": desfoque,
    "pinos": pinos, "destaques": destaques, "fios": fios, "funis": funis, "setas": setas, "nuvens": nuvens, "regioes": regioes, "rastros": rastros,
    "sats": sats, "ciclones": ciclones, "aneis": aneis, "supercelula": supercelula, "rotulos_mapa": rotulos,
    "midia": midia, "manchetes": manchetes, "cartoes": cartoes, "graficos": graficos, "checklists": checklists, "calendario": cal,
    "pergunta": pergunta, "caixas": {"itens": cx_itens, "estados": cx_estados}, "cortica": cortica, "cobre3d": cobre3d,
    "transicoes": transicoes, "cta": cta, "fontes": fontes,
    "texturas": sorted({s.get("img") for s in sats if s.get("img")} | {i for s in sats for i in s.get("imgs", [])}),
}
# câmera em ordem (chaves fora de ordem quebrariam a interpolação)
cues["camera"].sort(key=lambda k: k["t"])
json.dump(cues, open(A / "cues.json", "w"), ensure_ascii=False, indent=0)
with open(A.parent / "work/storyboard.txt", "w") as f:
    for tr in transicoes: f.write(f"TRANSIÇÃO {tr['t']:7.2f}s {tr['tipo']}: {tr['desc']}\n")
    for m in midia: f.write(f"MÍDIA {m['t0']:7.2f}–{m['t1']:7.2f}s {m['tipo']} {m['id']} ({m['lado']})\n")
    f.write("\n".join(avisos))
real = sum(m["t1"] - m["t0"] for m in midia) + sum(1 for _ in [])
print(f"ok: {len(palavras)} palavras, {len(camera)} chaves de câmera, {len(midia)} mídias ({sum(1 for m in midia if m['tipo']=='video')} vídeos), {len(transicoes)} transições")
print("avisos:", *avisos, sep="\n  ")
