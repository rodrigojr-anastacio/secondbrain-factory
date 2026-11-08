# Piloto clima pt: tornados no Sul (08/11/2026)

Brief: `~/workspace/referencias/BRIEF-clima-piloto-pt.md`. O Rodrigo definiu a estrutura (cidades → pergunta → 3 caixinhas → resposta parcial da 1ª); a redação é nossa. Um roteiro, uma voz e os mesmos trechos nas duas versões: **Shorts 1080×1920** (vai ao ar) e **amostra do longo 1920×1080** (não vai ao ar).

- **Duração:** 59,2 s (fala termina em 58,3 s).
- **Voz:** Kokoro **`pf_dora`**, velocidade 1,1 + atempo 1,05, custo US$ 0. Testei `pm_alex` e `pf_dora` nos mesmos blocos e transcrevi com o Whisper: as duas ficaram 100% inteligíveis (prob. média 0,935 × 0,938). Escolhi a `pf_dora` porque respeita as pausas. A `pm_alex` emendou "…destruição para a Defesa Civil" sem respirar e mudou o sentido. A Fish não foi usada. **Limite:** a Kokoro lê a pergunta do bloco b05 sem entonação de pergunta. Se o Rodrigo achar a voz robótica, dá para trocar pela Fish s2.1-pro com voz pública pt-BR por ~US$ 0,02, sem mexer em mais nada (`shared/blocos.json` → `monta_audio.py`).
- **Hook (0–8 s):** "Maringá, Paraná, 2 de novembro. Um tornado F2, com ventos de até 250 km/h, atinge 40% da cidade."

## Texto (a legenda da tela usa números; a fala, números por extenso)
| Bloco | Tempo | Aba | Texto |
|---|---|---|---|
| b01 | 0:00.1–0:08.0 | MARINGÁ | Maringá, Paraná, 2 de novembro. Um tornado F2, com ventos de até 250 km/h, atinge 40% da cidade. |
| b02 | 0:08.3–0:15.9 | CHAPECÓ | Dois dias depois, Chapecó, Santa Catarina. 16 km de destruição. Para a Defesa Civil, o maior evento climático em 50 anos. |
| b03 | 0:16.2–0:20.9 | SANTO AUGUSTO | No dia 7, Santo Augusto, no Rio Grande do Sul. 50 casas destelhadas de madrugada. |
| b04 | 0:21.2–0:23.5 | 7 EM 6 DIAS | 7 tornados confirmados em 6 dias. |
| b05 | 0:24.1–0:29.2 | A PERGUNTA | O que está acontecendo no Sul do Brasil para ter tantos eventos dessa magnitude, como nunca antes? |
| b06 | 0:29.6–0:34.7 | A PERGUNTA | Por que isso está acontecendo? Qual o risco de voltar a acontecer? E até que proporção isso pode chegar? |
| b07 | 0:35.2–0:40.6 | POR QUÊ? | A primeira resposta está no mapa. O Sul fica em um dos corredores de tempestade mais ativos do planeta. |
| b08 | 0:40.8–0:48.5 | POR QUÊ? | Ar quente e úmido desce da Amazônia, colado aos Andes, e encontra as frentes frias que sobem da Argentina. Desse contraste nascem as supercélulas. |
| b09 | 0:48.9–0:55.5 | EL NIÑO | E este ano tem um agravante: um El Niño muito forte, que faz essa combinação acontecer mais vezes. E ele ainda nem chegou ao pico. |
| b10 | 0:55.9–0:58.3 | PARTE 2 | As outras duas respostas, na parte 2. |

## O que a tela mostra (câmera contínua, sem corte)
- **b01:** a câmera abre baixa sobre o norte do PR. O pino cai em Maringá, o município acende em coral e um funil de argila gira. Polaroid com o drone da 7k Drones, ligada ao pino por um fio vermelho. Número no topo: F2 → 250 km/h (contador) → 40%.
- **b02:** pan rápido até Chapecó, com o fio vermelho Maringá → Chapecó. Polaroid da câmera ao vivo do Portal Chapecó (a parede de chuva chegando ao centro). Números 16 km e depois 50 ANOS.
- **b03:** pan até Santo Augusto, com fio. Polaroid do vídeo do morador Vagner Onuczak. 0 → 50 casas.
- **b04:** zoom-out até o Sul inteiro. Os outros 4 municípios com tornado confirmado (Xanxerê, Erval Grande, Palmeira das Missões, Rio Negrinho) ganham pino e acendem. Contador 3 → 7 TORNADOS.
- **b05:** a luz cai e o cartão "A PERGUNTA" é datilografado.
- **b06:** 3 caixinhas numeradas entram uma por fala.
- **b07:** as caixinhas vão para o canto (a 1 marcada "✓ AGORA"). A câmera abre até o Paraguai e a Argentina, e aparece o **corredor de tempestades** (faixa coral).
- **b08:** seta laranja "AR QUENTE E ÚMIDO · DA AMAZÔNIA" descendo pelo oeste (rótulo ◀ ANDES) e seta azul "FRENTE FRIA · DA ARGENTINA". Nuvens de argila (supercélulas) sobem sobre o oeste de SC. Por cima da maquete entra a **imagem real do GOES-19** (infravermelho de 04/11, 10h20, 10 min antes do tornado de Chapecó), como folha translúcida e em polaroid.
- **b09:** a luz esquenta. "+2,2 °C · PACÍFICO EQUATORIAL · EL NIÑO MUITO FORTE". Recorte de manchete recriado (Climatempo, 08/11) com "mais vezes" sublinhado. Depois "DEZ–JAN · PICO PREVISTO DO EL NIÑO".
- **b10:** as 3 caixinhas voltam, a 1 riscada e as 2 e 3 com "→ PARTE 2". Fecha com "PARTE 2", "SEGUE O CANAL PRA NÃO PERDER" no Shorts e as duas perguntas no longo.

## Fatos e fontes (conferidos em 08/11/2026)
| Fato na tela/voz | Fonte |
|---|---|
| Maringá, 02/11 (madrugada), tornado **F2**, ventos estimados de até ~250 km/h (Simepar: 180–253 km/h), ~40% da cidade afetada, calamidade | Simepar via [BandaB](https://www.bandab.com.br/noticias-parana/maringa-foi-atingida-por-tornado-confirmam-simepar-prefeitura/), [RIC](https://ric.com.br/economia/tornado-inedito-de-250-km-h-atinge-maringa-e-afeta-40-da-cidade/) |
| Chapecó, 04/11 ~10h30: rajadas de 126 km/h, rastro de ~16 km, "maior evento climático dos últimos 50 anos" (Defesa Civil municipal) | [ND Mais](https://ndmais.com.br/tempo/chapeco-registra-maior-evento-climatico-dos-ultimos-50-anos-apos-passagem-de-tornado-durante-el-nino-muito-forte/), [ClicRDC](https://clicrdc.com.br/tempo/defesa-civil-confirma-tornado-em-chapeco-e-identifica-segundo-fenomeno-em-xanxere/) |
| Santo Augusto (RS), 07/11 de madrugada: tornado confirmado pela Defesa Civil, ~50 casas destelhadas | [RCO](https://rco.com.br/noticias/clima/tornado-atinge-santo-augusto-no-rs-e-destelha-cerca-de-50-casas), [Rádio Pampa](https://www.radiopampa.com.br/defesa-civil-confirma-o-segundo-tornado-no-rio-grande-do-sul/) |
| 7 tornados confirmados de 2 a 7/11 no Sul (Maringá; Chapecó, Xanxerê, Rio Negrinho; Erval Grande/Itatiba do Sul/Barra do Rio Azul; Santo Augusto; Palmeira das Missões) | [Climatempo, 08/11](https://www.climatempo.com.br/noticia/el-nino/relacao-do-el-nino-com-os-tornados-no-sul-do-brasil-no-inicio-de-novembro-de-2026) |
| "um dos corredores de tempestades mais ativos do planeta"; corrente de ar quente e úmido da Amazônia em baixos níveis, junto aos Andes; frentes frias como gatilho | [Agrolink, 20/08/2026](https://www.agrolink.com.br/noticias/por-que-o-sul-do-brasil-vive-temporada-historica-de-tornados-em-2026_518021.html) (meteorologista Gabriel Rodrigues); Climatempo (jato de baixos níveis + frentes frias da Argentina + "forte contraste de temperatura" para supercélulas) |
| "O El Niño faz com que esta combinação de fatores ocorra mais vezes"; pico em dez/2026–jan/2027 | Climatempo, 08/11 |
| +2,2 °C de anomalia no Pacífico Equatorial | ND Mais (link acima) |

**Cuidados de precisão (para o vídeo longo):**
- O Climatempo e o Agrolink dizem que **o El Niño não causa cada tornado**. O roteiro diz "faz essa combinação acontecer mais vezes", que é a frase do Climatempo.
- "Como nunca antes" fica **só na pergunta**, a pedido do Rodrigo. As fontes dizem que parte do aumento vem da detecção melhor (celular, Prevots), e o longo precisa tratar isso ("Não foi o fenômeno que se multiplicou", Agrolink).
- **Maringá ≠ hipótese do brief:** Maringá teve, sim, tornado (F2, 02/11). A cidade do RS escolhida foi **Santo Augusto** (07/11), que teve o tornado com mais dano no RS na semana. Os outros 4 municípios só aparecem acesos no mapa.
- Os números de casas variam conforme o balanço. O "50 casas" é o número da Defesa Civil RS/MetSul no dia 7.
