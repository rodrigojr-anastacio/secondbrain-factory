import { continueRender, delayRender, staticFile } from 'remotion';

// Identidade do canal (biblia/visual.md, canal.yaml). Fontes locais em public/fonts (a imagem do Pod não tem @remotion/google-fonts).
export const DISPLAY = 'Anton';            // números grandes
export const MONO = 'IBM Plex Mono';        // fichas de arquivo
export const COND = 'Barlow Condensed';     // rótulos de mapa e então × agora
export const AMARELO = '#FDD505';
export const CIANO = '#2BCEE2';
export const FERRUGEM = '#C8561E';
export const TINTA = '#111418';
export const PAPEL = '#EDE6D6';
export const GRIFO = 'rgba(255, 225, 77, 0.55)';
export const AREIA = '#D9CBA8';
export const MAR = '#0E2A3B';
export const W = 1920;
export const H = 1080;

const FONTES = [
  ['Anton', 'Anton-Regular.ttf', '400'],
  ['IBM Plex Mono', 'IBMPlexMono-Medium.ttf', '400'],
  ['IBM Plex Mono', 'IBMPlexMono-Bold.ttf', '700'],
  ['Barlow Condensed', 'BarlowCondensed-SemiBold.ttf', '600'],
  ['Barlow Condensed', 'BarlowCondensed-Bold.ttf', '700'],
];
if (typeof document !== 'undefined' && !window.__fontesMidway) {
  window.__fontesMidway = true;
  const h = delayRender('fontes');
  Promise.all(FONTES.map(([fam, arq, peso]) => {
    const f = new FontFace(fam, `url('${staticFile('fonts/' + arq)}') format('truetype')`, { weight: peso });
    return f.load().then((ok) => document.fonts.add(ok));
  })).then(() => continueRender(h)).catch((e) => { console.error(e); continueRender(h); });
}
