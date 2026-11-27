// Botão "SUSCRÍBETE" do CTA de inscrição do Dossier en Minutos (27/11/2026, decisão do Rodrigo; regra em biblia/visual.md).
// FONTE ÚNICA: canais/dossie-es/cta/inscricao/BotonSuscribete.jsx. O `inscricao.py montar` copia para src/ do vídeo;
// não edite a cópia do vídeo. Desenhado no estilo do canal (ficha de papel com borda de tinta, sombra dura, sello rojo,
// Bebas Neue): nada do logo oficial do YouTube. Canto superior direito (espelho da ficha LUGAR Y FECHA), longe das
// legendas (embaixo) e do centro da imagem. Ritmo: entra → cursor clica no "-críbe-" (clique) → vira SUSCRITO com
// carimbo → cursor toca o sininho (balança) → sai. Props em quadros, relativos ao início da Sequence.
import React from 'react';
import { Easing, interpolate, useCurrentFrame } from 'remotion';
import { loadFont as loadBebas } from '@remotion/google-fonts/BebasNeue';
import { loadFont as loadElite } from '@remotion/google-fonts/SpecialElite';

const bebas = loadBebas('normal', { weights: ['400'], subsets: ['latin', 'latin-ext'] });
const elite = loadElite('normal', { weights: ['400'], subsets: ['latin', 'latin-ext'] });
const DISPLAY = `${bebas.fontFamily}, Impact, sans-serif`;
const TYPE = `${elite.fontFamily}, 'Courier New', monospace`;
const PAPEL = '#E9DFC9', ROJO = '#B3261E', TINTA = '#1A1A1A';
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const EASE = Easing.bezier(0.16, 1, 0.3, 1);
const SOFT = Easing.bezier(0.45, 0, 0.55, 1);

// sininho em traço de tinta (contorno grosso, miolo papel), com as "ondas" do toque
const Sino = ({ ang, ondas }) => (
  <svg width={78} height={78} viewBox="0 0 100 100" style={{ overflow: 'visible' }}>
    <g transform={`rotate(${ang} 50 14)`}>
      <path d="M50 14 C30 14 24 32 24 50 L24 64 L15 76 L85 76 L76 64 L76 50 C76 32 70 14 50 14 Z"
        fill={PAPEL} stroke={TINTA} strokeWidth={7} strokeLinejoin="round" />
      <path d="M40 80 Q50 94 60 80" fill="none" stroke={TINTA} strokeWidth={7} strokeLinecap="round" />
      <circle cx={50} cy={11} r={5} fill={TINTA} />
    </g>
    {[0, 1].map((k) => (
      <g key={k} opacity={ondas} stroke={ROJO} strokeWidth={6} fill="none" strokeLinecap="round">
        <path d={k ? 'M90 30 Q98 45 90 60' : 'M10 30 Q2 45 10 60'} />
      </g>
    ))}
  </svg>
);

// cursor de mão desenhado (seta de tinta com miolo papel)
const Cursor = () => (
  <svg width={46} height={58} viewBox="0 0 46 58">
    <path d="M4 3 L4 45 L15 35 L23 54 L31 50 L23 32 L39 32 Z" fill={PAPEL} stroke={TINTA} strokeWidth={4.5} strokeLinejoin="round" />
  </svg>
);

export const BotonSuscribete = ({ dur, clique }) => {
  const f = useCurrentFrame();
  const c = Math.max(16, Math.min(clique, dur - 40));          // clique no botão
  const s = Math.min(c + 24, dur - 22);                        // toque no sininho
  const ent = interpolate(f, [0, 12], [0, 1], { ...clamp, easing: EASE });
  const sai = interpolate(f, [dur - 10, dur], [1, 0], { ...clamp, easing: SOFT });
  const vis = ent * sai;

  // pressão do clique e troca para SUSCRITO (com "carimbo": escala que assenta)
  const press = interpolate(f, [c - 1, c + 2, c + 6], [1, 0.9, 1], clamp);
  const feito = f >= c + 2;
  const st = interpolate(f, [c + 2, c + 8], [1.25, 1], { ...clamp, easing: Easing.in(Easing.quad) });

  // sininho balança depois do toque (amortecido) e as ondas aparecem
  const tb = f - s;
  const ang = tb >= 0 ? 22 * Math.sin(tb * 0.9) * Math.exp(-tb / 9) : 0;
  const ondas = tb >= 0 ? interpolate(tb, [0, 3, 18, 26], [0, 1, 1, 0], clamp) : 0;

  // cursor: entra de baixo à direita até o botão, clica, vai ao sininho, clica, sai
  const BX = 150, BY = 62, SX = 372, SY = 56;                  // centro do botão / do sininho (px na ficha)
  const pIn = interpolate(f, [c - 16, c - 2], [0, 1], { ...clamp, easing: EASE });
  const pSino = interpolate(f, [c + 8, s - 1], [0, 1], { ...clamp, easing: SOFT });
  const pOut = interpolate(f, [s + 6, s + 20], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  let cx = 470 + (BX - 470) * pIn, cy = 230 + (BY - 230) * pIn;
  cx += (SX - BX) * pSino; cy += (SY - BY) * pSino;
  cx += 160 * pOut; cy += 150 * pOut;
  const cAlpha = interpolate(f, [c - 16, c - 12], [0, 1], clamp) * (1 - pOut);
  const cPress = (f >= c - 1 && f <= c + 3) || (f >= s - 1 && f <= s + 3) ? 0.86 : 1;

  return (
    <div style={{ position: 'absolute', right: 64, top: 56, opacity: vis,
      transform: `translateX(${(1 - ent) * 40 + (1 - sai) * 30}px) rotate(1deg) scale(${0.92 + 0.08 * ent})`, transformOrigin: 'top right' }}>
      <div style={{ position: 'relative', display: 'flex', alignItems: 'center', gap: 22, background: PAPEL,
        padding: '16px 26px 16px 22px', border: `3px solid ${TINTA}`, boxShadow: '6px 7px 0 rgba(0,0,0,.55)' }}>
        <div style={{ transform: `scale(${press * (feito ? st : 1)})`, background: feito ? TINTA : ROJO,
          border: `3px solid ${TINTA}`, borderRadius: 10, padding: '6px 26px 2px', boxShadow: '3px 4px 0 rgba(26,26,26,.75)',
          fontFamily: DISPLAY, fontSize: 66, lineHeight: 1, letterSpacing: 4, color: PAPEL, whiteSpace: 'nowrap', width: 300, boxSizing: 'border-box', textAlign: 'center' }}>
          {feito ? 'SUSCRITO' : 'SUSCRÍBETE'}
        </div>
        <Sino ang={ang} ondas={ondas} />
        <div style={{ position: 'absolute', left: 22, bottom: -30, fontFamily: TYPE, fontSize: 21, letterSpacing: 3, color: PAPEL,
          textShadow: '2px 2px 0 rgba(0,0,0,.8)', whiteSpace: 'nowrap' }}>DOSSIER EN MINUTOS</div>
        <div style={{ position: 'absolute', left: cx, top: cy, opacity: cAlpha, transform: `scale(${cPress})`, transformOrigin: 'top left' }}>
          <Cursor />
        </div>
      </div>
    </div>
  );
};
