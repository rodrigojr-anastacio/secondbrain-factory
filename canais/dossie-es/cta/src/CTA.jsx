import React from 'react';
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from 'remotion';
import { Audio } from '@remotion/media';
import { loadFont as loadElite } from '@remotion/google-fonts/SpecialElite';
import { loadFont as loadBebas } from '@remotion/google-fonts/BebasNeue';
import T from './tempos.json';

// CTA genérico da HQ "Expedientes Secretos" (Dossier en Minutos, 24/11/2026). Identidade do canal (biblia/visual.md):
// papel #E9DFC9, sello rojo #B3261E, tinta #1A1A1A, Special Elite + Bebas Neue, carimbo com SFX.
// Tempos: src/tempos.json (tools/build_cta.py, a partir das palavras reais da voz).
const elite = loadElite('normal', { weights: ['400'], subsets: ['latin', 'latin-ext'] });
const bebas = loadBebas('normal', { weights: ['400'], subsets: ['latin', 'latin-ext'] });
const TYPE = `${elite.fontFamily}, 'Courier New', monospace`;
const DISPLAY = `${bebas.fontFamily}, Impact, sans-serif`;
const PAPEL = '#E9DFC9', ROJO = '#B3261E', TINTA = '#1A1A1A';
const FPS = T.fps;
const s2f = (s) => Math.round(s * FPS);
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const EASE = Easing.bezier(0.16, 1, 0.3, 1);
const SOFT = Easing.bezier(0.45, 0, 0.55, 1);
const img = (n) => staticFile(`img/${n}`);
const lerp = (f, a, b, v0, v1, e = SOFT) => interpolate(f, [a, b], [v0, v1], { ...clamp, easing: e });

// livro: página 2:3
const PH = 860, PW = PH * 2 / 3;
const CH = 640, CW = CH * 2 / 3;   // capa no leque

// ───────────── carimbo ─────────────
const Carimbo = ({ f, t0, texto, size = 70, rot = -12, style }) => {
  const a = s2f(t0);
  if (f < a) return null;
  const sc = interpolate(f, [a, a + 6], [2.2, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  const op = interpolate(f, [a, a + 3], [0, 0.94], clamp);
  return (
    <div style={{ position: 'absolute', transform: `translate(-50%, -50%) rotate(${rot}deg) scale(${sc})`, opacity: op,
      border: `${size / 10}px solid ${ROJO}`, padding: `${size * 0.05}px ${size * 0.3}px`, fontFamily: DISPLAY, fontSize: size,
      color: ROJO, letterSpacing: size / 12, borderRadius: 8, whiteSpace: 'nowrap', background: 'rgba(233,223,201,.18)', ...style }}>{texto}</div>
  );
};

// ───────────── folha que vira: N tiras encadeadas em 3D (curvatura) + luz por ângulo ─────────────
const N = 16;
// ângulo acumulado da tira i (0 = lombada) com progresso p: a borda de fora vai na frente → a folha curva
const phi = (p, i) => {
  const d = 0.3;
  const q = Math.min(1, Math.max(0, p * (1 + d) - d * (1 - i / (N - 1))));
  return 180 * SOFT(q);
};
const Tira = ({ i, p, frente, verso, w, h }) => {
  if (i >= N) return null;
  const sw = w / N;
  const a = phi(p, i) - (i ? phi(p, i - 1) : 0);
  const abs = phi(p, i);
  const luz = Math.abs(Math.cos((abs * Math.PI) / 180));
  const face = { position: 'absolute', inset: 0, backfaceVisibility: 'hidden', WebkitBackfaceVisibility: 'hidden', overflow: 'hidden' };
  return (
    <div style={{ position: 'absolute', left: i ? sw - 1.5 : 0, top: 0, width: sw + 1.5, height: h, transformOrigin: 'left center',
      transform: `rotateY(${-a}deg)`, transformStyle: 'preserve-3d' }}>
      <div style={face}>
        <div style={{ position: 'absolute', left: -i * sw, top: 0, width: w, height: h }}>{frente}</div>
        <div style={{ position: 'absolute', inset: 0, background: `rgba(0,0,0,${0.5 * (1 - luz)})` }} />
      </div>
      <div style={{ ...face, transform: 'rotateY(180deg)' }}>
        <div style={{ position: 'absolute', left: -(w - (i + 1) * sw), top: 0, width: w, height: h }}>{verso}</div>
        <div style={{ position: 'absolute', inset: 0, background: `rgba(0,0,0,${0.45 * (1 - luz)})` }} />
      </div>
      <Tira i={i + 1} p={p} frente={frente} verso={verso} w={w} h={h} />
    </div>
  );
};
// parada (p = 0 ou 1) a folha é plana (sem tiras: some o risco fino das emendas); só vira em tiras durante o movimento
const Folha = ({ p, frente, verso, z }) => (
  <div style={{ position: 'absolute', left: 0, top: 0, width: PW, height: PH, transformStyle: 'preserve-3d', zIndex: z }}>
    {p <= 0 ? frente : p >= 1 ? <div style={{ position: 'absolute', left: -PW, top: 0 }}>{verso}</div>
      : <Tira i={0} p={p} frente={frente} verso={verso} w={PW} h={PH} />}
  </div>
);

const Pagina = ({ src }) => <Img src={img(src)} style={{ width: PW, height: PH, display: 'block' }} />;
const ContraCapa = () => (   // verso da capa: papel com a marca, centrado
  <div style={{ width: PW, height: PH, background: PAPEL, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
    boxShadow: 'inset -30px 0 40px rgba(0,0,0,.18)' }}>
    <div style={{ fontFamily: TYPE, fontSize: 22, color: ROJO, letterSpacing: 6 }}>DOSSIER EN MINUTOS</div>
    <div style={{ fontFamily: DISPLAY, fontSize: 64, color: TINTA, letterSpacing: 3, marginTop: 10 }}>EXPEDIENTES SECRETOS</div>
    <div style={{ width: 120, height: 4, background: ROJO, marginTop: 14 }} />
  </div>
);
const Pagina3 = () => (   // página da direita depois de virar a 1: quadro grande (arte já existente) em papel
  <div style={{ width: PW, height: PH, background: PAPEL, position: 'relative' }}>
    <div style={{ position: 'absolute', left: 26, top: 26, right: 26, bottom: 46, border: `5px solid ${TINTA}`, overflow: 'hidden' }}>
      <Img src={img('P203.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
    </div>
  </div>
);

// ───────────── cena 1: leque + livro ─────────────
const Leque = ({ f }) => {
  const zoom = s2f(T.zoom), abre = s2f(T.abre), folheia = s2f(T.folheia);
  const pz = lerp(f, zoom, zoom + 16, 0, 1, EASE);                     // #1 vai ao centro e cresce; #2/#3 saem
  const pc = lerp(f, abre - 2, abre + 26, 0, 1, Easing.linear);                           // capa abre
  const pp = lerp(f, folheia - 4, folheia + 22, 0, 1, Easing.linear);                     // pág. 1 vira
  // capas laterais (#2 esq, #3 dir): entram em leque, carimbo CLASIFICADO, saem no zoom
  const lado = (n, k, t0) => {
    const e = lerp(f, s2f(t0), s2f(t0) + 14, 0, 1, EASE);
    const x = 960 + k * (330 + 500 * pz), y = 560 + 40 + (1 - e) * 700;
    const rot = k * (13 + 10 * pz) * e;
    return (
      <div key={n} style={{ position: 'absolute', left: x - CW / 2, top: y - CH / 2, width: CW, height: CH, opacity: 1 - pz,
        transform: `rotate(${rot}deg)`, boxShadow: '14px 18px 30px rgba(0,0,0,.6)' }}>
        <Img src={img(`capa-${n}.jpg`)} style={{ width: CW, height: CH, filter: 'saturate(.7) brightness(.8)' }} />
        <div style={{ position: 'absolute', left: CW / 2, top: CH * 0.52 }}>
          <Carimbo f={f} t0={n === 2 ? T.carimbo2 : T.carimbo3} texto="CLASIFICADO" size={64} rot={n === 2 ? -18 : 14} />
        </div>
      </div>
    );
  };
  // livro (#1): escala de capa do leque → página grande; lombada desliza para o centro quando abre
  const e1 = lerp(f, s2f(0.45), s2f(0.45) + 14, 0, 1, EASE);
  const sc = (CH / PH) * (1 - pz) + 1 * pz;
  const yC = 560 + (1 - e1) * 700 - 20 * (1 - pz) + 0 * pz;
  const lombadaX = -PW / 2 + (PW / 2) * pc;                            // relativo ao centro da tela, em px do livro
  const sombra = Math.sin(Math.PI * pc), sombra2 = Math.sin(Math.PI * pp);
  return (
    <AbsoluteFill>
      {lado(2, -1, 0.1)}
      {lado(3, 1, 0.3)}
      <div style={{ position: 'absolute', left: 960, top: yC, transform: `scale(${sc})`, transformOrigin: '0 0' }}>
        <div style={{ position: 'absolute', left: lombadaX, top: -PH / 2, width: 0, height: PH, perspective: 2600, perspectiveOrigin: '0 50%' }}>
          {/* sombra do livro na mesa */}
          <div style={{ position: 'absolute', left: -PW * pc, top: 0, width: PW * (1 + pc), height: PH, boxShadow: '18px 24px 40px rgba(0,0,0,.65)' }} />
          {/* página da direita por baixo (3) */}
          <div style={{ position: 'absolute', left: 0, top: 0 }}><Pagina3 /></div>
          {/* folha da pág. 1 (verso = pág. 2) */}
          <Folha p={pp} frente={<Pagina src="pagina-1.jpg" />} verso={<Pagina src="pagina-2.jpg" />} z={pp > 0 ? 4 : 2} />
          {/* capa (verso = contracapa interna) */}
          <Folha p={pc} frente={<Img src={img('capa-1.jpg')} style={{ width: PW, height: PH, display: 'block' }} />} verso={<ContraCapa />} z={3} />
          {/* sombra da folha que vira sobre a página de baixo + vinco da lombada */}
          <div style={{ position: 'absolute', left: 0, top: 0, width: PW, height: PH, zIndex: 5, pointerEvents: 'none',
            background: `linear-gradient(90deg, rgba(0,0,0,${0.55 * Math.max(sombra, sombra2)}) 0%, rgba(0,0,0,0) ${30 + 40 * Math.max(sombra, sombra2)}%)` }} />
          <div style={{ position: 'absolute', left: -22, top: 0, width: 44, height: PH, zIndex: 6, opacity: pc,
            background: 'linear-gradient(90deg, rgba(0,0,0,0), rgba(0,0,0,.35) 50%, rgba(0,0,0,0))' }} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ───────────── cena 2: parede com pôster + celular com o wallpaper ─────────────
const Parede = ({ f }) => {
  const c2 = s2f(T.cena2), cel = s2f(T.celular);
  const push = lerp(f, c2, s2f(T.dur), 1.0, 1.06, Easing.linear);
  const pe = lerp(f, c2, c2 + 14, 0, 1, EASE);
  const ce = lerp(f, cel, cel + 12, 0, 1, EASE);
  const PoH = 820, PoW = PoH * 2 / 3;
  const fita = (st) => <div style={{ position: 'absolute', width: 120, height: 34, background: 'rgba(233,223,201,.75)', boxShadow: '0 2px 4px rgba(0,0,0,.3)', ...st }} />;
  return (
    <AbsoluteFill style={{ background: 'linear-gradient(180deg, #2b3440 0%, #1f262f 70%, #161b21 100%)', transform: `scale(${push})` }}>
      {/* textura de parede: listras verticais suaves */}
      <AbsoluteFill style={{ background: 'repeating-linear-gradient(90deg, rgba(255,255,255,.025) 0 2px, rgba(0,0,0,0) 2px 46px)' }} />
      {/* rodapé/mesa */}
      <div style={{ position: 'absolute', left: 0, right: 0, top: 930, bottom: 0, background: '#3a2c20', boxShadow: '0 -6px 18px rgba(0,0,0,.5)' }} />
      {/* pôster */}
      <div style={{ position: 'absolute', left: 960 - 400 * ce - PoW / 2, top: 70 + (1 - pe) * -60, width: PoW, height: PoH, opacity: pe,
        transform: `rotate(-2deg)`, boxShadow: '16px 20px 30px rgba(0,0,0,.6)', background: '#fff', padding: 10 }}>
        <Img src={img('capa-1.jpg')} style={{ width: PoW - 20, height: PoH - 20, display: 'block' }} />
        {fita({ left: -30, top: -6, transform: 'rotate(-35deg)' })}
        {fita({ right: -30, top: -6, transform: 'rotate(35deg)' })}
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: -64, textAlign: 'center', fontFamily: TYPE, fontSize: 30, color: PAPEL, letterSpacing: 4 }}>PÓSTER A3</div>
      </div>
      {/* celular */}
      <div style={{ position: 'absolute', left: 1300, top: 130 + (1 - ce) * 1150, width: 380, height: 800, borderRadius: 54, background: '#0d0d0f',
        padding: 16, boxShadow: '20px 26px 40px rgba(0,0,0,.65)', transform: `rotate(${6 - 3 * ce}deg)`, border: '3px solid #3a3a40' }}>
        <div style={{ width: '100%', height: '100%', borderRadius: 40, overflow: 'hidden', position: 'relative' }}>
          <Img src={img('wallpaper-celular.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
          <div style={{ position: 'absolute', top: 70, width: '100%', textAlign: 'center', fontFamily: 'Helvetica, Arial, sans-serif', fontSize: 74, color: 'rgba(255,255,255,.92)', fontWeight: 300 }}>21:30</div>
          <div style={{ position: 'absolute', left: '50%', top: 14, width: 100, height: 26, borderRadius: 14, background: '#000', transform: 'translateX(-50%)' }} />
        </div>
      </div>
      <div style={{ position: 'absolute', left: 1490, top: 960, transform: 'translateX(-50%)', fontFamily: TYPE, fontSize: 30, color: PAPEL, letterSpacing: 4, opacity: Math.max(0, ce * 5 - 4) }}>6 FONDOS DE PANTALLA</div>
      {/* DE REGALO */}
      <div style={{ position: 'absolute', left: 1000, top: 520 }}>
        <Carimbo f={f} t0={T.regalo} texto="DE REGALO" size={120} rot={-9} />
      </div>
    </AbsoluteFill>
  );
};

// ───────────── cena 3: banner do link ─────────────
const Banner = ({ f }) => {
  const b = s2f(T.banner);
  const e = lerp(f, b, b + 12, 0, 1, EASE);
  const seta = (k) => {
    const ph = ((f - b) / FPS * 1.6 + k * 0.22) % 1;
    return (
      <svg key={k} width="150" height="80" viewBox="0 0 150 80" style={{ display: 'block', margin: '-8px auto 0', opacity: e * (0.35 + 0.65 * Math.sin(Math.PI * ph)) }}>
        <polyline points="10,10 75,66 140,10" fill="none" stroke={ROJO} strokeWidth="18" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    );
  };
  const bob = Math.sin(((f - b) / FPS) * Math.PI * 2 * 1.2) * 10;
  return (
    <AbsoluteFill style={{ background: `rgba(10,12,16,${0.62 * e})` }}>
      <div style={{ position: 'absolute', left: 960, top: 360, transform: `translate(-50%, -50%) scale(${0.85 + 0.15 * e}) rotate(-1.2deg)`, opacity: e,
        background: PAPEL, border: `6px solid ${TINTA}`, boxShadow: '14px 16px 0 rgba(0,0,0,.55)', padding: '30px 64px 26px', borderLeft: `26px solid ${ROJO}` }}>
        <div style={{ fontFamily: TYPE, fontSize: 30, color: ROJO, letterSpacing: 8 }}>EXPEDIENTES SECRETOS</div>
        <div style={{ fontFamily: DISPLAY, fontSize: 104, lineHeight: 1.02, color: TINTA, letterSpacing: 3, whiteSpace: 'nowrap' }}>ENLACE EN LA DESCRIPCIÓN</div>
        <div style={{ fontFamily: DISPLAY, fontSize: 76, lineHeight: 1.02, color: ROJO, letterSpacing: 3, whiteSpace: 'nowrap' }}>· COMENTARIO FIJADO ·</div>
      </div>
      <div style={{ position: 'absolute', left: 960, top: 640 + bob, transform: 'translateX(-50%)' }}>
        {[0, 1, 2].map(seta)}
      </div>
    </AbsoluteFill>
  );
};

export const CTA = ({ mudo = false }) => {
  const f = useCurrentFrame();
  const c2 = s2f(T.cena2), b = s2f(T.banner);
  const o1 = interpolate(f, [c2, c2 + 9], [1, 0], clamp);
  const o2 = interpolate(f, [c2, c2 + 9], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: '#11151b' }}>
      {/* fundo da cena 1: mesa escura com luz de abajur */}
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 42%, #3a3328 0%, #1d1b18 55%, #0c0c0d 100%)', opacity: o1 }} />
      {f < c2 + 10 && <AbsoluteFill style={{ opacity: o1 }}><Leque f={f} /></AbsoluteFill>}
      {f >= c2 && <AbsoluteFill style={{ opacity: o2 }}><Parede f={f} /></AbsoluteFill>}
      {f >= b && <Banner f={f} />}
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 58%, rgba(0,0,0,.42) 100%)' }} />
      {!mudo && <Audio src={staticFile('audio/mix.wav')} />}
    </AbsoluteFill>
  );
};
