import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { TYPE, DISPLAY, PAPEL, ROJO, TINTA, PASTA } from './Video.jsx';

// 013 Núremberg. 3 conceitos DIFERENTES (EMBALAGEM.md, crivo r3):
// A (objeto-simbolo): fones de baquelita sobre papel creme; "NÚREMBERG" preto alto à direita + sello "SIN NOMBRE" sobre os fones.
// B (cena-acao): o fiscal lendo a acusação sob o refletor, SEM texto, sem aba.
// C (mapa-lugar): mapa do Atlântico; fio vermelho de Núremberg a 4 pontos latino-americanos (no código) + "HASTA AQUÍ".
const Aba = () => (
  <div style={{ position: 'absolute', right: 34, top: 0, background: PASTA, padding: '14px 28px 12px', borderRadius: '0 0 14px 14px',
    fontFamily: TYPE, fontSize: 30, color: TINTA, letterSpacing: 2, boxShadow: '4px 5px 0 rgba(0,0,0,.5)' }}>EXPEDIENTE Nº 013</div>
);

const Carimbo = ({ txt, fs, rot, pos }) => (
  <div style={{ position: 'absolute', transform: `rotate(${rot}deg)`, background: ROJO, border: `6px solid ${ROJO}`, outline: `3px solid ${PAPEL}`, outlineOffset: -14,
    padding: '10px 34px 4px', fontFamily: DISPLAY, fontSize: fs, color: PAPEL, letterSpacing: 4, whiteSpace: 'nowrap', boxShadow: '6px 8px 0 rgba(0,0,0,.5)', ...pos }}>{txt}</div>
);

const A = () => (
  <AbsoluteFill style={{ background: '#2E3A46' }}>
    <Img src={staticFile('img/thumb-A.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', transformOrigin: '22% 62%', transform: 'scale(1.3)' }} />
    <Aba />
    <div style={{ position: 'absolute', right: 40, top: 92, fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, color: TINTA, letterSpacing: 3,
      textShadow: '0 0 18px rgba(233,223,201,.9)', whiteSpace: 'nowrap' }}>NÚREMBERG</div>
    <Carimbo txt="SIN NOMBRE" fs={104} rot={-7} pos={{ left: 40, top: 470 }} />
  </AbsoluteFill>
);

const B = () => (
  <AbsoluteFill style={{ background: '#2a2f36' }}>
    <Img src={staticFile('img/thumb-B.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', transformOrigin: '38% 55%', transform: 'scale(1.15)' }} />
  </AbsoluteFill>
);

// pontos em fração do quadro 1280x720 (base 1344x768 com cover): Núremberg e 4 pontos latino-americanos
const NUR = [0.69, 0.105];
const PTS = [[0.205, 0.37], [0.41, 0.66], [0.262, 0.73], [0.33, 0.75]];
const C = () => {
  const W = 1280, H = 720;
  const p = (q) => [q[0] * W, q[1] * H];
  const [nx, ny] = p(NUR);
  return (
    <AbsoluteFill style={{ background: '#1d1712' }}>
      <Img src={staticFile('img/thumb-C.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
      <svg viewBox={`0 0 ${W} ${H}`} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
        {PTS.map((q, i) => { const [x, y] = p(q); const mx = (nx + x) / 2, my = Math.min(ny, y) - 120 - i * 18;
          return <path key={i} d={`M ${nx} ${ny} Q ${mx} ${my} ${x} ${y}`} fill="none" stroke={ROJO} strokeWidth={7} strokeLinecap="round" />; })}
        <circle cx={nx} cy={ny} r={17} fill={ROJO} stroke={PAPEL} strokeWidth={5} />
        {PTS.map((q, i) => { const [x, y] = p(q); return <circle key={i} cx={x} cy={y} r={14} fill={ROJO} stroke={PAPEL} strokeWidth={5} />; })}
      </svg>
      <Aba />
      <div style={{ position: 'absolute', left: 560, top: 400, fontFamily: DISPLAY, fontSize: 150, lineHeight: 1, color: PAPEL, letterSpacing: 3, whiteSpace: 'nowrap',
        textShadow: '0 7px 0 rgba(0,0,0,.8), 0 0 30px rgba(0,0,0,.8)' }}>HASTA AQUÍ</div>
    </AbsoluteFill>
  );
};

export const Thumbnail = ({ variante = 'A' }) => (variante === 'B' ? <B /> : variante === 'C' ? <C /> : <A />);
