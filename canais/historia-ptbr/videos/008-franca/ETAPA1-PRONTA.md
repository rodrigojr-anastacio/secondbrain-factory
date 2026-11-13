# ETAPA 1 PRONTA · historia-ptbr/008 França · youtube.videos id 33 · 13/11/2026

Etapa 1 (Opus) concluída: pesquisa, roteiro com checagem de fatos, checklist v2 **APROVADO** (14/14 obrigatórios estimados; ritmo só depois da voz), storyboard, cenas.json, títulos e conceitos de thumb. **Nada de voz, imagem ou render foi gerado. Custo da etapa 1: US$ 0.**

## O que está pronto
| Arquivo | Conteúdo |
|---|---|
| `roteiro.py` | fonte única (texto + planos + grafias de voz). Gera os 4 abaixo: `python3 roteiro.py` |
| `SCRIPT.md` / `blocos.json` | 2.000 palavras, 54 blocos (`texto` = grafia de voz para o Fish; `tela` = grafia correta para legendas) |
| `STORYBOARD.md` / `storyboard.json` / `cenas.json` | 299 planos, **183 imagens** únicas (reuso 0% até 3:00, 49% depois), 23 cortes no 1º min, 16 rótulos, 10 capítulos |
| `SOURCES.md` | checagem bloco a bloco; 9 correções aplicadas antes da voz |
| `BRIEF.md` | demanda, referência assistida (`ref/clone-franca-7amJtj96T0w.txt`), estrutura, teto |
| `ETAPA1.md` | resumo + saída do checklist v2 |
| `thumbs/CONCEITOS.md` + `thumbs/cenas-thumbs.json` | 3 títulos pareados com 3 thumbs e os prompts das 6 bases |

**Hook (3 primeiras frases):** "Soissons, quatrocentos e oitenta e seis. Imagine você entre guerreiros francos, diante do saque de uma batalha. Na pilha, um vaso precioso de igreja."
**Títulos:** A "A história INTEIRA da França em 16 minutos" ↔ thumb HiM (FRANÇA 486 – 2026) · B "Por que a França matou o rei e nunca viveu sem um?" ↔ REI × POVO 1793 · C "Como um machado decidiu quem manda na França" ↔ bonecos POR UM VASO? 486.

## O que a etapa 2 precisa saber
1. **Código de montagem:** copie `package.json`, `src/` (Video.jsx, labels.jsx, Thumbnail.jsx, index.jsx) e `tools/` (build.py, qa.sh, medir.py, escolher_tomadas.py, qa_fonetico.py, qa_voz_blocos.py, render_partes.sh…) de `../007-russia/` e troque só os caminhos/ids. Rótulos de mapa (`map_*`) vão no `src/labels.jsx`: mapas foram pedidos sem letras.
2. **Voz:** drama-3, 1 chamada por bloco, clone do canal (`canal.yaml`). **Preço mudou em 12/11** (US$ 10/M → ~US$ 50/M): o roteiro tem 11.389 bytes ≈ **US$ 0,57** por passada; confira o modelo cobrado pelo crédito antes/depois. Faça o **teste de nomes** antes do vídeo (lista `FALA` no `roteiro.py`, grafias chutadas, NÃO testadas): Soissons → "Suassôn", Reims → "Rrãns", Verdun → "Verdân", Orléans → "Orleã", Crécy → "Crecí", Azincourt → "Azancúr", Calais → "Calê", Bouvines → "Buvíne", Nantes → "Nânt", Notre-Dame → "Notrrí Dâm", Waterloo → "Uóterlu", Sedan → "Sedã", De Gaulle → "De Gól", Alésia → "Alézia", Capeto → "Capêto". Se alguma soar estranha, troque no `FALA` e rode `python3 roteiro.py` de novo (não edite `blocos.json` à mão). Atenção a "Luís Dezesseis"/"Luís, o Décimo Quarto" (por extenso de propósito) e "Gregório de Tours". Hook: 4 tomadas e escolha por bloco (`escolher_tomadas.py`, meta de repetição ≤ 0,12).
3. **Duração:** estimativa 15:30–16:00 (2.000 palavras a ~128 ppm). O título A diz "16 minutos": troque o N pela duração real (título, descrição, banco).
4. **Imagens:** nano-banana-2.1/edit + refs do `canal.yaml`. **Lote-prova de 6:** I001 (saque/multidão franca), I029 (mapa da Gália sem letras), I058 (batismo de Clóvis + bispo), I076 (coroação de Carlos Magno), I131 (Luís XIV e nobres no *lever*), I142 (Bastilha: conferir que não há bandeira tricolor em 1789). Depois o resto em lotes (183 × US$ 0,046 ≈ US$ 8,4). Prompts de risco para conferir na prancha: Notre-Dame/coroação de 1804 (sem minaretes, gótico), guilhotinas (sem sangue), `terror_tribunal` (faixas tricolores sem letras), `map_1420`/`map_angevin`/`map_verdun` (letras inventadas), `paris_liberation` (bandeira de 1944 é ok, letreiros não), `rice_market` (embalagem sem letras), `playing_card` (carta sem letras: se vier com "R"/"Charles", refazer).
5. **Trilha:** sugestão — modo dórico em Ré, alaúde/flauta medieval sintetizada nos caps. 1–5 e cravo barroco a partir do cap. 6 (região/época do tema; regra do `visual.md`).
6. **Teto US$ 14** (fal + Fish): voz ~0,7 (com tomadas e teste de nomes) + lote-prova 0,28 + 177 imagens ~8,1 + refeitas ~0,5 + 6 bases de thumb 0,28 ≈ **US$ 9,9**. Outros jobs gastam o mesmo saldo fal/Fish: meça pelo registro do `--video 33`, não pela queda do saldo.
7. **Entrega:** NÃO subir para o Drive (Drive quase cheio). Tudo em `entrega/` (video.mp4, legendas.srt, thumb-A/B/C.jpg, pacote/youtube.txt com os 3 títulos pareados às thumbs). Créditos de acervo só na descrição.
8. **Banco:** linha `youtube.videos` id 33 criada (`status='roteiro'`, `biblia_versao='v2'`); avance até `pronto` e grave `duracao_s`.
9. Neutralidade: termina em 1958/1963; nada de política atual.
