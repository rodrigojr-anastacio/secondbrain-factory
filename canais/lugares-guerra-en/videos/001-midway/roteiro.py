#!/usr/bin/env python3
"""Fonte do storyboard do piloto lugares-guerra-en 001 "Why Can't You Visit Midway Atoll?" (youtube.videos id 30).
Uso: cd <pasta do vídeo> && python3 roteiro.py   (python3 puro, sem dependências)

O roteiro FINAL é o SCRIPT.md (com checagem de fatos, CHECAGEM-FATOS.md). Este arquivo NÃO gera o SCRIPT.md: ele
divide a narração em blocos de áudio (um arquivo de voz por bloco) e define os planos visuais; a validação confere que a
narração daqui é idêntica à do SCRIPT.md, parágrafo a parágrafo (erro se divergir).
Gera: blocos.json, storyboard.json, STORYBOARD.md, cenas.json.

Bíblia do canal (prevalece): canais/lugares-guerra-en/biblia/visual.md (gramática de tela) e roteiro.md (checklist).
Matéria-prima: só midia/ (63 arquivos PD, ver midia.csv e licencas.md). Nenhuma imagem gerada por IA no corpo
(os cortes "SCHEMATIC" são desenhados em código: cenas.json vazio).

Sintaxe dos planos (cada plano começa no trecho `em` da narração do bloco e vai até o início do próximo plano):
  kb(em, arquivo, mov, ficha=None, crop=None, num=None)        KenBurns; mov = preset ou ((cx,cy,z),(cx,cy,z))
  filme(em, arquivo, tin, tout, oque, data=..., vel=1, num=None) trecho real do filme (s), sem o áudio original
  doc(em, arquivo, enq, grifo, frase=None, literal=True, num=None) DocGrifo: grifo = [(x,y,w,h)] em fração da imagem
  num(em, valor, rotulo)                                        Número em tela cheia (código)
  mapa(em, nome, pontos, linhas, selo=None, nota="")            Mapa2D (Natural Earth, código)
  cartela(em, linhas, selo="SCHEMATIC")                         cartela tipográfica (código)
  ea(em, antes, depois, rot1, rot2, num=None)                   EntaoAgora (cortina amarela)
  card(em)                                                      cartela final do canal
  num=... em kb/filme/doc/ea = Número sobreposto (conta como Número no checklist).
Duração estimada: 150 palavras/min (2,5 palavras/s), distribuída pelas palavras de cada trecho.
"""
import csv
import json
import os
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MIDIA = AQUI / "midia"
WPS = 2.5                 # 150 ppm (bíblia, roteiro.md); medir com a voz escolhida
RUN_MAX = 12.0            # s: o mesmo TIPO de tela no máximo 12 s seguidos
JANELA = 60.0             # s: mesmo arquivo + enquadramento só depois disso
INEDITO_ATE = 180.0       # s: sem reuso nos primeiros 3:00...
REUSO_LIBERADO = {"doc_cincpac_p1.jpg"}   # ...exceto o retorno planejado ao documento do hook
REAL_MIN = 0.85
DUR_FILME = {"filme_battle_of_midway.mp4": 1127.0, "filme_torpedo_squadron_8.mp4": 466.0}
# trechos dos filmes com cartela de texto/créditos (proibidos): títulos, cartelas pintadas, placas "In Memoriam"
FILME_PROIBIDO = {"filme_battle_of_midway.mp4": [(0, 70.4), (1054.0, 1127.0)],
                  "filme_torpedo_squadron_8.mp4": [(0, 72.0), (147.0, 165.0), (175.0, 438.0), (458.0, 466.0)]}

# ---------------------------------------------------------------- helpers
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
        if m.startswith("detalhe:"):            # detalhe:x,y  push-in no ponto
            x, y = (float(v) for v in m[8:].split(","))
            return m, ((x, y, 1.35), (x, y, 1.55))
        return m, MOV[m]
    return "custom", m


def kb(em, arq, mov="zoom-in", ficha=None, crop=None, num=None, enq=None):
    nome, (de, para) = _mov(mov)
    return dict(tipo="KenBurns", em=em, arq=arq, enq=enq or nome, de=de, para=para, ficha=ficha, crop=crop, num=num)


def filme(em, arq, tin, tout, oque, data="JUNE 4, 1942 · MIDWAY", vel=1.0, num=None):
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


CRED_FILME = {"filme_battle_of_midway.mp4": "The Battle of Midway (U.S. Navy, 1942) · National Archives",
              "filme_torpedo_squadron_8.mp4": "Torpedo Squadron 8 (U.S. Navy, 1942) · National Archives 428-MN-2004"}
BOM, VT8 = "filme_battle_of_midway.mp4", "filme_torpedo_squadron_8.mp4"
CINC = "doc_cincpac_p1.jpg"
EO = "doc_eo13022_p1.png"
GAO2 = "doc_gao16382_p2.png"

# Fichas (DATA · LUGAR / o que é / acervo, licença) das imagens reais.
FICHAS = {
    CINC: ("JUN 28 1942 · PEARL HARBOR", 'Nimitz (CINCPAC) to COMINCH: "Battle of Midway"', "National Archives, RG 38 · Unrestricted"),
    "doc_nhhc_discurso2017.png": ("JUN 5 2017 · WASHINGTON", "NHHC director, Battle of Midway 75th anniversary", "Naval History and Heritage Command · PD"),
    "doc_eo13022_p1.png": ("OCT 31 1996 · WASHINGTON", "Executive Order 13022, Administration of the Midway Islands", "Federal Register 61 FR 56875 · PD"),
    "doc_nhhc_h006-2_af.png": ("NHHC · H-GRAM 006", "The Navy's own history of the Midway codebreaking", "Naval History and Heritage Command · PD"),
    "doc_trackchart.jpg": ("JUNE 1942 · CINCPAC", "Track chart of the Battle of Midway (composite)", "National Archives, RG 38 · Unrestricted"),
    "doc_nhhc_ford_oral.png": ("NHHC · ORAL HISTORY", "John Ford remembers filming the Battle of Midway", "Naval History and Heritage Command · PD"),
    "doc_doi2014_topo.png": ("NOV 20 2014 · U.S. HOUSE", "USFWS testimony on Midway Atoll NWR", "U.S. Department of the Interior · PD"),
    "doc_doi2014_chumbo.png": ("NOV 20 2014 · U.S. HOUSE", "USFWS testimony: lead paint and albatross chicks", "U.S. Department of the Interior · PD"),
    "doc_doi2014_35mil_jatos.png": ("NOV 20 2014 · U.S. HOUSE", "USFWS testimony: Henderson Field", "U.S. Department of the Interior · PD"),
    "doc_doi2014_suspensao.png": ("NOV 20 2014 · U.S. HOUSE", "USFWS testimony: visitor services suspended", "U.S. Department of the Interior · PD"),
    "doc_gao16382_p1.png": ("JUN 2 2016 · GAO-16-382", "Report: Midway Atoll, historic properties and visitation", "U.S. Government Accountability Office · PD"),
    GAO2: ("JUN 2 2016 · GAO-16-382", "Highlights: budget cuts, visitation, historic buildings", "U.S. Government Accountability Office · PD"),
    "doc_pmnm_acesso.png": ("TODAY · PAPAHĀNAUMOKUĀKEA", "Monument access page (NOAA / USFWS)", "papahanaumokuakea.gov · PD"),
    "doc_usfws2022_hangar.png": ("JAN 18 2022 · USFWS", "Winter storms impact Midway: the seaplane hangar", "U.S. Fish and Wildlife Service · PD"),
    "doc_usfws_msp_camundongos.png": ("AUG 15 2023 · USFWS", "Midway Seabird Protection Project, Update #5", "U.S. Fish and Wildlife Service · PD"),
    "foto_iss2001.jpg": ("2001 · MIDWAY ATOLL", "Seen from the International Space Station", "NASA ISS002-E-8828 · PD"),
    "foto_henderson_f18_2015.jpg": ("JUL 14 2015 · HENDERSON FIELD", "Marine F-18s after an emergency landing", "USFWS / D. Dow · PD"),
    "foto_wisdom2023_a.jpg": ("DEC 3 2023 · SAND ISLAND", "Wisdom, Laysan albatross (banded 1956)", "USFWS · PD"),
    "foto_wisdom2023_b.jpg": ("DEC 3 2023 · SAND ISLAND", "Wisdom, Laysan albatross (banded 1956)", "USFWS · PD"),
    "foto_comemoracao2022.jpg": ("JUN 2022 · MIDWAY ATOLL", "80th commemoration of the Battle of Midway", "USFWS · PD"),
    "foto_casamata_s6_2015.jpg": ("APR 15 2015 · SAND ISLAND", "WWII concrete pillbox S-6", "U.S. GAO (GAO-16-382) · PD"),
    "foto_eastern_memorial2015.jpg": ("APR 16 2015 · EASTERN ISLAND", "Original Henderson Field memorial, now an albatross colony", "U.S. GAO (GAO-16-382) · PD"),
    "foto_posto_comando2015.jpg": ("APR 14 2015 · SAND ISLAND", "1942 command post, crumbling", "U.S. GAO (GAO-16-382) · PD"),
    "foto_rochefort1934.jpg": ("SEP 15 1934", "Lt. Joseph J. Rochefort, USN", "Naval History and Heritage Command NH 64844 · PD"),
    "foto_kaga1936.jpg": ("c. 1936 · JAPAN", "Aircraft carrier Kaga", "Naval History and Heritage Command NH 73060 · PD"),
    "foto_nimitz_midway1942.jpg": ("c. JUNE 1942 · MIDWAY", "Adm. Chester W. Nimitz (CINCPAC) at a bunker on Midway", "Naval History and Heritage Command NH 62674 · PD"),
    "foto_cannon.jpg": ("1ST LT. GEORGE H. CANNON, USMC", "Killed on Sand Island, Dec 7 1941 · Medal of Honor", "U.S. Marine Corps History Division · PD"),
    "foto_akagi1941.jpg": ("1941 · JAPAN", "Aircraft carrier Akagi", "Naval History and Heritage Command NH 73059 · PD"),
    "foto_cabo1935.jpg": ("MAY 1935 · SAND ISLAND", "The Commercial Pacific Cable station from the air", "U.S. Navy, NHHC NH 96598 · PD"),
    "foto_clipper1936.jpg": ("c. 1936 · SAN FRANCISCO", "Pan Am China Clipper (route via Honolulu, Midway, Wake)", "Clyde H. Sunderland, Library of Congress · PD"),
    "foto_aerea1941.jpg": ("NOV 24 1941 · MIDWAY ATOLL", "Aerial view, two weeks before the war", "U.S. Navy 80-G-451086, National Archives · PD"),
    "foto_canhao_historico.jpg": ("MIDWAY ATOLL", "WWII-era gun among the albatrosses", "USFWS / National Archives 022-DP-06622 · PD"),
    "foto_yamamoto.jpg": ("EARLY 1940s", "Adm. Isoroku Yamamoto, Combined Fleet", "Naval History and Heritage Command NH 63430 · PD"),
    "foto_b17_decolagem1942.jpg": ("MAY 31 1942 · MIDWAY", "Army B-17s take off from Midway", "U.S. Army Air Forces USAF-22635-AC · PD"),
    "foto_hangar1942.jpg": ("JUN 4 1942 · SAND ISLAND", "The seaplane hangar after the raid", "U.S. Navy 80-G-17081, National Archives · PD"),
    "foto_soryu_b17_1942.jpg": ("JUN 4 1942 · NORTHWEST OF MIDWAY", "Carrier Soryu circling under B-17 attack", "U.S. Army Air Forces USAF-ID-4845 · PD"),
    "foto_george_gay1942.jpg": ("JUNE 1942 · PEARL HARBOR", "Ens. George Gay, VT-8, in the hospital", "National Archives 80-G-17678 · Unrestricted"),
    "foto_george_gay1942_rot.jpg": ("JUNE 1942 · PEARL HARBOR", "Ens. George Gay, VT-8, in the hospital", "National Archives 80-G-17678 · Unrestricted"),
    "foto_hiryu_b17_1942.jpg": ("JUN 4 1942 · NORTHWEST OF MIDWAY", "Carrier Hiryu maneuvering under B-17 attack", "U.S. Army Air Forces USAF 75712 AC · PD"),
    "foto_b17_ataque1942.jpg": ("JUN 4 1942 · NORTHWEST OF MIDWAY", "Japanese carrier evading B-17 bombs", "U.S. Army Air Forces 342-FH, National Archives · PD"),
    "foto_yorktown_torpedo1942.jpg": ("JUN 4 1942 · AT SEA", "USS Yorktown (CV-5) hit by a torpedo", "U.S. Navy, National Archives · PD"),
    "foto_hiryu_chamas1942.jpg": ("JUN 5 1942 · AT SEA", "Hiryu adrift and burning", "Naval History and Heritage Command NH 73064 · PD"),
    "foto_yorktown_bomba1942.jpg": ("JUN 4 1942 · AT SEA", "USS Yorktown under attack by Hiryu's planes", "U.S. Navy 80-G-414423, National Archives · PD"),
    "foto_mikuma1942.jpg": ("JUN 6 1942 · AT SEA", "Heavy cruiser Mikuma, sinking", "U.S. Navy 80-G-414422, National Archives · PD"),
    "foto_prisioneiros_hiryu1942.jpg": ("JUNE 1942 · MIDWAY", "Hiryu survivors picked up by the U.S. Navy", "U.S. Navy 80-G-79984-28, National Archives · PD"),
    "foto_midway1945.jpg": ("APRIL 1945 · MIDWAY ATOLL", "Naval Air Station Midway", "U.S. Navy, National Archives (RG 313) · PD"),
    "foto_guerrafria1959.jpg": ("1959 · SAND ISLAND", "NAS Midway, base of the Pacific Barrier patrols", "U.S. Navy, All Hands (Aug 1959) · PD"),
    "foto_oficina_albatrozes2015.jpg": ("APR 13 2015 · SAND ISLAND", "Old Navy machine shop and nesting albatrosses", "U.S. GAO (GAO-16-382) · PD"),
    "foto_carpintaria_albatrozes2015.jpg": ("APR 13 2015 · SAND ISLAND", "Old Navy carpentry shop and albatrosses", "U.S. GAO (GAO-16-382) · PD"),
    "foto_albatroz_ninho.jpg": ("APR 2 2026 · MIDWAY ATOLL", "Laysan albatross colony", "USFWS / Dan Rapp · PD"),
    "foto_albatroz_moli.jpg": ("MIDWAY ATOLL NWR", "Laysan albatross (mōlī)", "USFWS · PD"),
    "foto_bateria_a_2015.jpg": ("APR 15 2015 · SAND ISLAND", "Battery A, 5-inch gun position", "U.S. GAO (GAO-16-382) · PD"),
    "foto_estacao_cabo_descascando2015.jpg": ("APR 2015 · SAND ISLAND", "Cable station: cracking, peeling paint", "U.S. GAO (GAO-16-382) · PD"),
    "foto_estacao_cabo2015.jpg": ("APR 2015 · SAND ISLAND", "Cable station building (1903) and the colony", "U.S. GAO (GAO-16-382) · PD"),
    "foto_hangar2015.jpg": ("APR 13 2015 · SAND ISLAND", "The seaplane hangar, half rebuilt, rusting", "U.S. GAO (GAO-16-382) · PD"),
    "foto_hangar2022.jpg": ("JAN 13 2022 · SAND ISLAND", "The seaplane hangar after its collapse", "USFWS · PD"),
    "foto_tsunami_eastern2011.jpg": ("MAR 13 2011 · EASTERN ISLAND", "Debris line left by the tsunami", "USFWS / Pete Leary · PD"),
    "foto_tsunami_lagoa2011.jpg": ("MAR 12 2011 · MIDWAY LAGOON", "Tsunami debris and birds in the lagoon", "USFWS / Pete Leary · PD"),
    "foto_robbins.jpg": ("USGS · PATUXENT", "Chandler Robbins, who banded Wisdom in 1956", "Barbara Dowell, USGS · PD"),
    "foto_lixo_marinho2017.jpg": ("2017 · MIDWAY ATOLL", "Marine debris removed from the atoll", "USFWS · PD"),
}

# Retângulos do grifo (x, y, w, h em fração da imagem). CINCPAC e EO medidos na página (grade de 5%); o resto vem do
# bbox em px do midia.csv (normalizado pela resolução).
def px(b, W, H):
    return (round(b[0] / W, 4), round(b[1] / H, 4), round(b[2] / W, 4), round(b[3] / H, 4))


G = {
    "cinc_secret": [(0.095, 0.184, 0.31, 0.053), (0.68, 0.169, 0.153, 0.028)],
    "cinc_a": [(0.282, 0.709, 0.60, 0.018), (0.327, 0.725, 0.557, 0.018), (0.327, 0.741, 0.09, 0.018)],
    "cinc_c": [(0.282, 0.775, 0.35, 0.018)],
    "cinc_g": [(0.282, 0.853, 0.60, 0.018)],
    "cinc_92": [(0.097, 0.915, 0.752, 0.018)],
    "cinc_subject": [(0.095, 0.275, 0.39, 0.019)],
    "eo_titulo": [(0.338, 0.152, 0.34, 0.018)],
    "eo_199a": [(0.452, 0.362, 0.355, 0.016)],   # só "Executive Order 199-A of January 20, 1903" (still do Remotion, 12/11)
    "eo_sec3a": [(0.50, 0.534, 0.427, 0.015), (0.338, 0.548, 0.245, 0.015)],
    "eo_1": [(0.38, 0.580, 0.546, 0.015)],
    "eo_5": [(0.817, 0.708, 0.11, 0.015), (0.338, 0.722, 0.48, 0.015)],
    "discurso": [px([1572, 1322, 1250, 80], 3840, 2880)],
    "ford": [px([2637, 1076, 240, 36], 3840, 2880), px([1572, 1120, 1158, 36], 3840, 2880)],   # "A Zero flew about 50 / feet over it and dropped a bomb and hit it, the whole thing went up. I was knocked unconscious."
    "h006_twist": [px([1572, 1034, 890, 36], 3840, 2880)],  # "...to get / Washington to believe that "AF" stood for Midway, not to convince Nimitz."
    "h006": [px([1732, 1120, 740, 36], 3840, 2880)],
    "chumbo": [px([2990, 1120, 62, 36], 3840, 2880), px([1484, 1158, 1556, 36], 3840, 2880), px([1484, 1196, 112, 36], 3840, 2880)],  # só a frase lida (12/11)
    "jatos": [px([1614, 1120, 590, 32], 3840, 2880)],
    "suspdoi": [px([2254, 1120, 734, 34], 3840, 2880)],
    "pmnm": [px([1522, 582, 480, 32], 3840, 2568)],
    "hangar22": [px([1800, 1120, 638, 44], 3840, 2880)],
    "camund": [px([2242, 1120, 530, 44], 3840, 2880)],
    "gao_susp": [px([1200, 1111, 551, 55], 2550, 3300)],
    "gao_reparo": [px([1082, 2599, 606, 55], 2550, 3300)],
    "gao_demol": [px([1779, 1807, 491, 55], 2550, 3300), px([899, 1855, 185, 55], 2550, 3300)],
    "pagina": [],
}

# Pontos de mapa (lon E 0–360, lat). Midway 28.21N 177.37W.
P = {"MIDWAY": (182.63, 28.21), "HONOLULU": (202.14, 21.31), "PEARL HARBOR": (202.03, 21.35), "TOKYO": (139.69, 35.68),
     "SAN FRANCISCO": (237.58, 37.77), "WAKE": (166.65, 19.28), "GUAM": (144.79, 13.44), "MANILA": (120.98, 14.60),
     "POINT LUCK": (187.0, 32.0), "JAPANESE CARRIERS": (180.71, 30.6), "ADAK": (183.35, 51.88),
     "YORKTOWN (WRECK)": (183.4, 30.6), "KAGA (WRECK)": (180.7, 30.3), "AKAGI (WRECK)": (181.2, 30.5)}

# ---------------------------------------------------------------- narração (blocos de áudio) + planos
B = []


def bloco(bid, texto, *planos, ideia=False):
    B.append(dict(id=bid, texto=texto, ideia=ideia, planos=list(planos)))


# ===== Bloco 1: hook =====
bloco("B01a", '''This page was typed in June 1942, and somebody stamped it SECRET. It's Admiral Chester Nimitz's report to Washington on a battle three weeks old.''',
      doc("This page was typed", CINC, "secret", G["cinc_secret"], frase="SECRET"),
      filme("It's Admiral Chester", BOM, 462.2, 468.0, "The flag over Midway during the Japanese raid"),
      ideia=True)
bloco("B01b", '''Read line (a). "4 CV sunk – Akagi, Kaga, Soryu, Hiryu – with the loss of all their planes and many of their personnel." Four Japanese aircraft carriers, gone.''',
      doc("Read line (a).", CINC, "a", G["cinc_a"], frase="with the loss of all their planes and many of their personnel"),
      kb("Four Japanese aircraft", "foto_hiryu_chamas1942.jpg", "detalhe:0.55,0.55", num=("4", "CARRIERS SUNK")))
bloco("B01c", '''Now do the math at the bottom. "Ninety-two officers and two hundred and fifteen men." The American cost. Three hundred and seven. Remember that number.''',
      doc("Now do the math", CINC, "92", G["cinc_92"], frase="Ninety-two officers and two hundred and fifteen men"),
      num("Three hundred and seven.", "92 + 215 = 307", "AMERICAN DEAD (OFFICIAL COUNT)"))
bloco("B01d", '''The subject line reads: Battle of Midway. That place is still out there, in the middle of the Pacific. And you're not allowed to go.''',
      doc("The subject line", CINC, "subject", G["cinc_subject"], frase="Battle of Midway"),
      filme("That place is still", BOM, 89.6, 96.6, "Midway's islands from the sea", vel=0.95))

# ===== Bloco 2: o lugar =====
bloco("B02a", '''Midway Atoll is a ring of coral more than twelve hundred miles northwest of Honolulu. About forty people live there. Nobody else gets to land.''',
      mapa("Midway Atoll is", "havai_midway", ["HONOLULU", "MIDWAY"], [("HONOLULU", "MIDWAY", "1,200+ MI")], nota="Número sobreposto «~40 PEOPLE LIVE THERE»"),
      ideia=True)
bloco("B02b", '''And two things there are very strange. A runway that's still kept ready, in case a jet full of passengers gets into trouble over the Pacific.''',
      kb("And two things", "foto_iss2001.jpg", "zoom-in"),
      kb("A runway that's", "foto_henderson_f18_2015.jpg", "pan-dir"))
bloco("B02c", '''And a bird that was already nesting here in 1956, when a scientist put a band on her leg. She's still coming back. Keep that year in mind.''',
      filme("And a bird", BOM, 161.2, 164.6, "Laysan albatross on Midway, filmed by Ford", data="1942 · MIDWAY", vel=0.85, num=("1956", "BANDED")),
      kb("when a scientist", "foto_wisdom2023_a.jpg", "detalhe:0.62,0.42"))

# ===== Bloco 2: âncora humana + pergunta do título =====
bloco("B03a", '''In 2017, two old Marines laid a wreath on Midway. One was John Miniclier. On June 4th, 1942, he was a young private on Sand Island, on top of a thirty-foot searchlight tower, counting Japanese planes.''',
      doc("In 2017, two old", "doc_nhhc_discurso2017.png", "wreath", G["discurso"], frase="lay a wreath", literal=False),
      filme("On June 4th, 1942,", BOM, 1036.0, 1041.6, "A lookout scans the sky", vel=0.74),
      filme("counting Japanese planes.", BOM, 494.1, 495.6, "Flak bursts over the atoll"),
      ideia=True)
bloco("B03b", '''In 2025, he died at a hundred and three, the last known survivor of the Battle of Midway.''',
      kb("In 2025, he died", "foto_comemoracao2022.jpg", "zoom-out", num=("103", "LAST KNOWN SURVIVOR")))
bloco("B03c", '''So why? Why can't you visit Midway Atoll, the place where the war in the Pacific turned?''',
      filme("So why?", BOM, 1046.6, 1053.4, "The flag above the burning base"),
      ideia=True)
bloco("B03d", '''It isn't a military secret. The Navy left decades ago. It isn't forgotten. It's a national memorial.''',
      kb("It isn't a military", "foto_casamata_s6_2015.jpg", "pan-esq"),
      kb("It isn't forgotten.", "foto_eastern_memorial2015.jpg", "zoom-in"))
bloco("B03e", '''And it isn't that nobody wants to go. For years, people flew in to see it. What keeps you out is a chain of decisions, a few million birds, and an island that's slowly falling apart.''',
      doc("And it isn't that", "doc_doi2014_topo.png", "topo", G["pagina"], literal=False),
      doc("What keeps you out", "doc_gao16382_p1.png", "capa", G["pagina"], literal=False),
      kb("and an island that's", "foto_posto_comando2015.jpg", "zoom-in"))
bloco("B03f", '''Along the way, you'll hear about a fake message about drinking water that told America where Japan would strike, a Hollywood director knocked out on a rooftop, and what a robot found three miles down.''',
      kb("Along the way,", "foto_rochefort1934.jpg", ((0.5, 0.33, 1.25), (0.5, 0.30, 1.45))),
      filme("a Hollywood director", BOM, 521.9, 525.3, "Oil tanks burning after the raid"),
      kb("and what a robot", "foto_kaga1936.jpg", "pan-dir"))

# ===== Bloco 3: o que aconteceu ali =====
bloco("B04a", '''To understand why anybody would fight over two specks of sand, start with a wire. In 1903, a cable company built a station on Sand Island. It was the final link in a telegraph line across the Pacific, and President Theodore Roosevelt used it to send a message.''',
      filme("To understand why", BOM, 81.8, 86.1, "Midway's islands from a patrol plane", data="JUNE 1942 · MIDWAY"),
      kb("start with a wire.", "foto_cabo1935.jpg", "zoom-in"),
      kb("It was the final link", "foto_estacao_cabo2015.jpg", "pan-dir"),
      doc("and President Theodore", EO, "pagina", G["pagina"], literal=False),
      ideia=True)
bloco("B04b", '''That same year, a presidential order put the atoll under the United States Navy.''',
      doc("That same year", EO, "199a", G["eo_199a"], frase="Executive Order 199-A", literal=False))
bloco("B04c", '''In 1935, Pan American Airways arrived. Its big flying boats, the Clippers, landed in Midway's lagoon on weekly flights across the Pacific, and Pan Am built a small hotel on the sand.''',
      kb("In 1935, Pan American", "foto_clipper1936.jpg", "pan-esq", crop=(0.05, 0.0, 0.95, 1.0)),  # sem a borda do scan à esquerda
      mapa("landed in Midway's", "clipper", ["SAN FRANCISCO", "HONOLULU", "MIDWAY", "WAKE", "GUAM", "MANILA"],
           [("SAN FRANCISCO", "HONOLULU", ""), ("HONOLULU", "MIDWAY", ""), ("MIDWAY", "WAKE", ""), ("WAKE", "GUAM", ""), ("GUAM", "MANILA", "PAN AM CLIPPER · 1935")],
           nota="exige base regenerada até 238°E (São Francisco)"),
      filme("built a small hotel", BOM, 97.0, 99.0, "Sand Island's dock and seaplane ramp", data="JUNE 1942 · SAND ISLAND", vel=0.56))
bloco("B04d", '''Then the Navy started building for real: dredging the lagoon, a seaplane base on Sand Island, runways on Eastern Island. This photo was taken on November 24th, 1941. Look how finished it is.''',
      filme("Then the Navy started", BOM, 101.2, 104.9, "Sand Island's dock and lagoon", data="JUNE 1942 · SAND ISLAND", vel=0.92),
      filme("a seaplane base", BOM, 105.0, 108.9, "PBY Catalinas at the Sand Island seaplane base", data="JUNE 1942 · SAND ISLAND", vel=0.92),
      kb("This photo was taken", "foto_aerea1941.jpg", "zoom-out"))
bloco("B04e", '''Two weeks later, on the same day as Pearl Harbor, Japanese warships shelled Midway too. A Marine officer killed in that attack, George Cannon, became the first Marine to earn the Medal of Honor in World War Two.''',
      filme("Two weeks later", BOM, 124.0, 129.5, "Marines of the Midway garrison", data="1942 · MIDWAY", vel=0.88, num=("DEC 7, 1941", "MIDWAY SHELLED")),
      kb("A Marine officer killed", "foto_cannon.jpg", ((0.5, 0.36, 1.04), (0.5, 0.30, 1.22))),
      filme("became the first Marine", BOM, 129.6, 133.3, "Marines of the Midway garrison", data="1942 · MIDWAY", vel=0.64,
            num=("MEDAL OF HONOR", "1ST LT. GEORGE H. CANNON · DEC 7 1941")),
      ideia=True)
bloco("B05a", '''By the spring of 1942, Japan had been winning for six months. Admiral Isoroku Yamamoto wanted to lure the American carriers into one big fight and finish them. The bait would be Midway.''',
      kb("By the spring", "foto_akagi1941.jpg", "pan-dir"),
      kb("Admiral Isoroku", "foto_yamamoto.jpg", ((0.5, 0.35, 1.2), (0.5, 0.32, 1.4))),
      mapa("The bait would be", "isca", ["TOKYO", "MIDWAY", "PEARL HARBOR"], [("TOKYO", "MIDWAY", "THE BAIT")]),
      ideia=True)
bloco("B05b", '''But at Pearl Harbor, a Navy codebreaking unit called Station Hypo was reading parts of the Japanese navy's code. The intercepts kept pointing to a target called "AF." The unit's commander, Joseph Rochefort, was sure AF was Midway. Washington wasn't convinced.''',
      mapa("But at Pearl Harbor", "isca_hypo", ["TOKYO", "MIDWAY", "PEARL HARBOR"], [("PEARL HARBOR", "PEARL HARBOR", "STATION HYPO")]),
      doc("The intercepts kept", "doc_nhhc_h006-2_af.png", "af", G["pagina"], literal=False),
      kb("The unit's commander", "foto_rochefort1934.jpg", ((0.5, 0.30, 1.6), (0.5, 0.36, 1.3))))
bloco("B05c", '''So one of his staff, Jasper Holmes, came up with a trick. The instructions went to Midway over the undersea cable, where Japan couldn't listen. Then Midway sent a fake radio message, in the clear: its fresh-water plant had broken down.''',
      doc("So one of his staff", "doc_nhhc_h006-2_af.png", "holmes", G["pagina"], literal=False),
      cartela("The instructions went", ["PEARL → MIDWAY  (UNDERSEA CABLE)", "SEND IN THE CLEAR: FRESH-WATER PLANT BROKEN"], selo="SCHEMATIC"),
      doc("Then Midway sent", "doc_nhhc_h006-2_af.png", "agua", G["h006"], frase="a phony radio message in the clear", literal=False))
bloco("B05d", '''Japanese listeners took the bait and passed the news along. Hypo decoded that, too. AF was short of water.''',
      kb("Japanese listeners", "foto_rochefort1934.jpg", "detalhe:0.5,0.28", num=("AF = MIDWAY", "SHORT OF WATER")))
bloco("B05e", '''The Navy's own historians add a twist. The trick wasn't really meant to convince Nimitz. It was meant to convince Washington.''',
      doc("The Navy's own", "doc_nhhc_h006-2_af.png", "twist", G["h006_twist"], frase="not to convince Nimitz", literal=False),
      ideia=True)
bloco("B06a", '''Nimitz already believed it. His intelligence officer, Edwin Layton, even predicted where the Japanese carriers would first be spotted: bearing 325 degrees, 175 nautical miles from Midway, at six in the morning on June 4th.''',
      kb("Nimitz already", "foto_nimitz_midway1942.jpg", ((0.5, 0.68, 1.0), (0.49, 0.64, 1.3))),
      mapa("bearing 325 degrees", "teatro", ["MIDWAY", "JAPANESE CARRIERS"], [("MIDWAY", "JAPANESE CARRIERS", "325° · 175 NM · 06:00")]),
      ideia=True)
bloco("B06b", '''Nimitz later said Layton was off by only "five degrees, five miles, and five minutes." The Navy's historians say it was a little more than that, but not by much.''',
      doc("Nimitz later said", "doc_trackchart.jpg", "detalhe", G["pagina"], literal=False, num=("5° · 5 MI · 5 MIN", "LAYTON'S MISS, PER NIMITZ")))
bloco("B06c", '''So three American carriers were waiting northeast of the island. Yorktown, Enterprise and Hornet.''',
      filme("So three American", BOM, 586.1, 588.9, "A U.S. carrier group at sea", data="JUNE 1942 · AT SEA"),
      filme("northeast of the island", BOM, 589.1, 593.6, "A U.S. carrier during the battle", data="JUNE 1942 · AT SEA"))
bloco("B06d", '''On the morning of June 4th, 108 Japanese planes came for Midway. The Marines were ready. Every plane on the atoll that could fly was already in the air. The fighting over the islands themselves lasted about half an hour.''',
      filme("On the morning", BOM, 385.1, 389.2, "Japanese planes over the runway", vel=0.85, num=("108", "JAPANESE PLANES")),
      filme("The Marines were ready.", BOM, 382.1, 384.9, "Marine gun crew in a sandbagged pit"),
      kb("Every plane on the atoll", "foto_b17_decolagem1942.jpg", "pan-dir"),
      filme("The fighting over", BOM, 433.1, 438.0, "Bombs fall on the islands", num=("~30", "MINUTES")),
      ideia=True)
bloco("B07a", '''One of the men watching from a rooftop was a Hollywood director. John Ford was now a Navy commander with a movie camera. He'd been posted on top of the power house on Sand Island, with phones wired to the command post.''',
      doc("One of the men", "doc_nhhc_ford_oral.png", "titulo", G["pagina"], literal=False),
      filme("He'd been posted", BOM, 457.8, 462.0, "Men on a rooftop during the raid", vel=0.87),
      kb("with phones wired", "foto_posto_comando2015.jpg", "pan-esq"),
      ideia=True)
bloco("B07b", '''He had his camera lined up on a hangar, guessing it would be one of the first things hit. He was right. In his own words: "A Zero flew about 50 feet over it and dropped a bomb and hit it, the whole thing went up. I was knocked unconscious."''',
      filme("He had his camera", BOM, 440.3, 445.2, "A hangar burning during the raid", vel=0.64),
      filme("He was right.", BOM, 450.2, 453.5, "A bomb hits near the camera"),
      doc("A Zero flew", "doc_nhhc_ford_oral.png", "grifo", G["ford"], frase="dropped a bomb and hit it"))
bloco("B07c", '''He came to, and he got the shot. It's in the film he made that year, *The Battle of Midway*. This is the seaplane hangar on Sand Island after the raid. Remember that hangar.''',
      filme("He came to,", BOM, 486.6, 489.5, "Fire beside the water towers", vel=0.9),
      filme("It's in the film", BOM, 489.7, 493.9, "Marines in a gun pit, from Ford's film", vel=0.87),
      kb("This is the seaplane", "foto_hangar1942.jpg", "zoom-in"))
bloco("B07d", '''Across the island, John Miniclier was still up on his searchlight tower, counting. He remembered about thirty-eight of them, coming in on a line, straight toward him.''',
      filme("Across the island", BOM, 366.8, 368.7, "A lookout with binoculars"),
      filme("John Miniclier was still", BOM, 1036.0, 1041.6, "A lookout scans the sky"),
      filme("He remembered about", BOM, 373.4, 377.6, "Flak bursts around the formation", vel=0.75, num=("~38", "PLANES, ON A LINE")))
bloco("B08a", '''Out at sea, the American counterattack was going badly. Wave after wave of torpedo planes found the Japanese carriers, and wave after wave was shot down.''',
      mapa("Out at sea", "ataques", ["MIDWAY", "JAPANESE CARRIERS", "POINT LUCK"],
           [("POINT LUCK", "JAPANESE CARRIERS", "TORPEDO SQUADRONS"), ("MIDWAY", "JAPANESE CARRIERS", "")]),
      filme("Wave after wave", VT8, 123.5, 130.4, "TBD Devastators launch from USS Hornet", data="JUNE 4 1942 · USS HORNET"),
      ideia=True)
bloco("B08b", '''From the three American carriers, forty-one torpedo bombers went in. Six came back. Torpedo Squadron Eight, from the Hornet, lost all fifteen of its planes.''',
      num("From the three", "41 → 6", "TORPEDO BOMBERS WENT IN · CAME BACK"),
      filme("Torpedo Squadron Eight", VT8, 87.0, 96.7, "Torpedo Squadron 8 on USS Hornet", data="JUNE 1942 · USS HORNET", num=("15 / 15", "PLANES LOST")))
bloco("B08c", '''Its skipper, John Waldron, had told his men that if only one plane was left, he wanted that man to go in and get a hit.''',
      filme("Its skipper", VT8, 165.1, 174.8, "Lt. Cdr. John Waldron (left), VT-8 skipper", data="1942 · USS HORNET"),
      kb("that if only one", "foto_soryu_b17_1942.jpg", ((0.5, 0.5, 1.0), (0.24, 0.72, 1.5))))
bloco("B08d", '''The last plane was flown by Ensign George Gay. He dropped his torpedo at the carrier Soryu. It missed, and he was shot down. Gay was the only man in that attack to survive. This is him a few days later, recovering in a hospital bed.''',
      filme("The last plane", VT8, 141.0, 146.8, "A VT-8 TBD Devastator takes off", data="1942 · USS HORNET"),
      kb("He dropped his torpedo", "foto_soryu_b17_1942.jpg", ((0.2, 0.68, 1.9), (0.2, 0.68, 2.2)), enq="navio"),
      filme("It missed, and", VT8, 440.4, 445.5, "The open sea where VT-8 attacked", data="JUNE 1942 · AT SEA"),
      kb("Gay was the only", "foto_george_gay1942_rot.jpg", ((0.55, 0.66, 1.0), (0.62, 0.45, 1.1))))  # foto montada de lado na ficha do NARA: recortada e girada (12/11)
bloco("B09a", '''But those sacrifices kept the Japanese carriers busy. Their crews were launching fighters, landing them, and swerving to dodge torpedoes. Nobody had time to get a counterstrike into the air.''',
      filme("But those sacrifices", VT8, 446.0, 451.8, "The open sea northwest of Midway", data="JUNE 1942 · AT SEA"),
      kb("Their crews were", "foto_hiryu_b17_1942.jpg", "tilt-baixo"),
      kb("Nobody had time", "foto_b17_ataque1942.jpg", ((0.5, 0.5, 1.0), (0.17, 0.8, 1.6)), crop=(0.13, 0.0, 0.87, 1.0)),
      ideia=True)
bloco("B09b", '''Then, at 10:20 that morning, forty-eight American dive bombers showed up overhead. Two squadrons from Enterprise and one from Yorktown arrived at almost the same moment, by pure coincidence.''',
      filme("Then, at 10:20", BOM, 589.0, 593.9, "A U.S. carrier seen from the air", data="JUNE 1942 · AT SEA", vel=0.9, num=("10:20", "48 DIVE BOMBERS")),
      filme("Two squadrons from", BOM, 598.3, 604.6, "U.S. Navy SBD dive bombers", data="JUNE 1942 · AT SEA", vel=0.92))
bloco("B09c", '''In about five minutes, Akagi, Kaga and Soryu were wrecks on fire.''',
      num("In about five", "5 MIN", "AKAGI · KAGA · SORYU"))
bloco("B09d", '''The fourth carrier, Hiryu, hit back. Her planes found the Yorktown and left her badly damaged and listing. That afternoon, American dive bombers caught Hiryu too.''',
      kb("The fourth carrier", "foto_hiryu_b17_1942.jpg", "detalhe:0.5,0.55"),
      kb("Her planes found", "foto_yorktown_torpedo1942.jpg", ((0.5, 0.6, 1.04), (0.3, 0.8, 1.35)), enq="push-navio"),
      filme("That afternoon", BOM, 710.8, 713.0, "Dive bombers heading out", data="JUNE 1942 · AT SEA", vel=0.7))
bloco("B09e", '''By the next morning, all four Japanese carriers had been sunk by their own side's torpedoes, so the Americans couldn't capture them.''',
      kb("By the next morning", "foto_hiryu_chamas1942.jpg", "pan-esq"))
bloco("B10a", '''The Yorktown almost made it. Her crew kept her afloat for two days, under tow toward Pearl Harbor.''',
      doc("The Yorktown almost", "doc_trackchart.jpg", "yorktown", G["pagina"], literal=False),
      ideia=True)
bloco("B10b", '''Then, on June 6th, the Japanese submarine I-168 put torpedoes into the Yorktown and the destroyer Hammann beside her. Hammann sank almost at once. Yorktown went down the next morning.''',
      kb("Then, on June 6th", "foto_yorktown_bomba1942.jpg", ((0.5, 0.55, 1.04), (0.45, 0.8, 1.4)), crop=(0.0, 0.0, 1.0, 0.9)),
      num("Hammann sank", "JUNE 7, 1942", "YORKTOWN SINKS"))
bloco("B10c", '''Japan also lost the heavy cruiser Mikuma. Her sister ship, Mogami, was badly damaged, but she got away.''',
      kb("Japan also lost", "foto_mikuma1942.jpg", "pan-dir"))
bloco("B10d", '''Now go back to Nimitz's page. Line (c). "2 CA sunk – Mogami, Mikuma." One of those two cruisers didn't sink. Hold on to that.''',
      doc("Now go back", CINC, "c", G["cinc_c"], frase="2 CA sunk – Mogami, Mikuma"),
      kb("Hold on to that.", "foto_mikuma1942.jpg", "detalhe:0.35,0.55"),
      ideia=True)
bloco("B10e", '''The page also estimates that Japan lost 4,800 men. Navy historians today say more than 3,000, including over 700 of the mechanics who kept their planes flying.''',
      doc("The page also", CINC, "g", G["cinc_g"], frase="4,800", literal=False, num=("4,800", "JAPANESE LOSSES · NIMITZ'S ESTIMATE")),
      kb("Navy historians today", "foto_prisioneiros_hiryu1942.jpg", "zoom-out", num=("3,000+", "JAPANESE DEAD · TODAY'S COUNT")))
bloco("B10f", '''All 248 of the carriers' planes were lost. After six months of winning, Japan's carrier fleet had finally been stopped, and Japan never got those ships back.''',
      num("All 248", "248", "CARRIER PLANES LOST"),
      kb("After six months", "foto_kaga1936.jpg", "zoom-out"))

# ===== Bloco 4: virada, por que fechou =====
bloco("B11a", '''Japan never took Midway. But the strangest part of this story starts after the shooting stops. The Navy didn't leave.''',
      filme("Japan never took", BOM, 774.0, 778.6, "Sailors walk past the damaged hangar", data="JUNE 1942 · SAND ISLAND", vel=0.72),
      kb("The Navy didn't", "foto_midway1945.jpg", "zoom-in"),
      ideia=True)
bloco("B11b", '''In 1957, a forty-million-dollar building program began on Sand Island. Midway became home to the Pacific end of America's early-warning line, a chain of radar meant to give early warning of an attack on North America.''',
      kb("In 1957, a forty", "foto_guerrafria1959.jpg", ((0.5, 0.5, 1.0), (0.52, 0.5, 1.08))),
      mapa("Midway became home", "barreira", ["MIDWAY", "ADAK"], [("MIDWAY", "ADAK", "PACIFIC BARRIER")], selo="SCHEMATIC",
           nota="exige base com lat até 53°N (Adak)"),
      kb("a chain of radar", "foto_midway1945.jpg", "detalhe:0.35,0.62"))
bloco("B11c", '''At one time, the atoll supported more than 5,000 people. Then the Cold War ended. In 1993, Naval Air Facility Midway Island closed.''',
      kb("At one time", "foto_midway1945.jpg", ((0.35, 0.62, 1.5), (0.5, 0.5, 1.04)), enq="abre", num=("5,000+", "PEOPLE AT ITS PEAK")),
      num("Then the Cold War", "1993", "NAVAL AIR FACILITY CLOSES"))
bloco("B11d", '''And the question became: what do you do with a little city in the middle of the ocean that nobody needs to defend anymore?''',
      kb("And the question", "foto_oficina_albatrozes2015.jpg", "pan-dir"),
      kb("in the middle of the ocean", "foto_carpintaria_albatrozes2015.jpg", "zoom-out"))
bloco("B12a", '''On October 31st, 1996, President Bill Clinton signed Executive Order 13022. It moved Midway from the Navy to the Department of the Interior.''',
      doc("On October 31st", EO, "titulo", G["eo_titulo"], literal=False),
      kb("It moved Midway", "foto_canhao_historico.jpg", "pan-esq"),
      ideia=True)
bloco("B12b", '''Read section three. The Fish and Wildlife Service "shall administer the Midway Islands as the Midway Atoll National Wildlife Refuge." Now look at the first purpose on its list: "maintaining and restoring natural biological diversity within the refuge."''',
      doc("Read section three.", EO, "sec3a", G["eo_sec3a"], frase="shall administer the Midway Islands as the Midway Atoll National Wildlife Refuge"),
      kb("Now look at the first", "foto_albatroz_ninho.jpg", "pan-esq"),
      doc('"maintaining and', EO, "1", G["eo_1"], frase="maintaining and restoring natural biological diversity within the refuge"))
bloco("B12c", '''History comes fifth: "recognize and maintain the historic significance of the Midway Islands." So the island's new boss was a wildlife agency, and on paper, the birds came first.''',
      doc("History comes fifth", EO, "5", G["eo_5"], frase="recognize and maintain the historic significance of the Midway Islands"),
      filme("So the island's new", BOM, 149.5, 155.6, "Laysan albatross on Midway, filmed by Ford", data="1942 · MIDWAY", vel=0.95))
bloco("B12d", '''The last Navy personnel left the next year. In 2000, the refuge was also named the Battle of Midway National Memorial. And for a while, you could still go. Small groups flew in for wildlife and history tours.''',
      kb("The last Navy", "foto_bateria_a_2015.jpg", "zoom-in"),
      kb("In 2000, the refuge", "foto_eastern_memorial2015.jpg", "pan-dir"),
      doc("And for a while", "doc_doi2014_topo.png", "visitas", G["pagina"], literal=False, num=("~300", "VISITORS A YEAR (UNTIL 2012)")))
bloco("B13a", '''But the Navy left something behind besides runways. Many of the buildings on Midway were finished with lead-based paint. As the paint flaked, it ended up in the soil, and albatross chicks nesting right next to the walls swallowed it.''',
      filme("But the Navy left", BOM, 242.0, 245.7, "Navy B-17 on Midway's runway", data="JUNE 1942 · EASTERN ISLAND", vel=0.66),
      kb("were finished with", "foto_estacao_cabo_descascando2015.jpg", "zoom-in"),
      kb("it ended up in the soil", "foto_posto_comando2015.jpg", "detalhe:0.5,0.75"),
      ideia=True)
bloco("B13b", '''In 2014, a Fish and Wildlife official told Congress: "Lead poisoning has caused the mortality of approximately 10,000 albatross chicks annually, creating a conservation crisis." Ten thousand chicks a year.''',
      doc("In 2014, a Fish", "doc_doi2014_chumbo.png", "grifo", G["chumbo"],
          frase="Lead poisoning has caused the mortality of approximately 10,000 albatross chicks annually"),
      num("Ten thousand chicks", "10,000", "ALBATROSS CHICKS A YEAR (2014)"))
bloco("B13c", '''Starting in 2011, the Service has been scraping, sealing and tearing down. Of the old cable station buildings that were shedding paint, three were removed because they were too far gone to save. A federal audit later counted seven historic buildings demolished as part of the lead cleanup.''',
      kb("Starting in 2011", "foto_estacao_cabo2015.jpg", "pan-esq"),
      num("three were removed", "3", "CABLE STATION BUILDINGS REMOVED"),
      doc("A federal audit", GAO2, "demol", G["gao_demol"], frase="demolished seven historic", literal=False, num=("7", "HISTORIC BUILDINGS DEMOLISHED")))
bloco("B14a", '''Then came the money. Running Midway is expensive. Food, fuel and building materials come from Hawaii or the mainland. A single barge of supplies can cost about 760,000 dollars per trip.''',
      doc("Then came the money.", GAO2, "demol", G["gao_demol"], literal=False),
      mapa("Food, fuel and", "suprimento", ["HONOLULU", "MIDWAY"], [("HONOLULU", "MIDWAY", "EVERYTHING SHIPPED IN")]),
      num("A single barge", "$760,000", "PER BARGE TRIP"),
      ideia=True)
bloco("B14b", '''For fiscal years 2012 and 2013, the Service cut Midway's budget by more than a million dollars. A report by the Government Accountability Office spells out what happened next.''',
      kb("For fiscal years", "foto_carpintaria_albatrozes2015.jpg", "detalhe:0.5,0.45", num=("−$1M+", "BUDGET, FY2012–13")),
      kb("A report by", "foto_casamata_s6_2015.jpg", "detalhe:0.5,0.5"))
bloco("B14c", '''Officials said the lower budget "led to suspension of public visitation on Midway in November 2012." The same report found that the building used to house visitors was "almost beyond the point of repair and renovation."''',
      doc("Officials said", GAO2, "susp", G["gao_susp"], frase="led to suspension of public visitation", num=("NOV 2012", "VISITS SUSPENDED")),
      doc("that the building", GAO2, "reparo", G["gao_reparo"], frase="almost beyond the point of repair and renovation"))
bloco("B14d", '''To bring visitors back, the Service estimated it would need 1.2 million dollars a year. Today, the government's own page for the monument says it plainly. "Historical and eco-tour access is currently not offered."''',
      kb("To bring visitors", "foto_bateria_a_2015.jpg", "detalhe:0.45,0.55", num=("$1.2M", "A YEAR TO REOPEN")),
      doc("Today, the government's", "doc_pmnm_acesso.png", "grifo", G["pmnm"], frase="eco-tour access is currently not offered"))

# ===== Bloco 5: o que ainda está lá =====
bloco("B15a", '''So the visitors stopped. One thing didn't. The runway, Henderson Field, is still maintained as an emergency landing site. In the Service's own words to Congress, it's there "for nearly 35,000 jet aircraft transiting the Pacific Ocean."''',
      kb("So the visitors", "foto_henderson_f18_2015.jpg", "zoom-out"),
      doc("In the Service's", "doc_doi2014_35mil_jatos.png", "grifo", G["jatos"], frase="35,000 jet aircraft transiting the Pacific Ocean",
          num=("35,000", "JETS CROSSING THE PACIFIC")),
      ideia=True)
bloco("B15b", '''But there's one more reason Midway stays closed, and you can see it in the buildings. Remember the seaplane hangar, the one hit on the morning of June 4th, 1942? After the battle, only half of it was rebuilt. For eighty years, salt, wind and rain worked on it.''',
      kb("But there's one more", "foto_oficina_albatrozes2015.jpg", "detalhe:0.55,0.45"),
      filme("Remember the seaplane", BOM, 440.3, 445.2, "A hangar burning during the raid", vel=0.87),
      kb("After the battle", "foto_hangar2015.jpg", "pan-dir"),
      ideia=True)
bloco("B15c", '''In January 2022, after weeks of storms, the Fish and Wildlife Service posted this. "Sadly, the seaplane hangar collapsed on January 13 during a torrential downpour."''',
      doc("In January 2022", "doc_usfws2022_hangar.png", "pagina", G["pagina"], literal=False),
      doc('"Sadly, the seaplane', "doc_usfws2022_hangar.png", "grifo", G["hangar22"], frase="the seaplane hangar collapsed on January 13"))
bloco("B15d", '''Same building. Then and now. And the water is rising. The Service says sea level at Midway is going up about five millimeters a year, faster than the global average.''',
      ea("Same building.", "foto_hangar1942.jpg", "foto_hangar2022.jpg", "JUNE 4, 1942", "2022", num=("5 MM", "SEA LEVEL RISE PER YEAR")))
bloco("B16a", '''Midway sits barely above the sea, and in 2011, the sea came over it. On March 11th, an earthquake off Japan sent a tsunami across the Pacific.''',
      kb("Midway sits barely", "foto_iss2001.jpg", "detalhe:0.62,0.42"),
      mapa("On March 11th", "tsunami", ["TOKYO", "MIDWAY"], [("TOKYO", "MIDWAY", "TSUNAMI · MAR 11 2011")]),
      ideia=True)
bloco("B16b", '''It washed completely over Spit Island and covered about sixty percent of Eastern Island. No people were hurt.''',
      kb("It washed completely", "foto_tsunami_eastern2011.jpg", "pan-dir", num=("~60%", "OF EASTERN ISLAND FLOODED")))
bloco("B16c", '''The birds weren't so lucky. Counting the tsunami and two winter storms just before it, the Service found that more than 110,000 albatross chicks were lost. About twenty-two percent of that year's chicks. And at least two thousand adults.''',
      kb("The birds weren't", "foto_tsunami_lagoa2011.jpg", ((0.5, 0.5, 1.0), (0.5, 0.5, 1.08))),
      num("Counting the tsunami", "110,000+", "ALBATROSS CHICKS LOST"),
      kb("About twenty-two", "foto_albatroz_ninho.jpg", "zoom-in", num=("22% · 2,000+", "OF THE YEAR'S CHICKS · ADULTS")))
bloco("B17a", '''Now, that bird from 1956. Her name is Wisdom. She's a Laysan albatross. In 1956, a federal scientist named Chandler Robbins put a band on her leg while she sat on an egg. He guessed she was at least five years old.''',
      num("Now, that bird", "1956", "BANDED"),
      kb("Her name is Wisdom.", "foto_wisdom2023_a.jpg", "pan-esq"),
      kb("In 1956, a federal", "foto_robbins.jpg", "detalhe:0.4,0.4"),
      filme("He guessed she", BOM, 158.9, 161.1, "Laysan albatross on Midway, filmed by Ford", data="1942 · MIDWAY", vel=0.6, num=("5+", "YEARS OLD IN 1956")),
      ideia=True)
bloco("B17b", '''That makes her at least seventy-five now, the oldest known wild bird in the world. She outlived the lead paint, the tsunami and the storms.''',
      num("That makes her", "75+", "OLDEST KNOWN WILD BIRD"),
      kb("She outlived", "foto_wisdom2023_b.jpg", "zoom-in"))
bloco("B17c", '''In late 2024, she laid another egg, with a new mate. It hatched, but the chick didn't survive. In November 2025, she flew in again, a little earlier than in recent years. Biologists estimate she's laid fifty to sixty eggs in her life.''',
      kb("In late 2024", "foto_wisdom2023_b.jpg", "detalhe:0.6,0.4"),
      num("In November 2025", "NOV 2025", "WISDOM RETURNS"),
      kb("Biologists estimate", "foto_wisdom2023_a.jpg", "detalhe:0.45,0.45", num=("50–60", "EGGS IN HER LIFE")))
bloco("B18a", '''Every chick on Midway is fed by its parents, with whatever they scoop off the ocean. And the ocean is full of plastic. The Service estimates adult albatrosses bring about five tons of plastic to the atoll every year. Almost all chicks hatched on Midway have plastic inside them.''',
      filme("Every chick on Midway", BOM, 165.1, 171.6, "Albatross chick and adult on Midway, filmed by Ford", data="1942 · MIDWAY"),
      kb("And the ocean is", "foto_lixo_marinho2017.jpg", "zoom-in"),
      num("adult albatrosses bring", "5 TONS", "OF PLASTIC A YEAR"),
      kb("Almost all chicks", "foto_albatroz_moli.jpg", "pan-dir"),
      ideia=True)
bloco("B18b", '''Then there's the strangest thing still living there. The rats were wiped out back in 1996. The house mice were not. At the end of 2015, biologists caught those mice attacking nesting albatrosses, birds with wings longer than a man is tall, while they sat on their eggs.''',
      doc("Then there's the", "doc_usfws_msp_camundongos.png", "texto", G["pagina"], literal=False, regiao=(0.07, 0.295, 0.86, 0.215)),  # só o texto (a foto aérea do topo pode ser de parceiro)
      kb("At the end of 2015", "foto_albatroz_ninho.jpg", "detalhe:0.5,0.6"),
      num("birds with wings", "6–7 FT", "WINGSPAN"),
      ideia=True)
bloco("B18c", '''In July 2023, crews dropped poison bait from the air across Sand Island to wipe the mice out. A month later, the project admitted it hadn't worked. "Mice are still present in many areas of the island, and a root cause is not immediately evident."''',
      kb("In July 2023", "foto_iss2001.jpg", ((0.42, 0.62, 1.4), (0.46, 0.6, 1.7)), enq="sand"),
      doc('"Mice are still', "doc_usfws_msp_camundongos.png", "grifo", G["camund"], frase="root cause is not immediately evident"))
bloco("B18d", '''It's one more reason every person and every crate that lands on Midway needs a permit.''',
      kb("It's one more reason", "foto_henderson_f18_2015.jpg", "detalhe:0.6,0.6"))
bloco("B19a", '''And the battle itself? It's still out there, just not on the island. Remember line (a). Four carriers sunk. For decades, nobody knew exactly where they lay.''',
      mapa("And the battle itself", "naufragios", ["MIDWAY", "YORKTOWN (WRECK)", "KAGA (WRECK)", "AKAGI (WRECK)"], [], selo="SCHEMATIC",
           nota="posições aproximadas"),
      doc("Remember line (a).", CINC, "a", G["cinc_a"], frase="four carriers sunk", literal=False),
      ideia=True)
bloco("B19b", '''In 1998, an expedition led by Robert Ballard, with the Navy and National Geographic, found the Yorktown, about three miles down. In October 2019, the research ship Petrel found the Kaga at around 5,400 meters, more than 17,000 feet. Days later, it found the Akagi.''',
      kb("In 1998, an expedition", "foto_yorktown_torpedo1942.jpg", "detalhe:0.3,0.8", num=("3 MILES", "DOWN: YORKTOWN WRECK, FOUND 1998")),
      cartela("In October 2019", ["DEPTH PROFILE", "KAGA · ~5,400 M (17,700 FT) · OCT 2019"], selo="SCHEMATIC"),
      kb("Days later, it found", "foto_akagi1941.jpg", "zoom-out"))
bloco("B19c", '''In September 2023, the ship Nautilus sent a robot down to all three. The dives went below 5,100 meters, the deepest that ship had ever worked. On the decks, as one of the scientists put it, "many anti-aircraft guns were still pointing up."''',
      cartela("In September 2023", ["DEPTH PROFILE", "ROV DIVES BELOW 5,100 M · SEP 2023", "YORKTOWN · KAGA · AKAGI"], selo="SCHEMATIC"),
      kb("The dives went", "foto_kaga1936.jpg", "detalhe:0.55,0.45", num=("5,100 M+", "ROV DIVES TO THE WRECKS, 2023")),
      kb("On the decks", "foto_kaga1936.jpg", "detalhe:0.62,0.42"))
bloco("B19d", '''And line (c)? There's no Mogami down there. She survived Midway. The page was wrong about her. The ocean keeps a better record than the paper does.''',
      doc("And line (c)?", CINC, "c2", G["cinc_c"], frase="Mogami", literal=False),
      filme("The ocean keeps", VT8, 452.5, 457.5, "The Pacific near Midway", data="JUNE 1942 · AT SEA"),
      ideia=True)

# ===== Bloco 6: fecho =====
bloco("B20a", '''So why can't you visit Midway? Because in 1996 it stopped being a Navy base and became a wildlife refuge, and the order that did it put the birds first.''',
      filme("So why can't you", BOM, 89.6, 92.2, "Midway's islands from the sea"),
      doc("Because in 1996", EO, "1b", G["eo_1"], literal=False),
      ideia=True)
bloco("B20b", '''Because it's more than twelve hundred miles from Honolulu, and every person, meal and nail has to be flown or shipped in.''',
      mapa("Because it's more", "havai_midway_2", ["HONOLULU", "MIDWAY"], [("HONOLULU", "MIDWAY", "1,200+ MI")]),
      kb("and every person", "foto_henderson_f18_2015.jpg", "pan-esq"))
bloco("B20c", '''Because the money ran out in 2012, and the building visitors slept in was almost beyond repair. Because the old base is still shedding lead paint and falling down around nearly three million birds.''',
      doc("Because the money", GAO2, "reparo2", G["gao_reparo"], literal=False),
      kb("Because the old base", "foto_posto_comando2015.jpg", "pan-dir"))
bloco("B20d", '''And because the government itself says so: "Funding, conservation, staffing, and safety challenges have caused the Service to suspend visitor services."''',
      kb("And because the", "foto_estacao_cabo2015.jpg", "detalhe:0.5,0.4"),
      doc('"Funding, conservation', "doc_doi2014_suspensao.png", "grifo", G["suspdoi"], frase="have caused the Service to suspend visitor services"))
bloco("B21a", '''Go back to Nimitz's page one more time. Ninety-two officers. Two hundred and fifteen men. Three hundred and seven. Eighty-four years later, that is still the official American count.''',
      doc("Go back to Nimitz's", CINC, "92b", G["cinc_92"], frase="Ninety-two officers", literal=False),
      num("Three hundred and seven.", "307", "STILL THE OFFICIAL U.S. COUNT"),
      ideia=True)
bloco("B21b", '''The men who could tell you what that morning looked like are gone now. John Miniclier was the last of them. The seaplane hangar that was hit that morning has fallen in. The carriers are three miles down, guns still pointing at the surface.''',
      filme("The men who could", BOM, 984.7, 990.1, "Marines on Midway, June 1942", data="JUNE 1942 · MIDWAY", vel=0.96),
      doc("John Miniclier was", "doc_nhhc_discurso2017.png", "wreath2", G["discurso"], literal=False),
      kb("The seaplane hangar that", "foto_hangar2022.jpg", "detalhe:0.4,0.45"),
      kb("The carriers are", "foto_akagi1941.jpg", "detalhe:0.55,0.5"))
bloco("B21c", '''And every November, on an island almost nobody is allowed to see, a seventy-five-year-old albatross lands on the sand, looks around, and stays a while.''',
      ea("And every November", "foto_aerea1941.jpg", "foto_iss2001.jpg", "1941", "2001"),
      kb("a seventy-five-year-old", "foto_wisdom2023_a.jpg", "zoom-out", enq="final"))
bloco("B21d", '''If someone in your family served at Midway, on the island, on the Yorktown, or in the air, tell us their name and where they were in the comments. This is Clearance Required. We go where the record goes. If you want the next one, subscribe.''',
      filme("If someone in your", BOM, 714.5, 720.8, "A Navy flier back from the battle", data="JUNE 1942 · AT SEA", vel=0.83),
      kb("tell us their name", "foto_comemoracao2022.jpg", "detalhe:0.5,0.5"),
      card("This is Clearance"),
      ideia=True)

# Imagens a gerar por IA no corpo do vídeo: nenhuma (os cortes SCHEMATIC são código). Ver justificativa no ETAPA1.md.
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


# Grafia para a voz (Fish s2.1-pro, Narrator/Max N; decisão do Rodrigo 12/11/2026). O texto da tela e do .srt continua o original.
VOZ_SUBS = [
    ("*", ""),
    ('"4 CV sunk – Akagi, Kaga, Soryu, Hiryu – with', '"Four C-V sunk. Ah-kah-gee, Kaga, Soryu, Hiryu. With'),
    ('"2 CA sunk – Mogami, Mikuma."', '"Two C-A sunk. Mogami, Mikuma."'),
    ("line (a)", "line A"), ("Line (c)", "Line C"), ("line (c)", "line C"),
    ("Akagi, Kaga and Soryu", "Ah-kah-gee, Kaga, and Soryu"),  # B09c: sem a vírgula saiu "Akaga" (Whisper, 12/11)
    ("Akagi", "Ah-kah-gee"), ('"AF."', '"A-F."'), ("AF was", "A-F was"),
    ("I-168", "I-one sixty-eight"), ("10:20", "ten twenty"), ("Order 13022", "Order thirteen-oh-twenty-two"),
]


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
    NOMES = {"Yorktown": ["yorktown", "mapa:reboque", "mapa:naufragios"], "Hiryu": ["hiryu"], "Soryu": ["soryu"],
             "Mikuma": ["mikuma", "cinc"], "Wisdom": ["wisdom"], "Rochefort": ["rochefort"], "Yamamoto": ["yamamoto"],
             "George Gay": ["gay", "filme_torpedo"], "Waldron": ["filme_torpedo"], "Robbins": ["robbins"]}
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

    L = ["# STORYBOARD: 001-midway (lugares-guerra-en, \"Clearance Required\")", "",
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
