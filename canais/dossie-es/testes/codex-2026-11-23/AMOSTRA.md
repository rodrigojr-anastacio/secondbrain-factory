# Amostra: cenas do Dossier pelo Codex (ChatGPT Plus, US$ 0) — 23/11/2026

**Só amostra para o Rodrigo aprovar.** `canal.yaml`, bíblia e pipeline não foram alterados (o canal segue `gerador: fal`).

## Como foi feito
- 6 cenas do `videos/015-gru/cenas.json` (prompts literais, sem mudar nada): `cenas-amostra.json`.
- `tools/img_codex.py dossie-es cenas-amostra.json <esta pasta> --paralelo 3 --sem-fallback` → mesmo `estilo_prompt` do `canal.yaml` do Dossier, **sem refs** (o canal não tem `visual.refs`; o nano-banana do vídeo também não usou), saída 1536×864 (mesmo tamanho das imagens do 015).
- Grade: `comparativo.jpg` (esquerda = nano-banana do vídeo 015, direita = Codex). Log por imagem: `codex_log.jsonl`.

| Cena | Tipo | Tempo Codex | Observação |
|---|---|---|---|
| I002 | retrato (Gurevich no escritório) | 95 s | bom rosto adulto; pôs uma bandeira na janela (o prompt não proibia, mas a bíblia evita) |
| I115 | ação/pessoas (prisão em Moscou) | 420 s timeout → 58 s na 2ª | respeitou "seen from far away" melhor que o nano-banana |
| I008 | documento (passaporte na mesa) | 72 s | **infiel**: inventou 2 pessoas (homem segurando o passaporte + mulher); o prompt pedia só objeto |
| I001 | lugar (rua de Bruxelas 1941) | 54 s | ótimo, sem letreiros legíveis |
| I012 | mapa-múndi limpo | 60 s | sem rótulos nem letras (ok para pino no código); mais colorido que o pedido "muted" |
| I056 | noturna (van de rádio-goniometria) | 37 s | bonito; acrescentou a Grand-Place e figurantes; placa em branco |

## Resultado
- **Falhas/recusas:** 0 recusas; 1 timeout (420 s) resolvido na 2ª tentativa. Média das que deram certo: **~63 s/imagem** (com paralelo 3 ≈ 20 s/imagem de relógio).
- **Molduras:** 0/6. **Letras inventadas:** 0/6 legíveis (o nano-banana do 015 escreveu "PASSPORT" e rabiscos no I008).
- **Fidelidade ao estilo "graphic novel em tinta":** parcial. Contorno preto e rostos adultos realistas, sim; mas o Codex sai **mais pintado, detalhado e quente** (luz âmbar, marrons e vermelhos) que a paleta da bíblia (ardósia/oliva/sépia/carvão, dessaturada, vermelho só pontual). Parece mais BD europeia pintada que tinta chapada. A cara do canal muda: um vídeo inteiro assim ficaria visivelmente diferente dos 015 anteriores.
- **Fidelidade ao prompt:** 4/6 fiéis; o Codex "enriquece" a cena (pessoas extras no documento, monumentos no fundo). Em planos de objeto/documento (muito comuns no Dossier, com carimbos) isso é um risco real.

## Cota do Codex (tools/codex_uso.sh + ops.event_log)
- Estas 7 chamadas (6 + 1 retry): janela 5 h 0 → 1%, semana 12 → 13%.
- Histórico do História (mesmo Plus): ~230 imagens/vídeo ≈ **42–44% da janela de 5 h** e **~6–7% da semana** (17/11: 248 img → 37%/5%; 20/11: 190 → 44%/6%; 21–22/11: 205 → 43%/6%). ≈ 5,5 imagens por 1% da janela de 5 h.
- **História + Dossier na mesma noite** (~230 + ~196 ≈ 430 imagens): ≈ **80% da janela de 5 h** se tudo cair na mesma janela, e ~12% da semana por noite → 4 noites ≈ **~50% da semana**. Cabe, mas sem folga para refações/thumbs se as duas rodarem juntas. Em 22/11 21:33 o Codex acusou limite com só 9% da janela (provável limite de rajada) → **não rodar os dois lotes em paralelo**; em série (Dossier ~196 img × 63 s ÷ 3 ≈ 70 min) cabe na noite.

## Se o Rodrigo aprovar (próximo passo sugerido, US$ 0)
1. Testar 2–3 imagens do 015 como `visual.refs` + `ref_instrucao` reforçando a paleta dessaturada e "no extra people, only the objects described" (o img_codex já suporta), e repetir estas 6 cenas.
2. Só depois trocar `gerador: codex` / `gerador_fallback: fal` no `canal.yaml` do Dossier.
