// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// Chave `chave:bloco` (variante por uso) ou só `chave`. { t, x, y, size, pin, lado } rótulo com pino; { arrow: [x0,y0,x1,y1] } seta.
// 013 Núremberg: posições medidas com grade nas bases I012 (atlantic_map), I056 (latam_map), I135 (ratline_map), I173 (guatemala_map), 20/11/2026; y em fração da altura.
export const LABELS = {
  // N004: do hook, "las palabras que viajaron desde allí hasta América Latina"
  'atlantic_map:N004': [
    { arrow: [0.745, 0.19, 0.40, 0.55] },
    { t: 'NÚREMBERG', x: 0.745, y: 0.19, size: 28, pin: true, lado: 'dir' },
    { t: 'AMÉRICA LATINA', x: 0.40, y: 0.55, size: 28, pin: true, lado: 'esq' },
  ],
  // N018: seis dos países latino-americanos que aderem
  'latam_map:N018': [
    { t: 'HAITÍ', x: 0.485, y: 0.165, size: 26, pin: true, lado: 'dir' },
    { t: 'HONDURAS', x: 0.377, y: 0.225, size: 26, pin: true, lado: 'esq' },
    { t: 'PANAMÁ', x: 0.417, y: 0.30, size: 26, pin: true, lado: 'esq' },
    { t: 'VENEZUELA', x: 0.53, y: 0.345, size: 26, pin: true, lado: 'dir' },
    { t: 'PARAGUAY', x: 0.575, y: 0.745, size: 26, pin: true, lado: 'dir' },
  ],
  // N049: responsáveis cruzam o oceano (regiões, sem pino)
  'ratline_map:N049': [
    { arrow: [0.50, 0.30, 0.285, 0.70] },
    { t: 'EUROPA', x: 0.50, y: 0.30, size: 28, pin: true, lado: 'dir' },
    { t: 'AMÉRICA DEL SUR', x: 0.285, y: 0.70, size: 28, pin: true, lado: 'dir' },
  ],
  // N064: a palavra de Lemkin em outro país
  'guatemala_map:N064': [
    { t: 'GUATEMALA', x: 0.36, y: 0.45, size: 30, pin: true, lado: 'dir' },
  ],
};
export const labelsDe = (s) => LABELS[`${s.chave}:${s.bloco}`] || LABELS[s.chave] || [];
