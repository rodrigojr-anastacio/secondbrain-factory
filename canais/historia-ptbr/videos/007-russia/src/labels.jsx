// Rótulos dos mapas, feitos no código (as imagens são geradas sem texto; nano-banana-2.1/edit, 09/11/2026).
// chave da imagem → [{ t: texto, x, y: posição em fração da imagem, size: px a 1x }]
// Posições conferidas na grade das imagens finais (qa/mapas-grade*.jpg) e nos stills do render (qa/stills/).
export const LABELS = {
  map_sea_route: [
    { t: 'ESCANDINÁVIA', x: 0.22, y: 0.3, size: 38 },
    { t: 'TERRA DOS ESLAVOS', x: 0.74, y: 0.62, size: 38 },
  ],
  map_russia_hook: [
    { t: 'RÚSSIA', x: 0.55, y: 0.44, size: 56 },
  ],
  map_rivers: [
    { t: 'MAR BÁLTICO', x: 0.45, y: 0.08, size: 34 },
    { t: 'MAR NEGRO', x: 0.91, y: 0.8, size: 30 },
  ],
  map_kievan_rus: [
    { t: 'RUS DE KIEV', x: 0.47, y: 0.42, size: 46 },
    { t: 'MAR NEGRO', x: 0.88, y: 0.76, size: 30 },
  ],
  map_neighbors: [
    { t: 'RUS', x: 0.62, y: 0.25, size: 44 },
    { t: 'BIZÂNCIO', x: 0.55, y: 0.6, size: 38 },
    { t: 'MUNDO ISLÂMICO', x: 0.5, y: 0.92, size: 34 },
  ],
  map_mongols: [
    { t: 'IMPÉRIO MONGOL', x: 0.62, y: 0.47, size: 46 },
    { t: 'RUS', x: 0.12, y: 0.36, size: 38 },
  ],
  map_moscow_threats: [
    { t: 'MOSCOU', x: 0.5, y: 0.41, size: 40 },
  ],
  map_siberia: [
    { t: 'SIBÉRIA', x: 0.5, y: 0.34, size: 50 },
    { t: 'PACÍFICO', x: 0.86, y: 0.56, size: 28 },
  ],
  map_poland: [
    { t: 'POLÔNIA', x: 0.53, y: 0.31, size: 40 },
  ],
  map_napoleon: [
    { t: 'PARIS', x: 0.22, y: 0.43, size: 36 },
    { t: 'MOSCOU', x: 0.84, y: 0.36, size: 36 },
  ],
  map_ussr: [
    { t: 'UNIÃO SOVIÉTICA', x: 0.62, y: 0.42, size: 50 },
  ],
  map_15: [
    { t: 'RÚSSIA', x: 0.6, y: 0.33, size: 52 },
    { t: '1991: 15 PAÍSES', x: 0.5, y: 0.9, size: 44 },
  ],
};
