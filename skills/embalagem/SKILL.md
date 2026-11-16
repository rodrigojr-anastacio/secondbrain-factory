---
name: embalagem
description: Use em todo vídeo NOVO da fábrica do YouTube logo depois da pesquisa-referencia e ANTES do roteiro - pesquisa real no YouTube (top vídeos do tema em ~12 meses, padrões de título e thumb, colisões com clones, mosaico das thumbs), propõe 3 pares título+thumb (T1/T2/T3 e Thumb A/B/C: 3 padrões de título e 3 padrões VISUAIS de thumb diferentes, cada um com evidência) + a promessa que o roteiro tem de pagar, grava EMBALAGEM.md e passa pelo crivo independente (CRIVO.md, até 3 rodadas; reprovado = BLOQUEIO.md). Decisão do Rodrigo de 14/11/2026; 3 conceitos de thumb diferentes desde 16/11/2026.
---

# embalagem: tema + BRIEF.md → EMBALAGEM.md (+ crivo → CRIVO.md)

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`. Python: `tools/.venv/bin/python`.
Modelo: **opus** (etapa 1 do lote). O crivo roda num **Task separado** (revisor independente): instruções em [`CRIVO.md`](CRIVO.md).

**Por que existe (Rodrigo, 14/11/2026):** a aula de métricas que ele segue diz que "retenção alta + CTR baixo + poucas views = o vídeo é bom, a embalagem errou". Na reembalagem dos 15 vídeos publicados (`pesquisa/reembalagem-2026-11-14/`) o crivo reprovou 19 de 45 elementos na 1ª rodada: título e thumb pensados **depois** do vídeo saíram fracos. Agora a ordem se inverte: **ideia → título → thumb → (crivo) → roteiro → hook → storyboard → voz → imagens → render.**
- **Portão = só o crivo** (agente separado, régua alta). O Rodrigo **não** aprova cada embalagem.
- **3 thumbs realmente diferentes (Rodrigo, 16/11/2026):** antes saía 1 conceito e o "Testar e comparar" recebia 3 variações quase iguais (Em Relevo seca 1877: as 3 eram mapa escuro + número/ano), e o teste não ensinava nada. Agora cada vídeo leva **3 conceitos de padrões visuais diferentes**, pareados a 3 títulos de padrões diferentes, e o resultado do teste vai para `youtube.embalagem_variantes` → o placar `youtube.padrao_thumb_placar` mostra **qual padrão ganha o clique em cada canal**.
- Vale para todo vídeo **novo** a partir de 14/11/2026, em todos os canais. Não se aplica a vídeos feitos, agendados ou com etapa 1 já concluída.
- Padrão-ouro de método e régua: `~/workspace/referencias/BRIEF-reembalagem-titulo-thumb.md`, `pesquisa/reembalagem-2026-11-14/padroes.md` (padrões medidos por canal + "o que NÃO funciona") e `PROPOSTAS.md` (lições por canal, seção b).

## Entrada
- Tema + `$V/BRIEF.md` (saída da `pesquisa-referencia`: referência, fontes, duração-alvo, teto).
- Sem `BRIEF.md`, não comece.

## Antes de agir
0. **Bíblia do canal primeiro:** `canais/<slug>/biblia/README.md` (o que NÃO fazer aqui), `titulo.md` e `thumb.md` (fórmula, template, padrões medidos, Hipóteses da reembalagem). Em Relevo: `pesquisa/canal-clima-2026-11/biblia-titulo.md` (até ganhar `canais/<slug>/`). A bíblia **prevalece**; desvio só explícito ("**desvio da bíblia:** … porque …") e com evidência.
1. Regras gerais: `conhecimento/titulos.md`, `conhecimento/thumbnails/README.md`, `conhecimento/politicas-youtube.md`, `conhecimento/decisao-do-clique.md`.
2. Padrões já medidos: `pesquisa/reembalagem-2026-11-14/padroes.md` (seção do canal), `pesquisa/benchmark-2026-11-14/RELATORIO.md`, `pesquisa/gap-2026-11-14/RELATORIO.md` (gap 2 = embalagem igual à dos clones). **Reaproveite** antes de buscar de novo; padrão já medido só precisa ser reconferido (views de hoje).
3. As thumbs no ar do **mesmo canal** (`conhecimento/thumbnails/<slug>-*.jpg` e `canais/<slug>/videos/*/reembalagem-2026-11-14/thumb-nova.jpg`) para a nova não ficar igual às vizinhas na grade.

## Passos
1. **Pesquisa no YouTube (custo zero, idioma do canal; inglês de apoio se o tema for global).** Ids dos **nossos** vídeos (para `--nossos`): `psql -d vida -Atc "select string_agg(youtube_id, ',') from youtube.videos where canal_slug='<slug>' and youtube_id is not null"` (o script não confere o canal: não passe id de concorrente). `--ids` só aceita vídeos que já estão no `refs.csv`: para pôr uma referência de fora no mosaico, rode antes um `buscar` com o título dela. Script: `skills/embalagem/scripts/pesquisa_embalagem.py` (saída em `$V/embalagem/`):
   ```bash
   P=~/workspace/fabrica-youtube/tools/.venv/bin/python; S=~/workspace/fabrica-youtube/skills/embalagem/scripts/pesquisa_embalagem.py
   $P $S buscar $V/embalagem --idioma <es|pt|en|fr> "<termo 1>" "<termo 2>" ...   # 4–8 termos: nome do tema, sinônimos, ângulo do BRIEF, "historia/história de X"
   $P $S enriquecer $V/embalagem --dias 400       # videos.list + channels.list + mediana real (últimos ≤ 30 longos) → refs.csv
   $P $S thumbs $V/embalagem --top 9 --nossos <id1,id2>   # thumbs via WARP + mosaico.jpg (≤ 1 MB) + mosaico-320.jpg
   $P $S thumbs $V/embalagem --ids <id,id,...> --nome mosaico-<idioma>   # mosaico curado: o top por views traz filmes/podcasts (Templarios: 2 filmes do Nicolas Cage); refaça só com vídeos do nicho
   ```
   - yt-dlp e download de thumb **só via `socks5://127.0.0.1:40000`** (o script já usa). Data API só `videos.list`/`channels.list`/`playlistItems` (1 unidade). `search.list` (100 unidades) no máx. **2 por vídeo** e só se o yt-dlp falhar. Anote a cota gasta no `EMBALAGEM.md`.
   - Janela ~12 meses (≤ 400 d). "Acima da mediana" = views > mediana real do canal da referência (o script calcula; medianas de olho erraram na reembalagem r1).
   - **Olhe as thumbs com Read** (o `mosaico.jpg` e as 3–4 melhores em tamanho cheio) e o `mosaico-320.jpg` (o que lê no celular).
2. **Colisões:** liste os títulos do tema que já existem no idioma (clones e canal-modelo), sobretudo fórmulas idênticas ("TODA la Historia de X en N Minutos", "A história INTEIRA de X em N minutos", "N anos de X em N minutos"). Fórmula do canal **só onde o tema ainda não existe nela** (lição dossie-es 1 e historia-ptbr 3 da reembalagem).
3. **Catálogo curto** (só o que serve a este vídeo): 3–5 padrões de título e **3–4 padrões de thumb de eixos visuais diferentes** (vocabulário abaixo), cada um com ≥ 2 vídeos reais (link, canal, views, data, mediana do canal, ×med), mesmo nicho e idioma, acima da mediana. Comece pelos padrões já medidos do canal em `padroes.md`.
4. **Promessa** (antes de escrever título): em 1 frase, o que o espectador ganha clicando. Tem de ser **cumprível com o material da pesquisa** (fatos com fonte no BRIEF/fontes: cite quais), caber na duração e ser **paga no 1º minuto** (ideal: no hook, ≤ 30 s) e sustentada pelo vídeo inteiro. Proibido prometer um caso que ocupa 1 minuto de um vídeo de 14 (lição "título de um caso só" do dossie-es), uma curiosidade resolvida em segundos ou só o fim (historia-ptbr: "como Roma caiu" pago aos 12:47). No historia-ptbr ≥ 006, a promessa é a **pergunta central** do roteiro v2.
5. **Proposta: 3 pares título+thumb (A, B, C)**, todos vendendo **a mesma promessa** por portas diferentes:
   - **Título 1, 2 e 3**, de **3 padrões diferentes** (gatilhos diferentes: `conhecimento/titulos.md`, regra de 12/11), cada um com nome do padrão + ≥ 2 referências medidas + nº de caracteres + por que não é cópia de clone. Nenhum entrega a resposta. Fórmula da bíblia em pelo menos um, salvo colisão (aí diga). (Até 15/11 o T3 saía no `pacote-youtube` como variação; desde 16/11 nasce aqui e passa no crivo.)
   - **3 conceitos de thumb (A, B, C), um por padrão visual diferente**, cada um com evidência no mosaico/pesquisa do tema e pareado a um título. **Pareamento:** forme primeiro os 3 pares (cada thumb com o título que ela melhor completa) e **só depois numere**: o par que leva o padrão de controle (o que a bíblia/placar já mediu como melhor) vira A/T1, os outros B/T2 e C/T3. Ao final, sempre A↔T1, B↔T2, C↔T3. **Vocabulário dos padrões** (grave exatamente um destes em `padrao_thumb`, para o placar agrupar): `rosto-emocao` (personagem/rosto com emoção forte), `objeto-simbolo` (objeto ou cena-símbolo isolado), `conflito-xvy` (X contra Y cara a cara, raio/divisão no meio), `numero-estatistica` (número/dado gigante como elemento dominante), `mapa-lugar` (mapa, satélite, lugar reconhecível), `antes-depois` (tela dividida no tempo), `cena-acao` (momento dramático em andamento), `documento-evidencia` (documento, foto de arquivo, prova). Escolha os 3 conforme a **bíblia do canal** (só padrões que o estilo do canal permite: sem rosto onde a bíblia proíbe, sem IA de cena no Em Relevo) e a evidência do mosaico; padrão que a bíblia/placar já mediu como vencedor entra como um dos 3 (**controle**), os outros 2 **exploram**.
   - **Evidência do padrão de thumb:** ≥ 2 thumbs reais do padrão acima da mediana real do canal delas, como sempre; para os 2 padrões de **exploração**, se o padrão não existe no tema, vale o **nicho amplo** (mesmo tipo de canal explicativo, idioma do canal ou inglês, ≤ 400 d), dito explicitamente ("evidência de nicho amplo: …"); nunca padrão sem nenhuma referência.
   - **Grade do próprio canal:** pelo menos **2 das 3** thumbs fogem do padrão dominante da grade do canal (as thumbs no ar/entregues: `conhecimento/thumbnails/<slug>-*.jpg`, `entrega/thumb-*.jpg` dos vídeos recentes); se uma lembra uma vizinha (mesmo elemento dominante + mesmo tipo de texto), troque.
   - **Canal sem `canal.yaml`** (Em Relevo): o "gerador/acervo" é o de `pesquisa/estilo-mapa-relevo-3d/PADRAO.md` + regras do canal no `noturna.py` (`REGRAS_CANAL`): mapa 3D/satélite, dados e fotos reais com licença, **sem IA de cena**.
   - **Proibido:** 2 conceitos com a mesma composição, o mesmo elemento dominante ou o mesmo tipo de texto (ex.: dois "mapa escuro + ano"; dois rostos de perfil; dois números). Teste rápido: descreva cada thumb em 5 palavras; se duas descrições trocarem só o texto, são a mesma thumb.
   - Cada conceito descrito para quem não vê imagem: composição (o que fica onde), **elemento dominante** (personagem e expressão, objeto, número, mapa…), fundo e cores (paleta da bíblia), **texto ≤ 3 palavras** no idioma do canal e posição (tipo de texto diferente entre os 3: número, palavra-pergunta, rótulo, nome, nenhum), o que promete, como conversa com **o título do par** sem repetir palavra dele (juntos criam uma pergunta), 1 foco a 320×180, ≥ 2 referências do padrão de thumb, e como se executa com o **gerador/acervo do `canal.yaml`** (1 ilustração-base por conceito). **Não gere imagem** (custo zero; a arte é da skill `thumbnail` na etapa 2).
6. **Escreva `$V/EMBALAGEM.md`** no modelo abaixo (autossuficiente: o revisor só lê ele, `embalagem/`, o BRIEF e a bíblia) e **`$V/embalagem/variantes.json`** (os 3 pares, formato em `tools/rotinas/embalagem_variantes.py`):
   `[{"letra":"A","titulo":"<T1>","padrao_titulo":"<nome>","padrao_thumb":"<eixo do vocabulário>","thumb_conceito":"<elemento dominante + composição, 1 linha>","thumb_texto":"<≤ 3 palavras>"}, {"letra":"B",…}, {"letra":"C",…}]` (thumb sem texto: `"thumb_texto": ""`)
7. **Crivo:** dispare um **Task separado, em primeiro plano**, com o prompt de [`CRIVO.md`](CRIVO.md) (preenchendo caminhos e rodada). Não passe o seu raciocínio nem diga o que você acha: só os arquivos. Ele grava `$V/embalagem/crivo-r<n>.md` e a cópia da última rodada em `$V/CRIVO.md`.
   - **APROVADO** (T1, T2, T3 e Thumbs A, B, C aprovados, e os 3 conceitos diferentes entre si) → registre os pares no banco (`tools/.venv/bin/python tools/rotinas/embalagem_variantes.py registrar --video <id> --json $V/embalagem/variantes.json`; ele recusa 2 thumbs do mesmo padrão) e siga para o roteiro.
   - **Reprovado** → reescreva **só** os elementos reprovados atendendo à "Correção pedida" (ou troque de padrão com evidência nova), marque `[MANTIDO]` / `[REESCRITO: motivo r<n> → o que mudou]`, grave a nova versão no mesmo `EMBALAGEM.md` (a anterior vai para `embalagem/EMBALAGEM-r<n>.md`) e dispare um revisor **novo** (outro Task). **Máximo 3 rodadas.**
   - Reprovou na 3ª: grave `$V/BLOQUEIO.md` (o que reprovou em cada rodada e por quê; o que faltaria: evidência, ângulo, tema fraco) e **pare a etapa** (nada de roteiro com embalagem fraca). Na fila, o e2 não roda sem `ETAPA1-PRONTA.md`.
8. **Status e commit:** `git add $V/EMBALAGEM.md $V/CRIVO.md $V/embalagem/*.md $V/embalagem/*.csv $V/embalagem/*.json $V/embalagem/busca` (mosaico/thumbs são jpg: ficam fora do git, sem problema) e `git commit -m "<canal>/<NNN>: embalagem aprovada no crivo r<n> (T1 …; thumbs <eixoA>/<eixoB>/<eixoC>)"`.

## Modelo do `EMBALAGEM.md`
```markdown
# Embalagem <canal>/<NNN-slug> · versão r<n> · <data>
Tema · idioma · duração-alvo (BRIEF) · cota gasta (unidades; search.list: N) · mosaico: embalagem/mosaico.jpg

## Pesquisa (resumo)
Top do tema (≤ 400 d): tabela link | canal | views | data | mediana do canal | ×med | padrão de título | padrão de thumb
Colisões: títulos/fórmulas que os clones já usaram neste tema (não repetir)
Thumbs do tema: o que todas fazem (o que evitar para não sumir na grade)

## Promessa
- Frase: …
- Material que a sustenta: fatos X, Y (fonte: BRIEF/SOURCES/link)
- Onde o roteiro paga: hook (0:00–0:30) "…"; 1º minuto: …; o vídeo inteiro sustenta porque …

## Título 1 · padrão "<nome>" · N caracteres [MANTIDO|REESCRITO: …]
"<título>"
Referências (≥ 2): link | canal | views | data | mediana | ×med
Por que não é cópia: …

## Título 2 · padrão "<nome>" · N caracteres [MANTIDO|REESCRITO: …]
(idem)

## Título 3 · padrão "<nome>" · N caracteres [MANTIDO|REESCRITO: …]
(idem; padrão diferente de T1 e T2)

## Pares A/B/C (resumo)
| par | título | padrão do título | padrão da thumb (vocabulário) | elemento dominante | texto da thumb |
|---|---|---|---|---|---|
| A | T1 | … | `mapa-lugar` | … | "…" |
| B | T2 | … | `rosto-emocao` | … | "…" |
| C | T3 | … | `numero-estatistica` | … | "…" |
Por que são 3 thumbs diferentes (composição, elemento dominante e tipo de texto distintos): …

## Thumb A · padrão `<eixo>` · par de T1 [MANTIDO|REESCRITO: …]
- Composição / elemento dominante (personagem e expressão, objeto, número, mapa…) / fundo e cores
- Texto: "<≤ 3 palavras>" (posição, cor; tipo de texto)
- Promete: … · Conversa com T1: … (sem repetir palavra)
- Leitura a 320×180: 1 foco = …
- Execução: gerador/acervo do `canal.yaml` (1 base: o que o prompt pede)
- Referências do padrão (≥ 2): link | canal | views | data | ×med
- Desvio da bíblia: nenhum | "… porque …"

## Thumb B · padrão `<eixo>` · par de T2 [MANTIDO|REESCRITO: …]
(idem; padrão diferente de A)

## Thumb C · padrão `<eixo>` · par de T3 [MANTIDO|REESCRITO: …]
(idem; padrão diferente de A e B)

## Obrigações (contrato com as próximas skills)
- roteiro: o hook e o 1º minuto pagam "<promessa>" (frase-âncora: "…"); o capítulo/expediente que paga o T2 entra até mm:ss; não prometer nada fora disto.
- thumbnail: 3 artes, **uma por conceito** (Thumb A, B, C: cada uma com seu prompt e composição), nunca 3 variações do mesmo.
- pacote-youtube: título A = T1, B = T2, C = T3 (pareados às thumbs A/B/C), com o padrão de cada par no `youtube.txt`; regrava `embalagem/variantes.json` + `embalagem_variantes.py registrar` com títulos finais e arquivos.
- qa: conferir o pagamento da promessa na `legendas.srt` (timestamp) e cada thumb final contra o seu conceito (e que as 3 seguem diferentes).

## Crivo
Rodada r<n>: <veredito> (CRIVO.md)
```

## Armadilhas do teste das 3 thumbs (granizo/Em Relevo, 16/11/2026: r1 3/6 → r2 4/6; `pesquisa/teste-embalagem-3thumbs-2026-11-16/RESULTADO.md`)
- **Mesmo herói com outro ângulo é a mesma thumb:** satélite da nuvem (A) × foto da nuvem do chão (C) reprovou no item 8. Diferença é de elemento dominante, não de câmera.
- **Acervo real tem de existir antes de propor:** baixe e olhe a foto citada (a "gota CC0" era uma vidraça com dezenas de gotas); se o conceito depende de recorte fino, faça a prévia 320×180 em código antes.
- **Foto genérica pareada com título de um caso específico** ("A NUVEM que fabricou…") vende a foto como o caso: reprova (promessa enganosa).
- Título do tipo "X tem mais A, mas Y tem mais B: por quê?" obriga o roteiro a pagar **os dois lados** do porquê (fonte para cada um no BRIEF).

## Armadilhas vistas no teste a seco (Templarios, 14/11/2026: r1 0/3 → r2 1/3 → r3 3/3; `pesquisa/teste-embalagem-2026-11-14/RESULTADO.md`)
- **Uma promessa só** para os 3 títulos e as 3 thumbs, e o hook planejado paga **essa** promessa (r1 caiu: título sobre o arresto, hook sobre Chinon).
- Todo verbo do título ("cómo", "en una mañana") e o **objeto da thumb** precisam de fato com fonte no BRIEF; senão, acrescente a fonte antes ou mude a promessa (r2 caiu: "cómo" sem fato; chave dourada que não é do caso).
- Sello/texto da thumb abre pergunta: não responde o título ("DEUDA") nem forma frase com a sigla ("TEMPLARIOS ABSUELTOS").
- Recalcule os ×med com as medianas do dia (o revisor confere e aponta).

## Critérios de pronto (avaliar)
- `CRIVO.md` com **APROVADO** (6 de 6 + diferenciação entre as thumbs) em ≤ 3 rodadas, ou `BLOQUEIO.md` e etapa parada.
- 3 thumbs de 3 padrões do vocabulário (composição, elemento dominante e tipo de texto distintos), registradas em `youtube.embalagem_variantes`.
- T1, T2 e T3 de padrões diferentes, ≤ 100 caracteres (e o teto da bíblia), sem palavras proibidas (`conhecimento/politicas-youtube.md`), sem entregar a resposta; "em N minutos" só se a bíblia mantiver (o N é provisório até a duração real).
- Cada elemento com ≥ 2 referências reais medidas (views e data de hoje, acima da mediana real do canal delas).
- Promessa cumprível com fatos com fonte, paga no 1º minuto, e virou obrigação escrita para o roteiro.
- Mosaico ≤ 1 MB em `embalagem/`, olhado; custo pago = 0.

## Loop de melhoria
1. **Avaliar:** quantas rodadas o crivo pediu e em quais itens reprovou (anote no `EMBALAGEM.md`).
2. **Corrigir:** só pelas rodadas do crivo (máx. 3).
3. **Registrar:** o placar `embalagem_variantes.py placar --canal <slug>` diz qual padrão de thumb vem ganhando no canal (o Métricas registra a vencedora do "Testar e comparar"); use-o para escolher o controle e os 2 padrões de exploração. Padrão novo de título/thumb medido vai para `canais/<slug>/biblia/titulo.md` ou `thumb.md` como **Hipótese** (com data, links e views), até o CTR/retenção do Studio confirmar (Métricas). Reprovação de crivo que se repete em canais diferentes vira regra em `conhecimento/titulos.md` ou `conhecimento/thumbnails/README.md`.
4. **Commitar** (passo 8).

## Depois (Métricas)
Com o vídeo no ar 7 dias, o Métricas pede ao Rodrigo a thumb vencedora do "Testar e comparar" (`embalagem_variantes.py pendentes`) e grava (`vencedora --video <id> --letra X`), e compara CTR e retenção com a promessa: CTR alto + retenção baixa = promessa não paga (volta como lição para a bíblia); CTR baixo + retenção alta = embalagem fraca (o crivo deixou passar: ajustar a régua em `CRIVO.md`). Próximo passo registrado em `conhecimento/titulos.md`: um **eval automático** do crivo (não implementado).
