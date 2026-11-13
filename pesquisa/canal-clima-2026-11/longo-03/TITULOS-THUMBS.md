# Títulos e thumbs: Em Relevo, vídeo 3 (A Grande Seca de 1877)

Etapa 1 (13/11/2026). Regra da bíblia de título (`../biblia-titulo.md`): 3 títulos de 3 padrões diferentes, cada um pareado com uma thumb, sem entregar a resposta. Base: pauta 13/11 §3. Thumbs **compostas no código** (Remotion `Thumb.jsx`, como no longo-02), 1280×720, < 2 MB, sem IA paga: fundo = still do nosso mapa 3D + foto real + texto.

| Braço | Título | Padrão (referência) | Thumb |
|---|---|---|---|
| **A** | **Por que quase ninguém fala da seca que matou 500 mil brasileiros?** | "esquecido" (Mundo Entrópico "Why is the coast of Piauí so FORGOTTEN?", 2,3 mi; Astrum "Why Nobody Talks About the Ozone Hole Anymore", 1,6 mi) | **A · "500 MIL"** |
| B | A seca que mudou o mapa do Brasil | "The X That Changed…" (Astrum "The Tornado That Changed Science", 4,9 mi) | **B · "MUDOU O MAPA"** |
| C | O El Niño de 1877 vai se repetir em 2026? | evento explicado + medo atual (Terra em Choque "El Niño de 1877 Está Voltando?", 569 mil) | **C · "1877 = 2026?"** |

Checagem dos títulos (`pesquisa/CHECAGEM.md` §12/C2): "matou 500 mil" é a estimativa da Agência Senado (o vídeo diz "as estimativas chegam a" e dá a faixa 150–500 mil em b17). "Mudou o mapa" é pago em b28–b34 (ferrovias, Cedro, Amazônia/Acre). C é pergunta sim/não (a bíblia acha mais fraco), mantido porque é o padrão do hit de 569 mil e o vídeo responde com "pode, mas…".
Alternativas, se quiser trocar: A2 "A maior tragédia do Brasil que ninguém aprendeu na escola" (Hipótese; mais forte, mas "ninguém aprendeu" não é verificável) · B2 "A seca que levou o Brasil até o Acre".

## Conceitos de thumb (para a etapa 2 compor)
Cores do canal: coral `#E8505B`, navy `#1F2A44`, papel `#E9DCC3`, branco papel `#FBF8F1`. Fonte do título igual às thumbs do longo-02 (`../longo-02/remotion/src/Thumb.jsx`). Texto ≤ 3 palavras, legível a 160 px.

**A · "500 MIL"** (pareada com o título A)
- Fundo: still do mapa em satélite (estilo A) do Nordeste seco, câmera baixa sobre o Ceará, luz de fim de tarde; Ceará com véu coral leve.
- Esquerda (40%): a carte-de-visite `retirantes-1878-grupo.jpg` em moldura de papel sépia, inclinada 4°, com fita adesiva (é pequena: usar no tamanho em que ainda fica nítida, ~360 px de largura, e não ampliar mais).
- Direita: "500 MIL" enorme em coral com contorno navy; abaixo, etiqueta navy pequena "ESQUECIDOS" (ou "1877").
- Por quê: número chocante + rosto real + mapa; não diz a causa.

**B · "MUDOU O MAPA"**
- Fundo: Brasil inteiro em relevo editorial (estilo B), câmera oblíqua.
- Fio vermelho grosso com tachinhas saindo do Ceará (pino coral) até o Acre, que está aceso em coral; trilho de ferrovia desenhado dentro do Ceará.
- Texto: "1877" grande em navy no topo esquerdo; "MUDOU O MAPA" em etiqueta de papel presa com tachinha.
- Por quê: a anomalia é a linha do Ceará ao Acre (curiosidade: o que uma seca tem a ver com o Acre?).

**C · "1877 = 2026?"**
- Fundo dividido na diagonal: esquerda em sépia (relevo de calor do Pacífico de dez/1877, `dados/sst_1877.json`, renderizado em tons de papel antigo), direita colorido (relevo de calor de out/2026, mesma câmera).
- Texto central: "1877" (sépia) "=" "2026" (coral) e um "?" coral enorme cortando a divisão.
- Opcional: tira pequena da foto do sertão seco de hoje na base direita.
- Por quê: comparação cara a cara e medo atual, sem dizer se repete.

Saídas esperadas na etapa 2: `entrega/thumb-A.jpg`, `thumb-B.jpg`, `thumb-C.jpg` (1280×720, < 2 MB) e `entrega/pacote/youtube.txt` com os 3 títulos pareados.
