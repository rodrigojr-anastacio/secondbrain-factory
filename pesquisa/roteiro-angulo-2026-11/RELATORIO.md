# Roteiro com ângulo próprio · 16/11/2026

Pedido do Rodrigo (16/11/2026, brief `~/workspace/referencias/BRIEF-roteiro-angulo-proprio.md`): o "A HISTÓRIA INTEIRA do Brasil em 13 minutos" (History Easy Guide, `sD0cIJ8JMYw`) e o nosso 005-brasil têm roteiro praticamente igual. Causa: a bíblia do historia-ptbr mandava "remodelar a transcrição da referência (mesma ordem, beats e números)", e a skill `roteiro` partia da transcrição do canal-modelo.

## O que mudou no fluxo
1. **Ângulo antes da embalagem** (`skills/pesquisa-referencia`, passo 7): `tools/manada.py` busca e transcreve os 3–5 vídeos de mais views do tema (+ canal-modelo + clones) → `ANGULO.md` (consenso da manada, 2–3 ângulos, 1 escolhido, anedotas próprias previstas). A embalagem lê o `ANGULO.md` e vende o ângulo.
2. **Roteiro:** a referência é molde só de forma; proibido reescrever/traduzir transcrição ou seguir a ordem de beats da manada; fatos de fonte própria no `SOURCES.md`; cota de anedotas próprias por canal.
3. **Detector de cópia** (`tools/similaridade_roteiro.py`) no fim da etapa 1: cópia ≥ 30 reprova; 18–29 = atenção. Calibragem: `CALIBRAGEM.md`.
4. **Crivo de ângulo** (`skills/roteiro/CRIVO-ANGULO.md`): revisor independente; máx. 2 reescritas; reprovado = `BLOQUEIO.md` (a palavra "crivo" faz o vigia da noite pôr o próximo tema).
5. **Backlog vivo:** subcomando `backlog.py angulo` (ângulo + evidência `manada`); a rotina de seg/qui preenche o ângulo de todo item novo; os 28 itens `agendado` foram refeitos em 16/11 (todos trocaram o hook/fio que coincidia com a manada; fatos novos marcados `[conferir]`).
6. Encaixe: skills `produzir-video`, `qa` (item 6c), modelos `BRIEF-lote-MODELO-ETAPA1/2.md`, `noturna.py` (briefs da noite), `MAPA.md`, `AGENTS.md`, `playbooks/produzir-video.md`, `conhecimento/roteiros.md`.

## Forma (modelada) × Conteúdo (nosso)
Seção nova em cada bíblia de roteiro: `canais/historia-ptbr/biblia/roteiro.md`, `canais/dossie-es/biblia/roteiro.md`, `canais/lugares-guerra-en/biblia/roteiro.md` e (novo) `pesquisa/canal-clima-2026-11/biblia-roteiro.md`. Cotas (Hipótese, 16/11): historia/Clearance/Em Relevo ≥ 40% das cenas principais fora da manada; dossie ≥ 50% dos expedientes.

## Arquivos
- `CALIBRAGEM.md`: casos e limites do detector.
- `AUDITORIA.md`: os 9 vídeos auditados (relatório por vídeo em `auditoria/`).
- `refs/<chave>/`: transcrições da manada de cada vídeo auditado (`manada.json` com canal, views, data).
- Custo: tradução Haiku US$ 0,13 (financas.consumo, `preqa:similaridade-traducao`); busca/transcrição US$ 0.
