# ETAPA 1 (storyboard): 001-midway, "Why Can't You Visit Midway Atoll?" (youtube.videos id 30)

Data: 2026-11-12. Fonte: `roteiro.py` (python3 puro; `cd $V && python3 roteiro.py`), que gera `blocos.json`, `storyboard.json`, `STORYBOARD.md` e `cenas.json`. O `SCRIPT.md` continua sendo o roteiro final: o `roteiro.py` não o reescreve, só confere que a narração é idêntica a ele.

## Números
| Item | Valor |
|---|---|
| Blocos de áudio | 87 (B01a…B21d; 30 com `ideia: true`), 2.687 palavras, idênticas ao SCRIPT.md |
| Duração estimada | **17:55** a 150 ppm (sem pausas; recalcular com a voz real) |
| Planos | **198** · 11,1 planos/min (média de 5,4 s; a bíblia mede troca de *tipo* de tela, não cortes/min) |
| Material real (foto, filme, documento, então × agora) | **85,4%** do tempo (mínimo 85%) |
| Reuso | **35,2%** do tempo, todo depois de 3:00, exceto o retorno planejado à página do Nimitz (doc do hook) |
| Imagens IA no corpo | **0** (`cenas.json = []`) |
| Custo previsto do storyboard | US$ 0 de imagem; pré-QA visual US$ 0,076 (gravado em `financas.consumo`, ref 30) |

## Componentes × checklist da bíblia
| Componente | Planos | Bíblia | OK |
|---|---|---|---|
| KenBurns | 79 (todos com movimento; nenhuma foto parada) | toda foto, nunca parada > 3 s | sim |
| Filme | 43 trechos reais (*The Battle of Midway* 36, *Torpedo Squadron 8* 7), sem áudio original e sem cartelas, títulos ou placas "In Memoriam" (faixas proibidas validadas) | clipes de 4 a 8 s no hook e nas viradas | sim |
| DocGrifo | 43 planos, 15 documentos distintos, **12 grifados** (10 com leitura literal validada pelo script) | ≥ 4 documentos lidos e grifados | sim |
| Número | 44 (16 em tela cheia + 28 sobrepostos) | 1 por minuto, ≥ 3 | sim |
| Mapa2D | 11 planos (Havaí–Midway ×2, Clipper, isca/Hypo, teatro 325°/175 NM, ataques, barreira SCHEMATIC, suprimento, tsunami, naufrágios SCHEMATIC) | 1 por bloco, ≥ 2 | sim |
| EntaoAgora | 2 (hangar 1942 × 2022 em B15d; aérea 1941 × ISS 2001 em B21c) | ≥ 1 | sim |
| Cartela | 3 (mensagem do cabo, SCHEMATIC, B05c; 2 perfis de profundidade, SCHEMATIC, B19) | imagem não fotográfica com selo | sim |
| Card | 1 (fecho do canal) | — | — |

Validações do `roteiro.py`, todas passando: narração = SCRIPT.md (parse dos parágrafos B01–B21); todos os arquivos existem em `midia/` e estão no `midia.csv`; toda foto tem Ficha; nenhum tipo de tela passa de 12 s seguidos; nenhum KenBurns parado; mesmo arquivo + enquadramento (ou trecho de filme sobreposto) nunca em menos de 60 s; nenhum reuso antes de 3:00 (fora o doc do hook); trecho de filme ÷ velocidade ≥ duração do plano (velocidade de 0,55 a 1,0); grifo literal lido na narração do plano; contagem por componente; ≥ 85% de material real. Avisos que restam: 4 KenBurns de 8,8 a 10,8 s (Gay, Hiryu, estação do cabo, ISS: conferir se o movimento sustenta) e 8 "fidelidade?" que são falsos positivos (nome citado sobre a página do Nimitz, sobre um Número ou sobre clipe genérico de SBD ou porta-aviões, com Ficha honesta).

## Imagens IA: por que zero
Os 3 cortes esquemáticos que a bíblia permite (mensagem do cabo, barreira do Pacífico, posições e profundidade dos naufrágios) são **desenhados em código** com selo "SCHEMATIC" (Cartela/Mapa2D), com os números do SCRIPT/SOURCES. Não sobra nada para gerar: nenhuma foto falsa, nenhum texto pedido à IA, custo zero. Nautilus/OET fora (licenças).

## Fidelidade (decisões)
- O que tem nome aparece: Yorktown (3 fotos 80-G), Hiryu (USAF 75712 AC, americana, e NH 73064), Soryu (USAF-ID-4845), Mikuma (80-G-414422), Akagi/Kaga (NH 73059/73060: japonesas pré-1946, liberadas no `licencas.md`, sem equivalente americano), Rochefort, Yamamoto, Gay, Waldron (clipe do *Torpedo Squadron 8* com Waldron e Dobbs, 165–175 s), Wisdom, Robbins, hangar 1942/2015/2022, Henderson Field, estação do cabo.
- Sem foto no `midia/`: Nimitz, Layton, Ford, Holmes, Cannon, Clinton, Ballard. Nesses planos entra o **documento sobre a pessoa** (página do Nimitz, H-Gram, track chart, história oral de Ford, EO 13022) ou um clipe genérico com Ficha honesta ("Marines of the Midway garrison (Cannon not shown)", "A lookout (not Miniclier)").
- Naufrágios (B19): Mapa2D SCHEMATIC + perfil de profundidade SCHEMATIC + fotos de época dos navios. Nada do Nautilus/OET.
- Sem gore. Mortos só em números; o funeral do filme de Ford ficou de fora.
- Albatrozes filmados por Ford em 1942 entram em 4 planos (B02c, B12c, B17a, B18a), sempre com Ficha "1942 · MIDWAY".

## Pré-QA (preqa/)
- `preqa/gerar_grades.py` (PIL, só stills) gera um quadro-chave por plano (`preqa/quadros/P001…P198.jpg`, 1280x720, com Ficha, Número, grifo, rótulos e selo simulados) e 9 grades de cerca de 2 min (`preqa/grade_NN_*.jpg`, 3 colunas, tempo no canto). Os quadros de filme são extraídos com ffmpeg do trecho real.
- **Olho (2 rodadas), corrigido:** enquadramento dos KenBurns de Soryu, B-17 sobre o porta-aviões, Yorktown ×2 (o navio estava fora do quadro); grifos da EO 13022 §3(a)/(5), do H-Gram ("not to convince Nimitz") e da fala de Ford (linha inteira lida); captura do projeto dos camundongos recortada só no texto (a foto aérea do topo pode ser de parceiro: era bloqueante de licença); clipe de avião não identificado em B09b trocado por SBDs americanos; repetições (midway1945, guerrafria1959, hangar2022 em B20c, Akagi em B19c) trocadas.
- **`tools/preqa_visual.py`** (Sonnet, US$ 0,076 no total) em 3 grades (0–2 min, 6–8 min, 14–16 min) + 1 nova rodada: 1 bloqueante na 1ª rodada (rótulos dos naufrágios encavalados no mapa), corrigido; **2ª rodada com 0 bloqueante**. Ficaram altos e médios que são da simulação ou de design: a Ficha cobre o texto nos DocGrifo (no Remotion ela deve sair antes do zoom/grifo); mapas em mar aberto sem terra (Midway não aparece no Natural Earth 50m); fotos aéreas P&B de porta-aviões parecidas em B08–B09; Número sobre o canto da foto. Relatórios em `preqa/visual_01`, `visual_04`, `visual_08`, `visual_08_r2`.

## Pendências para a produção
1. **Componentes Remotion a escrever** (os de `testes/estilo/src/Frames.jsx` são protótipos fixos): KenBurns (crop + de/para), Filme (in/out, velocidade, sem áudio), DocGrifo genérico (vários retângulos, `regiao`, zoom até a linha; **Ficha some antes do grifo**), Número (tela cheia e sobreposto), Mapa2D genérico (pontos/linhas/selo do `storyboard.json`), EntaoAgora genérico, Cartela SCHEMATIC, **PerfilProfundidade** (B19: Yorktown ~3 mi/~5.000 m, Kaga ~5.400 m, Akagi, mergulhos do ROV > 5.100 m) e Card final. O `build.py` lê o `storyboard.json` e redistribui os tempos pelo áudio real.
2. **Mapas:** o recorte `mapa_base_pacifico.json` não chega a São Francisco (rota do Clipper, B04c) nem a Adak/51,9°N (barreira, B11b). Regerar do `mapa_base_ne50m_land.geojson` com `testes/estilo/scripts/mapa_svg.py`. Perto de Midway o mapa é só mar: desenhar o contorno do atol ou um inset. Posições dos naufrágios são aproximadas (selo SCHEMATIC).
3. **Tempos reais:** tudo está estimado a 150 ppm. Com a voz escolhida, rodar a validação de novo com as durações reais: a sequência de um mesmo tipo de tela pode passar de 12 s, e trechos de filme podem ficar curtos (8 planos já estão em câmera lenta de 0,56 a 0,74: B04c 97–99 s a 0,56, B09b 594–597 s a 0,57, B17a 158,9–161,1 s a 0,6, B07b 440–445 s a 0,64, B13a, B09d, B11a e B03a de 0,66 a 0,74; conferir se ficam naturais). Se a voz for mais lenta, a margem de material real (85,4%) não aguenta plano novo em código: troque código por código.
4. **Resolução:** `foto_guerrafria1959.jpg` (1305 px; zoom ≤ 1,08), `foto_canhao_historico.jpg` (1024 px; janela de 914–931 px, amplia 1,4x), `foto_tsunami_lagoa2011.jpg` (1200 px), `foto_lixo_marinho2017.jpg` e `foto_albatroz_ninho.jpg` (1920 px). Nas capturas .gov, limitar o zoom a uma janela ≥ 1.100 px (até ~1,75x em 1080p) ou recapturar a 3x.
5. **Grifos:** CINCPAC e EO foram medidos numa grade de 5%; o resto vem do bbox do `midia.csv` (Ford e H-Gram remedidos). O do depoimento sobre o chumbo (B13b) pega também a frase anterior: refinar. Conferir todos no still do Remotion.
6. **Opcional, para mais fidelidade (US$ 0, PD NHHC/NARA):** fotos de Nimitz, Ford, Layton e do 1st Lt. George Cannon (NH 105688); hoje Cannon é coberto por um clipe da guarnição com Número "MEDAL OF HONOR".
7. **Para o Rodrigo decidir:** o Número "~300 VISITORS A YEAR (UNTIL 2012)" em B12d não é dito na narração (fonte: audiência de 2014, S18): manter ou tirar. Os albatrozes de 1942 sob frases no presente (B18a) também são decisão dele.
8. Nenhum commit feito (pedido do orquestrador). Ao commitar: `roteiro.py blocos.json storyboard.json STORYBOARD.md cenas.json ETAPA1.md preqa/gerar_grades.py preqa/grade_*.jpg preqa/visual_*`. `preqa/quadros/` tem 198 JPGs (~30 MB): deixar fora do git.
