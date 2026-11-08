# 5 vozes femininas pt-BR do Fish para o canal de clima (08/11/2026)

**Texto:** blocos b01, b02, b03 e b05 do `longo-01/shared/blocos.json` (Maringá → Chapecó → Santo Augusto → pergunta), 78 palavras, igual ao ROTEIRO.md. Modelo **drama-3**, sem tags. Silêncios das pontas aparados e `atempo` leve no ffmpeg para fechar **26,0 s = 180 palavras/min** (alvo 175–185).

| Nº | Voz | Id | Link | Timbre (descrição do autor / tags) | Fish speed + atempo | Pal/min | Custo |
|---|---|---|---|---|---|---|---|
| 1 | Mulher | `302d4d27c9344460a815ee46efdd5cf0` | https://fish.audio/m/302d4d27c9344460a815ee46efdd5cf0 | clara, amigável, tom profissional e caloroso (a mais "jornalística") | 1,4 + 1,164 | 180 | US$ 0,005 |
| 2 | maria luiza escova alisadora | `5ead3a4fedda4d1f8419ca8b2452f6d5` | https://fish.audio/m/5ead3a4fedda4d1f8419ca8b2452f6d5 | profissional e enérgica, meia-idade, sotaque BR claro (dinâmica, de locutora) | 1,2 + 1,047 | 180 | US$ 0,005 |
| 3 | senhora 50+ | `74f28613269e48d19d001f0c39e901dc` | https://fish.audio/m/74f28613269e48d19d001f0c39e901dc | grave, quente, mais velha (a mais séria) | 1,4 + 1,132 | 180 | US$ 0,005 |
| 4 | Simple - 02 mulher novinha | `f10700a1a6fb400880df70b9d176ccb2` | https://fish.audio/m/f10700a1a6fb400880df70b9d176ccb2 | jovem, vibrante, entusiasmada (a mais energética) | 1,2 + 1,051 | 180 | US$ 0,005 |
| 5 | Elena Gilbert | `dff066efb78a42d49e5e1865d60fe219` | https://fish.audio/m/dff066efb78a42d49e5e1865d60fe219 | tom conversacional, bom para narrativa (a mais "contadora de história") | 1,4 + 0,892 | 180 | US$ 0,005 |

**Custo total: US$ 0,040** (4.008 bytes × US$ 10/M, promo do drama-3 até 12/11; teto 0,50). Crédito do Fish 47,730205 → 47,690125 (US$ 0,04008) = exatamente 4.008 bytes a US$ 10/M, ou seja, cobrado em drama-3. Registrado em `financas.consumo` (servico "tts drama-3 teste clima vozes", sem ref_id). Uma primeira tentativa falhou por id digitado errado (HTTP 400, sem cobrança).

**Observações**
- As tags/descrições do Fish são pouco confiáveis (muitas vozes "female" têm descrição masculina). Busca: `GET /model?language=pt&tag=female`, ordenada por score e task_count; só entraram vozes com descrição feminina e perfil de narração/locução. Descartada a `1d8cb595…`.
- Voz 5 saiu rápida demais com speed 1,4 (199 pal/min) e foi desacelerada no ffmpeg; as vozes 1 e 3 precisaram de atempo ~1,15 (sem distorção perceptível esperada, mas **confira de ouvido**).
- Não rodei Whisper nesta amostra: a entonação das perguntas e a leitura de "éfe dois" ficam para o ouvido do Rodrigo.
- Vozes com o mesmo texto da amostra anterior (voz masculina `1d8cb595…`) ficaram em 25,7–35,6 s; aqui todas em 26,0 s.
