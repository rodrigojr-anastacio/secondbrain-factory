# Visual (imagens, edição, ritmo, texto na tela): dossie-es

Regra de canal: **prevalece** sobre `conhecimento/anti-padroes.md`. Estilo **aprovado pelo Rodrigo em 04/11/2026 (~19h)** (`videos/001-cia/AVISO-IMAGENS.md`). Testes: `../testes/ESTILO.md` e `../testes/ESTILO-es.md`.

## Imagens
- **`fal-ai/nano-banana` 16:9 (1344×768)** com o `estilo_prompt` do `canal.yaml`: graphic novel em tinta, contorno preto grosso, **proporções e rostos adultos realistas**, paleta dessaturada azul-ardósia/oliva/sépia/carvão com **vermelho pontual**, luz de cinema, grão de papel, época correta.
- Por que nano-banana [O, ESTILO-es.md]: coerente com o teste anterior, resolução maior, nenhum texto inventado; o flux/dev saiu fotográfico, com época errada (carros dos anos 70 em Langley 50s) e texto inventado em mapa.
- **Aprendizados do piloto CIA (04/11, 171 imagens; `videos/001-cia/RELATORIO.md` e `QA.md`):**
  - o nano-banana desenha **moldura de papel** em ~25% das imagens (43 de 171), mesmo com "full-bleed, no border". Rode `videos/001-cia/tools/checa_imagens.py` e recorte com `tools/recorta_moldura.py` (grátis; perde 6–20% da borda). ~~Hipótese: o "subtle paper grain texture" puxa a moldura~~ **derrubada no 002 (05/11)**: sem a frase, 51 de 198 (26%) saíram com moldura, e apareceu um 2º tipo, a **faixa preta (letterbox)** em cima e embaixo (21 das 51). O `videos/002-mossad/tools/checa_imagens.py` detecta as duas e o `recorta_moldura.py` recorta as duas; conte com ~26% e rode os dois sempre. A frase ficou fora do `canal.yaml` (a textura vem do traço, sem perda visível);
  - o **filtro do fal (HTTP 422, sem cobrança)** recusa míssil atingindo avião, tanques "in front of a house" e Torres Gêmeas com fumaça: descreva de longe e sem impacto ("trailing smoke, seen from far away"); para o 11-S, os feixes de luz do memorial;
  - **mapas:** mesmo com "completely blank", escreveu nome falso do mar Cáspio duas vezes: ponha um rótulo do código **por cima** (`fijo: true` em `src/labels.jsx`) e confira o enquadramento (o 1º mapa das Américas cortou o Chile);
  - **002 Mossad (05/11, 198 imagens): 0 recusas do filtro** escrevendo violência "seen from far away, no bodies, no blood" desde o storyboard (Munique, Lillehammer, Marjeh, Beirute). Inventou bandeira (alemã na cauda do MiG iraquiano: peça "plain bare metal tail without any flag or marking"), um medalhão redondo em vez de cena ("split face" → peça "wide interior shot") e "Egypt" num mapa (coberto por rótulo `fijo`). [`videos/002-mossad/QA.md`]
  - **003 FBI (05/11, 186 imagens): 0 recusas**; moldura de novo em 26% (48) e um **3º tipo, margem branca só nas laterais/embaixo** (4), que o `recorta_moldura.py` não pega: use `videos/003-fbi/tools/recorta_branco.py`. Ao **refazer** uma imagem, apague `imagens-orig/<id>.jpg` antes de recortar (o script reaproveita o original velho e sobrescreve a nova). Lugar real com fachada inventou letreiro ("ROXY PALACE" no Biograph): peça "blank marquee, blank signs". Pessoas "resembling" (Hoover, King, Roosevelt) saíram reconhecíveis e coerentes. [`videos/003-fbi/QA.md`]
  - **004 Cosa Nostra (05/11, 207 imagens): 0 recusas** com "seen from far away, no bodies" em Capaci, via D'Amelio, Ciaculli e Coney Island; moldura em 21% (44). Refeitas 4: o **mapa "só da Sicília" inventou uma 2ª Sicília** no canto (peça "alone in the center of a plain sea, no other land" e confira a geografia, não só o texto), "LUIGI'S PIZZA" no letreiro (peça "blank shop sign, no lettering anywhere"), manchete com letras falsas (peça "only a photograph, no headline") e um recorte de moldura que cortou a cabeça (recorte < 50% da largura: refaça em vez de recortar). [`videos/004-cosa-nostra/QA.md`]
  - 1344×768: zoom do Ken Burns até **1,44x** (no historia-ptbr vai a 1,68x) para não borrar.
- **Template do canal:** `videos/001-cia/src/` (Video.jsx com ficha "LUGAR Y FECHA", rótulo datilografado, cartão de expediente com carimbo CLASIFICADO, mapas com pinos e setas; Thumbnail.jsx A/B/C) e `videos/001-cia/tools/build.py` (trilha de espionagem + SFX de máquina e carimbo). **Copie daqui no 002**, nunca do historia-ptbr.
- Pessoas reais (Dulles, Árbenz, Castro): gerar como "a man resembling a 1950s official" e conferir com visão; **nunca foto**.
- Referência Archive [O]: ilustração de IA em quadrinho/graphic novel, iluminação de cena (lareira, neve, luminária), personagens adultos com rosto reconhecível. **Não** é o bonequinho do `historia-ptbr`. [LEVANTAMENTO §2e]

## Ritmo
- ~18–20 planos/min no 1º minuto e ~15–17 depois (Archive: 18–22 cortes/min no 1º minuto, contra 6–14 nos concorrentes que flopam). Ken Burns leve. [estilo.md de 04/11; LEVANTAMENTO §2e]
- Sem reuso nos 3 primeiros minutos; ~35% de reuso depois.

## Texto na tela (no código, em espanhol, nunca na IA)
- **Rótulo de cena** em máquina de escrever (Special Elite ou Courier Prime) sobre tira de papel `#E9DFC9`, com sublinhado ou sello rojo `#B3261E` ("CIUDAD DE GUATEMALA, 1954"). Archive [O]: rótulo em letra de mão maiúscula com sublinhado vermelho em ~1/3 dos planos.
- **Cartão de expediente:** pasta parda + "EXPEDIENTE 5" + título em caixa alta + sello "CLASIFICADO".
- **Mapas:** base sem rótulos e **sem pinos** ("no pins, no markers, no table", "flat scan of the map only, no table, no frame"); **pinos e setas desenhados no código** (nenhum modelo acertou a posição: os pinos caíram no México, Colômbia e Brasil em vez de Guatemala, Cuba e Chile). [ESTILO-es.md]
- Sem legenda queimada.

## Som
- Trilha original sintetizada no código (drone grave + pulso), sob a voz a −33 dB; mix em −15 LUFS. SFX discretos: máquina de escrever no rótulo, carimbo no expediente.

## Políticas
- Proibido: suástica, runas SS e insígnias extremistas em destaque; sangue e cadáveres; fotos de arquivo e trechos de filme (Content ID); texto em português.
- Conteúdo educacional/documental com contexto (EDSA). Nada que glorifique; cartéis sem glamour e com o custo humano. Cadência humana (2–3/semana), roteiro original, nunca template em massa (política de conteúdo inautêntico do YPP). [LEVANTAMENTO §3d; IDIOMA.md §4]

## Não faça
- Bonequinhos, cartoon chapado colorido, céu azul com nuvens, papiro e Libre Caslon (identidade do `historia-ptbr`); pintura a óleo romântica (`lotr-fr`).
