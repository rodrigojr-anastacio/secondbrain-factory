// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// { t, x, y, size, pin } → rótulo (com pino vermelho em x,y se pin: true; o rótulo fica do lado indicado em "lado")
// { arrow: [x0, y0, x1, y1] } → seta vermelha animada
// Posições medidas na imagem com grade (qa/mapa-grade.jpg, 13/11/2026) e conferidas num still do render.
export const LABELS = {
  // Expediente 13 (El Pasaporte): Génova → Buenos Aires (Mengele, 1949); Asunción e São Paulo (Mengele), Santiago (Rauff), La Paz (Barbie)
  map_ruta: [
    { arrow: [0.637, 0.205, 0.352, 0.765] },
    { t: 'GÉNOVA', x: 0.637, y: 0.205, size: 28, pin: true, lado: 'dir' },
    { t: 'BUENOS AIRES', x: 0.352, y: 0.765, size: 28, pin: true, lado: 'dir' },
    { t: 'ASUNCIÓN', x: 0.345, y: 0.70, size: 22, pin: true, lado: 'esq' },
    { t: 'SÃO PAULO', x: 0.405, y: 0.678, size: 22, pin: true, lado: 'dir' },
    { t: 'SANTIAGO', x: 0.300, y: 0.755, size: 22, pin: true, lado: 'esq' },
    { t: 'LA PAZ', x: 0.300, y: 0.630, size: 22, pin: true, lado: 'esq' },
  ],
};
