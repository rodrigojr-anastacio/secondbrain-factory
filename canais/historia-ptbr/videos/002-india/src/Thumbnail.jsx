import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { loadFont as loadCaslon } from '@remotion/google-fonts/LibreCaslonText';
import { loadFont as loadOpenSans } from '@remotion/google-fonts/OpenSans';

const caslon = loadCaslon('normal', { weights: ['700'], subsets: ['latin'] });
const sans = loadOpenSans('normal', { weights: ['800'], subsets: ['latin'] });

// Fórmula da referência: ilustração à esquerda, céu livre à direita com o título em serifa preta e as datas em sans bold.
export const Thumbnail = () => (
  <AbsoluteFill style={{ background: '#a9d4ea' }}>
    <Img src={staticFile('img/thumb-base.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 40%' }} />
    <div style={{ position: 'absolute', right: 56, top: 74, width: 590, textAlign: 'center' }}>
      <div style={{ fontFamily: `${caslon.fontFamily}, serif`, fontWeight: 700, fontSize: 156, lineHeight: 1, color: '#0b0b0b', letterSpacing: 2 }}>ÍNDIA</div>
      <div style={{ fontFamily: `${sans.fontFamily}, sans-serif`, fontWeight: 800, fontSize: 64, color: '#0b0b0b', marginTop: 22, whiteSpace: 'nowrap' }}>3300 a.C. – 2026</div>
    </div>
  </AbsoluteFill>
);
