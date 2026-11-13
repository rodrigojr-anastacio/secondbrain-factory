import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { TYPE, DISPLAY, PAPEL, ROJO, TINTA, PASTA } from './Video.jsx';

// Layout "pôster de expediente" (canais/dossie-es/biblia/thumb.md): imagem à esquerda, palavra gigante à direita,
// sello rojo inclinado e aba de pasta "EXPEDIENTE Nº 008" no canto superior direito. Sem fogo com gente, capuz pontudo nem tortura.
// 008 La Inquisición (pareadas com os títulos do pacote): A (fórmula) inquisidor com o pergaminho lacrado + "INQUISICIÓN" + sello 1478–1834 ·
// B (por dentro) vizinho cochichando com o bilhete + "POR DENTRO" + papel "DENUNCIA" · C (lado oculto en América) Maldonado de sambenito + "AMÉRICA" + sello SANTO OFICIO.
const V = {
  A: { base: 'thumb-A.jpg', tinta: PAPEL, palavra: 'INQUISICIÓN', size: 168, sello: '1478–1834' },
  B: { base: 'thumb-B.jpg', tinta: PAPEL, palavra: 'POR DENTRO', size: 190, sello: '1478–1834', papel: ['DENUNCIA'] },
  C: { base: 'thumb-C.jpg', tinta: TINTA, palavra: 'AMÉRICA', size: 220, sello: 'SANTO OFICIO' },
};

export const Thumbnail = ({ variante = 'A' }) => {
  const v = V[variante] || V.A;
  return (
    <AbsoluteFill style={{ background: '#222' }}>
      <Img src={staticFile(`img/${v.base}`)} style={{ width: '100%', height: '100%', objectFit: 'cover', transform: v.flip ? 'scaleX(-1)' : 'none' }} />
      <div style={{ position: 'absolute', right: 34, top: 0, background: PASTA, padding: '14px 28px 12px', borderRadius: '0 0 14px 14px',
        fontFamily: TYPE, fontSize: 30, color: TINTA, letterSpacing: 2, boxShadow: '4px 5px 0 rgba(0,0,0,.5)' }}>EXPEDIENTE Nº 008</div>
      <div style={{ position: 'absolute', right: 24, top: 90, width: 720, textAlign: 'center' }}>
        <div style={{ fontFamily: DISPLAY, fontSize: v.size, lineHeight: 0.95, color: v.tinta, letterSpacing: 3, whiteSpace: 'nowrap',
          textShadow: v.tinta === TINTA ? '0 0 24px rgba(255,255,255,.7)' : '0 6px 0 rgba(0,0,0,.6), 0 0 30px rgba(0,0,0,.6)' }}>{v.palavra}</div>
        <div style={{ display: 'inline-block', marginTop: 18, transform: 'rotate(-7deg)', border: `8px solid ${ROJO}`, outline: `3px solid ${ROJO}`,
          outlineOffset: 5, padding: '4px 26px 0', fontFamily: DISPLAY, fontSize: 92, color: ROJO, letterSpacing: 4, background: 'rgba(233,223,201,.88)' }}>{v.sello}</div>
        {v.papel && (
          <div style={{ marginTop: 26, background: PAPEL, padding: '8px 18px', fontFamily: TYPE, fontSize: 60, color: TINTA, lineHeight: 1.1,
            boxShadow: '5px 6px 0 rgba(0,0,0,.6)', transform: 'rotate(1deg)', display: 'table', margin: '30px auto 0' }}>{v.papel.map((l, i) => <div key={i}>{l}</div>)}</div>
        )}
      </div>
    </AbsoluteFill>
  );
};
