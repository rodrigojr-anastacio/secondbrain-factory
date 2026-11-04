# Amostras de voz v2 do 003: s2.1-pro × drama-3 (04/11/2026)

**Por que:** o Rodrigo achou a narração do 003 "lida corrida, e não contando uma história". Das amostras antigas (`../../amostras-voz/`), ele prefere a A (1 chamada por bloco). Ele quer ouvir o modelo mais recente do Fish, que é o **`drama-3`** (lançado em 13/10/2026; US$ 10/M bytes na promoção até 12/11, depois US$ 50/M). Pesquisa e parâmetros em `FISH-MODELOS.md`.
**Texto:** `abertura-atual.txt` traz os blocos N001–N007 do `blocos.json`, com as tags originais, cerca de 50 s (hook + começo de "O Túnel").
**Voz:** clone `48613fc675f84984981683d92266e543`, velocidade 1,0, temperature e top_p no padrão (0,7).
**Como reproduzir:** `gerar.py` (geração com custo registrado) e `medir.py` (medidas; mesma conta do `../../amostras-voz/melodia.py`, conferida com ele). Os parâmetros de cada amostra estão no `.json` ao lado do mp3, e o cache de cada chamada fica em `.partes/`.

## Amostras
| Letra | Arquivo | Texto | Modelo | Técnica | Parâmetros | Dur. | ppm | pausas ≥ 0,25 s | F0 mediana | F0 faixa p10–p90 | **repetição melódica** ↓ | queda no fim | Whisper |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | `A-atual-referencia.mp3` | atual | s2.1-pro | bloco (1 chamada por bloco) | gaps de 0,35 s, ou 0,9 s antes de "§" (N003, N006) | 49,3 s | 148 | 21 | 96,7 Hz | 9,1 st | 0,23 | −4,2 st | 97,5% |
| B | `B-drama-3-texto-atual.mp3` | atual (mesmas tags `[curious]` e `[serious]`; a sintaxe de colchetes é a mesma no drama-3) | **drama-3** | bloco | idem A | 57,8 s | 127 | 25 | 107,0 Hz | 10,8 st | 0,34 | −6,0 st | 99,2% |
| B2 | `B-drama-3-texto-atual-take2.mp3` | atual | drama-3 | bloco | idem, 2ª tomada (mede o ruído) | 58,3 s | 125 | 27 | 110,0 Hz | 10,4 st | 0,30 | −5,6 st | 97,1% |
| C | `C-drama-3-texto-contado.mp3` | **reescrito** (`abertura-v2.txt`, hook HiM da `ESTRUTURA-ROTEIRO.md`) | drama-3 | único, como o D | idem D | 65,0 s | 118 | 20 | 111,4 Hz | **12,1 st** | 0,24 | −5,2 st | 100% |
| C2 | `C2-s2.1-pro-texto-contado-bloco.mp3` | **reescrito** | s2.1-pro | bloco (técnica A) | idem A | 50,8 s | 151 | 20 | 91,1 Hz | 8,9 st | 0,22 | **−3,45 st** | 100% |
| D | `D-drama-3-unico-narrador.mp3` | atual | drama-3 | **único** (trecho todo numa chamada, `condition_on_previous_chunks` padrão true) | direção no início: `[warm storyteller telling an old legend to a friend, intrigued and unhurried, letting each surprise land]`; `[pause]` antes dos parágrafos "§"; quebra de linha entre parágrafos | 60,4 s | 121 | 27 | 106,8 Hz | **11,6 st** | 0,26 | −5,9 st | 98,4% |

Nenhuma tag nem direção foi falada (Whisper small). Referência antiga para comparar: `../../amostras-voz/A-atual.wav`, com o texto do hook do cavalo, mediu 0,14 / −2,4 st. **O texto atual do 003 é que mede mal** (0,23 já no s2.1-pro), como já dizia a validação no texto real em `../../amostras-voz/LEIA.md`.

## Ordem de escuta sugerida
1. **A**: referência, como está no vídeo hoje (técnica preferida pelo Rodrigo).
2. **B**: o mesmo texto e a mesma técnica, só trocando o modelo. Isola o efeito do drama-3.
3. **D**: drama-3 com direção de narrador e o trecho inteiro numa chamada. É a técnica que o drama-3 propõe.
4. **C2**: o texto reescrito na voz e técnica de hoje (A). Isola o efeito do texto.
5. **C**: o texto reescrito no drama-3 com direção de narrador. É a combinação candidata.

**Leitura das medidas de C/C2 (04/11):** o texto novo baixou a queda no fim da frase no s2.1-pro (−4,2 → −3,45 st) e, no drama-3, deu a maior faixa melódica de todas (12,1 st) com repetição de 0,24. As diferenças de repetição (0,22–0,26) estão perto do ruído. **Decida de ouvido** entre A, C2, D e C. O C fala devagar (118 ppm); se ganhar, o vídeo inteiro fica ~20% mais longo com o mesmo texto, e aí convém `prosody.speed` 1,1 ou cortar ~15% do texto.

## O que as medidas dizem (Hipótese; quem decide é o ouvido)
- **O drama-3 muda bastante a leitura.** Ele fala 15–18% mais devagar (121–127 ppm, contra 148), com mais pausas e faixa melódica maior (10,4–11,6 st, contra 9,1). A voz sai **mais aguda** (~+1,7 st), então confira se continua parecendo a voz do canal.
- **Por bloco, o drama-3 repetiu mais a "musiquinha"** (0,30–0,34 contra 0,23) e caiu mais no fim das frases (−5,6/−6,0 contra −4,2 st). Isso passa do ruído entre tomadas (~0,02–0,04). Em outras palavras, ele dramatiza cada frase curta com a mesma cadência de fecho.
- **D (direção de narrador + chamada única)** volta a repetição para o nível do A (0,26) e tem a maior faixa de F0. É o candidato mais "contado" na medida. Ressalva: numa chamada única não há controle de pausa. O `[pause]` antes de "O Túnel" não segurou, e o Whisper ouviu "…daquele caixão, o túnel". Para pausa garantida, use `bloco` ou `paragrafo` com `--direcao`.
- Para o vídeo inteiro (~15 min, ~13 mil bytes), o drama-3 custa ~US$ 0,13 até 12/11 e ~US$ 0,65 depois (no s2.1-pro, ~US$ 0,20).

## Como gerar a C (orquestrador)
Escreva `abertura-v2.txt` aqui: um parágrafo por bloco, linha em branco entre eles, "§ " no início do parágrafo que abre ideia nova, e tags `[..]` só onde a emoção muda. Depois rode, nesta pasta:
```
~/workspace/fabrica-youtube/tools/.venv/bin/python gerar.py abertura-v2.txt C-drama-3-texto-contado.mp3 --modelo drama-3 --tecnica unico --direcao "[warm storyteller telling an old legend to a friend, intrigued and unhurried, letting each surprise land]" --pausa-tag "[pause]"
~/workspace/fabrica-youtube/tools/.venv/bin/python medir.py C-drama-3-texto-contado.mp3
```
(Para comparar com o B na mesma técnica: `--tecnica bloco` sem `--direcao`, saída `C-drama-3-texto-contado-bloco.mp3`.) Cada take custa ~US$ 0,01. O custo vai para `financas.consumo` (ref_id 5, notas 'v2 amostras voz').

## Custo desta parte
US$ **0,054** no total (8 linhas; C US$ 0,0088 e C2 US$ 0,0111 foram lançados depois pelo orquestrador, mais as 6 linhas em `financas.consumo`, notas 'v2 amostras voz', ref_id 5): 2 chamadas de teste do clone (US$ 0,0012), A (0,0105), B (0,0070), B2 (0,0070) e D (0,0083). A queda do crédito no Fish bateu com o preço promocional do drama-3, como explicado em `FISH-MODELOS.md`.
