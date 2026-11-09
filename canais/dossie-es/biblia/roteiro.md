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

- **Medido no 002 Mossad (05/11):** 1.954 palavras, 85 blocos, 13 expedientes = **822,7 s (13:43), ~143 ppm**; o `roteiro.py` com `WPS = 2.38` estimou 13:50 (erro de 1%): use 2,38. O hook saiu com 40 s (5 s acima): corte o hook no texto antes da voz. [`videos/002-mossad/RELATORIO.md`]
- **Tema sensível (002):** morte atribuída a serviço secreto sempre com fonte ("se atribuye al Mossad", "según historiadores y periodistas") e a versão do outro lado ("su entorno siempre lo negó"); inclua o erro do próprio serviço (Lillehammer); recorte fechado no passado e 1 frase neutra de presente. A revisão nativa pegou 3 atribuições que faltavam. [`videos/002-mossad/RELATORIO.md`]
- **Medido no 003 FBI (05/11):** 1.830 palavras, 80 blocos, 13 expedientes = **796,6 s (13:17)**; o `roteiro.py` (WPS 2,38) estimou 12:57 (2,6% abaixo). Hook de 31 s: o `roteiro.py` do 003 avisa quando o hook passa de 35 s (`HOOK_MAX`). [`videos/003-fbi/RELATORIO.md`]
- **Hook por arrombamento/roubo de arquivos (003):** a anedota em que a organização é a vítima ("La oficina era del FBI") inverte o esperado e deu desfecho seco em 4 palavras; pago no expediente 10 (2/3 do vídeo, porque a cronologia manda) e no cierre ("La Cerradura"). **Hipótese** até ter retenção do Studio. Concorrentes do FBI abrem com a morte de Hoover (2 de 4), Dillinger e 11-S. [`videos/003-fbi/SOURCES.md`]
- **Revisão de fatos no 003:** a 2ª leitura (subagente Sonnet) pegou 4 erros reais antes da voz (Hanssen vendeu primeiro ao GRU, não à KGB; a carta a King não "termina" com a frase citada; ordem do fim do COINTELPRO; cronologia perpétua × 11-S). Peça sempre ao revisor que cheque **fatos e cronologia**, não só o espanhol. [`videos/003-fbi/RELATORIO.md`]
- **Medido no 004 Cosa Nostra (05/11):** 1.994 palavras, 83 blocos, 13 expedientes = **872,3 s (14:32)**; o `roteiro.py` (WPS 2,38) estimou 14:06 (3% abaixo, mais pausas de capítulo). Hook de 31,7 s. Para ficar em 13–14 min, mire ~1.850 palavras: tema de 130 anos pede cortar, não espremer. [`videos/004-cosa-nostra/QA.md`]
- **Hook por ritual de iniciação (004):** o juramento do santinho queimado de Buscetta (1945), pago no expediente 10 ("rompe su juramento") e no cierre "La Estampa". Antes de usar uma cena íntima como hook, confirme que **a própria pessoa** a relatou (o revisor achou só o rito genérico; a AGI confirma que Buscetta descreveu a dele): senão vira reconstrução. **Hipótese** até ter retenção. Concorrentes es/en abrem com definição, "imagina vivir…" ou os limões. [`videos/004-cosa-nostra/SOURCES.md`]
- **Revisão de fatos no 004:** 6 correções antes da voz (Ciaculli: carabineiros e artificieiros, não policiais; Gangi: cortou as comunicações, não a água; "murió en la mesa" era lenda; mês e veneno do suicídio de Buscetta divergem; derrota da máfia declarada pela propaganda, não por Mussolini; Inzerillo 18 dias depois). Tema de crime organizado: **lenda de filme se infiltra nos fatos**; peça ao revisor que separe lenda de documento. Inclua 1 frase que lembre quem era o arrependido ("mafioso y traficante de heroína") para não virar herói.

- **Medido no 005 KGB (09/11):** 1.961 palavras, 87 blocos, **14 expedientes** = **845,3 s (14:05)**; o `roteiro.py` (WPS 2,38) estimou 13:53 (1,5% abaixo). Hook de 30,1 s (74 palavras). [`videos/005-kgb/QA.md`]
- **Hook com morte atribuída por terceiros (005):** o guarda-chuva de Markov (1978), pago no expediente 11 (logo depois do CTA de inscrição, "volvemos al puente de Waterloo") e no cierre "La Bolita". Concorrentes da KGB em es: Te lo Pinto abre com a fundação de 1917 e Atlas com Putin em Dresden; nós fechamos sem Putin. **Hipótese** até ter retenção. Para tirar o "buraco" de 6:00–7:46 visto na CIA, o 005 põe ali as 2 anedotas mais fortes de América Latina (Feklisov/Cuba 6:31 e Oswald no México 7:30): conferir a curva nesse trecho.
- **Revisão de fatos no 005:** 10 correções antes da voz (ricina inferida, não detectada; Kostov 12 dias antes; execução búlgara e ajuda da KGB atribuídas a investigadores/Kalugin; o sinal de Gordievski e a corrida eram dias diferentes; detalhe da comida na bolsa de Mitrokhin sem fonte; "bidones" de leite; Cheka > 200 mil com tropas; psiquiatria punitiva não era "arma nova"; origem do emblema; deserção de Häyhänen em Paris). Tema de espionagem: **detalhe de filme/livro de divulgação** (sacola, comida, guarda-chuva) se infiltra; peça ao revisor a cena exata. [`videos/005-kgb/SOURCES.md`]

## Checklist do roteiro
- [ ] Hook ≤ 35 s com anedota própria (não a do Archive/clones), desfecho seco e "Esta es TODA la historia de X".
- [ ] 11–14 expedientes de 45–75 s, cada um uma cena/objeto datado, título falado; o fim de cada um puxa o próximo.
- [ ] Anedota paga; cierre volta ao objeto do hook + pergunta.
- [ ] Toda acusação atribuída a fonte; ângulo América Latina presente.
- [ ] Revisão nativa feita; nenhuma palavra em português.

## Métricas 2026-11-09 (relatório semanal)
- **CIA** (11:47): 83% em 0:42, 70% em 1:17, 52% em 3–5 min, 48% em 6:00, 35% em 7:46; 45,2% assistido (39 views). **Mossad** (13:43): 68% em 0:49, 60% em 1:30, 53% em 4:15, 43% em 5:37–7:40, 38% em 8:22–9:03; 44,3% assistido, 206 views em 3 dias. Retenção acima dos "similares" nos dois. Queda visível no trecho 6:00–7:46 da CIA (**Hipótese:** testar uma virada/anedota ali). FBI (4 views) e Cosa Nostra (0) sem retenção ainda: os hooks de 003/004 seguem **Hipótese**. Fonte: `report.py dossie-es --retencao`, `pesquisa/metricas/2026-11-09.md`.
