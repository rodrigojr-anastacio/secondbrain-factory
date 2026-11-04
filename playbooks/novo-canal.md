# Playbook: avaliar e montar um canal novo

Processo padrão da fábrica para transformar um achado (garimpo, ideia do Rodrigo, canal de referência) em **decisão com número** e, se não for DESCARTAR, em **canal pronto para o piloto**. Feito pela primeira vez em 2026-11-04 com o nicho "Archive in Minutes" → `dossie-es` (`pesquisa/archive-in-minutes/LEVANTAMENTO.md` e `IDIOMA.md`, que servem de **exemplo completo** de cada etapa; o canal saiu primeiro como `dossie-ptbr` e mudou para es depois da matriz de idioma).
Skill: `skills/novo-canal/SKILL.md`. Papéis: **Tendências** faz as etapas 1–3b (subagente `tendencias`); o orquestrador ou **Produtor** faz as etapas 4–6. Modelo: Opus no levantamento e no roteiro do piloto.

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

## Etapa 3: escolha de idioma (regra permanente do Rodrigo, 2026-11-04)
O idioma **não** é pt-BR por padrão. A **ordem de preferência é en → es → pt → fr → de** (depois it, pl etc.), porque os mercados que pagam melhor vêm primeiro. O pt-BR paga menos e só ganha se a demanda ou a falta de concorrência compensarem. Exemplo completo: `pesquisa/archive-in-minutes/IDIOMA.md`, onde o nicho "Dossiê" saiu em es, e não em pt.
1. **Cubra pelo menos en, es, pt, fr e de**, mais 3–4 buscas exploratórias em ru, hi, ar, pl, it, tr e ja, para ver se algum mercado fora da lista tem demanda grande e vaga. Use busca sem cota (yt-dlp via WARP; scripts reutilizáveis em `pesquisa/archive-in-minutes/idioma/scripts/`), com os temas escritos **nativamente** e a fórmula traduzida. Em cada idioma, levante:
   - **demanda:** mediana de views do top-10 por tema, vídeos do ano acima de 100 mil e **prova do formato no idioma** (algum canal do molde com tração);
   - **concorrência:** canais no molde, clones recentes, mediana deles, dono forte;
   - **RPM:** faixa do nicho × fator do idioma, cruzada com o país dos canais de demanda;
   - **alcance:** países do idioma;
   - **risco:** anúncio limitado, risco legal (ex.: §86a na Alemanha) e político;
   - **viabilidade:** voz nativa no Fish (liste com `idioma/scripts/fish_vozes.py` e gere uma amostra curta de 3–7 vozes, ≤ US$ 0,50, conferida com Whisper), imagens e **revisão** (o Rodrigo lê o idioma?).
2. **Matriz com pesos padrão:** demanda **30%**, concorrência **25%**, RPM **20%**, viabilidade **15%**, risco **10%**. Notas de 0 a 10, escritas com o critério de cada uma.
   - **Travas** que eliminam o idioma, seja qual for a soma: concorrência ≤ 2 (molde com dono e clones mortos: "não ser o 16º clone") **ou** RPM ≤ 1 (mercado sem receita, ex.: ru).
   - **Desempate** (diferença < 0,3): a ordem en → es → pt → fr → de, depois a prova do formato no idioma.
   - Faça a **sensibilidade**: pesos iguais e RPM 30%/demanda 20%. Diga se o vencedor muda.
3. **Recomende 1 idioma e o 2º**, explicando por que o en ganha ou perde. Ele é o 1º da ordem: se perder, diga qual trava ou nota o derrubou.
4. A ordem dos temas **não se transfere** entre idiomas: refaça o ranking com a demanda do idioma escolhido (ex.: Stasi e MI6 fortes em en, fracos em es e pt).
5. As imagens não têm idioma (o texto vai no código): pense no 2º idioma como **versão** do mesmo conteúdo (reescrita nativa + voz), não como canal do zero.
6. Escreva `pesquisa/<slug>/IDIOMA.md` (executivo no topo, [O] × [I]) ou a seção "Idioma" do LEVANTAMENTO.

## Etapa 3b: oportunidade e decisão
1. **Idioma:** use o resultado da etapa 3 (matriz e recomendação). O slug do canal leva o idioma (`<nicho>-<idioma>`, ex.: `dossie-es`).
2. **Projeção em faixa:** receita da referência; a nossa em 10–20% das views; views necessárias para o YPP (4.000 h); os 2 primeiros meses realistas (geralmente sem receita).
3. **Custo e viabilidade** na nossa pipeline (base real em `conhecimento/anti-padroes.md`).
4. **Diferenciação:** ângulo Brasil/lusófono, assinatura visual própria, fontes na descrição, cadência humana.
5. **Riscos** (tabela risco × política × mitigação): conteúdo violento ou extremista (EDSA, adequação para anunciantes), **conteúdo inautêntico/produzido em massa** (YPP), conteúdo sintético (rótulo), direitos (Content ID), pessoas reais, canibalização de canal nosso, clones.
6. **Recomendação:** INVESTIR / TESTAR / DESCARTAR, com idioma, 20 temas ranqueados com evidência e **critério numérico** para mudar de TESTAR para INVESTIR ou DESCARTAR (ex.: 3 vídeos; média ≥ 3 mil views em 14 dias ou 1 vídeo ≥ 15 mil, com % assistido ≥ 35%).
7. Grave fórmula e decisão em `youtube.garimpo_canais` (`formula`, `decisao`, `notas`).
8. Escreva `pesquisa/<slug>/LEVANTAMENTO.md`: **resumo executivo no topo** (recomendação, números-chave, próximos passos), seções 1–3, limitações e "Sugestões" (para a bíblia do canal novo e, se for geral, para `conhecimento/`).

## Etapa 4: blueprint do canal (se não for DESCARTAR)
1. **Banco:** `INSERT INTO youtube.canais (slug, nome, idioma, nicho, status) VALUES (…, 'em preparação')` e a linha do piloto em `youtube.videos` (status `roteiro`). Isso dá o id para o custo dos testes.
2. `canais/<slug>/canal.yaml`: fórmula (título, duração, palavras, estrutura), cadência, voz sugerida (**diferente** das dos outros canais), visual (`gerador`, `modelo`, `tamanho`, `estilo_prompt` com "no text… no extremist insignia" quando couber, cores).
3. **`canais/<slug>/biblia/` completa** (a "caixinha" do canal; modelo: `canais/dossie-es/biblia/`), no idioma de trabalho da fábrica (pt-BR) com exemplos no idioma do canal:
   - `README.md` (~10 linhas): canal-modelo, o que é **deste** canal e **"o que NÃO fazer aqui"**, citando o que é de **cada** canal existente (para nenhum agente misturar);
   - `roteiro.md`: estrutura, hook, transições entre capítulos, fecho, tamanho (palavras × duração com a voz escolhida) e tom, com exemplos **literais** das transcrições da referência ([O]) e checklist final;
   - `titulo.md` (fórmula, título B, temas que performam × flopam), `thumb.md` (template e o que não copiar), `visual.md` (motor de imagem, `estilo_prompt`, ritmo, texto na tela, políticas) e `voz.md` (voz, tom, pronúncia).
   - `estilo.md` fica só como índice apontando para a bíblia. Deixe explícito o que **não** copiar da referência.
   - Se o canal novo tiver risco de mistura com um existente (mesmo nicho, mesma fórmula), acrescente uma linha no "o que NÃO fazer aqui" da bíblia do canal existente.
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
3. Aprendizados do formato estudado vão para a **bíblia do canal novo** (com data e fonte); só o que vale para qualquer canal (ferramenta, custo, processo) vai para `conhecimento/`. Se outro job estiver mexendo lá, deixe-os na seção "Sugestões" do LEVANTAMENTO.

## Depois do OK
O piloto segue `playbooks/produzir-video.md` (skill `produzir-video`) com o id já criado. Após 3 vídeos e 14 dias, o **Métricas** aplica o critério da etapa 3b e o resultado volta para o `LEVANTAMENTO.md` e para `youtube.garimpo_canais.decisao`.
