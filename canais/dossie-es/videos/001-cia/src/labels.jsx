// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// { t, x, y, size, pin } → rótulo (com pino vermelho em x,y se pin: true; o rótulo fica acima do pino)
// { arrow: [x0, y0, x1, y1] } → seta vermelha animada
// Posições conferidas nas imagens finais com grade de 10% (qa/mapa-I*.jpg, 04/11/2026).
// map_iran: o nano-banana escreveu "ACSPRIN SEA" em (0.55, 0.13); o rótulo MAR CASPIO cobre esse texto de propósito.
export const LABELS = {
  map_americas: [
    { t: 'GUATEMALA', x: 0.395, y: 0.27, size: 34, pin: true },
    { t: 'CUBA', x: 0.475, y: 0.225, size: 34, pin: true, lado: 'dir' },
    { t: 'CHILE', x: 0.49, y: 0.63, size: 34, pin: true, lado: 'esq' },
  ],
  map_atlantic: [
    { arrow: [0.25, 0.52, 0.735, 0.55] },
    { t: 'WASHINGTON', x: 0.235, y: 0.525, size: 32, pin: true },
    { t: 'ROMA', x: 0.748, y: 0.56, size: 36, pin: true },
  ],
  map_iran: [
    { t: 'MAR CASPIO', x: 0.548, y: 0.128, size: 40, fijo: true },
    { t: 'TEHERÁN', x: 0.47, y: 0.44, size: 34, pin: true },
    { t: 'IRÁN', x: 0.56, y: 0.58, size: 52 },
  ],
  map_central: [
    { arrow: [0.375, 0.47, 0.33, 0.45] },
    { t: 'GUATEMALA', x: 0.32, y: 0.45, size: 34, pin: true, lado: 'esq' },
    { t: 'HONDURAS', x: 0.375, y: 0.47, size: 30, pin: true, lado: 'baixo' },
    { t: 'CUBA', x: 0.475, y: 0.37, size: 34, pin: true, lado: 'dir' },
  ],
  map_afghanistan: [
    { arrow: [0.47, 0.25, 0.545, 0.42] },
    { t: 'UNIÓN SOVIÉTICA', x: 0.45, y: 0.2, size: 34 },
    { t: 'AFGANISTÁN', x: 0.545, y: 0.45, size: 38, pin: true, lado: 'baixo' },
    { t: 'PAKISTÁN', x: 0.64, y: 0.62, size: 28 },
  ],
};
