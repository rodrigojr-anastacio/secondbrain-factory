// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// { t, x, y, size, pin } → rótulo (com pino vermelho em x,y se pin: true; o rótulo fica do lado indicado em "lado")
// { arrow: [x0, y0, x1, y1] } → seta vermelha animada
// 008 La Inquisición: posições medidas com grade nas imagens (qa/grade-*.jpg, 13/11/2026) e conferidas num still do render.
export const LABELS = {
  // Expediente 1 (Toulouse 1323 / Roma 1478)
  map_europa: [
    { t: 'TOULOUSE', x: 0.09, y: 0.23, size: 30, pin: true, lado: 'dir' },
    { t: 'ROMA', x: 0.37, y: 0.42, size: 30, pin: true, lado: 'esq' },
  ],
  // Expediente 6 (Exilio): setas de España hacia Portugal, norte de África, Italia e Imperio otomano
  map_exilio: [
    { arrow: [0.20, 0.38, 0.115, 0.40] },
    { arrow: [0.20, 0.38, 0.30, 0.56] },
    { arrow: [0.20, 0.38, 0.385, 0.25] },
    { arrow: [0.20, 0.38, 0.72, 0.38] },
    { t: 'ESPAÑA', x: 0.20, y: 0.38, size: 28, pin: true, lado: 'baixo' },
    { t: 'PORTUGAL', x: 0.115, y: 0.40, size: 22, pin: true, lado: 'esq' },
    { t: 'NORTE DE ÁFRICA', x: 0.30, y: 0.56, size: 22, pin: true, lado: 'baixo' },
    { t: 'ITALIA', x: 0.385, y: 0.25, size: 22, pin: true, lado: 'dir' },
    { t: 'IMPERIO OTOMANO', x: 0.72, y: 0.38, size: 22, pin: true, lado: 'baixo' },
  ],
  // Expediente 6 e 8: España → Antillas / México
  map_atlantico: [
    { arrow: [0.865, 0.26, 0.375, 0.535] },
    { arrow: [0.865, 0.26, 0.20, 0.47] },
    { t: 'ESPAÑA', x: 0.865, y: 0.26, size: 26, pin: true, lado: 'baixo' },
    { t: 'ANTILLAS', x: 0.375, y: 0.535, size: 24, pin: true, lado: 'baixo' },
    { t: 'MÉXICO', x: 0.20, y: 0.47, size: 24, pin: true, lado: 'baixo' },
  ],
  // Expediente 9 e 14: Lima, Cartagena, Quito, Chile, Río de la Plata
  map_sudamerica: [
    { t: 'CARTAGENA', x: 0.428, y: 0.105, size: 22, pin: true, lado: 'esq' },
    { t: 'QUITO', x: 0.415, y: 0.285, size: 22, pin: true, lado: 'esq' },
    { t: 'LIMA', x: 0.445, y: 0.41, size: 26, pin: true, lado: 'esq' },
    { t: 'CHILE', x: 0.475, y: 0.655, size: 22, pin: true, lado: 'esq' },
    { t: 'RÍO DE LA PLATA', x: 0.556, y: 0.672, size: 22, pin: true, lado: 'dir' },
  ],
};
