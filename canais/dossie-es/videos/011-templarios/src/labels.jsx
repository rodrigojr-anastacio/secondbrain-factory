// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// Chave `chave:bloco` (variante por uso) ou só `chave`. { t, x, y, size, pin, lado } rótulo com pino; { arrow: [x0,y0,x1,y1] } seta.
// 011 Templarios: posições medidas com grade nas bases I030 (map_iberia), I123 (map_holyland), I193 (map_atlantic), 17/11/2026; y em fração da altura.
export const LABELS = {
  // Exp. 2: o Hábito, Barcelona → Monzón
  'map_iberia:N009': [
    { arrow: [0.60, 0.52, 0.555, 0.495] },
    { t: 'BARCELONA', x: 0.60, y: 0.52, size: 28, pin: true, lado: 'dir' },
    { t: 'MONZÓN', x: 0.555, y: 0.495, size: 28, pin: true, lado: 'esq' },
  ],
  // Exp. 11: Monzón pasa a los hospitalarios
  'map_iberia:N051': [
    { t: 'MONZÓN', x: 0.555, y: 0.495, size: 28, pin: true, lado: 'esq' },
  ],
  // Exp. 7: Acre cae (1291)
  'map_holyland:N036': [
    { t: 'ACRE', x: 0.522, y: 0.645, size: 28, pin: true, lado: 'esq' },
    { t: 'JERUSALÉN', x: 0.531, y: 0.685, size: 28, pin: true, lado: 'dir' },
  ],
  // Exp. 12: de Lisboa a Brasil, 1500
  'map_atlantic:N061': [
    { arrow: [0.527, 0.154, 0.388, 0.573] },
    { t: 'LISBOA', x: 0.527, y: 0.154, size: 28, pin: true, lado: 'dir' },
    { t: 'BRASIL', x: 0.388, y: 0.573, size: 28, pin: true, lado: 'esq' },
  ],
};
export const labelsDe = (s) => LABELS[`${s.chave}:${s.bloco}`] || LABELS[s.chave] || [];
