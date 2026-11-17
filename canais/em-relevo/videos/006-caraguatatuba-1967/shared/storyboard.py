# Storyboard do 006 (Caraguatatuba 1967 × São Sebastião 2023: por que a Serra do Mar desaba sobre o litoral): plano por bloco
# -> shared/storyboard.json, shared/cenas.json e work/storyboard-tabela.md. Etapa 1 (17/11/2026). Tempos ESTIMADOS (hook 3,3 pal/s,
# corpo 2,9 pal/s); a etapa 2 amarra cada evento à palavra no Whisper (build_cues.py) e grava cues.json.
# Nada aqui é imagem gerada por IA: mapa 3D (terreno_v2/cena3d_v2 do 005, relevo SRTM via AWS Terrain Tiles z12 para o litoral norte de SP
# + Blue Marble/Sentinel), perfis reais (dados/perfis.json), satélite real (NASA EO Landsat 9 29/10/2022 × Landsat 8 26/02/2023;
# NASA IMERG dados/nasa/), documento real (carta de declividade de Olga Cruz, RBG 1975, CC BY 4.0; carta de suscetibilidade SGB)
# e fotos com licença (dl/fotos/video/, pesquisa/FOTOS.md; créditos SÓ na descrição; na tela só LUGAR · DATA).
# Estilos (estilo_v2): A = satélite (relevo real + cor natural), mundo real/impacto; B = relevo editorial (navy), dado/rótulo; "doc" = papel.
# ASSINATURA DO VÍDEO: o DEGRAU — o perfil da serra cortado de lado (bloco 3D com face de corte em terra), o mesmo da Thumb A, com a régua
# 0 → 700 m e a distância < 6 km; aparece no hook (b03, dois perfis lado a lado), b05–b06, b09, b12, b35 e b39.
# Fio condutor visual: 3 "fichas" da receita (PAREDE · CHUVA · CASCA) que acendem no canto quando cada ingrediente é provado (b06 → caps 1–3)
# e voltam juntas em b35 (2023) e b38 (resposta).
# Sensibilidade: nenhuma foto de vítima, resgate com rosto, corpo ou TV; 1967 só por mapa/documento (não há foto livre); fotos de 2023 sem pessoas
# em destaque; vítimas só em texto sóbrio (sem ícone).
import json, re
from pathlib import Path
A = Path(__file__).parent; R = A.parent
bl = {b["id"]: b for b in json.load(open(A / "blocos.json"))}

F = "dl/fotos/video/"; SAT = "dl/fotos/satelite/"; DOC = "dl/fotos/doc/"
ANT = SAT + "nasa-eo-landsat9-sao-sebastiao-antes-2022-10-29.jpg"; DEP = SAT + "nasa-eo-landsat8-sao-sebastiao-depois-2023-02-26.jpg"
CRUZ = DOC + "cruz1975-fig7-carta-declividade-santo-antonio.png"; SGB = DOC + "sgb-carta-suscetibilidade-caraguatatuba.pdf"
UBA = F + "ubatuba-encosta-arrancada-estrada-2023-02-19.jpg"
# id: (estilo, transição de entrada ou "", plano principal, camadas/overlays, mídias [(arquivo, palavra-gatilho, formato)])
S = {
# ---------------- HOOK ----------------
"b01": ("A", "", "Abre baixo sobre o mar, à noite (céu escuro, relevo satélite escurecido) olhando o litoral norte de SP; a câmera corre paralela à costa de Bertioga a Caraguatatuba. Duas colunas de chuva 3D: uma altíssima em Bertioga, uma baixa em Caraguatatuba.",
        ["cartão de lugar BERTIOGA (SP) · 18–19 FEV 2023", "na palavra 'seiscentos': coluna BERTIOGA 683 MM (sobe)", "na palavra 'Caraguatatuba': coluna CARAGUATATUBA 234 MM (para baixa)", "etiqueta 24 HORAS · CEMADEN"], []),
"b02": ("A", "corte para satélite (impacto suave)", "Coluna SÃO SEBASTIÃO 627 MM nasce entre as duas; em seguida, a imagem Landsat real de 26/02/2023 das encostas rasgadas entra grande (65% da largura) com Ken Burns lento.",
        ["coluna SÃO SEBASTIÃO 627 MM", "legenda SÃO SEBASTIÃO · LANDSAT 8 · 26 FEV 2023"],
        [(DEP, "satélite", "quadro grande 3 s, Ken Burns lento no trecho mais riscado (recorte apertado 2–3 km)")]),
"b03": ("B", "corte seco para o diorama (whoosh)", "ASSINATURA: dois blocos 3D do relevo real cortados de lado, um ao lado do outro: BARRA DO SAHY (esq.) e MORRO DO CRUZEIRO (dir.), com a face do corte em terra; régua vertical 0 → 700 M e régua horizontal < 6 KM sobem juntas nos dois.",
        ["rótulos SÃO SEBASTIÃO (2023) · CARAGUATATUBA (1967)", "réguas 685 M / 5,4 KM e 700 M / 5,7 KM (dados/perfis.json)", "frase-âncora em tipografia grande: NÃO FOI AZAR: A RECEITA ESTÁ NO RELEVO."], []),
"b04": ("B", "", "Câmera recua dos dois blocos e sobe até ver o litoral norte inteiro em relevo editorial (Bertioga → Ubatuba).",
        ["pergunta em tipografia: POR QUE A SERRA DO MAR DESABA SOBRE O LITORAL?", "subpergunta: E POR QUE ELA REPETE?"], []),
"b05": ("A", "giro de câmera para vista lateral (whoosh longo)", "Vista lateral do mar para a serra sobre Caraguatatuba (satélite + SRTM, exagero vertical 2,5× marcado 'ilustrativo'): faixa de areia e cidade (manchas claras) → a parede verde → o planalto.",
        ["rótulos na palavra: FAIXA DE AREIA · PAREDE · PLANALTO", "selo pequeno ILUSTRATIVO · ALTURA EXAGERADA 2,5×"],
        [(F + "serra-do-mar-vista-da-tamoios-caraguatatuba.jpg", "parede", "respiro 2 s, quadro médio; legenda SERRA DO MAR · CARAGUATATUBA")]),
"b06": ("B", "", "Bloco 3D cortado do Morro do Cruzeiro (assinatura). Três fichas acendem no canto superior direito uma a uma, cada uma com seu número.",
        ["ficha PAREDE · 700 M EM < 6 KM", "ficha CHUVA · ATÉ 400 MM EM 6 H", "ficha CASCA · 1 A 2,5 M SOBRE A ROCHA (na face do corte, uma faixa marrom fina sobre o cinza da rocha)"], []),
"b07": ("doc", "cortina de papel (swish)", "A carta de declividade de Olga Cruz (1975) entra grande, inclinada sobre papel claro; a câmera passa devagar sobre as hachuras; transição para a imagem Landsat de 2023 lado a lado (meia tela cada).",
        ["etiqueta OLGA CRUZ · GEÓGRAFA (USP)", "etiqueta LANDSAT · 2023"],
        [(CRUZ, "Olga Cruz", "quadro grande inclinado 3 s; legenda CARTA DE DECLIVIDADES · BACIA DO RIO SANTO ANTÔNIO"), (DEP, "satélite", "meia tela 2 s")]),
# ---------------- 1. A PAREDE ----------------
"b08": ("A", "push-in do mar para a serra (whoosh)", "Abertura do cap. 1: câmera vem do mar a 2 km de altura e encara a escarpa atrás de Caraguatatuba; a borda do planalto acende como linha clara na crista.",
        ["aba 1 · A PAREDE", "faixa de altitude 750–900 M na crista (Cruz)", "régua de distância da praia à crista"], []),
"b09": ("A", "voo rasante subindo o vale (sem corte)", "A câmera sobe pelo vale do Rio Santo Antônio (rio em ciano fino, OSM) a partir do centro; um altímetro no canto acompanha. Desvio rápido ao Morro do Cruzeiro, onde as encostas > 30° acendem em coral.",
        ["pino CENTRO · RIO SANTO ANTÔNIO", "altímetro 0 → 750 M em 7,5 KM", "na palavra 'Cruzeiro': encostas > 30° em coral"], []),
"b10": ("B", "", "Bacia do Santo Antônio isolada em relevo editorial (resto escurecido); as áreas com declive > 40% se pintam (mapa de declividade calculado do SRTM, mesma lógica da carta de Cruz).",
        ["etiqueta BACIA · ~30 KM²", "número 54% COM DECLIVE > 40%", "seta da nascente à foz: MINUTOS, NÃO DIAS"], []),
"b11": ("A", "subida de câmera para trás da crista", "Câmera passa por cima da borda e mostra o planalto e a serra de Juqueriquerê ao fundo; esquema simples da borda do bloco: uma linha de fratura tracejada no mar, a parede recuada atrás (ilustrativo, sem idade).",
        ["rótulo SERRA DE JUQUERIQUERÊ · > 1.300 M", "esquema FRATURA · BORDA DO BLOCO (ILUSTRATIVO)"], []),
"b12": ("B", "dolly lateral pela costa até São Sebastião (whoosh)", "A câmera viaja ~35 km pela costa até a Barra do Sahy; o bloco cortado da Barra do Sahy aparece com a mesma régua do Morro do Cruzeiro.",
        ["régua de distância CARAGUATATUBA ↔ BARRA DO SAHY · ~35 KM", "régua 685 M · 5,4 KM", "pino GUARDE ESTE LUGAR (pulso)"], []),
# ---------------- 2. A CHUVA QUE A SERRA FABRICA ----------------
"b13": ("B", "corte para noite (céu escuro sobre o relevo editorial)", "Abertura do cap. 2: mapa do litoral norte com os pluviômetros do CEMADEN como colunas 3D que sobem na ordem da fala.",
        ["aba 2 · A CHUVA QUE A SERRA FABRICA", "cartão 18–19 FEV 2023 · 24 H", "colunas BERTIOGA 683 · SÃO SEBASTIÃO 627 · CARAGUATATUBA 234 · UBATUBA 335 (MM)"], []),
"b14": ("A", "câmera baixa e lateral (sem corte)", "Câmera desce para vista lateral da costa entre Bertioga e São Sebastião: uma faixa de chuva intensa (partículas azuis densas) colada à parede, e setas de ar úmido vindo do mar subindo a encosta e virando nuvem.",
        ["rótulo FAIXA DE POUCOS KM", "setas AR ÚMIDO DO MAR → SOBE · ESFRIA · CHOVE (esquema)", "selo ILUSTRATIVO"], []),
"b15": ("B", "", "Camada real do NASA IMERG (dados/nasa/litoral-2023-camada.png) cobre o mesmo mapa em quadrados de ~10 km, quase apagada; ao lado, a coluna 683 do pluviômetro de Bertioga continua de pé.",
        ["rótulo SATÉLITE DE CHUVA (NASA) · QUADRADOS DE 10 KM", "número máx. ~110 MM × pluviômetro 683 MM", "frase O PICO NÃO CABIA NO QUADRADO"], []),
"b16": ("A", "subida para vista regional (whoosh longo)", "Vista do Sudeste do alto: faixa de frente fria parada sobre o litoral e um pequeno vórtice no mar entre Ubatuba e Paraty; o oceano ganha leve tom quente.",
        ["rótulos FRENTE FRIA · CICLONE PEQUENO · OCEANO MAIS QUENTE (+~1 °C)", "etiqueta SEGUNDO O IAG-USP", "selo ESQUEMA"], []),
"b17": ("B", "", "Pluviômetro gigante de Bertioga enche em 6 horas (relógio no canto); marca fantasma da média de fevereiro (225) bem embaixo.",
        ["contador 0 → 400 MM · 6 HORAS", "marca MÉDIA DE FEVEREIRO · 225 MM", "selo MAIOR ACUMULADO EM 24 H JÁ MEDIDO NO PAÍS (CEMADEN)"], []),
"b18": ("doc", "cortina de papel para 1967 (swish)", "Papel de arquivo (componente do 003/004): ficha de pluviômetro desenhada em código com as leituras de 1967; o nível transborda o tubo no dia 18.",
        ["cartão CARAGUATATUBA · MARÇO DE 1967", "leituras 17/03 · 115 MM e 18/03 · 420 MM", "rótulo O APARELHO TRANSBORDOU"], []),
"b19": ("B", "corte de volta ao relevo", "Mapa da bacia em relevo editorial com dois pinos de posto: o da fazenda (coluna alta) e o do DAEE (coluna com menos da metade), a poucos km.",
        ["colunas POSTO DA FAZENDA × POSTO A POUCOS KM (< METADE)", "frase NA SERRA, A CHUVA MUDA DE VALE PARA VALE", "na palavra 'terceiro': a ficha CASCA pulsa"], []),
# ---------------- 3. A CASCA DA SERRA ----------------
"b20": ("B", "push-in na face do bloco (whoosh)", "Abertura do cap. 3: zoom na face do corte do bloco do Morro do Cruzeiro até a escala de metros: régua de 0 a 2,5 M na casca; abaixo, rocha cinza.",
        ["aba 3 · A CASCA DA SERRA", "régua PLANO DE RUPTURA · 1 A 2,5 M", "rótulos ROCHA DECOMPOSTA E TERRA · GRANITO E GNAISSE", "selo ILUSTRATIVO"], []),
"b21": ("B", "", "Recuo da câmera até a encosta inteira: a casca vira uma película fina sobre a rocha, com a floresta (árvores-palito) por cima; comparação de escala 700 M × 2,5 M.",
        ["comparação 700 M DE SERRA · 2,5 M DE CASCA", "linha CONTATO COM A ROCHA em coral"], []),
"b22": ("B", "", "Esquema animado na encosta cortada: gotas entram, a casca escurece (encharcada) e escorrega em bloco sobre a rocha; num quadro lateral, ensaio de laboratório (cilindro de solo) com o mostrador de coesão perto de zero.",
        ["mostrador COESÃO ≈ 0 · SOLO QUASE SEM COLA", "na palavra 'rocha sã': a ruptura desce até a rocha", "selo ILUSTRATIVO"], []),
"b23": ("doc", "cortina de papel", "A carta de declividade de Olga Cruz (Fig. 7) em tela cheia; a câmera percorre as hachuras escuras; destaque translúcido nas classes > 40% e nos topos planos (claros).",
        ["rótulos > 40% · MAIS ATINGIDAS e TOPOS PLANOS · FICARAM DE PÉ", "legenda CARTA DE DECLIVIDADES · OLGA CRUZ · 1975"],
        [(CRUZ, "mapa de Olga Cruz", "tela cheia 6 s, pan lento; recortar o cabeçalho para mostrar a bacia")]),
"b24": ("B", "corte para o relevo", "Mapa geológico simplificado da bacia sobre o relevo editorial: a mancha do granito de Caraguatatuba em tom próprio; pontos de cicatriz (esquemáticos) se acumulam sobre ela.",
        ["número 8 EM CADA 10 · NO MESMO GRANITO (USP, 2017)", "rótulo GRANITO DE CARAGUATATUBA", "selo PONTOS ILUSTRATIVOS"], []),
"b25": ("A", "corte seco para foto (impacto grave)", "Foto real em quadro grande (65%): a encosta arrancada na beira da estrada em Ubatuba; Ken Burns lento do asfalto para a terra exposta. Depois, volta ao 3D com dezenas de 'cascas' marrons escorregando em encostas vizinhas.",
        ["legenda UBATUBA (SP) · 19 FEV 2023", "na palavra 'centenas': multiplicação das cicatrizes no 3D"],
        [(UBA, "isto", "quadro grande 4 s; recorte sem o galho claro do canto superior direito")]),
# ---------------- 4. 1967: O CAMINHO ATÉ A CIDADE ----------------
"b26": ("A", "subida vertical sobre a bacia (whoosh longo)", "Abertura do cap. 4: vista de cima da bacia do Santo Antônio em satélite + relevo; os vales acendem um a um em coral, todos ao mesmo tempo no fim.",
        ["aba 4 · 1967: O CAMINHO ATÉ A CIDADE", "cartão CARAGUATATUBA · 18 MAR 1967", "rótulo TODOS OS VALES"], []),
"b27": ("B", "", "Contadores sobre o mapa: 640 marcas de cicatriz aparecem (distribuídas pelas encostas íngremes do mapa de declividade; esquemáticas), um raio de 15 km desenhado em volta.",
        ["contador 0 → 640 CICATRIZES (FOTOS AÉREAS)", "contador ~2 MILHÕES DE TONELADAS", "fração 1/5 DA FLORESTA DA ÁREA ESTUDADA", "selo POSIÇÕES ILUSTRATIVAS"], []),
"b28": ("A", "voo rasante descendo o vale (sem corte)", "A câmera segue uma massa marrom que desce do alto de um vale, entra no leito do rio e corre para a planície; todos os vales convergem para a mancha da cidade.",
        ["rótulo AVALANCHE DE DETRITOS (OLGA CRUZ)", "aspas O MORRO RODOU (MORADORES)", "rótulo A PLANÍCIE · A CIDADE"], []),
"b29": ("B", "", "Linha do tempo horizontal de 4 casas que acendem em sequência sobre o mapa (enchente → escorregamentos → corridas → enchente por bloqueio), com ícones SVG simples.",
        ["linha 18 MAR 1967 · 4 FASES", "rótulos ENCHENTE · ESCORREGAMENTOS · CORRIDAS DE DETRITOS · ENCHENTE POR BLOQUEIO"], []),
"b30": ("A", "", "Rio Santo Antônio em 3D na altura da cidade: a fita do rio se alarga de 10–20 m para 60–80 m; régua de lama 80 cm sobre uma rua esquemática; troncos (cilindros) se espalham.",
        ["régua LARGURA DO RIO 10–20 M → 60–80 M (×4)", "régua LAMA NAS RUAS · ATÉ 80 CM", "rótulo DEZENAS DE MILHARES DE TRONCOS"], []),
"b31": ("B", "", "Card sóbrio navy, sem ícone: a faixa de estimativas de vítimas; depois, mapa da planície em 1967 com manchas de fazenda (esquema) e a cidade pequena.",
        ["card VÍTIMAS: 120 (ESTIMATIVA DE OLGA CRUZ) A ~500 (CONTAGENS DA ÉPOCA)", "rótulos PLANÍCIE EM 1967 · FAZENDAS (ESQUEMA)"], []),
"b32": ("B", "crossfade com câmera parada", "A carta de suscetibilidade do SGB (classes alta/média/baixa) é sobreposta ao relevo da mesma área; em seguida, a mancha urbana de hoje (satélite atual) acende na planície ao pé.",
        ["legenda CARTA DE SUSCETIBILIDADE · SERVIÇO GEOLÓGICO DO BRASIL", "classes ALTA · MÉDIA · BAIXA", "contador ~135 MIL MORADORES (CENSO 2022)"],
        [(SGB, "Serviço Geológico", "camada recortada da carta (classes de deslizamento) georreferenciada sobre o relevo; conferir antes que as classes altas batem com as encostas íngremes")]),
# ---------------- 5. 2023: A MESMA RECEITA ----------------
"b33": ("A", "dolly pela costa até São Sebastião (whoosh)", "Abertura do cap. 5: a câmera volta à Barra do Sahy; o recorte do Landsat (Juquehy → Praia da Baleia) é marcado no 3D.",
        ["aba 5 · 2023: A MESMA RECEITA", "retângulo ÁREA DA IMAGEM LANDSAT"],
        [(ANT, "outubro de 2022", "entra como textura do recorte 2 s; legenda LANDSAT 9 · 29 OUT 2022")]),
"b34": ("A", "cortina vertical antes × depois", "Antes × depois Landsat em cortina vertical que corre devagar da esquerda para a direita (mesmo estiramento nos dois); termina com zoom nas faixas de terra até as casas.",
        ["legendas ANTES · 29 OUT 2022 / DEPOIS · 26 FEV 2023", "na palavra 'cada faixa': uma faixa contornada em coral com a etiqueta CASCA"],
        [(ANT, "Antes", "metade esquerda da cortina"), (DEP, "Depois", "metade direita da cortina; recorte sem a nuvem do canto")]),
"b35": ("B", "", "As 3 fichas da receita voltam juntas sobre o bloco cortado da Barra do Sahy, cada uma com o número de 2023.",
        ["ficha PAREDE · 685 M EM 5,4 KM", "ficha CHUVA · 627 MM EM 24 H", "ficha CASCA · 1 A 2,5 M"], []),
"b36": ("A", "", "Citação em tipografia sobre a imagem Landsat escurecida; na palavra 'precedente', a câmera desliza 35 km até Caraguatatuba e pousa no Morro do Cruzeiro.",
        ["citação 'BEM INCOMUNS, MAS NÃO SEM PRECEDENTE' · ESPECIALISTA EM DESLIZAMENTOS DA NASA", "régua ~35 KM"], []),
"b37": ("B", "", "Card sóbrio navy, sem ícone nem foto de pessoas: números de 2023.",
        ["card 65 VIDAS · SÃO SEBASTIÃO E UBATUBA", "1.815 DESABRIGADOS · 2.251 DESALOJADOS (CEMADEN)"],
        [(F + "sao-sebastiao-encosta-aereo-2023-02-23.jpg", "desabrigadas", "fundo esmaecido 3 s (vista aérea de encosta, sem pessoas em destaque); legenda SÃO SEBASTIÃO · 23 FEV 2023")]),
# ---------------- A RESPOSTA ----------------
"b38": ("B", "subida de câmera (whoosh longo)", "Mapa do litoral norte inteiro; as 3 fichas se juntam no centro formando a frase-resposta; a parede, a faixa de chuva e a casca acendem no 3D ao mesmo tempo.",
        ["aba A RESPOSTA", "fichas 700 M EM < 6 KM · 400 MM EM 6 H · CASCA DE 1 A 2,5 M QUASE SEM COLA"], []),
"b39": ("A", "", "Cascas escorregando em várias encostas e descendo pelos vales até as cidades (reprise curta do cap. 4); fecha nos dois blocos cortados lado a lado do hook (assinatura).",
        ["réguas MORRO DO CRUZEIRO 700 M / 5,7 KM · BARRA DO SAHY 685 M / 5,4 KM"], []),
"b40": ("B", "", "Litoral norte em relevo editorial com as classes de suscetibilidade do SGB acesas em Caraguatatuba e São Sebastião (sem número de previsão).",
        ["selo NÃO É PREVISÃO", "frase A GEOGRAFIA NÃO MUDA"], []),
"b41": ("B", "", "Mapa de Caraguatatuba com os polígonos de área de risco mapeados (esquema a partir do IBGE/CEMADEN) acendendo.",
        ["contador ~3 MIL MORADORES EM ÁREAS DE RISCO (IBGE · CENSO 2010)"], []),
"b42": ("B", "", "Quadro 'O QUE FAZER' (cortiça, componente do 001/002) com o card do SMS.",
        ["card SMS: CEP PARA 40199 (DEFESA CIVIL)", "card SE O ALERTA DISSER PARA SAIR, SAIA"], []),
"b43": ("B", "", "Encerramento do canal: card do vídeo da seca de 1877 (I5KpDKy6r3E, publicado) + logo EM RELEVO + botão inscrever (sem card de próximo vídeo).", [], []),
}

assert set(S) == set(bl), sorted(set(bl) ^ set(S))
t, out, cenas = 0.4, [], []
for bid, b in bl.items():
    est, trans, plano, camadas, midias = S[bid]
    nw = len(re.findall(r"\w+", b["fala"])); dur = round(nw / (3.3 if b["marcha"] == 1 else 2.9) + 0.6, 1)
    out.append({"id": bid, "cap": b["cap"], "t_est": round(t, 1), "dur_est": dur, "estilo": est, "transicao": trans, "plano": plano,
                "camadas": camadas, "midias": [{"arquivo": m[0], "gatilho": m[1], "formato": m[2]} for m in midias]})
    for m in midias:
        assert (R / m[0]).exists(), m[0]
        cenas.append({"bloco": bid, "tipo": "documento" if m[0].startswith(DOC) else "foto", "arquivo": m[0], "gatilho": m[1], "formato": m[2]})
    cenas.append({"bloco": bid, "tipo": "mapa" if est in "AB" else "arquivo", "estilo": est, "descricao": plano})
    t += dur
json.dump({"_doc": "Etapa 1: plano por bloco (tempos estimados). A etapa 2 converte em cues.json amarrado ao Whisper.", "duracao_est_s": round(t, 1), "blocos": out},
          open(A / "storyboard.json", "w"), ensure_ascii=False, indent=1)
json.dump({"_doc": "Lista plana de planos/mídias (nenhuma imagem de IA; fotos de dl/fotos/video/, satélite de dl/fotos/satelite/, documentos de dl/fotos/doc/).", "cenas": cenas},
          open(A / "cenas.json", "w"), ensure_ascii=False, indent=1)
def mmss(x): return f"{int(x // 60)}:{x % 60:04.1f}"
L = ["| Bloco | Tempo est. | Estilo | Entrada | Plano | Camadas | Mídias |", "|---|---|---|---|---|---|---|"]
for o in out:
    L.append(f"| {o['id']} | {mmss(o['t_est'])} | {o['estilo']} | {o['transicao'] or '—'} | {o['plano']} | {'; '.join(o['camadas']) or '—'} | {'; '.join(m['arquivo'].split('/')[-1] + ' (' + m['formato'] + ')' for m in o['midias']) or '—'} |")
(R / "work").mkdir(exist_ok=True); open(R / "work/storyboard-tabela.md", "w").write("\n".join(L) + "\n")
usadas = sorted({c["arquivo"].split('/')[-1] for c in cenas if c["tipo"] in ("foto", "documento")})
tA = sum(o["dur_est"] for o in out if o["estilo"] == "A"); tB = sum(o["dur_est"] for o in out if o["estilo"] == "B"); tD = sum(o["dur_est"] for o in out if o["estilo"] == "doc")
print(f"duração estimada {mmss(t)}; A {tA:.0f} s, B {tB:.0f} s, doc {tD:.0f} s; {len(usadas)} mídias reais distintas: {', '.join(usadas)}")
