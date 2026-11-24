# BLOQUEIO dossie-es/016-mkultra · 23/11/2026 · embalagem reprovada no crivo (3 rodadas)

**Motivo:** o crivo independente da embalagem (`skills/embalagem/CRIVO.md`) reprovou na 3ª rodada (máximo da regra). Etapa 1 parada antes do roteiro; `ETAPA1-PRONTA.md` **não** foi gravado (o e2 não dispara).

## O que passou e o que não passou
| rodada | Par A (T1 + Thumb A) | Par B (T2 + Thumb B) | Par C (T3 + Thumb C) |
|---|---|---|---|
| r1 | APROVADO | thumb reprovada: Castro + charuto (bíblia "O que NÃO funciona": "Castro + caixa de puros"); "¿LO FUMÓ?" com resposta murcha | thumb reprovada: folha genérica + "SECRET" (= 010 B); a correção sumia a 320×180 |
| r2 | APROVADO | thumb reprovada: Castro aos microfones + "¿DROGARLO?" = composição da nossa 012 B (Roosevelt + "¿SABÍA?") | thumb reprovada: Honduras só no rótulo (regra do ícone cultural de 23/11); a caneta lia como "assinando" |
| r3 | APROVADO | **thumb reprovada:** estúdio vazio + quepe + mão enluvada com atomizador + "¿LSD?": caso de 1 frase da fonte (plano só discutido), mostra em execução algo que não aconteceu, "LSD" desvia a promessa, 6 elementos sem foco a 320×180 | **APROVADO** |

Os **3 títulos foram aprovados já na r1** e nunca mudaram:
- T1 (fórmula, controle): "TODA la historia de MKUltra en 13 minutos | Del laboratorio de la CIA a América Latina"
- T2 (Cómo + org + verbo): "Cómo la CIA buscó en América Latina la droga del control mental"
- T3 (SIGLA: aposto): "MKULTRA: lo que la CIA vino a buscar a México… y lo que dejó"
Thumbs aprovadas: A `objeto-simbolo` (cogumelos sagrados + vela sobre pano mazateco + "MKULTRA") e C `documento-evidencia` (folha do manual de 1983 sobre a bandeira de Honduras, "stress" riscado e "deplore" manuscrito + "HONDURAS").

**Falta só 1 elemento: a Thumb B.** O tema não é fraco e a promessa foi julgada cumprível nas 3 rodadas; o que falhou foi achar um 3º padrão visual para o recorte Cuba sem repetir as vizinhas (012 B, 015 B) nem a lista "O que NÃO funciona".

## Correção que o crivo r3 pediu (pronta para uma rodada extra, se o Rodrigo/orquestrador autorizar)
- Manter `cena-acao`, **1 figura grande fazendo o gesto de "buscar"**, num caso pago cedo e longo: **o cientista da CIA enchendo um saco de sementes de piule num mercado/serra do México, dez/1952–fev/1953** (expediente 1, ~0:35–1:30; Marks cap. 7 + docs ARTICHOKE de 14/11 e 05/12/1952; adendo CIA de 29/01/1975). Texto de tipo diferente da sigla (A) e do rótulo (C): ex. número "10 LIBRAS" ou pergunta curta que não leia junto com nada.
- Atualizar no `EMBALAGEM.md`: obrigações (tirar "¿drogarlo?"/Castro da Thumb B; Cuba vira só expediente, não a porta do par B; a linha de promessa pode continuar citando o estúdio de Castro) e o parágrafo "Por que são 3 thumbs diferentes".
- Notas para a skill `thumbnail` (não reprovam): luz neutra/fria nas Thumbs A e C (o `estilo_prompt` do Codex proíbe "warm amber/golden glow"); na C, "deplore" grande e o resto da linha ilegível.

## Opções
1. **Rodada extra (r4) só da Thumb B** com a correção acima (custo zero, ~15 min de etapa 1) e seguir para roteiro → storyboard; todo o resto da etapa 1 (BRIEF, ANGULO, fatos A–D, embalagem) está pronto.
2. Deixar a rotina noturna trocar o tema (regra padrão do lote) e retomar o MKUltra outra noite a partir daqui.

## Pendência de infraestrutura descoberta (afeta todos os canais)
A **YouTube Data API está fora desde hoje**: todos os tokens OAuth em `~/.segredos/youtube/tokens/*.json` devolvem 403 "Project #770884732048 has been deleted" (o projeto GCP do `client.json` foi apagado). Afeta `report.py`/métricas diárias, `analytics_completo.py`, `trends.py`, o crivo e a embalagem de todos os vídeos. Contorno usado aqui: `skills/embalagem/scripts/enriquecer_ytdlp.py` (views/datas/medianas por yt-dlp via WARP, cota zero). Precisa do Rodrigo: criar/restaurar o projeto no Google Cloud, novo `client.json` e refazer o login dos canais (`tools/auth.py`).

## Arquivos
`BRIEF.md`, `ANGULO.md`, `pesquisa/FATOS-A..D.md`, `pesquisa/MANADA-RESUMO.md`, `EMBALAGEM.md` (r3), `embalagem/EMBALAGEM-r1.md`, `EMBALAGEM-r2.md`, `embalagem/crivo-r1..r3.md`, `CRIVO.md` (= r3), `embalagem/variantes.json`, `refs.csv`, `medianas.json`, mosaicos.
