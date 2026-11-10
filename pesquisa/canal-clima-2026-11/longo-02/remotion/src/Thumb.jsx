// 3 thumbs do longo 02 (aprovadas na proposta de 09/11): É SUPER? · CHUVA × FOGO · ATÉ QUANDO?
// Compostas no código a partir de quadros do próprio vídeo (cues.thumbs = tempo do quadro de fundo) + polaroid de satélite. Sem IA paga.
import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { Longo } from './Longo';
import cues from '../../shared/cues.json';
const C = { coral: '#E8505B', navy: '#1F2A44', branco: '#FBF8F1', tinta: '#2B2622' };
const Polaroid = ({ src, left, top, w, rot, legenda }) => (
  <div style={{ position: 'absolute', left, top, width: w, background: C.branco, padding: '18px 18px 0', transform: `rotate(${rot}deg)`, boxShadow: '0 30px 60px rgba(0,0,0,0.55)' }}>
    <Img src={staticFile(src)} style={{ width: w - 36, height: (w - 36) * 0.75, objectFit: 'cover', display: 'block' }} />
    <div style={{ fontFamily: 'PlexMono', fontWeight: 700, fontSize: 34, color: C.tinta, padding: '12px 4px 16px', letterSpacing: '0.06em' }}>{legenda}</div>
    <div style={{ position: 'absolute', left: w / 2 - 22, top: -16, width: 44, height: 44, borderRadius: 22, background: 'radial-gradient(circle at 35% 35%, #ff8a8f, #C9303B 60%)', boxShadow: '0 4px 10px rgba(0,0,0,0.5)' }} />
  </div>
);
const Faixa = ({ texto, top = 760, left = 80, size = 84 }) => (
  <div style={{ position: 'absolute', left, top, background: C.navy, color: C.branco, fontFamily: 'PlexMono', fontWeight: 700, fontSize: size, letterSpacing: '0.06em', padding: '10px 34px', transform: 'rotate(-1.5deg)', boxShadow: '0 16px 40px rgba(0,0,0,0.5)' }}>{texto}</div>
);
const sombra = '0 10px 0 rgba(60,20,20,0.35), 0 20px 50px rgba(0,0,0,0.55)';
export const Thumb = ({ v }) => (
  <AbsoluteFill>
    <Longo tempo={cues.thumbs[String(v)]} soMapa />
    <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(20,12,6,0.6) 0%, rgba(20,12,6,0.2) 55%, rgba(20,12,6,0) 100%)' }} />
    {v === 1 && <>
      <Polaroid src="sat/pacifico-anomalia-nasa-2026-11-08.jpg" left={1150} top={150} w={700} rot={3} legenda="PACÍFICO · NOV/2026" />
      <div style={{ position: 'absolute', left: 70, top: 120, fontFamily: 'Anton', fontSize: 300, lineHeight: 0.9, color: C.coral, textShadow: sombra }}>É<br />SUPER?</div>
      <Faixa texto="EL NIÑO 2026" />
    </>}
    {v === 2 && <>
      <Polaroid src="sat/manaus-fumaca-2026-10-09-terra.jpg" left={1180} top={380} w={660} rot={-3} legenda="MANAUS · 09/10" />
      <div style={{ position: 'absolute', left: 60, top: 110, fontFamily: 'Anton', fontSize: 250, lineHeight: 0.95, textShadow: sombra }}>
        <span style={{ color: '#9CC3E4' }}>CHUVA</span><br /><span style={{ color: C.branco, fontSize: 200 }}>×</span> <span style={{ color: '#F2A07E' }}>FOGO</span></div>
      <svg style={{ position: 'absolute', left: 900, top: 60 }} width="260" height="560" viewBox="0 0 260 560"><path d="M170 0 L60 300 L140 300 L80 560 L230 220 L150 220 L220 0 Z" fill={C.coral} stroke={C.branco} strokeWidth="10" /></svg>
      <Faixa texto="O VERÃO DO EL NIÑO" top={800} size={72} />
    </>}
    {v === 3 && <>
      <Polaroid src="sat/sul-tempestade-2026-11-04-terra.jpg" left={1170} top={130} w={680} rot={3} legenda="SUL · 04/11/2026" />
      <div style={{ position: 'absolute', left: 70, top: 110, fontFamily: 'Anton', fontSize: 270, lineHeight: 0.9, color: C.branco, textShadow: sombra }}>ATÉ<br /><span style={{ color: C.coral }}>QUANDO?</span></div>
      <div style={{ position: 'absolute', left: 80, top: 790, display: 'flex', gap: 10, transform: 'rotate(-1deg)' }}>
        {['NOV', 'DEZ', 'JAN', 'FEV', 'MAR'].map((m) => (
          <div key={m} style={{ width: 190, padding: '12px 0', textAlign: 'center', fontFamily: 'Anton', fontSize: 70, background: m === 'DEZ' || m === 'JAN' ? C.coral : C.branco, color: m === 'DEZ' || m === 'JAN' ? C.branco : C.navy, boxShadow: '0 12px 30px rgba(0,0,0,0.45)', position: 'relative' }}>{m}
            {m === 'DEZ' && <div style={{ position: 'absolute', right: -22, top: -22, width: 44, height: 44, borderRadius: 22, background: 'radial-gradient(circle at 35% 35%, #ff8a8f, #C9303B 60%)' }} />}</div>))}
      </div>
      <div style={{ position: 'absolute', left: 80, top: 730, fontFamily: 'PlexMono', fontWeight: 700, fontSize: 40, color: C.branco, textShadow: '0 3px 8px #000' }}>SUPER EL NIÑO · PICO</div>
    </>}
  </AbsoluteFill>
);
