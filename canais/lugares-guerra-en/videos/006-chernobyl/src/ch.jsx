import React from 'react';
import { AbsoluteFill, Img, OffthreadVideo, staticFile, interpolate, useCurrentFrame, Easing, random } from 'remotion';
import { DISPLAY, MONO, COND, AMARELO, CIANO, FERRUGEM, TINTA, PAPEL, W, H } from './estilo.jsx';

// 006-chernobyl "o relógio de 67 h": componentes novos sobre a base do 005 (amostra aprovada 21/11/2026):
// Overlay (régua de horas + contador), Arquivo (áudio de época com legenda e onda), Contador, Datilo, Teletipo, TresRelogios, Mural, Glitch, MapaCh.
const cl = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const io = Easing.inOut(Easing.cubic);
const lin = (t, a, b, v0 = 0, v1 = 1, ease) => interpolate(t, [a, b], [v0, v1], { ...cl, easing: ease });
const p2 = (n) => String(Math.floor(n)).padStart(2, '0');
const BTN = 1 * 3600 + 23 * 60 + 40;
const DIAS = ['FRI 25 APR', 'SAT 26 APR', 'SUN 27 APR', 'MON 28 APR', 'TUE 29 APR'];
const sombra = '0 14px 30px rgba(0,0,0,.55), 0 2px 6px rgba(0,0,0,.4)';
const fundoEscuro = 'radial-gradient(ellipse at center, #2a2f36 0%, #0c0e11 78%)';

const hms = (s, seg = true) => `${p2(s / 3600)}:${p2((s % 3600) / 60)}${seg ? ':' + p2(s % 60) : ''}`;

// ───────── relógio persistente: régua 26–28/04 + contador (estado vem de q.rl, calculado no build.py) ─────────
function valorRelogio(q, f) {
  const r = q.rl; const loc = f - q.from_;
  if (!r.vis) return r.oc ? { v: r.v0, op: lin(loc, 0, 8, 1, 0) } : { v: null, op: 0 };
  const op = r.oc ? 1 : lin(loc, 0, 10);
  if (r.v0 != null && r.v0 !== r.v1) {
    const T = r.modo === 'corre' ? q.dur : Math.min(27, q.dur);
    return { v: r.v0 + (r.v1 - r.v0) * io(lin(loc, 0, T)), op };
  }
  return { v: r.v1, op };
}

const EV = [[1 + 23 / 60, 'AZ-5'], [20, 'ORDER'], [37.5, 'BUSES'], [57, 'FORSMARK'], [69, 'TASS']];
export const Overlay = ({ planos }) => {
  const f = useCurrentFrame();
  const q = planos.find((p) => f >= p.from_ && f < p.from_ + p.dur) || planos[planos.length - 1];
  const { v, op } = valorRelogio(q, f);
  if (v == null || op <= 0) return null;
  const h = Math.max(0, Math.min(72, v / 3600));
  const X0 = 150, X1 = 1770; const x = (hh) => X0 + (X1 - X0) * hh / 72;
  const ang = v < 0 ? 'BEFORE THE BUTTON' : 'SINCE THE SHUTDOWN BUTTON';
  const dec = Math.abs(v - BTN);
  const dIdx = Math.max(0, Math.min(4, Math.floor(v / 86400) + 1));
  const r = q.rl;
  return <>
    <div style={{ position: 'absolute', left: 0, top: 0, width: W, height: 78, background: 'rgba(10,12,14,.82)', opacity: op, borderBottom: '2px solid rgba(43,206,226,.35)' }}>
      <svg width={W} height={78} style={{ position: 'absolute' }}>
        <line x1={X0} x2={X1} y1={48} y2={48} stroke="#5d646d" strokeWidth={3} />
        <line x1={x(1.39)} x2={x(Math.max(1.39, h))} y1={48} y2={48} stroke={AMARELO} strokeWidth={6} />
        {Array.from({ length: 25 }, (_, i) => i * 3).map((hh) => <line key={hh} x1={x(hh)} x2={x(hh)} y1={hh % 24 ? 42 : 30} y2={54} stroke={hh % 24 ? '#7a828c' : PAPEL} strokeWidth={hh % 24 ? 2 : 3} />)}
        {EV.map(([hh, n]) => <circle key={n} cx={x(hh)} cy={48} r={8} fill={h >= hh ? AMARELO : TINTA} stroke={h >= hh ? AMARELO : '#7a828c'} strokeWidth={3} />)}
        <polygon points={`${x(h) - 9},14 ${x(h) + 9},14 ${x(h)},28`} fill={AMARELO} />
      </svg>
      {['SAT 26 APR', 'SUN 27 APR', 'MON 28 APR'].map((d, i) => <div key={d} style={{ position: 'absolute', left: x(i * 24) + 8, top: 6, fontFamily: COND, fontWeight: 700, fontSize: 22, color: PAPEL, letterSpacing: 2 }}>{d}</div>)}
      {EV.map(([hh, n]) => <div key={n} style={{ position: 'absolute', left: x(hh) - 60, width: 120, textAlign: 'center', top: 54, fontFamily: MONO, fontWeight: 700, fontSize: 17, color: h >= hh ? AMARELO : '#7a828c' }}>{n}</div>)}
    </div>
    {!r.sem_cont && <div style={{ position: 'absolute', left: 36, top: 96, width: 400, opacity: op, background: 'rgba(10,12,14,.88)', border: `2px solid ${r.modo === 'corre' ? AMARELO : '#3b4148'}`,
      padding: '8px 16px 10px', boxSizing: 'border-box' }}>
      <div style={{ fontFamily: COND, fontWeight: 700, fontSize: 17, letterSpacing: 3, color: '#9aa3ad' }}>{ang}</div>
      <div style={{ fontFamily: DISPLAY, fontSize: 52, lineHeight: '58px', color: AMARELO, letterSpacing: 2, fontVariantNumeric: 'tabular-nums' }}>{v < 0 ? '−' : '+'}{hms(dec)}</div>
      <div style={{ height: 2, background: '#3b4148', margin: '4px 0 6px' }} />
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 22, color: PAPEL }}>
        {DIAS[dIdx]}{r.dia ? '' : ' · ' + (r.aprox ? '~' : '') + hms(((v % 86400) + 86400) % 86400, r.seg || r.modo === 'seg' || (r.modo === 'parado' && r.seg))}
      </div>
    </div>}
  </>;
};

// ───────── Cred: crédito na tela (canto inferior esquerdo, Plex Mono 20 px) ─────────
export const Cred = ({ cred, baixo = 28 }) => {
  const f = useCurrentFrame();
  if (!cred) return null;
  const lin_ = Array.isArray(cred) ? cred : [cred];
  return <div style={{ position: 'absolute', left: 36, bottom: baixo, opacity: lin(f, 4, 14) * 0.95 }}>
    {lin_.map((l) => <div key={l} style={{ fontFamily: MONO, fontSize: 20, color: PAPEL, background: 'rgba(10,12,14,.9)', padding: '3px 10px', marginTop: 4, display: 'table' }}>{l}</div>)}
  </div>;
};

const SeloAr = ({ txt, f, top = 256 }) => {
  const parts = txt.split(' · '); const rec = txt.startsWith('RECONSTRUCTION');
  const tag = rec ? parts.slice(0, 2).join(' · ') : parts[0]; const sub = (rec ? parts.slice(2) : parts.slice(1)).join(' · ');
  const cor = rec ? FERRUGEM : CIANO;
  return <div style={{ position: 'absolute', left: 36, top, opacity: lin(f, 2, 10) }}>
    <div style={{ display: 'inline-block', fontFamily: COND, fontWeight: 700, fontSize: 30, letterSpacing: 4, color: rec ? PAPEL : TINTA, background: cor, padding: '2px 14px' }}>
      <span style={{ display: 'inline-block', width: 14, height: 14, borderRadius: 7, background: rec ? AMARELO : FERRUGEM, marginRight: 10, opacity: Math.floor(f / 15) % 2 ? 1 : 0.35 }} />{tag}</div>
    {sub && <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 21, color: PAPEL, marginTop: 6, background: 'rgba(10,12,14,.7)', padding: '3px 10px', display: 'table' }}>{sub}</div>}
  </div>;
};

// forma de onda do áudio de época
const Onda = ({ f, onda, x, y, w, h, cor, op = 1 }) => {
  if (f < 0 || f >= onda.length + 10) return null;
  const n = 72; const bw = w / n;
  return <svg width={w} height={h} style={{ position: 'absolute', left: x, top: y, opacity: op }}>
    {Array.from({ length: n }, (_, i) => {
      const k = f - (n - 1 - i); const v = k >= 0 && k < onda.length ? onda[k] : 0;
      const a = Math.max(3, v * h * 0.95);
      return <rect key={i} x={i * bw + 2} y={(h - a) / 2} width={bw - 4} height={a} fill={cor} opacity={0.35 + 0.65 * (i / n)} />;
    })}
  </svg>;
};

const Estatica = ({ f, op }) => <svg width={W} height={H} style={{ position: 'absolute', opacity: op }}>
  <filter id={`es${f}`}><feTurbulence type="fractalNoise" baseFrequency="0.02 0.9" seed={f} /><feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.8 0" /></filter>
  <rect width={W} height={H} filter={`url(#es${f})`} />
</svg>;

// ───────── Arquivo: áudio de época (real ou reconstrução) com legenda traduzida ─────────
export const Arquivo = ({ p }) => {
  const f = useCurrentFrame();
  const fa = f - p.onda_ini;
  const l = p.leg.find(([a, b]) => fa >= a && fa < b);
  const rec = p.aid === 'A5';
  const op = l ? Math.min(lin(fa, l[0], l[0] + 4), lin(fa, l[1] - 4, l[1], 1, 0)) : 0;
  const ing = l ? l[3].split(/(TEMPORARY|TEMPORARILY)/) : [];
  const fimGl = lin(f, p.dur - 20, p.dur - 4, 0, 1);
  return (
    <AbsoluteFill style={{ background: '#07080a' }}>
      {p.fundo ? <>
        <OffthreadVideo src={staticFile('clips/' + p.fundo)} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        <AbsoluteFill style={{ background: 'rgba(7,8,10,.5)' }} />
        <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 50%, rgba(0,0,0,.5) 100%)' }} />
      </> : <>
        <svg width={W} height={H} style={{ position: 'absolute', opacity: 0.22 }}>
          <filter id="g2"><feTurbulence type="fractalNoise" baseFrequency="0.8" seed={Math.floor(f / 2)} /><feColorMatrix values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0.25 0" /></filter>
          <rect width={W} height={H} filter="url(#g2)" />
        </svg>
        {p.rotulo && <div style={{ position: 'absolute', left: 0, right: 0, top: 330, textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: 6, color: '#7f8892' }}>{p.rotulo}</div>}
        <Onda f={fa} onda={p.onda} x={360} y={400} w={1200} h={240} cor={rec ? FERRUGEM : CIANO} />
      </>}
      {p.fundo && <Onda f={fa} onda={p.onda} x={1000} y={930} w={860} h={96} cor={rec ? FERRUGEM : CIANO} op={0.9} />}
      <SeloAr txt={p.selo} f={f} />
      {l && <div style={{ position: 'absolute', left: 120, right: 120, bottom: 150, textAlign: 'center', opacity: op }}>
        {l[2] && <div style={{ fontFamily: MONO, fontSize: 26, color: '#c9c4b8', marginBottom: 8, textShadow: '0 2px 6px #000' }}>{l[2]}</div>}
        <div style={{ display: 'inline-block', fontFamily: COND, fontWeight: 700, fontSize: 46, color: '#fff', background: 'rgba(10,12,14,.78)', padding: '4px 22px', letterSpacing: 0.5, lineHeight: 1.18 }}>
          {ing.map((s, i) => <span key={i} style={{ color: /TEMPORAR/.test(s) ? AMARELO : '#fff' }}>{s}</span>)}
        </div>
      </div>}
      <Cred cred={p.creds} />
      {(p.aid === 'A1' || p.aid === 'A6') && fimGl > 0 && <Estatica f={f} op={0.55 * fimGl} />}
    </AbsoluteFill>
  );
};

// ───────── Contador em tela cheia ─────────
function parseT(t) {
  if (t.startsWith('+')) { const [h, m, s] = t.slice(1).split(':').map(Number); return { k: 'dec', s: h * 3600 + m * 60 + s }; }
  const m = t.match(/^(?:(\d\d)\.(\d\d)(?:\.(\d{4}))? )?(\d\d):(\d\d)(?::(\d\d))?$/);
  const d = m && m[1] ? +m[1] : 26, mo = m && m[2] ? +m[2] : 4, y = m && m[3] ? +m[3] : 1986;
  const hasD = !!(m && m[1]);
  const s = ((m && m[3]) ? 0 : (d - 26) * 86400) + (+m[4]) * 3600 + (+m[5]) * 60 + (+(m[6] || 0));
  return { k: 'tod', s, seg: !!m[6], d, mo, y, hasD };
}
const MES = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
const DSEM = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT'];

export const Contador = ({ p }) => {
  const f = useCurrentFrame();
  const a = parseT(p.de_t), b = parseT(p.ate_t);
  let txt, sub = null, correndo = false;
  if (b.k === 'dec') {
    const s0 = a.k === 'dec' ? a.s : Math.max(0, a.s - BTN);
    const k = io(lin(f, 6, p.dur * 0.7));
    const v = s0 + (b.s - s0) * k; correndo = k < 1;
    txt = '+' + hms(v);
  } else {
    const k = a.s === b.s ? 1 : io(lin(f, 6, p.dur * 0.65));
    const v = a.s + (b.s - a.s) * k; correndo = a.s !== b.s && k < 1;
    const seg = a.seg || b.seg;
    txt = hms(((v % 86400) + 86400) % 86400, seg);
    const dd = new Date(Date.UTC(b.y, b.mo - 1, b.d));
    sub = `${DSEM[dd.getUTCDay()]} ${b.d} ${MES[b.mo - 1]} ${b.y}` + (Math.floor(v / 86400) !== Math.floor(b.s / 86400) && b.y === 1986 ? '' : '');
  }
  const pulso = !correndo ? 0.6 + 0.4 * Math.abs(Math.sin(f / 12)) : 1;
  const flash = b.k === 'dec' ? lin(f, p.dur * 0.7, p.dur * 0.7 + 6, 1, 0) * 0.14 : 0;
  return (
    <AbsoluteFill style={{ background: fundoEscuro, alignItems: 'center', justifyContent: 'center' }}>
      {sub && <div style={{ fontFamily: COND, fontWeight: 700, fontSize: 54, letterSpacing: 8, color: '#9aa3ad', marginBottom: 10, opacity: lin(f, 2, 12) }}>{sub}</div>}
      <div style={{ fontFamily: DISPLAY, fontSize: b.k === 'dec' ? 250 : 270, color: AMARELO, letterSpacing: 4, fontVariantNumeric: 'tabular-nums', opacity: lin(f, 0, 6) * (correndo ? 1 : pulso),
        textShadow: '0 8px 0 rgba(0,0,0,.55)' }}>{txt}</div>
      {p.rotulo && <div style={{ fontFamily: COND, fontWeight: 700, fontSize: 64, color: '#fff', letterSpacing: 5, marginTop: 22, opacity: lin(f, 10, 22) }}>{p.rotulo}</div>}
      <div style={{ width: lin(f, 8, 24, 0, 360, Easing.out(Easing.cubic)), height: 6, background: AMARELO, marginTop: 24 }} />
      <AbsoluteFill style={{ background: '#fff', opacity: flash }} />
    </AbsoluteFill>
  );
};

// ───────── texto datilografado ─────────
const Datilografado = ({ f, t0, t1, texto }) => {
  const n = Math.floor(lin(f, t0, t1, 0, texto.length));
  const fim = n >= texto.length;
  return <span style={{ whiteSpace: 'pre-wrap' }}>{texto.slice(0, n)}{!fim && f >= t0 ? <span style={{ opacity: Math.floor(f / 8) % 2 ? 1 : 0.2 }}>▌</span> : null}</span>;
};

export const Datilo = ({ p }) => {
  const f = useCurrentFrame();
  const cab = /^\d\d\.\d\d\.\d{4}/.test(p.linhas[0]) ? p.linhas[0] : null;
  const corpo = (cab ? p.linhas.slice(1) : p.linhas).join('\n');
  const grande = !cab && p.linhas.length === 1;
  const fim = Math.min(p.dur * 0.7, 20 + corpo.length * 1.4);
  const carimbo = lin(f, 8, 14, 0, 1, Easing.out(Easing.cubic));
  return (
    <AbsoluteFill style={{ background: fundoEscuro, alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ width: 1280, minHeight: 560, background: PAPEL, boxShadow: sombra, padding: '48px 70px', boxSizing: 'border-box', transform: 'rotate(-1.2deg)', position: 'relative',
        backgroundImage: 'repeating-linear-gradient(0deg, transparent 0 55px, rgba(43,206,226,.22) 55px 57px)', opacity: lin(f, 0, 6) }}>
        {cab && <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 38, color: FERRUGEM, letterSpacing: 3 }}>{cab}</div>}
        {grande ? <div style={{ textAlign: 'center', marginTop: 90, transform: `scale(${2.1 - 1.1 * carimbo}) rotate(-6deg)`, opacity: carimbo }}>
          <span style={{ fontFamily: DISPLAY, fontSize: 210, color: FERRUGEM, border: `12px solid ${FERRUGEM}`, padding: '0 40px', letterSpacing: 8, mixBlendMode: 'multiply' }}>{corpo}</span></div>
          : <div style={{ fontFamily: MONO, fontSize: 48, lineHeight: '58px', color: '#1d1b18', marginTop: 26 }}>
            <Datilografado f={f} t0={10} t1={fim} texto={corpo} />
          </div>}
        <div style={{ position: 'absolute', right: 26, bottom: 16, fontFamily: COND, fontWeight: 700, fontSize: 26, color: '#5a554c', letterSpacing: 2 }}>{p.selo || 'QUOTED'}</div>
      </div>
    </AbsoluteFill>
  );
};

export const Teletipo = ({ p }) => {
  const f = useCurrentFrame();
  const cab = /ТАСС/.test(p.linhas[0]) ? p.linhas[0] : null;
  const corpo = (cab ? p.linhas.slice(1) : p.linhas).join('\n');
  const fim = Math.min(p.dur * 0.78, 14 + corpo.length * 0.9);
  return (
    <AbsoluteFill style={{ background: fundoEscuro, alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ width: 1360, minHeight: 600, background: '#F1ECDD', boxShadow: sombra, padding: '48px 80px', boxSizing: 'border-box', position: 'relative', transform: 'rotate(.8deg)',
        backgroundImage: 'radial-gradient(circle at 20px 50%, #c9c2b0 8px, transparent 9px), radial-gradient(circle at calc(100% - 20px) 50%, #c9c2b0 8px, transparent 9px)', backgroundSize: '100% 50px', opacity: lin(f, 0, 6) }}>
        {cab && <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 40, color: FERRUGEM, marginBottom: 14 }}>{cab}</div>}
        <div style={{ fontFamily: MONO, fontSize: cab ? 46 : 44, lineHeight: '64px', color: '#1d1b18' }}>
          <Datilografado f={f} t0={8} t1={fim} texto={corpo} />
        </div>
        <div style={{ position: 'absolute', left: 80, bottom: 22, fontFamily: COND, fontWeight: 700, fontSize: 26, color: '#5a554c', letterSpacing: 2 }}>{p.selo}</div>
      </div>
    </AbsoluteFill>
  );
};

// ───────── três relógios (instrumentos × diretor × Politburo) ─────────
export const TresRelogios = ({ p }) => {
  const f = useCurrentFrame(); const D = p.dur;
  const ent = [0.04, 0.3, 0.56].map((k) => k * D);
  const ar = lin(f, D * 0.8, D * 0.92);
  return (
    <AbsoluteFill style={{ background: fundoEscuro, alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ display: 'flex', gap: 34 }}>
        {p.valores.map((v, i) => {
          const u = lin(f, ent[i], ent[i] + 14, 0, 1, Easing.out(Easing.back(1.3)));
          return <div key={i} style={{ width: 540, padding: '30px 14px 26px', textAlign: 'center', background: 'rgba(10,12,14,.9)', border: `3px solid ${i === 2 ? AMARELO : '#3b4148'}`,
            opacity: u, transform: `translateY(${(1 - u) * 50}px) scale(${0.94 + 0.06 * u})`, boxShadow: sombra }}>
            <div style={{ fontFamily: DISPLAY, fontSize: 132, color: i === 2 ? AMARELO : PAPEL, letterSpacing: 3, fontVariantNumeric: 'tabular-nums' }}>{v}</div>
            <div style={{ fontFamily: COND, fontWeight: 700, fontSize: 38, color: '#9aa3ad', letterSpacing: 4, marginTop: 8 }}>{p.rotulos[i]}</div>
          </div>;
        })}
      </div>
      <div style={{ marginTop: 56, fontFamily: COND, fontWeight: 700, fontSize: 56, letterSpacing: 6, color: AMARELO, opacity: ar }}>EVERY STEP UP THE LINE, THE CLOCK GOT ROUNDER</div>
    </AbsoluteFill>
  );
};

// ───────── mural do fecho: cada hora segue em papel ─────────
export const Mural = ({ p }) => {
  const f = useCurrentFrame(); const D = p.dur;
  const pos = [[130, 56, -2.5], [700, 90, 1.8], [1270, 50, -1.2], [150, 470, 2.2], [710, 500, -2], [1260, 460, 2.6]];
  const z = lin(f, 0, D, 1, 1.07);
  return (
    <AbsoluteFill style={{ background: TINTA, overflow: 'hidden' }}>
      <AbsoluteFill style={{ background: `radial-gradient(ellipse at 8% 92%, rgba(200,86,30,.28), transparent 45%), radial-gradient(ellipse at 50% 45%, #1d2127, ${TINTA} 80%)` }} />
      <AbsoluteFill style={{ transform: `scale(${z})`, transformOrigin: '50% 50%' }}>
        {p.mural_imgs.map(([img, iw, ih, hora, rot], i) => {
          const t0 = 6 + i * 0.075 * D; const u = lin(f, t0, t0 + 16, 0, 1, Easing.out(Easing.back(1.2)));
          const [x, y, r] = pos[i];
          return <div key={i} style={{ position: 'absolute', left: x, top: y + (1 - u) * -80, width: 520, opacity: u, transform: `rotate(${r - (1 - u) * 6}deg)`, boxShadow: sombra, background: '#E9E2D0', padding: '14px 14px 62px' }}>
            <div style={{ width: 492, height: 300, overflow: 'hidden', background: '#000' }}>
              <Img src={staticFile('img/' + img)} style={{ width: '100%', height: '100%', objectFit: 'cover', objectPosition: '50% 18%', filter: 'sepia(.15) contrast(1.05)' }} />
            </div>
            <div style={{ position: 'absolute', left: 18, bottom: 12, fontFamily: DISPLAY, fontSize: 40, color: FERRUGEM, letterSpacing: 2 }}>{hora}</div>
            <div style={{ position: 'absolute', right: 18, bottom: 18, fontFamily: COND, fontWeight: 700, fontSize: 24, color: '#4d483f', letterSpacing: 2 }}>{rot}</div>
          </div>;
        })}
      </AbsoluteFill>
      <div style={{ position: 'absolute', left: 0, right: 0, bottom: 58, textAlign: 'center', fontFamily: DISPLAY, fontSize: 88, color: AMARELO, letterSpacing: 4, opacity: lin(f, D * 0.55, D * 0.7), textShadow: '0 6px 0 rgba(0,0,0,.6)' }}>+67:36:20 · ALL ON PAPER</div>
    </AbsoluteFill>
  );
};

// ───────── glitch: o log acaba, silêncio ─────────
export const Glitch = ({ p }) => {
  const f = useCurrentFrame(); const k = Math.sin(Math.PI * lin(f, 0, p.dur));
  return (
    <AbsoluteFill style={{ background: '#050607', alignItems: 'center', justifyContent: 'center' }}>
      {Array.from({ length: 9 }, (_, i) => <div key={i} style={{ position: 'absolute', left: (random(`gx${Math.floor(f / 2)}-${i}`) - 0.5) * 280 * k, top: (i / 9) * H, width: W, height: H / 9,
        background: `rgba(237,230,214,${0.05 + 0.1 * random(`gy${Math.floor(f / 2)}-${i}`)})` }} />)}
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 40, letterSpacing: 10, color: '#7f8892', opacity: lin(f, 12, 22) * (0.5 + 0.5 * Math.abs(Math.sin(f / 6))) }}>— LOG ENDS —</div>
      <Estatica f={f} op={0.5 * k + 0.1} />
    </AbsoluteFill>
  );
};

// ───────── mapa 2D por país (terra escura; pluma até a Suécia) ─────────
export const MapaCh = ({ p }) => {
  const f = useCurrentFrame();
  const z = lin(f, 0, p.dur, 1.0, 1.04);
  const rotulo = (x, y, txt, cor, op, esq) => (
    <text x={esq ? x - 22 : x + 22} y={y + 12} fill={cor} fontFamily={COND} fontWeight={700} fontSize={42} textAnchor={esq ? 'end' : 'start'} opacity={op}
      style={{ paintOrder: 'stroke', stroke: TINTA, strokeWidth: 8, letterSpacing: 1.5 }}>{txt}</text>
  );
  const P = Object.fromEntries(p.pts.map(([n, x, y]) => [n, [x, y]]));
  const ch = P['CHERNOBYL NPP'], fo = P['FORSMARK'];
  const pk = lin(f, 10, Math.max(40, p.dur * 0.7), 0, 1, io);
  let pluma = null;
  if (p.pluma && ch && fo) {
    const mx = (ch[0] + fo[0]) / 2 - 90, my = (ch[1] + fo[1]) / 2 + 40;
    const d = `M${ch[0]},${ch[1]} Q${mx},${my} ${fo[0]},${fo[1]}`;
    pluma = <g>
      <path d={d} fill="none" stroke={AMARELO} strokeWidth={70} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - pk} opacity={0.18} />
      <path d={d} fill="none" stroke={AMARELO} strokeWidth={26} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - pk} opacity={0.3} />
      <path d={d} fill="none" stroke={AMARELO} strokeWidth={9} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - pk} />
    </g>;
  }
  return (
    <AbsoluteFill style={{ background: '#0a1822', overflow: 'hidden' }}>
      <AbsoluteFill style={{ transform: `scale(${z})` }}>
        <svg width={W} height={H} style={{ position: 'absolute', left: 0, top: 0 }}>
          {p.paths.map((q, i) => <path key={i} d={q.d} fill={p.pluma && q.pais === 'Sweden' ? '#2f5560' : q.pais === 'Ukraine' ? '#2d343d' : '#242a31'} stroke="#56606b" strokeWidth={1.6} />)}
          {pluma}
          {p.raio30 > 0 && ch && <circle cx={ch[0]} cy={ch[1]} r={p.raio30} fill="rgba(253,213,5,.07)" stroke={AMARELO} strokeWidth={4} strokeDasharray="22 14" opacity={lin(f, 8, 24)} />}
          {p.linhas.map(([x1, y1, x2, y2, rot], i) => {
            if (p.pluma) return null;
            const t0 = 10 + i * 14; const k = lin(f, t0, t0 + 32, 0, 1, io); const L = Math.hypot(x2 - x1, y2 - y1);
            const op = lin(f, t0 + 18, t0 + 30);
            const esq = (x1 + x2) / 2 > W - 380;
            return <g key={i}>
              <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={AMARELO} strokeWidth={7} strokeLinecap="round" strokeDasharray={L} strokeDashoffset={L * (1 - k)} />
              {rot ? <text x={(x1 + x2) / 2} y={(y1 + y2) / 2 - 30} fill={AMARELO} fontFamily={COND} fontWeight={700} fontSize={44} textAnchor={esq ? 'end' : 'middle'} opacity={op}
                style={{ paintOrder: 'stroke', stroke: TINTA, strokeWidth: 8, letterSpacing: 2 }}>{rot}</text> : null}
            </g>;
          })}
          {p.pts.map(([nome, x, y], i) => {
            const op = lin(f, 4 + i * 5, 12 + i * 5);
            const npp = nome === 'CHERNOBYL NPP', fm = nome === 'FORSMARK';
            const esq = x > W - 380 || nome === 'PRIPYAT';
            const dy = nome === 'PRIPYAT' ? -34 : nome === 'CHERNOBYL (TOWN)' ? 30 : npp && !p.pluma ? 18 : 0;
            return <g key={nome} opacity={op}>
              {npp && <circle cx={x} cy={y} r={24 + 8 * Math.abs(Math.sin(f / 10))} fill="none" stroke={AMARELO} strokeWidth={4} />}
              {fm && p.pluma && pk > 0.97 && <circle cx={x} cy={y} r={20 + 12 * Math.abs(Math.sin(f / 7))} fill="none" stroke={CIANO} strokeWidth={5} />}
              <circle cx={x} cy={y} r={11} fill={npp ? FERRUGEM : fm ? CIANO : AMARELO} stroke={TINTA} strokeWidth={3} />
              {rotulo(x, y + dy, nome, fm ? CIANO : npp ? '#fff' : '#dfe3e8', 1, esq)}
            </g>;
          })}
        </svg>
      </AbsoluteFill>
      {p.selo && <div style={{ position: 'absolute', right: 56, top: 96, fontFamily: MONO, fontWeight: 700, fontSize: 26, color: AMARELO, letterSpacing: 3, border: `3px solid ${AMARELO}`, background: 'rgba(17,20,24,.9)', padding: '6px 16px' }}>{p.selo}</div>}
      <Cred cred={['Map: Natural Earth (public domain)']} baixo={28} />
    </AbsoluteFill>
  );
};
