# Chuva NASA (GPM IMERG): teste real da `tools/nasa_chuva.py` (16/11/2026)

Comando (≈ 1 min 45 s na 1ª vez; 12 s com cache):
```
tools/.venv/bin/python tools/nasa_chuva.py --inicio 2024-04-27 --fim 2024-05-05 --regiao RS \
  --saida canais/em-relevo/amostras-nasa --nome enchente-rs-2024 --anomalia
```
| Arquivo | O que é |
|---|---|
| `enchente-rs-2024-tela.png` | 1920×1080 pronto: chuva acumulada 27/04–05/05/2024, UFs (IBGE) e vizinhos (Natural Earth), legenda em mm e período |
| `enchente-rs-2024-camada.png` (+ `.pgw`) | camada RGBA transparente, sem texto, 2048 px, em lon/lat no bbox do JSON, para pôr sobre o terreno 3D |
| `enchente-rs-2024-anomalia-tela.png` / `-anomalia-camada.png` | diferença da média 2001–2020 (IMERG mensal) |
| `enchente-rs-2024.json` | bbox, período, arquivos do GES DISC, números, escala de cor e linha de crédito |

**Números (IMERG Final V07, 9 dias):** máximo em terra **620 mm** em 29,05°S 51,45°W (serra gaúcha, entre Caxias do Sul e o vale do Taquari). Média no RS **308 mm**, contra ~43 mm esperados para esses dias: **~710% da média** no estado. O máximo do recorte (743 mm) fica **no mar**, a leste do litoral norte, e por isso o JSON separa `max` de `max_terra`.
**Cuidado ao narrar:** IMERG é estimativa de satélite em células de ~10 km, ajustada por pluviômetros. Fica abaixo das estações nos picos (Caxias: 707 mm em 13 dias no INMET; o WWA dá > 420 mm de média no estado entre 24/04 e 04/05, em outro período). Na tela, use o número do IMERG como "satélite da NASA"; o número da estação vem do INMET.
Crédito na descrição: "Chuva: NASA GPM IMERG (GES DISC), domínio público".
