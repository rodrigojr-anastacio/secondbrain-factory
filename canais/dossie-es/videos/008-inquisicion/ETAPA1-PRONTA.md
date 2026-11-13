# ETAPA 1 PRONTA · dossie-es 008 · La Inquisición (13/11/2026, Opus)

`youtube.videos` id **35** (status `roteiro`). Publica seg 16/11. Teto **US$ 10** (fal + Fish + Runpod). Nada gasto na etapa 1.

## O que está pronto
| Arquivo | Conteúdo |
|---|---|
| `roteiro.py` | fonte única (roteiro + planos); gera os arquivos abaixo. Geração copiada do 007-ss |
| `SCRIPT.md`, `blocos.json` | 2.030 palavras, 96 blocos, hook + 14 expedientes + cierre; ~14:23 estimados (863 s) (WPS 2,38; o real costuma sair 1–3% acima: ~14:40) |
| `STORYBOARD.md`, `storyboard.json` | 300 planos, média 2,9 s, 24 cortes no 1º minuto, 0 reuso antes de 3:00, 49% de reuso depois; 0 avisos |
| `cenas.json` | **183 imagens do vídeo + 3 bases de thumb = 186** (todas com SANGRIA) |
| `FATOS-revisao.md`, `ES-revisao.md` | checagem de fatos (Sonnet + web) e revisão nativa/sensibilidade (8,3/10); **já aplicadas** (números de bloco = versão anterior) |
| `SOURCES.md` | correções aplicadas, por que o hook mudou, fontes para a descrição |
| `TITULOS-THUMBS.md` | 3 títulos × 3 thumbs (A fórmula, B por dentro, C lado oculto en América) |
| `BRIEF.md` | resumo do vídeo |

Checklist da bíblia: hook 32,9 s est. (Maldonado, Lima 1639; desfecho seco "Lo había denunciado su propia hermana") ✔ · 14 expedientes com título falado, cada fim puxa o próximo ✔ · anedota paga no exp. 12 (~9:45) e no cierre "Los Libros" ✔ · acusações atribuídas, lenda × fato separados ✔ · ângulo América Latina (Tucumán/Chile/Lima, Texcoco 1539, Lima/México/Cartagena, 1649, Hidalgo, Lima 1813) ✔ · revisão nativa ✔ · CTA de inscrição no meio (~7:40, fim do exp. 9) ✔ · sem gancho de próximo vídeo ✔ (o CTA final cita os **Masones, já publicados** em 10/11, permitido pela regra de 13/11).

## O que a etapa 2 precisa saber
1. **Não reescreva o roteiro.** Rode `python3 roteiro.py` só se precisar regenerar; edite lá, nunca nos JSON.
2. **Voz (Fish "Dio Historias", s2.1-pro, por frase como no 007):** glossário de pronúncia na seção "Pronúncia para o Fish" do `ES-revisao.md` (aplicar só no texto mandado ao Fish, nunca no SCRIPT/legendas): Ometochtzin "Ometóch-tsin", Texcoco "Tescóco", Zugarramurdi "Sugarra-múrdi", Llorente "Yorénte", Ripoll "Ripóy", Henningsen "Hénnin-sen", Giordano "Yordáno", Gui "Gui" (/gi/), Toulouse "Tulús", García Cárcel ok. **Teste as aspas «»** (N003 não tem mais; ficam em "relajar", "hereje dogmatizante", "Decíamos ayer", "Y sin embargo, se mueve"): se o Fish tropeçar, tire as aspas só do texto da voz. Confira no Whisper que "TODA" não sai gritado.
3. **Hook:** estimado em 32,9 s; se a voz passar de 35 s, a bíblia manda cortar no texto antes (sugestão: tirar "Él mira al cielo:" mantendo o resto).
4. **Imagens (nano-banana, 186):** custo do 007 com 188 foi US$ 9,47 no total → o teto está **justo**: gere uma vez, refaça só o que reprovar. Moldura/letterbox em ~27%: `checa_imagens.py` + `recorta_moldura.py` + `recorta_branco.py` (copiar de `../007-ss/tools/`). Riscos deste tema:
   - **fogueiras**: todas pedem "only a column of smoke… no people visible in the fire" (`FOGO`); reprove qualquer figura nas chamas;
   - **capuz pontudo/capirote** (lembra KKK): `NOHOOD` nas procissões e efígies; confira de perto;
   - **sambenito** liso amarelo com aspa vermelha (`SAMB`); se vier com texto/demônios, refaça;
   - **texto inventado** em pergaminho, edito, livro, lista, decreto, jornal (todos com `SEM`); "green cross" pode virar logotipo: confira;
   - pessoas reais "resembling" (Torquemada, Isabel/Fernando, Sixto IV, Galileo, Felipe II, Fernando VII, Hidalgo, Paulo III não está mais): conferir com visão;
   - `museum_iron` (museu do séc. XIX) não pode mostrar donzela de ferro com corpo; `dungeon_empty` sem instrumentos de tortura.
5. **Mapas (pinos/setas no código, `src/labels.jsx`, rótulos `fijo` se o modelo escrever algo):**
   - `map_europa` (exp. 1): TOULOUSE, ROMA (e opcional SEVILLA);
   - `map_exilio` (exp. 6): setas de ESPAÑA para PORTUGAL, NORTE DE ÁFRICA, ITALIA, IMPERIO OTOMANO;
   - `map_atlantico` (exp. 6 e 8): seta ESPAÑA → ANTILLAS / MÉXICO;
   - `map_sudamerica` (exp. 9 e 14): pinos LIMA, CARTAGENA, QUITO, CHILE, RÍO DE LA PLATA; na reutilização do exp. 14, pinos LIMA, CARTAGENA e (fora do mapa) MÉXICO como rótulo.
   Confira os pinos num still do render (lição do 005/006).
6. **Cartões de data:** LIMA 1639, TOULOUSE 1323, ROMA 1478, SEVILLA 1481, GRANADA 1492, MÉXICO 1539, VALLADOLID 1559, LIMA 1570, LOGROÑO 1610, ROMA 1633, CHILE 1627, MÉXICO 1649, VALENCIA 1826, LIMA 1813, PARÍS 1817, LIMA HOY. 12 rótulos de nome (≤ 30 caracteres; "FRANCISCO MALDONADO DA SILVA" tem 28).
7. **Créditos/fontes só na descrição** (lista em `SOURCES.md`); nada de linha de acervo na tela. Nota de voz sintética + IA na descrição.
8. **Títulos × thumbs:** `TITULOS-THUMBS.md`. Ajuste o N ("en 14 minutos") à duração real. Aba "EXPEDIENTE Nº 008".
9. Capítulos estimados (reescalar pela voz real): 0:00 Hook · 0:33 Exp.1 · 1:16 · 1:59 · 2:51 · 3:45 · 4:29 · 5:08 · 6:01 · 6:48 · 7:43 (Brujas) · 8:46 · 9:45 (Complicidad) · 11:12 · 12:22 · 13:38 Cierre.
10. Entrega em `entrega/` (sem Drive), status até `pronto`, backlog do canal e aprendizados na bíblia (o 008 é o 1º tema religioso: registrar o que o revisor pegou).
