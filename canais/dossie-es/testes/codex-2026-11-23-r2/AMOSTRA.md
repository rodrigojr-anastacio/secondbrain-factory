# Codex parecido com o nano-banana: rodadas r1 e r2 (23/11/2026)

Decisão do Rodrigo (23/11): o próximo Dossier (**MKUltra**, noite de 23/11) sai inteiro pelo Codex, para ver se passa e como o público reage. Antes de ligar no canal, 2 rodadas (US$ 0) com as **mesmas 6 cenas** da amostra da manhã (`cenas-amostra.json`, do `videos/015-gru/cenas.json`, prompts literais).

Grade: `comparativo.jpg` (744 KB, fica na VPS: `*.jpg` fora do git). Colunas: nano-banana do 015 (fal) × Codex r0 (manhã, sem refs) × **r1** × **r2**. Configs: `visual-r1.yaml`, `visual-r2.yaml` (testadas com `img_codex.py --visual`).

## O que mudou em cada rodada
| | Refs de estilo | Prompt |
|---|---|---|
| r0 (manhã) | nenhuma | `estilo_prompt` do nano-banana |
| r1 | 3 imagens do 015: `I003` (galpão, lugar), `I040` (sótão com 2 pessoas), `I090` (retrato na rua) | `ref_instrucao`: "mesmo estilo das refs, contorno preto chapado, cel shading de 2–3 tons, sem pintura nem gradiente, paleta fria ardósia/oliva/sépia/carvão, vermelho só pontual; **só as pessoas descritas**, cena de objeto/lugar sem ninguém"; estilo + "no warm amber or golden glow" |
| **r2 (escolhida)** | as mesmas 3 | r1 + "large flat matte color areas, very little cross-hatching, no wet reflections, simple uncluttered composition like the references, **no famous landmarks unless named**" |

## Resultado (6 cenas por rodada, 0 falhas, ~48–102 s/imagem, ~2,5 min o lote com paralelo 3)
| Cena | r0 | r1 | r2 |
|---|---|---|---|
| I002 retrato Gurevich | marrom quente, pintado | frio, bom, ainda detalhado | **frio, limpo, mais perto do 015** |
| I115 prisão em Moscou | âmbar, chuva | frio, de longe, ok | **frio, chapado, ok** |
| I008 passaporte (só objeto) | **inventou 2 pessoas** | sem pessoas ✔ | **sem pessoas, composição simples** ✔ |
| I001 rua de Bruxelas | Grand-Place no fundo, muita gente | ainda pôs a torre da Grand-Place | **sem marco, poucas pessoas** ✔ |
| I012 mapa-múndi | colorido, relevo pintado | paleta certa (ardósia/oliva) | igual r1 ✔ |
| I056 van noturna | Grand-Place + figurantes, quente | torre ao fundo, frio | **sem marco**; ficou crepúsculo, menos noturno |

**Quanto ficou parecido:** a r2 acerta a **paleta** (fria, dessaturada, vermelho pontual), o **contorno preto** e a **fidelidade** (sem pessoas inventadas, sem marcos não pedidos, 0 letras, 0 molduras). Ainda é um pouco **mais detalhada e "desenhada"** que o nano-banana (mais textura em madeira/paralelepípedo, rostos mais marcados) e a resolução é maior (1536×864 contra 1344×768). Numa sequência de vídeo a diferença é leve: dá para o público notar, não para estranhar. Nota subjetiva: r0 ≈ 5/10, r1 ≈ 7,5/10, **r2 ≈ 8,5/10** de semelhança com o 015.

**Ajuste pós-r2 (no `canal.yaml`):** "under flat grey light" virou "cool even lighting (night scenes stay dark)" porque a r2 clareou a cena noturna. Conferido na validação abaixo (I056 saiu escuro/crepuscular, aceitável).

## Validação da config final (`canal.yaml`) + fallback Gemini (pasta `validacao/`)
`IMG_CODEX_FORCAR_FALHA=I002,I008 img_codex.py dossie-es … --so I002,I008,I056,I001`: I001 e I056 pelo Codex; I002 e I008 forçados a falhar → `img_gemini.py` (gemini-nano-banana-2.1 1K, mesmas refs) gerou os 2 em ~20 s cada, **US$ 0,10** (0,050 + 0,051), lançado em `financas.consumo` ("Google Gemini API"). Estilo do Gemini com as refs: coerente com o Codex r2 (mesma paleta e traço). Também 1 imagem do historia-ptbr pelo `img_gemini.py` com as refs do canal (bonequinho de cabeça redonda ok): US$ 0,05.

**Bug achado e corrigido:** com caminho de saída relativo, o fallback do `img_codex.py` (que roda com `cwd=tools/`) gravava em `tools/canais/...` e a imagem sumia. Já tinha acontecido no historia: **47 imagens fal pagas perdidas** em `tools/canais/historia-ptbr/videos/{011,012,017}/…/.fal-fallback/` (ainda lá, fora do git). Agora a saída é resolvida para caminho absoluto.

## Cota do Codex
r1 + r2 + validação = 14 imagens: janela 5 h 1% → 4%, semana 13%. Histórico: ~5,5 imagens por 1% da janela de 5 h.

## Custo
US$ 0 (Codex) + **US$ 0,15** (Gemini, validação) — teto US$ 1.
