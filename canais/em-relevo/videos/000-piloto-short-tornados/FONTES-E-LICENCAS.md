# Fontes e licenças dos trechos reais (piloto clima pt, 08/11/2026)

Regra aprovada pelo Rodrigo: o trecho real fica **sempre dentro do nosso quadro** (polaroid com tachinha, presa por fio vermelho ao pino do mapa), nunca em tela cheia. É curto, comentado pela narração e leva crédito na tela. **Zero imagem de TV/emissora** (Content ID). Os arquivos brutos ficam em `dl/` e os recortes em `remotion/public/clips/`, os dois fora do git. Para recortar de novo: `shared/cortar_clipes.sh`.

| # | Onde aparece | Fonte (URL) | Canal / autor | Publicado | Segundos usados do original | Na tela | Licença | Status para publicar |
|---|---|---|---|---|---|---|---|---|
| 1 | Maringá (0:02–0:08) | https://www.youtube.com/watch?v=gm5vWBbuXyY | **7k Drones** (@7kDrones), drone próprio | 07/11/2026 | 1:42,2–1:47,9 (5,7 s), recortado 4:3, sem áudio, sem o letreiro "Caminho do tornado" | "VÍDEO: 7K DRONES · YOUTUBE · 07/11/2026" | Licença padrão do YouTube (todos os direitos reservados) | ⚠️ **Pedir autorização** (DM no Instagram/YouTube da 7k Drones). Atenção: em outros trechos esse vídeo usa material de terceiros ("Créditos LUNGARTS", print do g1). **O trecho usado é o drone próprio**, sem crédito de terceiro na imagem |
| 2 | Chapecó (0:09,7–0:16) | https://www.youtube.com/watch?v=okd61_o5xks | **Portal Chapecó** (@PortalChapecoSC), câmera de monitoramento própria no Centro | 04/11/2026 | 1:44–1:50 (~6,2 s), sem a faixa de patrocinadores, sem áudio | "VÍDEO: CÂMERA AO VIVO PORTAL CHAPECÓ · 04/11/2026" | Licença padrão do YouTube | ⚠️ **Pedir autorização** ao Portal Chapecó (portal local de notícias, não é TV; e-mail/WhatsApp no site) |
| 3 | Santo Augusto (0:17,3–0:21) | https://www.youtube.com/watch?v=ix8SSbAajAw | **Vagner Onuczak** (@vagneronuczak), morador que filmou | 07/11/2026 | 0:13,0–0:16,9 (~3,9 s), recorte 4:3 sem as barras laterais, sem áudio | "VÍDEO: VAGNER ONUCZAK (MORADOR) · YOUTUBE" | Licença padrão do YouTube | ⚠️ **Pedir autorização por DM** ao autor |
| 4 | Supercélulas (0:48–0:51), polaroid + folha translúcida sobre o mapa | NASA GIBS WMS, camada `GOES-East_ABI_Band13_Clean_Infrared`, 2026-11-04 13:20 UTC (10h20 em Brasília), caixa 62–44 °O × 36–20 °S | NOAA/NASA (satélite GOES-19) | — | imagem fixa | "IMAGEM: GOES-19 · NOAA/NASA (GIBS)" | **Domínio público** (governo dos EUA). Crédito sem logo e sem sugerir endosso | ✅ Livre |
| 5 | Mapa 3D inteiro | IBGE, API de malhas v3 (UF 41/42/43, municípios, qualidade mínima/intermediária) + Natural Earth 50 m (países) | IBGE / Natural Earth | — | geometria redesenhada por nós | barra "MAPA: IBGE" | Dados públicos (IBGE, com citação da fonte) / Natural Earth = domínio público | ✅ Livre |
| 6 | Manchete recriada (0:51–0:55) | Climatempo, 08/11/2026 (link no `ROTEIRO.md`) | Climatempo | 08/11/2026 | 1 frase citada | recorte com o nosso tipo, veículo + data | Citação curta com fonte (art. 46 da Lei 9.610); não é print da página | ✅ Ok (citação) |
| 7 | Voz | Kokoro-82M `pf_dora` (local) | hexgrad | — | — | — | Apache-2.0 | ✅ Livre |
| 8 | SFX e drone de fundo | sintetizados no código (`shared/mix_audio.py`) | nós | — | — | — | próprios | ✅ Livre |
| 9 | Fontes tipográficas | Anton, IBM Plex Mono, Playfair Display (Google Fonts) | — | — | — | — | OFL | ✅ Livre |

## Descartados de propósito
- **TV/emissoras:** Band, RIC Record, CNN Brasil, g1, SBT, Gaúcha, Itatiaia, UOL e Terra, embora sejam os vídeos com mais views. Têm Content ID.
- **Reupload/compilado:** Natureza em Fúria, Planeta em Fúria, DNews, Rastro da Notícia, Douglas Konrad (compilado com origem incerta).
- **Drone de Santo Augusto** no vídeo do Celemar de Ávila (`6uxjHM1JUio`, 11:53–12:24): marcado "IMAGENS INTERNET", **com origem incerta**. O título credita "Bruno Vargas via drone". Se o Rodrigo quiser imagem aérea do RS, é preciso achar e pedir ao Bruno Vargas.

## Antes de postar o Short
1. Mandar DM/e-mail para **7k Drones**, **Portal Chapecó** e **Vagner Onuczak** pedindo uso de poucos segundos com crédito. Modelo de mensagem em `PUBLICAR.md`. Guardar a resposta (print) nesta pasta.
2. Se alguém negar ou não responder, trocar o trecho dessa pessoa. A troca não exige re-render total: basta editar `shared/cortar_clipes.sh` (ou apontar outra imagem em `cues.clipes`) e renderizar só a parte afetada (`shared/render.sh Shorts x 0`, que cobre 0–20 s) e depois `junta`.
3. **Plano B 100% livre:** usar no lugar do trecho uma 2ª imagem do GOES (GeoColor, já baixada em `dl/`) ou foto da Agência Brasil conferida uma a uma.
