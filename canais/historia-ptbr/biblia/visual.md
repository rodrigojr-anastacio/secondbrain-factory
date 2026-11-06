# Visual (imagens, edição, ritmo, texto na tela): historia-ptbr

Regra de canal: **prevalece** sobre `conhecimento/anti-padroes.md` (armadilhas de ferramenta e custos gerais). Configuração técnica em `../canal.yaml` (`visual`).

## Identidade das imagens
- **Bonequinhos de cabeça redonda**: cartoon desenhado à mão, contorno preto grosso, cores chapadas e vivas, sombreamento suave, pessoas simples com cabeça redonda branca, olhos de ponto e rosto expressivo; cenários detalhados e limpos, céu azul com nuvens brancas, paleta terrosa quente. (`estilo_prompt` do `canal.yaml`; definido no piloto do Egito, 11/2026.)
- **Motor desde 05/11/2026 (decisão do Rodrigo): `google/nano-banana-2.1/edit` no fal**, com 3 imagens gpt-image-2 do canal como referência de ESTILO (`001-egito/imagens/I041.jpg`, `I120.jpg` e `002-india/imagens/I041.jpg`, em `canal.yaml` → `visual.refs`), 1K (1376×768), reescalado para 1536×864 pelo `tools/img_fal.py`, `thinking_level: minimal`. Custo real: **US$ 0,046/img** (US$ 0,058 com o thinking padrão). 003 v2: 212 imagens, 0 pretas, 0 molduras, 2 refeitas por letras.
  - **Regra de prompt (aprendida no lote-prova do 003 v2):** personagem com nome sai com rosto semi-realista se o prompt descrever rosto ("long square curled beard", "thick dark eyebrows"). Escreva **"X as a round-white-head cartoon king with a simple flat beard shape, …"** e mantenha a `ref_instrucao` do `canal.yaml` ("every person… round white head… never realistic faces"). Figuras modernas reais vão sem nome no prompt (o nome entra no rótulo do código).
  - Sempre: lote-prova de 6 cenas variadas (multidão, mapa, rei, clérigo, diagrama, cenário) e conferência por pranchas antes e depois do lote.
- Motor anterior: gpt-image-2 `medium` (Egito e Índia; ainda vale como plano B no fal, `openai/gpt-image-2`, US$ 0,04). O `low` foi reprovado em 02/11 (borra no Ken Burns). [conhecimento/anti-padroes.md §1]
- **Alerta 04/11/2026:** no 003 v1, com OpenAI sem crédito, as imagens saíram no `fal-ai/flux/dev`, e o Rodrigo disse que ficaram "bem piores que as do gpt-image-2" e que **"sumiram os bonequinhos de cabeça redonda"**; apareceram rostos realistas e caricaturas (qizilbash com cara de Papai Noel). [BRIEF-historia-003-v2.md; conhecimento/anti-padroes.md §3b] A bancada de modelos do fal está em `videos/003-ira/v2-amostras/imagens/` (job `historia-003-v2`). **Registre aqui o modelo aprovado pelo Rodrigo.** Até lá: gpt-image-2 é o padrão; outro motor só depois de uma amostra aprovada que mantenha os bonequinhos.
- No flux/dev, use `{width: 1536, height: 864}` (landscape_16_9 sai 1024×576 e borra). [canal.yaml; anti-padroes §3b]

- **004 China (05/11/2026):** lote-prova aprovado na 1ª tomada (Qin, Confúcio, multidão, mapa, túmulo, Muralha) com a regra "round-white-head cartoon…". 215 imagens, 8 refeitas. O que o nano-banana errou: inventa astronautas e põe a Terra no céu numa sonda robótica (Chang'e 6) → escreva "unmanned… no people, no Earth visible"; desenha **coroa europeia** quando o prompt diz "crown" sem descrever ("a Chinese imperial crown: a flat black board with hanging bead strings"); "ancient tomb" com palmeiras vira Egito ("grassy Chinese burial hill with pine trees"); placas e quadros ganham letras inventadas ("no boards, no signs"); "flags" em 1911 saem com tricolor errada ("no flags"). Custo real US$ 0,0459/img. [QA.md 004]

## Edição e ritmo
- Um plano a cada ~3–3,6 s: ~20 por minuto nos 2 primeiros minutos e ~17 depois; Ken Burns ou pan leve; corte seco dentro do bloco e crossfade de 5 frames entre blocos. [estilo.md antigo; QA.md 001 e 002: Egito v2 295 planos, média 3,46 s; Índia 335 planos, média 3,48 s]
- 1º minuto: ≥ ~21 planos (o Egito v2 caiu para 21 com as pausas novas, no limite). [QA.md 001]
- Referência HiM Irã: 17 cortes/min no início (`youtube.assistidos`).
- Reuso: 0% nos 3 primeiros minutos, ~40% depois, nunca o mesmo enquadramento em < 60 s. Para ~16 min, ~190–205 imagens.
- Trilha original sintetizada no código (sem samples), sob a voz a −33 dB; mix em −15 LUFS. Trilha do 003: modo Hijaz (Oriente Médio); do 004: pentatônica chinesa (modo gong em Ré, timbre de guzheng). Escolha a escala pela região do tema. [commit fe5c7e4; 004 `tools/build.py`]

## Texto na tela
- **Nenhuma legenda queimada** (legenda só no `.srt`).
- Cartão de data (canto superior esquerdo), placa de capítulo ("CAPÍTULO N" + título-frase da era, embaixo) e rótulos de mapa. Tudo em Libre Caslon, tinta escura sobre placa de papiro claro com sombra chapada. [estilo.md antigo]
- Mapas gerados **sem texto** ("no labels") e rótulos no código (`src/labels.jsx`, posição em fração da imagem). O flux escreve letras falsas em mapas: reuse um mapa limpo. [anti-padroes §3b]
- Rótulo de nome/lugar (`@@NOME` no `roteiro.py`, placa no canto inferior esquerdo): entrou no 003 copiando o Archive in Minutes. **Hipótese** para este canal: use com moderação (nomes e lugares que o espectador precisa guardar), não como regra de "1 a cada 2 planos". Nunca no 1º plano de capítulo.

## Não faça
- Graphic novel em tinta com rostos adultos realistas, paleta ardósia/sépia, máquina de escrever, carimbo "CLASIFICADO": identidade do `dossie-es`.
- Pinturas a óleo românticas: identidade do `lotr-fr`.
- Bandeira atual em cena de época (Egito v1: bandeira de hoje em 1922 e 1952) e estereótipos (curandeiro de Mehrgarh com cocar de penas, Índia). [QA-v1.md 001; QA.md 002]

## Modelo de imagem: bancada do fal (04/11/2026, fonte `videos/003-ira/v2-amostras/imagens/MODELOS.md`)
- O 003 perdeu os bonequinhos porque saiu no `fal-ai/flux/dev`: o modelo ignora "round white heads, dot eyes". O prompt era o mesmo dos vídeos anteriores.
- O **gpt-image-2 existe no fal** (`openai/gpt-image-2`, medium 1536×864 a US$ 0,04/img) e reproduz o estilo do Egito e da Índia sem precisar de crédito na OpenAI.
- O plano B, `google/nano-banana-2.1/edit` com 2 refs do canal (US$ 0,044/img), fica próximo.
- O flux/dev, o ideogram, o z-image e o seedream 4 não servem para este canal.
- **Decisão (05/11/2026):** o Rodrigo escolheu o nano-banana-2.1/edit + refs (acima). O flux/dev saiu do `canal.yaml`.

## Identidade do canal (logo e capa), 06/11/2026
- Em `../identidade/` (`LEIA.md`): 3 logos sem letras (bonequinho + ampulheta em fundo ouro é o recomendado; coroa + pergaminho; ampulheta com globo) e 2 capas 2560×1440 (desfile das eras com marcos no horizonte; livro aberto com o mundinho da história), título "HISTÓRIA EM MINUTOS" em placa de papiro + tagline em pílula ouro, tudo dentro da área segura 1546×423. Bases no `nano-banana-2.1/edit` + refs do canal, texto no código (`identidade/tools/compor.py`). US$ 0,56. Entregue no Drive (`Youtube/História em minutos/identidade/`). **Aguardando a escolha do Rodrigo**: registre aqui qual logo e qual capa foram ao ar.
- Logo e capa usam a mesma linguagem das thumbs (ouro #F7C21B, Libre Caslon 700 + Open Sans 800, bonequinhos de cabeça redonda), nunca a do `dossie-es` (carimbos, pastas, tinta).
