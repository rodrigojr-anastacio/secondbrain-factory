import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { TYPE, DISPLAY, PAPEL, ROJO, TINTA, PASTA } from './Video.jsx';

// 010 Cártel de Medellín. 3 conceitos DIFERENTES (EMBALAGEM.md, crivo r3):
// A (objeto-simbolo): algemas de aço em close, fundo ardósia, "MEDELLÍN" em cor papel + sello INTOCABLES + aba Nº 010.
// B (documento-evidencia): folha datilografada ocupando o quadro, uma palavra sob tarja preta, "ART. 35" em máquina de escrever; sem sello, sem aba.
// C (cena-acao): fazenda branca + helicópteros de dia, sello "¿RESCATE?" com fundo papel no céu da direita.
const SELLO = (txt, fs, extra) => (
  <div style={{ position: 'absolute', transform: `rotate(${extra.rot}deg)`, border: `9px solid ${ROJO}`, outline: `3px solid ${ROJO}`, outlineOffset: 6,
    padding: '6px 26px 0', fontFamily: DISPLAY, fontSize: fs, color: ROJO, letterSpacing: 4, background: 'rgba(233,223,201,.95)', whiteSpace: 'nowrap', ...extra.pos }}>{txt}</div>
);

const A = () => (
  <AbsoluteFill style={{ background: '#2E3A46' }}>
    <Img src={staticFile('img/thumb-A.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
    <div style={{ position: 'absolute', right: 34, top: 0, background: PASTA, padding: '14px 28px 12px', borderRadius: '0 0 14px 14px',
      fontFamily: TYPE, fontSize: 30, color: TINTA, letterSpacing: 2, boxShadow: '4px 5px 0 rgba(0,0,0,.5)' }}>EXPEDIENTE Nº 010</div>
    <div style={{ position: 'absolute', right: 14, top: 160, width: 600, textAlign: 'center' }}>
      <div style={{ fontFamily: DISPLAY, fontSize: 170, lineHeight: 0.95, color: PAPEL, letterSpacing: 3, whiteSpace: 'nowrap', textShadow: '0 6px 0 rgba(0,0,0,.55)' }}>MEDELLÍN</div>
    </div>
    {SELLO('INTOCABLES', 92, { rot: -8, pos: { left: 96, bottom: 62 } })}
  </AbsoluteFill>
);

const LINHAS = [0.58, 0.9, 0.74, 0.86, 0.5, 0.82, 0.7];
const B = () => (
  <AbsoluteFill style={{ background: '#d9c9a0' }}>
    {/* a folha da base é ampliada para ocupar o quadro (sem mesa, sem o livro vermelho) */}
    <Img src={staticFile('img/thumb-B.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', transform: 'scale(1.42)', transformOrigin: '47% 52%' }} />
    <div style={{ position: 'absolute', left: 0, right: 0, top: 36, textAlign: 'center', fontFamily: TYPE, fontSize: 168, color: TINTA, letterSpacing: 6, fontWeight: 900,
      WebkitTextStroke: '5px #1A1A1A' }}>ART. 35</div>
    <div style={{ position: 'absolute', left: 210, right: 210, top: 280 }}>
      {LINHAS.map((w, i) => (
        <div key={i} style={{ height: 16, width: `${w * 100}%`, background: 'rgba(26,26,26,.28)', borderRadius: 8, marginBottom: 26, filter: 'blur(2.5px)' }} />
      ))}
    </div>
    <div style={{ position: 'absolute', left: 190, top: 430, width: 700, height: 120, background: '#0b0b0b', transform: 'rotate(-1.4deg)', boxShadow: '0 5px 0 rgba(0,0,0,.35)' }} />
    <div style={{ position: 'absolute', left: 150, right: 170, top: 580 }}>
      {LINHAS.slice(0, 3).map((w, i) => (
        <div key={i} style={{ height: 16, width: `${w * 100}%`, background: 'rgba(26,26,26,.28)', borderRadius: 8, marginBottom: 26, filter: 'blur(2.5px)' }} />
      ))}
    </div>
  </AbsoluteFill>
);

const C = () => (
  <AbsoluteFill style={{ background: '#889' }}>
    <Img src={staticFile('img/thumb-C.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
    {SELLO('¿RESCATE?', 150, { rot: -7, pos: { right: 50, top: 150 } })}
  </AbsoluteFill>
);

export const Thumbnail = ({ variante = 'A' }) => (variante === 'B' ? <B /> : variante === 'C' ? <C /> : <A />);
