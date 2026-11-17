// Em Relevo 006: cenas de tela cheia (blocos 3D cortados, fotos, documentos, esquemas, cards). Dirigidas por cues.cenas.
import React, { useMemo } from 'react';
import { AbsoluteFill, Img, staticFile } from 'remotion';
import blocos3d from '../public/v6/blocos3d.json';
import { pop, clamp01, easeOut } from '../../shared/camadas.js';
import { P, MONO, win } from './util6.js';

const Fundo = ({ a, v = 0.6 }) => <AbsoluteFill style={{ background: `rgba(10,16,34,${v * a})` }} />;
const Etq = ({ children, style }) => <div style={{ position: 'absolute', background: P.navy, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.1em', padding: '9px 18px', borderRadius: 4, boxShadow: '0 6px 18px rgba(0,0,0,0.45)', whiteSpace: 'nowrap', ...style }}>{children}</div>;
const Legenda = ({ texto, w = 1240 }) => <div style={{ width: w, background: P.coral, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 25, letterSpacing: '0.12em', padding: '9px 20px', boxSizing: 'border-box' }}>{texto}</div>;
const kbStyle = (kb, p) => { const s = kb[2] + (kb[5] - kb[2]) * p, fx = kb[0] + (kb[3] - kb[0]) * p, fy = kb[1] + (kb[4] - kb[1]) * p; return { transform: `scale(${s})`, transformOrigin: `${fx * 100}% ${fy * 100}%` }; };

// ---------------------------------------------------------------- foto grande / dupla / documento
const Foto = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.35, 0.35), p = clamp01((t - c.t0) / Math.max(0.1, c.t1 - c.t0));
  return <><Fundo a={a} v={0.62} />
    <div style={{ position: 'absolute', left: 340, top: 120, opacity: a, transform: `scale(${0.96 + 0.04 * easeOut(clamp01((t - c.t0) / 0.5))})`, boxShadow: '0 24px 60px rgba(0,0,0,0.6)' }}>
      <div style={{ width: 1240, height: 698, overflow: 'hidden', background: '#000' }}><Img src={staticFile('fotos/' + c.arq)} style={{ width: '100%', height: '100%', objectFit: 'cover', ...kbStyle(c.kb, p) }} /></div>
      <Legenda texto={c.legenda} />
    </div></>;
};
const Dupla = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.35, 0.35), p = clamp01((t - c.t0) / Math.max(0.1, c.t1 - c.t0));
  return <><Fundo a={a} v={0.7} />
    {c.arqs.map((arq, i) => <div key={i} style={{ position: 'absolute', left: 70 + i * 930, top: 150, opacity: a, boxShadow: '0 24px 60px rgba(0,0,0,0.6)', transform: `translateX(${(1 - easeOut(clamp01((t - c.t0) / 0.6))) * (i ? 120 : -120)}px)` }}>
      <div style={{ width: 850, height: 640, overflow: 'hidden', background: '#000' }}><Img src={staticFile('fotos/' + arq)} style={{ width: '100%', height: '100%', objectFit: 'cover', ...kbStyle(i ? [0.45, 0.65, 1.0, 0.5, 0.68, 1.35] : [0.5, 0.3, 1.0, 0.5, 0.55, 1.15], p) }} /></div>
      <Legenda texto={c.leg[i]} w={850} />
      <Etq style={{ left: 18, top: 18 }}>{c.rots[i]}</Etq>
    </div>)}</>;
};
const Doc = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.4, 0.4), p = clamp01((t - c.t0) / Math.max(0.1, c.t1 - c.t0));
  return <><AbsoluteFill style={{ background: `linear-gradient(135deg, ${P.papel}, #D9C9A4)`, opacity: a }} />
    <div style={{ position: 'absolute', left: 520, top: 36, width: 880, opacity: a, transform: `rotate(${c.inclina ? -2.2 : 0}deg) translateY(${(1 - easeOut(clamp01((t - c.t0) / 0.7))) * 80}px)`, boxShadow: '0 22px 50px rgba(60,40,10,0.45)', background: '#fff' }}>
      <div style={{ width: 880, height: 920, overflow: 'hidden' }}><Img src={staticFile('fotos/' + c.arq)} style={{ width: '100%', height: '100%', objectFit: 'cover', ...kbStyle(c.kb, p) }} /></div>
      <div style={{ background: P.coral, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.12em', padding: '8px 18px' }}>{c.legenda}</div>
    </div>
    {c.rot && <Etq style={{ left: 120, top: 220, opacity: a }}>{c.rot}</Etq>}
    {(c.tags || []).map(([t0, tx, i], k) => t >= t0 && <div key={k} style={{ position: 'absolute', left: 90, top: 300 + i * 190, transform: `scale(${pop(t, t0, 0.4)})`, transformOrigin: 'left center', background: i ? P.navy : P.coral, color: P.branco, fontFamily: 'Anton', fontSize: 44, padding: '8px 22px', borderRadius: 4, boxShadow: '0 8px 20px rgba(0,0,0,0.4)', opacity: a, maxWidth: 420 }}>{tx}</div>)}
  </>;
};

// ---------------------------------------------------------------- bloco 3D cortado (a assinatura do vídeo)
const mix = (a, b, f) => a.map((v, i) => v + (b[i] - v) * f);
const hex = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
const COR_PLANO = hex('#A8B27A'), COR_MATA = hex('#3E7040'), COR_TOPO = hex('#55804A');
const geomBloco = (chave, W, ex) => {
  const d = blocos3d[chave], z = d.z, nj = z.length, ni = z[0].length, Lk = d.km1 - d.km0, kx = W / Lk;
  const depthX = d.largura_km * kx * 0.34, depthY = d.largura_km * kx * 0.27, zmax = Math.max(...z.flat());
  const Ybase = zmax * ex + depthY + 24, rock = 80, mx = 120;
  const X = (i, j) => mx + i / (ni - 1) * W + j / (nj - 1) * depthX;
  const Y = (i, j, zz, g = 1) => Ybase - zz * ex * g - j / (nj - 1) * depthY;
  return { d, z, nj, ni, Lk, kx, depthX, depthY, zmax, Ybase, rock, mx, X, Y, Wsvg: mx + W + depthX + 40, Hsvg: Ybase + rock + 130, km: (i) => d.km0 + Lk * i / (ni - 1) };
};
export const Bloco3D = ({ chave, W, g = 1, rp = 0, casca = 0, arvores = 0, rot, ano, kmR, hR, extra, exag = 2.5, faceCor }) => {
  const G = useMemo(() => geomBloco(chave, W, exag * (W / (blocos3d[chave].km1 - blocos3d[chave].km0)) / 1000), [chave, W, exag]);
  const { z, nj, ni, X, Y, Ybase, rock, Wsvg, Hsvg } = G;
  const cores = useMemo(() => {
    const out = [];
    for (let j = nj - 2; j >= 0; j--) for (let i = 0; i < ni - 1; i++) {
      const za = (z[j][i] + z[j][i + 1] + z[j + 1][i] + z[j + 1][i + 1]) / 4; if (za <= 0.6) { out.push([j, i, '#1C5F85']); continue; }
      const dz = z[j][i + 1] - z[j][i], lit = Math.min(0.95, Math.max(0.15, 0.55 - dz / 110));
      const base = za < 40 ? mix(COR_PLANO, COR_MATA, za / 40 * 0.25) : mix(COR_MATA, COR_TOPO, Math.min(1, Math.max(0, (za - 300) / 500)));
      const k = 0.5 + 0.75 * lit; out.push([j, i, `rgb(${Math.min(255, base[0] * k) | 0},${Math.min(255, base[1] * k) | 0},${Math.min(255, base[2] * k) | 0})`]);
    }
    return out;
  }, [chave]);
  const topo = (i) => `${X(i, 0)},${Y(i, 0, Math.max(z[0][i], 0), g)}`;
  const fp = []; for (let i = 0; i < ni; i++) fp.push([X(i, 0), Y(i, 0, Math.max(z[0][i], 0), g)]);
  const rockBase = Ybase + rock;
  const xs = (i) => X(i, 0);
  const iR = Math.round(((kmR - G.d.km0) / G.Lk) * (ni - 1));
  const yv0 = Y(iR, 0, 0, 1), yv1 = Y(iR, 0, hR, 1), xv = xs(iR) - 40;
  const i0 = Math.round(((0 - G.d.km0) / G.Lk) * (ni - 1)); const yh = rockBase + 44;
  const rv = easeOut(clamp01(rp)), rh = easeOut(clamp01(rp * 1.2));
  const soloEsp = 10;
  return (
    <svg width={Wsvg} height={Hsvg} style={{ overflow: 'visible' }}>
      <defs>
        <linearGradient id={'rk' + chave} x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor={faceCor || '#8A8782'} /><stop offset="1" stopColor={faceCor ? '#8C7A55' : '#4B4947'} /></linearGradient>
      </defs>
      {/* superfície, de trás para a frente */}
      {cores.map(([j, i, cor], k) => <polygon key={k} points={`${X(i, j + 1)},${Y(i, j + 1, z[j + 1][i], g)} ${X(i + 1, j + 1)},${Y(i + 1, j + 1, z[j + 1][i + 1], g)} ${X(i + 1, j)},${Y(i + 1, j, z[j][i + 1], g)} ${X(i, j)},${Y(i, j, z[j][i], g)}`} fill={cor} stroke={cor} strokeWidth={0.6} />)}
      {/* lado direito (extremo da serra) */}
      <polygon points={[...Array(nj).keys()].map((j) => `${X(ni - 1, j)},${Y(ni - 1, j, z[j][ni - 1], g)}`).join(' ') + ` ${X(ni - 1, nj - 1)},${Y(ni - 1, nj - 1, -80)} ${X(ni - 1, 0)},${rockBase}`} fill="#5C5A56" />
      {/* face do corte (frente) */}
      <polygon points={fp.map((q) => q.join(',')).join(' ') + ` ${X(ni - 1, 0)},${rockBase} ${X(0, 0)},${rockBase}`} fill={`url(#rk${chave})`} />
      {/* mar na frente */}
      <polygon points={[...Array(ni).keys()].map((i) => `${X(i, 0)},${Y(i, 0, 0, 1)}`).join(' ') + ' ' + [...Array(ni).keys()].reverse().map((i) => `${X(i, 0)},${Y(i, 0, Math.max(Math.min(z[0][i], 0), -9999), g)}`).join(' ')} fill="#1C5F85" opacity="0.95" />
      {/* casca: faixa marrom fina sobre a rocha (exagerada) */}
      <polygon points={fp.filter((_, i) => z[0][i] > 6).map((q) => q.join(',')).join(' ') + ' ' + fp.filter((_, i) => z[0][i] > 6).reverse().map((q) => `${q[0]},${q[1] + soloEsp}`).join(' ')} fill="#9A6B3F" stroke={casca > 0 ? P.amarelo : 'none'} strokeWidth={casca > 0 ? 3 : 0} opacity={0.98} />
      <polyline points={fp.map((q) => q.join(',')).join(' ')} fill="none" stroke="#2A3A22" strokeWidth={2} />
      {/* árvores-palito sobre a casca */}
      {arvores > 0 && fp.filter((_, i) => i % 5 === 2 && z[0][i] > 30).map((q, k) => <g key={k} opacity={arvores}><line x1={q[0]} y1={q[1]} x2={q[0]} y2={q[1] - 26} stroke="#3E2A18" strokeWidth={3} /><ellipse cx={q[0]} cy={q[1] - 36} rx={11} ry={17} fill="#2F6B36" /></g>)}
      {/* réguas: 0 → hR (vertical) e 0 → kmR (horizontal) */}
      <g opacity={rv > 0 ? 1 : 0}>
        <line x1={xv} y1={yv0} x2={xv} y2={yv0 + (yv1 - yv0) * rv} stroke={P.amarelo} strokeWidth={6} />
        <line x1={xv - 14} y1={yv0} x2={xv + 14} y2={yv0} stroke={P.amarelo} strokeWidth={6} /><line x1={xv - 14} y1={yv0 + (yv1 - yv0) * rv} x2={xv + 14} y2={yv0 + (yv1 - yv0) * rv} stroke={P.amarelo} strokeWidth={6} />
        <text x={xv - 22} y={(yv0 + yv0 + (yv1 - yv0) * rv) / 2 + 16} textAnchor="end" fontFamily="Anton" fontSize={52} fill={P.amarelo} stroke="#0E1426" strokeWidth={6} paintOrder="stroke">{Math.round(hR * rv)} M</text>
      </g>
      <g opacity={rh > 0 ? 1 : 0}>
        <line x1={xs(i0)} y1={yh} x2={xs(i0) + (xs(iR) - xs(i0)) * rh} y2={yh} stroke={P.amarelo} strokeWidth={6} />
        <line x1={xs(i0)} y1={yh - 14} x2={xs(i0)} y2={yh + 14} stroke={P.amarelo} strokeWidth={6} /><line x1={xs(i0) + (xs(iR) - xs(i0)) * rh} y1={yh - 14} x2={xs(i0) + (xs(iR) - xs(i0)) * rh} y2={yh + 14} stroke={P.amarelo} strokeWidth={6} />
        <text x={(xs(i0) + xs(i0) + (xs(iR) - xs(i0)) * rh) / 2} y={yh + 54} textAnchor="middle" fontFamily="Anton" fontSize={50} fill={P.amarelo} stroke="#0E1426" strokeWidth={6} paintOrder="stroke">{(kmR * rh).toFixed(1).replace('.', ',')} KM</text>
      </g>
      {casca > 0 && <g opacity={casca}><line x1={xs(Math.round(ni * 0.84))} y1={Y(Math.round(ni * 0.84), 0, Math.max(0, z[0][Math.round(ni * 0.84)]))} x2={xs(Math.round(ni * 0.84)) - 120} y2={Y(Math.round(ni * 0.84), 0, z[0][Math.round(ni * 0.84)]) - 150} stroke={P.amarelo} strokeWidth={4} />
        <text x={xs(Math.round(ni * 0.84)) - 128} y={Y(Math.round(ni * 0.84), 0, z[0][Math.round(ni * 0.84)]) - 160} textAnchor="end" fontFamily="Anton" fontSize={46} fill="#C98B52" stroke="#0E1426" strokeWidth={6} paintOrder="stroke">CASCA · 1 A 2,5 M</text></g>}
      {extra}
    </svg>
  );
};
const TituloBloco = ({ ano, nome, x, y, w }) => <div style={{ position: 'absolute', left: x, top: y, width: w }}>
  <div style={{ display: 'inline-block', background: P.coral, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.14em', padding: '6px 14px', borderRadius: 4 }}>{ano}</div>
  <div style={{ fontFamily: 'Anton', fontSize: 58, color: P.branco, lineHeight: 1.05, marginTop: 6, textShadow: '0 4px 14px rgba(0,0,0,0.8)' }}>{nome}</div></div>;
const Bloco = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.25, 0.4), g = easeOut(clamp01((t - c.t0) / 1.5)), rp = clamp01((t - c.t0 - 0.9) / 1.6);
  const CR = { chave: 'cruzeiro', kmR: 5.7, hR: 700 }, SA = { chave: 'sahy', kmR: 5.4, hR: 685 };
  const base = { background: 'linear-gradient(180deg, rgba(10,16,34,0.92), rgba(18,28,56,0.95))' };
  if (c.modo === 'dois') return <AbsoluteFill style={{ opacity: a, ...base }}>
    <TituloBloco ano="2023" nome="BARRA DO SAHY · SÃO SEBASTIÃO" x={40} y={120} w={900} />
    <div style={{ position: 'absolute', left: -60, top: 300 }}><Bloco3D {...SA} W={800} g={g} rp={rp} /></div>
    <TituloBloco ano="1967" nome="MORRO DO CRUZEIRO · CARAGUATATUBA" x={990} y={120} w={900} />
    <div style={{ position: 'absolute', left: 930, top: 300 }}><Bloco3D {...CR} W={800} g={g} rp={rp} /></div>
  </AbsoluteFill>;
  if (c.modo === 'face') {
    const tz = c.t_zoom, tp = tz + 2.6, tr = c.t_recua;
    const zoomP = easeOut(clamp01((t - tz) / 2.4)) * (1 - easeOut(clamp01((t - tr) / 1.2)));
    const painel = win(t, tp, tr - 0.2, 0.5, 0.5);
    const arv = clamp01((t - c.t_planta) / 0.8);
    const comp = clamp01((t - c.t_comp) / 0.9);
    return <AbsoluteFill style={{ opacity: a, ...base }}>
      <TituloBloco ano="1967" nome="MORRO DO CRUZEIRO · CARAGUATATUBA" x={60} y={100} w={1000} />
      <div style={{ position: 'absolute', left: 40, top: 300, transformOrigin: '1080px 380px', transform: `scale(${1 + 0.8 * zoomP})` }}>
        <Bloco3D {...CR} W={1130} g={1} rp={1} casca={clamp01((t - tz) / 0.6)} arvores={arv} /></div>
      {painel > 0 && <div style={{ position: 'absolute', left: 120, top: 200, width: 1180, height: 640, background: 'rgba(24,34,62,0.97)', borderRadius: 10, opacity: painel, boxShadow: '0 20px 60px rgba(0,0,0,0.6)', border: '2px solid rgba(255,255,255,0.15)' }}>
        <div style={{ position: 'absolute', left: 36, top: 22, fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.16em', color: P.amarelo }}>CORTE DA ENCOSTA · ILUSTRATIVO · ESCALA EM METROS</div>
        <div style={{ position: 'absolute', left: 250, top: 90, width: 700, height: 450, overflow: 'hidden' }}>
          <div style={{ position: 'absolute', left: 0, top: 0, width: '100%', height: 160 * easeOut(clamp01((t - tp) / 0.8)), background: 'linear-gradient(180deg,#B88A5A,#8F5E36)', borderBottom: `6px solid ${P.coral}` }} />
          <div style={{ position: 'absolute', left: 0, top: 160, width: '100%', bottom: 0, background: 'linear-gradient(180deg,#8A8782,#4B4947)', opacity: easeOut(clamp01((t - tp - 0.3) / 0.8)) }} />
        </div>
        <svg style={{ position: 'absolute', left: 150, top: 90 }} width={100} height={520}><line x1={90} y1={0} x2={90} y2={160} stroke={P.amarelo} strokeWidth={6} />{[0, 1, 2, 2.5].map((m) => <g key={m}><line x1={70} y1={m * 64} x2={90} y2={m * 64} stroke={P.amarelo} strokeWidth={5} /><text x={60} y={m * 64 + 12} textAnchor="end" fontFamily="Anton" fontSize={34} fill={P.amarelo}>{String(m).replace('.', ',')}</text></g>)}</svg>
        <div style={{ position: 'absolute', left: 970, top: 110, width: 190, fontFamily: MONO, fontWeight: 700, fontSize: 22, letterSpacing: '0.06em', color: P.branco, lineHeight: 1.3 }}>ROCHA DECOMPOSTA E TERRA</div>
        <div style={{ position: 'absolute', left: 970, top: 330, width: 190, fontFamily: MONO, fontWeight: 700, fontSize: 22, letterSpacing: '0.06em', color: '#CFCBC4', lineHeight: 1.3 }}>GRANITO E GNAISSE</div>
        <div style={{ position: 'absolute', left: 250, top: 565, fontFamily: 'Anton', fontSize: 42, color: P.coral, opacity: easeOut(clamp01((t - tp - 1.2) / 0.6)) }}>PLANO DE RUPTURA · 1 A 2,5 M</div>
      </div>}
      {comp > 0 && <div style={{ position: 'absolute', right: 70, top: 160, width: 420, opacity: comp * (1 - clamp01((t - c.t1) / 0.4)), background: 'rgba(24,34,62,0.95)', borderRadius: 8, padding: '18px 24px', boxShadow: '0 12px 30px rgba(0,0,0,0.5)' }}>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 21, letterSpacing: '0.12em', color: P.amarelo, marginBottom: 12 }}>SERRA × CASCA</div>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: 40, height: 480, paddingTop: 120 }}>
          <div style={{ width: 80, height: 340 * comp, background: '#6D6A66', position: 'relative' }}><div style={{ position: 'absolute', top: -46, left: -8, fontFamily: 'Anton', fontSize: 40, color: P.branco, whiteSpace: 'nowrap' }}>700 M</div></div>
          <div style={{ width: 80, height: Math.max(3, 340 * (2.5 / 700) * comp), background: '#9A6B3F', position: 'relative' }}><div style={{ position: 'absolute', top: -120, left: -4, fontFamily: 'Anton', fontSize: 40, color: '#E3B183', whiteSpace: 'nowrap' }}>2,5 M<br />DE CASCA</div></div>
        </div>
      </div>}
    </AbsoluteFill>;
  }
  const ch = c.modo === 'cruzeiro' ? CR : SA;
  const cascaOn = c.casca_t ? clamp01((t - c.casca_t) / 0.5) * (1 - clamp01((t - c.casca_t - 4.5) / 0.6)) : 0;
  return <AbsoluteFill style={{ opacity: a, ...base }}>
    <TituloBloco ano={c.modo === 'cruzeiro' ? '1967' : '2023'} nome={c.modo === 'cruzeiro' ? 'MORRO DO CRUZEIRO · CARAGUATATUBA' : 'BARRA DO SAHY · SÃO SEBASTIÃO'} x={60} y={100} w={1100} />
    <div style={{ position: 'absolute', left: 20, top: 310 }}><Bloco3D {...ch} W={1130} g={g} rp={rp} casca={cascaOn} /></div>
  </AbsoluteFill>;
};

// ---------------------------------------------------------------- pluviômetros e fichas
const Tubo = ({ x, y, w = 150, h = 640, frac, cor = '#3FD8FF', marcas = [], rotulo, sub, transborda }) => {
  const f = Math.min(1, frac);
  return <div style={{ position: 'absolute', left: x, top: y, width: w, height: h }}>
    <div style={{ position: 'absolute', left: 0, top: 0, width: w, height: h, border: '6px solid rgba(251,248,241,0.9)', borderTop: 'none', borderRadius: '0 0 28px 28px', overflow: 'hidden', background: 'rgba(251,248,241,0.1)' }}>
      <div style={{ position: 'absolute', left: 0, bottom: 0, width: '100%', height: h * f, background: `linear-gradient(180deg, ${cor}, #1b8fb5)` }} />
    </div>
    {marcas.map(([fr, tx, cc], i) => <div key={i} style={{ position: 'absolute', left: -150, top: h * (1 - fr) - 2, width: w + 190, borderTop: `4px dashed ${cc || P.amarelo}` }}><span style={{ position: 'absolute', left: 0, top: -34, fontFamily: MONO, fontWeight: 700, fontSize: 22, color: cc || P.amarelo, letterSpacing: '0.08em' }}>{tx}</span></div>)}
    {rotulo && <div style={{ position: 'absolute', left: -60, top: h + 18, width: w + 120, textAlign: 'center' }}><div style={{ fontFamily: 'Anton', fontSize: 54, color: P.branco, lineHeight: 1 }}>{rotulo}</div><div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 20, letterSpacing: '0.1em', color: '#BFD0F0', marginTop: 4 }}>{sub}</div></div>}
  </div>;
};
const Pluv = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.35, 0.4), p = easeOut(clamp01((t - c.t_ini) / (c.t_fim - c.t_ini))), v = Math.round(400 * p);
  const horas = (6 * p).toFixed(1).replace('.', ',');
  return <AbsoluteFill style={{ opacity: a, background: 'linear-gradient(180deg, rgba(10,16,34,0.93), rgba(18,28,56,0.95))' }}>
    <div style={{ position: 'absolute', left: 140, top: 110, fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: '0.16em', color: P.ciano }}>PLUVIÔMETRO · BERTIOGA (SP) · 18–19 FEV 2023</div>
    <Tubo x={760} y={150} h={560} frac={p} marcas={t >= c.marca_t ? [[c.marca / 450, 'MÉDIA DE FEVEREIRO · 225 MM', '#FFD23F']] : []} rotulo={`${v} MM`} sub="EM 6 HORAS" />
    <div style={{ position: 'absolute', left: 1130, top: 250, width: 640 }}>
      <div style={{ fontFamily: 'Anton', fontSize: 190, color: P.branco, lineHeight: 1 }}>{v}<span style={{ fontSize: 70 }}> MM</span></div>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 34, letterSpacing: '0.12em', color: P.ciano, marginTop: 8 }}>{horas} H DE CHUVA</div>
      {t >= c.recorde_t && <div style={{ marginTop: 50, transform: `scale(${pop(t, c.recorde_t, 0.45)})`, transformOrigin: 'left center', background: P.coral, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: '0.1em', padding: '14px 22px', borderRadius: 6, lineHeight: 1.35 }}>MAIOR ACUMULADO EM 24 H<br />JÁ MEDIDO NO PAÍS (CEMADEN)</div>}
    </div>
  </AbsoluteFill>;
};
const Ficha1967 = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.4, 0.4), p17 = easeOut(clamp01((t - c.t17) / 1.2)), p18 = easeOut(clamp01((t - c.t18) / 1.6)), tr = t >= c.t_trans;
  return <AbsoluteFill style={{ opacity: a }}>
    <AbsoluteFill style={{ background: `linear-gradient(135deg, ${P.papel}, #D6C49C)` }} />
    <div style={{ position: 'absolute', left: 200, top: 90, width: 1520, height: 760, background: '#F4EBD6', boxShadow: '0 20px 50px rgba(60,40,10,0.4)', border: '3px solid #8A7A58', padding: 30, transform: 'rotate(-0.8deg)' }}>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: '0.14em', color: P.tinta }}>FICHA DE PLUVIÔMETRO · FAZENDA · CARAGUATATUBA · MARÇO DE 1967</div>
      <div style={{ position: 'absolute', left: 280, top: 110, width: 160, height: 540, border: `5px solid ${P.tinta}`, borderTop: 'none', borderRadius: '0 0 30px 30px', overflow: 'hidden', background: 'rgba(255,255,255,0.5)' }}><div style={{ position: 'absolute', bottom: 0, width: '100%', height: 540 * (115 / 300) * p17, background: '#3D7FB8' }} /></div>
      <div style={{ position: 'absolute', left: 230, top: 650, width: 260, textAlign: 'center', fontFamily: 'Anton', fontSize: 62, color: P.tinta, lineHeight: 1 }}>{Math.round(115 * p17)} MM<div style={{ fontFamily: MONO, fontSize: 22, fontWeight: 700, letterSpacing: '0.1em' }}>17 / 03</div></div>
      <div style={{ position: 'absolute', left: 800, top: 110, width: 160, height: 540, border: `5px solid ${P.tinta}`, borderTop: 'none', borderRadius: '0 0 30px 30px', overflow: 'hidden', background: 'rgba(255,255,255,0.5)' }}><div style={{ position: 'absolute', bottom: 0, width: '100%', height: 540 * Math.min(1, (420 / 300) * p18), background: '#3D7FB8' }} /></div>
      {tr && <div style={{ position: 'absolute', left: 740, top: 60, width: 280, height: 90, background: 'repeating-linear-gradient(90deg, #3D7FB8 0 10px, transparent 10px 24px)', opacity: 0.8, clipPath: 'polygon(0 100%, 50% 0, 100% 100%)' }} />}
      <div style={{ position: 'absolute', left: 750, top: 650, width: 260, textAlign: 'center', fontFamily: 'Anton', fontSize: 62, color: P.tinta, lineHeight: 1 }}>{Math.round(420 * p18)} MM<div style={{ fontFamily: MONO, fontSize: 22, fontWeight: 700, letterSpacing: '0.1em' }}>18 / 03</div></div>
      {tr && <div style={{ position: 'absolute', left: 1090, top: 250, transform: `rotate(-8deg) scale(${2 - easeOut(clamp01((t - c.t_trans) / 0.25))})`, opacity: clamp01((t - c.t_trans) / 0.25), border: `8px solid ${P.coral}`, color: P.coral, fontFamily: 'Anton', fontSize: 84, padding: '0 22px', borderRadius: 8, lineHeight: 1.15 }}>O APARELHO<br />TRANSBORDOU</div>}
    </div>
  </AbsoluteFill>;
};
const Postos = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.4, 0.4), p1 = easeOut(clamp01((t - c.t0 - 0.5) / 1.4)), p2 = easeOut(clamp01((t - c.t_poucos) / 1.4));
  const pulso = t >= c.t_terceiro ? 1 : 0;
  return <AbsoluteFill style={{ opacity: a, background: 'linear-gradient(180deg, rgba(10,16,34,0.93), rgba(18,28,56,0.95))' }}>
    <div style={{ position: 'absolute', left: 140, top: 110, fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: '0.16em', color: P.ciano }}>DOIS PLUVIÔMETROS · MESMOS DOIS DIAS · POUCOS KM DE DISTÂNCIA</div>
    <Tubo x={430} y={250} h={430} frac={p1 * 0.95} rotulo="POSTO DA FAZENDA" sub="TRANSBORDOU" />
    <Tubo x={1030} y={250} h={430} frac={p2 * 0.42} rotulo="POSTO A POUCOS KM" sub="MENOS DA METADE" marcas={[[0.475, 'METADE', P.coral]]} />
    <div style={{ position: 'absolute', left: 0, top: 165, width: '100%', textAlign: 'center', fontFamily: 'Anton', fontSize: 50, color: P.branco, opacity: clamp01((t - c.t_valer + 3.5) / 0.5) }}>NA SERRA, A CHUVA MUDA DE VALE PARA VALE</div>
  </AbsoluteFill>;
};

// ---------------------------------------------------------------- esquemas
const CascaEsq = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.4, 0.4), gotas = clamp01((t - c.t_gotas) / 1.0), enc = clamp01((t - c.t_desliza + 0.8) / 1.2);
  const desliza = easeOut(clamp01((t - c.t_desliza - 0.8) / 2.6)), cola = 1 - easeOut(clamp01((t - c.t_cola) / 1.2)), sa = easeOut(clamp01((t - c.t_sa) / 1.0));
  const Rr = 700, ang = Math.atan2(340, 900);
  return <AbsoluteFill style={{ opacity: a, background: 'linear-gradient(180deg, rgba(10,16,34,0.93), rgba(18,28,56,0.95))' }}>
    <div style={{ position: 'absolute', left: 140, top: 110, fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: '0.16em', color: P.amarelo }}>ESQUEMA ILUSTRATIVO · ENCOSTA DA SERRA DO MAR</div>
    <svg width={1100} height={620} style={{ position: 'absolute', left: 120, top: 220 }}>
      <polygon points="0,560 1100,560 1100,330 0,40" fill="#6D6A66" />
      <g transform={`translate(${desliza * 520},${desliza * 520 * 0.31 + sa * 14})`}>
        <polygon points="0,40 1100,330 1100,330 0,40" fill="none" />
        <polygon points={`0,40 1100,330 1100,${330 + 70} 0,${40 + 70 + sa * 40}`} fill={`rgb(${150 - enc * 70},${107 - enc * 45},${63 - enc * 25})`} />
        {[...Array(14)].map((_, i) => <g key={i}><line x1={60 + i * 75} y1={40 + (60 + i * 75) * 0.264 - 8} x2={60 + i * 75} y2={40 + (60 + i * 75) * 0.264 - 44} stroke="#3E2A18" strokeWidth={4} /><ellipse cx={60 + i * 75} cy={40 + (60 + i * 75) * 0.264 - 58} rx={14} ry={22} fill="#2F6B36" /></g>)}
      </g>
      {gotas > 0 && [...Array(40)].map((_, i) => { const x = 20 + ((i * 97) % 1060), y = ((i * 53 + t * 380) % 300); return <line key={i} x1={x} y1={y} x2={x - 6} y2={y + 22} stroke="#8EDBFF" strokeWidth={3} opacity={gotas} />; })}
    </svg>
    <div style={{ position: 'absolute', left: 1320, top: 240, width: 480, background: 'rgba(24,34,62,0.97)', borderRadius: 10, padding: '20px 26px', boxShadow: '0 16px 40px rgba(0,0,0,0.5)', opacity: clamp01((t - c.t_cola + 0.6) / 0.5) }}>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 22, letterSpacing: '0.14em', color: P.amarelo }}>ENSAIO DE LABORATÓRIO</div>
      <svg width={420} height={230}><path d="M40,200 A170,170 0 0 1 380,200" fill="none" stroke="rgba(255,255,255,0.25)" strokeWidth={18} /><path d="M40,200 A170,170 0 0 1 380,200" fill="none" stroke={P.coral} strokeWidth={18} strokeDasharray="534" strokeDashoffset={534 * (1 - cola)} />
        <line x1={210} y1={200} x2={210 - 150 * Math.cos(Math.PI * (1 - cola))} y2={200 - 150 * Math.sin(Math.PI * (1 - cola))} stroke={P.branco} strokeWidth={8} strokeLinecap="round" /><circle cx={210} cy={200} r={14} fill={P.branco} /></svg>
      <div style={{ fontFamily: 'Anton', fontSize: 66, color: P.branco, lineHeight: 1 }}>COESÃO ≈ 0</div>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 21, letterSpacing: '0.08em', color: '#BFD0F0', marginTop: 4 }}>SOLO QUASE SEM COLA</div>
    </div>
    {sa > 0 && <div style={{ position: 'absolute', left: 140, top: 160, opacity: sa, fontFamily: 'Anton', fontSize: 44, color: P.coral, textShadow: '0 3px 10px rgba(0,0,0,0.6)' }}>A RUPTURA DESCE ATÉ A ROCHA SÃ</div>}
  </AbsoluteFill>;
};
const Fases = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.4, 0.4);
  const ICO = [<path key="0" d="M10,60 Q40,20 70,60 T130,60" fill="none" stroke="#3FD8FF" strokeWidth={10} />, <path key="1" d="M10,20 L130,70 L10,70 Z" fill="#9A6B3F" />, <g key="2"><path d="M10,25 L130,70" stroke="#A8693A" strokeWidth={26} strokeLinecap="round" /><circle cx={60} cy={45} r={9} fill="#3E2A18" /><circle cx={95} cy={58} r={9} fill="#3E2A18" /></g>, <g key="3"><rect x={20} y={20} width={30} height={50} fill="#3E2A18" /><rect x={50} y={30} width={30} height={40} fill="#3E2A18" /><path d="M0,70 Q60,40 140,70" fill="none" stroke="#3FD8FF" strokeWidth={10} /></g>];
  return <AbsoluteFill style={{ opacity: a, background: 'linear-gradient(180deg, rgba(10,16,34,0.93), rgba(18,28,56,0.95))' }}>
    <div style={{ position: 'absolute', left: 140, top: 130, fontFamily: 'Anton', fontSize: 100, color: P.coral }}>18 DE MARÇO DE 1967 · 4 FASES</div>
    {c.nomes.map((n, i) => <div key={i} style={{ position: 'absolute', left: 90 + i * 440, top: 340, width: 400, height: 430, transform: `scale(${pop(t, c.ts[i], 0.45)})`, background: P.branco, borderRadius: 10, boxShadow: '0 16px 40px rgba(0,0,0,0.5)', padding: 22, boxSizing: 'border-box', textAlign: 'center' }}>
      <div style={{ fontFamily: 'Anton', fontSize: 120, color: P.coral, lineHeight: 1 }}>{i + 1}</div>
      <svg width={140} height={90} style={{ margin: '8px 0' }}>{ICO[i]}</svg>
      <div style={{ fontFamily: 'Anton', fontSize: 52, color: P.tinta, lineHeight: 1.1 }}>{n}</div></div>)}
  </AbsoluteFill>;
};
const Lama = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.4, 0.4), r = easeOut(clamp01((t - c.t_rio) / 1.4)), l = easeOut(clamp01((t - c.t_lama) / 1.2)), tr = clamp01((t - c.t_troncos) / 1.0);
  return <AbsoluteFill style={{ opacity: a, background: 'linear-gradient(180deg, rgba(10,16,34,0.94), rgba(18,28,56,0.96))' }}>
    <div style={{ position: 'absolute', left: 120, top: 110, fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.14em', color: P.amarelo }}>RIO SANTO ANTÔNIO · LARGURA (ESQUEMA)</div>
    <div style={{ position: 'absolute', left: 120, top: 220, width: 780, height: 520, background: '#2B4A38' }}>
      <div style={{ position: 'absolute', left: 0, top: 260 - (15 + 65 * r) * 2.4, width: '100%', height: (15 + 65 * r) * 4.8, background: r > 0.05 ? '#A8693A' : '#3D7FB8', opacity: 0.95 }} />
      {tr > 0 && [...Array(18)].map((_, i) => <div key={i} style={{ position: 'absolute', left: 30 + i * 40, top: 255 + ((i * 53) % 90 - 45) * 2.2, width: 54, height: 12, background: '#3E2A18', borderRadius: 6, transform: `rotate(${(i * 37) % 60 - 30}deg)`, opacity: tr }} />)}
      <div style={{ position: 'absolute', right: 20, top: 20, background: P.navy, color: P.branco, fontFamily: 'Anton', fontSize: 46, padding: '4px 16px' }}>{r < 0.05 ? '10–20 M' : `${Math.round(10 + 50 * r)}–${Math.round(20 + 60 * r)} M`}</div>
    </div>
    <div style={{ position: 'absolute', left: 1000, top: 110, fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.14em', color: P.amarelo }}>RUA · LAMA (ESQUEMA)</div>
    <svg width={800} height={520} style={{ position: 'absolute', left: 1000, top: 220 }}><rect x={0} y={0} width={800} height={520} fill="rgba(255,255,255,0.06)" />
      <rect x={60} y={120} width={240} height={340} fill="#CFC3A6" /><rect x={460} y={160} width={240} height={300} fill="#CFC3A6" /><rect x={0} y={460} width={800} height={60} fill="#555" />
      <rect x={0} y={460 - 160 * l} width={800} height={160 * l + 60} fill="#A8693A" opacity={0.92} />
      <line x1={760} y1={460} x2={760} y2={460 - 160 * l} stroke={P.amarelo} strokeWidth={7} /><text x={740} y={440 - 160 * l} textAnchor="end" fontFamily="Anton" fontSize={64} fill={P.amarelo} stroke="#0E1426" strokeWidth={6} paintOrder="stroke">{l > 0.05 ? `ATÉ ${Math.round(80 * l)} CM` : ''}</text></svg>
    <div style={{ position: 'absolute', left: 0, top: 780, width: '100%', textAlign: 'center', fontFamily: 'Anton', fontSize: 48, color: P.branco, opacity: tr }}>DEZENAS DE MILHARES DE TRONCOS</div>
  </AbsoluteFill>;
};
const Card = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.4, 0.4);
  return <AbsoluteFill style={{ opacity: a }}>
    {c.fundo ? <><Img src={staticFile('fotos/' + c.fundo)} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', opacity: 0.35, transform: `scale(${1.04 + 0.04 * clamp01((t - c.t0) / 5)})` }} /><AbsoluteFill style={{ background: 'rgba(18,28,56,0.88)' }} /></> : <AbsoluteFill style={{ background: 'rgba(18,28,56,0.9)' }} />}
    <div style={{ position: 'absolute', left: 0, top: 150, width: '100%', textAlign: 'center', fontFamily: MONO, fontWeight: 700, fontSize: 30, letterSpacing: '0.2em', color: '#BFD0F0' }}>{c.titulo}</div>
    <div style={{ position: 'absolute', left: 0, top: 290, width: '100%', display: 'flex', justifyContent: 'center', gap: 110 }}>
      {c.linhas.map(([n, rot, tt], i) => <div key={i} style={{ transform: `scale(${pop(t, tt, 0.5)})`, opacity: t >= tt ? 1 : 0, textAlign: 'center', minWidth: 360 }}>
        <div style={{ fontFamily: 'Anton', fontSize: 190, color: P.branco, lineHeight: 1 }}>{n}</div>
        <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 30, letterSpacing: '0.14em', color: '#BFD0F0', marginTop: 8 }}>{rot}</div></div>)}
    </div>
  </AbsoluteFill>;
};
const Cortina = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.3, 0.4), dur = c.t1 - c.t0, p = clamp01((t - c.t0 - 1.0) / (dur - 3.4)), zoom = 1 + 0.55 * easeOut(clamp01((t - (c.t1 - 3.0)) / 2.6));
  const W = 1500, Hh = 844, cx = 0.5, cy = 0.5;
  // recorte comum (mesmo estiramento): região das cicatrizes
  const rec = { x: 0.34, y: 0.60, w: 0.34 };   // fração da imagem 1840×1227
  const sc = W / (rec.w * 1840);
  const img = (src, extra) => <Img src={staticFile('fotos/' + src)} style={{ position: 'absolute', width: 1840 * sc, height: 1227 * sc, left: -rec.x * 1840 * sc, top: -rec.y * 1227 * sc, filter: 'contrast(1.12) brightness(1.08)', ...extra }} />;
  return <AbsoluteFill style={{ opacity: a }}>
    <AbsoluteFill style={{ background: 'rgba(10,16,34,0.9)' }} />
    <div style={{ position: 'absolute', left: 210, top: 80, width: W, height: Hh, overflow: 'hidden', boxShadow: '0 24px 60px rgba(0,0,0,0.6)' }}>
      <div style={{ position: 'absolute', inset: 0, transform: `scale(${zoom})`, transformOrigin: '60% 40%' }}>
        {img(c.depois)}
        <div style={{ position: 'absolute', left: 0, top: 0, width: `${p * 100}%`, height: '100%', overflow: 'hidden' }}><div style={{ position: 'absolute', left: 0, top: 0, width: W, height: Hh }}>{img(c.antes)}</div></div>
        <div style={{ position: 'absolute', left: `${p * 100}%`, top: 0, width: 5, height: '100%', background: P.branco, boxShadow: '0 0 20px rgba(0,0,0,0.6)' }} />
        {t >= c.t_faixa && <svg width={W} height={Hh} style={{ position: 'absolute', left: 0, top: 0, opacity: clamp01((t - c.t_faixa) / 0.5) }}><ellipse cx={W * 0.37} cy={Hh * 0.46} rx={150} ry={70} fill="none" stroke={P.coral} strokeWidth={6} transform={`rotate(-12 ${W * 0.37} ${Hh * 0.46})`} /><text x={W * 0.37 - 60} y={Hh * 0.46 - 100} fontFamily="Anton" fontSize={54} fill={P.coral} stroke="#fff" strokeWidth={5} paintOrder="stroke">CASCA</text></svg>}
      </div>
      <Etq style={{ left: 20, top: 20, background: 'rgba(31,26,24,0.9)' }}>ANTES · 29 OUT 2022</Etq>
      <Etq style={{ right: 20, top: 20, background: P.coral }}>DEPOIS · 26 FEV 2023</Etq>
    </div>
  </AbsoluteFill>;
};
const Citacao = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.4, 0.4), n = Math.round(clamp01((t - c.t0 - 0.2) / 2.2) * c.texto.length);
  return <AbsoluteFill style={{ opacity: a }}>
    <Img src={staticFile('fotos/' + c.arq)} style={{ position: 'absolute', width: '100%', height: '100%', objectFit: 'cover', opacity: 0.4, transform: `scale(${1.05 + 0.05 * clamp01((t - c.t0) / 12)})`, filter: 'brightness(0.7)' }} />
    <AbsoluteFill style={{ background: 'rgba(10,16,34,0.72)' }} />
    <div style={{ position: 'absolute', left: 160, top: 300, width: 1600, fontFamily: 'Playfair', fontStyle: 'italic', fontWeight: 700, fontSize: 112, lineHeight: 1.12, color: P.branco, textShadow: '0 6px 24px rgba(0,0,0,0.7)' }}>“{c.texto.slice(0, n)}{n >= c.texto.length ? '”' : ''}</div>
    <div style={{ position: 'absolute', left: 160, top: 640, fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: '0.16em', color: P.coral, background: P.branco, padding: '8px 18px', opacity: clamp01((t - c.t0 - 2.4) / 0.5) }}>{c.fonte}</div>
    {t >= c.t_prec && <div style={{ position: 'absolute', left: 160, top: 760, background: P.navy, color: P.amarelo, fontFamily: 'Anton', fontSize: 64, padding: '6px 26px', transform: `scale(${pop(t, c.t_prec, 0.4)})`, transformOrigin: 'left center' }}>35 KM · CARAGUATATUBA</div>}
  </AbsoluteFill>;
};
const Resposta = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.5, 0.5), COR = ['#B9A47F', '#3FD8FF', '#C98B52'], NM = ['PAREDE', 'CHUVA', 'CASCA'];
  return <AbsoluteFill style={{ opacity: a }}>
    <AbsoluteFill style={{ background: 'rgba(10,16,34,0.82)' }} />
    <div style={{ position: 'absolute', left: 0, top: 130, width: '100%', textAlign: 'center', fontFamily: 'Anton', fontSize: 84, color: P.branco }}>A RECEITA DA SERRA DO MAR</div>
    <div style={{ position: 'absolute', left: 0, top: 320, width: '100%', display: 'flex', justifyContent: 'center', gap: 36, alignItems: 'center' }}>
      {c.itens.map(([n, tx], i) => <React.Fragment key={i}>
        {i > 0 && <div style={{ fontFamily: 'Anton', fontSize: 100, color: P.amarelo, opacity: t >= c.ts[i] ? 1 : 0 }}>+</div>}
        <div style={{ width: 520, height: 400, transform: `scale(${pop(t, c.ts[i], 0.5)})`, background: P.navy, borderRadius: 12, borderTop: `16px solid ${COR[i]}`, boxShadow: '0 18px 44px rgba(0,0,0,0.55)', padding: '26px 28px', boxSizing: 'border-box', textAlign: 'center' }}>
          <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: '0.2em', color: COR[i] }}>{NM[i]}</div>
          <div style={{ fontFamily: 'Anton', fontSize: n.length > 8 ? 78 : 110, color: P.branco, lineHeight: 1.1, marginTop: 20 }}>{n}</div>
          <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 25, letterSpacing: '0.08em', color: '#BFD0F0', marginTop: 14 }}>{tx}</div></div>
      </React.Fragment>)}
    </div>
  </AbsoluteFill>;
};
const Cortica = ({ c, t }) => {
  const a = win(t, c.t0, c.t1, 0.4, 0.4);
  return <AbsoluteFill style={{ opacity: a }}>
    <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 40%, #B58B5C, #8E6A43)' }} />
    <div style={{ position: 'absolute', left: 0, top: 70, width: '100%', textAlign: 'center', fontFamily: 'Anton', fontSize: 100, color: P.branco, textShadow: '0 6px 0 rgba(60,30,10,0.55)' }}>O QUE FAZER</div>
    <div style={{ position: 'absolute', left: 190, top: 270, width: 740, minHeight: 440, transform: `rotate(-2deg) scale(${pop(t, c.ts1 - 0.6, 0.45)})`, background: P.branco, boxShadow: '0 18px 44px rgba(40,20,5,0.55)', padding: '30px 34px', borderTop: `14px solid ${P.coral}` }}>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: '0.14em', color: P.coral }}>ALERTA POR SMS · DEFESA CIVIL</div>
      <div style={{ fontFamily: 'Anton', fontSize: 80, color: P.tinta, lineHeight: 1.1, marginTop: 20 }}>MANDE O SEU CEP PARA</div>
      <div style={{ fontFamily: 'Anton', fontSize: 190, color: P.coral, lineHeight: 1 }}>40199</div></div>
    <div style={{ position: 'absolute', left: 1010, top: 330, width: 720, transform: `rotate(1.8deg) scale(${pop(t, c.ts2 - 0.8, 0.45)})`, background: P.navy, boxShadow: '0 18px 44px rgba(40,20,5,0.55)', padding: '36px 40px', borderTop: `14px solid ${P.amarelo}` }}>
      <div style={{ fontFamily: 'Anton', fontSize: 92, color: P.branco, lineHeight: 1.1 }}>SE O ALERTA DISSER PARA SAIR, <span style={{ color: P.amarelo }}>SAIA</span></div></div>
  </AbsoluteFill>;
};
const Final = ({ c, t }) => {
  const a = win(t, c.t0, c.t1 + 5, 0.5, 0.1);
  return <AbsoluteFill style={{ opacity: a }}>
    <AbsoluteFill style={{ background: 'rgba(10,16,34,0.92)' }} />
    <div style={{ position: 'absolute', left: 140, top: 200, width: 840, height: 470, transform: `scale(${pop(t, c.t_card, 0.5)})`, background: P.branco, boxShadow: '0 20px 50px rgba(0,0,0,0.6)', padding: 30, boxSizing: 'border-box', borderTop: `14px solid ${P.coral}` }}>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 24, letterSpacing: '0.14em', color: P.coral }}>VÍDEO NO CANAL</div>
      <div style={{ fontFamily: 'Anton', fontSize: 72, color: P.tinta, lineHeight: 1.1, marginTop: 20 }}>Por que quase ninguém fala da seca que matou 500 mil brasileiros?</div>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 26, letterSpacing: '0.1em', color: P.tinta, marginTop: 24 }}>SECA DE 1877 · NO MAPA</div></div>
    <div style={{ position: 'absolute', left: 1080, top: 230, width: 700, textAlign: 'center', opacity: t >= c.t_logo ? 1 : 0, transform: `scale(${pop(t, c.t_logo, 0.5)})` }}>
      <div style={{ fontFamily: 'Anton', fontSize: 190, color: P.branco, lineHeight: 0.95 }}>EM<br />RELEVO</div>
      <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 28, letterSpacing: '0.14em', color: P.amarelo, marginTop: 16 }}>CLIMA E GEOGRAFIA DO BRASIL NO MAPA</div></div>
    {t >= c.t_btn && <div style={{ position: 'absolute', left: 1180, top: 760, transform: `scale(${pop(t, c.t_btn, 0.4)})`, background: P.coral, color: P.branco, fontFamily: MONO, fontWeight: 700, fontSize: 38, letterSpacing: '0.14em', padding: '18px 44px', borderRadius: 8, boxShadow: '0 10px 26px rgba(0,0,0,0.5)' }}>INSCREVA-SE</div>}
  </AbsoluteFill>;
};

const MAPA = { foto: Foto, dupla: Dupla, doc: Doc, bloco: Bloco, pluv: Pluv, ficha1967: Ficha1967, postos: Postos, casca_esq: CascaEsq, fases: Fases, lama: Lama, card: Card, cortina: Cortina, citacao: Citacao, resposta: Resposta, cortica: Cortica, final: Final };
export const Cenas = ({ t, cues }) => <>{cues.cenas.filter((c) => t >= c.t0 - 0.05 && t <= c.t1 + 0.4).map((c, i) => { const C = MAPA[c.k]; return C ? <C key={i} c={c} t={t} /> : null; })}</>;
