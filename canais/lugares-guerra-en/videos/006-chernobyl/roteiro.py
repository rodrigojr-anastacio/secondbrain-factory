#!/usr/bin/env python3
"""Fonte do storyboard do lugares-guerra-en 006 "Chernobyl Burned for Days Before the World Knew" (youtube.videos id 55).
Uso: cd <pasta do vídeo> && python3 tools/split_blocos.py && python3 roteiro.py   (python3 puro)
O roteiro FINAL é o SCRIPT.md (fatos em FATOS.md/SOURCES.md). Blocos de áudio: tools/split_blocos.py (qa/split_blocos.json + blocos-voz.json);
os marcadores [[A1]]…[[A6]] do SCRIPT.md viram áudios de época (Arquivo) antes do bloco marcado com "arquivo_antes".
Base: 005-tarawa/roteiro.py (validação) + componentes da amostra aprovada (amostras/chernobyl-2026-11-21/src/Amostra.jsx → src/Amostra.jsx):
contador duplo + régua de horas (overlay persistente, estado por bloco em `relogio`), Arquivo (onda + legenda + selo), Datilo (cartão
datilografado), Teletipo (TASS/DREG), Mural (zoom-out), Glitch (transição), Mapa2D com pluma.
Desvios aprovados (BRIEF.md): material com dono entra COM CRÉDITO NA TELA (coluna `credito` do midia.csv vai no plano); meta ≥ 40% do tempo
com foto/vídeo REAL DE ÉPOCA (validado aqui: `epoca_pct`). Nada de vítimas/hospital/cadáver (midia.csv conferido pelo agente de acervo).
Âncoras: plano com `em=` explícito começa naquela frase; os sem `em` são distribuídos automaticamente entre as âncoras fixas, por peso
(filme = duração do clipe; foto/doc = 4 s), cortando só em fronteira de palavra. Grifos: posição EXATA do PDF (tools/docs_pos.json).
"""
import csv
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MIDIA = AQUI / "midia"
WPS = 2.8                 # voz Narrator medida no 002 (≈168 ppm)
RUN_MAX = 12.0
RUN_MAX_FOTO = 14.0
JANELA = 60.0
INEDITO_ATE = 180.0
REAL_MIN = 0.70           # material real (foto/filme/doc/satélite). Bíblia: 85%; aqui a linguagem APROVADA da amostra (contador, régua, mapa com pluma,
                          # teletipo, cartão datilografado, mural) ocupa ~25% por desenho; a meta do Rodrigo é a de época (EPOCA_MIN), validada abaixo
EPOCA_MIN = 0.40          # decisão do Rodrigo (21/11/2026): ≥ 40% do tempo com foto/vídeo real de época
FILME_VEL_MIN = 0.7       # build.py pode desacelerar o clipe até 0,7×
REUSO_LIBERADO = {"doc_insag7_p65_tabela-I-I-0123-40.png", "foto_kh9_pripyat_1984.jpg", "foto_landsat5_29abr1986.jpg",
                  "doc_wilson208406_p1_ministerstvo-avtotransporta-2000.png"}

MOV = {
    "zoom-in": ((0.5, 0.5, 1.04), (0.5, 0.5, 1.16)),
    "zoom-out": ((0.5, 0.5, 1.16), (0.5, 0.5, 1.04)),
    "pan-dir": ((0.44, 0.5, 1.12), (0.56, 0.5, 1.12)),
    "pan-esq": ((0.56, 0.5, 1.12), (0.44, 0.5, 1.12)),
    "tilt-baixo": ((0.5, 0.44, 1.12), (0.5, 0.56, 1.12)),
    "tilt-cima": ((0.5, 0.56, 1.12), (0.5, 0.44, 1.12)),
}


def _mov(m):
    if m.startswith("detalhe:"):
        x, y = (float(v) for v in m[8:].split(","))
        return m, ((x, y, 1.35), (x, y, 1.55))
    return m, MOV[m]


def _csv():
    out = {}
    with open(AQUI / "midia.csv", newline="") as f:
        for r in csv.DictReader(f):
            m = re.search(r"([\d.]+)s\b", r["resolucao"])
            fi = re.search(r"Ficha sugerida:\s*(.+)$", r["observacao"])
            out[r["arquivo"]] = dict(dur=float(m.group(1)) if (m and r["arquivo"].endswith(".mp4")) else None,
                                     ficha=fi.group(1).strip() if fi else None, credito=r["credito"].strip())
    return out


CSV = _csv()
DOCS = json.load(open(AQUI / "tools/docs_pos.json"))
DOCS_MD = (MIDIA / "DOCS.md").read_text() if (MIDIA / "DOCS.md").exists() else ""


def P(**k):
    k.setdefault("em", None)
    return k


def kb(arq, mov="zoom-in", em=None, num=None, crop=None):
    nome, (de, para) = _mov(mov)
    return P(tipo="KenBurns", arq=arq, enq=nome, de=de, para=para, em=em, num=num, crop=crop)


def filme(arq, tin=0.0, tout=None, em=None, num=None):
    d = CSV.get(arq, {}).get("dur") or 0
    return P(tipo="Filme", arq=arq, tin=tin, tout=tout if tout is not None else d, enq=f"{tin:.1f}", vel=1.0, em=em, num=num)


def doc(arq, chave=None, frase=None, em=None, literal=True, num=None, legenda=None):
    """DocGrifo: chave = frase grifada em docs_pos.json (None = página inteira). frase = texto lido literalmente na narração."""
    g = []
    if chave:
        d = DOCS[arq]
        W, H = d["pagina_pt"]
        g = [(round((b[0] - 3) / W, 4), round((b[1] - 2) / H, 4), round((b[2] + 6) / W, 4), round((b[3] + 4) / H, 4))
             for b in d["frases"][chave]]
    return P(tipo="DocGrifo", arq=arq, enq=chave or "pagina", grifo=g, frase_doc=frase, literal=bool(literal and frase), em=em,
             num=num, legenda=legenda)


def num(valor, rotulo="", em=None):
    return P(tipo="Número", arq="codigo", enq="num:" + valor, valor=valor, rotulo=rotulo, em=em)


def mapa(nome, pontos, linhas, selo="SCHEMATIC", nota="", em=None, pluma=False):
    return P(tipo="Mapa2D", arq="codigo", enq="mapa:" + nome, nome=nome, pontos=pontos, linhas=linhas, selo=selo, nota=nota, em=em,
             pluma=pluma)


def cartela(linhas, selo="QUOTED", em=None):
    return P(tipo="Cartela", arq="codigo", enq="cartela:" + linhas[0][:30], linhas=linhas, selo=selo, em=em)


def ea(antes, depois, rot1, rot2, em=None):
    return P(tipo="EntaoAgora", arq=antes, arq2=depois, enq="ea", rot1=rot1, rot2=rot2, em=em)


def contador(de, ate, rotulo="", em=None):
    """Contador duplo em tela cheia (componente Contador da amostra): tempo decorrido desde 01:23:40 e hora local de Chernobyl."""
    return P(tipo="Contador", arq="codigo", enq=f"contador:{de}-{ate}", de_t=de, ate_t=ate, rotulo=rotulo, em=em)


def datilo(linhas, selo=None, em=None):
    return P(tipo="Datilo", arq="codigo", enq="datilo:" + linhas[0][:30], linhas=linhas, selo=selo, em=em)


def teletipo(linhas, selo="QUOTED", em=None):
    return P(tipo="Teletipo", arq="codigo", enq="teletipo:" + linhas[0][:30], linhas=linhas, selo=selo, em=em)


def mural(em=None):
    return P(tipo="Mural", arq="codigo", enq="mural", em=em)


def card(em=None):
    return P(tipo="Card", arq="codigo", enq="card", em=em)


# Áudios de época (não narrados). dur = trecho previsto (s); fundo = mídia real atrás da onda (ou None = tela quase preta).
ARQUIVOS = {
    "A1": dict(dur=8.3, selo="ARCHIVE AUDIO · 26 APRIL 1986", fonte="Records_of_telephone_conversations…ogg (Commons, PD-UA-exempt)", trecho="0:04.8–0:13.1",
               legenda=["«Взрыв на главном корпусе, 3–4 блок.» — Explosion at the main building, units three and four.",
                        "«А там люди есть?» — Are there people there?", "«Да.» — Yes."], fundo=None,
               rotulo="FIRE DISPATCH → PLANT FIRE STATION · IVANKOV · POLESSKOYE"),
    "A2": dict(dur=2.6, selo="ARCHIVE AUDIO · PRIPYAT CITY RADIO · 27 APRIL 1986", fonte="Pripyat_1986.ogg (Commons, PD-UA-exempt)", trecho="~0:55–0:59",
               legenda=["«…провести временную эвакуацию…» — …to carry out a TEMPORARY evacuation…"], fundo="filme_pripyat_rua_vazia_1986.mp4"),
    "A3": dict(dur=15.0, selo="ARCHIVE AUDIO · 26 APRIL 1986", fonte="Records_of_telephone_conversations…ogg (Commons)", trecho="~0:26–0:41 + 0:44–0:58 (revisar de ouvido/2ª fonte)",
               legenda=["«Алло… 3–4 блок, горит крыша в результате взрыва.» — Hello… units three–four, the roof is on fire after an explosion.",
                        "«Алло, Иванков? Высылайте… на атомную станцию.» — Ivankov? Send [crews] to the nuclear plant.",
                        "«Полесская? … горит крыша 3–4 блока.» — Polesskoye? … the roof of units three–four is burning."],
               fundo="filme_aerea_pb_usina_1986.mp4"),
    "A4": dict(dur=40.0, selo="ARCHIVE AUDIO · PRIPYAT CITY RADIO · 27 APRIL 1986", fonte="Pripyat_1986.ogg (Commons, PD-UA-exempt; voz atribuída a Nina Melnik)",
               trecho="0:12–1:04 editado (0:12–0:40 + 0:55–1:04) + 2:07–2:20",
               legenda=["Dear comrades! The City Council of People's Deputies announces that, due to the accident at the Chernobyl nuclear power station,",
                        "unfavourable radiation conditions are developing in the city of Pripyat.",
                        "…it has become necessary to carry out a TEMPORARY evacuation of the city's residents…",
                        "…today, April 27, beginning at 14:00, buses will be sent to every apartment building…",
                        "Comrades, when TEMPORARILY leaving your homes, please do not forget to close the windows…"],
               fundo="filme_pripyat_sacadas_playground_1986.mp4"),
    "A5": dict(dur=15.0, selo="RECONSTRUCTION · SYNTHETIC AUDIO · TEXT: TASS, 28 APRIL 1986", fonte="voz sintética (Fish) lendo o texto TASS (ruwiki/tass.ru; UPI 28/04)",
               trecho="5 frases", legenda=["An accident has occurred at the Chernobyl nuclear power station.", "One of the atomic reactors has been damaged.",
                                            "Measures are being taken to eliminate the consequences of the accident.", "Those affected are being given assistance.",
                                            "A government commission has been set up."], fundo="filme_vremya_locutora_28abr1986.mp4"),
    "A6": dict(dur=5.0, selo="ARCHIVE AUDIO · 26 APRIL 1986", fonte="despacho (Commons) + rádio de Pripyat (Commons)", trecho="eco: 0:08–0:13 do despacho",
               legenda=["«А там люди есть?» — Are there people there?", "«Да.» — Yes."], fundo=None),
}

# Pontos (lon, lat)
PT = {"CHERNOBYL NPP": (30.10, 51.39), "PRIPYAT": (30.05, 51.40), "KYIV": (30.52, 50.45), "DYMER": (30.30, 50.79), "IVANKOV": (29.90, 50.94),
      "CHERNOBYL (TOWN)": (30.22, 51.27), "FORSMARK": (18.17, 60.40), "STOCKHOLM": (18.07, 59.33), "MOSCOW": (37.62, 55.76),
      "WASHINGTON": (-77.04, 38.90), "MINSK": (27.56, 53.90), "DYTIATKY CHECKPOINT": (30.13, 51.12), "VIENNA (IAEA)": (16.37, 48.21)}

B = []
SPLIT = json.load(open(AQUI / "qa/split_blocos.json"))
TEXTO = {b["id"]: b["texto"] for b in SPLIT}
ANTES = {b["id"]: b.get("arquivo_antes") for b in SPLIT}


def bloco(bid, *planos, ideia=False, relogio=None):
    """relogio = (hora local de Chernobyl mostrada no overlay, granularidade 'dia'|'hora'|'min'|'seg'|'parado'|'oculto')."""
    B.append(dict(id=bid, texto=TEXTO[bid], ideia=ideia, planos=list(planos), relogio=relogio, arquivo_antes=ANTES.get(bid)))


# ===================================================================== arquivos
INS21, INS63, INS64, INS65 = ("doc_insag7_p21_no-operator-error.png", "doc_insag7_p63_tabela-I-I-25abr.png",
                              "doc_insag7_p64_tabela-I-I-0122-0123.png", "doc_insag7_p65_tabela-I-I-0123-40.png")
INS76, INS122, INS123 = "doc_insag7_p76_unable-to-establish-why.png", "doc_insag7_p122_tabela-II-III-25abr.png", "doc_insag7_p123_tabela-II-III-margem-reatividade.png"
INS124, INS125, INS126 = "doc_insag7_p124_tabela-II-III-0123-40-e-0124.png", "doc_insag7_p125_fitas-de-telefone-II-2-3-4.png", "doc_insag7_p126_duas-explosoes-testemunhas.png"
W406A, W406B, W406C = ("doc_wilson208406_p1_ministerstvo-avtotransporta-2000.png", "doc_wilson208406_p2_lista-de-onibus.png",
                       "doc_wilson208406_p3_1125-onibus-250-caminhoes.png")
W405 = "doc_wilson208405_bryukhanov-0125.png"
POL1, POL3, POLRU = "doc_politburo-28abr_p1_dolgikh-0130.png", "doc_politburo-28abr_p3_gorbachev-statement.png", "doc_politburo-28abr_ru_gorbachev-soobshchenie.png"
FRUS = "doc_frus-v05-d220_cia-29abr.png"
UPI1, UPI2, UPI4 = "doc_upi-28abr1986_p1_titulo-dateline.png", "doc_upi-28abr1986_p2_tass-announcement.png", "doc_upi-28abr1986_p4_forsmark.png"
LEI13, LEI14 = "doc_lei791a_p13_art12-radiacao.png", "doc_lei791a_p14_residencia-proibida.png"
KH9, LANDSAT, SPOT = "foto_kh9_pripyat_1984.jpg", "foto_landsat5_29abr1986.jpg", "foto_spot1_tchernobyl_1maio1986.jpg"
SALA_HOJE = "hoje_sala_controle_bloco4.jpg"
EUROPA = ["CHERNOBYL NPP", "FORSMARK", "STOCKHOLM", "MOSCOW", "KYIV"]

# ===================================================================== planos
# ===== Bloco 1: hook — o papel + o relógio (paga T1/thumb A; plantas C e B até 1:00)
bloco("B01a",
      doc(INS65, "eps5_texto", em="This line is from"),
      doc(INS65, "eps5_texto", frase="EPS-5 button was pressed", em="\"EPS-5 button was pressed.\"", literal=True),
      kb(SALA_HOJE, "detalhe:0.5,0.45", em="Someone in Reactor Four's"),
      contador("01:23:40", "01:23:40", "LOCAL TIME · CHERNOBYL", em="at one twenty-three"),
      filme("filme_aerea_bloco4_detalhe_1986.mp4", em="Seconds later"),
      ideia=True, relogio=("26.04 01:23:40", "parado"))
bloco("B01b",
      contador("01:23:40", "+67:36:20", "FROM THE BUTTON TO THE BULLETIN", em="Between that button"),
      kb(KH9, "zoom-in", em="This is that clock."),
      filme("filme_cabine_helicoptero_bloco4_1986.mp4", em="The fires on the roof"),
      filme("filme_bloco4_ruina_panoramica_1986.mp4", em="The reactor itself was not."),
      relogio=("26.04 01:23:40", "corre"))
bloco("B01c",
      kb(LANDSAT, "zoom-in", em="Its graphite core"),
      doc(W406A, "sinal_2000_26abr", em="At eight o'clock", literal=False),
      filme("filme_onibus_estrada_laz_1986.mp4", em="the order to prepare"),
      filme("filme_aerea_pripyat_horizonte_1986.mp4", em="The city spent"),
      relogio=("26.04 20:00", "corre"))
bloco("B01d",
      datilo(["27.04.1986 · PRIPYAT CITY RADIO", "…a TEMPORARY evacuation…", "…for the first while, food…"], selo="QUOTED", em="On Sunday"),
      kb("hoje_parque_diversoes_pripyat.jpg", "zoom-in", em="Remember that word."),
      mapa("pluma", EUROPA, [("CHERNOBYL NPP", "FORSMARK", "")], selo="SCHEMATIC · PATH APPROXIMATE", em="The first public alarm", pluma=True),
      filme("filme_abc_forsmark_aerea.mp4", em="went off in Sweden"),
      filme("filme_vremya_locutora_28abr1986.mp4", em="Moscow still said nothing"),
      relogio=("28.04 21:00:00", "corre"))

# ===== Bloco 2: o portão de hoje + a pergunta do título
bloco("B02a",
      filme("filme_caminhao_posto_controle_1986.mp4", em="Today there is"),
      filme("filme_placa_zona_proibida_1986.mp4"),
      mapa("zona", ["KYIV", "DYTIATKY CHECKPOINT", "CHERNOBYL NPP", "PRIPYAT"], [("KYIV", "DYTIATKY CHECKPOINT", "")], selo="SCHEMATIC", em="Beyond it"),
      kb("hoje_ponto_onibus_mosaico_misha.jpg", "pan-dir", em="Before 2022"),
      ideia=True, relogio=("TODAY", "oculto"))
bloco("B02b",
      filme("hoje_blocos_floresta_pripyat_voa.mp4", em="Since the invasion"),
      num("67 HOURS", "BEFORE THE WORLD KNEW", em="Chernobyl burned for days"),
      filme("filme_aerea_bloco4_chamine_1986.mp4", em="So how do you keep"),
      filme("hoje_roda_gigante_pripyat_voa.mp4", em="And why is the place"),
      relogio=("TODAY", "oculto"))
bloco("B02c",
      doc(W406A, "secreto", em="It isn't a mystery.", literal=False),
      doc(POL1, None, em="It's written down"),
      doc(FRUS, None))
bloco("B02d",
      filme("filme_abc_forsmark_fila.mp4", em="Along the way"),
      doc(W405, None, em="you'll read the papers"),
      filme("filme_abc_forsmark_sapato.mp4", em="and you'll see"))

# ===== Bloco 3: o relógio começa um dia antes (25/04)
bloco("B03a",
      contador("25.04 01:06", "25.04 01:06", "ONE DAY EARLY", em="To read that clock"),
      kb("foto_usina_vista_do_lago_yevsyukov1986.jpg", "pan-dir", em="On Friday"),
      ideia=True, relogio=("25.04 01:06", "hora"))
bloco("B03b",
      filme("filme_usina_chamine_1982.mp4", em="Before it stopped"),
      kb("foto_salao_turbinas_cor_yevsyukov1986.jpg", "zoom-in", em="could a turbine"),
      filme("filme_sala_turbinas_operarios_1986.mp4", em="until the backup"),
      doc(INS63, "power_reduction_0106", em="At one in the morning", literal=False),
      kb("foto_subestacao_usina_yevsyukov1986.jpg", "tilt-cima", em="By two in the afternoon"),
      relogio=("25.04 14:00", "hora"))
bloco("B03c",
      doc(INS63, "eccs_14h", em="That's when the official timeline", literal=False),
      doc(INS63, "kievenergo_14h", em="And the power grid controller", literal=False),
      kb("foto_avenida_arvores_yevsyukov1986.jpg", "zoom-in", em="It was a Friday afternoon."),
      relogio=("25.04 14:00", "parado"))
bloco("B03d",
      filme("filme_pripyat_aerea_cidade_1982.mp4", em="Factories and homes"),
      kb("foto_sala_transformador_usina_yevsyukov1986.jpg", "pan-esq", em="and a reactor at full output"),
      contador("25.04 14:00", "25.04 23:10", "NINE HOURS · EMERGENCY COOLING OFF", em="The test was postponed"),
      doc(INS122, "kievenergo_14h", em="At ten past eleven", literal=False),
      relogio=("25.04 23:10", "hora"))
bloco("B03e",
      filme("filme_operador_painel_mnemonico_1982.mp4", em="A new shift"),
      kb("foto_paineis_controle_usina_yevsyukov1986.jpg", "zoom-in", em="with a test they had expected"),
      contador("26.04 00:00", "26.04 00:00", "NEW SHIFT", em="None of them knew"),
      relogio=("26.04 00:00", "min"))

# ===== a noite em minutos (INSAG-7)
bloco("B04a",
      doc(INS65, None, em="The official reconstruction"),
      filme("filme_legasov_placa_aiea_1986.mp4", em="It's called INSAG-7"),
      doc(INS21, "operator_error_insag1", em="and it corrects", literal=False),
      kb("foto_velikhov_sala_controle_1986.jpg", "zoom-in", em="Its first annex"),
      ideia=True, relogio=("26.04 00:00", "min"))
bloco("B04b",
      doc(INS63, "potencia_30MW", em="At twenty-eight minutes", literal=False),
      num("30 MW", "THERMAL POWER · 00:28", em="That's almost nothing."),
      doc(INS63, "potencia_30MW", frase="not envisaged in the testing programme", em="The table notes", literal=False),
      doc(INS21, "operator_error_insag1", em="The 1986 report", literal=False),
      relogio=("26.04 00:28", "min"))
bloco("B04c",
      doc(INS21, "no_operator_error", frase="no operator error as such", em="The 1992 report says"),
      filme("filme_operadores_painel_1982.mp4", tin=0.0, em="To bring it back"),
      num("200 MW", "01:03 · FAR BELOW THE TEST PLAN", em="At three minutes past one"),
      relogio=("26.04 01:03", "min"))
bloco("B04d",
      doc(INS64, "0122_30", em="Then there's a line", literal=False),
      doc(INS123, "margem_6_8_barras", em="A computer printout", literal=False),
      num("6–8 / 15", "RODS IN RESERVE · MINIMUM ALLOWED", em="Calculated afterward"),
      relogio=("26.04 01:22:30", "min"))

# ===== os 45 s em segundos
bloco("B05a",
      doc(INS64, "0123_04", em="At one twenty-three and four seconds", literal=False),
      contador("26.04 01:23:04", "26.04 01:23:40", "SECONDS", em="It was supposed to last"),
      filme("filme_sala_controle_operador_1986.mp4", em="For the first thirty-six seconds"),
      ideia=True, relogio=("26.04 01:23:04", "seg"))
bloco("B05b",
      contador("26.04 01:23:40", "26.04 01:23:40", "", em="Then, at one twenty-three"),
      doc(INS65, "eps5_texto", frase="EPS-5 button was pressed", em="The table says:"),
      doc(INS65, "teletape_0123_39", em="Even here", literal=False),
      relogio=("26.04 01:23:40", "parado"))
bloco("B05c",
      kb(SALA_HOJE, "tilt-baixo", em="That's the emergency shutdown."),
      doc(INS76, "unable_to_establish", frase="The Commission was unable to establish why the button was pressed", em="And here is the strangest"),
      relogio=("26.04 01:23:40", "parado"))
bloco("B05d",
      doc(INS65, "mw_530", em="Three seconds later", literal=False),
      num("530 MW", "01:23:43 · AND RISING", em="power passed"),
      teletipo(["01:23:49  PRESSURE INCREASE IN REACTOR SPACE", "01:23:49  RUPTURE OF A FUEL CHANNEL", "01:23:49  NO VOLTAGE = 48 V"],
               selo="TEXT: IAEA INSAG-7, TABLE I-I", em="At one twenty-three forty-nine"),
      doc(INS65, "severe_shocks", em="Then the shift engineer's log", literal=False),
      relogio=("26.04 01:23:49", "seg"))
bloco("B05e",
      doc(INS65, "severe_shocks_frase", frase="Severe shocks; the RCPS rods stopped moving before they reached the lower limit stop switches",
          em="\"Severe shocks;"),
      doc(INS126, "two_explosions", em="Most of the people", literal=False),
      filme("filme_bloco4_janela_veiculo_1986.mp4", em="There is no instrument"),
      P(tipo="Glitch", arq="codigo", enq="glitch", em="There is only the log"),
      relogio=("26.04 01:24", "parado"))

# ===== bombeiros (horas)
bloco("B06a",
      filme("filme_parede_usina_chamine_1986.mp4", em="At the fire station"),
      contador("26.04 01:24", "26.04 01:28", "", em="A first group"),
      cartela(["LT. VOLODYMYR PRAVIK, 23", "PLANT FIRE BRIGADE (VPCh-2) · ARRIVED 01:28"], selo="RECORD", em="Their commander"),
      filme("filme_pripyat_aerea_playground_1982.mp4", em="A second crew"),
      cartela(["LT. VIKTOR KIBENOK, 23", "PRIPYAT FIRE BRIGADE (SVPCh-6)"], selo="RECORD", em="under Lieutenant"),
      ideia=True, relogio=("26.04 01:28", "hora"))
bloco("B06b",
      doc(INS125, "tape_recordings_telephone", em="Back in the dispatch center", literal=False),
      mapa("despacho", ["CHERNOBYL NPP", "PRIPYAT", "IVANKOV", "KYIV"], [("CHERNOBYL NPP", "IVANKOV", ""), ("CHERNOBYL NPP", "PRIPYAT", "")],
           selo="SCHEMATIC", em="and they were recorded"),
      relogio=("26.04 01:30", "hora"))
bloco("B06c",
      filme("filme_helicoptero_chamine_pb_1986.mp4", em="Units three and four"),
      filme("filme_bloco4_ruina_externa_1986.mp4", em="Nobody on the line"),
      contador("26.04 02:20", "26.04 05:00", "ROOF FIRES OUT AT 05:00", em="The roof fires"),
      relogio=("26.04 05:00", "hora"))
bloco("B06d",
      kb("foto_bloco4_chamine_ruinas_iaea1986.jpg", "zoom-in", em="By four in the morning", num=("250", "FIREMEN ON SITE · 04:00")),
      filme("filme_usina_vista_estrada_1986.mp4", em="That night"),
      cartela(["VALERY KHODEMCHUK · NEVER FOUND", "VOLODYMYR SHASHENOK · 06:00, 26 APRIL"], selo="RECORD", em="Valery Khodemchuk"),
      relogio=("26.04 06:00", "hora"))
bloco("B06e",
      kb("foto_helicoptero_sobre_usina_iaea1986.jpg", "pan-dir", em="Within four months", num=("28", "WITHIN FOUR MONTHS · UNSCEAR")),
      kb("foto_aerea_bloco4_destruido_iaea1986.jpg", "tilt-baixo", em="Both lieutenants"),
      doc(W405, None, em="That Saturday, the plant director"),
      relogio=("26.04 ~10:00", "hora"))
bloco("B06f",
      doc(W405, "explosao_0125", em="It puts the explosion", literal=False),
      num("1 · 1 · 34", "DEAD · MISSING · UNDER OBSERVATION", em="It counts one dead"),
      doc(W405, "incendio_0450_0600", em="It says the fire", literal=False),
      kb("foto_pripyat_vista_alta_blocos_yevsyukov1986.jpg", "zoom-out", em="And it ends with"),
      relogio=("26.04 ~10:00", "hora"))
bloco("B06g",
      doc(W405, "pripyat_normal", em="\"The situation at the city", literal=False,
          legenda="\"The situation at the city of Pripyat' and the adjoining population centers is normal.\" (trans. Wilson Center)"),
      filme("filme_pripyat_predio_arvores_1982.mp4", em="Remember that word"),
      relogio=("26.04 ~10:00", "hora"))

# ===== Pripyat: a ordem das 20:00 (paga C)
bloco("B07a",
      filme("filme_pripyat_familias_passeio_1982.mp4", em="Pripyat was a young city"),
      kb("foto_criancas_bicicleta_calcada_yevsyukov1986.jpg", "pan-dir", em="Tens of thousands"),
      filme("filme_pripyat_carrinho_bebe_1982.mp4", em="Saturday went on."),
      ideia=True, relogio=("26.04 15:00", "hora"))
bloco("B07b",
      kb("foto_alameda_central_yevsyukov1986.jpg", "zoom-in", em="But in Kyiv"),
      doc(W406A, "ministerstvo_cabecalho", em="This is a report", literal=False),
      doc(W406A, "secreto", em="stamped secret", literal=False),
      relogio=("26.04 19:59", "hora"))
bloco("B07c",
      doc(W406A, "ordem_masik", em="It says that", literal=False,
          legenda="\"In fulfillment of an order of Cde. K. I. Masik… received a signal at 2000 26 April 1986\" (trans. Wilson Center)"),
      filme("filme_kiev_monumento_1986.mp4", em="the ministry"),
      contador("26.04 20:00", "26.04 20:00", "THE ORDER", em="Eight o'clock on Saturday night."),
      doc(W406A, "sinal_2000_26abr", em="A signal to prepare", literal=False),
      relogio=("26.04 20:00", "parado"))
bloco("B07d",
      num("1,100", "BUSES · + A BATTALION OF TRUCKS", em="Eleven hundred of them"),
      doc(W406A, "coluna_2325", em="At twenty-five past eleven", literal=False),
      mapa("rota", ["KYIV", "DYMER", "IVANKOV", "CHERNOBYL (TOWN)", "PRIPYAT"],
           [("KYIV", "DYMER", ""), ("DYMER", "IVANKOV", ""), ("IVANKOV", "CHERNOBYL (TOWN)", "")], selo="SCHEMATIC · ROUTE AS IN THE REPORT",
           em="on a route through"),
      relogio=("26.04 23:25", "hora"))
bloco("B07e",
      doc(W406C, "1125_onibus", em="And the report says", literal=False,
          legenda="\"By 0400 27 April 1986 … 1125 buses and 250 trucks and special vehicles was concentrated around the city of Chernobyl'\" (trans. Wilson Center)"),
      kb("foto_rodoviaria_onibus_yevsyukov1986.jpg", "zoom-in", em="were waiting outside", num=("1,125", "BUSES WAITING · 04:00, 27 APRIL")),
      filme("filme_aerea_pripyat_rio_1986.mp4", em="The city of Pripyat spent"),
      filme("filme_onibus_turno_usina_1986.mp4", em="The buses were already"),
      relogio=("27.04 04:00", "hora"))
bloco("B07f",
      doc(W406A, "numero_data_382s", em="On the report", literal=False),
      relogio=("27.04 04:00", "hora"))

# ===== domingo: o anúncio (áudio real A4 antes do B08b)
bloco("B08a",
      filme("filme_pripyat_predio_pedestres_1982.mp4", em="On Sunday"),
      kb("foto_bloco_residencial_yevsyukov1986.jpg", "zoom-in", em="This is the actual"),
      filme("filme_pripyat_predios_rua_1986.mp4", em="It was recorded"),
      ideia=True, relogio=("27.04 ~11:00", "hora"))
bloco("B08b",
      filme("filme_bagagens_calcada_1986.mp4", em="It tells people"),
      filme("filme_pripyat_rua_vazia_1986.mp4", em="essential things"),
      datilo(["TEMPORARY"], selo="QUOTED · PRIPYAT CITY RADIO", em="Notice what it calls it."),
      relogio=("27.04 ~12:00", "hora"))
bloco("B08c",
      filme("filme_pripyat_sacadas_playground_1986.mp4", em="And listen to"),
      datilo(["CLOSE THE WINDOWS.", "SWITCH OFF THE ELECTRICAL AND GAS APPLIANCES.", "TURN OFF THE WATER TAPS."], selo="QUOTED · PRIPYAT CITY RADIO",
             em="Close the windows."),
      relogio=("27.04 ~12:00", "hora"))
bloco("B08d",
      filme("filme_casa_abandonada_tabuas_1986.mp4", em="It's what you tell"),
      doc(W406C, "1330_evacuacao", em="The ministry's report", literal=False),
      contador("27.04 13:30", "27.04 13:30", "+36:06 · BUSES ROLL IN", em="almost exactly thirty-six"),
      relogio=("27.04 13:30", "hora"))
bloco("B08e",
      filme("filme_cbs_moscou_jovens.mp4", em="A day later"),
      doc(POL1, "populacao_45000", em="only five thousand", literal=False, num=("45,000 → 5,000", "POLITBURO, 28 APRIL")),
      contador("28.04 07:00", "28.04 07:00", "+55 HOURS", em="By then"),
      filme("filme_abc_mapa_europa.mp4", em="And outside the Soviet Union"),
      relogio=("28.04 ~09:00", "hora"))

# ===== segunda: Forsmark (paga B)
bloco("B09a",
      doc(UPI1, "titulo", em="It's a wire story", literal=False),
      doc(UPI4, "forsmark_alarm", frase="set off an alarm Monday morning when his clothes registered unusually high radiation levels", em="It says that"),
      ideia=True, relogio=("28.04 MON", "hora"))
bloco("B09b",
      filme("filme_abc_forsmark_aerea.mp4", em="The plant is Forsmark"),
      mapa("forsmark", EUROPA, [("CHERNOBYL NPP", "FORSMARK", "700+ MI")], selo="SCHEMATIC", em="more than seven hundred miles"),
      cartela(["CLIFF ROBINSON", "CHEMIST · FORSMARK NUCLEAR PLANT, SWEDEN"], selo="RECORD", em="That morning, a chemist"),
      filme("filme_abc_forsmark_fila.mp4", em="and through the radiation monitor"))
bloco("B09c",
      cartela(["\"I HADN'T EVEN BEEN IN THE CONTROLLED AREA!\"", "— CLIFF ROBINSON, SWEDISH RADIO, 2011"], selo="QUOTED", em="He hadn't even"))
bloco("B09d",
      kb("foto_rivm_medicao_anefo_1maio1986_a.jpg", "zoom-in", em="Then Robinson came back"),
      filme("filme_abc_forsmark_fila.mp4", tin=0.0, em="and there was a line"),
      filme("filme_abc_forsmark_sapato.mp4", em="So Robinson borrowed a shoe"),
      kb("foto_rivm_medicao_anefo_1maio1986_b.jpg", "detalhe:0.5,0.5", em="and put it on"))
bloco("B09e",
      doc(UPI4, "600_employees", em="Then a second alarm", literal=False, num=("600", "EMPLOYEES EVACUATED · FORSMARK")),
      filme("filme_cbs_mapa_radiacao.mp4", em="At first, the authorities"),
      filme("filme_cbs_iodeto_potassio.mp4", em="Chemical analysis"))
bloco("B09f",
      mapa("vento", EUROPA, [("CHERNOBYL NPP", "FORSMARK", "")], selo="SCHEMATIC · WIND PATH APPROXIMATE", em="Other plants", pluma=True),
      cartela(["SWEDEN → MOSCOW:", "\"COULD THERE HAVE BEEN A NUCLEAR ACCIDENT?\"", "THE ANSWER: \"NO.\""], selo="AS REPORTED BY SWEDISH RADIO", em="Swedish diplomats"),
      filme("filme_cbs_moscou_calcada.mp4", em="According to Swedish Radio"))
bloco("B09g",
      filme("filme_delegacao_sovietica_aiea_1986.mp4", em="Sweden said"),
      relogio=("28.04 MON", "hora"))

# ===== segunda: Politburo → TASS 21:00 (o relógio para)
bloco("B10a",
      filme("filme_cbs_moscou_multidao.mp4", em="That same Monday"),
      doc(POL1, None, em="The notes survive."),
      doc(POL1, "dolgikh_1_30am", frase="On April 26, at 1:30 a.m. there was an explosion", em="A secretary of the Central Committee"),
      ideia=True, relogio=("28.04 ~10:00", "hora"))
bloco("B10b",
      P(tipo="TresRelogios", arq="codigo", enq="tres-relogios", valores=["01:23:40", "01:25", "01:30"],
        rotulos=["INSTRUMENTS (INSAG-7)", "PLANT DIRECTOR", "POLITBURO"], em="The instruments said"))
bloco("B10c",
      cartela(["\"ONLY A SMALL CIRCLE OF PEOPLE KNOW ABOUT THE ACCIDENT.\"", "— V. CHEBRIKOV, KGB · POLITBURO, 28 APRIL 1986"], selo="QUOTED",
              em="The head of the KGB"),
      doc(POL3, "gorbachev_statement_quickly", frase="We should issue a statement quickly, we must not delay", em="Gorbachev says:"))
bloco("B10d",
      doc(POL3, "gromyko_panic", frase="in such a way that it does not cause excessive anxiety or panic", em="Andrei Gromyko adds"),
      filme("filme_cbs_moscou_guarda_chuva.mp4", em="And Anatoly Dobrynin"),
      doc(POL3, "dobrynin_americans", frase="The Americans will notice the fact of the explosion and the spread of the radioactive cloud anyway",
          em="\"The Americans will notice"))
bloco("B10e",
      contador("28.04 21:00:00", "28.04 21:00:00", "VREMYA · 21:00 MOSCOW", em="At nine o'clock"),
      filme("filme_abc_vremya_locutora.mp4", em="the announcer read"),
      teletipo(["ТАСС · 28.04.1986", "НА ЧЕРНОБЫЛЬСКОЙ АТОМНОЙ ЭЛЕКТРОСТАНЦИИ ПРОИЗОШЛА АВАРИЯ…"], selo="TEXT: TASS, 28 APRIL 1986", em="Five short sentences."),
      filme("filme_cbs_vremya_locutor.mp4", em="This is what they said."),
      relogio=("28.04 21:00:00", "parado"))
bloco("B10f",
      contador("26.04 01:23:40", "+67:36:20", "THE CLOCK STOPS · 67:36:20", em="The clock stops here."),
      doc(UPI2, "tass_announcement", em="In New York", literal=False),
      filme("filme_cbs_ancora_acidente.mp4", em="That evening"),
      filme("filme_cbs_mapa_chernobyl_kiev.mp4", em="of a place most viewers"),
      relogio=("28.04 21:00:00", "parado"))

# ===== terça: Washington (CIA + Landsat; paga "Burned")
bloco("B11a",
      filme("filme_cbs_moscou_quadro_avisos.mp4", em="On Tuesday"),
      doc(FRUS, "cabecalho_cia", em="A CIA report", literal=False),
      doc(FRUS, "possibly_occurred_last_friday",
          frase="The Soviet nuclear accident announced by Moscow yesterday possibly occurred last Friday or at the latest early Saturday",
          em="\"The Soviet nuclear accident"),
      ideia=True, relogio=("29.04 TUE", "dia"))
bloco("B11b",
      contador("26.04 01:23:40", "26.04 01:23:40", "SATURDAY 01:23:40 · INSIDE THE WINDOW", em="The real answer"),
      cartela(["\"THE SOVIETS DELAYED ADMISSION OF THE DISASTER AND CONTINUE TO MINIMIZE DOMESTIC MEDIA COVERAGE…\"", "— CIA, 29 APRIL 1986 (FRUS 1981–88, V, DOC. 220)"],
              selo="QUOTED", em="A few lines down"))
bloco("B11c",
      kb(LANDSAT, "zoom-in", em="That same day, Landsat 5"),
      kb(LANDSAT, "detalhe:0.52,0.48", em="In the infrared"),
      filme("filme_aerea_lago_usina_1986.mp4", em="And next to it"))
bloco("B11d",
      kb(SPOT, "zoom-in", em="The reactor was dead."),
      filme("filme_aerea_bloco4_chamine_1986.mp4", tin=0.0, em="The fires on the roof had been"),
      filme("filme_helicoptero_ao_lado_bloco4_1986.mp4", em="The one inside"),
      relogio=("29.04 TUE", "dia"))

# ===== a zona: maio de 1986 → 1991 (paga "temporary")
bloco("B12a",
      mapa("zona30", ["CHERNOBYL NPP", "PRIPYAT", "KYIV", "CHERNOBYL (TOWN)"], [], selo="SCHEMATIC · 30 KM ZONE", em="By early May"),
      filme("filme_posto_controle_milicia_1986.mp4", em="A zone of thirty"),
      kb("foto_helicoptero_sobre_usina_iaea1986.jpg", "zoom-out", em="In 1986, about", num=("115,000", "PEOPLE EVACUATED IN 1986 · UNSCEAR")),
      filme("filme_kiev_lavagem_ruas_1986.mp4", em="and children were sent"),
      ideia=True, relogio=("MAY 1986", "dia"))
bloco("B12b",
      filme("filme_moradores_novas_casas_1986.mp4", em="Later, another", num=("220,000", "RESETTLED LATER")),
      filme("filme_arame_farpado_trigo_1986.mp4", em="In February 1991"),
      doc(LEI13, "art12_titulo", em="Here is that law", literal=False),
      relogio=("27.02.1991", "dia"))
bloco("B12c",
      doc(LEI13, "radiacao_perigosa", em="The land of the zone", literal=False,
          legenda="\"…transferred to the category of radiologically dangerous land.\" (Law of Ukraine No. 791a-XII, Art. 12)"),
      filme("filme_arame_farpado_passaro_1986.mp4", em="fenced off"),
      doc(LEI14, "residencia", em="And the first thing it bans", literal=False,
          legenda="\"…permanent residence of the population;\""),
      ea("filme:filme_rodagigante_pripyat_1986.mp4@3.0", "hoje_parque_diversoes_pripyat.jpg", "1986", "TODAY", em="So the word from"))
bloco("B12d",
      filme("hoje_roda_gigante_pripyat_voa.mp4", em="There was no"),
      num("40 YEARS", "OF A \"TEMPORARY\" EVACUATION", em="The temporary evacuation"),
      relogio=("TODAY", "dia"))

# ===== mais uma razão: 2022 e 2025
bloco("B13a",
      filme("hoje_blindado_enferrujado_willis.mp4", em="There's one more reason"),
      mapa("2022", ["MINSK", "CHERNOBYL NPP", "KYIV"], [], selo="SCHEMATIC", em="When Russia invaded"),
      cartela(["24 FEB 2022 → 31 MAR 2022", "CHERNOBYL NPP UNDER RUSSIAN CONTROL"], selo="RECORD · WNN / IAEA", em="They stayed until"),
      ideia=True, relogio=("2022", "dia"))
bloco("B13b",
      filme("hoje_sala_abandonada_pripyat_voa.mp4", em="Tourism stopped"),
      kb("hoje_nsc_arco_2018.jpg", "zoom-in", em="Then there is another"))
bloco("B13c",
      contador("14.02.2025 01:50", "14.02.2025 01:50", "IAEA TEAM ON SITE", em="On the fourteenth"),
      kb("hoje_nsc_estrutura.jpg", "tilt-cima", em="they heard an explosion"),
      cartela(["\"RADIATION LEVELS INSIDE AND OUTSIDE REMAIN NORMAL AND STABLE.\"", "— IAEA TEAM AT CHERNOBYL, 14 FEB 2025"], selo="QUOTED",
              em="Their photos showed"),
      filme("hoje_arco_nsc_obras_voa.mp4", em="Ukraine says"),
      relogio=("14.02.2025 01:50", "hora"))
bloco("B13d",
      cartela(["IAEA, DEC 2025:", "PRIMARY SAFETY FUNCTIONS LOST, INCLUDING CONFINEMENT", "LOAD-BEARING STRUCTURE NOT PERMANENTLY DAMAGED"], selo="RECORD",
              em="By December"),
      kb("hoje_usina_vista_iss.jpg", "zoom-in", em="Radiation levels stayed"),
      P(tipo="Dupla", arq="filme:filme_aerea_bloco4_detalhe_1986.mp4@2.0", arq2="hoje_nsc_arco_2018.jpg", enq="dupla", rot1="26 APR 1986 · ~01:24",
        rot2="14 FEB 2025 · ~01:50", em="Almost thirty-nine years"),
      relogio=("14.02.2025 01:50", "hora"))

# ===== fecho
bloco("B14a",
      filme("hoje_gol_cadeira_pripyat_voa.mp4", em="So why is Chernobyl"),
      kb("foto_pripyat_vista_alta_blocos_yevsyukov1986.jpg", "pan-esq", em="Because the graphite"),
      ideia=True, relogio=("26.04 01:23:40", "oculto"))
bloco("B14b",
      doc(W406A, "sinal_2000_26abr", em="Because the buses", literal=False),
      filme("filme_pripyat_rua_vazia_1986.mp4", tin=1.0, em="and the city was told"),
      filme("filme_abc_forsmark_sapato.mp4", tin=0.5, em="and the world was told"))
bloco("B14c",
      kb("hoje_nsc_arco_2018.jpg", "zoom-out", em="And because what was built"),
      doc(LEI13, "radiacao_perigosa", em="on land that the law", literal=False),
      mural(em="Every one of those hours"),
      relogio=("+67:36:20", "oculto"))
bloco("B14d",
      contador("26.04 01:23:40", "+67:36:20", "FROM THAT ANSWER TO FIVE SENTENCES", em="Sixty-seven hours"),
      filme("filme_pripyat_criancas_desfile_1982.mp4", em="If you had been"),
      filme("hoje_blocos_floresta_pripyat_voa.mp4", tin=0.5, em="Tell me in the comments."),
      card(em="This is Clearance Required."),
      relogio=("+67:36:20", "parado"))
bloco("B14e",
      card(),
      relogio=None)

CENAS = []   # nenhuma imagem gerada no corpo (thumbs na etapa 2)


# ===================================================================== validação e saída
def palavras(t):
    return len(re.sub(r"\[[^]]*\]", "", t).split())


def norm(t):
    return " " + re.sub(r"[^a-z0-9]+", " ", t.lower()).strip() + " "


def fmt(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


def arq_real(a):
    return a.split(":", 1)[1].split("@")[0] if a and a.startswith(("filme:", "still:")) else a


def resolve(b, ERROS):
    texto = b["texto"]
    ws = [(m.start(), m.end()) for m in re.finditer(r"\S+", texto)]
    fixos = []
    for i, p in enumerate(b["planos"]):
        if p["em"]:
            k = texto.find(p["em"], fixos[-1][1] + 1 if fixos else 0)
            if k < 0:
                ERROS.append(f"{b['id']}: âncora não encontrada (ou fora de ordem): «{p['em']}»")
                k = fixos[-1][1] + 1 if fixos else 0
            fixos.append((i, k))
    if not fixos or fixos[0][0] != 0:
        fixos.insert(0, (-1, 0)) if not fixos or fixos[0][1] != 0 else None
    pos = [None] * len(b["planos"])
    for i, k in fixos:
        if i >= 0:
            pos[i] = k
    # distribui os sem âncora entre fixos
    marcos = [(i, k) for i, k in fixos] + [(len(b["planos"]), len(texto))]
    if marcos[0][0] != -1 and pos[0] is None:
        marcos.insert(0, (-1, 0))
    for (i0, k0), (i1, k1) in zip(marcos, marcos[1:]):
        livres = list(range(i0 + 1, i1))
        if not livres:
            continue
        grupo = ([i0] if i0 >= 0 else []) + livres
        pesos = [peso(b["planos"][j]) for j in grupo]
        wi = [n for n, (s, e) in enumerate(ws) if k0 <= s < k1]
        if not wi:
            for j in livres:
                pos[j] = k0
            continue
        tot = sum(pesos)
        acc = 0
        for g, j in zip(pesos, grupo):
            if j in livres:
                n = wi[0] + round(len(wi) * acc / tot)
                n = min(n, wi[-1])
                pos[j] = ws[n][0]
            acc += g
    if pos[0] != 0:
        if pos[0] is None or pos[0] > 0:
            ERROS.append(f"{b['id']}: o 1º plano precisa começar no início do bloco (pos {pos[0]})")
            pos[0] = 0
    for j in range(1, len(pos)):
        if pos[j] is None or pos[j] <= pos[j - 1]:
            ERROS.append(f"{b['id']}: plano {j + 1} sem espaço de texto (âncoras muito juntas)")
            pos[j] = (pos[j - 1] or 0) + 1
    return pos


def peso(p):
    if p["tipo"] == "Filme":
        return max(2.0, (p["tout"] - p["tin"]))
    return {"Número": 3.0, "Contador": 3.5, "Cartela": 4.5, "Datilo": 4.0, "Glitch": 1.5, "Card": 4.0}.get(p["tipo"], 4.0)


def main():
    ERROS, AVISOS = [], []
    faltam = set(TEXTO) - {b["id"] for b in B}
    if faltam:
        ERROS.append(f"blocos sem planos: {sorted(faltam)}")
    ordem = [b["id"] for b in SPLIT]
    if [b["id"] for b in B] != [x for x in ordem if x in {b['id'] for b in B}]:
        ERROS.append("blocos fora da ordem do split")

    planos, t = [], 0.0
    for b in B:
        if b["arquivo_antes"]:
            a = ARQUIVOS[b["arquivo_antes"]]
            q = dict(tipo="Arquivo", arq=a["fundo"] or "codigo", enq="arquivo:" + b["arquivo_antes"], bloco=b["arquivo_antes"], frase="(áudio de época)",
                     inicio=round(t, 2), dur=a["dur"], selo=a["selo"], legenda=a["legenda"], fonte=a["fonte"], trecho=a["trecho"], em="")
            planos.append(q)
            t += a["dur"]
        texto = b["texto"]
        pos = resolve(b, ERROS)
        b["inicio"], b["dur"] = round(t, 2), round(palavras(texto) / WPS, 2)
        for k, p in enumerate(b["planos"]):
            fim = pos[k + 1] if k + 1 < len(pos) else len(texto)
            frase = texto[pos[k]:fim].strip()
            d = max(palavras(frase), 1) / WPS
            q = dict(p)
            q.update(bloco=b["id"], frase=frase, inicio=round(t, 2), dur=round(d, 2), relogio=b["relogio"])
            q["em"] = frase[:40]
            planos.append(q)
            t += d
    total = t

    for q in planos:
        for campo in ("arq", "arq2"):
            arq = arq_real(q.get(campo))
            if not arq or arq == "codigo":
                continue
            if not (MIDIA / arq).exists():
                ERROS.append(f"{q['bloco']}: arquivo inexistente em midia/: {arq}")
            if not arq.startswith("doc_") and arq not in CSV:
                ERROS.append(f"{q['bloco']}: arquivo fora do midia.csv: {arq}")
            if arq.startswith("doc_") and arq not in DOCS:
                ERROS.append(f"{q['bloco']}: documento sem posição em tools/docs_pos.json: {arq}")
        a = arq_real(q.get("arq"))
        if a and a in CSV:
            q["ficha"], q["credito"] = CSV[a]["ficha"], CSV[a]["credito"]
        if q["tipo"] == "KenBurns" and q["dur"] > 8.5:
            AVISOS.append(f"{q['bloco']}: KenBurns longo ({q['dur']:.1f} s) em {q['arq']}")
        if q["tipo"] == "DocGrifo":
            if q["literal"] and norm(q["frase_doc"])[1:-1] not in norm(q["frase"])[1:-1]:
                ERROS.append(f"{q['bloco']}: grifo literal «{q['frase_doc'][:50]}» não é lido na narração do plano «{q['frase'][:60]}»")
            if q["dur"] > 9:
                AVISOS.append(f"{q['bloco']}: DocGrifo longo ({q['dur']:.1f} s) em {q['arq']}")
        if q["tipo"] == "Filme":
            seg = q["tout"] - q["tin"]
            if seg <= 0:
                ERROS.append(f"{q['bloco']}: filme sem duração no midia.csv: {q['arq']}")
                continue
            if seg + 0.15 < q["dur"]:
                vel = seg / q["dur"]
                if vel >= FILME_VEL_MIN:
                    q["vel"] = round(vel, 3)
                else:
                    ERROS.append(f"{q['bloco']}: clipe curto ({seg:.1f} s, mesmo a {FILME_VEL_MIN}×) para {q['dur']:.1f} s: {q['arq']} «{q['frase'][:50]}»")

    # tipo de tela seguido
    run_t, run_tipo, run_ini = 0.0, None, None
    for q in planos:
        d = q["dur"]
        if q["tipo"] == run_tipo:
            run_t += d
        else:
            run_tipo, run_t, run_ini = q["tipo"], d, q
        lim = RUN_MAX_FOTO if run_tipo in ("KenBurns", "DocGrifo", "Filme", "Dupla") else (45.0 if run_tipo == "Arquivo" else RUN_MAX)
        if run_t > lim + 1e-6:
            ERROS.append(f"{q['bloco']}: {run_tipo} por {run_t:.1f} s seguidos (desde {run_ini['bloco']} «{run_ini['em'][:30]}»); máximo {lim:.0f} s")

    # reuso
    vistos, ult = {}, {}
    ant = None
    reuso_t = 0.0
    for q in planos:
        arqs = [arq_real(a) for a in [q.get("arq"), q.get("arq2")] if a and a != "codigo"]
        q["reuso"] = False
        for a in arqs:
            ch = (a, q["enq"])
            if ch in ult and q["inicio"] - ult[ch] < JANELA and ant != a:
                AVISOS.append(f"{q['bloco']}: {a} [{q['enq']}] repetido em menos de {JANELA:.0f} s")
            if a in vistos and ant != a:
                q["reuso"] = True
                if q["inicio"] < INEDITO_ATE and a not in REUSO_LIBERADO:
                    AVISOS.append(f"{q['bloco']}: reuso de {a} antes de 3:00 ({fmt(q['inicio'])})")
            vistos.setdefault(a, q["inicio"])
            ult[ch] = q["inicio"] + q["dur"]
        if q["reuso"]:
            reuso_t += q["dur"]
        ant = arqs[-1] if arqs else None

    # métricas
    def epoca(a):
        a = arq_real(a) or ""
        return a.startswith(("foto_", "filme_")) and a in CSV
    REAL = {"KenBurns", "DocGrifo", "EntaoAgora", "Dupla", "Filme"}
    real_t = sum(q["dur"] for q in planos if q["tipo"] in REAL or (q["tipo"] == "Arquivo" and q["arq"] != "codigo"))
    epoca_t = sum(q["dur"] for q in planos if (q["tipo"] in ("KenBurns", "Filme", "Arquivo") and epoca(q["arq"]))
                  or (q["tipo"] in ("EntaoAgora", "Dupla") and epoca(q["arq"])))
    filme_epoca_t = sum(q["dur"] for q in planos if q["tipo"] in ("Filme", "Arquivo") and epoca(q["arq"]) and arq_real(q["arq"]).endswith(".mp4"))
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
    if real_t / total < REAL_MIN:
        ERROS.append(f"material real {real_t / total:.1%} < {REAL_MIN:.0%}")
    if epoca_t / total < EPOCA_MIN:
        ERROS.append(f"foto/vídeo de época {epoca_t / total:.1%} < {EPOCA_MIN:.0%} (decisão do Rodrigo)")

    for i, q in enumerate(planos, 1):
        q["id"] = f"P{i:03d}"
        q["real"] = q["tipo"] in REAL
        q["epoca"] = bool(epoca(q.get("arq")))
    stats = dict(planos=len(planos), duracao_s=round(total, 1), duracao=fmt(total), planos_por_min=round(len(planos) / (total / 60), 1),
                 real_pct=round(100 * real_t / total, 1), epoca_pct=round(100 * epoca_t / total, 1), filme_epoca_pct=round(100 * filme_epoca_t / total, 1),
                 reuso_pct=round(100 * reuso_t / total, 1), componentes=cont, docs_distintos=len(docs), docs_grifados=len(docs_grifo),
                 citacoes_literais=len(lidos), numeros=n_num, mapas_distintos=len(mapas), entao_agora=n_ea, imagens_ia=len(CENAS),
                 palavras=sum(palavras(b["texto"]) for b in B), blocos_audio=len(B), arquivos_epoca_s=sum(a["dur"] for a in ARQUIVOS.values()))
    blocos = [dict(id=b["id"], texto=b["texto"], ideia=b["ideia"], inicio_est=b["inicio"], dur_est=b["dur"], arquivo_antes=b["arquivo_antes"],
                   relogio=b["relogio"]) for b in B]
    chaves = ["id", "bloco", "tipo", "arq", "arq2", "enq", "inicio", "dur", "frase", "real", "epoca", "reuso", "ficha", "credito", "num", "de", "para",
              "crop", "frase_doc", "grifo", "literal", "legenda", "valor", "rotulo", "nome", "pontos", "linhas", "selo", "nota", "pluma",
              "rot1", "rot2", "em", "tin", "tout", "vel", "de_t", "ate_t", "valores", "rotulos", "relogio", "fonte", "trecho"]
    sb = [{k: q[k] for k in chaves if k in q and q[k] is not None} for q in planos]
    (AQUI / "blocos.json").write_text(json.dumps(blocos, ensure_ascii=False, indent=1) + "\n")
    (AQUI / "storyboard.json").write_text(json.dumps(dict(stats=stats, pontos=PT, arquivos=ARQUIVOS, planos=sb), ensure_ascii=False, indent=1) + "\n")
    (AQUI / "cenas.json").write_text(json.dumps(CENAS, ensure_ascii=False, indent=1) + "\n")

    L = ["# STORYBOARD: 006-chernobyl (lugares-guerra-en, \"Clearance Required\")", "",
         "Gerado por `roteiro.py` (não editar à mão). Tempos estimados a 168 ppm (voz Narrator) + áudios de época com a duração prevista; "
         "recalcular com o áudio real no `build.py` da etapa 2.",
         f"**{stats['planos']} planos · {stats['duracao']} · {stats['planos_por_min']} planos/min · material real {stats['real_pct']}% · "
         f"**foto/vídeo de época {stats['epoca_pct']}%** (vídeo de época {stats['filme_epoca_pct']}%) · reuso {stats['reuso_pct']}% · imagens IA {len(CENAS)}**", "",
         "Componentes: " + ", ".join(f"{k} {v}" for k, v in sorted(cont.items())) +
         f" · docs distintos {len(docs)} (grifados {len(docs_grifo)}, citações lidas literalmente {len(lidos)}) · Números {n_num} · mapas {len(mapas)} · EntaoAgora {n_ea}",
         "", "Overlay persistente (amostra): régua de horas 26–28/04 no topo + contador duplo (decorrido desde 01:23:40 · hora local de Chernobyl); "
         "estado por bloco na coluna «relógio» (`corre` = contador correndo; `parado`; `oculto` = sem overlay). Crédito na tela = coluna `credito` do midia.csv "
         "(canto inferior esquerdo, Plex Mono 20 px, como na amostra).", ""]
    for b in B:
        if b["arquivo_antes"]:
            a = ARQUIVOS[b["arquivo_antes"]]
            L.append(f"### {b['arquivo_antes']} · áudio de época · {a['dur']:.0f} s · {a['selo']}")
            L.append(f"Fonte: {a['fonte']} · trecho {a['trecho']} · fundo: `{a['fundo'] or 'tela quase preta + onda'}`")
            L.append("Legenda: " + " / ".join(a["legenda"]))
            L.append("")
        L.append(f"## {b['id']} [{fmt(b['inicio'])}]{' · IDEIA' if b['ideia'] else ''}{' · relógio ' + str(b['relogio']) if b['relogio'] else ''}")
        L.append(f"> {b['texto']}")
        L.append("")
        L.append("| # | t | s | tela | material / parâmetros | cobre |")
        L.append("|---|---|---|---|---|---|")
        for q in [q for q in planos if q["bloco"] == b["id"]]:
            L.append(f"| {q['id']} | {fmt(q['inicio'])} | {q['dur']:.1f} | {q['tipo']}{' ♻' if q['reuso'] else ''}{' ★' if q['epoca'] else ''} | {descr(q)} | "
                     f"{q['frase'][:80]}{'…' if len(q['frase']) > 80 else ''} |")
        L.append("")
    L.append("♻ = reuso planejado · ★ = foto/vídeo real de época (conta para a meta de 40%).")
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
    cr = f" · crédito «{q['credito']}»" if q.get("credito") else ""
    fx = f" · Ficha: {q['ficha']}" if q.get("ficha") else ""
    nm = f" · Número «{q['num'][0]} {q['num'][1]}»" if q.get("num") else ""
    if t == "KenBurns":
        return f"`{q['arq']}` {q['enq']}{fx}{nm}{cr}"
    if t == "Filme":
        v = f" @{q['vel']}×" if q.get("vel", 1) != 1 else ""
        return f"`{q['arq']}` {q['tin']:.1f}–{q['tout']:.1f} s{v}{fx}{nm}{cr}"
    if t == "DocGrifo":
        g = f"grifo «{q['frase_doc'][:60]}»" if q.get("frase_doc") else (f"grifo [{q['enq']}]" if q["grifo"] else "página/zoom")
        lg = f" · legenda en «{q['legenda'][:70]}…»" if q.get("legenda") else ""
        return f"`{q['arq']}` {g}{'' if q['literal'] else ' (não literal)'}{lg}{nm}"
    if t == "Arquivo":
        return f"onda + legenda + selo «{q['selo']}» · fundo `{q['arq']}`"
    if t == "Número":
        return f"código: **{q['valor']}** {q['rotulo']}"
    if t == "Contador":
        return f"código: contador duplo {q['de_t']} → {q['ate_t']} «{q['rotulo']}»"
    if t == "Mapa2D":
        return f"mapa {q['nome']} ({', '.join(q['pontos'])}){' · pluma animada' if q.get('pluma') else ''}{' · Selo ' + q['selo'] if q.get('selo') else ''}"
    if t in ("Cartela", "Datilo", "Teletipo"):
        return f"código: {t.lower()} «{' / '.join(q['linhas'])[:110]}»{' · Selo ' + q['selo'] if q.get('selo') else ''}"
    if t == "EntaoAgora":
        return f"`{q['arq']}` ({q['rot1']}) × `{q['arq2']}` ({q['rot2']})"
    if t == "Dupla":
        return f"`{q['arq']}` «{q['rot1']}» | `{q['arq2']}` «{q['rot2']}»"
    if t == "TresRelogios":
        return "código: 3 relógios lado a lado " + " · ".join(f"{v} {r}" for v, r in zip(q["valores"], q["rotulos"]))
    if t == "Mural":
        return "código: zoom-out revela o mural inteiro (payoff da amostra)"
    if t == "Glitch":
        return "código: glitch de sinal → silêncio (sem imagem de explosão)"
    if t == "Card":
        return "código: cartela final do canal (Clearance Required + inscrever)"
    return ""


if __name__ == "__main__":
    main()
