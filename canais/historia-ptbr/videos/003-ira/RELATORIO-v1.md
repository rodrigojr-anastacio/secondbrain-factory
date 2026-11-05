# RELATÓRIO · historia-ptbr/003 · "A história INTEIRA do Irã em 15 minutos" (youtube.videos id 5)

Job: `~/workspace/referencias/BRIEF-historia-003.md` (04/11/2026). Orquestrador: Claude Code (Opus) nesta sessão. Etapas pesadas via `tools/claude_run.sh`. Nada foi publicado nem enviado ao Telegram.

## Entrega
`canais/historia-ptbr/videos/003-ira/entrega/`:
- `video.mp4`: 15:18, 1080p30, H.264/AAC, −15,1 LUFS;
- `thumb-A.jpg`, `thumb-B.jpg`, `thumb-C.jpg`;
- `pacote.md`, com título, descrição, tags, 18 capítulos e checklist;
- `legendas.srt`;
- `amostras-voz/` (11 tomadas do A/B, 2 da validação no texto real e o `LEIA.md`).

QA aprovado (`QA.md`):
- 0 telas pretas;
- 24 cortes no 1º minuto e 20,2 por minuto em média;
- 143 rótulos de texto na tela;
- Whisper voz × roteiro em 95,4%, sem tags faladas.

## Custo por etapa (financas.consumo, ref_id 5)
| Etapa | Itens | US$ | R$ |
|---|---|---|---|
| A/B de voz (11 tomadas + teste da tool) | Fish | 0,14 | 0,80 |
| Voz do vídeo (102 blocos por frase + 3 frases regeradas) | Fish | 0,18 | 1,08 |
| Validação da voz no texto real (3 × 12 blocos) | Fish | 0,06 | 0,35 |
| Imagens, 1º lote fal 1024×576 (**descartado**: borraria) | fal | 4,83 | 28,23 |
| Imagens, lote final fal 1536×864 (189 + 2 thumbs + 15 refeitas + ajuste de preço/MP) | fal | 6,72 | 39,31 |
| **Total direto** | | **11,92** | **69,77** (teto R$ 80) |
- OpenAI: US$ 0. A conta estava sem crédito, e o 1º teste falhou sem cobrança.
- O custo do fal é estimado: a tool registra US$ 0,025 fixo por imagem, e eu lancei o ajuste por megapixel (id 38). Confira no painel do fal.
- `financas.custo_por_video` (id 5): direto R$ 69,77 + rateio fixo R$ 157,66 = **R$ 227,42**.

## Claude Code (youtube.execucoes_claude; preço de lista, não é cobrança no Max)
| Etapa | Modelo | Duração | Turnos | Tokens out | Cache lido / criado | US$ equivalente |
|---|---|---|---|---|---|---|
| 1 roteiro-storyboard | opus | 19,5 min | 30 | 129.759 | 4,51 mi / 224 mil | 5,29 |
| 2 producao | sonnet | 11,1 min | 32 | 19.193 | 2,00 mi / 85 mil | 0,73 |
| 3 montagem-render | sonnet | 30,8 min | 56 | 23.374 | 4,07 mi / 136 mil | 1,18 |
| **Total das etapas** | | **61 min** | 118 | 172 mil | | **7,20** |

O orquestrador (esta sessão Opus) não passa pelo `claude_run` e, por isso, **não entra** em `execucoes_claude`. Veja a falha 7.

## Tempo por etapa (relógio)
| Etapa | Tempo |
|---|---|
| Leitura, banco, escolha do tema, transcrição de 3 referências e `watch.py` | ~35 min (transcrições em background) |
| A/B de voz (geração + medição + implementação do `--por-frase`) | ~25 min |
| Etapa 1 (roteiro e storyboard) | 19,5 min |
| Etapa 2 (voz por frase ~3 min; 1º lote de imagens no fal ~3 min) | 11 min |
| Correções do orquestrador: regerar em 1536×864 (3,5 min), mapas, cilindro, imagens pretas, rótulos, validação de voz | ~35 min |
| Etapa 3 (build, stills, render de ~20 min, thumbs, pacote, QA) | 31 min |
| **Total** | **≈ 2h40** |

## O que mudou no roteiro (feedback 2 do Rodrigo)
- Estudei a transcrição completa de History in Minutes (Irã) e de Archive in Minutes (Gestapo e KGB). Estão em `ref/`, e a análise foi para o `BRIEF.md` e para `conhecimento/hooks.md` e `roteiros.md`.
- **Hook por anedota:** em Tus, a caravana com o ouro do poeta entra por um portão enquanto o caixão dele sai pelo outro. Vem em seguida a promessa do título, a pergunta e o loop "o que salva o Irã está dentro daquele caixão". O hook total ficou em 32 s, contra 0:49 no Egito e 2:21 na Índia. O desfecho cai em ~11 s, 1 s acima da meta.
- **16 capítulos-objeto**, com o título falado na narração ("O Cilindro.", "O Moinho.", "O Tabaco."…), mais "A Caravana" no fecho. Todos os capítulos abrem com mini-hook e fecham puxando o próximo, sem passar de 90 s.
- **Loops pagos:**
  - caixão → "O Poema" (6:32), com o detalhe que faltava (a carga era anil);
  - "guarde esse nome" → 1935;
  - tabaco → 1979.
- **Fecho circular:** volta a Tus, termina em "caravana", que é palavra persa, mais um aforismo e uma pergunta para os comentários.
- **Texto na tela:** placa de rótulo nova (`NameTag`, sintaxe `@@NOME` no `roteiro.py`) em 46% dos planos. Ritmo de 3,0 s por plano nos 2 primeiros minutos.
- Skills e conhecimento atualizados com data e fonte: `skills/roteiro/SKILL.md`, `conhecimento/roteiros.md`, `hooks.md`, `anti-padroes.md`, `titulos.md` e `estilo.md`.

## O que mudou na voz (feedback 1 do Rodrigo)
- A/B com 11 tomadas do mesmo hook e 6 técnicas, medido com Praat e Whisper (`amostras-voz/LEIA.md`).
  - No A/B, venceu o texto escrito para a fala, gerado frase a frase com 0,32 s de silêncio inserido e tag só na virada: repetição melódica de 0,09, contra 0,14 do jeito do 002.
  - Tags de direção e velocidade 0,97 pioraram o resultado. temperature/top_p não tiveram efeito.
  - Implementei como `tools/tts_fish.py --por-frase`, com cache por frase (regera e cobra só a frase alterada). O custo agora é registrado mesmo se a geração cair no meio.
- **Validação honesta no texto real:** por frase e por parágrafo **empataram**, com repetição de 0,18–0,20 contra 0,17–0,22.
  - O roteiro final, cheio de declarativas curtas, soa mais "caído" que o texto B do A/B. **O que pesa é o texto.**
  - A regra nova para o próximo vídeo é alternar tipos de frase e medir os primeiros 60 s antes de gerar o resto.
  - **Falta o ouvido do Rodrigo:** compare `A-atual.wav`, `G-por-frase+tags.wav` e `V-abertura-final-por-frase.wav`.

## Falhas da esteira (o que quebrou, o improviso, a correção sugerida)
1. **Sem crédito na OpenAI, e a esteira só descobriu na hora de gerar.** `financas.saldo_pre_pago` mostra −US$ 9,87 porque faltam lançamentos de recarga, então o banco não serve para decidir.
   - Improviso: plano B no fal, com estilo menos fiel (alguns rostos realistas, qizilbash com cara de Papai Noel) e thumbs sem `high`.
   - Correção: lançar as recargas e, no início da skill `imagens`, fazer 1 imagem de prova antes de planejar o lote.
2. **`img_fal.py` tem armadilhas que custaram R$ 28.**
   - O `landscape_16_9` sai em 1024×576, o que borra no Ken Burns em 1080p. O 1º lote inteiro foi descartado.
   - O preço fica fixo em US$ 0,025 por imagem, mas o flux/dev cobra por megapixel.
   - O filtro de segurança devolve **imagem preta sem erro** (I104 e I130, mapas inofensivos).
   - O flux escreve letras falsas nos mapas mesmo com "no text".
   - Correção (não mexi na tool, porque outro job a está editando):
     - exigir resolução mínima de 1536 px de largura;
     - calcular o custo por MP;
     - tratar `has_nsfw_concepts`/imagem preta como falha;
     - fazer o QA automático de média de luminância < 15 = falha.
   - Para mapas: gerar por código a partir de um SVG de domínio público ou usar a OpenAI.
3. **Código do vídeo copiado tinha suposições quebradas.**
   - O `Video.jsx` supunha imagens em 3:2.
   - O `build.py` quebrava na trilha (laço do dedilhado passando do fim; corrigido com `break`).
   - O rótulo novo colidia com a placa de capítulo.
   - Correção: tirar `build.py` e `Video.jsx` do "copie do vídeo anterior" e transformá-los num template versionado do canal (`canais/historia-ptbr/template/`), com teste de stills.
4. **O QA de voz por bloco dá falso alarme.**
   - O Whisper escreve números em algarismos e erra nomes persas. Na etapa 2, 58 de 102 blocos ficaram "reprovados" antes de corrigir a normalização, e 33 continuaram abaixo de 93% só por causa de nomes.
   - Correção: levar o `norm()` com números por extenso para o `compara_voz.py` da esteira e criar um glossário de nomes próprios por vídeo.
5. **Não existe medida objetiva confiável de "robótico".**
   - A repetição melódica separou bem no A/B, mas empatou no texto real e varia ±0,02–0,05 entre tomadas.
   - Correção: tratar a métrica como triagem e decidir de ouvido, com 2 amostras curtas mandadas ao Rodrigo antes do vídeo inteiro. Se não melhorar, regravar a referência do clone (30–60 s naturais).
6. **O contador de cortes do `qa.sh` não vê reenquadramentos:** marca 15 cortes no 1º minuto, contra 24 na timeline. Correção: contar pela `timeline.json`.
7. **Parte do custo de Claude fica invisível.**
   - O orquestrador e as correções feitas fora do `claude_run` não entram em `execucoes_claude`.
   - O `watch.py` grava em `pesquisa/tendencias/assets/`, que é o espaço do outro job.
   - Os `.prompt-*.md`, `cenas-teste.json` e `blocos-hook.json` ficam soltos na pasta.
   - Correção: orquestrador também via `claude_run` (etapa `orquestracao`); `watch.py --saida <pasta do vídeo>/ref`; `.gitignore` para os arquivos temporários de etapa.
8. **Banco desatualizado** (Egito com ID antigo, Índia sem `publicado`).
   - Corrigido de passagem: id 3 → `g847Td0Plsk`, "INTEIRA"; id 4 → `MV5SSjoccqE`, publicado em 03/11.
   - Correção: a skill `pacote-youtube` deve deixar pronto o `UPDATE` que o Rodrigo roda (ou que o Métricas aplica) ao publicar.

## Pendências para o Rodrigo
- Ouvir a voz (A × G × final) e dizer se ainda soa robótica.
- Recarregar a OpenAI e lançar a recarga em `financas.lancamentos`, se quiser o estilo gpt-image-2 e as thumbs em `high` (refazer as thumbs custa ~US$ 0,7).
- Na véspera de publicar, reconfirmar a frase "até a gravação deste vídeo, não há acordo de paz" (bloco do capítulo "O Filho").
- Publicar é decisão sua. O checklist está no `pacote.md`: pt-BR, conteúdo sintético = sim, não é para crianças, 3 thumbs no "Testar e comparar".
