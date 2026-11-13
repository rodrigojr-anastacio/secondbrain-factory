// 3 thumbs do longo 04 (1983, El Niño), compostas no código sobre quadros do próprio mapa 3D (cues.thumbs). Sem IA paga.
// A "MESMO ANO" (tela partida Sul água × sertão seco) · B "1983" (Brasil + Landsat de ago/1983) · C "1983 → 2026?" (diagonal sépia × cor)
import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { LongoV3 } from './LongoV3';
import cues from '../../shared/cues.json';
const C = { coral: '#E8505B', navy: '#1F2A44', branco: '#FBF8F1', tinta: '#2B2622', papel: '#E9DCC3', azul: '#4FA3D9' };
const sombra = '0 10px 0 rgba(20,30,60,0.45), 0 20px 50px rgba(0,0,0,0.6)';
const contorno = { WebkitTextStroke: '12px #1F2A44', paintOrder: 'stroke fill' };
const Selo = ({ style, cor, children }) => <div style={{ position: 'absolute', background: cor, color: C.branco, fontFamily: 'Anton', fontSize: 78, padding: '4px 30px 10px', boxShadow: '0 14px 34px rgba(0,0,0,0.55)', ...style }}>{children}</div>;
export const Thumb = ({ v }) => (
  <AbsoluteFill style={{ background: C.navy }}>
    {v === 'A' && <>
      <AbsoluteFill style={{ transform: 'scale(0.9) translate(9%, -2%)', transformOrigin: '50% 55%' }}><LongoV3 tempo={cues.thumbs.A} soMapa /></AbsoluteFill>
      <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(10,16,34,0.82) 0%, rgba(10,16,34,0.35) 38%, rgba(10,16,34,0) 60%)' }} />
      <div style={{ position: 'absolute', left: 60, top: 70, fontFamily: 'Anton', fontSize: 330, lineHeight: 0.92, color: C.branco, textShadow: sombra, ...contorno }}>MESMO<br />ANO</div>
      <Selo cor={C.azul} style={{ left: 1020, top: 760, transform: 'rotate(-3deg)' }}>ENCHENTE</Selo>
      <Selo cor={C.coral} style={{ right: 70, top: 250, transform: 'rotate(3deg)' }}>SECA</Selo>
      <div style={{ position: 'absolute', left: 70, top: 800 }}><div style={{ background: C.navy, color: C.branco, fontFamily: 'PlexMono', fontWeight: 700, fontSize: 110, padding: '4px 44px', letterSpacing: 10, boxShadow: '0 14px 34px rgba(0,0,0,0.55)', border: `6px solid ${C.coral}` }}>1983</div></div>
    </>}
    {v === 'B' && <>
      <AbsoluteFill style={{ opacity: 0 }}><LongoV3 tempo={cues.thumbs.B} soMapa /></AbsoluteFill>
      <AbsoluteFill><Img src={staticFile('fotos/landsat4-uv-19830804-par.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'saturate(1.35) contrast(1.12)' }} /></AbsoluteFill>
      <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(10,16,34,0.0) 0%, rgba(10,16,34,0.0) 40%, rgba(10,16,34,0.55) 100%)' }} />
      <div style={{ position: 'absolute', right: 40, top: 30, fontFamily: 'Anton', fontSize: 640, lineHeight: 0.95, color: C.coral, textShadow: sombra, ...contorno }}>1983</div>
      <div style={{ position: 'absolute', left: 60, top: 60, background: C.navy, color: C.branco, fontFamily: 'PlexMono', fontWeight: 700, fontSize: 52, padding: '8px 26px', letterSpacing: 4, boxShadow: '0 14px 34px rgba(0,0,0,0.55)' }}>SATÉLITE · AGO 1983</div>
      <div style={{ position: 'absolute', left: 60, top: 860, background: C.papel, color: C.navy, fontFamily: 'Anton', fontSize: 130, padding: '2px 34px 12px', transform: 'rotate(-2deg)', boxShadow: '0 20px 50px rgba(0,0,0,0.55)' }}>PARTIU O BRASIL</div>
    </>}
    {v === 'C' && <>
      <AbsoluteFill style={{ clipPath: 'polygon(0 0, 58% 0, 42% 100%, 0 100%)', filter: 'sepia(0.85) contrast(1.05)' }}><AbsoluteFill style={{ transform: 'translate(-27%, 0) scale(1.15)' }}><LongoV3 tempo={cues.thumbs.C0} soMapa /></AbsoluteFill></AbsoluteFill>
      <AbsoluteFill style={{ clipPath: 'polygon(58% 0, 100% 0, 100% 100%, 42% 100%)' }}><LongoV3 tempo={cues.thumbs.C1} soMapa /></AbsoluteFill>
      <svg style={{ position: 'absolute', left: 0, top: 0 }} width="1920" height="1080"><line x1={1113} y1={0} x2={806} y2={1080} stroke={C.branco} strokeWidth={10} /></svg>
      <AbsoluteFill style={{ background: 'linear-gradient(0deg, rgba(10,16,34,0.5) 0%, rgba(10,16,34,0) 45%)' }} />
      <div style={{ position: 'absolute', left: 60, top: 70, fontFamily: 'Anton', fontSize: 300, lineHeight: 0.95, color: '#EAD9B8', textShadow: sombra, ...contorno }}>1983</div>
      <div style={{ position: 'absolute', right: 60, top: 70, fontFamily: 'Anton', fontSize: 300, lineHeight: 0.95, color: C.coral, textShadow: sombra, ...contorno }}>2026</div>
      <div style={{ position: 'absolute', left: 800, top: 330, fontFamily: 'Anton', fontSize: 560, lineHeight: 1, color: C.branco, textShadow: sombra, ...contorno }}>?</div>
    </>}
  </AbsoluteFill>
);
