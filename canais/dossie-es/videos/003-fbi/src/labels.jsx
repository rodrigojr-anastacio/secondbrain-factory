// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// { t, x, y, size, pin } → rótulo (com pino vermelho em x,y se pin: true; o rótulo fica do lado indicado em "lado")
// { arrow: [x0, y0, x1, y1] } → seta vermelha animada
// Posições conferidas nas imagens finais com grade de 10% (qa/mapa-I086.jpg e qa/mapa-I155.jpg, 05/11/2026).
export const LABELS = {
  // América Latina (Servicio de Inteligencia Especial, 1940–1946)
  map_latam: [
    { t: 'MÉXICO', x: 0.36, y: 0.17, size: 30, pin: true, lado: 'esq' },
    { t: 'RÍO DE JANEIRO', x: 0.68, y: 0.6, size: 28, pin: true, lado: 'dir' },
    { t: 'BUENOS AIRES', x: 0.6, y: 0.705, size: 28, pin: true, lado: 'dir' },
    { t: 'SANTIAGO', x: 0.527, y: 0.7, size: 28, pin: true, lado: 'esq' },
  ],
  // México (caso Camarena, 1985)
  map_mexico: [
    { arrow: [0.375, 0.6, 0.69, 0.2] },
    { t: 'WASHINGTON', x: 0.69, y: 0.19, size: 30, pin: true, lado: 'dir' },
    { t: 'GUADALAJARA', x: 0.375, y: 0.6, size: 30, pin: true, lado: 'esq' },
    { t: 'MICHOACÁN', x: 0.44, y: 0.7, size: 26 },
  ],
};
