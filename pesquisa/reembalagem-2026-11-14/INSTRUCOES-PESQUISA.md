# Instruções comuns aos pesquisadores (Fase 1 + Fase 2) — reembalagem 14/11/2026

Brief-mãe: `~/workspace/referencias/BRIEF-reembalagem-titulo-thumb.md` (leia). Repo: `~/workspace/fabrica-youtube`.

## Leia antes
`conhecimento/titulos.md`, `conhecimento/thumbnails/README.md`, `conhecimento/politicas-youtube.md`, `conhecimento/decisao-do-clique.md` (se existir), a bíblia do seu canal (`biblia/README.md`, `titulo.md`, `thumb.md`; Em Relevo: `pesquisa/canal-clima-2026-11/biblia-titulo.md` + `RELATORIO.md`), `pesquisa/gap-2026-11-14/RELATORIO.md` + `canais/<slug>.md`, `pesquisa/benchmark-2026-11-14/RELATORIO.md` e `dados/videos-90d.csv`. **Reaproveite** os dados/thumbs já baixados lá antes de buscar de novo.

## Como pesquisar (custo zero)
- Preferência: `~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp --proxy socks5://127.0.0.1:40000 --flat-playlist --dump-json "ytsearch25:<termo>"` (sem cota) e depois `videos.list` (1 unidade/50 ids) para views/data exatas. Para views/inscritos use `channels.list` (1 unidade).
- Data API: `sys.path.insert(0,'~/workspace/fabrica-youtube/tools'); from trends import yt_client` (só leitura). `search.list` = 100 unidades: respeite o **seu orçamento de buscas** dado no prompt.
- **Nunca** acesse o YouTube sem o proxy WARP. Nunca imprima tokens.
- Thumbs: `https://i.ytimg.com/vi/<id>/hqdefault.jpg` (ou maxresdefault) via `curl --socks5-hostname 127.0.0.1:40000`. Baixe as dos top 5–8 de cada vídeo e **olhe com Read**. Monte 1 mosaico por vídeo (ffmpeg/PIL, ≤ 1 MB) em `pesquisa/reembalagem-2026-11-14/mosaicos/<canal>-<video>.jpg`, de preferência com a nossa thumb atual no 1º quadro (a nossa: `https://i.ytimg.com/vi/<nosso_id>/hqdefault.jpg`).
- Janela: últimos ~12 meses (idade ≤ ~400 d); para cada referência registre link, canal, inscritos, views, data, views/inscrito, e se está acima da mediana do canal dele (pegue a mediana dos últimos ~20–30 uploads do canal via `playlistItems` + `videos.list`, barato).
- Dados brutos em `pesquisa/reembalagem-2026-11-14/dados/<canal>/` (json/csv). Scripts em `pesquisa/reembalagem-2026-11-14/dados/<canal>/scripts/`. Temporários em `$TMPDIR` (nunca `/tmp`).

## O que entregar (um arquivo: `pesquisa/reembalagem-2026-11-14/canais/<arquivo-do-seu-prompt>.md`)
1. **Padrões do nicho** (seção curta, vale para o canal): catálogo de padrões de título (estrutura, gatilho, comprimento, promessa, pergunta × afirmação, número) e de thumb (rosto/personagem, expressão, nº de palavras, cor/fundo, contraste, objeto-símbolo, composição, como complementa o título), cada padrão com ≥ 2 vídeos reais (link, views, data, acima da mediana do canal deles: sim/não).
2. **Por vídeo**:
   - Atual: título, impressões, CTR, retenção (do brief).
   - Top referências do mesmo tema (tabela: link, canal, inscritos, views, data, v/i, > mediana?).
   - O que a gente entrega de verdade: 4–8 momentos fortes com **timestamp conferido na `legendas.srt`** (cite a frase), destacando o que paga uma promessa no 1º minuto.
   - **Proposta**: Título 1 e Título 2 (padrões diferentes; para cada um: nome do padrão + 2 referências reais com link/views/data que usam o padrão, no mesmo nicho/idioma e acima da mediana do canal delas) e **1 conceito de thumb** (cena/composição, personagem e expressão, objeto-símbolo, fundo e cores, texto na arte 2–3 palavras no idioma do canal e onde; o que promete; como conversa com os dois títulos sem repetir; 2 referências reais de thumb com o mesmo padrão). Diga onde no vídeo (timestamp) a promessa é paga.
   - Respeite a bíblia (bonequinhos historia-ptbr; graphic novel em tinta dossie-es; relevo/mapa/foto Em Relevo). Se a evidência pedir desvio, escreva "**desvio da bíblia:** … porque …".
3. Regras duras das propostas: ≤ 100 caracteres; **sem** morte/morreu/morto/assassinado/assassinato (pt), muerte/murió/muerto/asesinado/asesinato (es), nem massacre/chacina/chocante/perturbador, nem sangue/cadáver/caveira na thumb; "em N minutos" só se a bíblia do canal mantiver; **não copie literalmente** título/thumb de um clone (gap 2); thumb legível a 320×180 (≤ 3 palavras, 1 foco, contraste); nada de prometer o que o vídeo não tem. Nada inventado: todo padrão ancorado em vídeos reais medidos.
4. **Não gere imagem paga. Não mexa em bíblias, vídeos, banco (só leitura), nem fora de `pesquisa/reembalagem-2026-11-14/`. Não faça commit** (o orquestrador commita). Tudo em primeiro plano.
5. Resposta final ao orquestrador: curta (caminho do arquivo + 1 linha por vídeo com os 2 títulos propostos + nº de buscas `search.list` gastas).
