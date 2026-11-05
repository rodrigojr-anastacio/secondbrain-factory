// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// { t, x, y, size, pin } → rótulo (com pino vermelho em x,y se pin: true; o rótulo fica acima do pino)
// { arrow: [x0, y0, x1, y1] } → seta vermelha animada
// Posições conferidas nas imagens finais com grade de 10% (qa/mapa-I*.jpg, 05/11/2026).
// map_middleeast: o nano-banana escreveu "Egypt" em (0.14, 0.84); o rótulo EGIPTO cobre esse texto de propósito.
export const LABELS = {
  map_middleeast: [
    { arrow: [0.605, 0.52, 0.45, 0.6] },
    { t: 'EGIPTO', x: 0.145, y: 0.84, size: 34, fijo: true },
    { t: 'IRAK', x: 0.61, y: 0.52, size: 36, pin: true, lado: 'dir' },
    { t: 'ISRAEL', x: 0.44, y: 0.61, size: 34, pin: true, lado: 'esq' },
    { t: 'JORDANIA', x: 0.55, y: 0.63, size: 26 },
  ],
  map_southamerica: [
    { t: 'SÃO PAULO', x: 0.665, y: 0.465, size: 30, pin: true, lado: 'dir' },
    { t: 'BUENOS AIRES', x: 0.535, y: 0.6, size: 30, pin: true, lado: 'esq' },
    { t: 'MONTEVIDEO', x: 0.565, y: 0.59, size: 30, pin: true, lado: 'dir' },
  ],
  map_europe: [
    { t: 'LILLEHAMMER', x: 0.43, y: 0.19, size: 30, pin: true, lado: 'dir' },
    { t: 'PARÍS', x: 0.36, y: 0.48, size: 30, pin: true, lado: 'esq' },
    { t: 'MÚNICH', x: 0.43, y: 0.52, size: 30, pin: true, lado: 'dir' },
    { t: 'ROMA', x: 0.45, y: 0.64, size: 30, pin: true, lado: 'baixo' },
    { t: 'BEIRUT', x: 0.7, y: 0.785, size: 30, pin: true, lado: 'dir' },
  ],
  map_redsea: [
    { arrow: [0.548, 0.62, 0.505, 0.34] },
    { t: 'ISRAEL', x: 0.505, y: 0.33, size: 32, pin: true, lado: 'esq' },
    { t: 'SUDÁN', x: 0.36, y: 0.62, size: 40 },
    { t: 'AROUS', x: 0.548, y: 0.62, size: 30, pin: true, lado: 'esq' },
    { t: 'ETIOPÍA', x: 0.5, y: 0.9, size: 34 },
  ],
};
