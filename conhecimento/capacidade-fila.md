# Capacidade da fila (13/11/2026 10:16)

Gerado por `tools/fila.sh capacidade` (medições de `ops.fila_amostras`, `ops.fila_jobs`, `ops.max_janelas`). Custo-equivalente = preço de lista da API (`anthropic_api.PRECOS`), não o que o Max cobra.

_Backfill: 0 job(s) da fila preenchidos a partir dos jsonl._

## VPS (RAM / CPU)

RAM total 7.7 GB, 2 vCPU. Amostras da VPS: 1 desde 13/11 10:16.
Pico com 2 job(s) simultâneo(s): RAM disponível mínima 5.6 GB, swap máx 1.3 GB, load1 máx 0.9 (média 0.9), disco livre mín 34 GB.

| job | amostras | RAM média | RAM pico | CPU (s) | CPU média (núcleos) |
|---|---|---|---|---|---|
| lote-clearance-002-bikini | 1 | 3500 MB | 3501 MB | 127 | - |
| lote-dossie-007-ss | 1 | 231 MB | 347 MB | 19 | - |

Pico médio por job 1924 MB (inclui cache de arquivos do scope; é teto conservador). Base da VPS fora dos jobs ≈ 0.0 GB. **Cabem ~3 job(s) com folga de 1,5 GB** (limite técnico: `MemoryMax=3500M` por job; CPU de 2 vCPU limita render a 1 por vez).

## Claude Max (limite de 5 h / semanal)

Nenhum limite batido desde o início da medição (a coleta registra cada "hit your … limit"); capacidade ainda desconhecida.

Consumo por job da fila (preço de lista equivalente):

| job | tipo | status | duração | tokens in/out/cache | custo-eq. US$ | limites |
|---|---|---|---|---|---|---|

Histórico dos jobs `claude -p` anteriores (jsonl; backfill; duração = 1ª a última mensagem, inclui pausas):

| brief | tokens in/out/cache | custo-eq. US$ | duração |
|---|---|---|---|
| BRIEF-fase1.md | 0k/19k/1.2M+70k | 1.2 | 10 min |
| BRIEF-fase2-3.md | 0k/23k/3.7M+114k | 2.1 | 5 min |
| BRIEF-fase2-3.md | 0k/23k/2.5M+92k | 1.7 | 10 min |
| BRIEF-fase2-3.md | 0k/30k/2.0M+99k | 1.5 | 5 min |
| BRIEF-fase2-3.md | 0k/32k/3.5M+109k | 1.9 | 7 min |
| BRIEF-historia-003.md | 0k/111k/20.6M+300k | 8.8 | 102 min |
| BRIEF-canal-archive.md | 0k/79k/5.6M+214k | 4.4 | 32 min |
| BRIEF-canal-archive.md | 0k/37k/6.3M+170k | 2.9 | 10 min |
| BRIEF-subnichos-formato.md | 0k/3k/170k+33k | 0.4 | 35 min |
| BRIEF-subnichos-formato.md | 0k/98k/9.1M+334k | 5.4 | 35 min |
| BRIEF-countrycorns.md | 0k/32k/2.7M+126k | 2.2 | 19 min |
| BRIEF-headless-fix.md | 0k/6k/422k+42k | 0.3 | 2 min |
| BRIEF-dossie-idioma.md | 0k/80k/8.4M+230k | 5.1 | 41 min |
| BRIEF-dossie-001.md | 0k/108k/16.4M+289k | 7.8 | 52 min |
| BRIEF-historia-003-v2.md | 0k/10k/718k+61k | 0.8 | 2 min |
| BRIEF-historia-003-v2.md | 0k/39k/4.2M+150k | 2.8 | 34 min |
| BRIEF-caixinhas-canais.md | 0k/83k/8.3M+251k | 5.3 | 11 min |
| BRIEF-dossie-001-fix.md | 0k/8k/1.0M+60k | 0.4 | 2 min |
| BRIEF-dossie-identidade.md | 0k/14k/1.1M+68k | 1.0 | 3 min |
| BRIEF-historia-003-v2-fase2.md | 0k/116k/24.9M+347k | 10.1 | 73 min |
| BRIEF-dossie-002.md | 0k/94k/16.2M+257k | 7.2 | 89 min |
| BRIEF-drive-entrega.md | 0k/10k/697k+53k | 0.4 | 1 min |
| BRIEF-dossie-003.md | 0k/79k/15.0M+262k | 6.7 | 53 min |
| BRIEF-historia-004-china.md | 0k/118k/25.4M+310k | 9.9 | 92 min |
| BRIEF-dossie-004-cosa-nostra.md | 0k/88k/14.8M+251k | 6.7 | 66 min |
| BRIEF-historia-004-thumbs-v2.md | 0k/20k/2.4M+87k | 1.6 | 6 min |
| BRIEF-historia-identidade.md | 0k/26k/2.7M+113k | 2.0 | 7 min |
| BRIEF-rotina-palavras-chave.md | 0k/57k/5.8M+167k | 3.6 | 25 min |
| BRIEF-palavras-chave-exploracao.md | 0k/88k/4.7M+184k | 4.2 | 23 min |
| BRIEF-motion-teste-lotr.md | 0k/72k/7.7M+178k | 4.4 | 68 min |
| BRIEF-historia-003-thumbs-v3.md | 0k/18k/2.6M+91k | 1.6 | 6 min |
| BRIEF-historia-analise-roteiro.md | 0k/43k/5.7M+157k | 3.2 | 57 min |
| BRIEF-historia-005-brasil.md | 0k/116k/23.9M+328k | 9.7 | 78 min |
| BRIEF-historia-biblia-roteiro-v2.md | 0k/36k/3.3M+126k | 2.4 | 6 min |
| BRIEF-pesquisa-canal-clima.md | 0k/44k/3.9M+179k | 3.1 | 15 min |
| BRIEF-clima-amostra.md | 0k/3k/447k+75k | 0.8 | 1 min |
| BRIEF-clima-piloto-pt.md | 0k/3k/560k+82k | 0.8 | 1 min |
| BRIEF-clima-piloto-pt.md | 0k/3k/681k+67k | 0.7 | 1 min |
| BRIEF-clima-piloto-pt.md | 0k/3k/472k+53k | 0.6 | 1 min |
| BRIEF-clima-piloto-pt.md | 0k/99k/11.2M+224k | 6.0 | 63 min |
| BRIEF-clima-voz-amostra.md | 0k/5k/460k+50k | 0.3 | 2 min |
| BRIEF-clima-longo-01.md | 0k/9k/616k+102k | 1.1 | 2 min |
| BRIEF-clima-longo-01.md | 0k/30k/2.3M+110k | 1.9 | 7 min |
| BRIEF-clima-longo-01.md | 0k/10k/815k+79k | 1.0 | 2 min |
| BRIEF-clima-longo-01.md | 0k/232k/49.2M+570k | 19.0 | 319 min |
| BRIEF-clima-voz-5-femininas.md | 0k/9k/864k+61k | 0.4 | 3 min |
| BRIEF-clima-voz-3e5-natural.md | 0k/3k/469k+45k | 0.3 | 1 min |
| BRIEF-clima-longo-01-v2.md | 0k/52k/12.1M+182k | 4.9 | 199 min |
| BRIEF-clima-identidade.md | 0k/18k/1.9M+89k | 1.4 | 5 min |
| BRIEF-proximos-temas-2026-11.md | 0k/45k/3.2M+172k | 2.9 | 11 min |
| BRIEF-historia-006-roma.md | 0k/118k/23.0M+309k | 9.4 | 101 min |
| BRIEF-dossie-005-kgb.md | 0k/91k/17.2M+246k | 7.2 | 101 min |
| BRIEF-historia-007-russia.md | 0k/131k/27.1M+345k | 10.8 | 110 min |
| BRIEF-dossie-006-masones.md | 0k/95k/19.6M+278k | 8.0 | 70 min |
| BRIEF-painel-fase1.md | 0k/43k/3.0M+135k | 2.5 | 18 min |
| BRIEF-relevo-002-proposta.md | 0k/50k/2.7M+183k | 3.0 | 20 min |
| BRIEF-relevo-002-producao.md | 0k/187k/59.2M+457k | 19.2 | 570 min |
| BRIEF-relevo-002-visual-fase1.md | 0k/92k/14.5M+248k | 6.7 | 83 min |
| BRIEF-relevo-002-visual-fase2.md | 0k/5k/526k+75k | 0.8 | 1 min |
| BRIEF-relevo-002-visual-fase2.md | 0k/91k/34.5M+242k | 10.7 | 730 min |
| BRIEF-base-erros-qa.md | 0k/12k/508k+80k | 0.5 | 2 min |
| BRIEF-teste-render-gpu.md | 0k/55k/8.0M+146k | 3.9 | 68 min |
| BRIEF-render-gpu-padrao.md | 0k/135k/20.7M+257k | 8.9 | 133 min |
| BRIEF-nichos-editorial.md | 0k/49k/5.2M+201k | 3.6 | 23 min |
| BRIEF-entrega-youtube.md | 0k/24k/1.9M+122k | 1.8 | 13 min |
| BRIEF-reporting-api.md | 0k/6k/434k+59k | 0.3 | 1 min |
| BRIEF-metricas-completas.md | 0k/16k/639k+83k | 0.6 | 13 min |
| BRIEF-metricas-historico.md | 0k/11k/953k+66k | 0.5 | 12 min |
| BRIEF-novo-canal-lugares-guerra.md | 0k/11k/1.3M+109k | 1.4 | 2 min |
| BRIEF-novo-canal-lugares-guerra.md | 0k/75k/10.9M+305k | 6.1 | 134 min |
| BRIEF-api-anthropic.md | 0k/70k/8.4M+194k | 4.6 | 33 min |
| BRIEF-api-ajustes.md | 0k/10k/539k+71k | 0.4 | 1 min |
| BRIEF-job-teste.md | 0k/0k/74k+20k | 0.1 | 0 min |
| BRIEF-api-fallback-eventlog.md | 0k/22k/1.5M+92k | 0.7 | 3 min |
| BRIEF-teste-fb.md | 0k/0k/53k+34k | 0.0 | 0 min |
| BRIEF-clearance-001-preprod.md | 0k/21k/1.7M+240k | 2.7 | 123 min |
| BRIEF-clearance-vozes2.md | 0k/7k/674k+56k | 0.4 | 2 min |
| BRIEF-clearance-vozes-fish.md | 0k/6k/614k+69k | 0.4 | 4 min |
| BRIEF-clearance-vozes-fish2.md | 0k/7k/499k+58k | 0.3 | 5 min |
| BRIEF-clearance-001-producao.md | 0k/154k/59.2M+432k | 18.4 | 230 min |
| BRIEF-clearance-identidade.md | 0k/12k/552k+62k | 0.4 | 2 min |
| BRIEF-padroes-titulos.md | 0k/15k/769k+69k | 0.4 | 2 min |
| BRIEF-pauta-fds-15-16.md | 0k/34k/2.8M+133k | 1.9 | 7 min |
| BRIEF-lote-dossie-007-ss.md | 0k/39k/1.3M+129k | 2.1 | 6 min |
| BRIEF-lote-clearance-002-bikini.md | 0k/22k/4.5M+144k | 2.5 | 7 min |
| BRIEF-fila-jobs.md | 0k/13k/359k+43k | 0.3 | 1 min |
| BRIEF-fila-capacidade.md | 0k/14k/388k+48k | 0.3 | 1 min |

Consumo médio por tipo de job: pesquisa/outros: US$ 2.3 (n=60); produção de vídeo: US$ 6.6 (n=27).

## API Anthropic (mês)

- rotinas: US$ 1.85 / 30 (6%)
- qa: US$ 1.26 / 30 (4%)
- dev: US$ 2.63 / 40 (7%)

## Custo por vídeo (financas.consumo, direto, US$)

| fornecedor | vídeos | total | por vídeo |
|---|---|---|---|
| Fish Audio | 14 | 3.29 | 0.24 |
| OpenAI | 3 | 19.74 | 6.58 |
| Runpod | 2 | 1.43 | 0.71 |
| fal.ai | 15 | 114.52 | 7.63 |

## Recomendação

- `MAX_CONCORRENCIA`: manter 2; RAM comporta ~3, mas o Max (cota) e o render limitam antes. Subir para 3 só se não houver `pausado_limite` nas janelas. **Hipótese** (menos de 4 jobs medidos).
- Enviar à API (`--motor api`, grupo dev/rotinas) o que é curto e barato por job (pesquisa, garimpo, QA); manter no Max os jobs longos de produção, que têm cache alto e custo-equivalente grande. **Hipótese** (menos de 4 jobs medidos).
- Se uma janela de 5 h estourar com 2 jobs, o fila.py já pausa e retoma; o sinal de que há folga é a ausência de `pausado_limite` por 24 h.
