// Rótulos dos mapas, feitos no código (as imagens são geradas sem texto; nano-banana-2.1/edit, 09/11/2026).
// chave da imagem → [{ t: texto, x, y: posição em fração da imagem, size: px a 1x }]
// Posições conferidas na grade das imagens finais (qa/mapas-grade.jpg) e nos stills do render (qa/stills/).
export const LABELS = {
  map_empire_hook: [
    { t: 'ROMA', x: 0.42, y: 0.42, size: 34 },
    { t: 'IMPÉRIO ROMANO', x: 0.5, y: 0.88, size: 46 },
  ],
  map_italy_tiber: [
    { t: 'ROMA', x: 0.47, y: 0.62, size: 40 },
    { t: 'ITÁLIA', x: 0.62, y: 0.33, size: 44 },
  ],
  map_italy_conquest: [
    { t: 'ROMA', x: 0.42, y: 0.46, size: 40 },
    { t: 'ITÁLIA', x: 0.72, y: 0.22, size: 44 },
  ],
  map_carthage: [
    { t: 'ROMA', x: 0.63, y: 0.36, size: 40 },
    { t: 'CARTAGO', x: 0.42, y: 0.9, size: 44 },
  ],
  map_hannibal: [
    { t: 'HISPÂNIA', x: 0.22, y: 0.62, size: 40 },
    { t: 'ALPES', x: 0.6, y: 0.07, size: 38 },
    { t: 'ITÁLIA', x: 0.84, y: 0.36, size: 40 },
  ],
  map_gaul: [
    { t: 'GÁLIA', x: 0.3, y: 0.45, size: 48 },
    { t: 'ITÁLIA', x: 0.74, y: 0.66, size: 40 },
  ],
  map_empire_117: [
    { t: 'IMPÉRIO ROMANO, 117', x: 0.5, y: 0.9, size: 44 },
  ],
  map_split: [
    { t: 'OCIDENTE', x: 0.36, y: 0.47, size: 38 },
    { t: 'ORIENTE', x: 0.72, y: 0.52, size: 38 },
  ],
};
