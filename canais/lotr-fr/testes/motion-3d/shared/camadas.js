// Estado das camadas 2D em função do tempo (puro, determinístico). Usado pelas duas versões.
export function fmtKm(n) {
  return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}
const easeOut = (p) => 1 - Math.pow(1 - Math.min(1, Math.max(0, p)), 3);

// número grande + faixa navy. Devolve {texto, unidade, aprox, faixa, tNum (início do número atual), tFaixa}
export function numeroEm(cues, t) {
  let num = null, faixa = null;
  for (const c of cues.numero) {
    if (c.t > t) break;
    faixa = c;
    if (!c.manter) num = c;
  }
  if (!num) return null;
  let texto;
  if (num.valor !== undefined) texto = num.valor;
  else texto = fmtKm(num.de + (num.para - num.de) * easeOut((t - num.t) / (num.ate - num.t)));
  return { texto, unidade: num.unidade, aprox: !!num.aprox, faixa: faixa.faixa, tNum: num.t, tFaixa: faixa.t };
}

export function capituloEm(cues, t) {
  let cap = cues.capitulos[0];
  for (const c of cues.capitulos) if (c.t <= t) cap = c;
  return cap;
}

const LUGARES = /^(Comté|Fondcombe|Moria|Lórien|Mordor|kilomètres|anneau|compagnons)/i;

// legenda máquina de escrever: blocos separados por "|"; cada palavra digita entre seu início e o da próxima.
export function legendaEm(cues, t) {
  const blocos = [[]];
  for (const p of cues.palavras) {
    if (p === '|') blocos.push([]);
    else blocos[blocos.length - 1].push({ w: p[0], s: p[1] });
  }
  const todas = blocos.flat();
  todas.forEach((p, i) => { p.e = i + 1 < todas.length ? Math.min(todas[i + 1].s, p.s + 0.45) : p.s + 0.5; });
  let atual = null;
  for (const b of blocos) if (b.length && b[0].s <= t + 0.02) atual = b;
  if (!atual || t > cues.fim_fala + 0.8) return null;
  const palavras = atual.map((p) => {
    const frac = Math.min(1, Math.max(0, (t - p.s) / Math.max(0.12, (p.e - p.s) * 0.8)));
    const n = Math.round(frac * p.w.length);
    return { texto: p.w.slice(0, n), completo: n === p.w.length, destaque: LUGARES.test(p.w), visivel: n > 0 };
  }).filter((p) => p.visivel);
  return { palavras, tBloco: atual[0].s };
}

// popping: escala de entrada com overshoot (0 → 1.12 → 1) em ~0.35 s
export function pop(t, t0, dur = 0.35) {
  const p = (t - t0) / dur;
  if (p <= 0) return 0;
  if (p >= 1) return 1;
  const s = 1.70158 * 1.5;
  const q = p - 1;
  return 1 + (s + 1) * q * q * q + s * q * q;
}
