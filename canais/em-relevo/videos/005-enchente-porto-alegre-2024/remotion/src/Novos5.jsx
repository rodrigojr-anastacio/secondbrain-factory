// Em Relevo 005 (15/11/2026): camadas 2D novas do vídeo da enchente de maio/2024 em Porto Alegre.
// Dirigidas por cues.graficos5 (shared/build_cues.py). Esquemas são ESQUEMAS (não são mapas em escala) e dizem isso na tela.
import React from 'react';
import { janela, clamp01, easeOut, pop } from '../../shared/camadas.js';

const MONO = 'PlexMono, monospace';
const P = { papel: '#E9DCC3', coral: '#E8505B', navy: '#1F2A44', tinta: '#2B2622', branco: '#FBF8F1', agua: '#3D7FB8', agua2: '#7FB4DE', ciano: '#3FD8FF', amarelo: '#FFD23F', cinza: '#8C8F96' };
const tab = (lista, t) => {
  if (!lista || !lista.length) return 0;
  if (t <= lista[0][0]) return lista[0][1];
  for (let i = 1; i < lista.length; i++) if (t <= lista[i][0]) { const [t0, v0] = lista[i - 1], [t1, v1] = lista[i]; return v0 + (v1 - v0) * easeOut((t - t0) / Math.max(1e-6, t1 - t0)); }
  return lista[lista.length - 1][1];
};
const Painel = ({ a, children, left = 110, top = 190, w = 1100, titulo, fonte, sub }) => (
  <div style={{ position: 'absolute', left, top, width: w, transform: `scale(${a})`, transformOrigin: 'left center', background: '#F3EEE3', borderRadius: 6,
    boxShadow: '0 20px 50px rgba(0,0,0,0.42)', padding: '22px 28px 18px', fontFamily: MONO, color: P.tinta }}>
    {titulo && <div style={{ fontWeight: 700, fontSize: 21, letterSpacing: '0.12em', color: P.navy, marginBottom: 12 }}>{titulo}</div>}
    {children}
    {(fonte || sub) && <div style={{ fontWeight: 500, fontSize: 14, letterSpacing: '0.1em', color: '#7a7066', marginTop: 10 }}>{fonte ? `FONTE: ${fonte}` : ''}{fonte && sub ? ' · ' : ''}{sub || ''}</div>}
  </div>
);
const Etiqueta = ({ x, y, children, cor = P.navy, tam = 18, s = 1, anchor = 'middle' }) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <text textAnchor={anchor} fontFamily="PlexMono" fontWeight="700" fontSize={tam} letterSpacing="1.6" fill={cor}>{children}</text>
  </g>
);

// ------------------------------------------------------------ esquema da orla (muro, diques, comportas, casas de bombas)
// geometria fixa (esquemática): orla = curva de x=40 a x=1040; Guaíba acima, cidade abaixo
const ORLA = (x) => 150 + 38 * Math.sin((x - 40) / 1000 * Math.PI * 1.6) - 0.02 * (x - 40);
const COMP = Array.from({ length: 14 }, (_, i) => { const x = 90 + i * 70.5; return [x, ORLA(x) + 6]; });
const BOMB = Array.from({ length: 23 }, (_, i) => { const x = 70 + i * 43.5, y = ORLA(x) + 62 + (i % 3) * 34; return [x, y]; });
const PARADAS = [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22].filter((i) => i !== 4).slice(0, 19);
const IDX_SERTORIO = 2, IDX_SARANDI = 18;   // posições esquemáticas (zona norte = esquerda do esquema)
const Maquete = ({ g, t, a }) => {
  const oc = (g.ocultar || []).some(([x, y]) => t >= x && t <= y);
  if (oc) return null;
  const v = (k) => (g[k] !== undefined ? clamp01((t - g[k]) / 0.7) : 0);
  const pMuro = easeOut(v('t_muro')), pDique = easeOut(clamp01((t - (g.t_dique ?? 1e9)) / 1.4));
  const pComp = (i) => pop(t, (g.t_comp ?? 1e9) + i * 0.09, 0.3);
  const pBomb = (i) => pop(t, (g.t_bomb ?? 1e9) + i * 0.05, 0.3);
  const apaga = g.t_apaga !== undefined && t >= g.t_apaga;
  const falha = (g.t_falha !== undefined) ? clamp01((t - g.t_falha) / 1.2) : 0;
  const concreto = g.t_concreto !== undefined ? clamp01((t - g.t_concreto) / 0.6) : 0;
  const pisca = 0.55 + 0.45 * Math.sin(t * 9);
  const MURO = [[430, 360]];
  const dx0 = 430, dx1 = 640;
  return (
    <Painel a={a} w={g.w ?? 1140} left={g.left ?? 90} top={g.top ?? 215} titulo={g.titulo} sub="ESQUEMA FORA DE ESCALA · POSIÇÕES ILUSTRATIVAS">
      <svg width={1080} height={g.h ?? 410} viewBox={`0 0 1080 ${g.h ?? 410}`}>
        <defs><linearGradient id="gu" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stopColor="#9CC4E4" /><stop offset="1" stopColor="#5E9BCB" /></linearGradient></defs>
        <path d={`M0 0 H1080 V${ORLA(1080)} ${Array.from({ length: 28 }, (_, i) => `L${1080 - i * 40} ${ORLA(1080 - i * 40)}`).join(' ')} L0 ${ORLA(0)} Z`} fill="url(#gu)" />
        <Etiqueta x={540} y={70} cor="#1F4E7A" tam={30}>LAGO GUAÍBA</Etiqueta>
        <path d={`M0 ${ORLA(0)} ${Array.from({ length: 28 }, (_, i) => `L${i * 40} ${ORLA(i * 40)}`).join(' ')} L1080 ${ORLA(1080)} V470 H0 Z`} fill="#E3D6BA" opacity="0.95" />
        <Etiqueta x={880} y={g.h ? g.h - 20 : 392} cor="#7a6a4e" tam={22}>CIDADE</Etiqueta>
        {/* diques: linha tracejada contínua pela orla */}
        <path d={`M30 ${ORLA(30) + 8} ${Array.from({ length: 27 }, (_, i) => `L${30 + i * 40} ${ORLA(30 + i * 40) + 8}`).join(' ')}`} fill="none" stroke="#6E5D45" strokeWidth={7} strokeDasharray="14 9" opacity={pDique}
          strokeDashoffset={(1 - pDique) * 400} />
        {pDique > 0.2 && <Etiqueta x={170} y={ORLA(170) - 14} cor="#4a3c28" tam={18} s={pDique}>DIQUES · 68 KM</Etiqueta>}
        {/* muro da Mauá */}
        <rect x={dx0} y={ORLA(530) - 6} width={(dx1 - dx0) * pMuro} height={22} fill="#D9D9DC" stroke="#6b6b70" strokeWidth={3} rx={3} transform={`rotate(${Math.atan((ORLA(640) - ORLA(430)) / 210) * 180 / Math.PI} ${dx0} ${ORLA(530)})`} />
        {pMuro > 0.6 && <Etiqueta x={535} y={ORLA(530) - 24} cor="#3a3a40" tam={20} s={pMuro}>MURO DA MAUÁ</Etiqueta>}
        {/* comportas */}
        {COMP.map(([x, y], i) => { const s = pComp(i); if (s <= 0) return null; const cim = concreto > 0 && i < 8;
          const quebra = falha > 0 && i === IDX_SERTORIO;
          return <g key={i} transform={`translate(${x},${y}) scale(${s})`}><rect x={-10} y={-10} width={20} height={20} rx={3} fill={cim ? P.cinza : quebra ? P.coral : P.amarelo} stroke="#1F2A44" strokeWidth={3} opacity={quebra ? 0.6 + 0.4 * pisca : 1} />
            {cim && <path d="M-6 -6 L6 6 M6 -6 L-6 6" stroke="#fff" strokeWidth={2.5} />}</g>; })}
        {/* casas de bombas */}
        {BOMB.map(([x, y], i) => { const s = pBomb(i); if (s <= 0) return null; const parada = apaga && i % 23 < 23 && (i * 7) % 23 < 19 || false;
          const off = apaga && ![0, 5, 11, 16].includes(i) ? 1 : 0;
          const sar = g.t_sarandi !== undefined && t >= g.t_sarandi && i === 10;
          return <g key={i} transform={`translate(${x},${y}) scale(${s})`}><rect x={-9} y={-9} width={18} height={18} fill={sar ? P.coral : off ? '#9a9da4' : P.navy} opacity={off ? 0.55 : 1} stroke={sar ? '#fff' : 'none'} strokeWidth={2} />
            {!off && <circle r={3} cy={0} fill={P.amarelo} />}</g>; })}
        {/* água entrando pelos pontos fracos */}
        {falha > 0 && [IDX_SERTORIO].map((i) => <path key={i} d={`M${COMP[i][0]} ${COMP[i][1]} C ${COMP[i][0] + 10} ${COMP[i][1] + 60}, ${COMP[i][0] - 30} ${COMP[i][1] + 120}, ${COMP[i][0] - 10} ${COMP[i][1] + 190}`} stroke={P.ciano} strokeWidth={12} fill="none" strokeLinecap="round" strokeDasharray="300" strokeDashoffset={300 * (1 - falha)} opacity="0.9" />)}
        {g.t_agua !== undefined && t >= g.t_agua && [[COMP[IDX_SERTORIO]], [BOMB[10]], [BOMB[18]]].map(([p0], k) => <circle key={k} cx={p0[0]} cy={p0[1] + 30} r={40 * clamp01((t - g.t_agua - k * 0.4) / 1.2)} fill={P.ciano} opacity="0.35" />)}
        {g.rotulos && g.rotulos.map(([txt, x, y, tr, cor], i) => t >= tr ? <Etiqueta key={i} x={x} y={y} cor={cor || P.coral} tam={19} s={pop(t, tr, 0.3)}>{txt}</Etiqueta> : null)}
      </svg>
    </Painel>
  );
};

// ------------------------------------------------------------ corte esquemático (b27)
const Corte = ({ g, t, a }) => {
  const f = (k) => (g[k] !== undefined ? clamp01((t - g[k]) / 0.8) : 0);
  const cheia = 0.55 + 0.35 * easeOut(f('t_muro'));
  const falha = f('t_falha');
  const gate = 1 - easeOut(f('t_comp'));
  return (
    <Painel a={a} w={1300} left={310} top={210} titulo="COMO O SISTEMA FUNCIONA" sub="CORTE ESQUEMÁTICO · FORA DE ESCALA">
      <svg width={1240} height={500} viewBox="0 0 1240 500">
        {/* guaíba (esquerda) */}
        <rect x={0} y={500 - 380 * cheia} width={520} height={380 * cheia} fill="#6FA6D2" /><Etiqueta x={260} y={500 - 380 * cheia + 40} cor="#1F4E7A" tam={24}>GUAÍBA</Etiqueta>
        {/* solo / cidade */}
        <rect x={0} y={420} width={1240} height={80} fill="#CDB98F" /><rect x={700} y={330} width={540} height={170} fill="#D8C7A0" />
        {/* muro/dique */}
        <path d="M520 420 L560 150 L640 150 L700 330 L700 420 Z" fill="#B9B9BE" stroke="#5b5b60" strokeWidth={4} opacity={f('t_muro')} />
        <Etiqueta x={600} y={125} cor="#3a3a40" tam={20} s={f('t_muro')}>MURO / DIQUE</Etiqueta>
        {/* comporta (portão de aço): desce e fecha a passagem */}
        <rect x={568} y={150 + 120 * gate - 120 + 110} width={64} height={120} fill={P.amarelo} stroke={P.navy} strokeWidth={4} opacity={f('t_comp') > 0 || g.t_comp !== undefined && t >= g.t_comp - 0.4 ? 1 : 0} transform={`translate(0 ${-130 * gate})`} />
        <Etiqueta x={600} y={402} cor={P.navy} tam={18} s={f('t_comp')}>COMPORTA</Etiqueta>
        {/* casa de bombas e a chuva que sai por cima do dique */}
        <rect x={800} y={290} width={80} height={60} fill={P.navy} opacity={f('t_bomba')} /><Etiqueta x={840} y={380} cor={P.navy} tam={18} s={f('t_bomba')}>CASA DE BOMBAS</Etiqueta>
        {f('t_bomba') > 0.2 && <path d="M820 290 C 800 200, 640 90, 540 150" fill="none" stroke={P.agua} strokeWidth={9} strokeDasharray="22 14" strokeDashoffset={-t * 60} strokeLinecap="round" />}
        {f('t_bomba') > 0.2 && <Etiqueta x={760} y={130} cor={P.agua} tam={18}>CHUVA DE DENTRO, PARA FORA</Etiqueta>}
        {[0, 1, 2, 3, 4].map((i) => <line key={i} x1={760 + i * 90} x2={750 + i * 90} y1={190} y2={225} stroke={P.agua} strokeWidth={5} opacity={f('t_bomba') * 0.7} strokeLinecap="round" />)}
        {/* falha: uma peça pisca em coral e a água acha o caminho */}
        {falha > 0 && <rect x={640} y={330} width={60} height={50} fill={P.coral} opacity={0.5 + 0.5 * Math.sin(t * 10)} />}
        {falha > 0 && <path d="M520 400 C 600 410, 650 360, 720 372 S 900 400, 1000 395" fill="none" stroke={P.ciano} strokeWidth={14} strokeLinecap="round" strokeDasharray="700" strokeDashoffset={700 * (1 - falha)} />}
      </svg>
    </Painel>
  );
};

// ------------------------------------------------------------ perfil serra → capital (b11)
const Perfil = ({ g, t, a }) => {
  const PTS = [[0, 800], [14, 780], [22, 700], [30, 420], [38, 520], [48, 260], [58, 130], [70, 60], [82, 28], [92, 10], [100, 3]];
  const X = (km) => 40 + km / 100 * 1000, Y = (m) => 330 - Math.pow(m / 800, 0.8) * 270;
  const d = PTS.map(([k, m], i) => `${i ? 'L' : 'M'}${X(k)} ${Y(m)}`).join(' ');
  const u = tab(g.prog || [[0, 0]], t);
  const km = u * 100; let gy = 3, gx = 0;
  for (let i = 1; i < PTS.length; i++) if (km <= PTS[i][0]) { const [k0, m0] = PTS[i - 1], [k1, m1] = PTS[i]; const q = (km - k0) / (k1 - k0); gy = m0 + (m1 - m0) * q; gx = km; break; }
  return (
    <Painel a={a} w={1200} left={360} top={g.top ?? 200} titulo="DA SERRA À CAPITAL · PERFIL DO RELEVO" sub="ESQUEMA COM EXAGERO VERTICAL · ALTITUDES APROXIMADAS">
      <svg width={1140} height={380} viewBox="0 0 1140 380">
        <path d={`${d} L${X(100)} 350 L${X(0)} 350 Z`} fill="#CDB98F" stroke="#6E5D45" strokeWidth={4} />
        <rect x={X(0)} y={Y(3) - 4} width={1000} height={7} fill={P.agua} opacity="0" />
        <Etiqueta x={X(0)} y={Y(800) - 24} cor={P.navy} tam={22} anchor="start">CAXIAS DO SUL · ~800 M</Etiqueta>
        <Etiqueta x={X(94)} y={Y(3) - 28} cor={P.navy} tam={22}>PORTO ALEGRE</Etiqueta>
        {t >= (g.t_vales ?? 1e9) && <Etiqueta x={X(32)} y={Y(420) + 60} cor={P.coral} tam={20} s={pop(t, g.t_vales, 0.3)}>VALES ESTREITOS E FUNDOS</Etiqueta>}
        <circle cx={X(gx)} cy={Y(gy) - 12} r={14} fill="#BFF6FF" stroke={P.ciano} strokeWidth={5} opacity={u > 0.001 ? 1 : 0} />
        <line x1={X(0)} x2={X(100)} y1={352} y2={352} stroke="#6b625a" strokeWidth={2} />
        <text x={X(0)} y={374} fontFamily="PlexMono" fontSize={16} fill="#6b625a">0</text><text x={X(100)} y={374} textAnchor="end" fontFamily="PlexMono" fontSize={16} fill="#6b625a">~100 KM</text>
      </svg>
    </Painel>
  );
};

// ------------------------------------------------------------ vazão do Guaíba (b17)
const Vazao = ({ g, t, a }) => {
  const u = tab(g.agulha || [[0, 0]], t);   // 0..1 da escala; passa do fim = 1.18
  const ang = -90 + u * 180;
  const sel = g.t_selo !== undefined ? pop(t, g.t_selo, 0.35) : 0;
  const bar = (k) => easeOut(clamp01((t - g.t_barra - k * 0.25) / 0.8));
  return (
    <Painel a={a} w={1250} left={335} top={200} titulo="DE ONDE VEM A ÁGUA DO GUAÍBA" fonte="DMAE · PESQUISADORES (MAIO/2024)">
      <div style={{ display: 'flex', gap: 40, alignItems: 'center' }}>
        <svg width={520} height={340} viewBox="0 0 520 340">
          <Etiqueta x={260} y={30} cor={P.navy} tam={20}>QUEM ABASTECE O LAGO</Etiqueta>
          <rect x={60} y={60} width={400} height={64} fill="rgba(31,42,68,0.08)" />
          <rect x={60} y={60} width={400 * 0.55 * bar(0)} height={64} fill={P.ciano} /><rect x={60 + 400 * 0.55} y={60} width={400 * 0.35 * bar(1)} height={64} fill="#1F8FB3" />
          {bar(0) > 0.5 && <Etiqueta x={60 + 110} y={100} cor="#0b3140" tam={22}>JACUÍ</Etiqueta>}{bar(1) > 0.5 && <Etiqueta x={60 + 400 * 0.55 + 70} y={100} cor="#fff" tam={22}>TAQUARI</Etiqueta>}
          <Etiqueta x={260} y={160} cor={P.coral} tam={26} s={bar(1)}>JACUÍ + TAQUARI = QUASE TUDO</Etiqueta>
          <rect x={60 + 400 * 0.9} y={60} width={40 * bar(2)} height={64} fill="#9db6c6" /><Etiqueta x={420} y={190} cor="#6b625a" tam={16} s={bar(2)}>CAÍ, SINOS, GRAVATAÍ…</Etiqueta>
          <text x={260} y={300} textAnchor="middle" fontFamily="PlexMono" fontWeight="700" fontSize={15} fill="#7a7066">PROPORÇÕES ILUSTRATIVAS</text>
        </svg>
        <svg width={600} height={415} viewBox="0 0 600 415">
          <path d="M80 300 A220 220 0 0 1 520 300" fill="none" stroke="#c9c1b3" strokeWidth={26} strokeLinecap="round" />
          <path d="M80 300 A220 220 0 0 1 300 80" fill="none" stroke={P.agua} strokeWidth={26} strokeLinecap="round" opacity="0.9" />
          <Etiqueta x={80} y={330} cor={P.navy} tam={16}>0</Etiqueta><Etiqueta x={590} y={330} cor={P.navy} tam={14} anchor="end">MAIORES JÁ MEDIDAS</Etiqueta>
          <g transform={`translate(300 300) rotate(${ang})`}><line x1={0} y1={0} x2={0} y2={-196} stroke={P.coral} strokeWidth={9} strokeLinecap="round" /><circle r={16} fill={P.navy} /></g>
          <text x={300} y={372} textAnchor="middle" fontFamily="Anton" fontSize={50} fill={u > 0.97 ? P.coral : P.navy}>{u > 0.97 ? 'ACIMA' : '~1.200 M³/S'}</text>
          <text x={300} y={398} textAnchor="middle" fontFamily="PlexMono" fontWeight="700" fontSize={16} fill="#6b625a">{u > 0.97 ? 'MAIO DE 2024' : 'VAZÃO NORMAL · DMAE'}</text>
        </svg>
      </div>
      {sel > 0 && <div style={{ position: 'absolute', right: 40, top: 70, transform: `rotate(-6deg) scale(${sel})`, border: `6px solid ${P.coral}`, color: P.coral, fontFamily: 'Anton', fontSize: 42, padding: '0 20px', background: 'rgba(251,248,241,0.9)' }}>MAIO: ACIMA DAS MAIORES JÁ MEDIDAS</div>}
    </Painel>
  );
};

// ------------------------------------------------------------ três cheias em oito meses (b10)
const Cheias3 = ({ g, t, a }) => {
  const itens = [['SET 2023', 'TAQUARI ACIMA DE 1941', 0.42, g.t[0]], ['NOV 2023', 'GUAÍBA > 3 M', 0.58, g.t[1]], ['MAI 2024', 'GUAÍBA 5,35 M', 1.0, g.t[2]]];
  return (
    <Painel a={a} w={1300} left={310} top={205} titulo="3 CHEIAS GRANDES EM 8 MESES" fonte="DEFESA CIVIL RS · ANA · SGB" sub="ALTURAS ILUSTRATIVAS, FORA DE ESCALA">
      <svg width={1240} height={420} viewBox="0 0 1240 420">
        <line x1={40} x2={1200} y1={380} y2={380} stroke="#6b625a" strokeWidth={3} />
        {itens.map(([m, tx, h, tt], i) => {
          const p = easeOut(clamp01((t - tt) / 0.9)); const x = 130 + i * 380, hh = 320 * h * p;
          return (<g key={i} opacity={t >= tt ? 1 : 0}>
            <rect x={x} y={380 - hh} width={200} height={hh} fill={i === 2 ? P.coral : P.agua} />
            <Etiqueta x={x + 100} y={406} cor={P.navy} tam={22}>{m}</Etiqueta>
            {p > 0.8 && <Etiqueta x={x + 100} y={380 - hh - 14} cor={i === 2 ? P.coral : P.navy} tam={20}>{tx}</Etiqueta>}
          </g>);
        })}
      </svg>
    </Painel>
  );
};

// ------------------------------------------------------------ chuva em 11 dias × 3 meses (b08)
const Chuva3m = ({ g, t, a }) => {
  const p = (k) => easeOut(clamp01((t - g.t0 - k) / 0.7));
  return (
    <Painel a={a} w={820} left={1010} top={235} titulo="O TAMANHO DA CHUVA" fonte="WORLD WEATHER ATTRIBUTION" sub="BLOCOS ILUSTRATIVOS">
      <svg width={760} height={400} viewBox="0 0 760 400">
        <g>{[0, 1, 2].map((i) => <rect key={i} x={70} y={330 - (i + 1) * 100 * p(i * 0.45 + 0.2)} width={200} height={96 * p(i * 0.45 + 0.2)} fill={P.agua} stroke="#F3EEE3" strokeWidth={4} />)}
          <Etiqueta x={170} y={368} cor={P.navy} tam={20}>3 MESES DE CHUVA</Etiqueta></g>
        <text x={380} y={210} textAnchor="middle" fontFamily="Anton" fontSize={64} fill={P.coral} opacity={p(1.5)}>=</text>
        <g><rect x={490} y={330 - 300 * p(1.3)} width={200} height={300 * p(1.3)} fill={P.coral} /><Etiqueta x={590} y={368} cor={P.coral} tam={20}>11 DIAS</Etiqueta>
          <Etiqueta x={590} y={30} cor={P.navy} tam={17}>24/04 → 04/05</Etiqueta></g>
      </svg>
    </Painel>
  );
};

// ------------------------------------------------------------ calendário de picos (b18) e de maio (b24)
const Calendario5 = ({ g, t, a }) => {
  if (g.modo === 'picos') {
    const dias = ['QUI 2', 'SEX 3', 'SÁB 4', 'DOM 5', 'SEG 6'];
    const linhas = [['TAQUARI', 0, g.tp[0]], ['CAÍ', 0, g.tp[1]], ['SINOS', 2, g.tp[2]], ['JACUÍ', 3, g.tp[3]], ['GUAÍBA', 3, g.tp[4]]];
    return (
      <Painel a={a} w={1120} left={90} top={210} titulo="QUANDO CADA RIO ATINGIU O PICO · 2 A 6 DE MAIO DE 2024" fonte="IPH/UFRGS · ANA · DEFESA CIVIL" sub="PICOS APROXIMADOS (DIA)">
        <svg width={1060} height={400} viewBox="0 0 1060 400">
          {dias.map((d, i) => <g key={d}><rect x={190 + i * 172} y={10} width={164} height={44} fill={P.navy} /><text x={190 + i * 172 + 82} y={40} textAnchor="middle" fontFamily="PlexMono" fontWeight="700" fontSize={22} fill="#fff">{d}</text></g>)}
          {linhas.map(([nome, dia, tt], r) => {
            const y = 70 + r * 66, on = t >= tt, pu = on ? 1 + 0.12 * Math.sin((t - tt) * 7) * Math.max(0, 1 - (t - tt) / 2.5) : 0;
            return (<g key={nome}>
              <text x={10} y={y + 36} fontFamily="PlexMono" fontWeight="700" fontSize={24} fill={nome === 'GUAÍBA' ? P.coral : P.navy}>{nome}</text>
              {dias.map((d, i) => <rect key={d} x={190 + i * 172} y={y} width={164} height={56} fill="rgba(31,42,68,0.07)" />)}
              {on && <g transform={`translate(${190 + dia * 172 + 82},${y + 28}) scale(${pu})`}><rect x={-78} y={-24} width={156} height={48} rx={6} fill={nome === 'GUAÍBA' ? P.coral : P.ciano} /><text y={9} textAnchor="middle" fontFamily="Anton" fontSize={28} fill={nome === 'GUAÍBA' ? '#fff' : '#06303c'}>{nome === 'GUAÍBA' ? '5,35 M' : 'PICO'}</text></g>}
            </g>);
          })}
        </svg>
      </Painel>
    );
  }
  // maio inteiro
  const dia = (d) => 130 + (d - 1) / 30 * 900;
  const pb = easeOut(clamp01((t - g.t_banda) / 1.6));
  return (
    <Painel a={a} w={1160} left={90} top={215} titulo="MAIO DE 2024 · A ÁGUA DESCEU DEVAGAR" fonte="IPH/UFRGS · PREFEITURA DE PORTO ALEGRE" sub="BANDA = ~1 MÊS ACIMA DA COTA DE INUNDAÇÃO (4 M)">
      <svg width={1100} height={330} viewBox="0 0 1100 330">
        <line x1={dia(1)} x2={dia(31)} y1={250} y2={250} stroke="#6b625a" strokeWidth={3} />
        {[1, 5, 10, 16, 20, 27, 31].map((d) => <g key={d}><line x1={dia(d)} x2={dia(d)} y1={244} y2={256} stroke="#6b625a" strokeWidth={3} /><text x={dia(d)} y={280} textAnchor="middle" fontFamily="PlexMono" fontWeight="700" fontSize={18} fill="#6b625a">{d}</text></g>)}
        <rect x={dia(2)} y={190} width={(dia(31) - dia(2)) * pb} height={34} fill={P.ciano} opacity="0.55" /><Etiqueta x={dia(16)} y={212} cor="#0b3140" tam={19} s={pb}>GUAÍBA ACIMA DA COTA DE INUNDAÇÃO</Etiqueta>
        {[[5, 'GUAÍBA 5/5', g.tm[0], P.coral, 70], [16, 'LAGOA 16/5', g.tm[1], P.agua, 120], [27, 'LAGOA 27/5', g.tm[2], P.agua, 70]].map(([d, txt, tt, cor, h]) => t >= tt ? (
          <g key={txt} transform={`scale(1)`}><line x1={dia(d)} x2={dia(d)} y1={250} y2={250 - h * pop(t, tt, 0.35)} stroke={cor} strokeWidth={8} /><circle cx={dia(d)} cy={250 - h * pop(t, tt, 0.35)} r={14} fill={cor} /><Etiqueta x={dia(d)} y={250 - h - 26} cor={cor} tam={20}>{txt}</Etiqueta></g>) : null)}
      </svg>
    </Painel>
  );
};

// ------------------------------------------------------------ caminho inteiro da água (b22): bacia → lago raso → laguna → gargalo
const Etapas = ({ g, t, a }) => {
  const itens = [['1/3 DO ESTADO', 'BACIA'], ['LAGO RASO', 'GUAÍBA'], ['250 KM', 'LAGUNA'], ['GARGALO', 'RIO GRANDE']];
  const ang = g.t.map((tt) => tt);
  const gx = (() => { for (let i = ang.length - 1; i >= 0; i--) if (t >= ang[i]) return i + clamp01((t - ang[i]) / 1.0) * (i < 3 ? 1 : 0); return 0; })();
  return (
    <Painel a={a} w={1560} left={180} top={g.top ?? 250} titulo="O CAMINHO DA ÁGUA ATÉ O MAR">
      <svg width={1500} height={250} viewBox="0 0 1500 250">
        <line x1={150} x2={1350} y1={120} y2={120} stroke="#b7ad9b" strokeWidth={8} strokeDasharray="4 12" />
        {itens.map(([t1, t2], i) => { const s = pop(t, ang[i] - 0.3, 0.35); const w = 230;
          return (<g key={i} transform={`translate(${150 + i * 400},120) scale(${s})`}><rect x={-w / 2 + 0} y={-60} width={w} height={120} rx={14} fill={i === 3 ? P.coral : i === 1 ? '#6FA6D2' : P.navy} /><text y={-6} textAnchor="middle" fontFamily="Anton" fontSize={34} fill="#fff">{t1}</text><text y={34} textAnchor="middle" fontFamily="PlexMono" fontWeight="700" fontSize={18} fill="#dfe6f2">{t2}</text></g>);
        })}
        <circle cx={150 + Math.min(3, gx) * 400} cy={120} r={16} fill="#BFF6FF" stroke={P.ciano} strokeWidth={6} />
      </svg>
    </Painel>
  );
};

// ------------------------------------------------------------ WWA (b37)
const Wwa = ({ g, t, a }) => (
  <Painel a={a} w={1150} left={385} top={230} titulo="E O CLIMA? · WORLD WEATHER ATTRIBUTION · 03/06/2024" fonte="WORLD WEATHER ATTRIBUTION (ESTUDO RÁPIDO DE ATRIBUIÇÃO)">
    <div style={{ display: 'flex', gap: 24 }}>
      {[['> 2×', 'CHANCE DE UMA CHUVA ASSIM', 'AQUECIMENTO GLOBAL', g.t[0], P.coral], ['6–9%', 'CHUVA MAIS INTENSA', 'AQUECIMENTO GLOBAL', g.t[1], P.coral], ['≈', 'PESO PARECIDO', 'EL NIÑO DAQUELE ANO, SOZINHO', g.t[2], P.agua]].map(([n, l, s, tt, cor], i) => {
        const p = pop(t, tt, 0.4); return (
          <div key={i} style={{ flex: 1, transform: `scale(${p})`, background: P.branco, borderTop: `10px solid ${cor}`, padding: '18px 14px', textAlign: 'center', boxShadow: '0 10px 26px rgba(0,0,0,0.2)' }}>
            <div style={{ fontFamily: 'Anton', fontSize: 100, color: cor, lineHeight: 1 }}>{n}</div>
            <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 20, letterSpacing: '0.08em', color: P.navy, marginTop: 8 }}>{l}</div>
            <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 15, letterSpacing: '0.1em', color: '#6b625a', marginTop: 6 }}>{s}</div>
          </div>);
      })}
    </div>
  </Painel>
);

// ------------------------------------------------------------ SMS da Defesa Civil (b39) — ilustração
const Sms = ({ g, t, a }) => {
  const m = pop(t, g.t_msg, 0.45);
  return (
    <div style={{ position: 'absolute', left: 1310, top: 150, transform: `scale(${a})`, transformOrigin: 'center' }}>
      <div style={{ width: 400, height: 760, background: '#16181c', borderRadius: 48, padding: '56px 18px', boxShadow: '0 30px 70px rgba(0,0,0,0.55)' }}>
        <div style={{ height: '100%', background: 'linear-gradient(#2a3448, #1a2030)', borderRadius: 14, padding: 18 }}>
          <div style={{ marginTop: 60, transform: `scale(${m})`, background: '#F3EEE3', borderRadius: 16, padding: 18 }}>
            <div style={{ fontFamily: MONO, fontWeight: 700, fontSize: 21, color: P.coral, letterSpacing: '0.06em' }}>DEFESA CIVIL · ALERTA</div>
            <div style={{ fontFamily: MONO, fontWeight: 500, fontSize: 22, color: P.tinta, marginTop: 10, lineHeight: 1.3 }}>PARA RECEBER ALERTAS POR SMS, ENVIE O SEU CEP PARA</div>
            <div style={{ fontFamily: 'Anton', fontSize: 92, color: P.navy, lineHeight: 1.1, marginTop: 6 }}>40199</div>
          </div>
          <div style={{ fontFamily: MONO, fontSize: 14, color: '#9aa3b5', marginTop: 16, textAlign: 'center' }}>ILUSTRAÇÃO</div>
        </div>
      </div>
    </div>
  );
};

// ------------------------------------------------------------ frase grande (âncora b02, b19, b38)
const Frase = ({ g, t, a }) => {
  const n = Math.round(clamp01((t - g.t0) / (g.dur ?? 2.4)) * g.linhas.join('\n').length);
  let k = n;
  return (
    <div style={{ position: 'absolute', left: g.left ?? 90, top: g.top ?? 700, width: g.w ?? 1740, transform: `scale(${0.94 + 0.06 * a})`, opacity: Math.min(1, a * 1.6) }}>
      {g.linhas.map((l, i) => { const s = l.slice(0, Math.max(0, k)); k -= l.length + 1;
        return <div key={i} style={{ display: 'inline-block', clear: 'both', float: 'left', background: i === g.destaque ? P.coral : P.branco, color: i === g.destaque ? P.branco : P.tinta, fontFamily: 'Anton', fontSize: g.tam ?? 66, lineHeight: 1.1, padding: '8px 22px 12px', marginBottom: 8,
          boxShadow: '0 14px 34px rgba(0,0,0,0.45)', transform: `rotate(${i % 2 ? 0.6 : -0.6}deg)`, textTransform: 'uppercase', visibility: s ? 'visible' : 'hidden' }}>{s}</div>; })}
    </div>
  );
};

// ------------------------------------------------------------ selo pequeno
const Selo = ({ g, t, a }) => {
  const p = clamp01((t - g.t0) / 0.22);
  return <div style={{ position: 'absolute', left: g.left ?? 110, top: g.top ?? 150, transform: `rotate(${g.rot ?? -4}deg) scale(${2.0 - 1.0 * easeOut(p)})`, opacity: p * Math.min(1, a * 2), border: `6px solid ${g.cor ?? P.coral}`, color: g.cor ?? P.coral,
    fontFamily: 'Anton', fontSize: g.tam ?? 58, padding: '0 24px', background: 'rgba(251,248,241,0.92)', letterSpacing: '0.04em', whiteSpace: 'nowrap', boxShadow: '0 10px 26px rgba(0,0,0,0.3)' }}>{g.texto}</div>;
};

export const Grafico5 = ({ g, t }) => {
  const a = janela(t, g.t0, g.t1, 0.45, 0.35);
  if (a <= 0) return null;
  const C = { maquete: Maquete, corte: Corte, perfil: Perfil, vazao: Vazao, cheias3: Cheias3, chuva3m: Chuva3m, calendario: Calendario5, etapas: Etapas, wwa: Wwa, sms: Sms, frase: Frase, selo: Selo }[g.tipo];
  return C ? <C g={g} t={t} a={a} /> : null;
};
