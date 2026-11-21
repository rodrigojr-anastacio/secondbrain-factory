import React from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame, interpolate, Easing, continueRender, delayRender, random } from 'remotion';
import TL from './timeline.json';

// Clearance Required · AMOSTRA fase 1 (21/11/2026): abertura do vídeo "relógio de 67 h" de Chernobyl.
// Componentes P1 do REFERENCIAS-MOTION: ContadorDuplo, ReguaRelogio, LegendaArquivo, ColagemDossie/FotoPolaroid/FitaAdesiva,
// TextoDatilografado, MapaZoom (push-in no satélite), TransicaoGlitchSinal, Mapa2D com pluma, Teletipo (TASS) e Carimbo.

const DISPLAY = 'Anton', MONO = 'IBM Plex Mono', COND = 'Barlow Condensed';
const AMARELO = '#FDD505', CIANO = '#2BCEE2', FERRUGEM = '#C8561E', TINTA = '#111418', PAPEL = '#EDE6D6';
const FPS = TL.fps; const T = TL.T;

const FONTES = [
  ['Anton', 'Anton-Regular.ttf', '400'], ['IBM Plex Mono', 'IBMPlexMono-Medium.ttf', '400'], ['IBM Plex Mono', 'IBMPlexMono-Bold.ttf', '700'],
  ['Barlow Condensed', 'BarlowCondensed-SemiBold.ttf', '600'], ['Barlow Condensed', 'BarlowCondensed-Bold.ttf', '700'],
];
if (typeof document !== 'undefined' && !window.__fontesCh) {
  window.__fontesCh = true;
  const h = delayRender('fontes');
  Promise.all(FONTES.map(([fam, arq, peso]) => new FontFace(fam, `url('${staticFile('fonts/' + arq)}') format('truetype')`, { weight: peso })
    .load().then((ok) => document.fonts.add(ok)))).then(() => continueRender(h)).catch((e) => { console.error(e); continueRender(h); });
}

const cl = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const io = Easing.inOut(Easing.cubic);
const lin = (t, a, b, v0 = 0, v1 = 1, ease) => interpolate(t, [a, b], [v0, v1], { ...cl, easing: ease });

// ---------------- relógio ----------------
const E_TOTAL = 67 * 3600 + 36 * 60 + 20; // 26/04 01:23:40 → 28/04 21:00:00
const KF_RELOGIO = [[19.0, 0], [24.8, 12 * 3600], [29.0, 36 * 3600], [32.0, 37.5 * 3600], [35.0, 56 * 3600], [36.0, E_TOTAL]];
function decorrido(t) {
  if (t <= KF_RELOGIO[0][0]) return 0;
  for (let i = 1; i < KF_RELOGIO.length; i++) {
    const [t0, v0] = KF_RELOGIO[i - 1], [t1, v1] = KF_RELOGIO[i];
    if (t <= t1) return interpolate(t, [t0, t1], [v0, v1], { easing: i === KF_RELOGIO.length - 1 ? Easing.out(Easing.cubic) : undefined });
  }
  return E_TOTAL;
}
const p2 = (n) => String(Math.floor(n)).padStart(2, '0');
const fmtDec = (s) => `${p2(s / 3600)}:${p2((s % 3600) / 60)}:${p2(s % 60)}`;
const DIAS = ['SAT 26 APR 1986', 'SUN 27 APR 1986', 'MON 28 APR 1986'];
function horaLocal(s) {
  const abs = 1 * 3600 + 23 * 60 + 40 + s; // segundos desde 26/04 00:00
  const d = Math.floor(abs / 86400), r = abs % 86400;
  return { dia: DIAS[Math.min(d, 2)], hora: `${p2(r / 3600)}:${p2((r % 3600) / 60)}:${p2(r % 60)}`, horasDesde0: abs / 3600 };
}

// ---------------- câmera do mural ----------------
const CAM = [
  [10.9, 1000, 700, 0.85], [12.4, 1000, 700, 1.0], [13.2, 692, 478, 2.3], [14.6, 692, 478, 2.4], [15.6, 1150, 650, 1.0], [18.6, 1250, 650, 1.08],
  [19.6, 2550, 760, 0.95], [24.6, 2450, 600, 1.7], [25.6, 1000, 1750, 1.15], [31.8, 1050, 1760, 1.3], [32.8, 2650, 1800, 1.0], [35.6, 2650, 1750, 1.12],
  [36.6, 3480, 960, 1.1], [41.8, 3480, 975, 1.17], [44.0, 2000, 1200, 0.45], [46.5, 2000, 1200, 0.44],
];
function camera(t) {
  if (t <= CAM[0][0]) return CAM[0].slice(1);
  for (let i = 1; i < CAM.length; i++) {
    if (t <= CAM[i][0]) {
      const a = CAM[i - 1], b = CAM[i]; const u = io((t - a[0]) / (b[0] - a[0]));
      // escala interpolada em log (zoom com velocidade constante)
      return [a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u, Math.exp(Math.log(a[3]) + (Math.log(b[3]) - Math.log(a[3])) * u)];
    }
  }
  return CAM[CAM.length - 1].slice(1);
}

// entrada de elemento: cai 40 px, gira até o ângulo final, com mola curta
function entrada(t, t0) {
  const u = lin(t, t0, t0 + 0.55, 0, 1, Easing.out(Easing.back(1.4)));
  return { opacity: lin(t, t0, t0 + 0.2), dy: (1 - u) * -60, drot: (1 - u) * -6, s: 1 + (1 - u) * 0.06 };
}

const sombra = '0 14px 30px rgba(0,0,0,.55), 0 2px 6px rgba(0,0,0,.4)';

function Fita({ x, y, rot = -8, w = 150 }) {
  return <div style={{ position: 'absolute', left: x - w / 2, top: y - 20, width: w, height: 40, transform: `rotate(${rot}deg)`,
    background: 'rgba(237,230,214,.78)', boxShadow: '0 1px 3px rgba(0,0,0,.3)',
    clipPath: 'polygon(0 8%,4% 0,9% 10%,14% 0,20% 8%,26% 0,32% 9%,38% 0,44% 8%,50% 0,56% 9%,62% 0,68% 8%,74% 0,80% 9%,86% 0,92% 8%,100% 0,100% 92%,95% 100%,90% 91%,84% 100%,78% 92%,72% 100%,66% 91%,60% 100%,54% 92%,48% 100%,42% 91%,36% 100%,30% 92%,24% 100%,18% 91%,12% 100%,6% 92%,0 100%)' }} />;
}

function Item({ t, t0, x, y, w, rot = 0, children, z = 1 }) {
  const e = entrada(t, t0);
  if (t < t0) return null;
  return <div style={{ position: 'absolute', left: x, top: y + e.dy, width: w, transform: `rotate(${rot + e.drot}deg) scale(${e.s})`,
    transformOrigin: '50% 0%', opacity: e.opacity, zIndex: z }}>{children}</div>;
}

function Polaroid({ src, w, h, legenda, sepia = 0.25, pos = 'center' }) {
  return <div style={{ background: '#E9E2D0', padding: '16px 16px 58px', boxShadow: sombra, position: 'relative' }}>
    <div style={{ width: w, height: h, overflow: 'hidden', background: '#000' }}>
      <Img src={staticFile(src)} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: pos, filter: `sepia(${sepia}) contrast(1.05)` }} />
    </div>
    <div style={{ position: 'absolute', left: 18, bottom: 14, fontFamily: MONO, fontWeight: 700, fontSize: 21, color: '#2a2622', letterSpacing: 0.5 }}>{legenda}</div>
  </div>;
}

// texto datilografado: revela letra a letra entre t0 e t1
function Datilo({ t, t0, t1, texto, cursor = true }) {
  const n = Math.floor(lin(t, t0, t1, 0, texto.length));
  const fim = n >= texto.length;
  return <span style={{ whiteSpace: 'pre-wrap' }}>{texto.slice(0, n)}{cursor && !fim && t >= t0 ? <span style={{ opacity: Math.floor(t * 4) % 2 ? 1 : 0.2 }}>▌</span> : null}</span>;
}

// ---------------- o mural (prancha 4000×2400) ----------------
function Mural({ t }) {
  const M = TL.mapa;
  const [fx, fy, s] = camera(t);
  const plumaU = lin(t, T.N5 + 0.2, T.N5 + 2.6, 0, 1, io);
  const [cx, cy] = M.chernobyl, [sx2, sy2] = M.forsmark;
  const mx = (cx + sx2) / 2 - 120, my = (cy + sy2) / 2 + 60;
  const plumaD = `M${cx},${cy} Q${mx},${my} ${sx2},${sy2}`;
  const grifoU = lin(t, 13.4, 14.3, 0, 1, Easing.out(Easing.cubic));
  const carimbo = lin(t, T.stamp, T.stamp + 0.18, 0, 1, Easing.out(Easing.cubic));
  const anel = (t0) => lin(t, t0, t0 + 0.9, 0, 1, Easing.out(Easing.cubic));
  return (
    <div style={{ position: 'absolute', left: 0, top: 0, width: 4000, height: 2400,
      transform: `translate(${960 - fx * s}px, ${540 - fy * s}px) scale(${s})`, transformOrigin: '0 0' }}>
      {/* fundo: papelão escuro, vinheta ferrugem, mira ciano, tira de filme */}
      <div style={{ position: 'absolute', inset: 0, background: `radial-gradient(ellipse at 8% 92%, rgba(200,86,30,.28), transparent 45%), radial-gradient(ellipse at 50% 45%, #1d2127, ${TINTA} 80%)` }} />
      <svg width={4000} height={2400} style={{ position: 'absolute', inset: 0, opacity: 0.5 }}>
        <filter id="grao"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3" /><feColorMatrix values="0 0 0 0 0.6  0 0 0 0 0.55  0 0 0 0 0.5  0 0 0 0.35 0" /></filter>
        <rect width="4000" height="2400" filter="url(#grao)" />
        {[600, 1200, 1800].map((y) => <line key={y} x1="0" x2="4000" y1={y} y2={y} stroke={CIANO} strokeOpacity="0.12" strokeWidth="2" />)}
        {[1000, 2000, 3000].map((x) => <line key={x} y1="0" y2="2400" x1={x} x2={x} stroke={CIANO} strokeOpacity="0.12" strokeWidth="2" />)}
      </svg>
      <div style={{ position: 'absolute', left: -200, top: 1260, width: 4600, height: 120, background: '#0a0b0d', transform: 'rotate(-9deg)', opacity: 0.85,
        backgroundImage: 'repeating-linear-gradient(90deg, transparent 0 22px, #3a3a36 22px 40px)', backgroundSize: '100% 18px', backgroundRepeat: 'repeat-x',
        boxShadow: 'inset 0 18px 0 #0a0b0d, inset 0 -18px 0 #0a0b0d' }} />

      {/* A: INSAG-7, Tabela I-I (DREG), com a linha 01:23:40 grifada */}
      <Item t={t} t0={T.board} x={320} y={161} w={760} rot={-1.5} z={2}>
        <div style={{ position: 'relative', boxShadow: sombra }}>
          <Img src={staticFile('img/insag7-p65.jpg')} style={{ width: 760, display: 'block', filter: 'sepia(.18) contrast(1.08)' }} />
          <div style={{ position: 'absolute', left: '19.5%', top: '27.6%', height: '3.6%', width: `${59 * grifoU}%`, background: 'rgba(255,225,77,.55)', mixBlendMode: 'multiply' }} />
        </div>
        <Fita x={380} y={4} rot={-3} w={190} />
      </Item>

      {/* sala de controle do bloco 4 hoje (CC0, 2025) */}
      <Item t={t} t0={15.2} x={1180} y={420} w={672} rot={4} z={3}>
        <Polaroid src="img/controlroom-painel.jpg" w={640} h={300} legenda="CONTROL ROOM, UNIT 4 · TODAY" />
        <Fita x={336} y={2} rot={6} />
      </Item>

      {/* B: satélite KH-9 de 1984, push-in até a usina e Pripyat */}
      <Item t={t} t0={T.N3} x={1800} y={190} w={1500} rot={0.6} z={1}>
        <div style={{ position: 'relative', width: 1500, height: 1144, boxShadow: sombra, border: `10px solid #d8d1bf` }}>
          <Img src={staticFile('img/kh9-s.jpg')} style={{ width: '100%', height: '100%', objectFit: 'cover', filter: 'contrast(1.1) brightness(1.02)' }} />
          <svg width={1480} height={1124} style={{ position: 'absolute', left: 0, top: 0 }}>
            {[[0.522, 0.4, 62, 20.6], [0.33, 0.27, 110, 22.4]].map(([px, py, r, t0], i) => {
              const u = anel(t0); const L = 2 * Math.PI * r;
              return <circle key={i} cx={px * 1480} cy={py * 1124} r={r} fill="none" stroke={i ? CIANO : AMARELO} strokeWidth={7}
                strokeDasharray={L} strokeDashoffset={L * (1 - u)} transform={`rotate(-90 ${px * 1480} ${py * 1124})`} />;
            })}
          </svg>
          {t > 21.0 && <div style={{ position: 'absolute', left: 0.522 * 1480 + 70, top: 0.4 * 1124 + 30, opacity: lin(t, 21.0, 21.4), fontFamily: COND, fontWeight: 700, fontSize: 34,
            color: TINTA, background: AMARELO, padding: '2px 12px' }}>CHERNOBYL NPP · UNIT 4</div>}
          {t > 22.8 && <div style={{ position: 'absolute', left: 0.33 * 1480 - 240, top: 0.27 * 1124 - 160, opacity: lin(t, 22.8, 23.2), fontFamily: COND, fontWeight: 700, fontSize: 34,
            color: TINTA, background: CIANO, padding: '2px 12px' }}>PRIPYAT · ~49,000 PEOPLE</div>}
          <div style={{ position: 'absolute', left: 18, bottom: 18, fontFamily: MONO, fontWeight: 700, fontSize: 24, color: PAPEL, background: 'rgba(17,20,24,.85)',
            borderLeft: `6px solid ${AMARELO}`, padding: '6px 14px' }}>29 JAN 1984 · U.S. SPY SATELLITE (KH-9)</div>
        </div>
      </Item>

      {/* C: cartão datilografado com o texto do anúncio + carimbo TEMPORARY */}
      <Item t={t} t0={T.N4} x={560} y={1480} w={900} rot={-2} z={4}>
        <div style={{ position: 'relative', width: 900, height: 540, background: PAPEL, boxShadow: sombra, padding: '44px 54px', boxSizing: 'border-box',
          backgroundImage: 'repeating-linear-gradient(0deg, transparent 0 41px, rgba(43,206,226,.25) 41px 43px)' }}>
          <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 30, color: FERRUGEM, letterSpacing: 2 }}>27.04.1986 · PRIPYAT CITY RADIO</div>
          <div style={{ fontFamily: MONO, fontSize: 31, lineHeight: '43px', color: '#1d1b18', marginTop: 18 }}>
            <Datilo t={t} t0={T.N4 + 0.25} t1={T.N4 + 2.6} texto={'BUSES TO EVERY BUILDING\nFROM 14:00.\nTAKE DOCUMENTS, ESSENTIALS\nAND FOOD "FOR THE FIRST WHILE".'} />
          </div>
          <div style={{ position: 'absolute', right: 22, bottom: 16, fontFamily: COND, fontWeight: 700, fontSize: 22, color: '#5a554c', letterSpacing: 2 }}>QUOTED · CITY COUNCIL ANNOUNCEMENT</div>
          {t >= T.stamp && <div style={{ position: 'absolute', left: 330, top: 300, transform: `rotate(-12deg) scale(${2.2 - 1.2 * carimbo})`, opacity: 0.85 * carimbo,
            border: `7px solid ${FERRUGEM}`, color: FERRUGEM, fontFamily: DISPLAY, fontSize: 92, padding: '0 26px', letterSpacing: 6, mixBlendMode: 'multiply' }}>TEMPORARY</div>}
        </div>
        <Fita x={450} y={2} rot={2} w={170} />
      </Item>

      {/* D: mapa 2D da Europa com a pluma até Forsmark */}
      <Item t={t} t0={T.N5} x={2100} y={1330} w={950} rot={-1} z={2}>
        <div style={{ position: 'relative', width: 950, height: 1003, background: '#0E2A3B', boxShadow: sombra, border: '10px solid #d8d1bf', overflow: 'hidden' }}>
          <svg viewBox={`0 0 ${M.w} ${M.h}`} width={950} height={1003} style={{ position: 'absolute', left: 0, top: 0 }}>
            {M.paths.map((p, i) => <path key={i} d={p.d} fill={p.pais === 'Sweden' ? '#3f7480' : '#454c56'} stroke="#6a727c" strokeWidth={1.5} />)}
            <path d={plumaD} fill="none" stroke={AMARELO} strokeWidth={10} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - plumaU} opacity={0.95} />
            <circle cx={cx} cy={cy} r={14} fill={FERRUGEM} stroke={PAPEL} strokeWidth={4} />
            {plumaU > 0.97 && <circle cx={sx2} cy={sy2} r={14 + 10 * Math.abs(Math.sin(t * 4))} fill="none" stroke={CIANO} strokeWidth={5} />}
            <circle cx={sx2} cy={sy2} r={10} fill={CIANO} opacity={plumaU > 0.97 ? 1 : 0.3} />
          </svg>
          <div style={{ position: 'absolute', left: cx * 950 / M.w - 40, top: cy * 1003 / M.h + 22, fontFamily: COND, fontWeight: 700, fontSize: 32, color: PAPEL }}>CHERNOBYL</div>
          <div style={{ position: 'absolute', left: sx2 * 950 / M.w - 250, top: sy2 * 1003 / M.h - 70, opacity: lin(t, T.N5 + 2.4, T.N5 + 2.8), fontFamily: COND, fontWeight: 700, fontSize: 32,
            color: TINTA, background: CIANO, padding: '2px 10px' }}>FORSMARK, SWEDEN · 28 APR</div>
          <div style={{ position: 'absolute', right: 12, bottom: 10, fontFamily: COND, fontWeight: 700, fontSize: 20, color: '#9aa3ad', letterSpacing: 2 }}>SCHEMATIC · PATH APPROXIMATE</div>
        </div>
      </Item>
      <Item t={t} t0={33.6} x={3080} y={1820} w={612} rot={5} z={3}>
        <Polaroid src="img/anefo6456-s.jpg" w={580} h={385} legenda="NETHERLANDS · 1 MAY 1986" sepia={0.35} />
        <Fita x={306} y={2} rot={-5} />
      </Item>

      {/* E: teletipo TASS (texto literal; a voz é reconstrução) */}
      <Item t={t} t0={T.tass} x={3130} y={640} w={800} rot={1.5} z={5}>
        <div style={{ width: 800, height: 700, background: '#F1ECDD', boxShadow: sombra, padding: '40px 46px', boxSizing: 'border-box', position: 'relative',
          backgroundImage: 'radial-gradient(circle at 18px 50%, #c9c2b0 7px, transparent 8px), radial-gradient(circle at calc(100% - 18px) 50%, #c9c2b0 7px, transparent 8px)', backgroundSize: '100% 44px' }}>
          <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 30, color: FERRUGEM }}>ТАСС · 28.04.1986 · 21:00 МСК</div>
          <div style={{ fontFamily: MONO, fontSize: 31, lineHeight: '46px', color: '#1d1b18', marginTop: 22 }}>
            <Datilo t={t} t0={T.tass + 0.2} t1={T.tass + 5.4} texto={'НА ЧЕРНОБЫЛЬСКОЙ АТОМНОЙ\nЭЛЕКТРОСТАНЦИИ ПРОИЗОШЛА\nАВАРИЯ. ПОВРЕЖДЁН ОДИН ИЗ\nАТОМНЫХ РЕАКТОРОВ.\nПРИНИМАЮТСЯ МЕРЫ ПО\nЛИКВИДАЦИИ ПОСЛЕДСТВИЙ\nАВАРИИ...'} />
          </div>
          <div style={{ position: 'absolute', left: 46, bottom: 26, fontFamily: COND, fontWeight: 700, fontSize: 22, color: '#5a554c', letterSpacing: 2 }}>TASS BULLETIN · TEXT AS PRINTED IN PRAVDA, 29 APRIL 1986</div>
        </div>
        <Fita x={400} y={2} rot={-2} w={170} />
      </Item>
    </div>
  );
}

// ---------------- HUD ----------------
function Regua({ t }) {
  const op = lin(t, T.board, T.board + 0.6);
  if (op <= 0) return null;
  const h = horaLocal(decorrido(t)).horasDesde0;
  const X0 = 150, X1 = 1770; const x = (hh) => X0 + (X1 - X0) * hh / 72;
  const EV = [[1 + 23 / 60, 'AZ-5'], [38, 'BUSES'], [57, 'FORSMARK'], [69, 'TASS']];
  return <div style={{ position: 'absolute', left: 0, top: 0, width: 1920, height: 78, background: 'rgba(10,12,14,.82)', opacity: op, borderBottom: `2px solid rgba(43,206,226,.35)` }}>
    <svg width={1920} height={78} style={{ position: 'absolute' }}>
      <line x1={X0} x2={X1} y1={48} y2={48} stroke="#5d646d" strokeWidth={3} />
      <line x1={x(1.39)} x2={x(Math.max(1.39, h))} y1={48} y2={48} stroke={AMARELO} strokeWidth={6} />
      {Array.from({ length: 25 }, (_, i) => i * 3).map((hh) => <line key={hh} x1={x(hh)} x2={x(hh)} y1={hh % 24 ? 42 : 30} y2={54} stroke={hh % 24 ? '#7a828c' : PAPEL} strokeWidth={hh % 24 ? 2 : 3} />)}
      {EV.map(([hh, n]) => <circle key={n} cx={x(hh)} cy={48} r={8} fill={h >= hh ? AMARELO : TINTA} stroke={h >= hh ? AMARELO : '#7a828c'} strokeWidth={3} />)}
      <polygon points={`${x(h) - 9},14 ${x(h) + 9},14 ${x(h)},28`} fill={AMARELO} />
    </svg>
    {['SAT 26 APR', 'SUN 27 APR', 'MON 28 APR'].map((d, i) => <div key={d} style={{ position: 'absolute', left: x(i * 24) + 8, top: 6, fontFamily: COND, fontWeight: 700, fontSize: 22, color: PAPEL, letterSpacing: 2 }}>{d}</div>)}
    {EV.map(([hh, n]) => <div key={n} style={{ position: 'absolute', left: x(hh) - 60, width: 120, textAlign: 'center', top: 54, fontFamily: MONO, fontWeight: 700, fontSize: 17,
      color: h >= hh ? AMARELO : '#7a828c' }}>{n}</div>)}
  </div>;
}

function Contador({ t }) {
  const op = lin(t, T.board, T.board + 0.6);
  if (op <= 0) return null;
  const s = decorrido(t); const hl = horaLocal(s);
  const final = lin(t, 43.4, 44.4, 0, 1, io);   // no fim o contador cresce para o centro
  const left = 1418 + (560 - 1418) * final, top = 100 + (330 - 100) * final, sc = 1 + 1.25 * final;
  const corre = t > T.run[0] && t < T.run[1];
  return <div style={{ position: 'absolute', left, top, transform: `scale(${sc})`, transformOrigin: '0 0', opacity: op, width: 470,
    background: 'rgba(10,12,14,.88)', border: `2px solid ${corre ? AMARELO : '#3b4148'}`, padding: '12px 20px 14px', boxSizing: 'border-box' }}>
    <div style={{ fontFamily: COND, fontWeight: 700, fontSize: 20, letterSpacing: 3, color: '#9aa3ad' }}>TIME SINCE THE SHUTDOWN BUTTON</div>
    <div style={{ fontFamily: DISPLAY, fontSize: 76, lineHeight: '84px', color: AMARELO, letterSpacing: 2, fontVariantNumeric: 'tabular-nums' }}>{fmtDec(s)}</div>
    <div style={{ height: 2, background: '#3b4148', margin: '6px 0 8px' }} />
    <div style={{ fontFamily: COND, fontWeight: 700, fontSize: 20, letterSpacing: 3, color: '#9aa3ad' }}>LOCAL TIME · CHERNOBYL</div>
    <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 27, color: PAPEL }}>{hl.dia} · {hl.hora}</div>
  </div>;
}

const CREDITOS = [
  [0.0, 9.6, ['Audio: fire-service dispatch calls, 26 Apr 1986 · via pripyat.com / Wikimedia Commons']],
  [10.9, 15.2, ['Document: IAEA, INSAG-7 (1992), Table I-I · Source: IAEA']],
  [15.2, 18.8, ['Document: IAEA, INSAG-7 (1992), Table I-I · Source: IAEA', 'Photo: Bibric02 / Wikimedia Commons (CC0), 2025']],
  [18.8, 25.0, ['Satellite: KH-9 Hexagon, 29 Jan 1984 · U.S. Geological Survey (declassified)']],
  [25.0, 29.0, ['Text: Pripyat city radio announcement, 27 Apr 1986']],
  [29.0, 32.3, ['Audio: Pripyat city radio, 27 Apr 1986 · via pripyat.com / Wikimedia Commons']],
  [32.3, 36.0, ['Map: Natural Earth · Photo: Rob Croes / Anefo, Nationaal Archief (CC0)']],
  [36.0, 42.0, ['Synthetic voice reading the TASS text of 28 Apr 1986 · not the original broadcast']],
];
function Creditos({ t }) {
  const c = CREDITOS.find(([a, b]) => t >= a && t < b);
  if (!c) return null;
  const op = Math.min(lin(t, c[0], c[0] + 0.3), lin(t, c[1] - 0.3, c[1], 1, 0));
  return <div style={{ position: 'absolute', left: 36, bottom: 30, opacity: op * 0.92 }}>
    {c[2].map((l) => <div key={l} style={{ fontFamily: MONO, fontSize: 20, color: PAPEL, background: 'rgba(10,12,14,.7)', padding: '3px 10px', marginTop: 4, display: 'table' }}>{l}</div>)}
  </div>;
}

const LEG = [
  // [t0, t1, original, inglês]
  [1.14, 7.0, '«Взрыв на главном корпусе, 3–4 блок.»', 'Explosion at the main building, units 3 and 4.'],
  [7.08, 8.3, '«А там люди есть?»', 'Are there people there?'],
  [8.38, 8.95, '«Да.»', 'Yes.'],
  [29.0, 32.0, '«…провести временную эвакуацию…»', '"…to carry out a TEMPORARY evacuation…"'],
  [36.0, 39.2, '', 'An accident has occurred at the Chernobyl nuclear power station.'],
  [39.45, 41.9, '', 'One of the atomic reactors has been damaged.'],
];
function Legendas({ t }) {
  const l = LEG.find(([a, b]) => t >= a && t < b);
  if (!l) return null;
  const op = Math.min(lin(t, l[0], l[0] + 0.12), lin(t, l[1] - 0.12, l[1], 1, 0));
  const ing = l[3].split(/(TEMPORARY)/);
  return <div style={{ position: 'absolute', left: 0, right: 0, bottom: 112, textAlign: 'center', opacity: op }}>
    {l[2] && <div style={{ fontFamily: MONO, fontSize: 26, color: '#b9b4a8', marginBottom: 8, textShadow: '0 2px 6px #000' }}>{l[2]}</div>}
    <div style={{ display: 'inline-block', fontFamily: COND, fontWeight: 700, fontSize: 50, color: '#fff', background: 'rgba(10,12,14,.72)', padding: '4px 22px', letterSpacing: 0.5 }}>
      {ing.map((p, i) => <span key={i} style={{ color: p === 'TEMPORARY' ? AMARELO : '#fff' }}>{p}</span>)}
    </div>
  </div>;
}

function Selo({ t }) {
  const S = [
    [0.4, 9.0, 'ARCHIVE AUDIO', 'FIRE-SERVICE DISPATCH CALLS · CHERNOBYL · NIGHT OF 26 APRIL 1986', CIANO],
    [28.8, 32.2, 'ARCHIVE AUDIO', 'PRIPYAT CITY RADIO · 27 APRIL 1986', CIANO],
    [35.8, 42.0, 'RECONSTRUCTION · SYNTHETIC AUDIO', 'TEXT: TASS, 28 APRIL 1986, 21:00 MOSCOW · READ IN ENGLISH', FERRUGEM],
  ].find(([a, b]) => t >= a && t < b);
  if (!S) return null;
  const op = Math.min(lin(t, S[0], S[0] + 0.25), lin(t, S[1] - 0.25, S[1], 1, 0));
  const top = t > T.board ? 100 : 44;
  return <div style={{ position: 'absolute', left: 36, top, opacity: op }}>
    <div style={{ display: 'inline-block', fontFamily: COND, fontWeight: 700, fontSize: 30, letterSpacing: 4, color: S[4] === CIANO ? TINTA : PAPEL, background: S[4], padding: '2px 14px' }}>
      <span style={{ display: 'inline-block', width: 14, height: 14, borderRadius: 7, background: S[4] === CIANO ? FERRUGEM : AMARELO, marginRight: 10, opacity: Math.floor(t * 2) % 2 ? 1 : 0.35 }} />{S[2]}</div>
    <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 21, color: PAPEL, marginTop: 6, background: 'rgba(10,12,14,.7)', padding: '3px 10px', display: 'table' }}>{S[3]}</div>
  </div>;
}

// forma de onda do áudio de época / reconstrução
function Onda({ t, chave, x, y, w, h, cor, op = 1 }) {
  const o = TL.ondas[chave]; const f0 = Math.floor((t - o.inicio) * FPS);
  if (f0 < 0 || f0 >= o.rms.length + 10) return null;
  const n = 72; const bw = w / n;
  return <svg width={w} height={h} style={{ position: 'absolute', left: x, top: y, opacity: op }}>
    {Array.from({ length: n }, (_, i) => {
      const k = f0 - (n - 1 - i); const v = k >= 0 && k < o.rms.length ? o.rms[k] : 0;
      const a = Math.max(3, v * h * 0.95);
      return <rect key={i} x={i * bw + 2} y={(h - a) / 2} width={bw - 4} height={a} fill={cor} opacity={0.35 + 0.65 * (i / n)} />;
    })}
  </svg>;
}

// abertura: tela escura, linha telefônica, onda e legenda
function Abertura({ t }) {
  const op = lin(t, T.board - 0.3, T.board + 0.4, 1, 0);
  if (op <= 0) return null;
  const datOp = Math.min(lin(t, T.typed - 0.05, T.typed + 0.1), lin(t, T.board - 0.2, T.board + 0.3, 1, 0));
  return <AbsoluteFill style={{ background: '#07080a', opacity: op }}>
    <svg width={1920} height={1080} style={{ position: 'absolute', opacity: 0.25 }}>
      <filter id="g2"><feTurbulence type="fractalNoise" baseFrequency="0.8" seed={Math.floor(t * 12)} /><feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.25 0" /></filter>
      <rect width="1920" height="1080" filter="url(#g2)" />
    </svg>
    {t < T.typed && <>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 300, textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: 6, color: '#7f8892' }}>
        LINE: CENTRAL FIRE DISPATCH → PLANT FIRE STATION, IVANKOV, POLESSKOYE</div>
      <Onda t={t} chave="disp" x={360} y={380} w={1200} h={240} cor={CIANO} />
    </>}
    {t >= T.typed && <div style={{ position: 'absolute', left: 0, right: 0, top: 440, textAlign: 'center', opacity: datOp }}>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 92, color: PAPEL, letterSpacing: 4 }}><Datilo t={t} t0={T.typed} t1={T.typed + 1.1} texto="26.04.1986 — 01:23:40" /></div>
    </div>}
  </AbsoluteFill>;
}

// glitch de sinal (faixas deslocadas + separação de cor + ruído)
function Glitch({ t, janela, children }) {
  const [a, b] = janela;
  if (t < a || t > b) return children;
  const f = Math.floor(t * FPS); const u = (t - a) / (b - a); const k = Math.sin(Math.PI * u);
  const faixas = 7;
  return <AbsoluteFill>
    {Array.from({ length: faixas }, (_, i) => {
      const dx = (random(`gx${f}-${i}`) - 0.5) * 160 * k;
      return <AbsoluteFill key={i} style={{ clipPath: `inset(${(i / faixas) * 100}% 0 ${100 - ((i + 1) / faixas) * 100}% 0)`, transform: `translateX(${dx}px)` }}>{children}</AbsoluteFill>;
    })}
    <AbsoluteFill style={{ mixBlendMode: 'screen', opacity: 0.55 * k, transform: `translateX(${14 * k}px)`, filter: 'sepia(1) hue-rotate(140deg) saturate(5)' }}>{children}</AbsoluteFill>
    <AbsoluteFill style={{ mixBlendMode: 'screen', opacity: 0.5 * k, transform: `translateX(${-14 * k}px)`, filter: 'sepia(1) hue-rotate(-25deg) saturate(6)' }}>{children}</AbsoluteFill>
    <svg width={1920} height={1080} style={{ position: 'absolute', opacity: 0.6 * k }}>
      <filter id="gn"><feTurbulence type="fractalNoise" baseFrequency="0.02 0.9" seed={f} /><feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.8 0" /></filter>
      <rect width="1920" height="1080" filter="url(#gn)" />
    </svg>
  </AbsoluteFill>;
}

export const Amostra = () => {
  const frame = useCurrentFrame(); const t = frame / FPS;
  const fimOp = lin(t, 44.0, 44.6, 0, 0.6);
  const preto = lin(t, 45.3, 46.0, 0, 1);
  const cena = <AbsoluteFill style={{ background: TINTA }}>
    {t >= T.board - 0.3 && <Mural t={t} />}
    <Abertura t={t} />
  </AbsoluteFill>;
  return <AbsoluteFill style={{ background: '#000' }}>
    <Glitch t={t} janela={t < 12 ? T.glitch1 : T.glitch2}>{cena}</Glitch>
    {t >= T.tass && t < 42.0 && <Onda t={t} chave="tass" x={1140} y={850} w={720} h={90} cor={FERRUGEM} op={0.9} />}
    {t >= 29.0 && t < 32.2 && <Onda t={t} chave="evac" x={1140} y={850} w={720} h={90} cor={CIANO} op={0.9} />}
    <AbsoluteFill style={{ background: '#000', opacity: fimOp }} />
    {t >= 43.6 && <div style={{ position: 'absolute', left: 0, right: 0, top: 830, textAlign: 'center', opacity: lin(t, 44.2, 44.7), fontFamily: COND, fontWeight: 700,
      fontSize: 44, letterSpacing: 6, color: PAPEL }}>FROM THE BUTTON TO THE BULLETIN</div>}
    <Regua t={t} />
    <Contador t={t} />
    <Selo t={t} />
    <Legendas t={t} />
    <Creditos t={t} />
    <AbsoluteFill style={{ background: '#000', opacity: preto }} />
  </AbsoluteFill>;
};
