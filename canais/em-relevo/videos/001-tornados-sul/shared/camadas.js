// Estado das camadas 2D em função do tempo (puro, determinístico). Base: lotr-fr/testes/motion-3d/shared/camadas.js.
export function fmt(n) {
  return Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, '.');
}
export const easeOut = (p) => 1 - Math.pow(1 - Math.min(1, Math.max(0, p)), 3);
export const clamp01 = (x) => Math.min(1, Math.max(0, x));

// número grande + faixa navy. {texto, unidade, faixa, tNum}
export function numeroEm(cues, t) {
  let cur = null;
  for (const c of cues.numero) {
    if (c.t > t) break;
    cur = c;
  }
  if (!cur || cur.oculto) return null;
  const texto = cur.valor !== undefined ? cur.valor : fmt(cur.de + (cur.para - cur.de) * easeOut((t - cur.t) / (cur.ate - cur.t)));
  return { texto, unidade: cur.unidade, faixa: cur.faixa, tNum: cur.t };
}

export function capituloEm(cues, t) {
  let cap = cues.capitulos[0];
  for (const c of cues.capitulos) if (c.t <= t) cap = c;
  return cap;
}

const DESTAQUE = /^(Maringá|Chapecó|Santo|Augusto|Paraná|Catarina|Rio|Grande|Sul|F\d|\d|El|Niño|Amazônia|Andes|Argentina|supercélula|corredor|magnitude|pico|Xanxerê|Guaraciaba|Bonito|Iguaçu|Negrinho|Erval|Palmeira|mesociclone|tornado|NASA|IPCC|NOAA|40199|inédito|caixinha)/i;

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
  if (!atual || t > cues.fim_fala + 0.6) return null;
  const palavras = atual.map((p) => {
    const frac = clamp01((t - p.s) / Math.max(0.12, (p.e - p.s) * 0.8));
    const n = Math.round(frac * p.w.length);
    return { texto: p.w.slice(0, n), completo: n === p.w.length, destaque: DESTAQUE.test(p.w), visivel: n > 0 };
  }).filter((p) => p.visivel);
  return { palavras, tBloco: atual[0].s };
}

// pop com overshoot (0 → 1.12 → 1)
export function pop(t, t0, dur = 0.35) {
  const p = (t - t0) / dur;
  if (p <= 0) return 0;
  if (p >= 1) return 1;
  const s = 1.70158 * 1.5;
  const q = p - 1;
  return 1 + (s + 1) * q * q * q + s * q * q;
}
// entra com pop e sai com fade
export function janela(t, t0, t1, din = 0.35, dout = 0.3) {
  if (t < t0 || t > t1 + dout) return 0;
  return Math.min(pop(t, t0, din), 1 - clamp01((t - t1) / dout));
}
