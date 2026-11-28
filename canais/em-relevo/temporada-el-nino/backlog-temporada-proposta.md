# Backlog da temporada Super El Niño (proposta, 28/11/2026) — NÃO carregado no banco

Por que não carreguei: `tools/rotinas/backlog.py agendar` (rotina seg/qui) distribui **todo item `proposto`** do Em Relevo nas noites livres (`agendar`, linhas 216–249). Com os 6 temas no banco, eles ganhariam data sozinhos antes da aprovação do Rodrigo. Por isso ficam aqui + em `backlog-temporada.json` (formato do `backlog.py importar`).

| ordem | slug | título favorito | D·E·U | janela |
|---|---|---|---|---|
| sem. 1 | el-nino-pacifico-passou-1997-2015 | O Pacífico passou 1997 e 2015: o que o Super El Niño já faz com o Brasil | 9·9·10 | 15/01/2027 |
| sem. 1 | el-nino-roraima-seca | Super El Niño: por que Roraima seca quando o resto da Amazônia chove | 6·8·9 | 28/02/2027 |
| sem. 2 | el-nino-calor-sudeste | A frente fria que não chega: o Super El Niño no verão do Sudeste | 8·7·9 | 28/02/2027 |
| sem. 2 | el-nino-rio-iguacu | O rio Iguaçu que passou dos 10 metros no El Niño de 1983 | 7·9·8 | 31/01/2027 |
| sem. 3 | el-nino-vai-faltar-luz | Vai faltar luz no Brasil com o Super El Niño? | 6·7·8 | 28/02/2027 |
| sem. 3 | el-nino-sertao-quadra | Por que o Sertão fica sem chuva quando o Pacífico esquenta | 7·8·7 | 31/03/2027 |

**Depois do sim do Rodrigo** (a ordem do brief é 2/semana; a nota sozinha não respeita a ordem acima, então agende à mão com `--data` ou ajuste depois do import):
```
cd ~/workspace/fabrica-youtube
tools/.venv/bin/python tools/rotinas/backlog.py importar canais/em-relevo/temporada-el-nino/backlog-temporada.json --canal em-relevo --fonte "Em Relevo temporada El Niño, proposta 28/11"
# limpar os antigos (decisão do Rodrigo): descartar 28 (Granizo); tirar a data de 30–33; 29 (calor) vira o el-nino-calor-sudeste
tools/.venv/bin/python tools/rotinas/backlog.py descartar 28 --motivo "Em Relevo temporada El Niño (Rodrigo recusou o granizo em 17/11)"
# e pôr em-relevo de volta em CANAIS de ~/.config/fabrica/noturna.env para a noturna produzir (2 noites/semana: ajuste fino é decisão dele)
```
