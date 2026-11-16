import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { TYPE, DISPLAY, PAPEL, ROJO, TINTA, PASTA } from './Video.jsx';

// 009 La Gestapo. Conceito aprovado no crivo (EMBALAGEM.md): sobretudo de couro VAZIO no cabide (objeto, sem pessoa) à esquerda,
// "GESTAPO" preto à direita no alto, sello rojo "1983" inclinado sobre o peito do casaco (menor que a sigla e fora de alinhamento),
// aba "EXPEDIENTE Nº 009". Único vermelho = o sello. A/B pareadas com T1/T2 (mudam enquadramento da base); C muda o sello (LA PAZ 1983).
const V = {
  A: { base: 'thumb-A.jpg', palavra: 'GESTAPO', size: 205, sello: '1983', sx: 235, sy: 400, sfs: 104, rot: -9 },
  B: { base: 'thumb-B.jpg', palavra: 'GESTAPO', size: 205, sello: '1983', sx: 255, sy: 360, sfs: 110, rot: -7 },
  C: { base: 'thumb-C.jpg', palavra: 'GESTAPO', size: 205, sello: 'LA PAZ 1983', sx: 150, sy: 410, sfs: 66, rot: -10 },
};

export const Thumbnail = ({ variante = 'A' }) => {
  const v = V[variante] || V.A;
  return (
    <AbsoluteFill style={{ background: '#222' }}>
      <Img src={staticFile(`img/${v.base}`)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      <div style={{ position: 'absolute', right: 34, top: 0, background: PASTA, padding: '14px 28px 12px', borderRadius: '0 0 14px 14px',
        fontFamily: TYPE, fontSize: 30, color: TINTA, letterSpacing: 2, boxShadow: '4px 5px 0 rgba(0,0,0,.5)' }}>EXPEDIENTE Nº 009</div>
      <div style={{ position: 'absolute', right: 30, top: 118, width: 760, textAlign: 'center' }}>
        <div style={{ fontFamily: DISPLAY, fontSize: v.size, lineHeight: 0.95, color: TINTA, letterSpacing: 4, whiteSpace: 'nowrap',
          textShadow: '0 0 26px rgba(255,255,255,.75)' }}>{v.palavra}</div>
      </div>
      <div style={{ position: 'absolute', left: v.sx, top: v.sy, transform: `rotate(${v.rot}deg)`, border: `8px solid ${ROJO}`, outline: `3px solid ${ROJO}`,
        outlineOffset: 5, padding: '4px 22px 0', fontFamily: DISPLAY, fontSize: v.sfs, color: ROJO, letterSpacing: 4, background: 'rgba(233,223,201,.9)', whiteSpace: 'nowrap' }}>{v.sello}</div>
    </AbsoluteFill>
  );
};
