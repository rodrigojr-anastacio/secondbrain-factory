# Hooks: fórmulas e exemplos reais

**Como atualizar:** quem alimenta este arquivo é o especialista de **Tendências** (hooks de referência que viralizam), o de **Métricas** (retenção dos primeiros 30–60 s dos nossos vídeos) e o **feedback do Rodrigo**. Cada entrada nova leva **data e fonte** (arquivo, consulta SQL ou mensagem do Rodrigo). Sem dado, marque **Hipótese**. Depois de editar, faça commit descritivo (ex.: `conhecimento/hooks: retenção 30s do Egito`).

Última revisão: 2026-11-04 (base inicial, Fase 1).

---

## Regras rápidas

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
