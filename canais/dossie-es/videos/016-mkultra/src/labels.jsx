// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// Chave `chave:bloco` (variante por uso) ou só `chave`. { t, x, y, size, pin, lado } rótulo com pino; { arrow: [x0,y0,x1,y1] } seta.
// 016 MKUltra: posições estimadas sobre as bases I012 (América Central/Caribe) e I154 (Honduras), grade de 10%, 24/11/2026; conferidas em stills.
export const LABELS = {
  'americas_map': [
    { t: 'CIUDAD DE MÉXICO', x: 0.275, y: 0.36, size: 26, pin: true, lado: 'esq' },
    { t: 'HUAUTLA', x: 0.315, y: 0.415, size: 26, pin: true, lado: 'dir' },
    { t: 'LA HABANA', x: 0.535, y: 0.235, size: 26, pin: true, lado: 'cima' },
    { t: 'TEGUCIGALPA', x: 0.47, y: 0.49, size: 26, pin: true, lado: 'dir' },
  ],
  'honduras_map': [
    { t: 'TEGUCIGALPA', x: 0.43, y: 0.6, size: 32, pin: true, lado: 'dir' },
  ],
};
export const labelsDe = (s) => LABELS[`${s.chave}:${s.bloco}`] || LABELS[s.chave] || [];
