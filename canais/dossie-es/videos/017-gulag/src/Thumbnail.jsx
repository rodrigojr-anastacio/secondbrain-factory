import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { TYPE, DISPLAY, PAPEL, ROJO, TINTA, PASTA } from './Video.jsx';

// 017 Gulag. 3 conceitos DIFERENTES (EMBALAGEM.md, crivo r3):
// A (objeto-simbolo): lingote com estrela na marmita; "GULAG" grande em papel + sello "¿RENTABLE?".
// B (documento-evidencia): tabela de normas com 3 pães; "NORMA" impresso como cabeçalho da tabela (tinta preta sobre o papel).
// C (cena-acao): homem de costas de ushanka desce a passarela em Barcelona; rótulo datilografado "BARCELONA".
const Aba = () => (
  <div style={{ position: 'absolute', right: 34, top: 0, background: PASTA, padding: '14px 28px 12px', borderRadius: '0 0 14px 14px',
    fontFamily: TYPE, fontSize: 30, color: TINTA, letterSpacing: 2, boxShadow: '4px 5px 0 rgba(0,0,0,.5)' }}>EXPEDIENTE Nº 017</div>
);

const Carimbo = ({ txt, fs, rot, pos }) => (
  <div style={{ position: 'absolute', transform: `rotate(${rot}deg)`, background: ROJO, border: `6px solid ${ROJO}`, outline: `3px solid ${PAPEL}`, outlineOffset: -14,
    padding: '10px 34px 4px', fontFamily: DISPLAY, fontSize: fs, color: PAPEL, letterSpacing: 4, whiteSpace: 'nowrap', boxShadow: '6px 8px 0 rgba(0,0,0,.5)', ...pos }}>{txt}</div>
);

const A = () => (
  <AbsoluteFill style={{ background: '#2E3A46' }}>
    <Img src={staticFile('img/thumb-A.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <div style={{ position: 'absolute', left: 560, top: 130, fontFamily: DISPLAY, fontSize: 270, lineHeight: 1, color: PAPEL, letterSpacing: 4, whiteSpace: 'nowrap',
      textShadow: '6px 7px 0 rgba(0,0,0,.8)' }}>GULAG</div>
    <Carimbo txt="¿RENTABLE?" fs={96} rot={-6} pos={{ left: 640, top: 440 }} />
    <Aba />
  </AbsoluteFill>
);

const B = () => (
  <AbsoluteFill style={{ background: '#2a2f36' }}>
    <Img src={staticFile('img/thumb-B.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <div style={{ position: 'absolute', left: 350, top: 40, width: 500, height: 150, background: '#E4D7B4', transform: 'rotate(-1deg)' }} />
    <div style={{ position: 'absolute', left: 350, top: 30, width: 500, textAlign: 'center', fontFamily: DISPLAY, fontSize: 190, lineHeight: 1.05, color: '#111', letterSpacing: 6, transform: 'rotate(-1deg)' }}>NORMA</div>
    <div style={{ position: 'absolute', left: 365, top: 188, width: 470, height: 12, background: ROJO, transform: 'rotate(-1deg)' }} />
  </AbsoluteFill>
);

const C = () => (
  <AbsoluteFill style={{ background: '#1d1d1a' }}>
    <Img src={staticFile('img/thumb-C.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <div style={{ position: 'absolute', right: 36, bottom: 40, background: PAPEL, padding: '10px 34px 12px', transform: 'rotate(-2deg)', boxShadow: '6px 8px 0 rgba(0,0,0,.55)',
      fontFamily: TYPE, fontWeight: 700, fontSize: 112, lineHeight: 1.05, color: TINTA, letterSpacing: 4, whiteSpace: 'nowrap' }}>BARCELONA</div>
  </AbsoluteFill>
);

export const Thumbnail = ({ variante = 'A' }) => (variante === 'B' ? <B /> : variante === 'C' ? <C /> : <A />);
