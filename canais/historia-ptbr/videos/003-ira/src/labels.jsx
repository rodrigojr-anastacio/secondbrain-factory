// Rótulos dos mapas, feitos no código (as imagens são geradas sem texto).
// chave da imagem → [{ t: texto, x, y: posição em fração da imagem, size: px a 1x }]
// Posições estimadas pelo prompt; conferir na imagem gerada (etapa 2) e ajustar.
export const LABELS = {
  map_plateau: [
    { t: 'PLANALTO IRANIANO', x: 0.5, y: 0.5, size: 44 },
    { t: 'ZAGROS', x: 0.28, y: 0.55, size: 30 },
    { t: 'ALBORZ', x: 0.5, y: 0.24, size: 30 },
    { t: 'MAR CÁSPIO', x: 0.48, y: 0.08, size: 30 },
    { t: 'GOLFO PÉRSICO', x: 0.42, y: 0.88, size: 30 },
  ],
  map_iran_name: [
    { t: 'IRÃ', x: 0.5, y: 0.48, size: 72 },
    { t: 'TERRA DOS ÁRIAS', x: 0.5, y: 0.6, size: 34 },
  ],
  map_pars: [
    { t: 'PARS (FARS)', x: 0.46, y: 0.72, size: 40 },
    { t: 'GOLFO PÉRSICO', x: 0.36, y: 0.88, size: 28 },
  ],
  map_satrapies: [
    { t: 'EGITO', x: 0.12, y: 0.62, size: 34 },
    { t: 'ANATÓLIA', x: 0.18, y: 0.3, size: 32 },
    { t: 'PÉRSIA', x: 0.58, y: 0.5, size: 44 },
    { t: 'ÍNDIA', x: 0.9, y: 0.52, size: 34 },
  ],
  map_royal_road: [
    { t: 'SARDES', x: 0.1, y: 0.36, size: 36 },
    { t: 'ESTRADA REAL', x: 0.48, y: 0.3, size: 32 },
    { t: 'SUSA', x: 0.88, y: 0.62, size: 36 },
  ],
  map_arabic: [
    { t: 'EGITO', x: 0.36, y: 0.58, size: 32 },
    { t: 'SÍRIA', x: 0.52, y: 0.38, size: 30 },
    { t: 'IRAQUE', x: 0.62, y: 0.45, size: 30 },
    { t: 'IRÃ', x: 0.8, y: 0.45, size: 52 },
  ],
  map_shia_sunni: [
    { t: 'IRÃ', x: 0.66, y: 0.46, size: 56 },
    { t: 'IMPÉRIO OTOMANO', x: 0.28, y: 0.3, size: 30 },
  ],
  map_caucasus: [
    { t: 'MAR NEGRO', x: 0.14, y: 0.36, size: 30 },
    { t: 'CÁUCASO', x: 0.46, y: 0.42, size: 38 },
    { t: 'MAR CÁSPIO', x: 0.84, y: 0.5, size: 30 },
    { t: 'IRÃ', x: 0.56, y: 0.86, size: 46 },
  ],
};
