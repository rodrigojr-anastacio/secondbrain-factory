# ETAPA 1 PRONTA: Em Relevo 006, Caraguatatuba 1967 × São Sebastião 2023 (17/11/2026)

`youtube.videos` **id 47** (em-relevo, nº 6, status `roteiro`, título = T1). Pasta: `canais/em-relevo/videos/006-caraguatatuba-1967/`. Janela sugerida: qua ou sex (o Rodrigo decide). Custo da etapa 1 em dinheiro: **US$ 0** (Data API ~150 unidades, `search.list` 0; detector com Haiku ~US$ 0).

## Ângulo (1 linha)
**A receita medida:** por que a Serra do Mar desce sobre o litoral, mostrado com números próprios no relevo 3D (parede ~700 m a < 6 km da praia; temporal preso numa faixa estreita: 683 × 627 × 234 mm; casca de 1–2,5 m quase sem coesão) e provado em 1967 (640 cicatrizes, carta de Olga Cruz) e em 2023 (Landsat). `ANGULO.md` (6 vídeos da manada transcritos).

## Embalagem aprovada (crivo r3, 6 de 6)
| par | título | padrão do título | thumb (padrão) | texto |
|---|---|---|---|---|
| **A** | **Por que a SERRA DO MAR desaba sobre o LITORAL?** (46) | Por que [LUGAR] [anomalia]? (controle) | `mapa-lugar`: bloco 3D do relevo real em cor de satélite, parede cortada de lado, seta coral até a cidade | "UMA PAREDE?" |
| **B** | **CARAGUATATUBA 1967, SÃO SEBASTIÃO 2023: por que a serra repete?** (63) | Contraste A × B + por que | `antes-depois`: Landsat 29/10/2022 × 26/02/2023 das mesmas encostas, tela dividida | "UMA NOITE" |
| **C** | **A CASCA de terra que faz a SERRA DO MAR desabar** (47) | O/A [coisa concreta] que [faz algo] | `cena-acao`: foto real (Defesa Civil de Ubatuba/Gov. SP, CC BY 2.0, 19/02/2023) do solo laranja exposto mordendo o asfalto | (nenhum) |
Histórico: r1 4/6 (T3 "O MAPA de 1975…" e Thumb C carta de Olga Cruz reprovados: objeto de um capítulo só; documento ilegível a 320×180); r2 5/6 (Thumb C foto aérea da Vila Sahy reprovada: 3+ focos, resgate, lama marrom igual às cenas de IA); r3 aprovado. `embalagem/crivo-r1..r3.md`, `EMBALAGEM-r1/r2.md`. Registrado em `youtube.embalagem_variantes` (A/B/C = mapa-lugar, antes-depois, cena-acao).

**Promessa:** ver no relevo 3D por que a Serra do Mar desce sobre o litoral norte de SP (parede + temporal preso + casca de terra) e como essa receita fez Caraguatatuba em 1967 e São Sebastião em 2023.
**Onde o roteiro paga** (tempos estimados; hook a ~1,36×):
- hook b01–b03 (**0:00–~0:30**): 683 mm em Bertioga × 234 em Caraguatatuba; 627 em São Sebastião + satélite; os dois perfis lado a lado (o mesmo degrau, ~700 m a < 6 km) e a frase **"Não foi azar: a receita está no relevo."** (~0:27–0:30). *Desvio da obrigação do `EMBALAGEM.md`:* a 1ª metade da frase-âncora ("Em 1967 e em 2023, a mesma serra desceu sobre o litoral") saiu a pedido do **crivo de ângulo r1** (é a tese de fecho do ToXu, da manada); a promessa e o resto da frase ficaram.
- pergunta do T1 + T2 no b04 (~0:32); parede no b05; **3 ingredientes com números + "casca"** no b06 (**~0:46–1:01**, paga T3 no 1º minuto); Olga Cruz no b07 (~1:01).
- T2 (a serra repete): hook + cap. 5 **b33–b37 (~7:15–8:15)** com o Landsat e a frase da NASA "não sem precedente… o precedente fica a 35 km".
- T3 (casca): cap. **"3 · A CASCA DA SERRA" b20–b25 (~4:03–5:25)**, com a carta de Olga Cruz (b23) e a foto de Ubatuba (b25).
- Resposta b38–b39 (~8:15–8:55); fecho útil b40–b42 (SGB, IBGE, SMS 40199); CTA b43 (puxa para a seca de 1877, `I5KpDKy6r3E`; sem próximo vídeo).

## Roteiro e portões
- `shared/roteiro.py` → `shared/blocos.json` (43 blocos, **1.668 palavras, 9.183 caracteres** para o TTS, **~9:54** estimados); leitura em `ROTEIRO.md`; fatos em `pesquisa/FATOS.md`; bloco → fonte e cota em `SOURCES.md` (~90% dos blocos de conteúdo com dado/cena fora da manada; meta 40%).
- **Detector de cópia: 3/100** (`SIMILARIDADE.md`; maior = ToXu).
- **Crivo de ângulo: r1 REPROVADO** (itens 2 e 4: imagens do ToXu — "serra que fabrica a chuva", "capa de solo", "concreto da betoneira", "a serra continua a mesma", tese "a mesma serra desceu") → reescritos b01, b03, b06, b11, b13–b17, b20–b24, b28, b32, b38–b39 → **r2 APROVADO** (+ 4 ajustes recomendados aplicados). `roteiro-crivo/`, `CRIVO-ANGULO.md`.
- Storyboard: `STORYBOARD.md`, `shared/storyboard.py` → `shared/storyboard.json`, `shared/cenas.json`, `work/storyboard-tabela.md` (zero IA; 7 mídias reais em `dl/`, licenças em `pesquisa/FOTOS.md`).

## O que a etapa 2 precisa saber
1. **Voz ElevenLabs** (Fernanda `7iqXtOF3wl3pomwXFY7G`, `eleven_v3`; `shared/gera_voz_eleven.py` do 005 — **ajustar caminhos para o 006**). Pede ~9.200 caracteres (+15% de refações). **Conferir o saldo** (plano 38.634/mês, reset dia 08; o 005 consumiu em 16/11). Se não couber: reserva Fish #NATASHA drama-3 (`canal.yaml`), `--video 47`. Hook = b01–b06 (marcha 1; atempo 1,36×). Conferir com Whisper que a frase-âncora termina **antes de 0:30** na `legendas.srt` (se passar, aumentar o atempo do hook ou encurtar b01).
   **Pronúncia:** Caraguatatuba, Bertioga, Ubatuba, Juqueriquerê ("ju-ke-ri-ke-RÊ"), Barra do Sahy ("saí"), Santo Antônio, Juquehy ("juqueí"), IAG ("i-a-gê"), USP ("usp"), CEMADEN ("ce-ma-DÊN"), IBGE, SMS ("ésse-ême-ésse"), CEP ("cep"), "40199" (já por extenso no `fala_tts`), Landsat ("lend-sat"), "1877" ("mil oitocentos e setenta e sete").
2. **Thumbs A/B/C, uma por conceito** (skill `thumbnail`; `remotion/src/Thumb.jsx` ThumbA/B/C; US$ 0):
   - **A:** bloco 3D do Morro do Cruzeiro (perfil `dados/perfis.json`), **cor de satélite clara** (não navy), face do corte em terra `#B9A47F`, seta coral, "UMA PAREDE?" (UMA branco, PAREDE? amarelo `#FFD23F`). **Exagero vertical maior que 2×** (o crivo r1 avisou: a 2× parece morro, não parede) + "ilustrativo" pequeno fora da leitura.
   - **B:** `dl/fotos/satelite/nasa-eo-landsat9-…-antes-2022-10-29.jpg` | `…landsat8-…-depois-2023-02-26.jpg`, **mesmo recorte apertado (2–3 km por metade)**, estiramento comum, **sem a nuvem do canto**; "UMA NOITE" numa tarja no corte.
   - **C:** `dl/fotos/video/ubatuba-encosta-arrancada-estrada-2023-02-19.jpg` em tela cheia, recorte 16:9 como `embalagem/previa-c-r3-1280x720.jpg`, **cortar/escurecer o galho de folhas claras do canto superior direito**; sem texto.
   - Prévia 320×180 ao lado de `embalagem/mosaico.jpg` e `embalagem/vizinhas-em-relevo.jpg`. `entrega/thumbnail.jpg` = A.
3. **Pacote:** A = T1, B = T2, C = T3 com o padrão de cada par no `youtube.txt`; regravar `embalagem/variantes.json` + `embalagem_variantes.py registrar` com arquivos. Descrição/tags **sem** morte/morreu/morto/vítimas fatais. Créditos: NASA EO/USGS Landsat; Olga Cruz/RBG-IBGE (CC BY 4.0); Defesa Civil de Ubatuba/Gov. SP (CC BY 2.0); Gov. SP (CC BY 2.0); Themium (CC0); SGB; CEMADEN; IBGE; NASA GPM IMERG; SRTM/Terrain Tiles; OSM (ODbL); trilha Kevin MacLeod (CC BY 4.0). Fontes de `SOURCES.md`.
4. **Relevo do litoral norte de SP:** baixar com o script do 005 (`shared/baixa_relevo_rs.py` → adaptar bbox ~ −46,3/−23,95/−44,9/−23,35, Terrain Tiles z11–z12) e gerar texturas A/B (`gera_texturas_rs.py` adaptado). Os perfis já calculados estão em `dados/perfis.json`.
5. **Carta do SGB** (`dl/fotos/doc/sgb-carta-suscetibilidade-caraguatatuba.pdf`, 34 MB): extrair só as classes de deslizamento e **conferir** se as classes altas acompanham as encostas íngremes (b32 afirma isso; se não acompanhar, trocar a frase do b32 por "a carta marca as encostas de alta suscetibilidade ao pé das quais está a cidade" e regravar só o b32). Conferir o termo de uso no RIGEO.
6. **QA do contrato** (`legendas.srt`): frase-âncora ≤ 0:30; "casca" ≤ 1:05; aba "3 · A CASCA DA SERRA" ≤ ~4:30; Landsat ≤ ~7:30; números na tela = narração (683/627/234/335; 400 em 6 h; 640; 2 mi t; 120–~500; 65; 1.815/2.251; ~3 mil; 135 mil).
7. Render só no Runpod (`tools/render_runpod.sh`, em partes), pré-QA visual antes; nada em `/tmp`. **Teto US$ 3.** Entrega local em `entrega/` (sem Drive).

## Pendências (menores, não bloqueiam)
- Referência não reassistida com `watch.py` (janela da noite); formato do Mundo Entrópico em `youtube.assistidos`.
- "Contagens da época chegaram perto de 500" (b31): versões 436 (imprensa), ~450 (IPT, via imprensa), 487 (GADRI); ok como "perto de 500", mas sem fonte primária oficial.
- "15 mil em 1970" saiu do roteiro (fonte secundária); fica só o Censo 2022 (134.873).
- Origem da escarpa (b11) apoiada em resumos de Almeida & Carneiro 1998 (sem idade no texto).
- A 1ª metade da frase-âncora foi trocada pelo crivo de ângulo (ver acima); a QA confere a 2ª metade + os perfis lado a lado.
- Licença CC BY 4.0 da carta de Cruz é a declarada pela revista para todo o acervo (artigo de 1975): manter crédito completo; se o Rodrigo preferir zero risco, a carta pode ser trocada por mapa de declividade nosso (SRTM) no b07/b23.
