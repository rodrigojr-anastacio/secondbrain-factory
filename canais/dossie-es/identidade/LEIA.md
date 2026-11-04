# Identidade visual: Dossier en Minutos (dossie-es), 04/11/2026

## Arquivos para subir (YouTube Studio → Personalização → Branding)
| Arquivo | O que é |
|---|---|
| `logo-1.png` | **Recomendado.** Agente de fedora (rosto em sombra, fita vermelha no chapéu) segurando a pasta parda. É o que mais lê como "espionagem" a 98 px |
| `logo-2.png` | Pasta parda com clipe e sello rojo (anel + estrela). O mais simples e limpo em tamanho pequeno |
| `logo-3.png` | Lupa com olho sobre o dossiê, com lacre vermelho |
| `capa-1.png` | Mesa de ardósia vista de cima: pastas, máquina de escrever, lupas, fotos e carimbo nas bordas; título no centro |
| `capa-2.png` | Arquivo de fichários com agente de fedora à esquerda e luminária à direita; título no centro e sello rojo à direita |
| `previa-logos.jpg` | Os 3 logos em círculo (300 px e 98 px reais), só para conferência |
| `previa-capas.jpg` | As 2 capas com a área segura 1546×423 (verde) e a faixa do desktop (amarelo), só para conferência |

- Logos 800×800 (o YouTube corta em círculo); **nenhuma letra**. Capas 2560×1440 (< 6 MB); texto só dentro da área segura; fora dela, só fundo (o script falha se o texto sair da área).
- Texto da capa composto no código: "DOSSIER EN MINUTOS" em Bebas Neue + "La historia completa de las organizaciones más secretas del mundo" em Special Elite sobre tira de papel, sublinhado rojo sello `#B3261E`.
- Conferido com visão: nenhuma letra inventada pela IA. A base da capa-2 tinha pseudoletras num bilhete preso a um fichário; foram cobertas no código.

## Como refazer
- `tools/gerar.py` gera as bases sem texto em `base/` (fal `fal-ai/nano-banana`; pula as que já existem) e registra o custo em `financas.consumo` (youtube / dossie-es).
- `tools/compor.py` faz os finais e as prévias a partir de `base/` e `fontes/` (Bebas Neue OFL, Special Elite Apache 2.0). Grátis.
- Aprendizado: pedindo "avatar/emblem" o nano-banana desenha o próprio círculo sobre fundo branco, e "panoramic banner" sai com tarja preta (letterbox) em cima e embaixo; o `compor.py` contorna as duas coisas.

## Custo
5 imagens nano-banana (3 logos + 2 capas), US$ 0,195, sem refação.
