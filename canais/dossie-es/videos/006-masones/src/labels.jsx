// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// { t, x, y, size, pin } → rótulo (com pino vermelho em x,y se pin: true; o rótulo fica do lado indicado em "lado")
// { arrow: [x0, y0, x1, y1] } → seta vermelha animada
// Posições medidas na imagem com grade (qa/mapa-grade.jpg, 09/11/2026) e conferidas num still do render.
export const LABELS = {
  // Expediente 7 (La Fragata): a George Canning sai de Londres e chega a Buenos Aires em 1812; Cádiz (onde San Martín serviu) e Santiago (O'Higgins)
  map_lautaro: [
    { arrow: [0.469, 0.198, 0.30, 0.70] },
    { t: 'LONDRES', x: 0.469, y: 0.198, size: 28, pin: true, lado: 'dir' },
    { t: 'CÁDIZ', x: 0.452, y: 0.30, size: 24, pin: true, lado: 'dir' },
    { t: 'BUENOS AIRES', x: 0.298, y: 0.70, size: 28, pin: true, lado: 'dir' },
    { t: 'SANTIAGO', x: 0.247, y: 0.71, size: 24, pin: true, lado: 'esq' },
  ],
};
