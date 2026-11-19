# ETAPA 1 · dossie-es/012-mi6 · El MI6 · 18/11/2026 (Opus)
Custo pago da etapa 1: **US$ 0** (só tradução do detector, ~US$ 0,02 pela API de rotinas). `youtube.videos` id 51: título = T1, status `roteiro`.

## Ângulo e manada
- **Ângulo (`ANGULO.md`):** a história inteira do MI6 contada pelos papéis que fabricou, vazou ou fez sumir, com o miolo nas Américas (BSC 1940–41). Manada: 8 vídeos transcritos (Archive in Minutes `zDaBuuCTCg0`, 2 clones es, 1 clone en, Atlas del Tiempo, Archivo Desclasificado, Infographics, Into the Shadows); **nenhum** tem o MI6 nas Américas, Zinoviev, Crabb ou Exocet.
- **Detector de cópia (`SIMILARIDADE.md`): 6/100** (ok; máx. com o clone Archivo Minuto; os gêmeos são 1909, Philby e Chilcot, fatos obrigatórios).
- **Crivo de ângulo: APROVADO na r1** (`CRIVO-ANGULO.md`): 10 de 12 expedientes fora da manada (83%; meta 50%). Ressalvas aplicadas: exp. 1 abre direto no diário de Cumming; exp. 9 (Macmillan/Philby) reclassificado como "manada" no `SOURCES.md`.

## Embalagem (crivo r3, 6 de 6)
| par | título | thumb (padrão) | texto |
|---|---|---|---|
| A | MI6: el plan nazi para Sudamérica que nadie escribió en Berlín | máquina de escrever no escuro (`objeto-simbolo`, controle) | NUEVA YORK |
| B | Cómo el MI6 engañó a un presidente, a un país y a sí mismo | Roosevelt aos microfones com a folha do discurso riscada (`rosto-emocao`, **teste personagem do tema**) | ¿SABÍA? |
| C | El Complot Nazi que Nunca Existió \| Expedientes Secretos del MI6 | o mapa forjado em 5 blocos sendo traçado (`mapa-lugar`) | 14 → 5 |
Reprovações: r1 (T2 só pago pelo bloco 1940–41 e apoiado no Zimmermann; Thumb B com cena inventada — Roosevelt nunca exibiu o mapa — e cópia de Los Porqués; Thumb C com Rockefeller ilegível a 320×180); r2 (Thumb B: texto vermelho sobre ardósia ~1,1:1 e pasta genérica). Registrado em `youtube.embalagem_variantes` (objeto-simbolo, rosto-emocao, mapa-lugar).

## Roteiro
- **1.922 palavras, 67 blocos, hook + 12 expedientes + CTA + cierre, ~13:34 estimados** (WPS 2,38; o real costuma sair 1–3% acima → ~13:50). Hook 35,7 s (84 palavras; `HOOK_MAX` 36).
- **Promessa paga:** hook N001–N004 (0:00–0:36): Roosevelt por rádio, "mapa secreto hecho en Alemania", 14 países → 5 estados vasallos, Panamá, "Berlín lo llama falsificación. Según los historiadores, lo era: el mapa salió de una oficina británica en Nueva York" (0:21–0:29) + frase-âncora "Esta es TODA la historia del MI6. Y de los papeles con que movió el mundo." (0:29–0:36).
- **T2:** presidente = hook + N036 "¿Lo sabía Roosevelt?" (6:44); país = N018 "Un país votó con un papel falso sobre la mesa" (3:12–3:23) + Bolívia (exp. 6, 5:13); a sí mismo = N048 "El servicio que engañaba a otros con papeles estaba engañado por dentro" (9:21) + N062 Chilcot (12:23).
- **T3:** N037 "No hay rastro de ese complot nazi para Sudamérica: según los historiadores, nunca existió" (7:01–7:14). **T1/Thumb A:** BSC em Nova York (exp. 4, 3:23) + a máquina de escrever feita para imitar a de Belmonte (N032, 5:47). **Thumb C "14 → 5":** N002 (0:08).
- **Fio:** cada expediente é um documento (diário, telegrama, carta, passaporte, cartas das Bermudas, assinatura, mapa, carta, comunicado, registro, identidades falsas, relatório); o mapa abre, é pago no exp. 7 e fecha o cierre.
- **Loops pagos:** quem desenhou o mapa (hook → exp. 7); "un papel bien colocado puede mover a Washington" (exp. 2 → exp. 7 e exp. 12); a carta real das Bermudas vira molde da falsa (exp. 5 → 6); engano por dentro (exp. 8 → 9).
- **Checagem de fatos** (Sonnet, `roteiro-crivo/FATOS-CHECAGEM.md`): 21 itens corrigidos/atribuídos (Cumming sem patente e "casi sin personal ni presupuesto"; Zimmermann ao representante em México via Washington, "jefe de la diplomacia"; Zinoviev = conclusão de Gill Bennett; "nueve personas meses antes"; Gardner "según Hyde" e a prisão de Ludwig sem causalidade única; Jenkins era ministro (legação) → "representante"; Hyde 1962 + "relatos posteriores" para Toronto/máquina; Station M "según el museo"; Franks "por la decisión argentina"; Exocet = Freedman, "agentes británicos"; Crabb sem a troca de chefe (Andrew contesta); Chilcot = "certeza injustificada", não engano deliberado; tirada a frase "el mapa apareció entre sus papeles privados").
- **Revisão nativa** (Sonnet, `roteiro-crivo/REVISAO-NATIVA.md`, nota 7,0): aplicada (lusismos, "Armada", "representante", "golpe de Estado", "Jruschov", Bulganin, "muertos" em vez de "caídos", "tomar las islas por la fuerza" em vez de "invasión", "la compañía alemana Cóndor", "se atribuyó el mérito", frases > 20 palavras cortadas, vírgulas antes de "y").

### Checklist da bíblia (`biblia/roteiro.md`)
- [x] Hook ≤ 35 s com anedota própria (mapa de Roosevelt: nenhuma transcrição da manada), desfecho seco e "Esta es TODA la historia del MI6" (35,7 s estimado; cortar 1 palavra se a voz passar de 36 s).
- [x] 12 expedientes de 45–75 s (exp. 11 ~78 s, exp. 7 ~73 s), cada um um documento datado, título falado; fim de cada um puxa o próximo.
- [x] Anedota paga (exp. 7, ~6:13–7:18 ≈ 46% do vídeo) e cierre volta ao mapa + aforismo + pergunta.
- [x] Toda acusação atribuída (historiadores, museu, Hyde, BSC, Bennett, Freedman, Chilcot, Londres); ângulo América Latina = 7 de 12 capítulos (México, Bermudas, Bolívia, mapa, Brasil, Malvinas, NY).
- [x] Revisão nativa feita; nenhuma palavra em português.
- [x] `SIMILARIDADE.md` 6 < 30, `CRIVO-ANGULO.md` APROVADO, 83% fora da manada (lista no `SOURCES.md`).

## Storyboard
- **263 planos, 191 imagens novas + 3 bases de thumb = 194**, reuso 27,4% (35,8% depois de 3:00; 0% antes), 23 cortes no 1º minuto, plano médio 3,1 s, 26 rótulos. Aviso único: N061 ("Las armas nunca aparecieron.") com plano de 1,8 s (intencional).
- Mapas sem texto (pinos/nomes no `labels.jsx`, etapa 2): `map_14` (América do Sul e Central com fronteiras reais, N002), `map_americas` (México e sul dos EUA: pinos Texas, Nuevo México, Arizona, Ciudad de México, N009), `map_atlantic` (Bermudas entre América e Europa, N023), `map_south` (sul da América do Sul e as ilhas: rótulo **"ISLAS MALVINAS"**, N054). O mapa forjado (`secret_map`, `drawing_map`, `aging_map`) é ilustração, não mapa de pinos.
- **Custo previsto (etapa 2):** 194 imagens nano-banana (~US$ 0,04) ≈ US$ 7,8 + refações (~5%) ≈ US$ 8,2; voz Fish ~US$ 0,2; Runpod ~US$ 0,2 → **~US$ 8,6 < teto US$ 12**.

## Pendências / para a etapa 2
- **Voz (respelling só no `blocos-voz.json`, `tools/gera_blocos_voz.py`):** testar "MI6"/"MI5" (se sair "mi seis", usar "eme i seis"/"eme i cinco"), "BSC" → "be ese ce", "Estación M" → "Estación eme", "Ordzhonikidze" → "Ordyonikídze", "Exocet" → "Exoset", "Joe K" → "Yóu Kéi", "Maschwitz" → "Máshvits", "Chilcot" (ok?), "Daily Mail" (ok). Legenda mantém a grafia original.
- **Código copiado do 011:** `src/Video.jsx` já corrigido para "DOSSIER · EL MI6 · Nº 012"; `src/Thumbnail.jsx` e `src/labels.jsx` ainda têm o conteúdo do 011 (refazer: 3 thumbs da EMBALAGEM sem sigla, textos NUEVA YORK / ¿SABÍA? / 14 → 5; pinos dos 4 mapas acima). Grep "011|TEMPLARIOS" antes do 1º render.
- **Imagens a conferir com zoom:** nenhuma suástica/águia em Berlim, no cruzador soviético e nos documentos capturados (`NOINS` nos prompts); letras inventadas em cartas, relatório, dossiê, passaportes, avião da LATI/Condor; o mapa forjado sem segunda massa de terra; Roosevelt reconhecível (pince-nez); a folha da Thumb B com traço vermelho sem escorrer (não parecer sangue).
- Rascunho riscado de Roosevelt (N036): fonte = Cull via Mental Floss (o livro não foi aberto); a dúvida fica em aberto no roteiro.
