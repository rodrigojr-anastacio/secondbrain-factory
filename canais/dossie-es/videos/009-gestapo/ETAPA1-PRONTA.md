# ETAPA 1 PRONTA · dossie-es 009 · La Gestapo (15/11/2026, Opus)

`youtube.videos` id **41** (status `roteiro`, título = T1). Publica qua 18/11. Teto **US$ 12** (fal + Fish + Runpod). Etapa 1: US$ 0 pagos.

## Embalagem aprovada (crivo r1, 3 de 3, sem reprovação; `CRIVO.md`)
- **T1 (título A):** GESTAPO: La policía secreta de Hitler y sus hombres en Sudamérica (65 car.)
- **T2 (título B):** Cómo funcionaba la Gestapo: del sótano de Berlín a un nombre falso en Bolivia (77 car.)
- **Thumb:** sobretudo de couro preto **vazio** num cabide (≈55% à esquerda), janelinha com o Illimani/La Paz pequena e nítida (ou fora), parede papel `#E9DFC9`; "GESTAPO" preto à direita no alto; **sello vermelho "1983"** inclinado sobre o peito do casaco, menor que a sigla e sem alinhar com ela; aba "EXPEDIENTE Nº 009". Sem pessoa, insígnia, braçadeira, águia, suástica; único vermelho = o sello. O casaco tem de parecer de agente (couro brilhante, cinto, lapelas largas, fedora no gancho), não roupa de loja.
- **Promessa:** a história inteira da Gestapo em expedientes: como uma polícia pequena vigiava um país desde um porão de Berlim, e como seus homens acabaram com outro nome em Sudamérica, começando pelo empresário que a Bolívia prendeu em 1983.

## Onde o roteiro paga (tempos estimados; reescalar pela voz)
| Obrigação | Bloco | Tempo est. |
|---|---|---|
| Hook La Paz 1983 → Altmann → Montluc → era Barbie | N001–N005 | 0:00–0:27 |
| Frase-âncora "Esta es TODA la historia de la Gestapo. Y de cómo sus hombres llegaron a Sudamérica." | N006 | 0:27–0:34 |
| "del sótano de Berlín" (Prinz Albrecht 8, celdas no porão) | N009 | 0:49 |
| "cómo funcionaba": custódia sem juiz, fichário, denúncias (Gellately) | exp. 1–3 | 0:34–3:18 |
| 1º expediente de Sudamérica (Olga Benário, Brasil) | exp. 4, N029 | 3:18 |
| Eichmann/Argentina · Barbie em Lyon/Izieu | exp. 5 · 7–8 | 4:27 · 6:16–8:14 |
| "nombre falso en Bolivia" (Altmann, rota, Bolívia, Klarsfeld) | exp. 10–12 | 9:00–11:20 |
| Hook pago (expulsão 1983, Montluc, julgamento 1987) | exp. 13 | 11:20 |
| Priebke/Bariloche · cierre "La Deuda" (pretexto; Lyon e Izieu) | exp. 14 · cierre | 12:15 · 13:18 |
Sobretudo de couro (rima com a thumb): plano `coat_hook` no hook (N005), N045, N103 e no cierre.

## O que está pronto
| Arquivo | Conteúdo |
|---|---|
| `roteiro.py` | fonte única (roteiro + planos); geração copiada do 008 |
| `SCRIPT.md`, `blocos.json` | **1.954 palavras, 107 blocos**, hook + 14 expedientes + cierre; **~13:52 estimados** (832 s, WPS 2,38; o real costuma sair 1–3% acima: ~14:10) |
| `STORYBOARD.md`, `storyboard.json` | 292 planos, média 2,85 s, 25 cortes no 1º minuto, 0 reuso antes de 3:00, 48% de reuso depois; **0 avisos** |
| `cenas.json` | **184 imagens do vídeo + 3 bases de thumb = 187** (todas com SANGRIA) |
| `FATOS-revisao.md`, `ES-revisao.md` | checagem de fatos (20 correções) e revisão nativa/sensibilidade; **já aplicadas** |
| `SOURCES.md` | correções, por que este hook, fontes para a descrição |
| `BRIEF.md`, `EMBALAGEM.md`, `CRIVO.md`, `embalagem/` | pesquisa, embalagem e crivo |

Checklist da bíblia: hook ~34 s est. com anedota própria (não a viúva do Archive), desfecho seco e "Esta es TODA la historia" ✔ · 14 expedientes com título falado, cada fim puxa o próximo ✔ · anedota paga no exp. 13 e no cierre "La Deuda" ✔ · acusações atribuídas (relatório do DoJ, "según investigaciones periodísticas", Morais) ✔ · ângulo América Latina (Bolívia, Brasil, Argentina) ✔ · revisão nativa ✔ · CTA no meio (fim do exp. 7, ~7:19, colado no re-hook do télex) ✔ · sem gancho de próximo vídeo (menção ao expediente do **Mossad, já publicado**) ✔ · nenhum capítulo do Archive repetido como objeto ✔.

## O que a etapa 2 precisa saber
1. **Não reescreva o roteiro.** Edite só `roteiro.py` e rode `python3 roteiro.py`.
2. **Hook:** ~34 s estimado. Se a voz passar de 35 s, corte "Días después," (N003) ou junte N003 ao N004.
3. **Voz (Fish, conforme `canal.yaml`):** glossário em `ES-revisao.md` → "Pronúncia para o Fish", **só no texto mandado à voz** (Göring "Guéring", Himmler "Jímler", Heydrich "Jáidrik", Würzburg "Vúrtsburk", Geheime Staatspolizei por sílabas, Keitel "Káitel", Eichmann "Áikman", Getulio "Jetúlio", Izieu "Isié", Moulin "Mulán", Montluc, Caluire, Draganović, Klarsfeld, Priebke, Ardeatinas, "IV B4" = "cuatro be cuatro", Auschwitz "Áushvits"). Confira no Whisper "TODA" sem grito e a citação de Keitel.
4. **Imagens (nano-banana, 187):** custo do 008 (186) foi ~US$ 9,5 → teto US$ 12 justo: gere uma vez, refaça só o reprovado. Moldura/letterbox: `tools/checa_imagens.py` + `recorta_moldura.py` + `recorta_branco.py`. Riscos deste tema:
   - **símbolos nazistas**: todo prompt com uniforme/escritório leva `NOINS`; confira de perto suástica, águia, runas, braçadeira, bandeira (reprovar e refazer);
   - **corpos**: nada de vítimas visíveis (fumaça/vazio); Izieu só com objetos (sala, mesa, sapato, desenho);
   - **texto inventado** em decretos, télex, relatórios, documentos (`SEM`);
   - pessoas reais "resembling" (Barbie jovem/velho, Göring, Himmler, Heydrich, Müller, Olga, Prestes, Vargas, Filinto, Eichmann, Keitel, Moulin, Draganović, Banzer, Priebke): conferir que não saiu caricatura nem insígnia;
   - `old_young` (split jovem × velho) é plano-chave: refazer até ficar convincente.
5. **Mapas (pinos/setas no código, `src/labels.jsx`):** `map_atlantico` (exp. 4: seta RÍO DE JANEIRO → HAMBURGO; reuso no exp. 11: GÉNOVA → BUENOS AIRES → LA PAZ) · `map_europa` (fim do exp. 4: só BERLÍN; exp. 6: setas de FRANCIA, BÉLGICA, HOLANDA → ALEMANIA). Conferir pinos num still.
6. **Cartões de data:** LA PAZ 1983, BERLÍN 1933, BERLÍN 1934, WÜRZBURG 1939, RÍO DE JANEIRO 1936, BERLÍN 1939, BUENOS AIRES 1950, 1941, LYON 1942, IZIEU 1944, 1945, NÚREMBERG 1946, ALEMANIA 1947, GÉNOVA 1951, 1971, LA PAZ 1972, LA PAZ 1983, LYON 1987, BARILOCHE 1994, LA PAZ 1983 (cierre). 15 rótulos de nome (≤ 30 car.).
7. **Thumbs:** bases `thumb-A/B/C` em `cenas.json` (sem texto); texto no `src/Thumbnail.jsx`: A e B = "GESTAPO" + sello "1983" + aba "EXPEDIENTE Nº 009"; C = variação (pode testar sello "LA PAZ 1983"). Nunca mudar o conceito. Conferir a base de perto (código de cor escrito no canto, gotas vermelhas, insígnias).
8. **Pacote (A/B/C):** A = T1 ↔ thumb-A; B = T2 ↔ thumb-B; C = variação de T1/T2 (ex.: "GESTAPO: del sótano de Berlín a Sudamérica") ↔ thumb-C. Título/descrição/tags sem muerte/murió/asesinato/masacre. Fontes da descrição em `SOURCES.md`; nota de voz sintética + IA conforme a regra vigente do `pacote-youtube` (padrão de 14/11: sem menção a IA no texto).
9. **QA:** na `legendas.srt`, a frase-âncora ≤ 0:35, "sótano" ≤ 1:00, "El Barco" (Sudamérica) ≤ 3:30; thumb final contra o conceito.
10. Capítulos estimados (reescalar): 0:00 Hook · 0:34 · 1:26 · 2:19 · 3:18 · 4:27 · 5:28 · 6:16 · 7:28 · 8:14 · 9:00 · 9:36 · 10:24 · 11:20 · 12:15 · 13:18 Cierre.
11. Entrega em `entrega/` (sem Drive), status até `pronto`, aprendizados na bíblia.

## Pendências (menores, contornadas)
- Relatório Ryan e Gellately conferidos por fontes secundárias (o PDF do DoJ é escaneado); Morais não consultado diretamente (a frase de Filinto Müller está atribuída a ele).
