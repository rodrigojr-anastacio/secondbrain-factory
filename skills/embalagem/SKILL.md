---
name: embalagem
description: Use em todo vídeo NOVO da fábrica do YouTube logo depois da pesquisa-referencia e ANTES do roteiro - pesquisa real no YouTube (top vídeos do tema em ~12 meses, padrões de título e thumb, colisões com clones, mosaico das thumbs), propõe 2 títulos (T1/T2, padrões diferentes, com evidência) + 1 conceito de thumb + a promessa que o roteiro tem de pagar, grava EMBALAGEM.md e passa pelo crivo independente (CRIVO.md, até 3 rodadas; reprovado = BLOQUEIO.md). Decisão do Rodrigo de 14/11/2026.
---

# embalagem: tema + BRIEF.md → EMBALAGEM.md (+ crivo → CRIVO.md)

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`. Python: `tools/.venv/bin/python`.
Modelo: **opus** (etapa 1 do lote). O crivo roda num **Task separado** (revisor independente): instruções em [`CRIVO.md`](CRIVO.md).

**Por que existe (Rodrigo, 14/11/2026):** a aula de métricas que ele segue diz que "retenção alta + CTR baixo + poucas views = o vídeo é bom, a embalagem errou". Na reembalagem dos 15 vídeos publicados (`pesquisa/reembalagem-2026-11-14/`) o crivo reprovou 19 de 45 elementos na 1ª rodada: título e thumb pensados **depois** do vídeo saíram fracos. Agora a ordem se inverte: **ideia → título → thumb → (crivo) → roteiro → hook → storyboard → voz → imagens → render.**
- **Portão = só o crivo** (agente separado, régua alta). O Rodrigo **não** aprova cada embalagem.
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
1. **Pesquisa no YouTube (custo zero, idioma do canal; inglês de apoio se o tema for global).** Script: `skills/embalagem/scripts/pesquisa_embalagem.py` (saída em `$V/embalagem/`):
   ```bash
   P=~/workspace/fabrica-youtube/tools/.venv/bin/python; S=~/workspace/fabrica-youtube/skills/embalagem/scripts/pesquisa_embalagem.py
   $P $S buscar $V/embalagem --idioma <es|pt|en|fr> "<termo 1>" "<termo 2>" ...   # 4–8 termos: nome do tema, sinônimos, ângulo do BRIEF, "historia/história de X"
   $P $S enriquecer $V/embalagem --dias 400       # videos.list + channels.list + mediana real (últimos ≤ 30 longos) → refs.csv
   $P $S thumbs $V/embalagem --top 9 --nossos <id1,id2>   # thumbs via WARP + mosaico.jpg (≤ 1 MB) + mosaico-320.jpg
   ```
   - yt-dlp e download de thumb **só via `socks5://127.0.0.1:40000`** (o script já usa). Data API só `videos.list`/`channels.list`/`playlistItems` (1 unidade). `search.list` (100 unidades) no máx. **2 por vídeo** e só se o yt-dlp falhar. Anote a cota gasta no `EMBALAGEM.md`.
   - Janela ~12 meses (≤ 400 d). "Acima da mediana" = views > mediana real do canal da referência (o script calcula; medianas de olho erraram na reembalagem r1).
   - **Olhe as thumbs com Read** (o `mosaico.jpg` e as 3–4 melhores em tamanho cheio) e o `mosaico-320.jpg` (o que lê no celular).
2. **Colisões:** liste os títulos do tema que já existem no idioma (clones e canal-modelo), sobretudo fórmulas idênticas ("TODA la Historia de X en N Minutos", "A história INTEIRA de X em N minutos", "N anos de X em N minutos"). Fórmula do canal **só onde o tema ainda não existe nela** (lição dossie-es 1 e historia-ptbr 3 da reembalagem).
3. **Catálogo curto** (só o que serve a este vídeo): 3–5 padrões de título e 2–3 de thumb, cada um com ≥ 2 vídeos reais (link, canal, views, data, mediana do canal, ×med), mesmo nicho e idioma, acima da mediana. Comece pelos padrões já medidos do canal em `padroes.md`.
4. **Promessa** (antes de escrever título): em 1 frase, o que o espectador ganha clicando. Tem de ser **cumprível com o material da pesquisa** (fatos com fonte no BRIEF/fontes: cite quais), caber na duração e ser **paga no 1º minuto** (ideal: no hook, ≤ 30 s) e sustentada pelo vídeo inteiro. Proibido prometer um caso que ocupa 1 minuto de um vídeo de 14 (lição "título de um caso só" do dossie-es), uma curiosidade resolvida em segundos ou só o fim (historia-ptbr: "como Roma caiu" pago aos 12:47). No historia-ptbr ≥ 006, a promessa é a **pergunta central** do roteiro v2.
5. **Proposta:**
   - **Título 1 e Título 2**, de **padrões diferentes** (gatilhos diferentes: `conhecimento/titulos.md`, regra de 12/11), cada um com nome do padrão + ≥ 2 referências medidas + nº de caracteres + por que não é cópia de clone. Nenhum entrega a resposta. Fórmula da bíblia em pelo menos um, salvo colisão (aí diga). O 3º título do "Testar e comparar" sai depois, no `pacote-youtube`, como variação de T1/T2.
   - **1 conceito de thumb** descrito para quem não vê imagem: composição (o que fica onde), personagem e expressão (ou objeto, se a bíblia/Hipótese do canal pedir), objeto-símbolo, fundo e cores (paleta da bíblia), **texto ≤ 3 palavras** no idioma do canal e posição, o que promete, como conversa com **os dois** títulos **sem repetir** palavra deles (juntos criam uma pergunta), 1 foco, ≥ 2 referências do padrão de thumb. **Não gere imagem** (custo zero; a arte é da skill `thumbnail` na etapa 2).
6. **Escreva `$V/EMBALAGEM.md`** no modelo abaixo (autossuficiente: o revisor só lê ele, `embalagem/`, o BRIEF e a bíblia).
7. **Crivo:** dispare um **Task separado, em primeiro plano**, com o prompt de [`CRIVO.md`](CRIVO.md) (preenchendo caminhos e rodada). Não passe o seu raciocínio nem diga o que você acha: só os arquivos. Ele grava `$V/embalagem/crivo-r<n>.md` e a cópia da última rodada em `$V/CRIVO.md`.
   - **APROVADO** (T1, T2 e Thumb aprovados) → segue para o roteiro.
   - **Reprovado** → reescreva **só** os elementos reprovados atendendo à "Correção pedida" (ou troque de padrão com evidência nova), marque `[MANTIDO]` / `[REESCRITO: motivo r<n> → o que mudou]`, grave a nova versão no mesmo `EMBALAGEM.md` (a anterior vai para `embalagem/EMBALAGEM-r<n>.md`) e dispare um revisor **novo** (outro Task). **Máximo 3 rodadas.**
   - Reprovou na 3ª: grave `$V/BLOQUEIO.md` (o que reprovou em cada rodada e por quê; o que faltaria: evidência, ângulo, tema fraco) e **pare a etapa** (nada de roteiro com embalagem fraca). Na fila, o e2 não roda sem `ETAPA1-PRONTA.md`.
8. **Status e commit:** `git add $V/EMBALAGEM.md $V/CRIVO.md $V/embalagem/*.md $V/embalagem/*.csv $V/embalagem/*.json $V/embalagem/busca` (mosaico/thumbs são jpg: ficam fora do git, sem problema) e `git commit -m "<canal>/<NNN>: embalagem aprovada no crivo r<n> (T1 …)"`.

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

## Thumb [MANTIDO|REESCRITO: …]
- Composição / personagem e expressão (ou objeto) / objeto-símbolo / fundo e cores
- Texto: "<≤ 3 palavras>" (posição, cor)
- Promete: … · Conversa com T1: … · com T2: … (sem repetir palavra)
- Leitura a 320×180: 1 foco = …
- Referências do padrão (≥ 2): link | canal | views | data | ×med
- Desvio da bíblia: nenhum | "… porque …"

## Obrigações (contrato com as próximas skills)
- roteiro: o hook e o 1º minuto pagam "<promessa>" (frase-âncora: "…"); o capítulo/expediente que paga o T2 entra até mm:ss; não prometer nada fora disto.
- thumbnail: arte a partir deste conceito; as variações do "Testar e comparar" mudam só <texto/expressão/enquadramento>, nunca o conceito.
- pacote-youtube: T1 = título A, T2 = título B (pareados às thumbs A/B); 3º = variação de T1/T2.
- qa: conferir o pagamento da promessa na `legendas.srt` (timestamp) e a thumb final contra este conceito.

## Crivo
Rodada r<n>: <veredito> (CRIVO.md)
```

## Critérios de pronto (avaliar)
- `CRIVO.md` com **APROVADO** (3 de 3) em ≤ 3 rodadas, ou `BLOQUEIO.md` e etapa parada.
- T1 e T2 de padrões diferentes, ≤ 100 caracteres (e o teto da bíblia), sem palavras proibidas (`conhecimento/politicas-youtube.md`), sem entregar a resposta; "em N minutos" só se a bíblia mantiver (o N é provisório até a duração real).
- Cada elemento com ≥ 2 referências reais medidas (views e data de hoje, acima da mediana real do canal delas).
- Promessa cumprível com fatos com fonte, paga no 1º minuto, e virou obrigação escrita para o roteiro.
- Mosaico ≤ 1 MB em `embalagem/`, olhado; custo pago = 0.

## Loop de melhoria
1. **Avaliar:** quantas rodadas o crivo pediu e em quais itens reprovou (anote no `EMBALAGEM.md`).
2. **Corrigir:** só pelas rodadas do crivo (máx. 3).
3. **Registrar:** padrão novo de título/thumb medido vai para `canais/<slug>/biblia/titulo.md` ou `thumb.md` como **Hipótese** (com data, links e views), até o CTR/retenção do Studio confirmar (Métricas). Reprovação de crivo que se repete em canais diferentes vira regra em `conhecimento/titulos.md` ou `conhecimento/thumbnails/README.md`.
4. **Commitar** (passo 8).

## Depois (Métricas)
Com o vídeo no ar 7 dias, o Métricas compara CTR e retenção com a promessa: CTR alto + retenção baixa = promessa não paga (volta como lição para a bíblia); CTR baixo + retenção alta = embalagem fraca (o crivo deixou passar: ajustar a régua em `CRIVO.md`). Próximo passo registrado em `conhecimento/titulos.md`: um **eval automático** do crivo (não implementado).
