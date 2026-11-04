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
import { Audio } from '@remotion/media';
import { loadFont as loadCinzel } from '@remotion/google-fonts/Cinzel';
import { loadFont as loadCormorant } from '@remotion/google-fonts/CormorantGaramond';
// Word-level Caption[] built by scripts_v2/make_captions_v2.py (Whisper timings, script_fr.txt wording).
import captions from './captions_fr.json';

// ---------------------------------------------------------------------------
// Fonts: Google Fonts delay the render until loaded; bundled DejaVu is the
// per-glyph fallback (≠, ∞, → are not in the Latin subsets).
// ---------------------------------------------------------------------------
const cinzel = loadCinzel('normal', { weights: ['400', '700'], subsets: ['latin'] });
const cormorant = loadCormorant('normal', { weights: ['500', '600', '700'], subsets: ['latin'] });
loadCormorant('italic', { weights: ['500'], subsets: ['latin'] });

const FALLBACK = 'PilotV2DejaVu';
if (typeof document !== 'undefined') {
  const handle = delayRender('Loading bundled DejaVu fallback (V2)');
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
const PAGE_BG = 'linear-gradient(90deg, #e9dcb9 0%, #f6eedb 12%, #f3e8cf 100%)';

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const EASE = Easing.bezier(0.16, 1, 0.3, 1);
const INOUT = Easing.bezier(0.65, 0, 0.35, 1);

// ---------------------------------------------------------------------------
// Original schematic map geometry (not a copy of any published map).
// West is to the left: sea on the left, the Shire on the right.
// ---------------------------------------------------------------------------
const SHIRE = [1420, 560];
const HAVENS = [650, 495];
const cubic = (p0, p1, p2, p3, t) => {
  const u = 1 - t;
  return [0, 1].map((k) => u * u * u * p0[k] + 3 * u * u * t * p1[k] + 3 * u * t * t * p2[k] + t * t * t * p3[k]);
};
const ROUTE_PTS = Array.from({ length: 121 }, (_, i) => cubic(SHIRE, [1200, 730], [930, 330], HAVENS, i / 120));
const ROUTE_CUM = ROUTE_PTS.reduce((acc, p, i) => {
  acc.push(i === 0 ? 0 : acc[i - 1] + Math.hypot(p[0] - ROUTE_PTS[i - 1][0], p[1] - ROUTE_PTS[i - 1][1]));
  return acc;
}, []);
const ROUTE_LEN = ROUTE_CUM[ROUTE_CUM.length - 1];
const ROUTE_D = `M${ROUTE_PTS.map((p) => `${p[0].toFixed(1)} ${p[1].toFixed(1)}`).join(' L')}`;
const routePointAt = (progress) => {
  const target = Math.max(0, Math.min(1, progress)) * ROUTE_LEN;
  const i = Math.max(1, ROUTE_CUM.findIndex((c) => c >= target));
  const seg = ROUTE_CUM[i] - ROUTE_CUM[i - 1] || 1;
  const k = (target - ROUTE_CUM[i - 1]) / seg;
  return [
    ROUTE_PTS[i - 1][0] + (ROUTE_PTS[i][0] - ROUTE_PTS[i - 1][0]) * k,
    ROUTE_PTS[i - 1][1] + (ROUTE_PTS[i][1] - ROUTE_PTS[i - 1][1]) * k,
  ];
};
const COAST =
  'M560 0 C520 120 610 210 560 300 C520 370 470 400 520 440 C560 470 640 465 655 500 C668 540 560 560 520 600 C470 660 560 760 500 860 C460 940 520 1010 480 1080 L0 1080 L0 0 Z';
const WAVES = Array.from({ length: 34 }, (_, i) => [40 + random(`wx${i}`) * 380, 30 + random(`wy${i}`) * 1010]);
const MOUNTAINS = [
  ...Array.from({ length: 9 }, (_, i) => [720 + (i % 2) * 28, 110 + i * 32]),
  ...Array.from({ length: 9 }, (_, i) => [700 + (i % 2) * 30, 640 + i * 30]),
];
const TREES = [
  ...Array.from({ length: 16 }, (_, i) => [1020 + random(`t1x${i}`) * 170, 760 + random(`t1y${i}`) * 110]),
  ...Array.from({ length: 14 }, (_, i) => [1600 + random(`t2x${i}`) * 170, 230 + random(`t2y${i}`) * 120]),
];

const MapLayer = ({ idp, progress = 0, ring = false, stamp = 0, labels = 1, routeOpacity = 1 }) => {
  const head = routePointAt(progress);
  return (
    <g>
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
      </defs>
      <rect width={W} height={H} fill={`url(#${idp}-land)`} />
      <path d={COAST} fill={SEA} />
      {WAVES.map(([x, y], i) => (
        <path key={i} d={`M${x} ${y} q12 -8 24 0 q12 8 24 0`} fill="none" stroke="rgba(40,70,80,.38)" strokeWidth="2" />
      ))}
      <path d={COAST} fill="none" stroke={INK} strokeWidth="3.5" strokeLinejoin="round" />
      <path d="M1300 70 C1150 200 1010 170 910 300 S770 460 655 497" fill="none" stroke="rgba(60,95,105,.65)" strokeWidth="3" />
      {MOUNTAINS.map(([x, y], i) => (
        <path key={i} d={`M${x - 22} ${y + 16} L${x} ${y - 18} L${x + 22} ${y + 16}`} fill="rgba(120,95,60,.18)" stroke={INK} strokeWidth="2.5" strokeLinejoin="round" />
      ))}
      {TREES.map(([x, y], i) => (
        <g key={i}>
          <circle cx={x} cy={y} r="11" fill="rgba(80,105,60,.35)" stroke={INK} strokeWidth="1.8" />
          <path d={`M${x} ${y + 11} v9`} stroke={INK} strokeWidth="2" />
        </g>
      ))}
      {[[1380, 520], [1450, 600], [1480, 520], [1360, 610]].map(([x, y], i) => (
        <path key={i} d={`M${x - 26} ${y} q26 -24 52 0`} fill="none" stroke={INK} strokeWidth="2.5" />
      ))}
      <g transform="translate(1730 890)" opacity=".75">
        <circle r="62" fill="none" stroke={INK} strokeWidth="2" />
        <path d="M0 -78 L12 0 L0 78 L-12 0 Z" fill={INK} />
        <path d="M-78 0 L0 -12 L78 0 L0 12 Z" fill="rgba(43,34,25,.45)" />
        <text y="-88" textAnchor="middle" fontSize="26" fontFamily={TITLE} fill={INK}>N</text>
        <text x="-98" y="9" textAnchor="middle" fontSize="26" fontFamily={TITLE} fill={INK}>O</text>
      </g>
      <g opacity={labels} fontFamily={TITLE} fill={INK}>
        <text x={SHIRE[0]} y={SHIRE[1] + 90} textAnchor="middle" fontSize="40" letterSpacing="5">LA COMTÉ</text>
        <text x={HAVENS[0] + 70} y={HAVENS[1] - 70} textAnchor="middle" fontSize="36" letterSpacing="4">HAVRES GRIS</text>
        <text x="230" y="320" textAnchor="middle" fontSize="34" letterSpacing="10" fill="rgba(30,55,62,.8)">LA MER</text>
        <text x="235" y="790" textAnchor="middle" fontSize="26" letterSpacing="6" fill="rgba(30,55,62,.8)">← VERS L’OUEST</text>
        <text x="1220" y="1050" textAnchor="middle" fontSize="18" letterSpacing="5" fill="rgba(43,34,25,.55)">CARTE SCHÉMATIQUE ORIGINALE — NON À L’ÉCHELLE</text>
      </g>
      <g opacity={routeOpacity}>
        <path d={ROUTE_D} fill="none" stroke="rgba(60,40,20,.38)" strokeWidth="4" strokeDasharray="10 12" />
        {progress > 0.002 ? (
          <path d={ROUTE_D} fill="none" stroke={GOLD} strokeWidth="9" strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - progress} filter={`url(#${idp}-glow)`} />
        ) : null}
        <circle cx={SHIRE[0]} cy={SHIRE[1]} r="14" fill={RED} stroke={PAPER} strokeWidth="4" />
        <circle cx={HAVENS[0]} cy={HAVENS[1]} r="14" fill={INK} stroke={PAPER} strokeWidth="4" />
        {ring ? (
          <g transform={`translate(${head[0]} ${head[1]})`} filter={`url(#${idp}-glow)`}>
            <ellipse rx="20" ry="15" fill="none" stroke={GOLD_L} strokeWidth="7" />
          </g>
        ) : null}
      </g>
      {stamp > 0 ? (
        <g transform={`translate(${HAVENS[0] - 10} ${HAVENS[1] + 120}) rotate(-12) scale(${interpolate(stamp, [0, 1], [2.2, 1])})`} opacity={Math.min(1, stamp)}>
          <circle r="78" fill="rgba(142,42,31,.08)" stroke={RED} strokeWidth="6" />
          <circle r="64" fill="none" stroke={RED} strokeWidth="2" />
          <ellipse rx="30" ry="24" fill="none" stroke={RED} strokeWidth="8" />
          <text y="52" textAnchor="middle" fontSize="15" letterSpacing="3" fontFamily={TITLE} fill={RED}>À LA MER</text>
        </g>
      ) : null}
    </g>
  );
};

const MapSvg = ({ style, ...props }) => (
  <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0, ...style }}>
    <MapLayer {...props} />
  </svg>
);

// ---------------------------------------------------------------------------
// Original SVG icons
// ---------------------------------------------------------------------------
const ShipIcon = ({ color = INK, sail = '#f2e8cf', width = 300, flip = false }) => (
  <svg viewBox="0 0 300 220" width={width} height={(width * 220) / 300} style={{ overflow: 'visible', scale: flip ? '-1 1' : '1 1' }}>
    <path d="M150 20 L150 160" stroke={color} strokeWidth="5" />
    <path d="M154 28 Q232 80 214 150 L154 150 Z" fill={sail} stroke={color} strokeWidth="3" />
    <path d="M146 40 Q96 90 108 150 L146 150 Z" fill={sail} stroke={color} strokeWidth="3" opacity=".9" />
    <path d="M150 20 l26 8 l-26 8 z" fill={GOLD} />
    <path d="M30 150 L270 150 Q240 196 150 198 Q70 196 44 168 Z" fill={color} />
    <path d="M44 168 Q10 150 22 112 Q30 92 46 100 Q34 110 40 128 Q46 146 60 152" fill="none" stroke={color} strokeWidth="9" strokeLinecap="round" />
    <path d="M44 100 l-14 -4 l10 10 z" fill={GOLD} />
  </svg>
);

const RingIcon = ({ id, size = 200, spin = 0, glow = 1 }) => (
  <svg viewBox="-100 -100 200 200" width={size} height={size} style={{ overflow: 'visible', filter: `drop-shadow(0 0 ${18 * glow}px rgba(243,200,110,${0.8 * glow}))` }}>
    <defs>
      <linearGradient id={id} x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#fff3c6" />
        <stop offset=".5" stopColor="#c58b35" />
        <stop offset="1" stopColor="#f7d991" />
      </linearGradient>
    </defs>
    <g transform={`scale(${Math.max(0.14, Math.abs(Math.cos(spin)))} 1)`}>
      <ellipse rx="70" ry="70" fill="none" stroke={`url(#${id})`} strokeWidth="22" />
      <ellipse rx="57" ry="57" fill="none" stroke="rgba(255,248,220,.5)" strokeWidth="3" />
    </g>
  </svg>
);

// Original hobbit silhouette (Sam) and a slimmer figure (Elanor).
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

const PageLines = ({ seed, count = 13, until = 1 }) => (
  <svg viewBox="0 0 400 540" width="100%" height="100%" style={{ position: 'absolute', inset: 0 }}>
    {Array.from({ length: count }, (_, i) => {
      const w = 220 + random(`${seed}-${i}`) * 110;
      return i / count < until ? <rect key={i} x="48" y={70 + i * 32} width={w} height="5" rx="2.5" fill="rgba(60,40,25,.32)" /> : null;
    })}
  </svg>
);

// CSS-3D Red Book (original design).
const RedBook = ({ open = 0, leaves = [], left = null, right = null }) => {
  const PW = 400;
  const PH = 540;
  return (
    <div style={{ position: 'relative', width: PW * 2, height: PH, perspective: 2400 }}>
      <div style={{ position: 'absolute', left: PW, top: 0, width: PW, height: PH, background: PAGE_BG, borderRadius: '2px 8px 8px 2px', boxShadow: '0 22px 50px rgba(0,0,0,.35), inset 18px 0 30px rgba(90,60,20,.18)', overflow: 'hidden' }}>
        {right}
      </div>
      {leaves.map((p, i) =>
        p > 0 && p < 1 ? (
          <div key={i} style={{ position: 'absolute', left: PW, top: 2, width: PW - 4, height: PH - 4, transformOrigin: 'left center', transform: `rotateY(${-180 * p}deg)`, background: '#f4ead2', boxShadow: '0 0 30px rgba(60,40,20,.25)', borderRadius: '2px 8px 8px 2px' }} />
        ) : null,
      )}
      <div style={{ position: 'absolute', left: PW, top: -8, width: PW + 10, height: PH + 16, transformOrigin: 'left center', transform: `rotateY(${-180 * open}deg)`, transformStyle: 'preserve-3d' }}>
        <div style={{ position: 'absolute', inset: 0, backfaceVisibility: 'hidden', background: 'linear-gradient(135deg,#a3352a,#6d1d14)', borderRadius: '4px 12px 12px 4px', boxShadow: '0 24px 60px rgba(0,0,0,.45)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{ position: 'absolute', inset: 22, border: `3px solid ${GOLD}`, borderRadius: 6 }} />
          <div style={{ fontFamily: TITLE, color: GOLD_L, fontSize: 40, textAlign: 'center', lineHeight: 1.3, letterSpacing: '.08em' }}>
            LE LIVRE
            <br />
            ROUGE
          </div>
        </div>
        <div style={{ position: 'absolute', inset: 0, backfaceVisibility: 'hidden', transform: 'rotateY(180deg)', background: PAGE_BG, borderRadius: '8px 2px 2px 8px', overflow: 'hidden' }}>{left}</div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Typography helpers
// ---------------------------------------------------------------------------
const KineticTitle = ({ lines, top = 70, left = 120, width = 1680, align = 'center', delay = 0, stagger = 4, color = INK, shadow }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  let n = 0;
  return (
    <div style={{ position: 'absolute', top, left, width, textAlign: align, fontFamily: TITLE, fontWeight: 700, color, letterSpacing: '0.03em', textShadow: shadow }}>
      {lines.map((line, li) => {
        // Conservative width estimate for Cinzel capitals keeps every line inside the safe area.
        const size = Math.min(line.size ?? 96, Math.floor(width / (line.text.length * 0.8)));
        const words = line.text.split(' ');
        return (
          <div key={li} style={{ fontSize: size, lineHeight: 1.14, whiteSpace: 'nowrap', color: line.color ?? color }}>
            {words.map((word, wi) => {
              const s = spring({ frame: frame - delay - (line.delay ?? 0) - n++ * stagger, fps, config: { damping: 200 }, durationInFrames: 18 });
              return (
                <span key={wi} style={{ display: 'inline-block', marginRight: wi < words.length - 1 ? '0.25em' : 0, opacity: s, translate: `0px ${(1 - s) * 0.45 * size}px`, filter: `blur(${(1 - s) * 6}px)` }}>
                  {word}
                </span>
              );
            })}
          </div>
        );
      })}
    </div>
  );
};

const Pop = ({ at = 0, children, style, rise = 30 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - at, fps, config: { damping: 12, stiffness: 160 } });
  return <div style={{ opacity: Math.min(1, s * 1.4), scale: String(0.6 + 0.4 * s), translate: `0px ${(1 - s) * rise}px`, ...style }}>{children}</div>;
};

// ---------------------------------------------------------------------------
// Shared environment layers
// ---------------------------------------------------------------------------
const Grain = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0, mixBlendMode: 'multiply', opacity: 0.16 }}>
        <filter id="v2-fibers">
          <feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves="3" seed="7" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width={W} height={H} filter="url(#v2-fibers)" />
      </svg>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0, mixBlendMode: 'multiply', opacity: 0.2 }}>
        <filter id="v2-grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed={frame % 7} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width={W} height={H} filter="url(#v2-grain)" />
      </svg>
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(25,15,6,.5) 100%)' }} />
    </AbsoluteFill>
  );
};

const Coast = ({ sunX = 760, mist = 0.5, drift = 0, light = 1 }) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: 'linear-gradient(180deg, #b9c7c6 0%, #e6d9b6 52%, #f1dfb1 56%)' }} />
      <AbsoluteFill style={{ background: `radial-gradient(circle at ${sunX}px 560px, rgba(255,236,180,${0.85 * light}) 0px, rgba(255,226,160,${0.35 * light}) 160px, rgba(255,220,150,0) 480px)` }} />
      <div style={{ position: 'absolute', left: 0, top: 590, width: W, height: H - 590, background: 'linear-gradient(180deg, #6f8c8d 0%, #3d5a60 60%, #2a4248 100%)' }} />
      <div style={{ position: 'absolute', left: sunX - 90, top: 590, width: 180, height: 490, background: `linear-gradient(180deg, rgba(255,232,170,${0.7 * light}), rgba(255,232,170,0))`, filter: 'blur(14px)' }} />
      {Array.from({ length: 26 }, (_, i) => {
        const x = random(`g${i}`) * W;
        const y = 610 + random(`gy${i}`) * 440;
        const a = 0.5 + 0.5 * Math.sin(frame / 7 + i * 1.7);
        return <div key={i} style={{ position: 'absolute', left: x + Math.sin(frame / 25 + i) * 10, top: y, width: 40 + random(`gw${i}`) * 90, height: 3, borderRadius: 2, background: `rgba(255,240,200,${0.35 * a})` }} />;
      })}
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0, translate: `${drift * 0.35}px 0px` }}>
        <path d="M1060 592 C1250 520 1400 560 1560 500 C1700 450 1820 470 1920 430 L1920 600 L1060 600 Z" fill="#6c7d74" opacity=".75" />
      </svg>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0, translate: `${drift}px 0px` }}>
        <path d="M1240 640 C1380 560 1560 600 1680 540 C1800 490 1880 520 1960 500 L1960 1080 L1180 1080 C1220 900 1150 760 1240 640 Z" fill="#2f3d36" />
        <path d="M1260 652 L1080 662 L1080 676 L1270 670 Z" fill="#2a241d" />
      </svg>
      {[0, 1, 2].map((i) => (
        <div key={i} style={{ position: 'absolute', left: -400 + ((frame * (0.6 + i * 0.5) + i * 500) % 900), top: 470 + i * 70, width: 1900, height: 160, background: `radial-gradient(ellipse at center, rgba(255,255,255,${0.55 * mist}) 0%, rgba(255,255,255,0) 70%)`, filter: 'blur(10px)' }} />
      ))}
    </AbsoluteFill>
  );
};

const Timeline = ({ head, opacity = 1 }) => (
  <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0, opacity }}>
    <line x1="220" y1="600" x2="1560" y2="600" stroke="rgba(43,34,25,.25)" strokeWidth="4" strokeDasharray="8 10" />
    {Array.from({ length: 16 }, (_, i) => (
      <line key={i} x1={220 + i * 89} y1="584" x2={220 + i * 89} y2="616" stroke={INK} strokeWidth="3" opacity={220 + i * 89 <= head ? 0.9 : 0.25} />
    ))}
    <line x1="220" y1="600" x2={head} y2="600" stroke={GOLD} strokeWidth="10" strokeLinecap="round" />
    <line x1={head} y1="560" x2={head} y2="640" stroke={RED} strokeWidth="6" />
    <text x="1700" y="640" textAnchor="middle" fontSize="150" fontFamily={`${FALLBACK}, serif`} fill="rgba(43,34,25,.28)">∞</text>
  </svg>
);

// ---------------------------------------------------------------------------
// The 18 storyboard beats
// ---------------------------------------------------------------------------
const Beat01 = () => {
  const frame = useCurrentFrame();
  const r = interpolate(frame, [4, 40], [0, 380], { ...clamp, easing: EASE });
  const ring = interpolate(frame, [0, 46], [0, 1], { ...clamp, easing: EASE });
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <div style={{ position: 'absolute', inset: -60, scale: String(interpolate(frame, [0, 96], [1.08, 1.15])), translate: `${interpolate(frame, [0, 96], [20, -30])}px 0px`, opacity: 0.5, filter: 'blur(1.5px)' }}>
        <MapSvg idp="b1" labels={0.6} />
      </div>
      <div style={{ position: 'absolute', left: 1060, top: 100, width: 760, height: 760, clipPath: `circle(${r}px at 50% 50%)`, translate: `${interpolate(frame, [0, 96], [0, -24])}px 0px` }}>
        <Img src={staticFile('assets/bag_end_hobbiton.jpg')} style={{ position: 'absolute', left: -25, top: interpolate(frame, [0, 96], [-10, -45]), width: 900 }} />
      </div>
      <svg width="800" height="800" viewBox="0 0 800 800" style={{ position: 'absolute', left: 1040, top: 80, translate: `${interpolate(frame, [0, 96], [0, -24])}px 0px` }}>
        <circle cx="400" cy="400" r="384" fill="none" stroke={GOLD} strokeWidth="6" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - ring} />
      </svg>
      <div style={{ position: 'absolute', left: interpolate(frame, [0, 96], [1980, -380]), top: 600 + Math.sin(frame / 6) * 6 }}>
        <ShipIcon width={320} />
      </div>
      <KineticTitle top={200} left={110} width={900} align="left" lines={[{ text: 'FRODON PART…', size: 120 }]} />
    </AbsoluteFill>
  );
};

const Beat02 = () => {
  const frame = useCurrentFrame();
  const reveal = interpolate(frame, [0, 14], [90, 1300], { ...clamp, easing: EASE });
  const walk = interpolate(frame, [6, 96], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: INK }}>
      <AbsoluteFill style={{ clipPath: `circle(${reveal}px at 864px 520px)`, overflow: 'hidden' }}>
        {/* Portrait photo shown as a controlled horizontal band: oak tree + round door stay in frame. */}
        <div style={{ position: 'absolute', inset: 0, scale: String(interpolate(frame, [0, 96], [1, 1.14], { ...clamp, easing: INOUT })), transformOrigin: '864px 520px' }}>
          <Img src={staticFile('assets/bag_end_hobbiton.jpg')} style={{ position: 'absolute', left: 0, top: interpolate(frame, [0, 96], [-300, -360]), width: W, height: (W * 2880) / 1920 }} />
        </div>
        <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(20,15,8,.72) 0%, rgba(20,15,8,.25) 42%, rgba(20,15,8,0) 60%)' }} />
        <div style={{ position: 'absolute', left: interpolate(walk, [0, 1], [1640, 1180]), bottom: 150, filter: 'drop-shadow(0 0 3px rgba(255,244,214,.95)) drop-shadow(0 0 16px rgba(255,236,190,.65))' }}>
          <Figure height={240} facing={-1} phase={frame / 3.2} color="#1f1a14" />
        </div>
      </AbsoluteFill>
      <KineticTitle top={150} left={110} width={900} align="left" color="#f6edd6" shadow="0 4px 24px rgba(0,0,0,.6)" lines={[{ text: 'SAM RENTRE', size: 110 }, { text: 'DANS LA COMTÉ', size: 86, color: GOLD_L, delay: 8 }]} />
    </AbsoluteFill>
  );
};

const ART_W = 640;
const ART_H = (ART_W * 1322) / 1280; // exact aspect of sam_illustration.jpg: no crop, no distortion

const Beat03 = () => {
  const frame = useCurrentFrame();
  const px = interpolate(frame, [0, 96], [-10, 10]);
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <div style={{ position: 'absolute', inset: -40, opacity: 0.28, translate: `${px * 3}px 0px` }}>
        <MapSvg idp="b3" labels={0} />
      </div>
      {/* backplate (moves more = depth) */}
      <div style={{ position: 'absolute', left: 120 + px * 2.4, top: 60, width: 780, height: 830, rotate: '-3deg', background: '#d9c69b', boxShadow: '0 20px 60px rgba(40,25,10,.3)' }} />
      {/* frame: the artwork itself is never cropped, recoloured or retouched */}
      <div style={{ position: 'absolute', left: 170 + px, top: 88, padding: 16, background: 'linear-gradient(135deg,#d9b25f,#8a6424 50%,#e3c27a)', borderRadius: 6, boxShadow: '0 30px 70px rgba(30,20,10,.45)', scale: String(interpolate(frame, [0, 16], [0.96, 1], { ...clamp, easing: EASE })) }}>
        <div style={{ padding: 14, background: '#f6eedb' }}>
          <Img src={staticFile('assets/sam_illustration.jpg')} style={{ display: 'block', width: ART_W, height: ART_H }} />
        </div>
      </div>
      <div style={{ position: 'absolute', left: 170 + px, top: 828, width: 732, textAlign: 'center', fontFamily: BODY, fontSize: 24, fontWeight: 600, color: 'rgba(43,34,25,.85)' }}>
        Fan art « Sam Gamegie » — Lucie Vergne, CC BY-SA 4.0
      </div>
      <div style={{ position: 'absolute', left: 960, top: 300, width: 900, display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
        {[
          { at: 12, label: 'ROSIE', icon: <Figure variant="elanor" height={130} color={RED} /> },
          { at: 49, label: 'LES ENFANTS', icon: <div style={{ display: 'flex', gap: 6, alignItems: 'flex-end' }}><Figure variant="sam" height={86} /><Figure variant="elanor" height={100} /><Figure variant="sam" height={72} /></div> },
          { at: 88, label: 'LE LIVRE', icon: <BookMini width={100} /> },
        ].map((item, i) => (
          <React.Fragment key={item.label}>
            {i > 0 ? <Pop at={item.at} style={{ fontFamily: TITLE, fontSize: 60, color: GOLD, marginTop: 70 }}>·</Pop> : null}
            <Pop at={item.at} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22 }}>
              <div style={{ width: 210, height: 210, borderRadius: 105, background: '#f6eedb', border: `4px solid ${GOLD}`, display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 12px 30px rgba(40,25,10,.25)' }}>{item.icon}</div>
              <div style={{ fontFamily: TITLE, fontWeight: 700, fontSize: 44, color: INK, letterSpacing: '0.04em', whiteSpace: 'nowrap' }}>{item.label}</div>
            </Pop>
          </React.Fragment>
        ))}
      </div>
    </AbsoluteFill>
  );
};

const Beat04 = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const bg = interpolateColors(frame, [0, 32, 64, 96], ['#a9b97a', '#d6a54c', '#a7b3bd', '#b8c88c']);
  const open = spring({ frame: frame - 4, fps, config: { damping: 200 }, durationInFrames: 30 });
  const leaves = [0, 1, 2].map((i) => interpolate(frame, [28 + i * 12, 48 + i * 12], [0, 1], { ...clamp, easing: INOUT }));
  return (
    <AbsoluteFill style={{ background: bg }}>
      {Array.from({ length: 22 }, (_, i) => {
        const x = random(`lf${i}`) * W + Math.sin(frame / 12 + i) * 30;
        const y = -60 + ((random(`ly${i}`) * 1200 + frame * (3 + random(`ls${i}`) * 3)) % 1200);
        return <div key={i} style={{ position: 'absolute', left: x, top: y, width: 22, height: 12, borderRadius: '50%', rotate: `${frame * 4 + i * 40}deg`, background: interpolateColors(frame, [0, 32, 64, 96], ['#6d8a3c', '#b4562a', '#f4f4f0', '#7c9a48']), opacity: 0.7 }} />;
      })}
      <div style={{ position: 'absolute', left: 560, top: 330, scale: String(interpolate(frame, [0, 96], [0.88, 0.96])), transformOrigin: '400px 270px' }}>
        <RedBook open={open} leaves={leaves} left={<PageLines seed="b4l" />} right={<PageLines seed="b4r" />} />
      </div>
      <KineticTitle top={90} lines={[{ text: 'DES ANNÉES PLUS TARD', size: 100 }]} />
    </AbsoluteFill>
  );
};

const Beat05 = () => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [23, 65], [0, 1], { ...clamp, easing: INOUT });
  const bookX = interpolate(t, [0, 1], [330, 620]);
  const bookY = 600 - Math.sin(t * Math.PI) * 120;
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <div style={{ position: 'absolute', left: 150, top: 470 }}>
        <Figure height={330} />
      </div>
      <div style={{ position: 'absolute', left: 600, top: 440 }}>
        <Figure variant="elanor" height={360} facing={-1} color="#4a3a2a" />
      </div>
      <div style={{ position: 'absolute', left: bookX, top: bookY, rotate: `${t * 360}deg`, filter: 'drop-shadow(0 0 16px rgba(243,214,138,.8))' }}>
        <BookMini width={70} />
      </div>
      <div style={{ position: 'absolute', left: 960, top: 230, width: 860, height: 484, overflow: 'hidden', border: `4px solid ${INK}`, boxShadow: '0 20px 50px rgba(40,25,10,.3)', opacity: interpolate(frame, [49, 65], [0, 1], clamp), translate: `${interpolate(frame, [49, 69], [60, 0], { ...clamp, easing: EASE })}px 0px` }}>
        <MapSvg idp="b5" progress={interpolate(frame, [65, 115], [0, 0.4], clamp)} ring />
      </div>
      <div style={{ position: 'absolute', top: 80, width: W, display: 'flex', justifyContent: 'center', gap: 36, fontFamily: TITLE, fontWeight: 700, fontSize: 92, color: INK }}>
        <Pop at={51}>ELANOR</Pop>
        <Pop at={77} style={{ color: GOLD }}>→</Pop>
        <Pop at={91}>HAVRES GRIS</Pop>
      </div>
    </AbsoluteFill>
  );
};

const Beat06 = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const hit = spring({ frame: frame - 7, fps, config: { damping: 9, stiffness: 220 } });
  const k = interpolate(frame, [52, 96], [1, 14], { ...clamp, easing: Easing.in(Easing.cubic) });
  const ink = interpolate(frame, [34, 50], [1, 0], clamp);
  const tf = `translate(960 540) scale(${k * interpolate(hit, [0, 1], [1.6, 1])}) translate(-960 -540)`;
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0, translate: `${(1 - hit) * 14 * Math.sin(frame * 3)}px 0px` }}>
        <defs>
          <mask id="pq-mask">
            <rect width={W} height={H} fill="black" />
            <text x="960" y="625" textAnchor="middle" fontSize="250" fontWeight="700" fontFamily={TITLE} fill="white" transform={tf} opacity={Math.min(1, hit)}>POURQUOI ?</text>
          </mask>
        </defs>
        <g mask="url(#pq-mask)">
          <MapLayer idp="b6" progress={0.15} />
        </g>
        <text x="960" y="625" textAnchor="middle" fontSize="250" fontWeight="700" fontFamily={TITLE} fill={INK} transform={tf} opacity={Math.min(1, hit) * ink}>POURQUOI ?</text>
      </svg>
    </AbsoluteFill>
  );
};

const Beat07 = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const progress = interpolate(frame, [0, 56], [0.15, 1], { ...clamp, easing: INOUT });
  const stamp = spring({ frame: frame - 56, fps, config: { damping: 14, stiffness: 200 } });
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <div style={{ position: 'absolute', inset: 0, scale: String(interpolate(frame, [0, 96], [1, 1.12])), transformOrigin: '900px 520px' }}>
        <MapSvg idp="b7" progress={progress} ring stamp={stamp} />
      </div>
      <KineticTitle top={70} delay={4} lines={[{ text: 'LE DERNIER PORTEUR', size: 100 }]} shadow="0 2px 18px rgba(234,223,196,.9)" />
    </AbsoluteFill>
  );
};

const Beat08 = () => {
  const frame = useCurrentFrame();
  const trace = interpolate(frame, [14, 56], [0, 1], { ...clamp, easing: INOUT });
  const traceOut = interpolate(frame, [62, 86], [1, 0], clamp);
  const rx = interpolate(frame, [0, 90], [1500, 360], { ...clamp, easing: INOUT });
  const ry = 360 - Math.sin(interpolate(frame, [0, 90], [0, Math.PI], clamp)) * 120;
  return (
    <AbsoluteFill style={{ background: 'radial-gradient(circle at 50% 62%, #5a4426 0%, #2a1f14 70%)' }}>
      <div style={{ position: 'absolute', left: 860, top: 460, filter: `drop-shadow(0 0 ${30 * traceOut * trace}px rgba(243,214,138,.9))` }}>
        <Figure height={330} color="#120d08" />
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0 }}>
        <ellipse cx="970" cy="630" rx="210" ry="250" fill="none" stroke={GOLD_L} strokeWidth="5" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - trace} opacity={traceOut} style={{ filter: 'drop-shadow(0 0 10px rgba(243,214,138,.9))' }} />
      </svg>
      <div style={{ position: 'absolute', left: rx - 90, top: ry - 90 }}>
        <RingIcon id="b8-ring" size={180} spin={frame / 7} />
      </div>
      <KineticTitle top={60} color="#f6edd6" lines={[{ text: 'SAM AUSSI A PORTÉ L’ANNEAU', size: 84 }, { text: 'BRIÈVEMENT', size: 76, color: GOLD_L, delay: 27 }]} />
    </AbsoluteFill>
  );
};

const SeaPanel = ({ label, mirror, frame, lag = 0 }) => {
  const f = frame - lag;
  const sx = interpolate(f, [0, 96], mirror ? [140, 560] : [560, 140], { ...clamp, easing: INOUT });
  return (
    <div style={{ position: 'relative', width: 900, height: 620, overflow: 'hidden', border: `4px solid ${INK}`, background: 'linear-gradient(180deg,#c6d0cb 0%,#efdfb6 52%,#5d7b80 54%,#2d474d 100%)' }}>
      {Array.from({ length: 12 }, (_, i) => (
        <div key={i} style={{ position: 'absolute', left: (random(`sp${i}`) * 900 + f * (mirror ? 1.5 : -1.5) + 900) % 900, top: 350 + random(`spy${i}`) * 250, width: 60, height: 3, background: 'rgba(255,240,200,.35)' }} />
      ))}
      <div style={{ position: 'absolute', left: sx, top: 200 + Math.sin(f / 7) * 5 }}>
        <ShipIcon width={220} flip={mirror} />
      </div>
      <div style={{ position: 'absolute', top: 24, width: '100%', textAlign: 'center', fontFamily: TITLE, fontWeight: 700, fontSize: 46, color: INK, letterSpacing: '0.12em' }}>{label}</div>
    </div>
  );
};

const Beat09 = () => {
  const frame = useCurrentFrame();
  const apart = interpolate(frame, [40, 70], [0, 150], { ...clamp, easing: INOUT });
  const enter = interpolate(frame, [0, 14], [0, 1], { ...clamp, easing: EASE });
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <div style={{ position: 'absolute', left: 50 - apart, top: 230, translate: `${(1 - enter) * -300}px 0px`, opacity: enter }}>
        <SeaPanel label="FRODON" frame={frame} />
      </div>
      <div style={{ position: 'absolute', left: 970 + apart, top: 230, translate: `${(1 - enter) * 300}px 0px`, opacity: enter }}>
        <SeaPanel label="SAM" frame={frame} mirror lag={8} />
      </div>
      <KineticTitle top={70} lines={[{ text: 'UN DÉPART EN ÉCHO', size: 100 }]} />
    </AbsoluteFill>
  );
};

const Beat10 = () => {
  const frame = useCurrentFrame();
  const open = interpolate(frame, [6, 50], [1, 0.62], { ...clamp, easing: INOUT });
  const lineP = interpolate(frame, [4, 44], [0, 1], { ...clamp, easing: EASE });
  const q = interpolate(frame, [38, 60], [0, 120], { ...clamp, easing: EASE });
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <div style={{ position: 'absolute', inset: 0, opacity: 0.3 }}>
        <MapSvg idp="b10" labels={0} routeOpacity={0} />
      </div>
      <div style={{ position: 'absolute', left: -60, top: 420, scale: '0.6', transformOrigin: '0 0' }}>
        <RedBook open={open} left={<PageLines seed="b10l" />} right={<PageLines seed="b10r" until={0.55} />} />
      </div>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0 }}>
        <line x1="760" y1="600" x2={760 + 440 * lineP} y2="600" stroke={GOLD} strokeWidth="9" strokeLinecap="round" />
        <line x1="1800" y1="600" x2={1800 - 440 * lineP} y2="600" stroke={GOLD} strokeWidth="9" strokeLinecap="round" />
        <circle cx="760" cy="600" r="16" fill={INK} />
        <circle cx="1800" cy="600" r="16" fill={RED} />
        <text x="760" y="680" textAnchor="middle" fontSize="40" fontFamily={TITLE} fontWeight="700" fill={INK}>FRODON</text>
        <text x="1800" y="680" textAnchor="middle" fontSize="40" fontFamily={TITLE} fontWeight="700" fill={INK}>SAM</text>
        <defs>
          <clipPath id="b10-q">
            <circle cx="1280" cy="560" r={q} />
          </clipPath>
        </defs>
        <text x="1280" y="625" textAnchor="middle" fontSize="170" fontFamily={TITLE} fontWeight="700" fill={RED} clipPath="url(#b10-q)">?</text>
      </svg>
      <KineticTitle top={80} lines={[{ text: 'PAS DE RETROUVAILLES RACONTÉES', size: 90 }]} />
    </AbsoluteFill>
  );
};

const Beat11 = () => {
  const frame = useCurrentFrame();
  const ringY = interpolate(frame, [0, 36], [300, 615], { ...clamp, easing: Easing.in(Easing.quad) });
  const ringOp = interpolate(frame, [30, 56], [1, 0], clamp);
  return (
    <AbsoluteFill>
      <Coast drift={interpolate(frame, [0, 96], [0, -60])} sunX={interpolate(frame, [0, 96], [700, 760])} mist={0.4} />
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0 }}>
        {[0, 1, 2, 3].map((i) => {
          const p = interpolate(frame, [34 + i * 9, 80 + i * 9], [0, 1], clamp);
          return p > 0 ? <ellipse key={i} cx="760" cy="640" rx={40 + p * 360} ry={(40 + p * 360) * 0.12} fill="none" stroke="rgba(255,228,160,.9)" strokeWidth="3" opacity={1 - p} /> : null;
        })}
        {Array.from({ length: 18 }, (_, i) => {
          const a = interpolate(frame, [38, 60, 96], [0, 1, 0.2], clamp) * (0.5 + 0.5 * Math.sin(frame / 4 + i * 2.1));
          return <rect key={i} x={760 + (random(`rg${i}`) - 0.5) * 520} y={650 + random(`rgy${i}`) * 160} width={30 + random(`rgw${i}`) * 60} height="4" rx="2" fill={GOLD_L} opacity={a} />;
        })}
      </svg>
      <div style={{ position: 'absolute', left: 760 - 70, top: ringY - 70, opacity: ringOp, scale: String(interpolate(frame, [0, 36], [1.2, 0.7], clamp)) }}>
        <RingIcon id="b11-ring" size={140} spin={frame / 6} />
      </div>
      <KineticTitle top={90} lines={[{ text: 'AMAN ≠ IMMORTALITÉ', size: 104 }]} shadow="0 2px 20px rgba(241,223,177,.9)" />
    </AbsoluteFill>
  );
};

const HighlightWord = ({ word, at, appear }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: frame - appear, fps, config: { damping: 200 }, durationInFrames: 16 });
  const p = interpolate(frame, [at, at + 12], [0, 1], { ...clamp, easing: EASE });
  return (
    <span style={{ display: 'inline-block', margin: '0 0.15em', padding: '0 0.12em', opacity: s, translate: `0px ${(1 - s) * 40}px`, backgroundImage: `linear-gradient(${GOLD_L}, ${GOLD_L})`, backgroundRepeat: 'no-repeat', backgroundSize: `${p * 100}% 36%`, backgroundPosition: '0 88%', scale: String(1 + 0.06 * Math.sin(Math.min(1, p) * Math.PI)) }}>
      {word}
    </span>
  );
};

const Beat12 = () => {
  const frame = useCurrentFrame();
  const head = interpolate(frame, [0, 72], [220, 1450], { ...clamp, easing: INOUT });
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <Timeline head={head} />
      <div style={{ position: 'absolute', left: head - 70, top: 470 + Math.sin(frame / 6) * 4 }}>
        <ShipIcon width={140} />
      </div>
      <div style={{ position: 'absolute', top: 150, width: W, textAlign: 'center', fontFamily: TITLE, fontWeight: 700, fontSize: 120, color: INK }}>
        {/* Beat spans 32.68–35.20 s; both highlights complete before the cut */}
        <HighlightWord word="SÉJOUR" appear={0} at={22} />
        <HighlightWord word="LIMITÉ" appear={8} at={52} />
      </div>
    </AbsoluteFill>
  );
};

const Beat13 = () => {
  const frame = useCurrentFrame();
  const head = interpolate(frame, [0, 48], [1450, 220], { ...clamp, easing: INOUT });
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <Timeline head={head} opacity={interpolate(frame, [20, 64], [1, 0], clamp)} />
      {Array.from({ length: 48 }, (_, i) => {
        const x0 = 500 + random(`p${i}`) * 1500;
        const x = x0 - frame * (4 + random(`ps${i}`) * 7);
        const y = 220 + random(`py${i}`) * 640 + Math.sin(frame / 10 + i) * 12;
        const o = interpolate(frame, [10, 30, 80, 96], [0, 0.85, 0.85, 0], clamp);
        return <div key={i} style={{ position: 'absolute', left: x, top: y, width: 6 + random(`pr${i}`) * 8, height: 6 + random(`pr${i}`) * 8, borderRadius: '50%', background: GOLD, opacity: o, boxShadow: '0 0 12px rgba(243,214,138,.9)' }} />;
      })}
      <KineticTitle top={150} lines={[{ text: 'PAS POUR TOUJOURS', size: 110 }]} />
    </AbsoluteFill>
  );
};

const Beat14 = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Coast drift={interpolate(frame, [0, 96], [-40, 20])} sunX={interpolate(frame, [0, 96], [620, 900])} mist={0.75} light={interpolate(frame, [0, 96], [0.7, 1.1])} />
      <div style={{ position: 'absolute', top: 200, width: W, display: 'flex', justifyContent: 'center', alignItems: 'center', gap: 50, fontFamily: TITLE, fontWeight: 700, fontSize: 130, color: INK, textShadow: '0 2px 24px rgba(255,240,200,.9)' }}>
        <Pop at={24}>PAIX</Pop>
        <Pop at={44} style={{ color: GOLD }}>·</Pop>
        <Pop at={50}>GUÉRISON</Pop>
      </div>
    </AbsoluteFill>
  );
};

const Beat15 = () => {
  const frame = useCurrentFrame();
  const zoom = interpolate(frame, [0, 96], [1, 2.3], { ...clamp, easing: INOUT });
  const fog = interpolate(frame, [20, 80], [0, 0.85], clamp);
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <div style={{ position: 'absolute', inset: 0, scale: String(zoom), transformOrigin: `${HAVENS[0]}px ${HAVENS[1]}px` }}>
        <MapSvg idp="b15" progress={1} routeOpacity={1 - fog} labels={1 - fog} />
      </div>
      <AbsoluteFill style={{ background: `linear-gradient(90deg, rgba(246,244,238,${fog}) 0%, rgba(246,244,238,${fog * 0.7}) 60%, rgba(246,244,238,${fog * 0.3}) 100%)` }} />
      {[0, 1].map((i) => (
        <div key={i} style={{ position: 'absolute', left: -500 + frame * (2 + i), top: 300 + i * 220, width: 2400, height: 260, background: `radial-gradient(ellipse at center, rgba(255,255,255,${0.7 * fog}) 0%, rgba(255,255,255,0) 70%)`, filter: 'blur(12px)' }} />
      ))}
      {/* Upper safe area: the HAVRES GRIS label sits just above the zoom origin and would collide with a mid-frame title. */}
      <KineticTitle top={90} delay={6} lines={[{ text: 'SAM A-T-IL REVU FRODON ?', size: 104 }]} shadow="0 2px 24px rgba(246,244,238,.95)" />
    </AbsoluteFill>
  );
};

const Beat16 = () => {
  const frame = useCurrentFrame();
  const write = interpolate(frame, [12, 70], [0, 1], { ...clamp, easing: INOUT });
  const dots = interpolate(frame, [68, 80], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: 'radial-gradient(circle at 50% 60%, #f1e5c8 0%, #cdb487 100%)' }}>
      <div style={{ position: 'absolute', left: 560, top: 330, scale: String(interpolate(frame, [0, 96], [0.86, 0.92])), transformOrigin: '400px 270px' }}>
        <RedBook
          open={1}
          left={<PageLines seed="b16l" />}
          right={
            <svg viewBox="0 0 400 540" width="100%" height="100%" style={{ position: 'absolute', inset: 0 }}>
              <path d="M44 210 c18 -30 36 28 54 0 s36 -30 54 0 s36 28 54 0 s34 -26 52 0" fill="none" stroke={INK} strokeWidth="3.5" strokeLinecap="round" pathLength={1} strokeDasharray="1 1" strokeDashoffset={1 - write} />
              <text x="268" y="222" fontSize="54" fontFamily={BODY} fontStyle="italic" fill={INK} opacity={dots}>…</text>
            </svg>
          }
        />
      </div>
      <KineticTitle top={60} lines={[{ text: 'LE LIVRE LAISSE', size: 90 }, { text: 'LA QUESTION OUVERTE', size: 90, delay: 8 }]} />
    </AbsoluteFill>
  );
};

const Beat17 = () => {
  const frame = useCurrentFrame();
  const walk = interpolate(frame, [0, 56], [0, 1], { ...clamp, easing: Easing.inOut(Easing.quad) });
  const board = interpolate(frame, [50, 64], [1, 0], clamp);
  const sail = interpolate(frame, [58, 132], [0, 1], { ...clamp, easing: Easing.in(Easing.quad) });
  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      <AbsoluteFill style={{ scale: String(interpolate(frame, [0, 132], [1.28, 1], { ...clamp, easing: INOUT })), transformOrigin: '1100px 620px' }}>
        <Coast drift={interpolate(frame, [0, 132], [0, -30])} sunX={600} mist={0.45} />
        <div style={{ position: 'absolute', left: interpolate(sail, [0, 1], [930, 180]), top: interpolate(sail, [0, 1], [500, 548]), scale: String(interpolate(sail, [0, 1], [1, 0.35])), transformOrigin: '0 100%' }}>
          <ShipIcon width={260} color="#1f1a14" />
        </div>
        <div style={{ position: 'absolute', left: interpolate(walk, [0, 1], [1380, 1110]), top: 500, opacity: board }}>
          <Figure height={170} facing={-1} phase={frame / 3} book color="#1a1510" />
        </div>
      </AbsoluteFill>
      <KineticTitle top={70} color="#2b2219" shadow="0 2px 20px rgba(241,223,177,.95)" lines={[{ text: 'IL PREND À SON TOUR', size: 92 }, { text: 'LA ROUTE DE L’OUEST', size: 92, color: RED, delay: 10 }]} />
    </AbsoluteFill>
  );
};

const Beat18 = ({ duration }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const fadeScene = interpolate(frame, [0, 40], [1, 0], clamp);
  const bubble = spring({ frame: frame - 62, fps, config: { damping: 12, stiffness: 150 } });
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <AbsoluteFill style={{ opacity: fadeScene }}>
        <Coast sunX={600} mist={0.6} />
        <div style={{ position: 'absolute', left: 540, top: 420, opacity: 0.9 }}>
          <RingIcon id="b18-ring" size={120} spin={frame / 9} />
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ scale: String(interpolate(frame, [0, 132], [1, 1.05])) }}>
        <KineticTitle top={300} delay={20} stagger={5} lines={[{ text: 'ET VOUS, VOUS IMAGINEZ', size: 96 }, { text: 'LEURS RETROUVAILLES ?', size: 96, color: RED }]} />
        <div style={{ position: 'absolute', left: 960 - 70, top: 640, opacity: Math.min(1, bubble), scale: String(0.5 + 0.5 * bubble) }}>
          <svg viewBox="0 0 140 120" width="140" height="120">
            <path d="M14 10 H126 Q134 10 134 18 V78 Q134 86 126 86 H58 L30 112 L34 86 H14 Q6 86 6 78 V18 Q6 10 14 10 Z" fill={INK} />
            {[44, 70, 96].map((x, i) => (
              <circle key={x} cx={x} cy="48" r="8" fill={GOLD_L} opacity={0.4 + 0.6 * Math.max(0, Math.sin(frame / 5 - i))} />
            ))}
          </svg>
        </div>
      </AbsoluteFill>
      <AbsoluteFill style={{ background: '#000', opacity: interpolate(frame, [duration - 14, duration], [0, 1], clamp) }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Word-level captions: rolling phrase, active word highlighted
// ---------------------------------------------------------------------------
const CAPTION_PAGES = (() => {
  const pages = [];
  let cur = [];
  captions.forEach((c, i) => {
    const prev = captions[i - 1];
    if (cur.length) {
      const prevText = prev.text.trim();
      const sentenceEnd = /[.?!]$/.test(prevText);
      const softBreak = /[,—]$/.test(prevText) && cur.length >= 3;
      if (sentenceEnd || softBreak || cur.length >= 6 || c.startMs - prev.endMs > 450) {
        pages.push(cur);
        cur = [];
      }
    }
    cur.push(c);
  });
  if (cur.length) pages.push(cur);
  return pages.map((tokens, i, arr) => ({
    tokens,
    startMs: tokens[0].startMs,
    endMs: Math.min(tokens[tokens.length - 1].endMs + 700, arr[i + 1] ? arr[i + 1][0].startMs : Infinity),
  }));
})();

const Captions = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ms = (frame / fps) * 1000;
  const page = CAPTION_PAGES.find((p) => ms >= p.startMs - 120 && ms < p.endMs);
  if (!page) return null;
  const pageIn = interpolate(ms, [page.startMs - 120, page.startMs + 60], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 54, pointerEvents: 'none' }}>
      <div style={{ maxWidth: 1500, padding: '12px 34px 16px', borderRadius: 18, background: 'rgba(24,18,12,.68)', boxShadow: '0 10px 30px rgba(0,0,0,.25)', textAlign: 'center', opacity: pageIn, translate: `0px ${(1 - pageIn) * 14}px`, fontFamily: BODY, fontWeight: 600, fontSize: 52, lineHeight: 1.18, color: '#f4ead2' }}>
        {page.tokens.map((t, i) => {
          const next = page.tokens[i + 1];
          const active = ms >= t.startMs && (next ? ms < next.startMs : ms < t.endMs + 300);
          const spoken = ms >= t.startMs;
          const pop = spring({ frame: frame - Math.round((t.startMs / 1000) * fps), fps, config: { damping: 14, stiffness: 190 }, durationInFrames: 12 });
          return (
            <span key={i} style={{ display: 'inline-block', marginRight: next ? '0.3em' : 0, color: active ? GOLD_L : spoken ? '#f4ead2' : 'rgba(244,234,210,.42)', scale: active ? String(interpolate(pop, [0, 1], [1.08, 1.02])) : '1', translate: active ? `0px ${-4 * pop}px` : '0px 0px', textShadow: active ? '0 0 18px rgba(243,214,138,.55)' : 'none' }}>
              {t.text.trim()}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------------------
// Audio: unchanged narration + original bed (ducked) + original SFX
// ---------------------------------------------------------------------------
const SPEECH = captions.reduce((acc, c) => {
  const last = acc[acc.length - 1];
  if (last && c.startMs - last[1] < 350) last[1] = c.endMs;
  else acc.push([c.startMs, c.endMs]);
  return acc;
}, []);

const bedVolume = (f, fps) => {
  const ms = (f / fps) * 1000;
  let dist = Infinity;
  for (const [a, b] of SPEECH) {
    if (ms >= a && ms <= b) {
      dist = 0;
      break;
    }
    dist = Math.min(dist, ms < a ? a - ms : ms - b);
  }
  const duck = interpolate(dist, [0, 400], [0.1, 0.3], clamp);
  const fade = interpolate(f, [0, 1.5 * fps, 57 * fps, 60 * fps - 1], [0, 1, 1, 0], clamp);
  return duck * fade;
};

const Sfx = ({ name, file, at, seconds, volume }) => {
  const { fps } = useVideoConfig();
  return (
    <Sequence name={name} from={Math.round(at * fps)} durationInFrames={Math.round(seconds * fps)} layout="none">
      <Audio src={staticFile(`assets/v2/${file}`)} volume={volume} />
    </Sequence>
  );
};

const SoundTrack = () => {
  const { fps } = useVideoConfig();
  return (
    <>
      <Sequence name="Narration (unchanged)" layout="none">
        {/* File untouched; -1.9 dB gain because narration.wav already peaks at 0 dBFS. */}
        <Audio src={staticFile('assets/narration.wav')} volume={0.8} />
      </Sequence>
      <Sequence name="Original ambient bed (ducked)" layout="none">
        <Audio src={staticFile('assets/v2/bed_v2.wav')} volume={(f) => bedVolume(f, fps)} />
      </Sequence>
      <Sfx name="SFX whoosh · ship" file="sfx_whoosh.wav" at={0.1} seconds={1} volume={0.22} />
      <Sfx name="SFX page · Red Book" file="sfx_page.wav" at={9.75} seconds={0.6} volume={0.3} />
      <Sfx name="SFX whoosh · map card" file="sfx_whoosh.wav" at={13.8} seconds={1} volume={0.18} />
      <Sfx name="SFX impact · Pourquoi" file="sfx_impact.wav" at={16.2} seconds={1.4} volume={0.22} />
      <Sfx name="SFX whoosh · map" file="sfx_whoosh.wav" at={19.2} seconds={1} volume={0.2} />
      <Sfx name="SFX whoosh · split" file="sfx_whoosh.wav" at={24.48} seconds={1} volume={0.2} />
      <Sfx name="SFX page · close" file="sfx_page.wav" at={27.0} seconds={0.6} volume={0.26} />
      <Sfx name="SFX sea · Aman" file="sfx_sea.wav" at={28.92} seconds={6.4} volume={0.22} />
      <Sfx name="SFX sea · horizon" file="sfx_sea.wav" at={38.56} seconds={6.4} volume={0.2} />
      <Sfx name="SFX whoosh · map zoom" file="sfx_whoosh.wav" at={42.52} seconds={1} volume={0.18} />
      <Sfx name="SFX page · open" file="sfx_page.wav" at={45.14} seconds={0.6} volume={0.26} />
      <Sfx name="SFX sea · closing" file="sfx_sea.wav" at={53.6} seconds={6.4} volume={0.3} />
    </>
  );
};

// ---------------------------------------------------------------------------
// Composition: 18 beats anchored to phrase starts in out/lotr-pilot-v2-fr.srt
// ---------------------------------------------------------------------------
const BEAT_STARTS = [0, 2.24, 5.3, 9.6, 12.18, 16.0, 19.2, 21.78, 24.48, 26.8, 28.92, 32.68, 35.2, 38.56, 42.52, 45.14, 47.86, 51.98];
const VIDEO_END = 60;
const beatFrom = (i, fps) => Math.round(BEAT_STARTS[i] * fps);
const beatDuration = (i, fps) => Math.round((BEAT_STARTS[i + 1] ?? VIDEO_END) * fps) - beatFrom(i, fps);

export const PilotV2 = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: PAPER, fontFamily: BODY }}>
      <Sequence name="01 Frodon part" from={beatFrom(0, fps)} durationInFrames={beatDuration(0, fps)}><Beat01 /></Sequence>
      <Sequence name="02 Sam rentre" from={beatFrom(1, fps)} durationInFrames={beatDuration(1, fps)}><Beat02 /></Sequence>
      <Sequence name="03 Fan art · Rosie, enfants, livre" from={beatFrom(2, fps)} durationInFrames={beatDuration(2, fps)}><Beat03 /></Sequence>
      <Sequence name="04 Des années plus tard" from={beatFrom(3, fps)} durationInFrames={beatDuration(3, fps)}><Beat04 /></Sequence>
      <Sequence name="05 Elanor → Havres Gris" from={beatFrom(4, fps)} durationInFrames={beatDuration(4, fps)}><Beat05 /></Sequence>
      <Sequence name="06 Pourquoi ?" from={beatFrom(5, fps)} durationInFrames={beatDuration(5, fps)}><Beat06 /></Sequence>
      <Sequence name="07 Le dernier Porteur" from={beatFrom(6, fps)} durationInFrames={beatDuration(6, fps)}><Beat07 /></Sequence>
      <Sequence name="08 Sam aussi a porté l’Anneau" from={beatFrom(7, fps)} durationInFrames={beatDuration(7, fps)}><Beat08 /></Sequence>
      <Sequence name="09 Départ en écho" from={beatFrom(8, fps)} durationInFrames={beatDuration(8, fps)}><Beat09 /></Sequence>
      <Sequence name="10 Pas de retrouvailles racontées" from={beatFrom(9, fps)} durationInFrames={beatDuration(9, fps)}><Beat10 /></Sequence>
      <Sequence name="11 Aman ≠ immortalité" from={beatFrom(10, fps)} durationInFrames={beatDuration(10, fps)}><Beat11 /></Sequence>
      <Sequence name="12 Séjour limité" from={beatFrom(11, fps)} durationInFrames={beatDuration(11, fps)}><Beat12 /></Sequence>
      <Sequence name="13 Pas pour toujours" from={beatFrom(12, fps)} durationInFrames={beatDuration(12, fps)}><Beat13 /></Sequence>
      <Sequence name="14 Paix · guérison" from={beatFrom(13, fps)} durationInFrames={beatDuration(13, fps)}><Beat14 /></Sequence>
      <Sequence name="15 Sam a-t-il revu Frodon ?" from={beatFrom(14, fps)} durationInFrames={beatDuration(14, fps)}><Beat15 /></Sequence>
      <Sequence name="16 Question ouverte" from={beatFrom(15, fps)} durationInFrames={beatDuration(15, fps)}><Beat16 /></Sequence>
      <Sequence name="17 La route de l’Ouest" from={beatFrom(16, fps)} durationInFrames={beatDuration(16, fps)}><Beat17 /></Sequence>
      <Sequence name="18 Question finale" from={beatFrom(17, fps)} durationInFrames={beatDuration(17, fps)}><Beat18 duration={beatDuration(17, fps)} /></Sequence>
      <Grain />
      <Sequence name="Captions (word-level)" durationInFrames={Math.round(55.6 * fps)}><Captions /></Sequence>
      <SoundTrack />
    </AbsoluteFill>
  );
};
