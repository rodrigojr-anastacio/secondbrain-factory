import React from 'react';
import { AbsoluteFill, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame } from 'remotion';
import { Audio } from '@remotion/media';
import { loadFont as loadCaslon } from '@remotion/google-fonts/LibreCaslonText';
import timeline from './timeline.json';
import { LABELS } from './labels.jsx';

const caslon = loadCaslon('normal', { weights: ['400', '700'], subsets: ['latin', 'latin-ext'] });
const SERIF = `${caslon.fontFamily}, serif`;

const W = 1920, H = 1080;
const IMG_H = W * (1024 / 1536);   // imagens 3:2 cobrem pela largura
const XF = 5;                       // crossfade curto (frames) na troca de bloco
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const SOFT = Easing.bezier(0.45, 0, 0.55, 1);
const EASE = Easing.bezier(0.16, 1, 0.3, 1);
const INK = '#1d1710';
const PAPER = '#f4ead2';

// enquadramento → [zoom inicial, zoom final, foco x0, y0, x1, y1] (foco em fração da imagem)
const ENQ = {
  'médio-esq': [1.38, 1.42, 0.24, 0.5, 0.36, 0.5],
  'médio-dir': [1.42, 1.38, 0.76, 0.5, 0.64, 0.5],
  'detalhe-centro': [1.55, 1.68, 0.5, 0.5, 0.5, 0.5],
  'detalhe-alto': [1.6, 1.6, 0.5, 0.28, 0.5, 0.38],
  'detalhe-baixo': [1.6, 1.6, 0.5, 0.74, 0.5, 0.64],
};
// planos novos (aberto) variam pelo movimento do storyboard
const MOV = {
  'zoom-in lento': [1.0, 1.1, 0.5, 0.5, 0.5, 0.5],
  'zoom-out lento': [1.12, 1.0, 0.5, 0.5, 0.5, 0.5],
  'pan esq→dir': [1.14, 1.14, 0.3, 0.5, 0.7, 0.5],
  'pan dir→esq': [1.14, 1.14, 0.7, 0.5, 0.3, 0.5],
  'push-in leve': [1.04, 1.16, 0.5, 0.45, 0.5, 0.5],
  'tilt ↓ lento': [1.12, 1.12, 0.5, 0.3, 0.5, 0.7],
};
const kb = (s) => (s.enq !== 'aberto' && ENQ[s.enq]) || MOV[s.mov] || MOV['zoom-in lento'];

const Shot = ({ s, fade }) => {
  const f = useCurrentFrame();
  const [z0, z1, x0, y0, x1, y1] = kb(s);
  const p = interpolate(f, [0, s.dur + XF], [0, 1], { ...clamp, easing: SOFT });
  const z = z0 + (z1 - z0) * p, fx = x0 + (x1 - x0) * p, fy = y0 + (y1 - y0) * p;
  const w = W * z, h = IMG_H * z;
  const left = Math.min(0, Math.max(W - w, W / 2 - fx * w));
  const top = Math.min(0, Math.max(H - h, H / 2 - fy * h));
  const o = fade ? interpolate(f, [0, XF], [0, 1], clamp) : 1;
  const labels = LABELS[s.chave] || [];
  return (
    <AbsoluteFill style={{ opacity: o, overflow: 'hidden', background: '#000' }}>
      <div style={{ position: 'absolute', left, top, width: w, height: h }}>
        <Img src={staticFile(`img/${s.img}.jpg`)} style={{ width: '100%', height: '100%' }} />
        {labels.map((l, i) => <MapLabel key={i} l={l} z={z} f={f} i={i} />)}
      </div>
    </AbsoluteFill>
  );
};

// rótulo de mapa: serifa escura com contorno claro, posicionado em fração da imagem
const MapLabel = ({ l, z, f, i }) => {
  const a = interpolate(f, [6 + i * 6, 18 + i * 6], [0, 1], { ...clamp, easing: EASE });
  const size = (l.size || 44) / Math.sqrt(z);
  return (
    <div style={{ position: 'absolute', left: `${l.x * 100}%`, top: `${l.y * 100}%`, transform: `translate(-50%, -50%) scale(${0.9 + 0.1 * a})`,
      opacity: a, fontFamily: SERIF, fontWeight: 700, fontSize: size * z, color: l.color || INK, whiteSpace: 'nowrap', letterSpacing: 2,
      background: 'rgba(244,234,210,.92)', border: `${3 * Math.sqrt(z)}px solid ${INK}`, borderRadius: 8 * z, padding: `${0.1 * size * z}px ${0.4 * size * z}px` }}>{l.t}</div>
  );
};

// rótulo de nome/lugar (texto na tela, padrão Archive in Minutes): placa de papiro no canto inferior esquerdo
const NameTag = ({ text, dur }) => {
  const f = useCurrentFrame();
  const a = interpolate(f, [3, 13], [0, 1], { ...clamp, easing: EASE });
  const out = interpolate(f, [dur - 7, dur], [1, 0], clamp);
  return (
    <div style={{ position: 'absolute', left: 70, bottom: 70, opacity: a * out, transform: `translateX(${(1 - a) * -24}px)`,
      background: PAPER, border: `4px solid ${INK}`, borderRadius: 10, padding: '8px 28px 11px', boxShadow: '6px 6px 0 rgba(29,23,16,.85)' }}>
      <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 52, color: INK, letterSpacing: 1.5, whiteSpace: 'nowrap' }}>{text}</div>
    </div>
  );
};

// cartão de data: placa de papiro no canto superior esquerdo
const DateCard = ({ text, dur }) => {
  const f = useCurrentFrame();
  const a = interpolate(f, [0, 10], [0, 1], { ...clamp, easing: EASE });
  const out = interpolate(f, [dur - 8, dur], [1, 0], clamp);
  return (
    <div style={{ position: 'absolute', left: 70, top: 60, opacity: a * out, transform: `translateY(${(1 - a) * -16}px)`,
      background: PAPER, border: `4px solid ${INK}`, borderRadius: 10, padding: '10px 34px 14px', boxShadow: '6px 6px 0 rgba(29,23,16,.85)' }}>
      <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 72, color: INK, letterSpacing: 1 }}>{text}</div>
    </div>
  );
};

// título de capítulo: faixa clara embaixo, serifa
const ChapterTitle = ({ title, dur }) => {
  const f = useCurrentFrame();
  const m = title.match(/^(\d+)\.\s*(.*)$/);
  if (!m) return null;
  const a = interpolate(f, [4, 18], [0, 1], { ...clamp, easing: EASE });
  const out = interpolate(f, [dur - 10, dur], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 90, opacity: a * out }}>
      <div style={{ background: PAPER, border: `4px solid ${INK}`, borderRadius: 12, padding: '14px 56px 20px', textAlign: 'center',
        boxShadow: '8px 8px 0 rgba(29,23,16,.85)', transform: `translateY(${(1 - a) * 30}px)` }}>
        <div style={{ fontFamily: SERIF, fontSize: 34, letterSpacing: 8, color: '#7a5a2a' }}>CAPÍTULO {m[1]}</div>
        <div style={{ fontFamily: SERIF, fontWeight: 700, fontSize: 70, color: INK }}>{m[2]}</div>
      </div>
    </AbsoluteFill>
  );
};

export const Ira = () => {
  const { shots, cards, chapters } = timeline;
  return (
    <AbsoluteFill style={{ background: '#000' }}>
      {shots.map((s, i) => {
        const fade = i > 0 && shots[i - 1].bloco !== s.bloco;   // crossfade só na troca de bloco; dentro do bloco, corte seco
        const nextFade = i < shots.length - 1 && shots[i + 1].bloco !== s.bloco;
        return (
          <Sequence key={i} from={s.from} durationInFrames={s.dur + (nextFade ? XF : 0)} premountFor={30}>
            <Shot s={s} fade={fade} />
          </Sequence>
        );
      })}
      {shots.filter((s) => s.rot).map((s, i) => (
        <Sequence key={`r${i}`} from={s.from} durationInFrames={Math.max(30, s.dur)}><NameTag text={s.rot} dur={Math.max(30, s.dur)} /></Sequence>
      ))}
      {cards.map((c, i) => (
        <Sequence key={`c${i}`} from={c.from + 6} durationInFrames={78}><DateCard text={c.text} dur={78} /></Sequence>
      ))}
      {chapters.map((c, i) => (
        <Sequence key={`k${i}`} from={c.from + 8} durationInFrames={96}><ChapterTitle title={c.title} dur={96} /></Sequence>
      ))}
      <Audio src={staticFile('audio/mix.wav')} />
    </AbsoluteFill>
  );
};
