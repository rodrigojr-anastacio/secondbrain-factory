# Etapa final: 002-india pronto para publicar

**Título:** A HISTÓRIA COMPLETA da Índia em 19 minutos · `youtube.videos` id 4 → `status='pronto'`, `duracao_s=1167`

| Item | Valor |
|---|---|
| Duração | 1167,2 s (**19:27**) |
| Roteiro | 2.620 palavras, 129 blocos, 10 capítulos (hook + 9); remodelagem da transcrição de p9IIGdg91fE na mesma ordem, com os mesmos beats, hook e fecho |
| Imagens | **195 no vídeo + thumb-base (high)**; 335 planos; 0% de reuso antes de 3:00 e 50% depois |
| Voz | Fish s2.1-pro, 129 blocos (mais 2 regerados) |

## Custo (financas.consumo, ref_id = 4)
| Fornecedor | Item | US$ | R$ |
|---|---|---|---|
| OpenAI | 223 gerações gpt-image-2 medium/high (estimativa do script) | 9,43 | 54,96 |
| Fish Audio | narração + 2 blocos refeitos | 0,24 | 1,43 |
| **Total direto** | | **9,67** | **56,38** |
`custo_por_video` com o rateio do fixo: **R$ 70,20**. Calibrando pelo Egito (fator 0,756), o gasto real da OpenAI fica em ~US$ 7,1. 27 das 223 gerações saíram em dobro (2 processos em paralelo se cruzaram, ~US$ 1); o aprendizado foi registrado no playbook.

## Pacote (`out/`)
`video.mp4` (1080p), `thumbnail.jpg`, `legendas.srt`, `youtube.txt` (título, descrição com hook e CTA, capítulos a partir de 0:00, fontes, nota de voz sintética, tags e categoria Educação), além do `contact-sheet.jpg`.

Para refazer: `python3 roteiro.py` → `img_openai.py … --video 4 --qualidade medium` → `tts_fish.py … --video 4` → `tools/build.py` → `tools/render.sh` → `tools/qa.sh` → `tools/compara_voz.py`.

## Pendências
1. **OpenAI sem saldo** (ver `BLOQUEIO.md`): recarregar e lançar em `financas.lancamentos` (o banco mostra −US$ 9,87). Faltaram 2 imagens (Gandhi na roca e o desfile final), que foram substituídas por reuso, então o vídeo está completo.
2. **Opcional, depois da recarga:** regerar I035 (cocar de penas), `charkha` e `journey_lineup` (~US$ 0,15) e renderizar de novo (~45 min).
3. **Publicação (Rodrigo):** idioma pt-BR, "conteúdo alterado ou sintético" = sim, "não é para crianças", categoria Educação.
4. Duração de 19:27 (meta de ~17). Para os próximos, o `estilo.md` agora recomenda ~2.250–2.300 palavras.
5. Monção de 2026: a frase "mais de dez por cento abaixo do normal no fim de setembro" segue a referência e a projeção do IMD de agosto (~15%). Não achei o número oficial do fim da temporada (ver SOURCES.md).
6. `roteiro-egito-modelo.py` ficou como referência.
