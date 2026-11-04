# RELATÓRIO · dossie-es/001 · "TODA la historia de la CIA en 12 minutos" (youtube.videos id 7)

Job: `~/workspace/referencias/BRIEF-dossie-001.md` (04/11/2026, 18:39–19:35). Orquestrador: Claude Code (Opus) nesta sessão, que escreveu o roteiro e o storyboard (etapa de Opus). Uma revisão nativa do espanhol foi feita por um subagente Sonnet. Voz, imagens, build e render são comandos determinísticos, rodados em primeiro plano. Nada foi publicado nem enviado ao Telegram. Nada foi tocado em `canais/historia-ptbr/`.

## Entrega (`entrega/`)
- `video.mp4`: **11:46**, 1080p30, H.264/AAC, −15,2 LUFS;
- `thumb-A.jpg` (El Agente), `thumb-B.jpg` (La Radio) e `thumb-C.jpg` (América Latina);
- `pacote.md`: título, título B, descrição com fontes, 15 capítulos, tags, checklist e tradução pt-BR;
- `legendas.srt` (es).

QA aprovado (`QA.md`):
- 0 telas pretas;
- 23 cortes no 1º minuto e 20,1 por minuto em média;
- 56 rótulos, 14 fichas de lugar e data, 14 cartões de expediente e 5 mapas com pinos no código;
- Whisper voz × roteiro em 97,8%;
- 171/171 imagens.

## Custo por etapa (financas.consumo, ref_id 7)
| Etapa | Itens | US$ |
|---|---|---|
| Testes anteriores (voz es + estilo, antes deste job) | Fish 0,042 + fal 0,384 | 0,43 |
| Amostra de pronúncia (6 blocos) | Fish | 0,01 |
| Voz completa (78 blocos por frase) | Fish | 0,14 |
| Prova de imagem (1, com moldura, descartada) | fal | 0,04 |
| Lote (167) + 4 refeitas pelo filtro + 2 mapas refeitos | fal nano-banana | 6,75 |
| **Total direto** | | **7,36 (R$ ~43)**, teto de US$ 9 |
- O fal não cobrou as 4 recusas do filtro (HTTP 422). O custo vem do preço fixo da tool (US$ 0,039/imagem). Confira no painel do fal.
- `financas.custo_por_video` ainda não traz a linha do id 7 (a view parece só listar vídeos publicados ou com rateio do mês); o total acima saiu de `financas.consumo`.
- Saldo fal estimado depois do job: **US$ 5,37** (não cobre outro vídeo do mesmo tamanho: recarregar antes do 002) (`financas.saldo_pre_pago`).

## Claude Code (tokens e tempo)
- Orquestrador (esta sessão, Opus): **não registrado** em `youtube.execucoes_claude`, porque não roda via `claude_run` (falha 6 abaixo). Fiz roteiro, storyboard, Remotion e relatórios aqui para não repassar contexto entre três execuções; o custo de lista não fica visível.
- Subagente Sonnet (revisão nativa): 45 mil tokens, 27 s.

## Tempo (relógio)
| Etapa | Tempo |
|---|---|
| Leitura (brief, mapa, conhecimento, canal, 003) | ~8 min |
| Checagem de fatos (12 buscas) | ~4 min |
| `roteiro.py` (texto final + 168 planos) + revisão nativa | ~12 min |
| Voz (amostra + 78 blocos) + QA Whisper | ~6 min (Whisper em paralelo às imagens) |
| Imagens (lote de 171, filtro, molduras, mapas, revisão visual) | ~14 min |
| Remotion (identidade nova, thumb, trilha/SFX) + stills | ~12 min |
| Render em 4 partes + junção | ~18 min |
| QA, pacote e relatório | ~8 min |
| **Total** | **≈ 1h20** |

## Correções de fatos (antes da voz; detalhes em `SOURCES.md`, "Checagem de 04/11")
1. A OSS é de **junho de 1942**. Em 1941, Roosevelt encarregou Donovan, que dirigia o COI.
2. O xá ficou no poder "hasta 1979", não "veintiséis años" (~25,4).
3. O golpe no Irã: os EUA "tardan casi medio siglo en reconocerlo" (Albright, 2000) e a CIA admite por documento em 2013. O texto antigo dizia "durante décadas no lo admite".
4. Frank Olson era **bacteriologista civil** a serviço do Exército. O texto agora diz que a família nunca aceitou a versão de suicídio.
5. MKUltra: "miles de documentos" sobrevivem. As fontes divergem sobre os "veinte mil".
6. "Joias da família": **~700 páginas** (702), não 693.
7. Hinchey (2000): "no instigó" o golpe. O texto antigo dizia "no dirigió".
8. U-2: o míssil derruba o **avião** de Powers, não o piloto.

## Revisão do espanhol
Um subagente Sonnet leu como editor mexicano e depois espanhol e deu nota 8/10. Apliquei 20 mudanças: calcos do inglês ("sostenidas" → "respaldadas", "pareció aprobarlo" → "dio la impresión de aprobarlo"), regionalismo ("lleva adelante" → "impulsa"), "invencible" → "imparable", "cae desde" → "cae por", "toma una copa" → "bebe una copa" e vírgulas antes de "y". Todos os números estão por extenso.

## Falhas da esteira (o que quebrou, o improviso, a correção sugerida)
1. **O nano-banana desenha moldura de papel em ~25% das imagens** (43 de 171), e nem a prova nem o teste de estilo de 6 imagens mostravam isso.
   - Improviso: `tools/checa_imagens.py` (detecta tela preta e moldura) + `tools/recorta_moldura.py` (recorta o miolo e reenquadra), sem custo. Perde 6–20% da borda e um pouco de resolução.
   - Correção: levar os dois scripts para `tools/` da fábrica e chamá-los dentro do `img_fal.py` (QA logo depois de cada imagem). Testar, no 002, tirar "subtle paper grain texture" do `estilo_prompt` (**Hipótese**: é essa frase que puxa a moldura).
2. **O filtro do fal recusa cenas históricas comuns** (HTTP 422: tanques, míssil, helicóptero atingido, Torres Gêmeas).
   - O `img_fal.py` só mostra "422" e segue. Reescrevi os 4 prompts à mão; o 11-S virou o memorial de luz.
   - Correção: a skill `storyboard` deve escrever violência "de longe e sem impacto" desde o início, e o `img_fal.py` deve registrar o motivo (corpo da resposta).
3. **Os mapas continuam com letras falsas e enquadramento errado**, mesmo com "completely blank".
   - O 1º mapa das Américas cortou o Chile, e o do Irã inventou o nome do mar duas vezes ("CASPARIN SEA", "ACSPRIN SEA"). Custou 2 regerações e um rótulo posto **por cima** do texto falso.
   - Correção: mapa-base de domínio público (Natural Earth) desenhado em SVG no código, igual para todos os vídeos do canal. Isso elimina pinos errados, texto falso e regeração.
4. **Render longo × comando de 10 min:** a regra headless proíbe background e o Bash em primeiro plano tem teto de 10 min.
   - Resolvido com `tools/render.sh parte` (blocos de 6.000 frames, ~5 min cada, sem áudio) + `juntar` (concat com `-c copy` + mix AAC).
   - Correção: adotar esse `render.sh` como padrão da skill `montagem-render`.
5. **Código do vídeo ainda é "copie do anterior".** `Video.jsx`, `Thumbnail.jsx`, `build.py` (trilha) e `qa_voz_blocos.py` (números em espanhol) foram reescritos para a identidade nova.
   - Correção: `canais/dossie-es/template/` a partir desta pasta, como já sugerido no 003 para o historia-ptbr.
6. **Custo de Claude do orquestrador invisível** (mesma falha 7 do 003). Correção: etapa `orquestracao` no `claude_run` ou registro manual ao fim do job.
7. **QA de voz sem glossário:** 12 blocos ficaram "reprovados" só por grafia de nomes (Mosaddeq, Dulles, Gottlieb, CIA = "sía"). Correção: glossário por vídeo no `qa_voz_blocos.py` (lista de equivalências) para o critério ser automático.

## Pendências para o Rodrigo
- **Ouvir** o bloco N022 ("un agente de la CIA reparte dinero en Teherán", ~3:20). O Whisper ouviu "una gente entera": pode ser só transcrição, mas vale 10 s de ouvido.
- Renomear o canal para **Dossier en Minutos** / `@dossierenminutos` antes de publicar.
- Publicar é decisão sua; o checklist está no `pacote.md` (es, sintético = sim, não é para crianças, 3 thumbs no "Probar y comparar", legenda es).
- Há um `AVISO-IMAGENS.md` (18:45, "estilo aprovado, pode gerar o lote") que não foi escrito por este job. Deixei-o como está, fora do commit.
