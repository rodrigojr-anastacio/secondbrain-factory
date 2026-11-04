# Referências para o piloto (lotr-pilot)

Formato: ensaio narrado de lore, sem rosto, 16:9, cerca de 1 minuto.

## 1. O que assistir (referência de estilo)

| Referência | O que copiar |
|---|---|
| **Fireship, "This video was made with code. But how?"** ([resumo](https://rosetta.to/u/fireship/this-video-was-made-with-code-but-how)) | Até onde dá para levar o Remotion: cortes rápidos, texto cinético, ritmo marcado pela narração. |
| **Galeria oficial do Remotion** ([remotion.dev/showcase](https://remotion.dev/showcase)) | Vídeos reais feitos com Remotion, muitos com o código aberto. |
| **Johnny Harris**: mapas, papel e granulação ([técnica de mapas](https://aescripts.com/learn/how-johnny-harris-makes-maps/), [texturas](https://blog.motionarray.com/learn/premiere-pro/edit-documentary-in-premiere-pro/)) | Mapa com rota animada, camada de papel e grão por cima de tudo, revelação por máscara. Encaixa bem em lore (a viagem de Sam para o Oeste). |
| **Kings and Generals** ([guia de vídeos com mapas](https://fluxnote.io/guides/faceless-map-based-videos-guide-2026)) | Mapas animados com movimento e territórios, em canal de história sem rosto. |
| **"Hormozi 2.0"** ([análise de 2026](https://joyspace.ai/hormozi-editing-style-2026-analysis)) | Ritmo sem pausas e sem respiros, legenda palavra por palavra, zoom de ênfase, transições suaves em vez de "pops". |
| **Remotion + Claude Code** ([como usar as skills](https://www.tella.com/blog/how-to-use-remotion-agent-skills-with-claude-code)) | Demos de vídeos gerados por prompt, para ter noção do padrão possível. |

## 2. Por que o piloto ficou fraco

O que tem hoje no projeto: `Video.jsx` com cerca de 200 linhas, 6 imagens e vídeos, fonte DejaVu e voz Piper.

- **Poucos visuais:** um vídeo dinâmico troca de imagem a cada 3–5 segundos, o que dá 15 a 20 visuais por minuto. Hoje tem 6.
- **Fonte genérica:** a DejaVu é fonte de sistema. Trocar por uma serifada de fantasia gratuita do Google Fonts, como Cinzel ou Cormorant Garamond.
- **Voz robótica:** o Piper soa sintético e é o que mais "denuncia" um vídeo feito por IA. Testar uma TTS melhor (OpenAI ou ElevenLabs).
- **Movimento parado:** faltam Ken Burns, parallax 2.5D (separar frente e fundo da imagem), luz se movendo, partículas e névoa.
- **Sem textura:** falta a camada de papel, grão e vinheta por cima de tudo.
- **Sem sincronia:** cortes, legendas e efeitos sonoros (whoosh, impacto) devem cair no tempo exato das palavras da narração.

## 3. Ferramentas para o Claude na VPS

- **Skill oficial do Remotion** ([docs](https://www.remotion.dev/docs/ai/skills)): `npx skills add remotion-dev/skills`, rodado na raiz do projeto. Ensina ao Claude as boas práticas do Remotion.
- **Template de legendas animadas** ([remotion-dev/template-tiktok](https://github.com/remotion-dev/template-tiktok)): usa o Whisper para pegar o tempo de cada palavra e animar a legenda.
- **Template de prompt para vídeo** ([remotion-dev/template-prompt-to-video](https://github.com/remotion-dev/template-prompt-to-video)).

## 4. Direitos autorais

Cenas dos filmes e ilustrações oficiais (Alan Lee, John Howe) dão Content ID no YouTube. Use arte gerada por IA, domínio público ou CC, e mantenha o `ASSET_CREDITS.md`.

## 5. Prompt sugerido para o Hermes

> Refaça o lotr-pilot usando estas referências: ritmo de ensaio estilo Johnny Harris (mapa da Terra-média com a rota de Sam animada, camada de papel e grão, revelações por máscara) e cortes a cada 3–5 s. Antes de codar, instale a skill oficial do Remotion no projeto. Requisitos: 15–20 visuais por minuto (imagens geradas ou livres de direitos), parallax 2.5D e Ken Burns em todas as imagens, fonte Cinzel ou Cormorant, legenda palavra por palavra sincronizada pelo Whisper, efeitos sonoros nos cortes e trilha com ducking sob a voz. Primeiro me mande um storyboard (cena, tempo, visual, movimento, texto) para eu aprovar. Só depois delegue a implementação ao Claude Code.
