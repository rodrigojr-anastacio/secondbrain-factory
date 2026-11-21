import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { DISPLAY, AMARELO, CIANO, TINTA, MONO, COND } from './estilo.jsx';
import M from './mapa.json';

// Thumbs do 006-chernobyl (3 conceitos do EMBALAGEM.md r3): A numero-estatistica (67 HOURS), B mapa-lugar (ON A SHOE), C antes-depois ("TEMPORARY").
const stroke = (t) => ({ fontFamily: DISPLAY, color: AMARELO, letterSpacing: 1, WebkitTextStroke: `${Math.round(t / 14)}px ${TINTA}`,
  paintOrder: 'stroke fill', textShadow: '0 8px 0 rgba(0,0,0,.55), 0 0 30px rgba(0,0,0,.45)', lineHeight: 0.98 });
const Selo = ({ style }) => (
  <div style={{ position: 'absolute', padding: '4px 14px', border: '4px solid #D7261E', color: '#fff', background: 'rgba(215,38,30,.92)',
    fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: 4, transform: 'rotate(-3deg)', boxShadow: '0 5px 0 rgba(0,0,0,.5)', ...style }}>RESTRICTED</div>
);

// cartão de dígito mecânico (flip): metade de cima mais clara, vinco no meio
const Flip = ({ d, x, y, w = 300, h = 430, skew = 0, rot = 0 }) => (
  <div style={{ position: 'absolute', left: x, top: y, width: w, height: h, borderRadius: 26, background: `linear-gradient(180deg, #FFE24A 0%, ${AMARELO} 49.5%, #1a1608 49.5%, #1a1608 50.5%, #E6BD00 50.5%, #F2CB00 100%)`,
    border: `8px solid ${TINTA}`, boxShadow: '0 16px 0 rgba(0,0,0,.55), 0 0 40px rgba(0,0,0,.5)', transform: `rotate(${rot}deg) skewY(${skew}deg)`, overflow: 'hidden' }}>
    <div style={{ position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: DISPLAY, fontSize: 440, color: TINTA, lineHeight: 1, paddingTop: 8 }}>{d}</div>
    <div style={{ position: 'absolute', left: 0, right: 0, top: '49%', height: 8, background: '#1a1608' }} />
  </div>
);

// sapato (tênis) em SVG, ~200 px de largura, amarelo com contorno tinta
const Sapato = ({ x, y, s = 1, rot = -12 }) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <path d="M-110 30 C-110 -10 -100 -40 -80 -50 L-40 -60 C-30 -75 -10 -80 10 -70 L30 -40 C60 -30 100 -20 120 0 C130 12 128 30 110 36 L-100 40 Z" fill={AMARELO} stroke={TINTA} strokeWidth="9" strokeLinejoin="round" />
    <path d="M-108 30 L112 36 L112 52 C112 60 104 64 96 64 L-96 60 C-108 58 -112 46 -108 30 Z" fill="#fff" stroke={TINTA} strokeWidth="9" strokeLinejoin="round" />
    <path d="M-30 -52 L-8 -22 M-6 -62 L16 -30 M16 -62 L38 -34" stroke={TINTA} strokeWidth="7" strokeLinecap="round" fill="none" />
    <path d="M-80 -40 C-70 -10 -50 10 -10 16" stroke={TINTA} strokeWidth="6" fill="none" strokeLinecap="round" />
  </g>
);

export const Thumbnail = ({ variante = 'A' }) => {
  const [cx, cy] = M.chernobyl, [fx, fy] = M.forsmark;
  const mx = (cx + fx) / 2 + 120, my = (cy + fy) / 2 + 20;
  return (
    <AbsoluteFill style={{ background: TINTA, overflow: 'hidden' }}>
      {variante === 'A' && (<>
        <Img src={staticFile('img/A.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', filter: 'brightness(.2) contrast(1.1) saturate(.7)' }} />
        <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 40% 50%, rgba(253,213,5,.10), rgba(0,0,0,0) 60%)' }} />
        <Flip d="6" x={74} y={125} rot={-2} />
        <Flip d="7" x={398} y={140} rot={2} skew={-6} />
        <div style={{ position: 'absolute', left: 750, top: 205, ...stroke(210), fontSize: 215 }}>HOURS</div>
        <Selo style={{ top: 52, right: 60 }} />
      </>)}
      {variante === 'B' && (<>
        <AbsoluteFill style={{ background: '#0c1e2b' }} />
        <svg width="1280" height="720" style={{ position: 'absolute', left: 0, top: 0 }}>
          {M.paths.map((p, i) => <path key={i} d={p.d} fill={p.pais === 'Sweden' ? CIANO : '#262d35'} stroke={p.pais === 'Sweden' ? '#0b6f7d' : '#4a535e'} strokeWidth={2} opacity={p.pais === 'Sweden' ? 0.95 : 1} />)}
          <path d={`M${cx},${cy} Q${mx},${my} ${fx + 10},${fy + 70}`} fill="none" stroke={TINTA} strokeWidth="64" strokeLinecap="round" />
          <path d={`M${cx},${cy} Q${mx},${my} ${fx + 10},${fy + 70}`} fill="none" stroke={AMARELO} strokeWidth="46" strokeLinecap="round" />
          <circle cx={cx} cy={cy} r="20" fill="#D7261E" stroke="#fff" strokeWidth="6" />
          <text x={cx + 34} y={cy + 56} fill="#fff" fontFamily={MONO} fontWeight="700" fontSize="30" style={{ paintOrder: 'stroke', stroke: TINTA, strokeWidth: 8 }}>CHERNOBYL</text>
          <g style={{ filter: 'drop-shadow(0 8px 0 rgba(0,0,0,.5))' }}><Sapato x={fx + 4} y={fy + 6} s={1.55} /></g>
        </svg>
        <div style={{ position: 'absolute', top: 34, right: 50, textAlign: 'right', ...stroke(170), fontSize: 170 }}>ON A</div>
        <div style={{ position: 'absolute', top: 188, right: 50, textAlign: 'right', ...stroke(170), fontSize: 170 }}>SHOE</div>
      </>)}
      {variante === 'C' && (<>
        <Img src={staticFile('img/C.jpg')} style={{ position: 'absolute', left: -64, top: -52, width: 1408, height: 804, objectFit: 'cover' }} />
        <div style={{ position: 'absolute', left: 0, right: 0, top: 360, bottom: 0, background: 'linear-gradient(180deg, rgba(17,20,24,0), rgba(17,20,24,.9) 45%)' }} />
        <div style={{ position: 'absolute', left: 0, right: 0, top: 500, textAlign: 'center', ...stroke(160), fontSize: 160, letterSpacing: 4 }}>“TEMPORARY”</div>
        <Selo style={{ top: 40, left: 44 }} />
      </>)}
    </AbsoluteFill>
  );
};
