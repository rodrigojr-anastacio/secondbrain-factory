# Storyboard do 007 (vendavais no Paraná de 20/11/2026: por que o temporal entra pelo oeste): plano por bloco
# -> shared/storyboard.json, shared/cenas.json e STORYBOARD.md (tabela). Etapa 1 (22/11/2026). Tempos ESTIMADOS (hook 3,3 pal/s,
# corpo 2,9 pal/s); a etapa 2 amarra cada evento à palavra no Whisper (build_cues do 006) e grava cues.json.
# Nada aqui é imagem gerada por IA: mapa 3D do Paraná (relevo SRTM/Terrain Tiles z9–z10 + cor natural; motor do 006, Longo6/Cenas6),
# estações do Simepar como pinos (dados/rajadas-2026-11-20.json), satélite GOES-19 real (NOAA; NetCDF ABI-L2-CMIPF canal 13 reprojetado),
# chuva NASA IMERG (dados/nasa/), fotos CC0 (AEN, DPU) e Sentinel-2 (Copernicus). Créditos SÓ na descrição; na tela só LUGAR · DATA.
# Estilos (estilo_v2 do 005/006): A = satélite (relevo real + cor natural), B = relevo editorial (navy) para dado/rótulo, G = satélite
# meteorológico (GOES/IMERG sobre o relevo), doc = papel claro.
# ASSINATURA: A LINHA DAS RAJADAS — pinos que acendem na hora do pico e se ligam numa reta coral SW→NE (b05–b09); volta no b13, b27, b33 e b42.
# Segunda assinatura: A ESCADA — o Paraná visto de lado (perfil SRTM oeste→leste em bloco 3D, mesmo bloco da Thumb A), b20–b26.
# Sensibilidade: nenhuma foto de pessoa ferida, resgate ou TV; Rio Bonito por rastro (Sentinel-2, laudo) e por um telhado sem pessoas;
# vítimas não são citadas; legenda da foto do telhado neutra ("RIO BONITO DO IGUAÇU · 18 NOV 2025", ressalva do crivo r3).
import json
from pathlib import Path
A = Path(__file__).parent; R = A.parent
bl = {b["id"]: b for b in json.load(open(A / "blocos.json"))}

GO = "dl/goes19/"            # prévia STAR (jpg); a etapa 2 troca pelo NetCDF reprojetado (mesmos horários)
NA = "dados/nasa/"
FO = "dl/fotos/"
TELHADO = FO + "dpu/rb-telhado-54944696133-orig.jpg"         # DPU, CC0, 18/11/2025
RB_AER = FO + "commons-rb-03-orig.jpg"                        # Ari Dias/AEN, CC0, 08/11/2025 (só plano largo, sem zoom em entulho)
S2 = FO + "commons-Sentinel-2_Rio_Bonito_scar_labelled_no_m"  # Copernicus/ESA via Commons (atribuição); recortar o rótulo embutido
ARAUC = FO + "aen-copel-2026-11-07-78655.jpg"                 # Copel/AEN, CC0, 07/11/2026
POSTE = FO + "aen-copel-2026-11-07-78659.jpg"                 # Copel/AEN, CC0, 07/11/2026
MGA = FO + "aen-maringa-2026-11-04-defesacivil.jpg"           # Defesa Civil/AEN, 04/11/2026 (CC0 da galeria; conferir legenda)

# id: (estilo, transição, plano principal, camadas/overlays, mídias [(arquivo, palavra-gatilho, formato)])
S = {
# ---------------- HOOK ----------------
"b01": ("A", "", "Abre baixo sobre o rio Iguaçu na fronteira (Argentina à esquerda, Brasil à direita), fim de tarde nublado; a câmera desliza até Capanema. Um pino coral acende na palavra 'rajada' e pulsa.",
        ["cartão CAPANEMA (PR) · 20 NOV 2026 · 13H45", "na palavra 'oitenta': ficha 81,7 KM/H sobe do pino"], []),
"b02": ("A", "voo alto em diagonal (whoosh longo)", "A câmera sobe e voa ~420 km para nordeste por cima do estado até Cornélio Procópio; um segundo pino acende lá. No meio do voo, dois pinos menores piscam: FOZ e MANOEL RIBAS (ícone de redemoinho simples, sem foto).",
        ["régua 423 KM · 6H30 entre os dois pinos", "ficha 98,3 KM/H em Cornélio Procópio", "pinos TORNADO F1 · FOZ DO IGUAÇU / TORNADO F1 · MANOEL RIBAS"], []),
"b03": ("A", "dissolve para outra luz (dia claro)", "Mesmo enquadramento do estado, mas outro dia: uma linha fina de 2025 aparece no centro-sul (Quedas do Iguaçu → Cantagalo), em amarelo pálido, e a câmera faz um leve zoom sobre Rio Bonito do Iguaçu.",
        ["cartão RIO BONITO DO IGUAÇU · 7 NOV 2025", "linha tracejada 2025"], []),
"b04": ("B", "", "Câmera recua até o Paraná inteiro em relevo editorial; uma seta grande entra pela borda oeste (a mesma da Thumb A).",
        ["pergunta em tipografia: POR QUE O TEMPORAL ENTRA PELO OESTE DO PARANÁ?", "subtítulo: DE NOVO PELO MESMO LADO?"], []),
# ---------------- 1. O RASTRO DE UMA TARDE ----------------
"b05": ("B", "", "ASSINATURA: o mapa editorial do PR com 16 estações do Simepar como pontos apagados; um relógio no canto (13:00 → 21:00) começa a correr.",
        ["aba 1 · O RASTRO DE UMA TARDE", "relógio 13:00", "pontos apagados = estações"], []),
"b06": ("B", "", "Os pontos acendem um a um na hora do pico, em sincronia com a fala (Capanema → Santa Helena → Cascavel → Campo Mourão → Maringá → Londrina → Cornélio Procópio) e os demais da fila no intervalo; cada um deixa um número pequeno em km/h.",
        ["relógio corre até 20:15", "rótulos com hora e km/h (dados/rajadas-2026-11-20.json)", "na palavra 'linha': a reta coral liga os pontos de SW para NE"], []),
"b07": ("B", "", "Dois pontos acendem fora da ordem e fora da reta, em cinza: PARANAGUÁ (litoral) e CAMBARÁ (Norte Pioneiro); a câmera passa por eles e volta para a reta.",
        ["rótulos PARANAGUÁ 13H15 · CAMBARÁ 14H (cinza)", "etiqueta OUTRAS CÉLULAS", "a reta coral volta a brilhar: LINHA PRINCIPAL"], []),
"b08": ("B", "", "Gráfico limpo sobre o mapa escurecido: eixo horizontal = distância ao longo da reta (0 → 430 km), eixo vertical = hora (13h → 21h); os 14 pontos caem quase sobre uma linha reta (dado nosso, N1).",
        ["gráfico HORA × DISTÂNCIA (14 estações)", "número ~430 KM · ~70 KM/H", "ícone de carro na estrada ao lado do 70 KM/H"], []),
"b09": ("A", "transição do gráfico de volta ao 3D (sem corte)", "A faixa de tempestade aparece como uma banda translúcida que desliza sobre o relevo ao longo da reta, de Capanema a Cornélio Procópio, em ~5 s (acelerado).",
        ["etiqueta 6H30 · 13H45 → 20H15"], []),
"b10": ("A", "zoom para Foz (whoosh)", "A banda passa por Foz do Iguaçu; zoom até a cidade (satélite, cor natural); pino na Vila Yolanda. Depois a câmera corre para Manoel Ribas (zona rural, campos).",
        ["pino VILA YOLANDA · FOZ DO IGUAÇU · ~15H", "ficha TORNADO F1 · 117–180 KM/H (ESTIMADO)", "pino MANOEL RIBAS · ~18H · F1"], []),
"b11": ("B", "", "Contador sobe de 0 a 353.849 sobre o mapa do estado que escurece (lâmpadas se apagando por região); depois, 9 municípios se destacam em coral.",
        ["contador 353.849 IMÓVEIS SEM ENERGIA · 20H02", "ficha 9 MUNICÍPIOS · 249 IMÓVEIS DANIFICADOS", "Foz destacada: QUASE METADE"], []),
"b12": ("A", "", "Foto CC0 de árvore caída em temporal deste novembro (Copel/AEN, 07/11) como respiro, enquanto os números de Foz aparecem; depois volta ao mapa com as regiões da Copel e o Oeste em destaque.",
        ["ficha FOZ: ~50 ÁRVORES · LONAS PARA ~200 FAMÍLIAS", "ficha OESTE: 26,8 MIL SEM LUZ NA MANHÃ SEGUINTE"],
        [(ARAUC, "árvores", "quadro grande 1240 px, Ken Burns lento 2,5 s; legenda PARANÁ · 7 NOV 2026 (não é de Foz: legenda honesta)")]),
"b13": ("B", "", "A reta coral de novo, agora pintada em degradê: laranja (tarde) no oeste, azul-escuro (noite) no norte.",
        ["rótulos TARDE / NOITE ao longo da reta", "ícone de relógio com interrogação (loop: pago no b27)"], []),
# ---------------- 2. DE ONDE ELE VEM ----------------
"b14": ("G", "subida longa de câmera (whoosh)", "A câmera sobe e gira para oeste até mostrar Paraguai, Misiones e o PR; uma baixa pressão desenhada como um 'B' discreto sobre o Paraguai.",
        ["aba 2 · DE ONDE ELE VEM", "rótulo BAIXA PRESSÃO · PARAGUAI (previsão do Simepar, 19/11)", "setas suaves OESTE · SUDOESTE"], []),
"b15": ("G", "", "Sequência real do GOES-19 (canal 13, infravermelho, 9h → 20h, a cada 20 min) sobreposta ao relevo, em ~6 s: o aglomerado nasce a oeste e se estica sobre o estado; relógio no canto.",
        ["relógio 9H → 20H (hora de Brasília)", "rótulo GOES-19 · 20 NOV 2026"],
        [(GO + "b13/20263241200_GOES19-ABI-ssa-13-1800x1080.jpg", "nove", "prévia; etapa 2: NetCDF reprojetado, 34 quadros 12–23 UTC"), (GO + "b13/20263242300-3600.jpg", "oito da noite", "quadro final congelado 1,5 s")]),
"b16": ("A", "recuo continental (sem corte)", "A câmera recua até o continente inteiro: Andes à esquerda, a região entre Paraguai, norte da Argentina e Sul do Brasil se acende como uma mancha quente suave (sem números), a leste dos Andes.",
        ["rótulo A LESTE DOS ANDES", "rótulo SATÉLITE TRMM · NASA · 7 ANOS DE DADOS"], []),
"b17": ("B", "", "Duas silhuetas simples de continente lado a lado (América do Norte e América do Sul) com a faixa de latitudes médias destacada; ícones de 'complexo de tempestade' iguais nas duas.",
        ["etiqueta COMPLEXOS DE TEMPESTADE · LATITUDES MÉDIAS", "sinal = entre os dois lados"], []),
"b18": ("A", "", "Plano rápido de recapitulação: três setas finas e esmaecidas (Amazônia → sul; Andes como parede; ar frio do sul) sobre o continente, e um selo do nosso vídeo 001.",
        ["selo VÍDEO NO CANAL: TORNADOS DO SUL", "seta grande final aponta: A OESTE DO PARANÁ"], []),
"b19": ("B", "", "Mapa do Sul com a faixa de maior frequência de tornados do levantamento da UFSM (norte do RS, oeste de SC, sudoeste do PR) em coral translúcido; a borda oeste do PR acende.",
        ["etiqueta UFSM · 310 TORNADOS REGISTRADOS NO SUL", "rótulo O LADO DA PORTA"], []),
# ---------------- 3. A ESCADA DO PARANÁ ----------------
"b20": ("A", "giro de câmera para vista lateral (whoosh longo)", "SEGUNDA ASSINATURA: o Paraná em bloco 3D visto de lado, de leste (mar, à direita) para oeste (rio Paraná, à esquerda), exagero vertical marcado 'ilustrativo' — o mesmo bloco da Thumb A.",
        ["aba 3 · A ESCADA DO PARANÁ", "selo ILUSTRATIVO · ALTURA EXAGERADA"], []),
"b21": ("B", "", "Régua de altitude vai marcando cada degrau na fala: litoral 0 m → Pico Paraná 1.877 m → Curitiba ~930 m → Guarapuava > 1.000 m (perfil SRTM N4).",
        ["rótulos com altitude: LITORAL 0 · PICO PARANÁ 1.877 M · CURITIBA ~930 M · GUARAPUAVA > 1.000 M"], []),
"b22": ("B", "", "Continuação do perfil para oeste: os degraus descem até o rio Paraná; Cascavel e Foz marcados.",
        ["rótulos CASCAVEL ~780 M · FOZ DO IGUAÇU ~160 M", "seta da tempestade chegando pela esquerda, na ponta baixa"], []),
"b23": ("B", "", "Termômetro simples ao lado do perfil: a cor do ar fica mais quente à medida que o perfil desce para oeste.",
        ["etiqueta ~0,6 °C A CADA 100 M (MÉDIA)", "degradê azul (alto) → laranja (baixo)"], []),
"b24": ("A", "", "Mapa do PR com o norte em tom quente; ficha da previsão.",
        ["ficha PREVISÃO 19/11: > 30 °C NO NORTE", "ficha CALOR + UMIDADE = ALIMENTO DA TEMPESTADE"], []),
"b25": ("B", "", "Dois termômetros lado a lado: CURITIBA ~930 M e FOZ ~160 M, com a diferença calculada.",
        ["DIFERENÇA ~770 M → ~4 A 5 °C MAIS QUENTE EM FOZ (SÓ PELA ALTITUDE)"], []),
"b26": ("A", "", "Volta ao bloco 3D: a seta da tempestade encosta na ponta baixa do oeste; um ícone de ímã riscado (a ladeira não puxa).",
        ["rótulo A LADEIRA NÃO PUXA", "rótulo QUEM ELA ENCONTRA PRIMEIRO: A PONTA BAIXA E QUENTE"], []),
"b27": ("B", "", "A reta coral com o relógio (paga o loop do b13): um ponto anda pela reta a 70 km/h; quando chega ao norte, o céu do mapa escurece (noite).",
        ["relógio 13H45 → 19H30 (LONDRINA) → 20H15 (CORNÉLIO PROCÓPIO)", "ficha 70 KM/H"], []),
"b28": ("A", "", "Zoom em Cornélio Procópio, à noite (relevo escurecido, luzes da cidade em pontos); a ficha 98,3 sobe.",
        ["ficha 98,3 KM/H · 20H15 · O MAIOR DO DIA", "rótulo QUASE NA SAÍDA"], []),
# ---------------- 4. O MESMO LADO ----------------
"b29": ("A", "dissolve de dia (troca de data)", "O mesmo mapa, dia claro; o cartão de data troca de 2026 para 2025.",
        ["aba 4 · O MESMO LADO", "cartão 7 NOV 2025"], []),
"b30": ("A", "", "A linha da supercélula de 2025 é desenhada sobre o relevo; depois o rastro do tornado (75 km) se pinta de Quedas do Iguaçu a Cantagalo, de oeste para leste; a imagem real do Sentinel-2 da cicatriz entra por 2 s.",
        ["ficha SUPERCÉLULA ~270 KM · ~80 KM/H (LAUDO SIMEPAR)", "rótulos QUEDAS DO IGUAÇU → CANTAGALO · 75 KM"],
        [(S2, "rastro", "quadro grande 2 s, recortado sem o rótulo embutido; legenda RIO BONITO DO IGUAÇU · SENTINEL-2 · NOV 2025")]),
"b31": ("A", "", "Zoom em Rio Bonito do Iguaçu: largura do rastro como uma régua; foto aérea CC0 em plano bem largo (cidade inteira, sem zoom em entulho, sem pessoas) por 2 s.",
        ["régua ATÉ ~3,25 KM DE LARGURA", "ficha F4 · UM DOS MAIORES DO PR EM 30 ANOS (SIMEPAR)"],
        [(RB_AER, "Rio Bonito", "quadro médio 2 s, plano largo; legenda RIO BONITO DO IGUAÇU · 8 NOV 2025")]),
"b32": ("A", "", "A linha da mesma supercélula continua para leste e um segundo rastro aparece em Candói/Entre Rios (Guarapuava).",
        ["rótulos CANDÓI · ENTRE RIOS (GUARAPUAVA) · 44 KM", "seta UMA DIREÇÃO SÓ"], []),
"b33": ("B", "", "ASSINATURA de volta: a reta coral de 2026 e a linha amarela de 2025 lado a lado no mesmo mapa; as duas setas apontam para o mesmo lado.",
        ["rótulos 2025 · 2026", "fichas 80 KM/H · 70 KM/H", "rótulo A MESMA PORTA: O OESTE"], []),
"b34": ("B", "", "A borda oeste/sudoeste do PR acende como uma 'porta' (faixa coral), virada para o Paraguai/Argentina.",
        ["rótulo MESMO LADO ≠ MESMA CIDADE", "rótulo PORTA DE ENTRADA: OESTE E SUDOESTE"],
        [(TELHADO, "lado", "respiro 2 s, quadro médio; legenda RIO BONITO DO IGUAÇU · 18 NOV 2025 (neutra, ressalva do crivo r3)")]),
"b35": ("A", "", "Calendário de novembro de 2026 no canto; dia 2 acende com Maringá (pino + rastro de 15 km), dia 7 com o contador 493 mil.",
        ["calendário NOV 2026: 2 · 7 · 20", "pino MARINGÁ · F2 · ~15 KM", "contador 493 MIL SEM LUZ · MAIOR DO ANO"],
        [(MGA, "Maringá", "quadro médio 2 s; legenda MARINGÁ · NOV 2026 (conferir legenda/crédito da AEN)")]),
# ---------------- 5. POR QUE TANTO AGORA ----------------
"b36": ("B", "", "Pergunta em tipografia sobre o mapa do PR.",
        ["aba 5 · POR QUE TANTO AGORA", "pergunta POR QUE TANTA COISA NUM MÊS SÓ?"], []),
"b37": ("G", "", "Camada real NASA IMERG de 1–20/11 sobre o relevo do PR (fade-in com a câmera em movimento); depois a camada de anomalia.",
        ["ficha ~175 MM (MÉDIA NO PR) × ~108 NORMAIS", "ficha MAIS DE 60% ACIMA", "rótulo 1 – 20 NOV 2026"],
        [(NA + "pr-nov-1a20-camada.png", "caíram", "camada sobre o terreno"), (NA + "pr-nov-1a20-anom-anomalia-camada.png", "normal", "troca de camada")]),
"b38": ("B", "", "Mapa das estações do Simepar com pontos que ficam laranja acima de 30 °C (33 deles); Cerro Azul destacado.",
        ["ficha 12 NOV: 33 ESTAÇÕES > 30 °C", "pino CERRO AZUL · 35,1 °C"], []),
"b39": ("B", "", "Pacífico equatorial pequeno no canto com a língua quente do El Niño (como no 002), e uma seta discreta até o Sul; a porta oeste do PR continua acesa.",
        ["ficha EL NIÑO MUITO FORTE (SIMEPAR)", "rótulo AUMENTA AS CHANCES · NÃO FABRICA CADA TEMPESTADE"], []),
"b40": ("B", "", "Barras simples por estação do ano (sem números inventados: só qual é a maior), com o inverno em destaque.",
        ["etiqueta UFSM · MÁXIMO DE TORNADOS NO SUL: INVERNO", "rótulo NOVEMBRO 2026: CALOR + CHUVA DE SOBRA"], []),
# ---------------- A RESPOSTA ----------------
"b41": ("A", "recuo para o Paraná inteiro (sem corte)", "O Paraná em relevo, vista da Thumb A, com a seta entrando pelo oeste.",
        ["aba A RESPOSTA", "pergunta POR QUE PELO OESTE?"], []),
"b42": ("A", "", "As três camadas acendem uma a uma: (1) o berçário a oeste (mancha quente do b16), (2) a reta sudoeste → nordeste com 70–80 km/h, (3) a ponta baixa e quente (degradê do b23).",
        ["fichas 1 · BERÇÁRIO A OESTE · 2 · ANDA DE SW PARA NE · 3 · PONTA BAIXA E QUENTE"], []),
"b43": ("B", "", "As duas linhas (2026 coral, 2025 amarela) lado a lado, fixas; texto final.",
        ["rótulos CAPANEMA → CORNÉLIO PROCÓPIO (2026) · QUEDAS DO IGUAÇU → CANTAGALO (2025)", "frase UM ANO DE DISTÂNCIA, A MESMA PORTA"], []),
"b44": ("B", "", "Card de serviço (paleta do canal), celular simples com um alerta.",
        ["card ALERTAS DA DEFESA CIVIL: SMS COM O SEU CEP PARA 40199", "etiqueta O AVISO SAIU ANTES (SIMEPAR)"], []),
"b45": ("A", "", "Foto CC0 de poste/árvore caídos (Copel/AEN, 07/11) como fundo esmaecido do conselho.",
        ["card LONGE DE ÁRVORES, POSTES E PLACAS"],
        [(POSTE, "postes", "fundo esmaecido 3 s; legenda PARANÁ · 7 NOV 2026")]),
"b46": ("B", "", "Encerramento: miniatura do vídeo 001 (tornados do Sul), logo do canal, mapa do PR com o oeste e o norte destacados ('manda para quem mora aí').",
        ["card do vídeo 001", "logo EM RELEVO"], []),
}

def main():
    ids = list(bl)
    falta = [i for i in ids if i not in S]; sobra = [i for i in S if i not in bl]
    assert not falta and not sobra, (falta, sobra)
    t = 0.4; out = []; cenas = []
    for i in ids:
        x = bl[i]; w = len(x["fala"].split()); r = 3.3 if x["marcha"] == 1 else 2.9; d = w / r + 0.6
        est, tr, plano, camadas, midias = S[i]
        out.append({"id": i, "cap": x["cap"], "t_est": round(t, 1), "dur_est": round(d, 1), "estilo": est, "transicao": tr,
                    "plano": plano, "camadas": camadas, "midias": [{"arquivo": a, "gatilho": g, "formato": f} for a, g, f in midias]})
        cenas.append({"bloco": i, "tipo": "mapa" if est in "ABG" else est, "estilo": est, "descricao": plano})
        for a, g, f in midias:
            cenas.append({"bloco": i, "tipo": "foto" if a.startswith("dl/fotos") else "dado", "arquivo": a, "gatilho": g, "formato": f})
        t += d
    json.dump({"_doc": "Etapa 1: plano por bloco (tempos estimados). A etapa 2 converte em cues.json amarrado ao Whisper.",
               "duracao_est_s": round(t, 1), "blocos": out}, open(A / "storyboard.json", "w"), ensure_ascii=False, indent=1)
    json.dump({"_doc": "Lista plana de planos/mídias (nenhuma imagem de IA; satélite NOAA/NASA/Copernicus, fotos CC0 AEN/DPU).", "cenas": cenas},
              open(A / "cenas.json", "w"), ensure_ascii=False, indent=1)
    arquivos = sorted({m["arquivo"] for b in out for m in b["midias"]})
    est = {k: sum(b["dur_est"] for b in out if b["estilo"] == k) for k in "ABG"} | {"doc": sum(b["dur_est"] for b in out if b["estilo"] == "doc")}
    eventos = sum(1 + len(b["camadas"]) + len(b["midias"]) for b in out)
    L = [f"# Storyboard: Em Relevo 007 (vendavais no Paraná de 20/11/2026: por que o temporal entra pelo oeste)", "",
         f"Etapa 1 (22/11/2026). Fonte: `shared/storyboard.py` → `shared/storyboard.json`, `shared/cenas.json` (regenere com `python3 shared/storyboard.py`). "
         f"Duração estimada **~{int(t//60)}:{int(t%60):02d}**; {len(out)} blocos; ~{eventos} eventos visuais (~{eventos/(t/60):.0f}/min, alvo 2–4 s por evento); "
         f"tempo por estilo: A {est['A']:.0f} s · B {est['B']:.0f} s · G {est['G']:.0f} s. **Zero imagem de IA**; {len(arquivos)} mídias reais distintas; custo de imagem US$ 0.", "",
         "## Linguagem visual (a do 005/006, visual v2)",
         "- **A = satélite** (relevo SRTM do Paraná via Terrain Tiles + cor natural) para lugar e impacto; **B = relevo editorial** (navy) para dado, reta e rótulo; **G = satélite meteorológico** (GOES-19 infravermelho e NASA IMERG sobre o relevo).",
         "- Câmera sempre em movimento; cada evento amarrado à palavra falada (gatilho) na etapa 2. Legenda só LUGAR · DATA; créditos só na descrição. Exagero vertical sempre com 'ILUSTRATIVO'.", "",
         "## Assinaturas e fio condutor",
         "1. **A linha das rajadas** (b05–b09, b13, b27, b33, b42–b43): 16 pontos do Simepar que acendem na hora do pico; 14 se ligam numa reta coral sudoeste → nordeste; Paranaguá e Cambará ficam em cinza (outras células). Gráfico hora × distância no b08 (dado nosso, r² 0,98).",
         "2. **A escada do Paraná** (b04, b20–b26, b41 e a Thumb A): o estado em bloco 3D visto de lado, perfil SRTM oeste → leste com régua de altitude; a seta da tempestade encosta na ponta baixa.",
         "3. **Duas linhas lado a lado** (b03, b30–b33, b43): a reta de 2026 (coral) e o rastro de Rio Bonito 2025 (amarelo, do laudo).", "",
         "## Peças novas (prioridade; simplifique de baixo para cima se faltar tempo)",
         "1. **Pinos que acendem + reta + relógio** (dados/rajadas-2026-11-20.json; refazer a regressão N1 com as coordenadas finais).",
         "2. **GOES-19 sobre o relevo:** baixar ABI-L2-CMIPF canal 13 de 20/11 12–23 UTC do bucket público `s3://noaa-goes19`, reprojetar para lon/lat no bbox do PR (+ Paraguai/Misiones) e usar como camada (paleta infravermelho realçado). Prévia jpg do STAR em `dl/goes19/`.",
         "3. **Bloco 3D do Paraná de lado** com perfil SRTM (N4) e régua; mesmo still serve à Thumb A.",
         "4. **Camadas IMERG** (dados/nasa/pr-nov-1a20*.png) — já geradas.",
         "5. **Rastro de Rio Bonito 2025** desenhado a partir do laudo (municípios em ordem) + Sentinel-2 (Commons, atribuição Copernicus).",
         "6. Gráfico hora × distância (b08), termômetros (b23, b25), calendário (b35), barras por estação (b40), cards: componentes existentes.", "",
         "## Mídias reais", "| arquivo | blocos | licença/crédito (descrição) |", "|---|---|---|"]
    lic = {GO: "NOAA/NESDIS (GOES-19), domínio público", NA: "NASA GPM IMERG (GES DISC), domínio público", TELHADO: "DPU (Defensoria Pública da União), CC0",
           RB_AER: "Ari Dias/AEN, CC0", S2: "Contains modified Copernicus Sentinel data 2025 (via Wikimedia Commons)", ARAUC: "Copel/AEN, CC0",
           POSTE: "Copel/AEN, CC0", MGA: "Defesa Civil/AEN (galeria CC0; conferir legenda)"}
    for a in arquivos:
        bs = ", ".join(b["id"] for b in out if any(m["arquivo"] == a for m in b["midias"]))
        cred = next((v for k, v in lic.items() if a.startswith(k)), "")
        L.append(f"| `{a}` | {bs} | {cred} |")
    L += ["", "## Plano por bloco", "| bloco | t est. | estilo | plano | camadas |", "|---|---|---|---|---|"]
    for b in out:
        L.append(f'| {b["id"]} | {int(b["t_est"]//60)}:{int(b["t_est"]%60):02d} | {b["estilo"]} | {b["plano"]} | {" · ".join(b["camadas"])} |')
    L += ["", "## Sensibilidade",
          "Sem foto de pessoa, resgate, ferido ou TV; Rio Bonito por rastro, laudo e plano largo/telhado sem pessoas; vítimas não são citadas; fotos de 07/11 com legenda do dia certo (não fingem ser de 20/11); foto do telhado com legenda neutra."]
    (R / "STORYBOARD.md").write_text("\n".join(L) + "\n")
    print(len(out), "blocos;", f"{t:.0f} s;", eventos, "eventos;", len(arquivos), "mídias")

if __name__ == "__main__":
    main()
