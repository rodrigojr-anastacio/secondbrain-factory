// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// { t, x, y, size, pin } → rótulo (com pino vermelho em x,y se pin: true; o rótulo fica do lado indicado em "lado")
// { arrow: [x0, y0, x1, y1] } → seta vermelha animada
// Posições medidas nas imagens finais com grade (qa/mapa-I018.jpg e qa/mapa-I104-*.jpg, 05/11/2026).
export const LABELS = {
  // Sicília (1860)
  map_sicily: [
    { t: 'PALERMO', x: 0.40, y: 0.315, size: 32, pin: true, lado: 'esq' },
    { t: 'CORLEONE', x: 0.405, y: 0.43, size: 26, pin: true, lado: 'dir' },
    { t: 'GANGI', x: 0.555, y: 0.37, size: 26, pin: true, lado: 'dir' },
    { t: 'SICILIA', x: 0.62, y: 0.6, size: 40 },
  ],
  // Atlântico (Luciano: Nápoles → La Habana, 1946)
  map_atlantic: [
    { arrow: [0.755, 0.465, 0.18, 0.61] },
    { t: 'NUEVA YORK', x: 0.226, y: 0.425, size: 28, pin: true, lado: 'dir' },
    { t: 'LA HABANA', x: 0.175, y: 0.615, size: 28, pin: true, lado: 'esq' },
    { t: 'NÁPOLES', x: 0.755, y: 0.465, size: 28, pin: true, lado: 'dir' },
    { t: 'SICILIA', x: 0.76, y: 0.53, size: 22 },
  ],
};
