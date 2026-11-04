# Amostras de voz es (2026-11-04)

Texto: `hook-es.txt` (hook do piloto da CIA, 397 bytes). Gerado por `amostras.py` (Fish s2.1-pro, velocidade 1.0, uma chamada por voz) e avaliado por `avaliar.py` (faster-whisper small + ebur128). Custo: **US$ 0,042** (`financas.consumo`, `ref_id` = 7). Os mp3 ficam fora do git, nesta pasta.
A lista de vozes públicas do Fish em es/fr está em `pesquisa/archive-in-minutes/idioma/voz/` (`fish_vozes.py`).

| Arquivo | ID Fish | Descrição (Fish) | Usos | Duração | pal./min | Whisper × texto | LUFS | Leitura |
|---|---|---|---|---|---|---|---|---|
| **dio-historias.mp3** | `ac594943984a47e7a827416eb263c7b1` | masculina madura, **acento neutro**, documental, calma | 96 mil | 27,3 s | 138 | 0,952 | −19,7 | **Sugerida**: neutra para MX/ES/US, tom de documentário, uso moderado |
| arnold.mp3 | `4a6a697943254f63ab3143877712ceed` | masculina, neutra, séria, "announcer" | 83 mil | 27,3 s | 139 | 0,952 | −19,4 | 2ª opção: mais autoritária |
| marcus.mp3 | `93dc4e3a1a494d58ad0f50f712b8b152` | masculina grave, documental, calma | 59 mil | 26,5 s | 143 | 0,929 | −20,3 | 3ª opção: mais grave |
| narrador-documental-latino.mp3 | `c87656721dda48a7906f990f036ce76f` | "narrador latino de National Geographic" | 43 mil | 30,6 s | 124 | 0,952 | −22,7 | Evitar: imita um dublador real (risco de imitação), e é lenta |
| locutor-k.mp3 | `3f45a7fd7a614655a61eb7027b955783` | grave e autoritária | **825 mil** | 26,4 s | 143 | 0,929 | −19,4 | Evitar: é a voz de TikTok mais usada, soa "canal em massa" |
| natgeo-espana.mp3 | `85398a2a5ec24078aae24829fb03425d` | narrador de Espanha | 22 mil | 24,8 s | 153 | 0,929 | −19,6 | Evitar como padrão: sotaque da Espanha (só 22% da demanda) |
| voz-grave.mp3 | `3a42f62c3af240438066d7e927414dea` | grave, calma | 11 mil | 20,3 s | 186 | 0,945 | **−32,9** | Reprovada: rápida e baixa |

Nenhuma voz falou as tags `[serious]`/`[slightly dramatic]`. As diferenças de Whisper (0,93–0,95) vêm dos números ("27"/"veintisiete"), não de palavras perdidas.
**Decisão do Rodrigo:** ouvir as 3 primeiras e escolher. A sugerida já está no `canal.yaml`. Também dá para clonar uma voz própria no Fish com áudio licenciado, como no `historia-ptbr`.
