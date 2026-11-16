# Crivo de ângulo do roteiro (revisor independente; desde 16/11/2026)

Roda no fim da etapa 1, **depois** do `tools/similaridade_roteiro.py` e **antes** do storyboard/voz. Um Task separado, em primeiro plano, que **não** recebe o raciocínio do roteirista: só os caminhos abaixo. Máx. 2 rodadas de reescrita (3 pareceres); ainda reprovado = `BLOQUEIO.md` com a palavra "ângulo".

**Por que existe:** o historia-ptbr/005-brasil (09/11/2026) é praticamente o roteiro do History in Minutes `Vug2cLY3nxk` traduzido (nota 47/100 no detector; o clone History Easy Guide `sD0cIJ8JMYw` deu 38), porque a bíblia mandava "remodelar a transcrição da referência (mesma ordem, beats e números)". Diretriz do Rodrigo (16/11/2026): **forma** modelada dos canais de sucesso, **conteúdo e ângulo** nossos, para fugir da manada.

## Prompt (copie para o Task, preenchendo os <…>)
```
Você é um revisor editorial independente e exigente. Não escreveu este roteiro e não deve adivinhar a intenção de quem
escreveu: julgue só pelo que está nos arquivos. Responda em pt-BR.

Leia:
- <pasta>/SIMILARIDADE.md (nota do detector de cópia por referência + trechos parecidos; limites no topo)
- <pasta>/ANGULO.md (a manada, o consenso que NÃO pode ser repetido, o ângulo escolhido e a cota de anedotas próprias)
- <pasta>/SCRIPT.md (ou ROTEIRO.md) e <pasta>/SOURCES.md (ou FATOS/FONTES)
- <pasta>/EMBALAGEM.md (a promessa)
- as transcrições da manada em <pasta>/ref/manada-*.txt (para conferir; leia ao menos as 2 de maior nota no detector)
- a bíblia de roteiro do canal: <caminho da bíblia>/roteiro.md, seções "Forma (modelada)" e "Conteúdo (nosso)"

Avalie, com evidência (bloco do roteiro × trecho da transcrição):
1. Detector: nota máxima < limite de CÓPIA? (≥ limite = REPROVADO automático.) Se em "atenção", os trechos
   listados são fatos obrigatórios do tema ditos com palavras nossas (ok) ou a mesma cena/explicação da referência (não)?
2. Ordem: a sequência de capítulos/beats é diferente da de cada vídeo da manada? (Cronologia obrigatória do tema não
   basta para reprovar; reprova se a escolha do que entra, a cena de abertura de cada capítulo e as transições
   repetem um vídeo da manada.)
3. Hook: a anedota/cena do hook NÃO é a de nenhum vídeo da manada?
4. Ângulo: o roteiro executa o ângulo escolhido no ANGULO.md (tese/recorte/fio condutor visível no hook, que volta
   ao longo do vídeo e fecha no fim)? Ou o ângulo ficou só no papel e o corpo é o consenso da manada?
5. Cota de anedotas/dados próprios: conte as anedotas/cenas principais do roteiro; quantas NÃO aparecem em nenhuma
   transcrição da manada? Compare com a meta da bíblia do canal (seção "Conteúdo (nosso)").
6. Fontes: os fatos têm fonte própria no SOURCES (livro, artigo, enciclopédia, arquivo, dado oficial)? Algum fato só
   tem como "fonte" um vídeo concorrente/transcrição? (Isso reprova o fato.)
7. Forma: o roteiro continua na forma da bíblia (não é para fugir da forma, só do conteúdo)?

Grave <pasta>/roteiro-crivo/crivo-angulo-r<n>.md e copie para <pasta>/CRIVO-ANGULO.md, no formato:
# Crivo de ângulo r<n> · <data> · APROVADO | REPROVADO
| item | resultado | evidência |
(itens 1–7; no 5, "X de Y anedotas próprias = Z% (meta M%)")
## Correção pedida (só se reprovado)
- bloco/capítulo → o que trocar (cena, ordem, anedota, fonte) — nunca "trocar sinônimos"
Régua: APROVADO só se 1, 3, 5 e 6 passarem e 2/4 não tiverem falha grave. Na dúvida entre aprovar e reprovar, reprove
com correção específica.
```

## Depois do parecer
- APROVADO → anote nota do detector + rodada no `ETAPA1.md` (e no `ETAPA1-PRONTA.md`, na fila) e siga para o storyboard.
- REPROVADO → reescreva só o apontado, rode `tools/similaridade_roteiro.py` de novo e chame um revisor **novo** (outro Task). Rodada 3 reprovada → `BLOQUEIO.md` ("crivo de ângulo reprovado em 3 pareceres: …") e pare.
