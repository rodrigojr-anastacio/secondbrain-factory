# Hooks: regras gerais

> **Regras gerais. Regra de canal está em `canais/<slug>/biblia/` e sempre prevalece.** O molde de hook de cada canal (com exemplos reais e métricas) está em `canais/<slug>/biblia/roteiro.md`: `historia-ptbr` = paradoxo → prova → virada → pergunta central → promessa (History in Minutes); `dossie-es` = anedota seca de 25–35 s (Archive in Minutes); `lotr-fr` = do familiar à pergunta, com loop pago no fim.

**Como atualizar:** **Tendências** (hooks de referência), **Métricas** (retenção aos 30–60 s) e **feedback do Rodrigo**. Padrão de um formato vai para a bíblia do canal que usa esse formato; aqui só o que vale para qualquer canal. Cada entrada leva **data e fonte**; sem dado = **Hipótese**. Commit descritivo.

Última revisão: 2026-11-04 (caixinhas por canal: moldes movidos para as bíblias).

---

## Regras gerais
**Faça**
- **Entre no assunto no 1º segundo**: sem "olá, pessoal", sem vinheta, sem pedir inscrição no hook. [BRIEF.md historia-ptbr 001; transcrições do Archive, 04/11]
- **Abra pelo menos um loop** no hook e pague-o mais tarde (meio ou fim). Todos os nossos hooks e as referências que performam fazem isso. [ETAPA1.md historia-ptbr 001; SCRIPT_FR.md lotr-fr 001; transcrições do Archive]
- **Pergunta ou promessa explícita** que diga o que o vídeo entrega, ligada ao título.
- **Dê credibilidade** quando o dado for incerto ("quando for estimativa, eu aviso"). [SCRIPT_FR.md lotr-fr 001]
- **Modele a técnica** do canal-modelo da bíblia com texto próprio; nunca traduza o hook da referência. [playbooks/produzir-video.md]
- Muitos cortes no 1º minuto (≥ ~18–21/min); as referências que performam têm 14–26, as que flopam 6–14. [`youtube.assistidos`; LEVANTAMENTO archive-in-minutes §2e]

**Não faça**
- Não use o molde de hook de outro canal (ver a bíblia). Ex.: o 003 do historia-ptbr abriu com a anedota seca do Archive (04/11/2026), parte do erro de mistura de canais. [`conhecimento/anti-padroes.md` §8]
- Não estique o hook sem necessidade. **Hipótese:** hooks longos (Índia: 2:21) custam retenção inicial; medir.

## Evidência geral
- **Hipótese (garimpo de 2026-11-02 e LEVANTAMENTO archive-in-minutes):** **o tema pesa mais que o hook.** O Archive usou o mesmo molde de hook no Abwehr (33 mil) e na Gestapo (349 mil); tem 120–310 mil views em serviços secretos/Guerra Fria e 10–30 mil em Titanic/Abwehr/Romanovs.

## O que falta medir
- Retenção aos 30 s e aos 60 s de cada vídeo nosso (`tools/report.py <canal> --retencao <ID>`), registrada na bíblia do canal. Até lá, toda conclusão sobre "hook bom" é **Hipótese**.

## O que saiu daqui em 2026-11-04 (e para onde foi)
- "Padrão novo do historia-ptbr a partir do 003" (anedota ≤ 10 s, hook ≤ 35 s) → **revogado no historia-ptbr**; é o molde Archive, agora em `canais/dossie-es/biblia/roteiro.md`.
- Fórmula sintetizada de 6 referências (HiM, Genius History…), hooks do Egito, Índia e Irã → `canais/historia-ptbr/biblia/roteiro.md` ("Evidências de hook").
- Estudo de 04/11 (3 transcrições): HiM Irã → `canais/historia-ptbr/biblia/roteiro.md`; Archive Gestapo/KGB e "hook por anedota humana" → `canais/dossie-es/biblia/roteiro.md`.
- Hook das cidades (lotr-fr) → `canais/lotr-fr/biblia/roteiro.md`.
- "Fish corta frase curta depois de `[break]`" → `conhecimento/anti-padroes.md` §2 (ferramenta) e `canais/historia-ptbr/biblia/voz.md`.
