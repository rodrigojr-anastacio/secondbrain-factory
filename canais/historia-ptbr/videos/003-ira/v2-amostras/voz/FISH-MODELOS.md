# Modelos TTS do Fish Audio: qual é o mais recente e o que ele aceita (pesquisa de 04/11/2026)

## Resposta curta
- **Modelo mais recente: `drama-3`** (header `model: drama-3`), lançado em **13/10/2026** (changelog oficial). É um MoE de 35B (3B ativos), com pesos abertos (Fish Audio Community License).
  - A página "Models Overview" ainda chama o `s2.1-pro` de "latest" e recomenda-o para produção (é o único com garantia de TTFA/DPA), mas está desatualizada: o changelog e a página do Drama 3 são posteriores.
- **Preço:** US$ 50,00 por milhão de bytes UTF-8 (o `s2.1-pro` custa US$ 15). **Promoção de lançamento: US$ 10,00/M até 12/11/2026, 09:00 PT (17:00 UTC).** Hoje, então, sai mais barato que o s2.1-pro. Depois de 12/11 custa 3,3 vezes mais.
- **Voz clonada:** sim, pelo mesmo `reference_id`, sem mudar mais nada na chamada. **Testei em 04/11/2026 com o clone `48613fc675f84984981683d92266e543`** (frase "[curious] Tus, ano mil e vinte, conta a lenda."): HTTP 200, saiu em pt-BR, Whisper 100% e a tag não foi falada. O drama-3 fala mais devagar (4,0 s contra 2,8 s no s2.1-pro).
  - **Confirmação de que o modelo foi mesmo o drama-3:** o Fish **não dá erro** com header ausente ou errado; nesse caso cai calado no `s2.1-pro`, e a resposta não diz qual modelo usou. A prova é a cobrança. O crédito (`GET /wallet/self/api-credit`) caiu US$ 0,00115 nas 2 chamadas de teste (46 bytes cada): 46 × 10/M + 46 × 15/M = 0,00115. Se as duas tivessem ido para o s2.1-pro, seriam 0,00138. Nas amostras D + B, caiu US$ 0,01534, que é (832 + 702) × 10/M. O `gerar.py` mostra o crédito antes e depois, mas ele **atualiza com atraso** (só aparece na chamada seguinte).
- Outros modelos: `s2.1-pro` (US$ 15), `s2.1-pro-free` (US$ 0, sem garantia), `s2-pro` (US$ 15, anterior) e `s1` (US$ 15, aposentado em 31/12/2026).

## Parâmetros de expressividade no drama-3
O drama-3 usa o mesmo endpoint (`POST /v1/tts`) e o mesmo corpo de requisição. A diferença está na **direção dentro do texto**:
| Recurso | Sintaxe | Observação |
|---|---|---|
| Direção livre (tom, intenção, ritmo, público) | `[barely holding it together, forcing a smile] I'm fine.` antes das palavras | Não há lista fixa de tags. A doc pede para escrever "como quem orienta um ator". Pode ser em inglês ou noutro idioma, independente do idioma do texto. As tags do 003 (`[curious]`, `[serious]`, `[amazed]`) valem igual e **não foram faladas** em nenhuma amostra. |
| Sons e pausas | `[sigh]`, `[shaky breath]`, `[small laugh]`, `[pause]` no ponto exato | Na amostra D, o `[pause]` antes de "O Túnel" não segurou a virada: o Whisper ouviu "…daquele caixão, o túnel". |
| **Tags em par** (novo) | `<emphasis>…</emphasis>`, `<slow>`, `<soft>`, `<whisper>`, `<stress>`, `<fast>`, `<forceful>` | Mudam **só as palavras envolvidas**. A doc recomenda usar com parcimônia. Ainda não testei. |
| Troca de idioma (experimental) | `<french>…</french>`, `<spanish>`… | Não serve para o historia-ptbr. |
| Pronúncia | `<\|phoneme_start\|>…<\|phoneme_end\|>` | Só para inglês (Arpabet), chinês (pinyin) e japonês (romaji). Para pt-BR, use o `pronunciation_dictionary`. |
| Vários narradores | `reference_id: [id0, id1]` + `<\|speaker:0\|>`… | Até 16 vozes. |

Campos da API (OpenAPI `/v1/tts`; a doc não restringe nenhum deles para o drama-3):
- `prosody.speed` (0,5–2,0; padrão 1), `prosody.volume` (dB) e `prosody.normalize_loudness` (padrão true, família S2).
- `temperature` (0–1, padrão 0,7, "expressividade") e `top_p` (0–1, padrão 0,7). Os benchmarks do card do Hugging Face usam temp 1,0, top_p 0,9 e top_k 30, mas isso não está documentado como padrão da API.
- `chunk_length` (100–300, padrão 300), `min_chunk_length` (padrão 50) e `condition_on_previous_chunks` (padrão true; usa o áudio anterior como contexto quando a chamada tem vários chunks).
- `repetition_penalty` (padrão 1,2) e `max_new_tokens` (padrão 1024).
- `normalize` (padrão true: números, datas e unidades por extenso).
- `language` (novo em 16/10/2026, BCP-47). Serve **só** para normalizar e alinhar timestamps; não muda a voz. O `pt-BR` ganhou regras próprias de normalização em 20/10/2026.
- `latency` (`normal` = melhor qualidade, `balanced` ou `low`).
- `pronunciation_dictionary` (até 3 dicionários com itens `{key, value, case_sensitive}`): útil para "qanats", "Tus" e nomes persas.
- `features: ["quality-guard"]`, se o backend tiver.
- **Não existe campo de "instruction"/estilo.** O estilo vai no texto, como direção entre colchetes.
- Pelo card do Hugging Face, o modelo aberto tem `previous_takes`, que permite editar por continuação. A API não documenta esse campo.

## Implicações para o historia-ptbr (Hipótese, a confirmar de ouvido)
- O `tools/tts_fish.py` já tem `drama-3` com US$ 50/M em `PRECO_POR_MI_BYTES`. Até 12/11, isso **superestima** o custo em 5 vezes, o que é conservador. Não mexi no arquivo; o `gerar.py` aplica a promoção pela data.
- A voz no drama-3 sai **mais aguda** (mediana do F0 de 107–110 Hz, contra 97 Hz no s2.1-pro, cerca de +1,7 st), mais lenta (121–127 ppm, contra 148) e com faixa melódica maior. Confira se ainda soa como a voz do canal.

## Fontes (consultadas em 04/11/2026)
- Drama 3 (sintaxe, API, preço): https://docs.fish.audio/features/text-to-speech/drama-3.md
- Preços: https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits
- Changelog (Drama 3 em 13/10/2026; `language` em 16/10; pt-BR na normalização em 20/10): https://docs.fish.audio/developer-guide/getting-started/changelog.md
- API TTS (todos os campos e enum do header `model`): https://docs.fish.audio/api-reference/endpoint/openapi-v1/text-to-speech.md
- Models Overview (desatualizada: ainda não cita o drama-3): https://docs.fish.audio/developer-guide/models-pricing/models-overview.md
- Card do modelo (tags, speakers, sampling dos benchmarks): https://huggingface.co/fishaudio/drama-3
- Cobertura do lançamento: https://www.marktechpost.com/2026/10/14/fish-audio-drama-3-open-weight-tts-model/
