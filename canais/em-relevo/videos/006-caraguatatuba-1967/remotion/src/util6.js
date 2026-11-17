import { clamp01 } from '../../shared/camadas.js';
export const MONO = 'PlexMono, monospace';
export const P = { papel: '#E9DCC3', coral: '#E8505B', navy: '#1F2A44', tinta: '#2B2622', branco: '#FBF8F1', amarelo: '#FFD23F', ciano: '#3FD8FF', terra: '#B9A47F' };
export const tab = (arr, t) => {
  if (!arr.length) return 0;
  if (t <= arr[0][0]) return arr[0][1];
  for (let i = 1; i < arr.length; i++) if (t <= arr[i][0]) { const [a, va] = arr[i - 1], [b, vb] = arr[i]; return b === a ? vb : va + (vb - va) * clamp01((t - a) / (b - a)); }
  return arr[arr.length - 1][1];
};
export const win = (t, t0, t1, din = 0.45, dout = 0.4) => clamp01((t - t0) / din) * (1 - clamp01((t - t1) / dout));
import { useLayoutEffect, useState } from 'react';
import { staticFile, delayRender, continueRender } from 'remotion';
export const useFontes = () => {
  const [h] = useState(() => delayRender('fontes', { timeoutInMilliseconds: 120000 }));
  useLayoutEffect(() => {
    Promise.all([['Anton', 'Anton-Regular.ttf', '400', 'normal'], ['PlexMono', 'IBMPlexMono-Bold.ttf', '700', 'normal']].map(([fam, arq, w, st]) => { const f = new FontFace(fam, `url(${staticFile('fonts/' + arq)})`, { weight: w, style: st }); document.fonts.add(f); return f.load(); })).then(() => continueRender(h));
  }, [h]);
};
