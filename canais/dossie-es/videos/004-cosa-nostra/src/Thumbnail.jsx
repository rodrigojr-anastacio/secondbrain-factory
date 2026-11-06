import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { TYPE, DISPLAY, PAPEL, ROJO, TINTA, PASTA } from './Video.jsx';

// Layout "pôster de expediente" (canais/dossie-es/biblia/thumb.md): imagem à esquerda, SIGLA gigante à direita,
// sello rojo inclinado com o período e aba de pasta "EXPEDIENTE Nº 004" no canto superior direito.
// 004 Cosa Nostra · A: o chefe com a estampa queimando + "EL JURAMENTO" · B: o juiz com os autos + "ROMPIÓ EL SILENCIO" · C: o dedo nos lábios + faixa "UN SIGLO DE SILENCIO". Sem arma (brief).
const V = {
  A: { base: 'thumb-A.jpg', tinta: TINTA, extra: 'papel', papel: ['EL JURAMENTO'] },
  B: { base: 'thumb-B.jpg', tinta: PAPEL, extra: 'papel', papel: ['ROMPIÓ EL SILENCIO'] },
  C: { base: 'thumb-C.jpg', tinta: PAPEL, extra: 'faixa' },
};

export const Thumbnail = ({ variante = 'A' }) => {
  const v = V[variante] || V.A;
  return (
    <AbsoluteFill style={{ background: '#222' }}>
      <Img src={staticFile(`img/${v.base}`)} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      <div style={{ position: 'absolute', right: 34, top: 0, background: PASTA, padding: '14px 28px 12px', borderRadius: '0 0 14px 14px',
        fontFamily: TYPE, fontSize: 30, color: TINTA, letterSpacing: 2, boxShadow: '4px 5px 0 rgba(0,0,0,.5)' }}>EXPEDIENTE Nº 004</div>
      <div style={{ position: 'absolute', right: 24, top: 78, width: 700, textAlign: 'center' }}>
        <div style={{ fontFamily: DISPLAY, fontSize: 176, lineHeight: 0.86, color: v.tinta, letterSpacing: 4,
          textShadow: v.tinta === TINTA ? '0 0 24px rgba(255,255,255,.6)' : '0 6px 0 rgba(0,0,0,.6), 0 0 30px rgba(0,0,0,.6)' }}>COSA<br />NOSTRA</div>
        <div style={{ display: 'inline-block', marginTop: 18, transform: 'rotate(-7deg)', border: `8px solid ${ROJO}`, outline: `3px solid ${ROJO}`,
          outlineOffset: 5, padding: '4px 26px 0', fontFamily: DISPLAY, fontSize: 96, color: ROJO, letterSpacing: 4, background: 'rgba(233,223,201,.88)' }}>1860–1993</div>
        {v.extra === 'papel' && (
          <div style={{ marginTop: 26, background: PAPEL, padding: '8px 18px', fontFamily: TYPE, fontSize: 36, color: TINTA, lineHeight: 1.15,
            boxShadow: '5px 6px 0 rgba(0,0,0,.6)', transform: 'rotate(1deg)', display: 'inline-block' }}>{v.papel.map((l, i) => <div key={i}>{l}</div>)}</div>
        )}
      </div>
      {v.extra === 'faixa' && (
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 28, background: ROJO, padding: '10px 0 6px', textAlign: 'center',
          fontFamily: DISPLAY, fontSize: 80, color: PAPEL, letterSpacing: 6, boxShadow: '0 6px 0 rgba(0,0,0,.45)' }}>UN SIGLO DE SILENCIO</div>
      )}
    </AbsoluteFill>
  );
};
