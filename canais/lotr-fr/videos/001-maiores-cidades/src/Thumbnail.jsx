import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { loadFont as loadCinzel } from '@remotion/google-fonts/Cinzel';
const cinzel = loadCinzel('normal', { weights: ['700', '900'], subsets: ['latin', 'latin-ext'] });

export const Thumbnail = () => (
  <AbsoluteFill style={{ background: '#120d08' }}>
    <Img src={staticFile('img/cole_consummation.jpg')} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', objectPosition: '55% 45%', transform: 'scale(1.15)', transformOrigin: '60% 40%', filter: 'saturate(1.1) contrast(1.08)' }} />
    <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(10,7,4,.92) 0%, rgba(10,7,4,.75) 38%, rgba(10,7,4,0) 62%)' }} />
    <div style={{ position: 'absolute', left: 80, top: 150, width: 900, fontFamily: cinzel.fontFamily }}>
      <div style={{ fontSize: 58, color: '#e3b65a', fontWeight: 700, letterSpacing: 4 }}>LA PLUS GRANDE</div>
      <div style={{ fontSize: 132, color: '#fbf2dc', fontWeight: 900, lineHeight: 1.0, textShadow: '0 6px 24px rgba(0,0,0,.8)' }}>VILLE</div>
      <div style={{ fontSize: 58, color: '#e3b65a', fontWeight: 700, letterSpacing: 2, marginTop: 6 }}>DE LA TERRE DU MILIEU ?</div>
      <div style={{ width: 380, height: 6, background: '#c8932f', margin: '42px 0 30px' }} />
      <div style={{ fontSize: 44, color: '#fbf2dc', fontWeight: 700, letterSpacing: 2 }}>GONDOLIN · KHAZAD-DÛM</div>
      <div style={{ fontSize: 44, color: '#fbf2dc', fontWeight: 700, letterSpacing: 2, marginTop: 8 }}>OSGILIATH · ???</div>
    </div>
  </AbsoluteFill>
);
