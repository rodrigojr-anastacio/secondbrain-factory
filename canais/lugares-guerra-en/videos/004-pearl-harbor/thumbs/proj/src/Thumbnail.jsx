import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { DISPLAY, AMARELO, TINTA, MONO } from './estilo.jsx';

// Thumbs do 004-pearl-harbor (template: biblia/thumb.md). Base sem texto + texto no código.
const V = {
  A: { base: 'A.jpg', linhas: ['ON', 'PURPOSE'], lado: 'esq', top: 26, tam: [210, 170] },
  B: { base: 'B.jpg', linhas: ['ON', 'PURPOSE'], lado: 'dir', top: 360, tam: [140, 120] },
  C: { base: 'C.jpg', linhas: ['ON', 'PURPOSE'], lado: 'esq', top: 26, tam: [210, 170] },
};

export const Thumbnail = ({ variante = 'A' }) => {
  const v = V[variante] || V.A;
  const pos = v.lado === 'esq' ? { left: 46, textAlign: 'left' } : { right: 46, textAlign: 'right' };
  return (
    <AbsoluteFill style={{ background: TINTA }}>
      <Img src={staticFile(`img/${v.base}`)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      <div style={{ position: 'absolute', top: v.top, ...pos }}>
        {v.linhas.map((l, i) => (
          <div key={i} style={{ fontFamily: DISPLAY, fontSize: v.tam[i], lineHeight: 0.98, color: AMARELO, letterSpacing: 1,
            WebkitTextStroke: `${Math.round(v.tam[i] / 14)}px ${TINTA}`, paintOrder: 'stroke fill',
            textShadow: '0 8px 0 rgba(0,0,0,.55), 0 0 30px rgba(0,0,0,.45)' }}>{l}</div>
        ))}
        <div style={{ display: 'inline-block', marginTop: 14, padding: '4px 14px', border: '4px solid #D7261E', color: '#fff',
          background: 'rgba(215,38,30,.92)', fontFamily: MONO, fontWeight: 700, fontSize: 30, letterSpacing: 4,
          transform: 'rotate(-3deg)', boxShadow: '0 5px 0 rgba(0,0,0,.5)' }}>RESTRICTED</div>
      </div>
    </AbsoluteFill>
  );
};
