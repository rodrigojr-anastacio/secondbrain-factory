// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// Chave `chave:bloco` (variante por uso) ou só `chave`. { t, x, y, size, pin, lado } rótulo com pino; { arrow: [x0,y0,x1,y1] } seta.
// 010 Cártel de Medellín: posições medidas com grade na base I023 (map_caribe), 16/11/2026; y em fração da altura da imagem.
export const LABELS = {
  // Exp. 1: avionetas de Medellín rumo a Florida
  'map_caribe:N009': [
    { arrow: [0.49, 0.535, 0.447, 0.195] },
    { t: 'MEDELLÍN', x: 0.49, y: 0.535, size: 28, pin: true, lado: 'dir' },
    { t: 'FLORIDA', x: 0.447, y: 0.195, size: 28, pin: true, lado: 'dir' },
  ],
};
export const labelsDe = (s) => LABELS[`${s.chave}:${s.bloco}`] || LABELS[s.chave] || [];
