# Backlog vivo: Em Relevo, carga inicial (14/11/2026)

8 temas para as próximas 2 semanas. O detalhe de cada um (ângulo, título candidato, evidências com link, riscos) está em `em-relevo.json`. Custo: US$ 0. Nenhuma chamada a `search.list`.

| # | Tema | D | E | U | Nota | Janela | Evidência principal |
|---|---|---|---|---|---|---|---|
| 1 | Enchente de 2024: por que Porto Alegre ficou debaixo d'água | 9 | 9 | 6 | **7,9** | 31/12 | busca "enchente rio grande do sul 2024": mediana 326 mil, 11 vídeos ≥ 100 mil; previsão de chuva acima da média no Sul em OND |
| 2 | Caraguatatuba 1967: a serra que desceu sobre a cidade | 8 | 10 | 5 | **7,4** | 31/03/27 | AntigamenteBR 2,0 mi (28/08); Histórias da Tragédia 244 mil em 11 dias |
| 3 | Granizo e as tempestades gigantes da Bacia do Prata | 7 | 7 | 8 | **7,3** | 15/12 | Natureza em Fúria 633 mil e UOL 318 mil (27/09); temporada de temporais ativa |
| 4 | O calor do verão do Super El Niño, no mapa | 7 | 6 | 8 | **7,0** | 31/12 | Band 337 mil (26/09); Defesa Civil prevê excesso de calor de novembro a janeiro |
| 5 | O litoral do RS: 600 km de praia reta | 8 | 8 | 5 | **6,8** | 15/12 | Capital Financeiro 1,38 mi; o Chão do Sul publicou o tema hoje (14/11) |
| 6 | Neve no Brasil: por que só o Sul tem | 8 | 9 | 4 | **6,6** | perene | Urupema 1,05 mi; busca: mediana 66 mil; MetSul "geada em novembro" 157 mil |
| 7 | Os cânions do Sul (Aparados da Serra) | 6 | 10 | 4 | **6,2** | perene | busca "cânions do sul": mediana 57 mil, 5 vídeos ≥ 100 mil |
| 8 | Geada negra de 1975 e o mapa do café | 6 | 8 | 4 | **5,8** | perene | AntigamenteBR 418 mil em ~1 mês |

D = demanda, E = encaixe, U = urgência. Nota = (D × E × U)^(1/3).

## Método
- **Referências e vizinhos:** últimos 20 vídeos de Mundo Entrópico, Chão do Sul, Explica no Mapa, Além do Mapa, AntigamenteBR, Um Documentário, MetSul, Natureza Sinistra, entender.brasil, Mapa Verso e Canal Top10, via `yt-dlp --flat-playlist` (WARP, 14/11). As datas desses vídeos são aproximadas (`approximate_date`). As datas das evidências vieram do metadado completo de cada vídeo.
- **Concorrentes e demanda:** 18 buscas `ytsearch20` (WARP), mais o `demanda-temas.json` do gap de 14/11 (mediana dos longos no top-15) e o Google Trends de `canal-clima-2026-11/dados/gtrends.json`. A tabela `youtube.palavras_chave` não tem nenhum termo de clima com mediana validada: o destino é só `historia-ptbr` ou `novo-canal`. Não serviu.
- **Notícias:** INMET, CPTEC, Climatempo, Agência Gov, MetSul, Jornal do Comércio e IstoÉ. O El Niño está "muito forte", com pico provável em dezembro. A previsão é de chuva acima da média no Sul e de excesso de calor na maior parte do país de novembro a janeiro. Não achei alerta vigente para 13–14/11.
- **Nossos números** (`youtube.studio_video`, 17/10–13/11): Sul tem 15 views, 184 impressões e CTR de 2,72%. El Niño tem 14 views, 179 impressões e CTR de 1,68%. São os dois títulos de notícia/sim-ou-não. `metricas_video` e Analytics ainda não têm dados do canal. Isso reforça a conclusão do gap: busca perene e lugar como protagonista, não notícia.
- **Encaixe:** o tema precisa render mapa 3D ou satélite de fonte livre (NASA, NOAA, GOES, Copernicus, SRTM) e foto real com licença, sem TV e sem IA de cena. Também conta a regra de política: nada de "morte" no título e nenhuma vítima na thumb.
- **Urgência:** evergreen recebeu 3–4. Tema com janela de estação ou de notícia em nov–dez recebeu 5–8.

## O que ficou de fora e por quê
- **Furacão Catarina (2004):** a demanda existe (Manual do Mundo, "Por que não tem furacão no Brasil?", 2,58 mi; Climatempo 581 mil), mas a busca do tema tem mediana de só 22 mil. O sinal recente é negativo: a AntigamenteBR publicou o Catarina em 09/11 e tem **315 views** em 5 dias, enquanto os outros vídeos do canal fazem 7–418 mil. Nota estimada ~5,7. Volta se surgir um gancho de notícia.
- **"Por que o Sul escapou de virar deserto" / rios voadores:** o Explica no Mapa publicou em 07/11 e tem só 12,6 mil. O tema também sobrepõe a thumb do Sul ("rio de umidade" + Andes). Nota ~5,5.
- **Seca na Amazônia / Rio Negro e queimadas:** o pico passou em outubro. A nota técnica do governo prevê a seca forte para o verão e o outono de 2027, fora da janela de 2 semanas.
- **El Niño panorama e La Niña:** já feito (12/11) e saturado pelos grandes (Jubilut 5,9 mi, Manual do Mundo 3,5 mi).
- **Ciclone bomba e tornados:** o vídeo de 11/11 já cobre. A busca "ciclone bomba sul" só devolve TV.
- **Pantanal e Lençóis Maranhenses:** a busca é dominada por turismo e vida selvagem, e nenhum vizinho tem hit recente com eles. O Além do Mapa fez 10 mil com os Lençóis em 14/11.

## Limitações
- Os títulos que o yt-dlp devolve pelo WARP às vezes vêm traduzidos para o inglês. Os títulos citados no JSON vieram do metadado completo (original em pt).
- As views do 1º dia (Chão do Sul, 14/11) ainda não indicam desempenho. Servem só como sinal de que o vizinho está no tema agora.
- As datas marcadas "~" nas evidências são aproximadas (lista do canal).
- Todos os hooks estão marcados [I, conferir]: nenhum número foi checado na fonte primária.
