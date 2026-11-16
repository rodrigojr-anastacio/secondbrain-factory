// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// Chave `chave:bloco` (variante por uso) ou só `chave`. { t, x, y, size, pin, lado } rótulo com pino; { arrow: [x0,y0,x1,y1] } seta.
// 009 La Gestapo: posições medidas com grade nas bases I075 (mundo) e I088 (Europa), 15/11/2026; y em fração da altura da imagem.
export const LABELS = {
  // Exp. 4: Río de Janeiro → Hamburgo
  'map_atlantico:N029': [
    { arrow: [0.405, 0.675, 0.60, 0.22] },
    { t: 'RÍO DE JANEIRO', x: 0.405, y: 0.675, size: 26, pin: true, lado: 'esq' },
    { t: 'HAMBURGO', x: 0.60, y: 0.22, size: 26, pin: true, lado: 'dir' },
  ],
  // Exp. 11: Génova → Buenos Aires → La Paz
  'map_atlantico:N079': [
    { arrow: [0.585, 0.285, 0.365, 0.75] },
    { arrow: [0.365, 0.75, 0.338, 0.645] },
    { t: 'GÉNOVA', x: 0.585, y: 0.285, size: 24, pin: true, lado: 'esq' },
    { t: 'BUENOS AIRES', x: 0.365, y: 0.75, size: 24, pin: true, lado: 'dir' },
    { t: 'LA PAZ', x: 0.338, y: 0.645, size: 24, pin: true, lado: 'esq' },
  ],
  // Fim do exp. 4 / exp. 5: só Berlín
  'map_europa:N037': [
    { t: 'BERLÍN', x: 0.445, y: 0.455, size: 30, pin: true, lado: 'dir' },
  ],
  // Exp. 6: Francia, Bélgica y Holanda → Alemania
  'map_europa:N047': [
    { arrow: [0.30, 0.52, 0.43, 0.44] },
    { arrow: [0.36, 0.445, 0.43, 0.43] },
    { arrow: [0.355, 0.385, 0.43, 0.42] },
    { t: 'FRANCIA', x: 0.30, y: 0.52, size: 22, pin: true, lado: 'esq' },
    { t: 'BÉLGICA', x: 0.36, y: 0.445, size: 20, pin: true, lado: 'esq' },
    { t: 'HOLANDA', x: 0.355, y: 0.385, size: 20, pin: true, lado: 'esq' },
    { t: 'ALEMANIA', x: 0.43, y: 0.44, size: 26, pin: true, lado: 'dir' },
  ],
};
export const labelsDe = (s) => LABELS[`${s.chave}:${s.bloco}`] || LABELS[s.chave] || [];
