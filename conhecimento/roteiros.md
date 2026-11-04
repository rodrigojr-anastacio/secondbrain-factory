# Roteiros: estruturas, loops, mini-hooks e ritmo

**Como atualizar:** alimentado por **Tendências** (estrutura e capítulos de referências, via `watch.py`), **Métricas** (retenção por capítulo, quedas na curva) e **feedback do Rodrigo**. Cada entrada leva **data e fonte**. Sem dado, marque **Hipótese**. Depois de editar, faça commit descritivo.

Última revisão: 2026-11-04 (capítulos-objeto, fecho circular e escrita para a fala, vídeo 003).

---

## Regras rápidas

**Estrutura nova do historia-ptbr (a partir do 003, 04/11/2026; fonte: transcrições em `canais/historia-ptbr/videos/003-ira/ref/` e pedido do Rodrigo)**
- **Capítulos = cenas/objetos concretos, título de 1–2 palavras, falado na narração** ("O Cilindro.", "O Moinho.", "O Tabaco."), ~1 por minuto (Archive: 13 capítulos em 12 min). Nunca "Período X".
- **O fim de cada capítulo puxa o próximo**; o melhor é terminar com a frase que **é** o título do próximo ("…entregue a um homem que já criou galinhas. O criador de galinhas."). Re-hook a cada ~60–90 s.
- **Narração no presente**, frases curtas, números exatos, nomes e lugares (que viram rótulo na tela).
- **CTA de inscrição no meio, colado num re-hook** (Archive, Gestapo 3:45), não no fim.
- **Fecho volta à imagem do começo** + aforismo de 2 frases ("A Gestapo nunca foi grande. Grandes eram as pessoas que escreviam para ela.") + pergunta/gancho.
- **Escreva para a fala** (A/B de 04/11, `003-ira/amostras-voz/LEIA.md`): frases de 4–14 palavras, vírgula onde se respira, "…" só na virada, sem `[break]` (a voz por frase já põe 0,32 s), tag de tom só onde a emoção muda. O texto reescrito para a fala reduziu a "musiquinha repetida" entre frases (repetição melódica 0,14 → 0,10) mais que qualquer parâmetro do Fish.
- **Texto na tela:** rótulo (`@@NOME` no `roteiro.py`) em ~1 de cada 2 planos com nome, lugar ou data; 18–20 cortes/min nos 2 primeiros minutos (Archive 20, HiM Irã 17).
- **Tamanho com a voz por frase:** ~144 ppm com as pausas; 15 min ≈ 2.100 palavras. **Hipótese** até medir o 003.

**Faça**
- **Estrutura historia-ptbr até o 002 (substituída no 003, acima):** hook (~45 s) + 8–9 capítulos cronológicos, das origens até 2026, e fecho com ligação ao presente e pergunta para os comentários. [ETAPA1.md 001; ETAPA-FINAL.md 002]
- **Cada capítulo abre com um mini-hook** (contraste ou curiosidade) e fecha puxando o próximo. [BRIEF.md 001]
- **Loops "guarde isso"** pagos depois: "Guarde esse ano: 1922" (Egito, pago no cap. 7); algodão, Harappa, leões de Ashoka, diamante, chuva de Plassey e Hume (Índia). [ETAPA1.md 001; BRIEF.md 002]
- **Fio condutor** que costura o vídeo: o Nilo (Egito), o vento da monção (Índia), a "couronne" que passa de cidade em cidade (lotr-fr). [BRIEF.md 002; BRIEF.md lotr-fr 001]
- **Tamanho:** para ~17 min no historia-ptbr, mire **~2.250–2.300 palavras**. Com as pausas da v2, a fala fica em ~135 palavras/min. [estilo.md historia-ptbr, aprendizados do 002]
- **Remodelar a transcrição da referência** (mesma ordem, beats e números, texto reescrito em pt-BR) funcionou na Índia. Troque as autorreferências do concorrente por um equivalente brasileiro do mesmo fato (ex.: a fome de 1876 na Índia ↔ a Grande Seca de 1877 no Ceará). [estilo.md historia-ptbr]
- `roteiro.py` é a **fonte única**: gera `SCRIPT.md`, `blocos.json`, `cenas.json`, `STORYBOARD.md` e `storyboard.json` e valida as regras de reuso. Edite lá, nunca nos gerados. [ETAPA1.md 001]
- Marque no `roteiro.py` os blocos que **abrem ideia nova** (`IDEIA` → `"ideia": true`) para o `build.py` dar a pausa certa. [ETAPA3.md 001]
- Fato com fonte; estimativa dita como estimativa; fato não confirmado vai como `[PENDENTE]` com versão alternativa. Não trave por isso. [playbooks/produzir-video.md]

**Não faça**
- Não passe de ~2.300 palavras se a meta for 17 min: 2.620 palavras deram **19:27** na Índia. [ETAPA-FINAL.md 002]
- Não traduza nem copie o texto da referência; modele estrutura, ritmo e beats. [BRIEF.md 001]
- Não ponha capítulos fora de ordem na descrição (no `out/description.txt` das cidades, "6:38 La plus grande ville" vem antes de "6:23 Récapitulatif"). O YouTube exige ordem crescente a partir de 0:00. [out/description.txt lotr-fr 001]

---

## Evidências por vídeo

| Vídeo | Palavras | Blocos | Capítulos | Duração final | Fonte |
|---|---|---|---|---|---|
| Egito v1 | 2.293 | 106 | hook + 8 | 954,5 s (15:54), ~150 palavras/min | ETAPA1.md, QA-v1.md 001 |
| Egito v2 (publicado) | 2.293 (mesmo texto, mais tags e pausas) | 106 | hook + 8 | **1020,3 s (17:00)** | ETAPA3.md, QA.md 001 |
| Índia (publicado) | 2.620 | 129 | hook + 9 | **1167,2 s (19:27)** | ETAPA-FINAL.md 002 |
| Cidades lotr-fr (publicado) | meta de ~1.150–1.250 (Kokoro, velocidade 0,92) | P01… | hook + 3 Eras + payoff + fecho | 498,5 s (8:18) | BRIEF.md, SCRIPT_FR.md, out/QA.md lotr-fr 001 |

### Ritmo da referência × nosso
- Referência History in Minutes: ~195 palavras/min. Nós: ~135 com as pausas da v2. [estilo.md historia-ptbr, 03/11/2026]
- Ritmo visual: Egito v2 com 295 planos, média de 3,46 s, 17,3 por minuto; Índia com 335 planos, média de 3,48 s, 17,2 por minuto. As referências têm 10–26 cortes/min no início (`youtube.assistidos`). [QA.md 001 e 002]

### Retenção por estrutura
- lotr-fr: vídeos de ~8 min retêm ~47–50%; os de 13–15 min, 30–44% (`youtube.metricas_video`, 2026-11-04; tabela em `titulos.md`). O 001 (cidades, 8:18, cronológico com loop até o payoff) está em **49,74%** com 54 views.
- historia-ptbr: **sem dado** de retenção (Egito e Índia republicados/publicados há ~1 dia; `pct_assistido` vazio em 2026-11-04).
- **Hipótese:** o hook longo da Índia (2:21 até o 1º capítulo) pode custar retenção. Comparar com o Egito (0:49) quando houver curva.
- **Hipótese:** vídeos de 17–19 min no historia-ptbr seguram tanto quanto as referências (a da China tem 25 min e 1,17 milhão de views). Validar com métricas.
