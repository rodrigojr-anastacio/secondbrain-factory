# ETAPA 1 PRONTA: Em Relevo 005, enchente de maio/2024: por que a chuva da serra alagou Porto Alegre (15/11/2026)

`youtube.videos` **id 43** (em-relevo, nº 5, status `roteiro`, título = T1). Pasta: `pesquisa/canal-clima-2026-11/longo-05/`. Publicação prevista: qua 18/11/2026. Custo da etapa 1 em dinheiro: **US$ 0** (cota da Data API ~75 unidades, `search.list` 0).

## Embalagem aprovada (crivo r2, 3 de 3)
| | |
|---|---|
| **T1 (título A, thumb A)** | **Por que a chuva da SERRA alagou PORTO ALEGRE?** (45 car.; padrão "Por que [LUGAR] [anomalia]?") |
| **T2 (título B, thumb B)** | **O LAGO que engoliu PORTO ALEGRE em 2024** (39 car.; padrão "O/A [coisa concreta] que [faz algo]") |
| **Thumb** | maquete 3D escura (navy `#1F2A44`) do centro-nordeste do RS em relevo; a bacia do Guaíba um tom mais clara; **árvore de rios em ciano brilhante** (5 rios principais GROSSOS: Jacuí, Taquari-Antas, Caí, Sinos, Gravataí; afluentes finos só como textura) convergindo num ponto luminoso em frente a Porto Alegre (pino branco pequeno). Texto **"1/3 DO ESTADO?"** no alto à esquerda: "1/3" enorme amarelo `#FFD23F`, "DO ESTADO?" branco. Sem foto, muro, comporta, pessoa, seta ou vermelho. |
| Histórico | r1: T2 aprovado; T1 ("…se tinha um MURO contra enchentes?") e thumb (muro + comporta, "PELA PORTA?") **reprovados por colisão** com 5 vídeos de canais pequenos (set–nov/2026) e com a thumb do Edu Necessario. r2: ângulo trocado para a anomalia geográfica (chuva longe, capital alagada) → aprovado. `embalagem/crivo-r1.md`, `crivo-r2.md`, `EMBALAGEM-r1.md`. |

**Promessa:** ver no mapa em relevo por que a chuva que caiu na serra e no centro do estado pôs Porto Alegre debaixo d'água (caminho da água de ~30% do RS até a frente da cidade, por que ela não foi embora e o que cedeu).
**Onde o roteiro paga** (tempos estimados; hook a ~1,3×):
- frase-âncora **"A chuva mais pesada caiu na serra. Quem afundou foi Porto Alegre."** no **b02, ~0:22–0:25**;
- 5 rios + "oficialmente, o Guaíba é um lago" + "quase um terço do Rio Grande do Sul" + "só tem uma saída" no **b05–b06, ~0:44–1:10**;
- T2 (o lago que recebe tudo): cap. 2, **b14–b19, ~3:25–4:55** ("todos desembocam no mesmo lago" ~3:50; "o lago na frente da cidade recebe tudo" ~4:50);
- comporta (b28 ~6:50) e casas de bombas 19/23 (b29 ~7:00); fecho que junta as camadas b34–b36 (~8:20).

## O que ficou pronto
| Item | Arquivo |
|---|---|
| BRIEF (referência, fontes, fatos fortes, teto) | `BRIEF.md` |
| Embalagem + crivo | `EMBALAGEM.md`, `CRIVO.md`, `embalagem/` (refs.csv, medianas, mosaico fora do git) |
| Fatos com fonte (F1–F53) + checagem bloco a bloco (24 OK, 16 ajustados, 0 cortados; fatos novos N1–N8) | `pesquisa/FATOS.md`, `pesquisa/FATOS-bruto.md`, `pesquisa/CHECAGEM.md` |
| Fotos/satélite com licença (27 fotos + 11 satélites) | `pesquisa/FOTOS.md`, `pesquisa/fotos.json`; arquivos em `dl/fotos/video/` e `dl/fotos/satelite/` (fora do git) |
| Roteiro: **40 blocos, 1.727 palavras, 9.286 caracteres** para o TTS, **~10:00–10:20** | `shared/roteiro.py` → `shared/blocos.json`; leitura em `ROTEIRO.md` |
| Storyboard (plano por bloco, gatilhos, peças novas por prioridade) | `STORYBOARD.md`, `shared/storyboard.py` → `shared/storyboard.json`, `shared/cenas.json` |
| Pipeline copiado do longo-04 (sem dados/áudio do 04) | `shared/*.py|js|json|sh`, `tools/qa.sh`, `tools/whisper_final.py` |

## O que a etapa 2 precisa saber
1. **Voz ElevenLabs** (mesma do 002–004: voz `7iqXtOF3wl3pomwXFY7G`, `eleven_v3`; `shared/gera_voz_eleven.py`, ajustar caminhos para o longo-05). Pede **9.286 caracteres** (+15% de refações ≈ 10.700). **Conferir o saldo** antes (o 004 deixou ~21.900 − ~11.000 ≈ 10.900 em 13/11; se não couber, avise e use Fish com a voz pt do canal, registrando o custo com `--video 43`). Hook = b01–b06 (`marcha` 1). Pronúncia: Guaíba ("Gua-í-ba"), Taquari, Jacuí, Caí, Gravataí, Sarandi, Sertório, Mauá, Lajeado, Arroio do Meio, DMAE ("dê-ême-a-é"), UFRGS ("ufergis"), World Weather Attribution (em inglês), El Niño, CEP ("cep"), "40199" (quarenta mil cento e noventa e nove).
2. **Thumbs A/B/C** a partir do conceito acima, compostas no código (maquete própria + hidrografia real ANA/IBGE; custo US$ 0; `shared/thumbs.sh` do longo-04 como base). A = "1/3 DO ESTADO?"; B = mesmo conceito com câmera mais baixa e o ponto do Guaíba maior; C = variação ("UM TERÇO?" ou outro enquadramento). **Prévia 320×180 ao lado de `embalagem/mosaico.jpg`** antes de fechar (crivo r2). Nunca foto, muro, comporta, pessoa ou vermelho.
3. **Pacote:** A = T1, B = T2, C = variação de T1/T2 (ex.: "Por que a água da SERRA foi parar em PORTO ALEGRE?"). Descrição/tags **sem** morte/morto/vítimas fatais e sinônimos; créditos de `pesquisa/FOTOS.md` (PMPA "Attribution", Stuckert CC BY-SA 2.0, NASA, Copernicus) e fontes de `pesquisa/FATOS.md` (Defesa Civil RS, INMET, ANA/SGB, DMAE, IPH/UFRGS, WWA, Agência Brasil). CTA/descrição puxa sessão para `bG6-E4qjXYc` (clima do Sul, publicado); **não** anunciar próximo vídeo.
4. **QA do contrato:** na `legendas.srt`, frase-âncora antes de 0:30; "lago" + "quase um terço" perto de 1:00; cap. 2 antes de ~4:00; comporta/casas de bombas antes de ~8:00.
5. **Peças novas** e ordem de simplificação em `STORYBOARD.md` (árvore de rios = assinatura, manter; régua do Guaíba/Taquari; maquete do sistema de proteção; calendário de picos; perfil serra → capital; frente fria parada).
6. **Hidrografia:** baixar os rios da Região Hidrográfica do Guaíba (ANA, base hidrográfica ottocodificada, ou IBGE BC250) e o contorno da RH; relevo SRTM/ETOPO do longo-04.
7. Render só no Runpod (`tools/render_runpod.sh`, em partes), pré-QA visual (`tools/preqa_visual.py`) antes; nada em `/tmp`. Teto **US$ 3**.
8. Entrega local em `entrega/` (video.mp4, legendas.srt, thumb-A/B/C.jpg, thumbnail.jpg, pacote/youtube.txt). **Não** subir para o Drive.

## Pendências (menores, não bloqueiam)
- Referência não reassistida com `watch.py` (janela da noite); o formato do Mundo Entrópico já estava em `youtube.assistidos` (08/11).
- Série PMPA com licença "Attribution" (não CC): decisão de risco do Rodrigo; alternativa Stuckert/satélite.
- Fotos de 1941 com marca d'água de site: usar pequenas e recortadas, ou trocar por tipografia.
- Não confirmados e fora do texto: nível normal do Guaíba, vento no dia do pico, decreto que fez do Guaíba "lago", vazão de pico em m³/s.
- Fatos novos N1–N8 da checagem ainda não copiados para `FATOS.md` (estão em `CHECAGEM.md`).
