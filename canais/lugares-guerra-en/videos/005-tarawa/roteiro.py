#!/usr/bin/env python3
"""Fonte do storyboard do lugares-guerra-en 005 "Why Is America Digging Up Japanese Soldiers on Tarawa?" (youtube.videos id 46).
Uso: cd <pasta do vídeo> && python3 roteiro.py   (python3 puro)
O roteiro FINAL é o SCRIPT.md (fatos em FATOS.md/SOURCES.md). Blocos de áudio: tools/split_blocos.py (qa/split_blocos.json + blocos-voz.json).
Define os planos visuais e valida (regras do 004): narração = SCRIPT.md, arquivos no midia.csv, Ficha em toda foto, tipo de tela ≤ 12 s
(foto/doc/filme ≤ 14 s), reuso, grifo literal, ≥ 85% material real. Gera blocos.json, storyboard.json, STORYBOARD.md, cenas.json (vazio).
Código base: 004-pearl-harbor/roteiro.py. Regra do brief: NADA de corpo/ossada/restos na tela (escavação só terra/peneira/equipe; caixas fechadas).
Grifos: posição EXATA do texto extraída dos PDFs (tools/docs_pos.json, PyMuPDF), não estimada.
Mapas 2D: Natural Earth 50m (copiar midia/mapa_base_ne50m_land.geojson do 004 na etapa 2; mapas pacifico/volta/nagasaki em escala oceânica).
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
REUSO_LIBERADO = {"hoje_criancas_praia_betio_5603928.jpg", "doc_dpmo_factsheet_p1.png", "doc_taylor2019_p10_dna.png", "doc_dpaa_tarawa_casualties.png", "hoje_escavacao_sitio_ajoelhados_5589359.jpg"}
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



# Grifos (x, y, largura, altura) em fração da página: posição EXATA extraída do PDF (tools/docs_pos.json), com margem.
def gp(*bs):
    return [px([b[0] - 4, b[1] - 3, b[2] + 8, b[3] + 6], 612, 792) for b in bs]
G = {
    "pagina": [],
    "craters": gp((454, 302, 70, 12), (108, 315, 131, 13)),
    "seabee": gp((188, 399, 116, 12)),
    "kept": gp((263, 443, 256, 13), (108, 456, 107, 13)),
    "r31": gp((242, 117, 102, 13)),
    "r17": gp((402, 188, 83, 13)),
    "little": gp((446, 420, 75, 13), (64, 433, 162, 14)),
    "only146": gp((337, 447, 169, 13), (64, 460, 41, 14)),
    "rest": gp((111, 460, 163, 14)),
    "g4836": gp((467, 204, 27, 13)),
    "g129": gp((431, 249, 18, 13)),
    "g4690": gp((467, 316, 27, 14)),
    "dna124": gp((206, 347, 80, 13), (141, 366, 101, 14)),
    "houses": gp((144, 287, 186, 13)),
    "d374": gp((134, 447, 17, 11)),
    "commingled": gp((84, 493, 55, 11)),
}

# Pontos de mapa (lon E 0–360, lat).
P = {"BETIO (TARAWA)": (172.93, 1.35), "HONOLULU": (202.14, 21.31), "NAGASAKI": (129.87, 32.75), "SEOUL": (126.98, 37.57),
     "TOKYO": (139.69, 35.69), "SASEBO": (129.72, 33.18), "KOREA": (127.5, 36.5)}

B = []
SPLIT = {b["id"]: b["texto"] for b in json.load(open(AQUI / "qa/split_blocos.json"))}


def bloco(bid, *planos, ideia=False):
    B.append(dict(id=bid, texto=SPLIT[bid], ideia=ideia, planos=list(planos)))


# Arquivos
DPMO1, DPMO2 = "doc_dpmo_factsheet_p1.png", "doc_dpmo_factsheet_p2.png"
ST5, STC = "doc_stock1947_cap5.png", "doc_stock1947_apendice_c.png"
TY10, TY5, DPAA = "doc_taylor2019_p10_dna.png", "doc_taylor2019_p5_casas.png", "doc_dpaa_tarawa_casualties.png"
REEF48 = "doc_across_the_reef_p48_seabees_valas_foto_legenda.png"
MAPA43 = "mapa_betio_intelligence_map_2dmardiv_1943.png"
PENEIRA, AJOELH, HFLIGHT = "hoje_escavacao_equipe_peneira_5589355.jpg", "hoje_escavacao_sitio_ajoelhados_5589359.jpg", "hoje_escavacao_dpaa_history_flight_5589362.jpg"
CAIXAS, CRIANCAS, ISS = "hoje_caixas_transferencia_prateleira_5589365.jpg", "hoje_criancas_praia_betio_5603928.jpg", "hoje_atol_tarawa_iss_2017.jpg"
BUNK_V, BUNK_M, BATERIA = "hoje_bunker_japones_visita_5589369.jpg", "hoje_bunker_japones_vista_mar_5589372.jpg", "hoje_bateria_costeira_14cm_2019.jpg"
REP_PISTA, REP_C17, REP_FOCO = "hoje_repatriacao_caixa_bandeira_pista_5589325.jpg", "hoje_repatriacao_c17_guarda_5589326.jpg", "hoje_repatriacao_bandeira_foco_5589328.jpg"
REP_CAB, REP_SOL, REP_CONT = "hoje_repatriacao_cabecas_baixas_5589332.jpg", "hoje_repatriacao_salvas_por_do_sol_5589324.jpg", "hoje_repatriacao_continencia_5793634.jpg"
A80_EMB, A80_PRES, A80_JAP = "hoje_80anos_embaixadora_discurso_8142539.jpg", "hoje_80anos_presidente_kiribati_8142541.jpg", "hoje_80anos_japao_coroa_memorial_8142550.jpg"
A80_COROA, A80_GRUPO, A80_PREP = "hoje_80anos_coroa_embaixadora_memorial_8142551.jpg", "hoje_80anos_foto_grupo_memorial_8142559.jpg", "hoje_80anos_guarda_prepara_caixa_8142545.jpg"
A80_CARR, A80_C17 = "hoje_80anos_guarda_carrega_caixa_8142549.jpg", "hoje_80anos_embarque_c17_8142560.jpg"
CRUZES, BUNKER43, CAMUF = "foto_cruzes_cemiterio_betio_1943.jpg", "foto_bunker_aterrado_80g57356.jpg", "foto_posicao_camuflada_80g57435.jpg"
PRIS1, PRIS2, PRIS3 = "foto_prisioneiros_japoneses_praia.jpg", "foto_prisioneiros_nara532519.jpg", "foto_prisioneiros_arame_farpado_dpla.jpg"
CANHAO43, AEREA44, TENDAS = "foto_canhao_14cm_fuzileiro_1943.jpg", "foto_aerea_hawkins_field_1944.jpg", "foto_acampamento_tendas_betio.jpg"
F_MAQ, F_FUMACA, F_LANCHAS = "filme_maquete_betio_briefing_navio_nara77026.mp4", "filme_fumaca_sobre_betio_do_mar_nara77026.mp4", "filme_aproximacao_lanchas_fumaca_betio_nara77026.mp4"
F_RECIFE, F_CAMINHAM, F_AVIAO = "filme_lanchas_recife_nara77026.mp4", "filme_fuzileiros_caminham_pista_nara77026.mp4", "filme_aviao_destruido_carro_enterrado_nara77026.mp4"
F_PISTA, F_CANHAO, F_CRUZ = "filme_aerodromo_rolo_holofote_nara77026.mp4", "filme_canhao_destruido_betio_nara77026.mp4", "filme_cruzador_dispara_alvo_nara75861.mp4"
F_PRIS, F_DEFESAS, F_CASAMATA = "filme_prisioneiros_sentados_nara75866.mp4", "filme_defesas_praia_arame_nara75866.mp4", "filme_canhao_casamata_interior_nara75866.mp4"
F_PIER = "filme_barcos_e_pier_nara75866.mp4"
VOLTA = ["BETIO (TARAWA)", "HONOLULU", "NAGASAKI"]

# ===================================================================== planos
# ===== Bloco 1: hook (o número do laboratório + o papel)
bloco("B01a",
      doc("Here is a number from a Defense Department laboratory", TY10, "pagina", G["pagina"]),
      num("Two hundred forty-three.", "243", "DISTINCT DNA PROFILES · THE TARAWA PROJECT"),
      kb("That's how many distinct DNA profiles", CAIXAS, "zoom-in"),
      kb("Now the other number.", PENEIRA, "pan-dir"),
      ideia=True)
bloco("B01b",
      doc("One hundred twenty-four of them", TY10, "dna124", G["dna124"], literal=False),
      num("Hold on to that number:", "124", "OF 243 · ASIAN LINEAGES"),
      kb("The island is Betio,", ISS, "zoom-in"),
      doc("And this is a page from", DPMO1, "pagina", G["pagina"]))
bloco("B01c",
      doc("It says the enemy dead", DPMO1, "craters", G["craters"], frase="buried in bomb craters and existing trenches"),
      num("So why is America digging up", "?", "WHY IS AMERICA DIGGING UP JAPANESE SOLDIERS ON TARAWA?"))

# ===== Bloco 2: âncora humana + a pergunta
bloco("B02a",
      kb("It isn't a mistake.", AJOELH, "zoom-in"),
      kb("And it isn't new.", CRUZES, "pan-esq"),
      mapa("In February 2021,", "volta", VOLTA, [("BETIO (TARAWA)", "HONOLULU", ""), ("HONOLULU", "NAGASAKI", "2021")], selo="SCHEMATIC"),
      cartela("a man named Sadayuki Nomura", ["SADAYUKI NOMURA", "NAGASAKI AIRPORT · FEB 26, 2021"], selo="RECORD"),
      ideia=True)
bloco("B02b",
      kb("He was ninety-two.", REP_FOCO, "detalhe:0.5,0.4", num=("92", "SADAYUKI NOMURA")),
      kb("His brother, Masatoshi,", CAMUF, "zoom-in"),
      filme("He was twenty-three", F_FUMACA, 0.5, 7.0, num=("NOV 1943", "TARAWA")))
bloco("B02c",
      kb("He had been found in 2013,", HFLIGHT, "zoom-in"),
      kb("The Americans were searching", REP_PISTA, "pan-dir"))
bloco("B02d",
      filme("Along the way, you'll see who", F_PRIS, 0.5, 6.5),
      doc("the papers that explain", ST5, "pagina", G["pagina"]),
      kb("and what is still under the town", CRIANCAS, "zoom-in"))

# ===== a ilha hoje
bloco("B03a",
      kb("Tarawa isn't closed.", BUNK_V, "pan-dir"),
      mapa("Betio, in the Republic of Kiribati,", "pacifico", ["BETIO (TARAWA)", "HONOLULU", "TOKYO"], [], selo=None),
      kb("about eighteen thousand people", CRIANCAS, "pan-esq", num=("18,000", "PEOPLE ON BETIO · LESS THAN 2 KM²")),
      kb("What you can't visit", AJOELH, "detalhe:0.5,0.6"),
      ideia=True)
bloco("B03b",
      doc("The Defense POW/MIA Accounting Agency says", DPAA, "pagina", G["pagina"]),
      doc("about 374 Americans", DPAA, "d374", G["d374"], frase="374"),
      kb("That's the number every news story", REP_FOCO, "zoom-in"),
      doc("But the agency's own page", DPAA, "commingled", G["commingled"], frase="commingled"))
bloco("B03c",
      kb("Commingled.", AJOELH, "detalhe:0.4,0.6", num=("COMMINGLED", "MIXED TOGETHER")),
      doc("And on the other side of the ledger,", STC, "g4836", G["g4836"], literal=False),
      kb("They're in the thousands.", BUNKER43, "zoom-in", num=("4,690", "JAPANESE & KOREAN · USMC, 1947")))
bloco("B03d",
      kb("Visitors do come.", BATERIA, "pan-esq"),
      kb("They photograph", BUNK_M, "zoom-in"),
      kb("Very few of them", CRIANCAS, "detalhe:0.4,0.65"))

# ===== Bloco 3: o que aconteceu ali
bloco("B04a",
      filme("To understand how that happened,", F_MAQ, 0.5, 7.0),
      mapa("In September 1942,", "pacifico", ["TOKYO", "BETIO (TARAWA)"], [("TOKYO", "BETIO (TARAWA)", "SEPT 1942")], selo=None),
      kb("In December, a pioneer unit", "foto_general_bunker_80g57391.jpg", "zoom-in"),
      kb("Concrete bunkers.", BUNKER43, "detalhe:0.5,0.45"),
      ideia=True)
bloco("B04b",
      kb("Coconut-log walls.", CAMUF, "pan-dir"),
      filme("Big coastal guns", F_CASAMATA, 0.5, 5.5),
      kb("The island is shaped", MAPA43, "zoom-in"),
      kb("It's about three hundred acres", AEREA44, "zoom-in", num=("300", "ACRES OF SAND · BETIO, 1943")))
bloco("B04c",
      filme("And the people who did much", F_PRIS, 7.0, 13.0),
      kb("The Accounting Agency says", PRIS3, "zoom-in"))
bloco("B04d",
      filme("In other words,", F_DEFESAS, 0.5, 10.0))
bloco("B05a",
      cartela("The Accounting Agency puts it this way.", ["\"MORE THAN 2,500 JAPANESE SOLDIERS DEFENDED IT, ALONG WITH SOME 1,000 JAPANESE CONSTRUCTION WORKERS AND 1,200 KOREAN FORCED LABORERS.\"", "— DPAA, THE BATTLE OF TARAWA"], selo="QUOTED"),
      kb("Korea was a Japanese colony then.", PRIS3, "pan-esq", num=("1,200", "KOREAN FORCED LABORERS")),
      kb("Men were taken from farms", PRIS2, "pan-esq"))
bloco("B05b",
      doc("On November 20th, 1943,", STC, "pagina", G["pagina"]),
      kb("When the fighting stopped,", PRIS1, "zoom-in"),
      doc("Seventeen Japanese.", STC, "g129", G["g129"], frase="129"),
      num("Remember that number, too:", "129", "KOREAN LABORERS WALKED OFF ALIVE"))
bloco("B06a",
      filme("The landing was supposed to be quick.", F_CRUZ, 0.5, 6.5),
      filme("The tide was lower", F_RECIFE, 0.5, 7.0),
      filme("Marines waded", F_LANCHAS, 0.5, 7.0),
      kb("It took seventy-six hours", "foto_fuzileiros_invadem_nara532517.jpg", "pan-dir", num=("76", "HOURS")),
      ideia=True)
bloco("B06b",
      kb("More than a thousand Americans", "foto_fuzileiros_invadem_nara532517.jpg", "zoom-in"),
      kb("The Marine Corps' casualty division", CRUZES, "detalhe:0.4,0.5", num=("3,301", "MARINE CASUALTIES · USMC, 1947")),
      filme("The Japanese commander,", F_CANHAO, 0.5, 6.5))
bloco("B06c",
      doc("The Marine Corps' official history,", ST5, "pagina", G["pagina"]),
      cartela("The division, it said,", ["\"…ANNIHILATED ALL BUT 146 OF THE ENEMY'S 4,836 MEN.\"", "— THE BATTLE FOR TARAWA, USMC, 1947"], selo="QUOTED"),
      doc("On paper, that's 4,690 men.", STC, "g4690", G["g4690"], frase="4,690"),
      kb("On about three hundred acres.", AEREA44, "zoom-out"))
bloco("B07a",
      kb("Put the two sides together", AEREA44, "pan-esq", num=("~6,000", "MEN, BOTH SIDES · ABOUT 300 ACRES")),
      filme("In that heat,", F_CAMINHAM, 0.5, 6.5),
      kb("A Marine artilleryman,", "foto_fuzileiros_municao_80g57359.jpg", "zoom-in"),
      ideia=True)
bloco("B07b",
      cartela("\"Within a very short period,", ["\"…THE ONLY WAY WE COULD TELL A MARINE FROM A JAPANESE WAS BY THE WEB GEAR THAT WE WERE WEARING AND BY THE ARMAMENT THAT THE MAN HAD.\"", "— ROGER SCOVILL, 10TH MARINES (VIA G. ROECKER)"], selo="QUOTED"),
      kb("the only way we could tell", "foto_fuzileiros_municao_80g57359.jpg", "detalhe:0.5,0.4"),
      kb("That sentence is the whole story", "foto_sherman_tripulacao_80g57422.jpg", "pan-dir"))
bloco("B07c",
      kb("The Marines buried their own", CRUZES, "zoom-in"),
      kb("The other side was a different problem.", BUNKER43, "detalhe:0.3,0.55"))

# ===== Bloco 4: a virada (o papel)
bloco("B08a",
      kb("The 1947 history is honest about it.", "foto_coronel_latas_80g57394.jpg", "zoom-in"),
      doc("\"Although every effort was made", ST5, "little", G["little"], frase="little or nothing could be done for the enemy dead"),
      kb("It goes on.", PRIS1, "zoom-out"),
      ideia=True)
bloco("B08b",
      doc("The rest lay where they had fallen.", ST5, "rest", G["rest"], frase="The rest lay where they had fallen"),
      kb("So the Marine dead went into trenches", "foto_escavadeira_seabees_80g57390.jpg", "zoom-in"),
      doc("And the Pentagon's fact sheet gives the rest.", DPMO1, "craters", G["craters"], frase="buried in bomb craters and existing trenches"))
bloco("B08c",
      kb("No names.", BUNKER43, "detalhe:0.6,0.4", num=("NO NAMES", "NO MARKERS")),
      kb("In many places,", AJOELH, "pan-esq"),
      kb("A Navy inspector", TENDAS, "zoom-in"))
bloco("B08d",
      cartela("\"There was no time", ["\"THERE WAS NO TIME TO PROPERLY BURY THE DEAD. SUCH IS WAR.\"", "— NAVY INSPECTOR, 1947 (VIA G. ROECKER)"], selo="QUOTED"),
      kb("Roecker also notes", TENDAS, "detalhe:0.5,0.5", num=("5 : 1", "JAPANESE & KOREAN TO AMERICAN")),
      filme("But the strangest part", F_FUMACA, 8.0, 14.5))
bloco("B09a",
      filme("Within days,", F_PISTA, 0.5, 6.5),
      kb("Navy construction battalions,", "foto_pista_escavadeiras_80g57388.jpg", "pan-dir"),
      doc("The fact sheet is blunt", DPMO1, "seabee", G["seabee"], frase="at least five SeaBee units"),
      ideia=True)
bloco("B09b",
      kb("They moved graves and markers", "foto_hawkins_field_b24_nativos_41bg.jpg", "zoom-in"),
      doc("And then this line.", DPMO1, "kept", G["kept"], frase="we suspect none were kept"),
      kb("In 1946, an Army graves registration", CRUZES, "detalhe:0.6,0.4"))
bloco("B09c",
      kb("By its own count,", CRUZES, "zoom-out", num=("~50%", "OF THE AMERICAN GRAVES FOUND · 1946")),
      kb("And one of its first unknowns", CAIXAS, "detalhe:0.5,0.5"))
bloco("B10a",
      kb("X-1 was Betio's first unknown soldier,", REP_CAB, "zoom-in", num=("X-1", "BETIO'S FIRST UNKNOWN")),
      kb("Later laboratory work", PENEIRA, "zoom-out"),
      kb("He was almost certainly a Japanese", PRIS1, "pan-dir", num=("X-1", "ALMOST CERTAINLY JAPANESE OR KOREAN")))
bloco("B10b",
      kb("The graves teams set aside", TENDAS, "pan-dir"),
      filme("But on an island where", F_AVIAO, 0.5, 9.0))
bloco("B10c",
      kb("By 1947, the remains", REP_C17, "zoom-in"),
      kb("Hundreds were named.", REP_PISTA, "zoom-out", num=("465", "IDENTIFIED AFTER 1946 · DPMO")),
      kb("The rest were buried as unknowns,", REP_CAB, "pan-esq"),
      kb("And the other side?", BUNKER43, "zoom-out"))
bloco("B10d",
      filme("Most of it never left the island.", F_DEFESAS, 6.0, 12.0),
      doc("In 1949, someone even proposed", DPMO1, "pagina", G["pagina"]),
      kb("Even on paper,", REP_SOL, "zoom-in"))
bloco("B11a",
      doc("The fact sheet has a second page,", DPMO2, "pagina", G["pagina"]),
      kb("In 1978, several sets", BUNK_V, "detalhe:0.5,0.5", num=("1978", "MIXED REMAINS TURNED OVER FROM TARAWA")),
      kb("And then the line.", BUNK_M, "pan-dir"),
      ideia=True)
bloco("B11b",
      doc("\"31 comingled remains", DPMO2, "r31", G["r31"], frase="31 comingled remains"),
      doc("Two years later,", DPMO2, "r17", G["r17"], frase="17 sets of remains"),
      kb("In 2000, locals building a driveway", BUNK_V, "zoom-in"))
bloco("B11c",
      kb("In 2004, a Peace Corps volunteer", CRIANCAS, "detalhe:0.3,0.5", num=("2004", "TURNED OVER BY A PEACE CORPS VOLUNTEER")),
      doc("The same page ends with a table", DPMO2, "pagina", G["pagina"]))
bloco("B11d",
      num("The others just say UNKNOWN,", "UNKNOWN", "— — —"),
      kb("Every time someone on Betio", CRIANCAS, "pan-dir"))

# ===== Bloco 5: o que ainda está lá
bloco("B12a",
      kb("Then came the searches", HFLIGHT, "pan-esq"),
      kb("In 2009, a Pentagon team", PENEIRA, "pan-esq", num=("6+", "\"OF UNKNOWN NATIONAL ORIGIN\" · 2009")),
      doc("Its own fact sheet calls them", DPMO2, "pagina", G["pagina"]),
      ideia=True)
bloco("B12b",
      kb("A year later,", AJOELH, "zoom-in"),
      cartela("According to the Associated Press,", ["\"THEY UNEARTHED INSTEAD A MASS GRAVE OF JAPANESE SOLDIERS … ALONG WITH A FORGOTTEN LOCAL CEMETERY.\"", "— ASSOCIATED PRESS, NOV 2010"], selo="QUOTED"))
bloco("B12c",
      kb("Those remains were handed", A80_PRES, "zoom-in"),
      kb("Because there aren't only two sides", A80_GRUPO, "zoom-out", num=("4", "U.S. · JAPAN · KOREA · KIRIBATI")),
      doc("The agency's scientists list", TY5, "pagina", G["pagina"]))
bloco("B13a",
      filme("There's one more reason", F_CAMINHAM, 7.0, 13.5),
      kb("In 2008,", PENEIRA, "detalhe:0.45,0.55"),
      kb("In November 2013,", HFLIGHT, "detalhe:0.5,0.5"),
      ideia=True)
bloco("B13b",
      num("Inside were five sets of remains.", "4 + 1", "JAPANESE + AMERICAN · ONE FIGHTING POSITION, 2013"),
      cartela("One was a nineteen-year-old", ["PFC RANDOLPH ALLEN", "19 · RUSH, KENTUCKY · IDENTIFIED BY HIS TWO DOG TAGS"], selo="DoD RELEASE 14-024"),
      num("Five men, two sides, one hole.", "1", "HOLE · 2 SIDES · 5 MEN"))
bloco("B13c",
      kb("In July 2014,", REP_CONT, "zoom-in"),
      kb("The other four had no tags at all.", CAIXAS, "pan-dir"))
bloco("B14a",
      kb("In 2016,", REP_CONT, "detalhe:0.5,0.4", num=("2016", "THE TARAWA PROJECT · DPAA")),
      kb("It dug up all ninety-four caskets", REP_C17, "detalhe:0.5,0.55", num=("94", "CASKETS OF TARAWA UNKNOWNS · HONOLULU")),
      kb("and brought them to the lab", CAIXAS, "zoom-out"),
      ideia=True)
bloco("B14b",
      doc("Its scientists then wrote a paper", TY10, "pagina", G["pagina"]),
      doc("Here is the sentence.", TY10, "dna124", G["dna124"], frase="124 of the 243"),
      num("There's the number from the beginning.", "124 / 243", "~50% ASIAN LINEAGES"))
bloco("B14c",
      kb("Half of those DNA profiles", A80_PREP, "zoom-in"),
      doc("And the paper notes why", TY5, "houses", G["houses"], frase="houses built on top of cemeteries"),
      kb("History Flight kept digging.", AJOELH, "pan-dir"))
bloco("B14d",
      kb("In 2019, it recovered", HFLIGHT, "pan-dir", num=("33", "SETS OF REMAINS · ONE TRENCH · 2019")),
      kb("By September 2022,", REP_SOL, "pan-esq", num=("160", "AMERICANS IDENTIFIED · SEP 2022")))
bloco("B15a",
      kb("How do you even begin to sort that?", CAIXAS, "detalhe:0.35,0.5"),
      kb("By the time of the paper,", PENEIRA, "detalhe:0.5,0.6", num=("~9,000", "ITEMS · ~6,000 FROM BETIO'S SAND")),
      doc("The scientists describe three tools.", TY10, "pagina", G["pagina"]),
      num("The first is teeth.", "1", "TEETH"),
      ideia=True)
bloco("B15b",
      kb("Dental work done in America", PENEIRA, "detalhe:0.6,0.45"),
      kb("The second is mitochondrial DNA,", CAIXAS, "detalhe:0.6,0.5", num=("2", "MITOCHONDRIAL DNA · THE MOTHER'S LINE")),
      num("The third is chemistry.", "3", "ISOTOPES"))
bloco("B15c",
      filme("Isotopes locked in the body", F_PIER, 0.5, 8.0),
      kb("and the paper says", ISS, "pan-dir"),
      kb("None of it gives a name by itself.", REP_FOCO, "zoom-out"),
      num("For a name, you need a relative.", "DNA", "FROM A LIVING RELATIVE"))
bloco("B16a",
      kb("So what do you do with half?", A80_JAP, "zoom-in"),
      kb("In 2019, the American government", A80_PREP, "pan-dir", num=("162", "ASIAN REMAINS SAMPLED · TO JAPAN AND KOREA")),
      mapa("In April 2020,", "volta", ["BETIO (TARAWA)", "TOKYO", "SEOUL"], [("BETIO (TARAWA)", "TOKYO", ""), ("BETIO (TARAWA)", "SEOUL", "")], selo="SCHEMATIC"),
      kb("Sixty-two families applied.", A80_COROA, "pan-esq", num=("62", "FAMILIES APPLIED IN JAPAN")),
      ideia=True)
bloco("B16b",
      mapa("One of them was a man in Nagasaki.", "nagasaki", ["NAGASAKI", "SASEBO", "TOKYO"], [], selo=None),
      cartela("In September 2020,", ["SEP 2020 · DNA MATCH", "MASATOSHI NOMURA ↔ HIS BROTHER SADAYUKI, 92"], selo="RECORD"),
      kb("The ministry announced it", A80_COROA, "zoom-in"),
      kb("Masatoshi Nomura came home", REP_SOL, "detalhe:0.5,0.5", num=("77", "YEARS LATER")))
bloco("B16c",
      kb("Japanese reports called it a first:", A80_JAP, "detalhe:0.5,0.45"),
      kb("The ministry's notice was careful.", A80_GRUPO, "pan-dir"),
      cartela("Because the remains had been left", ["\"…RESULTS MAY NOT MEET YOUR EXPECTATIONS.\"", "— JAPAN'S HEALTH MINISTRY, DNA PROGRAM FOR IWO JIMA AND TARAWA (TRANSLATED)"], selo="QUOTED"))
bloco("B17a",
      kb("Remember the 129 Koreans", PRIS2, "zoom-in"),
      kb("More than a thousand others didn't.", PRIS1, "detalhe:0.5,0.5", num=("1,000+", "KOREAN LABORERS WHO NEVER CAME BACK")),
      kb("Korean reports say a scientist", CAIXAS, "pan-esq"),
      ideia=True)
bloco("B17b",
      kb("Korean reports say the government", CAIXAS, "zoom-out", num=("184", "KOREAN RELATIVES GAVE DNA")),
      num("Among the remains was one", "No. 46", "TARAWA"),
      kb("In October 2019,", PENEIRA, "zoom-in"),
      cartela("His name was Choi Byeong-yeon.", ["CHOI BYEONG-YEON", "TAKEN TO TARAWA IN 1942 · AGE 24"], selo="RECORD"))
bloco("B17c",
      filme("He was twenty-four", F_PRIS, 13.0, 18.0),
      kb("He left a wife and two sons.", PRIS3, "pan-dir"),
      kb("Then the pandemic", ISS, "zoom-out"),
      kb("In December 2023, Choi came home.", REP_C17, "pan-dir", num=("DEC 2023", "CHOI BYEONG-YEON, HOME")))
bloco("B17d",
      kb("Korea's Interior Ministry", REP_SOL, "pan-dir"),
      kb("His sons were in their eighties.", A80_CARR, "detalhe:0.5,0.5", num=("80+", "HIS SONS' AGE")),
      mapa("In August 2024,", "volta", ["HONOLULU", "SEOUL", "BETIO (TARAWA)"], [("SEOUL", "HONOLULU", "MOU 2024")], selo="SCHEMATIC"))
bloco("B17e",
      num("Korea's government counts", "5,000+", "KOREANS MOBILIZED · NEVER CAME BACK FROM THE PACIFIC"))
bloco("B18a",
      kb("Today, Betio looks", CRIANCAS, "zoom-out"),
      kb("Tin roofs.", ISS, "detalhe:0.5,0.5"),
      ideia=True)
bloco("B18b",
      dupla("The Japanese coastal guns", BATERIA, BUNK_M, "JAPANESE GUN, 2019", "BUNKER, 2019"),
      kb("Some concrete bunkers still stand.", BUNK_V, "pan-esq"),
      ea("This gun was photographed in 1943.", CANHAO43, BATERIA, "1943", "2019"))
bloco("B18c",
      kb("In November 2023,", A80_EMB, "zoom-in"),
      kb("the President of Kiribati", A80_PRES, "pan-dir"),
      dupla("and a delegation from Japan", A80_JAP, A80_COROA, "JAPAN", "UNITED STATES"),
      kb("Afterward, Marines carried", A80_CARR, "zoom-in"),
      kb("The island is still giving", A80_C17, "pan-esq"))
bloco("B18d",
      kb("In 1978, the census", CRIANCAS, "pan-dir", num=("7,600 → 18,000", "PEOPLE ON BETIO · 1978 → 2020")),
      kb("Every new house needed", CRIANCAS, "detalhe:0.6,0.4"))
bloco("B19a",
      ea("In 1943, about six thousand men", AEREA44, ISS, "1944", "2017"),
      kb("So how many are still down there?", AJOELH, "zoom-out"),
      doc("On the American side,", DPAA, "d374", G["d374"], frase="374"),
      ideia=True)
bloco("B19b",
      kb("On the other side,", BUNKER43, "pan-dir"),
      doc("The Marine Corps counted 4,690", STC, "g4690", G["g4690"], frase="4,690"),
      doc("The old fact sheet says", DPMO1, "pagina", G["pagina"]),
      kb("Japan's own records say", A80_JAP, "detalhe:0.4,0.5", num=("~4,200", "JAPANESE RECORDS")))
bloco("B19c",
      kb("The agency's scientists now write", BUNK_M, "pan-esq", num=("6,000+", "JAPANESE & KOREAN · DPAA SCIENTISTS, 2019")),
      doc("Some came back in 1978,", DPMO2, "pagina", G["pagina"]),
      kb("Most never left.", BUNK_M, "zoom-out"),
      kb("They're under the roads,", ISS, "pan-esq"))
bloco("B19d",
      kb("The agency's last operation", HFLIGHT, "detalhe:0.5,0.6", num=("APR 2020", "LAST DPAA OPERATION ON TARAWA")),
      kb("In Tokyo,", A80_JAP, "pan-dir"),
      kb("The search isn't finished.", PENEIRA, "zoom-in"))

# ===== Bloco 6: fecho
bloco("B20a",
      kb("So why is America digging up", HFLIGHT, "zoom-out"),
      filme("Because in 1943,", F_FUMACA, 15.0, 22.0),
      doc("Because the men who came next", DPMO1, "kept", G["kept"], literal=False),
      ideia=True)
bloco("B20b",
      kb("And because the only way", AJOELH, "detalhe:0.55,0.5"),
      doc("and that ground holds all of them.", DPAA, "commingled", G["commingled"], literal=False),
      kb("And the labs that can tell", CAIXAS, "zoom-in"))
bloco("B20c",
      doc("Two hundred forty-three profiles.", TY10, "dna124", G["dna124"], literal=False),
      kb("Each one is someone's brother,", REP_CAB, "zoom-out"),
      kb("So here's my question for you.", A80_GRUPO, "zoom-in"))
bloco("B20d",
      kb("If your family were still waiting", REP_SOL, "zoom-out"),
      card("This is Clearance Required."))


# Quebra de sequência: KenBurns seguidos por > 11 s viram Dupla (a foto do plano + a foto anterior da sequência, rótulos da Ficha).
def _rot(arq):
    f = FICHAS.get(arq)
    return (f[0].split(" · ")[0] if f else "").upper()


def quebra_kenburns(lim=11.0):
    run, ant = 0.0, None
    for b in B:
        texto, pos, ini = b["texto"], [], 0
        for p in b["planos"]:
            i = texto.find(p["em"], ini); pos.append(max(i, ini)); ini = max(i, ini) + 1
        for k, p in enumerate(b["planos"]):
            fim = pos[k + 1] if k + 1 < len(pos) else len(texto)
            d = len(texto[pos[k]:fim].split()) / WPS
            if p["tipo"] == "KenBurns":
                if run + d > lim and ant and ant != p["arq"]:
                    nova = dupla(p["em"], p["arq"], ant, _rot(p["arq"]), _rot(ant), num=p.get("num"))
                    b["planos"][k] = nova
                    run, ant = 0.0, None
                    continue
                run += d; ant = p["arq"]
            else:
                run, ant = 0.0, None


quebra_kenburns()

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
    NOMES = {"Seabees": ["seabee", "escavadeira", "pista", "aerodromo", "dpmo", "hawkins"], "ambassador": ["embaixadora"], "President of Kiribati": ["presidente"], "coastal guns": ["canhao", "bateria", "casamata"]}
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
              "rot1", "rot2", "em", "tin", "tout", "vel"]
    sb = [{k: q[k] for k in chaves if k in q and q[k] is not None} for q in planos]
    (AQUI / "blocos.json").write_text(json.dumps(blocos, ensure_ascii=False, indent=1) + "\n")
    (AQUI / "storyboard.json").write_text(json.dumps(dict(stats=stats, pontos=P, planos=sb), ensure_ascii=False, indent=1) + "\n")
    (AQUI / "cenas.json").write_text(json.dumps(CENAS, ensure_ascii=False, indent=1) + "\n")

    L = ["# STORYBOARD: 005-tarawa (lugares-guerra-en, \"Clearance Required\")", "",
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
