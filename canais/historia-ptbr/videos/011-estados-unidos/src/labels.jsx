// Rótulos dos mapas (010 Japão): imagens geradas sem texto; letras feitas no código.
// POSIÇÕES PROVISÓRIAS (etapa 1, sem imagem): conferir em still de início e fim de cada plano na etapa 2 (qa/mapas-stills.jpg)
// e manter x entre 0,2 e 0,8 (o pan/zoom corta rótulo na borda; lição do 008).
// chave da imagem → [{ t: texto, x, y: fração da imagem, size: px a 1x }]
export const LABELS = {
  map_mongol: [
    { t: 'IMPÉRIO MONGOL', x: 0.45, y: 0.4, size: 36 },
    { t: 'JAPÃO', x: 0.78, y: 0.5, size: 30 },
  ],
  map_japan_sea: [
    { t: 'JAPÃO', x: 0.66, y: 0.45, size: 44 },
    { t: 'COREIA', x: 0.26, y: 0.4, size: 32 },
  ],
  map_crossing: [
    { t: 'COREIA', x: 0.3, y: 0.35, size: 32 },
    { t: 'JAPÃO', x: 0.7, y: 0.6, size: 32 },
  ],
  map_china_japan: [
    { t: 'CHINA', x: 0.35, y: 0.5, size: 44 },
    { t: 'JAPÃO', x: 0.8, y: 0.68, size: 32 },
  ],
  map_korea_route: [
    { t: 'CHINA', x: 0.3, y: 0.5, size: 34 },
    { t: 'COREIA', x: 0.55, y: 0.38, size: 28 },
    { t: 'JAPÃO', x: 0.75, y: 0.5, size: 30 },
  ],
  map_hakata: [
    { t: 'COREIA', x: 0.3, y: 0.3, size: 30 },
    { t: 'KYUSHU', x: 0.65, y: 0.65, size: 30 },
  ],
  map_far: [
    { t: 'EUROPA', x: 0.22, y: 0.35, size: 30 },
    { t: 'JAPÃO', x: 0.78, y: 0.4, size: 30 },
  ],
  map_1905: [{ t: 'IMPÉRIO DO JAPÃO, 1905', x: 0.72, y: 0.45, size: 28 }],
  map_expansion: [{ t: 'IMPÉRIO DO JAPÃO', x: 0.7, y: 0.5, size: 28 }],
  pacific_map: [{ t: 'OCEANO PACÍFICO', x: 0.6, y: 0.65, size: 30 }],
};
