// Mapas: base gerada sem texto nem pinos; tudo o que é nome, pino e seta é feito aqui (posição em fração da imagem).
// Chave `chave:bloco` (variante por uso) ou só `chave`. { t, x, y, size, pin, lado } rótulo com pino; { arrow: [x0,y0,x1,y1] } seta.
// 014 Yakuza: posição medida na base I168 (japan_map), 21/11/2026; y em fração da altura. Okinawa fica fora do quadro: só Tokio.
export const LABELS = {
  'japan_map:N054': [
    { t: 'TOKIO', x: 0.61, y: 0.645, size: 30, pin: true, lado: 'dir' },
  ],
};
export const labelsDe = (s) => LABELS[`${s.chave}:${s.bloco}`] || LABELS[s.chave] || [];
