// Em Relevo 006 (17/11/2026): Caraguatatuba 1967 × São Sebastião 2023. Motor 2D: mapa do litoral norte (A satélite / B editorial) com câmera,
// camadas de mapa, rótulos ancorados, HUD e cenas de tela cheia (blocos 3D cortados, fotos, documentos, esquemas). Tudo vem de shared/cues.json
// (build_cues6.py). Peças em Cenas6.jsx.
import React, { useLayoutEffect, useState } from 'react';
import { AbsoluteFill, Img, staticFile, useCurrentFrame, delayRender, continueRender } from 'remotion';
import cues from '../../shared/cues.json';
import { numeroEm, capituloEm, legendaEm, pop, janela, clamp01, easeOut } from '../../shared/camadas.js';
import { Cenas } from './Cenas6.jsx';

import { P, MONO, tab, win } from './util6.js';
export const IW = cues.geo.w, IH = cues.geo.h;
const PXKM = cues.geo.k / 111.32;
const suave = (p) => p * p * (3 - 2 * p);
const camAt = (t) => { const c = camAt0(t); const z = Math.max(c.z, 1080 / IH + 0.001, 1920 / IW); return { x: Math.min(IW - 960 / z, Math.max(960 / z, c.x)), y: Math.min(IH - 540 / z, Math.max(540 / z, c.y)), z }; };
const camAt0 = (t) => {
  const K = cues.camera; if (t <= K[0].t) return K[0];
  for (let i = 1; i < K.length; i++) if (t <= K[i].t) { const a = K[i - 1], b = K[i], p = suave(clamp01((t - a.t) / Math.max(0.001, b.t - a.t))); return { x: a.x + (b.x - a.x) * p, y: a.y + (b.y - a.y) * p, z: a.z * Math.pow(b.z / a.z, p) }; }
  return K[K.length - 1];
};

const fontes = [['Anton', 'Anton-Regular.ttf', '400', 'normal'], ['PlexMono', 'IBMPlexMono-Medium.ttf', '500', 'normal'], ['PlexMono', 'IBMPlexMono-Bold.ttf', '700', 'normal'], ['Playfair', 'PlayfairDisplay-Italic.ttf', '400 900', 'italic']];
const useRecursos = () => {
  const [h] = useState(() => delayRender('fontes+imagens', { timeoutInMilliseconds: 240000 }));
  useLayoutEffect(() => {
    const pf = Promise.all(fontes.map(([fam, arq, w, st]) => { const f = new FontFace(fam, `url(${staticFile('fonts/' + arq)})`, { weight: w, style: st }); document.fonts.add(f); return f.load(); }));
    const imgs = ['v6/A.jpg', 'v6/B.jpg', 'v6/decliv40.png', 'v6/decliv30g.png', 'v6/imerg.png', ...cues.fotos.map((f) => 'fotos/' + f)];
    const pi = Promise.all(imgs.map((s) => new Promise((ok) => { const i = new window.Image(); i.onload = ok; i.onerror = ok; i.src = staticFile(s); })));
    Promise.all([pf, pi]).then(() => continueRender(h));
  }, [h]);
};

// ---------------------------------------------------------------- camadas de mapa (no espaço da imagem)
const polilinha = (pts, p) => {   // trecho inicial de fração p
  const seg = []; let tot = 0;
  for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); seg.push(d); tot += d; }
  let alvo = tot * p, out = [pts[0]];
  for (let i = 0; i < seg.length; i++) { if (alvo >= seg[i]) { out.push(pts[i + 1]); alvo -= seg[i]; } else { const f = alvo / seg[i]; out.push([pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f]); break; } }
  return out;
};
const seta = (a, b, cor, w) => {
  const ang = Math.atan2(b[1] - a[1], b[0] - a[0]), L = 22 / w;
  const p1 = [b[0] - L * Math.cos(ang - 0.45), b[1] - L * Math.sin(ang - 0.45)], p2 = [b[0] - L * Math.cos(ang + 0.45), b[1] - L * Math.sin(ang + 0.45)];
  return <g><line x1={a[0]} y1={a[1]} x2={b[0]} y2={b[1]} stroke={cor} strokeWidth={5} vectorEffect="non-scaling-stroke" strokeLinecap="round" /><polygon points={`${b[0]},${b[1]} ${p1[0]},${p1[1]} ${p2[0]},${p2[1]}`} fill={cor} /></g>;
};
const CamadaMapa = ({ m, t, z }) => {
  const a = win(t, m.t0, m.t1, 0.6, 0.6);
  if (a <= 0) return null;
  const pr = clamp01((t - m.t0) / Math.max(0.5, Math.min(3.5, (m.t1 - m.t0) * 0.7)));
  if (m.k === 'img') return <Img src={staticFile(m.src)} style={{ position: 'absolute', left: 0, top: 0, width: IW, height: IH, opacity: a * (m.op ?? 1) }} />;
  const svg = (children) => <svg width={IW} height={IH} style={{ position: 'absolute', left: 0, top: 0, opacity: a, overflow: 'visible' }}>{children}</svg>;
  if (m.k === 'linha') {
    const pts = m.cresce ? polilinha(m.pts, easeOut(pr)) : m.pts;
    return svg(<>
      <polyline points={pts.map((q) => q.join(',')).join(' ')} fill="none" stroke="rgba(0,0,0,0.45)" strokeWidth={m.largura + 4} vectorEffect="non-scaling-stroke" strokeLinecap="round" strokeLinejoin="round" strokeDasharray={m.dash ? '16 14' : undefined} />
      <polyline points={pts.map((q) => q.join(',')).join(' ')} fill="none" stroke={m.cor} strokeWidth={m.largura} vectorEffect="non-scaling-stroke" strokeLinecap="round" strokeLinejoin="round" strokeDasharray={m.dash ? '16 14' : undefined} />
    </>);
  }
  if (m.k === 'chuva') {
    const xs = m.poly.map((q) => q[0]), ys = m.poly.map((q) => q[1]); const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
    const linhas = []; for (let i = 0; i < 260; i++) { const rx = ((i * 7919) % 1000) / 1000, ry = ((i * 104729) % 1000) / 1000; const yy = y0 + ((ry * (y1 - y0) + t * 520) % (y1 - y0)); linhas.push([x0 + rx * (x1 - x0), yy]); }
    return svg(<>
      <defs><clipPath id="cp-chuva"><polygon points={m.poly.map((q) => q.join(',')).join(' ')} /></clipPath></defs>
      <polygon points={m.poly.map((q) => q.join(',')).join(' ')} fill="rgba(63,216,255,0.28)" stroke="#3FD8FF" strokeWidth={4} vectorEffect="non-scaling-stroke" strokeDasharray="14 10" />
      <g clipPath="url(#cp-chuva)" stroke="#BFEFFF" strokeWidth={2.4} vectorEffect="non-scaling-stroke" opacity={0.85}>{linhas.map((q, i) => <line key={i} x1={q[0]} y1={q[1]} x2={q[0] - 10 / z} y2={q[1] + 34 / z} vectorEffect="non-scaling-stroke" stroke="#BFEFFF" strokeWidth={2.4} />)}</g>
    </>);
  }
  if (m.k === 'setas_ar') {
    return svg(<>{m.de.map((d, i) => { const p = easeOut(clamp01((t - m.t0 - i * 0.25) / 1.4)); const b = [d[0] + (m.para[i][0] - d[0]) * p, d[1] + (m.para[i][1] - d[1]) * p]; return <g key={i}>{seta(d, b, '#FFFFFF', z)}</g>; })}</>);
  }
  if (m.k === 'ciclone') {
    const [x, y] = m.ll; const rot = t * 70;
    return svg(<g transform={`translate(${x},${y}) rotate(${rot})`}>{[0, 1, 2].map((k) => <path key={k} d="M0,0 C 60,-10 120,-60 90,-130" transform={`rotate(${k * 120})`} fill="none" stroke="#FBF8F1" strokeWidth={14} strokeLinecap="round" opacity={0.85} />)}<circle r={18} fill="#FBF8F1" /></g>);
  }
  if (m.k === 'cic') {
    const n = Math.floor(m.pts.length * easeOut(clamp01((t - m.t0) / m.ritmo)));
    return svg(<g>{m.pts.slice(0, n).map((q, i) => <ellipse key={i} cx={q[0]} cy={q[1]} rx={m.r * 1.5 / z} ry={m.r * 0.9 / z} fill={m.cor} stroke="rgba(30,20,10,0.55)" strokeWidth={0.8} vectorEffect="non-scaling-stroke" opacity={0.92} transform={`rotate(${(i * 37) % 180} ${q[0]} ${q[1]})`} />)}</g>);
  }
  if (m.k === 'circulo') {
    const r = m.r_km * PXKM * easeOut(clamp01((t - m.t0) / 1.8));
    return svg(<circle cx={m.ll[0]} cy={m.ll[1]} r={r} fill="rgba(232,80,91,0.06)" stroke="#E8505B" strokeWidth={5} vectorEffect="non-scaling-stroke" strokeDasharray="22 14" />);
  }
  if (m.k === 'vales') {
    const V = [[[-45.50, -23.55], [-45.45, -23.58], [-45.41, -23.62]], [[-45.44, -23.52], [-45.42, -23.575], [-45.40, -23.622]], [[-45.36, -23.54], [-45.385, -23.585], [-45.395, -23.622]], [[-45.53, -23.60], [-45.47, -23.612], [-45.415, -23.632]], [[-45.33, -23.57], [-45.37, -23.60], [-45.39, -23.628]], [[-45.47, -23.50], [-45.43, -23.56], [-45.405, -23.618]]];
    const X = (ll) => [(ll[0] - cues.geo.bbox[0]) / (cues.geo.bbox[1] - cues.geo.bbox[0]) * IW, (cues.geo.bbox[3] - ll[1]) / (cues.geo.bbox[3] - cues.geo.bbox[2]) * IH];
    return svg(<>{V.map((v, i) => { const p = clamp01((t - m.t0 - i * 0.9) / 1.6); if (p <= 0) return null; const pts = polilinha(v.map(X), easeOut(p)); return <polyline key={i} points={pts.map((q) => q.join(',')).join(' ')} fill="none" stroke="#E8505B" strokeWidth={8} vectorEffect="non-scaling-stroke" strokeLinecap="round" />; })}</>);
  }
  if (m.k === 'fluxo') {
    return svg(<>{m.vias.map((v, i) => <g key={i}>
      <polyline points={v.map((q) => q.join(',')).join(' ')} fill="none" stroke="rgba(60,30,10,0.55)" strokeWidth={16} vectorEffect="non-scaling-stroke" strokeLinecap="round" strokeLinejoin="round" />
      <polyline points={v.map((q) => q.join(',')).join(' ')} fill="none" stroke="#A8693A" strokeWidth={11} vectorEffect="non-scaling-stroke" strokeLinecap="round" strokeLinejoin="round" strokeDasharray="22 16" strokeDashoffset={-t * 70 - i * 9} />
    </g>)}</>);
  }
  if (m.k === 'ret') {
    const X = (lon, lat) => [(lon - cues.geo.bbox[0]) / (cues.geo.bbox[1] - cues.geo.bbox[0]) * IW, (cues.geo.bbox[3] - lat) / (cues.geo.bbox[3] - cues.geo.bbox[2]) * IH];
    const [x0, y0] = X(m.box[0], m.box[3]), [x1, y1] = X(m.box[1], m.box[2]);
    return svg(<><rect x={x0} y={y0} width={x1 - x0} height={y1 - y0} fill="rgba(232,80,91,0.1)" stroke="#E8505B" strokeWidth={6} vectorEffect="non-scaling-stroke" /><text x={x0} y={y0 - 14 / z} fontFamily="PlexMono" fontWeight="700" fontSize={26 / z} fill="#FBF8F1" style={{ paintOrder: 'stroke' }} stroke="rgba(0,0,0,0.7)" strokeWidth={5 / z}>{m.texto}</text></>);
  }
  return null;
};

// ---------------------------------------------------------------- rótulos ancorados
const ESTILO_ROT = {
  seta: { color: P.branco, background: P.navy },
  corredor: { color: P.branco, background: P.coral },
  quente: { color: P.branco, background: '#C9612A' },
  fria: { color: P.branco, background: '#3D6A9E' },
};
const Ancorado = ({ a, t, cam }) => {
  const w = win(t, a.t0, a.t1, 0.4, 0.35);
  if (w <= 0) return null;
  const sx = (a.ll[0] - cam.x) * cam.z + 960, sy = (a.ll[1] - cam.y) * cam.z + 540;
  if (sx < -300 || sx > 2220 || sy < -400 || sy > 1400) return null;
  if (a.k === 'rotulo') return <div style={{ position: 'absolute', left: sx, top: sy, transform: `translate(-50%,-50%) scale(${pop(t, a.t0, 0.35)})`, opacity: w, ...ESTILO_ROT[a.estilo], fontFamily: MONO, fontWeight: 700, fontSize: 25, letterSpacing: '0.1em', padding: '8px 16px', borderRadius: 4, whiteSpace: 'nowrap', boxShadow: '0 6px 18px rgba(0,0,0,0.45)' }}>{a.texto}</div>;
  if (a.k === 'pino') {
    const b = pop(t, a.t0, 0.5);
    return <div style={{ position: 'absolute', left: sx, top: sy, opacity: w }}>
      <div style={{ position: 'absolute', left: -2, top: -90 * b, width: 4, height: 90 * b, background: P.coral }} />
      <div style={{ position: 'absolute', left: -13, top: -13, width: 26, height: 26, borderRadius: 13, background: P.coral, border: `4px solid ${P.branco}`, boxShadow: '0 4px 12px rgba(0,0,0,0.5)' }} />
      <div style={{ position: 'absolute', left: 0, top: -90 * b - 60, transform: `translateX(-50%) scale(${b})`, background: P.branco, color: P.tinta, fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.08em', padding: '8px 16px', borderRadius: 4, whiteSpace: 'nowrap', boxShadow: '0 8px 22px rgba(0,0,0,0.5)' }}>{a.nome}</div>
    </div>;
  }
  if (a.k === 'coluna') {
    const p = easeOut(clamp01((t - a.t0) / 1.3)), h = a.altmax * (a.valor / a.maxv) * p;
    const v = Math.round(a.valor * p);
    return <div style={{ position: 'absolute', left: sx, top: sy, opacity: w }}>
      <div style={{ position: 'absolute', left: -26, top: -h, width: 52, height: h, background: `linear-gradient(90deg, ${a.cor}, #1b8fb5)`, border: '2px solid rgba(255,255,255,0.85)', borderRadius: '6px 6px 0 0', boxShadow: '0 10px 24px rgba(0,0,0,0.5)' }} />
      <div style={{ position: 'absolute', left: 0, top: -h - 78, transform: 'translateX(-50%)', textAlign: 'center', whiteSpace: 'nowrap' }}>
        <div style={{ fontFamily: 'Anton', fontSize: 62, color: P.branco, lineHeight: 1, textShadow: '0 4px 14px rgba(0,0,0,0.8)' }}>{v}<span style={{ fontSize: 26, marginLeft: 6 }}>MM</span></div>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 21, letterSpacing: '0.1em', color: P.navy, background: P.branco, padding: '3px 12px', borderRadius: 3, marginTop: 4 }}>{a.rot}</div>
      </div>
      <div style={{ position: 'absolute', left: -20, top: -6, width: 40, height: 12, borderRadius: 6, background: 'rgba(0,0,0,0.45)' }} />
    </div>;
  }
  return null;
};

// ---------------------------------------------------------------- HUD
const Numero = ({ t }) => {
  const n = numeroEm(cues, t);
  if (!n) return null;
  const sN = pop(t, n.tNum, 0.4), sF = pop(t, n.tNum + 0.1, 0.35), longo = String(n.texto).length > 9;
  return (
    <div style={{ position: 'absolute', top: 26, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <div style={{ transform: `scale(${sN})`, color: P.coral, fontFamily: 'Anton', fontSize: longo ? 100 : 124, lineHeight: 1, letterSpacing: 1, textShadow: '0 4px 0 rgba(255,255,255,0.9), 0 10px 30px rgba(0,0,0,0.55)', WebkitTextStroke: '3px #FBF8F1', paintOrder: 'stroke fill', display: 'flex', alignItems: 'baseline', gap: 14 }}>
        <span>{n.texto}</span>{n.unidade && <span style={{ fontSize: 46 }}>{n.unidade.toUpperCase()}</span>}
      </div>
      {n.faixa && <div style={{ marginTop: 10, transform: `scale(${sF})`, background: P.navy, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 23, letterSpacing: '0.12em', padding: '8px 22px', borderRadius: 6, boxShadow: '0 6px 16px rgba(0,0,0,0.35)', whiteSpace: 'nowrap' }}>{n.faixa}</div>}
    </div>
  );
};
const Capitulo = ({ t }) => {
  const c = capituloEm(cues, t), p = clamp01((t - c.t) / 0.35);
  return <div style={{ position: 'absolute', top: 40, left: 48, display: 'flex', alignItems: 'center', gap: 12, background: 'rgba(31,26,24,0.88)', padding: '9px 18px', borderRadius: 6, fontFamily: MONO, fontWeight: 700, fontSize: 20, letterSpacing: '0.16em', color: P.branco, transform: `translateX(${(1 - easeOut(p)) * -60}px)`, opacity: 0.2 + 0.8 * p }}>
    <span style={{ width: 11, height: 11, borderRadius: 6, background: P.coral, opacity: Math.floor(t * 2) % 2 ? 0.45 : 1 }} />{c.nome}</div>;
};
const Legenda = ({ t }) => {
  const l = legendaEm(cues, t);
  if (!l || !l.palavras.length) return null;
  const cursorOn = Math.floor(t * 3.2) % 2 === 0;
  return (
    <div style={{ position: 'absolute', bottom: 70, left: 0, width: '100%', display: 'flex', justifyContent: 'center' }}>
      <div style={{ maxWidth: 1500, background: P.branco, color: P.tinta, fontFamily: MONO, fontWeight: 500, fontSize: 38, lineHeight: 1.3, padding: '11px 24px', borderRadius: 4, boxShadow: '0 8px 24px rgba(0,0,0,0.3)', display: 'flex', flexWrap: 'wrap', columnGap: 15, alignItems: 'center', transform: `rotate(-0.6deg) scale(${0.92 + 0.08 * pop(t, l.tBloco, 0.25)})`, transformOrigin: 'left center' }}>
        {l.palavras.map((p, i) => <span key={i} style={{ whiteSpace: 'nowrap' }}><span style={{ borderBottom: p.destaque && p.completo ? `4px solid ${P.coral}` : '4px solid transparent' }}>{p.texto}</span>
          {i === l.palavras.length - 1 && <span style={{ display: 'inline-block', width: 14, height: 36, background: P.coral, marginLeft: 4, verticalAlign: 'middle', opacity: cursorOn ? 1 : 0 }} />}</span>)}
      </div>
    </div>
  );
};
const FICHA_COR = { PAREDE: '#B9A47F', CHUVA: '#3FD8FF', CASCA: '#C98B52' };
const Fichas = ({ t, hud }) => {
  const fs = hud.filter((h) => h.k === 'ficha');
  const slots = ['PAREDE', 'CHUVA', 'CASCA'];
  return <>{slots.map((nome, i) => {
    const lista = fs.filter((f) => f.nome === nome && t >= f.t0 && t <= f.t1 + 0.4);
    const f = lista[lista.length - 1]; if (!f) return null;
    const pulso = (f.pulsos || []).reduce((m, p) => Math.max(m, t >= p && t < p + 1.6 ? 1 - (t - p) / 1.6 : 0), 0);
    const s = pop(t, f.t0, 0.4) * (1 + 0.1 * pulso);
    return <div key={nome} style={{ position: 'absolute', right: 40, top: 130 + i * 168, width: 470, transform: `scale(${s})`, transformOrigin: 'right center', opacity: win(t, f.t0, f.t1, 0.2, 0.4), background: P.navy, color: P.branco, borderRadius: 8, borderLeft: `14px solid ${FICHA_COR[nome]}`, padding: '12px 22px 14px', boxShadow: `0 10px 26px rgba(0,0,0,0.5), 0 0 ${40 * pulso}px ${FICHA_COR[nome]}` }}>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 21, letterSpacing: '0.18em', color: FICHA_COR[nome] }}>{nome}</div>
      <div style={{ fontFamily: 'Anton', fontSize: 70, lineHeight: 1.05 }}>{f.num}</div>
      <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 22, letterSpacing: '0.08em', opacity: 0.9 }}>{f.txt}</div>
    </div>;
  })}</>;
};
const Hud = ({ t }) => {
  const hud = cues.hud;
  return <>
    {hud.filter((h) => h.k === 'cartao').map((h, i) => { const w = win(t, h.t0, h.t1, 0.4, 0.4); if (w <= 0) return null; const n = Math.round(clamp01((t - h.t0) / 1.2) * h.texto.length);
      return <div key={'c' + i} style={{ position: 'absolute', top: 110, left: 48, opacity: w, transform: `translateX(${(1 - easeOut(clamp01((t - h.t0) / 0.4))) * -80}px)`, background: P.coral, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: '0.14em', padding: '10px 20px', borderRadius: 4, boxShadow: '0 8px 22px rgba(0,0,0,0.4)' }}>{h.texto.slice(0, n)}</div>; })}
    <Fichas t={t} hud={hud} />
    {hud.filter((h) => h.k === 'selo').map((h, i) => { const w = win(t, h.t0, h.t1, 0.3, 0.3); if (w <= 0) return null;
      return <div key={'s' + i} style={{ position: 'absolute', right: 48, bottom: 8, opacity: w, background: 'rgba(31,26,24,0.9)', color: '#E9DCC3', fontFamily: MONO, fontWeight: 700, fontSize: 18, letterSpacing: '0.14em', padding: '6px 14px', borderRadius: 4, border: '2px dashed rgba(233,220,195,0.6)' }}>{h.texto}</div>; })}
    {hud.filter((h) => h.k === 'selo_grande').map((h, i) => { const w = win(t, h.t0, h.t1, 0.3, 0.4); if (w <= 0) return null;
      return <div key={'sg' + i} style={{ position: 'absolute', left: 60, top: 150, opacity: w, transform: `rotate(-6deg) scale(${2 - easeOut(clamp01((t - h.t0) / 0.3))})`, border: `9px solid ${P.coral}`, color: P.coral, background: 'rgba(251,248,241,0.92)', fontFamily: 'Anton', fontSize: 100, padding: '0 30px', borderRadius: 10, letterSpacing: '0.03em' }}>{h.texto}</div>; })}
    {hud.filter((h) => h.k === 'etiqueta').map((h, i) => { const w = win(t, h.t0, h.t1, 0.3, 0.3); if (w <= 0) return null;
      return <div key={'e' + i} style={{ position: 'absolute', left: h.pos[0], top: h.pos[1], opacity: w, transform: `scale(${pop(t, h.t0, 0.35)})`, transformOrigin: 'left center', background: P.navy, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.1em', padding: '9px 18px', borderRadius: 4, boxShadow: '0 6px 18px rgba(0,0,0,0.45)', whiteSpace: 'nowrap', maxWidth: 1500 }}>{h.texto}</div>; })}
    {hud.filter((h) => h.k === 'tag').map((h, i) => { const w = win(t, h.t0, h.t1, 0.3, 0.3); if (w <= 0) return null;
      return <div key={'t' + i} style={{ position: 'absolute', left: 340 + h.i * 430, top: 48, transform: `scale(${pop(t, h.t0, 0.35)})`, opacity: w, background: P.coral, color: P.branco, fontFamily: 'Anton', fontSize: 40, letterSpacing: '0.06em', padding: '3px 18px', borderRadius: 4, boxShadow: '0 6px 18px rgba(0,0,0,0.5)' }}>{h.texto}</div>; })}
    {hud.filter((h) => h.k === 'regua_h').map((h, i) => { const w = win(t, h.t0, h.t1, 0.3, 0.3); if (w <= 0) return null;
      return <div key={'r' + i} style={{ position: 'absolute', left: h.pos[0], top: h.pos[1], opacity: w, background: 'rgba(31,42,68,0.92)', color: P.amarelo, fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: '0.12em', padding: '8px 18px', borderRadius: 4, borderBottom: `5px solid ${P.amarelo}` }}>{h.texto}</div>; })}
    {hud.filter((h) => h.k === 'altimetro').map((h, i) => { const w = win(t, h.t0, h.t1, 0.4, 0.4); if (w <= 0) return null; const p = easeOut(clamp01((t - h.t0) / Math.max(0.5, h.t_fim - h.t0)));
      return <div key={'a' + i} style={{ position: 'absolute', right: 60, top: 160, width: 150, height: 560, opacity: w, background: 'rgba(31,42,68,0.9)', borderRadius: 8, padding: 12 }}>
        <div style={{ position: 'absolute', left: 70, top: 20, width: 6, height: 520, background: 'rgba(255,255,255,0.25)' }} />
        <div style={{ position: 'absolute', left: 70, bottom: 20, width: 6, height: 520 * p, background: P.amarelo }} />
        <div style={{ position: 'absolute', left: 8, bottom: 14 + 520 * p, background: P.amarelo, color: P.navy, fontFamily: 'Anton', fontSize: 34, padding: '0 8px', transform: 'translateY(50%)' }}>{Math.round(h.para * p)} M</div>
        <div style={{ position: 'absolute', left: 0, bottom: -44, width: '100%', textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 20, color: P.branco, background: 'rgba(31,42,68,0.9)', padding: '4px 0', letterSpacing: '0.1em' }}>{(h.km * p).toFixed(1).replace('.', ',')} KM</div>
      </div>; })}
    {hud.filter((h) => h.k === 'aspas').map((h, i) => { const w = win(t, h.t0, h.t1, 0.4, 0.4); if (w <= 0) return null;
      return <div key={'q' + i} style={{ position: 'absolute', left: 120, top: 760, opacity: w, transform: `scale(${pop(t, h.t0, 0.4)})`, transformOrigin: 'left center', background: P.branco, color: P.tinta, padding: '14px 30px', borderRadius: 4, boxShadow: '0 12px 30px rgba(0,0,0,0.5)' }}>
        <div style={{ fontFamily: 'Playfair', fontStyle: 'italic', fontSize: 66, fontWeight: 700 }}>{h.texto}</div><div style={{ fontFamily: MONO, fontSize: 22, letterSpacing: '0.16em', color: P.coral, fontWeight: 700 }}>{h.sub}</div></div>; })}
    {hud.filter((h) => h.k === 'pergunta').map((h, i) => { const w = win(t, h.t0, h.t1, 0.3, 0.5); if (w <= 0) return null; const n = Math.round(clamp01((t - h.t0) / 1.8) * h.texto.length);
      return <div key={'p' + i} style={{ position: 'absolute', left: 0, top: 250, width: '100%', opacity: w, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 22 }}>
        <div style={{ background: 'rgba(31,42,68,0.93)', color: P.branco, fontFamily: 'Anton', fontSize: 98, lineHeight: 1.1, padding: '24px 48px', maxWidth: 1600, textAlign: 'center', borderRadius: 6, boxShadow: '0 18px 50px rgba(0,0,0,0.55)', borderBottom: `10px solid ${P.coral}` }}>{h.texto.slice(0, n)}<span style={{ color: P.coral }}>{n < h.texto.length ? '▌' : ''}</span></div>
        {t >= h.t_sub && <div style={{ transform: `scale(${pop(t, h.t_sub, 0.4)})`, background: P.coral, color: P.branco, fontFamily: 'Anton', fontSize: 58, padding: '6px 34px', borderRadius: 4 }}>{h.sub}</div>}
      </div>; })}
  </>;
};

// ---------------------------------------------------------------- composição
export const Longo6 = ({ tempo }) => {
  useRecursos();
  const frame = useCurrentFrame();
  const t = tempo !== undefined ? tempo : frame / cues.fps;
  const cam = camAt(t), b = tab(cues.estilo, t), esc = tab(cues.escuro, t);
  const tr = `translate(${960 - cam.x * cam.z}px, ${540 - cam.y * cam.z}px) scale(${cam.z})`;
  const fade = Math.min(clamp01(t / 0.5), 1 - clamp01((t - (cues.duracao - 0.6)) / 0.6));
  return (
    <AbsoluteFill style={{ background: '#0E1A33', opacity: fade }}>
      <div style={{ position: 'absolute', left: 0, top: 0, width: IW, height: IH, transformOrigin: '0 0', transform: tr, willChange: 'transform' }}>
        <Img src={staticFile('v6/A.jpg')} style={{ position: 'absolute', left: 0, top: 0, width: IW, height: IH }} />
        {b > 0.001 && <Img src={staticFile('v6/B.jpg')} style={{ position: 'absolute', left: 0, top: 0, width: IW, height: IH, opacity: b }} />}
        {cues.mapa.map((m, i) => <CamadaMapa key={i} m={m} t={t} z={cam.z} />)}
      </div>
      <AbsoluteFill style={{ background: `rgba(6,10,26,${esc})` }} />
      {cues.anc.map((a, i) => <Ancorado key={i} a={a} t={t} cam={cam} />)}
      <Cenas t={t} cues={cues} />
      <Numero t={t} />
      <Capitulo t={t} />
      <Hud t={t} />
      <Legenda t={t} />
    </AbsoluteFill>
  );
};
