import React from 'react';
import {
  AbsoluteFill,
  Easing,
  Img,
  Sequence,
  cancelRender,
  continueRender,
  delayRender,
  interpolate,
  interpolateColors,
  random,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';
import { Audio, Video } from '@remotion/media';
import { loadFont as loadCinzel } from '@remotion/google-fonts/Cinzel';
import { loadFont as loadCormorant } from '@remotion/google-fonts/CormorantGaramond';
// Phrase-level Caption[] (src/v3/captions_fr.json): cue times are the measured silence boundaries of narration_v3.mp3.
import captions from './captions_fr.json';

// ---------------------------------------------------------------------------
// Registration values for src/index.jsx (registered separately):
//   <Composition id="LotR1MinPilotV3" component={PilotV3} durationInFrames={1830} fps={30} width={1920} height={1080} />
// ---------------------------------------------------------------------------
export const PILOT_V3 = { id: 'LotR1MinPilotV3', durationInFrames: 1830, fps: 30, width: 1920, height: 1080 };

// ---------------------------------------------------------------------------
// Fonts: Cinzel + Cormorant Garamond; bundled DejaVu is the per-glyph fallback (→ is not in the Latin subsets).
// ---------------------------------------------------------------------------
const cinzel = loadCinzel('normal', { weights: ['400', '700'], subsets: ['latin'] });
const cormorant = loadCormorant('normal', { weights: ['500', '600', '700'], subsets: ['latin'] });
loadCormorant('italic', { weights: ['500', '600'], subsets: ['latin'] });

const FALLBACK = 'PilotV3DejaVu';
if (typeof document !== 'undefined') {
  const handle = delayRender('Loading bundled DejaVu fallback (V3)');
  Promise.all(
    [
      ['DejaVuSans.ttf', '400'],
      ['DejaVuSans-Bold.ttf', '700'],
    ].map(([file, weight]) =>
      new FontFace(FALLBACK, `url(${staticFile(`assets/${file}`)})`, { weight })
        .load()
        .then((face) => document.fonts.add(face)),
    ),
  )
    .then(() => document.fonts.ready)
    .then(() => continueRender(handle))
    .catch((err) => cancelRender(err));
}

const TITLE = `${cinzel.fontFamily}, ${FALLBACK}, serif`;
const BODY = `${cormorant.fontFamily}, ${FALLBACK}, serif`;

const W = 1920;
const H = 1080;
const PAPER = '#eadfc4';
const INK = '#2b2219';
const GOLD = '#c8932f';
const GOLD_L = '#f3d68a';
const RED = '#8e2a1f';
const SEA = '#9fb5ae';
const NIGHT = '#14100b';
const PAGE_BG = 'linear-gradient(90deg, #e9dcb9 0%, #f6eedb 12%, #f3e8cf 100%)';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const EASE = Easing.bezier(0.16, 1, 0.3, 1);
const INOUT = Easing.bezier(0.65, 0, 0.35, 1);
const SLOW = Easing.bezier(0.45, 0, 0.2, 1);

// ---------------------------------------------------------------------------
// Photo helper: the licensed portrait photo of Bag End (1920×2880) is only ever cropped/moved, never retouched.
// (fx, fy) is a focus point as a fraction of the image; it is placed at screen position (tx, ty).
// ---------------------------------------------------------------------------
const BAG_END = { door: [0.46, 0.4], tree: [0.46, 0.29], table: [0.51, 0.85] };
const Photo = ({ src = 'assets/bag_end_hobbiton.jpg', ratio = 1.5, width, focus, at, style }) => (
  <Img
    src={staticFile(src)}
    style={{ position: 'absolute', left: at[0] - focus[0] * width, top: at[1] - focus[1] * width * ratio, width, height: width * ratio, ...style }}
  />
);

// ---------------------------------------------------------------------------
// Original schematic map of north-western Eriador. West is LEFT.
// West → east: Belegaer (sea) · Gulf of Lhûn with the Grey Havens/Mithlond at its eastern end (Lindon)
//              · Tower Hills/Emyn Beraid · Westmarch · the Shire.
// Not to scale; the dotted continuation after the Tower Hills is a family tradition, not a surveyed route.
// ---------------------------------------------------------------------------
const SHIRE_PT = [1560, 620];
const TOWER_PT = [1010, 520];
const HAVENS_PT = [712, 652];
const SOLID = { p0: SHIRE_PT, p1: [1420, 520], p2: [1230, 650], p3: TOWER_PT };
const DOTTED = { p0: TOWER_PT, p1: [905, 505], p2: [790, 560], p3: HAVENS_PT };
const cubic = ({ p0, p1, p2, p3 }, t) => {
  const u = 1 - t;
  return [0, 1].map((k) => u * u * u * p0[k] + 3 * u * u * t * p1[k] + 3 * u * t * t * p2[k] + t * t * t * p3[k]);
};
const cubicD = (c) => `M${c.p0.join(' ')} C${c.p1.join(' ')} ${c.p2.join(' ')} ${c.p3.join(' ')}`;
const WESTMARK_PT = cubic(SOLID, 0.5);

// Coast: open sea on the left, the Gulf of Lhûn cutting east to its head at the Grey Havens.
const COAST =
  'M0 0 L480 0 C450 110 505 200 462 300 C430 380 470 440 450 510 C440 545 470 575 540 592 C620 610 690 630 712 652 C690 676 620 690 548 700 C478 712 440 740 452 800 C466 870 430 980 462 1080 L0 1080 Z';
const WAVES = Array.from({ length: 30 }, (_, i) => [40 + random(`v3wx${i}`) * 340, 30 + random(`v3wy${i}`) * 1010]);
const TREES = [
  ...Array.from({ length: 14 }, (_, i) => [1180 + random(`v3t1x${i}`) * 260, 790 + random(`v3t1y${i}`) * 110]),
  ...Array.from({ length: 14 }, (_, i) => [1480 + random(`v3t2x${i}`) * 300, 260 + random(`v3t2y${i}`) * 120]),
  ...Array.from({ length: 10 }, (_, i) => [640 + random(`v3t3x${i}`) * 220, 790 + random(`v3t3y${i}`) * 120]),
];

const Mound = ({ x, y, r = 30 }) => (
  <path d={`M${x - r} ${y} q${r} ${-r * 1.1} ${2 * r} 0`} fill="rgba(120,140,80,.22)" stroke={INK} strokeWidth="2.5" />
);

const MapLayer = ({ idp, solid = 0, dotted = 0, labels = 1, pin = null }) => {
  const frame = useCurrentFrame();
  const head = cubic(SOLID, Math.max(0, Math.min(1, solid)));
  const ripple = (frame % 60) / 60;
  return (
    <svg viewBox={`0 0 ${W} ${H}`} width={W} height={H} style={{ position: 'absolute', left: 0, top: 0 }}>
      <defs>
        <filter id={`${idp}-glow`} x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="6" result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
        <radialGradient id={`${idp}-land`} cx="65%" cy="50%" r="75%">
          <stop offset="0" stopColor="#f0e3c3" />
          <stop offset="1" stopColor="#d3bd8f" />
        </radialGradient>
        <mask id={`${idp}-dmask`}>
          <path d={cubicD(DOTTED)} fill="none" stroke="white" strokeWidth="40" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - dotted} />
        </mask>
      </defs>
      <rect width={W} height={H} fill={`url(#${idp}-land)`} />
      <path d={COAST} fill={SEA} />
      {WAVES.map(([x, y], i) => (
        <path key={i} d={`M${x} ${y} q12 -8 24 0 q12 8 24 0`} fill="none" stroke="rgba(40,70,80,.38)" strokeWidth="2" />
      ))}
      <path d={COAST} fill="none" stroke={INK} strokeWidth="3.5" strokeLinejoin="round" />
      {TREES.map(([x, y], i) => (
        <g key={i}>
          <circle cx={x} cy={y} r="11" fill="rgba(80,105,60,.35)" stroke={INK} strokeWidth="1.8" />
          <path d={`M${x} ${y + 11} v9`} stroke={INK} strokeWidth="2" />
        </g>
      ))}
      {/* Shire hills, Far Downs-like mounds in Westmarch, Tower Hills with a tower */}
      {[[1500, 560], [1620, 570], [1600, 690], [1500, 720]].map(([x, y], i) => <Mound key={`s${i}`} x={x} y={y} r={28} />)}
      {[[1390, 470], [1420, 700], [1210, 450]].map(([x, y], i) => <Mound key={`w${i}`} x={x} y={y} r={26} />)}
      <Mound x={TOWER_PT[0] - 70} y={TOWER_PT[1] - 6} r={34} />
      <Mound x={TOWER_PT[0] + 70} y={TOWER_PT[1] - 6} r={34} />
      <path d={`M${TOWER_PT[0] - 7} ${TOWER_PT[1] - 14} v-34 h14 v34`} fill="#f6eedb" stroke={INK} strokeWidth="2.5" />

      {/* Compass: west is to the left */}
      <g transform="translate(1790 760)" opacity=".8">
        <circle r="62" fill="none" stroke={INK} strokeWidth="2" />
        <path d="M0 -78 L12 0 L0 78 L-12 0 Z" fill="rgba(43,34,25,.45)" />
        <path d="M-78 0 L0 -12 L78 0 L0 12 Z" fill="rgba(43,34,25,.45)" />
        <path d="M-78 0 L0 -12 L0 12 Z" fill={INK} />
        <text y="-88" textAnchor="middle" fontSize="26" fontFamily={TITLE} fill={INK}>N</text>
        <text x="-104" y="9" textAnchor="middle" fontSize="26" fontFamily={TITLE} fill={INK}>O</text>
        <text x="104" y="9" textAnchor="middle" fontSize="26" fontFamily={TITLE} fill="rgba(43,34,25,.6)">E</text>
      </g>

      {/* Labels (French, with Sindarin/alternate names smaller) */}
      <g opacity={labels} fontFamily={TITLE} fill={INK} textAnchor="middle">
        <text x="230" y="300" fontSize="36" letterSpacing="8" fill="rgba(30,55,62,.85)">BELEGAER</text>
        <text x="230" y="340" fontSize="26" fontFamily={BODY} fontStyle="italic" fontWeight="600" fill="rgba(30,55,62,.85)">la Grande Mer</text>
        <text x="235" y="880" fontSize="26" letterSpacing="5" fill="rgba(30,55,62,.8)">← VERS L’OUEST</text>
        <text x="600" y="455" fontSize="36" letterSpacing="7">LINDON</text>
        <text x="552" y="656" fontSize="23" fontFamily={BODY} fontStyle="italic" fontWeight="600" fill="rgba(30,55,62,.95)">golfe de Lhûn</text>
        <text x={HAVENS_PT[0] + 40} y="730" fontSize="36" letterSpacing="3" textAnchor="start" transform="translate(-30 0)">HAVRES GRIS</text>
        <text x={HAVENS_PT[0] + 40} y="764" fontSize="26" fontFamily={BODY} fontStyle="italic" fontWeight="600" textAnchor="start" transform="translate(-30 0)">Mithlond</text>
        <text x={TOWER_PT[0]} y="428" fontSize="34" letterSpacing="3">COLLINES DES TOURS</text>
        <text x={TOWER_PT[0]} y="462" fontSize="26" fontFamily={BODY} fontStyle="italic" fontWeight="600">Emyn Beraid</text>
        <text x={WESTMARK_PT[0]} y="760" fontSize="34" letterSpacing="3">MARCHE DE L’OUEST</text>
        <text x={WESTMARK_PT[0]} y="794" fontSize="26" fontFamily={BODY} fontStyle="italic" fontWeight="600">Westmarch</text>
        <text x={SHIRE_PT[0]} y="820" fontSize="42" letterSpacing="6">LA COMTÉ</text>
        <text x={SHIRE_PT[0]} y="854" fontSize="26" fontFamily={BODY} fontStyle="italic" fontWeight="600">The Shire</text>
        <text x={SHIRE_PT[0]} y="578" fontSize="28" letterSpacing="2">CUL-DE-SAC</text>
      </g>

      {/* Solid route: Shire → Westmarch → Tower Hills (text-supported) */}
      <path d={cubicD(SOLID)} fill="none" stroke="rgba(60,40,20,.25)" strokeWidth="4" />
      {solid > 0.002 ? (
        <path d={cubicD(SOLID)} fill="none" stroke={GOLD} strokeWidth="9" strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - solid} filter={`url(#${idp}-glow)`} />
      ) : null}
      {solid > 0.5 ? <circle cx={WESTMARK_PT[0]} cy={WESTMARK_PT[1]} r="8" fill={GOLD} stroke={PAPER} strokeWidth="3" /> : null}

      {/* Dotted continuation toward the Grey Havens: tradition only, schematic */}
      <g mask={`url(#${idp}-dmask)`}>
        <path d={cubicD(DOTTED)} fill="none" stroke={RED} strokeWidth="7" strokeLinecap="round" strokeDasharray="1 16" opacity=".9" />
      </g>
      {/* Legend: solid = supported by the text; dotted = family tradition, schematic only */}
      {solid > 0.6 || dotted > 0.05 ? (
        <g transform="translate(910 836)">
          <rect x="-290" y="-44" width="580" height="92" rx="12" fill="rgba(246,238,219,.94)" stroke={INK} strokeWidth="2.5" />
          <g opacity={Math.min(1, Math.max(0, (solid - 0.6) * 4))}>
            <line x1="-262" y1="-14" x2="-196" y2="-14" stroke={GOLD} strokeWidth="9" strokeLinecap="round" />
            <text x="-176" y="-6" fontSize="24" fontFamily={BODY} fontWeight="700" fill={INK}>route d’après le texte</text>
          </g>
          <g opacity={Math.min(1, dotted * 4)}>
            <line x1="-262" y1="26" x2="-196" y2="26" stroke={RED} strokeWidth="7" strokeLinecap="round" strokeDasharray="1 16" />
            <text x="-176" y="34" fontSize="24" fontFamily={BODY} fontWeight="700" fill={RED}>selon la tradition familiale · tracé indicatif</text>
          </g>
        </g>
      ) : null}

      {/* Markers */}
      <circle cx={SHIRE_PT[0]} cy={SHIRE_PT[1]} r="14" fill={RED} stroke={PAPER} strokeWidth="4" />
      <circle cx={TOWER_PT[0]} cy={TOWER_PT[1]} r="13" fill={INK} stroke={PAPER} strokeWidth="4" />
      <circle cx={HAVENS_PT[0]} cy={HAVENS_PT[1]} r="13" fill={INK} stroke={PAPER} strokeWidth="4" />
      {solid > 0.01 && solid < 0.99 ? <circle cx={head[0]} cy={head[1]} r="12" fill={GOLD_L} stroke={RED} strokeWidth="4" filter={`url(#${idp}-glow)`} /> : null}
      {pin
        ? (() => {
            const p = pin === 'tower' ? TOWER_PT : HAVENS_PT;
            return [0, 0.5].map((o) => {
              const k = (ripple + o) % 1;
              return <circle key={o} cx={p[0]} cy={p[1]} r={16 + k * 70} fill="none" stroke={GOLD} strokeWidth="5" opacity={(1 - k) * 0.9} />;
            });
          })()
        : null}
    </svg>
  );
};

// Fixed-size camera over the 1920×1080 map. cam = {cx, cy, s}; (w, h) is the viewport.
const MapView = ({ w = W, h = H, cam = { cx: 960, cy: 540, s: 1 }, badgeSize = 22, style, ...layer }) => {
  const k = (w / W) * cam.s;
  return (
    <div style={{ position: 'relative', width: w, height: h, overflow: 'hidden', background: PAPER, ...style }}>
      <div style={{ position: 'absolute', left: 0, top: 0, width: W, height: H, transformOrigin: '0 0', transform: `translate(${w / 2 - cam.cx * k}px, ${h / 2 - cam.cy * k}px) scale(${k})` }}>
        <MapLayer {...layer} />
      </div>
      <div style={{ position: 'absolute', right: 24, top: 20, padding: '6px 16px', background: 'rgba(246,238,219,.92)', border: `2px solid ${INK}`, fontFamily: TITLE, fontWeight: 700, fontSize: badgeSize, letterSpacing: '0.08em', color: INK, whiteSpace: 'nowrap' }}>
        CARTE SCHÉMATIQUE — NON À L’ÉCHELLE
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Original vector icons
// ---------------------------------------------------------------------------
const ShipIcon = ({ color = INK, sail = '#f2e8cf', width = 300, flip = false }) => (
  <svg viewBox="0 0 300 220" width={width} height={(width * 220) / 300} style={{ overflow: 'visible', scale: flip ? '-1 1' : '1 1' }}>
    <path d="M150 20 L150 160" stroke={color} strokeWidth="5" />
    <path d="M154 28 Q232 80 214 150 L154 150 Z" fill={sail} stroke={color} strokeWidth="3" />
    <path d="M146 40 Q96 90 108 150 L146 150 Z" fill={sail} stroke={color} strokeWidth="3" opacity=".9" />
    <path d="M150 20 l26 8 l-26 8 z" fill={GOLD} />
    <path d="M30 150 L270 150 Q240 196 150 198 Q70 196 44 168 Z" fill={color} />
    <path d="M44 168 Q10 150 22 112 Q30 92 46 100 Q34 110 40 128 Q46 146 60 152" fill="none" stroke={color} strokeWidth="9" strokeLinecap="round" />
  </svg>
);

// Original hobbit silhouette (Sam) and a slimmer figure (Elanor / Rosie).
const Figure = ({ color = INK, phase = 0, height = 300, facing = 1, variant = 'sam', book = false, style }) => {
  const swing = Math.sin(phase) * 12;
  const bob = -Math.abs(Math.sin(phase)) * 4;
  return (
    <svg viewBox="0 0 200 300" width={(height * 200) / 300} height={height} style={{ overflow: 'visible', scale: facing < 0 ? '-1 1' : '1 1', ...style }}>
      <g fill={color} transform={`translate(0 ${bob})`}>
        {variant === 'sam' ? (
          <>
            <circle cx="100" cy="62" r="30" />
            <circle cx="78" cy="46" r="15" />
            <circle cx="95" cy="33" r="15" />
            <circle cx="115" cy="35" r="14" />
            <circle cx="128" cy="50" r="12" />
            <circle cx="74" cy="68" r="12" />
            <path d="M126 60 L146 50 L134 74 Z" />
            <rect x="50" y="98" width="36" height="72" rx="12" />
            <path d="M72 94 Q100 84 128 94 L146 198 Q100 214 54 198 Z" />
            <g transform={`rotate(${swing} 88 196)`}>
              <rect x="80" y="190" width="18" height="60" rx="8" />
              <ellipse cx="96" cy="254" rx="24" ry="9" />
            </g>
            <g transform={`rotate(${-swing} 112 196)`}>
              <rect x="104" y="190" width="18" height="60" rx="8" />
              <ellipse cx="120" cy="254" rx="24" ry="9" />
            </g>
          </>
        ) : (
          <>
            <circle cx="100" cy="60" r="25" />
            <path d="M74 50 Q100 16 126 50 L134 150 Q100 138 66 150 Z" />
            <path d="M80 92 Q100 84 120 92 L150 238 Q100 252 50 238 Z" />
            <ellipse cx="86" cy="250" rx="16" ry="7" />
            <ellipse cx="116" cy="250" rx="16" ry="7" />
          </>
        )}
        <path d="M126 104 Q152 138 142 170 L128 168 Q134 140 118 112 Z" />
        {book ? <rect x="132" y="148" width="36" height="28" rx="3" fill={RED} stroke={GOLD} strokeWidth="2" transform="rotate(-10 150 162)" /> : null}
      </g>
    </svg>
  );
};

const BookMini = ({ width = 90 }) => (
  <svg viewBox="0 0 90 110" width={width} height={(width * 110) / 90}>
    <rect x="8" y="6" width="74" height="98" rx="6" fill={RED} stroke={INK} strokeWidth="3" />
    <rect x="17" y="15" width="56" height="80" rx="3" fill="none" stroke={GOLD} strokeWidth="3" />
    <ellipse cx="45" cy="55" rx="14" ry="11" fill="none" stroke={GOLD_L} strokeWidth="4" />
  </svg>
);

// Open book: left page with lines, right page left blank except for a trailing "…" (no invented reunion).
const OpenBook = ({ width = 900, write = 1, dots = 0 }) => (
  <svg viewBox="0 0 900 600" width={width} height={(width * 600) / 900} style={{ overflow: 'visible' }}>
    <rect x="30" y="30" width="840" height="560" rx="16" fill="rgba(0,0,0,.3)" />
    <rect x="20" y="14" width="860" height="560" rx="12" fill="#7a2018" stroke={INK} strokeWidth="3" />
    <path d="M40 40 Q250 20 450 56 L450 556 Q250 524 40 548 Z" fill="#f3e8cf" stroke={INK} strokeWidth="2" />
    <path d="M860 40 Q650 20 450 56 L450 556 Q650 524 860 548 Z" fill="#f6eedb" stroke={INK} strokeWidth="2" />
    {Array.from({ length: 10 }, (_, i) => {
      const w = 250 + random(`v3pg${i}`) * 90;
      const on = i / 10 < write;
      return on ? <rect key={i} x="82" y={96 + i * 42} width={w} height="6" rx="3" fill="rgba(60,40,25,.36)" /> : null;
    })}
    {Array.from({ length: 4 }, (_, i) => (
      <rect key={i} x="500" y={96 + i * 42} width={230 + random(`v3pr${i}`) * 100} height="6" rx="3" fill="rgba(60,40,25,.36)" opacity={write} />
    ))}
    <text x="500" y="320" fontSize="70" fontFamily={BODY} fontStyle="italic" fontWeight="600" fill={INK} opacity={dots}>…</text>
  </svg>
);

// ---------------------------------------------------------------------------
// Typography: labels use a soft fade (no kinetic word pops)
// ---------------------------------------------------------------------------
const Label = ({ lines, top = 80, left = 110, width = 1700, align = 'center', delay = 0, fadeFrames = 16, max = 96, color = INK, pill = null, style }) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [delay, delay + fadeFrames], [0, 1], { ...clamp, easing: EASE });
  const longest = Math.max(...lines.map((l) => l.text.length));
  return (
    <div style={{ position: 'absolute', top, left, width, display: 'flex', justifyContent: align === 'left' ? 'flex-start' : 'center', opacity: p, translate: `0px ${(1 - p) * 12}px`, ...style }}>
      <div style={{ textAlign: align, fontFamily: TITLE, fontWeight: 700, letterSpacing: '0.03em', padding: pill ? '10px 34px 14px' : 0, background: pill ?? 'none', borderRadius: 14, boxShadow: pill ? '0 8px 28px rgba(30,20,10,.18)' : 'none' }}>
        {lines.map((line, i) => {
          const size = Math.min(line.size ?? max, Math.floor(width / (longest * 0.82)));
          return (
            <div key={i} style={{ fontSize: Math.min(size, line.size ?? max), lineHeight: 1.16, whiteSpace: 'nowrap', color: line.color ?? color }}>
              {line.text}
            </div>
          );
        })}
      </div>
    </div>
  );
};

const Credit = ({ children, style }) => (
  <div style={{ position: 'absolute', left: 36, top: 22, maxWidth: 1150, padding: '5px 14px 7px', borderRadius: 8, background: 'rgba(24,18,12,.62)', fontFamily: BODY, fontWeight: 600, fontSize: 22, lineHeight: 1.15, color: '#f4ead2', ...style }}>{children}</div>
);

const Pop = ({ at = 0, children, style, rise = 24 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - at, fps, config: { damping: 200 }, durationInFrames: 22 });
  return <div style={{ opacity: s, translate: `0px ${(1 - s) * rise}px`, ...style }}>{children}</div>;
};

// ---------------------------------------------------------------------------
// Shared layers
// ---------------------------------------------------------------------------
const Grain = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0, mixBlendMode: 'multiply', opacity: 0.14 }}>
        <filter id="v3-fibers">
          <feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves="3" seed="7" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width={W} height={H} filter="url(#v3-fibers)" />
      </svg>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0, mixBlendMode: 'multiply', opacity: 0.16 }}>
        <filter id="v3-grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={frame % 7} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width={W} height={H} filter="url(#v3-grain)" />
      </svg>
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 58%, rgba(25,15,6,.45) 100%)' }} />
    </AbsoluteFill>
  );
};

// Quiet horizon used for the last two beats.
const Horizon = ({ drift = 0, glow = 1 }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: 'linear-gradient(180deg, #a9b8b9 0%, #e3d5b2 54%, #efdcae 58%)' }} />
      <AbsoluteFill style={{ background: `radial-gradient(circle at ${760 + drift}px 600px, rgba(255,236,180,${0.8 * glow}) 0px, rgba(255,226,160,${0.3 * glow}) 170px, rgba(255,220,150,0) 520px)` }} />
      <div style={{ position: 'absolute', left: 0, top: 604, width: W, height: 180, background: 'linear-gradient(180deg, #6f8c8d 0%, #3d5a60 100%)' }} />
      {Array.from({ length: 16 }, (_, i) => {
        const a = 0.5 + 0.5 * Math.sin(frame / 18 + i * 1.7);
        return <div key={i} style={{ position: 'absolute', left: random(`v3hz${i}`) * W, top: 622 + random(`v3hy${i}`) * 240, width: 50 + random(`v3hw${i}`) * 110, height: 3, borderRadius: 2, background: `rgba(255,240,200,${0.3 * a})` }} />;
      })}
      <div style={{ position: 'absolute', left: 0, top: 780, width: W, height: 300, background: 'linear-gradient(180deg, #3a2a1b 0%, #1d140c 100%)' }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// The 15 beats (times follow STORYBOARD_V3.md; durations vary on purpose)
// ---------------------------------------------------------------------------
const Beat01 = () => {
  const frame = useCurrentFrame();
  const cut = 34; // archive-ship insert, then hard cut to the Hobbiton photo
  const r = interpolate(frame, [cut, cut + 26], [0, 400], { ...clamp, easing: EASE });
  const ring = interpolate(frame, [cut, cut + 30], [0, 1], { ...clamp, easing: EASE });
  const drift = interpolate(frame, [cut, 114], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <div style={{ position: 'absolute', inset: -40, scale: String(1.06 + drift * 0.06), opacity: 0.5, filter: 'blur(1.5px)' }}>
        <MapView w={W + 80} h={H + 80} cam={{ cx: 960, cy: 540, s: 1 }} labels={0.5} badgeSize={20} idp="m1" />
      </div>
      <div style={{ position: 'absolute', left: 1040, top: 130, width: 800, height: 800, borderRadius: 400, overflow: 'hidden', clipPath: `circle(${r}px at 50% 50%)`, translate: `${-drift * 24}px 0px` }}>
        <Photo width={1150 + drift * 60} focus={BAG_END.door} at={[400, 400]} />
      </div>
      <svg width="840" height="840" viewBox="0 0 840 840" style={{ position: 'absolute', left: 1020, top: 110, translate: `${-drift * 24}px 0px` }}>
        <circle cx="420" cy="420" r="404" fill="none" stroke={GOLD} strokeWidth="6" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - ring} />
      </svg>
      <div style={{ position: 'absolute', left: interpolate(frame, [cut, 114], [380, -420]), top: 700 + Math.sin(frame / 6) * 5, opacity: interpolate(frame, [cut, cut + 12], [0, 1], clamp) }}>
        <ShipIcon width={320} />
      </div>
      <Label lines={[{ text: 'FRODON PART' }, { text: 'VERS L’OUEST', color: RED }]} top={230} left={90} width={900} align="left" max={110} delay={cut + 4} pill="rgba(246,238,219,.82)" />
      <Credit style={{ opacity: interpolate(frame, [cut, cut + 10], [0, 1], clamp) }}>
        Photo du lieu de tournage de Hobbiton (Bag End) — May0313, CC BY 4.0 · recadrée, animée · pas un photogramme du film
      </Credit>
      {frame < cut ? (
        <AbsoluteFill style={{ background: NIGHT }}>
          <Video src={staticFile('assets/ship_archive.webm')} muted trimBefore={48} objectFit="cover" style={{ width: W, height: H, filter: 'sepia(.55) contrast(1.05) brightness(.92)', scale: String(interpolate(frame, [0, cut], [1.03, 1.12])) }} />
          <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(10,6,2,.7) 100%)' }} />
          <Label lines={[{ text: 'FRODON PART VERS L’OUEST' }]} top={110} max={84} color="#f6edd6" delay={2} fadeFrames={8} style={{ textShadow: '0 4px 24px rgba(0,0,0,.7)' }} />
          <Credit>Film d’archive « S.S. Coptic Sailing Away » (1897), James H. White — domaine public · pas une image du film</Credit>
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};

const Beat02 = () => {
  const frame = useCurrentFrame();
  const reveal = interpolate(frame, [0, 26], [60, 1500], { ...clamp, easing: EASE });
  const walk = interpolate(frame, [8, 100], [0, 1], clamp);
  // The narration says "cent deux ans" at the start of this beat; keep the
  // numeral fixed so it is already correct as soon as that line is heard.
  const age = 102;
  const push = interpolate(frame, [0, 108], [1, 1.12], { ...clamp, easing: SLOW });
  return (
    <AbsoluteFill style={{ background: NIGHT }}>
      <AbsoluteFill style={{ clipPath: `circle(${reveal}px at 900px 520px)`, overflow: 'hidden' }}>
        <div style={{ position: 'absolute', inset: 0, scale: String(push), transformOrigin: '900px 520px' }}>
          <Photo width={1920} focus={BAG_END.door} at={[900, 520]} />
        </div>
        <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(20,15,8,.55) 0%, rgba(20,15,8,.12) 45%, rgba(20,15,8,0) 62%)' }} />
        <div style={{ position: 'absolute', left: interpolate(walk, [0, 1], [1680, 1190]), bottom: 130, filter: 'drop-shadow(0 0 3px rgba(255,244,214,.95)) drop-shadow(0 0 16px rgba(255,236,190,.65))' }}>
          <Figure height={250} facing={-1} phase={frame / 3.2} color="#1f1a14" />
        </div>
      </AbsoluteFill>
      <Label lines={[{ text: 'SAM EST RENTRÉ.' }, { text: 'PUIS IL EST REPARTI.', color: GOLD_L }]} top={150} left={90} width={1000} align="left" max={92} color="#f6edd6" delay={10} style={{ textShadow: '0 4px 24px rgba(0,0,0,.7)' }} />
      <Pop at={30} style={{ position: 'absolute', right: 120, top: 190, padding: '8px 40px 16px', background: 'rgba(24,18,12,.7)', borderRadius: 18, border: `3px solid ${GOLD}`, textAlign: 'center', fontFamily: TITLE, fontWeight: 700, color: GOLD_L }}>
        <div style={{ fontSize: 190, lineHeight: 1 }}>{age}</div>
        <div style={{ fontSize: 42, letterSpacing: '0.2em' }}>ANS</div>
      </Pop>
      <Credit>Hobbiton (Bag End) — May0313, CC BY 4.0 · recadrée, animée · photo de lieu, pas un photogramme</Credit>
    </AbsoluteFill>
  );
};

// Fan art by Lucie Vergne: shown whole, unaltered, signature visible; only its card moves slightly.
const ART_W = 540;
const ART_H = (ART_W * 1322) / 1280;

const Beat03 = () => {
  const frame = useCurrentFrame();
  const px = interpolate(frame, [0, 138], [-8, 8]);
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <div style={{ position: 'absolute', inset: 0, opacity: 0.25, translate: `${px * 2}px 0px` }}>
        <MapView cam={{ cx: 960, cy: 540, s: 1 }} labels={0} badgeSize={20} idp="m3" />
      </div>
      <div style={{ position: 'absolute', left: 150 + px * 1.6, top: 168, width: 640, height: 640, rotate: '-3deg', background: '#d9c69b', boxShadow: '0 20px 60px rgba(40,25,10,.3)' }} />
      <div style={{ position: 'absolute', left: 160 + px, top: 170, padding: 14, background: 'linear-gradient(135deg,#d9b25f,#8a6424 50%,#e3c27a)', borderRadius: 6, boxShadow: '0 30px 70px rgba(30,20,10,.45)', opacity: interpolate(frame, [0, 14], [0, 1], clamp) }}>
        <div style={{ padding: 12, background: '#f6eedb' }}>
          <Img src={staticFile('assets/sam_illustration.jpg')} style={{ display: 'block', width: ART_W, height: ART_H }} />
        </div>
      </div>
      <div style={{ position: 'absolute', left: 160 + px, top: 810, width: 604, textAlign: 'center', fontFamily: BODY, fontSize: 23, fontWeight: 600, lineHeight: 1.1, color: 'rgba(43,34,25,.92)' }}>
        Fan art « Sam Gamegie » — Lucie Vergne (signature : Lucie Schrimpf), CC BY-SA 4.0
      </div>
      <div style={{ position: 'absolute', left: 900, top: 330, width: 930, display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
        {[
          { at: 14, label: 'ROSIE', icon: <Figure variant="elanor" height={130} color={RED} /> },
          { at: 52, label: 'LES ENFANTS', icon: <div style={{ display: 'flex', gap: 6, alignItems: 'flex-end' }}><Figure height={86} /><Figure variant="elanor" height={100} /><Figure height={72} /></div> },
          { at: 92, label: 'LE LIVRE ROUGE', icon: <BookMini width={100} /> },
        ].map((item) => (
          <Pop key={item.label} at={item.at} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22 }}>
            <div style={{ width: 210, height: 210, borderRadius: 105, background: '#f6eedb', border: `4px solid ${GOLD}`, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 12px 30px rgba(40,25,10,.25)' }}>{item.icon}</div>
            <div style={{ fontFamily: TITLE, fontWeight: 700, fontSize: 36, color: INK, letterSpacing: '0.04em', whiteSpace: 'nowrap' }}>{item.label}</div>
          </Pop>
        ))}
      </div>
      <Label lines={[{ text: 'ROSIE · LEURS ENFANTS · LE LIVRE ROUGE' }]} top={72} max={74} delay={4} />
    </AbsoluteFill>
  );
};

const Beat04 = () => {
  const frame = useCurrentFrame();
  const season = interpolateColors(frame, [0, 22, 44, 66, 88], ['rgba(110,150,70,.30)', 'rgba(190,110,40,.34)', 'rgba(200,215,230,.38)', 'rgba(130,170,90,.30)', 'rgba(110,150,70,.22)']);
  const toPhoto = interpolate(frame, [26, 44], [0, 1], clamp);
  const push = interpolate(frame, [26, 89], [1, 1.18], { ...clamp, easing: SLOW });
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <AbsoluteFill>
        <Img src={staticFile('assets/book.jpg')} style={{ position: 'absolute', left: 0, top: 0, width: W, height: H, objectFit: 'cover', objectPosition: '50% 38%', scale: String(interpolate(frame, [0, 60], [1.04, 1.12], clamp)) }} />
        <AbsoluteFill style={{ background: 'rgba(60,35,10,.35)' }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ opacity: toPhoto, overflow: 'hidden' }}>
        <div style={{ position: 'absolute', inset: 0, scale: String(push), transformOrigin: '960px 540px' }}>
          <Photo width={1920} focus={BAG_END.tree} at={[960, 470]} />
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: season, mixBlendMode: 'multiply' }} />
      <Label lines={[{ text: 'UNE VIE ENSEMBLE' }]} top={90} max={100} color="#fbf3dd" pill="rgba(24,18,12,.55)" delay={6} />
      <Credit>Pages de livre — Shixart1985, CC BY 2.0 · Hobbiton — May0313, CC BY 4.0 · recadrées, teintées, animées</Credit>
    </AbsoluteFill>
  );
};

// Rosie's death: slowest beat. Held photo, light dims, no kinetic text.
const Beat05 = () => {
  const frame = useCurrentFrame();
  const dim = interpolate(frame, [0, 100], [0.15, 0.62], { ...clamp, easing: SLOW });
  const push = interpolate(frame, [0, 127], [1, 1.05], clamp);
  const lantern = interpolate(frame, [10, 100], [1, 0.12], { ...clamp, easing: SLOW });
  return (
    <AbsoluteFill style={{ background: NIGHT }}>
      <div style={{ position: 'absolute', inset: 0, overflow: 'hidden' }}>
        <div style={{ position: 'absolute', inset: 0, scale: String(push), transformOrigin: '1000px 700px', filter: `grayscale(${dim * 1.2}) sepia(.25) brightness(${1 - dim * 0.55})` }}>
          <Photo width={2100} focus={BAG_END.table} at={[1000, 700]} />
        </div>
      </div>
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 52% 62%, rgba(0,0,0,0) 20%, rgba(10,8,5,.82) 85%)' }} />
      <div style={{ position: 'absolute', left: 1000 - 160, top: 700 - 210, width: 320, height: 320, borderRadius: 160, background: `radial-gradient(circle, rgba(255,214,130,${0.55 * lantern}) 0%, rgba(255,214,130,0) 70%)` }} />
      <Label lines={[{ text: 'PUIS, ROSIE MEURT.' }]} top={150} max={104} color="#f1e6cb" delay={30} fadeFrames={44} style={{ textShadow: '0 4px 30px rgba(0,0,0,.8)' }} />
      <Credit>Hobbiton — May0313, CC BY 4.0 · recadrée, assombrie, animée</Credit>
    </AbsoluteFill>
  );
};

const Beat06 = () => {
  const frame = useCurrentFrame();
  const path = { p0: [1500, 850], p1: [1100, 880], p2: [800, 650], p3: [300, 650] };
  const t = interpolate(frame, [22, 138], [0, 1], { ...clamp, easing: Easing.inOut(Easing.quad) });
  const [sx, sy] = cubic(path, t);
  const size = interpolate(t, [0, 1], [270, 130]);
  const write = interpolate(frame, [4, 30], [0, 100], { ...clamp, easing: INOUT });
  return (
    <AbsoluteFill style={{ background: NIGHT }}>
      <div style={{ position: 'absolute', inset: 0, overflow: 'hidden' }}>
        <Img src={staticFile('assets/hills.jpg')} style={{ position: 'absolute', left: -60, top: -50 - frame * 0.25, width: 2040, height: (2040 * 1285) / 1920, scale: String(1 + frame * 0.0007) }} />
      </div>
      <AbsoluteFill style={{ background: 'linear-gradient(180deg, rgba(20,15,8,.25) 0%, rgba(20,15,8,.05) 40%, rgba(20,15,8,.55) 100%)' }} />
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0 }}>
        <path d={cubicD(path)} fill="none" stroke="rgba(244,232,190,.78)" strokeWidth="46" strokeLinecap="round" />
        <path d={cubicD(path)} fill="none" stroke="rgba(120,90,50,.5)" strokeWidth="46" strokeLinecap="round" strokeDasharray="2 30" />
      </svg>
      <div style={{ position: 'absolute', left: 1500 - 120, top: 850 - 250, width: 240, height: 240, borderRadius: 120, overflow: 'hidden', border: `5px solid ${GOLD}`, boxShadow: '0 12px 30px rgba(0,0,0,.45)' }}>
        <Photo width={900} focus={BAG_END.door} at={[120, 120]} />
      </div>
      <div style={{ position: 'absolute', left: sx - size / 3, top: sy - size, filter: 'drop-shadow(0 0 3px rgba(255,244,214,.95)) drop-shadow(0 0 14px rgba(255,236,190,.6))', opacity: interpolate(frame, [18, 30], [0, 1], clamp) }}>
        <Figure height={size} facing={-1} phase={frame / 3.4} book color="#1f1a14" />
      </div>
      <div style={{ position: 'absolute', top: 260, left: 0, width: W, display: 'flex', justifyContent: 'center' }}>
        <div style={{ padding: '6px 52px 14px', background: 'rgba(24,18,12,.62)', borderTop: `3px solid ${GOLD}`, borderBottom: `3px solid ${GOLD}`, fontFamily: TITLE, fontWeight: 700, fontSize: 112, letterSpacing: '0.05em', color: GOLD_L, clipPath: `inset(0 ${100 - write}% 0 0)`, whiteSpace: 'nowrap' }}>22 SEPTEMBRE 1482</div>
      </div>
      <Label lines={[{ text: 'IL QUITTE CUL-DE-SAC' }]} top={96} max={84} color="#fbf3dd" delay={2} style={{ textShadow: '0 4px 24px rgba(0,0,0,.7)' }} />
      <Credit>Paysage — Shadowmeld Photography, CC BY-SA 4.0 · Hobbiton — May0313, CC BY 4.0 · recadrés, animés</Credit>
    </AbsoluteFill>
  );
};

const Beat07 = () => {
  const frame = useCurrentFrame();
  const solid = interpolate(frame, [10, 98], [0, 1], { ...clamp, easing: INOUT });
  const s = interpolate(frame, [0, 114], [1, 1.1], { ...clamp, easing: SLOW });
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <MapView cam={{ cx: 1300 - (s - 1) * 300, cy: 560, s }} solid={solid} idp="m7" />
      <Label lines={[{ text: 'LA COMTÉ → COLLINES DES TOURS' }]} top={90} max={72} pill="rgba(246,238,219,.9)" delay={4} />
    </AbsoluteFill>
  );
};

const Beat08 = () => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [26, 78], [0, 1], { ...clamp, easing: INOUT });
  const bookX = interpolate(t, [0, 1], [330, 640]);
  const bookY = 640 - Math.sin(t * Math.PI) * 110;
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <div style={{ position: 'absolute', left: 130, top: 490 }}>
        <Figure height={330} />
      </div>
      <div style={{ position: 'absolute', left: 620, top: 460 }}>
        <Figure variant="elanor" height={360} facing={-1} color="#4a3a2a" />
      </div>
      <div style={{ position: 'absolute', left: bookX, top: bookY, rotate: `${t * 12 - 6}deg`, filter: 'drop-shadow(0 0 16px rgba(243,214,138,.8))' }}>
        <BookMini width={72} />
      </div>
      <div style={{ position: 'absolute', left: 930, top: 250, width: 872, height: 492, border: `4px solid ${INK}`, boxShadow: '0 20px 50px rgba(40,25,10,.3)', opacity: interpolate(frame, [0, 16], [0, 1], clamp), translate: `${interpolate(frame, [0, 20], [60, 0], { ...clamp, easing: EASE })}px 0px` }}>
        <MapView w={872} h={492} cam={{ cx: 1060, cy: 540, s: 2.1 }} solid={1} pin="tower" idp="m8" badgeSize={17} style={{ position: 'absolute', left: 0, top: 0 }} />
      </div>
      <Pop at={44} style={{ position: 'absolute', left: 930, top: 770, width: 880, textAlign: 'center', fontFamily: TITLE, fontWeight: 700, fontSize: 30, letterSpacing: '0.08em', color: RED }}>REMISE DU LIVRE · EMYN BERAID</Pop>
      <Label lines={[{ text: 'ELANOR REÇOIT LE LIVRE' }]} top={84} max={90} delay={4} />
    </AbsoluteFill>
  );
};

const Beat09 = () => {
  const frame = useCurrentFrame();
  const dotted = interpolate(frame, [14, 104], [0, 1], { ...clamp, easing: INOUT });
  const cam = {
    cx: interpolate(frame, [0, 120], [1130, 900], { ...clamp, easing: SLOW }),
    cy: interpolate(frame, [0, 120], [560, 580], clamp),
    s: interpolate(frame, [0, 120], [1.1, 1.25], { ...clamp, easing: SLOW }),
  };
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <MapView cam={cam} solid={1} dotted={dotted} idp="m9" />
      <Label lines={[{ text: 'SELON LA TRADITION FAMILIALE' }]} top={90} max={74} pill="rgba(246,238,219,.9)" delay={6} />
    </AbsoluteFill>
  );
};

const Beat10 = () => {
  const frame = useCurrentFrame();
  const cam = {
    cx: interpolate(frame, [0, 120], [900, 770], { ...clamp, easing: SLOW }),
    cy: interpolate(frame, [0, 120], [580, 640], { ...clamp, easing: SLOW }),
    s: interpolate(frame, [0, 120], [1.25, 1.85], { ...clamp, easing: SLOW }),
  };
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <MapView cam={cam} solid={1} dotted={1} pin="havens" idp="m10" />
      <Label lines={[{ text: 'HAVRES GRIS · MITHLOND' }, { text: 'LINDON · GOLFE DE LHÛN', size: 44, color: RED }]} top={84} max={78} pill="rgba(246,238,219,.92)" delay={6} />
    </AbsoluteFill>
  );
};

// The crossing of Belegaer: a separate sea panel, never drawn on the north-west map.
const Beat11 = () => {
  const frame = useCurrentFrame();
  const enter = interpolate(frame, [0, 18], [0, 1], { ...clamp, easing: EASE });
  return (
    <AbsoluteFill style={{ background: NIGHT }}>
      <Video src={staticFile('assets/waves.mp4')} muted trimBefore={30} objectFit="cover" style={{ width: W, height: H, filter: 'sepia(.35) saturate(.8) brightness(.62)' }} />
      <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(14,10,6,.55) 0%, rgba(14,10,6,.25) 100%)' }} />
      <div style={{ position: 'absolute', left: 150, top: 190, width: 840, height: 630, border: `5px solid ${GOLD}`, boxShadow: '0 24px 70px rgba(0,0,0,.6)', overflow: 'hidden', opacity: enter, translate: `${(1 - enter) * -60}px 0px`, background: NIGHT }}>
        <Video src={staticFile('assets/ship_archive.webm')} muted trimBefore={24 * 8} objectFit="cover" style={{ width: 840, height: 630, filter: 'sepia(.5) contrast(1.05) brightness(.95)', scale: String(interpolate(frame, [0, 138], [1.02, 1.1])) }} />
      </div>
      <Pop at={14} style={{ position: 'absolute', left: 1050, top: 330, width: 760, fontFamily: TITLE, color: '#f6edd6' }}>
        <div style={{ fontSize: 58, fontWeight: 700, letterSpacing: '0.1em', lineHeight: 1.1 }}>BELEGAER</div>
        <div style={{ fontFamily: BODY, fontStyle: 'italic', fontWeight: 600, fontSize: 38, color: GOLD_L, marginTop: 4 }}>la Grande Mer</div>
        <div style={{ fontFamily: BODY, fontWeight: 600, fontSize: 30, lineHeight: 1.25, marginTop: 34, color: 'rgba(246,237,214,.92)' }}>
          Panneau séparé : la traversée se fait au-delà de la carte, vers l’Ouest.
        </div>
      </Pop>
      <Label lines={[{ text: 'LE DERNIER PORTEUR À PARTIR' }]} top={84} max={80} color="#f6edd6" delay={4} style={{ textShadow: '0 4px 24px rgba(0,0,0,.7)' }} />
      <Credit>Film d’archive « S.S. Coptic » (1897), James H. White — domaine public, pas une image du film · Vagues — Mostafameraji, CC0 · teintés</Credit>
    </AbsoluteFill>
  );
};

// The text does not narrate a reunion: the route dissolves into fog, then an open page with nothing invented.
const Beat12 = () => {
  const frame = useCurrentFrame();
  const fog = interpolate(frame, [0, 56], [0.05, 0.92], { ...clamp, easing: INOUT });
  const toBook = interpolate(frame, [64, 84], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <MapView cam={{ cx: 900, cy: 600, s: interpolate(frame, [0, 80], [1.35, 1.5], clamp) }} solid={1} dotted={1} idp="m12" labels={1 - fog * 0.7} />
      <AbsoluteFill style={{ opacity: Math.min(1, fog * 1.1), mixBlendMode: 'screen' }}>
        <Video src={staticFile('assets/fog.webm')} muted objectFit="cover" style={{ width: W, height: H }} />
      </AbsoluteFill>
      <AbsoluteFill style={{ background: `linear-gradient(90deg, rgba(240,236,226,${fog * 0.85}) 0%, rgba(240,236,226,${fog * 0.55}) 70%, rgba(240,236,226,${fog * 0.2}) 100%)` }} />
      <AbsoluteFill style={{ opacity: toBook, background: 'radial-gradient(circle at 50% 58%, #f1e5c8 0%, #cdb487 100%)' }}>
        <div style={{ position: 'absolute', left: 510, top: 330, scale: String(interpolate(frame, [64, 150], [0.98, 1.04], clamp)) }}>
          <OpenBook width={900} write={interpolate(frame, [70, 112], [0, 1], clamp)} dots={interpolate(frame, [112, 128], [0, 1], clamp)} />
        </div>
      </AbsoluteFill>
      <Label lines={[{ text: 'LE TEXTE NE RACONTE PAS' }, { text: 'LEURS RETROUVAILLES', color: RED }]} top={70} max={84} pill="rgba(246,238,219,.92)" delay={6} />
    </AbsoluteFill>
  );
};

const Beat13 = () => {
  const frame = useCurrentFrame();
  const draw = (a, b) => interpolate(frame, [a, b], [0, 1], { ...clamp, easing: INOUT });
  const x0 = 260;
  const xF = 560; // Frodo's departure
  const xS = 1560; // Sam's departure
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0 }}>
        <text x={x0} y="380" fontSize="40" fontFamily={TITLE} fontWeight="700" fill={INK}>FRODON</text>
        <text x={x0} y="640" fontSize="40" fontFamily={TITLE} fontWeight="700" fill={INK}>SAM</text>
        <line x1={x0} y1="420" x2={x0 + (xF - x0) * draw(6, 34)} y2="420" stroke={INK} strokeWidth="8" strokeLinecap="round" />
        <line x1={x0} y1="680" x2={x0 + (xS + 100 - x0) * draw(4, 20)} y2="680" stroke="rgba(43,34,25,.25)" strokeWidth="6" strokeDasharray="8 12" />
        <line x1={xF} y1="680" x2={xF + (xS - xF) * draw(32, 96)} y2="680" stroke={GOLD} strokeWidth="18" strokeLinecap="round" />
        <line x1={xF} y1="440" x2={xF} y2={440 + 240 * draw(30, 48)} stroke="rgba(43,34,25,.4)" strokeWidth="4" strokeDasharray="8 10" />
        <circle cx={xF} cy="420" r="16" fill={INK} opacity={draw(30, 36)} />
        <circle cx={xF} cy="680" r="14" fill={RED} opacity={draw(30, 36)} />
        <circle cx={xS} cy="680" r="16" fill={INK} opacity={draw(94, 100)} />
        <text x={xF} y="478" textAnchor="middle" fontSize="30" fontFamily={BODY} fontWeight="700" opacity={draw(34, 46)} fill={INK}>départ de Frodon</text>
        <text x={xS} y="740" textAnchor="middle" fontSize="30" fontFamily={BODY} fontWeight="700" opacity={draw(96, 108)} fill={INK}>départ de Sam</text>
        <text x={(xF + xS) / 2} y="636" textAnchor="middle" fontSize="36" fontFamily={TITLE} fontWeight="700" letterSpacing="4" opacity={draw(60, 76)} fill={RED}>UNE VIE DANS LA COMTÉ</text>
      </svg>
      <div style={{ position: 'absolute', left: xF - 70 - 30 * draw(30, 80), top: 300 - 40 * draw(30, 80), opacity: draw(30, 40) * (1 - draw(80, 110)) }}>
        <ShipIcon width={140} />
      </div>
      <div style={{ position: 'absolute', left: xS - 70, top: 530, opacity: draw(96, 110) }}>
        <ShipIcon width={140} />
      </div>
      <Label lines={[{ text: 'DEUX DÉPARTS.' }, { text: 'UNE VIE ENTRE EUX.', color: RED }]} top={70} max={90} delay={4} />
    </AbsoluteFill>
  );
};

// "Et vous…": a breath. Sparse; the bed is lowered in the mix.
const Beat14 = () => (
  <AbsoluteFill>
    <Horizon drift={0} glow={0.8} />
    <div style={{ position: 'absolute', left: 960 - 240, top: 610 }}>
      <OpenBook width={480} write={0.6} dots={0} />
    </div>
    <Label lines={[{ text: 'ET VOUS…' }]} top={250} max={150} delay={14} fadeFrames={30} style={{ textShadow: '0 2px 24px rgba(255,240,200,.9)' }} />
  </AbsoluteFill>
);

const Beat15 = ({ dur }) => {
  const frame = useCurrentFrame();
  const dim = interpolate(frame, [dur - 40, dur], [0, 1], { ...clamp, easing: SLOW });
  return (
    <AbsoluteFill>
      <Horizon drift={interpolate(frame, [0, dur], [0, 60])} glow={interpolate(frame, [0, dur - 40], [0.8, 1], clamp)} />
      <div style={{ position: 'absolute', left: 960 - 240, top: 610 }}>
        <OpenBook width={480} write={0.6} dots={interpolate(frame, [30, 60], [0, 1], clamp)} />
      </div>
      <Label lines={[{ text: 'VOUS IMAGINEZ' }, { text: 'LEURS RETROUVAILLES ?', color: RED }]} top={240} max={104} delay={12} fadeFrames={40} style={{ textShadow: '0 2px 24px rgba(255,240,200,.9)' }} />
      <AbsoluteFill style={{ background: NIGHT, opacity: dim }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Captions: phrase cards with soft fades (no word-by-word flashing)
// ---------------------------------------------------------------------------
const CARDS = captions.map((c, i, arr) => ({
  text: c.text,
  start: c.startMs - 100,
  end: Math.min(c.endMs + 250, arr[i + 1] ? arr[i + 1].startMs - 100 : Infinity),
}));

const Captions = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const card = CARDS.find((c) => ms >= c.start && ms < c.end);
  if (!card) return null;
  const a = Math.min(interpolate(ms, [card.start, card.start + 180], [0, 1], clamp), interpolate(ms, [card.end - 180, card.end], [1, 0], clamp));
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 54, pointerEvents: 'none' }}>
      <div style={{ maxWidth: 1480, padding: '12px 36px 16px', borderRadius: 18, background: 'rgba(24,18,12,.7)', boxShadow: '0 10px 30px rgba(0,0,0,.25)', textAlign: 'center', opacity: a, translate: `0px ${(1 - a) * 8}px`, fontFamily: BODY, fontWeight: 600, fontSize: 44, lineHeight: 1.18, whiteSpace: 'pre-line', color: '#f4ead2' }}>
        {card.text}
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Audio: narration + original bed that fades and ducks around speech
// ---------------------------------------------------------------------------
const SPEECH = captions.map((c) => [c.startMs, c.endMs]);

const bedVolume = (f, fps) => {
  const ms = (f / fps) * 1000;
  const s = ms / 1000;
  let dist = Infinity;
  for (const [a, b] of SPEECH) {
    if (ms >= a && ms <= b) {
      dist = 0;
      break;
    }
    dist = Math.min(dist, ms < a ? a - ms : ms - b);
  }
  // Perceptible in pauses, clearly under the voice.
  const duck = interpolate(dist, [0, 600], [0.13, 0.36], clamp);
  // Thinner under Rosie's death, lowered again for the breath before the final question.
  const mood = interpolate(s, [0, 13.8, 15.5, 19, 20.5, 51.5, 53.5, 60], [1, 1, 0.5, 0.5, 1, 1, 0.62, 0.62], clamp);
  const fade = interpolate(f, [0, 2 * fps, 56 * fps, 60 * fps - 1], [0, 1, 1, 0], clamp);
  return duck * mood * fade;
};

const SoundTrack = () => {
  const { fps } = useVideoConfig();
  return (
    <>
      <Sequence name="Narration V3 (full length)" layout="none">
        <Audio src={staticFile('assets/v3/narration_v3.mp3')} volume={0.95} />
      </Sequence>
      <Sequence name="Original music bed (ducked)" durationInFrames={60 * fps} layout="none">
        <Audio src={staticFile('assets/v3/music_bed_v3.wav')} volume={(f) => bedVolume(f, fps)} />
      </Sequence>
    </>
  );
};

// ---------------------------------------------------------------------------
// Composition: 15 beats anchored to the measured phrase starts. `fade` = crossfade length into the beat.
// ---------------------------------------------------------------------------
const BEATS = [
  { name: '01 Hook · Frodon part vers l’Ouest', at: 0, fade: 0, C: Beat01 },
  { name: '02 Sam est rentré · 102 ans', at: 3.8, fade: 5, C: Beat02 },
  { name: '03 Fan art · Rosie, enfants, Livre Rouge', at: 7.4, fade: 8, C: Beat03 },
  { name: '04 Une vie ensemble', at: 12.0, fade: 14, C: Beat04 },
  { name: '05 Rosie meurt (lent)', at: 14.97, fade: 26, C: Beat05 },
  { name: '06 22 septembre 1482', at: 19.2, fade: 12, C: Beat06 },
  { name: '07 Carte · Comté → Collines des Tours', at: 24.2, fade: 10, C: Beat07 },
  { name: '08 Elanor reçoit le Livre', at: 28.0, fade: 10, C: Beat08 },
  { name: '09 Selon la tradition familiale', at: 32.0, fade: 12, C: Beat09 },
  { name: '10 Havres Gris · Lindon', at: 36.0, fade: 12, C: Beat10 },
  { name: '11 Belegaer · dernier Porteur', at: 40.0, fade: 12, C: Beat11 },
  { name: '12 Le texte ne raconte pas', at: 44.6, fade: 14, C: Beat12 },
  { name: '13 Deux départs, une vie', at: 49.6, fade: 10, C: Beat13 },
  { name: '14 Et vous… (respiration)', at: 53.8, fade: 20, C: Beat14 },
  { name: '15 Question finale (lent)', at: 56.4, fade: 36, C: Beat15 },
];
const VIDEO_END = 61;

const FadeIn = ({ frames, children }) => {
  const frame = useCurrentFrame();
  const o = frames > 0 ? interpolate(frame, [0, frames], [0, 1], { ...clamp, easing: INOUT }) : 1;
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};

export const PilotV3 = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: PAPER, fontFamily: BODY }}>
      {BEATS.map((b, i) => {
        const from = Math.round(b.at * fps);
        const next = BEATS[i + 1];
        const end = Math.round((next ? next.at : VIDEO_END) * fps);
        const dur = end - from + (next ? next.fade : 0); // keep this beat under the next one while it fades in
        return (
          <Sequence key={b.name} name={b.name} from={from} durationInFrames={dur}>
            <FadeIn frames={b.fade}>
              <b.C dur={dur} />
            </FadeIn>
          </Sequence>
        );
      })}
      <Grain />
      <Sequence name="Captions (phrase cards)" durationInFrames={Math.round(60 * fps)}>
        <Captions />
      </Sequence>
      <SoundTrack />
    </AbsoluteFill>
  );
};
