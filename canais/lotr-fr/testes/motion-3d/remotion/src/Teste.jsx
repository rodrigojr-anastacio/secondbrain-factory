import React, { useLayoutEffect, useMemo, useState } from 'react';
import * as THREE from 'three';
import { useThree } from '@react-three/fiber';
import { ThreeCanvas } from '@remotion/three';
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig, delayRender, continueRender } from 'remotion';
import cues from '../../shared/cues.json';
import { criarMundo } from '../../shared/cena3d.js';
import { numeroEm, capituloEm, legendaEm, pop } from '../../shared/camadas.js';

const P = cues.paleta;
const MONO = 'PlexMono, monospace';

// fontes locais (OFL) carregadas antes do 1º frame
const fontes = [
  ['Anton', 'Anton-Regular.ttf', '400'],
  ['PlexMono', 'IBMPlexMono-Medium.ttf', '500'],
  ['PlexMono', 'IBMPlexMono-Bold.ttf', '700'],
];
const useFontes = () => {
  const [h] = useState(() => delayRender('fontes'));
  useLayoutEffect(() => {
    Promise.all(fontes.map(([fam, arq, w]) => {
      const f = new FontFace(fam, `url(${staticFile('fonts/' + arq)})`, { weight: w });
      document.fonts.add(f);
      return f.load();
    })).then(() => continueRender(h));
  }, [h]);
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

const Numero = ({ t }) => {
  const n = numeroEm(cues, t);
  if (!n) return null;
  const sN = pop(t, n.tNum, 0.4), sF = pop(t, n.tFaixa - 0.05, 0.35);
  return (
    <div style={{ position: 'absolute', top: 38, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ transform: `scale(${sN})`, color: P.coral, fontFamily: 'Anton', fontSize: 150, lineHeight: 1, letterSpacing: 1,
        textShadow: '0 4px 0 rgba(60,20,20,0.18), 0 10px 30px rgba(0,0,0,0.18)', display: 'flex', alignItems: 'baseline', gap: 14 }}>
        {n.aprox && <span style={{ fontSize: 96 }}>≈</span>}
        <span>{n.texto}</span>
        {n.unidade && <span style={{ fontSize: 72 }}>{n.unidade.toUpperCase()}</span>}
      </div>
      <div style={{ marginTop: 14, transform: `scale(${sF})`, background: P.navy, color: P.branco, fontFamily: MONO, fontWeight: 700,
        fontSize: 30, letterSpacing: '0.14em', padding: '10px 26px', borderRadius: 6, boxShadow: '0 6px 16px rgba(0,0,0,0.25)' }}>
        {n.faixa}
      </div>
    </div>
  );
};

const Capitulo = ({ t }) => {
  const c = capituloEm(cues, t);
  const p = Math.min(1, Math.max(0, (t - c.t) / 0.3));
  return (
    <div style={{ position: 'absolute', top: 42, left: 48, display: 'flex', alignItems: 'center', gap: 12, background: 'rgba(31,26,24,0.82)',
      padding: '9px 18px', borderRadius: 6, fontFamily: MONO, fontWeight: 700, fontSize: 20, letterSpacing: '0.16em', color: P.branco,
      transform: `translateX(${(1 - p) * -30}px)`, opacity: 0.3 + 0.7 * p }}>
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
    <div style={{ position: 'absolute', bottom: 150, width: '100%', display: 'flex', justifyContent: 'center' }}>
      <div style={{ background: P.branco, color: P.tinta, fontFamily: MONO, fontWeight: 500, fontSize: 44, padding: '12px 26px',
        borderRadius: 4, boxShadow: '0 8px 24px rgba(0,0,0,0.28)', display: 'flex', gap: 18, alignItems: 'center',
        transform: `rotate(-0.6deg) scale(${0.9 + 0.1 * pop(t, l.tBloco, 0.25)})` }}>
        {l.palavras.map((p, i) => (
          <span key={i} style={{ borderBottom: p.destaque && p.completo ? `4px solid ${P.coral}` : '4px solid transparent' }}>{p.texto}</span>
        ))}
        <span style={{ width: 16, height: 46, background: P.coral, marginLeft: -12, opacity: cursorOn ? 1 : 0 }} />
      </div>
    </div>
  );
};

const Etiquetas = ({ t, proj }) => (
  <>
    {proj.rotulos.map((r) => r.ok && (
      <div key={r.nome} style={{ position: 'absolute', left: r.x, top: r.y, transform: 'translate(-50%,-50%)', fontFamily: MONO, fontWeight: 700,
        fontSize: 21, letterSpacing: '0.32em', color: 'rgba(43,38,34,0.55)', whiteSpace: 'nowrap', opacity: Math.min(1, t / 1.2) }}>{r.nome}</div>
    ))}
    {cues.pinos.map((p, i) => {
      const q = proj.pinos[i];
      const s = pop(t, p.t + 0.35, 0.35);
      if (!q.ok || s <= 0) return null;
      return (
        <div key={p.id} style={{ position: 'absolute', left: q.x + 16, top: q.y - 18, transform: `translateY(-100%) scale(${s})`, transformOrigin: 'left bottom',
          background: P.navy, color: P.branco, fontFamily: MONO, padding: '7px 14px 8px', borderRadius: 4, boxShadow: '0 6px 14px rgba(0,0,0,0.3)',
          borderLeft: `5px solid ${P.coral}`, whiteSpace: 'nowrap' }}>
          <div style={{ fontWeight: 700, fontSize: 25, letterSpacing: '0.1em' }}>{p.nome}</div>
          <div style={{ fontWeight: 500, fontSize: 17, letterSpacing: '0.12em', opacity: 0.8 }}>{p.sub}</div>
        </div>
      );
    })}
  </>
);

export const Teste = () => {
  useFontes();
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const t = frame / fps;
  const mundo = useMemo(() => criarMundo(THREE, cues), []);
  mundo.update(t);
  const proj = mundo.projetar(width, height);
  return (
    <AbsoluteFill style={{ background: '#B9A47F' }}>
      <ThreeCanvas width={width} height={height} shadows flat gl={{ antialias: true, preserveDrawingBuffer: true }}>
        <Camera mundo={mundo} />
      </ThreeCanvas>
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(40,25,10,0.38) 100%)' }} />
      <Etiquetas t={t} proj={proj} />
      <Numero t={t} />
      <Capitulo t={t} />
      <Legenda t={t} />
      <div style={{ position: 'absolute', bottom: 34, left: '50%', transform: 'translateX(-50%)', background: 'rgba(31,26,24,0.8)', color: '#E9DCC3',
        fontFamily: MONO, fontWeight: 500, fontSize: 15, letterSpacing: '0.12em', padding: '8px 18px', borderRadius: 4, whiteSpace: 'nowrap' }}>
        SOURCES : {cues.fontes}
      </div>
      <Audio src={staticFile('narracao.wav')} />
    </AbsoluteFill>
  );
};
