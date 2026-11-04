# 003 Irã v2, FASE 1: amostras para aprovação (04/11/2026)

O brief é o `~/workspace/referencias/BRIEF-historia-003-v2.md`, com o escopo reduzido pelo `AVISO-ESCOPO.md` (só a estrutura do roteiro). Nada foi regenerado nem publicado.

## 1. Imagens: "usou os mesmos prompts?"
**Sim, foram os mesmos.** O `estilo_prompt` é idêntico ao do Egito e da Índia, e os prompts de cena seguem o mesmo padrão. **O que mudou foi o modelo:** o 003 saiu no `fal-ai/flux/dev`, que ignora "round white heads", e não no gpt-image-2. Comparação em `imagens/diagnostico-gpt-vs-flux.jpg`.

Bancada com 12 configurações × 2 cenas em `imagens/grade-1.jpg` e `grade-2.jpg`. As notas estão em `imagens/MODELOS.md`, e o catálogo completo do fal (213 geradores, com preço a 1536×864) em `imagens/catalogo/CATALOGO.md`.

**Recomendo:**
1. **`openai/gpt-image-2` medium dentro do fal, US$ 0,04/img** (vencedor). É o mesmo estilo do Egito e da Índia, sem recarregar a OpenAI.
2. `openai/gpt-image-2/edit` low + refs do canal, US$ 0,02/img. Precisa de teste de zoom antes.
3. `google/nano-banana-2.1/edit` + refs, US$ 0,044/img (plano B fora da OpenAI).

Nenhum modelo fora da família gpt-image chegou ao nível do gpt-image-2. **Tire o flux/dev do canal.**

## 2. Voz: Fish `drama-3` (o mais recente, lançado em 13/10/2026)
- O clone funciona nele.
- O preço é US$ 10/M bytes até 12/11 e US$ 50/M depois.
- A voz sai ~1,7 st mais aguda.

Amostras em `voz/` (ordem de escuta e medidas no `voz/LEIA.md`):
- **A**: texto atual, s2.1-pro, por bloco (a de hoje).
- **B**: texto atual no drama-3.
- **D**: drama-3 com direção de narrador numa chamada só.
- **C2**: texto **reescrito** no s2.1-pro, técnica A.
- **C**: texto **reescrito** no drama-3 com direção de narrador.

**Sugestão:** comparar A × C2 × C. Nas medidas, o texto reescrito deixou as frases menos "caídas" (−4,2 → −3,45 st), e o C teve a maior faixa melódica. Quem decide é o ouvido do Rodrigo.

## 3. Roteiro: só a estrutura
A estrutura está em `ESTRUTURA-ROTEIRO.md`:
- **Diagnóstico:** a v1 usou fichas no molde Archive, com ganchos de charada, sem fio condutor dito em voz alta e com texto de ficha.
- **Hook HiM:** "paraíso" é palavra persa → invasores que viram persas → pergunta central → promessa em lista.
- **Corpo:** 10 eras com a ponte "mas… então…" escrita.
- **Fio condutor:** a língua e o paraíso. São 7 "guarde isso", com o lugar onde cada um é pago.
- **Fecho:** volta ao túmulo-jardim de Ferdowsi.

Existe um rascunho corrido, escrito antes do aviso, em `rascunho-roteiro-v2.md`. **Não está aprovado.**

## 4. Thumbs: 4 conceitos (`thumbs/`, `CONCEITOS.md`, pesquisa de 52 thumbs do nicho)
1. **PÉRSIA → IRÃ:** um rei aquemênida × um clérigo, antes e depois.
2. **SALVOU O IRÃ?:** o caixão brilhando e o bonequinho em choque (lacuna de informação).
3. **COROA × TURBANTE:** o xá × o clérigo, "1891 · 1979" (conflito).
4. **VIRARAM PERSAS:** os conquistadores tomando chá num tapete (humor; fica de reserva).

Para o "Testar e comparar", recomendo a 1, a 2 e a 3. As propostas para trocar as thumbs do Egito e da Índia também estão no `CONCEITOS.md`.

## Custo da fase 1 (financas.consumo, ref_id 5, notas 'v2…')
**US$ 0,99** de um teto de US$ 9:
- fal: US$ 0,93 (bancada 0,70 + thumbs 0,23);
- Fish: US$ 0,05.

**Alerta:** o saldo **real** do fal está em **US$ 0,67**, mas o banco diz US$ 4,43, então há consumo sem lançamento. A FASE 2 (~190 imagens × US$ 0,04 ≈ US$ 7,60 + thumbs) **exige recarregar o fal**.

## Decisões do Rodrigo para destravar a FASE 2
1. Modelo de imagem (recomendo gpt-image-2 medium no fal) e recarga do fal.
2. Voz: A, C2 ou C (modelo + técnica).
3. Aprovar ou ajustar a estrutura do roteiro.
4. Quais 3 thumbs (e se troca as do Egito e da Índia).
