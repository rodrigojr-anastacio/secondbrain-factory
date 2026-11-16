// 3 thumbs do longo 05 (enchente de 2024, Porto Alegre), compostas no código sobre quadros do próprio mapa 3D (cues.thumbs). Sem IA paga.
// Conceito aprovado no crivo (EMBALAGEM.md): maquete escura do RS, árvore de rios ciano grossa convergindo num ponto luminoso em frente a Porto Alegre,
// "1/3 DO ESTADO?" (1/3 enorme amarelo + DO ESTADO? branco). A = conceito base · B = câmera mais baixa e ponto do Guaíba maior · C = "UM TERÇO?".
import React from 'react';
import { AbsoluteFill } from 'remotion';
import { LongoV5 } from './LongoV5';
import cues from '../../shared/cues.json';
const C = { navy: '#1F2A44', branco: '#FBF8F1', amarelo: '#FFD23F', ciano: '#3FD8FF' };
const contorno = { WebkitTextStroke: '14px #0E1426', paintOrder: 'stroke fill' };
const sombra = '0 10px 0 rgba(8,12,28,0.6), 0 24px 60px rgba(0,0,0,0.7)';
const Fundo = ({ t, desloca = '0%,0%', escala = 1.12 }) => (
  <>
    <AbsoluteFill style={{ background: '#101830' }} />
    <AbsoluteFill style={{ transform: `scale(${escala}) translate(${desloca})`, transformOrigin: '50% 50%' }}><LongoV5 tempo={t} soMapa /></AbsoluteFill>
    <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 62% 55%, rgba(10,16,34,0) 25%, rgba(10,16,34,0.55) 80%)' }} />
  </>
);
export const Thumb = ({ v }) => (
  <AbsoluteFill style={{ background: C.navy }}>
    {v === 'A' && <>
      <Fundo t={cues.thumbs.A} desloca="6%,3%" />
      <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(8,12,28,0.78) 0%, rgba(8,12,28,0.3) 36%, rgba(8,12,28,0) 55%)' }} />
      <div style={{ position: 'absolute', left: 50, top: 24, fontFamily: 'Anton', fontSize: 560, lineHeight: 0.95, color: C.amarelo, textShadow: sombra, ...contorno }}>1/3</div>
      <div style={{ position: 'absolute', left: 60, top: 590, fontFamily: 'Anton', fontSize: 190, lineHeight: 1, color: C.branco, textShadow: sombra, ...contorno }}>DO ESTADO?</div>
    </>}
    {v === 'B' && <>
      <Fundo t={cues.thumbs.B} desloca="4%,5%" escala={1.15} />
      <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(8,12,28,0.78) 0%, rgba(8,12,28,0.3) 36%, rgba(8,12,28,0) 55%)' }} />
      <div style={{ position: 'absolute', left: 50, top: 24, fontFamily: 'Anton', fontSize: 560, lineHeight: 0.95, color: C.amarelo, textShadow: sombra, ...contorno }}>1/3</div>
      <div style={{ position: 'absolute', left: 60, top: 590, fontFamily: 'Anton', fontSize: 190, lineHeight: 1, color: C.branco, textShadow: sombra, ...contorno }}>DO ESTADO?</div>
    </>}
    {v === 'C' && <>
      <Fundo t={cues.thumbs.A} desloca="6%,3%" />
      <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(8,12,28,0.78) 0%, rgba(8,12,28,0.3) 36%, rgba(8,12,28,0) 55%)' }} />
      <div style={{ position: 'absolute', left: 50, top: 40, fontFamily: 'Anton', fontSize: 330, lineHeight: 0.98, color: C.amarelo, textShadow: sombra, ...contorno }}>UM</div>
      <div style={{ position: 'absolute', left: 50, top: 340, fontFamily: 'Anton', fontSize: 330, lineHeight: 0.98, color: C.branco, textShadow: sombra, ...contorno }}>TERÇO?</div>
    </>}
  </AbsoluteFill>
);
