# BRIEF: dossie-es 001, CIA (`youtube.videos` id 7)

**Status (2026-11-04, 19:30):** **pronto para publicar**: 11:46, "TODA la historia de la CIA en 12 minutos", entrega em `entrega/`, relatório em `RELATORIO.md`. OK do Rodrigo dado em `~/workspace/referencias/BRIEF-dossie-001.md` (voz Dio Historias). O canal existe no YouTube (`UCVCYqeuCwTWC7Lqez_qeWRA`), ainda com o nome "Dossiê em Minutos": renomear antes do 1º vídeo (ver `../../identidade.md`).

- **Título de trabalho:** TODA la historia de la CIA en 11 minutos. N = duração real; recalcular no render.
- **Título B** (para o "Testar e comparar"): La historia COMPLETA de la CIA en 11 minutos.
- **Idioma:** espanhol neutro latino-americano (tú). **Duração-alvo:** 11–12 min. **Texto:** ~1.500 palavras narradas (hook de ~85 palavras + 13 expedientes + cierre).
- **Por que a CIA, e não a KGB, como piloto em es** (`pesquisa/archive-in-minutes/IDIOMA.md` §5):
  - a CIA tem a maior demanda em es entre as organizações clássicas: mediana do top-10 de **1,10 mi**, contra 372 mil da KGB, e 18 vídeos de 2026 acima de 100 mil [O];
  - a KGB em es já tem Te lo Pinto (139 mil), Atlas del Tiempo (30,6 mil) e quase todos os clones;
  - o ângulo **América Latina** (Guatemala, Cuba, Chile) é nosso e ninguém no molde o usa.
- **Referências:** Archive in Minutes, CIA (141 mil); Atlas del Tiempo, "CIA vs KGB" (15,2 mil) e "TODA la Historia del Mossad en 17 Minutos" (`9LyvAHVecwY`, 33,1 mil; o hook abre com Eichmann). Assets em `pesquisa/tendencias/assets/2026-11-04/`.
- **O que muda em relação às referências:** hook com a rádio da Guatemala (1954), não com Dulles ou Langley; loop pago (a rádio → a desculpa de Clinton na mesma cidade, em 1999); expedientes-objeto próprios (El coronel, La ley, Las maletas, El petróleo, La radio, El ácido, La foto, La bahía, Los puros, La orden, Las joyas, El misil, El error).
- **Visual:** `canal.yaml` (nano-banana 16:9) + `estilo.md`. ~140 imagens para ~11 min, sem reuso até 3:00 e com ~35% de reuso depois. Mapas com pinos **no código**: Washington→Roma, Teerã, Honduras→Guatemala, Cuba, Chile, Afeganistão. Teste es em `../../testes/ESTILO-es.md`.
- **Voz:** Fish s2.1-pro, por frase. Sugestão "Dio Historias" (`ac594943984a47e7a827416eb263c7b1`); 3 finalistas em `../../testes/voz/LEIA.md`. Escolha do Rodrigo.
- **Teto de custo (US$):** **9** = imagens ~140 × 0,039 ≈ 5,5 + thumb e variações ~0,5 + Fish ~0,20 + margem de regeração ~2,8. Já gastos US$ 0,43 em testes (voz US$ 0,04 + imagens US$ 0,38; `financas.consumo` com `ref_id` = 7).
- **Saldos (2026-11-04):** fal.ai ~US$ 23,7; Fish ~US$ 49; **OpenAI sem crédito**.

## Pendências antes de produzir
1. OK do Rodrigo: idioma (es), nome/handle, voz e produção.
2. Converter o `SCRIPT.md` em `roteiro.py` (skill `roteiro`), com `IDEIA` e tags de tom. Revisar o espanhol: Whisper na voz e 2ª leitura de LLM (ver `../../estilo.md`, "Revisão em espanhol").
3. Adaptar o Remotion: cartão "EXPEDIENTE N", rótulo em máquina de escrever, sello rojo; tudo em espanhol.
4. Descrição em espanhol com fontes (edições em espanhol quando houver) e a nota "Narración con voz sintética; ilustraciones generadas con IA a partir de investigación histórica".

## Critérios de pronto
Os da skill `qa`, mais: N do título igual à duração; nenhum texto em português na tela nem na descrição; Whisper ≥ 95% por bloco; fontes na descrição.
