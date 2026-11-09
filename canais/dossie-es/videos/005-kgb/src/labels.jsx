// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// { t, x, y, size, pin } → rótulo (com pino vermelho em x,y se pin: true; o rótulo fica do lado indicado em "lado")
// { arrow: [x0, y0, x1, y1] } → seta vermelha animada
// Posições medidas na imagem final com grade (qa/mapa-I191.jpg e frame do render qa/mapa-frame.jpg, 09/11/2026).
export const LABELS = {
  // Mundo (arquivo Mitrokhin: a KGB na América Latina)
  map_world: [
    { arrow: [0.577, 0.247, 0.30, 0.725] },
    { t: 'MOSCÚ', x: 0.577, y: 0.247, size: 28, pin: true, lado: 'dir' },
    { t: 'LA HABANA', x: 0.265, y: 0.451, size: 24, pin: true, lado: 'dir' },
    { t: 'CIUDAD DE MÉXICO', x: 0.218, y: 0.450, size: 24, pin: true, lado: 'esq' },
    { t: 'SANTIAGO', x: 0.298, y: 0.73, size: 28, pin: true, lado: 'esq' },
  ],
};
