# Etapa 1: roteiro, blocos, storyboard e cenas (sem geração paga)

**Título:** A HISTÓRIA COMPLETA do Egito em 17 minutos (`youtube.videos` id 3 → `status='producao'`)

| Item | Valor |
|---|---|
| Palavras (SCRIPT.md, sem tags) | 2.293 |
| Duração estimada | ~17:00 (1.020 s a 150 ppm, contando anos por extenso e pausas) |
| Blocos de narração (`blocos.json`) | 106 (1–3 frases cada); tags: 99 `[break]`, 6 `[long-break]`, 1 `[emphasis]` |
| Capítulos | Hook + 8 (origens → unificação → pirâmides → Médio/Novo Império → dominações → Egito árabe → europeus e Suez → Egito de hoje) |
| Planos (`STORYBOARD.md`) | 296, média de 3,45 s (2,4–4,25 s estimados) |
| Imagens únicas (`cenas.json`) | 180 = 179 do vídeo + `thumb-base` (medium) |
| Reuso | 39,5% do total · 0% nos 3 primeiros minutos · 49% depois dos 3 min |
| Regras checadas | nenhum reuso antes de 3:00; nenhum (imagem, enquadramento) repetido em < 60 s; nenhum plano < 2 s |

## Hook (3 primeiras frases)
> O Egito não é um país que tem um rio. É um rio com um país em volta. Mais de noventa por cento dele é deserto.

Sequência completa (~45 s): paradoxo → prova em rajada (deserto; Cleópatra mais perto do iPhone que da Grande Pirâmide) → virada ("sumérios, hititas, assírios: todos sumiram") → pergunta central ("como um país invadido por persas, gregos, romanos, árabes, turcos e britânicos continuou sendo o Egito?") → promessa + loop aberto ("o medo que o Egito carrega desde o primeiro faraó", pago no fim com a represa da Etiópia) → entrada direta com a múmia tatuada de Gebelein. Outro loop: "Guarde esse ano: 1922", pago no capítulo 7.

## Arquivos
- `roteiro.py`: **fonte única**. Texto, planos e prompts ficam nele; ele gera `SCRIPT.md`, `blocos.json`, `cenas.json`, `STORYBOARD.md` e `storyboard.json` (planos em JSON para o código Remotion) e valida as regras. Para mudar algo, edite o `roteiro.py` e rode `python3 roteiro.py`.
- `SOURCES.md`: fontes por bloco.

## Pendências e decisões
1. **Reuso depois dos 3 min (49% contra a meta de ~40%).** Com ~17 min, planos de no máximo 4 s e teto de 180 imagens, a conta não fecha: ficar em 40% exigiria ~205 imagens (+25, cerca de US$ 0,18 em `low`) ou um vídeo de ~16 min. No total o reuso fica em 39,5%, e todo reuso é reenquadramento da imagem do próprio trecho ou uma âncora que bate com a narração (faraó/oficial olhando o Nilo, mapa do império, Abu Simbel, máscara de Tutancâmon). **Decisão do Rodrigo:** manter assim ou liberar +25 imagens.
2. **Duração real:** depende da velocidade do clone no Fish. Se o áudio der menos de 16:30, troque o N do título (no banco e no `youtube.txt`). O texto não cita a duração ("em menos de vinte minutos").
3. **[PENDENTE] em SOURCES.md:** a data de abertura total do Grande Museu Egípcio (nov. 2025) e a de inauguração da GERD (set. 2025). Há uma frase alternativa sem a data para cada uma.
4. **Tempos do storyboard são estimados.** Na montagem, reescale os planos de cada bloco pela duração real do áudio do bloco. Cartões de data (coluna "nota") e rótulos dos mapas são feitos no código.
5. Sobrou uma pasta de rascunho `.tmp/` (script de edição já aplicado). Pode apagar; não consegui remover sem aprovação.
