// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// Chave `chave:bloco` (variante por uso) ou só `chave`. { t, x, y, size, pin, lado } rótulo com pino; { arrow: [x0,y0,x1,y1] } seta.
// 015 GRU: posições estimadas sobre as bases I012/I041/I096/I148/I178 (grade de 10%), 23/11/2026; conferidas em stills.
export const LABELS = {
  'world_map': [
    { t: 'MOSCÚ', x: 0.646, y: 0.237, size: 30, pin: true, lado: 'dir' },
    { t: 'BRUSELAS', x: 0.498, y: 0.277, size: 28, pin: true, lado: 'esq' },
    { t: 'LA HAYA', x: 0.503, y: 0.262, size: 26, pin: true, lado: 'cima' },
    { t: 'NÁPOLES', x: 0.533, y: 0.35, size: 28, pin: true, lado: 'dir' },
    { t: 'RÍO DE JANEIRO', x: 0.352, y: 0.692, size: 28, pin: true, lado: 'dir' },
    { t: 'MONTEVIDEO', x: 0.335, y: 0.769, size: 28, pin: true, lado: 'esq' },
  ],
  'europe_map': [
    { arrow: [0.455, 0.423, 0.424, 0.505] },
    { arrow: [0.455, 0.423, 0.464, 0.377] },
    { arrow: [0.455, 0.423, 0.595, 0.377] },
    { t: 'BRUSELAS', x: 0.455, y: 0.423, size: 32, pin: true, lado: 'esq' },
    { t: 'PARÍS', x: 0.424, y: 0.505, size: 26, pin: true, lado: 'esq' },
    { t: 'ÁMSTERDAM', x: 0.464, y: 0.377, size: 26, pin: true, lado: 'cima' },
    { t: 'BERLÍN', x: 0.595, y: 0.377, size: 26, pin: true, lado: 'dir' },
  ],
  'caribbean_map': [
    { arrow: [0.349, 0.255, 0.484, 0.204] },
    { t: 'LOURDES', x: 0.349, y: 0.255, size: 32, pin: true, lado: 'baixo' },
    { t: 'CAYOS DE FLORIDA', x: 0.484, y: 0.204, size: 26, pin: true, lado: 'dir' },
  ],
  'ukraine_map': [
    { arrow: [0.729, 0.355, 0.633, 0.505] },
    { t: 'MOSCÚ', x: 0.729, y: 0.355, size: 30, pin: true, lado: 'dir' },
    { t: 'KIEV', x: 0.633, y: 0.505, size: 30, pin: true, lado: 'baixo' },
  ],
  'mexico_map': [
    { t: 'CIUDAD DE MÉXICO', x: 0.585, y: 0.63, size: 30, pin: true, lado: 'dir' },
  ],
};
export const labelsDe = (s) => LABELS[`${s.chave}:${s.bloco}`] || LABELS[s.chave] || [];
