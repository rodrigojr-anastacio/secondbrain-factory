# RELATÓRIO · dossie-es/006 · "TODA la historia de los Masones en 14 minutos" (youtube.videos id 15)

Job: `~/workspace/referencias/BRIEF-dossie-006-masones.md` (09/11/2026, ~13h10–14h30). Claude Code (Opus) fez referência, roteiro e storyboard; checagem de fatos e 2ª leitura nativa em 2 subagentes Sonnet com busca web, em paralelo. Voz, imagens, build e render: comandos determinísticos em primeiro plano. O job do historia-ptbr (Rússia) rodou em paralelo: cada parte do render esperou a CPU livre (`tools/espera_render.sh`, 0 s de espera) e não toquei nos caminhos dele. Nada publicado nem enviado ao Telegram; thumbs dos vídeos publicados intocadas.

## Entrega (`entrega/` + Drive `Youtube/Dossier en Minutos/006-masones/`)
- `video.mp4`: **14:10**, 1080p30, −15,2 LUFS; `legendas.srt` (es);
- `thumb-A.jpg` (maçom do séc. XVIII com esquadro e compasso na loja, "EL SECRETO"), `thumb-B.jpg` (William Morgan com o manuscrito e a carruagem, "IBA A CONTARLO TODO"), `thumb-C.jpg` (esquadro e compasso sobre o livro à luz de vela, faixa "300 AÑOS DE SECRETO"); aba "EXPEDIENTE Nº 006", sello "1717–HOY";
- `pacote.md`: título A/B, descrição com links Cosa Nostra/CIA/KGB/FBI, 16 capítulos, fontes, tags, checklist e tradução pt-BR.
- QA aprovado (`QA.md`): 0 telas pretas, Whisper 97,2%, hook de 31,2 s.

## Título
A: "TODA la historia de los Masones en 14 minutos" · B: "La historia COMPLETA de los Masones en 14 minutos". "Masones" > "Masonería" (pesquisa de 09/11).

## O roteiro
- **Hook (31 s):** Batavia, 1826: Morgan anuncia o livro dos rituais, é preso em Canandaigua por dívida < US$ 3, alguém paga, é posto numa carruagem; "Nadie volvió a ver a William Morgan". Pago no expediente 8 ("El Libro", logo após o CTA) e no cierre "El Secreto".
- **14 expedientes:** La Logia (canteiros, Schaw 1598), El Diario (Ashmole 1646), La Taberna (1717, Anderson 1723), La Bula (1738, Fernando VI), La Biblia (Washington 1789, Franklin e Voltaire), El Abate (Barruel e os Iluminados: o mito nasce), La Fragata (George Canning 1812, Logia Lautaro), El Libro (Morgan, Partido Antimasónico, 1ª convenção nacional), El Decreto (Noite Setembrina, Bolívar proíbe as sociedades secretas; escoceses × yorkinos), La Confesión (Taxil 1897), El Seudónimo (Franco, 80 mil fichas, Jakim Boor), La Lista (P2, Massera e López Rega), El Puente (Calvi, Calò absolvido: liga com a Cosa Nostra), La Declaración (Vaticano 2023, números de hoje, inglesa × francesa).
- **Fato × mito:** Barruel/Iluminados, Taxil e as fichas de Franco ditos como o que são; acusações atribuídas; sem "dominam o mundo".
- **Diferença dos concorrentes** (`ref/OyQMNlGbwEI.txt`, Academia Play 790 mil): eles abrem em 1717 e gastam o meio em símbolos e graus; nós abrimos com Morgan e damos expediente próprio a Lautaro, Bolívar, Taxil, Jakim Boor, P2 e Calvi.
- **Números:** 1.977 palavras, 88 blocos; estimado 13:59, medido 14:10 (+1,3%).

## Custo (financas.consumo, ref_id 15)
| Etapa | Itens | US$ |
|---|---|---|
| Voz (88 blocos, por frase) | Fish s2.1-pro, 11.861 bytes | 0,18 |
| 3 thumbs + 3 lotes (198 cenas) | fal nano-banana, medido pelo uso do endpoint (a Rússia usa outro endpoint) | 7,92 |
| 7 refeitas/falhas | fal | 0,32 |
| **Total direto** | | **8,42** (teto US$ 10) |
- **Fish, modelo cobrado:** a API não expõe histórico de uso (7 endpoints testados, 404/401). Conciliação: o crédito caiu 0,333 durante a voz = 0,178 (nosso, s2.1-pro) + ~0,152 (drama-3 da Rússia, linhas de `financas.consumo` no mesmo intervalo). Se tivesse caído em drama-3, seriam ~0,27. Compatível com s2.1-pro.
- **Saldos depois (banco):** fal **US$ 7,21** (inclui a Rússia) · Fish US$ 47,02. **O fal não cobre mais um vídeo inteiro (~US$ 8): recarga necessária antes do próximo.**

## Correções de fatos (antes da voz; detalhes em `SOURCES.md`)
18 correções. As principais: Mason Word não está nos estatutos de Schaw; Ashmole feito maçom junto com o coronel Mainwaring (não "na casa dele"); Ashmolean "primeiro museu universitário"; Anderson pede lei moral e não ser ateu (não "crer em Deus"); Illuminati proibidos em 1784–85; o duque de Orleans renunciara à maçonaria antes da guilhotina; Bolívar iniciado "según la tradición"; decreto na Gran Colombia; Taxil sem "escolta policial"; tribunal de Franco até 1964 e cifra 80 mil fichas × 5 mil maçons; colunas Jakín e Boaz; P2: cofre e mala, já desautorizada pelo Gran Oriente, Berlusconi "negó haber participado"; Calvi: correio, ~US$ 14 mil em 3 moedas, banco quebrou semanas depois, absolvição por falta de provas; EUA < 900 mil; GODF sem Deus e com mulheres desde 2010.

## Revisão do espanhol
Nota 8,5/10. Ajustes: "yorkinos" (grafia mexicana), "el primero de marzo", "cabaña" no lugar de "caseta", "Padres Fundadores", "farsante" no lugar de "bromista", sujeitos explícitos (Bolívar, el partido), e as 6 frases que soavam a conspiração reescritas.

## Falhas da esteira (o que quebrou, o improviso, a correção sugerida)
1. **Os 2 subagentes foram para segundo plano** (faltou `run_in_background: false` na chamada); esperei em primeiro plano até os transcritos pararem de crescer. Correção: sempre passar `run_in_background: false`.
2. **Teto vs. número de imagens:** o 1º storyboard tinha 228 imagens (~US$ 9,2); cortei para 198 tirando 1 imagem dos blocos depois de 3:00 (o reuso automático cobre). Sugestão: o `roteiro.py` avisar quando `imagens_total × 0,04` passar de 80% do teto.
3. **`checa_imagens.py`:** 7 falsos positivos (cenas escuras, vinheta circular); como no 005, olhei a folha de contato antes de recortar.
4. **Custo de Claude do orquestrador invisível** (igual ao 001–005): esta sessão não roda via `claude_run`.
5. Ferramentas da fábrica: nenhuma alterada. Copiei as do 005 para `videos/006-masones/tools/`.

## Também feito
- `youtube.videos` id 15: `pronto`, 850 s, título A. `backlog.md`: Masones = 006 pronto; Templarios passa a 007.
- Aprendizados na bíblia: `roteiro.md` (medidas, hook de desaparecimento, tema de sociedade secreta, padrão das correções), `visual.md` (envelope/calendário com texto em inglês, objeto isolado vira vinheta) e `voz.md` (nomes, conciliação do modelo cobrado no Fish).

## Pendências para o Rodrigo
- **Ouvir** (timestamps conferidos na `legendas.srt`): 0:10 "Canandaigua" · 1:05 "William Schaw" · 1:35 "Henry Mainwaring" · 2:32 "Anthony Sayer" · 3:14 "In eminenti" · 4:43 "Augustin Barruel" · 8:03 "Manuela Sáenz" · 8:25 "yorkinos / Joel Poinsett" · 9:21 "Diana Vaughan" · 10:17 "Jakim Boor" · 10:45 "Castiglion Fibocchi / Licio Gelli" · 12:32 "Pippo Calò".
- **Recarga do fal** (saldo ~US$ 7).
- Publicar é decisão sua (checklist no `pacote.md`). Medir vs. Mossad e CIA: impressões no dia 7 (testa se busca alta sem molde aquecido traz impressões), CTR, % visualizado.
