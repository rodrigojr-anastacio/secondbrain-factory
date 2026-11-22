# Thumb (em-relevo)

Base: identidade de 09/11/2026 (`pesquisa/canal-clima-2026-11/identidade/LEIA.md`), bíblia de título/thumb antiga (`pesquisa/canal-clima-2026-11/biblia-titulo.md`), reembalagem de 14/11/2026 (`pesquisa/reembalagem-2026-11-14/PROPOSTAS.md` seção Em Relevo, `padroes.md`, `thumbs/emrelevo.py`), crivo do 005 (`../videos/005-enchente-porto-alegre-2024/EMBALAGEM.md` e `CRIVO.md`, 15/11/2026), teste a seco das 3 thumbs (`pesquisa/teste-embalagem-3thumbs-2026-11-16/`, 16/11/2026) e o CTR da seca 1877 (Rodrigo, 16/11/2026). CTR medido do canal ainda é pouco: o que não tiver número nosso é **Hipótese**.

## O que o CTR já mostrou (único dado nosso)
| Vídeo | Thumb | CTR | Fonte |
|---|---|---|---|
| 001 tornados do Sul | bege/papel + polaroid pequena | 2,7% (184 impr.) | `PROPOSTAS.md` (14/11/2026) |
| 002 El Niño 2026 | bege/papel + polaroid pequena | 1,7% (179 impr.) | `PROPOSTAS.md` (14/11/2026) |
| 003 seca de 1877 | as 3 (A/B/C) mapa escuro + número/ano ("500 MIL", "1877", "1877 = 2026?") | **0,8% nas primeiras horas** | Rodrigo, 16/11/2026 |

- **Aprendizado de 16/11/2026 (Rodrigo):** as 3 thumbs da seca 1877 (`../videos/003-seca-1877/entrega/thumb-A/B/C.jpg`) eram a mesma família (mapa escuro + número/ano) e tiveram CTR 0,8%. **Mapa escuro dominando o quadro some na lateral dos sugeridos** (thumb pequena ao lado de outras escuras). E o "Testar e comparar" não ensinou nada, porque as 3 eram variações do mesmo conceito.
- **Regra (Rodrigo, 16/11/2026): no máximo 1 das 3 thumbs com mapa escuro dominante.** As outras 2 saem de outro padrão visual: foto real grande, contraste claro, objeto ou rosto real (ver "Padrões" abaixo).
- O bege/polaroid antigo também sumia: "as nossas eram as únicas claras da grade e somem a 320×180" (`biblia-titulo.md`, reembalagem 14/11/2026). Ou seja, claro não basta: o que falhou nos dois casos foi **herói pequeno ou difuso**. **Hipótese:** o que destaca é um herói único e grande com contraste próprio (foto real nítida, forma brilhante, rosto), não a cor do fundo.
- Grade do próprio canal em 16/11/2026: 9 de 11 thumbs já eram "mapa escuro + número/ano" (`pesquisa/teste-embalagem-3thumbs-2026-11-16/granizo/EMBALAGEM.md`, `vizinhas-em-relevo.jpg`). O crivo reprovou um número gigante por repetir a grade. Número volta em no máximo 1 das 3, e sem mapa escuro.

## Identidade (o que existe hoje)
- **Fontes** (OFL, em `pesquisa/canal-clima-2026-11/identidade/fontes/`): **Anton** (texto da thumb, números), **IBM Plex Mono** Bold/Medium (etiquetas), Playfair Display Italic (manchetes, não usada em thumb). Anton e Plex Mono não têm ✓ ✗ ▶ ⚠: ícone vira SVG (`../videos/001-tornados-sul/RELATORIO.md`, 08/11/2026).
- **Cores do canal** (`identidade/LEIA.md`): coral `#E8505B`, navy `#1F2A44`, papel `#E9DCC3`, branco papel `#FBF8F1`, tinta `#2B2622`.
- **Cores das thumbs de 14–15/11** (`../videos/005-enchente-porto-alegre-2024/remotion/src/Thumb.jsx`): fundo `#101830`/navy, amarelo `#FFD23F` (palavra/número principal), branco `#FBF8F1`, ciano `#3FD8FF` (água/rios), contorno de texto `#0E1426` (~14 px a 1920) + sombra.
- **Texto:** 2–3 palavras, em pergunta ou lacuna ("SÓ 2 °C?", "CULPA DOS ANDES?", "1/3 DO ESTADO?"), sem repetir palavra do título e sem dar a resposta (`biblia-titulo.md`; `conhecimento/thumbnails/README.md`).
- **Sem IA de imagem na thumb** desde o 003: tudo composto em código a partir de stills do nosso mapa 3D, dados reais e fotos com licença, custo US$ 0 (`../videos/003-seca-1877/TITULOS-THUMBS.md`, `../videos/005.../ETAPA2-PRONTA.md`). A IA (nano-banana) só fez logo e capa do canal (`identidade/LEIA.md`, US$ 0,39).

## Como fazer (pipeline usado no 003–005)
1. Conceitos A/B/C saem do `EMBALAGEM.md` aprovado no crivo (skill `embalagem`); não invente conceito na etapa 2 (skill `thumbnail`).
2. Composição em `remotion/src/Thumb.jsx` (composições `ThumbA/B/C` no `Root.jsx`, 1920×1080) sobre still do nosso 3D (`LongoV5`) ou foto/satélite real; `shared/thumbs.sh` renderiza o still (`--gl=swangle`) e reduz para 1280×720 (< 2 MB; os do 001 deram 76–120 KB). Saída em `entrega/thumb-A/B/C.jpg` + `entrega/thumbnail.jpg` (= A).
3. Alternativa sem Remotion: homografia em PIL (`pesquisa/reembalagem-2026-11-14/thumbs/emrelevo.py`: língua de anomalia NOAA OISST, Andes + fita de umidade).
4. **Prévia 320×180 ao lado do mosaico do tema** (`embalagem/mosaico.jpg`) e da grade do próprio canal antes de fechar (crivo 005 r2; `conhecimento/thumbnails/README.md`).
5. Crédito da foto/dado usado na thumb vai **na descrição** (`youtube.txt`), nunca na arte (ver `visual.md`).

## 3 thumbs A/B/C de padrões visuais diferentes (desde 16/11/2026)
Regra da fábrica (Rodrigo, 16/11/2026; `skills/embalagem/SKILL.md` passo 5 e `skills/thumbnail/SKILL.md` passo 4): cada vídeo leva 3 conceitos de **padrões visuais diferentes** (composição, elemento dominante e tipo de texto distintos), pareados a T1/T2/T3, registrados em `youtube.embalagem_variantes` (placar `youtube.padrao_thumb_placar`). Vocabulário: `rosto-emocao`, `objeto-simbolo`, `conflito-xvy`, `numero-estatistica`, `mapa-lugar`, `antes-depois`, `cena-acao`, `documento-evidencia`.
- **Mesmo herói com outro ângulo é a mesma thumb** (satélite da nuvem × foto da nuvem do chão: reprovado; teste granizo 16/11/2026).
- **O acervo tem de existir antes de propor:** baixe e olhe a foto (a "gota CC0" era uma vidraça com dezenas de gotas; teste granizo).
- **Foto genérica com título de caso específico** vende a foto como o caso: reprova (teste granizo).

### Padrões para o Em Relevo (A = controle, B e C = exploração)
| Uso | Padrão | Como no Em Relevo | Evidência | Status |
|---|---|---|---|---|
| **A (controle; o único com mapa escuro)** | `mapa-lugar` | 1 herói só sobre mapa escuro: árvore de rios ciano convergindo (005), Andes + fita de umidade (001 reembalado), língua quente real (002 reembalado). Pergunta de 2–3 palavras | it5Vsv851Rc 14,4× e CMHf4Cqpcrs 12,6× (pergunta sobre mapa escuro com 1 região); xpBOF8FXXHM 16,4× (bloco 3D + seta) (`biblia-titulo.md`, `granizo/EMBALAGEM.md`) | **Hipótese** (aprovado no crivo; o 003 mostra que sozinho não basta) |
| B/C | `cena-acao` | **Foto real grande, em tela cheia**, nítida e com contraste (supercélula, rio cheio, cidade alagada vista de cima), texto curto ou nenhum. Só foto com licença conferida; sem vítima, sem TV | N9U-HFY5XRE "De olho no céu" 151,7× (supercélula real, sem texto); 9PsvJ_Xu-M4 Mati Mederos 17,4× (`granizo/EMBALAGEM.md`, 16/11/2026) | **Hipótese** (melhor evidência de exploração do nicho) |
| B/C | `antes-depois` | Satélite real antes × depois (Landsat/USGS, Sentinel-2/HLS via NASA Worldview), lado a lado ou cortina, em cor natural clara (não navy) | Usado dentro do vídeo no 004 (Landsat 1983) e 005 (Sentinel-2/HLS); listado como eixo viável em `biblia-titulo.md` | **Hipótese sem referência de thumb medida**: a embalagem precisa achar ≥ 2 |
| B/C | `conflito-xvy` | 2 objetos/lugares reais cara a cara, raio ou rachadura no meio, 2 rótulos | GnEXgEaYz1M JeanGrafia 6,2× ("BRASIL RACHADO", com rosto); 8W5B2KiJgyc 1,4× (canal mínimo) | **Hipótese, evidência fraca** (granizo r2 reprovou a execução: fotos não serviam e rótulo repetia o título) |
| B/C | `documento-evidencia` | Imagem de radar/chuva real da NASA (GPM/IMERG) ou jornal/página de época em domínio público, grande e legível | Nenhuma referência medida no nicho ainda; no granizo ficou travado por falta da conta NASA Earthdata (agora resolvido, abaixo) | **Hipótese** |
| B/C | `numero-estatistica` | Número gigante **sem mapa escuro** (sobre foto ou fundo claro) | 9 das 11 do canal já usam número: o crivo reprovou "−90 °C" por repetir a grade | Só se nenhuma vizinha recente usar; nunca com mapa escuro |
| evitar | `objeto-simbolo` | (pedra de granizo 3D, termômetro isolado) | Sem prova no nicho nem no nicho amplo: todos os casos têm rosto (`biblia-titulo.md`, 16/11/2026) | Só com evidência nova |
| evitar | `rosto-emocao` | Canal sem apresentador; rosto só de pessoa viva em foto licenciada, nunca vítima em close | Nenhuma medida | Só com evidência nova |

**NASA Earthdata (16/11/2026):** token disponível em `~/.segredos/nasa/earthdata.env` (variável `EARTHDATA_TOKEN`, header `Authorization: Bearer`; vale até 15/01/2027; app "NASA GESDISC DATA ARCHIVE" autorizado; `AGENTS.md`). Destrava produtos **GPM/IMERG no GES DISC** (chuva acumulada/radar) para `documento-evidencia` e para o vídeo. Nunca leia, imprima nem copie o arquivo; o script lê a variável. Crédito NASA na descrição.
**Ferramenta (16/11/2026):** `tools/nasa_chuva.py` gera a chuva acumulada (e a anomalia) de qualquer período e região desde jun/2000. Para a thumb `documento-evidencia`, use **`--fundo claro`**: papel claro, sem mapa escuro, porque a thumb A já é a do mapa escuro. Componha a partir de `<slug>-camada.png` (sem texto) ou de `<slug>-tela.png`, com a palavra/número no `Thumb.jsx`. A legenda em mm só entra se for legível em 1280×720. Exemplo: `../amostras-nasa/enchente-rs-2024-claro-tela.png`. Continua **Hipótese** até haver CTR medido.

## Não fazer
- **Mais de 1 thumb com mapa escuro dominante** no mesmo vídeo; 3 variações do mesmo conceito (seca 1877, Rodrigo 16/11/2026).
- **Thumb com 3+ focos** ("VEM DAQUI": língua + fumaça + chuva + relevo; "NÃO É AZAR": 6 elementos com o Sul a ~15% da altura): reprovadas na r1 (reembalagem 14/11/2026).
- **Pintar o Pacífico inteiro de vermelho** (5 das 12 thumbs do tema) e **continente de satélite + Sul vermelho + funil** (composição do Além do Mapa) (`biblia-titulo.md`).
- **Bege + polaroid pequena** (001/002: somem a 320×180).
- Copiar a thumb de canal pequeno do tema (005 r1: muro + comporta = cópia do Edu Necessario `Xl5VTdAgAYU`; reprovado).
- Foto pequena de baixa resolução ampliada (retirantes de 1878 em 221–400 px: só como carte pequena; `../videos/003-seca-1877/ETAPA2-PRONTA.md`).

## Políticas (14/11/2026, `conhecimento/politicas-youtube.md`; `biblia-titulo.md`)
Sem foto real de morto ou vítima em destaque; acervo de vítimas/retirantes só como contexto distante, nunca close; nada de TV/emissora; sem "morte" e sinônimos no texto da thumb. Foto CC BY-SA na thumb deixa a thumb derivada sob CC BY-SA (aceito no teste granizo; crédito na descrição).

## Lições do 006 (Caraguatatuba 1967 × São Sebastião 2023, crivo 17/11/2026; `../videos/006-caraguatatuba-1967/embalagem/crivo-r1..r3.md`)
- **Desastre antigo sem foto livre** (1967: acervos municipais sem licença): `documento-evidencia` com página científica escaneada (carta de declividade de Olga Cruz, RBG 1975, CC BY 4.0) **reprovou** (r1): hachuras viram mancha cinza a 320×180, nome próprio sem lacuna ("OLGA CRUZ") e destaque sobre documento lembra o "documento grifado" de outro canal.
- `cena-acao` com foto aérea de pós-desastre (Vila Sahy 2023, CC BY 2.0) **reprovou** (r2): 3+ focos a 320×180 (escavadeiras, caixas-d'água, telhados), equipes de resgate no meio e lama marrom igual às cenas de IA do tema.
- **Aprovado** (r3): `cena-acao` com **um herói só, de perto e de cor viva** — solo laranja exposto mordendo o asfalto (Defesa Civil de Ubatuba/Gov. SP no Commons, CC BY 2.0), sem pessoa, sem máquina, sem texto. O acervo "Emergência - Chuvas no litoral norte" do Governo de SP no Commons (CC BY 2.0, 80+ fotos de 2023) serve a pautas da Serra do Mar. **Hipótese** até o CTR.
- `antes-depois` com o par Landsat da NASA Earth Observatory (domínio público) aprovado de primeira; evidência de nicho amplo explicativo pt (`XexidjTKJGY`, `g60GrTMKyiA`, `kZ3YWuGWF0k`) + CNN `eoLAkdGWVO8`. **Hipótese.**
- `mapa-lugar` controle em **cor de satélite clara** (não navy) com bloco 3D cortado de lado + "UMA PAREDE?" aprovado; aviso: exagero vertical ≤ 2× faz a parede parecer morro.

## Lições do 007 (vendavais no Paraná, crivo 21–22/11/2026; `../videos/007-vendavais-parana-2026/embalagem/crivo-r1..r3.md`)
- **Texto da thumb `mapa-lugar` tem de ser coerente com a seta e com o fato:** "POR AQUI?" (r1) só repetia o título; "LADEIRA ABAIXO?" (r2) dizia o contrário da seta (o temporal entra pela ponta baixa e sobe) e ainda soa como "piorando". Aprovado (r3): "PELO LADO BAIXO?" — pista física nova e verdadeira, sem dar a causa. Prévia a 320 feita com o relevo real (Terrain Tiles z7 + contorno IBGE, esboço oblíquo em PIL) antes do crivo.
- **`documento-evidencia` com satélite meteorológico real** (GOES-19 infravermelho, NOAA, domínio público) aprovado de primeira na r2: a mancha laranja/vermelha salta no meio de thumbs cinzentas de funil. Referências: SBT News `RKQKPMstiZk` (Melissa em IR, 10,5×) e Brasil Urgente `Kzo1yKN-O3w` (13,1×). Live de 6 h não vale como referência de thumb. **O arquivo do STAR guarda só ~10 dias:** baixe no dia; para o vídeo, o NetCDF do bucket `s3://noaa-goes19` é permanente. Um quadro só por imagem (nada de juntar horários).
- **`cena-acao` de desastre:** foto aérea de entulho (Rio Bonito, AEN) foi reprovada (tragédia + textura a 320 + pessoas/máquina, igual ao aéreo da TV); aprovado: **um objeto de perto, ao nível do chão, sem pessoas** (madeiramento de telhado, DPU CC0). Atenção à legenda: foto de dias depois pode mostrar reconstrução, então legenda só LUGAR · DATA. Sentinel-2 em cor natural/falsa-cor/ΔNDVI **não** mostra a cicatriz de um tornado no meio de lavouras a 320×180 (testado).
- Todas **Hipótese** até o CTR.
