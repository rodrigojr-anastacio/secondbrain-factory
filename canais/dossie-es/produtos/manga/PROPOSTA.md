# Proposta v2: MANGÁ "Operación Garbo" + pôster + wallpapers (Dossier en Minutos) · 23/11/2026

Ideia do Rodrigo (23/11): um mangá com balões que conte um expediente **que o canal ainda não contou**, mais um pôster para imprimir e wallpapers. Esta versão substitui o formato da v1 (`../expedientes-pdf/PROPOSTA.md`), mas aproveita dela plataforma, recebimento, CTA e direitos. **FATO** = tem fonte; **EST.** = estimativa nossa.

## Resumo (10 linhas)
1. **História:** *Operación Garbo*, sobre Juan Pujol García, o catalão que inventou 27 espiões e enganou Hitler no Dia D. Fica entre a Espanha e a América Latina: ele nasceu em Barcelona e morreu em Caracas.
2. **Formato:** 32 páginas em 6×9 pol., 5 capítulos, 4 a 6 quadros por página e leitura **ocidental** (esquerda → direita). No fim, 2 páginas de "Lo que es real" com as fontes.
3. **Estilo recomendado:** **mangá P&B com retícula + vermelho só nos carimbos e onomatopeias**. A outra página-teste, no estilo do canal, também ficou boa (veja a comparação).
4. **Personagem consistente:** uma folha de personagem entra como referência fixa em todo quadro, junto com a mesma descrição física. **Segurou em 10/10 quadros** da amostra.
5. **Texto no código:** os quadros saem sem letras e os balões, legendas e onomatopeias são compostos em Python (PIL). As fontes são OFL.
6. **Pôster A3 300 dpi (3508×4961):** a arte do Codex ampliada com LANCZOS + nitidez, grátis. O Real-ESRGAN **estraga a retícula** e foi descartado. Para A2, gerar a arte na Gemini 4K (~US$ 0,12).
7. **Wallpapers:** 4K no desktop e 1440×3120 no celular, 3 de cada na v1.
8. **Pacote e preço:** PDF do mangá + pôster (PDF/PNG) + 6 wallpapers num zip, a **US$ 4,99**. Combo com o *Expedientes Secretos* da v1 a US$ 9,99. Venda na **Hotmart**.
9. **Série:** sim, um mangá por mês ("Expediente especial nº 2, 3…"), vendável em qualquer vídeo.
10. **Prazo e custo:** v1 em **~4–5 dias** depois do OK (2 jobs, ~150 imagens pelo Codex, US$ 0). A amostra custou **US$ 0,12**.

---

## 1. A história: 3 candidatas (nenhuma aparece nos vídeos 001–015; conferido com grep nos roteiros)

| | **A. Operación Garbo (escolhida)** | B. Operación Mincemeat | C. Las lanchas de Cherburgo |
|---|---|---|---|
| O quê | Juan Pujol, catalão, é recusado pelos ingleses, vira espião dos alemães e inventa da Espanha e de Portugal uma rede de 27 agentes que não existem. Depois o MI5 o adota e ele engana Hitler sobre o Dia D (1941–44) | Os ingleses jogam no mar de **Huelva** um cadáver vestido de oficial, com cartas falsas. A Espanha passa os papéis aos alemães, e Hitler espera o desembarque na Grécia em vez da Sicília (1943) | No Natal de 1969, sob embargo francês, Israel tira 5 lanchas de guerra do porto de Cherburgo usando uma empresa de fachada norueguesa e uma tempestade |
| Por que vira HQ | Herói azarão e engraçado, conflito em dobro (alemães e a própria esposa), reviravolta enorme (**Cruz de Ferro dos nazistas + MBE do rei**) e epílogo de cinema: finge a própria morte em Angola e reaparece na Venezuela em 1984 | Imagem forte, lugar espanhol e tensão de "será que vão cair?" | Golpe sem violência, ritmo de *heist*, mar e tempestade |
| Público es | **Espanha + LatAm (Barcelona → Caracas)** | Espanha (Huelva) | baixo vínculo |
| Risco de política | baixo: sem violência gráfica; figuras históricas mortas (Pujol †1988); filhos vivos não aparecem | médio: protagonista é um **cadáver** (Glyndwr Michael, morador de rua galês); exige respeito. Já tem filme (2021) e musical, então é menos inédito | baixo, mas o "Mossad" no título seria impreciso: foi a Marinha e o Ministério da Defesa |
| Fontes | MI5 "Agent GARBO"; Tomás Harris, *Garbo: The Spy Who Saved D-Day* (PRO, 2000); Pujol & West, *Operation Garbo* (1985); Macintyre, *Double Cross* (2012); arquivos KV 2/39–42 | Montagu, *The Man Who Never Was* (1953); Macintyre, *Operation Mincemeat* (2010) | Rabinovich, *The Boats of Cherbourg* (1988) |

**Por que A:** é a única com protagonista **hispânico**, cabe nos 3 temas fortes do canal (espionagem, Segunda Guerra, MI6/MI5 já publicados) sem repetir nada e tem humor, que é raro no nicho e combina com mangá.
**Checagem:** o MI5 diz que os alemães chamavam o próprio Pujol de **"Alaric"** e a rede inventada de **"Arabal"**. A amostra segue o MI5; o job e1 confere isso e o resto (Araceli, a pensão à "viúva" do agente fictício de Liverpool, as datas da Cruz de Ferro e do MBE) com fonte, como num `SOURCES.md`.

## 2. Formato
- **32 páginas, 6×9 pol.** (o mesmo tamanho da v1: lê bem no celular e já serve para KDP): capa · créditos + aviso de IA · **28 páginas de história** · 2 de "Lo que es real" (fatos × liberdades, fontes) · contracapa.
- **Capítulos:** 1 *El hombre que nadie quería* (Madrid–Lisboa 1941) · 2 *Inglaterra inventada* (o MI5 o encontra) · 3 *Los 27 fantasmas* (Londres, Tomás Harris) · 4 *Araceli* (a crise com a esposa) · 5 *La noche más larga* (Dia D) · epílogo *Muerto en Angola, vivo en Venezuela*.
- **4 a 6 quadros por página** (~140 quadros).
- **Leitura ocidental (esquerda → direita), recomendo:** é obra original em espanhol, lida em PDF no celular, onde o leitor passa as páginas para a direita, e o público do canal não é só leitor de mangá. O "mangá" está no traço, na retícula, nas linhas de velocidade e nos balões, não na ordem. A ordem japonesa confundiria ~metade dos leitores (EST.).

## 3. Estilo visual: as 2 páginas-teste (mesmo roteiro)
| | (a) Mangá P&B + retícula (**recomendo**) | (b) Arte do canal em quadrinho |
|---|---|---|
| Prévia | `pagina-1.jpg`, `pagina-2.jpg` | `pagina-1-estilo-canal.jpg` |
| Leitura | é mangá à primeira vista, que é o que foi pedido | parece graphic novel; continua a marca dos vídeos |
| Diferença do vídeo | produto novo (o comprador vê algo que o vídeo não tem) | "mais do mesmo" que o vídeo |
| Marca | o vermelho `#B3261E` dos carimbos e onomatopeias e o cabeçalho ligam ao canal | total |
| Impressão | P&B sai mais barato no KDP (EST.) | colorido |

**Consistência de personagem (o maior risco):** a técnica testada foi gerar 1 folha de personagem (`folha-personagem.jpg`), passá-la como referência fixa no `img_codex.py` (via `--visual`) e repetir a mesma descrição física em todo prompt. **Resultado: Pujol reconhecível em 10/10 quadros** (calvície, bigode fino, terno trespassado). O diplomata e o oficial alemão, só por descrição, também ficaram iguais entre os quadros. Na v1: 1 folha por personagem recorrente (Pujol, Araceli, Harris, Kühlenthal).

## 4. Balões e texto
- Os quadros são gerados **sem texto**. Balões de fala, pensamento e grito, legendas, "carta" e onomatopeias são desenhados em `src/diagramar.py` (PIL, em 2× com antialias), a partir de `src/paginas.json`: posição do balão em fração do quadro e rabicho apontando para a boca, em fração da imagem.
- **Fontes OFL** (`src/fontes/LEIA.md`): Bangers (onomatopeias e título), Comic Neue Bold (balões), Bebas Neue e Special Elite (já do canal). Todas com ¿¡ÁÉÍÓÚÑ. **Anime Ace: não usar** (a licença da Blambot não foi conferida e a OFL resolve).
- **Fluxo:** `gerar.py` (Codex, com orientação paisagem ou retrato) → `paginas.json` → `diagramar.py` → `pagina-N.png` (300 dpi), prévias jpg e `amostra.pdf`. Na v1 o PDF vai a ~1600 px por página para ficar < 40 MB.

## 5. Pôster em alta resolução: teste feito (`comparacao-poster-100pct.jpg`, recorte a 100 % do A3)
| Caminho | Resultado | Custo |
|---|---|---|
| Codex 1024×1536 + **Real-ESRGAN** (anime x4, x4plus e animevideov3; roda no CPU via lavapipe, ~9 min) | ❌ **transforma a retícula em textura de "labirinto"**, visível no fundo e no céu | US$ 0 |
| Codex + **LANCZOS + nitidez** (escolhido) | ✅ retícula preservada; levemente macio a 100 %, **bom em A3 visto a ~50 cm** (EST.) | US$ 0 |
| **Gemini 4K nativa** (nano-banana-2.1, 3392×5056) | linhas nítidas de verdade, mas a arte ficou mais genérica que a do Codex | **US$ 0,12** |
- **Recomendo:** A3 com LANCZOS + nitidez, grátis, como em `poster-A3.png`. Para **A2 (4961×7016)**, gerar a arte-chave direto na Gemini 4K e comparar antes. Outra saída: pedir a arte do pôster **sem retícula** (tinta + preto chapado); aí o Real-ESRGAN fica limpo (Hipótese).

## 6. Wallpapers
- Amostra: `wallpaper-desktop.jpg` (3840×2160) e `wallpaper-celular.jpg` (1440×3120; título embaixo, longe do relógio). Na v1 entram **3 de cada**: a mansarda do rádio, o céu de espiões, a capa sem texto, Lisboa e a praia na alvorada.

## 7. Pacote e preço
- **Zip:** `Operacion-Garbo.pdf` (32 p.) + `poster-A3.pdf/png` + 6 wallpapers. ~60–80 MB (EST.).
- **Preço: US$ 4,99** (~MX$ 89) por mangá. **Combo US$ 9,99** com o *Expedientes Secretos* da v1, se ele sair.
  - Referência: no itch.io, PDFs de quadrinho indie aparecem com mínimo de US$ 8–10 ([Kamthology](https://kamthings.itch.io/kamthology), [post](https://itch.io/post/6722067)). Vendedores comentam que preço sem nº de páginas soa caro ([guia de zines](https://yamino.itch.io/beginners-guide-to-digital-zines)), então a página de venda mostra "32 páginas + pôster + 6 wallpapers". O History in Minutes vende a US$ 9,99 (FATO, v1). Não achei dado firme de preço de mangá indie em espanhol: os US$ 4,99 são EST. para compra por impulso a partir de um vídeo grátis.
- **Plataforma: Hotmart** (motivos da v1: OXXO, SPEI, Mercado Pago e saque em BRL). Entregar um zip não muda nada: a área de membros aceita arquivo e troca de versão. O itch.io (10% padrão, ajustável) fica como 2ª vitrine se a Espanha pedir.
- **Série: sim.** Um "Expediente especial" por mês, vendável em qualquer vídeo (mesmo CTA). Depois de 3 números, um "pase" com todos (EST. US$ 11,99).

## 8. Produção e custo
| Etapa | Quem | Tempo / custo |
|---|---|---|
| e1 (Opus) | checagem dos fatos com fonte, roteiro página a página (`paginas.json` com textos) + prompts de cada quadro | ~2–3 h, US$ 0 (Max) |
| e2 (Sonnet) | 4 folhas de personagem, ~140 quadros, capa, 6 wallpapers (**~150 imagens Codex**), diagramação, QA visual de todas as páginas, pôster, zip, Drive | ~4–6 h, **US$ 0** (Gemini só se faltar Codex: ~US$ 0,05/img) |
| Rodrigo | ler o PDF (~20 min), decidir o preço, conta Hotmart (a mesma da v1), subir o zip | ~1 h |
- **Cota do Codex:** os 21 quadros da amostra subiram a janela de 5 h de 5 % → 9 % e a semana de 13 % → 14 %. 150 imagens ≈ ~35–40 % de uma janela de 5 h e ~8–10 % da semana (EST.). **Produzir de dia na qua/qui/sex** (sem fábrica noturna), em 2 blocos, com `fila.sh add … --agora`.
- **Prazo da v1:** ~4–5 dias depois do OK.

## 9. Direitos (o que muda em relação à v1)
- Vale tudo da v1: output de IA pode ser vendido, colofão "ilustraciones generadas con IA", nada de selo oficial nem foto de arquivo, texto autoral passando no detector de cópia.
- **"Estilo mangá"** é gênero, não obra: nada de imitar autor ou série específica nos prompts ("in the style of X" é proibido), nem personagem existente. Isso foi seguido na amostra.
- **Pessoas reais:** Pujol, Harris, Kühlenthal e o diplomata (genérico, sem nome) são figuras históricas mortas, retratadas sem degradação. **Filhos de Pujol (vivos) não aparecem.** Araceli: retratar com respeito, sem inventar cena íntima, e com o fato marcado em "Lo que es real". Hitler, se aparecer, só de costas ou em silhueta e sem insígnia (regra do canal).
- **Fontes tipográficas:** todas OFL ou Apache, embutíveis no PDF vendido.
- **Liberdades dramáticas** (diálogos reconstruídos) vão declaradas nas 2 páginas de "Lo que es real".

## 10. Divulgação
- **Linha fixa no topo da descrição:**
  > 📘 NUEVO: *Operación Garbo*, el manga del español que engañó a Hitler (32 páginas + póster para imprimir + wallpapers) → [link]
- **Comentário fixado (sem link):**
  > ¿Sabías que un catalán inventó 27 espías que nunca existieron… y Hitler le dio la Cruz de Hierro? Lo contamos en manga, con viñetas y bocadillos. Enlace en la descripción. ¿Qué expediente quieres en el próximo manga?
- **Fecho falado (~6 s):** *"Y si quieres una historia que no está en el canal, el manga de Operación Garbo está en la descripción."*
- **Teaser:** `teaser.jpg` (1280×720) para a aba Comunidade e a imagem do Short ("link en el perfil"; sem YPP o link não é clicável no Short, como na v1).

---

## Arquivos da amostra (prévias jpg ≤ 1 MB)
`capa.jpg` · `pagina-1.jpg` · `pagina-2.jpg` · `pagina-1-estilo-canal.jpg` · `folha-personagem.jpg` (+ `-estilo-canal`) · `poster-preview.jpg` (+ `poster-A3.png` 300 dpi, 15 MB) · `wallpaper-desktop.jpg` · `wallpaper-celular.jpg` · `teaser.jpg` · `comparacao-poster-100pct.jpg` · `amostra.pdf` (capa + 3 páginas). Código em `src/` (`gerar.py`, `diagramar.py`, `extras.py`, `gemini_4k.py`, `paginas.json`, prompts `cenas-*.json`, `visual-*.yaml`). Mídia fora do git (`.gitignore`).
**Custo da amostra:** 21 imagens no Codex (US$ 0) + 1 teste Gemini 4K = **US$ 0,12** (`financas.consumo`).

## O que precisa da decisão do Rodrigo
1. **História:** Garbo (recomendo), Mincemeat ou Cherburgo.
2. **Estilo:** (a) mangá P&B + vermelho (recomendo) ou (b) arte do canal.
3. **Páginas:** 32 (recomendo) ou mais curto (24) para sair mais rápido.
4. **Preço:** US$ 4,99 sozinho / US$ 9,99 no combo com a v1 (recomendo).
5. **Plataforma:** Hotmart (recomendo; a mesma conta da v1).
6. **Série mensal** sim/não e OK para disparar os 2 jobs (de dia, qua/qui/sex).
