// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// Chave `chave:bloco` (variante por uso) ou só `chave`. { t, x, y, size, pin, lado } rótulo com pino; { arrow: [x0,y0,x1,y1] } seta.
// 012 MI6: posições medidas com grade nas bases I005 (map_14), I035 (map_americas), I081 (map_atlantic), I163 (map_south), 18/11/2026; y em fração da altura.
export const LABELS = {
  // N002: o mapa de Roosevelt, o canal de Panamá
  'map_14:N002': [
    { t: 'PANAMÁ', x: 0.385, y: 0.215, size: 28, pin: true, lado: 'esq' },
  ],
  // Exp. 2: o telegrama de Zimmermann (1917), México
  'map_americas:N009': [
    { t: 'TEXAS', x: 0.43, y: 0.2, size: 28, pin: true, lado: 'dir' },
    { t: 'CIUDAD DE MÉXICO', x: 0.51, y: 0.66, size: 28, pin: true, lado: 'dir' },
  ],
  // N023: papéis que cruzam o Atlântico passam por uma ilha (Bermudas)
  'map_atlantic:N023': [
    { arrow: [0.30, 0.43, 0.476, 0.565] },
    { arrow: [0.476, 0.565, 0.665, 0.31] },
    { t: 'NUEVA YORK', x: 0.30, y: 0.43, size: 28, pin: true, lado: 'esq' },
    { t: 'BERMUDAS', x: 0.476, y: 0.565, size: 28, pin: true, lado: 'dir' },
    { t: 'LONDRES', x: 0.665, y: 0.31, size: 28, pin: true, lado: 'dir' },
  ],
  // Exp. 11: o míssil, julho de 1981 (Malvinas)
  'map_south:N054': [
    { t: 'ISLAS MALVINAS', x: 0.465, y: 0.874, size: 28, pin: true, lado: 'esq' },
  ],
};
export const labelsDe = (s) => LABELS[`${s.chave}:${s.bloco}`] || LABELS[s.chave] || [];
