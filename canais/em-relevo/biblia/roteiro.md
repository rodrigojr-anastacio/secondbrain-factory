# Bíblia de roteiro: Em Relevo (clima e geografia do Brasil em mapa 3D) — 16/11/2026

> **Origem:** movido em 16/11/2026 de `pesquisa/canal-clima-2026-11/biblia-roteiro.md` (versão de 16/11/2026, com as seções Forma × Conteúdo do job de ângulo), na mudança do Em Relevo para `canais/em-relevo/`. Conteúdo igual; só os caminhos foram ajustados para a estrutura nova (`longo-NN` → `videos/NNN-slug/`). Fonte única daqui em diante.

Bíblia de roteiro do canal (ao lado de [`titulo.md`](titulo.md), [`thumb.md`](thumb.md), [`visual.md`](visual.md) e [`voz.md`](voz.md); índice em [`README.md`](README.md)). Prevalece sobre `conhecimento/`. Toda entrada leva data e fonte; sem dado = **Hipótese**.

## Forma (modelada) × Conteúdo (nosso)
Diretriz do Rodrigo (16/11/2026): *"identificar um tema que tem demanda, mas abordá-lo de outro ângulo, para fugir da manada; mas ter um padrão claro de roteiro que funciona em canais de sucesso."* Motivo: no historia-ptbr, remodelar a transcrição da referência fez o 005-brasil sair quase igual ao History in Minutes (detector 47/100). Auditoria de 16/11: **005 (enchente de Porto Alegre, antigo longo-05) = 11/100** contra 5 vídeos do tema (Fatos Desconhecidos, Domingo Espetacular, BBC News Brasil, Brasil Escola, Terra em Choque): ângulo próprio (o caminho da água no mapa) (`pesquisa/roteiro-angulo-2026-11/AUDITORIA.md`).

### Forma (modelada): o que copiamos dos canais de sucesso, de propósito
- **Hook com lugar + data + número** no 1º segundo, depois a pergunta ("Dois tornados em 18 minutos." do @relevo.ia; "Era 11 de março de 2011, duas e quarenta e seis da tarde…" do Um Documentário; "At 8.37 in the morning…" do The Last Day). Fonte: `pesquisa/canal-clima-2026-11/RELATORIO.md` (Arquivos, hooks literais) e `pesquisa/estilo-mapa-relevo-3d/PADRAO.md` (Ritmo e estrutura).
- **Estrutura** (003/004/005, antigos longo-03/04/05): hook com lugar/data/número → a pergunta do título dita até ~0:40 → "a resposta está no mapa" → 4–6 capítulos numerados (a aba de capítulo é uma pergunta ou uma camada da resposta) → A RESPOSTA que junta as camadas → fecho útil e compartilhável (o que fazer / mande para quem mora lá).
- **Câmera contínua no mapa** em vez de cortes; "olhe de cima", "suba a câmera" como transições faladas (`canais/em-relevo/videos/005-enchente-porto-alegre-2024/ROTEIRO.md`).
- Números com fonte primária, sem alarmismo; probabilidade dita como probabilidade.

### Conteúdo (nosso): o que nunca vem da referência
- **Ângulo próprio** (`ANGULO.md`, skill `pesquisa-referencia` passo 7): transcreva a manada do tema (os 3–5 vídeos de mais views em pt, inclusive TV/jornal no YouTube e canais de curiosidade; `tools/manada.py`) e escolha uma **explicação geográfica** que eles não dão (o caminho da água, o relevo, a série histórica, a comparação de mapas). Notícia e depoimento são a manada; o mapa que explica é o nosso.
- **Proibido:** o hook de um vídeo da manada; a sequência de cenas de uma reportagem; traduzir/reescrever transcrição; usar reportagem de TV como fonte de número (fonte = INMET, ANA, CEMADEN, Defesa Civil, prefeituras, artigos, WWA, NOAA/USGS).
- **Cota: ≥ 40% dos dados/cenas principais** fora de todas as transcrições da manada (listados em `pesquisa/FATOS.md` / `SOURCES` da pasta do vídeo). **Hipótese** (16/11/2026).
- **Portão:** `tools/similaridade_roteiro.py <pasta do vídeo canais/em-relevo/videos/NNN-slug>` (lê `shared/blocos.json`) < 30 e `CRIVO-ANGULO.md` APROVADO (`skills/roteiro/CRIVO-ANGULO.md`) antes do storyboard/voz.

## Checklist (acrescenta ao do brief do lote)
- [ ] `ANGULO.md` com a manada transcrita e o ângulo escolhido; hook não é o de nenhum vídeo da manada.
- [ ] `SIMILARIDADE.md` < 30; `CRIVO-ANGULO.md` APROVADO; ≥ 40% dos dados/cenas fora da manada.

## Lições do 006 (crivo de ângulo, 17/11/2026; `../videos/006-caraguatatuba-1967/roteiro-crivo/`)
- **Vídeo longo da manada já explica a geografia qualitativamente** (Histórias da Tragédia `ToXuPrJ8814`, 66 min: chuva orográfica sem número, "capa de solo fina", côncavas > 30°, "a serra que fabrica a chuva", 2023 no epílogo). O crivo r1 reprovou o roteiro por repetir essas **imagens/metáforas e a tese de fecho**, mesmo com detector 10/100. O que passou (r2, detector 2–3/100): **a mesma explicação, mas medida** — perfis SRTM próprios lado a lado, pluviômetro × satélite IMERG, cicatrizes contadas, coesão de laboratório, carta científica, Landsat. Regra: antes de escrever, leia a transcrição longa inteira e liste as **metáforas** dela (não só os fatos) para não usar.
- Hook em 2023 com contraste de pluviômetros (683 × 234 mm no mesmo dia) + dois perfis lado a lado = cena que nenhum vídeo da manada usa. **Hipótese** (sem retenção ainda).

## Lições do 007 (vendavais no Paraná, 22/11/2026; `../videos/007-vendavais-parana-2026/`)
- **Tema quente sobre um assunto que o próprio canal já explicou** (o 001 cobriu o corredor de tornados): ponha o roteiro do nosso vídeo como referência no detector (`ref/nosso-001-*.txt`) e reduza a explicação repetida a 1 frase + convite ao vídeo publicado. O 007 deu 14/100 contra o 001 e 1–3 contra a manada; crivo de ângulo aprovou na r1.
- **Dado próprio a partir de dado oficial bruto** é o que separa o vídeo da TV: as horas de pico de 16 estações do Simepar viraram uma reta (r² 0,98) e uma velocidade (~70 km/h). Diga em voz alta as exceções (estações fora da reta) para a tese não virar inverdade.
- Metáforas da manada a evitar neste tema (Além do Mapa `x_xE2HyxQE0`): "muro dos Andes", "rios voadores", "motor"/"combustível para o motor", "o endereço que se repete", "a estrada não muda de lugar". **Hipótese** (sem retenção ainda).
