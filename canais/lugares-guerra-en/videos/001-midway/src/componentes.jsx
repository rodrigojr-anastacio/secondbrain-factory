import React from 'react';
import { AbsoluteFill, Img, OffthreadVideo, staticFile, interpolate, useCurrentFrame, Easing, spring, useVideoConfig } from 'remotion';
import { DISPLAY, MONO, COND, AMARELO, CIANO, TINTA, GRIFO, AREIA, MAR, W, H } from './estilo.jsx';

// Gramática de tela do canal (biblia/visual.md): KenBurns, Filme, DocGrifo, Número, Mapa2D, EntaoAgora, Cartela (SCHEMATIC),
// PerfilProfundidade, Card; sobreposições Ficha (data · lugar · acervo) e Num (número sobreposto). Tempos vêm do tools/build.py.
const ease = Easing.bezier(0.45, 0, 0.2, 1);
const suave = Easing.inOut(Easing.sin);
const C = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const lerp = (a, b, k) => a + (b - a) * k;
const glerp = (a, b, k) => a * Math.pow(b / a, k);
const fundoEscuro = 'radial-gradient(ellipse at center, #2a2f36 0%, #0c0e11 78%)';
const sombraTxt = '0 4px 0 rgba(0,0,0,.65), 0 0 22px rgba(0,0,0,.5)';

// ───────── sobreposições ─────────
export const Ficha = ({ linhas, inicio = 8, fim = null }) => {
  const f = useCurrentFrame();
  if (!linhas || !linhas.length) return null;
  let op = interpolate(f, [inicio, inicio + 10], [0, 1], C);
  if (fim !== null) op *= interpolate(f, [fim - 8, fim], [1, 0], C);
  if (op <= 0) return null;
  const x = interpolate(f, [inicio, inicio + 12], [-26, 0], { ...C, easing: ease });
  return (
    <div style={{ position: 'absolute', left: 56, bottom: 52, opacity: op, transform: `translateX(${x}px)`, maxWidth: 1060,
      background: 'rgba(17,20,24,.88)', borderLeft: `6px solid ${AMARELO}`, padding: '11px 22px 11px 18px' }}>
      {linhas.map((l, i) => (
        <div key={i} style={{ fontFamily: MONO, fontSize: i === 0 ? 30 : 22, color: i === 0 ? '#fff' : '#C9CDD2', letterSpacing: i === 0 ? 1.5 : 0.6,
          fontWeight: i === 0 ? 700 : 400, lineHeight: 1.38, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{l}</div>
      ))}
    </div>
  );
};

export const Num = ({ num, topo = false, inicio = 14 }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!num) return null;
  const s = spring({ frame: f - inicio, fps, config: { damping: 14, mass: 0.7 } });
  if (f < inicio) return null;
  return (
    <div style={{ position: 'absolute', right: 56, [topo ? 'top' : 'bottom']: topo ? 52 : 52, opacity: Math.min(1, s * 1.4), transform: `scale(${0.88 + 0.12 * s})`,
      transformOrigin: topo ? 'top right' : 'bottom right', textAlign: 'right', background: '#111418', padding: '14px 28px 12px', boxShadow: '0 6px 24px rgba(0,0,0,.5)', borderRight: `6px solid ${AMARELO}`, maxWidth: 900 }}>
      <div style={{ fontFamily: DISPLAY, fontSize: 104, color: AMARELO, lineHeight: 0.98, letterSpacing: 1 }}>{num[0]}</div>
      {num[1] ? <div style={{ fontFamily: COND, fontWeight: 700, fontSize: 38, color: '#fff', letterSpacing: 2.5, marginTop: 4 }}>{num[1]}</div> : null}
    </div>
  );
};

const Selo = ({ txt }) => txt ? (
  <div style={{ position: 'absolute', right: 56, top: 48, fontFamily: MONO, fontWeight: 700, fontSize: 28, color: AMARELO, letterSpacing: 3,
    border: `3px solid ${AMARELO}`, background: 'rgba(17,20,24,.9)', padding: '6px 16px' }}>{txt}</div>
) : null;

const Vinheta = () => <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,.38) 100%)' }} />;

// ───────── KenBurns ─────────
function vista(iw, ih, cx, cy, z, crop) {
  let ox = 0, oy = 0, sw = iw, sh = ih;
  if (crop) { ox = crop[0] * iw; oy = crop[1] * ih; sw = crop[2] * iw; sh = crop[3] * ih; }
  let bw, bh;
  if (sw / sh > W / H) { bh = sh; bw = (sh * W) / H; } else { bw = sw; bh = (sw * H) / W; }
  const vw = bw / z, vh = bh / z;
  const x0 = Math.min(Math.max(cx * sw - vw / 2, 0), sw - vw) + ox;
  const y0 = Math.min(Math.max(cy * sh - vh / 2, 0), sh - vh) + oy;
  return { x0, y0, s: W / vw };
}

export const KenBurns = ({ p }) => {
  const f = useCurrentFrame();
  const k = interpolate(f, [0, p.dur], [0, 1], { ...C, easing: suave });
  const [a, b] = [p.de, p.para];
  const v = vista(p.iw, p.ih, lerp(a[0], b[0], k), lerp(a[1], b[1], k), glerp(a[2], b[2], k), p.crop);
  return (
    <AbsoluteFill style={{ background: TINTA, overflow: 'hidden' }}>
      <Img src={staticFile('img/' + p.img)} style={{ position: 'absolute', left: -v.x0 * v.s, top: -v.y0 * v.s, width: p.iw * v.s, height: p.ih * v.s, maxWidth: 'none' }} />
      <Vinheta />
      <Ficha linhas={p.ficha} />
      <Num num={p.num} topo={!!p.ficha} />
    </AbsoluteFill>
  );
};

// ───────── Filme (trecho já cortado, sem áudio, na velocidade certa: public/clips/<plano>.mp4) ─────────
export const Filme = ({ p }) => {
  const f = useCurrentFrame();
  const z = interpolate(f, [0, p.dur], [1.0, 1.045], C);
  return (
    <AbsoluteFill style={{ background: TINTA, overflow: 'hidden' }}>
      <AbsoluteFill style={{ transform: `scale(${z})` }}>
        <OffthreadVideo src={staticFile('clips/' + p.clip)} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      </AbsoluteFill>
      <Vinheta />
      <Ficha linhas={p.ficha} />
      <Num num={p.num} topo={!!p.ficha} />
    </AbsoluteFill>
  );
};

// ───────── DocGrifo ─────────
export const DocGrifo = ({ p }) => {
  const f = useCurrentFrame();
  const { pag, alvo } = p;
  const folga = Math.max(0, Math.min(290, (W - p.iw * pag[2]) / 2 - 30));   // desloca a página só se couber
  let cam, ficha = null, fichaFim = null, zoomFim = 0, off = 0;   // off: página deslocada à direita enquanto a Ficha está na tela
  if (p.regiao) {   // só a região (recorte): nunca a página inteira (ex.: foto de terceiros no topo da página da USFWS)
    const k = interpolate(f, [0, p.dur], [0, 1], C);
    cam = [alvo[0], alvo[1], alvo[2] * (1 + 0.05 * k)];
    ficha = p.ficha;
  } else if (!alvo) {
    const k = interpolate(f, [0, p.dur], [0, 1], C);
    cam = [pag[0], pag[1], pag[2] * (1 + 0.06 * k)];
    ficha = p.ficha; off = p.ficha ? folga : 0;
  } else if (p.cont && p.cam_ant) {
    zoomFim = 20;
    const k = interpolate(f, [0, zoomFim], [0, 1], { ...C, easing: ease });
    const a = p.cam_ant;
    cam = [lerp(a[0], alvo[0], k), lerp(a[1], alvo[1], k), glerp(a[2], alvo[2], k)];
  } else if (p.dur >= 80) {
    const P = 16; zoomFim = P + 26;
    const k = interpolate(f, [P, zoomFim], [0, 1], { ...C, easing: ease });
    cam = [lerp(pag[0], alvo[0], k), lerp(pag[1], alvo[1], k), glerp(pag[2], alvo[2], k)];
    ficha = p.ficha; fichaFim = P + 8;   // a Ficha sai antes do zoom e do grifo
    off = p.ficha ? folga * (1 - k) : 0;
  } else {
    cam = alvo;
  }
  if (alvo && !p.regiao) {  // respiro depois do zoom
    const k2 = interpolate(f, [zoomFim, p.dur], [0, 1], C);
    cam = [cam[0], cam[1], cam[2] * (1 + 0.035 * k2)];
  }
  const [cx, cy, s] = cam;
  // grifo: corre quando a narração lê a frase (g_ini/g_fim do Whisper), senão logo depois do zoom
  const g = p.grifo || [];
  let gs = p.g_ini != null ? Math.max(p.g_ini, zoomFim + 2) : zoomFim + 8;
  let ge = p.g_fim != null ? p.g_fim : gs + 30;
  ge = Math.min(Math.max(ge, gs + 12), gs + 90);
  if (gs > p.dur - 14) { gs = Math.max(zoomFim, p.dur - 30); ge = gs + 16; }
  const totW = g.reduce((t, r) => t + r[2], 0) || 1;
  const prog = interpolate(f, [gs, ge], [0, 1], { ...C, easing: Easing.inOut(Easing.quad) }) * totW;
  let acc = 0;
  return (
    <AbsoluteFill style={{ background: fundoEscuro, overflow: 'hidden' }}>
      <div style={{ position: 'absolute', left: W / 2 + off - cx * s, top: H / 2 - cy * s, width: p.iw * s, height: p.ih * s, boxShadow: '0 30px 90px rgba(0,0,0,.75)',
        clipPath: p.regiao ? `inset(${p.regiao[1] * 100}% ${(1 - p.regiao[0] - p.regiao[2]) * 100}% ${(1 - p.regiao[1] - p.regiao[3]) * 100}% ${p.regiao[0] * 100}%)` : undefined }}>
        <Img src={staticFile('img/' + p.img)} style={{ width: '100%', height: '100%', maxWidth: 'none', filter: 'contrast(1.06)' }} />
        {g.map((r, i) => {
          const fr = Math.min(1, Math.max(0, (prog - acc) / r[2])); acc += r[2];
          if (fr <= 0) return null;
          const padX = 0.004, padY = 0.0025;
          return <div key={i} style={{ position: 'absolute', left: `${(r[0] - padX) * 100}%`, top: `${(r[1] - padY) * 100}%`, height: `${(r[3] + 2 * padY) * 100}%`,
            width: `${(r[2] + 2 * padX) * fr * 100}%`, background: GRIFO, mixBlendMode: 'multiply', borderRadius: 4 }} />;
        })}
      </div>
      <Ficha linhas={ficha} inicio={3} fim={fichaFim} />
      <Num num={p.num} topo inicio={Math.max(14, zoomFim + 4)} />
    </AbsoluteFill>
  );
};

// ───────── Número (tela cheia) ─────────
function partesValor(v) {
  if (/ [+→=] /.test(v)) return { tipo: 'seq', partes: v.split(/(?= [+→=] )/) };
  const m = v.match(/^([^\d]*)([\d][\d,]*)([^\d]*)$/);
  if (m) {
    const n = parseInt(m[2].replace(/,/g, ''), 10);
    const ano = /^(19|20)\d\d$/.test(m[2]) && !m[2].includes(',');
    if (!ano && !/[A-Z]{3} /.test(m[1]) && n >= 10) return { tipo: 'conta', pre: m[1], n, suf: m[3], virg: m[2].includes(',') };
  }
  return { tipo: 'fixo' };
}

export const Numero = ({ p }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 15, mass: 0.8 } });
  const P = partesValor(p.valor);
  let txt = p.valor;
  if (P.tipo === 'conta') {
    const k = interpolate(f, [2, 26], [0, 1], { ...C, easing: Easing.out(Easing.cubic) });
    const n = Math.round(P.n * k);
    txt = P.pre + (P.virg ? n.toLocaleString('en-US') : String(n)) + P.suf;
  }
  const rot = interpolate(f, [10, 22], [0, 1], C);
  return (
    <AbsoluteFill style={{ background: fundoEscuro, alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ fontFamily: DISPLAY, fontSize: 250, color: AMARELO, lineHeight: 1, transform: `scale(${0.85 + 0.15 * s})`, opacity: Math.min(1, s * 1.5),
        textShadow: '0 8px 0 rgba(0,0,0,.55)', letterSpacing: 2, whiteSpace: 'nowrap' }}>
        {P.tipo === 'seq' ? P.partes.map((pt, i) => (
          <span key={i} style={{ opacity: interpolate(f, [i * 14, i * 14 + 8], [0, 1], C), color: i === P.partes.length - 1 && P.partes.length > 2 ? '#fff' : AMARELO }}>{pt}</span>
        )) : txt}
      </div>
      <div style={{ fontFamily: COND, fontWeight: 700, fontSize: 64, color: '#fff', letterSpacing: 5, marginTop: 26, opacity: rot,
        transform: `translateY(${(1 - rot) * 16}px)` }}>{p.rotulo}</div>
      <div style={{ width: interpolate(f, [8, 24], [0, 360], { ...C, easing: ease }), height: 6, background: AMARELO, marginTop: 26 }} />
    </AbsoluteFill>
  );
};

// ───────── Mapa 2D (Natural Earth 50m, projeção e caminhos calculados no build.py) ─────────
export const Mapa2D = ({ p }) => {
  const f = useCurrentFrame();
  const z = interpolate(f, [0, p.dur], [1.0, 1.05], C);
  const rotulo = (x, y, txt, cor, op, esq, dy = 0) => (
    <text x={esq ? x - 22 : x + 22} y={y + 12 + dy} fill={cor} fontFamily={COND} fontWeight={700} fontSize={42} textAnchor={esq ? 'end' : 'start'} opacity={op}
      style={{ paintOrder: 'stroke', stroke: TINTA, strokeWidth: 8, letterSpacing: 1.5 }}>{txt}</text>
  );
  return (
    <AbsoluteFill style={{ background: MAR, overflow: 'hidden' }}>
      <AbsoluteFill style={{ transform: `scale(${z})` }}>
        <svg width={W} height={H}>
          <defs>
            <pattern id="grade" width="120" height="120" patternUnits="userSpaceOnUse"><path d="M120 0H0V120" fill="none" stroke="rgba(255,255,255,.05)" strokeWidth="2" /></pattern>
          </defs>
          <rect width={W} height={H} fill="url(#grade)" />
          {p.paths.map((d, i) => <path key={i} d={d} fill={AREIA} stroke="#8C7A57" strokeWidth={1.5} />)}
          {p.linhas.map(([x1, y1, x2, y2, rot], i) => {
            const t0 = 14 + i * 16;
            const k = interpolate(f, [t0, t0 + 34], [0, 1], { ...C, easing: ease });
            const L = Math.hypot(x2 - x1, y2 - y1);
            const op = interpolate(f, [t0 + 20, t0 + 32], [0, 1], C);
            if (L < 1) {
              const pul = (f - t0) % 40 / 40;
              return <g key={i}>
                <circle cx={x1} cy={y1} r={30 + 40 * pul} fill="none" stroke={AMARELO} strokeWidth={5} opacity={f > t0 ? 1 - pul : 0} />
                {rot ? rotulo(x1, y1 + 70, rot, AMARELO, op, x1 > W - 420) : null}
              </g>;
            }
            const esq = (x1 + x2) / 2 > W - 380;
            return <g key={i}>
              <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={AMARELO} strokeWidth={7} strokeLinecap="round" strokeDasharray={L} strokeDashoffset={L * (1 - k)} />
              {rot ? <text x={(x1 + x2) / 2} y={(y1 + y2) / 2 - 30} fill={AMARELO} fontFamily={COND} fontWeight={700} fontSize={44} textAnchor={esq ? 'end' : 'middle'} opacity={op}
                style={{ paintOrder: 'stroke', stroke: TINTA, strokeWidth: 8, letterSpacing: 2 }}>{rot}</text> : null}
            </g>;
          })}
          {p.pts.map(([nome, x, y], i) => {
            const op = interpolate(f, [4 + i * 5, 12 + i * 5], [0, 1], C);
            const mid = nome === 'MIDWAY';
            const esq = x > W - 380 || nome.startsWith('KAGA');
            const dy = p.naufr && nome.includes('WRECK') ? ({ 1: -44, 2: 0, 3: 44 }[i] || 0) : 0;
            return <g key={nome} opacity={op}>
              {mid ? <circle cx={x} cy={y} r={22} fill="none" stroke={CIANO} strokeWidth={5} /> : null}
              <circle cx={x} cy={y} r={11} fill={mid ? CIANO : AMARELO} stroke={TINTA} strokeWidth={3} />
              {rotulo(x, y, nome, mid ? CIANO : '#fff', 1, esq, dy)}
            </g>;
          })}
        </svg>
      </AbsoluteFill>
      <Selo txt={p.selo} />
      {p.selo ? <div style={{ position: 'absolute', left: 56, bottom: 40, fontFamily: MONO, fontSize: 22, color: '#C9CDD2' }}>SCHEMATIC · POSITIONS APPROXIMATE</div>
        : null}
      <Num num={p.num} topo={false} inicio={30} />
    </AbsoluteFill>
  );
};

// ───────── Cartela SCHEMATIC e perfil de profundidade ─────────
export const Cartela = ({ p }) => {
  const f = useCurrentFrame();
  if (p.linhas[0].startsWith('DEPTH')) return <PerfilProfundidade p={p} />;
  let t = 4;
  return (
    <AbsoluteFill style={{ background: fundoEscuro, alignItems: 'center', justifyContent: 'center' }}>
      {p.linhas[0].includes('CABLE') ? <CaboEsquema /> : null}
      {p.linhas.map((l, i) => {
        const ini = t; t += l.length * 0.9 + 6;
        const n = Math.floor(interpolate(f, [ini, ini + l.length * 0.9], [0, l.length], C));
        return <div key={i} style={{ fontFamily: MONO, fontWeight: 700, fontSize: i ? 44 : 54, color: i ? '#fff' : AMARELO, letterSpacing: 2, marginTop: i ? 34 : 0,
          minHeight: 70, whiteSpace: 'pre' }}>{l.slice(0, n)}<span style={{ opacity: n < l.length && n > 0 ? 1 : 0 }}>▌</span></div>;
      })}
      <Selo txt={p.selo} />
    </AbsoluteFill>
  );
};

const CaboEsquema = () => {
  const f = useCurrentFrame();
  const k = interpolate(f, [10, 50], [0, 1], { ...C, easing: ease });
  const x1 = 420, x2 = 1500, y = 250;
  return (
    <svg width={W} height={H} style={{ position: 'absolute', left: 0, top: 0 }}>
      <line x1={x1} y1={y} x2={x1 + (x2 - x1) * k} y2={y} stroke={CIANO} strokeWidth={6} strokeDasharray="18 12" />
      <circle cx={x1} cy={y} r={14} fill={AMARELO} stroke={TINTA} strokeWidth={3} />
      <circle cx={x2} cy={y} r={14} fill={CIANO} stroke={TINTA} strokeWidth={3} opacity={k > 0.95 ? 1 : 0.25} />
      <text x={x1} y={y - 34} fill="#fff" fontFamily={COND} fontWeight={700} fontSize={40} textAnchor="middle">PEARL HARBOR</text>
      <text x={x2} y={y - 34} fill={CIANO} fontFamily={COND} fontWeight={700} fontSize={40} textAnchor="middle">MIDWAY</text>
      <text x={(x1 + x2) / 2} y={y + 56} fill="rgba(201,205,210,.85)" fontFamily={MONO} fontSize={26} textAnchor="middle">UNDERSEA CABLE · NO RADIO</text>
    </svg>
  );
};

export const PerfilProfundidade = ({ p }) => {
  const f = useCurrentFrame();
  const z = (m) => 180 + (m / 5600) * 780;
  const fundo = [[0, 5200], [450, 5050], [780, 5450], [1200, 5350], [1575, 5500], [W, 5250]];
  const alvo = [['YORKTOWN · ~3 MI (~5,000 M)', 495, 5000], ['KAGA · ~5,400 M', 960, 5400], ['AKAGI', 1350, 5450]];
  const rov = p.linhas.join(' ').includes('ROV');
  const kr = interpolate(f, [24, 70], [0, 1], { ...C, easing: ease });
  return (
    <AbsoluteFill style={{ background: MAR }}>
      <svg width={W} height={H}>
        <defs><linearGradient id="agua" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#1d4a63" /><stop offset="1" stopColor="#061722" /></linearGradient></defs>
        <rect x={0} y={180} width={W} height={H - 180} fill="url(#agua)" />
        <rect x={0} y={0} width={W} height={180} fill="#284660" />
        <line x1={0} y1={180} x2={W} y2={180} stroke="#C8DCEB" strokeWidth={4} />
        <polygon points={[...fundo.map(([x, m]) => `${x},${z(m)}`), `${W},${H}`, `0,${H}`].join(' ')} fill={AREIA} />
        {[1000, 2000, 3000, 4000, 5000].map((m) => <g key={m}>
          <line x1={90} y1={z(m)} x2={135} y2={z(m)} stroke="#C8D2DC" strokeWidth={3} />
          <text x={145} y={z(m) + 9} fill="#C8D2DC" fontFamily={MONO} fontSize={26}>{m.toLocaleString('en-US')} M</text>
        </g>)}
        {rov ? <g>
          <line x1={W - 510} y1={180} x2={W - 510} y2={180 + (z(5150) - 180) * kr} stroke={AMARELO} strokeWidth={6} />
          <text x={W - 490} y={z(2600)} fill={AMARELO} fontFamily={COND} fontWeight={700} fontSize={42} opacity={kr}>ROV DIVES {'>'} 5,100 M (2023)</text>
        </g> : null}
        {alvo.map(([nome, x, m], i) => {
          const op = interpolate(f, [10 + i * 8, 20 + i * 8], [0, 1], C);
          return <g key={nome} opacity={op}>
            <circle cx={x} cy={z(m)} r={15} fill={AMARELO} stroke={TINTA} strokeWidth={4} />
            <text x={x} y={z(m) - 44} fill="#fff" fontFamily={COND} fontWeight={700} fontSize={44} textAnchor="middle" style={{ paintOrder: 'stroke', stroke: TINTA, strokeWidth: 8 }}>{nome}</text>
          </g>;
        })}
        <text x={W / 2} y={118} fill={AMARELO} fontFamily={MONO} fontWeight={700} fontSize={44} textAnchor="middle">{p.linhas[1]}</text>
        <text x={W / 2} y={H - 40} fill="#1e2a34" fontFamily={MONO} fontSize={26} textAnchor="middle">SCHEMATIC · NOT TO SCALE · POSITIONS APPROXIMATE</text>
      </svg>
      <Selo txt={p.selo} />
    </AbsoluteFill>
  );
};

// ───────── Então × agora ─────────
export const EntaoAgora = ({ p }) => {
  const f = useCurrentFrame();
  const D = p.dur;
  const z1 = interpolate(f, [0, D], [1.04, 1.14]);
  const z2 = interpolate(f, [0, D], [1.12, 1.03]);
  const a = Math.round(D * 0.34), b = Math.round(D * 0.58);
  const corte = interpolate(f, [a, b], [0, 100], { ...C, easing: ease });
  const v1 = vista(p.iw, p.ih, 0.5, 0.5, z1), v2 = vista(p.iw2, p.ih2, 0.5, 0.5, z2);
  const lab = (txt, cred, cor, op, lado) => (
    <div style={{ position: 'absolute', top: 52, [lado]: 60, opacity: op, textAlign: lado === 'left' ? 'left' : 'right' }}>
      <div style={{ fontFamily: DISPLAY, fontSize: 104, color: cor, textShadow: sombraTxt, letterSpacing: 2, lineHeight: 1 }}>{txt}</div>
      {cred ? <div style={{ fontFamily: MONO, fontSize: 21, color: '#E8EAED', background: 'rgba(17,20,24,.82)', padding: '5px 12px', marginTop: 10, display: 'inline-block' }}>{cred}</div> : null}
    </div>
  );
  return (
    <AbsoluteFill style={{ background: TINTA, overflow: 'hidden' }}>
      <Img src={staticFile('img/' + p.img)} style={{ position: 'absolute', left: -v1.x0 * v1.s, top: -v1.y0 * v1.s, width: p.iw * v1.s, height: p.ih * v1.s, maxWidth: 'none', filter: 'grayscale(1) contrast(1.1)' }} />
      <div style={{ position: 'absolute', inset: 0, clipPath: `inset(0 ${100 - corte}% 0 0)` }}>
        <Img src={staticFile('img/' + p.img2)} style={{ position: 'absolute', left: -v2.x0 * v2.s, top: -v2.y0 * v2.s, width: p.iw2 * v2.s, height: p.ih2 * v2.s, maxWidth: 'none' }} />
      </div>
      {corte > 0 && corte < 100 ? <div style={{ position: 'absolute', top: 0, bottom: 0, left: `${corte}%`, width: 8, marginLeft: -4, background: AMARELO, boxShadow: '0 0 20px rgba(253,213,5,.85)' }} /> : null}
      <Vinheta />
      {lab(p.rot1, p.cred1, '#fff', interpolate(f, [6, 16, a, a + 14], [0, 1, 1, 0], C), 'left')}
      {lab(p.rot2, p.cred2, AMARELO, interpolate(f, [b - 6, b + 8], [0, 1], C), 'right')}
      <Num num={p.num} topo={false} inicio={b + 14} />
    </AbsoluteFill>
  );
};

// ───────── Card final ─────────
export const Card = ({ p }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = spring({ frame: f, fps, config: { damping: 16 } });
  const op2 = interpolate(f, [16, 28], [0, 1], C);
  const op3 = interpolate(f, [34, 46], [0, 1], C);
  const sai = interpolate(f, [p.dur - 24, p.dur], [1, 0.45], C);
  return (
    <AbsoluteFill style={{ background: fundoEscuro, alignItems: 'center', justifyContent: 'center', opacity: sai }}>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 30, color: '#C9CDD2', letterSpacing: 8, opacity: op2, marginBottom: 18 }}>FILE CLOSED</div>
      <div style={{ fontFamily: DISPLAY, fontSize: 170, color: AMARELO, letterSpacing: 4, transform: `scale(${0.9 + 0.1 * s})`, opacity: Math.min(1, s * 1.5), textShadow: '0 8px 0 rgba(0,0,0,.55)' }}>CLEARANCE REQUIRED</div>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 40, color: '#fff', letterSpacing: 3, opacity: op2, marginTop: 10 }}>WE GO WHERE THE RECORD GOES</div>
      <div style={{ fontFamily: COND, fontWeight: 700, fontSize: 52, color: TINTA, background: AMARELO, padding: '10px 44px', marginTop: 56, letterSpacing: 6, opacity: op3 }}>SUBSCRIBE</div>
    </AbsoluteFill>
  );
};
