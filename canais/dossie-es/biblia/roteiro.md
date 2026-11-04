# Roteiro: dossie-es (molde Archive in Minutes)

Regra de canal: **prevalece** sobre `conhecimento/roteiros.md` e `conhecimento/hooks.md`. Toda entrada leva data e fonte; sem dado = **Hipótese**.
Base: `pesquisa/archive-in-minutes/LEVANTAMENTO.md` §2 (anatomia, 2026-11-04), transcrições completas do Archive "Gestapo" (pbIzG1QvoWs) e "KGB" (VNJhu4rh6OY) em `canais/historia-ptbr/videos/003-ira/ref/` (Whisper, 04/11/2026), o `estilo.md` do canal (04/11) e o piloto `videos/001-cia/SCRIPT.md`.

---

## Estrutura (do hook ao cierre)
1. **Hook de 25–35 s, molde anedota:** data + lugar → cena humana concreta em 2–4 frases curtas, no presente → **desfecho seco ou reviravolta** → "Esta es TODA la historia de X" → promessa em 1 linha. Sem "hola", sem vinheta, sem pedir inscrição.
   - Archive [O]: Gestapo "In 1943, a war widow tells a colleague at her munitions factory a joke… The colleague reports her. She is put to death. This is the entire history of the Gestapo, and how a small police force watched 80 million people." (promessa aos 9 s, hook ~18 s) · KGB "December 1989, Dresden. A KGB officer burns files so fast the furnace bursts… His name is Vladimir Putin." (13 s; ~22 s) · SS "…thousands of silver rings with a skull… They have never been found."
   - Nosso piloto CIA [O]: "Ciudad de Guatemala, junio de 1954. Cada noche, una radio clandestina anuncia que miles de rebeldes avanzan sobre la capital. […] Los miles de rebeldes eran menos de quinientos. Y la radio… la operaba la CIA. Esta es toda la historia de la CIA. Y de lo que hizo, una y otra vez, en América Latina."
   - Use uma anedota **diferente** da do Archive e dos clones (Eichmann no Mossad e Putin em Dresden na KGB já foram usados; os clones copiam a mesma). Cena genérica sem nome nem fato verificável perde força (Fuse Room, "Moscow, 1971…", 9,8 mil views). [LEVANTAMENTO §2c]
2. **EXPEDIENTES (capítulos-objeto): 11–14 de 45–75 s**, cronológicos (fundação → auge → crimes → queda → herança). Título "EXPEDIENTE N: EL/LA <OBJETO>", 1–2 palavras com artigo, **falado** no começo ("El Coronel.", "La Radio.", "Las Maletas.", "La Bahía."). Cada expediente é **uma cena ou objeto concreto datado**, com números exatos e fonte.
   - Archive [O]: 13–17 capítulos de 40–70 s ("The joke", "The stamp", "The card index", "The cellar", "The rings"); o KGB usa "lugar, ano" ("Dresden, 1989") e tem 8.
3. **Cada expediente puxa o próximo:** o fim do capítulo prepara o objeto seguinte; o melhor é terminar com a frase que **é** o título do próximo ("…entregue a um homem que já criou galinhas. O criador de galinhas."). Re-hook a cada ~60–90 s. [estudo de 04/11, ex-`conhecimento/roteiros.md`]
4. **Pague a anedota** entre 1/4 e 1/2 do vídeo ou no fim: o Archive Gestapo volta à viúva aos 3:29 com o detalhe cruel ("os juízes contaram contra ela que o marido morreu pela pátria"); o KGB paga no fim (o oficial de Dresden vira presidente). [estudo de 04/11]
5. **Cierre:** volta ao objeto do hook (Gestapo: "The joke" → "The cellar"; SS: "The skull rings" → "The rings"), + aforismo de 2 frases ("A Gestapo nunca foi grande. Grandes eram as pessoas que escreviam para ela.") + liga ao presente + 1 pergunta ("Y tú, ¿…? Déjalo en los comentarios."). Piloto CIA: "Cierre. La Disculpa".
6. **CTA de inscrição:** no meio, colado num re-hook (Archive Gestapo, 3:45). O Archive não tem CTA no hook nem patrocínio. [estudo de 04/11; LEVANTAMENTO §2d]

## Tom
- **Presente histórico**, factual, seco, quase sem adjetivo; o horror vem do fato. Números exatos, nomes e lugares (viram rótulo na tela).
- Toda acusação atribuída a um documento ("según documentos desclasificados…", "un comité del Senado documentó…"). Fato incerto é dito como incerto.
- **Ângulo América Latina** sempre que houver fato real com fonte (Guatemala, Cuba, Chile, Operação Condor, cartéis, nazistas na Argentina). É a diferença em relação ao Archive e aos clones.
- Escreva para a fala (regra geral em `conhecimento/roteiros.md`): frases de 4–14 palavras, números por extenso quando o Fish ler mal, datas como "27 de junio de 1954".

## Idioma: espanhol escrito nativamente
1. Direto em espanhol, **nunca traduzido do pt**. Falsos amigos: "exquisito", "embarazada", "polvo", "largo" (= comprido), "oficina" (= escritório).
2. Espanhol neutro com **tú** (nunca "vosotros"); sem gírias locais ("chido", "guay", "boludo"); termos neutros (evite "computadora/ordenador"). Público [O, `idioma/NOTAS.md` §3]: MX 22%, ES 22%, US 9%, AR 6%.
3. **2ª leitura por LLM** antes do `roteiro.py` (e antes da voz): "revise como editor nativo mexicano e depois como editor espanhol: erros, calcos do português, termos regionais". No piloto CIA (subagente Sonnet, nota 8/10) os erros foram calcos do inglês ("sostenidas por", "pareció aprobarlo"), vírgula antes de "y", "lleva adelante" (rioplatense) e "invencible". [`videos/001-cia/RELATORIO.md`, 04/11]
4. O Rodrigo lê o `SCRIPT.md` e o pacote, mas não é nativo: dúvida de sentido = reescrever a frase.

## Tamanho
- **11–16 min (alvo 13)**; acima de ~17 min, não (os de 16–20 min do Archive se espalham entre hits e flops; os de 31–36 min da Prima Historian ficaram em ~1 mil). [LEVANTAMENTO §2a]
- **Medido no piloto CIA (2026-11-04):** 1.686 palavras, 78 blocos, hook + 13 expedientes + cierre = **706,4 s (11:46), ~143 ppm** com as pausas do `build.py`; o `WPS = 2.3` do `roteiro.py` estimou 12:21 (5% acima). **Para 13 min, mire ~1.850 palavras.** [`videos/001-cia/RELATORIO.md` e `QA.md`; ex-`estilo.md` e ex-`conhecimento/roteiros.md`]
- Antes do piloto: ~140 palavras/min nas amostras Fish es (1.500 ≈ 11 min; 1.800 ≈ 13 min). O Archive fala ~160–170 ppm (13 min ≈ 2.100 palavras na fala deles). [canal.yaml; SCRIPT.md 001; LEVANTAMENTO §2d]

## Checklist do roteiro
- [ ] Hook ≤ 35 s com anedota própria (não a do Archive/clones), desfecho seco e "Esta es TODA la historia de X".
- [ ] 11–14 expedientes de 45–75 s, cada um uma cena/objeto datado, título falado; o fim de cada um puxa o próximo.
- [ ] Anedota paga; cierre volta ao objeto do hook + pergunta.
- [ ] Toda acusação atribuída a fonte; ângulo América Latina presente.
- [ ] Revisão nativa feita; nenhuma palavra em português.
