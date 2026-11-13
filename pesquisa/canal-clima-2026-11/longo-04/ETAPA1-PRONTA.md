# ETAPA 1 PRONTA: Em Relevo 004, 1983 — o El Niño que partiu o Brasil ao meio (13/11/2026)

`youtube.videos` **id 38** (em-relevo, nº 4, status `roteiro`). Pasta: `pesquisa/canal-clima-2026-11/longo-04/`. Publicação prevista: seg 16/11. Custo da etapa 1 em dinheiro: **US$ 0** (sem voz, imagem nem render; dados ANA/NOAA/USGS abertos).

## O que ficou pronto
| Item | Arquivo |
|---|---|
| Fatos com fonte (F1–F22), status PRIMÁRIA / SEGUNDO X / FORA | `pesquisa/FATOS.md` |
| Dados reais (régua do Iguaçu 1982–83, chuva de Mombaça 1911–2024, RONI/ONI, boletim NOAA 12/11) | `pesquisa/DADOS.md`, `dados/` |
| Fotos/imagens com licença conferida (30) + seção satélite 1983 | `pesquisa/FOTOS.md`, `pesquisa/fotos.json`; arquivos em `dl/fotos/video/` e `dl/fotos/satelite/` (fora do git) |
| Par Landsat 4 de 1983 (03/07 × 04/08, mesma janela) | `tools/landsat_par.py` → `dl/fotos/satelite/landsat4-uv-19830703-par.jpg`, `…0804-par.jpg` (cópias em `dl/fotos/video/`) |
| Roteiro final: 42 blocos, 1.755 palavras, **9.621 caracteres** para o TTS, ~10:30 | `shared/roteiro.py` → `shared/blocos.json`; leitura em `ROTEIRO.md` |
| Checagem bloco a bloco + correções da pauta + checklist do canal | `pesquisa/CHECAGEM.md` |
| Storyboard (plano por bloco, estilo A/B/arquivo, mídias com palavra-gatilho, peças novas por prioridade) | `STORYBOARD.md`, `shared/storyboard.py` → `shared/storyboard.json`, `shared/cenas.json` |
| 3 títulos × 3 conceitos de thumb (A/B/C) | `TITULOS-THUMBS.md` |

## Correções de fatos (resumo; detalhe em CHECAGEM)
- Iguaçu: 10,42 m em **18/07/1983** confirmado em duas fontes primárias (Defesa Civil PR + régua da ANA ao centímetro). Mas o rio estava em 4,94 m no começo de julho (já tinha cheio em nov/82 e mai/83); "2,5 m" é o nível normal.
- "Terceira safra seguida" virou dado de pluviômetro: Mombaça 1981 472 · 1982 407 · 1983 366 mm (média 783).
- "2 mil km" → ~2.500 km (2.582 km calculados).
- Totais de SC (197.790 desabrigados, 49 mortos, 78 municípios) só em Herrmann/UFSC → narrados com atribuição. "80% da cidade por 45 dias", "60.330 desabrigados", "162 municípios" e "3,5 milhões de mortos da seca" **saíram**.
- Achado novo: Blumenau teve **4 cheias acima de 10 m em 1983**; e a cheia de julho veio com o Pacífico já esfriando (RONI MJJ +0,47) → é o "guarde isso" do roteiro, pago no paralelo com 2026 (outono-inverno de 2027 merece atenção, sem prever enchente).
- NOAA 12/11/2026: chance de El Niño histórico caiu para **~60%** (era 83%/70% em outubro). Roteiro usa "cerca de 60%, mais provável que sim, mas não é certeza".

## O que a etapa 2 precisa saber
1. **Voz ElevenLabs** (mesma do 002/003: voz `7iqXtOF3wl3pomwXFY7G`, `eleven_v3`; script `../longo-03/shared/gera_voz_eleven.py`, copie e ajuste os caminhos). **Saldo conferido 13/11 ~17h45: 16.699 de 38.634 usados → sobram ~21.900** (reset 08/12). Este vídeo pede 9.621 (+15% de refações ≈ 11.100): **cabe**. Confira de novo antes.
   - Tags: `[serious]`, `[curious]`, `[intrigued]`. Hook = b01–b06 (`marcha` 1; no 002 o hook foi a 1,36× e o resto a 1,1×). Whisper bloco a bloco.
   - Pronúncia: Iguaçu, Itajaí-Açu, Mombaça, Canindé, Cobal ("Cobáu"), Dnócs (tela DNOCS), Inpe, Inmet, Funceme, Laranjeiras do Sul, Dionísio Cerqueira, Herrmann ("Hérman"), Landsat ("Lândsat"), El Niño.
2. **Pipeline:** copiar do `../longo-03` (`shared/` de áudio/srt/cues/pacote, `remotion/` com LongoV3, `terreno_v2.js`, `cena3d_v2.js`, `estilo_v2.json`, `tools/qa.sh`, `tools/whisper_final.py`) e adaptar. Escreva só em `longo-04/` e na linha 38 do banco. `build_cues.py` novo a partir de `shared/storyboard.json` (cada mídia tem `gatilho`).
3. **Peças novas** e ordem de simplificação em `STORYBOARD.md` (tela partida = assinatura, manter; régua do rio; hidrograma em relevo; antes × depois Landsat; anéis de meses; fita do jato).
4. **b13 (Landsat):** a cena de 04/08/1983 tem nuvem sobre a cidade; a várzea alagada aparece a sudeste. Trate as cores das duas para ficarem comparáveis. Se a diferença não ficar clara na tela, troque a última frase do b13 por "A várzea ainda estava debaixo d'água" (fala e tela) antes de gerar a voz. Há ainda cenas sem nuvem de 20/08 (221/078, 7%) e 27/08 (222/078, 0%) com o rio já normal, se quiser um "depois".
5. **Fotos:** não existe foto livre da enchente nem da seca de 1983 (Commons, NOAA, Arquivo Nacional); o 1983 é contado com dado + satélite + mapa. Fotos de outros anos **sempre** com o ano real na legenda. Conferir a licença do slide `retirantes-pernambuco-…` (Unicamp) na página antes de publicar; se houver dúvida, troque por papel tipográfico. 4 downloads do Commons falharam por 429 (listados em FOTOS.md): opcionais.
6. **Créditos** só na descrição (`FONTES-E-LICENCAS.md` + `youtube.txt`): Landsat 4/USGS (domínio público, processado pela produção), ANA (dados), NOAA/CPC, Defesa Civil PR/Blumenau, Herrmann (UFSC), Sudene via REP/SciELO, Memorial da Democracia, INMET, fotos do Commons conforme FOTOS.md. **Nenhuma imagem da Globo/TV.**
7. **CTA/descrição:** puxar sessão para o vídeo do El Niño (https://youtu.be/FeSLzHvlkbo, publicado). **Não** anunciar próximo vídeo (b42 já está assim).
8. **b25 "Até hoje, é o recorde":** vale enquanto o RONI de 2026 (ASO +1,97) não passar +2,40; o próximo valor sai depois de 16/11, não muda nada agora.
9. Render só no Runpod (`tools/render_runpod.sh`, em partes), pré-QA visual (`tools/preqa_visual.py`) antes; nada em `/tmp`. Teto **US$ 3** (voz já paga pelo plano; Runpod ~US$ 0,05–0,20).
10. Entrega local em `entrega/` (video.mp4, legendas.srt, thumb-A/B/C.jpg, pacote/youtube.txt com os 3 títulos pareados). **Não** subir para o Drive.
