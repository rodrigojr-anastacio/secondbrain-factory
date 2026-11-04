// Rótulos dos mapas, feitos no código (as imagens são geradas sem texto).
// chave da imagem → [{ t: texto, x, y: posição em fração da imagem, size: px a 1x }]
// Posições conferidas nas imagens finais do fal (grade em qa/mapas-grade.jpg, 04/11/2026).
// map_royal_road e map_caucasus usam cópias de I074 e I130 (o fal escrevia letras falsas nesses mapas).
export const LABELS = {
  map_plateau: [
    { t: 'PLANALTO IRANIANO', x: 0.5, y: 0.84, size: 44 },
  ],
  map_iran_name: [
    { t: 'IRÃ', x: 0.62, y: 0.46, size: 72 },
    { t: 'TERRA DOS ÁRIAS', x: 0.62, y: 0.6, size: 34 },
  ],
  map_pars: [
    { t: 'PARS (FARS)', x: 0.62, y: 0.72, size: 40 },
    { t: 'GOLFO PÉRSICO', x: 0.37, y: 0.9, size: 28 },
  ],
  map_satrapies: [
    { t: 'EGITO', x: 0.33, y: 0.74, size: 34 },
    { t: 'ANATÓLIA', x: 0.38, y: 0.42, size: 32 },
    { t: 'PÉRSIA', x: 0.74, y: 0.52, size: 44 },
    { t: 'ATÉ A ÍNDIA →', x: 0.88, y: 0.66, size: 30 },
  ],
  map_royal_road: [
    { t: 'SARDES', x: 0.3, y: 0.44, size: 36 },
    { t: 'ESTRADA REAL · 2.500 KM', x: 0.52, y: 0.56, size: 32 },
    { t: 'SUSA', x: 0.72, y: 0.64, size: 36 },
  ],
  map_arabic: [
    { t: 'EGITO', x: 0.3, y: 0.86, size: 32 },
    { t: 'SÍRIA', x: 0.5, y: 0.5, size: 30 },
    { t: 'IRAQUE', x: 0.58, y: 0.66, size: 30 },
    { t: 'IRÃ', x: 0.73, y: 0.45, size: 52 },
  ],
  map_shia_sunni: [
    { t: 'IRÃ', x: 0.74, y: 0.36, size: 56 },
    { t: 'IMPÉRIO OTOMANO', x: 0.42, y: 0.14, size: 30 },
  ],
  map_caucasus: [
    { t: 'CÁUCASO', x: 0.6, y: 0.1, size: 38 },
    { t: 'IRÃ', x: 0.74, y: 0.36, size: 46 },
  ],
};
