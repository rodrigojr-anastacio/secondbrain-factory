# Roteiro do 006 (Em Relevo): Caraguatatuba 1967 × São Sebastião 2023 — por que a Serra do Mar desaba sobre o litoral.
# Fonte única do texto -> shared/blocos.json. Base: EMBALAGEM.md + CRIVO.md (aprovado r3, 17/11/2026), ANGULO.md e pesquisa/FATOS.md.
# Formato igual ao 005: id, cap (aba), marcha (1 = hook mais rápido), fala (limpa, números por extenso), fala_tts (tags v3 + extenso),
# tela (algarismos; "|" separa os cartões da legenda), fonte (IDs de pesquisa/FATOS.md), ideia (abre ideia nova).
# Aqui o texto-fonte de cada bloco é escrito com algarismos; o extenso é gerado por ext() (normaliza_pt.py) — anos e números inteiros.
# Promessa (EMBALAGEM): ver no relevo 3D por que a Serra do Mar desce sobre o litoral norte (parede + chuva que ela fabrica + casca de terra)
# e como a mesma receita fez Caraguatatuba 1967 e São Sebastião 2023. Frase-âncora no b03 (< 0:30). T3 ("casca") dito até 1:00 (b06).
# Fio condutor: os 3 ingredientes da receita, um por capítulo, provados em 1967 (cap. 4) e em 2023 (cap. 5); a resposta junta tudo.
# Sem minuto a minuto de 1967, sem rádio amador/ponte como cena (consenso da manada, ANGULO.md); sem "morte" no título; sem próximo vídeo.
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from normaliza_pt import ext

B = []
TAG = re.compile(r"\[[a-z ]+\]\s*")

def extenso(s):
    s = re.sub(r"(\d+)\s*%", lambda m: m.group(1) + " por cento", s)
    return re.sub(r"\d+", lambda m: ext(int(m.group(0))), s)

def b(cap, texto, fonte="", ideia=False, tts_extra=None):
    """texto: com algarismos e tags [serious]/[curious]; frases separadas por '\\n' viram cartões da legenda."""
    texto = texto.strip()
    linhas = [l.strip() for l in texto.split("\n") if l.strip()]
    tela = " | ".join(TAG.sub("", l) for l in linhas)
    tts = extenso(" ".join(linhas)) if tts_extra is None else tts_extra
    B.append({"id": f"b{len(B)+1:02d}", "cap": cap, "marcha": 1 if len(B) < 6 else 2,
              "fala": TAG.sub("", tts).strip(), "fala_tts": tts, "tela": tela, "fonte": fonte, "ideia": ideia})

C1 = "1 · A PAREDE"
C2 = "2 · A CHUVA QUE A SERRA FABRICA"
C3 = "3 · A CASCA DA SERRA"
C4 = "4 · 1967: O CAMINHO ATÉ A CIDADE"
C5 = "5 · 2023: A MESMA RECEITA"
R = "A RESPOSTA"

# ---------------- HOOK (frase-âncora até ~0:30; parede + 3 ingredientes + "casca" até ~1:00) ----------------
b("BERTIOGA (SP) · 18–19 FEV 2023",
  "Fevereiro de 2023.\nEm Bertioga, 683 milímetros de chuva em 24 horas.\nEm Caraguatatuba, ali perto, no mesmo dia: 234.",
  "C3", ideia=True)
b("SÃO SEBASTIÃO (SP) · 19 FEV 2023",
  "Em São Sebastião, 627.\nDepois, o satélite mostrou as encostas rasgadas até as casas.",
  "C3, S2")
b("SÃO SEBASTIÃO × CARAGUATATUBA",
  "Ponha lado a lado o relevo de São Sebastião e o de Caraguatatuba, onde a serra cedeu em 1967.\nO mesmo degrau: 700 metros em menos de 6 quilômetros.\n[serious] Não foi azar: a receita está no relevo.",
  "R2, R3 (perfis SRTM próprios), K1")
b("O MAPA",
  "[curious] Por que a Serra do Mar desaba sobre o litoral?\nE por que ela repete?\nA resposta está no mapa.",
  "pergunta do T1/T2", ideia=True)
b("O MAPA",
  "Olhe de lado, do mar para a serra.\nPrimeiro, uma faixa estreita de areia, onde ficam as cidades.\nDepois, a parede. Em cima dela, o planalto.",
  "R2, R4", ideia=True)
b("O MAPA",
  "A receita cabe em 3 números.\n700 metros de parede a menos de 6 quilômetros do mar.\nAté 400 milímetros de chuva em 6 horas, numa faixa de poucos quilômetros.\nE uma casca de terra de 1 a 2 metros e meio, solta sobre a rocha.",
  "R2, C4, P2")
b("O MAPA",
  "Depois de 1967, a geógrafa Olga Cruz, da USP, mediu encosta por encosta dessa serra.\nVamos juntar o que ela mediu com o que o satélite viu em 2023.",
  "P12; Cruz 1975")

# ---------------- 1. A PAREDE ----------------
b(C1,
  "Comece pela altura.\nAtrás de Caraguatatuba, a borda do planalto fica entre 750 e 900 metros.\nE ela está perto demais do mar.",
  "R4", ideia=True)
b(C1,
  "Suba a câmera pelo vale do Rio Santo Antônio, o rio que corta a cidade.\nA 7 quilômetros e meio da praia, você já está a 750 metros de altura.\nNo Morro do Cruzeiro, colado no centro, a encosta passa de 30 graus.",
  "R1, R2 (perfis SRTM próprios)")
b(C1,
  "A bacia desse rio é pequena: uns 30 quilômetros quadrados.\nMas mais da metade dela tem declive acima de 40%.\nÉ água que nasce no alto e chega ao mar em minutos, não em dias.",
  "R7")
b(C1,
  "Mais para trás, a serra de Juqueriquerê passa de 1300 metros.\nSegundo os geólogos, toda essa borda é a beirada de um bloco da crosta que se partiu quando o Atlântico se abriu.\nO degrau que se vê no mapa é o que sobrou dessa fratura.",
  "R4 (Cruz 1975), R6 (Almeida & Carneiro 1998, via resumos; sem idade)", ideia=True)
b(C1,
  "E ela não é só de Caraguatatuba.\nAtrás da Barra do Sahy, em São Sebastião, o mesmo degrau: quase 700 metros a 5 quilômetros e meio da areia.\nGuarde esse lugar.",
  "R3 (perfil SRTM próprio)")

# ---------------- 2. A CHUVA QUE A SERRA FABRICA ----------------
b(C2,
  "Agora, a chuva.\nVeja o mapa dos pluviômetros na noite de 18 para 19 de fevereiro de 2023.\nBertioga, 683. São Sebastião, 627. Caraguatatuba, 234. Ubatuba, 335.",
  "C3 (CEMADEN via Kobiyama/GADRI)", ideia=True)
b(C2,
  "[intrigued] O temporal não cobriu o litoral por igual.\nEle se concentrou numa faixa de poucos quilômetros, justo onde a parede fica mais perto do mar.\nÉ o ar úmido do oceano subindo a serra, esfriando e despejando tudo ali.",
  "C1, C3, R3")
b(C2,
  "Tão estreita que o satélite de chuva da NASA, que enxerga em quadrados de 10 quilômetros, estimou menos de 110 milímetros na região.\nO pico não cabia no quadrado.",
  "C7 (IMERG, cálculo próprio)")
b(C2,
  "Por que naquela noite?\nSegundo pesquisadores do IAG, da USP, uma frente fria e um pequeno ciclone no mar seguraram as nuvens por horas no mesmo lugar.\nO oceano estava mais quente que o normal, e o vento, batendo na serra, reforçou a chuva.",
  "C2 (Pesquisa FAPESP 326)", ideia=True)
b(C2,
  "Em Bertioga, foram mais de 400 milímetros em 6 horas.\nA média de fevereiro inteiro, ali, fica perto de 225.\nNo dia, o CEMADEN registrou o maior acumulado de 24 horas já medido no país.",
  "C4, C5 (Kobiyama/GADRI, CEMADEN)")
b(C2,
  "Em 1967, a chuva começou no dia 16 de março.\nNo pluviômetro de uma fazenda de Caraguatatuba, foram 115 milímetros no dia 17 e 420 no dia 18.\nE o aparelho transbordou: o número real foi maior.",
  "C8 (Cruz 1975, p. 103)", ideia=True)
b(C2,
  "Num posto a poucos quilômetros, o pluviômetro marcou menos da metade disso nos mesmos dois dias.\nNa serra, a chuva muda de vale para vale.\nE onde ela despeja tudo, entra o terceiro ingrediente.",
  "C10 (Vieira 2022, postos DAEE)")

# ---------------- 3. A CASCA DA SERRA ----------------
b(C3,
  "Comece pela medida.\nNas cicatrizes de Caraguatatuba, o plano onde a terra se soltou fica entre 1 e 2 metros e meio de profundidade.\nAcima dele, rocha decomposta e terra. Abaixo, granito e gnaisse.",
  "P2, P6 (corte ilustrativo)", ideia=True)
b(C3,
  "Para uma serra de 700 metros, é uma película.\nA floresta inteira, com árvores de muitos metros, está plantada nessa camada.\nE é ali, no contato com a rocha, que a casca se descola.",
  "P2 (De Ploey & Cruz 1979; Vieira 2022)")
b(C3,
  "Os pesquisadores levaram essa terra para o laboratório.\nMediram coesão quase zero: é um solo quase sem cola.\nEncharcado, ele desliza sobre a rocha. Em 1967, em muitas encostas, o escorregamento raspou até a rocha sã.",
  "P10, P3 (Vieira 2022)")
b(C3,
  "Agora, o mapa de Olga Cruz.\nEla desenhou a declividade de toda a bacia do Santo Antônio.\nAs encostas que mais cederam passavam de 40% de declive. Os topos planos ficaram de pé.",
  "P5, P12 (Cruz 1975, carta de declividade)", ideia=True)
b(C3,
  "Um estudo da USP de 2017 cruzou as cicatrizes de 1967 com o mapa geológico.\n8 em cada 10 estão sobre a mesma rocha, o granito de Caraguatatuba.\nA receita tem até um endereço geológico.",
  "P4, P6 (Dias, Dias & Vieira 2017)")
b(C3,
  "É isto que sobra quando a casca se solta.\nUbatuba, fevereiro de 2023: terra viva exposta, raízes no ar, a beira da estrada levada junto.\nAgora imagine isso em centenas de encostas, na mesma noite.",
  "foto Defesa Civil de Ubatuba/Gov. SP (CC BY 2.0), 19/02/2023")

# ---------------- 4. 1967: O CAMINHO ATÉ A CIDADE ----------------
b(C4,
  "Volte a março de 1967 e olhe de cima a bacia do Santo Antônio.\nCom a casca encharcada por dias, as encostas começaram a escorregar em todos os vales.",
  "K1, K2", ideia=True)
b(C4,
  "Anos depois, em fotos aéreas, os pesquisadores contaram 640 cicatrizes, num raio de até 15 quilômetros.\nCerca de 2 milhões de toneladas de terra, rocha e árvores se moveram.\nUm quinto da floresta da área estudada foi junto.",
  "P7, P8, P9")
b(C4,
  "Cada escorregamento descia até o fundo do vale e seguia pelo leito do rio, misturado com água e troncos.\nOlga Cruz registrou isso como avalanche de detritos. Os moradores diziam que o morro tinha rodado.\nE todos os vales da bacia levam ao mesmo lugar: a planície onde está a cidade.",
  "P1, K2", ideia=True)
b(C4,
  "Os pesquisadores dividem aquele 18 de março em 4 fases.\nPrimeiro, a enchente dos rios. Depois, os escorregamentos. Depois, as corridas de detritos.\nE, por fim, uma nova enchente, quando os troncos represaram os canais.",
  "P11 (Gramani 2001)")
b(C4,
  "O Rio Santo Antônio, que tinha de 10 a 20 metros de largura, abriu para 60 a 80.\nAs ruas ficaram com até 80 centímetros de lama e dezenas de milhares de troncos, alguns com mais de 1 metro de diâmetro.",
  "K3, K4 (Cruz 1975)")
b(C4,
  "O número de vítimas nunca fechou.\nA geógrafa estimou 120. Contagens da época chegaram perto de 500.\nE, segundo um estudo de 2020, a maior parte da planície ainda era fazenda. Se fosse cidade, o estrago teria sido muito maior.",
  "K6, K7", ideia=True)
b(C4,
  "Agora, a carta do Serviço Geológico do Brasil.\nEla marca as encostas de alta suscetibilidade a deslizamento, e é ao pé delas que está a cidade.\nNa planície, onde em 1967 havia fazenda, o censo de 2022 contou quase 135 mil moradores.",
  "M1 (SGB), P12, K7, K8 (IBGE 2022)")

# ---------------- 5. 2023: A MESMA RECEITA ----------------
b(C5,
  "Agora, compare com 2023.\nO satélite Landsat fotografou as encostas de São Sebastião em outubro de 2022 e de novo uma semana depois da chuva.",
  "S2 (NASA Earth Observatory)", ideia=True)
b(C5,
  "Antes: morro verde, contínuo, até a praia.\nDepois: dezenas de faixas de terra descendo, uma ao lado da outra, até as casas.\nCada faixa é uma casca que se soltou.",
  "S2")
b(C5,
  "Coloque os ingredientes em cima.\nA parede: quase 700 metros a 5 quilômetros e meio da Barra do Sahy.\nA chuva: 627 milímetros em um dia. E a mesma casca fina sobre a rocha.",
  "R3, C3, P2")
b(C5,
  "Um especialista em deslizamentos da NASA resumiu assim: áreas com tantos escorregamentos juntos são bem incomuns, mas não sem precedente.\nO precedente fica a 35 quilômetros, em Caraguatatuba.",
  "S3, S7")
b(C5,
  "Em São Sebastião e em Ubatuba, 65 pessoas morreram.\nMais de 1800 ficaram desabrigadas, e mais de 2200 tiveram de sair de casa.",
  "S1 (Kobiyama/GADRI)")

# ---------------- A RESPOSTA ----------------
b(R,
  "Então, por que a Serra do Mar desaba sobre o litoral?\nPorque ela sobe 700 metros a menos de 6 quilômetros do mar e prende o temporal numa faixa estreita, onde cabem 400 milímetros em 6 horas.\nE porque está coberta por uma casca de 1 a 2 metros e meio, quase sem cola, que escorrega quando encharca.",
  "síntese R1–R3, C1–C4, P2", ideia=True)
b(R,
  "Não é a montanha que cai de uma vez.\nÉ a casca que desliza, encosta por encosta, e desce pelos vales até a planície, onde estão as cidades.\nNo Morro do Cruzeiro e na Barra do Sahy, o degrau medido é o mesmo: quase 700 metros a menos de 6 quilômetros da areia.",
  "síntese K2, S2")
b(R,
  "Ninguém sabe dizer quando vai cair outra chuva assim, nem em qual trecho da serra.\nMas a geografia não muda, e o mapa de onde ela cede já existe, para Caraguatatuba e para São Sebastião.",
  "M1 (SGB); fecho sem previsão", ideia=True)
b(R,
  "E, no censo de 2010, o IBGE contou cerca de 3 mil moradores de Caraguatatuba dentro de áreas de risco mapeadas.\nO que muda o resultado é o aviso chegar a tempo.",
  "M2 (IBGE/CEMADEN 2018)")
b(R,
  "A Defesa Civil manda alertas por SMS.\nPara receber, mande o seu CEP para o número 40199.\nE, se o alerta disser para sair, saia: quando a casca começa a descer, não dá tempo.",
  "M3 (SMS 40199, Defesa Civil)",
  tts_extra="A Defesa Civil manda alertas por SMS. Para receber, mande o seu CEP para o número quarenta mil cento e noventa e nove. E, se o alerta disser para sair, saia: quando a casca começa a descer, não dá tempo.")
b(R,
  "Se você quer ver outro desastre brasileiro explicado no mapa, o vídeo da seca de 1877 está aqui no canal.\nSe você tem família no litoral norte de São Paulo, manda este vídeo para ela.\nE se inscreve no Em Relevo, para entender o clima do Brasil no mapa.",
  "CTA: puxa sessão para I5KpDKy6r3E (seca 1877, publicado); sem gancho de próximo vídeo")

if __name__ == "__main__":
    json.dump(B, open(Path(__file__).parent / "blocos.json", "w"), ensure_ascii=False, indent=1)
    n = sum(len(re.findall(r"\w+", x["fala"])) for x in B)
    ch = sum(len(x["fala_tts"]) for x in B)
    print(len(B), "blocos;", n, "palavras faladas;", ch, "caracteres para o TTS")
    t = 0.4
    for x in B:
        w = len(re.findall(r"\w+", x["fala"]))
        r = 3.3 if x["marcha"] == 1 else 2.9      # hook a ~1,36× (bíblia voz.md: ~198 pal/min) × corpo ~173
        print(f'{x["id"]} {int(t//60)}:{t%60:04.1f} {w:3d}p {x["cap"]}')
        t += w / r + 0.6
    print(f"total estimado {int(t//60)}:{t%60:04.1f}")
