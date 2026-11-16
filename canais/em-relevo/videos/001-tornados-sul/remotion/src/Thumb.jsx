// 3 thumbs compostas no código (mapa 3D do próprio vídeo + quadro real + texto grande). Sem IA paga.
import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { Longo } from './Longo';
const C = { coral: '#E8505B', navy: '#1F2A44', branco: '#FBF8F1', tinta: '#2B2622' };
const Polaroid = ({ src, left, top, w, rot, legenda }) => (
  <div style={{ position: 'absolute', left, top, width: w, background: C.branco, padding: '18px 18px 0', transform: `rotate(${rot}deg)`, boxShadow: '0 30px 60px rgba(0,0,0,0.55)' }}>
    <Img src={staticFile(src)} style={{ width: w - 36, height: (w - 36) * 0.75, objectFit: 'cover', display: 'block' }} />
    <div style={{ fontFamily: 'PlexMono', fontWeight: 700, fontSize: 30, color: C.tinta, padding: '12px 4px 16px', letterSpacing: '0.06em' }}>{legenda}</div>
    <div style={{ position: 'absolute', left: w / 2 - 22, top: -16, width: 44, height: 44, borderRadius: 22, background: 'radial-gradient(circle at 35% 35%, #ff8a8f, #C9303B 60%)', boxShadow: '0 4px 10px rgba(0,0,0,0.5)' }} />
  </div>
);
export const Thumb = ({ v }) => {
  const mapa = { 1: 194.8, 2: 331, 3: 517 }[v];
  return (
    <AbsoluteFill>
      <Longo tempo={mapa} soMapa />
      <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(20,12,6,0.55) 0%, rgba(20,12,6,0.15) 55%, rgba(20,12,6,0) 100%)' }} />
      {v === 1 && <>
        <Polaroid src="img/q-chapeco-centro.jpg" left={1110} top={170} w={740} rot={3} legenda="CHAPECÓ · 04/11" />
        <div style={{ position: 'absolute', left: 70, top: 110, fontFamily: 'Anton', fontSize: 250, lineHeight: 0.9, color: C.coral, textShadow: '0 10px 0 rgba(60,20,20,0.35), 0 20px 50px rgba(0,0,0,0.5)' }}>7<br />TORNADOS</div>
        <div style={{ position: 'absolute', left: 80, top: 690, background: C.navy, color: C.branco, fontFamily: 'Anton', fontSize: 130, padding: '6px 34px', transform: 'rotate(-2deg)', boxShadow: '0 16px 40px rgba(0,0,0,0.5)' }}>EM 6 DIAS</div>
      </>}
      {v === 2 && <>
        <Polaroid src="img/q-santo-augusto-rua.jpg" left={1150} top={420} w={680} rot={-3} legenda="SANTO AUGUSTO · 07/11" />
        <div style={{ position: 'absolute', left: 70, top: 120, background: C.branco, color: C.tinta, fontFamily: 'Anton', fontSize: 210, lineHeight: 1, padding: '10px 40px 20px', transform: 'rotate(-2deg)', boxShadow: '0 20px 50px rgba(0,0,0,0.5)' }}>
          POR QUE<br /><span style={{ color: C.coral }}>AGORA?</span></div>
        <div style={{ position: 'absolute', left: 90, top: 690, background: C.coral, color: C.branco, fontFamily: 'Anton', fontSize: 92, padding: '4px 30px', boxShadow: '0 14px 30px rgba(0,0,0,0.45)' }}>TORNADOS NO SUL</div>
      </>}
      {v === 3 && <>
        <Polaroid src="img/q-rbi-rastro.jpg" left={1080} top={150} w={770} rot={3} legenda="RIO BONITO DO IGUAÇU · F4" />
        <div style={{ position: 'absolute', left: 70, top: 150, fontFamily: 'Anton', fontSize: 225, lineHeight: 0.92, color: C.branco, textShadow: '0 10px 0 rgba(0,0,0,0.35), 0 20px 50px rgba(0,0,0,0.6)' }}>VAI<br /><span style={{ color: C.coral }}>VOLTAR?</span></div>
        <div style={{ position: 'absolute', left: 80, top: 700, background: C.navy, color: C.branco, fontFamily: 'Anton', fontSize: 96, padding: '6px 30px', transform: 'rotate(-1.5deg)', boxShadow: '0 14px 30px rgba(0,0,0,0.45)' }}>O RISCO NO SUL</div>
      </>}
    </AbsoluteFill>
  );
};
