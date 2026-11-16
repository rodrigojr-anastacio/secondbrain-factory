# Storyboard do longo 04 (1983: El Niño, enchente no Sul × seca no sertão): plano por bloco -> shared/storyboard.json, shared/cenas.json
# e work/storyboard-tabela.md. Etapa 1 (13/11/2026). Tempos ESTIMADOS (2,9 palavras/s, ritmo do longo-02/03); a etapa 2 amarra cada
# evento à palavra no Whisper (build_cues.py, mesmo método do longo-03) e grava cues.json.
# Nada aqui é imagem gerada por IA: mapa 3D (terreno_v2/cena3d_v2 do longo-03), dados reais (dados/*.json) e fotos de dl/fotos/video/
# (licenças em pesquisa/FOTOS.md; créditos só na descrição). NÃO existe foto livre da enchente nem da seca de 1983: o "1983" do vídeo
# é feito com DADO (régua do rio, pluviômetro, Landsat de 1983) + mapa; fotos de hoje sempre com o ano real na legenda.
# Estilos (estilo_v2): A = satélite (Blue Marble + relevo ETOPO), mundo real/impacto; B = relevo editorial, dado/rótulo;
# "arquivo" = papel/jornal sépia (tipografia, citações, carimbos; sem foto de época).
# Assinatura do vídeo: TELA PARTIDA do Brasil (Sul azul-água subindo × sertão coral secando) com o MESMO relógio de 1983 correndo.
import json, re
from pathlib import Path
A = Path(__file__).parent; R = A.parent
bl = {b["id"]: b for b in json.load(open(A / "blocos.json"))}

# id: (estilo, transição de entrada ou "", plano principal, camadas/overlays, mídias [(arquivo, palavra-gatilho, formato)])
S = {
# ---------------- HOOK ----------------
"b01": ("A", "", "Abre baixo sobre o vale do Iguaçu em satélite, céu de chuva; dolly até a curva do rio e pousa em União da Vitória (pino coral). Régua de nível vertical gigante cravada no rio (componente novo 'régua'), começando em 2,5 m.",
        ["cartão de lugar UNIÃO DA VITÓRIA (PR) · JULHO DE 1983", "na palavra 'dezoito': a água da régua sobe 2,5 → 10,42 m (dados/ana_65310000_cota.json, jul/1983) e o relevo da várzea afunda sob um plano de água azul que cresce", "número 10,42 M grande"],
        [("landsat4-uv-19830703-par.jpg", "Iguaçu", "fundo de 2 s antes do 3D: satélite real de 1983 com legenda UNIÃO DA VITÓRIA · LANDSAT 4 · 3 JUL 1983")]),
"b02": ("A", "whip pan para leste (swish)", "Câmera corre 200 km pelo relevo até o vale do Itajaí, encaixado entre morros; pino BLUMENAU; segunda régua 15,34 M.",
        ["régua Itajaí-Açu sobe até 15,34 M (09/07/1983)", "contador de cheias do ano: 3 marcas (MAR · MAI · JUL) e uma 4ª pontilhada (SET)"],
        [("blumenau-aerea-2010.jpg", "Blumenau", "quadro grande à direita 3 s; legenda BLUMENAU · CENTRO E RIO ITAJAÍ-AÇU · 2010")]),
"b03": ("A", "zoom-out vertical do Sul até o Brasil inteiro e mergulho no Ceará (whoosh longo)", "Plano-assinatura começa: câmera sobe do Sul, o Brasil inteiro aparece, régua de distância 2.500 KM se desenha de União da Vitória a Mombaça; mergulho no sertão seco, céu limpo, luz dura.",
        ["régua 2.500 KM", "pino MOMBAÇA (CE) · 1983", "pluviômetro lateral esvaziando: 783 → 366 MM (47%)", "selo 5º ANO DE SECA · DESDE 1979"],
        [("acude-seco-santa-quiteria-ce-2018.jpg", "pluviômetro", "quadro grande 3 s; legenda AÇUDE SECO · SANTA QUITÉRIA (CE) · 2018")]),
"b04": ("arquivo", "corte seco (impacto grave)", "Página de jornal sépia (tipografia, sem foto): manchete composta por nós 'FLAGELADOS INVADEM ARMAZÉM EM CANINDÉ' com data AGO/1983; número 5 MIL carimbado.",
        ["carimbo 5 MIL FLAGELADOS · CANINDÉ (CE)", "contador 10 MILHÕES DE FLAGELADOS NO NORDESTE (etiqueta pequena SEGUNDO O MEMORIAL DA DEMOCRACIA)"],
        [("retirantes-pernambuco-slide-janjao-sem-data.jpg", "flagelados", "quadro médio inclinado sobre o papel 3 s; legenda RETIRANTES · PERNAMBUCO · FOTO DE ACERVO (SEM DATA) — nunca escrever 1983")]),
"b05": ("B", "corte seco de volta ao mapa (impacto suave)", "TELA PARTIDA (assinatura): Brasil inteiro em relevo editorial, linha diagonal divide o país; Sul tinge em azul-água pulsando, Nordeste em coral seco rachando. Mesmo relógio '1983' no centro.",
        ["rótulos ÁGUA DEMAIS (Sul) · ÁGUA NENHUMA (sertão)", "na palavra 'dois mil e vinte e seis': miniatura do Pacífico com o relevo de calor de 2026 (do longo-02) no canto e '1983 ↔ 2026?'"], []),
"b06": ("B", "", "Câmera parada na tela partida; barra das 4 perguntas (componente do longo-02/03) entra pergunta a pergunta.",
        ["barra 4 perguntas: O QUE ACONTECEU NO SUL? · NO SERTÃO? · POR QUE OS DOIS? · E EM 2026?"], []),
"b07": ("B", "", "Dois anéis de 12 meses (componente do longo-03), um sobre o Sul (todos os meses com gotas iguais) e um sobre o sertão (só FEV–MAI com gota). Na última frase, o anel do Sul transborda e o do sertão apaga.",
        ["rótulos SUL: CHUVA O ANO INTEIRO · SERTÃO: FEV–MAI", "setas opostas EXTREMOS OPOSTOS"], []),
# ---------------- 1. O QUE ACONTECEU NO SUL ----------------
"b08": ("A", "push-in através de nuvens de chuva (whoosh longo)", "Abertura do cap. 1: o Iguaçu se desenha como fio azul brilhante do leste do PR (perto de Curitiba) até Foz; câmera desce e acompanha as curvas até a península de União da Vitória/Porto União.",
        ["barra das perguntas: ▶ 1/4", "etiquetas CURITIBA · UNIÃO DA VITÓRIA · CATARATAS", "na palavra 'curvas': a península urbana acende em branco (cidade dentro da curva)"],
        [("uniao-da-vitoria-vista-aerea-2009.jpg", "cresceu", "quadro grande 4 s; legenda UNIÃO DA VITÓRIA · RIO IGUAÇU · 2009")]),
"b09": ("B", "whip pan para o gráfico (swish)", "HIDROGRAMA EM RELEVO (peça nova): a cota diária de nov/1982 a set/1983 (dados/ana_65310000_cota.json) vira uma serra de água azul que cresce da esquerda para a direita; linha tracejada 6 M = transbordamento.",
        ["pico NOV/82 6,45 M acende na palavra 'novembro'", "pico MAI–JUN/83 6,65 M na palavra 'maio'", "ponto 3 JUL 4,94 M com etiqueta 'CHEIO, MAS SOB CONTROLE'"], []),
"b10": ("B", "", "O hidrograma pausa no começo de julho; ao lado, dois pluviômetros: MÉDIA JUN+JUL 138 MM × 1 SEMANA EM JUL/83 ~800 MM; o segundo transborda.",
        ["barras 138 × 800 MM", "selo ~6× · DEFESA CIVIL DO PARANÁ"], []),
"b11": ("B", "", "O hidrograma retoma: em 15 dias a serra azul dispara de 4,94 a 10,42 M (18/07) e fica acima da linha de 6 m até 10/08.",
        ["contador da régua 4,94 → 10,42 M", "chave '15 DIAS'", "faixa sombreada '+1 MÊS ACIMA DE 6 M'"], []),
"b12": ("A", "corte seco de volta ao mapa (impacto suave)", "União da Vitória em 3D com o plano de água no nível de 10,42 m cobrindo a várzea e a península; câmera em órbita lenta, chuva fina.",
        ["ícones riscados: LUZ · ÁGUA · COMIDA", "contador +2.400 FAMÍLIAS", "ícone abrigo"],
        [("porto-uniao-centro-2014.jpg", "famílias", "quadro médio 3 s; legenda PONTE SOBRE O IGUAÇU · UNIÃO DA VITÓRIA E PORTO UNIÃO · 2014")]),
"b13": ("A", "", "Satélite real de 1983 em tela cheia, ANTES × DEPOIS com cortina deslizante: landsat4-uv-19830703-par.jpg → landsat4-uv-19830804-par.jpg (mesma janela de 72 × 40 km). Cortina na palavra 'quatro de agosto'; zoom lento na várzea a sudeste da cidade, que fica larga e clara (alagada).",
        ["datas 3 JUL 1983 · RIO 4,94 M | 4 AGO 1983 · RIO 7,42 M", "rótulo LANDSAT 4 · 1983", "seta A VÁRZEA VIROU UM LAGO"],
        [("landsat4-uv-19830703-par.jpg", "três de julho", "tela cheia (equalizar cores com a de 04/08; corrigir a falsa-cor para água azul e vegetação verde-escura)"),
         ("landsat4-uv-19830804-par.jpg", "agosto", "tela cheia; recortar a parte sem nuvem (várzea a sudeste) — nuvens sobre a cidade")]),
"b14": ("A", "whip pan para leste (swish)", "Vale do Itajaí em 3D, câmera baixa entre os morros; seção transversal desenhada: vale em V estreito × várzea larga do Iguaçu (miniatura).",
        ["comparação de seção: IGUAÇU ESPALHA · ITAJAÍ SOBE"],
        [("blumenau-rio-itajai-acu-2006.jpg", "apertado", "quadro grande 3 s; legenda BLUMENAU · RIO ITAJAÍ-AÇU EM ESTIAGEM · 2006 (o mesmo rio baixo)")]),
"b15": ("B", "", "Régua de Blumenau grande ao lado do mapa: quatro marcas de 1983 sobem em sequência (10,60 · 12,52 · 15,34 · 11,75 M) com as datas; a de 9 de julho acende em coral.",
        ["etiquetas 04/03 · 20/05 · 09/07 · 24/09", "número 15,34 M"], []),
"b16": ("B", "", "Santa Catarina em relevo editorial: municípios em calamidade tingem de coral (ilustrativo, sem afirmar quais), contadores sobem.",
        ["contadores 78 MUNICÍPIOS EM CALAMIDADE · 49 MORTOS · ~200 MIL DESABRIGADOS", "etiqueta pequena SEGUNDO HERRMANN (UFSC)"],
        [("blumenau-enchente-2008-exercito-NAO-1983.jpg", "atingida", "OPCIONAL quadro médio 2 s SÓ com legenda BLUMENAU · ENCHENTE DE 2008 (é outra enchente; se houver dúvida, não use)")]),
# ---------------- 2. O QUE ACONTECEU NO SERTÃO ----------------
"b17": ("A", "zoom-out orbital do Sul e voo para o norte sobre o Brasil (whoosh longo)", "Abertura do cap. 2: a tela partida volta por 1 s e a câmera voa para o sertão do Ceará em satélite, terreno marrom, céu sem nuvem.",
        ["barra das perguntas: ▶ 2/4", "linha do tempo 1979 → 1983 acendendo ano a ano"], []),
"b18": ("B", "whip pan para o gráfico (swish)", "Régua de montanhas (componente do longo-03) com a chuva anual de Mombaça 1911–2024 (dados/ana_539001_chuva.json, só anos completos); linha da média 783 mm; 1981–82–83 afundam em sequência.",
        ["pino MOMBAÇA (CE) · PLUVIÔMETRO DO DNOCS · DESDE 1910", "barras 81 472 · 82 407 · 83 366 MM acendem nas palavras", "selo 47% DA MÉDIA"], []),
"b19": ("B", "", "Três cartões de papel em sequência sobre o sertão em relevo: ANO 1 roça · ANO 2 reserva · ANO 3 açude/gado, cada um riscado ao entrar.",
        ["ícones: milho · saco · açude secando · gado"],
        [("acude-coremas-seco-2017.jpg", "açudes", "quadro grande panorâmico 3 s; legenda AÇUDE DE COREMAS (PB) · SECA · 2017")]),
"b20": ("B", "", "Mapa do Nordeste semiárido (../longo-03/dados/semiarido.json) com ícones de obra (açude, estrada, poço) se espalhando; contador.",
        ["barras ALISTADOS NAS FRENTES DE EMERGÊNCIA: 1979 ~460 MIL · 1983 3,13 MILHÕES (etiqueta PELOS NÚMEROS DA SUDENE)"],
        [("sertao-caatinga-arido-2013.jpg", "estrada", "quadro grande 3 s; legenda SERTÃO · CAATINGA NA ESTIAGEM · 2013")]),
"b21": ("arquivo", "corte seco (impacto grave)", "Papel sépia com linha do tempo de agosto de 1983: pino FORTALEZA · PALÁCIO DA LUZ, seta 'DOIS DIAS DEPOIS', pino CANINDÉ · ARMAZÉM DA COBAL.",
        ["tipografia de jornal: 'A FOME VIROU REVOLTA'", "carimbo AGOSTO DE 1983"], []),
"b22": ("arquivo", "", "Mesmo papel: grande ponto de interrogação em tinta sobre 'MORTOS: ?'; a interrogação não é preenchida (não mostramos número).",
        ["rótulo NENHUM NÚMERO OFICIAL CONFIÁVEL"], []),
"b23": ("B", "corte seco de volta ao mapa (impacto suave)", "Nordeste em relevo; a régua de Mombaça reaparece pequena e 1984 sobe de volta à média (792 mm).",
        ["etiqueta 1984 · A CHUVA VOLTA", "selo UMA DAS MAIORES SECAS DO SÉCULO 20"], []),
# ---------------- 3. POR QUE OS DOIS AO MESMO TEMPO ----------------
"b24": ("A", "zoom-out orbital do Brasil até o globo (whoosh longo)", "Globo em satélite gira do Brasil para o Pacífico equatorial.",
        ["barra das perguntas: ▶ 3/4"], []),
"b25": ("A", "", "Maquete do Pacífico (mesa do longo-02) com o relevo de calor de 1982-83; depois régua de montanhas RONI (dados/roni.txt): 1982-83 · 1997-98 · 2015-16 · 2026 (até ASO) lado a lado; 1982-83 é a mais alta.",
        ["montanhas RONI: 1982-83 +2,4 · 1997-98 +2,3 · 2015-16 +2,3 · 2026 +2,0 (até out)", "coroa RECORDE DESDE 1950 sobre 1982-83"],
        [("elnino-1982-83-anomalia-temp-pacifico-jan1983.jpg", "Pacífico", "quadro grande 3 s; legenda PACÍFICO · JAN 1983 (NOAA)")]),
"b26": ("A", "", "Circulação de Walker (componente do longo-02): ar sobe sobre o Pacífico quente, setas descem sobre a Amazônia e o norte do Nordeste.",
        ["card 'ASSISTA: EL NIÑO 2026' (vídeo publicado FeSLzHvlkbo) por 3 s", "seta AR QUE DESCE = SEM NUVEM"], []),
"b27": ("B", "whip pan para o calendário (swish)", "Anel de 12 meses do sertão (b07) com uma onda coral (RONI mensal 1982-83) passando por cima: o pico DEZ–JAN encosta na quadra FEV–MAI, que apaga.",
        ["rótulos PICO DO EL NIÑO: DEZ–JAN · CHUVA DO SERTÃO: FEV–MAI", "selo 3º ANO SEGUIDO"], []),
"b28": ("A", "whip pan para o sul (swish)", "América do Sul em satélite; o jato subtropical como fita de vento branca/azul animada em altitude, cruzando o Sul; frentes frias (linhas com triângulos) chegam e PARAM debaixo da fita; um 'cadeado' de alta pressão (H) aparece sobre o Atlântico na palavra 'bloqueios'.",
        ["rótulos JATO SUBTROPICAL · FRENTES PRESAS · BLOQUEIO", "etiqueta pequena ESTUDO DO INPE · 1984"],
        [("noaa-cpc-elnino-impactos-globais-jun-ago.jpg", "contrário", "quadro grande 3 s (mapa NOAA de impactos JUN–AGO: Sul úmido); legenda NOAA · IMPACTOS DO EL NIÑO · JUN–AGO")]),
"b29": ("B", "corte seco (impacto suave)", "Volta o hidrograma do Iguaçu (b09–b11) e, sobreposta na mesma linha do tempo, a onda RONI 1982-83 em coral: no pico do rio (18/07/83) a onda do Pacífico já desceu para +0,5.",
        ["marcador vertical 18 JUL 1983", "rótulos PACÍFICO ESFRIANDO ↘ · RIO NO PICO ↗"], []),
"b30": ("B", "", "Anel de 24 meses (2 anos) sobre o Sul: acendem PRIMAVERA DO ANO 1 e OUTONO–INVERNO DO ANO 2; os picos reais do Iguaçu (NOV/82, MAI/83, JUL/83) caem exatamente nas faixas acesas.",
        ["rótulos PRIMAVERA (ANO 1) · OUTONO E INVERNO (ANO 2)", "na palavra 'Guarde isso': carimbo GUARDE ISSO sobre o anel"], []),
"b31": ("B", "zoom-out (whoosh médio)", "Volta à tela partida (assinatura) com o Pacífico à esquerda: dois fios saem do Pacífico, um coral até o sertão (chave DESLIGA) e um azul até o Sul (chave LIGA).",
        ["régua 2.500 KM entre as pontas", "rótulo O MESMO FENÔMENO"], []),
"b32": ("A", "", "Câmera baixa alterna entre a várzea ocupada de União da Vitória (3D) e o sertão seco (3D), mesma luz de fim de tarde.",
        ["frase em tipografia grande: O EL NIÑO ESCOLHEU OS LUGARES"],
        [("uniao-da-vitoria-rio-iguacu-helicoptero-2016.jpg", "várzea", "quadro médio 2 s; legenda UNIÃO DA VITÓRIA · RIO IGUAÇU · 2016 (cortar o painel do helicóptero)")]),
# ---------------- 4. E EM 2026? ----------------
"b33": ("A", "zoom-out orbital até o globo (whoosh longo)", "Globo de hoje; Pacífico com o relevo de calor de out/nov 2026 (dados do longo-02/03).",
        ["barra das perguntas: ▶ 4/4"], []),
"b34": ("A", "", "Maquete do Pacífico 2026; mostrador de probabilidade (componente do longo-02) gira até ~60%.",
        ["número NIÑO-3.4 +2,5 °C · 12/11/2026", "mostrador ~60% · MAIS FORTE DESDE 1950?", "selo PROVÁVEL ≠ CERTO"], []),
"b35": ("B", "whip pan para o Sul (swish)", "Sul em relevo editorial; dois pinos com colunas de chuva de outubro/2026; SC com 54 pinos pequenos piscando (estragos 7–8/11).",
        ["colunas 577,6 MM · LARANJEIRAS DO SUL (PR) e 581,6 MM · DIONÍSIO CERQUEIRA (SC) · OUT/2026", "contador 54 CIDADES (SC) · 7–8 NOV"], []),
"b36": ("B", "", "O anel de 24 meses de b30 volta, agora rotulado 2026–2027: PRIMAVERA 2026 já acesa; OUTONO–INVERNO 2027 em contorno pontilhado (atenção, não previsão).",
        ["rótulo NOAA: ENFRAQUECE NO INÍCIO DE 2027", "selo NÃO É PREVISÃO DE ENCHENTE", "etiqueta ATENÇÃO: OUTONO E INVERNO 2027"], []),
"b37": ("B", "whip pan para o norte (swish)", "Nordeste em relevo editorial; norte da região tingido em coral claro (abaixo da média NDJ); anel do sertão com FEV–MAI 2027 em interrogação.",
        ["card PREVISÃO NOV–JAN: ABAIXO DA MÉDIA EM ÁREAS DO NE (INMET)", "selo FUNCEME: AINDA É CEDO"], []),
"b38": ("A", "", "Sertão em satélite de hoje; pinos se acendem em cachos (cisternas, ilustrativo).",
        ["contador 1,2 MILHÃO DE CISTERNAS", "régua de secas 1983 × 2012–2017 com ícone de fome em massa só em 1983"],
        [("sobradinho-represa-seca-2015.jpg", "dois mil e doze", "quadro grande 3 s; legenda SOBRADINHO (BA) · RESERVATÓRIO BAIXO · 2015")]),
"b39": ("A", "", "Vale do Iguaçu em 3D de hoje com ícone de alerta (sino/celular) pulsando sobre União da Vitória e Blumenau; a régua de 1983 (10,42 M) aparece fantasma ao lado do rio.",
        ["ícone ALERTA NO CELULAR · DEFESA CIVIL", "régua fantasma 10,42 M · 1983"], []),
# ---------------- A RESPOSTA ----------------
"b40": ("B", "zoom-out até o Brasil inteiro (whoosh longo)", "Reprise da tela partida com o relógio parado em JULHO 1983: régua do Iguaçu a 10,42 M no Sul, pluviômetro de Mombaça vazio no sertão; um único fio do Pacífico puxa os dois lados.",
        ["frase final em tipografia grande: O MESMO EL NIÑO, PUXANDO O BRASIL PARA OS DOIS LADOS"], []),
"b41": ("A", "", "Globo: Pacífico de 2026 esfriando lentamente (animação da cor) enquanto o Brasil continua aceso nas duas pontas.",
        ["frase: O PERIGO NÃO ACABA QUANDO O PACÍFICO COMEÇA A ESFRIAR"], []),
"b42": ("B", "", "Encerramento do canal: card do vídeo EL NIÑO 2026 (FeSLzHvlkbo, publicado) + logo EM RELEVO + botão inscrever (sem card de próximo vídeo).", [], []),
}

assert set(S) == set(bl), sorted(set(bl) ^ set(S))
t, out, cenas = 0.4, [], []
for bid, b in bl.items():
    est, trans, plano, camadas, midias = S[bid]
    nw = len(re.findall(r"\w+", b["fala"])); dur = round(nw / 2.9 + 0.7, 1)
    out.append({"id": bid, "cap": b["cap"], "t_est": round(t, 1), "dur_est": dur, "estilo": est, "transicao": trans, "plano": plano,
                "camadas": camadas, "midias": [{"arquivo": m[0], "gatilho": m[1], "formato": m[2]} for m in midias]})
    for m in midias: cenas.append({"bloco": bid, "tipo": "foto", "arquivo": m[0], "gatilho": m[1], "formato": m[2]})
    cenas.append({"bloco": bid, "tipo": "mapa" if est in "AB" else "arquivo", "estilo": est, "descricao": plano})
    t += dur
json.dump({"_doc": "Etapa 1: plano por bloco (tempos estimados). A etapa 2 converte em cues.json amarrado ao Whisper.", "duracao_est_s": round(t, 1), "blocos": out},
          open(A / "storyboard.json", "w"), ensure_ascii=False, indent=1)
json.dump({"_doc": "Lista plana de planos/mídias (nenhuma imagem de IA; fotos de dl/fotos/video/ e dl/fotos/satelite/).", "cenas": cenas}, open(A / "cenas.json", "w"), ensure_ascii=False, indent=1)
def mmss(x): return f"{int(x // 60)}:{x % 60:04.1f}"
L = ["| Bloco | Tempo est. | Estilo | Entrada | Plano | Camadas | Mídias |", "|---|---|---|---|---|---|---|"]
for o in out:
    L.append(f"| {o['id']} | {mmss(o['t_est'])} | {o['estilo']} | {o['transicao'] or '—'} | {o['plano']} | {'; '.join(o['camadas']) or '—'} | {'; '.join(m['arquivo'] + ' (' + m['formato'] + ')' for m in o['midias']) or '—'} |")
(R / "work").mkdir(exist_ok=True); open(R / "work/storyboard-tabela.md", "w").write("\n".join(L) + "\n")
usadas = sorted({c["arquivo"] for c in cenas if c["tipo"] == "foto"})
tA = sum(o["dur_est"] for o in out if o["estilo"] == "A"); tB = sum(o["dur_est"] for o in out if o["estilo"] == "B"); tR = sum(o["dur_est"] for o in out if o["estilo"] == "arquivo")
print(f"duração estimada {mmss(t)}; A {tA:.0f} s, B {tB:.0f} s, arquivo {tR:.0f} s; {len(usadas)} fotos distintas: {', '.join(usadas)}")
