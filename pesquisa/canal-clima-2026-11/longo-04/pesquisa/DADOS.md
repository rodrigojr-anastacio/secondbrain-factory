# Dados do longo 04 (todos baixados em 13/11/2026; domínio público / dado oficial aberto)

| Arquivo | O que é | Fonte | Uso |
|---|---|---|---|
| `dados/iguacu-uv-1982-83.json` | cota diária do Iguaçu em União da Vitória, out/1982–set/1983 (m), picos, linha de 6 m, níveis nas datas Landsat | ANA HidroWeb, estação 65310000 | hidrograma em relevo (b09–b11, b29), régua do hook (b01) |
| `dados/ana_65310000_cota.json` | bruto 1982–1984 (cm) | ANA (`shared/baixa_ana.py 65310000 1 …`) | — |
| `dados/mombaca-anual.json` | chuva anual de Mombaça (CE) 1911–2024 (70 anos completos), média 783 mm; 1983 = 366 mm (0,47) | ANA HidroWeb, estação 00539001 (DNOCS) | régua de montanhas (b18, b23), pluviômetro (b03) |
| `dados/ana_539001_chuva.json` | bruto diário (mm) | ANA | — |
| `dados/roni.txt`, `dados/oni.txt` | índices RONI e ONI trimestrais 1950–2026 | NOAA CPC | montanhas (b25), onda mensal (b27, b29) |
| `dados/cpc-ensodisc-2026-11-12.html` | boletim ENSO de 12/11/2026 (cópia) | NOAA CPC | b34, b36 |
| `../longo-03/dados/semiarido.json`, `nino34-*.csv`, `sst_comparativo*.json` | semiárido oficial, Niño 3.4 e relevo de calor 2026 | ver `../longo-03/pesquisa/DADOS.md` | b20, b33 |

Números-chave: Iguaçu UV 03/07/83 4,94 m → 18/07/83 10,42 m; > 6 m de 08/07 a 10/08 (34 dias); 56 dias > 6 m em 1983; nov/82 6,45 m; jun/83 6,65 m; 04/08/83 7,42 m. Mombaça 1981 472 · 1982 407 · 1983 366 · 1984 792 mm. RONI DJF 1983 +2,40 (máx. 1950–2026), MJJ 1983 +0,47; RONI ASO 2026 +1,97; ONI ASO 2026 +2,46. Distâncias: UV–Mombaça 2.582 km; UV–Blumenau 214 km.

A estação ANA de Blumenau (83900000) usa outro zero de régua (pico 7,04 m em 1983): **não usar**; a régua da cidade é a da Defesa Civil (15,34 m).
Satélite: `tools/landsat_par.py` recorta a mesma janela (72 × 40 km, centro -26,235/-51,075) das cenas Landsat 4 MSS do bucket público `gcp-public-data-landsat` (bandas em `dl/sat_bandas/`, fora do git). Saídas: `dl/fotos/satelite/landsat4-uv-19830703-par.jpg` e `-19830804-par.jpg` (copiadas para `dl/fotos/video/`).
