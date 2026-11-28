# Bíblia, ramo "Expediente de ingreso" (dossie-es) — teste aprovado em 28/11/2026

**Decisão do Rodrigo (28/11/2026, 13:45 e 13:50):** aprovado o formato "Expediente de ingreso" da proposta `../analises/2026-11-28-formato-como-era-vivir.md` como **teste**, num **ramo separado** da bíblia. A bíblia padrão (`../biblia/`) fica exatamente como está e continua valendo para todos os outros vídeos do canal.

## Quando usar este ramo
- **Só** no vídeo cujo item do `youtube.backlog` tem no ângulo a tag **`RAMO: biblia-ingreso`** (mecanismo de seleção, 28/11/2026). A `tools/rotinas/noturna.py` lê essa tag e aponta os briefs das etapas 1 e 2 para esta pasta; sem a tag, o vídeo usa `../biblia/`.
- Skills, crivos e QA que mandam ler `canais/dossie-es/biblia/` (embalagem/`CRIVO.md`, roteiro/`CRIVO-ANGULO.md`, `qa`): num vídeo deste ramo, leiam **este** README e os arquivos daqui primeiro; não reprovem por faltar "TODA la historia", hook-anedota em 3ª pessoa ou 11–14 expedientes cronológicos (não valem aqui).
- 1º teste: **"Así era formar parte de la MAFIA SICILIANA (Sicilia, 1962)"** (noite de 28/11/2026). Plano do teste (3 vídeos, métricas e corte): proposta §4.

## O que é
O espectador recebe a **ficha de entrada** numa organização, **num ano e num lugar exatos**. Cada EXPEDIENTE é uma etapa da vida lá dentro (entrada → prova → juramento → regras → dinheiro → rotina → falta → saída), contada em **2ª pessoa ("tú")** e **provada pelo depoimento/documento de um recluta real**, que é o fio do vídeo. Diferença para a manada ("Tu vida en cada rango…", Te lo Pinto e clones): lá é escada fictícia sem data nem fonte; aqui é uma época, um lugar e um recluta documentado.

## Arquivos deste ramo (prevalecem sobre o padrão nestes assuntos)
- [`roteiro.md`](roteiro.md): esqueleto fixo, 2ª pessoa, recluta-fio, regras novas.
- [`titulo.md`](titulo.md): padrões de título do ramo (sem "TODA la historia"; proibido "Tu vida en cada rango").
- [`thumb.md`](thumb.md): a ficha de ingresso como objeto e os 3 padrões A/B/C.

## O que herda da bíblia padrão (não copiado aqui: leia lá)
Tudo o que este ramo não define vem de `../biblia/`:
- `../biblia/README.md`: o que NÃO fazer no canal, políticas do YouTube (sem morte/assassinato no título, sem violência explícita, sem foto de morto, sem menção a IA).
- `../biblia/roteiro.md`: **Forma × Conteúdo** (ângulo próprio, `ANGULO.md`, manada, detector < 30, crivo de ângulo, cota ≥ 50% fora da manada), **Tom** (presente histórico, seco, atribuição a documento, ângulo América Latina quando houver), **Idioma** (espanhol neutro com tú, revisão nativa), **Tamanho/WPS 2,38**, revisão de fatos, **CTA de inscrição** (frase fixa, ~60%, `cta/inscricao/`), e todas as lições dos vídeos 001–017.
- CTA da HQ ~37–40% (`../cta/encaixe.py`), botão SUSCRÍBETE, carimbos, SFX nas transições, pasta parda, máquina de escrever, cartelas "EXPEDIENTE N": `../biblia/visual.md`.
- Voz: `../biblia/voz.md` e `../canal.yaml`. Escolha de tema (bolha): `../biblia/temas.md`.
- Regra do **nome que diz o que é** (explicador "mafia + país" nas primeiras ~5 palavras do título e escrito na thumb): `../biblia/titulo.md` e `../biblia/thumb.md` (24 e 27/11/2026).
- Thumb: paleta, traço graphic novel, ícone cultural do país, sem suástica/runas: `../biblia/thumb.md`.

Aprendizado de um vídeo deste ramo vai para **este** ramo (com data e fonte; sem dado = Hipótese). Se o teste passar (critério na proposta §4c), o Rodrigo decide se o ramo vira slot fixo.
