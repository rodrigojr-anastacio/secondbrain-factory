# ETAPA 1: roteiro + storyboard · 003 Irã (youtube.videos id 5)

04/11/2026 · fonte única `roteiro.py` → `SCRIPT.md`, `blocos.json`, `cenas.json`, `STORYBOARD.md`, `storyboard.json`; mais `SOURCES.md`, `thumb-variacoes.json` e `src/labels.jsx`. Nada pago nesta etapa. `status = 'roteiro'` no banco.

## Números (saída de `python3 roteiro.py`, sem avisos)
| Critério | Meta | Resultado |
|---|---|---|
| Palavras faladas (sem tags) | 2.050–2.150 | **2.137** |
| Duração estimada (2,4 palavras/s, com as pausas entre frases) | 14–16 min | **903 s ≈ 15:03** (+ pausas entre blocos do `build.py`, ~1 min → ~16 min; título provável "em 15/16 minutos", decidir pelo áudio real) |
| Hook | ≤ 35 s | **32,6 s** (N001–N005); desfecho da anedota ("sai o caixão do poeta") em **~11 s** pela estimativa conservadora |
| Capítulos-objeto falados | 13–16 | **16** + hook + fecho |
| Maior intervalo sem re-hook | ≤ 90 s | 86 s (O Poema, com o CTA e o pagamento do hook no meio) |
| Blocos | — | 102 (40 marcados em `IDEIA`) |
| Tags | ≤ 1 a cada 2–3 blocos | 11 de tom (`curious`, `amazed`, `serious`, `warm`) + 3 `[long-break]` (N051 "não o ouro… a língua", N076 CIA, N095 "é o filho dele"); nenhum `[break]` |
| Planos | — | **309** (média de 2,92 s) |
| Cortes no 1º minuto | ≥ 18 | **24** (46 nos 2 primeiros minutos) |
| Rótulos `@@` | ≥ 40% dos planos | **143 / 309 = 46%**; nenhum no 1º plano de capítulo; todos ≤ 28 caracteres |
| Cartões de data | — | 33 |
| Imagens únicas | 160–190 | **188** + thumb-base = 189 em `cenas.json` (+ 2 thumbs alternativas em `thumb-variacoes.json`) |
| Reuso | 0% até 3:00, ~40% depois | 0% até 3:00; **50% depois** (39% no total). Ver pendência 1. |
| Custo previsto | ≤ R$ 80 | 188 × ~US$ 0,042–0,055 (`medium`) ≈ US$ 7,9–10,3 + 3 thumbs `high` ~US$ 0,6 + voz ~US$ 0,3 → **~US$ 9–11 (R$ 52–64)** |

## Estrutura e loops
Hook (Tus, c. 1020: a caravana entra, o caixão sai) → "Essa é a história inteira do Irã…" + pergunta ("como um país conquistado tantas vezes nunca deixa de ser ele mesmo?") + loop ("o que salva o Irã… está dentro daquele caixão").
Capítulos: 1. O Túnel · 2. O Nome · 3. O Cilindro · 4. O Cavalo · 5. As Colunas · 6. A Flecha · 7. A Rocha · 8. O Moinho · 9. O Poema · 10. A Água · 11. O Menino · 12. O Tabaco · 13. O Poço · 14. As Fitas · 15. O Lenço · 16. O Filho · Fecho. Cada capítulo abre falando o próprio título e o anterior termina puxando o próximo ("…trazendo um nome", "…vai virar uma máquina", "…E fica gravado numa rocha", "…cabe num livro", "…começa com um diamante e termina com um narguilé", "…vai dar uma festa").

| Loop | Aberto | Pago |
|---|---|---|
| Caravana/caixão ("o que salva o Irã está no caixão") | N001–N005 (0:00–0:33) | N048–N051 (~7:07–7:40, ~48% do vídeo): "Lembra da caravana?" + detalhe que faltava (a carga era anil, 60 mil dinares; a filha recusa) + "Era isso que estava no caixão… a língua" |
| O Nome ("Guarde esse nome") | N014 (~1:45) | N073 (~10:51): Reza Xá, 1935, "Lembra do nome?" |
| O Tabaco ("Guarde esse tabaco") | N069 (~10:15) | N081 (~12:05): "Lembra do tabaco? De novo, um turbante enfrenta uma coroa." |
| "Paraíso" | N009 | N086 (as chaves de plástico "abriam o paraíso") e no fecho |
| Fecho circular | — | N097–N102: volta a Tus (túmulo num jardim = "pequeno paraíso"), palavras persas em português (paraíso, laranja, azul, bazar, xeque) e **caravana**, de kārvān; aforismo "Exércitos conquistam o Irã. A língua do Irã conquista os exércitos."; pergunta para os comentários |

- CTA de inscrição no meio (N053, ~7:50), colado no re-hook dos mongóis.
- Vídeo da Índia citado uma vez (N065, Nader Xá e o Koh-i-Noor).
- Mito desmontado: "primeira carta de direitos humanos" (N019–N022); lendas sempre como lenda (cavalo de Dario, ouro de Crasso, caravana); estimativas como estimativa (44%, mortos mongóis, guerra Irã–Iraque, chaves de plástico). 2025–2026: só o que está no BRIEF, com "até a gravação deste vídeo".

## Storyboard
- Personagens com descrição fixa entre prompts (constantes no topo do bloco de roteiro: FERDOWSI meia-idade/velho, CIRO, DARIO, SHAPUR, ISMAIL, NADER, NASER, REZA, MOSSADEGH, XÁ 1971, KHOMEINI) e figurino por época (aquemênida, parta, sassânida, safávida, Qajar, Pahlavi, moderno). Nenhuma bandeira pedida (embaixada com "no flags"); Mahsa Amini não é retratada (vela + lenço).
- Mapas sem texto, com rótulos em `src/labels.jsx`: `map_plateau`, `map_iran_name`, `map_pars`, `map_satrapies`, `map_royal_road`, `map_arabic`, `map_shia_sunni`, `map_caucasus` (posições estimadas; conferir depois de gerar).
- Thumb: `thumb-base` (Portão de Todas as Nações em Persépolis à esquerda, céu livre à direita) em `cenas.json`; `thumb-variacoes.json` com `thumb-v2-guia` (Praça de Isfahan + bonequinho-guia espantado) e `thumb-v3-ciro` (Ciro em destaque diante de Persépolis).

## Pendências
1. **Reuso de 50% depois dos 3 min** (meta ~40%). Com 18–20 cortes/min e o teto de 190 imagens, 40% exigiria ~212 imagens. Escolhi respeitar o teto; o reuso extra vem do próprio `roteiro.py` (mesma imagem com outro enquadramento dentro do bloco). Se o Rodrigo preferir 40%, são +24 imagens (~US$ 1–1,3).
2. Desfecho da anedota em ~11 s pela estimativa (meta ≤ 10 s). A voz por frase costuma ser um pouco mais rápida dentro da frase; confirmar no áudio da etapa 2.
3. Posições dos rótulos de mapa são estimadas pelo prompt: ajustar no `labels.jsx` depois de ver as imagens.
4. Reconfirmar na véspera de publicar a frase "até a gravação deste vídeo, não há acordo de paz" (N096).
5. Prompts com risco de texto inventado pela IA: `manuscript_pages`, `elamite_tablet`, `silver_beaker`, `cylinder_museum` (escrita cuneiforme/sinais). Conferir no QA.

## Melhorias sugeridas
1. Gravar o hook (N001–N005) primeiro e medir: se o desfecho passar de 10 s, cortar "carregada de riquezas" → "de riquezas".
2. Medir a retenção aos 30 s do 003 contra Egito/Índia, para validar a **Hipótese** do hook curto por anedota (`conhecimento/hooks.md`).
3. Rodar no `roteiro.py` uma checagem de frases com mais de 16 palavras (hoje ~15 frases passam disso, todas por causa de datas por extenso). Partir datas como frase própria ("Mil novecentos e setenta e um. O xá…") funcionou bem nos blocos N078, N089, N093 e N094.
