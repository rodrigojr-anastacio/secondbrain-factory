# QA · historia-ptbr/003 Irã (youtube.videos id 5) · 04/11/2026

**Veredito: aprovado, com pendências não bloqueantes (abaixo).** Nenhuma rodada de correção foi necessária no render (1 correção de código antes dele: rótulo × placa de capítulo).

| Critério | Meta | Medido | OK |
|---|---|---|---|
| Duração | 14–16 min; = N do título | **918,4 s = 15:18** → título "em 15 minutos" | ✅ |
| Formato | 1080p30 H.264/AAC | 1920x1080, 30 fps, h264 + aac 48 kHz, 262 MB | ✅ |
| Loudness | ~-15 LUFS, pico < -1 dBTP | **-15,1 LUFS**, LRA 3,4 LU, pico de amostra -4,4 dBFS | ✅ |
| Telas pretas ≥ 0,2 s | 0 | **0** | ✅ |
| Silêncios > 1,5 s | 0 | **0** | ✅ |
| Cortes no 1º minuto | ≥ 18–21 | timeline: **24**; o detector de cena do ffmpeg (`scene>0.3`) conta só 15 (não vê reenquadramentos da mesma imagem) | ✅ (ver nota) |
| Cortes/min | — | média **20,2** (309 planos, 2,97 s em média, mín 1,9 s) | ✅ |
| Rótulos | ~1 a cada 2 planos | **143** rótulos (46%), 33 cartões de data | ✅ |
| Whisper × roteiro (vídeo inteiro) | ≥ 93% | **95,4%** (1.991 palavras no roteiro, 1.982 na voz), **0 tags faladas** | ✅ |
| Whisper por bloco (etapa 2) | ≥ 93% | mín 75% / média 95,1% (nomes persas; ver ETAPA2) | ✅ (aceito) |
| Capítulos | crescentes desde 0:00, último < duração | 18 capítulos, 0:00 … 14:27, validado por script | ✅ |
| `.srt` | sincronizada | início 0:00,25 "Tus, ano mil e vinte…"; 5:11 "Roma e Pérsia viram os dois olhos do mundo" (cap. A Rocha 5:04); 10:21 "William D'Arcy" (cap. O Poço 10:20); fim 15:14 "Conta aqui nos comentários" | ✅ |
| Thumb | JPG 1280x720 < 2 MB | A 154 KB, B 138 KB, C 125 KB; legíveis em 320x180 | ✅ |
| Custo | ≤ R$ 80 | **R$ 69,77** (fal US$ 11,54 = R$ 67,55 + Fish US$ 0,38 = R$ 2,22); nada gasto nesta etapa | ✅ |

## Conferência visual
- `qa/grade-capitulos.jpg`: 1 frame de cada um dos 17 capítulos + hook; a placa "CAPÍTULO N" lê bem e o cartão de data fica no canto oposto. Nada cortado ou sobreposto.
- `qa/grade-nomeadas.jpg`: Ciro, Persépolis, Shapur, Valeriano, Ferdowsi (livro aberto), Isfahan, Khomeini: lugares e figurinos plausíveis, rótulos certos, sem bandeira, sem texto inventado nas cenas vistas. `out/contact-sheet.jpg` (20 frames) sem frames pretos nem texto falso.
- Mapas (Pars, Estrada Real) com rótulos do `labels.jsx` bem posicionados.

## Problema achado e corrigido
- **Rótulo × placa de capítulo:** no frame 1075 o rótulo "PLANALTO IRANIANO" encostava na placa "CAPÍTULO 1". Corrigido em `src/Video.jsx`: o rótulo espera a placa sair (c.from+104). Conferido em still antes do render.
- `tools/build.py` quebrava na trilha (`ValueError`, passo do dedilhado passava do fim); corrigido com um `break`.

## Pendências (não bloqueiam)
1. **Estilo flux/dev × gpt-image-2:** alguns personagens têm rostos mais "realistas" que os bonequinhos de cabeça redonda do 001/002 (Khomeini, Ciro, juízes, 2009). Mistura de estilos dentro do mesmo vídeo; aceitável, mas o Rodrigo deve olhar.
2. **Thumbs em flux/dev, não em `high`** (OpenAI sem crédito). Se recarregar, regerar `thumb-base` em `high`. A thumb A usa cavalos alados que parecem burros com asas; B (guia espantado) e C (Ciro) são mais legíveis. Recomendo testar as 3.
3. **I106** (livro) tinha uma assinatura minúscula no canto inferior direito (etapa 2); não apareceu nos frames vistos, mas só ~40 das 189 imagens foram abertas em todo o pipeline.
4. **Voz:** "robótica" é julgamento do ouvido do Rodrigo (hipótese da etapa 2); não medi nada novo. N075 diz "mil novecentos e cinquenta e três" onde o texto tem "cinquenta e três" (inofensivo).
5. **Reconfirmar na véspera** a frase "até a gravação deste vídeo, não há acordo de paz" (N096).
6. Desfecho da anedota do hook em ~11,7 s (meta 10 s).
