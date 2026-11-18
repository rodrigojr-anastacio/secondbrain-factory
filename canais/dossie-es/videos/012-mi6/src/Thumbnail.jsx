import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { TYPE, DISPLAY, PAPEL, ROJO, TINTA, PASTA } from './Video.jsx';

// 011 Los Templarios. 3 conceitos DIFERENTES (EMBALAGEM.md, crivo r3):
// A (objeto-simbolo): coroa de criança sobre o manto templário dobrado (base ampliada), fundo ardósia, "TEMPLARIOS" em cor papel + sello HUÉRFANO + aba Nº 011.
// B (documento-evidencia): sentença em pergaminho com selos pendentes, luz de vela, "TARRAGONA" grande; texto do pergaminho desfocado; sem sello, sem aba.
// C (cena-acao): trabuco em silhueta contra a lua cheia diante do castelo, noite azul, sello "¿HEREJES?" no céu da direita.
const SELLO = (txt, fs, extra) => (
  <div style={{ position: 'absolute', transform: `rotate(${extra.rot}deg)`, border: `9px solid ${ROJO}`, outline: `3px solid ${ROJO}`, outlineOffset: 6,
    padding: '6px 26px 0', fontFamily: DISPLAY, fontSize: fs, color: ROJO, letterSpacing: 4, background: 'rgba(233,223,201,.95)', whiteSpace: 'nowrap', ...extra.pos }}>{txt}</div>
);

const A = () => (
  <AbsoluteFill style={{ background: '#2E3A46' }}>
    <Img src={staticFile('img/thumb-A.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', transform: 'scale(1.8)', transformOrigin: '12% 72%' }} />
    <div style={{ position: 'absolute', right: 34, top: 0, background: PASTA, padding: '14px 28px 12px', borderRadius: '0 0 14px 14px',
      fontFamily: TYPE, fontSize: 30, color: TINTA, letterSpacing: 2, boxShadow: '4px 5px 0 rgba(0,0,0,.5)' }}>EXPEDIENTE Nº 011</div>
    <div style={{ position: 'absolute', right: 24, top: 150, width: 700, textAlign: 'center' }}>
      <div style={{ fontFamily: DISPLAY, fontSize: 138, lineHeight: 0.95, color: PAPEL, letterSpacing: 3, whiteSpace: 'nowrap', textShadow: '0 6px 0 rgba(0,0,0,.55)' }}>TEMPLARIOS</div>
    </div>
    {SELLO('HUÉRFANO', 100, { rot: -7, pos: { right: 30, top: 340 } })}
  </AbsoluteFill>
);

const B = () => (
  <AbsoluteFill style={{ background: '#2a2622' }}>
    {/* a base é ampliada para esconder a moldura e deixar a mesa + selos ocuparem o quadro */}
    <Img src={staticFile('img/thumb-B.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', transform: 'scale(1.16)', transformOrigin: '50% 62%' }} />
    <div style={{ position: 'absolute', left: '24%', width: '50%', top: '30%', height: '26%', backdropFilter: 'blur(4px)', transform: 'rotate(3deg)' }} />
    <div style={{ position: 'absolute', left: 0, right: 0, top: 22, textAlign: 'center', fontFamily: DISPLAY, fontSize: 200, color: PAPEL, letterSpacing: 6,
      textShadow: '0 7px 0 rgba(0,0,0,.7), 0 0 30px rgba(0,0,0,.6)' }}>TARRAGONA</div>
  </AbsoluteFill>
);

const C = () => (
  <AbsoluteFill style={{ background: '#889' }}>
    <Img src={staticFile('img/thumb-C.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
    {SELLO('¿HEREJES?', 120, { rot: -6, pos: { right: 36, top: 56 } })}
  </AbsoluteFill>
);

export const Thumbnail = ({ variante = 'A' }) => (variante === 'B' ? <B /> : variante === 'C' ? <C /> : <A />);
