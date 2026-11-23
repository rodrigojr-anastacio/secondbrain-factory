import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { TYPE, DISPLAY, PAPEL, ROJO, TINTA, PASTA } from './Video.jsx';

// 015 GRU. 3 conceitos DIFERENTES (EMBALAGEM.md, crivo r3):
// A (objeto-simbolo): matrioska empresário/oficial soviético; "GRU" gigante em papel + sello "GULAG".
// B (cena-acao): Putin aperta a mão na pista de Vnukovo à noite; carimbo "¿BRASILEÑO?" no terço inferior direito.
// C (documento-evidencia): 3 passaportes em leque, MRZ desenhada no código na página aberta; carimbo "NUNCA NACIERON".
const Aba = () => (
  <div style={{ position: 'absolute', right: 34, top: 0, background: PASTA, padding: '14px 28px 12px', borderRadius: '0 0 14px 14px',
    fontFamily: TYPE, fontSize: 30, color: TINTA, letterSpacing: 2, boxShadow: '4px 5px 0 rgba(0,0,0,.5)' }}>EXPEDIENTE Nº 015</div>
);

const Carimbo = ({ txt, fs, rot, pos }) => (
  <div style={{ position: 'absolute', transform: `rotate(${rot}deg)`, background: ROJO, border: `6px solid ${ROJO}`, outline: `3px solid ${PAPEL}`, outlineOffset: -14,
    padding: '10px 34px 4px', fontFamily: DISPLAY, fontSize: fs, color: PAPEL, letterSpacing: 4, whiteSpace: 'nowrap', boxShadow: '6px 8px 0 rgba(0,0,0,.5)', ...pos }}>{txt}</div>
);

const A = () => (
  <AbsoluteFill style={{ background: '#2E3A46' }}>
    <Img src={staticFile('img/thumb-A.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <Aba />
    <div style={{ position: 'absolute', left: 600, top: 150, fontFamily: DISPLAY, fontSize: 470, lineHeight: 1, color: PAPEL, letterSpacing: 6, whiteSpace: 'nowrap',
      textShadow: '8px 9px 0 rgba(0,0,0,.55)' }}>GRU</div>
    <Carimbo txt="GULAG" fs={96} rot={-8} pos={{ left: 40, top: 560 }} />
  </AbsoluteFill>
);

const B = () => (
  <AbsoluteFill style={{ background: '#1b222b' }}>
    <Img src={staticFile('img/thumb-B.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <Aba />
    <Carimbo txt="¿BRASILEÑO?" fs={138} rot={-5} pos={{ right: 14, bottom: 20 }} />
  </AbsoluteFill>
);

// Passaporte aberto: a base (nano-banana) traz rabiscos de letra nos campos; o código cobre os campos com papel/oliva,
// desenha linhas cinza ilegíveis e a zona de leitura mecânica (MRZ "P<…<<<<"), sem nome real. Coordenadas medidas na base 1344x768 → tela 1280x720.
const Campos = () => (
  <>
    <div style={{ position: 'absolute', left: 678, top: 236, width: 202, height: 235, background: '#E5DFCD' }} />
    <div style={{ position: 'absolute', left: 474, top: 424, width: 172, height: 84, background: '#6B7356' }} />
    {[262, 288, 314, 340, 374, 400, 426].map((y, i) => (
      <div key={y} style={{ position: 'absolute', left: 690, top: y, width: i % 3 === 0 ? 120 : 176, height: 4, background: 'rgba(55,50,42,.55)' }} />
    ))}
    {[446, 466, 486].map((y) => (
      <div key={y} style={{ position: 'absolute', left: 486, top: y, width: 140, height: 3, background: 'rgba(25,25,20,.45)' }} />
    ))}
    <div style={{ position: 'absolute', left: 676, top: 476, width: 208, height: 40, background: '#E5DFCD' }} />
    <div style={{ position: 'absolute', left: 680, top: 479, fontFamily: TYPE, fontWeight: 700, fontSize: 15.5, lineHeight: 1.22, letterSpacing: 0.4, color: 'rgba(30,28,24,.85)', whiteSpace: 'nowrap' }}>
      <div>P&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;</div>
      <div>&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;</div>
    </div>
  </>
);

const C = () => (
  <AbsoluteFill style={{ background: '#1d1a16' }}>
    <Img src={staticFile('img/thumb-C.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover' }} />
    <Campos />
    <div style={{ position: 'absolute', left: 858, top: 440, transform: 'rotate(-8deg)', background: ROJO, border: `7px solid ${ROJO}`, outline: `4px solid ${PAPEL}`, outlineOffset: -14,
      padding: '10px 36px 2px', fontFamily: DISPLAY, fontSize: 100, lineHeight: 0.98, textAlign: 'center', color: PAPEL, letterSpacing: 4, whiteSpace: 'nowrap', opacity: 0.96,
      boxShadow: '7px 9px 0 rgba(0,0,0,.55)' }}>NUNCA<br />NACIERON</div>
  </AbsoluteFill>
);

export const Thumbnail = ({ variante = 'A' }) => (variante === 'B' ? <B /> : variante === 'C' ? <C /> : <A />);
