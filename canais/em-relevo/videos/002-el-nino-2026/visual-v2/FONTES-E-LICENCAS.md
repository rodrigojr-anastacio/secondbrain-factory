# Fontes e licenças do visual v2 (mapa)

| Uso | Fonte | Licença | Como baixamos |
|---|---|---|---|
| Cor do estilo A; tom da vegetação no estilo B | **NASA Blue Marble Next Generation** (500 m) | domínio público (NASA) | NASA GIBS WMS, camada `BlueMarble_NextGeneration` (`codigo/baixa_bases.py`) |
| Altura (deslocamento 3D) e relevo sombreado dos 3 estilos; batimetria | **NOAA NCEI ETOPO 2022** (60 arc-sec, superfície) | domínio público (governo dos EUA) | OPeNDAP do THREDDS da NOAA (`ETOPO_2022_v1_60s_N90W180_surface.nc`), recortes com passo de 2′ (Brasil) e 6′ (continente e Pacífico) |
| Rios e lagos desenhados na textura | **Natural Earth** 10 m (`rivers_lake_centerlines`, `lakes`) | domínio público | GitHub `nvkelso/natural-earth-vector` |
| Fronteiras de países e UFs, municípios (os mesmos do vídeo atual) | Natural Earth e IBGE (malhas) | domínio público / livre com crédito | já estavam em `dados/` |

Também baixamos a camada `BlueMarble_ShadedRelief_Bathymetry` (GIBS, domínio público), mas não a usamos: o oceano é gerado do ETOPO.

**Crédito na tela (canto inferior direito, sempre que o 3D aparece):**
- fase 2 (vídeo final, mistura A/B; o crédito troca junto com a textura):
  - A: `MAPA: NASA BLUE MARBLE · RELEVO: NOAA ETOPO 2022 · LIMITES: IBGE / NATURAL EARTH`
  - B: `RELEVO: NOAA ETOPO 2022 · COR: NASA BLUE MARBLE · RIOS E LIMITES: NATURAL EARTH / IBGE`
- (fase 1, amostras: A `MAPA: NASA BLUE MARBLE · RELEVO: NOAA ETOPO 2022`; B/C `RELEVO: NOAA ETOPO 2022 · NATURAL EARTH · IBGE`)
- Fase 2: o recorte do Pacífico passou a 85°E–310°E × 45°S–65°N (`codigo/baixa_bases.py`, `codigo/gera_texturas.py`; `REGIOES=pac python3 gera_texturas.py A B`).

**Na descrição (fase 2):** "Mapa: NASA Blue Marble (GIBS) e NOAA ETOPO 2022 (domínio público); rios: Natural Earth."

As texturas (`remotion/public/v2/`, ~60 MB) e os dados brutos (`work/v2/`) ficam fora do git. Para recriar: `codigo/baixa_bases.py` e depois `codigo/gera_texturas.py`.

Os vídeos de referência (GeoGlobeTales, HistóriAtenta) foram usados só para análise (`work/refs/`, fora do git). Nada deles entra no vídeo.
