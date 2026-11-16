# ETAPA 1 PRONTA: Em Relevo 003, A Grande Seca de 1877 (13/11/2026)

`youtube.videos` **id 34** (em-relevo, nº 3, status `roteiro`). Pasta: `pesquisa/canal-clima-2026-11/longo-03/`. Custo da etapa 1 em dinheiro: **US$ 0** (só pesquisa, sem gerar voz, imagem nem render).

## O que ficou pronto
| Item | Arquivo |
|---|---|
| Fatos com fonte (C1–C12) | `pesquisa/FATOS.md` |
| Dados e geometrias (D1–D7) | `pesquisa/DADOS.md`, `dados/` (chuva de Fortaleza 1849–2018, Niño 3.4 ERSSTv5 1854–2026, SST de dez/1877 e comparativos, semiárido, rios do CE, ferrovias/rotas/pontos, fome global, Monitor de Secas set/2026) |
| Fotos com licença conferida (31) | `pesquisa/FOTOS.md`, `pesquisa/fotos.json` (cópia versionada de `dl/fotos/fotos.json`), arquivos em `dl/fotos/video/` (fora do git) |
| Roteiro final (47 blocos, 1.850 palavras, 10.102 caracteres para o TTS, ~11 min) | `shared/roteiro.py` → `shared/blocos.json`; leitura em `ROTEIRO.md` |
| Checagem bloco a bloco + correções da pauta + checklist do canal | `pesquisa/CHECAGEM.md` |
| Storyboard (plano por bloco, estilo A/B/arquivo, transições, mídias com palavra-gatilho) | `STORYBOARD.md`, `shared/storyboard.py` → `shared/storyboard.json`, `shared/cenas.json` |
| 3 títulos × 3 conceitos de thumb (A/B/C) | `TITULOS-THUMBS.md` |

## Correções de fatos (em relação à pauta)
- "114 mil" é o número de **abarracados em agosto de 1878**, não de chegados: o hook diz "mais de 100 mil" e b13 usa os 114 mil.
- Comparação com a Guerra do Paraguai **saiu** (sem número firme); entrou "pelas contas mais altas, 5% da população do Império; proporcionalmente, a maior catástrofe da história do Brasil" (Agência Senado).
- Mortos: faixa **150 mil–500 mil** na narração (b17); "500 mil" só como "as estimativas chegam a".
- Lenda da "última joia da Coroa" narrada como lenda, sem documento.
- Sinimbu não era visconde em 1878: "o chefe do governo, o senador Sinimbu".
- +3,06 °C de out/2026 (ERSSTv5, base 1991–2020) **não** é o ONI oficial: o roteiro diz só "pela mesma reconstrução, no nível do de 1877, ou acima".
- Achado bom do dado: **1877 foi o ano mais seco em 153 anos de série em Fortaleza (468 mm, 32% da média de 1.450 mm); 1878 foi o 2º.**

## O que a etapa 2 precisa saber
1. **Voz (ElevenLabs, mesma do 002: voz `7iqXtOF3wl3pomwXFY7G`, `eleven_v3`, script `../longo-02/shared/gera_voz_eleven.py`).** Saldo conferido em 13/11 ~13h: plano *starter*, **12.664 de 38.634 caracteres usados → sobram ~25.970** (reset em 08/12/2026). Este vídeo pede 10.102 (+~15% de refações ≈ 11.600). O 004 (Catarina) deve pedir ~10 mil. **Cabe os dois, com folga de ~4 mil**: refaça só o necessário; se o 004 não couber, BLOQUEIO.md conforme o brief. Confira o saldo de novo antes (outros jobs podem ter usado).
   - Tags usadas: `[serious]`, `[curious]`, `[intrigued]` (as mesmas do 002). Siglas escritas para a voz: "Dnócs" (tela DNOCS). Atenção na pronúncia de: Theophilo ("Teófilo"), Sinimbu, Baturité, Quixadá, Camocim, Funceme, El Niño.
   - Hook (b01–b07) com `marcha` 1 (no 002 o hook foi a 1,36× e o resto a 1,1×). Whisper bloco a bloco.
2. **Pipeline:** copie do `../longo-02` o que for preciso (`shared/` de áudio, srt, cues; `remotion/` com `LongoV2.jsx`, `terreno_v2.js`, `estilo_v2.json`) para `longo-03/` e adapte. Escreva só em `longo-03/` e na linha 34 do banco. `build_cues.py` novo a partir de `shared/storyboard.json` (cada mídia tem `gatilho` = palavra falada onde entra).
3. **Peças novas** estão listadas em `STORYBOARD.md` (rios de retirantes escorrendo pelo relevo, régua de chuva 1849–2018, anel de meses, relevo de calor de 1877, fita da ZCIT, ferrovias com datas, rota até o Acre, mapa sépia dos campos). Se faltar tempo, simplifique nessa ordem: fita da ZCIT → setas simples; mapa sépia dos campos → pinos no mapa B; rios de retirantes → setas animadas (mas tente manter: é o plano-assinatura).
4. **Fotos:** as de retirantes só existem em 221–400 px (Brasiliana/BN bloqueiam robô, mesmo pelo WARP). Use como **cartes-de-visite pequenas**, sem ampliar e sem zoom em corpo (regras em `STORYBOARD.md` §Sensibilidade). `retirante-corrêa-1878-c.jpg` é duplicata da `-b`. Nada de linha de crédito na tela: créditos e licenças vão para a descrição (`FONTES-E-LICENCAS.md` + `youtube.txt`). CC BY-SA: só corte/redimensionamento.
5. **Render só no Runpod** (`tools/render_runpod.sh`, em partes), pré-QA visual (`tools/preqa_visual.py`) antes; nada em `/tmp`.
6. **Thumbs** compostas no código (`TITULOS-THUMBS.md`), 1280×720 < 2 MB → `entrega/thumb-A/B/C.jpg`; `entrega/pacote/youtube.txt` com os 3 títulos pareados, capítulos (as 4 perguntas + A RESPOSTA) e as fontes de `pesquisa/CHECAGEM.md`/`FATOS.md`.
7. **CTA (b47)** anuncia o próximo vídeo como "o furacão que não devia existir no Brasil" (Catarina, 004). Se o 004 não for publicado logo depois, troque essa frase antes de gerar a voz.
8. b41 (96% do NE em seca, set/2026) vem da imprensa citando o Monitor de Secas: se der, confira no `dados/monitor-secas-2026-09.json` (área S0–S2 sobre o NE) e ajuste o número.
9. Teto do brief: **US$ 3** em dinheiro (voz já paga pelo plano; Runpod ~US$ 0,05–0,20).
10. Opcional para o Rodrigo: baixar à mão, num navegador, a série "Secca de 1877/78" (J. A. Corrêa) em alta resolução na Brasiliana Fotográfica; a etapa 2 troca as cartes por quadros grandes se aparecer em `dl/fotos/`.
