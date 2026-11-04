# Estilo: Dossier en Minutos (dossie-es)

Base: `pesquisa/archive-in-minutes/LEVANTAMENTO.md` (anatomia do formato), `IDIOMA.md` (por que es) e `idioma/NOTAS.md` (demanda es). Modelo: Archive in Minutes (en); prova em es: Atlas del Tiempo. A **identidade é nossa** (o "expediente"): nunca copie a thumb, o hook ou o texto deles. Este canal **não** usa o bonequinho nem o papiro do `historia-ptbr`. A versão pt-BR adiada está em `arquivo-ptbr/`.

## Idioma e público
- **Espanhol neutro latino-americano**, com **tú** (nunca "vosotros"; sem gírias locais: nada de "chido", "guay", "boludo"). Datas em "27 de junio de 1954"; números por extenso quando o Fish ler mal.
- Público [O, `NOTAS.md` §3]: canais de demanda MX 22%, ES 22%, US 9%, AR 6%. Escreva para quem está no México e para quem está em Madri: termos neutros ("computadora/ordenador" → evite os dois; "auto/coche" → "vehículo" só se precisar).
- **Ângulo América Latina** sempre que houver fato real com fonte (Guatemala, Cuba, Chile, Operação Condor, cartéis, nazistas na Argentina). É a diferença em relação ao Archive e aos clones.

## Fórmula
- **Título:** "TODA la historia de <la organización> en N minutos". TODA em caixa alta; N = duração real arredondada; X com 1–3 palavras, de preferência sigla famosa. Título B: "La historia COMPLETA de X en N minutos".
- **Duração:** 11–16 min (alvo 13). ~140 palavras/min nas amostras Fish es: 1.500 palavras ≈ 11 min; 1.800 ≈ 13 min. Acima de ~17 min, não.
- **Temas:** os fortes **em espanhol**, e não a ordem do Archive. Em es, CIA, FBI, máfia, cartéis, SS e Templários têm muito mais busca que Stasi e MI6 (`backlog.md`).

## Roteiro
1. **Hook de 25–35 s (molde anedota):** data + lugar → cena humana concreta em 2–4 frases curtas, no presente → desfecho seco ou reviravolta → "Esta es TODA la historia de X" → promessa em 1 linha. Sem "hola", sem vinheta, sem pedir inscrição.
   - Use uma anedota **diferente** da usada pelo Archive e pelos clones (Eichmann no Mossad, Putin em Dresden na KGB).
2. **Expedientes (capítulos-objeto):** 11–14 capítulos de 45–75 s, cronológicos, com o título "EXPEDIENTE N: EL/LA <OBJETO>" ("EXPEDIENTE 5: LA RADIO"). Cada expediente é uma cena ou objeto datado, com números exatos e fonte.
3. **Cierre:** volta ao objeto do hook (loop pago), liga ao presente e termina com 1 pergunta para os comentários ("Y tú, ¿…? Déjalo en los comentarios.").
4. **Tom:** presente histórico, factual, seco, quase sem adjetivo; o horror vem do fato. Toda acusação vai atribuída a um documento ("según documentos desclasificados…", "un comité del Senado documentó…"). Fato incerto é dito como incerto.

## Revisão em espanhol (o Rodrigo lê, mas não é nativo)
1. O roteiro é escrito **direto em espanhol**, nunca traduzido do pt. Falsos amigos a vigiar: "exquisito", "embarazada", "polvo", "largo" (= comprido), "oficina" (= escritório).
2. **2ª leitura por LLM** com o prompt "revise como editor nativo mexicano e depois como editor espanhol: erros, calcos do português, termos regionais" antes do `roteiro.py`.
3. **Whisper por bloco ≥ 95%** depois da voz (skill `voz`); nomes próprios conferidos à parte.
4. O Rodrigo lê o `SCRIPT.md` e o pacote (`youtube.txt`). Dúvida de sentido = reescrever a frase, não discutir.

## Visual
- **Imagens:** `fal-ai/nano-banana` 16:9 (1344×768) com o `estilo_prompt` do `canal.yaml`: graphic novel em tinta, contorno grosso, paleta azul-ardósia/oliva/sépia/carvão com **vermelho pontual**. Rostos adultos e época correta. Testes em `testes/ESTILO.md` e `testes/ESTILO-es.md`.
- **Ritmo:** ~18–20 planos/min no 1º minuto e ~15–17 depois. Sem reuso nos 3 primeiros minutos; ~35% de reuso depois.
- **Texto na tela (no código, em espanhol, nunca na IA):**
  - rótulo de cena em máquina de escrever (Special Elite ou Courier Prime) sobre tira de papel `#E9DFC9`, com sublinhado ou sello rojo `#B3261E` ("CIUDAD DE GUATEMALA, 1954");
  - cartão de expediente: pasta parda + "EXPEDIENTE 5" + título em caixa alta + sello "CLASIFICADO";
  - mapas: base sem rótulos e **sem pinos** ("no pins, no markers, no table"); **pinos e setas desenhados no código** (o modelo erra a posição, ver `testes/ESTILO-es.md`).
- **Proibido:** suástica, runas SS e insígnias extremistas em destaque; sangue e cadáveres; fotos de arquivo e trechos de filme (Content ID); legenda queimada; texto em português.
- **Trilha:** original, sintetizada no código (drone grave + pulso), sob a voz a −33 dB; mix em −15 LUFS. SFX discretos: máquina de escrever no rótulo, carimbo no expediente.

## Thumbnail
- Layout "pôster de expediente": personagem-ícone em meio corpo à **esquerda** (chefe ou agente arquetípico, com objeto na mão) + cenário reconhecível + **SIGLA gigante** (Bebas Neue ou Oswald 700, preta) à direita + **sello rojo inclinado com o período** ("1947–HOY") + **aba de pasta parda** no canto superior direito com "EXPEDIENTE Nº 001". A aba é a nossa assinatura na grade.
- Base em nano-banana com "right half empty, no signage, no lettering"; texto em `src/Thumbnail.jsx`. 3 variações para o "Testar e comparar".

## Voz
- Fish s2.1-pro, por frase, velocidade 1.0. Masculina, acento **neutro** (nem mexicano marcado nem espanhol), documental. Sugestão no `canal.yaml`; finalistas em `testes/voz/LEIA.md` (escolha do Rodrigo). **Não** usar vozes que imitam pessoas reais (dubladores, políticos, Iker Jiménez) nem a voz de TikTok mais usada (`locutor k`).
- Siglas como no uso latino ("la ce-i-a", "el ka-ge-be", "el efe-be-i"); confira a pronúncia na 1ª amostra do roteiro.

## Políticas (ver `pesquisa/archive-in-minutes/LEVANTAMENTO.md` §3d e `IDIOMA.md` §4)
- Conteúdo educacional/documental com contexto (EDSA). Nada que glorifique; cartéis sem glamour e com o custo humano.
- Descrição em espanhol, com fontes (edições em espanhol quando houver) e a nota "Narración con voz sintética; ilustraciones generadas con IA a partir de investigación histórica."
- Cadência humana (2–3/semana), roteiro original: nunca template em massa (política de conteúdo inautêntico do YPP).

## Aprendizados do piloto 001 (CIA, 2026-11-04; fonte: `videos/001-cia/RELATORIO.md` e `QA.md`)
- **Ritmo da voz Dio Historias por frase:** 1.686 palavras deram 11:46 com as pausas do `build.py`, ou seja, **~143 ppm**. O `WPS = 2.3` do `roteiro.py` estimou 12:21 (5% acima). Para 13 min, mire ~1.850 palavras.
- **nano-banana desenha moldura de papel** em ~25% das imagens (43 de 171), mesmo com o estilo do canal. O prompt com "full-bleed, no border" não resolveu. Rode `videos/001-cia/tools/checa_imagens.py` e recorte com `tools/recorta_moldura.py`, que é grátis e perde 6–20% da borda. **Hipótese:** o "subtle paper grain texture" do `estilo_prompt` puxa a moldura; teste tirar essa frase no 002.
- **Filtro do fal (HTTP 422, sem cobrança)** recusa míssil atingindo avião, tanques "in front of a house" e Torres Gêmeas com fumaça. Descreva de longe e sem impacto ("trailing smoke, seen from far away"); para o 11-S, use os feixes de luz do memorial.
- **Mapas:** mesmo com "completely blank", o nano-banana escreveu nome falso do mar Cáspio duas vezes. Ponha um rótulo do código **por cima** (`fijo: true` em `src/labels.jsx`). Confira o enquadramento (o 1º mapa das Américas cortou o Chile).
- **Pronúncia:** "CIA" sai como "sía" (uso latino), e "OSS", "U dos", "PB Success" e "MK Ultra" saem bem. Números sempre por extenso no texto.
- **Revisão nativa** (subagente Sonnet, nota 8/10): os erros foram calcos do inglês ("sostenidas por", "pareció aprobarlo"), vírgula antes de "y", "lleva adelante" (rioplatense) e "invencible". Mantenha a 2ª leitura antes da voz.
- **Template do canal:** `videos/001-cia/src/` (Video.jsx com ficha "LUGAR Y FECHA", rótulo datilografado, cartão de expediente com carimbo CLASIFICADO e mapas com pinos e setas; Thumbnail.jsx A/B/C) e `tools/build.py` (trilha de espionagem + SFX de máquina e carimbo). Copie daqui no 002.
