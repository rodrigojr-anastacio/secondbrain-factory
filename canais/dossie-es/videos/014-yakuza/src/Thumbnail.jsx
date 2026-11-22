import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { loadFont as loadJP } from '@remotion/google-fonts/NotoSerifJP';
import { TYPE, DISPLAY, PAPEL, ROJO, TINTA, PASTA } from './Video.jsx';

const jp = loadJP('normal', { weights: ['900'], subsets: ['japanese'], ignoreTooManyRequestsWarning: true });
// 014 Yakuza. 3 conceitos DIFERENTES (EMBALAGEM.md, crivo r3):
// A (objeto-simbolo): letreiro de madeira arrancado sob a marca na parede; 組 em código; "YAKUZA" + sello "¿LEGAL?".
// B (numero-estatistica): salão de tatame vazio; "184.000" gigante riscado em vermelho + "HOY 17.600" sobre tira vermelha.
// C (cena-acao): homem em contraluz rasgando o cartão de visita com o emblema; rótulo datilografado "YAKUZA".
const Aba = () => (
  <div style={{ position: 'absolute', right: 34, top: 0, background: PASTA, padding: '14px 28px 12px', borderRadius: '0 0 14px 14px',
    fontFamily: TYPE, fontSize: 30, color: TINTA, letterSpacing: 2, boxShadow: '4px 5px 0 rgba(0,0,0,.5)' }}>EXPEDIENTE Nº 014</div>
);

const Carimbo = ({ txt, fs, rot, pos }) => (
  <div style={{ position: 'absolute', transform: `rotate(${rot}deg)`, background: ROJO, border: `6px solid ${ROJO}`, outline: `3px solid ${PAPEL}`, outlineOffset: -14,
    padding: '10px 34px 4px', fontFamily: DISPLAY, fontSize: fs, color: PAPEL, letterSpacing: 4, whiteSpace: 'nowrap', boxShadow: '6px 8px 0 rgba(0,0,0,.5)', ...pos }}>{txt}</div>
);

const A = () => (
  <AbsoluteFill style={{ background: PAPEL }}>
    <Img src={staticFile('img/thumb-A.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <Aba />
    <div style={{ position: 'absolute', left: 232, top: 300, width: 268, textAlign: 'center', fontFamily: jp.fontFamily, fontWeight: 900, fontSize: 210, lineHeight: 1,
      color: TINTA, transform: 'rotate(-3deg)', opacity: 0.88 }}>組</div>
    <div style={{ position: 'absolute', left: 560, top: 120, fontFamily: DISPLAY, fontSize: 260, lineHeight: 1, color: TINTA, letterSpacing: 4, whiteSpace: 'nowrap' }}>YAKUZA</div>
    <Carimbo txt="¿LEGAL?" fs={92} rot={-7} pos={{ left: 150, top: 540 }} />
  </AbsoluteFill>
);

const B = () => (
  <AbsoluteFill style={{ background: '#2a2f36' }}>
    <Img src={staticFile('img/thumb-B.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <AbsoluteFill style={{ background: 'linear-gradient(120deg, rgba(10,14,20,.62) 0%, rgba(10,14,20,.25) 55%, rgba(10,14,20,0) 100%)' }} />
    <div style={{ position: 'absolute', left: 36, top: 70, fontFamily: DISPLAY, fontSize: 320, lineHeight: 1, color: PAPEL, letterSpacing: 4, whiteSpace: 'nowrap',
      textShadow: '0 0 0 #000, 6px 6px 0 rgba(0,0,0,.85), -3px -3px 0 rgba(0,0,0,.6), 3px -3px 0 rgba(0,0,0,.6), -3px 3px 0 rgba(0,0,0,.6)' }}>184.000</div>
    <div style={{ position: 'absolute', left: 20, top: 205, width: 1010, height: 26, background: ROJO, transform: 'rotate(-6deg)', boxShadow: '0 4px 0 rgba(0,0,0,.5)' }} />
    <div style={{ position: 'absolute', right: 40, bottom: 48, background: ROJO, padding: '10px 38px 2px', transform: 'rotate(-2deg)', boxShadow: '6px 8px 0 rgba(0,0,0,.5)',
      fontFamily: DISPLAY, fontSize: 130, lineHeight: 1.1, color: PAPEL, letterSpacing: 3, whiteSpace: 'nowrap' }}>HOY 17.600</div>
    <Aba />
  </AbsoluteFill>
);

const C = () => (
  <AbsoluteFill style={{ background: '#1d1d1a' }}>
    <Img src={staticFile('img/thumb-C.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <div style={{ position: 'absolute', right: 36, bottom: 40, background: PAPEL, padding: '10px 34px 12px', transform: 'rotate(-2deg)', boxShadow: '6px 8px 0 rgba(0,0,0,.55)',
      fontFamily: TYPE, fontWeight: 700, fontSize: 112, lineHeight: 1.05, color: TINTA, letterSpacing: 4, whiteSpace: 'nowrap' }}>YAKUZA</div>
  </AbsoluteFill>
);

export const Thumbnail = ({ variante = 'A' }) => (variante === 'B' ? <B /> : variante === 'C' ? <C /> : <A />);
