# Amostra de voz Fish para o canal de clima (08/11/2026)

**Voz:** `1d8cb595b6284ff7aa7e8fec7b93249d`, título "Modelo 01", idioma pt (Fish API). A descrição fala em voz masculina energética, conversacional, ritmo rápido, mas as tags dizem `female`: confira de ouvido.

**Texto:** blocos b01 (Maringá), b02 (Chapecó) e b05 (a pergunta) do `piloto-pt/ROTEIRO.md`, na ordem, texto igual. Velocidade 1,0, sem ajuste.

| Arquivo | Modelo | Duração | Bytes | Custo |
|---|---|---|---|---|
| `amostra-s21pro.mp3` | s2.1-pro (US$ 15/M) | 25,7 s | 325 | US$ 0,0049 |
| `amostra-drama3.mp3` | drama-3 (US$ 10/M na promo até 12/11; 50/M depois) | 35,6 s | 349 | US$ 0,0035 |

Total US$ 0,0084 (teto 0,30). Registrado em `financas.consumo` (servico "tts <modelo> teste clima", sem ref_id).
**Cobrança conferida:** o crédito do Fish caiu de 47,73857 para 47,73020 (US$ 0,00837), igual à soma esperada dos dois modelos.

**drama-3:** tags `[serious tone]` no hook e `[urgent]` na pergunta. Ficou mais lento (35,6 s contra 25,7 s), com mais pausa dramática. O s2.1-pro, sem tag, é mais corrido.

**Whisper (small), conferido contra o texto:**
- s2.1-pro: todo o texto presente; "km/h" lido "km por hora"; a pergunta final saiu **sem** ponto de interrogação (entonação não de pergunta, a conferir de ouvido).
- drama-3: todo o texto presente; "km/h" lido "quilômetros por hora"; a pergunta final saiu **com** interrogação. Nenhuma tag foi falada.
