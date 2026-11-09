# Identidade visual: Em Relevo (canal de mapa 3D, pt-BR), 09/11/2026

## Arquivos para subir (YouTube Studio → Personalização → Branding)
| Arquivo | O que é |
|---|---|
| `logo-1.png` | **Recomendado.** Morro de curvas de nível em camadas de papel com tachinha coral no topo. É o "relevo" mais direto, redondo (casa com o corte em círculo) e o que melhor lê a 98 px |
| `logo-2.png` | Quadrado de terreno-maquete em degraus com pino de localização coral. Lê como "lugar no mapa" |
| `logo-3.png` | Mapa dobrado (sem rótulos) com montanha de papel saindo do meio e tachinha. O mais narrativo; perde detalhe a 98 px |
| `capa-1.png` | Mapa-múndi de papel em relevo sobre oceano navy, pinos e fio vermelho nas bordas; "EM RELEVO" coral + faixa navy |
| `capa-2.png` | Quadro de cortiça com relevo de papel no centro e polaroids com fio vermelho nas laterais; título numa etiqueta de papel presa com tachinhas ("EM" navy, "RELEVO" coral) + faixa navy |
| `previa-logos.jpg` | Os 3 logos em círculo (300 px e 98 px reais), só para conferência |
| `previa-capas.jpg` | As 2 capas com a área segura 1546×423 (verde) e a faixa do desktop (amarelo), só para conferência |

- Logos 800×800, **nenhuma letra** (conferido com visão). Capas 2560×1440 (< 6 MB); texto só dentro da área segura (o script falha se sair); fora dela, só fundo. Conferido com visão: nenhuma letra inventada pela IA nas bases.
- Linha da capa: **"O que está acontecendo no mundo, explicado no mapa"** (diz o que o canal faz sem prender a clima). Alternativa mais curta, se quiser trocar: "As notícias do mundo, explicadas no mapa".

## Handle (API `channels.list forHandle`, 09/11/2026)
- `@emrelevo` **ocupado** (canal "Em Relevo", 2 inscritos, 2 vídeos).
- Livres: **`@emrelevobr`** (recomendado: curto, e o canal é pt-BR), `@canalemrelevo`, `@emrelevotv`. Também livres: `@omundoemrelevo`, `@emrelevomapa`, `@emrelevonews`, `@emrelevooficial`.
- Atenção: já existe um canal com o nome "Em Relevo" (pequeno) e a referência do formato é o Instagram @relevo.ia. Nome repetido é permitido no YouTube; o handle é que precisa ser único.

## Descrição do canal (pt-BR)
> O que está acontecendo no mundo, explicado no mapa. Enchentes, tornados, secas, terremotos, guerras, fronteiras e as notícias que mexem com a geografia, contadas em mapas 3D com dados, fontes e o porquê de cada coisa.
> Vídeos novos toda semana. Narração com voz sintética; mapas e animações produzidos a partir de dados públicos (IBGE, INMET, NOAA, NASA e outros). Fontes na descrição de cada vídeo.

Palavras-chave: mapa, geografia, clima, notícias, tornado, enchente, explicado, mapa 3D.

## Assinatura visual (tirada dos vídeos: `longo-01/shared/cues.json` e `remotion/src/Longo.jsx`)
| Cor | Hex | Uso |
|---|---|---|
| Coral | `#E8505B` | título, destaque, áreas afetadas |
| Navy | `#1F2A44` | faixas/etiquetas, fundo do logo |
| Papel | `#E9DCC3` | mapa/maquete |
| Branco papel | `#FBF8F1` | etiquetas, polaroid |
| Tinta | `#2B2622` | texto sobre papel |
| Tachinha | `#ff8a8f` → `#C9303B` | gradiente radial do pino |
| Fio vermelho | `#D8404B` | fios entre pinos |
| Terreno | `#B9A47F` | fundo do mapa |
| Cortiça | `#C79766` / `#B07F52` / `#95683F`, moldura `#6B4A2E` | quadro "O que fazer" |

Fontes (em `fontes/`, todas OFL): **Anton** (títulos e números), **IBM Plex Mono** Bold/Medium (faixas, legendas máquina de escrever), Playfair Display Italic (manchetes).

## Como refazer
- `tools/gerar.py` gera as bases sem texto em `base/` (fal `fal-ai/nano-banana`, 2 variações por conceito; pula as que existem) e registra o custo em `financas.consumo` (youtube / em-relevo / "identidade em relevo").
- `tools/compor.py` faz os finais e as prévias a partir de `base/` e `fontes/`. Grátis.
- Bases usadas: logo-1 = `logo-b-2`, logo-2 = `logo-a-1`, logo-3 = `logo-c-1`, capa-1 = `capa-a-2`, capa-2 = `capa-b-2`. As outras 5 ficaram de reserva.
- Aprendizado: pedindo fundo navy "edge to edge, no circle", 2 de 6 logos ainda vieram com círculo próprio (sobre branco); por isso 2 variações por conceito. As capas em 16:9 (1344×768) não vieram com tarja preta desta vez.

## Custo
10 imagens nano-banana (6 logos + 4 capas), **US$ 0,39** (R$ 2,29), sem refação. Teto era US$ 2.
