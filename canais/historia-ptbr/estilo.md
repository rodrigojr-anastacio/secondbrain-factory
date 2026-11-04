# Estilo — História em minutos

Modelo: History in Minutes / Genius History ("A HISTÓRIA COMPLETA de X em N minutos"). O visual será definido no piloto.

## Visual (definido no piloto do Egito, 11/2026)
- Imagens: gpt-image-2 `low` no estilo do `canal.yaml`; um plano a cada ~3,3 s (~18 por minuto), Ken Burns ou pan leve, corte seco dentro do bloco e crossfade de 5 frames entre blocos.
- **Nenhuma legenda queimada** (a legenda vai só no `.srt`). Texto na tela só em: cartão de data (canto superior esquerdo), placa de capítulo ("CAPÍTULO N" + título, embaixo) e rótulos de mapa. Tudo em Libre Caslon, tinta escura sobre placa de papiro claro com sombra chapada.
- Mapas são gerados sem texto ("no labels"), e os rótulos ficam no código (`src/labels.jsx`, com posição em fração da imagem).
- Thumbnail: ilustração panorâmica à esquerda (medium) e céu livre à direita, com o PAÍS em Libre Caslon 700 preta grande e "ANO a.C. – 2026" em Open Sans 800.
- Trilha: original, sintetizada no código (sem samples), sob a voz a -33 dB; mix em -15 LUFS.
- Reuso: 0% nos 3 primeiros minutos e ~40% depois; para ~16 min, isso dá cerca de 205 imagens (~US$ 1,50).

## Voz (aprovado pelo Rodrigo)
- Clone pt-BR 48613fc… no s2.1-pro, velocidade 1.0. Pausas com moderação: [break] só entre ideias e [long-break] só antes de revelações; o excesso de pausas e a velocidade 0.95 soaram lentos e estranhos. No Egito (2.293 palavras), 15 `[break]` + 6 `[long-break]` deram 15:54 (~150 palavras/min), bom ritmo. Não passe de ~1 `[break]` por minuto.


## Fórmula de hook (sintetizada de 6 vídeos de referência; os hooks reais estão em videos/001-egito/ref/*/hook.txt)
Vídeos: Egito (VQPzrVMHWlg, 417 mil views), Irã (XO1-4FH1X1I, 918 mil), Roma (kHCamT4zfH4, 364 mil), Jerusalém (zMn0RYC6U6w, 161 mil), China (wuhnBi8jNl0, 1,17 milhão), Império Britânico (cqGJ5ZRLAvs, 222 mil).
1. **Frase 1 = paradoxo ou contraste extremo**, dito como fato: "A China morreu mais vezes que qualquer país da Terra." · "Uma vila de lama na beira de um rio que acabou dona de todo o Mediterrâneo." · "Todo império cometeu o mesmo erro fatal." · "O Egito não é um país com um rio…"
2. **Prova em rajada:** 2–4 números ou fatos curtos e impossíveis em sequência ("destruída 2 vezes, sitiada 23, atacada 52, conquistada 44…") ou uma comparação de escala de tempo.
3. **A virada:** "Mas com X, algo impossível aconteceu." · "E aqui está a parte mais louca."
4. **A pergunta central**, que sustenta o vídeo inteiro: "Então como o Egito sobreviveu a…?" · "Como um bando de foras da lei construiu um império que se recusou a morrer por 2 mil anos?"
5. **(Opcional) A promessa do percurso:** "Nos próximos N minutos, 5 mil anos de história."
6. **Entrada imediata no corpo** com uma curiosidade estranha e concreta, sem enrolação ("Nossa história começa em…" e um fato bizarro, como os reis Shang perguntando aos avós mortos).
- Tudo em **até ~40 s**, com frases curtas, linguagem falada e sem "olá, pessoal" nem vinheta.
- Mantenha o tom ao longo do vídeo: cada capítulo abre com um mini-hook (contraste ou curiosidade) e fecha puxando para o próximo.
- Duração: as referências vão de 8 a 25 min (a da China tem 25 min e 1,17 milhão de views). Para o piloto, mantenha 15–17 min.

## Thumbnail (direção do Rodrigo: inspirada na referência, mas com identidade NOSSA)
- **O que manter da referência, porque funciona:** o nome do lugar gigante e legível no celular, uma ilustração do lugar que dá para reconhecer na hora e um contraste limpo.
- **O que torna a thumb nossa:**
  - **Personagem-guia:** o bonequinho do canal em primeiro plano reagindo (espanto, curiosidade) ao lugar/época. Vira a "cara" do canal.
  - **Assinatura de tempo:** uma faixa ou selo de linha do tempo com o período (ex.: "5.000 ANOS"), sempre no mesmo canto e na mesma cor de destaque do canal.
  - **Cor de destaque fixa do canal** (ex.: amarelo-ouro ou laranja) no selo e num detalhe do título, para ser reconhecível na grade de vídeos.
  - **Título curto em PT**, no máximo 2–3 palavras na arte (ex.: "EGITO"). O resto fica no título do vídeo.
- **Para cada vídeo, gerar 3 variações** e subir as 3 no "Testar e comparar" do YouTube, deixando os dados escolherem.
- Ilustração em qualidade `medium`; o texto sempre composto no código, nunca escrito pela IA.

## Aprendizados do piloto 001 (feedback do Rodrigo, 02/11/2026)
- **Imagens:** a qualidade `low` ficou ruim no vídeo, porque o zoom do Ken Burns amplia a imagem. O padrão do canal passa a ser **`medium`** (~US$ 0,055 por imagem, ~US$ 11 por vídeo com ~200 imagens), e a thumbnail sai em **`high`**.
- **Narração:** soou robótica e atropelada, sem pausa entre um assunto e outro. Regras:
  - pausa no encadeamento dos blocos: ~0,35 s entre frases do mesmo assunto, **~0,8–1,0 s quando muda de ideia** e **~1,5 s antes de um capítulo novo**;
  - `[break]` de volta nas viradas de ideia dentro do bloco (mas não em toda frase);
  - tom de narrador contador de história: tag de emoção no início das frases-chave (`[curious]`, `[serious]`, `[amazed]`, `[slightly dramatic]`, `[warm]`), variando ao longo do vídeo, no máximo 1 por frase;
  - não aparar o silêncio natural do fim das frases de forma agressiva.
- **Como ficou implementado na v2 do 001 (use como padrão):** no `roteiro.py`, um conjunto `IDEIA` com os números dos blocos que abrem ideia nova vira `"ideia": true` no `blocos.json`; o `tools/build.py` encadeia com 0,35 s (mesmo assunto), 0,9 s (`ideia`) e 1,5 s (capítulo) e apara com cauda de 0,15 s (limiar -45 dB). Resultado: ~51 de 106 blocos marcados, 59 tags de tom (12 curious, 16 serious, 8 amazed, 12 warm, 11 slightly dramatic) e 50 `[break]`; a duração subiu ~7% (15:54 → 17:00). O Fish s2.1-pro **não lê as tags de tom em voz alta** (conferido no Whisper). A regex que limpa tags para legenda/SCRIPT precisa pegar qualquer `[tag]`, não só as pausas.

## Aprendizados do 002 (Índia, 03/11/2026)
- **Remodelar a transcrição da referência** (pedido do Rodrigo) funciona: mesma ordem, beats e números, com o texto reescrito em pt-BR. Troque as autorreferências do concorrente ("our China video") por citações do nosso catálogo (só o que já publicamos) ou por um **equivalente brasileiro do mesmo fato** (ex.: a fome de 1876 na Índia ↔ a Grande Seca de 1877 no Ceará, ambas do mesmo El Niño; Vasco da Gama → Cabral; "monsoon" ↔ a palavra portuguesa "monção").
- **Ritmo:** a referência fala ~195 palavras/min; nós, ~135 com as pausas. 2.620 palavras deram **19:27**. Para ~17 min, mire **~2.250–2.300 palavras** (encolha a transcrição em ~30%).
- **Fish corta a frase curta depois de `[break]` no fim do bloco** (o "Guarde essa chuva" sumiu). Ao fechar o bloco com uma frase de 2–3 palavras, use tag de tom em vez de `[break]` e confira com o Whisper **por bloco**.
