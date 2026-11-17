// 3 thumbs do 006 (Em Relevo), uma por conceito do EMBALAGEM.md (crivo r3): A mapa-lugar (bloco 3D do relevo, "UMA PAREDE?"),
// B antes-depois (Landsat 29/10/2022 × 26/02/2023, "UMA NOITE"), C cena-ação (foto real de Ubatuba, sem texto). Texto no código, US$ 0.
import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { Bloco3D } from './Cenas6.jsx';
import { useFontes } from './util6.js';
const C = { navy: '#1F2A44', branco: '#FBF8F1', amarelo: '#FFD23F', coral: '#E8505B' };
const contorno = { WebkitTextStroke: '14px #0E1426', paintOrder: 'stroke fill' };
const sombra = '0 10px 0 rgba(8,12,28,0.6), 0 24px 60px rgba(0,0,0,0.7)';
const Rec = ({ src, x, y, w, h, W = 960, H = 1080, filtro }) => { const s = W / w; return <div style={{ width: W, height: H, overflow: 'hidden', position: 'relative' }}><Img src={staticFile('fotos/' + src)} style={{ position: 'absolute', width: 1840 * s, height: 1227 * s, left: -x * s, top: -y * s, filter: filtro }} /></div>; };
export const Thumb = ({ v }) => {
  useFontes();
  if (v === 'A') return (
    <AbsoluteFill style={{ background: 'linear-gradient(180deg,#7FB8E6 0%,#CFE8F7 55%,#E9F3F8 100%)' }}>
      <div style={{ position: 'absolute', left: 150, top: 330, transform: 'scale(1.0)', filter: 'drop-shadow(0 30px 40px rgba(10,30,60,0.45))' }}>
        <Bloco3D chave="cruzeiro" W={1500} g={1} rp={0} exag={4.2} faceCor="#C9B58E" />
      </div>
      <svg width={1920} height={1080} style={{ position: 'absolute', left: 0, top: 0 }}>
        <path d="M 250 860 C 330 960, 520 960, 600 880" fill="none" stroke={C.coral} strokeWidth={22} strokeLinecap="round" />
        <polygon points="610,845 640,905 570,895" fill={C.coral} transform="rotate(8 600 880)" />
        <circle cx={250} cy={860} r={20} fill={C.coral} stroke="#fff" strokeWidth={6} />
      </svg>
      <div style={{ position: 'absolute', left: 60, top: 14, fontFamily: 'Anton', fontSize: 300, lineHeight: 0.95, color: C.branco, textShadow: sombra, ...contorno }}>UMA</div>
      <div style={{ position: 'absolute', left: 60, top: 270, fontFamily: 'Anton', fontSize: 300, lineHeight: 0.95, color: C.amarelo, textShadow: sombra, ...contorno }}>PAREDE?</div>
      <div style={{ position: 'absolute', right: 24, bottom: 14, fontFamily: 'Anton', fontSize: 30, color: 'rgba(20,30,50,0.7)', letterSpacing: 2 }}>ILUSTRATIVO</div>
    </AbsoluteFill>
  );
  if (v === 'B') {
    const f = 'contrast(1.18) brightness(1.2) saturate(1.2)';
    return (
      <AbsoluteFill style={{ background: '#000' }}>
        <div style={{ position: 'absolute', left: 0, top: 0 }}><Rec src="satelite/nasa-eo-landsat9-sao-sebastiao-antes-2022-10-29.jpg" x={770} y={690} w={250} h={281} filtro={f} /></div>
        <div style={{ position: 'absolute', left: 960, top: 0 }}><Rec src="satelite/nasa-eo-landsat8-sao-sebastiao-depois-2023-02-26.jpg" x={770} y={690} w={250} h={281} filtro={f} /></div>
        <div style={{ position: 'absolute', left: 954, top: 0, width: 12, height: 1080, background: C.branco }} />
        <div style={{ position: 'absolute', left: 0, top: 60, width: '100%', display: 'flex', justifyContent: 'center' }}>
          <div style={{ background: C.coral, color: C.branco, fontFamily: 'Anton', fontSize: 210, padding: '0 50px', lineHeight: 1.15, border: '10px solid #fff', boxShadow: '0 20px 50px rgba(0,0,0,0.6)', transform: 'rotate(-3deg)' }}>UMA NOITE</div>
        </div>
        <div style={{ position: 'absolute', left: 30, bottom: 26, fontFamily: 'Anton', fontSize: 62, color: C.branco, ...{ WebkitTextStroke: '8px #0E1426', paintOrder: 'stroke fill' } }}>ANTES</div>
        <div style={{ position: 'absolute', right: 30, bottom: 26, fontFamily: 'Anton', fontSize: 62, color: C.amarelo, ...{ WebkitTextStroke: '8px #0E1426', paintOrder: 'stroke fill' } }}>DEPOIS</div>
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{ background: '#000' }}>
      <Img src={staticFile('fotos/video/ubatuba-encosta-arrancada-estrada-2023-02-19.jpg')} style={{ position: 'absolute', width: 2000, height: 1500, left: -40, top: -330, filter: 'contrast(1.1) saturate(1.15)' }} />
      <AbsoluteFill style={{ background: 'linear-gradient(215deg, rgba(8,14,10,0.97) 0%, rgba(8,14,10,0.9) 14%, rgba(8,14,10,0) 42%)' }} />
    </AbsoluteFill>
  );
};
