// Piloto clima pt (08/11/2026): mesma cena 3D e camadas em dois formatos. formato = 'v' (Shorts 1080×1920) | 'h' (longo 1920×1080).
import React, { useLayoutEffect, useMemo, useState } from 'react';
import * as THREE from 'three';
import { useThree } from '@react-three/fiber';
import { ThreeCanvas } from '@remotion/three';
import { AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig, delayRender, continueRender } from 'remotion';
import cuesBase from '../../shared/cues.json';
import geo from '../../shared/geo.json';
import { criarMundo } from '../../shared/cena3d.js';
import { numeroEm, capituloEm, legendaEm, pop, janela, clamp01 } from '../../shared/camadas.js';

const P = cuesBase.paleta;
const MONO = 'PlexMono, monospace';

// layout por formato (px). V: deixa ~15% livres embaixo e à direita (UI do Shorts)
const LAYOUTS = {
  v: {
    fov: 40, dist: 1.32, sombra: 1024,
    num: { top: 150, size: 168, faixa: 30 }, cap: { top: 62, left: 48, size: 22 },
    pol: { left: 44, top: 440, w: 520, rot: -2.2 },
    leg: { top: 1330, left: 48, maxW: 830, size: 44 },
    fontes: { top: 1568, left: 48, maxW: 840, size: 15 },
    etq: { size: 25, sub: 17 }, rot: 19,
    perg: { top: 560, left: 70, w: 860, size: 56 },
    cx: { top: 1020, left: 70, w: 820, size: 31, dir: 'column' }, cxc: { top: 150, left: 48, size: 20 },
    man: { left: 70, top: 1010, w: 760, size: 40 },
    cta: { top: 760 },
  },
  h: {
    fov: 32, dist: 1.0, sombra: 1024,
    num: { top: 30, size: 128, faixa: 26 }, cap: { top: 40, left: 48, size: 20 },
    pol: { right: 70, top: 200, w: 560, rot: 2.0 },
    leg: { bottom: 112, left: 0, maxW: 1500, size: 40, centro: true },
    fontes: { bottom: 30, left: 0, maxW: 1800, size: 15, centro: true },
    etq: { size: 23, sub: 16 }, rot: 19,
    perg: { top: 300, left: 260, w: 1400, size: 58 },
    cx: { top: 640, left: 160, w: 1600, size: 28, dir: 'row' }, cxc: { top: 40, left: 1390, size: 18 },
    man: { left: 80, top: 330, w: 640, size: 38 },
    cta: { top: 380 },
  },
};

const fontes = [
  ['Anton', 'Anton-Regular.ttf', '400', 'normal'],
  ['PlexMono', 'IBMPlexMono-Medium.ttf', '500', 'normal'],
  ['PlexMono', 'IBMPlexMono-Bold.ttf', '700', 'normal'],
  ['Playfair', 'PlayfairDisplay-Italic.ttf', '400 900', 'italic'],
];
const useRecursos = () => {
  const [h] = useState(() => delayRender('fontes+textura'));
  const [tex, setTex] = useState(null);
  useLayoutEffect(() => {
    const pf = Promise.all(fontes.map(([fam, arq, w, st]) => {
      const f = new FontFace(fam, `url(${staticFile('fonts/' + arq)})`, { weight: w, style: st });
      document.fonts.add(f);
      return f.load();
    }));
    const pt = new Promise((ok) => new THREE.TextureLoader().load(staticFile('img/goes-ir.png'), ok));
    Promise.all([pf, pt]).then(([, t]) => { setTex(t); continueRender(h); });
  }, [h]);
  return tex;
};

const Camera = ({ mundo }) => {
  const set = useThree((s) => s.set);
  const gl = useThree((s) => s.gl);
  useLayoutEffect(() => {
    mundo.configurarRenderer(gl);
    set({ camera: mundo.camera });
  }, [mundo, set, gl]);
  return <primitive object={mundo.scene} />;
};

const Numero = ({ t, L }) => {
  const n = numeroEm(cuesBase, t);
  if (!n) return null;
  const sN = pop(t, n.tNum, 0.4), sF = pop(t, n.tNum + 0.1, 0.35);
  return (
    <div style={{ position: 'absolute', top: L.num.top, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ transform: `scale(${sN})`, color: P.coral, fontFamily: 'Anton', fontSize: L.num.size, lineHeight: 1, letterSpacing: 1,
        textShadow: '0 4px 0 rgba(60,20,20,0.18), 0 10px 30px rgba(0,0,0,0.25)', display: 'flex', alignItems: 'baseline', gap: 14 }}>
        <span>{n.texto}</span>
        {n.unidade && <span style={{ fontSize: L.num.size * 0.42 }}>{n.unidade.toUpperCase()}</span>}
      </div>
      <div style={{ marginTop: 12, transform: `scale(${sF})`, background: P.navy, color: P.branco, fontFamily: MONO, fontWeight: 700,
        fontSize: L.num.faixa, letterSpacing: '0.12em', padding: '9px 24px', borderRadius: 6, boxShadow: '0 6px 16px rgba(0,0,0,0.25)', whiteSpace: 'nowrap' }}>
        {n.faixa}
      </div>
    </div>
  );
};

const Capitulo = ({ t, L }) => {
  const c = capituloEm(cuesBase, t);
  const p = clamp01((t - c.t) / 0.3);
  return (
    <div style={{ position: 'absolute', top: L.cap.top, left: L.cap.left, display: 'flex', alignItems: 'center', gap: 12, background: 'rgba(31,26,24,0.85)',
      padding: '9px 18px', borderRadius: 6, fontFamily: MONO, fontWeight: 700, fontSize: L.cap.size, letterSpacing: '0.16em', color: P.branco,
      transform: `translateX(${(1 - p) * -30}px)`, opacity: 0.3 + 0.7 * p }}>
      <span style={{ width: 11, height: 11, borderRadius: 6, background: P.coral, opacity: Math.floor(t * 2) % 2 ? 0.45 : 1 }} />
      {c.nome}
    </div>
  );
};

const Legenda = ({ t, L }) => {
  const l = legendaEm(cuesBase, t);
  if (!l || !l.palavras.length) return null;
  const cursorOn = Math.floor(t * 3.2) % 2 === 0;
  const pos = L.leg.centro ? { bottom: L.leg.bottom, left: 0, width: '100%', justifyContent: 'center' } : { top: L.leg.top, left: L.leg.left, width: L.leg.maxW };
  return (
    <div style={{ position: 'absolute', display: 'flex', ...pos }}>
      <div style={{ maxWidth: L.leg.maxW, background: P.branco, color: P.tinta, fontFamily: MONO, fontWeight: 500, fontSize: L.leg.size, lineHeight: 1.3,
        padding: '12px 24px', borderRadius: 4, boxShadow: '0 8px 24px rgba(0,0,0,0.3)', display: 'flex', flexWrap: 'wrap', columnGap: 16, alignItems: 'center',
        transform: `rotate(-0.6deg) scale(${0.92 + 0.08 * pop(t, l.tBloco, 0.25)})`, transformOrigin: 'left center' }}>
        {l.palavras.map((p, i) => (
          <span key={i} style={{ whiteSpace: 'nowrap' }}>
            <span style={{ borderBottom: p.destaque && p.completo ? `4px solid ${P.coral}` : '4px solid transparent' }}>{p.texto}</span>
            {i === l.palavras.length - 1 && <span style={{ display: 'inline-block', width: 15, height: L.leg.size * 0.95, background: P.coral, marginLeft: 4, verticalAlign: 'middle', opacity: cursorOn ? 1 : 0 }} />}
          </span>
        ))}
      </div>
    </div>
  );
};

const ESTILO_ROT = {
  mapa: (s) => ({ color: 'rgba(43,38,34,0.55)', fontWeight: 700, fontSize: s, letterSpacing: '0.3em' }),
  corredor: (s) => ({ color: P.branco, background: P.coral, fontWeight: 700, fontSize: s * 1.15, letterSpacing: '0.14em', padding: '6px 14px', borderRadius: 4 }),
  quente: (s) => ({ color: P.branco, background: '#C9612A', fontWeight: 700, fontSize: s * 1.1, letterSpacing: '0.1em', padding: '6px 14px', borderRadius: 4 }),
  fria: (s) => ({ color: P.branco, background: '#3D6A9E', fontWeight: 700, fontSize: s * 1.1, letterSpacing: '0.1em', padding: '6px 14px', borderRadius: 4 }),
  seta: (s) => ({ color: P.branco, background: P.navy, fontWeight: 700, fontSize: s * 1.1, letterSpacing: '0.1em', padding: '6px 14px', borderRadius: 4 }),
};

const Etiquetas = ({ t, proj, L }) => (
  <>
    {proj.rotulos.map((r) => {
      const a = janela(t, r.t0, r.t1, 0.4, 0.4);
      if (!r.ok || a <= 0) return null;
      return (
        <div key={r.nome} style={{ position: 'absolute', left: r.x, top: r.y, transform: `translate(-50%,-50%) scale(${r.tipo === 'mapa' ? 1 : a})`, fontFamily: MONO,
          whiteSpace: 'nowrap', opacity: r.tipo === 'mapa' ? Math.min(1, a) * clamp01(t / 1.0) : 1, boxShadow: r.tipo === 'mapa' ? 'none' : '0 6px 14px rgba(0,0,0,0.3)',
          ...ESTILO_ROT[r.tipo](L.rot) }}>{r.nome}</div>
      );
    })}
    {cuesBase.pinos.map((p, i) => {
      const q = proj.pinos[i];
      const s = janela(t, p.t + 0.35, cuesBase.rotulos_pinos_ate, 0.35, 0.3);
      if (!q.ok || s <= 0 || p.pequeno) return null;
      const k = 1;
      return (
        <div key={p.id} style={{ position: 'absolute', left: q.x + 14, top: q.y - 14, transform: `translateY(-100%) scale(${s})`, transformOrigin: 'left bottom',
          background: P.navy, color: P.branco, fontFamily: MONO, padding: '6px 13px 7px', borderRadius: 4, boxShadow: '0 6px 14px rgba(0,0,0,0.3)',
          borderLeft: `5px solid ${P.coral}`, whiteSpace: 'nowrap' }}>
          <div style={{ fontWeight: 700, fontSize: L.etq.size * k, letterSpacing: '0.08em' }}>{p.nome}</div>
          {p.sub && <div style={{ fontWeight: 500, fontSize: L.etq.sub, letterSpacing: '0.12em', opacity: 0.85 }}>{p.sub}</div>}
        </div>
      );
    })}
  </>
);

// trecho real dentro do nosso quadro: polaroid com tachinha + fio vermelho até o pino + crédito
const Polaroid = ({ c, t, proj, L, fps }) => {
  const a = janela(t, c.t0, c.t1, 0.45, 0.35);
  if (a <= 0) return null;
  const W = L.pol.w, img = W - 32, ih = Math.round(img * 0.75);
  const x = L.pol.left !== undefined ? L.pol.left : 1920 - L.pol.right - W;
  const y = L.pol.top;
  const giro = L.pol.rot + 4 * (1 - clamp01((t - c.t0) / 0.6)) * Math.sin((t - c.t0) * 9);
  const pin = c.pino ? proj.pinos.find((p) => p.id === c.pino) : null;
  const fio = clamp01((t - c.t0 - 0.2) / 0.5);
  const tx = x + W / 2, ty = y + 10;
  return (
    <>
      {pin && pin.ok && (
        <svg style={{ position: 'absolute', left: 0, top: 0, width: '100%', height: '100%', opacity: Math.min(1, a) }}>
          <line x1={tx} y1={ty} x2={tx + (pin.x - tx) * fio} y2={ty + (pin.y - ty) * fio} stroke="#D8404B" strokeWidth={4} strokeLinecap="round" />
          {fio >= 1 && <circle cx={pin.x} cy={pin.y} r={7} fill="#D8404B" />}
        </svg>
      )}
      <div style={{ position: 'absolute', left: x, top: y, width: W, background: '#FBF8F1', padding: '16px 16px 0', borderRadius: 3,
        boxShadow: '0 18px 40px rgba(0,0,0,0.4)', transform: `rotate(${giro}deg) scale(${a})`, transformOrigin: '50% 0%' }}>
        <div style={{ width: img, height: ih, overflow: 'hidden', background: '#222' }}>
          {c.src ? (
            <Sequence from={Math.round(c.t0 * fps)} layout="none">
              <OffthreadVideo src={staticFile(c.src)} muted style={{ width: img, height: ih, objectFit: 'cover' }} />
            </Sequence>
          ) : (
            <Img src={staticFile(c.img)} style={{ width: img, height: ih, objectFit: 'cover', transform: `scale(${1.05 + 0.04 * (t - c.t0)})` }} />
          )}
        </div>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: W * 0.045, letterSpacing: '0.08em', color: P.tinta, padding: '12px 4px 2px' }}>{c.legenda}</div>
        <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: W * 0.03, letterSpacing: '0.06em', color: '#6b625a', padding: '0 4px 14px' }}>{c.credito}</div>
        <div style={{ position: 'absolute', left: W / 2 - 16, top: -10, width: 32, height: 32, borderRadius: 16, background: 'radial-gradient(circle at 35% 35%, #ff8a8f, #C9303B 60%)',
          boxShadow: '0 4px 8px rgba(0,0,0,0.4)' }} />
      </div>
    </>
  );
};

const Pergunta = ({ t, L }) => {
  const g = cuesBase.pergunta;
  const a = janela(t, g.t0, g.t1, 0.4, 0.4);
  if (a <= 0) return null;
  const n = Math.round(clamp01((t - g.t0) / 4.2) * g.texto.length);
  return (
    <div style={{ position: 'absolute', top: L.perg.top, left: L.perg.left, width: L.perg.w, transform: `scale(${a})`, opacity: Math.min(1, a * 1.5) }}>
      <div style={{ display: 'inline-block', background: P.coral, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: L.perg.size * 0.42, letterSpacing: '0.2em',
        padding: '8px 18px', borderRadius: 4, marginBottom: 18 }}>A PERGUNTA</div>
      <div style={{ background: P.branco, color: P.tinta, fontFamily: 'Anton', fontSize: L.perg.size, lineHeight: 1.12, padding: '26px 32px', borderRadius: 4,
        boxShadow: '0 20px 50px rgba(0,0,0,0.45)', transform: 'rotate(-0.8deg)', textTransform: 'uppercase' }}>
        {g.texto.slice(0, n)}<span style={{ color: P.coral }}>{n < g.texto.length ? '▌' : ''}</span>
      </div>
    </div>
  );
};

const Caixas = ({ t, L }) => {
  const cx = cuesBase.caixas;
  if (t < cx.itens[0].t) return null;
  const compacta = (t >= cx.compacta && t < cx.volta);
  if (t >= cx.some && t < cx.volta) return null;
  const final = t >= cx.volta;
  const fadeC = compacta ? clamp01((t - cx.compacta) / 0.4) : 1;
  const st = compacta ? L.cxc : L.cx;
  return (
    <div style={{ position: 'absolute', top: st.top, left: st.left, width: compacta ? undefined : st.w, display: 'flex', flexDirection: compacta ? 'column' : st.dir,
      gap: compacta ? 8 : 18, opacity: fadeC }}>
      {cx.itens.map((it, i) => {
        const s = final ? pop(t, cx.volta + 0.15 * i, 0.35) : compacta ? 1 : pop(t, it.t, 0.4);
        const aberta = it.n === 1 && t >= cx.compacta;
        const tranca = final && it.n > 1;
        if (s <= 0) return null;
        return (
          <div key={it.n} style={{ flex: compacta || st.dir === 'column' ? undefined : 1, transform: `scale(${s})`, transformOrigin: 'left center', display: 'flex', alignItems: 'center',
            gap: 14, background: aberta ? '#F6E7DF' : P.branco, border: `3px solid ${aberta ? P.coral : P.navy}`, borderRadius: 6, padding: compacta ? '6px 12px' : '14px 18px',
            fontFamily: MONO, fontWeight: 700, fontSize: st.size, color: P.tinta, boxShadow: '0 10px 24px rgba(0,0,0,0.3)', opacity: final && it.n === 1 ? 0.55 : 1 }}>
            <span style={{ background: aberta ? P.coral : P.navy, color: P.branco, borderRadius: 4, padding: '2px 10px', fontFamily: 'Anton', fontWeight: 400, fontSize: st.size * 1.15 }}>{it.n}</span>
            <span style={{ flex: 1, textDecoration: final && it.n === 1 ? 'line-through' : 'none' }}>{it.texto}</span>
            <span style={{ fontSize: st.size * 0.8, color: aberta ? P.coral : tranca ? P.coral : '#8a8178', whiteSpace: 'nowrap' }}>
              {aberta ? '✓ AGORA' : tranca ? '→ PARTE 2' : '□'}
            </span>
          </div>
        );
      })}
    </div>
  );
};

const Manchete = ({ t, L }) => {
  const m = cuesBase.manchete;
  const a = janela(t, m.t0, m.t1, 0.45, 0.35);
  if (a <= 0) return null;
  const [antes, depois] = m.texto.split(m.destaque);
  const sub = clamp01((t - m.t0 - 0.9) / 0.6);
  return (
    <div style={{ position: 'absolute', left: L.man.left, top: L.man.top, width: L.man.w, transform: `rotate(-1.6deg) scale(${a})`, background: '#F3EEE3',
      padding: '22px 28px 26px', boxShadow: '0 14px 36px rgba(0,0,0,0.38)', clipPath: 'polygon(0 3%, 4% 0, 30% 2%, 58% 0, 100% 2%, 99% 60%, 100% 97%, 70% 100%, 35% 98%, 2% 100%, 0 70%)' }}>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: L.man.size * 0.45, letterSpacing: '0.18em', color: P.coral, marginBottom: 10 }}>{m.veiculo}</div>
      <div style={{ fontFamily: 'Playfair', fontStyle: 'italic', fontWeight: 600, fontSize: L.man.size, lineHeight: 1.18, color: P.tinta }}>
        {antes}
        <span style={{ backgroundImage: `linear-gradient(${P.coral}, ${P.coral})`, backgroundRepeat: 'no-repeat', backgroundPosition: '0 92%', backgroundSize: `${sub * 100}% 6px` }}>{m.destaque}</span>
        {depois}
      </div>
    </div>
  );
};

const Cta = ({ t, L, v }) => {
  const a = pop(t, cuesBase.cta.t0, 0.45);
  if (a <= 0) return null;
  return (
    <div style={{ position: 'absolute', top: L.cta.top, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16, transform: `scale(${a})` }}>
      <div style={{ fontFamily: 'Anton', fontSize: v ? 120 : 110, color: P.coral, lineHeight: 1, textShadow: '0 6px 24px rgba(0,0,0,0.35)' }}>PARTE 2</div>
      <div style={{ background: P.navy, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: v ? 34 : 30, letterSpacing: '0.14em', padding: '10px 26px', borderRadius: 6 }}>
        {v ? 'SEGUE O CANAL PRA NÃO PERDER' : 'O RISCO DE VOLTAR · ATÉ ONDE PODE CHEGAR'}
      </div>
    </div>
  );
};

const Fontes = ({ L }) => {
  const pos = L.fontes.centro ? { bottom: L.fontes.bottom, left: '50%', transform: 'translateX(-50%)', whiteSpace: 'nowrap' } : { top: L.fontes.top, left: L.fontes.left, maxWidth: L.fontes.maxW };
  return (
    <div style={{ position: 'absolute', ...pos, background: 'rgba(31,26,24,0.82)', color: '#E9DCC3', fontFamily: MONO, fontWeight: 500, fontSize: L.fontes.size,
      letterSpacing: '0.1em', padding: '7px 16px', borderRadius: 4, lineHeight: 1.4 }}>
      {cuesBase.fontes}
    </div>
  );
};

const CapaTitulo = () => (
  <>
    <div style={{ position: 'absolute', top: 170, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 18 }}>
      <div style={{ fontFamily: 'Anton', fontSize: 230, color: P.coral, lineHeight: 0.95, textShadow: '0 8px 30px rgba(0,0,0,0.35)' }}>7 TORNADOS</div>
      <div style={{ background: P.navy, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 52, letterSpacing: '0.12em', padding: '12px 30px', borderRadius: 6 }}>EM 6 DIAS NO SUL</div>
    </div>
    <div style={{ position: 'absolute', top: 1300, width: '100%', display: 'flex', justifyContent: 'center' }}>
      <div style={{ background: P.branco, color: P.tinta, fontFamily: 'Anton', fontSize: 120, padding: '10px 40px', transform: 'rotate(-2deg)', boxShadow: '0 16px 40px rgba(0,0,0,0.4)' }}>
        POR QUÊ<span style={{ color: P.coral }}>?</span>
      </div>
    </div>
  </>
);

export const Piloto = ({ formato, capa = false }) => {
  const tex = useRecursos();
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / fps;
  const L = LAYOUTS[formato];
  const v = formato === 'v';
  const mundo = useMemo(() => (tex ? criarMundo(THREE, { ...cuesBase, largura: width, altura: height }, geo,
    { fov: L.fov, dist: L.dist, sombra: L.sombra, texturaSat: tex, offV: formato === 'v' }) : null), [tex, width, height]);
  if (!mundo) return null;
  mundo.update(t);
  const proj = mundo.projetar(width, height);
  const escurece = cuesBase.luz ? 0 : 0;
  return (
    <AbsoluteFill style={{ background: '#B9A47F' }}>
      <ThreeCanvas width={width} height={height} shadows flat gl={{ antialias: true, preserveDrawingBuffer: true }}>
        <Camera mundo={mundo} />
      </ThreeCanvas>
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(40,25,10,0.38) 100%)', opacity: 1 + escurece }} />
      <Etiquetas t={t} proj={proj} L={L} />
      {cuesBase.clipes.map((c) => <Polaroid key={c.id} c={c} t={t} proj={proj} L={L} fps={fps} />)}
      {!capa && <Numero t={t} L={L} />}
      <Pergunta t={t} L={L} />
      <Caixas t={t} L={L} />
      <Manchete t={t} L={L} />
      <Cta t={t} L={L} v={v} />
      {!capa && <Capitulo t={t} L={L} />}
      {!capa && <Legenda t={t} L={L} />}
      {!capa && <Fontes L={L} />}
      {capa && <CapaTitulo />}
      <Audio src={staticFile('narracao.wav')} />
    </AbsoluteFill>
  );
};
