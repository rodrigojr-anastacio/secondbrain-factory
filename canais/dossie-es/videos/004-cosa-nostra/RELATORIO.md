# RELATÓRIO · dossie-es/004 · "TODA la historia de la Cosa Nostra en 15 minutos" (youtube.videos id 11)

Job: `~/workspace/referencias/BRIEF-dossie-004-cosa-nostra.md` (05/11/2026, ~21h10–22h30). Orquestrador: Claude Code (Opus) nesta sessão, que fez a pesquisa, o roteiro e o storyboard. A checagem de fatos e a 2ª leitura nativa foram feitas por um subagente Sonnet com buscas web. Voz, imagens, build e render são comandos determinísticos, todos em primeiro plano. Um job do historia-ptbr (China) rodou em paralelo: os 5 renders esperaram a CPU livre (`tools/espera_render.sh`) e não toquei nos caminhos dele. Nada foi publicado nem enviado ao Telegram.

## Entrega (`entrega/` + Google Drive `Youtube/Dossier en Minutos/004-cosa-nostra/`)
- `video.mp4`: **14:32**, 1080p30, −15,3 LUFS;
- `thumb-A.jpg` (o chefe com o santinho queimando, "EL JURAMENTO"), `thumb-B.jpg` (o juiz com os autos, "ROMPIÓ EL SILENCIO") e `thumb-C.jpg` (dedo nos lábios, faixa "UN SIGLO DE SILENCIO"). Nenhuma com arma;
- `pacote.md`: título A/B, descrição com links da CIA e do FBI, 15 capítulos, fontes, tags, checklist e tradução pt-BR;
- `legendas.srt` (es).
- QA aprovado (`QA.md`): 0 telas pretas, Whisper com 96,5% de média, hook de 31,7 s, 204 imagens + 3 thumbs, 2 mapas com pinos no código.

## Título
**"Cosa Nostra"** venceu: entre os vídeos de história em es (busca yt-dlp via WARP, 6 consultas, sem músicas nem filmes), "Cosa Nostra" aparece em 24 títulos com mediana top-10 de ~451 mil views; "Mafia italiana", em 13 (~259 mil); "Mafia siciliana", em 4 (~90 mil). Título B: "La historia COMPLETA de la Cosa Nostra en 15 minutos". Registrado no `backlog.md` e na `biblia/titulo.md`.

## O roteiro
- **Hook (31,7 s):** Palermo, 1945. Buscetta, aos 17 anos, jura com o santinho queimando nas mãos: "si traiciono, que mi carne arda como arde este santo". "Cuarenta años después, se lo contará todo a un juez." Concorrentes es/en abrem com definição, "imagina vivir…" ou os limões; ninguém usa o juramento. Pago no expediente 10 ("Buscetta rompe su juramento", com Falcone) e no cierre "La Estampa" (Riina preso em 1993).
- **13 expedientes:** El Nombre, El Detective (Petrosino), El Prefecto (Mori), El Restaurante (Masseria/Luciano), El Puerto, El Hotel (La Habana), Las Reuniones (des Palmes + Apalachin), El Cemento (saque de Palermo + Ciaculli), La Guerra, El Arrepentido, La Pizzería, El Búnker (Maxiprocesso), La Autopista (Capaci e via D'Amelio).
- **América Latina e trinca:** Havana 1946–59 e o complô CIA–máfia contra Castro (liga com o 001), Buscetta preso em São Paulo (1983), Apalachin (liga com o 003) e Louis Freeh na Pizza Connection (também do 003). O fecho pede comentário e puxa para os expedientes da CIA e do FBI.
- **Sem glamour:** as vítimas têm nome (Petrosino, os 7 de Ciaculli, Dalla Chiesa, Falcone, Morvillo, Montinaro, Dicillo, Schifani, Borsellino e 5 agentes); Buscetta aparece como "mafioso y traficante de heroína". Frase de presente: Messina Denaro preso em 2023.
- **Números:** 1.994 palavras e 83 blocos. Estimado em 14:06 (WPS 2,38) e medido em 14:32 (+3%).

## Custo (financas.consumo, ref_id 11)
| Etapa | Itens | US$ |
|---|---|---|
| Voz (83 blocos, por frase) | Fish s2.1-pro (crédito caiu US$ 0,157, preço do s2.1-pro) | 0,18 |
| Lote (204 cenas + 3 thumbs) | fal nano-banana, medido pelo uso do endpoint (o job da China usa outro endpoint) | 8,24 |
| 4 refeitas | fal | 0,16 |
| **Total direto** | | **8,58**, teto de US$ 10 |
- Saldo depois do job: fal ~US$ 63,1 (inclui o gasto do job da China); Fish ~US$ 48,06.

## Correções de fatos (antes da voz; detalhes em `SOURCES.md`)
1. **Ciaculli:** os 7 mortos eram carabineiros e artificieiros do Exército, não policiais.
2. **Gangi:** Mori cortou as comunicações, não a água; reféns eram mulheres e filhos dos procurados.
3. **Masseria:** "muere en la mesa" é lenda → "muere a tiros"; a versão do banheiro ficou como "según la versión más conocida".
4. **Suicídio de Buscetta:** fontes divergem sobre mês, lugar e veneno → "en 1984, antes de ser extraditado… con veneno".
5. **1929:** a derrota da máfia foi declarada pela propaganda fascista.
6. **Inzerillo:** 18 dias depois de Bontade → "menos de tres semanas".
7. **Havana:** a ameaça de Anslinger era cortar os medicamentos com narcóticos; Luciano foi preso antes da expulsão; os cassinos fecharam "poco después".
8. **Hook:** o rito foi confirmado como relato do próprio Buscetta (AGI); o expediente 10 diz "según su propio relato".

## Revisão do espanhol
Nota 8,5/10. Mudanças aplicadas: "la queman entre sus manos" (era ambíguo), "como arde este santo", "la Mano Negra", "unidad especial" (não "escuadrón"), "logra que lo condenen", "Inframundo" (não o calco "Bajo Mundo"), "queda libre, con la condición de ser deportado", "estadounidenses", "prestanombres", "intenta suicidarse", "fingen locura", "Riina decide matar a los jueces", "vía D'Amelio… Mueren él y cinco agentes".

## Falhas da esteira (o que quebrou, o improviso, a correção sugerida)
1. **Mapa com geografia inventada:** o "só a Sicília" saiu com uma 2ª Sicília no canto. Refeito com "alone in the center of a plain sea, no other land". Correção: no QA de mapa, conferir a geografia, não só o texto.
2. **Recorte de moldura agressivo** (I200, 48% da largura) cortou a cabeça do Riina. Correção: o `recorta_moldura.py` deveria recusar recortes < 60% e mandar regerar.
3. **Letreiro e manchete inventados** (pizzaria e jornal), mesmo com "without legible letters". Pedir "blank sign, no lettering anywhere" / "only a photograph, no headline".
4. **Duração acima do alvo** (14:32 contra o alvo de 13): 1.994 palavras para 130 anos de história. Próximo vídeo longo: cortar para ~1.850 palavras.
5. **Custo de Claude do orquestrador invisível** (mesma falha do 001–003): esta sessão não roda via `claude_run`.
6. Ferramentas da fábrica: **nenhuma alterada**. Copiei as do 003 para `videos/004-cosa-nostra/tools/`.

## Também feito
- **002 Mossad (id 8) e 003 FBI (id 9)** gravados em `youtube.videos` com `youtube_id` e título enviado. Pela API, os dois estão **privados e agendados**: o Mossad para 06/11 às 12:00 UTC ("La historia COMPLETA del Mossad en 14 minutos") e o FBI para 08/11 às 17:00 UTC. Ficaram como `pronto`, com nota "enviado/agendado". Backlog atualizado.
- Aprendizados na bíblia: `roteiro.md` (medidas, hook de ritual, revisão de lenda × documento), `titulo.md` (como medir o termo), `visual.md` (mapa, letreiros, recorte) e `voz.md` (nomes italianos).

## Pendências para o Rodrigo
- **Ouvir** (timestamps conferidos na `legendas.srt`):
  - 0:19 "Tommaso Buscetta" (sai "Buseta");
  - 3:52 "Masseria" e 3:55 "Castellammare";
  - 7:08 "Grand Hotel et des Palmes";
  - 9:13 "Inzerillo";
  - 11:13 "Badalamenti";
  - 11:45 "Ucciardone";
  - 12:59 "Schifani";
  - 14:11 "Messina Denaro".
- Publicar é decisão sua. O checklist está no `pacote.md`: es, sintético = sim, não é para crianças, 3 thumbs em "Probar y comparar", legenda es e tela final com a CIA ou o FBI.
