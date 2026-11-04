---
name: roteiro
description: Use para escrever ou revisar o roteiro de um vídeo da fábrica do YouTube a partir do BRIEF.md - segue a bíblia do canal (canais/<slug>/biblia/roteiro.md, que define estrutura, hook, capítulos, transições, fecho e tamanho), edita o roteiro.py (fonte única) e gera SCRIPT.md, blocos.json e SOURCES.md, com loops pagos e fatos com fonte.
---

# roteiro: roteiro.py → SCRIPT.md, blocos.json, SOURCES.md

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `canais/<slug>/videos/NNN-slug/` (abaixo, `$V`).
Procedimento-base: `playbooks/produzir-video.md` §2. Modelo recomendado: **opus** (etapa `roteiro` ou `roteiro-storyboard` do `tools/claude_run.py`).

**Caixinha do canal:** a estrutura do roteiro **não é da fábrica, é do canal.** Cada canal tem a sua em `canais/<slug>/biblia/roteiro.md`, e ela prevalece sobre `conhecimento/`. Nunca use estrutura, hook ou tom de outro canal. Ex.: `historia-ptbr` = narrativa contínua com eras ligadas (History in Minutes); `dossie-es` = EXPEDIENTES curtos encadeados (Archive in Minutes); `lotr-fr` = do familiar à pergunta, cronológico com payoff no fim. O erro de 04/11/2026 (capítulos-objeto do Archive no Irã do historia-ptbr) está em `conhecimento/anti-padroes.md` §8.

## Antes de agir
1. **Primeiro a bíblia:** `canais/<slug>/biblia/README.md` (canal-modelo e "o que NÃO fazer aqui") e `biblia/roteiro.md` inteiro (estrutura, hook, transições, fecho, tamanho, tom, checklist). Para o título de trabalho, `biblia/titulo.md`; para a voz (tags, pausas), `biblia/voz.md`.
2. Leia `$V/BRIEF.md` (referência, duração-alvo, loops, teto) e, se houver, `$V/ref/*.txt`.
3. Leia `canais/<slug>/canal.yaml` e as regras gerais: `conhecimento/roteiros.md`, `conhecimento/hooks.md` e `conhecimento/anti-padroes.md`.
4. Use como modelo o `roteiro.py` do **vídeo anterior do mesmo canal** (nunca de outro canal), exceto onde a bíblia revogou algo depois dele.

## Passos
0. **Estude a referência pela transcrição completa** (não só o hook): `tools/.venv/bin/python tools/transcrever.py <ID> $V/ref/<nome>.txt <idioma>`, em 1–3 vídeos **do canal-modelo da bíblia** sobre o tema ou a fórmula. Anote como a referência faz o que a bíblia pede (tempo até a promessa, capítulos, transições, loops, fecho). Transcrição de outro canal-modelo não serve de molde.
1. **Estrutura:** monte o esqueleto exatamente como `biblia/roteiro.md` define (hook, nº e tipo de capítulo, ligação entre capítulos, fecho). Defina o **fio condutor** e os **loops** e onde cada um é pago.
2. **Hook:** o molde da bíblia. Modele a técnica da referência; **nunca traduza nem copie** o texto.
3. **Escreva no `roteiro.py`** (nunca nos arquivos gerados): um bloco `N...` = um arquivo de áudio (2–4 frases); marque `IDEIA` nos blocos que abrem ideia nova (vira `"ideia": true`, usado nas pausas do `build.py`).
   **Escreva para a fala** (regra geral em `conhecimento/roteiros.md`): frases de 4–14 palavras, vírgula onde se respira, "…" só na virada, números por extenso. Tags de tom, `[break]` e pausas: siga `biblia/voz.md` do canal.
   **Texto na tela** (rótulos, cartões de data, placas de capítulo): siga `biblia/visual.md` do canal. Mapas sem texto + rótulos em `src/labels.jsx`.
4. **Fatos:** cada número/data com fonte em `SOURCES.md`; estimativa dita como estimativa; fato não confirmado como `[PENDENTE]` com versão alternativa (não trave).
5. **Gere e valide:** `cd $V && python3 roteiro.py` (gera `SCRIPT.md`, `blocos.json` e, se o storyboard já estiver no arquivo, `cenas.json`/`STORYBOARD.md`/`storyboard.json`).
6. Conte as palavras: `python3 -c "import json,re;b=json.load(open('blocos.json'));print(sum(len(re.sub(r'\[[^]]*\]','',x['texto']).split()) for x in b))"` e compare com a tabela "Tamanho" da bíblia (ritmo medido da voz do canal).
7. Atualize o status: `psql -d vida -c "UPDATE youtube.videos SET status='roteiro', atualizado_em=now() WHERE id=<id>"`.

## Critérios de pronto (avaliar)
- **Passa no checklist de `canais/<slug>/biblia/roteiro.md`** item por item (marque cada um no `ETAPA1.md`).
- Nada da lista "O que NÃO fazer aqui" do `biblia/README.md` (ex.: no historia-ptbr, nenhum capítulo-objeto; no dossie-es, nenhuma narrativa sem expedientes).
- Tamanho dentro da faixa da bíblia para a duração-alvo.
- Todo loop aberto é pago; todo fato tem fonte em `SOURCES.md`; `[PENDENTE]` sempre com alternativa.
- `python3 roteiro.py` roda sem erro e `blocos.json` tem `ideia` nos blocos certos.
- Escreva o resumo da etapa em `$V/ETAPA1.md` (palavras, duração estimada, fio condutor, loops, checklist da bíblia, pendências).

## Loop de melhoria
1. **Avaliar:** checklist da bíblia + palavras, duração estimada do hook e loops pagos/abertos.
2. **Corrigir:** até 2 rodadas (cortar, reescrever hook, ligar capítulos, pagar loop). O resto vira pendência no `ETAPA1.md`.
3. **Registrar:** aprendizado de estrutura, hook ou tom vai para **`canais/<slug>/biblia/roteiro.md`** (do canal deste vídeo) com **data e fonte**; sem retenção medida = **Hipótese**. Só sobe para `conhecimento/roteiros.md` o que for **comprovadamente geral** (vale para qualquer canal: escrita para a fala, ferramenta, processo).
4. **Commitar:** `git add $V/roteiro.py $V/SCRIPT.md $V/SOURCES.md $V/blocos.json $V/ETAPA1.md` (+ bíblia/conhecimento tocados) e
   `git commit -m "<canal>/<NNN>: roteiro v1 (N palavras, hook X s)"`.
