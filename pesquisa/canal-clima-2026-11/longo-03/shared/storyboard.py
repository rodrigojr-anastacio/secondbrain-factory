# Storyboard do longo 03 (Grande Seca de 1877): plano por bloco -> shared/storyboard.json, shared/cenas.json e work/storyboard-tabela.md.
# Etapa 1 (13/11/2026). Tempos ESTIMADOS (2,9 palavras/s, ritmo do longo-02); a etapa 2 amarra cada evento à palavra no Whisper
# (shared/build_cues.py, mesmo método do longo-02) e grava cues.json. Nada aqui é imagem gerada por IA: mapa 3D (terreno_v2 do
# longo-02), dados reais (dados/*.json) e fotos de dl/fotos/video/ (licenças em pesquisa/FOTOS.md; créditos só na descrição).
# Estilos (estilo_v2 do longo-02): A = satélite (Blue Marble + relevo ETOPO), mundo real/impacto; B = relevo editorial, dado/rótulo.
# "arquivo" = corte seco para o tratamento sépia de papel (foto de época grande, como as T3/T14 do longo-02).
import json, re
from pathlib import Path
A = Path(__file__).parent; R = A.parent
bl = {b["id"]: b for b in json.load(open(A / "blocos.json"))}

# id: (estilo, transição de entrada ou "", plano principal, camadas/overlays, mídias [(arquivo, palavra-gatilho, formato)])
S = {
# ---------------- HOOK ----------------
"b01": ("A", "", "Abre no Nordeste em satélite ao entardecer, câmera baixa sobre o sertão seco do Ceará; dolly até a costa e pousa em Fortaleza (pino coral).",
        ["cartão de lugar FORTALEZA · 1878", "contador de população 25 MIL (ícones de gente empilhados ao lado do pino)", "na palavra 'chegam': rios de pontinhos claros saem do sertão (Quixadá, Crato, Icó, Sobral) e escorrem até Fortaleza; contador sobe para 100 MIL+"],
        [("fortaleza-planta-1875.jpg", "cidade", "quadro grande à direita, 3 s, papel antigo")]),
"b02": ("A", "", "Câmera parada sobre Fortaleza; os pontinhos continuam chegando e formam mancha ao redor da planta da cidade.",
        ["contador 160 MIL (Theophilo) com etiqueta 'SEGUNDO RODOLPHO THEOPHILO, QUE VIVEU AQUILO'", "barra comparativa 25 MIL × 160 MIL = '6×'"],
        [("teofilo-vacinando-1907.jpg", "Theophilo", "quadro grande à esquerda 4 s; legenda 'RODOLPHO THEOPHILO (À DIREITA) · FORTALEZA · 1907'")]),
"b03": ("arquivo", "corte seco no impacto (impacto grave)", "Tela de papel sépia: data 10/12/1878 carimbada; número 1.004 grande cresce em tinta.",
        ["número 1.004 em contador rápido", "legenda MORTOS DE VARÍOLA · 1 DIA"], []),
"b04": ("B", "corte seco de volta ao mapa (impacto suave)", "Zoom-out do Ceará para o Brasil inteiro em relevo editorial; províncias do Norte de 1877 (CE, RN, PB, PE, PI, AL, SE, BA) tingidas de coral.",
        ["contador 500 MIL (etiqueta 'ESTIMATIVAS')", "pizza/anel 5% DA POPULAÇÃO DO IMPÉRIO", "título A GRANDE SECA · 1877–1879"], []),
"b05": ("B", "", "Câmera parada; o coral pulsa; aparece no canto o Pacífico com o relevo de calor de 2026 (miniatura do longo-02) e '1877 ↔ 2026'.",
        ["rótulo QUASE NINGUÉM FALA DELA (papel rasgado)", "pergunta: E EM 2026?"], []),
"b06": ("B", "", "Câmera parada; barra das 4 perguntas (mesmo componente do longo-02) entra pergunta a pergunta.",
        ["barra 4 perguntas: O QUE ACONTECEU? · POR QUE NÃO CHOVEU? · O QUE MUDOU NO MAPA? · E EM 2026?"], []),
"b07": ("B", "", "Câmera desce para o Ceará; calendário em anel de 12 meses ao lado do mapa: FEV–MAI acende (gotas), o resto apaga.",
        ["anel de meses com a quadra chuvosa FEV–MAI destacada", "rótulo O 'INVERNO' DO SERTÃO"], []),
# ---------------- 1. O QUE ACONTECEU ----------------
"b08": ("A", "push-in que atravessa nuvens secas (whoosh longo)", "Abertura do cap. 1: sertão do Ceará em satélite, terreno seco; céu sem nuvem.",
        ["barra das perguntas: ▶ 1/4", "folhinha 19 DE MARÇO · SÃO JOSÉ com gota que não cai"], [("hoje-santa-quiteria-2018.jpg", "chuva", "quadro grande (cenário do sertão seco; legenda com lugar e ano reais)")]),
"b09": ("B", "whip pan para o gráfico (swish)", "Régua de montanhas (componente do longo-02) com 153 barras = chuva anual de Fortaleza 1849–2018; linha da média 1.450 mm.",
        ["barras crescem da esquerda para a direita", "na palavra 'quatrocentos': 1877 afunda e acende em coral (468 MM · 32%)", "'segundo': 1878 acende (503 MM)", "pluviômetro lateral: 1.450 × 468"], []),
"b10": ("A", "whip pan de volta ao mapa (swish)", "Sertão em satélite, câmera em órbita lenta; o verde (se houver) dessatura para marrom.",
        ["ícones simples: pasto, gado, roça (milho/feijão/mandioca) riscados em sequência"], [("hoje-coremas-seca-2017.jpg", "gado", "quadro grande, panorâmica")]),
"b11": ("B", "", "Ceará em relevo editorial com contorno; contador 721.686 (1872); pontinhos espalhados pelo estado inteiro.",
        ["CEARÁ · 1872 · 721 MIL HABITANTES (censo)"], [("mapa-seca-1877-rebouças.jpg", "andou", "documento grande à direita com pan lento (mapa da região da seca de 1877)")]),
"b12": ("A", "", "Plano-assinatura: câmera alta, os pontinhos viram rios que 'escorrem' pelos vales (seguindo o relevo real e os rios Jaguaribe, Banabuiú, Acaraú, Curu) até a costa.",
        ["rótulo RETIRANTES (entra na palavra)", "rios de dados/rios-ce.json acesos fracos"], [("retirantes-1878-grupo.jpg", "retirantes", "carte-de-visite pequena (é o tamanho original da foto) pousada sobre o mapa, moldura de papel; 4 s")]),
"b13": ("B", "rack focus para Fortaleza (whoosh médio)", "Fortaleza em zoom: planta de 1875 (Herbster) estendida sobre o terreno como textura; ao redor, barracas (ícones) se multiplicam nos arredores.",
        ["contador ABARRACADOS · AGO/1878 → 113.900", "rótulo ABARRACAMENTOS"], [("fortaleza-planta-1875.jpg", "Fortaleza", "textura sobre o mapa (não quadro)")]),
"b14": ("A", "", "Rota de navios chegando ao porto de Fortaleza (linhas do mar para a costa); sacos empilhados que não sobem até o sertão.",
        ["etiquetas carimbadas CARNE ESTRAGADA · FARINHA COM CAL (DENÚNCIAS, 1878)"], [("mapa-seca-1878-ferrovias.jpg", "mar", "documento grande, detalhe do litoral cearense")]),
"b15": ("arquivo", "corte seco (impacto grave)", "Papel sépia com calendário de 1878; manchas de varíola (pontos coral) se espalham pela planta de Fortaleza.",
        ["barras mensais: NOV 9.844 · DEZ 15.352 (14.491 VARÍOLA)"], [("retirante-corrêa-1877-a.jpg", "fome", "carte-de-visite pequena no papel, SEM zoom no corpo; 4 s; legenda CEARÁ · 1877")]),
"b16": ("arquivo", "", "Mesmo papel; o '10' de dezembro é circulado em tinta; 1.004 volta (paga o hook).",
        ["1.004 · 10/12/1878", "rótulo O DIA DOS MIL MORTOS (tipografia de jornal)"], []),
"b17": ("B", "corte seco de volta ao mapa colorido (impacto suave)", "Nordeste em relevo editorial; faixa 150 MIL ↔ 500 MIL como régua com ponta incerta (degradê).",
        ["régua de estimativas: 150 MIL (NYT, 1879) · 400–500 MIL (estimativas)", "linha do tempo 1877 · 1878 · 1879 · 1880 (gota volta em 1880)"], []),
"b18": ("arquivo", "match cut: o mapa vira a página de jornal (impacto suave + whoosh)", "Mesa de papel com recortes: cartes-de-visite de retirantes lado a lado, como foram publicadas.",
        ["rótulo RIO DE JANEIRO · 1878 · O BESOURO", "carimbo 'PRIMEIRO FOTOJORNALISMO DO BRASIL?'"],
        [("retirante-corrêa-1878-b.jpg", "fotografias", "carte-de-visite original com moldura dourada, pequena"), ("retirantes-1878-grupo.jpg", "fotografias", "carte-de-visite pequena"), ("patrocinio-1879.jpg", "historiadores", "retrato pequeno no canto (José do Patrocínio, que trabalhou com Corrêa na série)")]),
# ---------------- 2. POR QUE NÃO CHOVEU ----------------
"b19": ("A", "zoom-out orbital do Ceará até o globo (whoosh longo)", "Globo em satélite gira do Atlântico para o Pacífico.", ["barra das perguntas: ▶ 2/4"], []),
"b20": ("A", "", "Maquete do Pacífico (mesa do longo-02) com o RELEVO DE CALOR de nov/1877–fev/1878 (dados/sst_1877.json) subindo; depois régua de montanhas Niño 3.4 (dados/nino34-resumo.json, NDJ): 1877 · 1982 · 1997 · 2015 lado a lado.",
        ["rótulo PACÍFICO · DEZ/1877 · RECONSTRUÇÃO", "montanhas: 1877 +2,4 · 1982 +2,1 · 1997 +2,4 · 2015 +2,6 °C (fonte na descrição: NOAA ERSSTv5)"], []),
"b21": ("A", "", "Circulação de Walker (componente do longo-02): ar sobe sobre o Pacífico quente, setas descem sobre o norte do Nordeste.",
        ["card 'ASSISTA: EL NIÑO 2026' (vídeo anterior) por 3 s", "seta AR QUE DESCE = SEM NUVEM"], []),
"b22": ("B", "whip pan para o Atlântico (swish)", "Atlântico tropical em relevo editorial; faixa de nuvens (ZCIT) como fita branca animada sobre o equador; Atlântico Norte ganha véu coral e a fita sobe para o norte, deixando o Ceará descoberto.",
        ["rótulos ATLÂNTICO NORTE MAIS QUENTE · FAIXA DE NUVENS (ZCIT) · CEARÁ SEM CHUVA", "selo 1878 · RECORDE NO ATLÂNTICO NORTE"], []),
"b23": ("A", "zoom-out orbital até o globo inteiro (whoosh longo)", "Globo com a anomalia de dez/1877 (dados/sst_1877_global.json); 3 pinos: Nordeste do Brasil, Índia (Madras/Bombaim/Mysore), norte da China (Shanxi/Henan/Shandong); fios vermelhos ligando os 3.",
        ["contadores por pino: ÍNDIA 5,5–9,6 MI · CHINA 9–13 MI · BRASIL ATÉ 500 MIL"], [("india-1877-graphic-bellary.jpg", "Índia", "quadro grande (gravura de jornal de 1877); não há imagem da fome na China com licença: o pino da China fica só no globo")]),
"b24": ("A", "", "Globo gira devagar com os 3 pinos acesos.", ["número > 50 MILHÕES (etiqueta 'ESTIMATIVAS')", "selo ESTUDO DE 2018 · JOURNAL OF CLIMATE"], []),
"b25": ("B", "rack focus de volta ao Ceará (whoosh médio)", "Ceará em relevo editorial em 1877: só o trecho Fortaleza–Pacatuba da ferrovia existe (linha curta); interior vazio; ícone de navio no porto e trilhas a pé até o sertão.",
        ["rótulos 0 GRANDES AÇUDES · FERROVIA: SÓ ATÉ PACATUBA (1873)"], []),
"b26": ("arquivo", "corte seco (impacto grave)", "Papel do Senado: citação em tipografia de época, aspas grandes.",
        ["citação “A SOLUÇÃO DEPENDE DA DIVINA PROVIDÊNCIA, E NÃO DE NÓS.” — SINIMBU, CHEFE DO GOVERNO", "carimbo CPI · NÃO APROVADA"], []),
# ---------------- 3. O QUE MUDOU NO MAPA ----------------
"b27": ("A", "corte seco de volta ao mapa, luz da manhã (whoosh médio)", "Ceará em satélite, câmera alta; abertura do cap. 3.", ["barra das perguntas: ▶ 3/4"], []),
"b28": ("B", "", "A Estrada de Ferro de Baturité se desenha como fio vermelho sobre o relevo (dados/historia.json): Fortaleza → Baturité (1882) → Quixadá (1891), etiquetas de ano surgindo nas estações.",
        ["etiquetas 1878 OBRA DE SOCORRO · 1882 BATURITÉ · 1891 QUIXADÁ", "ícones de retirantes trabalhando ao longo da linha"],
        [("ferrovia-baturite-estacao.jpg", "Baturité", "quadro grande (estação de 1882, foto de hoje)"), ("ferrovia-quixada-estacao.jpg", "Quixadá", "quadro grande")]),
"b29": ("B", "whip pan para o norte (swish)", "Ferrovia Camocim → Sobral se desenha (31/12/1882).", ["etiqueta SOBRAL · 31/12/1882"], [("mapa-seca-1878-ferrovias.jpg", "ferrovia", "documento de época com as ferrovias de socorro, detalhe")]),
"b30": ("A", "whip pan para Quixadá (swish)", "Mergulho no relevo real dos monólitos de Quixadá; pino AÇUDE DO CEDRO; o lago enche em azul (animação simples do espelho d'água).",
        ["etiquetas 1884 → 1906 · 22 ANOS", "rótulo 1º GRANDE AÇUDE PÚBLICO DO PAÍS"],
        [("cedro-galinha-choca-pd.jpg", "Galinha", "quadro GRANDE (a foto mais bonita do vídeo), 5 s"), ("cedro-barragem-detalhe.jpg", "República", "quadro grande")]),
"b31": ("arquivo", "corte seco (impacto suave)", "Papel com coroa desenhada em traço; carimbo LENDA sobre a frase.",
        ["frase atribuída em itálico", "carimbo coral SEM DOCUMENTO"], []),
"b32": ("A", "zoom-out orbital do Ceará para a América do Sul (whoosh longo)", "Rota marítima pontilhada animada Fortaleza → Belém → Manaus (dados/historia.json); navios pequenos; a floresta em satélite.",
        ["contador AMAZONAS · JUN/1877–AGO/1878 → 4.963", "rótulo PASSAGEM PAGA PELO GOVERNO"], [("seringal-acre-1910.jpg", "borracha", "quadro grande, vertical à direita")]),
"b33": ("B", "", "A rota sobe o Purus até o Acre; o Acre aparece listrado (BOLÍVIA) e, na palavra 'mil novecentos e três', vira coral (BRASIL) com selo TRATADO DE PETRÓPOLIS.",
        ["etiquetas SERINGUEIROS NORDESTINOS · ACRE: BOLÍVIA → BRASIL · 1903"], [("seringueiro-acre-2010.jpg", "seringueiros", "quadro médio (foto de hoje; legenda com o ano real)")]),
"b34": ("B", "", "Câmera abre para o Brasil inteiro: a fronteira oeste brilha em coral, ligada por fio vermelho ao Ceará.", ["rótulo A SECA AJUDOU A DESENHAR A FRONTEIRA"], []),
"b35": ("arquivo", "corte seco (impacto grave)", "Mapa do Ceará em papel sépia com 7 pinos dos campos de 1932 (Fortaleza ×2, Senador Pompeu, Crato, Quixeramobim, Cariús, Ipu) e 1 de 1915 (Alagadiço); cercas desenhadas em traço.",
        ["etiquetas 1915 · ALAGADIÇO · 1932 · 7 CAMPOS · +70 MIL", "rótulo 'CURRAIS DO GOVERNO'"], []),
"b36": ("B", "corte seco de volta ao mapa (impacto suave)", "Semiárido oficial (dados/semiarido.json) se desenha sobre o Nordeste em relevo editorial.", ["selo 1909 · INSPETORIA DE OBRAS CONTRA AS SECAS → DNOCS"], []),
"b37": ("B", "", "Câmera parada sobre o Ceará; quatro fichas de papel entram uma a uma (POBRES DO SERTÃO · LONGE DA CAPITAL · CORPOS SEM CONTAGEM · CPI BARRADA); a última vira uma pilha de anos de seca (1915, 1932, 1958, 1983, 2012).", [], []),
# ---------------- 4. E EM 2026? ----------------
"b38": ("A", "zoom-out orbital até o globo (whoosh longo)", "Globo de hoje; Pacífico com o relevo de calor de out/2026 (dados/sst_comparativo.json).", ["barra das perguntas: ▶ 4/4"], []),
"b39": ("A", "", "Maquete do Pacífico: o relevo de calor de 1877 (fantasma, contorno) e o de 2026 (cheio) sobrepostos; régua Niño 3.4 com 2026 crescendo ao vivo até passar 1877.",
        ["montanhas 1877 · 2026 (fonte na descrição: NOAA ERSSTv5, mesma base)", "card PREVISÃO NOV–JAN: CHUVA ABAIXO DA MÉDIA EM ÁREAS DO NE (INMET)"], []),
"b40": ("B", "whip pan para o Atlântico/Ceará (swish)", "Ceará em relevo editorial; anel de meses de novo com FEV–MAI 2027 em interrogação; fita da ZCIT oscila sobre o Atlântico.",
        ["rótulo O QUE DECIDE: FEV–MAI 2027", "selo FUNCEME: AINDA É CEDO"], []),
"b41": ("B", "", "Monitor de Secas de set/2026 (dados/monitor-secas-2026-09.json) tinge o Nordeste nas cores S0–S2.", ["contador 96% DO NORDESTE EM SECA · SET/2026"], []),
"b42": ("A", "", "Sertão em satélite de hoje; pinos se acendem em cachos (cisternas, ilustrativo), Castanhão em azul, linha da transposição (Eixo Norte) chegando ao Ceará.",
        ["contador 1,2 MILHÃO DE CISTERNAS", "etiquetas CASTANHÃO · TRANSPOSIÇÃO · 2020"],
        [("hoje-castanhao.jpg", "Castanhão", "quadro grande"), ("hoje-transposicao-jati.jpg", "transposição", "quadro grande (satélite; cortar a borda preta)")]),
"b43": ("B", "", "Linha do tempo de secas 1877 → 2012–2017 com marcador de mortes em massa só em 1877.", ["régua 1877 · 1915 · 1932 · 2012–2017", "ícones carro-pipa/emergência sobre 2012–2017"],
        [("hoje-pipa-caninde-2026.jpg", "carro-pipa", "quadro grande")]),
"b44": ("A", "", "Sertão de hoje em satélite ao entardecer, câmera em órbita lenta.", ["ícones simples: torneira, colheita, gado, termômetro"], []),
# ---------------- A RESPOSTA ----------------
"b45": ("A", "zoom-out: do sertão ao Nordeste inteiro (whoosh longo)", "Volta ao plano do hook: Fortaleza 1878 com os rios de pontinhos; os 3 fatores entram como pinos ligados por fio (PACÍFICO · ATLÂNTICO · GOVERNO).", ["contador 25 MIL → 100 MIL+ (reprise)"], []),
"b46": ("A", "", "Câmera sobe: ferrovia, Cedro e a rota até o Acre acendem juntos sobre o continente ao entardecer (os 'trilhos do mapa' do cap. 3).",
        ["frase final em tipografia grande: O QUE TRANSFORMA SECA EM TRAGÉDIA É O QUE SE FAZ ANTES DELA"], []),
"b47": ("B", "", "Encerramento do canal: logo EM RELEVO + card do próximo vídeo (Catarina: espiral no Atlântico Sul, silhueta) + botão inscrever.", ["card PRÓXIMO: O FURACÃO QUE NÃO DEVIA EXISTIR"], []),
}

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
json.dump({"_doc": "Lista plana de planos/mídias (nenhuma imagem de IA; fotos de dl/fotos/video/).", "cenas": cenas}, open(A / "cenas.json", "w"), ensure_ascii=False, indent=1)
def mmss(x): return f"{int(x // 60)}:{x % 60:04.1f}"
L = ["| Bloco | Tempo est. | Estilo | Entrada | Plano | Camadas | Mídias |", "|---|---|---|---|---|---|---|"]
for o in out:
    L.append(f"| {o['id']} | {mmss(o['t_est'])} | {o['estilo']} | {o['transicao'] or '—'} | {o['plano']} | {'; '.join(o['camadas']) or '—'} | {'; '.join(m['arquivo'] + ' (' + m['formato'] + ')' for m in o['midias']) or '—'} |")
(R / "work").mkdir(exist_ok=True); open(R / "work/storyboard-tabela.md", "w").write("\n".join(L) + "\n")
usadas = sorted({c["arquivo"] for c in cenas if c["tipo"] == "foto"})
tA = sum(o["dur_est"] for o in out if o["estilo"] == "A"); tB = sum(o["dur_est"] for o in out if o["estilo"] == "B"); tR = sum(o["dur_est"] for o in out if o["estilo"] == "arquivo")
print(f"duração estimada {mmss(t)}; A {tA:.0f} s, B {tB:.0f} s, arquivo {tR:.0f} s; {len(usadas)} fotos distintas: {', '.join(usadas)}")
