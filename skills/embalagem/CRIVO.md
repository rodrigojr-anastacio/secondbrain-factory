# Crivo da embalagem (revisor independente)

Portão único da embalagem de um vídeo novo (decisão do Rodrigo, 14/11/2026: **só o crivo** aprova; ele não aprova cada vídeo). Adaptado do crivo de 7 itens da reembalagem (`pesquisa/reembalagem-2026-11-14/crivo/INSTRUCOES-REVISOR.md`), que reprovou 19 de 45 elementos na 1ª rodada. A diferença: o vídeo **ainda não existe**, então "promessa paga" vira "promessa **cumprível** com o material da pesquisa" e vira obrigação para o roteiro.

## Como disparar (quem propôs faz isto)
Um **Task separado, em primeiro plano**, por rodada, sempre um revisor **novo** (nunca o mesmo agente que propôs, nunca um revisor que já viu outra rodada). Cole o prompt abaixo trocando `<…>`. Não acrescente opinião, resumo nem "acho que está bom".

```text
Você é o revisor independente do crivo da embalagem da fábrica do YouTube. Siga à risca
~/workspace/fabrica-youtube/skills/embalagem/CRIVO.md, seção "Instruções do revisor".
Rodada: <n> de 3. Canal: <slug>. Vídeo: <pasta do vídeo, caminho absoluto>.
Proposta: <pasta>/EMBALAGEM.md · dados e mosaico: <pasta>/embalagem/ · BRIEF: <pasta>/BRIEF.md
Bíblia: ~/workspace/fabrica-youtube/canais/<slug>/biblia/ (README, titulo.md, thumb.md)
Grave <pasta>/embalagem/crivo-r<n>.md e copie para <pasta>/CRIVO.md. Tudo em primeiro plano. Não faça commit.
```

## Instruções do revisor
Você é **cético** por ofício. Não foi você quem propôs; seu trabalho é achar o que está errado. **Na dúvida, reprove** e diga exatamente o que corrigir. Embalagem fraca aprovada custa um vídeo inteiro (~R$ 50 e um dia de fila) com CTR baixo. Responda em pt-BR. Repo `~/workspace/fabrica-youtube`. Tudo em primeiro plano.

**Você lê só:** `EMBALAGEM.md`, a pasta `embalagem/` (`refs.csv`, `medianas.json`, `mosaico.jpg`, `mosaico-320.jpg`, thumbs), o `BRIEF.md` (e as fontes que ele cita), a bíblia do canal (`README.md`, `titulo.md`, `thumb.md`; Em Relevo: `pesquisa/canal-clima-2026-11/biblia-titulo.md`), `conhecimento/politicas-youtube.md`, `conhecimento/titulos.md`, e `pesquisa/reembalagem-2026-11-14/padroes.md` (seção do canal, incluindo "O que NÃO funciona"). Na rodada ≥ 2, **não** leia `crivo-r<n-1>.md` nem `EMBALAGEM-r*.md`: você é um revisor novo.

**Confira de verdade:**
- ≥ 2 referências de cada elemento com `videos.list` (views e data): `cd ~/workspace/fabrica-youtube/tools && .venv/bin/python -c "from trends import yt_client; yt=yt_client(); print([(v['id'], v['statistics']['viewCount'], v['snippet']['publishedAt'][:10], v['snippet']['title']) for v in yt.videos().list(part='snippet,statistics', id='ID1,ID2').execute()['items']])"`. Mediana do canal: `embalagem/medianas.json` (se faltar, `playlistItems` + `videos.list` dos últimos 50). **Não use `search.list`.** YouTube pelo navegador/yt-dlp só via `socks5://127.0.0.1:40000`. Nunca imprima tokens.
- Colisão: procure no `refs.csv` (e, se precisar, 1–2 buscas yt-dlp via WARP) títulos iguais ou com a mesma fórmula no tema.
- Caracteres: `python3 -c "print(len('<título>'))"`.
- Olhe o `mosaico.jpg` e o `mosaico-320.jpg` com Read e imagine a thumb proposta no meio deles a 320×180.

**Avalie SEPARADAMENTE Título 1, Título 2 e Thumb.** Cada um passa só se passar em todos os itens que se aplicam:
1. **Evidência:** ≥ 2 vídeos reais com o mesmo padrão (título: padrão de título; thumb: padrão de thumb), mesmo nicho e idioma (inglês só como apoio de tema global), ≤ ~400 d, **acima da mediana real** do canal deles. Referência inexistente, views > 30% diferentes do real, "acima da mediana" falso ou padrão diferente do alegado = reprova.
2. **Promessa cumprível:** o que título/thumb prometem é sustentado pelo material da pesquisa (fatos com fonte no BRIEF/fontes: confira que existem), cabe na duração-alvo e pode ser **paga no 1º minuto** e sustentada pelo vídeo inteiro. Reprove: promessa sem material; caso que ocupará ~1 minuto de um vídeo longo vendido como o vídeo todo; curiosidade resolvida em segundos; pagamento só no fim; exagero que o tema não entrega ("lo que NO te contaron", "segredo" de fonte pública). A seção "Obrigações" tem de transformar a promessa em instrução concreta para o roteiro (frase-âncora + até quando paga); se estiver vaga, reprove.
3. **Título × thumb:** se complementam; a thumb não repete palavra nem ideia do título; juntos criam uma pergunta. Avalie a thumb com **cada** título.
4. **Celular** (só thumb): legível a 320×180: ≤ 3 palavras de leitura, contraste, **1 foco**; destaca-se no mosaico do tema (não faz o que todas fazem).
5. **Diferenciação:** não é cópia literal de título/thumb de clone ou referência; a fórmula idêntica à dos clones no mesmo tema conta como cópia (ex.: "TODA la Historia de X en N Minutos" onde o Atlas já tem o mesmo tema; "N anos de X em N minutos" onde já há 5+). Subtítulo diferente pode ou não bastar: julgue e justifique.
6. **Regras:** `conhecimento/politicas-youtube.md` (sem morte/morreu/morto/matou/assassinado/assassinato; muerte/murió/muerto/mató/asesinado/asesinato; death/dead/died/killed/murdered; massacre/chacina/chocante/perturbador e equivalentes; sem cadáver, sangue, ferimento, caveira, insígnia extremista ou apelação na thumb); ≤ 100 caracteres e o teto da bíblia; "em N minutos" só se a bíblia mantiver; **bíblia do canal** respeitada (fórmula, identidade visual, "O que NÃO fazer aqui"); desvio só se escrito "desvio da bíblia: … porque …" **com** evidência (desvio sem justificativa = reprova); nada de padrão de outro canal da fábrica.
7. **Faz sentido de verdade?** Em 2–3 linhas: "um espectador que viu os vídeos do mosaico clicaria neste em vez deles? por quê?". Se a resposta honesta for "não" ou "talvez", reprove.

**Rodada ≥ 2:** avalie completamente cada elemento `[REESCRITO]`. Nos `[MANTIDO]`, confira os itens 3 e 6 (casam com os elementos novos?) e reprove só se passaram a conflitar ou violar regra. Na rodada 3, lembre: reprovar aqui bloqueia o vídeo; seja justo e específico, mas não baixe a régua.

## Saída: `embalagem/crivo-r<n>.md` (e cópia idêntica em `CRIVO.md`)
```text
# Crivo <canal>/<NNN-slug> · rodada <n> · <data>
Conferido: videos.list (N ids), medianas, mosaico, fontes do BRIEF (quais)
## Título 1: APROVADO | REPROVADO — "<título>"
1 Evidência: ok/falha — números reais conferidos
2 Promessa: ok/falha — material que sustenta / o que falta
3 Título×thumb: …
5 Diferenciação: …
6 Regras: … (N caracteres)
7 Faz sentido: …
Correção pedida (se reprovado): …
## Título 2: … (mesmos itens)
## Thumb: … (itens 1–7)
## Obrigações para o roteiro: suficientes | vagas (o que falta)
## Veredito: APROVADO (3 de 3) | REPROVADO (X de 3) — rodada <n> de 3
- 1 linha por elemento reprovado com a correção pedida
```
Não escreva em nenhum outro lugar. Não faça commit. Resposta final a quem disparou: o bloco "Veredito".

## Regra do portão
- **APROVADO** = T1, T2 e Thumb aprovados **e** obrigações suficientes. Só aí a etapa 1 segue para o roteiro (e só aí grava `ETAPA1-PRONTA.md` no fim).
- Reprovado → quem propôs reescreve só o reprovado e chama um revisor novo. **Máx. 3 rodadas.** Reprovado na 3ª → `BLOQUEIO.md` na pasta do vídeo e a etapa para.
- Toda reprovação fica no histórico (`embalagem/crivo-r*.md` + `EMBALAGEM-r*.md`): é a base do futuro eval automático (próximo passo em `conhecimento/titulos.md`, não implementado).
