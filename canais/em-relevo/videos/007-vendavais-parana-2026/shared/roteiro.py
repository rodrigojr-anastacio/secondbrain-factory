# Roteiro do 007 (Em Relevo): o temporal de 20/11/2026 no Paraná — por que o temporal entra pelo oeste (e de novo pelo mesmo lado).
# Fonte única do texto -> shared/blocos.json. Base: EMBALAGEM.md + CRIVO.md (aprovado r3, 22/11/2026), ANGULO.md e pesquisa/FATOS.md.
# Formato igual ao 006: id, cap (aba), marcha (1 = hook mais rápido), fala (limpa, por extenso), fala_tts (tags v3 + extenso),
# tela (algarismos; "|" separa os cartões da legenda), fonte (IDs de pesquisa/FATOS.md), ideia (abre ideia nova).
# Promessa (EMBALAGEM): o caminho do temporal de 20/11 (Capanema 13h45 → Cornélio Procópio 20h15) e por que os temporais entram
# pelo oeste do Paraná, o mesmo lado de Rio Bonito do Iguaçu em 2025. Frase-âncora no b04 (< 0:40). Reta + exceções até ~1:15 (b05–b07).
# Fio condutor: a linha das rajadas (pontos → reta → estica até o Paraguai → deita na escada do relevo → ganha a trilha de 2025 → engrossa em novembro).
# Fora: explicação continental completa (é o nosso 001), "2º corredor do mundo", Fujita degrau a degrau, vítimas (consenso da manada, ANGULO.md).
# Sem "morte" no título; sem próximo vídeo; CTA puxa o 001 (bG6-E4qjXYc, publicado).
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from normaliza_pt import ext

B = []
TAG = re.compile(r"\[[a-z ]+\]\s*")

def extenso(s):
    s = re.sub(r"(\d+)h(\d\d)", lambda m: ext(int(m.group(1))) + " e " + ext(int(m.group(2))), s)
    s = re.sub(r"(\d+)h\b", lambda m: ext(int(m.group(1))) + " horas", s)
    s = re.sub(r"(\d{1,3})\.(\d{3})\b", lambda m: m.group(1) + m.group(2), s)
    s = re.sub(r"(\d+),(\d+)", lambda m: ext(int(m.group(1))) + " vírgula " + ext(int(m.group(2))), s)
    s = re.sub(r"(\d+)\s*%", lambda m: m.group(1) + " por cento", s)
    s = s.replace("km/h", "quilômetros por hora").replace(" km", " quilômetros").replace(" mm", " milímetros")
    s = s.replace("°C", " graus").replace("F1", "éfe um").replace("F2", "éfe dois").replace("F4", "éfe quatro")
    s = s.replace("GOES-19", "GOES dezenove").replace("TRMM", "T R M M").replace("NOAA", "NOA").replace("SMS", "ésse-ême-ésse")
    s = s.replace("CEP", "cép")
    return re.sub(r"\d+", lambda m: ext(int(m.group(0))), s)

def b(cap, texto, fonte="", ideia=False, tts_extra=None):
    """texto: com algarismos e tags [serious]/[curious]; frases separadas por '\\n' viram cartões da legenda."""
    texto = texto.strip()
    linhas = [l.strip() for l in texto.split("\n") if l.strip()]
    tela = " | ".join(TAG.sub("", l) for l in linhas)
    tts = extenso(" ".join(linhas)) if tts_extra is None else tts_extra
    B.append({"id": f"b{len(B)+1:02d}", "cap": cap, "marcha": 1 if len(B) < 4 else 2,
              "fala": TAG.sub("", tts).strip(), "fala_tts": tts, "tela": tela, "fonte": fonte, "ideia": ideia})

C1 = "1 · O RASTRO DE UMA TARDE"
C2 = "2 · DE ONDE ELE VEM"
C3 = "3 · A ESCADA DO PARANÁ"
C4 = "4 · O MESMO LADO"
C5 = "5 · POR QUE TANTO AGORA"
R = "A RESPOSTA"

# ---------------- HOOK (frase-âncora até ~0:40) ----------------
b("CAPANEMA (PR) · 20 NOV 2026 · 13H45",
  "[serious] Sexta-feira, 20 de novembro, 13h45.\nCapanema, na fronteira com a Argentina.\nA estação do Simepar mede uma rajada de 81,7 km/h.",
  "E4", ideia=True)
b("CORNÉLIO PROCÓPIO (PR) · 20H15",
  "6 horas e meia depois, a 423 km dali, Cornélio Procópio: 98,3 km/h, o vento mais forte do dia.\nNo meio do caminho, dois tornados: em Foz do Iguaçu e em Manoel Ribas.",
  "E4, N2, E2")
b("RIO BONITO DO IGUAÇU · 7 NOV 2025",
  "E não era a primeira vez.\nHá um ano, outro temporal entrou pelo mesmo lado do estado e passou por Rio Bonito do Iguaçu.",
  "B1")
b("O MAPA",
  "[curious] Por que o temporal entra pelo oeste do Paraná, de novo pelo mesmo lado?\nA resposta está no mapa.",
  "pergunta do T1/T3 (frase-âncora)", ideia=True)

# ---------------- 1º minuto: as estações viram uma reta ----------------
b(C1,
  "Ponha no mapa as estações do Simepar daquela sexta.\nCada uma acende na hora do seu pico de vento.",
  "E4", ideia=True)
b(C1,
  "Capanema, 13h45. Santa Helena, 15h15. Cascavel, 16h15.\nCampo Mourão, 17h45. Maringá, 18h45. Londrina, 19h30.\nCornélio Procópio, 20h15.\nOs pontos não acendem ao acaso: andam numa linha, do sudoeste para o nordeste.",
  "E4, N1")
b(C1,
  "Duas estações fugiram da fila: Paranaguá, à 1 e 15 da tarde, e Cambará, às 2.\nEram outras células: o Simepar falou em diversas linhas de instabilidade.\nMas a linha principal está aqui.",
  "E4, E3",
  tts_extra="Duas estações fugiram da fila: Paranaguá, à uma e quinze da tarde, e Cambará, às duas. Eram outras células: o Simepar falou em diversas linhas de instabilidade. Mas a linha principal está aqui.")
b(C1,
  "Faça a conta com as 14 estações da fila.\nO pico chega mais tarde quanto mais a nordeste está a estação, quase sem desvio.\nSão uns 430 km de ponta a ponta, a uns 70 km/h.\nA velocidade de um carro na estrada.",
  "N1 (regressão própria, r² 0,98)")
b(C1,
  "Foi isso que atravessou o Paraná em 6 horas e meia.\nNão um vento parado sobre o estado: uma faixa de tempestades andando.",
  "N1, N2")
b(C1,
  "Por volta das 3 da tarde, a faixa passa por Foz do Iguaçu.\nNa Vila Yolanda, o Simepar confirmou um tornado F1, com vento estimado entre 117 e 180 km/h.\nPor volta das 6, outro F1, na zona rural de Manoel Ribas.",
  "E2", ideia=True)
b(C1,
  "Às 20h02, a Copel chegou a 353.849 imóveis sem energia.\nNo dia seguinte, a Defesa Civil contava 9 municípios atingidos e 249 imóveis danificados, quase metade em Foz.",
  "E5, E6")
b(C1,
  "Em Foz, a Defesa Civil contou umas 50 árvores no chão e distribuiu lonas para cerca de 200 famílias. Os destelhamentos se concentraram na Vila Yolanda.\nE, na manhã seguinte, a região com mais casas ainda sem luz era o Oeste: 26,8 mil.",
  "E7, E5")
b(C1,
  "E repare: o oeste levou o temporal à tarde. O norte, à noite.\nA velocidade da faixa explica isso. Já chegamos lá.",
  "E4 (loop: pago no b26)")

# ---------------- 2 · DE ONDE ELE VEM ----------------
b(C2,
  "Agora suba a câmera e olhe para trás, para o oeste.\nNa véspera, o Simepar já avisava: um sistema de baixa pressão se intensificava sobre o Paraguai,\ne o tempo mudaria primeiro no Oeste e no Sudoeste do Paraná.",
  "E1", ideia=True)
b(C2,
  "O satélite GOES-19, da NOAA, fotografa a região a cada 10 minutos.\nÀs 9 da manhã, já havia um aglomerado de tempestades a oeste do Paraná.\nÀs 8 da noite, era uma faixa de topos gelados atravessando o estado.",
  "E9 (posição a conferir com o NetCDF georreferenciado, etapa 2)")
b(C2,
  "Esse canto do mapa, entre o Paraguai, o norte da Argentina e o Sul do Brasil, não é um lugar qualquer.\nSete anos de dados do satélite TRMM, da NASA, mostraram que algumas das tempestades mais intensas da Terra se formam aqui, a leste dos Andes.",
  "C1 (Zipser et al. 2006; release NASA)", ideia=True)
b(C2,
  "Nos anos 80, dois meteorologistas contaram os grandes complexos de tempestade das Américas.\nNas latitudes médias, eles são tão frequentes deste lado do continente quanto nos Estados Unidos.",
  "C2 (Velasco & Fritsch 1987, abstract)")
b(C2,
  "Por que aqui, a gente já mostrou em outro vídeo do canal: umidade da Amazônia, a cordilheira dos Andes, o ar frio do sul.\nAqui, o que interessa é de que lado ele fica.\nO berçário dessas tempestades fica a oeste do Paraná.",
  "recapitulação do 001 (bG6-E4qjXYc); C1")
b(C2,
  "Um levantamento da Universidade Federal de Santa Maria reuniu 310 tornados registrados no Sul.\nA faixa de maior frequência: norte gaúcho, oeste catarinense e sudoeste do Paraná.\nJustamente o lado de onde o temporal chega.",
  "C3 (Lopes & Nascimento 2025)")

# ---------------- 3 · A ESCADA DO PARANÁ ----------------
b(C3,
  "Agora olhe o Paraná de lado, do mar para o rio Paraná.",
  "R2, N4", ideia=True)
b(C3,
  "Ele é uma escada.\nNo litoral, o nível do mar. Logo atrás, a Serra do Mar, com o Pico Paraná, o ponto mais alto do Sul do Brasil: 1.877 metros.\nDepois, Curitiba, a uns 930 metros. Mais para o interior, Guarapuava, a mais de 1.000.",
  "R2, R3, N4 (altitudes a conferir no perfil SRTM)")
b(C3,
  "Daí em diante, o estado desce, degrau por degrau, até o rio Paraná.\nCascavel fica a uns 780 metros. Foz do Iguaçu, a uns 160.",
  "R1, N4")
b(C3,
  "Ou seja: o temporal que vem do Paraguai encontra o Paraná pela ponta mais baixa.\nE a ponta mais baixa é também a mais quente: o ar esquenta, em média, uns 6 décimos de grau a cada 100 metros que se desce.",
  "R1, N4; gradiente térmico médio da troposfera (~0,6 °C/100 m)", ideia=True,
  tts_extra="Ou seja: o temporal que vem do Paraguai encontra o Paraná pela ponta mais baixa. E a ponta mais baixa é também a mais quente: o ar esquenta, em média, uns seis décimos de grau a cada cem metros que se desce.")
b(C3,
  "Na véspera, o Simepar previa mais de 30 °C no norte do estado.\nE dizia que os temporais viriam favorecidos pelo calor e pela umidade.\nÉ do ar quente e úmido que uma tempestade se alimenta.",
  "E1")
b(C3,
  "Faça a conta entre Curitiba e Foz: uns 770 metros de diferença.\nSó pela altitude, o ar de Foz tende a ficar uns 4 a 5 graus mais quente que o de Curitiba.\nÉ a mesma tempestade encontrando outro ar.",
  "cálculo próprio: (930 − 160) m × 0,6 °C/100 m ≈ 4,6 °C; altitudes N4",
  tts_extra="Faça a conta entre Curitiba e Foz: uns setecentos e setenta metros de diferença. Só pela altitude, o ar de Foz tende a ficar uns quatro a cinco graus mais quente que o de Curitiba. É a mesma tempestade encontrando outro ar.")
b(C3,
  "Atenção: a ladeira não puxa a tempestade.\nO relevo decide quem ela encontra primeiro: a ponta baixa e quente do estado, virada para o lado onde as tempestades nascem.",
  "síntese C1, C3, R1 (resposta à Thumb A, sem causalidade inventada)")
b(C3,
  "E lembra da velocidade?\nA uns 70 km/h, uma faixa que entra pelo sudoeste no começo da tarde só chega ao norte do estado à noite.\nPor isso o pior em Londrina e em Cornélio Procópio veio depois das 7.",
  "N1, E4 (paga o loop do b12)")
b(C3,
  "E o vento mais forte não foi na entrada. Foi quase na saída: 98,3 km/h em Cornélio Procópio, às 20h15.\nO temporal atravessou o estado sem perder força.",
  "E4")

# ---------------- 4 · O MESMO LADO ----------------
b(C4,
  "Agora ponha no mesmo mapa o temporal de um ano atrás.",
  "B1", ideia=True)
b(C4,
  "7 de novembro de 2025.\nPelo laudo do Simepar, uma supercélula percorreu uns 270 km, a uns 80 km/h.\nO tornado mais forte deixou um rastro de 75 km, de Quedas do Iguaçu até Cantagalo: de oeste para leste.",
  "B1")
b(C4,
  "Em Rio Bonito do Iguaçu, ele chegou por volta das 6 da tarde e foi classificado como F4.\nPara o Simepar, um dos maiores do estado em 30 anos.",
  "B1")
b(C4,
  "E a mesma tempestade seguiu para o leste.\nAdiante, gerou outro tornado, que passou por Candói e por Entre Rios, em Guarapuava, num rastro de 44 km.\nUma supercélula, uma direção só.",
  "B1 (laudo: tornado 2 da mesma supercélula, Candói F2 e Entre Rios F4, ~44 km)")
b(C4,
  "Ponha as duas linhas lado a lado: a de 2025 e a de 2026.\nA mesma entrada, o oeste. A mesma direção, para o leste.\nE quase a mesma velocidade: 80 e 70 km/h.",
  "B1 + N1", ideia=True)
b(C4,
  "Mesmo lado não quer dizer a mesma cidade.\nQuer dizer a mesma porta de entrada: o oeste e o sudoeste, de frente para o berçário.",
  "síntese B1, N1, C3")
b(C4,
  "E este novembro não parou em 20 de novembro.\nNo dia 7, a Copel chegou a 493 mil imóveis sem luz, o maior número do ano.\nE, até o começo do mês, o Simepar já tinha classificado 15 tornados no Paraná em 2026.",
  "B4, B5")

# ---------------- 5 · POR QUE TANTO AGORA ----------------
b(C5,
  "Sobra uma pergunta: por que tanta coisa num mês só?",
  "pergunta-ponte", ideia=True)
b(C5,
  "Os satélites de chuva da NASA estimam que, de 1º a 20 de novembro, caíram em média uns 175 milímetros sobre o Paraná.\nPara esses 20 dias, o normal seria uns 108.\nMais de 60% acima.",
  "N3 (IMERG, cálculo próprio)",
  tts_extra="Os satélites de chuva da NASA estimam que, de primeiro a vinte de novembro, caíram em média uns cento e setenta e cinco milímetros sobre o Paraná. Para esses vinte dias, o normal seria uns cento e oito. Mais de sessenta por cento acima.")
b(C5,
  "No dia 12, 33 estações do Simepar passaram de 30 °C.\nCerro Azul chegou a 35,1.\nCalor e umidade de sobra, justamente o que alimenta tempestades.",
  "B6")
b(C5,
  "E há o El Niño, que o Simepar classifica como muito forte.\nA previsão é de chuva acima da média até março, com mais temporais severos.\nMas o El Niño não fabrica cada tempestade: aumenta as chances. A porta continua a mesma.",
  "B7")
b(C5,
  "E não confunda com uma temporada certa.\nNo levantamento da UFSM, o maior número de tornados no Sul aparece no inverno, não na primavera.\nO que faz deste novembro um mês fora da curva é o calor e a chuva de sobra, em cima da mesma geografia.",
  "C3 (Lopes & Nascimento 2025: máximo no inverno); N3, B6")

# ---------------- A RESPOSTA ----------------
b(R,
  "Então, por que o temporal entra pelo oeste do Paraná?",
  "pergunta do T1", ideia=True)
b(R,
  "Porque o oeste é a ponta do estado virada para um dos berçários de tempestades mais intensos do planeta, entre o Paraguai e o norte da Argentina.\nPorque essas tempestades andam de sudoeste para nordeste, a uns 70, 80 km/h.\nE porque a primeira terra que elas encontram é a ponta mais baixa e mais quente do Paraná.",
  "síntese C1, N1, B1, R1")
b(R,
  "Em 20 de novembro, isso desenhou uma linha de Capanema a Cornélio Procópio.\nEm 2025, uma linha de Quedas do Iguaçu a Cantagalo.\nUm ano de distância, a mesma direção.",
  "E4, B1")
b(R,
  "O aviso existe. Segundo o Simepar, o alerta de tempestades daquela sexta saiu antes de os temporais chegarem.\nPara receber os alertas da Defesa Civil no celular, mande o seu CEP por SMS para 40199.",
  "E2 (aviso antecipado, S), O1",
  tts_extra="O aviso existe. Segundo o Simepar, o alerta de tempestades daquela sexta saiu antes de os temporais chegarem. Para receber os alertas da Defesa Civil no celular, mande o seu cép por ésse-ême-ésse para quarenta mil cento e noventa e nove.",
  ideia=True)
b(R,
  "E, quando o alerta tocar, fique longe de árvores, postes e placas.\nEm 20 de novembro, foi isso que mais caiu: árvores e telhados.",
  "O2, E7")
b(R,
  "Se você quer ver por que o Sul inteiro junta tantos ingredientes de tempestade, o nosso vídeo sobre os tornados do Sul está aqui no canal.\nSe você tem família no oeste ou no norte do Paraná, manda este vídeo para ela.\nE se inscreve no Em Relevo, para entender o clima do Brasil no mapa.",
  "CTA: puxa sessão para bG6-E4qjXYc (001, publicado); sem gancho de próximo vídeo")

if __name__ == "__main__":
    pasta = Path(__file__).parent
    json.dump(B, open(pasta / "blocos.json", "w"), ensure_ascii=False, indent=1)
    n = sum(len(re.findall(r"\w+", x["fala"])) for x in B)
    ch = sum(len(x["fala_tts"]) for x in B)
    print(len(B), "blocos;", n, "palavras faladas;", ch, "caracteres para o TTS")
    t = 0.4
    linhas = []
    for x in B:
        w = len(re.findall(r"\w+", x["fala"]))
        r = 3.3 if x["marcha"] == 1 else 2.9      # hook a ~1,36× (~198 pal/min) × corpo ~173 pal/min (bíblia voz.md)
        linhas.append((x, t))
        print(f'{x["id"]} {int(t//60)}:{t%60:04.1f} {w:3d}p {x["cap"]}')
        t += w / r + 0.6
    print(f"total estimado {int(t//60)}:{t%60:04.1f}")
    # ROTEIRO.md (leitura humana) + SCRIPT.md (topo com promessa e títulos)
    top = ["# ROTEIRO · Em Relevo 007 · vendavais no Paraná de 20/11/2026",
           "",
           "Promessa: no mapa (estações, satélite e relevo 3D), o caminho do temporal de 20/11 pelo Paraná — de Capanema às 13h45 a Cornélio Procópio às 20h15 — e por que os temporais entram pelo oeste do estado, o mesmo lado de Rio Bonito do Iguaçu em 2025.",
           "Títulos: T1 \"Por que o temporal entra pelo OESTE do PARANÁ?\" / T2 \"O temporal que atravessou o PARANÁ em 6 horas e meia\" / T3 \"RIO BONITO 2025, FOZ 2026: por que o temporal vem pelo mesmo lado?\"",
           f"Gerado por `shared/roteiro.py` · {len(B)} blocos · {n} palavras · {ch} caracteres no TTS · ~{int(t//60)}:{int(t%60):02d} estimados (hook a ~198 pal/min, corpo ~173).",
           "", "| bloco | tempo est. | aba | texto (tela) | fonte |", "|---|---|---|---|---|"]
    for x, tt in linhas:
        top.append(f'| {x["id"]} | {int(tt//60)}:{int(tt%60):02d} | {x["cap"]} | {x["tela"]} | {x["fonte"]} |')
    (pasta.parent / "SCRIPT.md").write_text("\n".join(top) + "\n")
    (pasta.parent / "ROTEIRO.md").write_text("\n".join(top) + "\n")
