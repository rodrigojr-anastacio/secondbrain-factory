import { continueRender, delayRender, staticFile } from 'remotion';
export const DISPLAY = 'Anton'; export const MONO = 'IBM Plex Mono'; export const COND = 'Barlow Condensed';
export const AMARELO = '#FDD505'; export const CIANO = '#2BCEE2'; export const FERRUGEM = '#C8561E'; export const TINTA = '#111418';
const FONTES = [['Anton', 'Anton-Regular.ttf', '400'], ['IBM Plex Mono', 'IBMPlexMono-Medium.ttf', '400'], ['IBM Plex Mono', 'IBMPlexMono-Bold.ttf', '700'],
  ['Barlow Condensed', 'BarlowCondensed-SemiBold.ttf', '600'], ['Barlow Condensed', 'BarlowCondensed-Bold.ttf', '700']];
if (typeof document !== 'undefined' && !window.__fontesTh) {
  window.__fontesTh = true; const h = delayRender('fontes');
  Promise.all(FONTES.map(([fam, arq, peso]) => new FontFace(fam, `url('${staticFile('fonts/' + arq)}') format('truetype')`, { weight: peso }).load().then((ok) => document.fonts.add(ok))))
    .then(() => continueRender(h)).catch((e) => { console.error(e); continueRender(h); });
}
