# BRIEF: dossie-ptbr 001, KGB (`youtube.videos` id 6)

**Status:** roteiro completo (`SCRIPT.md`); **produção aguarda o OK do Rodrigo** (voz, imagens, render). O canal ainda não existe no YouTube.

- **Título de trabalho:** A história INTEIRA da KGB em 12 minutos (N = duração real; recalcular no render).
- **Idioma:** pt-BR. **Duração-alvo:** 11–13 min. **Texto:** ~1.500 palavras (hook de 65 palavras + 13 fichas).
- **Referência principal:** Archive in Minutes, "The ENTIRE History of the KGB in 13 Minutes" (`VNJhu4rh6OY`): 236 mil views em 17 dias, 13:51, 18 cortes/min, 8 capítulos "lugar, ano". Hook real: "December 1989, Dresden. A KGB officer burns files so fast the furnace bursts… His name is Vladimir Putin. This is the entire history of the KGB, from 40 men to an empire of secrets, and why it never died."
- **Referências secundárias:** Te lo Pinto (es), "La HISTORIA COMPLETA de la KGB" (`by7uTDjSx7Y`, 138 mil, 36 min); Fuse Room (clone en, `uBRJbDwWc9Q`, 9,8 mil). Assets em `pesquisa/tendencias/assets/2026-11-04/<id>/`.
- **O que muda em relação à referência:**
  - hook com **outra anedota** (Markov e o guarda-chuva, 1978), não Dresden/Putin, que todos repetem;
  - **loop pago** no fim (guarda-chuva 1978 → bule de chá 2006, mesma cidade);
  - fichas-objeto próprias (A espada, O prédio, As cotas, O picador de gelo, A bomba, O nome, Os cinco, O hospital, O guarda-chuva, A sacola, O arquivista, A estátua, O bule);
  - "Guarde esse prédio" (Lubianka), pago no fecho.
- **Visual:** `canal.yaml` (nano-banana 16:9) + `estilo.md`. ~150 imagens para ~12 min (0% de reuso até 3:00, ~35% depois). Mapas: Petrogrado→Moscou, Moscou→Coyoacán, Semipalatinsk, Moscou→fronteira finlandesa, Riga.
- **Voz:** Fish s2.1-pro, voz nova a escolher (não a do `historia-ptbr`).
- **Teto de custo (US$):** **10** = imagens ~150 × 0,039 ≈ 5,9 + thumb e variações ~0,5 + Fish ~0,25 + margem de regeração ~3. Já gastos US$ 0,79 nos testes de estilo (`financas.consumo` ids 24–27).
- **Saldo (2026-11-04):** fal.ai US$ 24,87 no banco; **OpenAI sem crédito** (a API respondeu "no credits remaining"); Fish US$ 49,32.

## Pendências antes de produzir
1. OK do Rodrigo: nome do canal, voz e produção.
2. Converter o `SCRIPT.md` em `roteiro.py` (skill `roteiro`; copiar o setup de `canais/historia-ptbr/videos/002-india/` sem `node_modules`, só para leitura) com `IDEIA` e tags de tom.
3. Adaptar o Remotion: cartão "FICHA N", rótulo em máquina de escrever, carimbo e pasta (ver `estilo.md`); trilha nova.
4. Conferir, no QA, a nitidez de 1344×768 com Ken Burns (Hipótese em `testes/ESTILO.md`).

## Critérios de pronto
Os da skill `qa` + N do título = duração; nenhuma suástica ou insígnia em destaque; fontes na descrição; nota de voz e imagem sintéticas.
