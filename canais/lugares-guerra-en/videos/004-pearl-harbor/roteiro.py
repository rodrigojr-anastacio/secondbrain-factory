#!/usr/bin/env python3
"""Fonte do storyboard do lugares-guerra-en 004 "Why Are There Still Bullet Holes at Pearl Harbor?" (youtube.videos id 42).
Uso: cd <pasta do vídeo> && python3 roteiro.py   (python3 puro, sem dependências)

O roteiro FINAL é o SCRIPT.md (fatos em FATOS.md/SOURCES.md). Os blocos de áudio vêm de tools/split_blocos.py
(qa/split_blocos.json + blocos-voz.json). Este arquivo define os planos visuais de cada bloco e valida:
narração idêntica ao SCRIPT.md, arquivos no midia.csv, Ficha em toda foto, tipo de tela ≤ 12 s (KenBurns/Dupla/DocGrifo/Filme ≤ 14 s:
cada plano é outro enquadramento ou outro trecho), reuso, grifo literal, ≥ 85% material real.
Gera: blocos.json, storyboard.json, STORYBOARD.md, cenas.json (vazio: nenhuma imagem IA no corpo).
Código base: 003-gettysburg/roteiro.py (Dupla) + o tipo Filme do 002-bikini (trechos de filme NARA 428-NPC já recortados em midia/).
Citações que só existem em página web/fact sheet (sem scan) vão em Cartela com Selo QUOTED (bíblia/visual.md, aprendizado do 002);
as 3 "recomposições tipográficas" (doc_lei…, doc_dvids…, doc_dpaa…) NÃO entram como DocGrifo (não são documento escaneado).
Bíblia: canais/lugares-guerra-en/biblia/. Regra do brief: nada de corpo/ferido/restos/exumação na tela.
"""
import csv
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MIDIA = AQUI / "midia"
WPS = 2.8                 # voz Narrator medida no 002: 2.549 palavras em 15,2 min de áudio (≈168 ppm)
RUN_MAX = 12.0
RUN_MAX_FOTO = 14.0       # KenBurns/Dupla seguidos (planos diferentes)
JANELA = 60.0
INEDITO_ATE = 180.0
REUSO_LIBERADO = {"hoje_hickam_qg_marcas_tiro.jpg", "hoje_pacaf_qg_staff_ride.jpg", "hoje_jbphh_portao_omalley_a.jpg", "hoje_jbphh_portao_omalley_b.jpg", "foto_hickam_quartel_hangar_ave_1941.jpg"}   # a parede do hook e o portão voltam de propósito
REAL_MIN = 0.85

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


def _dur_filmes():
    out = {}
    with open(AQUI / "midia.csv", newline="") as f:
        for r in csv.DictReader(f):
            m = re.search(r"([\d.]+)s", r["resolucao"])
            if r["arquivo"].endswith(".mp4") and m:
                out[r["arquivo"]] = float(m.group(1))
    return out


DUR_FILME = _dur_filmes()
FILME_MAX = 7.0           # trecho de filme por plano (regra do build.py)


def filme(em, arq, tin, tout, vel=1.0, num=None):
    return dict(tipo="Filme", em=em, arq=arq, enq=f"{tin:.1f}-{tout:.1f}", tin=tin, tout=tout, vel=vel, num=num)


def dupla(em, arq, arq2, rot1, rot2, num=None, selo=None):
    return dict(tipo="Dupla", em=em, arq=arq, arq2=arq2, enq="dupla", rot1=rot1, rot2=rot2, num=num, selo=selo)


def doc(em, arq, enq, grifo, frase=None, literal=True, num=None, ficha=None, regiao=None):
    return dict(tipo="DocGrifo", em=em, arq=arq, enq=enq, grifo=grifo, frase_doc=frase, literal=literal and bool(frase), num=num,
                ficha=ficha, regiao=regiao)


def num(em, valor, rotulo=""):
    return dict(tipo="Número", em=em, arq="codigo", enq="num:" + valor, valor=valor, rotulo=rotulo)


def mapa(em, nome, pontos, linhas, selo=None, nota="", base=None):
    return dict(tipo="Mapa2D", em=em, arq=base or "codigo", enq="mapa:" + nome, nome=nome, pontos=pontos, linhas=linhas,
                selo=selo, nota=nota)


def cartela(em, linhas, selo="SCHEMATIC"):
    return dict(tipo="Cartela", em=em, arq="codigo", enq="cartela:" + linhas[0], linhas=linhas, selo=selo)


def ea(em, antes, depois, rot1, rot2, num=None):
    return dict(tipo="EntaoAgora", em=em, arq=antes, arq2=depois, enq="ea", rot1=rot1, rot2=rot2, num=num)


def card(em):
    return dict(tipo="Card", em=em, arq="codigo", enq="card")


# Fichas: 1 linha (DATA · LUGAR) na tela; vem da "Ficha sugerida" do midia.csv (tools/gera_midia_csv.py).
def _fichas():
    out = {}
    with open(AQUI / "midia.csv", newline="") as f:
        for r in csv.DictReader(f):
            m = re.search(r"Ficha sugerida:\s*(.+)$", r["observacao"])
            if m:
                out[r["arquivo"]] = (m.group(1).strip(), "", r["credito"])
    return out


FICHAS = _fichas()


def px(b, W, H):
    return (round(b[0] / W, 4), round(b[1] / H, 4), round(b[2] / W, 4), round(b[3] / H, 4))



# Grifos (x, y, largura, altura) em pixels do arquivo; estimados à vista em 15/11/2026: CONFERIR nos stills da etapa 2.
DESP = (2410, 1898)   # doc_despacho_not_drill_nara596244.png
NHLM = (1997, 764)    # doc_nhl_hickam_marcas.png
NHLC = (1997, 1232)   # doc_nhl_hickam_capa.png
FAQ = (2200, 950)     # doc_nps_faq_utah.png
G = {
    "drill": [px([307, 1205, 1464, 62], *DESP)],
    "data41": [px([1780, 690, 330, 70], *DESP)],
    "capa_nome": [px([318, 598, 240, 50], *NHLC)],
    "nhl_repaired": [px([568, 528, 1290, 44], *NHLM), px([110, 570, 1748, 44], *NHLM), px([110, 612, 412, 42], *NHLM)],
    "nhl_steel": [px([800, 180, 945, 44], *NHLM)],
    "nhl_hale": [px([840, 440, 1020, 44], *NHLM), px([110, 482, 470, 44], *NHLM)],
    "faq_tour": [px([20, 180, 2125, 44], *FAQ), px([20, 233, 478, 44], *FAQ)],
    "faq_cancel": [px([92, 820, 1560, 46], *FAQ)],
    "pagina": [],
}

# Pontos de mapa (lon E 0–360, lat). Coordenadas aproximadas (15/11/2026) a conferir na etapa 2; o QG da PACAF (Hale Makai)
# fica ~3,3 km (~2 mi) ao sul do Pearl Harbor Visitor Center em linha reta [I] (FATOS.md F81).
P = {"VISITOR CENTER": (202.0607, 21.3676), "USS ARIZONA MEMORIAL": (202.0500, 21.3649), "FORD ISLAND": (202.0390, 21.3640),
     "USS UTAH MEMORIAL": (202.0380, 21.3685), "PACAF HQ (HALE MAKAI)": (202.0539, 21.3389), "HICKAM FIELD": (202.0600, 21.3300),
     "PEARL HARBOR": (202.0200, 21.3700), "HONOLULU": (202.1420, 21.3070), "WHEELER": (201.9620, 21.4810), "BELLOWS": (202.2880, 21.3660),
     "KAHUKU": (202.0300, 21.6900), "HALEIWA": (201.8900, 21.5850), "KILO PIER": (202.0430, 21.3550)}

B = []
SPLIT = {b["id"]: b["texto"] for b in json.load(open(AQUI / "qa/split_blocos.json"))}


def bloco(bid, *planos, ideia=False):
    B.append(dict(id=bid, texto=SPLIT[bid], ideia=ideia, planos=list(planos)))


# Arquivos usados com frequência
WALL = "hoje_hickam_qg_marcas_tiro.jpg"            # A PAREDE DO HOOK (foto oficial USAF)
CRAT = "detalhe:0.87,0.22"                        # cratera grande no alto à direita
CRAT2 = "detalhe:0.78,0.47"                       # cratera na moldura art déco
CHIPS = "detalhe:0.6,0.6"                         # lascas pequenas
WALL_ZOOM = ((0.5, 0.5, 1.04), (0.82, 0.35, 1.6))
PRED = "hoje_hickam_predio_marcas_tiro_134arw.jpg"
REPA, REPB, REPC = "hoje_hickam_replica_marca_tiro_a.jpg", "hoje_hickam_replica_marca_tiro_b.jpg", "hoje_hickam_replica_marca_tiro_c.jpg"
FLAG41, FLAGNOW = "foto_hickam_bandeira_fumaca_1941.jpg", "hoje_hickam_bandeira_1941_exposta.jpg"
QUARTEL41 = "foto_hickam_quartel_hangar_ave_1941.jpg"
GATEA, GATEB = "hoje_jbphh_portao_omalley_a.jpg", "hoje_jbphh_portao_omalley_b.jpg"
STAFF, COURT = "hoje_pacaf_qg_staff_ride.jpg", "hoje_hickam_courtyard_heroes.jpg"
DESPACHO, NHLM_, NHLC_, FAQ_ = "doc_despacho_not_drill_nara596244.png", "doc_nhl_hickam_marcas.png", "doc_nhl_hickam_capa.png", "doc_nps_faq_utah.png"
FORD41, FORD22, FORD23 = "foto_ford_aerea_1941-11-10.jpg", "hoje_ford_aerea_2022a.jpg", "hoje_ford_island_aerea_2023.jpg"
F_AVIAO, F_FUMACA = "filme_ataque_aviao_sobre_navio_nara76168.mp4", "filme_ataque_fumaca_pearl_harbor_nara76168.mp4"
F_FORDH, F_FORDE = "filme_ford_hangares_avioes_danificados_nara76169.mp4", "filme_ford_hangar_escombros_fumaca_nara76171.mp4"
F_RESC, F_ANTES, F_CASCO = "filme_pearl_navios_danificados_rescaldo_nara76169.mp4", "filme_pearl_navy_yard_antes_nara77339.mp4", "filme_casco_emborcado_nara76171.mp4"
H79 = "hoje_hangar79_habs_1991.jpg"
MAPA_PORTO = ["VISITOR CENTER", "USS ARIZONA MEMORIAL", "FORD ISLAND", "PACAF HQ (HALE MAKAI)"]

# ===================================================================== planos
# ===== Bloco 1: hook (a parede)
bloco("B01a",
      kb("Look at this wall.", WALL, "zoom-in"),
      kb("Count the marks.", WALL, CRAT),
      kb("Some are small chips.", WALL, CHIPS),
      ideia=True)
bloco("B01b",
      kb("They're bullet and shrapnel strikes,", REPB, "zoom-in"),
      filme("and they come from one morning:", F_FUMACA, 0.5, 6.5, num=("DEC 7, 1941", "PEARL HARBOR")),
      filme("This is Pearl Harbor,", F_AVIAO, 24.0, 31.0),
      kb("And these marks were never patched.", PRED, "pan-esq"),
      kb("They were left there on purpose.", WALL, CRAT2))
bloco("B01c",
      kb("And unless you carry a military ID,", GATEA, "zoom-in"),
      kb("you can't get anywhere near this wall.", GATEB, "pan-dir"),
      num("So why are there still bullet holes", "?", "WHY ARE THERE STILL BULLET HOLES AT PEARL HARBOR?"))

# ===== Bloco 2: o portão + âncora humana
bloco("B02a",
      kb("It isn't neglect.", WALL, "pan-dir"),
      kb("And it isn't a museum.", COURT, "zoom-in"),
      kb("This wall belongs to a working headquarters:", STAFF, "zoom-out", num=("PACAF", "PACIFIC AIR FORCES HEADQUARTERS")),
      ideia=True)
bloco("B02b",
      mapa("It sits on what was once Hickam Field,", "porto", MAPA_PORTO, [("VISITOR CENTER", "PACAF HQ (HALE MAKAI)", "~2 MILES")],
           nota="linha reta Visitor Center → QG; conferir distância"),
      kb("On the other side of a gate.", GATEB, "zoom-in"),
      kb("In 1941, this was a barracks.", QUARTEL41, "zoom-in", num=("DURWARD SWANSON", "MILITARY POLICE · HICKAM FIELD, 1941")))
bloco("B02c",
      dupla("Decades later, he came back", "hoje_cerimonia_7dez_2013_hickam.jpg", QUARTEL41, "HICKAM SURVIVORS, 2013", "HIS BARRACKS, 1941", num=("2011", "BACK IN HIS OLD ROOM")),
      cartela("\"I saw a plane banking", ["\"I SAW A PLANE BANKING AND THE RISING SUN ON THE WING…", "WE WERE AT WAR.\"", "— DURWARD SWANSON (PACAF, 2011)"], selo="QUOTED"))
bloco("B02d",
      dupla("Along the way, you'll see", QUARTEL41, WALL, "1941", "TODAY"),
      doc("the paper that explains", NHLC_, "pagina", G["pagina"]),
      kb("and everything else that still sits", "hoje_utah_memorial_aerea_2016.jpg", "zoom-in"))

# ===== atrás do portão
bloco("B03a",
      kb("Most visitors never think about the gate,", "hoje_arizona_barco_visitantes_fuqua.jpg", "pan-dir"),
      dupla("A visitor center. A boat.", "hoje_arizona_barco_finn.jpg", "hoje_arizona_memorial_visita_2012.jpg", "THE BOAT", "THE MEMORIAL"),
      ideia=True)
bloco("B03b",
      kb("But almost everything around it", FORD23, "pan-esq", num=("JBPHH", "ACTIVE MILITARY BASE")),
      dupla("And the building with the scarred walls", PRED, WALL, "HICKAM", "THE OLD BARRACKS"),
      kb("It's a headquarters,", STAFF, "pan-dir"),
      doc("And it's part of a National Historic Landmark.", NHLC_, "nome", G["capa_nome"], literal=False))
bloco("B03c",
      cartela("As one historian of Hickam Field put it,", ["\"SINCE THE BUILDINGS ARE PROTECTED BY LAW, THE MILITARY CAN'T CHANGE THE APPEARANCE.\"", "— JESSIE HIGA, HICKAM HISTORIAN (DVIDS, 2017)"], selo="QUOTED"),
      kb("So the most guarded building", WALL, "zoom-out"),
      kb("And it's not alone.", "hoje_hickam_base_ops_historiadora.jpg", "zoom-in"))
bloco("B03d",
      kb("Behind the same gate there are hangars", "hoje_hangar6_habs_frente.jpg", "pan-dir"),
      dupla("There's a memorial to a battleship", "hoje_utah_memorial_1988.jpg", "hoje_utah_memorial_aerea_2016.jpg", "USS UTAH MEMORIAL", "FORD ISLAND"),
      kb("And in the lobby of this building,", STAFF, "detalhe:0.75,0.4"),
      num("We'll come back to it.", "?", "BEHIND THE GLASS"))

# ===== Bloco 3: o que aconteceu ali
bloco("B04a",
      kb("To understand the marks,", "foto_hickam_campo_antes.jpg", "pan-dir"),
      dupla("In the 1930s, the Army Air Corps", "foto_ford_aerea_1940-05-03.jpg", "foto_hickam_entrada_1937.jpg", "PEARL HARBOR, 1940", "HICKAM FIELD, 1937"),
      kb("They named it Hickam Field.", "foto_hickam_entrada_1937.jpg", "zoom-in"),
      kb("At its heart was one enormous building,", QUARTEL41, "pan-esq"),
      ideia=True)
bloco("B04b",
      ea("The Air Force calls it", QUARTEL41, COURT, "1941", "TODAY", num=("3,200", "MEN · BIGGEST BARRACKS IN THE ARMY AIR FORCES")),
      kb("In Hawaiian, it was Hale Makai,", COURT, "detalhe:0.5,0.35", num=("HALE MAKAI", "\"HOUSE BY THE SEA\"")))
bloco("B04c",
      doc("On the morning of December 7th, 1941,", NHLM_, "pagina", G["pagina"], num=("51", "AIRPLANES ON THE GROUND AT HICKAM")),
      kb("Big B-17 bombers stood out", "foto_hickam_b17s_1941.jpg", "zoom-in"),
      filme("And a flight of twelve more B-17s", F_ANTES, 4.0, 12.0))

bloco("B05a",
      kb("At 7:55 a.m.,", "foto_ford_japonesa_80g30550.jpg", "zoom-in", num=("183", "JAPANESE AIRCRAFT · FIRST WAVE")),
      kb("One of the first bombs fell", "foto_ford_japonesa_80g30553_lado_norte.jpg", "zoom-in"),
      filme("Minutes later, a message went out.", F_AVIAO, 2.0, 8.0),
      ideia=True)
bloco("B05b",
      doc("This is a copy of it,", DESPACHO, "pagina", G["pagina"]),
      doc("\"Air raid on Pearl Harbor.", DESPACHO, "drill", G["drill"], frase="this is not drill"))
bloco("B05c",
      cartela("The Navy's own report records", ["\"AIR RAID PEARL HARBOR X THIS IS NO DRILL\"", "— PATROL WING TWO ACTION REPORT, 0758"], selo="QUOTED"),
      filme("Either way, the warning came after", F_FUMACA, 9.0, 16.0),
      num("Remember one word:", "UNPREPARED", ""))
bloco("B05d",
      kb("A few miles away, at Hickam,", "foto_hickam_kate_sobrevoa_1941.jpg", "pan-dir"),
      kb("They were concentrating on the B-17s.", "foto_hickam_b17_hangar5_1941.jpg", "zoom-in"))

bloco("B06a",
      dupla("And in the middle of all this,", "foto_hickam_b17s_1941.jpg", "foto_hickam_80g32899.jpg", "12 B-17s FROM CALIFORNIA", "HICKAM, DEC 7"),
      filme("They were unarmed,", F_AVIAO, 14.0, 21.0),
      kb("Instead of a welcome,", "foto_hickam_80g32899.jpg", "zoom-in"),
      ideia=True)
bloco("B06b",
      kb("Their crews landed wherever they could.", "foto_hickam_cratera_hangares_1941.jpg", "zoom-in"),
      mapa("The Air Force lists one at Bellows Field,", "oahu", ["HICKAM FIELD", "WHEELER", "BELLOWS", "KAHUKU", "HALEIWA"],
           [("HICKAM FIELD", "BELLOWS", ""), ("HICKAM FIELD", "WHEELER", ""), ("HICKAM FIELD", "KAHUKU", ""), ("HICKAM FIELD", "HALEIWA", "")],
           nota="onde pousaram os 12 B-17 (AF-FS)"),
      kb("and the rest at Hickam, under attack.", "foto_hickam_aerea_7dez.jpg", "zoom-in"),
      kb("Three hangars took direct hits.", "foto_hickam_hangar11_1941.jpg", "pan-dir"))
bloco("B06c",
      kb("The Park Service's landmark report", "foto_hickam_cratera_hangar7_1941.jpg", "zoom-in"),
      num("At 8:40, a second wave struck.", "8:40", "SECOND WAVE · OVER BY 9:45"),
      kb("About half the airplanes", "foto_hickam_b18_danificados_1941.jpg", "zoom-in"))

bloco("B07a",
      kb("And the Big Barracks?", QUARTEL41, "zoom-in"),
      filme("Planes strafed it.", F_FORDE, 30.0, 37.0),
      ideia=True)
bloco("B07b",
      kb("Part of it caught fire.", FLAG41, "tilt-baixo"),
      kb("Many of the men had been at breakfast", "foto_hickam_bombeiros_quartel_incendio_1941.jpg", "pan-dir"),
      dupla("Air Force captions call it", QUARTEL41, FLAG41, "THE BIG BARRACKS", "DEC 7, 1941", num=("\"MOST BOMBED\"", "BUILDING ON OAHU (REPORTEDLY)")))
bloco("B07c",
      dupla("When the smoke cleared,", "hoje_hickam_memorial_1991.jpg", COURT, "HICKAM MEMORIAL, 1991", "COURTYARD OF HEROES", num=("189", "MEN LOST AT HICKAM · 303 WOUNDED")),
      filme("The building was repaired.", F_RESC, 4.0, 11.0),
      kb("So the question is the one", WALL, "zoom-in"))

# ===== Bloco 4: a virada (por que ficou)
bloco("B08a",
      kb("Why keep the marks?", WALL, CRAT),
      cartela("\"This former 'Big Barracks'", ["\"…ITS BULLET-SCARRED WALLS ARE CAREFULLY PRESERVED TO SERVE AS A CONSTANT REMINDER", "TO NEVER AGAIN BE CAUGHT UNPREPARED.\"", "— U.S. AIR FORCE FACT SHEET, \"DECEMBER 7, 1941 ATTACK\""], selo="QUOTED"),
      kb("There's the word.", PRED, "zoom-in"),
      ideia=True)
bloco("B08b",
      num("Unprepared.", "UNPREPARED", "THE OFFICIAL REASON"),
      kb("The headquarters for American air power", STAFF, "pan-esq"),
      kb("Every officer who goes to work", WALL, "pan-esq"))
bloco("B08c",
      doc("But the strangest part", NHLC_, "pagina", G["pagina"]))

bloco("B09a",
      doc("In 1984, the National Park Service", NHLC_, "nome", G["capa_nome"], frase="Hickam Field", num=("1985", "NATIONAL HISTORIC LANDMARK")),
      kb("The Secretary of the Interior designated it in 1985:", "foto_hickam_aerea_7dez.jpg", "pan-dir", num=("81", "ACRES OF AN ACTIVE AIRFIELD")),
      ideia=True)
bloco("B09b",
      num("Two years later, Wheeler Field,", "1987", "WHEELER FIELD · SAME STATUS"),
      doc("The form describes the barracks plainly.", NHLM_, "hale", G["nhl_hale"], literal=False),
      doc("\"The bomb and fire damage", NHLM_, "repaired", G["nhl_repaired"],
          frase="but a large number of spatter holes remain on the exterior walls where bullets hit the concrete"))
bloco("B09c",
      kb("The hangars, it says,", "foto_hickam_hangar11_1941.jpg", "zoom-in"),
      doc("\"A bullet hole clear through", NHLM_, "steel", G["nhl_steel"], frase="a bullet hole clear through a steel column"),
      kb("And then one sentence", "hoje_hickam_ninho_corvo_a.jpg", "zoom-in"))
bloco("B09d",
      cartela("\"Here, one captures the feeling", ["\"HERE, ONE CAPTURES THE FEELING OF THE PRE-WORLD WAR II MILITARY ENVIRONMENT IN HAWAII,",
              "AS WELL AS COMING INTO CONTACT WITH THE PHYSICAL DAMAGE OF THE SURPRISE ATTACK.\"", "— NHL NOMINATION, HICKAM FIELD (1984)"], selo="QUOTED"),
      kb("Coming into contact.", REPC, "zoom-in"),
      kb("The landmark exists so that someone", WALL, CRAT2),
      kb("The base exists so that almost no one can.", GATEA, "pan-esq"))

bloco("B10a",
      dupla("So the marks are protected twice:", WALL, NHLC_, "THE AIR FORCE: A REMINDER", "THE LAW: A LANDMARK"),
      kb("When the building was renovated,", PRED, "pan-dir"),
      ideia=True)
bloco("B10b",
      dupla("The firm that did the work says", PRED, WALL, "STRAFING MARKS", "PRESERVED"),
      kb("and that fire-damaged beams", COURT, "zoom-out"),
      kb("The same historian, Jessie Higa,", "hoje_hickam_base_ops_historiadora.jpg", "detalhe:0.3,0.45"))
bloco("B10c",
      cartela("\"The outside markings", ["\"THE OUTSIDE MARKINGS FROM THE DECEMBER 7 DAMAGE BECOME A BIRTHMARK…\"", "— JESSIE HIGA (DVIDS, 2017)"], selo="QUOTED"),
      kb("In 2017, an airman was given", REPA, "zoom-in", num=("2017", "A CAST OF ONE POCKMARK")),
      dupla("Think about that.", REPB, WALL, "THE COPY", "THE ORIGINAL"))
bloco("B10d",
      dupla("To carry a piece of this wall", REPC, PRED, "THE MOLD", "THE WALL"))

bloco("B11a",
      kb("Now, the thing behind the glass.", STAFF, "detalhe:0.75,0.4"),
      kb("That morning, an American flag", FLAG41, "zoom-out"),
      kb("It flew through both waves.", FLAG41, "detalhe:0.45,0.25"),
      ideia=True)
bloco("B11b",
      num("That night, around nine,", "9 P.M.", "DEC 7, 1941"),
      kb("Durward Swanson and his best friend,", "hoje_cerimonia_7dez_2013_hickam.jpg", "zoom-in"),
      cartela("Swanson remembered telling him,", ["\"STUD, THE FLAG IS STILL FLYING.", "WE'VE GOT TO TAKE THAT DOWN.\"", "— DURWARD SWANSON (PACAF, 2011)"], selo="QUOTED"))
bloco("B11c",
      kb("They lowered it and folded it,", FLAGNOW, "detalhe:0.5,0.55"),
      ea("That flag is now in a case", FLAG41, FLAGNOW, "DEC 7, 1941", "TODAY"))
bloco("B11d",
      kb("The Air Force calls it", FLAGNOW, "zoom-out"),
      kb("It's torn.", FLAGNOW, "detalhe:0.62,0.5"),
      kb("And like the wall,", WALL, "pan-esq"))

# ===== Bloco 5: por que o portão continua fechado / o que mais está lá
bloco("B12a",
      dupla("So why can't a tourist", GATEA, GATEB, "O'MALLEY GATE", "ENTRY CONTROL"),
      kb("Because in 2010,", FORD22, "pan-dir", num=("2010", "JOINT BASE PEARL HARBOR-HICKAM")),
      ideia=True)
bloco("B12b",
      dupla("It isn't a historic park", "hoje_arizona_memorial_visita_2012.jpg", FORD23, "THE PARK", "THE BASE"),
      kb("To get in without military ID,", GATEA, "detalhe:0.45,0.45"))
bloco("B12c",
      dupla("The Navy's own instructions say", GATEB, STAFF, "VISITORS", "\"AUTHORIZED SPONSORS ONLY\""),
      kb("Even the identification is controlled:", GATEB, "detalhe:0.55,0.5", num=("REAL ID", "REQUIRED SINCE MAY 2025")),
      dupla("None of that is about hiding the wall.", WALL, FORD22, "THE WALL", "EVERYTHING AROUND IT"))
bloco("B12d",
      kb("The marks just happen to be", PRED, "zoom-out"),
      num("In 2019, Congress created", "2019", "PEARL HARBOR NATIONAL MEMORIAL"),
      kb("The law says it plainly.", "hoje_arizona_memorial_navsup.jpg", "zoom-in"))
bloco("B12e",
      cartela("\"There is established", ["\"THERE IS ESTABLISHED THE PEARL HARBOR NATIONAL MEMORIAL IN THE STATE OF HAWAI'I", "AS A UNIT OF THE NATIONAL PARK SYSTEM.\"", "— PUBLIC LAW 116-9, SEC. 2206 (2019)"], selo="QUOTED"),
      kb("But the law doesn't list the places.", "hoje_arizona_memorial_visita_2012.jpg", "pan-dir"))
bloco("B12f",
      mapa("And on the Park Service's own list,", "memorial", ["VISITOR CENTER", "USS ARIZONA MEMORIAL", "FORD ISLAND", "USS UTAH MEMORIAL", "PACAF HQ (HALE MAKAI)"], [],
           nota="pontos do memorial em amarelo; o QG (fora do memorial) em vermelho"),
      kb("The barracks at Hickam aren't on it.", WALL, "zoom-out"))
bloco("B12g",
      dupla("So the most visited part", "hoje_arizona_barco_visitantes_fuqua.jpg", PRED, "NATIONAL PARK", "NOT ON THE LIST"),
      kb("It's a landmark inside a base,", STAFF, "zoom-out"))

bloco("B13a",
      kb("There's one more reason", FORD22, "zoom-in"),
      dupla("This is Ford Island.", "foto_ford_aerea_1941-06_overhead.jpg", FORD23, "JUNE 1941", "2023"),
      ideia=True)
bloco("B13b",
      kb("The Navy's historians say", "foto_ford_pby_destruidos_nara306552.jpg", "pan-dir", num=("33", "AIRCRAFT PUT OUT OF ACTION")),
      filme("and one big hangar was gutted.", F_FORDH, 6.0, 13.0),
      kb("Reportedly, the very first bomb", "foto_ford_hangar_incendio_nara306544.jpg", "zoom-in"),
      doc("That's what set off the message", DESPACHO, "data", G["data41"], literal=False),
      kb("Today Ford Island is still part of the base.", FORD23, "pan-esq"))
bloco("B13c",
      kb("But part of it opened to visitors:", "hoje_ford_torre_controle.jpg", "tilt-cima"),
      dupla("And in one of them, Hangar 79,", H79, "hoje_hangar79_voluntarios_c.jpg", "HANGAR 79, 1991", "HANGAR 79, 2024"))
bloco("B13d",
      kb("Its windows still have bullet holes", "hoje_hangar79_voluntarios_a.jpg", "detalhe:0.7,0.3"),
      kb("The museum says the Navy didn't replace them,", H79, "zoom-in"))

bloco("B14a",
      kb("And the museum adds something", "hoje_hangar79_voluntarios_b.jpg", "zoom-in"),
      filme("That night, American fighters", F_FORDE, 40.0, 47.0),
      filme("Nervous gunners opened fire,", F_FORDE, 10.0, 17.0),
      kb("So some of those holes", H79, "pan-esq"),
      ideia=True)
bloco("B14b",
      kb("The glass records the whole day,", "hoje_hangar79_voluntarios_a.jpg", "zoom-out"),
      dupla("Out on the old seaplane ramp", "hoje_ford_rampa_marcas_tiro_habs.jpg", "hoje_ford_estacionamento_marcas_tiro_habs.jpg", "SEAPLANE RAMP", "AIRCRAFT PARKING"),
      kb("Those areas are part of the working base.", FORD23, "zoom-in"))
bloco("B14c",
      ea("Ford Island is the one place", "foto_ford_hangar6_destrocos_1941.jpg", "hoje_hangar6_habs_frente.jpg", "1941", "1990s"),
      dupla("And it's the place that proves", H79, GATEA, "YOU CAN SEE THIS", "BUT NOT PAST THIS"))

bloco("B15a",
      kb("Because a few hundred yards", "hoje_utah_memorial_aerea_2016.jpg", "zoom-in"),
      kb("A target ship,", "foto_ford_utah_emborcado_80g266626.jpg", "zoom-in"),
      num("Fifty-eight of her crew were lost.", "58", "CREW LOST · USS UTAH"),
      ideia=True)
bloco("B15b",
      kb("She was never raised.", "hoje_utah_memorial_1988.jpg", "pan-dir"),
      kb("A memorial was dedicated", "hoje_utah_memorial_74_comemoracao.jpg", "zoom-in", num=("1972", "USS UTAH MEMORIAL")),
      kb("The Park Service puts it plainly.", GATEB, "pan-esq"))
bloco("B15c",
      doc("\"To visit these memorials,", FAQ_, "tour", G["faq_tour"],
          frase="you must reserve a seat on the Ford Island Bus Tour if you do not have an Active-Duty Military ID"))
bloco("B15d",
      num("The tour runs on Mondays,", "MON · WED · FRI", "AFTERNOONS · RESERVATION REQUIRED"),
      doc("and the Park Service warns", FAQ_, "cancel", G["faq_cancel"], literal=False))
bloco("B15e",
      kb("Even the anniversary ceremony at the Utah,", "hoje_utah_memorial_74_comemoracao.jpg", "pan-esq", num=("DEC 6", "UTAH CEREMONY · BASE ACCESS REQUIRED")),
      dupla("The same goes for the ceremony", "hoje_cerimonia_7dez_2016.jpg", GATEB, "DEC 7 CEREMONIES", "BASE ACCESS REQUIRED"),
      kb("Open to the public. Inside the gate.", GATEA, "zoom-in"))

bloco("B16a",
      kb("December 7th, 2026,", "hoje_cerimonia_7dez_2016.jpg", "pan-dir", num=("85", "YEARS · DEC 7, 2026")),
      dupla("For decades, eighty-six unidentified sailors", "hoje_arizona_memorial_visita_2012.jpg", "hoje_arizona_memorial_navsup.jpg", "USS ARIZONA MEMORIAL", "THE WALL OF NAMES", num=("86", "USS ARIZONA UNKNOWNS")),
      ideia=True)
bloco("B16b",
      cartela("Now the Defense POW/MIA Accounting Agency", ["DEFENSE POW/MIA ACCOUNTING AGENCY", "USS ARIZONA (BB-39) UNKNOWN IDENTIFICATION PROJECT", "\"…THE 60% THRESHOLD OF DNA FAMILY REFERENCE SAMPLES HAS BEEN MET…\""], selo="QUOTED"),
      kb("It waited until DNA reference samples", "hoje_cerimonia_7dez_2013_hickam.jpg", "pan-esq"))
bloco("B16c",
      dupla("The first eight caskets were moved this month,", FORD23, GATEB, "JOINT BASE PEARL HARBOR-HICKAM", "DPAA LAB · ON BASE", num=("8 OF 86", "NOVEMBER 2026")))
bloco("B16d",
      kb("On the anniversary,", "hoje_cerimonia_7dez_2016.jpg", "zoom-out", num=("700+", "FAMILY MEMBERS EXPECTED")),
      dupla("So even the work of giving those men", "hoje_arizona_memorial_navsup.jpg", GATEA, "THE NAMES", "BEHIND THE GATE"))

bloco("B17a",
      kb("Every year, around one and a half million", "hoje_arizona_barco_visitantes_fuqua.jpg", "zoom-in", num=("~1.5M", "VISITORS A YEAR")),
      dupla("They take the boat.", "hoje_arizona_barco_finn.jpg", "hoje_arizona_memorial_visita_2012.jpg", "THE BOAT", "THE MEMORIAL"),
      ideia=True)
bloco("B17b",
      filme("It's a powerful visit,", F_RESC, 20.0, 27.0),
      kb("But it's built on a small piece", FORD23, "zoom-out"),
      kb("Ford Island tells that story", FORD41, "zoom-in"),
      kb("Here it is four weeks before the attack,", FORD41, "detalhe:0.6,0.55"))
bloco("B17c",
      ea("And here it is now,", FORD41, FORD22, "NOV 10, 1941", "2022"),
      kb("About two miles away,", PRED, "pan-dir"),
      kb("Here it is in 1941, burning.", QUARTEL41, "zoom-in"))
bloco("B17d",
      ea("And here it is today,", QUARTEL41, WALL, "1941", "TODAY"),
      kb("The fire is gone.", "foto_hickam_bombeiros_1941.jpg", "zoom-out"),
      kb("The people inside plan", STAFF, "pan-dir"))
bloco("B17e",
      kb("And the marks are still in the concrete,", WALL, WALL_ZOOM, enq="zoom-marcas"))

# ===== Bloco 6: fecho
bloco("B18a",
      num("So why are there still bullet holes", "?", "WHY ARE THERE STILL BULLET HOLES AT PEARL HARBOR?"),
      kb("Because the Air Force keeps them on purpose,", PRED, "zoom-in"),
      doc("Because federal law protects the buildings", NHLM_, "repaired2", G["nhl_repaired"], literal=False),
      ideia=True)
bloco("B18b",
      dupla("And because the wall belongs to a headquarters", GATEA, STAFF, "AN ACTIVE BASE", "A WORKING HEADQUARTERS"),
      kb("Now look at the wall one more time.", WALL, "zoom-out"),
      kb("Count the marks.", WALL, CRAT))
bloco("B18c",
      kb("Every one of them is a few seconds", WALL, CHIPS),
      kb("kept for eighty-five years", FLAGNOW, "zoom-in"),
      num("Here's my question for you.", "?", "CLOSED AND WORKING, OR OPEN TO THE PUBLIC?"))
bloco("B18d",
      kb("Should places like this stay closed", WALL, "pan-dir"),
      card("This is Clearance Required."))

CENAS = []   # nenhuma imagem IA no corpo (a thumb fica em thumbs/)


# ===================================================================== validação
def palavras(t):
    return len(t.split())


def norm(t):
    t = t.replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[^a-z0-9 ]", "", t.lower().replace("-", " ")).split().__str__()


def fmt(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def voz(t):
    return t


def main():
    ERROS, AVISOS = [], []
    csvm = {}
    with open(AQUI / "midia.csv", newline="") as f:
        for r in csv.DictReader(f):
            csvm[r["arquivo"]] = r
    # 0. narração = SCRIPT.md
    s = (AQUI / "SCRIPT.md").read_text()
    paras = {m.group(1): m.group(2).strip() for m in re.finditer(r"^### (B\d\d) .*\n(.+)$", s, re.M)}
    junto = {}
    for b in B:
        junto.setdefault(b["id"][:3], []).append(b["texto"])
    for k, t in paras.items():
        if " ".join(junto.get(k, [])) != t:
            ERROS.append(f"{k}: narração dos blocos ≠ SCRIPT.md (rode tools/split_blocos.py)")
    faltam = set(SPLIT) - {b["id"] for b in B}
    if faltam:
        ERROS.append(f"blocos sem planos: {sorted(faltam)}")

    # 1. tempos estimados
    planos, t = [], 0.0
    for b in B:
        texto = b["texto"]
        pos, ini = [], 0
        for p in b["planos"]:
            i = texto.find(p["em"], ini)
            if i < 0:
                ERROS.append(f"{b['id']}: âncora não encontrada (ou fora de ordem): «{p['em']}»")
                i = ini
            pos.append(i)
            ini = i + 1
        if pos and pos[0] != 0:
            ERROS.append(f"{b['id']}: o 1º plano precisa começar no início do bloco")
        b["inicio"], b["dur"] = round(t, 2), round(palavras(texto) / WPS, 2)
        for k, p in enumerate(b["planos"]):
            fim = pos[k + 1] if k + 1 < len(pos) else len(texto)
            frase = texto[pos[k]:fim].strip()
            d = palavras(frase) / WPS
            q = dict(p)
            q.update(bloco=b["id"], frase=frase, inicio=round(t, 2), dur=round(d, 2))
            planos.append(q)
            t += d
    total = t

    # 2. arquivos, fichas, grifo literal, KenBurns com movimento
    for q in planos:
        for arq in [q["arq"], q.get("arq2")]:
            if not arq or arq == "codigo":
                continue
            if not (MIDIA / arq).exists():
                ERROS.append(f"{q['bloco']}: arquivo inexistente em midia/: {arq}")
            if arq not in csvm:
                ERROS.append(f"{q['bloco']}: arquivo fora do midia.csv: {arq}")
            if arq.startswith(("foto_", "hoje_")) and arq not in FICHAS:
                ERROS.append(f"{q['bloco']}: foto sem Ficha: {arq}")
        if q["tipo"] == "KenBurns":
            if tuple(q["de"]) == tuple(q["para"]):
                ERROS.append(f"{q['bloco']}: KenBurns parado ({q['arq']})")
            if q["dur"] > 8.5:
                AVISOS.append(f"{q['bloco']}: KenBurns longo ({q['dur']:.1f} s) em {q['arq']}")
            q["ficha"] = q.get("ficha") or FICHAS.get(q["arq"])
        if q["tipo"] in ("DocGrifo",):
            q["ficha"] = q.get("ficha") or FICHAS.get(q["arq"])
            if q["literal"] and norm(q["frase_doc"])[1:-1] not in norm(q["frase"])[1:-1]:
                ERROS.append(f"{q['bloco']}: grifo literal «{q['frase_doc']}» não é lido na narração do plano «{q['frase'][:60]}»")
        if q["tipo"] == "Dupla":
            q["ficha"] = FICHAS.get(q["arq"])
            q["ficha2"] = FICHAS.get(q["arq2"])
        if q["tipo"] == "Filme":
            q["ficha"] = FICHAS.get(q["arq"])
            seg = (q["tout"] - q["tin"]) / q["vel"]
            if seg + 0.15 < q["dur"]:
                ERROS.append(f"{q['bloco']}: trecho do filme curto ({seg:.1f} s) para {q['dur']:.1f} s de narração ({q['arq']} {q['tin']}–{q['tout']})")
            if q["dur"] > FILME_MAX + 0.5:
                AVISOS.append(f"{q['bloco']}: plano de filme com {q['dur']:.1f} s (> {FILME_MAX} s): o build.py corta/acelera")
            if q["tout"] > DUR_FILME.get(q["arq"], 0):
                ERROS.append(f"{q['bloco']}: trecho além do fim do filme {q['arq']}")

    # 3. tipo de tela: no máximo RUN_MAX s seguidos (tempos reais em qa/tempos.json, gravado pelo build.py da etapa 2)
    reais = {}
    if (AQUI / "qa/tempos.json").exists():
        reais = {(x["bloco"], x["em"]): x["d"] for x in json.load(open(AQUI / "qa/tempos.json"))}
    run_t, run_tipo, run_ini = 0.0, None, None
    for q in planos:
        d = reais.get((q["bloco"], q["em"]), q["dur"])
        if q["tipo"] == run_tipo:
            run_t += d
        else:
            run_tipo, run_t, run_ini = q["tipo"], d, q
        lim = RUN_MAX_FOTO if run_tipo in ("KenBurns", "Dupla", "DocGrifo", "Filme") else RUN_MAX
        if run_t > lim + (1.0 if reais else 0) + 1e-6:
            ERROS.append(f"{q['bloco']}: {run_tipo} por {run_t:.1f} s seguidos (desde {run_ini['bloco']} «{run_ini['em']}»); máximo {lim:.0f} s")

    # 4. reuso
    vistos, ult_enq = {}, {}
    ant_arq = None
    reuso_t = 0.0
    for q in planos:
        arqs = [a for a in [q["arq"], q.get("arq2")] if a and a != "codigo"]
        q["reuso"] = False
        for arq in arqs:
            chave = (arq, q["enq"])
            if chave in ult_enq and q["inicio"] - ult_enq[chave] < JANELA and ant_arq != arq:
                AVISOS.append(f"{q['bloco']}: {arq} [{q['enq']}] repetido em menos de {JANELA:.0f} s")
            if arq in vistos and ant_arq != arq:
                q["reuso"] = True
                if q["inicio"] < INEDITO_ATE and arq not in REUSO_LIBERADO:
                    AVISOS.append(f"{q['bloco']}: reuso de {arq} antes de 3:00 ({fmt(q['inicio'])})")
            vistos.setdefault(arq, q["inicio"])
            ult_enq[chave] = q["inicio"] + q["dur"]
        if q["reuso"]:
            reuso_t += q["dur"]
        ant_arq = arqs[-1] if arqs else None

    # 5. checklist
    REAL = {"KenBurns", "DocGrifo", "EntaoAgora", "Dupla", "Filme"}
    real_t = sum(q["dur"] for q in planos if q["tipo"] in REAL or (q["tipo"] == "Mapa2D" and q["arq"] != "codigo"))
    docs = sorted({q["arq"] for q in planos if q["tipo"] == "DocGrifo"})
    docs_grifo = sorted({q["arq"] for q in planos if q["tipo"] == "DocGrifo" and q["grifo"]})
    lidos = sorted({(q["arq"], q["frase_doc"]) for q in planos if q["tipo"] == "DocGrifo" and q["literal"]})
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

    # 6. fidelidade (aviso): nomes citados × arquivo
    NOMES = {"Utah": ["utah"], "Hangar 79": ["hangar79"], "flag": ["bandeira", "staff", "flagnow"], "Ford Island": ["ford"],
             "Swanson": ["swanson", "cerimonia", "quartel", "bandeira", "cartela"], "Arizona": ["arizona"]}
    for q in planos:
        alvo = (q["arq"] + " " + str(q.get("arq2")) + " " + q["enq"]).lower()
        for nome, oks in NOMES.items():
            if oks and nome in q["frase"] and not any(o in alvo for o in oks):
                AVISOS.append(f"fidelidade? {q['bloco']} cita {nome} sobre {q['arq']}: «{q['frase'][:60]}»")

    for i, q in enumerate(planos, 1):
        q["id"] = f"P{i:03d}"
        q["real"] = q["tipo"] in REAL
    stats = dict(planos=len(planos), duracao_s=round(total, 1), duracao=fmt(total), planos_por_min=round(len(planos) / (total / 60), 1),
                 real_pct=round(100 * frac_real, 1), reuso_pct=round(100 * reuso_t / total, 1),
                 componentes=cont, docs_distintos=len(docs), docs_grifados=len(docs_grifo), citacoes_literais=len(lidos), numeros=n_num,
                 mapas_distintos=len(mapas), entao_agora=n_ea, imagens_ia=len(CENAS), palavras=sum(palavras(b["texto"]) for b in B),
                 blocos_audio=len(B))
    blocos = [dict(id=b["id"], texto=b["texto"], texto_voz=voz(b["texto"]), ideia=b["ideia"],
                   inicio_est=b["inicio"], dur_est=b["dur"]) for b in B]
    chaves = ["id", "bloco", "tipo", "arq", "arq2", "enq", "inicio", "dur", "frase", "real", "reuso", "ficha", "ficha2", "num", "de", "para",
              "crop", "regiao", "frase_doc", "grifo", "literal", "valor", "rotulo", "nome", "pontos", "linhas", "selo", "nota",
              "rot1", "rot2", "em"]
    sb = [{k: q[k] for k in chaves if k in q and q[k] is not None} for q in planos]
    (AQUI / "blocos.json").write_text(json.dumps(blocos, ensure_ascii=False, indent=1) + "\n")
    (AQUI / "storyboard.json").write_text(json.dumps(dict(stats=stats, pontos=P, planos=sb), ensure_ascii=False, indent=1) + "\n")
    (AQUI / "cenas.json").write_text(json.dumps(CENAS, ensure_ascii=False, indent=1) + "\n")

    L = ["# STORYBOARD: 004-pearl-harbor (lugares-guerra-en, \"Clearance Required\")", "",
         "Gerado por `roteiro.py` (não editar à mão). Tempos estimados a 168 ppm (voz Narrator); recalcular com o áudio real no `build.py` da etapa 2.",
         f"**{stats['planos']} planos · {stats['duracao']} · {stats['planos_por_min']} planos/min · material real {stats['real_pct']}% · "
         f"reuso {stats['reuso_pct']}% · imagens IA {len(CENAS)}**", "",
         "Componentes: " + ", ".join(f"{k} {v}" for k, v in sorted(cont.items())) +
         f" · docs distintos {len(docs)} (grifados {len(docs_grifo)}, citações lidas literalmente {len(lidos)}) · Números {n_num} · mapas {len(mapas)} · EntaoAgora {n_ea}", ""]
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
    fx = f" · Ficha: {f[0]}" if f else ""
    nm = f" · Número «{q['num'][0]} {q['num'][1]}»" if q.get("num") else ""
    if t == "KenBurns":
        return f"`{q['arq']}` {q['enq']} {tuple(q['de'])}→{tuple(q['para'])}{' crop ' + str(q['crop']) if q.get('crop') else ''}{fx}{nm}"
    if t == "DocGrifo":
        g = f"grifo «{q['frase_doc']}»" if q.get("frase_doc") else ("página/zoom" if not q["grifo"] else "grifo")
        return f"`{q['arq']}` [{q['enq']}] {g}{'' if q['literal'] else ' (não literal)'}{fx}{nm}"
    if t == "Dupla":
        return f"`{q['arq']}` «{q['rot1']}» | `{q['arq2']}` «{q['rot2']}»{' · Selo ' + q['selo'] if q.get('selo') else ''}{nm}"
    if t == "Número":
        return f"código: **{q['valor']}** {q['rotulo']}"
    if t == "Mapa2D":
        base = f" · base `{q['arq']}`" if q["arq"] != "codigo" else ""
        return f"mapa {q['nome']} ({', '.join(q['pontos'])}){base}{' · Selo ' + q['selo'] if q.get('selo') else ''}{' · ' + q['nota'] if q.get('nota') else ''}"
    if t == "Cartela":
        return f"código: cartela «{' / '.join(q['linhas'])}»{' · Selo ' + q['selo'] if q.get('selo') else ''}"
    if t == "EntaoAgora":
        return f"`{q['arq']}` ({q['rot1']}) × `{q['arq2']}` ({q['rot2']}){nm}"
    if t == "Card":
        return "código: cartela final do canal (Clearance Required + inscrever)"
    return ""


if __name__ == "__main__":
    main()
