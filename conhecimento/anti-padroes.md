# Anti-padrões: erros já cometidos (e quanto custaram)

**Como atualizar:** todo agente que errar, ou vir um erro no QA, registra aqui. Também alimentam: **Métricas** (o que derrubou views ou retenção), **Tendências** (o que as referências evitam) e o **feedback do Rodrigo**. Cada entrada leva **data e fonte**. Sem dado, marque **Hipótese**. Depois de editar, faça commit descritivo (ex.: `conhecimento/anti-padroes: imagens em dobro na Índia`).

Última revisão: 2026-11-04 (A/B de voz e banco corrigido, vídeo 003).

---

## Regras rápidas

**Não faça**
1. **Imagens em `low` no vídeo.** O zoom do Ken Burns amplia a imagem e ela vira borrão. Padrão: `medium` no vídeo e `high` na thumb.
2. **Narração corrida, sem respiro entre ideias, e "robótica".** Use pausas de 0,35 s (mesmo assunto), 0,9 s (ideia nova) e 1,5 s (capítulo). Desde o 003: texto escrito para a fala + `tts_fish.py --por-frase` (0,32 s entre frases) e tag de tom só na virada; tags de "direção" (`[serious, calm]`, `[low voice]`) e velocidade 0,97 deixam as frases mais iguais (ver evidência 2b).
3. **Dois `img_openai.py` em paralelo na mesma pasta.** Gera imagens em dobro. Use `--paralelo 8` num processo só.
4. **Gerar sem conferir o saldo.** A Índia parou com "no credits" e ficou sem 2 imagens.
5. **Lugar real no lugar de um fictício** (Mont-Saint-Michel como Minas Tirith) e **cidades desenhadas por código** (ficam amadoras).
6. **Frames de filme ou série** (Content ID).
7. **Subir a versão do Telegram** no YouTube.
8. **Republicar, trocar título ou thumb sem atualizar** `youtube.videos`, o `backlog.md` e este conhecimento.

**Faça**
- Reuso planejado no storyboard: 0% nos 3 primeiros minutos, ~40% depois, nunca o mesmo enquadramento em menos de 60 s.
- Antes de gerar: crie a linha em `youtube.videos`, confira `financas.saldo_pre_pago` e o teto do brief, e rode as gerações com `--video <id>`.
- Confira a voz com Whisper **por bloco** (palavras faltando ou tags faladas).

---

## Evidências

### 1. Imagens `low` reprovadas (Egito, 2026-11-02)
- A v1 do Egito saiu com 204 imagens em `low` (thumb em `medium`). [QA-v1.md, ETAPA2.md 001]
- Feedback do Rodrigo (02/11/2026): "a qualidade `low` ficou ruim no vídeo, porque o zoom do Ken Burns amplia a imagem". Novo padrão: `medium` (~US$ 0,055/imagem estimado; ~US$ 0,042 no custo calibrado) e thumb em `high`. [estilo.md historia-ptbr; canal.yaml]
- Na v2, a nitidez média em 8 planos reenquadrados (1,4–1,68x) foi de 182,6 para **265,5 (+45%)** (variância do Laplaciano). [QA.md 001]
- Custo da troca: a v2 refez as 204 imagens em `medium` por **US$ 8,55 (R$ 49,84)**, contra ~US$ 1,06 da leva `low` (ids 7 e 9 de `financas.consumo`). [ETAPA3.md 001; consulta de 2026-11-04]
- Atenção: a seção "Visual" do `canais/historia-ptbr/estilo.md` ainda diz `low`; vale a seção "Aprendizados do piloto 001" e o `canal.yaml` (`qualidade: medium`).

### 2. Narração corrida sem pausas reprovada (Egito, 2026-11-02)
- Na v1, 85 `[break]` foram removidos (ficaram 15), e o `build.py` encadeava os blocos com 0,16 s. Pausa média real entre blocos: **0,33 s**. [ETAPA2.md, QA.md 001]
- Feedback do Rodrigo: soou "robótica e atropelada": "termina um assunto e já emenda o próximo, sem respiro". [.v2-prompt.txt, estilo.md historia-ptbr]
- Correção na v2: 50 `[break]` nas viradas, 59 tags de tom (no máximo 1 por frase) e encadeamento de 0,35/0,9/1,5 s com cauda de 0,15 s. Pausa média: **0,90 s** (1,10 s em ideia nova e 1,70 s antes de capítulo). A duração subiu ~7% (15:54 → 17:00). [ETAPA3.md, QA.md 001]
- O extremo oposto também foi reprovado: excesso de pausas e velocidade 0,95 "soaram lentos e estranhos" nos testes de voz. [estilo.md historia-ptbr]
- Cuidado: o Fish corta uma frase curta depois de `[break]` no fim do bloco ("Guarde essa chuva" sumiu na Índia). [QA.md 002]

### 2b. Narração "robótica": A/B de 11 tomadas do hook (vídeo 003, 2026-11-04)
- Feedback do Rodrigo no `BRIEF-historia-003.md`: "a narração está robótica". Teste com o mesmo hook de ~60 s em 6 técnicas (2 tomadas em 3 delas). Arquivos, medidas e critério em `canais/historia-ptbr/videos/003-ira/amostras-voz/LEIA.md`; custo US$ 0,14.
- Medida principal: **repetição melódica** (correlação entre os contornos de F0 das frases; Praat). Texto do 002 (A) = 0,14 e queda de −2,4 st no fim de cada frase; texto reescrito para a fala (B) = 0,10–0,11 e −1,7/−2,1; **por frase com silêncio inserido (G) = 0,09**; tags de direção (F) = 0,16–0,17; tags + velocidade 0,97 (H) = 0,19 e −3,0. temperature/top_p 0,9 = sem efeito além do ruído (~0,15 st entre tomadas).
- Decisão: **G** = texto falado + `tools/tts_fish.py --por-frase` (cache por frase; regera só a frase ruim). **Hipótese** até o Rodrigo ouvir A × G e até a retenção do 003. Se ainda soar robótico, regravar a referência do clone (30–60 s naturais com pausas, guia do Fish), não mexer em parâmetro.

### 3. Imagens geradas em dobro (Índia, 2026-11-03)
- 223 gerações para 196 imagens (195 do vídeo + thumb-base): **27 em dobro**. Causa: 2 processos `img_openai.py` em paralelo, cada um numa ponta da lista. Eles calculam os pendentes só no início e se cruzaram no meio. Custo extra: **~US$ 1,1** (27 × ~US$ 0,042). [BLOQUEIO.md, ETAPA-FINAL.md 002; `financas.consumo` ids 16 e 17: 133 + 90 imagens]
- Regra já registrada no playbook: um processo só, com `--paralelo 8`. [playbooks/produzir-video.md]
- O plano da Fase 2 pede uma **trava anti-duplicação** na skill `imagens`. [PLANO-ARQUITETURA.md, item 11]
- **Implementada em 2026-11-04:** `img_openai.py` e `img_fal.py` fazem `flock` em `<pasta>/.img.lock` (o 2º processo na mesma pasta sai com aviso, código 3) e re-checam cada id logo antes da chamada paga. O `claude_run.py` tem trava equivalente por vídeo+etapa. [tools/_trava.py, tools/claude_run.py; testado sem gasto com trava simulada]

### 3b. Armadilhas do fal.ai flux/dev (Irã, 2026-11-04)
Fonte: `canais/historia-ptbr/videos/003-ira/RELATORIO.md` (falha 2), `financas.consumo` ids 30–40.
- `image_size: landscape_16_9` sai **1024×576**: borra no Ken Burns em 1080p. O 1º lote (189 imagens, **US$ 4,83 = R$ 28**) foi descartado. Use `{width: 1536, height: 864}` (`canal.yaml` do historia-ptbr).
- O preço é **por megapixel** (US$ 0,025/MP): 1536×864 ≈ US$ 0,033/img. O `img_fal.py` registra US$ 0,025 fixo por imagem, então lance o ajuste (id 38).
- O filtro de segurança devolve **imagem preta sem erro** (2 mapas inofensivos do Oriente Médio). Confira a luminância média de cada imagem (< 15 = refazer com outro texto).
- O flux escreve **letras falsas em mapas** mesmo com "no text, no labels". Mapas: reuse um mapa limpo e ponha os rótulos no código, ou use outra fonte.
- "barrel-shaped clay cylinder" virou barril de madeira (Cilindro de Ciro). Descreva a forma sem a palavra "barrel" ("shaped like a rugby ball").
- O estilo do canal fica menos fiel no flux que no gpt-image-2: aparecem rostos realistas e caricaturas (qizilbash com cara de Papai Noel). **Hipótese:** isso pesa na percepção de qualidade; o Rodrigo é quem julga.

### 4. Saldo zerado no meio da geração (Índia, 2026-11-03, ~19:45)
- A OpenAI respondeu "You have no credits remaining"; faltaram 2 imagens (`charkha`, `journey_lineup`), cobertas com reuso. [BLOQUEIO.md 002]
- O banco não reflete o saldo real: `financas.saldo_pre_pago` mostra a OpenAI com US$ 10,00 recarregados, US$ 19,87 consumidos e **saldo de −US$ 9,87** (2026-11-04). Faltam lançar recargas em `financas.lancamentos` (dado do Rodrigo).
- **Hipótese (atenção ao custo real da Índia):** o ETAPA-FINAL estima o gasto real em ~US$ 7,1, aplicando o fator 0,756 do Egito sobre os US$ 9,43. Mas o custo por imagem registrado na Índia (~US$ 0,042) já é igual ao calibrado do Egito (US$ 8,55 / 204 = US$ 0,042), então o fator pode ter sido aplicado duas vezes. O saldo real era de ~US$ 8,71 depois do Egito (ETAPA3.md 001) e foi a zero com a Índia e as thumbs v2 das cidades (US$ 0,50), o que sugere **~US$ 8,2** para a Índia. Confira no painel da OpenAI.
- Também: o `img_openai.py` só grava o custo no fim; se for interrompido, o custo se perde e precisa ser lançado à mão (aconteceu com 165 imagens do Egito v1, `financas.consumo` id 9). [ETAPA2.md 001; playbooks/produzir-video.md]

### 5. Fidelidade visual (lotr-fr, cidades, 2026-11-01)
- Minas Tirith ilustrada com o **Mont-Saint-Michel** (pintura de Haseltine): "inaceitável, ainda mais para o público francês". [AJUSTES_V2.md lotr-fr 001]
- Na v2, as cidades foram substituídas por "ilustrações originais geradas localmente" (`tools/gen_cities.py`). O QA registrou "composições esquemáticas/estilizadas em vez de pintura a óleo". [out/QA.md lotr-fr 001] O `estilo.md` do canal conclui: "cidades desenhadas por código ficaram amadoras". [estilo.md lotr-fr]
- Anacronismos de bandeira no Egito v1 (bandeira atual em cenas de 1922 e 1952), corrigidos nos prompts da v2. [QA-v1.md, ETAPA3.md 001]
- Estereótipo na Índia: o curandeiro de Mehrgarh (I035) saiu com cocar de penas; ficou pendente de regerar. [QA.md 002]

### 6. Banco e backlog desatualizados (encontrado em 2026-11-04)
- `youtube.videos` id 3 (Egito) ainda tem `youtube_id = s-D5Sk7prJI`, que está indisponível; o vídeo no ar é `g847Td0Plsk`. O id 4 (Índia) está como `status = pronto`, sem `youtube_id`, mas está publicado como `MV5SSjoccqE`. [consulta SQL + oEmbed, 2026-11-04]
- `canais/historia-ptbr/backlog.md` lista só o Egito, com o ID antigo.
- Consequência: `financas.custo_por_video` e os relatórios de métricas não ligam os vídeos novos aos custos.
- **Corrigido em 2026-11-04 (Produtor, vídeo 003):** id 3 → `g847Td0Plsk`, "A história INTEIRA do Egito em 17 minutos", publicado 03/11; id 4 → `MV5SSjoccqE`, `publicado`, 03/11 (título e `upload_date` conferidos com yt-dlp via WARP). `backlog.md` atualizado.

---

## Custos reais por vídeo
Fonte: `financas.custo_por_video` e `financas.consumo` (consulta de 2026-11-04). OpenAI = **estimativa do script** (calibrada pelo saldo no Egito em 02/11 21:40, fator 0,756). O rateio do fixo muda com o mês: hoje é (Hostinger R$ 41,45 + Claude Max R$ 589,17) ÷ 3 vídeos de novembro = R$ 210,21 por vídeo.

| Vídeo | Itens diretos (financas.consumo) | Direto (R$) | Rateio fixo (R$) | Total (R$) |
|---|---|---|---|---|
| Egito (id 3) | v1: Fish US$ 0,20 + 205 imagens `low`/`medium` US$ 1,10; v2: Fish US$ 0,21 + 204 `medium` US$ 8,55 + thumb `high` US$ 0,17 | **59,65** (v1 7,59 + v2 52,06) | 210,21 | 269,86 |
| Índia (id 4) | Fish US$ 0,24; 223 gerações `medium`/`high` US$ 9,43 (27 em dobro); thumbs fal.ai US$ 0,13 | **57,14** | 210,21 | 267,35 |
| Irã (id 5), 2026-11-04 | Fish US$ 0,38 (A/B + vídeo + validação); fal US$ 11,54 (1º lote 1024×576 descartado: US$ 4,83; lote final 1536×864: US$ 6,72); OpenAI sem crédito | **69,77** | 157,66 | 227,42 |
| Cidades lotr-fr (id 2) | 3 thumbs v2 gpt-image-2 US$ 0,50 (voz Kokoro e imagens locais/domínio público, sem custo) | **2,89** | 210,21 | 213,09 |

- Testes de estilo e voz sem `ref_id` (ids 1–5 e 18): ~US$ 0,15 (R$ 0,87), fora do custo por vídeo.
- Os ETAPA*.md citam custos com rateio diferente (R$ 30,39, R$ 80,38, R$ 70,20) porque, na época, o Claude Max ainda não estava lançado. Use sempre a view, com a data.

### 7. Job headless morto por tarefa de fundo (BRIEF-canal-archive, 2026-11-04)
- O job disparou um subagente e um shell em segundo plano, respondeu "ainda está rodando, quando terminar eu faço o resto" e encerrou o turno. Em `claude -p` não há "depois": o harness esperou 10 min ("Background tasks still running 10m after the last turn ... stopping them") e matou tudo; trabalho pela metade, sem commit. [referencias/canal-archive.log]
- Correção: regra em `~/.claude/CLAUDE.md` (primeiro plano, commit+push antes de responder, senão `BLOQUEIO.md`) e `CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0` em `~/.claude/settings.json`, `claude_run.py` e `_rotina_claude.sh`. Atenção: na doc, `0` = esperar indefinidamente (não desliga a espera), então a variável só segura o processo; o `--timeout` do `claude_run.py` continua sendo o limite. Para proibir background de vez existe `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1` (não aplicado; **Hipótese** de que resolveria).

