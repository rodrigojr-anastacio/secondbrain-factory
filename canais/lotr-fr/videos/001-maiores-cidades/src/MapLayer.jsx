import React from 'react';
import { interpolate, random, useCurrentFrame, Easing } from 'remotion';

// Original schematic map of Arda (not to scale). World space 2400×1500, west on the left.
// Screen = (world − camera.c) · camera.z + (960, 500).
export const INK = '#2f2416';
const GOLD = '#b8862b';
const SEA_FILL = '#b7c2ae';
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const EASE = Easing.bezier(0.45, 0, 0.2, 1);

export const CITIES = {
  brithombar: { p: [650, 500], name: 'Brithombar', side: 'r' },
  eglarest: { p: [668, 640], name: 'Eglarest', side: 'r' },
  nargothrond: { p: [790, 560], name: 'Nargothrond', side: 'r' },
  gondolin: { p: [870, 320], name: 'Gondolin', side: 'r' },
  menegroth: { p: [1030, 470], name: 'Menegroth', side: 'r' },
  belegost: { p: [1185, 330], name: 'Belegost', side: 'r' },
  nogrod: { p: [1180, 470], name: 'Nogrod', side: 'r' },
  khazad: { p: [1630, 620], name: 'Khazad-dûm', side: 'r' },
  eregion: { p: [1530, 690], name: 'Eregion', side: 'l' },
  annuminas: { p: [1330, 420], name: 'Annúminas (Arnor)', side: 'r' },
  lindon: { p: [1250, 470], name: 'Lindon', side: 'r' },
  minas_tirith: { p: [1830, 1040], name: 'Minas Tirith', side: 'l' },
  osgiliath: { p: [1885, 1040], name: 'Osgiliath', side: 'r' },
  pelargir: { p: [1862, 1160], name: 'Pelargir', side: 'r' },
  umbar: { p: [1650, 1400], name: 'Umbar', side: 'r' },
  armenelos: { p: [380, 1200], name: 'Armenelos', side: 'r' },
};

export const VIEWS = {
  all: { c: [1500, 800], z: 0.58 },
  beleriand: { c: [880, 500], z: 1.35 },
  beleriand_wide: { c: [1000, 560], z: 1.0 },
  ered_luin: { c: [1000, 470], z: 1.5 },
  eriador: { c: [1450, 520], z: 1.3 },
  south: { c: [1650, 1160], z: 1.1 },
  gondor: { c: [1820, 1080], z: 2.0 },
  numenor: { c: [620, 1180], z: 1.1 },
  arda: { c: [1050, 1000], z: 0.62 },
};

// Coastline (sea to the west/south). PRE = before the War of Wrath; POST = Beleriand drowned, Gulf of Lhûn.
const SOUTH = [[1000, 870], [1080, 1000], [1200, 1100], [1350, 1180], [1500, 1200], [1650, 1185], [1760, 1260], [1800, 1250], [1730, 1330], [1660, 1395], [1700, 1500]];
const PRE = [[600, 0], [585, 160], [615, 300], [600, 420], [612, 520], [600, 620], [640, 760], [760, 820], [900, 800], ...SOUTH];
const POST = [[1110, 0], [1095, 160], [1125, 300], [1140, 400], [1250, 470], [1130, 530], [1110, 680], [1090, 800], [1010, 830], ...SOUTH];
const lerpPts = (a, b, t) => a.map((p, i) => [p[0] + (b[i][0] - p[0]) * t, p[1] + (b[i][1] - p[1]) * t]);
const smooth = (pts) => {
  // Catmull-Rom → cubic Bézier
  let d = `M${pts[0][0]} ${pts[0][1]}`;
  for (let i = 0; i < pts.length - 1; i++) {
    const p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C${c1[0]} ${c1[1]} ${c2[0]} ${c2[1]} ${p2[0]} ${p2[1]}`;
  }
  return d;
};

const RANGES = {
  ered_luin: [[1170, 110], [1182, 350], [1160, 600], [1172, 830]],
  misty: [[1640, 110], [1650, 400], [1632, 610], [1622, 820]],
  nimrais: [[1440, 1090], [1600, 1060], [1810, 1060]],
  ephel: [[1960, 940], [1970, 1100], [1955, 1270]],
  lithui: [[1960, 930], [2150, 915], [2350, 925]],
  thangorodrim: [[900, 60], [1000, 50], [1100, 70]],
};
const RIVERS = {
  sirion: [[950, 150], [955, 400], [925, 650], [880, 790]],
  narog: [[760, 330], [785, 560], [840, 770]],
  anduin: [[1760, 150], [1770, 420], [1790, 700], [1850, 900], [1885, 1040], [1866, 1160], [1800, 1250]],
};
const BELERIAND_RIVERS = ['sirion', 'narog'];

const along = (pts, step) => {
  const out = [];
  for (let i = 0; i < pts.length - 1; i++) {
    const [a, b] = [pts[i], pts[i + 1]];
    const len = Math.hypot(b[0] - a[0], b[1] - a[1]);
    for (let s = 0; s < len; s += step) out.push([a[0] + ((b[0] - a[0]) * s) / len, a[1] + ((b[1] - a[1]) * s) / len]);
  }
  return out;
};
const Mountains = ({ pts, size = 22, seed }) => (
  <g>
    {along(pts, size * 0.9).map(([x, y], i) => {
      const h = size * (0.8 + random(`${seed}${i}`) * 0.6);
      const dx = (random(`${seed}x${i}`) - 0.5) * size * 0.8;
      return (
        <path key={i} d={`M${x + dx - h * 0.6} ${y + h * 0.4} L${x + dx} ${y - h * 0.6} L${x + dx + h * 0.6} ${y + h * 0.4}`}
          fill="#e3d3ad" stroke={INK} strokeWidth={2.4} strokeLinejoin="round" />
      );
    })}
  </g>
);

const star = (cx, cy, r1, r2) => {
  const pts = [];
  for (let i = 0; i < 10; i++) {
    const a = -Math.PI / 2 + (i * Math.PI) / 5 + 0.25;
    const r = i % 2 ? r2 : r1;
    pts.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
  }
  return smooth([...pts, pts[0]]) + ' Z';
};

const Label = ({ x, y, text, size, italic, color = INK, anchor = 'middle', spacing = 2, weight = 600, font }) => (
  <text x={x} y={y} textAnchor={anchor} fontSize={size} fontStyle={italic ? 'italic' : 'normal'} fontWeight={weight}
    letterSpacing={spacing} fill={color} fontFamily={font}
    stroke="#efe3c6" strokeWidth={size * 0.22} paintOrder="stroke" strokeLinejoin="round">{text}</text>
);

export const MapLayer = ({ shot, fonts }) => {
  const f = useCurrentFrame();
  const D = shot.dur;
  const prog = interpolate(f, [0, D], [0, 1], clamp);
  const v = VIEWS[shot.view] || VIEWS.all;
  const v0 = shot.pan_from ? VIEWS[shot.pan_from] : v;
  const pt = shot.pan_from ? interpolate(f, [0, Math.min(D, 75)], [0, 1], { ...clamp, easing: EASE }) : 1;
  const cx = v0.c[0] + (v.c[0] - v0.c[0]) * pt, cy = v0.c[1] + (v.c[1] - v0.c[1]) * pt;
  const z = (v0.z + (v.z - v0.z) * pt) * (1 + 0.035 * prog);
  const toS = ([x, y]) => [(x - cx) * z + 960, (y - cy) * z + 500];

  const sinkT = shot.sink ? interpolate(f, [15, Math.max(30, D * 0.75)], [0, 1], { ...clamp, easing: EASE }) : shot.sunk ? 1 : 0;
  const coast = lerpPts(PRE, POST, sinkT);
  const seaD = smooth(coast) + ' L0 1500 L0 0 Z';
  const coastD = smooth(coast);

  const show = shot.show === 'all' ? Object.keys(CITIES).filter((k) => !['lindon', 'eregion', 'annuminas', 'armenelos'].includes(k)) : shot.show || [];
  const hl = shot.hl || [];
  const fade = shot.fade || [];
  const beleriandIds = ['brithombar', 'eglarest', 'nargothrond', 'gondolin', 'menegroth', 'belegost', 'nogrod'];
  const s = 1 / z; // keep strokes/labels constant on screen

  const numSink = shot.sink_numenor ? interpolate(f, [10, D * 0.7], [0, 1], { ...clamp, easing: EASE }) : 0;
  const showNumenor = shot.numenor && !shot.numenor_gone;

  const route = shot.route ? shot.route.map((k) => CITIES[k].p) : null;
  const routeT = interpolate(f, [10, D - 10], [0, 1], clamp);

  const fleetSrc = shot.fleet_from ? CITIES[shot.fleet_from === 'numenor_wreck' ? 'armenelos' : shot.fleet_from].p : null;
  const fleets = shot.fleet ? [[[80, CITIES[shot.fleet].p[1] - 40], CITIES[shot.fleet].p]] : fleetSrc ? shot.fleet_to.map((k) => [fleetSrc, CITIES[k].p]) : [];
  const fleetT = interpolate(f, [8, Math.min(D - 5, 90)], [0, 1], { ...clamp, easing: EASE });

  return (
    <svg width={1920} height={1080} viewBox="0 0 1920 1080" style={{ position: 'absolute', inset: 0 }}>
      <g transform={`translate(${960 - cx * z} ${500 - cy * z}) scale(${z})`}>
        {/* sea */}
        <path d={seaD} fill={SEA_FILL} />
        {[16, 34, 56].map((w, i) => (
          <path key={i} d={coastD} fill="none" stroke={INK} strokeOpacity={0.16 - i * 0.04} strokeWidth={w * s * 0.25} transform={`translate(${-w * 0.35 * s} 0)`} />
        ))}
        <path d={coastD} fill="none" stroke={INK} strokeWidth={3 * s} />
        {/* Númenor */}
        {showNumenor && (
          <g opacity={1 - numSink} transform={`translate(380 1200) scale(${1 - numSink * 0.55}) translate(-380 -1200)`}>
            <path d={star(380, 1200, 165, 80)} fill="#e6d7b2" stroke={INK} strokeWidth={3 * s} />
            <Mountains pts={[[372, 1150], [392, 1160]]} size={16} seed="men" />
          </g>
        )}
        {shot.numenor_gone && <path d={star(380, 1200, 165, 80)} fill="none" stroke={INK} strokeOpacity={0.35} strokeDasharray={`${10 * s} ${10 * s}`} strokeWidth={2.4 * s} />}
        {numSink > 0 && [0, 1, 2].map((i) => {
          const r = 60 + ((numSink * 260 + i * 80) % 260);
          return <circle key={i} cx={380} cy={1200} r={r} fill="none" stroke={INK} strokeOpacity={0.35 * (1 - r / 320)} strokeWidth={2.5 * s} />;
        })}
        {/* rivers */}
        {Object.entries(RIVERS).map(([k, pts]) => (
          <path key={k} d={smooth(pts)} fill="none" stroke="#5f7b86" strokeWidth={4 * s} strokeLinecap="round"
            opacity={BELERIAND_RIVERS.includes(k) ? 1 - sinkT : 1} />
        ))}
        {/* mountains */}
        <g opacity={1 - sinkT}><Mountains pts={RANGES.thangorodrim} size={26} seed="th" /></g>
        <Mountains pts={RANGES.ered_luin} size={22} seed="el" />
        <Mountains pts={RANGES.misty} size={24} seed="mm" />
        <Mountains pts={RANGES.nimrais} size={18} seed="en" />
        <Mountains pts={RANGES.ephel} size={20} seed="ep" />
        <Mountains pts={RANGES.lithui} size={20} seed="li" />
        {/* Echoriath ring around Gondolin */}
        <g opacity={1 - sinkT}>
          <Mountains pts={Array.from({ length: 19 }, (_, i) => [870 + Math.cos((i / 18) * Math.PI * 2) * 62, 320 + Math.sin((i / 18) * Math.PI * 2) * 52])} size={14} seed="ech" />
        </g>
        {/* region labels */}
        <g opacity={1 - sinkT}><Label x={820} y={700} text="BELERIAND" size={30 * s} italic spacing={10 * s} font={fonts.title} color="#5a4630" /></g>
        <Label x={1400} y={300} text="ERIADOR" size={30 * s} italic spacing={10 * s} font={fonts.title} color="#5a4630" />
        <Label x={1690} y={1110} text="GONDOR" size={26 * s} italic spacing={8 * s} font={fonts.title} color="#5a4630" />
        <Label x={2160} y={1080} text="MORDOR" size={26 * s} italic spacing={8 * s} font={fonts.title} color="#5a4630" />
        <Label x={sinkT > 0.5 ? 760 : 380} y={420} text="BELEGAER" size={28 * s} italic spacing={12 * s} font={fonts.title} color="#4d6466" />
        {showNumenor && <g opacity={1 - numSink}><Label x={380} y={1415} text="NÚMENOR" size={26 * s} italic spacing={8 * s} font={fonts.title} color="#5a4630" /></g>}
        {/* route of the crown */}
        {route && (() => {
          const d = smooth(route);
          return <path d={d} fill="none" stroke={GOLD} strokeWidth={5 * s} strokeDasharray={`${14 * s} ${10 * s}`} pathLength={1000}
            style={{ strokeDasharray: 1000, strokeDashoffset: 1000 * (1 - routeT) }} />;
        })()}
        {/* links (migration / move) */}
        {(shot.links || []).map(([a, b], i) => {
          const [p, q] = [CITIES[a].p, CITIES[b].p];
          const m = [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2 - Math.hypot(q[0] - p[0], q[1] - p[1]) * 0.25];
          const t = interpolate(f, [10 + i * 10, 70 + i * 10], [0, 1], { ...clamp, easing: EASE });
          return <path key={i} d={`M${p[0]} ${p[1]} Q${m[0]} ${m[1]} ${q[0]} ${q[1]}`} fill="none" stroke={GOLD} strokeWidth={4.5 * s}
            strokeLinecap="round" pathLength={1000} strokeDasharray={1000} strokeDashoffset={1000 * (1 - t)} />;
        })}
        {/* sea routes */}
        {fleets.map(([p, q], i) => {
          const m = [(p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 60];
          const t = interpolate(fleetT, [i * 0.12, 0.7 + i * 0.12], [0, 1], clamp);
          return (
            <g key={i}>
              <path d={`M${p[0]} ${p[1]} Q${m[0]} ${m[1]} ${q[0]} ${q[1]}`} fill="none" stroke="#2f4a55" strokeWidth={3.5 * s}
                strokeDasharray={`${4 * s} ${12 * s}`} strokeLinecap="round" pathLength={1000}
                style={{ clipPath: 'none' }} opacity={t > 0 ? 1 : 0} />
              <path d={`M${p[0]} ${p[1]} Q${m[0]} ${m[1]} ${q[0]} ${q[1]}`} fill="none" stroke={SEA_FILL} strokeWidth={8 * s}
                pathLength={1000} strokeDasharray={1000} strokeDashoffset={-1000 * t} />
            </g>
          );
        })}
        {/* cities */}
        {show.map((k) => {
          const c = CITIES[k];
          if (!c) return null;
          const isH = hl.includes(k), isF = fade.includes(k);
          const bi = beleriandIds.indexOf(k);
          let op = 1;
          if (shot.sink && bi >= 0) op = interpolate(f, [D * 0.25 + bi * 9, D * 0.25 + bi * 9 + 20], [1, 0], clamp);
          if (k === 'armenelos') op *= 1 - numSink;
          const appear = interpolate(f, [4, 16], [0, 1], clamp);
          const pulse = isH ? 1 + 0.18 * Math.sin(f / 7) : 1;
          const [x, y] = c.p;
          const r = (isH ? 13 : 8) * s;
          const lx = c.side === 'l' ? x - 22 * s : x + 22 * s;
          return (
            <g key={k} opacity={op * appear}>
              {isH && <circle cx={x} cy={y} r={r * 2.2 * pulse} fill="none" stroke={GOLD} strokeWidth={3 * s} />}
              <circle cx={x} cy={y} r={r} fill={isF ? '#8a7f6e' : isH ? GOLD : INK} stroke={INK} strokeWidth={2.5 * s} />
              {isF && <path d={`M${x - r} ${y - r} L${x + r} ${y + r} M${x + r} ${y - r} L${x - r} ${y + r}`} stroke="#5b1f14" strokeWidth={3 * s} />}
              <Label x={lx} y={y + (isH ? 12 : 9) * s} text={c.name} anchor={c.side === 'l' ? 'end' : 'start'}
                size={(isH ? 36 : 27) * s} font={fonts.title} spacing={1 * s} weight={isH ? 700 : 600} color={isF ? '#6f6250' : INK} />
            </g>
          );
        })}
      </g>
    </svg>
  );
};
