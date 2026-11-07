import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { loadFont as loadCaslon } from '@remotion/google-fonts/LibreCaslonText';
import { loadFont as loadOpenSans } from '@remotion/google-fonts/OpenSans';

const caslon = loadCaslon('normal', { weights: ['700'], subsets: ['latin'] });
const sans = loadOpenSans('normal', { weights: ['800'], subsets: ['latin'] });
const OURO = '#F2B705'; // cor de destaque fixa do canal (selo de datas)

// Fórmula do canal: ilustração à esquerda, céu livre à direita; nome do país em serifa preta gigante + selo de datas em amarelo-ouro.
// props: base (arquivo em public/img), variante (A | B | C) só ajusta posição/tamanho conforme a composição da base.
const LAYOUT = {
  A: { right: 50, top: 70, w: 620, size: 270, pos: '50% 40%' },
  B: { right: 40, top: 50, w: 600, size: 235, pos: '50% 50%' },
  C: { right: 50, top: 70, w: 600, size: 270, pos: '50% 40%' },
};

export const Thumbnail = ({ base = 'thumb-base.jpg', variante = 'A', texto = 'IRÃ', datas = '4200 a.C. – 2026' }) => {
  const L = LAYOUT[variante] || LAYOUT.A;
  return (
    <AbsoluteFill style={{ background: '#a9d4ea' }}>
      <Img src={staticFile(`img/${base}`)} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: L.pos }} />
      <div style={{ position: 'absolute', right: L.right, top: L.top, width: L.w, textAlign: 'center' }}>
        <div style={{ fontFamily: `${caslon.fontFamily}, serif`, fontWeight: 700, fontSize: L.size, lineHeight: 1, color: '#0b0b0b', letterSpacing: 4,
          textShadow: '0 0 18px rgba(255,255,255,.55)' }}>{texto}</div>
        <div style={{ display: 'inline-block', marginTop: 14, background: OURO, border: '6px solid #0b0b0b', borderRadius: 14, padding: '6px 26px 10px',
          boxShadow: '7px 7px 0 rgba(11,11,11,.85)', fontFamily: `${sans.fontFamily}, sans-serif`, fontWeight: 800, fontSize: 62, color: '#0b0b0b', whiteSpace: 'nowrap' }}>{datas}</div>
      </div>
    </AbsoluteFill>
  );
};
