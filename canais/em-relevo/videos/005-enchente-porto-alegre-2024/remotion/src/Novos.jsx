// Em Relevo 003 (13/11/2026): camadas 2D novas do vídeo da Grande Seca: papel de arquivo (sépia) e gráficos de dado.
// Dirigidas por cues.papeis e cues.graficos3 (shared/build_cues.py). Reusa a paleta do canal.
import React from 'react';
import { AbsoluteFill } from 'remotion';
import { pop, janela, clamp01, easeOut } from '../../shared/camadas.js';

const MONO = 'PlexMono, monospace';
const P = { papel: '#E9DCC3', coral: '#E8505B', navy: '#1F2A44', tinta: '#2B2622', branco: '#FBF8F1' };
const milhar = (n) => Math.round(n).toLocaleString('pt-BR');

const ItemPapel = ({ it, t }) => {
  const s = pop(t, it.t, 0.35);
  if (s <= 0) return null;
  if (it.tipo === 'data') return <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 40, letterSpacing: '0.2em', color: '#6b3b2a', transform: `scale(${s})` }}>{it.texto}</div>;
  if (it.tipo === 'numero') {
    const v = it.de + (it.para - it.de) * easeOut(clamp01((t - it.t) / (it.dur || 1.2)));
    return <div style={{ fontFamily: 'Anton', fontSize: it.tam || 240, lineHeight: 1, color: P.tinta, transform: `scale(${s})`, textShadow: '0 3px 0 rgba(255,255,255,0.35)' }}>{milhar(v)}</div>;
  }
  if (it.tipo === 'rotulo') return <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: it.tam || 34, letterSpacing: '0.16em', color: P.navy, background: 'rgba(251,248,241,0.7)', padding: '8px 22px', transform: `scale(${s})` }}>{it.texto}</div>;
  if (it.tipo === 'titulo') return <div style={{ fontFamily: 'Anton', fontSize: it.tam || 96, lineHeight: 1.08, color: P.tinta, textAlign: 'center', maxWidth: 1500, transform: `scale(${s})` }}>{it.texto}</div>;
  if (it.tipo === 'citacao') return (
    <div style={{ transform: `scale(${s})`, maxWidth: 1400, textAlign: 'center' }}>
      <div style={{ fontFamily: 'Playfair', fontStyle: 'italic', fontWeight: 600, fontSize: 70, lineHeight: 1.18, color: P.tinta }}>“{it.texto}”</div>
      {it.autor && <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: '0.14em', color: '#6b3b2a', marginTop: 18 }}>{it.autor}</div>}
    </div>
  );
  if (it.tipo === 'carimbo') {
    const p = clamp01((t - it.t) / 0.22);
    return <div style={{ transform: `rotate(-6deg) scale(${2.2 - 1.2 * easeOut(p)})`, opacity: p, border: `7px solid ${P.coral}`, color: P.coral, fontFamily: 'Anton', fontSize: it.tam || 72, padding: '0 26px', borderRadius: 8, background: 'rgba(251,248,241,0.5)', whiteSpace: 'nowrap' }}>{it.texto}</div>;
  }
  if (it.tipo === 'barras') return (
    <div style={{ width: 1100, transform: `scale(${s})`, transformOrigin: 'center' }}>
      {it.itens.map(([rot, v, tb, cor], i) => {
        const p = easeOut(clamp01((t - tb) / 0.9));
        return (
          <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 16, margin: '10px 0', opacity: t >= tb ? 1 : 0 }}>
            <div style={{ width: 200, fontFamily: MONO, fontWeight: 700, fontSize: 28, color: P.tinta }}>{rot}</div>
            <div style={{ flex: 1, height: 58, background: 'rgba(31,42,68,0.1)' }}><div style={{ width: `${(v / it.max) * 100 * p}%`, height: '100%', background: cor || P.coral }} /></div>
            <div style={{ width: 170, fontFamily: 'Anton', fontSize: 50, color: cor || P.coral }}>{milhar(v * p)}</div>
          </div>
        );
      })}
    </div>
  );
  if (it.tipo === 'fichas') return (
    <div style={{ display: 'flex', gap: 22, flexWrap: 'wrap', justifyContent: 'center', maxWidth: 1600 }}>
      {it.itens.map(([txt, tf], i) => { const sf = pop(t, tf, 0.35); if (sf <= 0) return null;
        return <div key={i} style={{ transform: `scale(${sf}) rotate(${(i % 2 ? 1 : -1) * 1.6}deg)`, background: P.branco, color: P.tinta, fontFamily: 'Anton', fontSize: 50, padding: '18px 28px', boxShadow: '0 10px 26px rgba(0,0,0,0.35)' }}>{txt}</div>; })}
    </div>
  );
  return null;
};

export const PapeisCamada = ({ t, papeis }) => (
  <>
    {papeis.map((pp, k) => {
      const a = janela(t, pp.t0, pp.t1, 0.12, 0.12);
      if (a <= 0) return null;
      return (
        <AbsoluteFill key={k} style={{ opacity: Math.min(1, a * 2) }}>
          <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 45%, #E5D3AA 0%, #D2BC8D 60%, #A98F62 100%)' }} />
          <AbsoluteFill style={{ opacity: 0.18, backgroundImage: 'repeating-linear-gradient(0deg, rgba(90,60,30,0.5) 0 1px, transparent 1px 7px)' }} />
          <AbsoluteFill style={{ top: pp.topo ? 110 : 130, bottom: 190, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: pp.topo ? 'flex-start' : 'center', gap: 26 }}>
            {pp.itens.map((it, i) => <ItemPapel key={i} it={it} t={t} />)}
          </AbsoluteFill>
        </AbsoluteFill>
      );
    })}
  </>
);

// ---- gráficos de dado (painéis de papel, mesmo estilo do longo-02)
const Painel = ({ a, children, left = 110, top = 220, w = 1100, titulo, fonte }) => (
  <div style={{ position: 'absolute', left, top, width: w, transform: `scale(${a})`, transformOrigin: 'left center', background: '#F3EEE3', borderRadius: 6,
    boxShadow: '0 20px 50px rgba(0,0,0,0.42)', padding: '24px 30px 20px', fontFamily: MONO, color: P.tinta }}>
    {titulo && <div style={{ fontWeight: 700, fontSize: 21, letterSpacing: '0.12em', color: P.navy, marginBottom: 16 }}>{titulo}</div>}
    {children}
    {fonte && <div style={{ fontWeight: 500, fontSize: 14, letterSpacing: '0.1em', color: '#7a7066', marginTop: 14 }}>FONTE: {fonte}</div>}
  </div>
);
export const Grafico3 = ({ g, t }) => {
  const a = janela(t, g.t0, g.t1, 0.45, 0.35);
  if (a <= 0) return null;
  if (g.tipo === 'chuva') {
    const n = g.anos.length, wv = 1180, hv = 330, max = g.max;
    const p = clamp01((t - g.t_ini) / g.dur); const a0 = g.anos[0][0], span = 2018 - a0 + 1;
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={1240} left={340} top={250}>
        <svg width={wv} height={hv + 36}>
          {g.anos.map(([ano, mm], i) => {
            if ((ano - a0) / span > p) return null;
            const h = (mm / max) * hv, dest = ano === 1877 || ano === 1878;
            const on = dest && t >= (ano === 1877 ? g.t_1877 : g.t_1878);
            return <rect key={ano} x={((ano - a0) / span) * wv} width={wv / span - 1} y={hv - h} height={h} fill={on ? P.coral : dest ? '#A99C8A' : '#7FA2C9'} />;
          })}
          <line x1={0} x2={wv} y1={hv - (g.media / max) * hv} y2={hv - (g.media / max) * hv} stroke={P.navy} strokeWidth={3} strokeDasharray="10 8" />
          <text x={wv - 4} y={hv - (g.media / max) * hv - 8} textAnchor="end" fontFamily="PlexMono" fontWeight={700} fontSize={19} fill={P.navy} stroke="#F3EEE3" strokeWidth={6} paintOrder="stroke">MÉDIA {milhar(g.media)} MM</text>
          {[1850, 1900, 1950, 2000].map((ano) => <text key={ano} x={Math.max(0, ((ano - a0) / span) * wv - 20)} y={hv + 28} fontFamily="PlexMono" fontSize={17} fill="#6b625a">{ano}</text>)}
          {t >= g.t_1877 && <text x={((1877 - a0) / span) * wv} y={30} textAnchor="middle" fontFamily="Anton" fontSize={34} fill={P.coral} stroke="#F3EEE3" strokeWidth={7} paintOrder="stroke">1877 · {g.mm1877} MM</text>}
        </svg>
      </Painel>
    );
  }
  if (g.tipo === 'estimativas') {
    const x = (v) => (v / g.max) * 1000;
    const p = easeOut(clamp01((t - g.t_ini) / 1.2));
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={1150} left={385} top={560}>
        <div style={{ position: 'relative', height: 120 }}>
          <div style={{ position: 'absolute', left: 0, top: 50, width: 1000, height: 28, background: 'rgba(31,42,68,0.1)' }} />
          <div style={{ position: 'absolute', left: x(g.de) , top: 50, width: x(g.para - g.de) * p, height: 28, background: 'linear-gradient(90deg, #E8505B, rgba(232,80,91,0.25))' }} />
          {g.marcas.map(([v, txt, tm], i) => t >= tm && (
            <div key={i} style={{ position: 'absolute', left: x(v) - 3, top: 20, height: 90, borderLeft: `6px solid ${P.navy}` }}>
              <div style={{ position: 'absolute', top: i % 2 ? 76 : -8, left: 10, whiteSpace: 'nowrap', fontWeight: 700, fontSize: 24, color: P.navy }}>{txt}</div>
            </div>
          ))}
        </div>
      </Painel>
    );
  }
  if (g.tipo === 'meses') {
    const R = 150, cx = 190, cy = 190;
    const MM = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={470} left={1330} top={230}>
        <svg width={380} height={380}>
          {MM.map((m, i) => {
            const a0 = (i / 12) * 2 * Math.PI - Math.PI / 2, a1 = ((i + 1) / 12) * 2 * Math.PI - Math.PI / 2;
            const x0 = cx + R * Math.cos(a0), y0 = cy + R * Math.sin(a0), x1 = cx + R * Math.cos(a1), y1 = cy + R * Math.sin(a1);
            const chuva = i >= 1 && i <= 4, on = chuva && t >= g.t_chuva, duvida = on && g.duvida;
            const am = (a0 + a1) / 2;
            return (
              <g key={i}>
                <path d={`M${cx} ${cy} L${x0} ${y0} A${R} ${R} 0 0 1 ${x1} ${y1} Z`} fill={on ? (duvida ? '#E9C46A' : '#5B86B8') : '#D9CDB6'} stroke="#F3EEE3" strokeWidth={3} />
                <text x={cx + (R + 24) * Math.cos(am)} y={cy + (R + 24) * Math.sin(am) + 7} textAnchor="middle" fontFamily="PlexMono" fontWeight={700} fontSize={20} fill={P.tinta}>{m}</text>
              </g>
            );
          })}
          <circle cx={cx} cy={cy} r={56} fill="#F3EEE3" />
          <text x={cx} y={cy + 12} textAnchor="middle" fontFamily="Anton" fontSize={34} fill={P.navy}>{g.centro}</text>
        </svg>
      </Painel>
    );
  }
  if (g.tipo === 'secas') {
    const x = (v) => ((v - g.a0) / (g.a1 - g.a0)) * 1000;
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={1150} left={385} top={330}>
        <div style={{ position: 'relative', height: 190 }}>
          <div style={{ position: 'absolute', left: 0, top: 120, width: 1000, borderTop: '4px solid #6b625a' }} />
          {g.eventos.map(([ano, txt, tm, forte], i) => { const s = pop(t, tm, 0.4); if (s <= 0) return null;
            return (
              <div key={i} style={{ position: 'absolute', left: x(ano) - 8, top: forte ? 10 : 70, transform: `scale(${s})`, transformOrigin: 'bottom left' }}>
                <div style={{ fontFamily: 'Anton', fontSize: forte ? 54 : 38, color: forte ? P.coral : P.navy }}>{txt}</div>
                <div style={{ width: 16, height: 16, borderRadius: 8, background: forte ? P.coral : P.navy, marginTop: forte ? 56 : 14 }} />
              </div>); })}
        </div>
      </Painel>
    );
  }
  if (g.tipo === 'populacao') {
    const p = easeOut(clamp01((t - g.t_ini) / 1.2));
    const w1 = (g.a / g.b) * 900;
    return (
      <Painel a={a} titulo={g.titulo} fonte={g.fonte} w={1100} left={60} top={560}>
        <div style={{ margin: '10px 0', display: 'flex', alignItems: 'center', gap: 14 }}><div style={{ width: w1, height: 46, background: P.navy }} /><span style={{ fontFamily: 'Anton', fontSize: 44, color: P.navy }}>{g.rotA}</span></div>
        <div style={{ margin: '10px 0', display: 'flex', alignItems: 'center', gap: 14 }}><div style={{ width: 900 * p, height: 46, background: P.coral }} /><span style={{ fontFamily: 'Anton', fontSize: 44, color: P.coral }}>{p > 0.9 ? g.rotB : ''}</span></div>
      </Painel>
    );
  }
  return null;
};
