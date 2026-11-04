# Hooks: fórmulas e exemplos reais

**Como atualizar:** quem alimenta este arquivo é o especialista de **Tendências** (hooks de referência que viralizam), o de **Métricas** (retenção dos primeiros 30–60 s dos nossos vídeos) e o **feedback do Rodrigo**. Cada entrada nova leva **data e fonte** (arquivo, consulta SQL ou mensagem do Rodrigo). Sem dado, marque **Hipótese**. Depois de editar, faça commit descritivo (ex.: `conhecimento/hooks: retenção 30s do Egito`).

Última revisão: 2026-11-04 (estudo de 3 transcrições e hook por anedota no 003).

---

## Regras rápidas

**Padrão novo do historia-ptbr (a partir do 003, 04/11/2026; pedido do Rodrigo + estudo de 3 transcrições, ver "Estudo de 04/11" abaixo):**
1. **Anedota humana concreta em ≤ 10 s**: data + lugar + uma pessoa + uma ação + desfecho seco ("Tus, por volta de 1025. Uma caravana com o ouro devido a um poeta entra por um portão. Pelo outro, sai o caixão do poeta.").
2. **Promessa do título + pergunta central numa frase** ("Essa é a história inteira do Irã: …").
3. **1 loop aberto** ("e o que salvou o Irã estava naquele caixão") pago por volta de 1/4–1/2 do vídeo, com o detalhe que faltava.
4. **Hook total ≤ 35 s**, e o 1º capítulo começa já com o título falado. A fórmula "paradoxo → prova em rajada" abaixo continua valendo como recurso dentro dos capítulos.

**Faça**
- Abra com **paradoxo ou reformulação que choca**, dito como fato ("O Egito não é um país que tem um rio. É um rio com um país em volta."). [estilo.md historia-ptbr; SCRIPT.md 001]
- Em seguida, a **prova em rajada**: 2–4 números ou uma comparação de escala de tempo ("Cleópatra viveu mais perto do iPhone do que dos homens que ergueram a Grande Pirâmide"). [SCRIPT.md 001]
- **Virada** ("Mas a parte mais louca é outra") → **pergunta central** que segura o vídeo inteiro → (opcional) **promessa do percurso** → entrada **imediata** no corpo com um fato estranho e concreto. [BRIEF.md 001]
- Feche o hook em **~40–45 s**. Frases curtas, linguagem falada, sem "olá, pessoal" nem vinheta. [BRIEF.md 001]
- **Abra loops** no hook e pague no fim ("o medo que o Egito carrega desde o primeiro faraó" → a represa da Etiópia; "a mais grande cité de toute Arda… je vous la révèle à la fin"). [ETAPA1.md 001; SCRIPT_FR.md lotr-fr 001]
- No lotr-fr: comece pelo **familiar** (Minas Tirith, Khazad-dûm, Osgiliath, Umbar) e vire a expectativa ("on les découvre presque toujours au pire moment"). [SCRIPT_FR.md lotr-fr 001]
- Dê **credibilidade** quando o dado for incerto ("Tolkien ne donne presque jamais de chiffres… quand c'est une estimation, je vous le dirai"). [SCRIPT_FR.md lotr-fr 001]

**Não faça**
- Não traduza o hook da referência. Modele a técnica com texto próprio. [BRIEF.md 001; playbooks/produzir-video.md]
- Não estique o hook: na Índia ele foi até 2:21 (16 blocos), contra 0:49 no Egito. **Hipótese:** isso pesa na retenção inicial; confira quando houver curva de retenção. [out/youtube.txt 002 e 001, capítulos]
- Não termine um bloco do hook com frase curta depois de `[break]`: o Fish corta a frase (aconteceu com "Guarde essa chuva"). [QA.md 002; estilo.md historia-ptbr]
- Não deixe o 1º minuto com poucos cortes: com as pausas novas, o Egito v2 caiu para 21 planos no 1º minuto (de 23), no limite inferior. [QA.md 001; ETAPA3.md 001]

---

## Evidências

### Fórmula sintetizada de 6 referências (Tendências, 2026-11-02)
Fonte: `canais/historia-ptbr/estilo.md` e `canais/historia-ptbr/videos/001-egito/BRIEF.md`; hooks reais em `pesquisa/tendencias/assets/2026-11-02/<id>/hook.txt`; dados de `youtube.assistidos` (consulta de 2026-11-04).

| Referência | Views (na época) | Duração | Cortes/min no início (`assistidos.cortes_por_min`) |
|---|---|---|---|
| Egito, History in Minutes (VQPzrVMHWlg) | 417 mil | 1038 s | 14 |
| Índia, History in Minutes (p9IIGdg91fE) | 606 mil | 1001 s | 16 |
| Irã, Genius History (XO1-4FH1X1I) | 918 mil | 657 s | 26 |
| Roma, Genius History (kHCamT4zfH4) | 364 mil | 733 s | 19 |
| Jerusalém, History Is Strange (zMn0RYC6U6w) | 161 mil | 526 s | 12 |
| China, Animated History (wuhnBi8jNl0) | 1,17 milhão | 1556 s | 10 |
| Império Britânico, Genius History (cqGJ5ZRLAvs) | 222 mil | 613 s | 22 |

Estrutura: frase 1 = paradoxo → prova em rajada → virada → pergunta central → promessa (opcional) → entrada imediata no corpo. Tudo em até ~40 s.

### Nossos hooks reais

**Egito (historia-ptbr 001), publicado.** Fonte: `canais/historia-ptbr/videos/001-egito/SCRIPT.md`, `ETAPA1.md`.
> O Egito não é um país que tem um rio. É um rio com um país em volta. / Mais de noventa por cento dele é deserto. […] / Cleópatra viveu mais perto do iPhone do que dos homens que ergueram a Grande Pirâmide. / Mas a parte mais louca é outra. Sumérios, hititas, assírios: todos sumiram. O Egito continua aqui. / Então como um país invadido por persas, gregos, romanos, árabes, turcos e britânicos continuou sendo o Egito? / Em menos de vinte minutos, sete mil anos. E, no fim, o medo que o Egito carrega desde o primeiro faraó.

- Entrada no corpo: a múmia tatuada de Gebelein. Loop extra: "Guarde esse ano: 1922", pago no capítulo 7.
- Introdução: 0:00–0:49 (v2). [out/youtube.txt 001]
- **Métrica:** nenhuma ainda. O vídeo foi republicado como `g847Td0Plsk` (6 views em `youtube.metricas_video`, 2026-11-04, sem retenção). A retenção do hook fica **sem dado**.

**Índia (historia-ptbr 002), publicado.** Fonte: `canais/historia-ptbr/videos/002-india/SCRIPT.md`, `BRIEF.md`.
> Olhe para a Índia do espaço em maio, e você não vai ver um país verde. Vai ver um país marrom […] Agora olhe em setembro. É outro país. […] A Índia não é um país que tem uma monção. A Índia é uma monção que fez crescer um país.

- Mesma técnica do Egito (reformulação "não é um país que tem X; é X que fez um país"), seguida de pergunta central ("como uma terra que todo império queria sobrevive a todos os impérios que a tomaram?") e de uma lista de promessas (dentistas, cidade que virou ferrovia, batalha decidida por tempestade…).
- Hook modelado na **transcrição completa** da referência p9IIGdg91fE, por pedido do Rodrigo. [BRIEF.md 002]
- Introdução: 0:00–2:21. [out/youtube.txt 002]
- **Métrica:** `MV5SSjoccqE`, 17 views em 2026-11-04, sem retenção ainda. **Sem dado** para julgar o hook.

**Cidades da Terra-média (lotr-fr 001), publicado em 2026-11-02.** Fonte: `canais/lotr-fr/videos/001-maiores-cidades/SCRIPT_FR.md`.
> Minas Tirith, la cité blanche adossée à la montagne. Khazad-dûm […] Ces noms, vous les connaissez. Mais il y a un piège. On les découvre presque toujours au pire moment de leur histoire. […] Alors, quelle a été la plus grande ville de la Terre du Milieu ? […] Et la plus grande cité de toute Arda… je vous la révèle à la fin.

- Modelado em "What were Middle-earth's largest cities?" (Darth Gandalf, 76 mil views em 11 dias). [BRIEF.md lotr-fr 001]
- **Métrica (youtube.metricas_video, 87BdomKxa-M, 2026-11-04):** 54 views, média assistida de 248 s, **49,74% assistido** (vídeo de 499 s). É o melhor % assistido entre os vídeos de ~8 min do canal com mais de 50 views (ver `roteiros.md`). A curva de retenção dos primeiros 30 s **não foi coletada**.

### O que falta medir
- Retenção aos 30 s e aos 60 s de cada vídeo nosso (`tools/report.py <canal> --retencao <ID>`). Até lá, toda conclusão sobre "hook bom" é **Hipótese**.

## Estudo de 04/11/2026: 3 transcrições completas (Produtor, vídeo 003)
Fonte: `canais/historia-ptbr/videos/003-ira/ref/` (Whisper small via WARP, `tools/transcrever.py`): History in Minutes "Iran" (XVwr1Rm_9jc, 89 mil views), Archive in Minutes "Gestapo" (pbIzG1QvoWs, 349 mil) e "KGB" (VNJhu4rh6OY, 236 mil); views via yt-dlp em 04/11/2026.
| Vídeo | Abertura | Até a promessa do título | Hook total |
|---|---|---|---|
| Gestapo | "In 1943, a war widow tells a colleague… a joke. The colleague reports her. She is put to death." | 9 s | ~18 s, e já entra "The Stamp." |
| KGB | "December 1989. Dresden. A KGB officer burns files so fast the furnace bursts… His name is Vladimir Putin." | 13 s | ~22 s |
| HiM Irã | paisagem de 9 mil anos atrás → qanats → jardim "paraíso" → crise de hoje → pergunta → lista de 4 promessas | 92 s ("This is the story of Iran") | 1:54 até o 1º fato datado |
- O Archive paga a anedota perto de 1/4 do vídeo (a viúva volta aos 3:29 com o detalhe cruel: "os juízes contaram contra ela que o marido morreu pela pátria"). O KGB paga no fim (o oficial de Dresden vira presidente).
- O HiM usa loops "Remember that word" (Irã → 1935) e "Remember the tobacco" (1891 → 1979).
- **Hipótese:** o hook curto por anedota do Archive (15–22 s) retém melhor que o hook longo do HiM (1:32); o Archive tem 3–4× mais views por vídeo com 1/4 da idade. Medir no 003 (retenção aos 30 s) × Egito/Índia.

## Referência: hook por anedota humana (Archive in Minutes, Gestapo)
Fonte: `watch.py pbIzG1QvoWs` em 2026-11-04 (hook.txt); views do garimpo de 2026-11-02 (310 mil em ~7 dias após 26/10).
> In 1943, a war widow tells a colleague at her munitions factory a joke. […] The colleague reports her. She is put to death. This is the entire history of the Gestapo, and how a small police force watched 80 million people.

- Técnica: cena humana datada com desfecho cruel em ~9 s, depois a promessa do título e a pergunta implícita. Cortes ≈ 20/min no início.
- **Hipótese:** funciona melhor que abrir direto com a definição. Sem dado nosso; testar num vídeo do historia-ptbr e medir retenção aos 30 s.
- Observação do mesmo garimpo: o tema pesa mais que o hook; Archive in Minutes tem 120–310 mil views em serviços secretos/Guerra Fria e 10–30 mil em Titanic/Abwehr/Romanovs. Vídeos de 31–36 min (Prima Historian) ficaram em ~700 views. [garimpo 2026-11-02]
