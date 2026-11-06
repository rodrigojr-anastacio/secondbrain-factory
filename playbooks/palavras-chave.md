# Rotina (quarta 09:30) — palavras-chave em alta → sugestões de vídeo e de canal

Criada em 2026-11-06 (decisão do Rodrigo: quarta 09:30; idiomas en, es, pt, fr; resumo no Telegram como o garimpo). **Separada do garimpo** (`garimpo-tendencias.md`, seg/qui): o garimpo acha *canais* novos com tração; esta acha *termos e padrões de busca* em alta e os transforma em temas para os canais que já temos e em ideias de canal novo.

**Só sugere.** Não edita backlog, bíblia, `trend_seeds.txt` nem `keyword_seeds.yaml`: quem decide é o Rodrigo (ou o orquestrador, com o OK dele).

## Peças
| Peça | O que faz |
|---|---|
| `pesquisa/keyword_seeds.yaml` | sementes por idioma (`expandir` = semente + " a" … " z"; `simples`), temas dos backlogs, palavras que levam um termo a cada canal (`destinos`) e os moldes nossos (`moldes`). **Atualize os temas quando o backlog mudar** |
| `tools/keywords.py` | coleta determinística (abaixo). `--teste` (sem a–z, 3 termos, não grava no banco), `--sem-validar`, `--termos N`, `--max-cota N` |
| `youtube.palavras_chave` | uma linha por (data, idioma, termo, origem); DDL em `tools/db/schema_palavras_chave.sql`; view `palavras_chave_ultima` |
| `tools/rotinas/palavras-chave.sh` + `prompts/palavras-chave.md` | a rotina (`claude -p` sonnet via `_rotina_claude.sh`, etapa `palavras-chave`) |
| `systemd/fabrica-palavras-chave.{service,timer}` | quarta 09:30 |

## O que o `keywords.py` faz
1. **Descoberta (grátis):** autocomplete do YouTube (`suggestqueries.google.com`, `client=youtube&ds=yt`, `hl` + `gl` do idioma) **via WARP** (curl `--socks5-hostname 127.0.0.1:40000`; o venv não tem PySocks), com 0,35–0,65 s de pausa. ~840 chamadas, ~10 min. Peso de cada sugestão = (1 − posição/n), dobrado quando vem da semente sem sufixo; o score de descoberta é normalizado 0–10 por idioma (log).
2. **Destino:** palavras de `destinos` no idioma do canal (palavra inteira, aceita plural; `historia-ptbr` exige "história" no termo). O resto vira `novo-canal` (o Claude tira o lixo).
3. **Validação (cota):** 20 termos (5 dossie-es, 5 historia-ptbr, 4 lotr-fr, 6 novo-canal com ≥ 3 palavras e no máximo 2 por idioma). Para cada um: `search.list` (100 un., type=video, order=viewCount, relevanceLanguage, publishedAfter 12 meses, 50 resultados) + `videos.list` (1 un.). Ficam só os vídeos **longos (> 75 s)**, **com as palavras do termo no título**, **sem idioma diferente** (o declarado no vídeo, `defaultAudioLanguage`/`defaultLanguage`, ou o adivinhado pelo título) e, se o termo é "história de X", com cara de história/documentário (sem isso, "história do Egito" trazia jogo da Copa). Métricas: `mediana_top10`, `recentes_100k` (< 90 dias e > 100 mil), `no_molde` (títulos com "in minutes", "toda la historia"…), `amostra`. Teto de **2.500 unidades** por execução (conta e para; 20 termos = 2.020).
4. **Padrões de título:** n-gramas de 2–4 palavras (dígitos → N) dos títulos de `garimpo_videos`, do último `pesquisa/tendencias/<data>.json` e dos resultados da validação, por idioma (adivinhado por palavras marcadoras), pesados por views/dia de vida; só os que aparecem em ≥ 2 canais.
5. **Score:** validado = 10·log10(mediana) + 4·recentes (máx. 10) − 3·no_molde (máx. 5) + descoberta; não validado = descoberta (0–10). **Tendência** contra a execução anterior (score de descoberta ±20%): novo | subindo | estavel | caindo; o `.md` lista o que sumiu.
6. Saídas: `pesquisa/palavras-chave/<data>.json` e `.md` + banco.

## Análise (o Claude da rotina)
Siga `tools/rotinas/prompts/palavras-chave.md`: top 5 temas por canal **dentro da caixinha** (bíblia de cada canal), padrões, até 3 ideias de canal novo pela matriz de idioma (`novo-canal.md`, etapa 3: en → es → pt → fr → de), sugestões para `trend_seeds.txt`, resumo no Telegram. Relatório em `~/workspace/relatorios/palavras-chave/<data>.md` e cópia em `pesquisa/palavras-chave/<data>-analise.md`.

## Limitações conhecidas (2026-11-06)
- O autocomplete mede **popularidade relativa** de busca, não volume absoluto; serve para achar termos e comparar semanas.
- A busca da API por viewCount em 12 meses traz muito Short e vídeo fora do tema: a `amostra` útil costuma ficar entre 2 e 30 de 50. Amostra < 5 = sinal fraco (diga no relatório).
- Termos de semente (backlog) empatam no score de descoberta (todos vêm da 1ª posição): o autocomplete diz que existem, não qual é maior; a validação desempata.
- 1ª execução (06/11/2026, teste completo sem Telegram): 837 chamadas, 0 falhas, 20 termos, **2.020 unidades**, 10.361 linhas; ~10 min de coleta + ~5 min de análise. Relatório em `pesquisa/palavras-chave/2026-11-06-analise.md`.
- A janela de 12 meses deixa as medianas abaixo das do levantamento de idioma (yt-dlp, sem janela): compare semana com semana, não com os backlogs.
