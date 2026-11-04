# Playbook: avaliar e montar um canal novo

Processo padrão da fábrica para transformar um achado (garimpo, ideia do Rodrigo, canal de referência) em **decisão com número** e, se não for DESCARTAR, em **canal pronto para o piloto**. Feito pela primeira vez em 2026-11-04 com o nicho "Archive in Minutes" → `dossie-ptbr` (`pesquisa/archive-in-minutes/LEVANTAMENTO.md`, que serve de **exemplo completo** de cada etapa).
Skill: `skills/novo-canal/SKILL.md`. Papéis: **Tendências** faz as etapas 1–3 (subagente `tendencias`); o orquestrador ou **Produtor** faz as etapas 4–6. Modelo: Opus no levantamento e no roteiro do piloto.

**Decisões do Rodrigo (nunca do agente):** criar o canal no YouTube, o nome, a voz, gastar acima do teto, produzir e publicar o piloto.

## Entradas e orçamento
- Canal(is) de referência (link + por que interessa) e o slug de pesquisa (`pesquisa/<slug>/`).
- **Cota do YouTube:** até ~15 `search.list` (1.500 unidades) + chamadas baratas (`channels`, `playlistItems`, `videos`: 1 unidade cada). Não rode o `trends.py` completo para isso.
- **Dinheiro:** até **US$ 3** em imagens de teste, registradas com `--video <id do piloto>`. Voz e vídeo completo, não.
- **Execução headless (`claude -p`):** subagentes e comandos **em primeiro plano**. O modo `-p` mata as tarefas de fundo quando o turno acaba (aconteceu em 2026-11-04: o levantamento parou no meio e teve de ser retomado). Salve os dados brutos cedo (`dados.json`) para poder retomar.

## Etapa 1: mapa de concorrência (`pesquisa/<slug>/dados.json`)
1. Puxe **a lista completa de vídeos** do canal de referência (`channels.list` → `uploads` → `playlistItems` → `videos`): título, data, views, likes, comentários, duração, `licensedContent`.
2. Faça **buscas por tema × idioma**: os 3–5 temas mais fortes da referência em en, mais 1–2 buscas em pt, es, fr e de (`relevanceLanguage`) e 1 busca pela **fórmula do título traduzida** ("a história INTEIRA … em minutos").
3. Para cada canal que aparecer e for do formato ou do nicho, colete: link, 1º vídeo (idade), nº de vídeos, views, inscritos, **views/mês** (canal com < 1 ano: views ÷ idade × 30; canal antigo: views dos longos dos últimos 90 dias ÷ 3), ritmo de postagem, melhor vídeo, **mediana** de views e sinal de monetização (inscritos ≥ 1.000, horas estimadas, `licensedContent`, anúncios na página: só indícios).
4. Separe em 3 tabelas: **(a) fórmula exata, canais novos**; **(b) clones** do canal de referência (canais que copiaram título e thumb depois dele); **(c) mesmo nicho com outro formato**, que dá o teto do nicho.
5. **Conte os clones e a mediana deles.** Muitos clones com mediana < 1 mil = o idioma saturou: não entre nele com a mesma fórmula ("não ser o 16º clone").

## Etapa 2: anatomia do formato (≥ 6 vídeos de ≥ 3 canais)
1. `tools/watch.py <ID>` (via WARP) em hits **e** em flops do mesmo canal; pelo menos 1 clone fraco e 1 vídeo em outro idioma.
2. Abra `thumb.jpg`, `hook_sheet.jpg` e `video_sheet.jpg` com a ferramenta Read (visão). Monte um **mosaico das thumbs** do canal de referência (ffmpeg `xstack`) e salve exemplos em `pesquisa/<slug>/thumbs/<canal>-<id>.jpg` (fora do git).
3. Registre, separando **[O] observado** de **[I] inferido**:
   - **Títulos:** molde, palavras, N; **temas que performam × flopam** (mediana por grupo de tema). O tema costuma pesar mais que o hook.
   - **Thumbs:** composição, cores, tipografia, elementos fixos, o que **não** aparece (ex.: suástica).
   - **Hook:** os primeiros 20–30 s **literais** e a técnica.
   - **Roteiro:** capítulos, ordem, loops, fechamento, palavras por minuto.
   - **Edição:** estilo, cortes/min (`info.json`), texto na tela, mapas, voz e trilha.
   - **Cadência** e a explicação do crescimento.

## Etapa 3: oportunidade e decisão
1. **Idioma:** tabela en × pt-BR × es × fr × de com saturação (etapa 1), RPM (tabela de `playbooks/garimpo-tendencias.md` × fator do idioma) e leitura. Prefira o mercado grande **sem** a fórmula em que a fábrica já opera.
2. **Projeção em faixa:** receita da referência; a nossa em 10–20% das views; views necessárias para o YPP (4.000 h); os 2 primeiros meses realistas (geralmente sem receita).
3. **Custo e viabilidade** na nossa pipeline (base real em `conhecimento/anti-padroes.md`).
4. **Diferenciação:** ângulo Brasil/lusófono, assinatura visual própria, fontes na descrição, cadência humana.
5. **Riscos** (tabela risco × política × mitigação): conteúdo violento ou extremista (EDSA, adequação para anunciantes), **conteúdo inautêntico/produzido em massa** (YPP), conteúdo sintético (rótulo), direitos (Content ID), pessoas reais, canibalização de canal nosso, clones.
6. **Recomendação:** INVESTIR / TESTAR / DESCARTAR, com idioma, 20 temas ranqueados com evidência e **critério numérico** para mudar de TESTAR para INVESTIR ou DESCARTAR (ex.: 3 vídeos; média ≥ 3 mil views em 14 dias ou 1 vídeo ≥ 15 mil, com % assistido ≥ 35%).
7. Grave fórmula e decisão em `youtube.garimpo_canais` (`formula`, `decisao`, `notas`).
8. Escreva `pesquisa/<slug>/LEVANTAMENTO.md`: **resumo executivo no topo** (recomendação, números-chave, próximos passos), seções 1–3, limitações e "Sugestões para `conhecimento/`".

## Etapa 4: blueprint do canal (se não for DESCARTAR)
1. **Banco:** `INSERT INTO youtube.canais (slug, nome, idioma, nicho, status) VALUES (…, 'em preparação')` e a linha do piloto em `youtube.videos` (status `roteiro`). Isso dá o id para o custo dos testes.
2. `canais/<slug>/canal.yaml`: fórmula (título, duração, palavras, estrutura), cadência, voz sugerida (**diferente** das dos outros canais), visual (`gerador`, `modelo`, `tamanho`, `estilo_prompt` com "no text… no extremist insignia" quando couber, cores).
3. `canais/<slug>/estilo.md`: fórmula, roteiro (molde de hook, capítulos, tom), visual, texto na tela, thumb, voz e políticas. Deixe explícito o que **não** copiar da referência.
4. `canais/<slug>/backlog.md`: 20 temas ranqueados com evidência (views em concorrentes; sem dado = **Hipótese**) e a lista do que evitar (flops).
5. `canais/<slug>/identidade.md`: 3 nomes com **handle conferido** (`channels.list forHandle=@handle`, 1 unidade: sem item = livre), descrição do canal, conceito de avatar e de banner, paleta e tipos.
6. Piloto em `canais/<slug>/videos/001-<tema>/`: `BRIEF.md` (referência com hook real, teto de custo, saldos, pendências), `SCRIPT.md` (roteiro completo, com hook próprio, **não** a anedota da referência), `SOURCES.md` (fonte por fato) e `THUMBS.md` (3 conceitos para o "Testar e comparar").

## Etapa 5: teste de estilo (≤ US$ 3)
1. Confira o saldo: `SELECT * FROM financas.saldo_pre_pago`. **O banco pode mentir:** em 2026-11-04 a OpenAI aparecia com −US$ 9,87 e a API respondeu "no credits remaining". Uma chamada que falha por crédito não custa nada.
2. `canais/<slug>/testes/cenas-estilo.json` com 5 cenas do piloto: 1 cena de rua com pessoas, 1 prédio ou lugar real, **1 mapa**, 1 interior com personagem e **1 base de thumb** (metade livre para texto). Use `seed` fixo.
3. Rode o mesmo estilo em 3–4 modelos, **um processo por pasta e em primeiro plano**:
   `tools/.venv/bin/python tools/img_fal.py <slug> canais/<slug>/testes/cenas-estilo.json canais/<slug>/testes/estilo-<modelo> --video <id> --modelo <modelo>`
4. Monte uma grade (ffmpeg `xstack`), avalie com visão (traço, época, rostos, texto inventado, mapa limpo) e confira a **resolução** (`ffprobe`; abaixo de ~1300 px de largura vira borrão no Ken Burns).
5. Escreva `canais/<slug>/testes/ESTILO.md` (modelo × custo × saída × avaliação × decisão) e grave o modelo escolhido no `canal.yaml`.
   - Aprendido em 2026-11-04: `fal-ai/nano-banana` só sai em 16:9 com `aspect_ratio` (o `img_fal.py` já manda); `fal-ai/imagen4/preview/fast` deu 404; o flux-pro saiu em 1024×576.

## Etapa 6: entrega e commit
1. Resposta curta ao Rodrigo: recomendação, nº de canais mapeados, idioma, 3 nomes, tema do piloto, custo gasto, caminho do relatório e **as decisões dele** (nome/criação do canal, voz, OK do piloto).
2. `git add` **só os seus caminhos** (`pesquisa/<slug>/`, `canais/<slug>/`, playbook/skill), conferindo `git status` (sem mídia nem segredo). Se outro job estiver no repo e der `index.lock`, espere e tente de novo. Commit descritivo e push.
3. Aprendizados de formato vão para `conhecimento/` com data e fonte. Se outro job estiver mexendo lá, deixe-os na seção "Sugestões para `conhecimento/`" do LEVANTAMENTO.

## Depois do OK
O piloto segue `playbooks/produzir-video.md` (skill `produzir-video`) com o id já criado. Após 3 vídeos e 14 dias, o **Métricas** aplica o critério da etapa 3 e o resultado volta para o `LEVANTAMENTO.md` e para `youtube.garimpo_canais.decisao`.
