# Calibragem do detector de cópia (`tools/similaridade_roteiro.py`) · 16/11/2026

Pedido do Rodrigo (16/11/2026): o 005-brasil e o "A HISTÓRIA INTEIRA do Brasil em 13 minutos" (History Easy Guide, `sD0cIJ8JMYw`) têm roteiro praticamente igual, porque os dois remodelaram o History in Minutes (`Vug2cLY3nxk`). O detector tem de chamar isso de cópia e deixar passar um roteiro com ângulo próprio.

## Como mede
- Referência em outro idioma → traduzida para o idioma do roteiro (Claude Haiku, chave `qa`, cache em `~/cache/similaridade/`; custo total desta calibragem + auditoria: **US$ 0,13**, registrado em `financas.consumo` como `preqa:similaridade-traducao`).
- Normalização: minúsculas, sem acento, sem palavras vazias, radical = 5 letras, números por extenso → dígitos.
- Cada bloco do roteiro × janelas de tamanho igual da referência (TF-IDF, cosseno). **Gêmeo** = cosseno ≥ 0,30.
- `nota = 100 × (0,55 × cobertura + 0,25 × cobertura × ordem + 0,20 × min(1, 4 × trigramas))`; vale a maior nota entre as referências.

## Casos
| Roteiro | Referência | Relação real | cobertura | ordem | trigramas | **nota** |
|---|---|---|---|---|---|---|
| 005-brasil | History in Minutes `Vug2cLY3nxk` (en→pt) | cópia (remodelado, bíblia v1) | 51% | 96% | 8,4% | **47** |
| 005-brasil | History Easy Guide `sD0cIJ8JMYw` (pt) | cópia indireta (os dois do HiM) | 45% | 78% | 5,5% | **38** |
| 005-brasil | Canal Nostalgia `q7E4XrfGGnE` (pt, 11 mil palavras) | mesmo tema, independente | 15% | 87% | 1,9% | 13 |
| 005-brasil | Overly Sarcastic `W9tBXt1YZ_w` (en→pt) | mesmo tema, independente | 6% | 83% | 0,0% | 4 |
| 005-brasil | Knowledgia `rqT51lU1IJw` (pt) | mesmo tema, independente | 4% | 75% | 0,4% | 3 |
| 005-brasil | HiM Irã `XVwr1Rm_9jc` | tema diferente, mesmo molde | 1% | – | 0,0% | 0,5 |
| transcrição HEG (`--texto`) | HiM Brasil | cópia indireta, transcrição × transcrição | 28% | 93% | 3,7% | 25 |
| transcrição Knowledgia (`--texto`) | HiM / Overly / Nostalgia | independentes entre si | ≤ 6% | – | ≤ 0,7% | ≤ 5 |
| 006-roma (v2) | AVM queda `RDmf1C7xXv0` | referência só de forma | 5% | 33% | 0,1% | 3 |

Leitura: cópia = **muitos gêmeos na mesma ordem** (≥ 30% dos blocos, ordem ≥ 75%); independente do mesmo tema = gêmeos isolados (fatos obrigatórios: Cabral, café com leite) com cobertura ≤ 15%. Transcrição × transcrição (`--texto`, blocos cortados a cada 35 palavras de legenda automática) mede ~35% abaixo do roteiro real: serve só para comparar concorrentes entre si.

## Limites adotados (em `LIMITES` no script)
- **CÓPIA ≥ 30** (reprova; volta para reescrita): pega os dois casos conhecidos (47 e 38) com folga sobre o maior independente (13).
- **Atenção 18–29** (passa, mas o crivo de ângulo lê os trechos): faixa do 008-franca e do 007-ss (28), ver `AUDITORIA.md`.
- **ok < 18**.
- Revisar os limites depois de ~10 roteiros escritos com a regra nova (**Hipótese**: um roteiro com ângulo próprio fica < 15).
