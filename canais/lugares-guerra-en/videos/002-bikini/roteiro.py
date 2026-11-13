#!/usr/bin/env python3
"""Fonte do storyboard do lugares-guerra-en 002 "Why Can't You Visit Bikini Atoll?" (youtube.videos id 32).
Uso: cd <pasta do vídeo> && python3 roteiro.py   (python3 puro, sem dependências)

O roteiro FINAL é o SCRIPT.md (fatos em FATOS.md/SOURCES.md). Os blocos de áudio vêm de tools/split_blocos.py
(qa/split_blocos.json; a voz já foi gerada com eles). Este arquivo define os planos visuais de cada bloco e valida:
narração idêntica ao SCRIPT.md, arquivos no midia.csv, Ficha em toda foto, tipo de tela ≤ 12 s, reuso, grifo literal.
Gera: blocos.json, storyboard.json, STORYBOARD.md, cenas.json (vazio: nenhuma imagem IA no corpo).
Código base: 001-midway/roteiro.py (mesmo canal). Bíblia: canais/lugares-guerra-en/biblia/.
"""
import csv
import json
import os
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MIDIA = AQUI / "midia"
WPS = 2.8                 # voz Narrator medida: 2.549 palavras em 15,2 min de áudio (≈168 ppm)
RUN_MAX = 12.0
JANELA = 60.0
INEDITO_ATE = 180.0
REUSO_LIBERADO = {"filme_reuniao_wyatt_1946.mp4"}
REAL_MIN = 0.85
W46, R46, DOE, NAV, CAS, LIM = ("filme_reuniao_wyatt_1946.mp4", "filme_moradores_rongerik_1946.mp4", "filme_crossroads_doe_1946.mp4",
                                "filme_crossroads_marinha_1949.mp4", "filme_castle_1954.mp4", "filme_limpeza_1969.mp4")
DUR_FILME = {W46: 471.0, R46: 572.0, DOE: 2552.0, NAV: 1622.0, CAS: 1261.0, LIM: 291.0}
# SHOTLIST.md: cartelas, claquetes, líderes, gráficos com apontador, apresentadores, exames médicos
FILME_PROIBIDO = {
    W46: [(0, 8), (176, 186), (268, 276), (468, 471)],
    R46: [(0, 6), (144, 150), (318, 326), (350, 356)],
    DOE: [(0, 47), (130, 240), (1044, 1120), (1645, 1668), (2518, 2552)],
    NAV: [(0, 165), (1440, 1455), (1615, 1622)],
    CAS: [(0, 58), (90, 125), (355, 368), (468, 500), (550, 560), (600, 635), (830, 860), (1240, 1261)],
    LIM: [(0, 6), (287, 291)],
}
CRED_FILME = {W46: "428-NPC-18008 (U.S. Navy, March 1946) · National Archives",
              R46: "428-NPC-18022 (U.S. Navy, 1946) · National Archives",
              DOE: "Project Crossroads (JTF-1, 1946) · U.S. Department of Energy",
              NAV: "Operation Crossroads (U.S. Navy, 1949) · NTIS / DoD",
              CAS: "Operation Castle (USAF Lookout Mountain Laboratory, 1954) · U.S. Department of Energy",
              LIM: "111-DD-278-69 (U.S. Army, 1969) · National Archives"}

MOV = {
    "zoom-in": ((0.5, 0.5, 1.04), (0.5, 0.5, 1.16)),
    "zoom-out": ((0.5, 0.5, 1.16), (0.5, 0.5, 1.04)),
    "pan-dir": ((0.44, 0.5, 1.12), (0.56, 0.5, 1.12)),
    "pan-esq": ((0.56, 0.5, 1.12), (0.44, 0.5, 1.12)),
    "tilt-baixo": ((0.5, 0.44, 1.12), (0.5, 0.56, 1.12)),
    "tilt-cima": ((0.5, 0.56, 1.12), (0.5, 0.44, 1.12)),
}


def _mov(m):
    if isinstance(m, str):
        if m.startswith("detalhe:"):
            x, y = (float(v) for v in m[8:].split(","))
            return m, ((x, y, 1.35), (x, y, 1.55))
        return m, MOV[m]
    return "custom", m


def kb(em, arq, mov="zoom-in", ficha=None, crop=None, num=None, enq=None):
    nome, (de, para) = _mov(mov)
    return dict(tipo="KenBurns", em=em, arq=arq, enq=enq or nome, de=de, para=para, ficha=ficha, crop=crop, num=num)


def filme(em, arq, tin, tout, oque, data, vel=1.0, num=None):
    return dict(tipo="Filme", em=em, arq=arq, enq=f"{tin:.1f}-{tout:.1f}", tin=tin, tout=tout, vel=vel, num=num,
                ficha=(data, oque, CRED_FILME[arq]))


def doc(em, arq, enq, grifo, frase=None, literal=True, num=None, ficha=None, regiao=None):
    return dict(tipo="DocGrifo", em=em, arq=arq, enq=enq, grifo=grifo, frase_doc=frase, literal=literal and bool(frase), num=num,
                ficha=ficha, regiao=regiao)


def num(em, valor, rotulo=""):
    return dict(tipo="Número", em=em, arq="codigo", enq="num:" + valor, valor=valor, rotulo=rotulo)


def mapa(em, nome, pontos, linhas, selo=None, nota=""):
    return dict(tipo="Mapa2D", em=em, arq="codigo", enq="mapa:" + nome, nome=nome, pontos=pontos, linhas=linhas,
                selo=selo, nota=nota)


def cartela(em, linhas, selo="SCHEMATIC"):
    return dict(tipo="Cartela", em=em, arq="codigo", enq="cartela:" + linhas[0], linhas=linhas, selo=selo)


def ea(em, antes, depois, rot1, rot2, num=None):
    return dict(tipo="EntaoAgora", em=em, arq=antes, arq2=depois, enq="ea", rot1=rot1, rot2=rot2, num=num)


def card(em):
    return dict(tipo="Card", em=em, arq="codigo", enq="card")


# Fichas: a 1ª linha (DATA · LUGAR) é a que vai à tela; vem da "Ficha sugerida" do midia.csv, com ajustes abaixo.
def _fichas():
    out = {}
    with open(AQUI / "midia.csv", newline="") as f:
        for r in csv.DictReader(f):
            m = re.search(r"Ficha sugerida:\s*(.+)", r["observacao"])
            if m:
                f = re.split(r"\.\s|\s(?=[A-Z][a-zà-ú])|\s\(|;", m.group(1))[0].strip().rstrip(".")
                out[r["arquivo"]] = (f, "", r["credito"])
    return out


FICHAS = _fichas()
FICHAS.update({
    "doc_crossroads_evacuacao.png": ("DEFENSE NUCLEAR AGENCY · OPERATION CROSSROADS 1946", "", "DNA 6032F"),
    "doc_crossroads_errou_alvo.png": ("DEFENSE NUCLEAR AGENCY · OPERATION CROSSROADS 1946", "", "DNA 6032F"),
    "doc_crossroads_minutos.png": ("DEFENSE NUCLEAR AGENCY · OPERATION CROSSROADS 1946", "", "DNA 6032F"),
    "doc_crossroads_saratoga.png": ("DEFENSE NUCLEAR AGENCY · JULY 25, 1946", "", "DNA 6032F"),
    "doc_castle_bravo_15mt.png": ("DEFENSE NUCLEAR AGENCY · CASTLE SERIES 1954", "", "DNA 6035F"),
    "doc_nv209_23testes.png": ("DEPARTMENT OF ENERGY · U.S. NUCLEAR TESTS 1945–1992", "", "DOE/NV-209"),
    "doc_aec1968_seguro.png": ("AUG 12 1968 · ATOMIC ENERGY COMMISSION", "", "AEC L-191"),
    "doc_interior1968_anuncio.png": ("1968 · DEPARTMENT OF THE INTERIOR", "", "Bikini Resettlement Program"),
    "doc_interior1968_johnson.png": ("1968 · PRESIDENT LYNDON JOHNSON", "", "Bikini Resettlement Program"),
    "doc_bnl1979_reevacuacao.png": ("1979 · BROOKHAVEN NATIONAL LABORATORY", "", "BNL 26797"),
    "doc_cafc2009_563mi.png": ("JAN 29 2009 · U.S. COURT OF APPEALS", "", "People of Bikini v. United States"),
    "doc_camara2005_sem_base_legal.png": ("MAY 25 2005 · U.S. HOUSE HEARING", "", "CHRG-109hhrg21448"),
    "doc_llnl_persuadidos.png": ("TODAY · LAWRENCE LIVERMORE NATIONAL LAB", "", "marshallislands.llnl.gov"),
    "foto_nagato_1946.jpg": ("1946 · NAGATO, YAMAMOTO'S FLAGSHIP", "", ""),
    "hoje_nps_saratoga_desenho.jpg": ("USS SARATOGA TODAY · SURVEY DRAWING", "", ""),
    "hoje_nps_arkansas_desenho.jpg": ("USS ARKANSAS TODAY · SURVEY DRAWING", "", ""),
    "hoje_kili_iss_2001.jpg": ("KILI ISLAND · FROM THE ISS", "", ""),
})


def px(b, W, H):
    return (round(b[0] / W, 4), round(b[1] / H, 4), round(b[2] / W, 4), round(b[3] / H, 4))


A4 = (2550, 3284)
G = {
    "evac_167": [px([468, 1800, 1294, 60], 2550, 3284)],
    "evac_7mar": [px([410, 1702, 839, 59], 2550, 3284)],
    "errou": [px([2164, 2542, 182, 59], 2550, 3284), px([318, 2589, 1520, 60], 2550, 3284)],
    "42mil": [px([1305, 1797, 385, 59], 2550, 3284)],
    "minutos": [px([730, 1004, 1236, 59], 2550, 3288), px([225, 1052, 1591, 59], 2550, 3288)],
    "banho": [px([844, 461, 910, 59], 2550, 3288)],
    "sara_1608": [px([319, 2643, 695, 60], 2550, 3288)],
    "sara_radio": [px([1535, 2743, 579, 59], 2550, 3288), px([222, 2792, 1036, 61], 2550, 3288)],
    "bravo": [px([501, 1642, 1747, 50], 2542, 3280), px([403, 1717, 1804, 50], 2542, 3280), px([402, 1792, 1701, 51], 2542, 3280)],
    "nv23": [px([671, 690, 856, 38], 2550, 3300)],
    "aec_volta": [px([921, 1492, 1195, 60], 2588, 3317)],
    "aec_seguro": [px([496, 1690, 1597, 62], 2588, 3317), px([349, 1740, 615, 60], 2588, 3317)],
    "lbj_anuncio": [px([477, 498, 1799, 68], 2544, 3300), px([348, 600, 1877, 68], 2544, 3300), px([349, 699, 1501, 68], 2544, 3300)],
    "lbj_modelo": [px([1657, 678, 627, 68], 2544, 3300), px([380, 780, 1805, 68], 2544, 3300), px([379, 886, 436, 68], 2544, 3300)],
    "bnl_dramatic": [px([829, 1154, 1200, 50], 2558, 3308)],
    "bnl_140": [px([1135, 1251, 917, 49], 2558, 3308), px([336, 1299, 1596, 53], 2558, 3308)],
    "cafc_563": [px([450, 761, 1800, 56], 2550, 3300), px([300, 876, 866, 56], 2550, 3300)],
    "cafc_pago": [px([796, 991, 1453, 56], 2550, 3300)],
    "camara_base": [px([687, 2445, 1250, 33], 2550, 3300), px([612, 2478, 426, 33], 2550, 3300)],
    "camara_regrets": [px([1650, 694, 287, 33], 2550, 3300), px([612, 726, 1325, 33], 2550, 3300)],
    "llnl_persuad": [px([1084, 1887, 942, 38], 3840, 3846), px([774, 1932, 1266, 38], 3840, 3846), px([774, 1976, 378, 38], 3840, 3846)],
    "llnl_23": [px([774, 1753, 1242, 38], 3840, 3846)],
    "pagina": [],
}

# Pontos de mapa (lon E 0–360, lat)
P = {"BIKINI": (165.4, 11.6), "HONOLULU": (202.14, 21.31), "RONGERIK": (167.45, 11.35), "KWAJALEIN": (167.73, 9.19),
     "KILI": (169.12, 5.64), "RONGELAP": (166.85, 11.16), "UTIRIK": (169.85, 11.23), "MAJURO": (171.38, 7.09),
     "GUAM": (144.79, 13.44), "TOKYO": (139.69, 35.68), "SAN FRANCISCO": (237.58, 37.77)}

B = []
SPLIT = {b["id"]: b["texto"] for b in json.load(open(AQUI / "qa/split_blocos.json"))}


def bloco(bid, *planos, ideia=False):
    B.append(dict(id=bid, texto=SPLIT[bid], ideia=ideia, planos=list(planos)))

# ===================================================================== planos
M46 = "MARCH 1946 · BIKINI ISLAND"
J46 = "JULY 1946 · BIKINI LAGOON"
EVAC, ERR, MIN, SARA = "doc_crossroads_evacuacao.png", "doc_crossroads_errou_alvo.png", "doc_crossroads_minutos.png", "doc_crossroads_saratoga.png"

# ===== Bloco 1: hook
bloco("B01a",
      filme("Watch the officer", W46, 30.0, 42.0, "Commodore Ben Wyatt and the people of Bikini", M46),
      kb("This is Bikini Atoll", "foto_moradores_mulheres_palha.jpg", "zoom-out"),
      filme("He's Commodore Ben Wyatt", W46, 196.0, 210.0, "Commodore Ben Wyatt (seated)", M46, num=("1946", "U.S. MILITARY GOVERNOR")),
      kb("and he's asking", "foto_moradores_embarque_lcm.jpg", "zoom-in"),
      ideia=True)
bloco("B01b",
      filme("Now look at the man", W46, 336.0, 348.0, "Juda, leader of Bikini (standing)", M46),
      filme("That's Juda,", W46, 352.0, 360.0, "Juda, leader of Bikini", M46),
      kb("And here's the strange", "foto_moradores_wyatt_filmagem.jpg", "detalhe:0.3,0.45"))
bloco("B01c",
      filme("The meeting did happen", R46, 60.0, 72.0, "A Sunday service", "1946 · SUNDAY SERVICE"),
      filme("What you're watching", W46, 256.0, 266.0, "The re-enactment, filmed by the Navy", M46),
      doc("A Defense Department", EVAC, "167", G["evac_167"], frase="The 167 Bikinians arrived at Rongerik the next day"),
      num("One hundred and sixty-seven", "167", "PEOPLE OF BIKINI · MARCH 1946"))

# ===== Bloco 2: o lugar
bloco("B02a",
      mapa("Bikini is a ring", "havai_bikini", ["HONOLULU", "BIKINI"], [("HONOLULU", "BIKINI", "2,500+ MI")]),
      kb("You probably know", "hoje_iss_2018_a.jpg", "zoom-in"),
      kb("Today, a handful", "hoje_ilha_bikini_s2_2025.jpg", "pan-dir"),
      ideia=True)
bloco("B02b",
      filme("There's no regular way", LIM, 8.0, 18.0, "Bikini from the air", "1969 · BIKINI ATOLL"),
      kb("And two things", "hoje_sentinel2_2025.jpg", "zoom-out"),
      filme("At the bottom of the lagoon", DOE, 2462.0, 2474.0, "USS Saratoga goes down", "JULY 25, 1946 · USS SARATOGA", num=("SUNK", "ON PURPOSE")))
bloco("B02c",
      kb("And in the reef", "hoje_cratera_bravo_s2_2025.jpg", "zoom-in", num=("1+ MILE", "WIDE")))

# ===== Bloco 2b: a pergunta
bloco("B03a",
      filme("Those 167 people", R46, 276.0, 290.0, "Women and children of Bikini", M46, num=("~5,400", "BIKINIANS TODAY")),
      kb("Some live on a small", "hoje_kili_iss_2001.jpg", "zoom-in"),
      kb("Almost none of them", "foto_ilha_bikini_barcos.jpg", "zoom-in"),
      ideia=True)
bloco("B03b",
      filme("Why can't you visit", W46, 448.0, 462.0, "The people of Bikini", M46),
      kb("It isn't a military base.", "foto_bravo_eneman_danos.jpg", "zoom-in"),
      kb("It isn't forgotten.", "hoje_iss_2018_b.jpg", "zoom-out"))
bloco("B03c",
      kb("It's a UNESCO", "hoje_landsat8_2013.jpg", "pan-dir"),
      doc("And the United States", "doc_aec1968_seguro.png", "seguro", G["aec_seguro"], literal=False),
      filme("What keeps it empty", DOE, 2246.0, 2258.0, "Test Baker, seen from the island", "JULY 25, 1946 · BIKINI"))
bloco("B03d",
      kb("Along the way", "foto_nagato_1946.jpg", "zoom-in"),
      filme("a bomb that missed", DOE, 610.0, 622.0, "Test Able", "JULY 1, 1946 · TEST ABLE"),
      kb("and an aircraft carrier", "foto_saratoga_afundando.jpg", "zoom-in"))
# ===== Bloco 3: Crossroads
bloco("B04a",
      filme("In 1946, the United States", DOE, 62.0, 74.0, "The target fleet from the air", J46),
      kb("What does this thing", "mapa_disposicao_able.jpg", "zoom-in"),
      filme("To find out,", DOE, 240.0, 250.0, "The target fleet at anchor", J46),
      ideia=True)
bloco("B04b",
      kb("More than ninety", "foto_frota_alvo_junho.jpg", "zoom-out", num=("90+", "TARGET SHIPS")),
      doc("Forty-two thousand men.", ERR, "42mil", G["42mil"], literal=False, num=("42,000", "MEN")),
      kb("A support fleet", "foto_frota_pearl_harbor.jpg", "pan-dir"),
      kb("On the decks,", "foto_cabras_conves.jpg", "zoom-in"),
      filme("to see what would", DOE, 300.0, 311.0, "A test animal aboard a target ship", "1946 · BIKINI LAGOON"))
bloco("B04c",
      kb("They needed a place", "foto_bikini_1944_costa_norte.jpg", "pan-dir"),
      filme("They picked Bikini.", DOE, 48.0, 58.0, "Bikini Atoll from the air", "1946 · BIKINI ATOLL"))
# ===== A Sunday in February
bloco("B05a",
      kb("For centuries,", "foto_bikini_1944_ponta_noroeste.jpg", "zoom-in"),
      kb("Germany and then Japan", "foto_bikini_1944_sudeste.jpg", "pan-esq"),
      filme("On Sunday, February 10th,", R46, 74.0, 88.0, "A Sunday service", "1946 · SUNDAY SERVICE", num=("FEB 10", "1946")),
      kb("On Bikini, people lived", "foto_moradores_mudanca.jpg", "zoom-in", crop=(0.0, 0.0, 0.94, 1.0)),
      ideia=True)
bloco("B05b",
      kb("Remember the coconuts.", "foto_moradores_mudanca.jpg", "detalhe:0.45,0.5", crop=(0.0, 0.0, 0.94, 1.0)),
      filme("According to Navy records,", W46, 140.0, 152.0, "Commodore Wyatt speaks to the islanders", M46),
      cartela("American scientists,", ["\"...for the good of mankind", "and to end all world wars.\"", "— COMMODORE BEN WYATT, AS QUOTED IN NAVY RECORDS"], selo="QUOTED"))
bloco("B05c",
      filme("Then he asked:", W46, 210.0, 222.0, "Commodore Wyatt and the interpreter", M46),
      filme("The answer from Juda", R46, 372.0, 386.0, "Juda answers", M46),
      cartela("kindness and benefit", ["\"...kindness and benefit to all mankind,", "my people will be pleased", "to go elsewhere.\"", "— JUDA, AS RECORDED"], selo="QUOTED"),
      filme("Wyatt couldn't promise", W46, 300.0, 312.0, "Commodore Wyatt and the people of Bikini", M46))

# ===== Rongerik
bloco("B06a",
      kb("On March 7th,", "foto_moradores_carregando_lst.jpg", "zoom-in"),
      kb("their canoes", "foto_canoa_lst1108.jpg", "pan-dir", crop=(0.0, 0.06, 0.94, 0.94)),
      mapa("They were taken", "rongerik", ["BIKINI", "RONGERIK"], [("BIKINI", "RONGERIK", "140 MI")]),
      kb("to Rongerik,", "foto_lst1108_rongerik.jpg", "zoom-out"),
      ideia=True)
bloco("B06b",
      filme("Starting on February 26th,", R46, 152.0, 166.0, "Navy Seabees build houses on Rongerik", "MARCH 1946 · RONGERIK"),
      kb("cisterns, water catchments", "foto_casas_rongerik.jpg", "zoom-in", num=("26", "HOUSE FRAMES")),
      doc("The U.S. government's own", "doc_llnl_persuadidos.png", "persuad", G["llnl_persuad"], frase="persuaded by the U.S. military to relocate"))
bloco("B06c",
      kb("Rongerik was smaller", "foto_casas_rongerik.jpg", "detalhe:0.5,0.35"),
      filme("Within a year,", R46, 452.0, 466.0, "Rongerik", "1946 · RONGERIK", num=("\"STARVING\"", "HAROLD ICKES, 1947")))
bloco("B07a",
      filme("It got worse.", R46, 6.0, 20.0, "Rongerik", "1946 · RONGERIK"),
      num("and in 1947", "1947", "FIRE IN RONGERIK'S COCONUT TREES"),
      ideia=True)
bloco("B07b",
      kb("In early 1948,", "foto_partida_lcvp.jpg", "zoom-in"),
      filme("where they lived in tents", R46, 510.0, 524.0, "Canvas tents", "1946 · MARSHALL ISLANDS"))
bloco("B07c",
      mapa("Then, on November 3rd,", "kili", ["BIKINI", "RONGERIK", "KILI"], [("BIKINI", "KILI", "400+ MI")]),
      kb("No lagoon to fish in", "hoje_kili_iss_2001.jpg", "detalhe:0.5,0.5"),
      filme("That's where most", R46, 290.0, 300.0, "The people of Bikini", M46))

# ===== Able
bloco("B08a",
      kb("Back on Bikini,", "foto_frota_alvo_aerea.jpg", "zoom-out", crop=(0.06, 0.06, 0.94, 0.94)),
      kb("American battleships,", "foto_prinz_eugen.jpg", "pan-dir"),
      filme("On July 1st, 1946,", DOE, 504.0, 516.0, "B-29 \"Dave's Dream\"", "JULY 1, 1946 · KWAJALEIN"),
      ideia=True)
bloco("B08b",
      filme("It exploded five hundred", NAV, 676.0, 688.0, "Test Able", "JULY 1, 1946 · TEST ABLE", num=("23,000", "TONS OF TNT")),
      doc("And it missed.", ERR, "errou", G["errou"], frase="between 1,500 and 2,000 feet", literal=False),
      kb("Even so, five ships", "foto_able_frota_depois.jpg", "zoom-in", num=("5", "SHIPS SUNK")))
bloco("B08c",
      kb("One of the ships", "foto_independence_fogo.jpg", "zoom-in"),
      filme("Reporters were taken", DOE, 1444.0, 1456.0, "USS Independence after Test Able", "JULY 1946 · USS INDEPENDENCE"),
      kb("The German cruiser", "foto_prinz_eugen_agosto.jpg", "zoom-in"))
bloco("B08d",
      filme("Four days later,", DOE, 720.0, 732.0, "The Able cloud", "JULY 1, 1946 · TEST ABLE", num=("JULY 5, 1946", "THE BIKINI SWIMSUIT · PARIS")),
      kb("He named it", "foto_able_aerea_cor.jpg", "zoom-in"))

# ===== Baker
bloco("B09a",
      kb("The second test", "foto_baker_mckinley.jpg", "zoom-in"),
      filme("On July 25th,", DOE, 2132.0, 2144.0, "Test Baker from the air", "JULY 25, 1946 · TEST BAKER", num=("90 FT", "UNDERWATER")),
      kb("A column of seawater", "foto_baker_larga.jpg", "pan-dir"),
      ideia=True)
bloco("B09b",
      filme("Then a wall", DOE, 2262.0, 2274.0, "The base surge, seen from Bikini Island", "JULY 25, 1946 · TEST BAKER"),
      filme("It bathed almost", NAV, 1306.0, 1318.0, "The base surge from the air", "JULY 25, 1946 · TEST BAKER"),
      kb("That afternoon,", "foto_saratoga_afundando_aerea.jpg", "zoom-in"))
bloco("B09c",
      doc("\"Radiological conditions", SARA, "radio", G["sara_radio"], frase="Radiological conditions prevented any attempt to save the ship"),
      kb("In the early hours", "foto_nagato_1946.jpg", "pan-esq"))
bloco("B09d",
      filme("Its radio room", DOE, 1222.0, 1234.0, "Nagato in the lagoon", J46))

# ===== Measured in minutes
bloco("B10a",
      kb("Now the Navy had", "foto_descontaminacao_vassouras.jpg", "zoom-in"),
      kb("and men with Geiger", "foto_geiger_dupla.jpg", "tilt-cima"),
      doc("It didn't work.", MIN, "minutos", G["minutos"], frase="was measured only in minutes"),
      ideia=True)
bloco("B10b",
      filme("The ships had become", NAV, 1485.0, 1497.0, "Hosing down a target ship", "AUGUST 1946 · BIKINI LAGOON"),
      kb("On August 10th,", "foto_descontaminacao_new_york.jpg", "pan-esq", crop=(0.0, 0.0, 0.94, 1.0), num=("AUG 10, 1946", "WORK STOPPED")))
bloco("B10c",
      filme("A day later,", DOE, 2382.0, 2394.0, "A radiological survey team", "1946 · BIKINI LAGOON"),
      kb("admitted the ships", "foto_descontaminacao_salt_lake.jpg", "tilt-cima"),
      kb("A third test", "foto_monitor_pensacola.jpg", "zoom-in", crop=(0.0, 0.0, 0.94, 1.0)),
      kb("The verdict", "foto_evacuacao_pennsylvania.jpg", "zoom-in", crop=(0.0, 0.0, 1.0, 0.93)))
bloco("B10d",
      cartela("With weapons like these", ["\"...it is quite possible to depopulate", "vast areas of the earth's surface...\"", "— JCS EVALUATION BOARD, 1947"], selo="QUOTED"),
      kb("leaving only vestigial", "foto_peixe_radioativo.jpg", "zoom-in"))

# ===== Bloco 4: por que fechou
bloco("B11a",
      kb("But the strangest part", "foto_baker_cogumelo.jpg", "zoom-in"),
      filme("Bikini stayed a test site", CAS, 640.0, 652.0, "A test barge in Bikini lagoon", "1954 · BIKINI LAGOON"),
      doc("The Department of Energy's", "doc_nv209_23testes.png", "nv23", G["nv23"], frase="Bikini Atoll", literal=False),
      ideia=True)
bloco("B11b",
      num("\"Bikini Atoll, twenty-three.\"", "23", "NUCLEAR TESTS · 1946–1958"),
      kb("Together, they released", "foto_bravo_aerea.jpg", "zoom-in", num=("78", "MEGATONS · ALL 23 TESTS")),
      filme("The people of Bikini waited", R46, 216.0, 230.0, "The new village on Rongerik", "1946 · RONGERIK"))
bloco("B12a",
      filme("On March 1st, 1954,", CAS, 296.0, 308.0, "Castle Bravo", "MARCH 1, 1954 · BIKINI ATOLL"),
      doc("The report reads:", "doc_castle_bravo_15mt.png", "bravo", G["bravo"], frase="had a yield of 15 MT", literal=False),
      ideia=True)
bloco("B12b",
      filme("About two and a half", CAS, 318.0, 330.0, "Castle Bravo", "MARCH 1, 1954 · BIKINI ATOLL", num=("×1,000", "HIROSHIMA")),
      kb("It left a crater", "hoje_cratera_bravo_s2_2025.jpg", "detalhe:0.45,0.45"),
      kb("Then the wind", "foto_bravo_estes.jpg", "pan-esq"))
bloco("B12c",
      mapa("It fell on Rongelap,", "fallout", ["BIKINI", "RONGELAP", "RONGERIK", "UTIRIK"],
           [("BIKINI", "RONGELAP", ""), ("BIKINI", "RONGERIK", ""), ("BIKINI", "UTIRIK", "FALLOUT · MARCH 1954")]),
      filme("and on a Japanese fishing", CAS, 412.0, 424.0, "Radiation survey in an island village", "MARCH 1954 · MARSHALL ISLANDS"),
      filme("Both islands had to be", CAS, 444.0, 452.0, "Islanders evacuated", "MARCH 1954 · MARSHALL ISLANDS", num=("157", "EVACUATED FROM UTIRIK")))
bloco("B12d",
      filme("One of the Japanese", CAS, 340.0, 352.0, "The Bravo cloud", "MARCH 1, 1954 · BIKINI ATOLL"),
      doc("Half a century later,", "doc_camara2005_sem_base_legal.png", "regrets", G["camara_regrets"], frase="still deeply regrets"))

bloco("B13a",
      kb("Then, in 1968,", "foto_retorno_1968_visita.jpg", "tilt-baixo"),
      doc("On August 12th,", "doc_interior1968_anuncio.png", "anuncio", G["lbj_anuncio"], literal=False),
      kb("That same day,", "foto_enyu_aerea.jpg", "zoom-in"),
      doc("Its report", "doc_aec1968_seguro.png", "seguro", G["aec_seguro"], frase="declares the atoll once again safe for human habitation"),
      ideia=True)
bloco("B13b",
      doc("Johnson's goal", "doc_interior1968_johnson.png", "modelo", G["lbj_modelo"], frase="a new and model community"),
      filme("In 1969, a joint task", LIM, 82.0, 94.0, "Clearing the island", "1969 · BIKINI ISLAND"),
      filme("New concrete houses", LIM, 22.0, 34.0, "A landing ship brings the cleanup crews", "1969 · BIKINI ISLAND"),
      kb("By the 1970s,", "foto_retorno_barco.jpg", "zoom-in"))
bloco("B13c",
      filme("By 1978,", LIM, 262.0, 274.0, "Bikini Island during the cleanup", "1969 · BIKINI ISLAND", num=("~140", "LIVING ON BIKINI BY 1978")))

bloco("B14a",
      kb("Now, the coconuts.", "foto_retorno_casa.jpg", "detalhe:0.55,0.4"),
      filme("And all of it", DOE, 2366.0, 2378.0, "Radiation survey on the beach", "1946 · BIKINI ISLAND"),
      kb("Government scientists measured", "foto_1978_amostras_peixe.jpg", "zoom-in"),
      ideia=True)
bloco("B14b",
      doc("Between April 1977", "doc_bnl1979_reevacuacao.png", "dramatic", G["bnl_dramatic"], frase="dramatic increases"),
      doc("The average was", "doc_bnl1979_reevacuacao.png", "pagina", G["pagina"], literal=False, num=("2.3 µCi", "AVERAGE CESIUM-137 · LIMIT 3")),
      kb("Several people", "foto_1978_tarrafa.jpg", "zoom-in"))
bloco("B14c",
      doc("So in August 1978,", "doc_bnl1979_reevacuacao.png", "140", G["bnl_140"], frase="the 140 Bikinians in residence at that time"),
      filme("For the second time", R46, 326.0, 332.5, "A landing ship on the beach", "1946 · MARSHALL ISLANDS"),
      kb("This time, the danger", "foto_ilha_bikini_barcos.jpg", "detalhe:0.5,0.45"))

bloco("B15a",
      kb("Then came the money.", "hoje_landsat8_2013.jpg", "zoom-in"),
      doc("In 1986, a treaty", "doc_camara2005_sem_base_legal.png", "pagina", G["pagina"], literal=False, num=("$150M", "1986 · \"FULL SETTLEMENT\"")),
      kb("In 2001, that tribunal", "foto_retorno_1968_visita.jpg", "detalhe:0.5,0.4"),
      ideia=True)
bloco("B15b",
      doc("It awarded the people", "doc_cafc2009_563mi.png", "563", G["cafc_563"], frase="in compensation"),
      kb("Two hundred and seventy-eight", "mapa_carta_bikini_leste.jpg", "detalhe:0.45,0.4", num=("$278M", "FOR THE LOSS OF THEIR LAND")),
      doc("The fund paid", "doc_cafc2009_563mi.png", "pago", G["cafc_pago"], literal=False, num=("0.4%", "OF THE AWARD PAID")))
bloco("B15c",
      kb("That's about zero", "foto_retorno_moradores.jpg", "detalhe:0.5,0.55"),
      doc("In 2005, the State", "doc_camara2005_sem_base_legal.png", "base", G["camara_base"], frase="no legal basis under the Settlement Agreement for considering additional payments"),
      kb("The Bikinians sued", "foto_bikini_1944_sudeste.jpg", "zoom-in"))
bloco("B15d",
      doc("In 2009, an appeals", "doc_cafc2009_563mi.png", "pagina", G["pagina"], literal=False),
      kb("In 2010, the Supreme", "foto_cargueiro_encalhado.jpg", "pan-dir"))

# ===== Bloco 5: o que ainda está lá
bloco("B16a",
      kb("There's one more reason", "hoje_ilha_bikini_s2_2025.jpg", "zoom-in"),
      filme("In 2019, a team", CAS, 700.0, 712.0, "A radiation check (1954)", "1954 · BIKINI ATOLL", num=("190", "MILLIREM A YEAR (2019)")),
      kb("The limit agreed", "hoje_landsat8_2013.jpg", "detalhe:0.6,0.5", num=("100", "AGREED LIMIT")),
      ideia=True)
bloco("B16b",
      filme("In some soil samples", CAS, 426.0, 440.0, "Radiation survey (1954)", "1954 · MARSHALL ISLANDS"),
      kb("at up to three times", "foto_enyu_aerea.jpg", "detalhe:0.5,0.5"),
      kb("Another study found", "foto_retorno_casa.jpg", "pan-esq"))
bloco("B16c",
      kb("The fish in the lagoon", "foto_1978_amostras_peixe.jpg", "detalhe:0.5,0.6"),
      filme("The danger is the soil,", LIM, 96.0, 108.0, "Bulldozing the island's soil", "1969 · BIKINI ISLAND"),
      kb("Coconut trees pull", "foto_ilha_bikini_barcos.jpg", "pan-dir"),
      num("About ninety percent", "~90%", "OF THE DOSE: CESIUM FROM SOIL INTO PLANTS"))
bloco("B16d",
      kb("Government scientists found", "foto_1978_tarrafa.jpg", "detalhe:0.45,0.45"),
      doc("The Department of Energy", "doc_llnl_persuadidos.png", "texto", None, literal=False, regiao=(0.19, 0.40, 0.36, 0.20)),
      kb("But a fix on paper", "foto_cargueiro_encalhado.jpg", "zoom-in"))
bloco("B17a",
      kb("Then there's the crater.", "hoje_sentinel2_2025.jpg", "detalhe:0.22,0.3"),
      ea("This is Bravo,", "par_bravo_1954.jpg", "par_bravo_hoje.jpg", "1954", "2025"),
      ideia=True)
bloco("B17b",
      kb("A dark blue circle", "hoje_cratera_bravo_s2_2025.jpg", "zoom-out"),
      filme("Seventy years later,", LIM, 10.0, 20.0, "Bikini from the air", "1969 · BIKINI ATOLL"),
      kb("Astronauts on the International", "hoje_iss_2018_b.jpg", "zoom-in"))
bloco("B18a",
      kb("And now, the strangest", "foto_saratoga_convoo_teste.jpg", "zoom-in"),
      filme("When it sank,", NAV, 928.0, 940.0, "USS Saratoga in the target fleet", J46),
      ideia=True)
bloco("B18b",
      ea("It's still down there,", "par_saratoga_1946.jpg", "par_saratoga_hoje.jpg", "1946", "1990", num=("180 FT", "TO THE BOTTOM")),
      kb("When National Park Service", "hoje_nps_saratoga_desenho.jpg", "pan-dir"))
bloco("B18c",
      filme("They found the planes", DOE, 2412.0, 2424.0, "USS Saratoga after Test Baker", "JULY 25, 1946 · USS SARATOGA"),
      kb("Three Helldiver", "hoje_nps_saratoga_convoo.jpg", "detalhe:0.5,0.5", num=("3 + 1", "HELLDIVERS + AVENGER, STILL ABOARD")),
      kb("And the bombs never", "hoje_nps_saratoga_canhao.jpg", "pan-dir"))
bloco("B18d",
      num("UNESCO lists", "BOMBS + FUEL", "STILL IN THE LAGOON · UNESCO"),
      filme("Not far away", NAV, 1520.0, 1532.0, "Nagato in 1946", J46),
      kb("The American battleship", "hoje_nps_arkansas_casco.jpg", "pan-dir"),
      kb("For twelve years,", "hoje_nps_nagato_canhao.jpg", "zoom-in", num=("1996–2008", "DIVE TOURS")))
bloco("B19a",
      mapa("And Kili,", "kili_hoje", ["BIKINI", "KILI", "MAJURO"], [("BIKINI", "KILI", "")]),
      kb("The ocean is coming", "hoje_kili_iss_2001.jpg", "zoom-out"),
      filme("In 2016, king tides", R46, 356.0, 368.0, "The people of Bikini", "1946 · MARSHALL ISLANDS"),
      ideia=True)
bloco("B19b",
      filme("Hundreds of Bikinians", R46, 330.0, 344.0, "The people of Bikini", "1946 · MARSHALL ISLANDS"),
      kb("In 2023, the local", "foto_moradores_mudanca.jpg", "pan-dir", crop=(0.0, 0.0, 0.94, 1.0)))
bloco("B19c",
      filme("A lawsuit says", R46, 236.0, 250.0, "Houses on Rongerik", "1946 · RONGERIK", num=("$89,002", "TRUST FUND (WAS ~$60 MILLION)")))
# ===== Bloco 6: fecho
bloco("B20a",
      kb("So why can't you visit", "foto_baker_larga.jpg", "zoom-out"),
      filme("Because a Navy wanted", NAV, 1244.0, 1256.0, "Test Baker", "JULY 25, 1946 · TEST BAKER"),
      kb("Because the tests didn't stop", "foto_bravo_cogumelo_doe.jpg", "zoom-in"),
      ideia=True)
bloco("B20b",
      doc("Because the island", "doc_aec1968_seguro.png", "seguro", G["aec_seguro"], literal=False),
      kb("And because the ground", "foto_bikini_1944_costa_norte.jpg", "zoom-in"))
bloco("B21a",
      filme("Watch the beach", W46, 50.0, 62.0, "Commodore Ben Wyatt and the people of Bikini", M46),
      filme("Juda, standing up,", W46, 362.0, 374.0, "Juda, leader of Bikini", M46),
      ideia=True)
bloco("B21b",
      kb("A hundred and sixty-seven", "foto_moradores_carregando_lst.jpg", "detalhe:0.55,0.5"),
      num("Eighty years later,", "167 → ~5,400", "BIKINIANS, 1946 → TODAY"),
      filme("The scene was staged.", W46, 462.0, 468.0, "The people of Bikini", M46))
bloco("B21c",
      kb("If someone in your family", "foto_baker_mckinley.jpg", "detalhe:0.6,0.4"),
      card("This is Clearance"))

CENAS = []

CENAS = []

# ---------------------------------------------------------------- validação e geração
ERROS, AVISOS = [], []


def palavras(t):
    return len(t.replace("*", "").split())


def norm(t):
    t = t.lower().replace("–", " ").replace("—", " ").replace("-", " ")
    t = re.sub(r"[^a-z0-9 ]", " ", t.replace(",", ""))
    return " ".join(t.split())


def script_md():
    out, cur = {}, None
    for l in (AQUI / "SCRIPT.md").read_text().split("\n"):
        m = re.match(r"^### (B\d\d) ", l)
        if m:
            cur = m.group(1)
            out[cur] = []
            continue
        if cur is None:
            continue
        if l.startswith("**Tela:**") or l.startswith("## ") or l.startswith("---"):
            cur = None
            continue
        if l.strip():
            out[cur].append(l.strip())
    return {k: " ".join(v) for k, v in out.items()}


def midia_csv():
    with open(AQUI / "midia.csv", newline="") as f:
        return {r["arquivo"]: r for r in csv.DictReader(f)}


def fmt(s):
    return f"{int(s // 60)}:{s % 60:04.1f}"


sys.path.insert(0, str(AQUI / 'tools'))
from split_blocos import VOZ_SUBS  # mesma grafia usada na geração da voz


def voz(t):
    for a, b in VOZ_SUBS:
        t = t.replace(a, b)
    return t


def main():
    # 1. narração idêntica ao SCRIPT.md
    ref = script_md()
    meus = {}
    for b in B:
        meus.setdefault(b["id"][:3], []).append(b["texto"])
    for k in sorted(set(ref) | set(meus)):
        a, r = " ".join(meus.get(k, [])), ref.get(k, "")
        if a != r:
            i = next((j for j in range(min(len(a), len(r))) if a[j] != r[j]), min(len(a), len(r)))
            ERROS.append(f"narração {k} diverge do SCRIPT.md na posição {i}: roteiro.py «{a[i-30:i+40]}» × SCRIPT «{r[i-30:i+40]}»")
    for b in B:
        n = len(re.findall(r"[.?!][\"”]?(\s|$)", b["texto"]))
        if not 1 <= n <= 6:
            AVISOS.append(f"{b['id']}: {n} frases (alvo 2–5)")

    csvm = midia_csv()
    planos, t = [], 0.0
    for b in B:
        texto = b["texto"]
        pos = []
        ini = 0
        for p in b["planos"]:
            i = texto.find(p["em"], ini)
            if i < 0:
                ERROS.append(f"{b['id']}: âncora não encontrada (ou fora de ordem): «{p['em']}»")
                i = ini
            pos.append(i)
            ini = i + 1
        if pos and pos[0] != 0:
            ERROS.append(f"{b['id']}: o 1º plano precisa começar no início do bloco")
        dur_b = palavras(texto) / WPS
        b["inicio"], b["dur"] = round(t, 2), round(dur_b, 2)
        for k, p in enumerate(b["planos"]):
            fim = pos[k + 1] if k + 1 < len(pos) else len(texto)
            frase = texto[pos[k]:fim].strip()
            d = palavras(frase) / WPS
            q = dict(p)
            q.update(bloco=b["id"], frase=frase, inicio=round(t, 2), dur=round(d, 2))
            planos.append(q)
            t += d
    total = t

    # 2. arquivos existem e estão no midia.csv; filmes; docs literais; KenBurns com movimento
    for q in planos:
        for arq in [q["arq"], q.get("arq2")]:
            if not arq or arq == "codigo":
                continue
            if not (MIDIA / arq).exists():
                ERROS.append(f"{q['bloco']}: arquivo inexistente em midia/: {arq}")
            if arq not in csvm:
                ERROS.append(f"{q['bloco']}: arquivo fora do midia.csv: {arq}")
            if arq.startswith("foto_") and arq not in FICHAS:
                ERROS.append(f"{q['bloco']}: foto sem Ficha: {arq}")
        if q["tipo"] == "KenBurns":
            if tuple(q["de"]) == tuple(q["para"]):
                ERROS.append(f"{q['bloco']}: KenBurns parado ({q['arq']})")
            if q["dur"] > 8.5:
                AVISOS.append(f"{q['bloco']}: KenBurns longo ({q['dur']:.1f} s) em {q['arq']}: conferir se o movimento sustenta")
            q["ficha"] = q.get("ficha") or FICHAS.get(q["arq"])
        if q["tipo"] == "DocGrifo":
            q["ficha"] = q.get("ficha") or FICHAS.get(q["arq"])
            if q["literal"] and norm(q["frase_doc"]) not in norm(q["frase"]):
                ERROS.append(f"{q['bloco']}: grifo literal «{q['frase_doc']}» não é lido na narração do plano «{q['frase'][:60]}»")
        if q["tipo"] == "Filme":
            seg = (q["tout"] - q["tin"]) / q["vel"]
            if q["vel"] < 0.55 or q["vel"] > 1.0:
                ERROS.append(f"{q['bloco']}: velocidade de filme fora de 0,55–1,0 ({q['vel']})")
            if seg + 0.15 < q["dur"]:
                ERROS.append(f"{q['bloco']}: trecho do filme curto ({seg:.1f} s) para {q['dur']:.1f} s de narração ({q['arq']} {q['tin']}–{q['tout']})")
            if q["tout"] > DUR_FILME[q["arq"]]:
                ERROS.append(f"{q['bloco']}: trecho além do fim do filme")
            for a, z in FILME_PROIBIDO[q["arq"]]:
                if q["tin"] < z and q["tout"] > a:
                    ERROS.append(f"{q['bloco']}: trecho {q['tin']}–{q['tout']} toca cartela/créditos ({a}–{z}) em {q['arq']}")
    # 3. tipo de tela: no máximo RUN_MAX s seguidos (com a voz real: durações de qa/tempos.json, gravado pelo tools/build.py)
    reais = {}
    if (AQUI / "qa/tempos.json").exists():
        reais = {(t["bloco"], t["em"]): t["d"] for t in json.load(open(AQUI / "qa/tempos.json"))}
    run_t, run_tipo, run_ini = 0.0, None, None
    for q in planos:
        d = reais.get((q["bloco"], q["em"]), q["dur"])
        if q["tipo"] == run_tipo:
            run_t += d
        else:
            run_tipo, run_t, run_ini = q["tipo"], d, q
        # com a voz real a conta inclui a pausa de bloco/capítulo (o 1º plano começa no meio dela): tolerância de 1 s;
        # Filme até 14 s (cada trecho é outro plano de câmera, todos < 7 s pela regra do Ford)
        if run_t > (14.0 if run_tipo == "Filme" else RUN_MAX) + (1.0 if reais else 0) + 1e-6:
            ERROS.append(f"{q['bloco']}: {run_tipo} por {run_t:.1f} s seguidos (desde {run_ini['bloco']} «{run_ini['em']}»); máximo {RUN_MAX:.0f} s")

    # 4. reuso: aparições (planos consecutivos do mesmo arquivo = 1 aparição)
    vistos, ult_enq = {}, {}
    ant_arq = None
    reuso_t = 0.0
    for q in planos:
        arqs = [a for a in [q["arq"], q.get("arq2")] if a and a != "codigo"]
        q["reuso"] = False
        for arq in arqs:
            chave = (arq, q["enq"])
            if q["tipo"] == "Filme":
                # trecho de filme: reuso = sobreposição com um trecho já mostrado
                ja = [p for p in planos[:planos.index(q)] if p["tipo"] == "Filme" and p["arq"] == arq
                      and p["tin"] < q["tout"] and p["tout"] > q["tin"]]
                prev = planos[planos.index(q) - 1] if planos.index(q) else None
                if ja and not (prev is ja[-1]):
                    q["reuso"] = True
                    if q["inicio"] - (ja[-1]["inicio"] + ja[-1]["dur"]) < JANELA:
                        ERROS.append(f"{q['bloco']}: trecho de filme {q['enq']} repetido em menos de {JANELA:.0f} s")
                    if q["inicio"] < INEDITO_ATE:
                        ERROS.append(f"{q['bloco']}: reuso de trecho de filme antes de 3:00")
                continue
            if chave in ult_enq and q["inicio"] - ult_enq[chave] < JANELA and ant_arq != arq:
                ERROS.append(f"{q['bloco']}: {arq} [{q['enq']}] repetido em menos de {JANELA:.0f} s")
            if arq in vistos and ant_arq != arq:
                q["reuso"] = True
                if q["inicio"] < INEDITO_ATE and arq not in REUSO_LIBERADO:
                    ERROS.append(f"{q['bloco']}: reuso de {arq} antes de 3:00 ({fmt(q['inicio'])})")
            vistos.setdefault(arq, q["inicio"])
            ult_enq[chave] = q["inicio"] + q["dur"]
        if q["tipo"] == "Filme":
            ant_arq = None
        if q["reuso"]:
            reuso_t += q["dur"]
        ant_arq = arqs[0] if arqs else None
        if q.get("arq2"):
            ant_arq = q["arq2"]

    # 5. checklist de componentes e material real
    REAL = {"KenBurns", "Filme", "DocGrifo", "EntaoAgora"}
    real_t = sum(q["dur"] for q in planos if q["tipo"] in REAL)
    docs = sorted({q["arq"] for q in planos if q["tipo"] == "DocGrifo"})
    docs_grifo = sorted({q["arq"] for q in planos if q["tipo"] == "DocGrifo" and q["grifo"]})
    n_ea = sum(1 for q in planos if q["tipo"] == "EntaoAgora")
    n_num = sum(1 for q in planos if q["tipo"] == "Número") + sum(1 for q in planos if q.get("num"))
    mapas = sorted({q["nome"] for q in planos if q["tipo"] == "Mapa2D"})
    cont = {}
    for q in planos:
        cont[q["tipo"]] = cont.get(q["tipo"], 0) + 1
    if len(docs_grifo) < 4:
        ERROS.append(f"só {len(docs_grifo)} documentos grifados (mínimo 4)")
    if n_ea < 1:
        ERROS.append("nenhum EntaoAgora")
    if n_num < 3:
        ERROS.append(f"só {n_num} Números (mínimo 3)")
    if len(mapas) < 2:
        ERROS.append(f"só {len(mapas)} Mapa2D (mínimo 2)")
    frac_real = real_t / total
    if frac_real < REAL_MIN:
        ERROS.append(f"material real {frac_real:.1%} < {REAL_MIN:.0%}")

    # 6. fidelidade (aviso): nomes citados × arquivo do plano
    NOMES = {"Saratoga": ["saratoga", "doe_1946.mp4"], "Nagato": ["nagato", "doe_1946"], "Independence": ["independence"],
             "Prinz Eugen": ["prinz"], "Arkansas": ["arkansas"], "Kili": ["kili"], "Wyatt": ["wyatt", "rongerik_1946"], "Juda": ["wyatt", "rongerik_1946"]}
    for q in planos:
        alvo = (q["arq"] + " " + q["enq"]).lower()
        for nome, oks in NOMES.items():
            if nome in q["frase"] and not any(o in alvo for o in oks):
                AVISOS.append(f"fidelidade? {q['bloco']} cita {nome} sobre {q['arq']} [{q['enq']}]: «{q['frase'][:60]}»")

    # ids e saída
    for i, q in enumerate(planos, 1):
        q["id"] = f"P{i:03d}"
        q["real"] = q["tipo"] in REAL
    stats = dict(planos=len(planos), duracao_s=round(total, 1), duracao=fmt(total), planos_por_min=round(len(planos) / (total / 60), 1),
                 real_pct=round(100 * frac_real, 1), reuso_pct=round(100 * reuso_t / total, 1),
                 componentes=cont, docs_distintos=len(docs), docs_grifados=len(docs_grifo), numeros=n_num,
                 mapas_distintos=len(mapas), entao_agora=n_ea, imagens_ia=len(CENAS), palavras=sum(palavras(b["texto"]) for b in B),
                 blocos_audio=len(B))

    blocos = [dict(id=b["id"], texto=b["texto"], texto_voz=voz(b["texto"]), ideia=b["ideia"],
                   inicio_est=b["inicio"], dur_est=b["dur"]) for b in B]
    chaves = ["id", "bloco", "tipo", "arq", "arq2", "enq", "inicio", "dur", "frase", "real", "reuso", "ficha", "num", "de", "para",
              "crop", "regiao", "frase_doc", "tin", "tout", "vel", "grifo", "literal", "valor", "rotulo", "nome", "pontos", "linhas", "selo", "nota",
              "linhas", "rot1", "rot2", "em"]
    sb = [{k: q[k] for k in chaves if k in q and q[k] is not None} for q in planos]
    (AQUI / "blocos.json").write_text(json.dumps(blocos, ensure_ascii=False, indent=1) + "\n")
    (AQUI / "storyboard.json").write_text(json.dumps(dict(stats=stats, pontos=P, planos=sb), ensure_ascii=False, indent=1) + "\n")
    (AQUI / "cenas.json").write_text(json.dumps(CENAS, ensure_ascii=False, indent=1) + "\n")

    L = ["# STORYBOARD: 002-bikini (lugares-guerra-en, \"Clearance Required\")", "",
         "Gerado por `roteiro.py` (não editar à mão). Tempos estimados a 150 ppm; recalcular com o áudio real no `build.py`.",
         f"**{stats['planos']} planos · {stats['duracao']} · {stats['planos_por_min']} planos/min · material real {stats['real_pct']}% · "
         f"reuso {stats['reuso_pct']}% · imagens IA {len(CENAS)}**", "",
         "Componentes: " + ", ".join(f"{k} {v}" for k, v in sorted(cont.items())) +
         f" · docs distintos {len(docs)} (grifados {len(docs_grifo)}) · Números {n_num} (tela cheia + sobrepostos) · mapas distintos {len(mapas)} · EntaoAgora {n_ea}", ""]
    for b in B:
        L.append(f"## {b['id']} [{fmt(b['inicio'])}]{' · IDEIA' if b['ideia'] else ''}")
        L.append(f"> {b['texto']}")
        L.append("")
        L.append("| # | t | s | tela | material / parâmetros | cobre |")
        L.append("|---|---|---|---|---|---|")
        for q in [q for q in planos if q["bloco"] == b["id"]]:
            L.append(f"| {q['id']} | {fmt(q['inicio'])} | {q['dur']:.1f} | {q['tipo']}{' ♻' if q['reuso'] else ''} | {descr(q)} | {q['frase'][:90]}{'…' if len(q['frase']) > 90 else ''} |")
        L.append("")
    L.append("♻ = reuso planejado (arquivo já mostrado antes; enquadramento diferente ou > 60 s depois).")
    (AQUI / "STORYBOARD.md").write_text("\n".join(L) + "\n")

    print(json.dumps(stats, ensure_ascii=False, indent=1))
    for a in AVISOS:
        print("AVISO:", a)
    if ERROS:
        for e in ERROS:
            print("ERRO:", e)
        print(f"\n{len(ERROS)} erro(s). Validação REPROVADA.")
        sys.exit(1)
    print("\nValidação OK.")



def descr(q):
    t = q["tipo"]
    f = q.get("ficha")
    fx = f" · Ficha: {f[0]} / {f[1]}" if f else ""
    nm = f" · Número «{q['num'][0]} {q['num'][1]}»" if q.get("num") else ""
    if t == "KenBurns":
        return f"`{q['arq']}` {q['enq']} {tuple(q['de'])}→{tuple(q['para'])}{' crop ' + str(q['crop']) if q.get('crop') else ''}{fx}{nm}"
    if t == "Filme":
        return f"`{q['arq']}` {q['tin']:.1f}–{q['tout']:.1f} s{' vel ' + str(q['vel']) if q['vel'] != 1 else ''} (sem áudio){fx}{nm}"
    if t == "DocGrifo":
        g = f"grifo «{q['frase_doc']}»" if q.get("frase_doc") else ("página/zoom" if not q["grifo"] else "grifo")
        return f"`{q['arq']}` [{q['enq']}] {g}{'' if q['literal'] else ' (não literal)'}{fx}{nm}"
    if t == "Número":
        return f"código: **{q['valor']}** {q['rotulo']}"
    if t == "Mapa2D":
        return f"código: mapa {q['nome']} ({', '.join(q['pontos'])}){' · Selo ' + q['selo'] if q.get('selo') else ''}{' · ' + q['nota'] if q.get('nota') else ''}"
    if t == "Cartela":
        return f"código: cartela «{' / '.join(q['linhas'])}»{' · Selo ' + q['selo'] if q.get('selo') else ''}"
    if t == "EntaoAgora":
        return f"`{q['arq']}` ({q['rot1']}) × `{q['arq2']}` ({q['rot2']}){nm}"
    if t == "Card":
        return "código: cartela final do canal (Clearance Required + inscrever)"
    return ""


if __name__ == "__main__":
    main()
