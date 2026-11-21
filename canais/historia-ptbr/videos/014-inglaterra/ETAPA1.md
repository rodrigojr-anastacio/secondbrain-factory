# ETAPA 1 · historia-ptbr/014-inglaterra · 20/11/2026
Vídeo `youtube.videos` id 52 (`biblia_versao='v2'`, status `roteiro`, título = T1). Custo pago da etapa: US$ 0 (+ ~US$ 0,01 de Haiku no detector). Cota YouTube Data API: 110 unidades (search.list: 0).

## Pesquisa e ângulo
- Manada: 16 transcrições (`ref/manada-*.txt`, fora do git) em 3 buscas: tema, recorte do backlog ("ilha / nunca invadida desde 1066") e recorte vizinho do ângulo novo ("família real alemã", "1688 invasão"). Consenso em `ref/consenso.md` e `ANGULO.md`.
- **Ângulo do backlog descartado:** "o Canal protege → frota → império; o avião acaba com a muralha" repete o esqueleto do nosso 010 Japão ("Como o MAR protegeu o Japão") e se apoia no mito "ninguém invade desde 1066" (1216, 1688, 1797). O recorte só tem vídeos en com < 1.200 views.
- **Ângulo escolhido: "a coroa que vem de fora"** — 6 coroas para gente de fora (Canuto, Guilherme I, Henrique II, Jaime I, Guilherme III, Jorge I); cada rei de fora paga com um pedaço de poder no papel; o papel vira Parlamento → crédito (1694) → frota → império. Nenhum vídeo da manada liga os 6 nem usa o "preço" como motor (o 37hG tem "Parlamento forte → império", sem os reis de fora).
- Fatos: `ref/fatos-checados.md` (44 itens, 2 checagens) → `SOURCES.md`.

## Embalagem (crivo)
- r1: REPROVADO 1/3 — Thumb A (decalque do 007-1 "UM VIKING NO TRONO?" + erro de fato: Jaime esperava a sucessão), Thumb B (frota de 1688 = cena da manada, ilegível a 320 px), obrigações vagas.
- r2: REPROVADO 2/3 — Thumb A (lorde horrorizado = decalque do 013-A; "ELE" irreconhecível).
- r3: **APROVADO 3/3.** A/T1 "A Inglaterra IMPORTAVA reis. Como mandou em 1/4 do mundo?" + `rosto-emocao` (Jaime VI de manta xadrez se coroando, "MINHA!"); B/T2 "Como reis de FORA deixaram a Inglaterra mais forte" + `cena-acao` (coroação de Natal de 1066 com fogo, "NATAL DE 1066"); C/T3 "Inglaterra, o país que dava a COROA a estrangeiros" + `documento-evidencia` (Declaração de Direitos circulada, "O PREÇO"). Registrado em `youtube.embalagem_variantes`.

## Roteiro (v2)
- 70 blocos, **2.212 palavras**; estimativa da ferramenta 17:41 a 2,1 pal/s, mas o ritmo real medido nos 011–013 é ~130 ppm (2.138 palavras → 16:28 no 012) → **~17:00 real**. Hook até o cap. 1: 1:09. Fecho 0:42. Sem "em N minutos" no título.
- Pergunta central: "Como um país que vivia buscando rei lá fora acabou mandando em um quarto do mundo?" (0:25). Volta 5× (N024 1ª peça, N043, N049 2ª peça, N061 3ª peça, fecho).
- Fio: a coroa que vem de fora + o papel cobrado. "Guarde" único: a promessa no estandarte de 1688 (N045) → paga no juramento de Carlos III (N067).
- Checklist v2 (`checklist_roteiro_v2.py`, estimado a 130 ppm):
```
  1 PASSA    Pergunta central declarada / até ~0:50 (0:25 em N003)
  2 PASSA    Pergunta volta em voz alta 5× (≥ 3)
  3 PASSA    Conectivos 1,72/100 (38) · capítulo fecha com problema 10/10 · sucessão seca 0
  4 PASSA    "Você/imagine" 1,08/100 (24) · ponte 10/10
  7 PASSA    "Guarde" 1 · 8 PASSA hook 1:09, promessa em lista: nenhuma
 11 PASSA    Fecho 0:42
 ok          falas de personagem 2 (indiretas; aviso da regra 9) · 11,8 palavras/frase · capítulo abrindo com data 0
Resultado: APROVADO
```
- Manuais: cena antes dos fatos em todo capítulo (Canuto no trono; coroação; Ruão; Westminster 1362; Henrique VIII e o papa; Comuns 1604 + Hampden 1637; estandarte 1688; regras de 1701; medalha 1804; Washington 1945); humor seco (lei do inglês escrita em francês, "imagine o fiscal contando as suas galinhas", Walpole recusando o título, faixa de campeão antes da final, quitar em 2006 a conta de 45); teste da troca: cada capítulo nasce do problema do anterior.
- **Detector de cópia: 2/100** (máx. 1,6 × lon75v0e7_s). **Crivo de ângulo: APROVADO na r1** (16/20 cenas próprias = 80%); recomendação aplicada depois: Carlos I/11 anos (cena da 37hG) trocado pelo caso Hampden (1637) como abertura do cap. 6 → 17/20 (85%); detector refeito: 2/100.
- Correções de fato feitas no roteiro: ordem das línguas na coroação (francês = Geoffrey de Coutances; inglês = Ealdred); "parente normando" (não primo); Elizabeth "quase 45 anos"; "sete ingleses poderosos" (6 lordes + 1 bispo); Declaração lida antes da coroa (não dita como condição); "teve de aceitar por escrito"; Jorge I "fala pouco inglês e prefere o francês" (sem o mito); Walpole com a ressalva do título.

## Storyboard
- 333 planos, média 3,19 s, 23 cortes no 1º minuto, **202 imagens** (`cenas.json`), reuso 39% (0% antes de 3:00; 49% depois — um pouco acima dos ~40% da bíblia para caber no teto), 28 rótulos `@@`, 0 avisos.
- 100% dos prompts ancorados (ING/LON/ESC/FRA/MOD + NAO_EG) contra o vazamento das refs do Egito (lição do 013: 17/199 refeitas sem âncora). Mapas sem letras (`MAPA`), documentos com `PAPEL` (linhas ilegíveis), `SEMBAND` e `GUERRA`.
- Custo previsto: Codex US$ 0; se tudo caísse no fallback fal, 202 × US$ 0,046 ≈ US$ 9,3 (> teto de US$ 8) → a etapa 2 não deve deixar o lote inteiro no fal.

## Pendências (não bloqueiam)
- Texto exato do estandarte de 1688 não confirmado (roteiro diz "segundo os relatos"; imagem sem letras).
- Data em que Jorge I deixou o gabinete é incerta (roteiro diz "com o tempo").
- Regra 9 (1–2 falas curtas em discurso direto) só como aviso: falas estão em discurso indireto.
