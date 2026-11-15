import React from 'react';
import { AbsoluteFill, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame } from 'remotion';
import { Audio } from '@remotion/media';
import { loadFont as loadElite } from '@remotion/google-fonts/SpecialElite';
import { loadFont as loadBebas } from '@remotion/google-fonts/BebasNeue';
import timeline from './timeline.json';
import { LABELS } from './labels.jsx';

// Identidade do Dossier en Minutos (canais/dossie-es/estilo.md e identidade.md):
// papel #E9DFC9, sello rojo #B3261E, tinta #1A1A1A, pasta parda; Special Elite (máquina de escrever) e Bebas Neue (títulos).
const elite = loadElite('normal', { weights: ['400'], subsets: ['latin', 'latin-ext'] });
const bebas = loadBebas('normal', { weights: ['400'], subsets: ['latin', 'latin-ext'] });
export const TYPE = `${elite.fontFamily}, 'Courier New', monospace`;
export const DISPLAY = `${bebas.fontFamily}, Impact, sans-serif`;
export const PAPEL = '#E9DFC9', ROJO = '#B3261E', TINTA = '#1A1A1A', PASTA = '#C8A46A', PASTA_ESC = '#9C7A43';

const W = 1920, H = 1080;
const IMG_H = W * (768 / 1344);    // nano-banana 16:9 (1344x768) cobre a tela inteira
const XF = 5;                       // crossfade curto (frames) na troca de bloco
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const SOFT = Easing.bezier(0.45, 0, 0.55, 1);
const EASE = Easing.bezier(0.16, 1, 0.3, 1);

// enquadramento → [zoom inicial, zoom final, foco x0, y0, x1, y1]. Zooms menores que no historia-ptbr:
// a base tem 1344 px de largura (o 003 provou que zoom alto em imagem pequena borra).
const ENQ = {
  'médio-esq': [1.24, 1.28, 0.26, 0.5, 0.36, 0.5],
  'médio-dir': [1.28, 1.24, 0.74, 0.5, 0.64, 0.5],
  'detalhe-centro': [1.34, 1.44, 0.5, 0.5, 0.5, 0.5],
  'detalhe-alto': [1.38, 1.38, 0.5, 0.3, 0.5, 0.38],
  'detalhe-baixo': [1.38, 1.38, 0.5, 0.72, 0.5, 0.64],
};
const MOV = {
  'zoom-in lento': [1.0, 1.1, 0.5, 0.5, 0.5, 0.5],
  'zoom-out lento': [1.1, 1.0, 0.5, 0.5, 0.5, 0.5],
  'pan esq→dir': [1.12, 1.12, 0.3, 0.5, 0.7, 0.5],
  'pan dir→esq': [1.12, 1.12, 0.7, 0.5, 0.3, 0.5],
  'push-in leve': [1.03, 1.14, 0.5, 0.45, 0.5, 0.5],
  'tilt ↓ lento': [1.1, 1.1, 0.5, 0.3, 0.5, 0.7],
};
const kb = (s) => (s.enq !== 'aberto' && ENQ[s.enq]) || MOV[s.mov] || MOV['zoom-in lento'];

const Shot = ({ s, fade }) => {
  const f = useCurrentFrame();
  const mapa = (LABELS[s.chave] || []).length > 0;
  const [z0, z1, x0, y0, x1, y1] = mapa ? [1.0, 1.06, 0.5, 0.5, 0.5, 0.5] : kb(s);   // mapa: quase parado, para os pinos ficarem na tela
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
        <svg viewBox="0 0 1000 1000" preserveAspectRatio="none" style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
          {labels.filter((l) => l.arrow).map((l, i) => <Arrow key={i} a={l.arrow} f={f} />)}
        </svg>
        {labels.filter((l) => !l.arrow).map((l, i) => <MapLabel key={i} l={l} z={z} f={f} i={i} />)}
      </div>
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,.38) 100%)' }} />
    </AbsoluteFill>
  );
};

const Arrow = ({ a, f }) => {
  const [x0, y0, x1, y1] = a.map((v) => v * 1000);
  const p = interpolate(f, [10, 40], [0, 1], { ...clamp, easing: EASE });
  const mx = (x0 + x1) / 2, my = Math.min(y0, y1) - 60;   // curva para cima
  return (
    <path d={`M ${x0} ${y0} Q ${mx} ${my} ${x1} ${y1}`} fill="none" stroke={ROJO} strokeWidth={5} strokeLinecap="round"
      pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - p} opacity={0.9} />
  );
};

// rótulo de mapa: papel com borda de tinta; com pin, um alfinete vermelho no ponto e o rótulo ao lado
const MapLabel = ({ l, z, f, i }) => {
  const a = l.fijo ? 1 : interpolate(f, [8 + i * 6, 20 + i * 6], [0, 1], { ...clamp, easing: EASE });
  const size = (l.size || 40) * 1.1;
  const off = { cima: 'translate(-50%, -135%)', baixo: 'translate(-50%, 45%)', dir: 'translate(14%, -50%)', esq: 'translate(-114%, -50%)' }[l.lado || 'cima'];
  return (
    <div style={{ position: 'absolute', left: `${l.x * 100}%`, top: `${l.y * 100}%` }}>
      {l.pin && (
        <div style={{ position: 'absolute', left: -13 * z, top: -13 * z, width: 26 * z, height: 26 * z, borderRadius: '50%', background: ROJO,
          border: `${4 * z}px solid ${PAPEL}`, boxShadow: '0 3px 8px rgba(0,0,0,.6)', transform: `scale(${a})` }} />
      )}
      <div style={{ position: 'absolute', transform: l.pin ? off : 'translate(-50%, -50%)', opacity: a, whiteSpace: 'nowrap',
        fontFamily: TYPE, fontSize: size * z, color: TINTA, background: PAPEL, border: `${2.5 * z}px solid ${TINTA}`,
        padding: `${0.12 * size * z}px ${0.4 * size * z}px`, boxShadow: `${4 * z}px ${4 * z}px 0 rgba(26,26,26,.75)`, letterSpacing: 1 }}>{l.t}</div>
    </div>
  );
};

// texto que vai sendo "datilografado"
const typed = (text, f, start, cps = 1.6) => text.slice(0, Math.max(0, Math.floor((f - start) * cps)));

// rótulo de nome/lugar: tira de papel no canto inferior esquerdo, máquina de escrever, sublinhado vermelho
const NameTag = ({ text, dur }) => {
  const f = useCurrentFrame();
  const a = interpolate(f, [2, 10], [0, 1], { ...clamp, easing: EASE });
  const out = interpolate(f, [dur - 7, dur], [1, 0], clamp);
  const t = typed(text, f, 4);
  return (
    <div style={{ position: 'absolute', left: 70, bottom: 72, opacity: a * out, transform: `translateX(${(1 - a) * -30}px) rotate(-0.6deg)`,
      background: PAPEL, padding: '12px 30px 14px', boxShadow: '5px 6px 0 rgba(0,0,0,.55)', borderLeft: `10px solid ${ROJO}` }}>
      <div style={{ fontFamily: TYPE, fontSize: 50, color: TINTA, whiteSpace: 'nowrap', letterSpacing: 1 }}>
        {t}<span style={{ opacity: 0 }}>{text.slice(t.length)}</span>
      </div>
      <div style={{ height: 4, background: ROJO, marginTop: 4, width: `${(100 * t.length) / text.length}%` }} />
    </div>
  );
};

// rótulo de cena [PANTALLA]: ficha de papel no canto superior esquerdo, com carimbo vermelho
const SceneCard = ({ text, dur }) => {
  const f = useCurrentFrame();
  const a = interpolate(f, [0, 9], [0, 1], { ...clamp, easing: EASE });
  const out = interpolate(f, [dur - 8, dur], [1, 0], clamp);
  const t = typed(text, f, 4, 1.8);
  return (
    <div style={{ position: 'absolute', left: 64, top: 56, opacity: a * out, transform: `translateY(${(1 - a) * -18}px) rotate(-1deg)`,
      background: PAPEL, padding: '14px 34px 16px', boxShadow: '6px 7px 0 rgba(0,0,0,.55)', border: `3px solid ${TINTA}` }}>
      <div style={{ fontFamily: TYPE, fontSize: 25, color: ROJO, letterSpacing: 6 }}>LUGAR Y FECHA</div>
      <div style={{ fontFamily: TYPE, fontSize: 52, color: TINTA, whiteSpace: 'nowrap' }}>
        {t}<span style={{ opacity: 0 }}>{text.slice(t.length)}</span>
      </div>
    </div>
  );
};

// cartão de expediente: pasta parda com aba "EXPEDIENTE N", título em Bebas e carimbo CLASIFICADO
export const Expediente = ({ title, dur }) => {
  const f = useCurrentFrame();
  const m = title.match(/^(\d+)\.\s*(.*)$/) || title.match(/^(Cierre)\.\s*(.*)$/);
  if (!m) return null;
  const aba = m[1] === 'Cierre' ? 'EXPEDIENTE CERRADO' : `EXPEDIENTE ${m[1]}`;
  const a = interpolate(f, [0, 12], [0, 1], { ...clamp, easing: EASE });
  const out = interpolate(f, [dur - 10, dur], [1, 0], clamp);
  const st = interpolate(f, [16, 22], [1.9, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  const so = interpolate(f, [16, 19], [0, 0.92], clamp);
  return (
    <AbsoluteFill style={{ justifyContent: 'center', alignItems: 'center', opacity: out, background: `rgba(0,0,0,${0.45 * a})` }}>
      <div style={{ position: 'relative', transform: `translateY(${(1 - a) * 60}px) rotate(-1.2deg)` }}>
        <div style={{ position: 'absolute', left: 40, top: -62, height: 64, padding: '10px 36px 0', background: PASTA, borderRadius: '14px 14px 0 0',
          fontFamily: TYPE, fontSize: 34, color: TINTA, letterSpacing: 3, boxShadow: '0 -2px 0 rgba(0,0,0,.15) inset' }}>{aba}</div>
        <div style={{ width: 1100, padding: '46px 70px 54px', background: PASTA, borderRadius: '0 14px 14px 14px', boxShadow: '12px 14px 0 rgba(0,0,0,.5)',
          borderTop: `6px solid ${PASTA_ESC}` }}>
          <div style={{ background: PAPEL, padding: '26px 40px 18px', transform: 'rotate(0.8deg)', boxShadow: '3px 3px 0 rgba(0,0,0,.25)' }}>
            <div style={{ fontFamily: TYPE, fontSize: 28, color: '#5b4a33', letterSpacing: 4 }}>DOSSIER · LA INQUISICIÓN · Nº 008</div>
            <div style={{ fontFamily: DISPLAY, fontSize: 168, lineHeight: 1, color: TINTA, letterSpacing: 4 }}>{m[2].toUpperCase()}</div>
          </div>
        </div>
        <div style={{ position: 'absolute', right: -90, top: -96, transform: `rotate(-10deg) scale(${st})`, opacity: so,
          border: `7px solid ${ROJO}`, padding: '6px 24px', fontFamily: DISPLAY, fontSize: 80, color: ROJO, letterSpacing: 6, borderRadius: 8 }}>CLASIFICADO</div>
      </div>
    </AbsoluteFill>
  );
};

export const CARD_DUR = 100;   // frames do cartão de expediente (o build.py usa o mesmo valor para o carimbo)

export const INQ = () => {
  const { shots, cards, chapters } = timeline;
  return (
    <AbsoluteFill style={{ background: '#000' }}>
      {shots.map((s, i) => {
        const fade = i > 0 && shots[i - 1].bloco !== s.bloco;
        const nextFade = i < shots.length - 1 && shots[i + 1].bloco !== s.bloco;
        return (
          <Sequence key={i} from={s.from} durationInFrames={s.dur + (nextFade ? XF : 0)} premountFor={30}>
            <Shot s={s} fade={fade} />
          </Sequence>
        );
      })}
      {shots.filter((s) => s.rot).map((s, i) => {
        const k = chapters.find((c) => c.from + 4 < s.from + s.dur && c.from + 4 + CARD_DUR > s.from);
        const start = k ? Math.max(s.from, k.from + 4 + CARD_DUR) : s.from;
        const d = s.from + Math.max(36, s.dur) - start;
        if (d < 24) return null;
        return <Sequence key={`r${i}`} from={start} durationInFrames={d}><NameTag text={s.rot} dur={d} /></Sequence>;
      })}
      {cards.map((c, i) => {
        const k = chapters.find((ch) => ch.from + 4 < c.from + 90 && ch.from + 4 + CARD_DUR > c.from);
        const start = k ? k.from + 4 + CARD_DUR : c.from + 6;
        return <Sequence key={`c${i}`} from={start} durationInFrames={90}><SceneCard text={c.text} dur={90} /></Sequence>;
      })}
      {chapters.map((c, i) => (
        <Sequence key={`k${i}`} from={c.from + 4} durationInFrames={CARD_DUR}><Expediente title={c.title} dur={CARD_DUR} /></Sequence>
      ))}
      <Audio src={staticFile('audio/mix.wav')} />
    </AbsoluteFill>
  );
};
