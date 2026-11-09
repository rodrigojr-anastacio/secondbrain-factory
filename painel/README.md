# Painel da Fábrica (fase 1, só leitura)

Página única para o Rodrigo ver, pelo celular, o estado da fábrica e dos gastos. O orquestrador publica `dist/` como Artifact no claude.ai; este job não publica nada.

## Regenerar
```bash
~/workspace/fabrica-youtube/tools/.venv/bin/python ~/workspace/fabrica-youtube/painel/exportar.py
```
Leva ~1 s. Apaga e recria `dist/data.json` e `dist/thumbs/` (idempotente). Só faz SELECT no banco `vida` (conexão `read_only`). Depois, republicar `dist/` (index.html + data.json + thumbs/).

`dist/data.json` e `dist/thumbs/` são gerados e ficam fora do git (`painel/.gitignore`); o `dist/index.html` é fonte e vai para o git.

## Arquivos
| Arquivo | O que é |
|---|---|
| `exportar.py` | lê banco + repo e grava `dist/data.json` e `dist/thumbs/NNN-k.jpg` (480 px, jpg q≤75, < 60 KB cada) |
| `dist/index.html` | a página (HTML+CSS+JS puro, sem build). Segue as regras do host do Artifact: sem `<html>/<head>/<body>`, cores só por tokens (claro, escuro por `prefers-color-scheme` e `data-theme`), `marked 12.0.2` do cdnjs, fontes Geist/Geist Mono do Google Fonts, `fetch('data.json')` relativo, `localStorage` só para aba e filtros |

## O que cada seção lê
| Seção (`#hash`) | Fonte |
|---|---|
| `#resumo` | `youtube.canais` (sem os arquivados) + `youtube.videos` (contagem por status) + `youtube.studio_ultimo` (impressões, CTR ponderado por impressões, views dos 28 dias) + `youtube.metricas_canal` (inscritos, último dia) + `financas.resumo_mensal` (gasto do mês por projeto) + `financas.saldo_pre_pago` (alerta < US$ 10, crítico < 0) |
| `#esteira` | `youtube.videos` + `financas.custo_por_video` (custo direto) + `youtube.custo_claude_por_video` (equivalente em US$) |
| `#backlog` | `canais/<slug>/backlog.md` (markdown renderizado na página) |
| `#pesquisas` | `youtube.garimpo_execucoes` + `garimpo_snapshots` + `garimpo_canais` (último garimpo, top 25 por score); `youtube.palavras_chave_ultima` (40 validados + 30 dos nossos canais); relatórios `pesquisa/*/RELATORIO.md`, `LEVANTAMENTO.md`, `IDIOMA.md`, `PADRAO.md` (até 1 nível abaixo), `pesquisa/{tendencias,palavras-chave,metricas}/*.md` e `~/workspace/relatorios/{tendencias,palavras-chave,metricas}/*.md` (cópias idênticas descartadas) |
| `#videos` | thumbs: `conhecimento/thumbnails/<canal>-<pasta>.jpg` (a que está no ar) ou `out/thumbnail.*`, depois as variantes `entrega/thumb-*` (ou `out/thumb-*`), máx. 4; métricas de `studio_ultimo` (retenção = `pct_visualizada`), com fallback em `metricas_video` (API) |
| `#gastos` | `financas.saldo_pre_pago`, `financas.custo_por_video` (média por canal), `financas.resumo_mensal` e `financas.custo_mensal` (até o mês atual) |

## Decisões e limites
- **Só o domínio `youtube` de `financas`.** As contas pessoais (`dominio=pessoal`) ficam fora da página publicada.
- **Fatos fixos no exportador** (o banco ainda não tem): `lotr-fr` aparece como `stand-by`; o canal **Em Relevo (clima)** é sintético (sem linha em `youtube.canais`), com gasto dos projetos `em-relevo` + `clima`. Canal `em preparação` que já publicou aparece como `ativo`. Ajuste em `STATUS_EXIBICAO` / `CANAIS_EXTRA`.
- **Limpeza**: todo texto passa por `limpar()`: some linha que cita `.segredos`, e-mails, padrões de token e strings de conexão; `/home/hermes` vira `~`.
- Dado inexistente aparece como "sem dado"; nada é estimado.
- Testado com o Chromium headless (`~/.hermes/tools/chromium-1208/`) num iframe de 400 px (o headless não desce de ~500 px de janela) e em 1280 px, claro e escuro: sem rolagem horizontal em nenhuma aba.
