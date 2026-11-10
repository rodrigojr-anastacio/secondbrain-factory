// Visual v2 (Em Relevo 002, 10/11/2026): terreno real sob a cena 3D (só quando opts.estilo = 'A' | 'B' | 'C').
// Planos deslocados pela altura do NOAA ETOPO 2022 com a textura do estilo (NASA Blue Marble ou relevo sombreado gerado do ETOPO,
// ver visual-v2/codigo/gera_texturas.py). Três planos: Brasil detalhado, Brasil largo (o resto do continente/oceano) e Pacífico.
// - foco: o shader escurece e dessatura o que está longe do alvo da câmera (a região de interesse fica viva, o resto recua);
// - máscara: as UFs tingidas (tintas/amazônia) são pintadas num canvas e "drapeadas" no terreno (sem placa flutuando);
// - fronteiras e municípios viram linhas drapeadas no relevo.

export const ESTILOS = {
  A: { fundo: '#0E2A50', pais: ['#FFFFFF', 0.55], uf: ['#FFFFFF', 0.32], sul: ['#FFFFFF', 0.85], mun: ['#FFFFFF', 0.16], dim: 0.5, dessat: 0.6, brilho: 0.64 },
  B: { fundo: '#1F2A44', pais: ['#2B2622', 0.55], uf: ['#2B2622', 0.3], sul: ['#1F2A44', 0.8], mun: ['#5A4A3A', 0.2], dim: 0.38, dessat: 0.5, brilho: 0.68 },
  C: { fundo: '#2E6170', pais: ['#3A2A1C', 0.6], uf: ['#3A2A1C', 0.32], sul: ['#3A2A1C', 0.85], mun: ['#6B5236', 0.2], dim: 0.32, dessat: 0.45, brilho: 0.7 },
};
// regiões das texturas (iguais às de gera_texturas.py)
export const REGIOES = {
  br_largo: [-140, 20, -75, 35], br_det: [-84, -28, -40, 8], pac: [95, 295, -45, 45],
};
export const arquivosTerreno = (estilo) => Object.keys(REGIOES).flatMap((r) => [`v2/${estilo}_${r}.jpg`, `v2/alt_${r}.png`]);

// decodifica o png de altura (R = alto, G = baixo) -> metros
export async function lerAltura(url) {
  const blob = await (await fetch(url)).blob();
  const bmp = await createImageBitmap(blob, { colorSpaceConversion: 'none', premultiplyAlpha: 'none' });
  const cv = new OffscreenCanvas(bmp.width, bmp.height);
  const cx = cv.getContext('2d', { willReadFrequently: true });
  cx.drawImage(bmp, 0, 0);
  const d = cx.getImageData(0, 0, bmp.width, bmp.height).data;
  const z = new Float32Array(bmp.width * bmp.height);
  for (let i = 0; i < z.length; i++) z[i] = ((d[i * 4] << 8) | d[i * 4 + 1]) / 65535 * 18000 - 11000;
  return { w: bmp.width, h: bmp.height, z };
}

export function criarTerreno(THREE, scene, geo, cues, opts) {
  const E = ESTILOS[opts.estilo];
  const T = opts.terreno; // { tex: {chave: THREE.Texture}, alt: {regiao: {w,h,z}} }
  const PJ = geo.proj, PAC = geo.pac;
  const brXZ = (lon, lat) => [(lon - PJ.lon0) * PJ.cos * PJ.k, -(lat - PJ.lat0) * PJ.k];
  const brLL = (x, z) => [PJ.lon0 + x / (PJ.cos * PJ.k), PJ.lat0 - z / PJ.k];
  const pacXZ = (lon, lat) => [PAC.x0 + (lon - PAC.lonc) * PAC.k, PAC.z0 - lat * PAC.k];
  const pacLL = (x, z) => [PAC.lonc + (x - PAC.x0) / PAC.k, -(z - PAC.z0) / PAC.k];

  // metros -> y da cena (exagero vertical; 0,012 = nível do mar, como o antigo mar de papel)
  const yBR = (m) => 0.012 + (m > 0 ? m * 0.000105 : Math.max(m, -6500) * 0.000012);
  const yPAC = (m) => 0.012 + (m > 0 ? m * 0.00005 : Math.max(m, -6500) * 0.000004);

  const amostra = (A, reg, lon, lat) => {
    const [l0, l1, a0, a1] = REGIOES[reg];
    const fx = (lon - l0) / (l1 - l0) * A.w - 0.5, fy = (a1 - lat) / (a1 - a0) * A.h - 0.5;
    const x0 = Math.max(0, Math.min(A.w - 2, Math.floor(fx))), y0 = Math.max(0, Math.min(A.h - 2, Math.floor(fy)));
    const u = Math.min(1, Math.max(0, fx - x0)), v = Math.min(1, Math.max(0, fy - y0));
    const i = y0 * A.w + x0;
    return (A.z[i] * (1 - u) + A.z[i + 1] * u) * (1 - v) + (A.z[i + A.w] * (1 - u) + A.z[i + A.w + 1] * u) * v;
  };
  const dentroReg = (reg, lon, lat, m = 0) => { const [l0, l1, a0, a1] = REGIOES[reg]; return lon > l0 + m && lon < l1 - m && lat > a0 + m && lat < a1 - m; };
  // altura da cena no ponto (x, z) do Brasil
  const alturaBR = (x, z) => { const [lon, lat] = brLL(x, z); return yBR(amostra(dentroReg('br_det', lon, lat) ? T.alt.br_det : T.alt.br_largo, dentroReg('br_det', lon, lat) ? 'br_det' : 'br_largo', lon, lat)); };

  // máscara (UFs tingidas) sobre a caixa do br_det
  const [dx0, dz0] = brXZ(REGIOES.br_det[0], REGIOES.br_det[3]), [dx1, dz1] = brXZ(REGIOES.br_det[1], REGIOES.br_det[2]);
  const MW = 2048, MH = Math.round(MW * (dz1 - dz0) / (dx1 - dx0));
  const cv = document.createElement('canvas'); cv.width = MW; cv.height = MH;
  const cx = cv.getContext('2d');
  const texMask = new THREE.CanvasTexture(cv); texMask.colorSpace = THREE.SRGBColorSpace;

  const uniFoco = { uFoco: { value: new THREE.Vector2() }, uRaio: { value: 30 }, uDim: { value: E.dim }, uDessat: { value: E.dessat } };
  const material = (mapa, comMascara, recorte) => {
    const m = new THREE.MeshLambertMaterial({ map: mapa, color: new THREE.Color(E.brilho, E.brilho, E.brilho) });   // Lambert: mesmo difuso do Standard, sem o especular (mais barato)
    m.onBeforeCompile = (sh) => {
      Object.assign(sh.uniforms, uniFoco, { uMask: { value: texMask }, uMin: { value: new THREE.Vector2(dx0, dz0) }, uMax: { value: new THREE.Vector2(dx1, dz1) } });
      sh.vertexShader = 'varying vec3 vWp;\n' + sh.vertexShader.replace('#include <project_vertex>', '#include <project_vertex>\n vWp = (modelMatrix * vec4(transformed, 1.0)).xyz;');
      sh.fragmentShader = 'varying vec3 vWp;\nuniform vec2 uFoco; uniform float uRaio, uDim, uDessat; uniform sampler2D uMask; uniform vec2 uMin, uMax;\n' +
        sh.fragmentShader.replace('#include <map_fragment>', `#include <map_fragment>
  vec2 muv = (vWp.xz - uMin) / (uMax - uMin);
  ${recorte ? 'if (muv.x > 0.004 && muv.x < 0.996 && muv.y > 0.004 && muv.y < 0.996) discard;' : ''}
  ${comMascara ? 'if (muv.x > 0.0 && muv.x < 1.0 && muv.y > 0.0 && muv.y < 1.0) { vec4 mk = texture2D(uMask, vec2(muv.x, 1.0 - muv.y)); diffuseColor.rgb = mix(diffuseColor.rgb, mk.rgb * ' + E.brilho.toFixed(3) + ', mk.a); }' : ''}
  float fq = smoothstep(0.55, 1.45, distance(vWp.xz, uFoco) / uRaio) * uDim;
  float lu = dot(diffuseColor.rgb, vec3(0.299, 0.587, 0.114));
  diffuseColor.rgb = mix(diffuseColor.rgb, mix(diffuseColor.rgb, vec3(lu), uDessat) * 0.45, fq);`);
    };
    return m;
  };

  const plano = (reg, ll2xz, xz2ll, yFn, segX, mat) => {
    const [l0, l1, a0, a1] = REGIOES[reg];
    const [x0, z0] = ll2xz(l0, a1), [x1, z1] = ll2xz(l1, a0);
    const g = new THREE.PlaneGeometry(x1 - x0, z1 - z0, segX, Math.round(segX * (z1 - z0) / (x1 - x0)));
    g.rotateX(-Math.PI / 2); g.translate((x0 + x1) / 2, 0, (z0 + z1) / 2);
    const p = g.attributes.position;
    for (let i = 0; i < p.count; i++) { const [lon, lat] = xz2ll(p.getX(i), p.getZ(i)); p.setY(i, yFn(amostra(T.alt[reg], reg, lon, lat))); }
    p.needsUpdate = true; // normais ficam "para cima": o relevo já vem sombreado na textura (luz única, sem sombra dupla)
    const m = new THREE.Mesh(g, mat); m.receiveShadow = !PF.semSombra; scene.add(m);
    return m;
  };
  const tx = (k) => { const t = T.tex[k]; t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = opts.aniso ?? 1; return t; };   // anisotrópico custa caro no SwiftShader (medido em tempos.txt)
  const PF = opts.perf || {}; const SEG = PF.seg ?? 0.35;   // malha: 0.35 da original (vértices custam caro no SwiftShader; o relevo fino já vem sombreado na textura)
  const det = plano('br_det', brXZ, brLL, yBR, Math.max(8, Math.round(520 * SEG)), material(tx(`v2/${opts.estilo}_br_det.jpg`), true, false));
  const largo = plano('br_largo', brXZ, brLL, yBR, Math.max(8, Math.round(360 * (PF.segLargo ?? 0.12))), material(tx(`v2/${opts.estilo}_br_largo.jpg`), false, true));
  largo.position.y = -0.004; if (PF.semLargo) largo.visible = false;
  const pac = plano('pac', pacXZ, pacLL, yPAC, Math.max(8, Math.round(420 * SEG)), material(tx(`v2/${opts.estilo}_pac.jpg`), false, false));

  // linhas drapeadas: fronteiras de países, UFs, contorno do Sul e municípios
  const linhas = (aneis, cor, op, dy = 0.008) => {
    const s = [];
    for (const anel of aneis) for (let i = 1; i < anel.length; i++) {
      const [ax, az] = anel[i - 1], [bx, bz] = anel[i];
      const n = Math.max(1, Math.ceil(Math.hypot(bx - ax, bz - az) / 0.12));
      for (let k = 0; k < n; k++) {
        const u0 = k / n, u1 = (k + 1) / n;
        const px = ax + (bx - ax) * u0, pz = az + (bz - az) * u0, qx = ax + (bx - ax) * u1, qz = az + (bz - az) * u1;
        s.push(px, alturaBR(px, pz) + dy, pz, qx, alturaBR(qx, qz) + dy, qz);
      }
    }
    const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(s, 3));
    const l = new THREE.LineSegments(g, new THREE.LineBasicMaterial({ color: cor, transparent: true, opacity: op, depthWrite: false }));
    l.renderOrder = 1; if (!PF.semLinhas) scene.add(l); return l;
  };
  linhas(geo.vizinhos.filter((v) => !v.br).map((v) => v.anel), ...E.pais);
  linhas(geo.vizinhos.filter((v) => v.br).map((v) => v.anel), ...E.uf);
  linhas(geo.mun, ...E.mun, 0.006);
  linhas(Object.values(geo.estados).flat(), ...E.sul, 0.01);

  // máscara: redesenha só quando o estado das tintas muda
  const anelUF = {};
  for (const v of geo.vizinhos) if (v.br) (anelUF[v.nome] = anelUF[v.nome] || []).push(v.anel);
  const codSul = { PR: '41', SC: '42', RS: '43' };
  for (const [uf, aneis] of Object.entries(geo.estados)) anelUF[codSul[uf]] = aneis;
  let chave = '';
  const corTmp = new THREE.Color();
  function pintarMascara(t, interp) {
    const camadas = [];
    const amaz = interp(cues.amazonia, t);
    if (amaz > 0.01) camadas.push({ cor: '#7FA05A', a: 0.55 * amaz, ufs: geo.vizinhos.filter((v) => v.br && v.amaz).map((v) => v.nome) });
    for (const tn of cues.tintas || []) { const o = interp(tn.op, t); if (o > 0.005) camadas.push({ cor: tn.cor, a: Math.min(1, o * (tn.max ?? 0.85)) * 0.82, ufs: tn.ufs }); }
    const k = camadas.map((c) => `${c.cor}${c.a.toFixed(2)}${c.ufs.join()}`).join('|');
    if (k === chave) return;
    chave = k;
    cx.clearRect(0, 0, MW, MH);
    for (const c of camadas) {
      corTmp.set(c.cor); cx.fillStyle = `rgba(${Math.round(corTmp.r * 255)},${Math.round(corTmp.g * 255)},${Math.round(corTmp.b * 255)},${c.a})`;
      cx.beginPath();
      for (const cod of new Set(c.ufs)) for (const anel of anelUF[cod] || []) {
        anel.forEach(([x, z], i) => { const u = (x - dx0) / (dx1 - dx0) * MW, v = (z - dz0) / (dz1 - dz0) * MH; i ? cx.lineTo(u, v) : cx.moveTo(u, v); });
        cx.closePath();
      }
      cx.fill();
    }
    texMask.needsUpdate = true;
  }

  return {
    alturaBR,
    atualizar(t, alvo, dist, interp) {
      uniFoco.uFoco.value.set(alvo[0], alvo[2]);
      uniFoco.uRaio.value = Math.max(4, dist * 0.5);
      pintarMascara(t, interp);
    },
  };
}
