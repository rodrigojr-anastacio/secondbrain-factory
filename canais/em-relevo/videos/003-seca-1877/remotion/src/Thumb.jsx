// 3 thumbs do longo 03 (Grande Seca de 1877), compostas no código sobre quadros do próprio mapa 3D (cues.thumbs). Sem IA paga.
// A "500 MIL" (carte-de-visite + mapa) · B "MUDOU O MAPA" (fio Ceará → Acre) · C "1877 = 2026?" (diagonal sépia × cor)
import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { LongoV3 } from './LongoV3';
import cues from '../../shared/cues.json';
const C = { coral: '#E8505B', navy: '#1F2A44', branco: '#FBF8F1', tinta: '#2B2622', papel: '#E9DCC3' };
const sombra = '0 10px 0 rgba(60,20,20,0.4), 0 20px 50px rgba(0,0,0,0.6)';
const contorno = { WebkitTextStroke: '10px #1F2A44', paintOrder: 'stroke fill' };
const Tachinha = ({ left, top }) => <div style={{ position: 'absolute', left, top, width: 46, height: 46, borderRadius: 23, background: 'radial-gradient(circle at 35% 35%, #ff8a8f, #C9303B 60%)', boxShadow: '0 4px 10px rgba(0,0,0,0.5)' }} />;
export const Thumb = ({ v }) => (
  <AbsoluteFill style={{ background: C.navy }}>
    {v === 'A' && <>
      <LongoV3 tempo={cues.thumbs.A} soMapa />
      <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(20,12,6,0.55) 0%, rgba(20,12,6,0.15) 60%, rgba(20,12,6,0.45) 100%)' }} />
      <div style={{ position: 'absolute', left: 90, top: 190, width: 470, background: '#EFE3C8', padding: '22px 22px 70px', transform: 'rotate(-4deg)', boxShadow: '0 30px 60px rgba(0,0,0,0.6)', filter: 'sepia(0.35)' }}>
        <Img src={staticFile('fotos/retirantes-1878-grupo.jpg')} style={{ width: 426, display: 'block' }} />
        <div style={{ position: 'absolute', left: 22, bottom: 18, fontFamily: 'PlexMono', fontWeight: 700, fontSize: 30, color: '#4a3a2a' }}>CEARÁ · 1878</div>
        <Tachinha left={212} top={-18} />
      </div>
      <div style={{ position: 'absolute', right: 70, top: 120, textAlign: 'right', fontFamily: 'Anton', fontSize: 400, lineHeight: 0.92, color: C.coral, textShadow: sombra, ...contorno }}>500<br />MIL</div>
      <div style={{ position: 'absolute', right: 80, top: 800, background: C.navy, color: C.branco, fontFamily: 'PlexMono', fontWeight: 700, fontSize: 80, padding: '8px 34px', transform: 'rotate(-1.5deg)', boxShadow: '0 16px 40px rgba(0,0,0,0.5)' }}>ESQUECIDOS</div>
    </>}
    {v === 'B' && <>
      <LongoV3 tempo={cues.thumbs.B} soMapa />
      <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(20,12,6,0.55) 0%, rgba(20,12,6,0.1) 60%, rgba(20,12,6,0) 100%)' }} />
      <div style={{ position: 'absolute', left: 70, top: 60, fontFamily: 'Anton', fontSize: 330, lineHeight: 0.95, color: C.branco, textShadow: sombra, ...contorno }}>1877</div>
      <div style={{ position: 'absolute', left: 70, top: 760, background: C.papel, color: C.navy, fontFamily: 'Anton', fontSize: 170, padding: '4px 40px 14px', transform: 'rotate(-2deg)', boxShadow: '0 20px 50px rgba(0,0,0,0.55)' }}>MUDOU O MAPA<Tachinha left={20} top={-20} /></div>
    </>}
    {v === 'C' && <>
      <AbsoluteFill style={{ clipPath: 'polygon(0 0, 58% 0, 42% 100%, 0 100%)', filter: 'sepia(0.85) contrast(1.05)' }}><LongoV3 tempo={cues.thumbs.C0} soMapa /></AbsoluteFill>
      <AbsoluteFill style={{ clipPath: 'polygon(58% 0, 100% 0, 100% 100%, 42% 100%)' }}><LongoV3 tempo={cues.thumbs.C1} soMapa /></AbsoluteFill>
      <svg style={{ position: 'absolute', left: 0, top: 0 }} width="1920" height="1080"><line x1={1113} y1={0} x2={806} y2={1080} stroke={C.branco} strokeWidth={10} /></svg>
      <AbsoluteFill style={{ background: 'linear-gradient(0deg, rgba(20,12,6,0.5) 0%, rgba(20,12,6,0) 45%)' }} />
      <div style={{ position: 'absolute', left: 60, top: 70, fontFamily: 'Anton', fontSize: 300, lineHeight: 0.95, color: '#EAD9B8', textShadow: sombra, ...contorno }}>1877</div>
      <div style={{ position: 'absolute', right: 60, top: 70, fontFamily: 'Anton', fontSize: 300, lineHeight: 0.95, color: C.coral, textShadow: sombra, ...contorno }}>2026</div>
      <div style={{ position: 'absolute', left: 810, top: 330, fontFamily: 'Anton', fontSize: 560, lineHeight: 1, color: C.branco, textShadow: sombra, ...contorno }}>=?</div>
    </>}
  </AbsoluteFill>
);
