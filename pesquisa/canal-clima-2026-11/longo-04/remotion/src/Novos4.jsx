// Em Relevo 004 (13/11/2026): camadas 2D novas do vídeo "1983, o El Niño que partiu o Brasil ao meio".
// Dirigidas por cues.graficos4 (shared/build_cues.py). Reusa a paleta e o painel de papel do canal.
import React from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import { janela, clamp01, easeOut } from '../../shared/camadas.js';

const MONO = 'PlexMono, monospace';
const P = { papel: '#E9DCC3', coral: '#E8505B', navy: '#1F2A44', tinta: '#2B2622', branco: '#FBF8F1', agua: '#3D7FB8', agua2: '#7FB4DE' };
const milhar = (n) => Math.round(n).toLocaleString('pt-BR');
const dec = (n, d = 2) => n.toFixed(d).replace('.', ',');
const tab = (lista, t) => { // [[t, v], ...] linear
  if (!lista.length) return 0;
  if (t <= lista[0][0]) return lista[0][1];
  for (let i = 1; i < lista.length; i++) if (t <= lista[i][0]) { const [t0, v0] = lista[i - 1], [t1, v1] = lista[i]; return v0 + (v1 - v0) * easeOut((t - t0) / Math.max(1e-6, t1 - t0)); }
  return lista[lista.length - 1][1];
};
const Painel = ({ a, children, left = 110, top = 220, w = 1100, titulo, fonte }) => (
  <div style={{ position: 'absolute', left, top, width: w, transform: `scale(${a})`, transformOrigin: 'left center', background: '#F3EEE3', borderRadius: 6,
    boxShadow: '0 20px 50px rgba(0,0,0,0.42)', padding: '24px 30px 20px', fontFamily: MONO, color: P.tinta }}>
    {titulo && <div style={{ fontWeight: 700, fontSize: 21, letterSpacing: '0.12em', color: P.navy, marginBottom: 16 }}>{titulo}</div>}
    {children}
    {fonte && <div style={{ fontWeight: 500, fontSize: 14, letterSpacing: '0.1em', color: '#7a7066', marginTop: 14 }}>FONTE: {fonte}</div>}
  </div>
);
const MESES = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];

export const Grafico4 = ({ g, t }) => {
  const a = janela(t, g.t0, g.t1, 0.45, 0.35);
  if (a <= 0) return null;

  if (g.tipo === 'relogio') return (
    <div style={{ position: 'absolute', left: 0, right: 0, top: g.top ?? 90, display: 'flex', justifyContent: 'flex-start', paddingLeft: 130, transform: `scale(${a})` }}>
      <div style={{ fontFamily: 'Anton', fontSize: 190, lineHeight: 1, color: P.branco, background: P.navy, padding: '4px 54px 14px', border: `8px solid ${P.coral}`, borderRadius: 8, boxShadow: '0 20px 50px rgba(0,0,0,0.5)', letterSpacing: 4 }}>
        {g.texto}{g.sub && <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 30, letterSpacing: '0.2em', color: P.agua2, textAlign: 'center', marginTop: -8 }}>{g.sub}</div>}
      </div>
    </div>
  );

  if (g.tipo === 'hidro') {
    const wv = 1180, hv = 340, n = g.n, ymax = g.ymax, x = (i) => (i / (n - 1)) * wv, y = (v) => hv - (v / ymax) * hv;
    const frac = tab(g.prog, t), lim = Math.floor(frac * (n - 1));
    const pts = g.dias.filter(([i]) => i <= lim);
    const linha = pts.map(([i, v]) => `${x(i)},${y(v)}`).join(' ');
    const area = pts.length ? `${x(pts[0][0])},${hv} ${linha} ${x(pts[pts.length - 1][0])},${hv}` : '';
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={1250} left={g.left ?? 330} top={g.top ?? 250}>
        <svg width={wv} height={hv + 70} style={{ overflow: 'visible' }}>
          {[0, 2.5, 6, 10].map((m) => <g key={m}><line x1={0} x2={wv} y1={y(m)} y2={y(m)} stroke={m === 6 ? P.coral : '#c9bfae'} strokeWidth={m === 6 ? 3 : 1} strokeDasharray={m === 6 ? '10 8' : '2 6'} />
            <text x={-8} y={y(m) + 6} textAnchor="end" fontFamily="PlexMono" fontWeight={700} fontSize={17} fill={m === 6 ? P.coral : '#6b625a'}>{m}</text></g>)}
          <text x={wv} y={y(6) - 8} textAnchor="end" fontFamily="PlexMono" fontWeight={700} fontSize={17} fill={P.coral}>6 M · TRANSBORDA</text>
          {g.faixa && t >= g.faixa.t && <g><rect x={x(g.faixa.i0)} y={y(10.6)} width={x(g.faixa.i1) - x(g.faixa.i0)} height={hv - y(10.6)} fill="rgba(232,80,91,0.13)" />
            <text x={x(g.faixa.i1) + 10} y={y(9.2)} textAnchor="start" fontFamily="PlexMono" fontWeight={700} fontSize={19} fill={P.coral}>{g.faixa.texto}</text></g>}
          {pts.length > 1 && <><polygon points={area} fill="rgba(61,127,184,0.55)" /><polyline points={linha} fill="none" stroke={P.agua} strokeWidth={4} /></>}
          {g.roni && t >= g.roni.t && (() => {
            const p2 = easeOut(clamp01((t - g.roni.t) / 2.2)), sel = g.roni.serie.filter(([i]) => i <= p2 * (n - 1));
            const yr = (v) => y(v * g.roni.k);
            return sel.length > 1 ? <polyline points={sel.map(([i, v]) => `${x(i)},${yr(v)}`).join(' ')} fill="none" stroke={P.coral} strokeWidth={5} strokeDasharray="14 6" /> : null;
          })()}
          {g.marcas.map((m, k) => {
            if (t < m.t) return null;
            const s = clamp01((t - m.t) / 0.35), up = k % 2 === 0;
            return <g key={k} opacity={s}><circle cx={x(m.i)} cy={y(m.v)} r={9} fill={m.cor || P.coral} stroke="#fff" strokeWidth={3} />
              <text x={x(m.i) + (m.dx || 0)} y={y(m.v) + (up ? -18 : 34) + (m.dy || 0)} textAnchor="middle" fontFamily="Anton" fontSize={m.tam || 30} fill={m.cor || P.coral} stroke="#F3EEE3" strokeWidth={7} paintOrder="stroke">{m.texto}</text></g>;
          })}
          {g.vertical && t >= g.vertical.t && <g><line x1={x(g.vertical.i)} x2={x(g.vertical.i)} y1={0} y2={hv} stroke={P.navy} strokeWidth={4} /><text x={x(g.vertical.i) + 8} y={22} fontFamily="PlexMono" fontWeight={700} fontSize={19} fill={P.navy}>{g.vertical.texto}</text></g>}
          {g.eixo.map(([i, rot]) => <text key={rot} x={x(i)} y={hv + 30} textAnchor="middle" fontFamily="PlexMono" fontSize={17} fill="#6b625a">{rot}</text>)}
          {g.rotulos && g.rotulos.map((r, k) => t >= r.t && <text key={k} x={r.x} y={r.y} fontFamily="PlexMono" fontWeight={700} fontSize={22} fill={r.cor} stroke="#F3EEE3" strokeWidth={6} paintOrder="stroke">{r.texto}</text>)}
        </svg>
      </Painel>
    );
  }

  if (g.tipo === 'regua') {
    const hv = 560, nivel = tab(g.niveis.map(([tt, m]) => [tt, m]), t), ult = g.niveis.filter(([tt]) => t >= tt - 0.2).slice(-1)[0];
    const y = (m) => hv - (m / g.max) * hv;
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={g.w ?? 560} left={g.left ?? 110} top={g.top ?? 220}>
        <div style={{ position: 'relative', height: hv + 20, display: 'flex' }}>
          <svg width={150} height={hv + 20}>
            <rect x={60} y={0} width={64} height={hv} fill="rgba(31,42,68,0.08)" stroke="#6b625a" strokeWidth={3} />
            <rect x={62} y={y(nivel)} width={60} height={hv - y(nivel)} fill={P.agua} />
            {Array.from({ length: g.max + 1 }, (_, m) => <g key={m}><line x1={44} x2={60} y1={y(m)} y2={y(m)} stroke="#4a4036" strokeWidth={m % 5 === 0 ? 4 : 2} />{(m % 2 === 0) && <text x={38} y={y(m) + 6} textAnchor="end" fontFamily="PlexMono" fontWeight={700} fontSize={16} fill="#4a4036">{m}</text>}</g>)}
            {g.linha != null && <g><line x1={20} x2={140} y1={y(g.linha)} y2={y(g.linha)} stroke={P.coral} strokeWidth={4} strokeDasharray="8 6" /><text x={140} y={y(g.linha) - 6} textAnchor="end" fontFamily="PlexMono" fontWeight={700} fontSize={14} fill={P.coral}>{g.linha_txt}</text></g>}
          </svg>
          <div style={{ flex: 1, position: 'relative' }}>
            <div style={{ fontFamily: 'Anton', fontSize: 100, color: P.coral, lineHeight: 1 }}>{dec(nivel)}<span style={{ fontSize: 40 }}> M</span></div>
            {ult && <div style={{ fontWeight: 700, fontSize: 24, letterSpacing: '0.1em', color: P.navy, marginTop: 8 }}>{ult[2]}</div>}
            <div style={{ marginTop: 22 }}>{g.niveis.map(([tt, m, rot, cor], k) => t >= tt && <div key={k} style={{ fontWeight: 700, fontSize: 21, margin: '6px 0', color: cor || P.tinta }}>{rot} · {dec(m)} M</div>)}</div>
          </div>
        </div>
      </Painel>
    );
  }

  if (g.tipo === 'cortina') {
    const u = easeOut(clamp01((t - g.t_cortina) / 1.6)), z = 1 + 0.12 * clamp01((t - g.t0) / (g.t1 - g.t0));
    const fil = 'saturate(1.25) contrast(1.08)';
    const rot = (txt, cor) => <div style={{ background: cor, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 30, letterSpacing: '0.1em', padding: '8px 18px', borderRadius: 4 }}>{txt}</div>;
    return (
      <AbsoluteFill style={{ opacity: Math.min(1, a * 1.6), background: '#0c1220' }}>
        <AbsoluteFill style={{ overflow: 'hidden' }}><Img src={staticFile(g.antes)} style={{ width: '100%', height: '100%', objectFit: 'cover', filter: fil, transform: `scale(${z})`, transformOrigin: g.origem }} /></AbsoluteFill>
        <AbsoluteFill style={{ overflow: 'hidden', clipPath: `inset(0 0 0 ${(1 - u) * 100}%)` }}><Img src={staticFile(g.depois)} style={{ width: '100%', height: '100%', objectFit: 'cover', filter: fil, transform: `scale(${z})`, transformOrigin: g.origem }} /></AbsoluteFill>
        <div style={{ position: 'absolute', top: 0, bottom: 0, left: `${(1 - u) * 100}%`, width: 6, background: P.branco, boxShadow: '0 0 24px rgba(0,0,0,0.6)', opacity: u > 0.01 && u < 0.99 ? 1 : 0 }} />
        <div style={{ position: 'absolute', left: 60, top: 120 }}>{rot(g.rotA, P.navy)}</div>
        {u > 0.5 && <div style={{ position: 'absolute', right: 60, top: 120 }}>{rot(g.rotB, P.coral)}</div>}
        {t >= g.t_seta && <div style={{ position: 'absolute', left: g.seta.x, top: g.seta.y, transform: `scale(${clamp01((t - g.t_seta) / 0.4)})`, fontFamily: 'Anton', fontSize: 52, color: P.branco, background: 'rgba(31,42,68,0.85)', border: `4px solid ${P.coral}`, padding: '8px 22px', borderRadius: 6 }}>{g.seta.texto}</div>}
        <div style={{ position: 'absolute', left: 60, bottom: 230, fontFamily: MONO, fontWeight: 700, fontSize: 22, letterSpacing: '0.12em', color: P.branco, textShadow: '0 2px 8px #000' }}>LANDSAT 4 · MESMA JANELA · ~52 × 29 KM</div>
      </AbsoluteFill>
    );
  }

  if (g.tipo === 'anuais') {
    const wv = 1200, hv = 330, n = g.anos.length, bw = wv / n, max = g.max, p = easeOut(clamp01((t - g.t_ini) / g.dur));
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={1280} left={320} top={g.top ?? 250}>
        <svg width={wv} height={hv + 40}>
          {g.anos.map(([ano, mm], i) => {
            if (i / n > p) return null;
            const h = (mm / max) * hv, d = g.dest.find((q) => q[0] === ano), on = d && t >= d[1];
            return <rect key={ano} x={i * bw} width={bw - 1} y={hv - h} height={h} fill={on ? P.coral : '#7FA2C9'} />;
          })}
          <line x1={0} x2={wv} y1={hv - (g.media / max) * hv} y2={hv - (g.media / max) * hv} stroke={P.navy} strokeWidth={3} strokeDasharray="10 8" />
          <text x={wv - 4} y={hv - (g.media / max) * hv - 8} textAnchor="end" fontFamily="PlexMono" fontWeight={700} fontSize={19} fill={P.navy} stroke="#F3EEE3" strokeWidth={6} paintOrder="stroke">MÉDIA {milhar(g.media)} MM</text>
          {[1920, 1950, 1980, 2010].map((ano) => { const i = g.anos.findIndex((q) => q[0] === ano); return i >= 0 && <text key={ano} x={i * bw} y={hv + 28} fontFamily="PlexMono" fontSize={17} fill="#6b625a">{ano}</text>; })}
          {g.dest.map(([ano, tt, rot], k) => t >= tt && <text key={ano} x={wv - 10} y={40 + k * 38} textAnchor="end" fontFamily="Anton" fontSize={32} fill={P.coral} stroke="#F3EEE3" strokeWidth={7} paintOrder="stroke">{rot}</text>)}
        </svg>
      </Painel>
    );
  }

  if (g.tipo === 'colunas') {
    const hv = 250, bw = 170;
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={g.w ?? 680} left={g.left ?? 1100} top={g.top ?? 260}>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: 34, height: hv + 130, justifyContent: 'center', paddingTop: 20 }}>
          {g.itens.map(([rot, v, tt, cor, txt], i) => {
            const p = easeOut(clamp01((t - tt) / 1.1)); const h = (v / g.max) * hv * p;
            return <div key={i} style={{ width: bw, textAlign: 'center', opacity: t >= tt ? 1 : 0 }}>
              <div style={{ fontFamily: 'Anton', fontSize: 40, color: cor, marginBottom: 6 }}>{txt}</div>
              <div style={{ height: h, background: cor, borderRadius: '4px 4px 0 0' }} />
              <div style={{ fontWeight: 700, fontSize: 17, letterSpacing: '0.06em', marginTop: 8, color: P.tinta, minHeight: 44 }}>{rot}</div>
            </div>;
          })}
        </div>
        {g.selo && t >= g.selo.t && <div style={{ marginTop: 10, display: 'inline-block', background: P.coral, color: P.branco, fontFamily: 'Anton', fontSize: 40, padding: '2px 22px', borderRadius: 4, transform: 'rotate(-2deg)' }}>{g.selo.texto}</div>}
      </Painel>
    );
  }

  if (g.tipo === 'anel24') {
    const R = 190, cx = 250, cy = 250, N = 24;
    const ang = (i) => (i / N) * 2 * Math.PI - Math.PI / 2;
    const fatia = (i, r0, r1) => { const a0 = ang(i), a1 = ang(i + 1);
      return `M${cx + r0 * Math.cos(a0)} ${cy + r0 * Math.sin(a0)} L${cx + r1 * Math.cos(a0)} ${cy + r1 * Math.sin(a0)} A${r1} ${r1} 0 0 1 ${cx + r1 * Math.cos(a1)} ${cy + r1 * Math.sin(a1)} L${cx + r0 * Math.cos(a1)} ${cy + r0 * Math.sin(a1)} A${r0} ${r0} 0 0 0 ${cx + r0 * Math.cos(a0)} ${cy + r0 * Math.sin(a0)}Z`; };
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={600} left={g.left ?? 1230} top={g.top ?? 210}>
        <svg width={500} height={520}>
          {Array.from({ length: N }, (_, i) => {
            const corr = g.acende.filter((z) => i >= z.i0 && i <= z.i1 && t >= z.t);
            const z = corr[corr.length - 1], pont = z && z.pontilhado;
            return <path key={i} d={fatia(i, i < 12 ? 120 : 84, i < 12 ? R : 118)} fill={z && !pont ? z.cor : pont ? 'rgba(232,80,91,0.12)' : '#D9CDB6'} stroke={pont ? P.coral : '#F3EEE3'} strokeWidth={pont ? 3 : 2} strokeDasharray={pont ? '6 5' : undefined} />;
          })}
          {Array.from({ length: N }, (_, i) => { const am = (ang(i) + ang(i + 1)) / 2, r = i < 12 ? R + 20 : 138; return i < 12 ? <text key={i} x={cx + r * Math.cos(am)} y={cy + r * Math.sin(am) + 6} textAnchor="middle" fontFamily="PlexMono" fontWeight={700} fontSize={16} fill={P.tinta}>{MESES[i % 12]}</text> : null; })}
          <text x={cx} y={cy - 2} textAnchor="middle" fontFamily="Anton" fontSize={24} fill={P.navy}>{g.centro[0]}</text>
          <text x={cx} y={cy + 24} textAnchor="middle" fontFamily="Anton" fontSize={24} fill={P.coral}>{g.centro[1]}</text>
          {(g.marcas || []).map((m, k) => { if (t < m.t) return null; const am = (ang(m.i) + ang(m.i + 1)) / 2, r = m.i < 12 ? 155 : 101, s = clamp01((t - m.t) / 0.3);
            return <g key={k} opacity={s}><circle cx={cx + r * Math.cos(am)} cy={cy + r * Math.sin(am)} r={11} fill={P.navy} stroke="#fff" strokeWidth={3} /></g>; })}
        </svg>
        <div style={{ fontWeight: 700, fontSize: 19, lineHeight: 1.5 }}>
          {g.legenda.map(([cor, txt, tt], k) => t >= tt && <div key={k} style={{ display: 'flex', alignItems: 'center', gap: 10 }}><span style={{ width: 22, height: 22, background: cor, display: 'inline-block' }} />{txt}</div>)}
        </div>
      </Painel>
    );
  }

  if (g.tipo === 'gauge') {
    const p = easeOut(clamp01((t - g.t_gira) / 1.6));
    const ang = (v) => Math.PI * (1 - v / 100), pt = (v, r) => [260 + r * Math.cos(ang(v)), 260 - r * Math.sin(ang(v))];
    const arco = (v0, v1, r) => { const [x0, y0] = pt(v0, r), [x1, y1] = pt(v1, r); return `M${x0},${y0} A${r},${r} 0 0 1 ${x1},${y1}`; };
    const [ax, ay] = pt(g.valor * p, 190);
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={640} left={1180} top={250}>
        <svg width={560} height={300}>
          <path d={arco(0, 100, 210)} stroke="rgba(31,42,68,0.15)" strokeWidth={42} fill="none" />
          <path d={arco(0, Math.max(0.01, g.valor * p), 210)} stroke={P.coral} strokeWidth={42} fill="none" />
          <line x1={260} y1={260} x2={ax} y2={ay} stroke={P.navy} strokeWidth={8} strokeLinecap="round" /><circle cx={260} cy={260} r={16} fill={P.navy} />
          {[0, 50, 100].map((v) => { const [x, y] = pt(v, 250); return <text key={v} x={x} y={y + 6} textAnchor="middle" fontFamily="PlexMono" fontWeight={700} fontSize={20} fill="#6b625a">{v}%</text>; })}
        </svg>
        <div style={{ textAlign: 'center', fontFamily: 'Anton', fontSize: 92, color: P.coral, lineHeight: 1, marginTop: -40 }}>~{Math.round(g.valor * p)}%</div>
        {g.selo && t >= g.selo.t && <div style={{ marginTop: 14, textAlign: 'center' }}><span style={{ background: P.navy, color: P.branco, fontFamily: 'Anton', fontSize: 36, padding: '2px 22px', borderRadius: 4 }}>{g.selo.texto}</span></div>}
      </Painel>
    );
  }
  return null;
};
