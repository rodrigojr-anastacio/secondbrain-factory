#!/usr/bin/env python3
"""Fonte do storyboard do lugares-guerra-en 003 "The Gettysburg Photos You Weren't Supposed to See" (youtube.videos id 36).
Uso: cd <pasta do vídeo> && python3 roteiro.py   (python3 puro, sem dependências)

O roteiro FINAL é o SCRIPT.md (fatos em FATOS.md/SOURCES.md). Os blocos de áudio vêm de tools/split_blocos.py
(qa/split_blocos.json + blocos-voz.json). Este arquivo define os planos visuais de cada bloco e valida:
narração idêntica ao SCRIPT.md, arquivos no midia.csv, Ficha em toda foto, tipo de tela ≤ 12 s (KenBurns/Dupla ≤ 14 s:
DocGrifo ≤ 14 s quando são grifos sucessivos; cada plano é outro enquadramento, como os trechos de filme no 002), reuso, grifo literal, ≥ 85% material real.
Gera: blocos.json, storyboard.json, STORYBOARD.md, cenas.json (vazio: nenhuma imagem IA no corpo).
Código base: 002-bikini/roteiro.py (mesmo canal), sem Filme (Gettysburg 1863 não tem filme) e com o tipo novo "Dupla"
(duas fotos reais lado a lado com rótulo curto; componente a criar na etapa 2, ver ETAPA1-PRONTA.md).
Bíblia: canais/lugares-guerra-en/biblia/. Regra do brief: fotos de mortos sem close gráfico (nada de "detalhe:" em rosto).
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
REUSO_LIBERADO = {"foto_toca_gardner_1863.jpg"}   # a foto do hook volta de propósito (B01, B08, B18)
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


# Grifos (x, y, largura, altura) em pixels do arquivo; estimados à vista em 13/11/2026: CONFERIR nos stills da etapa 2.
SB = (4400, 3400)   # páginas do Sketch Book (doc_sketchbook_p*.jpg)
G = {
    "p41_titulo": [px([1350, 990, 1700, 150], *SB)],
    "p41_built": [px([1704, 1561, 1620, 58], *SB), px([638, 1624, 352, 58], *SB)],
    "p41_await": [px([746, 1817, 900, 58], *SB)],
    "p41_musket": [px([3105, 2081, 222, 58], *SB), px([638, 2145, 1980, 58], *SB)],
    "p40_fell": [px([1680, 1466, 1580, 55], *SB), px([555, 1529, 120, 55], *SB)],
    "p36_shoes": [px([3005, 1720, 215, 55], *SB), px([530, 1783, 765, 55], *SB)],
    "p36_treason": [px([680, 2038, 830, 55], *SB)],
    "p37_own": [px([725, 1953, 910, 55], *SB)],
    "nara_100": [px([1150, 3143, 115, 48], 1400, 3550), px([60, 3200, 895, 50], 1400, 3550)],
    "loc_prop": [px([880, 1612, 620, 50], 1900, 2600)],
    "loc_rearr": [px([135, 1168, 1675, 50], 1900, 1400)],
    "nps_unknown": [px([700, 4060, 490, 45], 1500, 4150)],
    "nps_1996": [px([100, 3860, 1000, 45], 1500, 4150)],
    "bliss_world": [],      # página do meio da cópia Bliss: grifo a marcar na etapa 2 (sem OCR aqui); por ora página/zoom
    "pagina": [],
}

# Pontos de mapa (lon E 0–360, lat). Mapa "campo" usa como base o mapa de Ditterline (1863, LoC): georreferenciar na etapa 2.
P = {"GETTYSBURG": (282.769, 39.831), "SEMINARY RIDGE": (282.756, 39.833), "McPHERSON'S WOODS": (282.751, 39.8285)   # etapa 2: Reynolds caiu a ~1,5 km a oeste/sudoeste da cidade (antes 39.836 = norte, errado),
     "CEMETERY HILL": (282.770, 39.821), "CULP'S HILL": (282.780, 39.820), "LITTLE ROUND TOP": (282.763, 39.792),
     "DEVIL'S DEN": (282.758, 39.792), "ROSE FARM": (282.752, 39.796), "RAILROAD CUT": (282.755, 39.838),
     "FREDERICKSBURG": (282.540, 38.303), "WASHINGTON": (282.963, 38.907), "RICHMOND": (282.564, 37.541),
     "HARRISBURG": (283.116, 40.274), "SLOPE": (282.7578, 39.7915), "THE NOOK": (282.7575, 39.7918)}
DITT = "mapa_ditterline_1863.jpg"

B = []
SPLIT = {b["id"]: b["texto"] for b in json.load(open(AQUI / "qa/split_blocos.json"))}


def bloco(bid, *planos, ideia=False):
    B.append(dict(id=bid, texto=SPLIT[bid], ideia=ideia, planos=list(planos)))


# Arquivos usados com frequência
TOCA, TOCA2, ALB41 = "foto_toca_gardner_1863.jpg", "foto_toca_osullivan_estereo.jpg", "foto_toca_album_1866.jpg"
P40, NEG40, V3, V4 = "foto_encosta_prancha40.jpg", "foto_encosta_negativo.jpg", "foto_encosta_vista3.jpg", "foto_encosta_vista4.jpg"
VA, VB = "foto_linha_vista_a.jpg", "foto_linha_vista_b.jpg"
S36, S37, S40, S41 = "doc_sketchbook_p36.jpg", "doc_sketchbook_p37.jpg", "doc_sketchbook_p40.jpg", "doc_sketchbook_p41.jpg"
RIFLE = "detalhe:0.42,0.52"     # fuzil encostado na pedra (foto_toca_gardner_1863)
MURO = "detalhe:0.33,0.28"      # parede de pedra entre os dois blocos
MULT = "foto_multidao_lincoln_1863.jpg"
LINCOLN = "detalhe:0.418,0.424"  # Lincoln na chapa inteira (achado por correlação com o recorte NARA do Commons, 13/11/2026)
LINCOLN_ZOOM = ((0.5, 0.5, 1.04), (0.418, 0.424, 3.2))   # zoom forte para "Right here"

# ===================================================================== planos
# ===== Bloco 1: hook
bloco("B01a",
      doc("Look at this photograph.", "foto_toca_montada_1863.jpg", "pagina", G["pagina"]),
      kb("A young soldier lies dead", TOCA, "zoom-out", num=("JULY 1863", "GETTYSBURG, PENNSYLVANIA")),
      ideia=True)
bloco("B01b",
      kb("A rifle leans", TOCA, RIFLE),
      doc("The man who sold this picture", S41, "titulo", G["p41_titulo"], frase="The Home of a Rebel Sharpshooter"),
      kb("How the sharpshooter built", TOCA, MURO))
bloco("B01c",
      doc("How he lay down", S41, "await", G["p41_await"], literal=False),
      kb("Now look at the rifle again.", TOCA, RIFLE),
      num("Because two things", "2", "THINGS THAT AREN'T WHAT THEY SEEM"))
bloco("B01d",
      dupla("This man was probably", TOCA, NEG40, "THE FAMOUS PLATE", "THE SAME MAN, 40 YARDS AWAY"))

# ===== Bloco 2: âncora + pergunta do título
bloco("B02a",
      kb("In 1975, a historian", "foto_devils_den_1863.jpg", "zoom-in", num=("1975", "WILLIAM FRASSANITO")),
      ea("He took the original", "foto_vista_lrt_1863.jpg", "hoje_lrt_vista_highsmith.jpg", "1863", "TODAY"),
      ideia=True)
bloco("B02b",
      dupla("And the photographs began", NEG40, TOCA, "PLATE 40", "PLATE 41"),
      num("So what are the Gettysburg", "?", "THE PHOTOS YOU WEREN'T SUPPOSED TO SEE"),
      kb("They weren't classified.", "foto_galeria_gardner.jpg", "zoom-in"))
bloco("B02c",
      kb("Some of them were on sale", "foto_toca_osullivan_estereo.jpg", "zoom-out"),
      dupla("The photos you weren't supposed", V3, V4, "THE SLOPE", "THE SLOPE, ANOTHER ANGLE"),
      kb("or from the other side", VB, "pan-esq"))
bloco("B02d",
      kb("The ones that show how", "foto_rose_carroca.jpg", "zoom-in"),
      doc("The National Archives puts it", "doc_nara_2013.png", "100", G["nara_100"], frase="historians did not question the captions"))
bloco("B02e",
      kb("Along the way, you'll see", V4, "pan-dir"),
      dupla("the same dead men", VA, VB, "VIEW A", "VIEW B"),
      kb("and a crowd photograph", MULT, "zoom-out", num=("89", "YEARS")))

# ===== Bloco 3: Three days in July
bloco("B03a",
      mapa("In the summer of 1863,", "invasao", ["FREDERICKSBURG", "WASHINGTON", "RICHMOND", "GETTYSBURG", "HARRISBURG"],
           [("FREDERICKSBURG", "GETTYSBURG", "LEE MARCHES NORTH · JUNE 1863")]),
      ideia=True)
bloco("B03b",
      kb("On the morning of July 1st,", "foto_seminario_1863.jpg", "pan-dir", num=("JULY 1", "1863")),
      kb("his men ran into", "foto_mcpherson_1863.jpg", "zoom-in"))
bloco("B03c",
      mapa("For three days,", "campo", ["GETTYSBURG", "SEMINARY RIDGE", "CEMETERY HILL", "CULP'S HILL", "LITTLE ROUND TOP", "DEVIL'S DEN"], [],
           nota="base: mapa de Ditterline (1863)", base=DITT),
      kb("around a hill called", "foto_little_round_top_1863.jpg", "pan-esq"),
      kb("and a jumble of giant boulders", "foto_devils_den_1863.jpg", "zoom-in"),
      num("When it ended,", "51,000+", "DEAD, WOUNDED OR MISSING"))
bloco("B03d",
      kb("It was the costliest", "foto_culps_hill_arvores.jpg", "tilt-cima"),
      kb("On the Fourth of July,", "foto_prisioneiros_1863.jpg", "zoom-in"),
      kb("And the people of Gettysburg", "foto_rose_pomar.jpg", "pan-dir"),
      dupla("In the words of the National", "foto_centro_campo.jpg", "foto_mortos_federais_1jul.jpg", "CONFEDERATE DEAD", "UNION DEAD"))   # etapa 2 (13/11): a página doc_nps_2015 é sobre um crânio de 2015, não a frase do "graveyard"
# Nota: a frase "every farm field or garden was a graveyard" é da página Gettysburg Overview do NPS; aqui só a página do parque
# como fundo (não literal). Etapa 2 pode trocar por captura da página Overview com o grifo (FATOS.md F07).

# ===== The man who quit Brady
bloco("B04a",
      kb("Into those fields,", "foto_rose_enterro.jpg", "zoom-in"),
      dupla("Alexander Gardner was", "foto_gardner_1863.jpg", "foto_gardner_autorretrato.jpg", "ALEXANDER GARDNER", "SCOTTISH-BORN PHOTOGRAPHER"),
      kb("Brady was the most famous", "foto_brady_mcpherson.jpg", "pan-dir"),
      ideia=True)
bloco("B04b",
      cartela("Pictures his employees", ["\"PHOTOGRAPHED BY BRADY\"", "— THE CREDIT LINE ON HIS STUDIO'S PICTURES"], selo="QUOTED"),
      kb("In May of 1863,", "foto_galeria_gardner.jpg", "pan-esq", num=("MAY 1863", "GARDNER'S GALLERY")),
      kb("One of them was a young", "foto_toca_osullivan_estereo.jpg", "zoom-in"))
bloco("B04c",
      num("On July 5th,", "JULY 5", "1863 · GARDNER REACHES GETTYSBURG"),
      kb("Brady's own team", "foto_brady_mcpherson.jpg", "detalhe:0.62,0.55"))
bloco("B04d",
      dupla("For a few days,", "foto_rose_borda.jpg", "foto_rose_bosque.jpg", "JULY 1863", "GARDNER'S PLATES"))

# ===== Ten seconds of stillness
bloco("B05a",
      kb("To understand what happened", "foto_john_burns.jpg", "zoom-in"),
      cartela("In 1863, a photographer", ["WET PLATE · 1863", "GLASS + WET CHEMICALS → CAMERA → 5–20 SECONDS → DEVELOP BEFORE IT DRIES"], selo="SCHEMATIC"),
      ideia=True)
bloco("B05b",
      kb("Then he had minutes", "foto_rose_carroca.jpg", "detalhe:0.08,0.62"),
      kb("Nothing that moved", "foto_culps_hill_bosque.jpg", "zoom-in"),
      num("The camera could only record", "5–20 SEC", "ONE EXPOSURE"))
bloco("B05c",
      kb("And what was left", "foto_caixao_mula.jpg", "zoom-out"),
      kb("Gardner knew his customers.", "foto_galeria_gardner.jpg", "detalhe:0.5,0.4"),
      dupla("as large prints", ALB41, TOCA2, "LARGE PRINT", "STEREO CARD"))
bloco("B05d",
      doc("Years later,", "doc_sketchbook_frontispicio.jpg", "pagina", G["pagina"]),
      dupla("each plate with a page", ALB41, S41, "THE PLATE", "HIS WORDS"),
      kb("Remember one more thing", "doc_sketchbook_titulo.jpg", "zoom-in"))   # etapa 2: 3 Números seguidos (13 s) → página-título do Sketch Book
bloco("B05e",
      num("He said he came back", "NOV 19", "1863"))

# ===== The field by the Rose farm
bloco("B06a",
      num("On July 5th and 6th,", "JULY 5–6", "1863"),
      dupla("Near the Rose family's farm,", "foto_rose_pomar.jpg", "foto_rose_borda.jpg", "THE ROSE FARM", "THE EDGE OF THE ROSE WOODS"),
      kb("some gathered in rows", "foto_rose_carroca.jpg", ((0.5, 0.5, 1.04), (0.2, 0.6, 1.3)), enq="pan-carroca"),
      ideia=True)
bloco("B06b",
      mapa("That wagon is very likely", "rose", ["ROSE FARM", "DEVIL'S DEN", "LITTLE ROUND TOP", "GETTYSBURG"], [], base=DITT),
      kb("He made one exposure.", VA, "zoom-in"))
bloco("B06c",
      kb("Then he moved around", VB, "pan-esq"),
      dupla("The men in these pictures", VA, VB, "ONE SIDE", "THE OTHER SIDE"),
      num("Remember that.", "THE SHOES", ""))
bloco("B06d",
      kb("The shoes. These were real men,", "foto_covas_inacabadas.jpg", "zoom-in"))

# ===== A young man on the slope
bloco("B07a",
      ea("On July 6th, the team", "foto_devils_den_1863.jpg", "hoje_devils_den_highsmith.jpg", "JULY 1863", "TODAY", num=("JULY 6", "1863")),
      kb("Here, on the second day", "foto_trincheiras_lrt.jpg", "pan-dir"),
      doc("On the southern slope,", P40, "pagina", G["pagina"]),
      ideia=True)
bloco("B07b",
      kb("Something about him", NEG40, "zoom-out"),
      num("At a time when every plate", "1 PLATE", "= TIME AND MONEY"),
      kb("They photographed him lying", NEG40, "pan-esq"))
bloco("B07c",
      dupla("Then from another angle,", V3, V4, "ANOTHER ANGLE", "AND ANOTHER"),
      num("In all, the Park Service counts", "6", "PLATES OF ONE SOLDIER"),
      kb("Four of them were made", "hoje_nps_encosta_thennow.jpg", "zoom-in", crop=(0.0, 0.0, 0.62, 1.0)))
bloco("B07d",
      kb("Which raises a question.", TOCA, "zoom-in"))

# ===== Forty yards
bloco("B08a",
      dupla("Frassanito's answer", V4, "hoje_nps_stereo263_thennow.jpg", "1863", "THE SAME ROCK TODAY"),
      dupla("In the background of four", NEG40, V3, "SOUTHERN SLOPE", "SOUTHERN SLOPE"),
      ideia=True)
bloco("B08b",
      kb("In the other two,", TOCA, MURO),
      mapa("That spot is about forty yards", "toca", ["SLOPE", "THE NOOK"], [("SLOPE", "THE NOOK", "~40 YARDS")], selo="SCHEMATIC",
           nota="esquema simples (2 pontos), não precisa de base cartográfica"),
      ea("The body is the same.", NEG40, TOCA, "THE SLOPE", "THE 'DEN'"))
bloco("B08c",
      dupla("The uniform is the same.", V3, TOCA2, "BEFORE", "AFTER"),
      kb("carried the dead man there,", "hoje_devils_den_highsmith.jpg", "zoom-in"))
bloco("B08d",
      kb("In one stereo view", TOCA2, "zoom-in"),
      doc("And then they made their picture.", ALB41, "pagina", G["pagina"]))
bloco("B08e",
      kb("A knapsack under the head.", TOCA, RIFLE))

# ===== The rifle
bloco("B09a",
      kb("Remember the rifle.", TOCA, RIFLE),
      doc("According to the Library", "doc_loc_camera_3.png", "prop", G["loc_prop"], frase="probably was the photographer's prop", literal=False),
      dupla("And the same rifle", NEG40, TOCA, "PLATE 40", "PLATE 41"),
      ideia=True)
# (literal=False: a narração diz "most likely the photographer's prop"; o grifo mostra a frase exata da LoC)
bloco("B09b",
      kb("Frassanito also noticed", V3, "zoom-out"),
      num("A whole series", "~1 HOUR", "ONE BODY"),
      kb("It suggests he may have been", "foto_slaughter_pen.jpg", "pan-esq"))
bloco("B09c",
      kb("Gardner may have felt", ALB41, "zoom-in"),
      cartela("None of this means", ["HE WAS REAL."], selo=None))
bloco("B09d",
      kb("He died at Gettysburg,", "hoje_vista_lrt_highsmith.jpg", "zoom-in"),
      doc("But the man in the most famous", "foto_toca_montada_1863.jpg", "pagina", G["pagina"], num=("160+", "YEARS")))

# ===== Bloco 4: as legendas
bloco("B10a",
      kb("But the strangest part", ALB41, "zoom-out"),
      doc("When the Sketch Book came out", "doc_sketchbook_frontispicio.jpg", "pagina", G["pagina"]),
      kb("For the man by the wall,", TOCA, "zoom-in"),
      ideia=True)
bloco("B10b",
      doc("\"The Confederate soldier", S41, "built", G["p41_built"],
          frase="The Confederate soldier had built up between two huge rocks, a stone wall, from the crevices of which he had directed his shots"),
      doc("Then he described how", S41, "await", G["p41_await"], frase="had laid down upon his blanket to await death"))
bloco("B10c",
      kb("Now turn back one page,", P40, "zoom-in", num=("PLATE 40", "THE SAME MAN")),
      doc("A burial party", S40, "fell", G["p40_fell"], frase="found, in a secluded spot, a sharpshooter lying as he fell when struck by the bullet"),
      kb("Lying as he fell.", NEG40, "zoom-in"))
bloco("B10d",
      dupla("Two plates, one man,", P40, ALB41, "PLATE 40: \"LYING AS HE FELL\"", "PLATE 41: \"LAID DOWN TO AWAIT DEATH\""),
      doc("And for over a hundred years,", "doc_nara_2013.png", "100b", G["nara_100"], literal=False))

# ===== Two armies, one row of dead
bloco("B11a",
      kb("And then there are the men", VA, "zoom-out"),
      num("Remember the shoes.", "THE SHOES", ""),
      kb("Gardner used one of", "foto_colheita_prancha36.jpg", "zoom-out", num=("PLATE 36", "\"A HARVEST OF DEATH\"")),
      doc("His text says", S36, "pagina", G["pagina"]),
      ideia=True)
bloco("B11b",
      doc("\"The rebels represented", S36, "shoes", G["p36_shoes"], frase="The rebels represented in the photograph are without shoes."),
      doc("It says they died attacking", S36, "treason", G["p36_treason"], frase="they paid with life the price of their treason"),
      kb("Now look at plate thirty-seven,", "foto_reynolds_prancha37.jpg", "zoom-in"))
bloco("B11c",
      kb("It's the other exposure,", VB, "zoom-in"),
      doc("And the text for this one says:", S37, "own", G["p37_own"], frase="The dead shown in the photograph were our own men."),
      kb("Our own men.", VB, "pan-dir"))
bloco("B11d",
      dupla("When Frassanito matched", VA, VB, "PLATE 36: \"REBELS\"", "PLATE 37: \"OUR OWN MEN\"", selo="SAME ROW"),
      cartela("And on that coat,", ["◆", "THE DIAMOND BADGE OF THE UNION THIRD CORPS", "(VISIBLE ON A COAT IN BOTH VIEWS)"], selo="SCHEMATIC"),
      kb("The men Gardner sold", "foto_colheita_prancha36.jpg", "zoom-out", num=("UNION", "SOLDIERS")))

# ===== Why lie?
bloco("B12a",
      kb("Why would he do it?", "foto_gardner_autorretrato.jpg", "zoom-in"),
      dupla("A row of dead Confederates", VA, VB, "\"REBELS\"", "\"OUR OWN MEN\""),
      ideia=True)
bloco("B12b",
      mapa("And Gardner's title", "reynolds", ["McPHERSON'S WOODS", "ROSE FARM", "GETTYSBURG"],
           [("McPHERSON'S WOODS", "ROSE FARM", "")], nota="McPherson's = onde Reynolds caiu; Rose farm = onde a foto foi feita", base=DITT),
      kb("General John Reynolds", "foto_mcpherson_1863.jpg", "pan-esq"))
bloco("B12c",
      doc("The Library of Congress,", "doc_loc_camera_1.png", "rearr", G["loc_rearr"],
          frase="Gardner sometimes rearranged the elements in his photographs or departed from the facts in his writing"))
bloco("B12d",
      kb("The book came out", "foto_cemiterio_tipton.jpg", "zoom-in"),
      kb("Gardner gave them stories.", ALB41, "zoom-out"))

# ===== Bloco 5: November 19th
bloco("B13a",
      doc("There's one more line", S41, "pagina", G["pagina"]),
      num("Remember November 19th.", "NOV 19", "1863"),
      kb("Gardner wrote that on that day", "hoje_devils_den_highsmith.jpg", "zoom-in"),
      ideia=True)
bloco("B13b",
      doc("\"The musket, rusted", S41, "musket", G["p41_musket"],
          frase="The musket, rusted by many storms, still leaned against the rock, and the skeleton of the soldier lay undisturbed within the mouldering uniform"),
      kb("Four months, and nobody", TOCA, "zoom-out"))
bloco("B13c",
      kb("By November, burial parties", "foto_covas_inacabadas.jpg", "pan-dir"),
      doc("A rifle left in plain sight", "doc_loc_camera_3.png", "relic", G["pagina"], literal=False, regiao=[0, 0, 1, 0.4]),
      kb("But Gardner was right", "foto_portao_cemiterio_1863.jpg", "zoom-in"))
bloco("B13d",
      kb("So was a crowd", "foto_multidao_discurso.jpg", "pan-dir", num=("10,000+", "PEOPLE")),
      num("and the President", "\"A FEW APPROPRIATE REMARKS\"", "WHAT LINCOLN WAS INVITED TO GIVE"))

# ===== Find the President
bloco("B14a",
      kb("Eleven days earlier,", "foto_lincoln_8nov1863.jpg", "tilt-cima"),
      num("This one.", "NOV 8", "1863 · GARDNER'S STUDIO"),
      kb("Now here is a photograph", MULT, "zoom-out"),
      ideia=True)
bloco("B14b",
      kb("It shows the crowd", MULT, "pan-dir"),
      num("Try to find him.", "?", "FIND THE PRESIDENT"),
      kb("For eighty-nine years,", MULT, "pan-esq", num=("89", "YEARS")))
bloco("B14c",
      doc("Then, in 1952,", "foto_cobb_nara.jpg", "pagina", G["pagina"], num=("1952", "JOSEPHINE COBB")),
      kb("She found the President's bodyguard,", MULT, "detalhe:0.43,0.41"))
bloco("B14d",
      kb("And when she enlarged", MULT, LINCOLN_ZOOM, enq="zoom-lincoln"),
      num("The National Archives calls it", "1", "PHOTO OF LINCOLN AT GETTYSBURG"))

# ===== Two minutes
bloco("B15a",
      kb("The main speaker", "foto_multidao_discurso.jpg", "zoom-out"),
      num("Then Lincoln stood up", "~2 MIN", "10 SENTENCES"),
      kb("Many people at the back", MULT, "pan-esq"),
      ideia=True)
bloco("B15b",
      doc("In one of those sentences,", "doc_discurso_bliss.jpg", "pagina", G["bliss_world"]),
      cartela("He was wrong", ["\"THE WORLD WILL LITTLE NOTE, NOR LONG REMEMBER WHAT WE SAY HERE…\""], selo="QUOTED"))
bloco("B15c",
      kb("The speech became", "hoje_cerimonia_2013.jpg", "zoom-in"),
      dupla("and that's where Gardner's", V3, ALB41, "JULY 6, 1863", "THE SKETCH BOOK"),
      kb("Because what they did there", "foto_rose_bosque.jpg", "pan-esq"))
bloco("B15d",
      dupla("Not the charge up the slope,", V3, "foto_little_round_top_1863.jpg", "THE SLOPE", "LITTLE ROUND TOP"),
      kb("Not the speeches,", "foto_rose_pomar.jpg", "zoom-out"))

# ===== What's still out there
bloco("B16a",
      kb("So what's still out there today?", "hoje_parque_highsmith.jpg", "pan-dir"),
      ea("Most of the Union dead", "foto_cemiterio_tipton.jpg", "hoje_cemiterio_highsmith.jpg", "1880s", "TODAY"),
      ideia=True)
bloco("B16b",
      kb("More than thirty-five hundred", "hoje_cerimonia_2013.jpg", "pan-esq", num=("979", "UNKNOWN")),
      kb("The Confederate dead stayed", "foto_covas_inacabadas.jpg", "zoom-out"))
bloco("B16c",
      num("Between 1871 and 1873,", "1871–1873", "CONFEDERATE DEAD MOVED SOUTH"),
      kb("And not all of the dead", "hoje_parque_highsmith.jpg", "zoom-in"),
      doc("In 1996, erosion", "doc_nps_2015.png", "1996", G["nps_1996"], literal=False))
bloco("B16d",
      kb("Scientists from the Smithsonian", "hoje_cemiterio_highsmith.jpg", "pan-dir"),
      doc("In 1997 he was buried", "doc_nps_2015.png", "unknown", G["nps_unknown"], frase="Unknown Civil War Remains"))

# ===== The wall is still there
bloco("B17a",
      kb("And the sharpshooter's den?", "hoje_toca_2015.jpg", "zoom-in"),
      ea("The low stone wall", TOCA, "hoje_toca_2015.jpg", "1863", "2015"),
      ideia=True)
bloco("B17b",
      kb("Park Service photographers", "hoje_nps_toca_thennow.jpg", "zoom-out"),
      dupla("Visitors climb in", "hoje_toca_2015.jpg", "hoje_devils_den_cc0.jpg", "THE 'DEN' TODAY", "DEVIL'S DEN TODAY"),
      num("As for who he was,", "?", "WHO WAS HE?"))
bloco("B17c",
      kb("A Park Service historian,", "hoje_devils_den_cc0.jpg", "pan-dir"),
      num("from what may be the number 2", "\"2\"", "ON THE KNAPSACK?"),
      kb("that he was probably a Georgian,", "hoje_den_haer.jpg", "zoom-in"))
bloco("B17d",
      kb("After a hundred and sixty years,", ALB41, "zoom-out"))

# ===== Bloco 6: fecho
bloco("B18a",
      num("So what are the Gettysburg photos", "?", "THE PHOTOS YOU WEREN'T SUPPOSED TO SEE"),
      dupla("The quiet pictures", NEG40, V4, "WHERE HE MOST LIKELY FELL", "BEFORE THE 'DEN'"),
      ideia=True)
bloco("B18b",
      kb("The second view", VB, "zoom-in", num=("UNION", "THIRD CORPS")),
      dupla("And a crowd on November 19th,", MULT, "foto_lincoln_8nov1863.jpg", "NOV 19, 1863", "NOV 8, 1863"))
bloco("B18c",
      kb("Now look at the first photograph", TOCA, "zoom-out"))
bloco("B18d",
      kb("Everything in this picture", TOCA, RIFLE),
      num("Here's my question for you.", "?", "DOES IT MATTER THAT THE SCENE WAS ARRANGED?"))
bloco("B18e",
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
        if q["tipo"] == "KenBurns" and q["arq"] in {TOCA, NEG40, V3, V4, VA, VB, P40, ALB41, TOCA2} and str(q["enq"]).startswith("detalhe:") \
                and q["enq"] not in (RIFLE, MURO, "detalhe:0.5,0.35"):
            AVISOS.append(f"{q['bloco']}: detalhe em foto de morto ({q['arq']} {q['enq']}): conferir que não é close de rosto/ferimento")

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
        lim = RUN_MAX_FOTO if run_tipo in ("KenBurns", "Dupla", "DocGrifo") else RUN_MAX
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
    REAL = {"KenBurns", "DocGrifo", "EntaoAgora", "Dupla"}
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
    NOMES = {"Lincoln": ["lincoln", "multidao", "discurso", "bliss"], "Cobb": ["cobb", "multidao"], "Gardner": None,
             "O'Sullivan": None, "Brady": ["brady", "galeria", "multidao", "gardner"], "plate forty": ["40", "prancha40", "p40"],
             "thirty-seven": ["37", "reynolds"], "thirty-six": ["36", "colheita"]}
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

    L = ["# STORYBOARD: 003-gettysburg (lugares-guerra-en, \"Clearance Required\")", "",
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
