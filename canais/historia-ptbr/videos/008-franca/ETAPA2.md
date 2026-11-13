# ETAPA 2 · historia-ptbr/008 França (youtube.videos id 33) · 13/11/2026

**Resultado:** `entrega/video.mp4` 15:16 (916 s), 1080p30, −15,1 LUFS, pico −4,3 dBFS, 0 telas pretas, 0 silêncios > 1,5 s, 23 cortes no 1º minuto. Checklist v2: **13/14** (só o ritmo reprova: 131 ppm × 140–145, Hipótese conhecida do drama-3).

## Custo (financas.consumo, ref_id 33)
fal US$ 8,68 (183 imagens do vídeo + 6 bases de thumb, US$ 0,046 cada) · Fish drama-3 US$ 0,73 (vídeo inteiro 11.389 bytes + 3 tomadas extras do hook) · Runpod US$ 0,11 (RTX 3090/A4000) · pré-QA Anthropic US$ 0,28. **fal+Fish = US$ 9,41 (teto 14).** Uma tentativa da parte 3 do render foi morta pelo limite de 10 min do harness em background (Pod destruído pelo trap; ~US$ 0,02 sem registro).

## Voz
- Fish drama-3, 1 chamada por bloco, 54 blocos. Whisper: mín 82,3% / média 97,4% bruto; **fonético mín 92,5% (N042), média 99,1%**. Só "Soissons" (Whisper ouve "Sua som") e "Reims" ("Hans") saem fora na transcrição; a grafia de voz do `FALA` ficou como estava (nenhuma troca). Pedir ao Rodrigo para ouvir os nomes (abaixo).
- **Crédito Fish:** a leitura do saldo caiu bem menos que bytes × US$ 50/M (queda aparente ~US$ 0,15 para ~US$ 0,8 faturados no banco): o painel atualiza com atraso ou a cobrança real ainda está no preço promocional. O banco registra o preço de tabela (US$ 50/M); conferir no painel do Fish.
- Hook: 3 tomadas extras de N001–N006; melhor combinação `ddcdca` (repetição melódica 0,10; tomadas únicas 0,16–0,30).

## Imagens
Lote-prova de 6 (I001, I029, I058, I076, I131, I142) aprovado na prancha (Bastilha sem tricolor, mapa sem letras), depois as 177 restantes em 4 partes. Prancha 183/183: bonequinhos mantidos, 0 faltando, 0 refeitas. Mapas sem letras (rótulos no `src/labels.jsx`). I168 (paisagem de guerra) sem personagens: aceito.

## Pré-QA
154 stills (a cada 10 s + mapas + cartões + capítulos), 120 analisados pelo `preqa_visual.py`: **0 bloqueantes**, 7 altos, 21 médios. Tratados: rótulos de mapa reposicionados (GÁLIA, DOMÍNIO DO REI, REI INGLÊS, FRANÇA 1420, ALEMANHA/ALSÁCIA-LORENA; stills conferidos de novo). Falsos positivos anotados: barretes e tricolor da I023 no hook (flash-forward intencional), tricolor em 1791 (já existia), coroa/arquitetura "medievais" no batismo e em Luís XIV (estilo do canal), placa de capítulo cobrindo a base da cena (layout padrão do canal, 3 s).

## Render
Runpod em 3 partes (0–9159, 9160–18319, 18320–27479; ~11 min cada; provas SSIM ≥ 0,999) + concat com `mix.wav` AAC 192k. Trilha: Ré dórico, alaúde sintetizado até o cap. 5 e cravo + sino a partir do cap. 6.

## Pendências
Título A diz "15 minutos" (duração real 15:16; o `SCRIPT.md` ainda diz 16, é só da etapa 1). Ouvir os nomes antes de publicar.
