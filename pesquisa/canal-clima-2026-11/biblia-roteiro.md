# Bíblia de roteiro: Em Relevo (clima e geografia do Brasil em mapa 3D) — 16/11/2026

O canal ainda não tem `canais/em-relevo/biblia/`: esta é a bíblia de roteiro dele (ao lado de `biblia-titulo.md`, que cobre título e thumb). Prevalece sobre `conhecimento/`. Toda entrada leva data e fonte; sem dado = **Hipótese**.

## Forma (modelada) × Conteúdo (nosso)
Diretriz do Rodrigo (16/11/2026): *"identificar um tema que tem demanda, mas abordá-lo de outro ângulo, para fugir da manada; mas ter um padrão claro de roteiro que funciona em canais de sucesso."* Motivo: no historia-ptbr, remodelar a transcrição da referência fez o 005-brasil sair quase igual ao History in Minutes (detector 47/100). Auditoria de 16/11: **longo-05 (enchente de Porto Alegre) = 11/100** contra 5 vídeos do tema (Fatos Desconhecidos, Domingo Espetacular, BBC News Brasil, Brasil Escola, Terra em Choque): ângulo próprio (o caminho da água no mapa) (`pesquisa/roteiro-angulo-2026-11/AUDITORIA.md`).

### Forma (modelada): o que copiamos dos canais de sucesso, de propósito
- **Hook com lugar + data + número** no 1º segundo, depois a pergunta ("Dois tornados em 18 minutos." do @relevo.ia; "Era 11 de março de 2011, duas e quarenta e seis da tarde…" do Um Documentário; "At 8.37 in the morning…" do The Last Day). Fonte: `RELATORIO.md` (Arquivos, hooks literais) e `../estilo-mapa-relevo-3d/PADRAO.md` (Ritmo e estrutura).
- **Estrutura** (longo-03/04/05): hook com lugar/data/número → a pergunta do título dita até ~0:40 → "a resposta está no mapa" → 4–6 capítulos numerados (a aba de capítulo é uma pergunta ou uma camada da resposta) → A RESPOSTA que junta as camadas → fecho útil e compartilhável (o que fazer / mande para quem mora lá).
- **Câmera contínua no mapa** em vez de cortes; "olhe de cima", "suba a câmera" como transições faladas (longo-05 `ROTEIRO.md`).
- Números com fonte primária, sem alarmismo; probabilidade dita como probabilidade.

### Conteúdo (nosso): o que nunca vem da referência
- **Ângulo próprio** (`ANGULO.md`, skill `pesquisa-referencia` passo 7): transcreva a manada do tema (os 3–5 vídeos de mais views em pt, inclusive TV/jornal no YouTube e canais de curiosidade; `tools/manada.py`) e escolha uma **explicação geográfica** que eles não dão (o caminho da água, o relevo, a série histórica, a comparação de mapas). Notícia e depoimento são a manada; o mapa que explica é o nosso.
- **Proibido:** o hook de um vídeo da manada; a sequência de cenas de uma reportagem; traduzir/reescrever transcrição; usar reportagem de TV como fonte de número (fonte = INMET, ANA, CEMADEN, Defesa Civil, prefeituras, artigos, WWA, NOAA/USGS).
- **Cota: ≥ 40% dos dados/cenas principais** fora de todas as transcrições da manada (listados em `pesquisa/FATOS.md` / `SOURCES`). **Hipótese** (16/11/2026).
- **Portão:** `tools/similaridade_roteiro.py <pasta longo-NN>` (lê `shared/blocos.json`) < 30 e `CRIVO-ANGULO.md` APROVADO (`skills/roteiro/CRIVO-ANGULO.md`) antes do storyboard/voz.

## Checklist (acrescenta ao do brief do lote)
- [ ] `ANGULO.md` com a manada transcrita e o ângulo escolhido; hook não é o de nenhum vídeo da manada.
- [ ] `SIMILARIDADE.md` < 30; `CRIVO-ANGULO.md` APROVADO; ≥ 40% dos dados/cenas fora da manada.
