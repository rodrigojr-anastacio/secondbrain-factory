# Voz: historia-ptbr

Regra de canal: **prevalece** sobre `conhecimento/anti-padroes.md` (que guarda só o comportamento geral do Fish e das ferramentas). Configuração em `../canal.yaml` (`voz`).

## Voz do canal
- **Clone pt-BR feito pelo Rodrigo no Fish:** `48613fc675f84984981683d92266e543`, modelo `s2.1-pro`, velocidade **1.0** (aprovada; 0,95 soou lento). [canal.yaml]
- Tom: narrador contador de história, caloroso e curioso, que **conta** e não lê. Não é o narrador seco de documentário do `dossie-es`.

## Estado em 04/11/2026 (em revisão)
- Feedback do Rodrigo sobre o 002: "robótica e atropelada". A/B de 11 tomadas do hook do 003 (`videos/003-ira/amostras-voz/LEIA.md`, US$ 0,14): texto reescrito para a fala + `tts_fish.py --por-frase` (0,32 s entre frases) teve a menor repetição melódica (0,09 × 0,14 do jeito do 002); tags de direção e velocidade 0,97 pioraram. O 003 v1 saiu assim (`modo: por_frase`). [conhecimento/anti-padroes.md §2b]
- **Depois de ouvir, o Rodrigo achou a narração do 003 ainda ruim** ("parece que o cara tá lendo corrido, e não contando uma história") e **preferiu a amostra A (`A-atual`)**. Ele quer testar o modelo mais recente do Fish. [BRIEF-historia-003-v2.md, 04/11/2026] Teste em `videos/003-ira/v2-amostras/voz/` (job `historia-003-v2`). **Registre aqui o modelo/técnica aprovados.** Até lá, a decisão "G = por frase" é **Hipótese em xeque**.
- **Hipótese:** parte do "lendo corrido" vem do roteiro em fichas (sem conectores), não só do motor. Roteiro contínuo (`roteiro.md`) primeiro, parâmetro depois. Se ainda soar robótico, regravar a referência do clone (30–60 s naturais com pausas), não mexer em temperature/top_p (sem efeito no A/B).

## Pausas e tags (aprovado até o 002; valem para o encadeamento entre blocos)
- Encadeamento no `build.py`: ~0,35 s entre frases do mesmo assunto, **~0,9 s quando muda de ideia** (`IDEIA` no `roteiro.py` → `"ideia": true`) e **~1,5 s antes de capítulo**; cauda de 0,15 s (limiar −45 dB). Não aparar o silêncio natural do fim das frases de forma agressiva. [ETAPA3.md 001]
- Tags de tom (não são lidas pelo s2.1-pro): `[curious]`, `[serious]`, `[amazed]`, `[warm]`, `[slightly dramatic]`, no máximo 1 por frase, variando ao longo do vídeo. No Egito v2: 59 tags (12 curious, 16 serious, 8 amazed, 12 warm, 11 slightly dramatic). Com a voz por frase: tag só onde a emoção muda (~1 a cada 2–3 blocos). [ETAPA3.md 001; skill roteiro]
- `[break]`/`[long-break]`: no modo por frase, sem `[break]` (a tool já põe 0,32 s); `[long-break]` só antes de revelação. Sem o modo por frase: `[break]` só entre ideias, no máximo ~1 por minuto; excesso de pausas soou "lento e estranho". [estilo.md antigo]
- O Fish **corta a frase curta depois de `[break]` no fim do bloco** ("Guarde essa chuva" sumiu na Índia): feche o bloco com tag de tom em vez de `[break]` e confira com Whisper por bloco. [QA.md 002]

## Não faça
- Voz "Dio Historias"/espanhol neutro (é do `dossie-es`) ou Kokoro `ff_siwis` (é do `lotr-fr`).
- Tags de direção ("[serious, calm]", "[low voice]") e velocidade 0,97 (A/B do 003).
