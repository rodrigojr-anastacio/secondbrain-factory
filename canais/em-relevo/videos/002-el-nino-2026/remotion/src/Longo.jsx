// Longo 02 (Em Relevo, Super El Niño, 09/11/2026): cena 3D (shared/cena3d.js) + camadas 2D, tudo dirigido por shared/cues.json.
// Base: longo-01. Novos: termômetro, mostrador, 27 modelos, probabilidade por trimestre, ano seguinte, legenda do mapa,
// rótulos da régua de montanhas, data/legenda do relevo de calor, foto (imagem) no quadro de cortiça.
import React, { useLayoutEffect, useMemo, useState } from 'react';
import * as THREE from 'three';
import { useThree } from '@react-three/fiber';
import { ThreeCanvas } from '@remotion/three';
import { AbsoluteFill, Img, Loop, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig, delayRender, continueRender } from 'remotion';
import cues from '../../shared/cues.json';
import geo from '../../shared/geo.json';
import sst from '../../shared/sst_pacifico.json';
import { criarMundo, interpTabela } from '../../shared/cena3d.js';
import { numeroEm, capituloEm, legendaEm, pop, janela, clamp01, easeOut, fmt } from '../../shared/camadas.js';

const P = cues.paleta;
const MONO = 'PlexMono, monospace';
const W = 1920, H = 1080;

const fontes = [
  ['Anton', 'Anton-Regular.ttf', '400', 'normal'],
  ['PlexMono', 'IBMPlexMono-Medium.ttf', '500', 'normal'],
  ['PlexMono', 'IBMPlexMono-Bold.ttf', '700', 'normal'],
  ['Playfair', 'PlayfairDisplay-Italic.ttf', '400 900', 'italic'],
];
const useRecursos = () => {
  const [h] = useState(() => delayRender('fontes+texturas'));
  const [tex, setTex] = useState(null);
  useLayoutEffect(() => {
    const pf = Promise.all(fontes.map(([fam, arq, w, st]) => {
      const f = new FontFace(fam, `url(${staticFile('fonts/' + arq)})`, { weight: w, style: st });
      document.fonts.add(f);
      return f.load();
    }));
    const loader = new THREE.TextureLoader();
    const pt = Promise.all(cues.texturas.map((k) => new Promise((ok) => loader.load(staticFile(k), (t) => ok([k, t]), undefined, () => ok([k, null])))));
    Promise.all([pf, pt]).then(([, lista]) => { setTex(Object.fromEntries(lista)); continueRender(h); });
  }, [h]);
  return tex;
};

const Camera = ({ mundo }) => {
  const set = useThree((s) => s.set);
  const gl = useThree((s) => s.gl);
  useLayoutEffect(() => { mundo.configurarRenderer(gl); set({ camera: mundo.camera }); }, [mundo, set, gl]);
  return <primitive object={mundo.scene} />;
};


// ícones em SVG (as fontes não têm ✓ ✗ ▶ □ ⚠ ◀)
const Icone = ({ tipo, cor = '#2B2622', size = 24 }) => {
  const sw = size * 0.16;
  const d = {
    check: <path d="M4 13 L10 19 L21 5" fill="none" stroke={cor} strokeWidth={sw * 1.4} strokeLinecap="round" strokeLinejoin="round" />,
    cross: <path d="M5 5 L19 19 M19 5 L5 19" fill="none" stroke={cor} strokeWidth={sw * 1.4} strokeLinecap="round" />,
    play: <path d="M6 4 L20 12 L6 20 Z" fill={cor} />,
    left: <path d="M18 4 L4 12 L18 20 Z" fill={cor} />,
    box: <rect x="4" y="4" width="16" height="16" fill="none" stroke={cor} strokeWidth={sw} />,
    warn: <g><path d="M12 2 L23 21 L1 21 Z" fill={cor} /><path d="M12 8 L12 14 M12 17 L12 18" stroke="#fff" strokeWidth={2.4} strokeLinecap="round" /></g>,
  }[tipo];
  return <svg width={size} height={size} viewBox="0 0 24 24" style={{ display: 'inline-block', verticalAlign: 'middle', flex: 'none' }}>{d}</svg>;
};

const dentro = (lista, t) => lista.some(([a, b]) => t >= a && t <= b);
const transAtiva = (t) => cues.transicoes.filter((x) => Math.abs(t - x.t) <= x.dur);

// ---------------------------------------------------------------- número do topo
const Numero = ({ t }) => {
  const n = numeroEm(cues, t);
  if (!n) return null;
  const sN = pop(t, n.tNum, 0.4), sF = pop(t, n.tNum + 0.1, 0.35);
  const longo = String(n.texto).length > 7;
  return (
    <div style={{ position: 'absolute', top: 26, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ transform: `scale(${sN})`, color: P.coral, fontFamily: 'Anton', fontSize: longo ? 104 : 124, lineHeight: 1, letterSpacing: 1,
        textShadow: '0 4px 0 rgba(60,20,20,0.18), 0 10px 30px rgba(0,0,0,0.25)', display: 'flex', alignItems: 'baseline', gap: 14 }}>
        <span>{n.texto}</span>
        {n.unidade && <span style={{ fontSize: 50 }}>{n.unidade.toUpperCase()}</span>}
      </div>
      {n.faixa && <div style={{ marginTop: 10, transform: `scale(${sF})`, background: P.navy, color: P.branco, fontFamily: MONO, fontWeight: 700,
        fontSize: 23, letterSpacing: '0.12em', padding: '8px 22px', borderRadius: 6, boxShadow: '0 6px 16px rgba(0,0,0,0.25)', whiteSpace: 'nowrap' }}>{n.faixa}</div>}
    </div>
  );
};

const Capitulo = ({ t }) => {
  const c = capituloEm(cues, t);
  const p = clamp01((t - c.t) / 0.35);
  return (
    <div style={{ position: 'absolute', top: 40, left: 48, display: 'flex', alignItems: 'center', gap: 12, background: 'rgba(31,26,24,0.85)',
      padding: '9px 18px', borderRadius: 6, fontFamily: MONO, fontWeight: 700, fontSize: 20, letterSpacing: '0.16em', color: P.branco,
      transform: `translateX(${(1 - easeOut(p)) * -60}px)`, opacity: 0.2 + 0.8 * p }}>
      <span style={{ width: 11, height: 11, borderRadius: 6, background: P.coral, opacity: Math.floor(t * 2) % 2 ? 0.45 : 1 }} />
      {c.nome}
    </div>
  );
};

const Legenda = ({ t }) => {
  const l = legendaEm(cues, t);
  if (!l || !l.palavras.length) return null;
  const cursorOn = Math.floor(t * 3.2) % 2 === 0;
  return (
    <div style={{ position: 'absolute', bottom: 108, left: 0, width: '100%', display: 'flex', justifyContent: 'center' }}>
      <div style={{ maxWidth: 1500, background: P.branco, color: P.tinta, fontFamily: MONO, fontWeight: 500, fontSize: 38, lineHeight: 1.3,
        padding: '11px 24px', borderRadius: 4, boxShadow: '0 8px 24px rgba(0,0,0,0.3)', display: 'flex', flexWrap: 'wrap', columnGap: 15, alignItems: 'center',
        transform: `rotate(-0.6deg) scale(${0.92 + 0.08 * pop(t, l.tBloco, 0.25)})`, transformOrigin: 'left center' }}>
        {l.palavras.map((p, i) => (
          <span key={i} style={{ whiteSpace: 'nowrap' }}>
            <span style={{ borderBottom: p.destaque && p.completo ? `4px solid ${P.coral}` : '4px solid transparent' }}>{p.texto}</span>
            {i === l.palavras.length - 1 && <span style={{ display: 'inline-block', width: 14, height: 36, background: P.coral, marginLeft: 4, verticalAlign: 'middle', opacity: cursorOn ? 1 : 0 }} />}
          </span>
        ))}
      </div>
    </div>
  );
};

const Fontes = ({ t }) => {
  let f = cues.fontes[0];
  for (const x of cues.fontes) if (x.t <= t) f = x;
  return (
    <div style={{ position: 'absolute', bottom: 30, left: '50%', transform: 'translateX(-50%)', whiteSpace: 'nowrap', background: 'rgba(31,26,24,0.82)', color: '#E9DCC3',
      fontFamily: MONO, fontWeight: 500, fontSize: 15, letterSpacing: '0.1em', padding: '7px 16px', borderRadius: 4, opacity: 0.5 + 0.5 * clamp01((t - f.t) / 0.5) }}>
      {f.texto}
    </div>
  );
};

// ---------------------------------------------------------------- etiquetas do mapa e dos pinos
const ESTILO_ROT = {
  mapa: (s) => ({ color: 'rgba(43,38,34,0.6)', fontWeight: 700, fontSize: s, letterSpacing: '0.3em' }),
  mapa_grande: (s) => ({ color: 'rgba(43,58,30,0.75)', fontWeight: 700, fontSize: s * 2, letterSpacing: '0.4em' }),
  corredor: (s) => ({ color: P.branco, background: P.coral, fontWeight: 700, fontSize: s * 1.15, letterSpacing: '0.14em', padding: '6px 14px', borderRadius: 4 }),
  quente: (s) => ({ color: P.branco, background: '#C9612A', fontWeight: 700, fontSize: s * 1.1, letterSpacing: '0.1em', padding: '6px 14px', borderRadius: 4 }),
  fria: (s) => ({ color: P.branco, background: '#3D6A9E', fontWeight: 700, fontSize: s * 1.1, letterSpacing: '0.1em', padding: '6px 14px', borderRadius: 4 }),
  seta: (s) => ({ color: P.branco, background: P.navy, fontWeight: 700, fontSize: s * 1.1, letterSpacing: '0.1em', padding: '6px 14px', borderRadius: 4 }),
};
const Etiquetas = ({ t, proj }) => (
  <>
    {proj.rotulos.map((r, i) => {
      const a = janela(t, r.t0, r.t1, 0.4, 0.4);
      if (!r.ok || a <= 0) return null;
      const plano = r.tipo === 'mapa' || r.tipo === 'mapa_grande';
      return (
        <div key={i} style={{ position: 'absolute', left: r.x, top: r.y, transform: `translate(-50%,-50%) scale(${plano ? 1 : a})`, fontFamily: MONO,
          whiteSpace: 'nowrap', opacity: plano ? Math.min(1, a) : 1, boxShadow: plano ? 'none' : '0 6px 14px rgba(0,0,0,0.3)', ...ESTILO_ROT[r.tipo](19) }}>{r.nome}</div>
      );
    })}
    {cues.pinos.map((p, i) => {
      const q = proj.pinos[i];
      const s = janela(t, p.t + 0.35, p.ate, 0.35, 0.3);
      if (!q.ok || s <= 0 || p.pequeno) return null;
      return (
        <div key={p.id} style={{ position: 'absolute', left: q.x + 14, top: q.y - 14, transform: `translateY(-100%) scale(${s})`, transformOrigin: 'left bottom',
          background: P.navy, color: P.branco, fontFamily: MONO, padding: '6px 13px 7px', borderRadius: 4, boxShadow: '0 6px 14px rgba(0,0,0,0.3)',
          borderLeft: `5px solid ${p.cor === '#1F2A44' ? '#C9A46A' : P.coral}`, whiteSpace: 'nowrap' }}>
          <div style={{ fontWeight: 700, fontSize: 22, letterSpacing: '0.08em' }}>{p.nome}</div>
          {p.sub && <div style={{ fontWeight: 500, fontSize: 16, letterSpacing: '0.12em', opacity: 0.85 }}>{p.sub}</div>}
        </div>
      );
    })}
  </>
);

// ---------------------------------------------------------------- mídia real dentro do nosso quadro
const FORMATOS = {
  pol: { w: 560, ar: 0.75 }, mon: { w: 660, ar: 0.5625 }, cel: { w: 300, ar: 16 / 9 }, grande: { w: 1080, ar: 0.444 },
};
const Midia = ({ c, t, proj, fps }) => {
  const a = janela(t, c.t0, c.t1, 0.45, 0.35);
  if (a <= 0) return null;
  const F = FORMATOS[c.fmt] || FORMATOS.pol;
  const Wq = F.w, img = Wq - (c.fmt === 'cel' ? 24 : 32), ih = Math.round(img * F.ar);
  const total = ih + (c.fmt === 'cel' ? 70 : 110);
  const x = c.lado === 'esq' ? 70 : c.lado === 'centro' ? (W - Wq) / 2 : W - 70 - Wq;
  const y = c.lado === 'centro' ? 200 : Math.max(215, Math.min(250, 880 - total));
  const rot0 = c.lado === 'esq' ? -2.2 : c.lado === 'centro' ? -0.8 : 2.0;
  const giro = rot0 + 4 * (1 - clamp01((t - c.t0) / 0.6)) * Math.sin((t - c.t0) * 9);
  const pin = c.pino ? proj.pinos.find((p) => p.id === c.pino) : null;
  const fio = clamp01((t - c.t0 - 0.2) / 0.5);
  const tx = x + Wq / 2, ty = y + 10;
  const media = c.tipo === 'video' ? (
    <Sequence from={Math.round(c.t0 * fps)} layout="none">
      <OffthreadVideo src={staticFile(c.src)} muted playbackRate={c.rate || 1} style={{ width: img, height: ih, objectFit: 'cover' }} />
    </Sequence>
  ) : <Img src={staticFile(c.src)} style={{ width: img, height: ih, objectFit: 'cover', transform: `scale(${1.04 + 0.025 * (t - c.t0)})` }} />;
  const moldura = c.fmt === 'cel'
    ? { background: '#16181c', padding: '34px 12px 36px', borderRadius: 34, boxShadow: '0 18px 40px rgba(0,0,0,0.45)' }
    : c.fmt === 'mon'
      ? { background: '#22252a', padding: '16px 16px 0', borderRadius: 10, boxShadow: '0 18px 40px rgba(0,0,0,0.45)' }
      : { background: '#FBF8F1', padding: '16px 16px 0', borderRadius: 3, boxShadow: '0 18px 40px rgba(0,0,0,0.4)' };
  const corTxt = c.fmt === 'pol' || c.fmt === 'grande' ? P.tinta : '#ECE6DA', corCred = c.fmt === 'pol' || c.fmt === 'grande' ? '#6b625a' : '#A9A196';
  return (
    <>
      {pin && pin.ok && (
        <svg style={{ position: 'absolute', left: 0, top: 0, width: W, height: H, opacity: Math.min(1, a) }}>
          <line x1={tx} y1={ty} x2={tx + (pin.x - tx) * fio} y2={ty + (pin.y - ty) * fio} stroke="#D8404B" strokeWidth={4} strokeLinecap="round" />
          {fio >= 1 && <circle cx={pin.x} cy={pin.y} r={7} fill="#D8404B" />}
        </svg>
      )}
      <div style={{ position: 'absolute', left: x, top: y, width: Wq, ...moldura, transform: `rotate(${giro}deg) scale(${a})`, transformOrigin: '50% 0%' }}>
        <div style={{ width: img, height: ih, overflow: 'hidden', background: '#222', borderRadius: c.fmt === 'cel' ? 8 : 0, position: 'relative' }}>
          {media}
          {c.fmt === 'mon' && <div style={{ position: 'absolute', top: 12, left: 14, display: 'flex', alignItems: 'center', gap: 8, fontFamily: MONO, fontWeight: 700, fontSize: 16, color: '#fff',
            textShadow: '0 1px 3px #000' }}><span style={{ width: 11, height: 11, borderRadius: 6, background: '#E8505B', opacity: Math.floor(t * 2) % 2 ? 0.3 : 1 }} />CÂMERA</div>}
        </div>
        {c.fmt === 'cel' ? (
          <div style={{ position: 'absolute', left: 0, right: 0, bottom: -64, textAlign: 'center' }}>
            <div style={{ display: 'inline-block', background: '#FBF8F1', padding: '6px 12px', fontFamily: MONO, fontWeight: 700, fontSize: 15, color: P.tinta, boxShadow: '0 6px 14px rgba(0,0,0,0.3)' }}>{c.legenda}</div>
            <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 12, color: '#F3EEE3', marginTop: 5, textShadow: '0 1px 3px #000', whiteSpace: 'nowrap' }}>{c.credito}</div>
          </div>
        ) : (
          <>
            <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: Math.min(25, Wq * 0.042), letterSpacing: '0.08em', color: corTxt, padding: '12px 4px 2px' }}>{c.legenda}</div>
            <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: Math.min(17, Wq * 0.029), letterSpacing: '0.06em', color: corCred, padding: '0 4px 14px' }}>{c.credito}</div>
          </>
        )}
        {c.fmt !== 'cel' && c.fmt !== 'mon' && <div style={{ position: 'absolute', left: Wq / 2 - 16, top: -10, width: 32, height: 32, borderRadius: 16, background: 'radial-gradient(circle at 35% 35%, #ff8a8f, #C9303B 60%)', boxShadow: '0 4px 8px rgba(0,0,0,0.4)' }} />}
      </div>
    </>
  );
};

// ---------------------------------------------------------------- pergunta, cartões, manchetes, caixas
const Pergunta = ({ t }) => {
  const g = cues.pergunta;
  const a = janela(t, g.t0, g.t1, 0.4, 0.4);
  if (a <= 0) return null;
  const n = Math.round(clamp01((t - g.t0) / 4.2) * g.texto.length);
  return (
    <div style={{ position: 'absolute', top: 300, left: 260, width: 1400, transform: `scale(${a})`, opacity: Math.min(1, a * 1.5) }}>
      <div style={{ display: 'inline-block', background: P.coral, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.2em', padding: '8px 18px', borderRadius: 4, marginBottom: 18 }}>A PERGUNTA</div>
      <div style={{ background: P.branco, color: P.tinta, fontFamily: 'Anton', fontSize: 58, lineHeight: 1.12, padding: '26px 32px', borderRadius: 4, boxShadow: '0 20px 50px rgba(0,0,0,0.45)', transform: 'rotate(-0.8deg)', textTransform: 'uppercase' }}>
        {g.texto.slice(0, n)}<span style={{ color: P.coral }}>{n < g.texto.length ? '▌' : ''}</span>
      </div>
    </div>
  );
};
const Carimbo = ({ texto, t, t0, size = 92 }) => {
  if (t < t0) return null;
  const p = clamp01((t - t0) / 0.22);
  return (
    <div style={{ position: 'absolute', right: -20, bottom: -50, transform: `rotate(-9deg) scale(${2.2 - 1.2 * easeOut(p)})`, opacity: p, border: `7px solid ${P.coral}`, color: P.coral,
      fontFamily: 'Anton', fontSize: size, padding: '0 26px', borderRadius: 8, background: 'rgba(251,248,241,0.85)', letterSpacing: '0.04em', whiteSpace: 'nowrap' }}>{texto}</div>
  );
};
const Cartao = ({ c, t }) => {
  const a = janela(t, c.t0, c.t1, 0.4, 0.4);
  if (a <= 0) return null;
  const n = Math.round(clamp01((t - c.t0) / Math.min(3.5, 0.05 * c.texto.length + 0.6)) * c.texto.length);
  return (
    <div style={{ position: 'absolute', top: c.top, left: 140, width: 1060, transform: `scale(${a})`, opacity: Math.min(1, a * 1.5), transformOrigin: 'left center' }}>
      <div style={{ display: 'inline-block', background: P.coral, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 22, letterSpacing: '0.2em', padding: '7px 16px', borderRadius: 4, marginBottom: 14 }}>{c.rotulo}</div>
      <div style={{ position: 'relative', background: P.branco, color: P.tinta, fontFamily: 'Anton', fontSize: c.texto.length > 40 ? 46 : 64, lineHeight: 1.12, padding: '24px 30px', borderRadius: 4, boxShadow: '0 20px 50px rgba(0,0,0,0.45)', transform: 'rotate(-0.8deg)', textTransform: 'uppercase' }}>
        {c.texto.slice(0, n)}<span style={{ color: P.coral }}>{n < c.texto.length ? '▌' : ''}</span>
        {c.carimbo && <Carimbo texto={c.carimbo.texto} t={t} t0={c.carimbo.t} size={c.carimbo.texto.length > 6 ? 58 : 92} />}
      </div>
    </div>
  );
};
const Manchete = ({ m, t }) => {
  const a = janela(t, m.t0, m.t1, 0.45, 0.35);
  if (a <= 0) return null;
  const [antes, depois] = m.texto.split(m.destaque);
  const sub = clamp01((t - m.t0 - 0.9) / 0.6);
  return (
    <div style={{ position: 'absolute', left: m.lado === 'dir' ? 1180 : 80, top: 330, width: 660, transform: `rotate(-1.6deg) scale(${a})`, background: '#F3EEE3',
      padding: '22px 28px 26px', boxShadow: '0 14px 36px rgba(0,0,0,0.38)', clipPath: 'polygon(0 3%, 4% 0, 30% 2%, 58% 0, 100% 2%, 99% 60%, 100% 97%, 70% 100%, 35% 98%, 2% 100%, 0 70%)' }}>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 17, letterSpacing: '0.16em', color: P.coral, marginBottom: 10 }}>{m.veiculo}</div>
      <div style={{ fontFamily: 'Playfair', fontStyle: 'italic', fontWeight: 600, fontSize: 38, lineHeight: 1.18, color: P.tinta }}>
        {antes}
        <span style={{ backgroundImage: `linear-gradient(${P.coral}, ${P.coral})`, backgroundRepeat: 'no-repeat', backgroundPosition: '0 92%', backgroundSize: `${sub * 100}% 6px` }}>{m.destaque}</span>
        {depois}
      </div>
    </div>
  );
};
const Caixas = ({ t }) => {
  const cx = cues.caixas;
  if (t < cx.itens[0].t) return null;
  let e = null;
  for (const s of cx.estados) if (s.t <= t) e = s;
  if (!e || e.modo === 'oculto') return null;
  const grande = e.modo === 'grande' || e.modo === 'final';
  const primeira = cx.estados[0] === e;
  return (
    <div style={{ position: 'absolute', top: grande ? (e.modo === 'final' ? 600 : 640) : 40, left: grande ? 160 : 1390, width: grande ? 1600 : undefined,
      display: 'flex', flexDirection: grande ? 'row' : 'column', gap: grande ? 18 : 8, opacity: grande ? 1 : clamp01((t - e.t) / 0.4) }}>
      {cx.itens.map((it, i) => {
        const s = primeira ? pop(t, it.t, 0.4) : e.volta || e.modo === 'final' ? pop(t, e.t + 0.12 * i, 0.35) : 1;
        if (s <= 0) return null;
        const ativa = it.n === e.ativa, feita = e.feitas.includes(it.n);
        const sz = grande ? 28 : 18;
        return (
          <div key={it.n} style={{ flex: grande ? 1 : undefined, transform: `scale(${s * (ativa && grande ? 1.06 : 1)})`, transformOrigin: 'left center', display: 'flex', alignItems: 'center',
            gap: 14, background: ativa ? '#F6E7DF' : P.branco, border: `3px solid ${ativa ? P.coral : P.navy}`, borderRadius: 6, padding: grande ? '14px 18px' : '6px 12px',
            fontFamily: MONO, fontWeight: 700, fontSize: sz, color: P.tinta, boxShadow: '0 10px 24px rgba(0,0,0,0.3)', opacity: feita && !ativa && e.modo !== 'final' ? 0.6 : 1 }}>
            <span style={{ background: ativa ? P.coral : P.navy, color: P.branco, borderRadius: 4, padding: '2px 10px', fontFamily: 'Anton', fontWeight: 400, fontSize: sz * 1.15 }}>{it.n}</span>
            <span style={{ flex: 1 }}>{it.texto}</span>
            <span style={{ fontSize: sz * 0.8, color: ativa || feita ? P.coral : '#8a8178', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: 6 }}>{feita ? <Icone tipo="check" cor={P.coral} size={sz * 1.1} /> : ativa ? <><Icone tipo="play" cor={P.coral} size={sz * 0.8} />AGORA</> : <Icone tipo="box" cor="#8a8178" size={sz * 0.9} />}</span>
          </div>
        );
      })}
    </div>
  );
};

// ---------------------------------------------------------------- calendário dos 6 dias
const Calendario = ({ t }) => {
  const c = cues.calendario;
  if (!c) return null;
  const a = janela(t, c.t0, c.t1, 0.4, 0.4);
  if (a <= 0) return null;
  let foco = null; const n = {};
  for (const e of c.eventos) if (e.t <= t) { if (e.tipo === 'foco') foco = e.dia; else n[e.dia] = (n[e.dia] || 0) + 1; }
  const total = Object.values(n).reduce((x, y) => x + y, 0);
  return (
    <div style={{ position: 'absolute', left: 48, bottom: 200, transform: `scale(${a})`, transformOrigin: 'left bottom', display: 'flex', alignItems: 'stretch', gap: 6,
      background: 'rgba(31,26,24,0.85)', padding: 10, borderRadius: 8, boxShadow: '0 10px 24px rgba(0,0,0,0.35)' }}>
      <div style={{ fontFamily: MONO, fontWeight: 700, color: P.papel, fontSize: 16, letterSpacing: '0.14em', writingMode: 'vertical-rl', transform: 'rotate(180deg)', textAlign: 'center' }}>NOV 2026</div>
      {[1, ...c.dias].map((d) => {
        const on = d === foco, k = n[d] || 0;
        return (
          <div key={d} style={{ width: 62, background: on ? P.coral : d === 1 ? 'rgba(251,248,241,0.15)' : P.branco, borderRadius: 5, padding: '4px 0 6px', textAlign: 'center',
            transform: `scale(${on ? 1.08 : 1})`, opacity: d === 1 && !on ? 0.6 : 1 }}>
            <div style={{ fontFamily: 'Anton', fontSize: 30, color: on ? P.branco : P.tinta, lineHeight: 1.1 }}>{d}</div>
            <div style={{ height: 22, display: 'flex', justifyContent: 'center', gap: 1, flexWrap: 'wrap', fontSize: 16, lineHeight: 1 }}>
              {Array.from({ length: k }).map((_, i) => <span key={i} style={{ color: on ? P.branco : P.coral, fontFamily: 'Anton' }}>▼</span>)}
            </div>
          </div>
        );
      })}
      <div style={{ minWidth: 92, background: P.navy, borderRadius: 5, textAlign: 'center', padding: '4px 8px', color: P.branco }}>
        <div style={{ fontFamily: 'Anton', fontSize: 38, color: P.coral, lineHeight: 1 }}>{total}</div>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 12, letterSpacing: '0.1em' }}>TORNADOS</div>
      </div>
    </div>
  );
};

// ---------------------------------------------------------------- gráficos
const Painel = ({ a, children, left = 110, top = 220, w = 1100, titulo, fonte }) => (
  <div style={{ position: 'absolute', left, top, width: w, transform: `scale(${a})`, transformOrigin: 'left center', background: '#F3EEE3', borderRadius: 6,
    boxShadow: '0 20px 50px rgba(0,0,0,0.42)', padding: '24px 30px 20px', fontFamily: MONO, color: P.tinta }}>
    {titulo && <div style={{ fontWeight: 700, fontSize: 21, letterSpacing: '0.12em', color: P.navy, marginBottom: 16 }}>{titulo}</div>}
    {children}
    {fonte && <div style={{ fontWeight: 500, fontSize: 14, letterSpacing: '0.1em', color: '#7a7066', marginTop: 14 }}>FONTE: {fonte}</div>}
  </div>
);
const Grafico = ({ g, t }) => {
  const a = janela(t, g.t0, g.t1, 0.45, 0.35);
  if (a <= 0) return null;
  if (g.tipo === 'barras') return (
    <Painel a={a} titulo={g.titulo} fonte="PREVOTS · AGÊNCIA BRASIL · AGROLINK" w={980}>
      {g.barras.map(([rot, v, tb, tag], i) => {
        const p = easeOut(clamp01((t - tb + 0.3) / 1.0));
        return (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 16, margin: '14px 0' }}>
            <div style={{ width: 250, fontWeight: 700, fontSize: 22 }}>{rot}</div>
            <div style={{ flex: 1, height: 64, background: 'rgba(31,42,68,0.08)', borderRadius: 4, position: 'relative' }}>
              <div style={{ width: `${(v / g.max) * 100 * p}%`, height: '100%', background: i === 0 ? P.coral : P.navy, borderRadius: 4 }} />
              <div style={{ position: 'absolute', left: `calc(${(v / g.max) * 100 * p}% + 12px)`, top: 4, fontFamily: 'Anton', fontSize: 48, color: i === 0 ? P.coral : P.navy }}>{Math.round(v * p)}</div>
            </div>
            <div style={{ width: 120, fontWeight: 700, fontSize: 18, color: P.coral, opacity: p > 0.95 ? 1 : 0 }}>{tag}</div>
          </div>
        );
      })}
    </Painel>
  );
  if (g.tipo === 'x10') {
    const p = clamp01((t - g.t_n + 1.2) / 1.6), k = Math.max(1, Math.round(1 + 9 * easeOut(p)));
    return (
      <Painel a={a} titulo={g.rotulo} fonte={g.fonte} w={980}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 30 }}>
          <div style={{ fontFamily: 'Anton', fontSize: 170, color: P.coral, lineHeight: 1, width: 300 }}>×{k}</div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 90px)', gap: 12 }}>
            {Array.from({ length: 10 }).map((_, i) => (
              <div key={i} style={{ height: 70, borderRadius: 8, background: i < k ? P.navy : 'rgba(31,42,68,0.12)', display: 'flex', alignItems: 'center', justifyContent: 'center',
                color: P.branco, fontFamily: 'Anton', fontSize: 34, transform: `scale(${i < k ? 1 : 0.85})` }}>{i < k ? '▼' : ''}</div>
            ))}
          </div>
        </div>
        <div style={{ fontWeight: 700, fontSize: 20, marginTop: 14 }}>1980 → 2010 · BOA PARTE É DETECÇÃO: MAIS GENTE, MAIS CÂMERAS, MAIS REGISTRO</div>
      </Painel>
    );
  }
  if (g.tipo === 'placar') return (
    <div style={{ position: 'absolute', left: 120, top: 330, display: 'flex', gap: 18, transform: `scale(${a})`, transformOrigin: 'left center' }}>
      {g.itens.map(([uf, n, tt]) => {
        const s = pop(t, tt, 0.35);
        if (s <= 0) return null;
        return (
          <div key={uf} style={{ transform: `scale(${s})`, background: P.branco, borderRadius: 8, padding: '10px 24px', boxShadow: '0 12px 28px rgba(0,0,0,0.35)', textAlign: 'center', borderTop: `8px solid ${P.coral}` }}>
            <div style={{ fontFamily: 'Anton', fontSize: 84, color: P.coral, lineHeight: 1 }}>{n}</div>
            <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.12em', color: P.navy }}>{uf}</div>
          </div>
        );
      })}
    </div>
  );
  if (g.tipo === 'oni') {
    const xs = g.serie, n = xs.length, wv = 1040, hv = 380, max = 3.0, min = -2.0;
    const p = easeOut(clamp01((t - g.t0) / Math.max(1, g.t_fim - g.t0)));
    const zero = hv * (max / (max - min));
    return (
      <Painel a={a} titulo={g.titulo} fonte="NOAA/CPC · ONI (ANOMALIA TRIMESTRAL, MAIOR VALOR DO ANO)" w={1120}>
        <svg width={wv} height={hv + 40}>
          <line x1={0} x2={wv} y1={zero} y2={zero} stroke="#6b625a" strokeWidth={2} />
          <line x1={0} x2={wv} y1={hv * ((max - 2) / (max - min))} y2={hv * ((max - 2) / (max - min))} stroke={P.coral} strokeWidth={2} strokeDasharray="8 8" />
          <text x={wv - 4} y={hv * ((max - 2) / (max - min)) - 8} textAnchor="end" fontFamily="PlexMono" fontWeight={700} fontSize={18} fill={P.coral}>+2 °C · MUITO FORTE</text>
          {xs.map(([ano, v], i) => {
            if (i / n > p) return null;
            const bx = (i / n) * wv, bw = wv / n - 2, y = hv * ((max - v) / (max - min));
            const dest = g.destaques.includes(ano);
            return <rect key={ano} x={bx} width={bw} y={Math.min(y, zero)} height={Math.abs(zero - y)} fill={v > 0 ? (dest ? P.coral : '#D9A07A') : '#7FA2C9'} />;
          })}
          {g.destaques.map((ano) => {
            const i = xs.findIndex((x) => x[0] === ano); if (i < 0 || i / n > p) return null;
            const v = xs[i][1], bx = (i / n) * wv, y = hv * ((max - v) / (max - min));
            return <text key={ano} x={bx + 6} y={y - 10} textAnchor="middle" fontFamily="Anton" fontSize={ano === 2026 ? 34 : 24} fill={ano === 2026 ? P.coral : P.tinta}>{ano === 2026 ? '2026' : ano}</text>;
          })}
          {[1950, 1970, 1990, 2010].map((ano) => <text key={ano} x={((ano - 1950) / n) * wv} y={hv + 30} fontFamily="PlexMono" fontSize={16} fill="#6b625a">{ano}</text>)}
        </svg>
      </Painel>
    );
  }
  if (g.tipo === 'ciencia') return (
    <Painel a={a} titulo="O QUE A CIÊNCIA DIZ · E O QUE NÃO DIZ" fonte={g.fonte} w={1100} top={240}>
      {g.itens.map(([txt, ok, ti], i) => {
        const s = pop(t, ti, 0.35);
        if (s <= 0) return null;
        return (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 18, margin: '12px 0', transform: `scale(${s})`, transformOrigin: 'left center' }}>
            <div style={{ width: 62, height: 62, borderRadius: 31, background: ok ? '#3E8E5A' : P.coral, color: P.branco, fontFamily: 'Anton', fontSize: 40, display: 'flex', alignItems: 'center', justifyContent: 'center' }}><Icone tipo={ok ? 'check' : 'cross'} cor={P.branco} size={38} /></div>
            <div style={{ fontWeight: 700, fontSize: 27, textDecoration: ok ? 'none' : 'line-through', textDecorationColor: P.coral, textDecorationThickness: 4 }}>{txt}</div>
          </div>
        );
      })}
    </Painel>
  );
  if (g.tipo === 'meses') {
    const n = g.meses.length, wm = 1060 / n;
    return (
      <Painel a={a} w={1120} top={520} titulo="PRIMAVERA E VERÃO 2026/27 NO SUL" fonte="CLIMATEMPO · EPAGRI/CIRAM · INPE · NOAA/CPC">
        <div style={{ position: 'relative', height: 210 }}>
          {g.meses.map((m, i) => <div key={m} style={{ position: 'absolute', left: i * wm, top: 160, width: wm - 4, textAlign: 'center', fontWeight: 700, fontSize: 20, borderTop: '3px solid #6b625a', paddingTop: 6 }}>{m}</div>)}
          {g.marcas.map((mk, k) => {
            const p = easeOut(clamp01((t - mk.t) / 0.8));
            if (p <= 0) return null;
            return (
              <div key={k} style={{ position: 'absolute', left: mk.de * wm, top: 104 - k * 50, width: (mk.ate - mk.de + 1) * wm * p - 6, height: 42, background: mk.cor, borderRadius: 6, color: P.branco,
                fontWeight: 700, fontSize: 18, letterSpacing: '0.06em', display: 'flex', alignItems: 'center', paddingLeft: 12, whiteSpace: 'nowrap', overflow: 'hidden' }}>{mk.texto}</div>
            );
          })}
          {t >= g.hoje.t && (
            <div style={{ position: 'absolute', left: g.hoje.i * wm + wm / 2 - 3, top: -6, height: 170, width: 6, background: P.navy, transform: `scaleY(${easeOut(clamp01((t - g.hoje.t) / 0.4))})`, transformOrigin: 'bottom' }}>
              <div style={{ position: 'absolute', top: -34, left: -80, width: 166, textAlign: 'center', background: P.navy, color: P.branco, fontWeight: 700, fontSize: 16, padding: '4px 0', borderRadius: 4 }}>{g.hoje.texto}</div>
            </div>
          )}
        </div>
      </Painel>
    );
  }
  if (g.tipo === 'escala') {
    const maxV = 520;
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={1120} top={200}>
        {g.faixas.map(([cl, v0, v1], i) => {
          const p = easeOut(clamp01((t - g.t_barras - 0.25 * i) / 0.6));
          const marca = g.marcas.find((m) => m[0] === cl);
          const on = marca && t >= marca[2];
          return (
            <div key={cl} style={{ display: 'flex', alignItems: 'center', gap: 14, margin: '7px 0' }}>
              <div style={{ width: 70, fontFamily: 'Anton', fontSize: 40, color: on ? P.coral : P.navy }}>{cl}</div>
              <div style={{ flex: 1, height: 48, position: 'relative' }}>
                <div style={{ position: 'absolute', left: `${(v0 / maxV) * 100 * p}%`, width: `${((v1 - v0) / maxV) * 100 * p}%`, height: '100%', borderRadius: 4,
                  background: `rgba(232,80,91,${0.25 + 0.13 * i})`, outline: on ? `4px solid ${P.coral}` : 'none' }} />
                <div style={{ position: 'absolute', left: `calc(${(v1 / maxV) * 100 * p}% + 10px)`, top: 10, fontWeight: 700, fontSize: 21, whiteSpace: 'nowrap', opacity: p }}>{v0}–{v1} km/h</div>
              </div>
              <div style={{ width: 300, fontWeight: 700, fontSize: 18, color: P.coral, opacity: on ? 1 : 0, transform: `scale(${on ? pop(t, marca[2], 0.35) : 0})`, transformOrigin: 'left center' }}>{marca ? <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}><Icone tipo="left" cor={P.coral} size={18} />{marca[1]}</span> : ''}</div>
            </div>
          );
        })}
      </Painel>
    );
  }
  if (g.tipo === 'comparacao') {
    const sil = (a3, cor) => {
      const rs = geo.silhuetas[a3]; const xs = rs.flat().map((p) => p[0]), ys = rs.flat().map((p) => p[1]);
      const x0 = Math.min(...xs), y0 = Math.min(...ys), sw = Math.max(...xs) - x0, sh = Math.max(...ys) - y0, k = 150 / Math.max(sw, sh);
      return (
        <svg width={sw * k + 4} height={sh * k + 4}>
          {rs.map((r, i) => <path key={i} d={'M' + r.map((p) => `${((p[0] - x0) * k + 2).toFixed(1)},${((p[1] - y0) * k + 2).toFixed(1)}`).join('L') + 'Z'} fill={cor} stroke={P.tinta} strokeWidth={1.5} />)}
        </svg>
      );
    };
    // escala real: os dois países no mesmo k (área comparável)
    return (
      <Painel a={a} w={1090} top={200} titulo="BRASIL × ESTADOS UNIDOS" fonte="PREVOTS · SIMEPAR · NOAA/NSSL · NWS">
        <div style={{ display: 'flex', alignItems: 'flex-end', marginBottom: 10 }}>
          <div style={{ width: 360 }} />
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 12 }}>{sil('BRA', '#E9DCC3')}<span style={{ fontFamily: 'Anton', fontSize: 40, color: P.navy }}>BRASIL</span></div>
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', gap: 12 }}>{sil('USA', '#D9C6A0')}<span style={{ fontFamily: 'Anton', fontSize: 40, color: P.navy }}>EUA</span></div>
        </div>
        {g.linhas.map(([rot, vb, sb, vu, su, tl], i) => {
          const s = pop(t, tl, 0.35);
          if (s <= 0) return null;
          return (
            <div key={i} style={{ display: 'flex', alignItems: 'center', borderTop: '2px solid rgba(43,38,34,0.15)', padding: '10px 0', transform: `scale(${s})`, transformOrigin: 'left center' }}>
              <div style={{ width: 360, fontWeight: 700, fontSize: 22 }}>{rot}</div>
              <div style={{ flex: 1 }}><span style={{ fontFamily: 'Anton', fontSize: 52, color: P.coral }}>{vb}</span><div style={{ fontSize: 15, fontWeight: 700, color: '#6b625a' }}>{sb}</div></div>
              <div style={{ flex: 1 }}><span style={{ fontFamily: 'Anton', fontSize: 52, color: P.navy }}>{vu}</span><div style={{ fontSize: 15, fontWeight: 700, color: '#6b625a' }}>{su}</div></div>
            </div>
          );
        })}
        {t >= g.barras[2] && (
          <div style={{ marginTop: 10 }}>
            {[[g.barras[0], P.coral, 'RIO BONITO DO IGUAÇU'], [g.barras[1], P.navy, 'EL RENO']].map(([v, cor, nm]) => (
              <div key={nm} style={{ display: 'flex', alignItems: 'center', gap: 12, margin: '6px 0' }}>
                <div style={{ width: 360, fontWeight: 700, fontSize: 17 }}>LARGURA · {nm}</div>
                <div style={{ height: 26, width: (v / 4.2) * 640 * easeOut(clamp01((t - g.barras[2]) / 0.8)), background: cor, borderRadius: 4 }} />
                <div style={{ fontFamily: 'Anton', fontSize: 28, color: cor }}>{String(v).replace('.', ',')} KM</div>
              </div>
            ))}
          </div>
        )}
      </Painel>
    );
  }

  if (g.tipo === 'termometro') {
    const max = 2.6, hT = 520, val = 0.5 + 1.9 * easeOut(clamp01((t - g.t0) / Math.max(1, g.faixas[2][2] + 1 - g.t0)));
    const y = (v) => hT * (1 - v / max);
    const sup = clamp01((t - g.t_super) / 0.3);
    return (
      <div style={{ position: 'absolute', right: 560, top: 230, transform: `scale(${a})`, transformOrigin: 'right center', background: '#F3EEE3', borderRadius: 8, padding: '26px 30px 18px', boxShadow: '0 20px 50px rgba(0,0,0,0.42)', fontFamily: MONO, color: P.tinta, width: 560 }}>
        <div style={{ fontWeight: 700, fontSize: 20, letterSpacing: '0.12em', color: P.navy, marginBottom: 14 }}>NIÑO 3.4 · ACIMA DO NORMAL (°C)</div>
        <div style={{ position: 'relative', height: hT, display: 'flex' }}>
          <div style={{ position: 'relative', width: 70, height: hT, borderRadius: 35, background: 'rgba(31,42,68,0.1)', border: `4px solid ${P.navy}`, overflow: 'hidden' }}>
            <div style={{ position: 'absolute', bottom: 0, width: '100%', height: hT - y(val), background: `linear-gradient(0deg, #F2A07E, ${P.coral})` }} />
          </div>
          {g.faixas.map(([v, nome, tf], i) => {
            const on = t >= tf;
            return (
              <div key={i} style={{ position: 'absolute', left: 64, top: y(v) - 2, display: 'flex', alignItems: 'center', gap: 12, opacity: on ? 1 : 0.25 }}>
                <div style={{ width: 38, height: 4, background: P.navy }} />
                <div style={{ fontFamily: 'Anton', fontSize: 40, color: v >= 2 ? P.coral : P.navy, width: 70 }}>{String(v).replace('.', ',')}</div>
                <div style={{ fontWeight: 700, fontSize: 24, transform: `scale(${on ? pop(t, tf, 0.35) : 1})`, transformOrigin: 'left center' }}>{nome}</div>
              </div>
            );
          })}
          {sup > 0 && <div style={{ position: 'absolute', left: 250, top: y(2.35) - 34, fontFamily: 'Anton', fontSize: 64, color: P.coral, transform: `rotate(-6deg) scale(${pop(t, g.t_super, 0.35)})`, opacity: Math.floor(t * 3) % 2 ? 1 : 0.6 }}>“SUPER”?</div>}
        </div>
        <div style={{ fontWeight: 500, fontSize: 13, letterSpacing: '0.08em', color: '#7a7066', marginTop: 12 }}>FONTE: {g.fonte}</div>
      </div>
    );
  }
  if (g.tipo === 'mostrador') {
    const p = easeOut(clamp01((t - g.t_gira) / 1.4));
    const ang = (v) => Math.PI * (1 - v / 100);
    const pt = (v, r) => [260 + r * Math.cos(ang(v)), 260 - r * Math.sin(ang(v))];
    const arco = (v0, v1, r) => { const [x0, y0] = pt(v0, r), [x1, y1] = pt(v1, r); return `M${x0},${y0} A${r},${r} 0 0 1 ${x1},${y1}`; };
    const vAg = 76.5 * p, [ax, ay] = pt(vAg, 190);
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={640} left={1180} top={250}>
        <svg width={560} height={300}>
          <path d={arco(0, 100, 210)} stroke="rgba(31,42,68,0.15)" strokeWidth={42} fill="none" />
          <path d={arco(g.de, g.de + (g.ate - g.de) * p, 210)} stroke={P.coral} strokeWidth={42} fill="none" />
          <line x1={260} y1={260} x2={ax} y2={ay} stroke={P.navy} strokeWidth={8} strokeLinecap="round" />
          <circle cx={260} cy={260} r={16} fill={P.navy} />
          {[0, 50, 100].map((v) => { const [x, y] = pt(v, 250); return <text key={v} x={x} y={y + 6} textAnchor="middle" fontFamily="PlexMono" fontWeight={700} fontSize={20} fill="#6b625a">{v}%</text>; })}
        </svg>
        <div style={{ textAlign: 'center', fontFamily: 'Anton', fontSize: 92, color: P.coral, lineHeight: 1, marginTop: -40 }}>{Math.round(g.de * p)}–{Math.round(g.ate * p)}%</div>
      </Painel>
    );
  }
  if (g.tipo === 'modelos') {
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={700} left={1130} top={260}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(9, 60px)', gap: 12 }}>
          {Array.from({ length: g.n }).map((_, i) => {
            const on = t >= g.t_acende + 0.05 * i;
            return <div key={i} style={{ height: 60, borderRadius: 30, background: on ? P.coral : 'rgba(31,42,68,0.15)', transform: `scale(${on ? pop(t, g.t_acende + 0.05 * i, 0.3) : 0.8})`, display: 'flex', alignItems: 'center', justifyContent: 'center', color: P.branco, fontFamily: 'Anton', fontSize: 24 }}>{on ? i + 1 : ''}</div>;
          })}
        </div>
      </Painel>
    );
  }
  if (g.tipo === 'prob') {
    const n = g.tri.length, wm = 1240 / n, hb = 300;
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={1340} left={290} top={330}>
        <div style={{ display: 'flex', gap: 26, marginBottom: 12 }}>{g.legendas.map(([cor, txt, tl]) => t >= tl && <div key={txt} style={{ display: 'flex', alignItems: 'center', gap: 8, fontWeight: 700, fontSize: 19 }}><span style={{ width: 22, height: 22, background: cor, borderRadius: 4 }} />{txt}</div>)}</div>
        <div style={{ position: 'relative', height: hb + 50 }}>
          {g.pico && t >= g.pico.t && <div style={{ position: 'absolute', left: g.pico.de * wm, width: (g.pico.ate - g.pico.de) * wm, top: 0, height: hb, background: 'rgba(232,80,91,0.12)', border: `3px dashed ${P.coral}`, borderRadius: 6, opacity: clamp01((t - g.pico.t) / 0.4) }}>
            <div style={{ position: 'absolute', bottom: 8, width: '100%', textAlign: 'center', fontWeight: 700, fontSize: 18, color: P.navy, background: 'rgba(251,248,241,0.85)' }}>{g.pico.texto}</div></div>}
          {g.barras.map((b, k) => {
            const p = easeOut(clamp01((t - b.t) / 0.7)); if (p <= 0) return null;
            return (
              <div key={k} style={{ position: 'absolute', left: b.i * wm + wm * 0.2, width: wm * 0.6, bottom: 50, height: (hb - 40) * b.v / 100 * p, background: b.cor, borderRadius: '6px 6px 0 0' }}>
                <div style={{ position: 'absolute', top: -46, width: '100%', textAlign: 'center', fontFamily: 'Anton', fontSize: 38, color: b.cor }}>{Math.round(b.v * p)}%</div>
              </div>
            );
          })}
          {g.tri.map((tr, i) => <div key={tr} style={{ position: 'absolute', left: i * wm, bottom: 0, width: wm, textAlign: 'center', fontWeight: 700, fontSize: 20, borderTop: '3px solid #6b625a', paddingTop: 8 }}>{tr}</div>)}
          {t >= g.hoje.t && <div style={{ position: 'absolute', left: g.hoje.i * wm + 6, bottom: 46, background: P.navy, color: P.branco, fontWeight: 700, fontSize: 15, padding: '4px 10px', borderRadius: 4, transform: `scale(${pop(t, g.hoje.t, 0.3)})`, transformOrigin: 'left bottom', whiteSpace: 'nowrap' }}>{g.hoje.texto}</div>}
        </div>
      </Painel>
    );
  }
  if (g.tipo === 'depois') return (
    <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={620} left={1220} top={240}>
      {g.itens.map(([ano, v, tl]) => {
        const p = easeOut(clamp01((t - tl) / 0.6));
        return (
          <div key={ano} style={{ display: 'flex', alignItems: 'center', gap: 16, margin: '12px 0', opacity: p > 0 ? 1 : 0.2 }}>
            <div style={{ width: 90, fontFamily: 'Anton', fontSize: 40 }}>{ano}</div>
            <div style={{ height: 46, width: 220 * (-v / 1.5) * p, background: '#3D6A9E', borderRadius: 4 }} />
            <div style={{ fontFamily: 'Anton', fontSize: 36, color: '#3D6A9E' }}>{p > 0.9 ? String(v).replace('.', ',') : ''}</div>
          </div>
        );
      })}
      <div style={{ fontWeight: 700, fontSize: 18, color: '#3D6A9E', marginTop: 6 }}>NEGATIVO = LA NIÑA (OU QUASE)</div>
    </Painel>
  );
  if (g.tipo === 'legenda') return (
    <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={600} left={1250} top={560}>
      {g.itens.map(([cor, txt, tl]) => {
        const s2 = pop(t, tl, 0.35); if (s2 <= 0) return null;
        return <div key={txt} style={{ display: 'flex', alignItems: 'center', gap: 14, margin: '8px 0', transform: `scale(${s2})`, transformOrigin: 'left center' }}><span style={{ width: 34, height: 34, background: cor, borderRadius: 4, flex: 'none' }} /><span style={{ fontWeight: 700, fontSize: 21 }}>{txt}</span></div>;
      })}
    </Painel>
  );
  return null;
};
const Checklist = ({ c, t }) => {
  const a = janela(t, c.t0, c.t1, 0.4, 0.4);
  if (a <= 0) return null;
  return (
    <Painel a={a} titulo={c.titulo} w={760} top={250}>
      {c.itens.map(([txt, ti], i) => {
        const s = pop(t, ti, 0.35);
        return (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 16, margin: '10px 0', opacity: s > 0 ? 1 : 0.35 }}>
            <div style={{ width: 46, height: 46, border: `4px solid ${P.navy}`, borderRadius: 6, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Anton', fontSize: 38, color: P.coral }}>
              <span style={{ transform: `scale(${s})`, display: 'flex' }}><Icone tipo="check" cor={P.coral} size={36} /></span></div>
            <div style={{ fontWeight: 700, fontSize: 28 }}>{txt}</div>
          </div>
        );
      })}
    </Painel>
  );
};

// ---------------------------------------------------------------- quadro de cortiça (O QUE FAZER)
const IconeFunil = ({ cor = P.tinta }) => (
  <svg width="180" height="200" viewBox="0 0 180 200">
    <path d="M10 20 Q90 0 170 20 Q140 40 130 60 Q110 80 104 110 Q98 140 92 190 Q84 140 78 110 Q70 80 50 60 Q40 40 10 20Z" fill="none" stroke={cor} strokeWidth={7} strokeLinejoin="round" />
    {[40, 70, 100, 130].map((y, i) => <path key={y} d={`M${40 + i * 12} ${y} Q90 ${y + 10} ${140 - i * 12} ${y}`} fill="none" stroke={cor} strokeWidth={4} />)}
  </svg>
);
const Cortica = ({ t, fps }) => {
  const c = cues.cortica;
  if (t < c.t0 || t > c.t1 + 1.5) return null;
  const tz = cues.transicoes.find((x) => x.tipo === 'zoomout');
  const z = tz ? easeOut(clamp01((t - tz.t) / tz.dur)) : 0;
  return (
    <AbsoluteFill style={{ transform: `scale(${1 - 0.75 * z}) rotate(${-4 * z}deg)`, opacity: 1 - clamp01((z - 0.6) / 0.4), boxShadow: z > 0 ? '0 30px 80px rgba(0,0,0,0.6)' : 'none' }}>
      <AbsoluteFill style={{ background: 'radial-gradient(circle at 30% 30%, #C79766 0%, #B07F52 45%, #95683F 100%)', border: '26px solid #6B4A2E' }}>
        <AbsoluteFill style={{ backgroundImage: 'radial-gradient(rgba(60,35,15,0.35) 1.2px, transparent 1.6px), radial-gradient(rgba(255,230,190,0.18) 1px, transparent 1.4px)', backgroundSize: '9px 9px, 13px 13px', backgroundPosition: '0 0, 5px 7px' }} />
      </AbsoluteFill>
      {c.itens.map((it, i) => {
        const s = it.tipo === 'postit' && it.icone ? (t < it.t ? 0 : 1) * (it.troca ? 1 : 1) : pop(t, it.t, 0.4);
        if (s <= 0) return null;
        if (it.icone && cues.cortica.itens.some((o) => o.titulo === 'NUNCA' && t >= o.t)) return null;
        const tachinha = <div style={{ position: 'absolute', left: '50%', top: -12, marginLeft: -14, width: 28, height: 28, borderRadius: 14, background: 'radial-gradient(circle at 35% 35%, #ff8a8f, #C9303B 60%)', boxShadow: '0 4px 8px rgba(0,0,0,0.45)' }} />;
        const base = { position: 'absolute', left: it.x, top: it.y, width: it.w, transform: `rotate(${it.rot}deg) scale(${s})`, boxShadow: '0 14px 28px rgba(0,0,0,0.4)' };
        if (it.tipo === 'titulo') return (
          <div key={i} style={{ ...base, background: P.branco, padding: '10px 26px', textAlign: 'center', fontFamily: 'Anton', fontSize: 76, color: P.coral }}>{it.texto}{tachinha}</div>
        );
        if (it.tipo === 'postit') return (
          <div key={i} style={{ ...base, minHeight: it.w * 0.9, background: it.cor, padding: '30px 24px 20px', fontFamily: MONO, color: it.claro ? P.branco : P.tinta }}>
            {it.icone ? <div style={{ display: 'flex', justifyContent: 'center' }}><IconeFunil /></div> : <>
              <div style={{ fontFamily: 'Anton', fontSize: 44, lineHeight: 1.05, marginBottom: 10 }}>{it.titulo}</div>
              <div style={{ fontWeight: 700, fontSize: 27, lineHeight: 1.3, whiteSpace: 'pre-line' }}>{it.texto}</div>
            </>}
            {tachinha}
          </div>
        );
        if (it.tipo === 'celular') {
          const [tit, msg] = it.texto.split('\n');
          return (
            <div key={i} style={{ ...base, height: it.w * 1.9, background: '#16181c', borderRadius: 34, padding: '40px 12px' }}>
              <div style={{ height: '100%', borderRadius: 10, background: 'linear-gradient(#2a3448, #1a2030)', padding: 12 }}>
                <div style={{ marginTop: 40, background: '#F3EEE3', borderRadius: 12, padding: 14, transform: `translateY(${(1 - easeOut(clamp01((t - it.t - 0.4) / 0.4))) * -40}px)`, opacity: clamp01((t - it.t - 0.4) / 0.3) }}>
                  <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 17, color: P.coral, letterSpacing: '0.08em', display: 'flex', alignItems: 'center', gap: 6 }}><Icone tipo="warn" cor={P.coral} size={18} />{tit}</div>
                  <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 17, color: P.tinta, marginTop: 6, lineHeight: 1.3 }}>{msg}</div>
                </div>
                <div style={{ fontFamily: MONO, fontSize: 12, color: '#9aa3b5', marginTop: 12, textAlign: 'center' }}>ILUSTRAÇÃO</div>
              </div>
            </div>
          );
        }
        if (it.tipo === 'fotoimg') {
          const iw = it.w - 28, ih2 = Math.round(iw * 0.75);
          return (
            <div key={i} style={{ ...base, background: '#FBF8F1', padding: '14px 14px 0' }}>
              <div style={{ width: iw, height: ih2, overflow: 'hidden', background: '#222' }}><Img src={staticFile(it.src)} style={{ width: iw, height: ih2, objectFit: 'cover' }} /></div>
              <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 15, color: P.tinta, padding: '8px 2px 0' }}>{it.legenda}</div>
              <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 11, color: '#6b625a', padding: '0 2px 10px' }}>{it.credito}</div>
              {tachinha}
            </div>
          );
        }
        if (it.tipo === 'foto') {
          const iw = it.w - 28, ih2 = Math.round(iw * 0.75);
          return (
            <div key={i} style={{ ...base, background: '#FBF8F1', padding: '14px 14px 0' }}>
              <div style={{ width: iw, height: ih2, overflow: 'hidden', background: '#222' }}>
                <Sequence from={Math.round(it.t * fps)} layout="none"><Loop durationInFrames={150} layout="none"><OffthreadVideo src={staticFile(it.src)} muted style={{ width: iw, height: ih2, objectFit: 'cover' }} /></Loop></Sequence>
              </div>
              <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 17, color: P.tinta, padding: '8px 2px 0' }}>{it.legenda}</div>
              <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 12, color: '#6b625a', padding: '0 2px 10px' }}>VÍDEO: {it.credito}</div>
              {tachinha}
            </div>
          );
        }
        return null;
      })}
    </AbsoluteFill>
  );
};


// ---------------------------------------------------------------- rótulos da régua de montanhas e data do relevo de calor
const RotulosMontanhas = ({ t, proj }) => (proj.montanhas || []).map((m, i) => {
  if (!m.vis || !m.topo.ok || m.o < 0.5) return null;
  const mt = cues.montanhas[i]; const eh = mt.nome === '2026';
  return (
    <React.Fragment key={i}>
      <div style={{ position: 'absolute', left: m.topo.x, top: m.topo.y, transform: 'translate(-50%,-100%)', fontFamily: 'Anton', fontSize: eh ? 50 : 40, color: eh ? P.coral : P.tinta, textShadow: '0 2px 0 rgba(255,255,255,0.6)' }}>{m.h.toFixed(2).replace('.', ',')}</div>
      <div style={{ position: 'absolute', left: m.base.x, top: m.base.y, transform: 'translate(-50%,0)', background: eh ? P.coral : P.navy, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 22, padding: '4px 12px', borderRadius: 4, whiteSpace: 'nowrap' }}>{mt.nome}</div>
    </React.Fragment>
  );
});
const MESES = ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ'];
const DataRelevo = ({ t }) => {
  const r = cues.relevos.find((x) => x.mostra_data && interpTabela(x.op, t) > 0.5);
  if (!r) return null;
  const i = Math.round(Math.max(0, Math.min(cues.sst_datas.length - 1, interpTabela(r.idx, t))));
  const [y, m, d] = cues.sst_datas[i].split('-');
  const PAL = 'linear-gradient(90deg, #3D6A9E 0%, #C9D6D8 25%, #E8C9A8 33%, #EE9A82 42%, #E8505B 53%, #B23545 70%, #6E1A28 100%)';
  return (
    <div style={{ position: 'absolute', left: 60, bottom: 200, background: 'rgba(31,26,24,0.85)', borderRadius: 8, padding: '12px 18px', fontFamily: MONO, color: P.branco, width: 430 }}>
      <div style={{ fontWeight: 700, fontSize: 15, letterSpacing: '0.12em', color: '#E9DCC3' }}>TEMPERATURA DO MAR ACIMA DO NORMAL</div>
      <div style={{ fontFamily: 'Anton', fontSize: 52, lineHeight: 1.1 }}>{d} {MESES[+m - 1]} {y}</div>
      <div style={{ height: 14, borderRadius: 3, background: PAL, marginTop: 6 }} />
      <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 700, fontSize: 14, marginTop: 4 }}><span>−2</span><span>0</span><span>+2</span><span>+4</span><span>+6 °C</span></div>
      <div style={{ fontWeight: 500, fontSize: 12, color: '#B9AE9C', marginTop: 4 }}>DADOS: NOAA OISST · RELEVO: EM RELEVO</div>
    </div>
  );
};

// ---------------------------------------------------------------- transições (camadas por cima)
const Transicoes = ({ t }) => (
  <>
    {transAtiva(t).map((x, i) => {
      const u = (t - x.t) / x.dur; // -1..1, 0 = instante do corte
      const pico = 1 - Math.abs(u);
      if (x.tipo === 'nuvem') return (
        <AbsoluteFill key={i} style={{ opacity: clamp01(pico * 1.6), background: 'radial-gradient(circle at 50% 50%, rgba(250,248,244,1) 0%, rgba(232,228,220,0.97) 40%, rgba(200,195,188,0.9) 75%, rgba(150,145,140,0.85) 100%)',
          transform: `scale(${1 + 0.4 * (u + 1)})` }}>
          {[0, 1, 2, 3, 4, 5].map((k) => <div key={k} style={{ position: 'absolute', left: `${(k * 23) % 90}%`, top: `${(k * 37) % 80}%`, width: 700, height: 500, borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(255,255,255,0.9), rgba(255,255,255,0))', transform: `translate(-50%,-50%) scale(${1 + 0.6 * (u + 1)})` }} />)}
        </AbsoluteFill>
      );
      if (x.tipo === 'whip' || x.tipo === 'whip_v') {
        const v = x.tipo === 'whip_v';
        return <AbsoluteFill key={i} style={{ opacity: clamp01(pico * 1.4) * 0.85, backgroundImage: `repeating-linear-gradient(${v ? 0 : 90}deg, rgba(255,250,240,0.0) 0px, rgba(255,250,240,0.55) 3px, rgba(255,250,240,0) 14px, rgba(60,45,30,0.25) 22px, rgba(255,250,240,0) 34px)`,
          transform: v ? `translateY(${u * 300}px)` : `translateX(${u * 400}px)` }} />;
      }
      if (x.tipo === 'corte') return u >= 0 ? <AbsoluteFill key={i} style={{ background: '#FFF8EC', opacity: clamp01(1 - u * 3) * 0.9 }} /> : null;
      if (x.tipo === 'match') {
        const r = u < 0 ? 40 + 260 * easeOut(clamp01(u + 1)) : 300 + 200 * u;
        return <div key={i} style={{ position: 'absolute', left: W / 2 - r, top: H / 2 - r, width: r * 2, height: r * 2, borderRadius: '50%', border: `14px solid ${P.coral}`,
          background: u < 0 ? 'rgba(232,80,91,0.18)' : 'rgba(232,80,91,0.08)', opacity: u < 0 ? clamp01((u + 1) * 2) : clamp01(1 - u * 1.3) }} />;
      }
      if (x.tipo === 'match_funil') return u >= 0 && u < 0.35 ? <AbsoluteFill key={i} style={{ background: '#FFF8EC', opacity: (0.35 - u) * 2 }} /> : null;
      if (x.tipo === 'luz') return <AbsoluteFill key={i} style={{ background: 'radial-gradient(ellipse at 50% 50%, rgba(10,15,40,0) 30%, rgba(10,15,40,0.55) 100%)', opacity: clamp01(pico * 1.2) }} />;
      return null;
    })}
  </>
);

const Cta = ({ t }) => {
  const c = cues.cta;
  const a = pop(t, c.t0, 0.45);
  if (a <= 0) return null;
  const b = pop(t, c.t_inscreve, 0.4);
  return (
    <div style={{ position: 'absolute', top: 300, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22, transform: `scale(${a})` }}>
      <div style={{ fontFamily: 'Anton', fontSize: 70, color: P.coral, lineHeight: 1.05, background: P.branco, padding: '14px 36px 18px', maxWidth: 1500, textAlign: 'center', transform: 'rotate(-1.5deg)', boxShadow: '0 16px 40px rgba(0,0,0,0.4)' }}>{c.texto}</div>
      {b > 0 && <div style={{ transform: `scale(${b})`, background: P.coral, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 34, letterSpacing: '0.14em', padding: '14px 34px', borderRadius: 8, boxShadow: '0 10px 26px rgba(0,0,0,0.35)' }}>
        {c.inscreve}</div>}
    </div>
  );
};

export const Longo = ({ tempo, soMapa = false }) => {
  const tex = useRecursos();
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = tempo ?? frame / fps;
  const mundo = useMemo(() => (tex ? criarMundo(THREE, { ...cues, largura: width, altura: height }, geo, tex, { fov: 32, sombra: 1024, sst }) : null), [tex, width, height]);
  if (!mundo) return null;
  const cobre = dentro(cues.cobre3d, t);
  let proj = { pinos: cues.pinos.map((p) => ({ id: p.id, x: 0, y: 0, ok: false })), rotulos: [] };
  if (!cobre) { mundo.update(t); proj = mundo.projetar(width, height); }
  // filtro do canvas: desfoque (rack focus), chicote (whip) e "arquivo" (sépia)
  let blur = 10 * interpTabela(cues.desfoque, t);
  for (const x of transAtiva(t)) if (x.tipo === 'whip' || x.tipo === 'whip_v') blur = Math.max(blur, 18 * clamp01((1 - Math.abs((t - x.t) / x.dur)) * 1.3));
  const sep = interpTabela(cues.arquivo, t);
  const filtro = [blur > 0.2 ? `blur(${blur.toFixed(1)}px)` : '', sep > 0.01 ? `sepia(${(0.7 * sep).toFixed(2)}) contrast(${(1 + 0.08 * sep).toFixed(2)})` : ''].join(' ').trim();
  const fundoCena = !cobre ? (
    <AbsoluteFill style={{ filter: filtro || undefined }}>
      <ThreeCanvas width={width} height={height} shadows flat gl={{ antialias: true, preserveDrawingBuffer: true }}>
        <Camera mundo={mundo} />
      </ThreeCanvas>
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(40,25,10,0.38) 100%)' }} />
    </AbsoluteFill>
  ) : null;
  if (soMapa) return <AbsoluteFill style={{ background: '#B9A47F' }}>{fundoCena}</AbsoluteFill>;
  return (
    <AbsoluteFill style={{ background: '#B9A47F' }}>
      {fundoCena}
      {!cobre && <Etiquetas t={t} proj={proj} />}
      {!cobre && <RotulosMontanhas t={t} proj={proj} />}
      {!cobre && <DataRelevo t={t} />}
      {cues.midia.map((c) => <Midia key={c.id + c.t0} c={c} t={t} proj={proj} fps={fps} />)}
      {cues.graficos.map((g, i) => <Grafico key={i} g={g} t={t} />)}
      {cues.checklists.map((c, i) => <Checklist key={i} c={c} t={t} />)}
      {cues.manchetes.map((m, i) => <Manchete key={i} m={m} t={t} />)}
      {cues.cartoes.map((c, i) => <Cartao key={i} c={c} t={t} />)}
      <Numero t={t} />
      <Calendario t={t} />
      <Pergunta t={t} />
      <Cortica t={t} fps={fps} />
      <Caixas t={t} />
      <Cta t={t} />
      <Transicoes t={t} />
      <Capitulo t={t} />
      <Legenda t={t} />
      <Fontes t={t} />
    </AbsoluteFill>
  );
};
