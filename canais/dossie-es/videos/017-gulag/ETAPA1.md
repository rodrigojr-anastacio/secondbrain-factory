# ETAPA 1 · dossie-es/017-gulag · youtube.videos id 64 · 23/11/2026

## Resumo
- **Ângulo** (`ANGULO.md`): o Gulag como empresa (contado pelos seus papéis) + os hispanofalantes que ele engoliu (marinheiros, pilotos, divisionários, o mexicano Vadillo) até o *Semíramis* (Barcelona, 1954). Manada: 10 transcrições (Atrium/Auren, Weird History via Bartolozzi, SLICE ×3, Historia Incomprendida, clones Tinta y Ceniza/The Full Record/Uncovered History): **zero** espanhóis/América Latina.
- **Embalagem:** crivo **APROVADO na r3** (r1 0/3, r2 2/3). Pares em `EMBALAGEM.md`; registrados em `youtube.embalagem_variantes`.
- **Roteiro v3:** 1.892 palavras, 64 blocos, hook + 11 expedientes + cierre, **~13:21 estimados** (WPS 2,38; os vídeos 001–015 saíram 1–3% acima da estimativa → ~13:30–13:45 real). Hook ~36 s (frase-ponte pedida pela embalagem; bíblia 25–35 s).
- **Detector de cópia:** **1/100** (`SIMILARIDADE.md`; atenção ≥ 18, cópia ≥ 30). **Crivo de ângulo: APROVADO na r3** (r1 reprovou a ordem do Full Record nos exp. 1/3/cierre e Plata Loira sem fonte; r2 reprovou o capítulo Kolyma/Berzin e as ligações dos clones: canal raso, preso fraco, Kengir, "os campos seguiram", Memorial no fecho).
- **Checagem de fatos:** `pesquisa/REVISAO.md` (≈20 correções: Firin ex-subchefe preso na primavera e fuzilado em agosto de 1937; Dalstroi 11 mil no fim de 1932; nº 12123 = ficha militar, não de preso; 17h35; Gonzalo condenado em jun/1941; ~130 por Istambul incluem o *Ciudad de Tarragona*; 370–500 divisionários; convivência "a finales de los años cuarenta"; causalidades sem fonte retiradas) + `pesquisa/FATOS-C.md` (Wallace em Magadan 24–26/05/1944; padeiro de Karagandá; créditos de 1939; salário de 13/03/1950; livro de 2025). **Revisão nativa:** `pesquisa/REVISAO-NATIVA.md` (7,5/10; aplicadas: tese sem contradição no cierre, "cuarta parte", "estudio" no lugar de "plató", "chorizo… ladrón de las letras", Nobel compartido, ordem do memorando).
- **Storyboard:** 258 planos, **189 imagens novas + 3 bases de thumb = 192 no `cenas.json`**, reuso 26,7% (35,2% depois de 3:00; 0% antes), plano médio 3,1 s, 23 cortes no 1º minuto, 27 rótulos, 0 avisos. Custo previsto: Codex US$ 0 (fallback Gemini ~US$ 0,045/img → pior caso ~US$ 8,6, dentro do teto de US$ 12).

## Promessa e onde é paga (tempos estimados)
- Frase-âncora "Esta es TODA la historia del Gulag: la empresa de Stalin que necesitaba presos. Y la de los españoles…" no **N004 (0:22–0:36)**; "los mismos campos" no N003 (0:16).
- "Empresa" no exp. 1 El Decreto (N005–N009, 0:36–1:32: decreto de 1929, colonizar e explorar, plano de 50 mil vagas).
- **T2/Thumb A:** Kolimá e Dalstrói no N015–N016 (2:35–2:55); ouro em toneladas no N018 (~3:10–3:20, um pouco depois do "até ~3:00" das obrigações); "¿era rentable?" no N019 (3:30), respondido no N049 (10:10).
- **Thumb B (NORMA):** a escala de pão no N021 (3:51–4:12).
- **476 complexos:** N024 (4:41).
- **T3 (dois bandos no mesmo Gulag):** hook N003; anúncio no N025 (~5:10, ≤ 5:30); convivência atribuída a Iordache no N039 (8:04); *Semíramis* no exp. 10 (10:23–11:25) e no cierre "Las Fotos" (12:26).

## Checklist da bíblia (`biblia/roteiro.md`)
- [x] Hook com anedota própria (*Semíramis*, fora da manada), desfecho seco ("Unos habían luchado por Franco. Otros, contra él.") e "Esta es TODA la historia de…" (~36 s: 1 s acima pela frase-ponte da embalagem).
- [x] 11 expedientes de ~50–80 s, cada um cena/objeto datado, título falado; o fim de cada um puxa o próximo.
- [x] Anedota paga (exp. 10 + cierre volta ao cais de Barcelona); cierre com aforismo + pergunta.
- [x] Acusações atribuídas (Applebaum, Jlevniuk, Iordache, Time, Nóvaya Gazeta, "según su hija", "según presos que lo vivieron"); ângulo hispânico como fio (6 expedientes + hook + cierre), com América Latina (Vadillo, Octavio Paz).
- [x] Revisão nativa feita; nada em português.
- [x] Ângulo próprio: `SIMILARIDADE.md` 1/100, `CRIVO-ANGULO.md` APROVADO (r3), 10 de 11 expedientes abertos em cena fora da manada (lista no `SOURCES.md`).
- CTA no meio colado num re-hook: N030 (6:11), depois dos marinheiros.

## Pendências para a etapa 2
- **Voz (Fish):** grafias que o TTS pode ler mal (sugestões da revisão nativa, só no `blocos-voz.json`): Jlevniuk → "Jlevniúk", Solzhenitsyn → "Solyenítsin", Iordache → "Iordake", Dalstrói → "Dalstróy", Kirovabad → "Kirovabád", Time → "Taim"; conferir "TODA" (não gritar). Citações «…» com "textualmente" já no texto.
- **Mapas no código** (`src/labels.jsx`, pinos desenhados no código, nunca pela IA): `ussr_map` (N004: Moscú, Kolimá, Norilsk, Karagandá), `kolyma_map` (Magadán), `camps_dots_map` (N024: muitos pontos de campos), `norilsk_map` (Norilsk), `leningrad_map` (Krasni Bor).
- Pessoas reais "resembling": Firin, Górki, Wallace, Nikíshov, Beria, Vadillo, Joublanc, Muñoz Grandes, Solzhenitsyn, Íñigo, Octavio Paz, Marsé, Pérez de Rozas. Uniformes sem insígnia ("plain tunic/greatcoat"); conferir de perto estrelas/emblemas indevidos nas cenas soviéticas (a estrela só deve aparecer nas thumbs A/B).
- **Thumbs:** notas do crivo r3 para a skill `thumbnail`: B com carimbo de estrela grande o bastante a 320×180 e "NORMA" com tratamento diferente do rótulo "BARCELONA" (ex.: cabeçalho impresso da tabela); A precisa ler "marmita vazia + lingote" (não tigela de comida); conferir que o lingote não lê como manteiga/queijo.
- Fatos a reconferir se der (não bloqueiam): data exata da ordem de Beria de jun/1941 (26 × 27–28: o texto diz "a finales de junio"); a frase de Solzhenitsyn é da tradução simultânea (dita como "textualmente" a partir da imprensa espanhola: ok); o título exato da edição espanhola de 1974 (Plaza & Janés).
- A YouTube Data API segue fora (projeto GCP apagado; ver `016-mkultra/BLOQUEIO.md`): a embalagem foi medida por yt-dlp.
