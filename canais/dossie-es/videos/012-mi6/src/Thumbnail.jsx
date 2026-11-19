import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { TYPE, DISPLAY, PAPEL, ROJO, TINTA, PASTA } from './Video.jsx';

// 012 El MI6. 3 conceitos DIFERENTES (EMBALAGEM.md, crivo r3), nenhuma com a sigla "MI6":
// A (objeto-simbolo): máquina de escrever sozinha no cone de luz; sello vermelho "NUEVA YORK" no terço direito (tipo: rótulo de lugar).
// B (rosto-emocao, teste "personagem do tema"): Roosevelt aos microfones com a folha riscada; "¿SABÍA?" cor papel sobre carimbo vermelho (tipo: pergunta).
// C (mapa-lugar): o mapa forjado em 5 blocos, pena terminando uma fronteira; "14 → 5" cor papel sobre a mesa escura (tipo: número).
const Aba = () => (
  <div style={{ position: 'absolute', right: 34, top: 0, background: PASTA, padding: '14px 28px 12px', borderRadius: '0 0 14px 14px',
    fontFamily: TYPE, fontSize: 30, color: TINTA, letterSpacing: 2, boxShadow: '4px 5px 0 rgba(0,0,0,.5)' }}>EXPEDIENTE Nº 012</div>
);

const Carimbo = ({ txt, fs, rot, pos }) => (
  <div style={{ position: 'absolute', transform: `rotate(${rot}deg)`, background: ROJO, border: `6px solid ${ROJO}`, outline: `3px solid ${PAPEL}`, outlineOffset: -14,
    padding: '10px 34px 4px', fontFamily: DISPLAY, fontSize: fs, color: PAPEL, letterSpacing: 4, whiteSpace: 'nowrap', boxShadow: '6px 8px 0 rgba(0,0,0,.5)', ...pos }}>{txt}</div>
);

const A = () => (
  <AbsoluteFill style={{ background: '#2E3A46' }}>
    <Img src={staticFile('img/thumb-A.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <Aba />
    <Carimbo txt="NUEVA YORK" fs={118} rot={-6} pos={{ right: 36, top: 330 }} />
  </AbsoluteFill>
);

const B = () => (
  <AbsoluteFill style={{ background: '#2a2f36' }}>
    <Img src={staticFile('img/thumb-B.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <Aba />
    <Carimbo txt="¿SABÍA?" fs={160} rot={-5} pos={{ right: 36, top: 110 }} />
  </AbsoluteFill>
);

const C = () => (
  <AbsoluteFill style={{ background: '#1d1712' }}>
    <Img src={staticFile('img/thumb-C.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', transform: 'translateX(-140px)' }} />
    <Aba />
    <div style={{ position: 'absolute', right: 30, top: 260, width: 330, textAlign: 'center', fontFamily: DISPLAY, fontSize: 118, lineHeight: 1, color: PAPEL,
      letterSpacing: 2, whiteSpace: 'nowrap', textShadow: '0 7px 0 rgba(0,0,0,.75), 0 0 28px rgba(0,0,0,.7)' }}>14 → 5</div>
  </AbsoluteFill>
);

export const Thumbnail = ({ variante = 'A' }) => (variante === 'B' ? <B /> : variante === 'C' ? <C /> : <A />);
