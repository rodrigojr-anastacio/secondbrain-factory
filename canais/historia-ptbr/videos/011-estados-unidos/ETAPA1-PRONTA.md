# ETAPA 1 PRONTA · historia-ptbr/011 Estados Unidos · youtube.videos id 44 · 16/11/2026

Pasta: `canais/historia-ptbr/videos/011-estados-unidos/` · `youtube.videos` id **44** (`status='roteiro'`, `biblia_versao='v2'`, título = T1). Etapa 1 (Opus) concluída: pesquisa, ângulo, **embalagem aprovada no crivo (r3)**, roteiro v2 com checagem de fatos (checklist APROVADO), detector de cópia, crivo de ângulo, storyboard e `cenas.json`. **Nada de voz, imagem ou render foi gerado. Custo pago: US$ 0.**

## Ângulo (ANGULO.md)
**A promessa cobrada:** os EUA nasceram de uma frase que não cumpriam ("todos os homens são criados iguais"); cada geração foi cobrá-la, e cada cobrança paga obrigou o país a deixar mais gente entrar (e ele cresceu com isso). **Detector de cópia: 1/100** (limite 30). **Crivo de ângulo: APROVADO na r1** (95% → 100% de cenas próprias depois do ajuste do cap. 9 recomendado pelo revisor).

## Embalagem aprovada (CRIVO.md = embalagem/crivo-r3.md, rodada 3 de 3)
| par | título | padrão do título | thumb (padrão) | texto |
|---|---|---|---|---|
| A | "Os EUA prometeram o que NÃO cumpriam. Como viraram potência?" (60) | afirmação estranha + pergunta | `rosto-emocao` (controle): Douglass bonequinho indignado, **do lado de fora** no escuro, apontando para a festa do 4 de Julho na janela iluminada | "IGUAIS?" |
| B | "Como UMA FRASE construiu os Estados Unidos" (42) | Como [coisa concreta] construiu [lugar] | `objeto-simbolo`: o Sino da Liberdade sozinho, enorme, rachadura acesa em ouro, fundo preto, bronze sem letras | "LIBERDADE" |
| C | "Como 13 colônias viraram potência? A resposta é uma PROMESSA" (60) | ascensão + fato-surpresa | `antes-depois`: Independence Hall em 1776 (sépia, rua de terra) × 2026 (entre arranha-céus), divisão vertical, 2 bases unidas no código | "1776" · "2026" |
- r1 reprovou só a Thumb B (pergaminho rasgado: refs sem objeto dominante, a Declaração nunca foi rasgada); r2 reprovou só a âncora da Thumb B nas Obrigações (o nome do sino veio em 1835, antes da rachadura). Conceitos completos e referências em `EMBALAGEM.md`.

## Promessa e onde o roteiro a paga (tempos estimados a 126 ppm; conferir na `legendas.srt`)
- **Promessa:** como um país fundado numa frase que ele mesmo não cumpria virou a maior potência do mundo: cada cobrança obrigou o país a deixar mais gente entrar.
- **Hook:** N001–N003 (0:00–0:35) Douglass em Rochester, 5/7/1852, "o que é, para o escravo, o seu Quatro de Julho?" (paga a Thumb A) → **N004 (0:35) pergunta central** → N005 (0:52) "o Sino da Liberdade já está rachado e mudo… o que está escrito pode ser cobrado" → N006 (1:04) "Essa é a história inteira dos Estados Unidos" + "Guarde a pergunta de Douglass" → cap. 1 em ~1:17 (checklist a 130 ppm: 1:13).
- **T2 (a frase):** N013 (2:33) Jefferson escreve "todos os homens são criados iguais"; N015 (2:59) o parágrafo cortado; N018 (3:40) **1ª peça da resposta**; fecho N064 (15:18) "Construiu o país porque estava escrita, para todos, e qualquer um podia cobrar".
- **Thumb B (sino):** N005 (0:52) e **N030–N031 (6:22–6:50)**: "Os abolicionistas deram ao sino o nome de liberdade. Poucos anos depois, ele rachou. E em mil oitocentos e quarenta e seis, calou para sempre."
- **Thumb C (Independence Hall):** N006 (1:04), N015 (3:00), N020 (4:04, "no mesmo prédio de tijolos"), N041 (9:18, Centenário) e fecho N065 (15:36, `hall_today`, 2026).
- **T3 (13 colônias → potência):** N010 (treze colônias), N044 (10:02, "a outra metade da nossa pergunta, a potência"), N056 (13:15, metade da produção mundial), fecho.
- Peças da resposta: N018 (3:40), N034 (7:24), N060 (14:11); "lembra da nossa pergunta?" N063; guarde pago em N065 (15:36).

## Números
| Item | Valor |
|---|---|
| Palavras / blocos | 2.008 / 66 (hook + 10 capítulos + fecho) |
| Duração estimada | ~16:04 no gerador (126 ppm); ritmo real 006–010 → ~15:40–16:10 |
| Checklist v2 | **APROVADO** (pergunta 0:34, volta 5×, conectivos 1,74, "você" 1,05, ponte 10/10, 1 "guarde", cap. 1 em 1:13, fecho 0:44; ritmo só depois da voz) |
| Imagens planejadas | **248** únicas (308 planos; reuso 0% até 3:00, 24,6% depois; 23 cortes no 1º min; 2 rótulos) + bases das 3 thumbs (A: 1, B: 1, C: 2) |
| Voz | `texto` = 11.623 bytes ≈ US$ 0,12 por passada no drama-3 (US$ 10/M até 30/11/2026) |

## O que a etapa 2 precisa saber
1. **Código:** `src/` e `tools/` vieram do 010 e ainda têm 010/Japão: `tools/build.py`, `tools/render_parte.sh`, `tools/render_resto.sh` (`010-japao`, `VIDEO=40`), `src/Video.jsx` e `src/index.jsx` (composição `Japao`), `src/labels.jsx` (rótulos do Japão). Troque para `011-estados-unidos` / `VIDEO=44` / composição `EstadosUnidos`; rótulos de mapa: `map_13_colonies` ("13 COLÔNIAS, 1776"), `map_usa_today` ("ESTADOS UNIDOS"), `map_louisiana` ("LUISIANA, 1803"), `map_1765`, `map_georgia`/`map_trail` ("NAÇÃO CHEROKEE"), `map_split` ("UNIÃO" × "CONFEDERAÇÃO"), `map_states_1920` ("TENNESSEE"). Trilha: sugestão folk americano (violão/banjo/rabeca sintetizados) nos caps. 1–7, piano/metais nos 8–10, piano esparso nos trechos graves (remoção cherokee, Guerra Civil, Pearl Harbor).
2. **3 thumbs, uma por conceito** (A/B/C = T1/T2/T3), nunca variações. **Douglass em 1852 tinha cabelo escuro** (34 anos): use a cabeleira **escura** volumosa (o "grisalha" do prompt-exemplo do EMBALAGEM.md está errado). Thumb A: manter o gesto de apontar, a janela iluminada e a paleta azul-noite (ressalva do crivo r3: não ficar gêmea do "DE NOVO?"); conferir na maquete 320×180 que "o excluído aponta para a festa" lê sem legenda. Thumb C: 2 bases no mesmo ângulo, divisão no código. Registrar de novo os pares com os arquivos finais (`embalagem_variantes.py registrar`).
3. **Imagens pelo Codex** (fallback fal), um processo só, `--video 44`. **Lote-prova de 6:** I005 `douglass_stage` (cartoon, sem rosto realista), I025 `hall_1776` (prédio certo, sem bandeira/arranha-céu), I020 `bell_crack` (bronze sem letras), I072 `statue_fall` (estátua dourada derrubada, sem bandeira), I114 `trail_winter` (de longe, sem corpo), I235 `king_podium`. **Conferir um a um os planos graves**: escravidão (I036 `point_comfort`, `tobacco_field`, `cabins_row`, `cotton_field`: constante `ESCRAV`, sem corrente/chicote/ferida), Guerra Civil (I139, I149: sem corpos), 1941–45 (I204–I225: `SEMSIMB`), `wall_1991` (estrela de pedra, sem foice/martelo). Bandeiras: nenhuma em close; bunting sem estrelas. Datas: nada de arranha-céu antes de 1890, carro antes de 1900, Estátua da Liberdade antes de 1886.
4. **Voz:** drama-3, 1 chamada por bloco. Testar antes os nomes da lista `FALA` (NÃO testadas): Rochester "Rótchester", Frederick Douglass "Frédérik Dâglas", Jamestown "Djêimstáun", White Lion "Uáit Láion", Jefferson "Djéferson", Abigail Adams "Ábigueil Édams", Sequoyah "Sicóia", Cherokee "Tcherokí", Andrew Jackson "Éndru Djéquisson", Seneca Falls "Sêneca Fóls", Elizabeth Cady Stanton, Gettysburg "Guétisburg", Lincoln "Líncoln", Susan B. Anthony, Wong Kim Ark "Uóng Quim Árk", Woodrow Wilson, Tennessee "Ténessi", Harry Burn "Rári Bârn", A. Philip Randolph, Roosevelt "Rôusvelt", Pittsburgh, Pearl Harbor, Martin Luther King. Troque no `FALA` e rode `python3 roteiro.py` (nunca edite `blocos.json` à mão). Tom: `[serious]` no hook; sóbrio em N028 (remoção), N036–N039 (Gettysburg/guerra) e N055 (tropas segregadas).
5. **Pacote:** A = T1, B = T2, C = T3 com o padrão de cada par; duração na descrição (nenhum título tem "em N minutos"); sem palavras proibidas; sem menção a IA; fontes de `SOURCES.md`.
6. **QA:** na `legendas.srt`, pergunta ≤ 0:50, Douglass e "Quatro de Julho" no hook, sino em N005 e N030–N031, "primeira peça" (~3:40), fecho ≤ 45 s; cada thumb final contra o seu conceito.
7. **Teto US$ 8:** voz ~0,15–0,5 (com tomadas e teste de nomes) + Codex US$ 0 (fallback fal US$ 0,046/img) + render Runpod ~0,2.
8. **Neutralidade:** fecho com 1 frase sobre os 250 anos (4/7/2026), sem política atual; sem anúncio de próximo vídeo.

## Pendências
- Grafias de voz e posições dos rótulos (`src/labels.jsx`) não conferidas (dependem de voz/imagens).
- `watch.py` não rodou na referência (a transcrição completa veio do `manada.py`; frames/cortes por minuto não medidos).
