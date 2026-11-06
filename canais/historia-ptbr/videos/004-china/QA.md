# QA · 004 China (05/11/2026) · APROVADO

Render `out/video.mp4` = `entrega/video.mp4` (`qa/qa.txt`, `out/contact-sheet.jpg`):
- 974,2 s (**16:14**), 1920×1080, 30 fps, H.264 + AAC 48 kHz estéreo, 480 MB.
- −15,3 LUFS integrado, LRA 4,1, pico −4,3 dBFS.
- 0 telas pretas (≥ 0,2 s); 0 silêncios > 1,5 s.
- 338 planos, média de 2,88 s, 20,8 cortes/min; 1º minuto: 27 planos pela timeline (o `qa.sh` conta 20 por cena).
- 38 cartões de data, 37 rótulos, 10 placas de capítulo. Rótulos de 8 mapas conferidos em stills (`qa/stills-mapas*.jpg`; 3 reposicionados: Yangtzé estava sob a placa do capítulo 1, Taiwan cortado, Roma na borda).
- **Hook: 1:16** até o capítulo 1 (meta ≤ 90 s; o Irã tinha 1:31).

Voz × roteiro (Whisper small por bloco, `qa/voz_blocos.json` + `qa/voz_blocos_fonetico.json`):
- 99 blocos, 0 tags faladas.
- Bruto: média 96,0% (os blocos abaixo de 93% são nomes chineses: o Whisper escreve "Qin", "Zhu Yuanzhang", "Xiaoping", o que mostra que a grafia fonética mandada ao Fish soa como o nome certo).
- Com chave fonética (melhor de grafia de voz × grafia de tela): mínimo 93,9%, média 99,4%. Os 2 abaixo de 95% são formatação do Whisper ("XVII" por "dezessete", "30%" por "trinta por cento"). N023 foi regerado ("os Djou enfraqueceram" saía "os duem fraqueceram").
- 60 s iniciais: repetição melódica **0,11** (meta ≤ 0,12), queda −2,0 st, faixa 10,7 st, F0 102 Hz.

Imagens (`qa/prancha-1..6.jpg`, `qa/refeitas.jpg`, `qa/mapas-grade.jpg`):
- 215 únicas, 0 faltando, 0 pretas, 0 molduras; bonequinhos de cabeça redonda em todas as cenas com gente.
- Refeitas (8): I143 e I171 (letras inventadas), I148 (coroa europeia), I174 (bandeira tricolor errada em 1911), I208 (salão gótico), I210 (astronautas e depois a Terra no céu do lado oculto da Lua; a Chang'e 6 é robótica), I215 (túmulo com cara de Egito).
- Resíduos menores: letreiro "XMNX" ao fundo em I179 (invasão de 1937), "Zagros" miúdo no mapa da Rota da Seda (I105), "安全第一" (texto chinês real, "segurança em primeiro lugar") na fábrica de carros (I209); o rótulo "ZHONGGUO = PAÍS DO MEIO" fica sobre a cena do ferro-velho (fato verdadeiro do vaso, cortado da fala por tempo).

Bíblia do canal:
- Narrativa contínua, hook + 10 eras + fecho, títulos-frase só na placa, pontes "mas… então…".
- Fio condutor (Mandato do Céu) dito em voz alta em 9 das 10 eras e no fecho; loops pagos: túmulo (hook → era 3 → fecho), dez mil gerações (hook → fecho), escrita (era 1 → 3 → 5 → fecho), papel-moeda (era 6 → era 6), Puyi (era 8 → era 9).
- Sem capítulo-objeto, sem legenda queimada, sem nada do `dossie-es`.
- Duração 16:14 (alvo 15–17) e hook 1:16 (teto 90 s): **dentro da meta**.
