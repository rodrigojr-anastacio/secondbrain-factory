import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { loadFont as loadCaveat } from '@remotion/google-fonts/Caveat';
import { TYPE, DISPLAY, PAPEL, ROJO, TINTA, PASTA } from './Video.jsx';

// 016 MKUltra. 3 conceitos DIFERENTES (EMBALAGEM.md r5, crivo aprovado):
// A (objeto-simbolo): cogumelos sagrados + vela sobre pano mazateco; "MKULTRA" gigante em papel (sem sello).
// B (cena-acao): cientista da CIA de perfil, saco de lona no ombro; "10 LIBRAS" estampado na lona (diegético).
// C (documento-evidencia): folha sobre a bandeira de Honduras; "stress" riscado e "deplore" manuscrito + rótulo "HONDURAS".
const caveat = loadCaveat('normal', { weights: ['700'], subsets: ['latin'] });
const Aba = () => (
  <div style={{ position: 'absolute', right: 34, top: 0, background: PASTA, padding: '14px 28px 12px', borderRadius: '0 0 14px 14px',
    fontFamily: TYPE, fontSize: 30, color: TINTA, letterSpacing: 2, boxShadow: '4px 5px 0 rgba(0,0,0,.5)' }}>EXPEDIENTE Nº 016</div>
);

const Carimbo = ({ txt, fs, rot, pos }) => (
  <div style={{ position: 'absolute', transform: `rotate(${rot}deg)`, background: ROJO, border: `6px solid ${ROJO}`, outline: `3px solid ${PAPEL}`, outlineOffset: -14,
    padding: '10px 34px 4px', fontFamily: DISPLAY, fontSize: fs, color: PAPEL, letterSpacing: 4, whiteSpace: 'nowrap', boxShadow: '6px 8px 0 rgba(0,0,0,.5)', ...pos }}>{txt}</div>
);

const A = () => (
  <AbsoluteFill style={{ background: '#2E3A46' }}>
    <Img src={staticFile('img/thumb-A.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <Aba />
    <div style={{ position: 'absolute', left: 575, top: 235, fontFamily: DISPLAY, fontSize: 212, lineHeight: 1, color: PAPEL, letterSpacing: 4, whiteSpace: 'nowrap',
      textShadow: '8px 9px 0 rgba(0,0,0,.55)' }}>MKULTRA</div>
  </AbsoluteFill>
);

const B = () => (
  <AbsoluteFill style={{ background: '#1b222b' }}>
    <Img src={staticFile('img/thumb-B.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <Aba />
    <div style={{ position: 'absolute', left: 665, top: 395, width: 250, textAlign: 'center', transform: 'rotate(-22deg)', fontFamily: DISPLAY, fontSize: 92, lineHeight: 0.92,
      color: '#15130f', opacity: 0.9, letterSpacing: 3 }}>10<br />LIBRAS</div>
  </AbsoluteFill>
);

const C = () => (
  <AbsoluteFill style={{ background: '#1d1a16' }}>
    <Img src={staticFile('img/thumb-C.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <Aba />
    <div style={{ position: 'absolute', left: 385, top: 250, width: 700, transform: 'rotate(-5deg)', textAlign: 'center' }}>
      <div style={{ position: 'absolute', left: 10, right: 10, top: 20, height: 330, background: '#DCCB9E' }} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: -30, fontFamily: caveat.fontFamily, fontWeight: 700, fontSize: 235, lineHeight: 1, color: '#1F3C9B' }}>deplore</div>
      <div style={{ position: 'absolute', left: 255, top: 150, fontFamily: caveat.fontFamily, fontWeight: 700, fontSize: 80, color: '#1F3C9B' }}>^</div>
      <div style={{ position: 'relative', top: 175, fontFamily: TYPE, fontSize: 130, lineHeight: 1, color: '#2a251d', letterSpacing: 2 }}>stress
        <div style={{ position: 'absolute', left: -12, right: -12, top: '52%', height: 16, background: '#1F3C9B', transform: 'rotate(-2deg)', borderRadius: 8 }} />
      </div>
    </div>
    <div style={{ position: 'absolute', right: 26, bottom: 24, background: '#111', padding: '6px 14px' }}>
      <div style={{ background: PAPEL, padding: '4px 22px 0', fontFamily: TYPE, fontSize: 38, color: TINTA, letterSpacing: 6 }}>HONDURAS</div>
    </div>
  </AbsoluteFill>
);

export const Thumbnail = ({ variante = 'A' }) => (variante === 'B' ? <B /> : variante === 'C' ? <C /> : <A />);
