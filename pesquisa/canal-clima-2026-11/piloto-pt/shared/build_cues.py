# Gera shared/cues.json (fonte única das duas Compositions) a partir de blocos.json, tempos.json, whisper.json e geo.json.
# Tempos de evento amarrados às palavras faladas (whisper small, 08/11/2026).
import json, math
from pathlib import Path

A = Path(__file__).parent
blocos = json.load(open(A / "blocos.json"))
tempos = json.load(open(A / "tempos.json"))
wh = json.load(open(A / "whisper.json"))
geo = json.load(open(A / "geo.json"))
pj = geo["proj"]
def P(lon, lat): return [round((lon - pj["lon0"]) * pj["cos"] * pj["k"], 3), round(-(lat - pj["lat0"]) * pj["k"], 3)]
C = geo["cidades"]
T = {b["id"]: b for b in tempos["blocos"]}

# ---------- legenda: palavras da tela com o tempo da palavra falada correspondente ----------
import re, unicodedata
def norm(w):
    w = unicodedata.normalize("NFD", w.lower()); w = "".join(c for c in w if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]", "", w.replace("km/h", "km"))
palavras = []
for b in blocos:
    tb = T[b["id"]]
    ws = [w for w in wh if tb["s"] - 0.25 <= w["s"] <= tb["e"] + 0.1]
    linhas = [l.split() for l in b["tela"].split("|")]
    toks = [w for l in linhas for w in l]
    n, m = len(toks), len(ws)
    tempos_tok, j = [None] * n, 0
    for i, tk in enumerate(toks):
        for k in range(j, min(m, j + 4)):
            a, c = norm(tk), norm(ws[k]["w"])
            if a and c and (a == c or a.startswith(c) or c.startswith(a)):
                tempos_tok[i] = ws[k]["s"]; j = k + 1; break
    # preenche os não casados por interpolação entre vizinhos casados
    for i in range(n):
        if tempos_tok[i] is None:
            ant = next((tempos_tok[k] for k in range(i - 1, -1, -1) if tempos_tok[k] is not None), tb["s"])
            prox = next((tempos_tok[k] for k in range(i + 1, n) if tempos_tok[k] is not None), tb["e"])
            tempos_tok[i] = ant + (prox - ant) * 0.5
    i = 0
    for li, l in enumerate(linhas):
        if li > 0 or b is not blocos[0]:
            palavras.append("|")
        for w in l:
            palavras.append([w, round(max(tempos_tok[i], tb["s"] - 0.05), 3)]); i += 1

def cam(t, alvo, dist, el, az, y=0.3):
    el, az = math.radians(el), math.radians(az)
    x, z = alvo
    return {"t": t, "offV": [0, -1.1] if dist < 10 else [0, 0], "alvo": [x, y, z], "pos": [round(x + dist * math.sin(az) * math.cos(el), 3), round(y + dist * math.sin(el), 3),
                                              round(z + dist * math.cos(az) * math.cos(el), 3)]}

MA, CH, SA = C["MARINGÁ"], C["CHAPECÓ"], C["SANTO AUGUSTO"]
SUL = [-0.9, 0.7]
camera = [
    cam(0.0, MA, 6.2, 40, -16), cam(3.2, MA, 7.0, 45, -2), cam(7.7, MA, 7.8, 50, 14),
    cam(9.3, CH, 6.8, 44, -10), cam(12.8, CH, 7.4, 47, 4), cam(15.9, CH, 7.8, 50, 14),
    cam(17.0, SA, 6.6, 44, -6), cam(20.8, SA, 7.4, 48, 10),
    cam(23.3, SUL, 20.5, 58, 0), cam(26.5, SUL, 19.5, 62, 6), cam(29.5, [-1.0, 0.5], 19.0, 60, -3), cam(34.8, [-1.0, 0.5], 18.5, 58, 4),
    cam(37.8, [-3.0, 0.0], 26.0, 56, 0), cam(41.0, [-4.0, -0.5], 28.0, 54, -6), cam(45.6, [-4.0, 0.0], 28.0, 55, 4),
    cam(48.6, [-2.0, 0.0], 25.0, 60, 0), cam(52.5, SUL, 22.0, 61, 6), cam(55.8, SUL, 21.0, 60, 10), cam(59.3, SUL, 23.0, 63, 15),
]

def tw(palavra, apos=0.0):
    """tempo da 1ª palavra falada que começa com <palavra> depois de <apos>"""
    for w in wh:
        if w["s"] >= apos and w["w"].lower().strip(",.?!").startswith(palavra.lower()):
            return w["s"]
    raise SystemExit(f"palavra não achada: {palavra} após {apos}")

t_cha, t_sa = tw("Chapecó"), tw("Santo")
pinos = [
    {"id": "ma", "nome": "MARINGÁ · PR", "sub": "02/11 · TORNADO F2", "x": MA[0], "z": MA[1], "t": 0.25},
    {"id": "ch", "nome": "CHAPECÓ · SC", "sub": "04/11 · 10H30", "x": CH[0], "z": CH[1], "t": t_cha},
    {"id": "sa", "nome": "SANTO AUGUSTO · RS", "sub": "07/11 · MADRUGADA", "x": SA[0], "z": SA[1], "t": t_sa},
]
t7 = tw("Sete")
extras = [("XANXERÊ", "XANXERÊ · SC"), ("ERVAL GRANDE", "ERVAL GRANDE · RS"), ("PALMEIRA DAS MISSÕES", "PALMEIRA DAS MISSÕES · RS"), ("RIO NEGRINHO", "RIO NEGRINHO · SC")]
for k, (cid, nome) in enumerate(extras):
    pinos.append({"id": cid, "nome": nome, "sub": "", "x": C[cid][0], "z": C[cid][1], "t": round(t7 + 0.3 + 0.38 * k, 3), "pequeno": True})
destaques = [{"nome": "MARINGÁ", "t": 0.6}, {"nome": "CHAPECÓ", "t": t_cha + 0.25}, {"nome": "SANTO AUGUSTO", "t": t_sa + 0.25}] + \
            [{"nome": cid, "t": p["t"] + 0.1} for (cid, _), p in zip(extras, pinos[3:])]
fios = [{"pontos": [MA, CH], "t0": T["b02"]["s"] + 0.1, "t1": t_cha}, {"pontos": [CH, SA], "t0": T["b03"]["s"] + 0.1, "t1": t_sa}]
funis = [{"x": MA[0] + 0.15, "z": MA[1] - 0.1, "t0": 0.5, "t1": T["b01"]["e"] - 0.2},
         {"x": CH[0] + 0.15, "z": CH[1] - 0.1, "t0": t_cha + 0.1, "t1": T["b02"]["e"] - 0.2},
         {"x": SA[0] + 0.15, "z": SA[1] - 0.1, "t0": t_sa + 0.05, "t1": T["b03"]["e"] - 0.1}]

# números do topo (oculto = some)
def num_cont(t, de, para, dur, unidade, faixa): return {"t": t, "de": de, "para": para, "ate": t + dur, "unidade": unidade, "faixa": faixa}
numero = [
    {"t": tw("tornado"), "valor": "F2", "faixa": "TORNADO · MARINGÁ · 02/11"},
    num_cont(tw("250"), 0, 250, 1.1, "km/h", "VENTOS ESTIMADOS · SIMEPAR"),
    {"t": tw("40"), "valor": "40%", "faixa": "DA CIDADE ATINGIDA"},
    {"t": T["b02"]["s"], "oculto": True},
    num_cont(tw("16"), 0, 16, 0.8, "km", "DE DESTRUIÇÃO · CHAPECÓ · 04/11"),
    {"t": tw("maior"), "valor": "50 ANOS", "faixa": "MAIOR EVENTO CLIMÁTICO · DEFESA CIVIL"},
    {"t": T["b03"]["s"], "oculto": True},
    num_cont(tw("50", T["b03"]["s"]), 0, 50, 0.8, "casas", "DESTELHADAS · SANTO AUGUSTO · 07/11"),
    num_cont(t7, 3, 7, 1.8, "tornados", "CONFIRMADOS EM 6 DIAS · 2 A 7/11"),
    {"t": T["b05"]["s"] - 0.1, "oculto": True},
    {"t": tw("muito", T["b09"]["s"]) - 0.35, "valor": "+2,2 °C", "faixa": "PACÍFICO EQUATORIAL · EL NIÑO MUITO FORTE"},
    {"t": tw("pico") - 0.6, "valor": "DEZ–JAN", "faixa": "PICO PREVISTO DO EL NIÑO · CLIMATEMPO"},
    {"t": T["b10"]["s"], "oculto": True},
]
capitulos = []
for b in blocos:
    if not capitulos or capitulos[-1]["nome"] != b["cap"]:
        capitulos.append({"t": max(0, T[b["id"]]["s"] - 0.15), "nome": b["cap"]})

# corredor de tempestades: elipse SW-NE (estilizada; Agrolink/MetSul: Bacia do Prata)
c0, ang, a_, b_ = (-57.0, -28.6), math.radians(38), 8.5, 2.7
corr = [P(c0[0] + a_ * math.cos(u) * math.cos(ang) - b_ * math.sin(u) * math.sin(ang),
          c0[1] + a_ * math.cos(u) * math.sin(ang) + b_ * math.sin(u) * math.cos(ang)) for u in [2 * math.pi * i / 48 for i in range(48)]]
t_corr = tw("corredores")
t_quente, t_frente, t_super = tw("Arquente"), tw("frentes"), tw("supercélulas")
setas = [
    {"cor": "#E07A3A", "pontos": [P(*q) for q in [(-60.2, -19.0), (-60.0, -22.6), (-58.9, -25.6), (-56.6, -27.4), (-53.8, -27.3)]], "t0": t_quente, "t1": t_quente + 2.4, "t2": T["b08"]["e"] + 0.3, "y": 0.95},
    {"cor": "#4C7FB8", "pontos": [P(*q) for q in [(-61.8, -35.6), (-59.2, -33.4), (-56.8, -31.0), (-54.5, -28.9)]], "t0": t_frente - 0.3, "t1": t_frente + 1.6, "t2": T["b08"]["e"] + 0.3, "y": 0.95},
]
nuvens = [{"x": P(-53.4, -27.0)[0], "z": P(-53.4, -27.0)[1], "s": 1.0, "t": t_super - 0.5, "t2": T["b09"]["s"] + 2.5},
          {"x": P(-51.6, -26.4)[0], "z": P(-51.6, -26.4)[1], "s": 0.8, "t": t_super - 0.2, "t2": T["b09"]["s"] + 2.7},
          {"x": P(-54.8, -28.6)[0], "z": P(-54.8, -28.6)[1], "s": 0.85, "t": t_super + 0.1, "t2": T["b09"]["s"] + 2.9}]
x0, z0 = P(-62, -20); x1, z1 = P(-44, -36)
t_sat = t_super + 0.4
satelite = {"caixa": [x0, z0, x1, z1], "op": [[0, 0], [t_sat, 0], [t_sat + 0.8, 0.6], [T["b09"]["s"] + 1.4, 0.6], [T["b09"]["s"] + 2.4, 0]]}

rot = lambda nome, lonlat, t0=0, t1=999, tipo="mapa": {"nome": nome, "x": P(*lonlat)[0], "z": P(*lonlat)[1], "t0": t0, "t1": t1, "tipo": tipo}
rotulos = [
    rot("PARANÁ", (-51.4, -24.6)), rot("SANTA CATARINA", (-50.3, -27.15)), rot("RIO GRANDE DO SUL", (-53.3, -29.7)),
    rot("ARGENTINA", (-60.8, -29.8), 23), rot("PARAGUAI", (-57.6, -23.4), 23), rot("URUGUAI", (-56.0, -32.9), 23),
    rot("CORREDOR DE TEMPESTADES", (-58.6, -30.2), t_corr, T["b08"]["s"] + 1.0, "corredor"),
    rot("AR QUENTE E ÚMIDO · DA AMAZÔNIA", (-58.2, -19.6), t_quente + 0.3, T["b08"]["e"] + 0.4, "quente"),
    rot("◀ ANDES", (-61.8, -24.8), tw("Andes") - 0.1, T["b08"]["e"] + 0.4, "seta"),
    rot("FRENTE FRIA · DA ARGENTINA", (-59.0, -35.6), t_frente, T["b08"]["e"] + 0.4, "fria"),
    rot("SUPERCÉLULAS", (-52.6, -25.9), t_super, T["b09"]["s"] + 2.4, "seta"),
]

clipes = [
    {"id": "ma", "src": "clips/maringa.mp4", "pino": "ma", "t0": T["b01"]["e"] - 5.7, "t1": T["b01"]["e"] + 0.15, "legenda": "MARINGÁ · PR · DEPOIS DO TORNADO",
     "credito": "VÍDEO: 7K DRONES · YOUTUBE · 07/11/2026"},
    {"id": "ch", "src": "clips/chapeco.mp4", "pino": "ch", "t0": t_cha + 0.4, "t1": T["b02"]["e"] + 0.2, "legenda": "CHAPECÓ · SC · 04/11, MANHÃ",
     "credito": "VÍDEO: CÂMERA AO VIVO PORTAL CHAPECÓ · 04/11/2026"},
    {"id": "sa", "src": "clips/santo-augusto.mp4", "pino": "sa", "t0": t_sa + 0.35, "t1": T["b03"]["e"] + 0.15, "legenda": "SANTO AUGUSTO · RS · 07/11",
     "credito": "VÍDEO: VAGNER ONUCZAK (MORADOR) · YOUTUBE"},
    {"id": "sat", "img": "img/goes-ir.png", "pino": None, "t0": t_sat + 0.2, "t1": T["b09"]["s"] + 2.4, "legenda": "SATÉLITE · 04/11 · 10H20",
     "credito": "IMAGEM: GOES-19 · NOAA/NASA (GIBS)"},
]
cues = {
    "_doc": "Gerado por shared/build_cues.py (não editar à mão). Tempos em segundos de audio/narracao.wav.",
    "fps": 30, "duracao": tempos["duracao"], "fim_fala": tempos["blocos"][-1]["e"],
    "paleta": {"papel": "#E9DCC3", "coral": "#E8505B", "navy": "#1F2A44", "tinta": "#2B2622", "branco": "#FBF8F1"},
    "palavras": palavras, "capitulos": capitulos, "numero": numero, "camera": camera,
    "luz": [[0, 1], [T["b05"]["s"] - 0.3, 1], [T["b05"]["s"] + 0.5, 0.5], [T["b07"]["s"] - 0.4, 0.5], [T["b07"]["s"] + 0.4, 1]],
    "quente": [[0, 0], [T["b09"]["s"], 0], [T["b09"]["s"] + 1.2, 0.75]],
    "pinos": pinos, "destaques": destaques, "fios": fios, "funis": funis,
    "corredor": {"anel": corr, "op": [[0, 0], [t_corr - 0.2, 0], [t_corr + 0.6, 1], [T["b08"]["s"] + 0.8, 1], [T["b08"]["s"] + 1.8, 0.35], [T["b09"]["s"], 0.35], [T["b09"]["s"] + 1, 0]]},
    "setas": setas, "nuvens": nuvens, "satelite": satelite, "rotulos_mapa": rotulos, "clipes": clipes,
    "rotulos_pinos_ate": T["b04"]["s"] - 0.1,
    "pergunta": {"t0": T["b05"]["s"] - 0.1, "t1": T["b06"]["s"] - 0.1, "texto": "O que está acontecendo no Sul do Brasil para ter tantos eventos dessa magnitude?"},
    "caixas": {"itens": [{"n": 1, "texto": "POR QUE ISSO ESTÁ ACONTECENDO?", "t": tw("Porque")},
                         {"n": 2, "texto": "QUAL O RISCO DE VOLTAR?", "t": tw("qual", T["b06"]["s"])},
                         {"n": 3, "texto": "ATÉ QUE PROPORÇÃO PODE CHEGAR?", "t": tw("até", T["b06"]["s"])}],
               "compacta": T["b07"]["s"] - 0.1, "some": T["b09"]["s"] - 0.2, "volta": T["b10"]["s"] - 0.1},
    "manchete": {"t0": tw("faz", T["b09"]["s"]) - 0.2, "t1": T["b10"]["s"] - 0.2, "veiculo": "CLIMATEMPO · 08/11/2026",
                 "texto": "“O El Niño faz com que esta combinação de fatores ocorra mais vezes.”", "destaque": "mais vezes"},
    "cta": {"t0": T["b10"]["s"] + 0.6},
    "fontes": "FONTES: SIMEPAR · DEFESA CIVIL SC/RS · CLIMATEMPO · ND MAIS · MAPA: IBGE · SATÉLITE: NOAA/NASA",
}
json.dump(cues, open(A / "cues.json", "w"), ensure_ascii=False, indent=1)
print("ok", len(palavras), "palavras;", [round(c["t"], 2) for c in camera][:4], "t_cha", t_cha, "t_sa", t_sa, "t7", t7, "t_super", t_super)
