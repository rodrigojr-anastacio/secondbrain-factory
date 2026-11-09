# RELATÓRIO · dossie-es/005 · "TODA la historia de la KGB en 14 minutos" (youtube.videos id 14)

Job: `~/workspace/referencias/BRIEF-dossie-005-kgb.md` (09/11/2026, ~10h50–12h50). Claude Code (Opus) fez pesquisa de concorrência, roteiro e storyboard; checagem de fatos + 2ª leitura nativa por subagente Sonnet com busca web. Voz, imagens, build e render: comandos determinísticos em primeiro plano. O job do historia-ptbr (Roma) rodou em paralelo: cada parte do render esperou a CPU livre (`tools/espera_render.sh`; até 7 min de espera) e não toquei nos caminhos dele. Nada publicado nem enviado ao Telegram; thumbs dos vídeos publicados intocadas.

## Entrega (`entrega/` + Drive `Youtube/Dossier en Minutos/005-kgb/`)
- `video.mp4`: **14:05**, 1080p30, −15,3 LUFS; `legendas.srt` (es);
- `thumb-A.jpg` (oficial de ushanka com o guarda-chuva diante da Lubianka, "EL PARAGUAS"), `thumb-B.jpg` (agente com o dossiê, "74 AÑOS DE MIEDO"), `thumb-C.jpg` (a estátua de Dzerzhinski içada, faixa "EL DÍA QUE CAYÓ"); aba "EXPEDIENTE Nº 005", sello "1917–1991";
- `pacote.md`: título A/B, descrição com links CIA/Mossad/FBI, 16 capítulos, fontes, tags, checklist e tradução pt-BR.
- QA aprovado (`QA.md`): 0 telas pretas, Whisper 97,2% de média, hook de 30,1 s.

## Título
A: "TODA la historia de la KGB en 14 minutos" · B: "La historia COMPLETA de la KGB en 14 minutos". Sigla única, sem disputa de termo.

## O roteiro
- **Hook (30 s):** Londres, 1978, ponte de Waterloo: a picada, o guarda-chuva, o táxi; Markov morto 4 dias depois com uma bolita < 2 mm. Pago no expediente 11 (logo após o CTA: "volvemos al puente de Waterloo") e no cierre "La Bolita".
- **14 expedientes:** La Comisión, El Edificio, La Cuota (ordem 00447), El Piolet (Trotski/Mercader; Mercader morre em Havana em 1978, "el mismo año del paraguas"), La Bomba, El Escudo, La Moneda (Abel; liga com o FBI), El Almuerzo (Feklisov × Scali, Cuba), La Embajada (Oswald no México), El Hospital (Andrópov, Sájarov), El Paraguas, La Bolsa (Gordievski; Ames liga com a CIA), La Estatua, El Archivista (Mitrokhin: Allende 1970 e Melita Norwood).
- **Diferença dos concorrentes** (legendas em `ref/`): Te lo Pinto (36 min, 196 mil) abre com 1917 e fecha com Putin; Atlas (20 min) abre com Putin em Dresden. Ninguém cita Cuba/Feklisov, Oswald no México, Mitrokhin, Allende, Abel ou a 00447. Sem Putin; FSB em 1 frase.
- **América Latina:** Coyoacán 1940, Havana 1978, Cuba 1962, Cidade do México 1963, Chile 1970 (+ mapa Moscú → Santiago).
- **Números:** 1.961 palavras, 87 blocos; estimado 13:53, medido 14:05 (+1,5%).

## Custo (financas.consumo, ref_id 14)
| Etapa | Itens | US$ |
|---|---|---|
| Voz (87 blocos, por frase) | Fish s2.1-pro, 11.544 bytes | 0,17 |
| Lote (197 cenas + 3 thumbs) | fal nano-banana, medido pelo uso do endpoint (o job de Roma usa outro endpoint) | 7,96 |
| 5 refeitas | fal | 0,20 |
| **Total direto** | | **8,33**, teto de US$ 10 |
- Fish: o crédito caiu US$ 0,27 durante a voz (esperado 0,17 no s2.1-pro; o job de Roma também usa Fish). Bem abaixo do preço do drama-3 cheio, compatível com s2.1-pro.
- Saldos depois: fal ~US$ 30,98 (inclui o gasto de Roma); Fish ~US$ 47,39.

## Correções de fatos (antes da voz; detalhes em `SOURCES.md`)
1. Ricina **inferida**, não detectada. 2. Kostov: "menos de dos semanas antes". 3. Execução atribuída ao serviço búlgaro "según los investigadores"; ajuda da KGB e aprovação de Andrópov atribuídas a Kalugin. 4. Gordievski: o sinal (esquina, sacola, agente com chocolate) e a corrida (dia da fuga) estavam misturados. 5. Mitrokhin: cortado "debajo de la comida" (fontes divergem). 6. "latas" → "bidones de leche". 7. Cheka: "más de doscientos mil con sus tropas". 8. Psiquiatria punitiva não era "arma nueva". 9. Emblema: tirada a origem na Cheká. 10. Häyhänen se entregou na embaixada dos EUA em Paris.

## Revisão do espanhol
Nota 9/10. Ajustes: "junto al puente de Waterloo", "según sus biógrafos", "según los propios disidentes… el único síntoma era disentir", "bajo la vigilancia del Partido", "el arma más recordada de aquellos años" (em vez de "su arma más temida", que acusava sem fonte). "Maletero" mantido (entendido em toda parte).

## Falhas da esteira (o que quebrou, o improviso, a correção sugerida)
1. **Pinos do mapa fora do lugar**: medi na grade da imagem, mas o plano "aberto" tem Ken Burns e o frame não bate com a grade. Custou 3 rerenders da parte 5 (~3 min cada + espera). Correção: no `build.py`/QA, gerar um still do frame do mapa antes do render completo.
2. **`checa_imagens.py` com 4 falsos positivos** em cenas noturnas (recorte de 6–31% da largura teria destruído a imagem). Correção: recusar recorte < 60% e mandar olhar/regerar (mesma sugestão do 004).
3. **Texto inventado** em logo de avião, capa de pasta e luz "ON AIR": pedir "no logo/no lettering anywhere" desde o storyboard em qualquer objeto com marca.
4. **1 comando de render foi para segundo plano** (o laço de espera + render passou de 10 min por causa do render de Roma); esperei o término em primeiro plano antes de seguir. Correção: esperar a CPU num comando e renderizar em outro (feito depois).
5. **Custo de Claude do orquestrador invisível** (igual ao 001–004): esta sessão não roda via `claude_run`.
6. Ferramentas da fábrica: nenhuma alterada. Copiei as do 004 para `videos/005-kgb/tools/`.

## Também feito
- `youtube.videos` id 14: `pronto`, 845 s, título A. `backlog.md`: KGB = 005 pronto.
- Aprendizados na bíblia: `roteiro.md` (medidas, hook atribuído, teste do trecho 6–8 min, revisão de detalhe de livro de divulgação), `visual.md` (falsos positivos, logos, mapa × Ken Burns) e `voz.md` (nomes russos).

## Pendências para o Rodrigo
- **Ouvir** (timestamps conferidos na `legendas.srt`): 0:15 "Georgi Markov" · 0:51 "Félix Dzerzhinski" · 2:17 "Nikolái Yezhov" · 3:22 "David Alfaro Siqueiros" · 3:48 "Ramón Mercader" · 6:43 "Alexandr Feklisov" · 7:47 "Oleg Nechiporenko" · 9:41 "Zhivkov" · 10:33 "Oleg Gordievski" · 11:34 "Vladímir Kriuchkov" · 12:23 "Vasili Mitrojin".
- Publicar é decisão sua (checklist no `pacote.md`). Medir vs. Mossad: impressões no dia 7, sugeridos de Te lo Pinto/Atlas, CTR, % visualizado e a curva em 6:00–8:00.
