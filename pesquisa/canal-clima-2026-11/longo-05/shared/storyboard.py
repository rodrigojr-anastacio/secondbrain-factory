# Storyboard do longo 05 (enchente de maio/2024: por que a chuva da serra alagou Porto Alegre): plano por bloco -> shared/storyboard.json,
# shared/cenas.json e work/storyboard-tabela.md. Etapa 1 (15/11/2026). Tempos ESTIMADOS (2,9 palavras/s); a etapa 2 amarra cada evento
# à palavra no Whisper (build_cues.py, método do longo-03/04) e grava cues.json.
# Nada aqui é imagem gerada por IA: mapa 3D (terreno_v2/cena3d_v2 do longo-03/04, relevo ETOPO/SRTM), hidrografia real (ANA/IBGE: rios
# da Região Hidrográfica do Guaíba), satélite real (NASA Landsat 8 08/05/2024, HLS/Sentinel-2 01/04 e 06/05/2024, MODIS) e fotos
# com licença de dl/fotos/video/ (pesquisa/FOTOS.md; créditos SÓ na descrição; na tela só LUGAR · DATA).
# Estilos (estilo_v2): A = satélite (Blue Marble + relevo), mundo real/impacto; B = relevo editorial, dado/rótulo; "arquivo" = papel sépia.
# ASSINATURA DO VÍDEO: a ÁRVORE DE RIOS em ciano brilhante (a mesma da thumb): dezenas de afluentes que engrossam e convergem
# num ponto só, o Guaíba em frente a Porto Alegre. Fio condutor visual: uma GOTA/partícula luminosa que sai de Caxias do Sul (b01)
# e é seguida pela câmera até o centro de Porto Alegre (b33); volta inteira na reprise (b34–b36).
# Sensibilidade: nenhuma foto de vítima, de resgate com rosto ou de TV; fotos aéreas de cidade/infraestrutura; nada de "1941" em foto de 2024.
import json, re
from pathlib import Path
A = Path(__file__).parent; R = A.parent
bl = {b["id"]: b for b in json.load(open(A / "blocos.json"))}

F = "dl/fotos/video/"; SAT = "dl/fotos/satelite/"
# id: (estilo, transição de entrada ou "", plano principal, camadas/overlays, mídias [(arquivo, palavra-gatilho, formato)])
S = {
# ---------------- HOOK ----------------
"b01": ("A", "", "Abre baixo, dentro de nuvens escuras sobre a serra gaúcha em relevo (satélite + ETOPO); a câmera desce e pousa em Caxias do Sul (pino coral). Coluna de chuva 3D cai sobre a cidade; um pluviômetro gigante ao lado enche.",
        ["cartão de lugar CAXIAS DO SUL (RS) · 2 DE MAIO DE 2024", "na palavra 'duzentos': pluviômetro sobe 0 → 266 MM; marca fantasma do recorde anterior 94 MM (2017) bem embaixo", "selo QUASE 3× O RECORDE", "nasce a GOTA luminosa (fio condutor) no fundo do pluviômetro"], []),
"b02": ("A", "dolly longo para sudeste seguindo a gota (whoosh)", "A gota escorre do pluviômetro para um vale e a câmera a segue em voo rasante 100 km até Porto Alegre; régua de nível vertical cravada no Guaíba (componente 'régua' do longo-04) sobe até 5,35 M; a orla da cidade afunda sob o plano de água.",
        ["régua de distância 100 KM entre os dois pinos", "cartão de lugar PORTO ALEGRE (RS) · 5 DE MAIO DE 2024", "régua 5,35 M com marca fantasma 1941 · 4,76 M", "frase-âncora em tipografia grande, 2 linhas: A CHUVA MAIS PESADA CAIU NA SERRA. / QUEM AFUNDOU FOI PORTO ALEGRE."],
        [(SAT + "nasa-landsat8-porto-alegre-alagado-2024-05-08.jpg", "Porto Alegre", "fundo 2 s antes do 3D (satélite real), legenda PORTO ALEGRE · LANDSAT 8 · 8 MAI 2024")]),
"b03": ("A", "corte seco para foto (impacto grave)", "Sequência de 3 fotos aéreas reais em quadro grande (polaroid escura, sem tachinha bege), câmera em Ken Burns lento; volta ao 3D da orla alagada no fim.",
        ["contador ~160 MIL PESSOAS ATINGIDAS · PORTO ALEGRE (etiqueta SEGUNDO A PREFEITURA)", "na palavra 'Defesa Civil': card sóbrio navy 184 MORTES · RS (DEFESA CIVIL, BALANÇO DE 24/04/2025), sem ícone"],
        [(F + "centro-historico-rodoviaria-cais-mauah-alagados-aereo-2024-05-05.jpg", "capital", "quadro grande 3 s; legenda CENTRO HISTÓRICO · PORTO ALEGRE · 5 MAI 2024"),
         (F + "rodoviaria-viaduto-cais-maua-alagados-aereo-2024-05-05.jpg", "rodoviária", "quadro grande 2,5 s; legenda RODOVIÁRIA · PORTO ALEGRE · 5 MAI 2024"),
         (F + "aeroporto-salgado-filho-pista-alagada-aereo-2024-05-05.jpg", "aeroporto", "quadro grande 2,5 s; legenda AEROPORTO SALGADO FILHO · 5 MAI 2024")]),
"b04": ("B", "corte seco de volta ao mapa (impacto suave)", "Relevo editorial do RS; duas colunas de chuva lado a lado: Porto Alegre (564,8 mm em maio) e Caxias do Sul (919 mm em maio). Na pergunta, a câmera começa a subir.",
        ["colunas PORTO ALEGRE 565 MM · CAXIAS DO SUL 919 MM (MAIO DE 2024, INMET)", "pergunta em tipografia: COMO A CHUVA DA SERRA FOI PARAR DENTRO DE PORTO ALEGRE?"], []),
"b05": ("A", "subida vertical (whoosh longo)", "Câmera sobe até ver o centro-nordeste do RS inteiro em relevo escuro. A ÁRVORE DE RIOS acende: cada rio principal se desenha em ciano grosso da nascente à foz, na ordem da fala, e todos convergem num ponto brilhante em frente a Porto Alegre.",
        ["etiquetas navy JACUÍ · TAQUARI · CAÍ · SINOS · GRAVATAÍ (pop na palavra)", "pino PORTO ALEGRE + rótulo GUAÍBA no ponto de convergência"], []),
"b06": ("B", "", "Mesmo plano; a Região Hidrográfica do Guaíba ganha um tom mais claro e o resto do estado escurece; afluentes finos aparecem como textura. Ao sul do Guaíba, um único canal estreito acende (a saída).",
        ["selo LAGO GUAÍBA (OFICIAL) · RIO? (pequeno, riscado não: só 'RIO?' em cinza)", "número grande ~1/3 DO RS (QUASE UM TERÇO)", "seta curta ciano na saída: 1 SAÍDA", "na palavra 'caminho': a gota reaparece na serra, pronta para a viagem"], []),
# ---------------- 1. A CHUVA DA SERRA ----------------
"b07": ("A", "push-in através das nuvens (whoosh longo)", "Abertura do cap. 1: céu 3D sobre o RS; uma frente fria (faixa azul de nuvens) desliza do sudoeste e PARA sobre o estado; ao norte, uma cúpula alaranjada translúcida (bloqueio de ar quente); setas finas de umidade vindo do norte alimentam as nuvens.",
        ["aba 1 · A CHUVA DA SERRA", "rótulos FRENTE FRIA (PARADA) · BLOQUEIO · UMIDADE DO NORTE", "selo esquemático (sem número)"], []),
"b08": ("B", "", "Mapa do RS em relevo editorial com o calendário 24/04 → 04/05 correndo num canto; a chuva acumulada pinta o estado em azul crescente (escala esquemática, sem dado por pixel).",
        ["contador 0 → 420 MM (MÉDIA DO ESTADO, 24/04–04/05, WWA)", "comparação lateral: 3 barras = 3 MESES DE CHUVA × 1 barra = 11 DIAS"], []),
"b09": ("B", "whip pan para a serra (swish)", "Câmera baixa sobre o planalto e a serra; colunas de chuva 3D sobre Caxias do Sul e Santa Maria (as mais altas do mapa).",
        ["coluna CAXIAS DO SUL 707 MM · 1–13 MAI", "coluna SANTA MARIA · MAIOR CHUVA DIÁRIA EM 112 ANOS (01/05)", "rótulo ONDE NASCEM OS RIOS"], []),
"b10": ("B", "", "Linha do tempo horizontal em relevo de régua (componente do longo-04): três picos de cheia SET/2023, NOV/2023, MAI/2024 crescendo; o terceiro estoura o quadro.",
        ["marcas TAQUARI ACIMA DE 1941 · SET 2023", "GUAÍBA > 3 M · NOV 2023", "contador 3 CHEIAS EM 8 MESES"], []),
"b11": ("A", "orbit lento (sem corte)", "Perfil de relevo: corte 3D de Caxias (~800 m) até Porto Alegre (~nível do mar), exagero vertical; a gota desce pelo perfil, rápida nos vales estreitos.",
        ["régua de altitude 800 M → 0 M", "rótulo VALES ESTREITOS E FUNDOS"], []),
"b12": ("A", "dolly ao longo do vale (whoosh médio)", "Câmera voa pelo vale do Taquari em satélite + relevo; régua cravada no rio em Lajeado sobe até 33,7 M; o fundo do vale afunda sob o plano de água.",
        ["pino LAJEADO", "régua 33,7 M com marca fantasma 1941 · 29,92 M", "selo +3 M ACIMA DE 1941"],
        [(F + "arroio-do-meio-navegantes-destruicao-aereo-2024-06-06.jpg", "Cidades", "quadro grande 3 s; legenda ARROIO DO MEIO · VALE DO TAQUARI · JUN 2024 (depois da cheia)")]),
"b13": ("A", "", "A gota sai de Lajeado, entra no Jacuí (fio ciano) e corre para o leste; câmera acompanha de cima até ver Porto Alegre ao fundo.",
        ["etiquetas TAQUARI → JACUÍ → PORTO ALEGRE"], []),
# ---------------- 2. O LAGO QUE RECEBE TUDO ----------------
"b14": ("A", "subida vertical até o mapa inteiro (whoosh longo)", "Abertura do cap. 2: a ÁRVORE DE RIOS completa (assinatura) acende de novo, agora com os mais de 250 municípios como pontinhos que piscam ao longo da rede; o contorno da bacia se fecha.",
        ["aba 2 · O LAGO QUE RECEBE TUDO", "contador 250+ MUNICÍPIOS", "número 85 MIL KM² · ~30% DO RS"], []),
"b15": ("B", "", "Relevo editorial: as 9 sub-bacias se acendem uma a uma em tons de ciano (Alto Jacuí, Pardo, Vacacaí, Baixo Jacuí, Taquari-Antas, Caí, Sinos, Gravataí, Lago Guaíba); os rios engrossam na direção do Guaíba.",
        ["etiquetas JACUÍ · TAQUARI · CAÍ · SINOS · GRAVATAÍ", "rótulo final O MESMO LAGO: GUAÍBA"], []),
"b16": ("A", "push-in no Guaíba (whoosh)", "Câmera baixa sobre o Guaíba em satélite real (01/04/2024, sem cheia); corte de seção 3D mostrando o lago largo e raso, com uma pessoa de escala na margem.",
        ["número ~500 KM² · ~2 M DE FUNDURA MÉDIA", "rótulo LARGO E RASO", "na palavra 'sobe': o plano de água sobe e se espalha pelas margens"],
        [(SAT + "hls-sentinel2-porto-alegre-guaiba-antes-2024-04-01.jpg", "Guaíba", "fundo de satélite do plano; legenda GUAÍBA · SENTINEL-2 · 1 ABR 2024")]),
"b17": ("B", "", "Medidor de vazão (componente novo simples): um cano/rio estilizado com o número de vazão; dia normal → maio (o ponteiro passa do fim da escala).",
        ["pizza simples: JACUÍ + TAQUARI = QUASE TUDO", "vazão NORMAL ~1.200 M³/S (DMAE)", "selo MAIO: ACIMA DAS MAIORES JÁ MEDIDAS"], []),
"b18": ("B", "", "Calendário de 5 dias (QUI 2 → SEG 6) sobre o mapa: cada rio pulsa no seu dia de pico e manda uma onda ciano até o Guaíba; as ondas se empilham no ponto da capital.",
        ["marcas TAQUARI e CAÍ · QUI 2", "SINOS · SÁB 4", "JACUÍ · DOM 5", "GUAÍBA · DOM 5, MADRUGADA · 5,35 M"], []),
"b19": ("A", "zoom-out lento (sem corte)", "Árvore de rios inteira, toda acesa, escoando para o ponto; na última frase o ponto do Guaíba incha em frente à cidade (pino PORTO ALEGRE).",
        ["frase em tipografia grande: O LAGO NA FRENTE DA CIDADE RECEBE TUDO"], []),
# ---------------- 3. A SAÍDA ----------------
"b20": ("A", "pan para o sul (whoosh longo)", "Abertura do cap. 3: câmera desce do Guaíba para o sul e revela a Lagoa dos Patos inteira em satélite + relevo.",
        ["aba 3 · A SAÍDA", "rótulo LAGOA DOS PATOS"],
        [(SAT + "nasa-modis-sul-do-rs-durante-2024-05-06.jpg", "Lagoa dos Patos", "fundo de 2 s (MODIS real, água turva descendo a lagoa); legenda LAGOA DOS PATOS · MODIS · 6 MAI 2024")]),
"b21": ("A", "dolly longo para o sul (whoosh)", "Voo de 250 km pela laguna até a barra de Rio Grande; os dois molhes de pedra 3D apertam a passagem.",
        ["régua 250 KM ao longo da laguna", "rótulos LAGUNA · LIGADA AO MAR · RIO GRANDE", "etiqueta na barra: SAÍDA ESTREITA"],
        [(F + "rio-grande-fragata-f44-canal-da-barra-molhes-2023-08-15.jpg", "molhes", "quadro médio 2 s; legenda CANAL DA BARRA · RIO GRANDE · 2023")]),
"b22": ("B", "", "Esquema em relevo editorial do caminho inteiro: bacia (árvore) → lago raso → laguna longa → gargalo; a gota percorre as 4 etapas em velocidade crescente e engasga no gargalo.",
        ["ícones 1/3 DO ESTADO → LAGO RASO → 250 KM → GARGALO"], []),
"b23": ("A", "", "Lagoa dos Patos em 3D; setas de vento do sul (fitas brancas) varrem a laguna e a água 'empilha' para o norte, contra o Guaíba.",
        ["setas VENTO SUL", "rótulo ATÉ ~50 CM A MAIS (IPH/UFRGS)", "selo pequeno AGRAVANTE, NÃO A CAUSA PRINCIPAL"], []),
"b24": ("B", "", "Calendário de maio em barra: pico do Guaíba (05/05) e picos da laguna (16 e 27/05); pinos Pelotas, São Lourenço do Sul, Rio Grande acendem em ciano; régua do Guaíba com faixa de inundação mostrada por ~30 dias.",
        ["marcas GUAÍBA 5/5 · LAGOA 16/5 e 27/5", "contador ~1 MÊS ACIMA DA COTA DE INUNDAÇÃO"],
        [(F + "pelotas-bairros-alagados-aereo-2024-05-18.jpg", "Pelotas", "quadro médio 2,5 s; legenda PELOTAS · 18 MAI 2024")]),
# ---------------- 4. O QUE CEDEU ----------------
"b25": ("arquivo", "corte seco para papel (impacto suave)", "Abertura do cap. 4: papel sépia com foto de 1941 em domínio público; régua 1941 · 4,7 M; calendário 'MAIS DE UM MÊS'.",
        ["aba 4 · O QUE CEDEU", "carimbo 1941"],
        [(F + "mercado-publico-fachada-alagado-enchente-1941-05.jpg", "mil novecentos e quarenta e um", "quadro médio no papel 3 s; legenda MERCADO PÚBLICO · PORTO ALEGRE · MAIO DE 1941 (sem zoom; foto de 800 px, formato 'carte')")]),
"b26": ("B", "transição papel → mapa 3D (whoosh)", "Maquete 3D da orla de Porto Alegre (relevo editorial): o sistema de proteção se desenha peça a peça na ordem da fala: muro da Mauá (cinza claro, centro), 68 km de diques (linha contínua), 14 comportas (pontos amarelos), 23 casas de bombas (cubos).",
        ["carimbo PROJETO 1943 · OBRAS ANOS 70", "contadores 68 KM DE DIQUES · 14 COMPORTAS · 23 CASAS DE BOMBAS"],
        [(F + "muro-da-maua-grafite-dia-normal-2016-04-23.jpg", "muro da Mauá", "quadro médio 2 s; legenda MURO DA MAUÁ · DIA NORMAL · 2016")]),
"b27": ("B", "", "Corte esquemático 3D do sistema: Guaíba à esquerda, muro/dique no meio, cidade à direita; comporta fecha; casa de bombas joga água da chuva por cima do dique. Na última frase, uma peça pisca em coral e uma fita de água acha a passagem.",
        ["rótulos MURO E DIQUES · COMPORTA (PORTÃO DE AÇO) · CASA DE BOMBAS", "frase SE UMA PEÇA FALHA, A ÁGUA ACHA O CAMINHO"],
        [(F + "comporta-cais-maua-fechamento-2024-05-02.jpg", "comportas", "quadro grande 3 s; legenda COMPORTA DO CAIS MAUÁ · 2 MAI 2024")]),
"b28": ("A", "pan para a zona norte (swish)", "Maquete 3D da zona norte (Navegantes / 4º Distrito, perto da av. Sertório): uma comporta pisca e a água ciano invade os quarteirões.",
        ["pino COMPORTA · AV. SERTÓRIO · 3 MAI 2024", "etiqueta NAVEGANTES"], []),
"b29": ("B", "", "As 23 casas de bombas como cubos sobre o mapa da cidade; na fala '19 das 23', 19 apagam (cinza) e 4 seguem acesas; setas de água da chuva presas do lado de dentro; uma seta do Guaíba entra por uma casa apagada.",
        ["contador 19 DE 23 PARADAS · NO PICO (DADOS DA PREFEITURA)", "rótulos SEM ENERGIA · INUNDADAS"], []),
"b30": ("A", "dolly (whoosh médio)", "Maquete do Sarandi: o dique baixo é vencido em dois pontos; a casa de bombas nº 10 afunda; o bairro enche.",
        ["pino SARANDI · ZONA NORTE", "etiqueta CASA DE BOMBAS Nº 10", "contador ~26 MIL PESSOAS ATINGIDAS (PREFEITURA)"], []),
"b31": ("B", "orbit para o centro", "Maquete do muro da Mauá inteiro com o Guaíba no pico (5,35) ABAIXO do topo do muro (régua ao lado); a água entra por trás, pelos pontos já mostrados (comporta, bombas, dique), em fitas coral.",
        ["selo A ÁGUA NÃO PASSOU POR CIMA DO MURO", "régua FALHAS DESDE ~4,5 M · CAPACIDADE DECLARADA 6 M (WWA)"], []),
"b32": ("arquivo", "", "Papel com três recortes tipográficos lado a lado (sem foto, sem rosto): MANUTENÇÃO (ex-diretores do DMAE) · CONCEPÇÃO (prefeitura) · GESTÃO (pesquisadores); carimbo EM DISCUSSÃO.",
        ["frase final NÃO SEGUROU"], []),
"b33": ("A", "voo baixo sobre o centro alagado", "A gota termina a viagem: entra no centro de Porto Alegre e se dissolve no plano de água; câmera passa sobre o Mercado Público e os bairros citados acendendo em ciano.",
        ["marca 1,5 M no Mercado Público", "etiquetas MENINO DEUS · FARRAPOS · HUMAITÁ · ILHAS", "número ~30% DO TERRITÓRIO DA CAPITAL (PREFEITURA)"],
        [(F + "mercado-publico-ilhado-aereo-2024-05-05.jpg", "Mercado Público", "quadro grande 3 s; legenda MERCADO PÚBLICO · 5 MAI 2024"),
         (F + "centro-historico-edificios-historicos-alagados-aereo-2024-05-05.jpg", "território", "quadro grande 2,5 s; legenda CENTRO HISTÓRICO · 5 MAI 2024")]),
# ---------------- A RESPOSTA ----------------
"b34": ("A", "zoom-out até o estado inteiro (whoosh longo)", "Volta à serra: Caxias e o pluviômetro do b01, a árvore de rios apagada esperando.",
        ["aba A RESPOSTA", "pergunta do T1 em tipografia: POR QUE A CHUVA DA SERRA ALAGOU PORTO ALEGRE?"], []),
"b35": ("A", "", "A viagem da gota em reprise acelerada, uma camada por frase: chuva sobre a serra → 3 cheias em 8 meses (ícone) → árvore de rios acende e converge no Guaíba com as ondas chegando juntas.",
        ["checklist que se preenche: ✓ 3 MESES DE CHUVA EM 11 DIAS · ✓ RIOS JÁ CHEIOS · ✓ 1/3 DO ESTADO, 1 LAGO"], []),
"b36": ("A", "", "Continua: Guaíba → laguna → gargalo (saída lenta) → maquete da cidade com as falhas piscando em coral.",
        ["checklist: ✓ SAÍDA LENTA · ✓ DEFESA CEDEU NOS PONTOS FRACOS"], []),
"b37": ("B", "", "Card de dados sobre o mapa escuro (estilo do longo-02): duas barras de probabilidade e intensidade.",
        ["WWA (03/06/2024): CHANCE > 2× · CHUVA 6–9% MAIS INTENSA (AQUECIMENTO)", "EL NIÑO: PESO PARECIDO"], []),
"b38": ("A", "orbit lento", "A árvore de rios do RS de hoje, calma, escoando devagar para o Guaíba; nada de chuva na tela.",
        ["selo NÃO É PREVISÃO", "frase A GEOGRAFIA NÃO MUDA"], []),
"b39": ("B", "", "Maquete da orla com as comportas que serão concretadas marcadas em cinza sólido; ícone de celular com alerta da Defesa Civil.",
        ["card SMS: CEP PARA 40199 (DEFESA CIVIL)", "rótulo OBRAS ANUNCIADAS PELA PREFEITURA"],
        [(F + "cais-maua-galpao-marcas-da-enchente-2026-03-12.jpg", "concreto", "quadro médio 2 s; legenda CAIS MAUÁ · MARCAS DA ENCHENTE · 2026")]),
"b40": ("B", "", "Encerramento do canal: card do vídeo sobre o clima do Sul (bG6-E4qjXYc, publicado) + logo EM RELEVO + botão inscrever (sem card de próximo vídeo).", [], []),
}

assert set(S) == set(bl), sorted(set(bl) ^ set(S))
t, out, cenas = 0.4, [], []
for bid, b in bl.items():
    est, trans, plano, camadas, midias = S[bid]
    nw = len(re.findall(r"\w+", b["fala"])); dur = round(nw / 2.9 + 0.7, 1)
    out.append({"id": bid, "cap": b["cap"], "t_est": round(t, 1), "dur_est": dur, "estilo": est, "transicao": trans, "plano": plano,
                "camadas": camadas, "midias": [{"arquivo": m[0], "gatilho": m[1], "formato": m[2]} for m in midias]})
    for m in midias:
        assert (R / m[0]).exists(), m[0]
        cenas.append({"bloco": bid, "tipo": "foto", "arquivo": m[0], "gatilho": m[1], "formato": m[2]})
    cenas.append({"bloco": bid, "tipo": "mapa" if est in "AB" else "arquivo", "estilo": est, "descricao": plano})
    t += dur
json.dump({"_doc": "Etapa 1: plano por bloco (tempos estimados). A etapa 2 converte em cues.json amarrado ao Whisper.", "duracao_est_s": round(t, 1), "blocos": out},
          open(A / "storyboard.json", "w"), ensure_ascii=False, indent=1)
json.dump({"_doc": "Lista plana de planos/mídias (nenhuma imagem de IA; fotos de dl/fotos/video/ e dl/fotos/satelite/).", "cenas": cenas}, open(A / "cenas.json", "w"), ensure_ascii=False, indent=1)
def mmss(x): return f"{int(x // 60)}:{x % 60:04.1f}"
L = ["| Bloco | Tempo est. | Estilo | Entrada | Plano | Camadas | Mídias |", "|---|---|---|---|---|---|---|"]
for o in out:
    L.append(f"| {o['id']} | {mmss(o['t_est'])} | {o['estilo']} | {o['transicao'] or '—'} | {o['plano']} | {'; '.join(o['camadas']) or '—'} | {'; '.join(m['arquivo'].split('/')[-1] + ' (' + m['formato'] + ')' for m in o['midias']) or '—'} |")
(R / "work").mkdir(exist_ok=True); open(R / "work/storyboard-tabela.md", "w").write("\n".join(L) + "\n")
usadas = sorted({c["arquivo"].split('/')[-1] for c in cenas if c["tipo"] == "foto"})
tA = sum(o["dur_est"] for o in out if o["estilo"] == "A"); tB = sum(o["dur_est"] for o in out if o["estilo"] == "B"); tR = sum(o["dur_est"] for o in out if o["estilo"] == "arquivo")
print(f"duração estimada {mmss(t)}; A {tA:.0f} s, B {tB:.0f} s, arquivo {tR:.0f} s; {len(usadas)} fotos/satélites distintos: {', '.join(usadas)}")
