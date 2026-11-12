import React from 'react';
import { AbsoluteFill, Img, staticFile, interpolate, useCurrentFrame, Easing } from 'remotion';
import { DISPLAY, MONO, COND, AMARELO, CIANO, TINTA, PAPEL, GRIFO } from './estilo.jsx';
import mapa from './mapa.json';

const ease = Easing.bezier(0.45, 0, 0.2, 1);
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };

// Ficha de arquivo: a legenda fixa do canal (data · lugar · fonte), em mono, canto inferior esquerdo.
export const Ficha = ({ linhas, inicio = 12 }) => {
  const f = useCurrentFrame();
  const op = interpolate(f, [inicio, inicio + 12], [0, 1], clamp);
  const x = interpolate(f, [inicio, inicio + 12], [-30, 0], { ...clamp, easing: ease });
  return (
    <div style={{ position: 'absolute', left: 60, bottom: 56, opacity: op, transform: `translateX(${x}px)`,
      background: 'rgba(17,20,24,.86)', borderLeft: `6px solid ${AMARELO}`, padding: '12px 22px 12px 18px' }}>
      {linhas.map((l, i) => (
        <div key={i} style={{ fontFamily: MONO, fontSize: i === 0 ? 34 : 24, color: i === 0 ? '#fff' : '#C9CDD2', letterSpacing: 1.5,
          fontWeight: i === 0 ? 700 : 400, lineHeight: 1.35 }}>{l}</div>
      ))}
    </div>
  );
};

// F1 · documento real com zoom até a linha e grifo amarelo (assinatura do canal).
// NARA, CINCPAC "Battle of Midway" (Enc A-F), 28/06/1942, p. 1: catalog.archives.gov/id/133919628 (Unrestricted).
export const DocGrifo = () => {
  const f = useCurrentFrame();
  const PW = 4480, PH = 5458, H0 = 1000, W0 = (H0 * PW) / PH; // página inteira na tela
  const foco = { x: 0.595, y: 0.7205 };                          // centro da linha "(a) 4 CV sunk - AKAGI, KAGA, SORYU, HIRYU"
  const z = interpolate(f, [18, 105], [1, 2.3], { ...clamp, easing: ease });
  const k = interpolate(f, [18, 105], [0, 1], { ...clamp, easing: ease });
  // scale(z) translate(tx,ty) com origem no centro: o foco vai para 40% da altura da tela
  const tx = k * (0.5 - foco.x) * W0;
  const ty = k * ((0.5 - foco.y) * H0 - (0.1 * 1080) / z);
  const grifo = interpolate(f, [112, 150], [0, 1], { ...clamp, easing: ease });
  const num = interpolate(f, [160, 176], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, #2a2f36 0%, #0c0e11 75%)' }}>
      <div style={{ position: 'absolute', left: '50%', top: '50%', width: W0, height: H0,
        marginLeft: -W0 / 2, marginTop: -H0 / 2, transform: `scale(${z}) translate(${tx}px, ${ty}px)`, transformOrigin: '50% 50%',
        boxShadow: '0 30px 80px rgba(0,0,0,.7)' }}>
        <Img src={staticFile('img/nara_0372.jpg')} style={{ width: '100%', height: '100%', filter: 'sepia(.18) contrast(1.08)' }} />
        <div style={{ position: 'absolute', left: `${0.318 * 100}%`, top: `${0.709 * 100}%`, height: `${0.024 * 100}%`,
          width: `${0.555 * 100 * grifo}%`, background: GRIFO, mixBlendMode: 'multiply', borderRadius: 3 }} />
      </div>
      <div style={{ position: 'absolute', right: 60, bottom: 56, opacity: num, transform: `scale(${0.9 + 0.1 * num})`, textAlign: 'right', background: 'rgba(17,20,24,.88)', padding: '18px 30px 14px', borderRight: `6px solid ${AMARELO}` }}>
        <div style={{ fontFamily: DISPLAY, fontSize: 120, color: AMARELO, lineHeight: 0.95 }}>4 CARRIERS</div>
        <div style={{ fontFamily: COND, fontWeight: 700, fontSize: 52, color: '#fff', letterSpacing: 3, textShadow: '0 3px 0 rgba(0,0,0,.7)' }}>ALL HIT IN ONE DAY</div>
      </div>
      <Ficha linhas={['SECRET · JUNE 28, 1942', 'Nimitz to the fleet: "Battle of Midway"', 'U.S. National Archives · RG 38']} inicio={20} />
    </AbsoluteFill>
  );
};

// F2 · então × agora: a mesma estrutura, 1942 e 2022, com cortina vertical e rótulos de data.
// NHHC/Commons "Damaged Midway seaplane hangar 1942" (PD) × USFWS "Midway seaplane hangar collapse" 2022 (PD).
export const EntaoAgora = () => {
  const f = useCurrentFrame();
  const z1 = interpolate(f, [0, 240], [1.04, 1.16]);
  const z2 = interpolate(f, [0, 240], [1.14, 1.04]);
  const corte = interpolate(f, [92, 150], [0, 100], { ...clamp, easing: ease }); // % revelado do "agora"
  const lab = (txt, cor, op, lado) => (
    <div style={{ position: 'absolute', top: 60, [lado]: 60, opacity: op, fontFamily: DISPLAY, fontSize: 96, color: cor,
      textShadow: '0 5px 0 rgba(0,0,0,.65), 0 0 24px rgba(0,0,0,.5)', letterSpacing: 2 }}>{txt}</div>
  );
  return (
    <AbsoluteFill style={{ background: TINTA, overflow: 'hidden' }}>
      <Img src={staticFile('img/hangar1942.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover',
        transform: `scale(${z1})`, filter: 'grayscale(1) contrast(1.1)' }} />
      <div style={{ position: 'absolute', inset: 0, clipPath: `inset(0 ${100 - corte}% 0 0)` }}>
        <Img src={staticFile('img/hangar2022.jpg')} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover',
          transform: `scale(${z2})` }} />
      </div>
      {corte > 0 && corte < 100 && (
        <div style={{ position: 'absolute', top: 0, bottom: 0, left: `${corte}%`, width: 6, marginLeft: -3, background: AMARELO,
          boxShadow: '0 0 18px rgba(253,213,5,.8)' }} />
      )}
      {lab('JUNE 4, 1942', '#fff', interpolate(f, [10, 22, 95, 115], [0, 1, 1, 0], clamp), 'left')}
      {lab('2022', AMARELO, interpolate(f, [140, 155], [0, 1], clamp), 'right')}
      {f < 92 && <Ficha linhas={['SEAPLANE HANGAR · SAND ISLAND', 'After the Japanese air raid', 'U.S. Navy · NHHC (public domain)']} inicio={18} />}
      {f >= 150 && <Ficha linhas={['THE SAME HANGAR · 2022', 'Roof collapsed, 80 years later', 'U.S. Fish & Wildlife Service (public domain)']} inicio={152} />}
    </AbsoluteFill>
  );
};

// F3 · mapa 2D simples (Natural Earth, PD) com a linha Honolulu → Midway e o número, depois a foto aérea de 1941 em Ken Burns.
export const MapaKenBurns = () => {
  const f = useCurrentFrame();
  const { Honolulu: H, Midway: M, Tokyo: T } = mapa.pontos;
  const comp = Math.hypot(M[0] - H[0], M[1] - H[1]);
  const linha = interpolate(f, [24, 70], [0, 1], { ...clamp, easing: ease });
  const milhas = Math.round(interpolate(f, [24, 70], [0, 1200], { ...clamp, easing: ease }));
  const zm = interpolate(f, [0, 110], [1, 1.12], { ...clamp, easing: ease });
  const fotoOp = interpolate(f, [104, 124], [0, 1], clamp);
  const zf = interpolate(f, [104, 240], [1.08, 1.32]);
  const ponto = (p, nome, cor, op = 1, dir = 1) => (
    <g opacity={op}>
      <circle cx={p[0]} cy={p[1]} r={11} fill={cor} stroke={TINTA} strokeWidth={3} />
      <text x={p[0] + 20 * dir} y={p[1] - 16} fill="#fff" fontFamily={COND} fontWeight={700} fontSize={40} textAnchor={dir > 0 ? 'start' : 'end'}
        style={{ paintOrder: 'stroke', stroke: TINTA, strokeWidth: 6 }}>{nome}</text>
    </g>
  );
  return (
    <AbsoluteFill style={{ background: '#0E2A3B', overflow: 'hidden' }}>
      <AbsoluteFill style={{ transform: `scale(${zm})`, transformOrigin: `${(M[0] / 1920) * 100}% ${(M[1] / 1080) * 100}%` }}>
        <svg width={1920} height={1080}>
          {mapa.paths.map((d, i) => <path key={i} d={d} fill="#D9CBA8" stroke="#8C7A57" strokeWidth={1} />)}
          <line x1={H[0]} y1={H[1]} x2={M[0]} y2={M[1]} stroke={AMARELO} strokeWidth={6} strokeDasharray={comp} strokeDashoffset={comp * (1 - linha)} strokeLinecap="round" />
          {ponto(T, 'TOKYO', '#C9CDD2', interpolate(f, [8, 18], [0, 1], clamp))}
          {ponto(H, 'HONOLULU', '#fff', interpolate(f, [8, 18], [0, 1], clamp), -1)}
          {ponto(M, 'MIDWAY', CIANO, interpolate(f, [60, 72], [0, 1], clamp), -1)}
        </svg>
      </AbsoluteFill>
      <div style={{ position: 'absolute', right: 90, top: 80, textAlign: 'right', opacity: interpolate(f, [24, 34, 100, 112], [0, 1, 1, 0], clamp) }}>
        <div style={{ fontFamily: DISPLAY, fontSize: 170, color: AMARELO, lineHeight: 0.95, textShadow: '0 6px 0 rgba(0,0,0,.6)' }}>{milhas.toLocaleString('en-US')}+ MILES</div>
        <div style={{ fontFamily: COND, fontWeight: 700, fontSize: 50, color: '#fff', letterSpacing: 3 }}>FROM THE NEAREST CITY</div>
      </div>
      <AbsoluteFill style={{ opacity: fotoOp }}>
        <Img src={staticFile('img/aerea1941.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 45%',
          transform: `scale(${zf})`, filter: 'grayscale(1) contrast(1.12)' }} />
      </AbsoluteFill>
      {f > 118 && <Ficha linhas={['MIDWAY ATOLL · NOV 24, 1941', 'Thirteen days before Pearl Harbor', 'U.S. Navy · NARA 80-G-451086']} inicio={126} />}
    </AbsoluteFill>
  );
};
