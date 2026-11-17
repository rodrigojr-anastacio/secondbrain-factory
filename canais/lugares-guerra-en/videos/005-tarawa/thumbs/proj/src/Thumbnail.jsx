import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { DISPLAY, AMARELO, TINTA, MONO } from './estilo.jsx';

// Thumbs do 005-tarawa: 3 conceitos (A objeto-simbolo, B cena-acao, C antes-depois). Base sem texto + texto no código.
const stroke = (t) => ({ fontFamily: DISPLAY, color: AMARELO, letterSpacing: 1, WebkitTextStroke: `${Math.round(t / 14)}px ${TINTA}`,
  paintOrder: 'stroke fill', textShadow: '0 8px 0 rgba(0,0,0,.55), 0 0 30px rgba(0,0,0,.45)', lineHeight: 0.98 });
const Selo = ({ style }) => (
  <div style={{ position: 'absolute', padding: '4px 14px', border: '4px solid #D7261E', color: '#fff', background: 'rgba(215,38,30,.92)',
    fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: 4, transform: 'rotate(-3deg)', boxShadow: '0 5px 0 rgba(0,0,0,.5)', ...style }}>RESTRICTED</div>
);
const Rotulo = ({ t, style }) => (
  <div style={{ position: 'absolute', fontFamily: DISPLAY, fontSize: 54, color: '#fff', letterSpacing: 3, WebkitTextStroke: `4px ${TINTA}`,
    paintOrder: 'stroke fill', textShadow: '0 4px 0 rgba(0,0,0,.6)', ...style }}>{t}</div>
);

export const Thumbnail = ({ variante = 'A' }) => (
  <AbsoluteFill style={{ background: TINTA }}>
    <Img src={staticFile(`img/${variante}.jpg`)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
    {variante === 'A' && (<>
      <Rotulo t="U.S." style={{ left: 410, top: 520 }} />
      <Rotulo t="JAPAN" style={{ left: 690, top: 600 }} />
      <div style={{ position: 'absolute', top: 40, right: 50, textAlign: 'right' }}>
        <div style={{ ...stroke(190), fontSize: 190 }}>SAME</div>
        <div style={{ ...stroke(190), fontSize: 190 }}>HOLE</div>
      </div>
      <Selo style={{ top: 420, right: 60 }} />
    </>)}
    {variante === 'B' && (<>
      <div style={{ position: 'absolute', top: 30, left: 46, ...stroke(160), fontSize: 160 }}>WHOSE?</div>
      <svg width="1280" height="720" style={{ position: 'absolute', left: 0, top: 0 }}>
        <g stroke="#111418" strokeWidth="14" strokeLinejoin="round"><line x1="110" y1="470" x2="400" y2="360" strokeWidth="46" strokeLinecap="round" /><polygon points="480,330 380,290 395,400" fill="#111418" /></g>
        <line x1="110" y1="470" x2="400" y2="360" stroke="#D7261E" strokeWidth="30" strokeLinecap="round" />
        <polygon points="470,330 385,300 398,385" fill="#D7261E" />
      </svg>
      <Selo style={{ bottom: 40, left: 50 }} />
    </>)}
    {variante === 'C' && (<>
      <div style={{ position: 'absolute', left: 632, top: 0, width: 16, height: 720, background: AMARELO, boxShadow: '0 0 0 4px #111418' }} />
      <div style={{ position: 'absolute', top: 24, left: 40, ...stroke(170), fontSize: 170 }}>1943</div>
      <div style={{ position: 'absolute', top: 24, right: 40, ...stroke(170), fontSize: 170 }}>NOW</div>
      <Selo style={{ bottom: 40, left: 540 }} />
    </>)}
  </AbsoluteFill>
);
