// Mundo 3D "maquete de papel" da Terra-média, ESTILIZADO e procedural (não copia nenhum mapa oficial).
// Puro three.js, sem dependência de framework: recebe o THREE de quem chama (Remotion/R3F ou Hyperframes)
// e expõe update(t) determinístico (t em segundos) + project() para as camadas 2D.
// Fonte única: canais/lotr-fr/testes/motion-3d/shared/cena3d.js (teste de motion, 06/11/2026).

// ---------- utilidades determinísticas ----------
function hash2(ix, iz) {
  let h = (ix * 374761393 + iz * 668265263) | 0;
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  h ^= h >>> 16;
  return (h >>> 0) / 4294967295;
}
function sq(v) { return v * v; }
function smooth(a, b, x) {
  const t = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
}
function vnoise(x, z) {
  const ix = Math.floor(x), iz = Math.floor(z);
  const fx = x - ix, fz = z - iz;
  const ux = fx * fx * (3 - 2 * fx), uz = fz * fz * (3 - 2 * fz);
  const a = hash2(ix, iz), b = hash2(ix + 1, iz), c = hash2(ix, iz + 1), d = hash2(ix + 1, iz + 1);
  return a + (b - a) * ux + (c - a) * uz + (a - b - c + d) * ux * uz;
}
function fbm(x, z, oct = 4) {
  let s = 0, amp = 0.5, f = 1;
  for (let i = 0; i < oct; i++) { s += amp * vnoise(x * f, z * f); f *= 2.03; amp *= 0.5; }
  return s; // ~0..1
}
function ridged(x, z) {
  let s = 0, amp = 0.55, f = 1, w = 1;
  for (let i = 0; i < 5; i++) {
    let n = 1 - Math.abs(2 * vnoise(x * f, z * f) - 1);
    n = n * n * w;
    w = Math.min(1, n * 2);
    s += n * amp; f *= 2.1; amp *= 0.5;
  }
  return s; // ~0..1
}
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function interpTabela(tab, t) {
  if (t <= tab[0][0]) return tab[0][1];
  for (let i = 1; i < tab.length; i++) {
    if (t <= tab[i][0]) {
      const [t0, v0] = tab[i - 1], [t1, v1] = tab[i];
      return v0 + (v1 - v0) * smooth(0, 1, (t - t0) / (t1 - t0));
    }
  }
  return tab[tab.length - 1][1];
}

// ---------- geografia estilizada ----------
const SLAB = 0.28;          // espessura da folha de papel (terra) sobre a mesa
const STEP = 0.09;          // altura de cada camada de papel (curvas de nível)
const MORDOR = { x0: 5.7, x1: 11.5, z0: 2.3, z1: 6.4 };
const ORODRUIN = { x: 7.6, z: 4.2 };
const COMTE = { x: -7.0, z: -0.9 };
const LORIEN = { x: 1.9, z: 1.45 };

function mistyX(z) { return 0.15 + 0.45 * Math.sin(z * 0.55 + 0.4); }
function anduinX(z) { return 3.05 + 0.28 * Math.sin(z * 0.9 + 1.0); }

// altura "crua" (sem terraços), acima do tampo da mesa
export function alturaCrua(x, z) {
  // contorno da folha: borda oeste recortada (costa), demais bordas retas e rasgadas
  const costa = -9.3 + 0.7 * (fbm(0.5, z * 0.35 + 3.1) - 0.5) * 2;
  const sdf = Math.min(x - costa, 11.6 - x, z + 6.8, 7.0 - z) + 0.12 * (fbm(x * 1.7, z * 1.7) - 0.5);
  const terra = smooth(-0.04, 0.04, sdf);
  if (terra <= 0) return 0;
  let h = 0.05 * fbm(x * 0.7 + 10, z * 0.7);
  // colinas da Comté
  const dC = Math.hypot(x - COMTE.x, z - COMTE.z);
  h += 0.32 * Math.exp(-(dC * dC) / 3.0) * fbm(x * 1.6, z * 1.6 + 5);
  // Monts Brumeux: crista norte-sul com picos (ridged multifractal)
  const tz = smooth(-7.5, -5.8, z) * (1 - smooth(0.9, 2.1, z));
  const dx = (x - mistyX(z)) / 0.8;
  const env = Math.exp(-dx * dx) * tz;
  if (env > 0.01) h += 1.35 * env * (0.25 + 0.95 * ridged(x * 1.6 + 40, z * 1.6));
  // Ered Nimrais (montanhas brancas): leste-oeste ao sul
  const tx = smooth(-3.5, -2.0, x) * (1 - smooth(4.0, 5.2, x));
  const dz = (z - (5.3 + 0.35 * Math.sin(x * 0.7))) / 0.55;
  const env2 = Math.exp(-dz * dz) * tx;
  if (env2 > 0.01) h += 0.95 * env2 * (0.25 + 0.9 * ridged(x * 1.7 + 11, z * 1.7 + 4));
  // Mordor: muralha em U (norte, oeste, sul) + planalto
  const dN = Math.abs(z - MORDOR.z0), dW = Math.abs(x - MORDOR.x0), dS = Math.abs(z - MORDOR.z1);
  const emX = x > MORDOR.x0 - 0.6, emZ = z > MORDOR.z0 - 0.6 && z < MORDOR.z1 + 0.6;
  let muro = 0;
  if (x > MORDOR.x0 - 0.5) muro = Math.max(muro, Math.exp(-sq(dN / 0.34)), Math.exp(-sq(dS / 0.34)) * smooth(4.0, 5.0, x));
  if (emZ) muro = Math.max(muro, Math.exp(-sq(dW / 0.34)));
  if (!emX) muro *= smooth(MORDOR.x0 - 1.3, MORDOR.x0 - 0.5, x);
  if (muro > 0.01) h += 0.95 * muro * (0.35 + 0.85 * ridged(x * 2.2 + 70, z * 2.2));
  const dentro = smooth(MORDOR.x0, MORDOR.x0 + 0.3, x) * smooth(MORDOR.z0, MORDOR.z0 + 0.3, z) * (1 - smooth(MORDOR.z1 - 0.3, MORDOR.z1, z));
  h += 0.13 * dentro;
  // Orodruin
  const dO = Math.hypot(x - ORODRUIN.x, z - ORODRUIN.z);
  h += 1.2 * Math.pow(Math.max(0, 1 - dO / 1.0), 1.5) - 0.3 * Math.max(0, 1 - dO / 0.16);
  // Emyn Muil
  const dE = Math.hypot(x - 3.9, z - 3.0);
  h += 0.42 * Math.exp(-(dE * dE) / 0.45) * fbm(x * 2.5, z * 2.5 + 9);
  // Anduin (sulco)
  const dR = (x - anduinX(z)) / 0.085;
  h -= 0.05 * Math.exp(-dR * dR);
  return (SLAB + Math.max(-0.04, h)) * terra;
}
function terraco(hc) {
  if (hc <= SLAB + 0.001) return hc;
  const rel = hc - SLAB, f = rel / STEP, i = Math.floor(f), fr = f - i;
  return SLAB + STEP * (i + smooth(0.86, 1.0, fr));
}
export function altura(x, z) { return terraco(alturaCrua(x, z)); }

function rioMask(x, z) { const d = (x - anduinX(z)) / 0.085; return Math.exp(-d * d); }
function mordorMask(x, z) {
  return smooth(MORDOR.x0 - 0.45, MORDOR.x0 + 0.1, x) * smooth(MORDOR.z0 - 0.45, MORDOR.z0 + 0.1, z) * (1 - smooth(MORDOR.z1 - 0.1, MORDOR.z1 + 0.45, z));
}

// ---------- curva Hermite (Catmull-Rom no tempo) para a câmera ----------
function hermite(keys, t, campo) {
  const n = keys.length;
  if (t <= keys[0].t) return keys[0][campo].slice();
  if (t >= keys[n - 1].t) return keys[n - 1][campo].slice();
  let i = 0;
  while (t > keys[i + 1].t) i++;
  const k0 = keys[i], k1 = keys[i + 1];
  const tang = (j) => {
    const a = keys[Math.max(0, j - 1)], b = keys[Math.min(n - 1, j + 1)];
    return a[campo].map((v, c) => (b[campo][c] - v) / (b.t - a.t));
  };
  const m0 = tang(i), m1 = tang(i + 1);
  const dt = k1.t - k0.t, s = (t - k0.t) / dt;
  const h00 = 2 * s ** 3 - 3 * s ** 2 + 1, h10 = s ** 3 - 2 * s ** 2 + s, h01 = -2 * s ** 3 + 3 * s ** 2, h11 = s ** 3 - s ** 2;
  return k0[campo].map((v, c) => h00 * v + h10 * dt * m0[c] + h01 * k1[campo][c] + h11 * dt * m1[c]);
}

// queda com bounce leve: 0 = no chão, 1 = alto
function queda(p) {
  if (p <= 0) return 1;
  if (p < 0.55) { const q = p / 0.55; return 1 - q * q; }
  if (p < 0.8) return 0.10 * Math.sin(Math.PI * (p - 0.55) / 0.25);
  if (p < 1) return 0.025 * Math.sin(Math.PI * (p - 0.8) / 0.2);
  return 0;
}

// ---------- montagem ----------
export function criarMundo(THREE, cues, opts = {}) {
  const segX = opts.segX ?? 440, segZ = opts.segZ ?? 290;
  const W = 28, D = 19, CX = 1.0, CZ = 0.2;
  const scene = new THREE.Scene();
  const fundo = new THREE.Color('#B9A47F');
  scene.background = fundo;
  scene.fog = new THREE.Fog(fundo, 26, 55);

  // terreno
  const geo = new THREE.PlaneGeometry(W, D, segX, segZ);
  geo.rotateX(-Math.PI / 2);
  geo.translate(CX, 0, CZ);
  const pos = geo.attributes.position;
  const cores = new Float32Array(pos.count * 3);
  const reg = new Float32Array(pos.count * 3);
  const c = new THREE.Color();
  const papel = new THREE.Color('#EADDC4'), papelClaro = new THREE.Color('#F4EBDA'), mesa = new THREE.Color('#A88F69');
  const cinzaM = new THREE.Color('#9A897C'), escuroM = new THREE.Color('#76675F'), rio = new THREE.Color('#5C6F8E');
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), z = pos.getZ(i);
    const hc = alturaCrua(x, z), h = terraco(hc);
    pos.setY(i, h);
    if (hc < 0.02) {
      c.copy(mesa).multiplyScalar(0.94 + 0.08 * fbm(x * 3, z * 3));
    } else {
      const nivel = Math.floor(Math.max(0, h - SLAB) / STEP);
      c.copy(papel).lerp(papelClaro, Math.min(1, nivel * 0.07));
      if (nivel % 2 === 1) c.multiplyScalar(0.955);
      const m = mordorMask(x, z);
      if (m > 0) c.lerp(h > SLAB + 0.35 ? escuroM : cinzaM, m * 0.85);
      c.lerp(rio, rioMask(x, z) * 0.8 * (1 - m));
      c.multiplyScalar(0.96 + 0.07 * fbm(x * 6.0, z * 6.0, 3));
    }
    cores[i * 3] = c.r; cores[i * 3 + 1] = c.g; cores[i * 3 + 2] = c.b;
    const dC = Math.hypot(x - COMTE.x, (z - COMTE.z) * 1.15) + 0.35 * (fbm(x * 1.4, z * 1.4) - 0.5);
    const dL = Math.hypot(x - LORIEN.x, z - LORIEN.z) + 0.25 * (fbm(x * 1.8 + 3, z * 1.8) - 0.5);
    reg[i * 3] = hc > 0.02 ? 1 - smooth(1.3, 1.45, dC) : 0;
    reg[i * 3 + 1] = hc > 0.02 ? 1 - smooth(0.85, 1.0, dL) : 0;
    reg[i * 3 + 2] = hc > 0.02 ? mordorMask(x, z) : 0;
  }
  geo.setAttribute('color', new THREE.BufferAttribute(cores, 3));
  geo.setAttribute('aRegiao', new THREE.BufferAttribute(reg, 3));
  geo.computeVertexNormals();

  const uRealce = { value: new THREE.Vector3(0, 0, 0) };
  const matTerra = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.96, metalness: 0 });
  matTerra.onBeforeCompile = (sh) => {
    sh.uniforms.uRealce = uRealce;
    sh.uniforms.uRosa = { value: new THREE.Color('#F0A9A0') };
    sh.uniforms.uCoral = { value: new THREE.Color('#E8505B') };
    sh.vertexShader = sh.vertexShader
      .replace('#include <common>', '#include <common>\nattribute vec3 aRegiao;\nvarying vec3 vRegiao;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\nvRegiao = aRegiao;');
    sh.fragmentShader = sh.fragmentShader
      .replace('#include <common>', '#include <common>\nuniform vec3 uRealce;\nuniform vec3 uRosa;\nuniform vec3 uCoral;\nvarying vec3 vRegiao;')
      .replace('#include <color_fragment>', '#include <color_fragment>\n' +
        'diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb * uRosa * 1.08, clamp(vRegiao.x * uRealce.x + vRegiao.y * uRealce.y, 0.0, 1.0) * 0.75);\n' +
        'diffuseColor.rgb = mix(diffuseColor.rgb, diffuseColor.rgb * uCoral * 1.25, vRegiao.z * uRealce.z * 0.5);');
  };
  matTerra.customProgramCacheKey = () => 'terra-realce';
  const terra = new THREE.Mesh(geo, matTerra);
  terra.castShadow = true; terra.receiveShadow = true;
  scene.add(terra);

  // mesa infinita por baixo
  const mesaMesh = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), new THREE.MeshStandardMaterial({ color: '#A88F69', roughness: 1 }));
  mesaMesh.rotation.x = -Math.PI / 2; mesaMesh.position.y = -0.002; mesaMesh.receiveShadow = true;
  scene.add(mesaMesh);

  // luzes: fim de tarde, sol baixo vindo do oeste
  const hemi = new THREE.HemisphereLight('#F4EEE4', '#6E5C49', 0.8);
  scene.add(hemi);
  const sol = new THREE.DirectionalLight('#FFE2BE', 2.0);
  sol.castShadow = true;
  sol.shadow.mapSize.set(opts.sombra ?? 2048, opts.sombra ?? 2048);
  const sc = sol.shadow.camera; sc.left = -17; sc.right = 17; sc.top = 12; sc.bottom = -12; sc.near = 1; sc.far = 60;
  sol.shadow.bias = -0.0006; sol.shadow.normalBias = 0.02;
  sol.position.set(-12 + CX, 7.5, 4 + CZ); sol.target.position.set(CX, 0, CZ);
  scene.add(sol); scene.add(sol.target);
  const brasa = new THREE.PointLight('#FF5030', 0, 5, 2);
  brasa.position.set(ORODRUIN.x, altura(ORODRUIN.x, ORODRUIN.z) + 0.9, ORODRUIN.z);
  scene.add(brasa);
  const cratera = new THREE.Mesh(new THREE.SphereGeometry(0.13, 16, 10), new THREE.MeshStandardMaterial({ color: '#3a1d17', emissive: '#FF4A20', emissiveIntensity: 0 }));
  cratera.position.set(ORODRUIN.x, altura(ORODRUIN.x, ORODRUIN.z) - 0.06, ORODRUIN.z);
  cratera.visible = false;
  scene.add(cratera);

  // casinhas da Comté (miniaturas) e árvores douradas da Lórien
  const r = rng(1954);
  const casas = [];
  for (let k = 0; casas.length < 42 && k < 400; k++) {
    const a = r() * Math.PI * 2, d = 0.3 + r() * 1.1;
    const x = COMTE.x + Math.cos(a) * d * 1.2, z = COMTE.z + Math.sin(a) * d;
    if (alturaCrua(x, z) < 0.2) continue;
    casas.push({ x, z, rot: r() * Math.PI, s: 1.3 + r() * 0.7, t: 4.9 + r() * 1.1 });
  }
  const corpoGeo = new THREE.BoxGeometry(0.13, 0.08, 0.1); corpoGeo.translate(0, 0.04, 0);
  const telhaGeo = new THREE.ConeGeometry(0.1, 0.07, 4); telhaGeo.rotateY(Math.PI / 4); telhaGeo.scale(1.0, 1, 0.8); telhaGeo.translate(0, 0.115, 0);
  const corpos = new THREE.InstancedMesh(corpoGeo, new THREE.MeshStandardMaterial({ color: '#F6F0E4', roughness: 0.9 }), casas.length);
  const telhas = new THREE.InstancedMesh(telhaGeo, new THREE.MeshStandardMaterial({ color: '#C65A4E', roughness: 0.9 }), casas.length);
  corpos.castShadow = telhas.castShadow = true; corpos.receiveShadow = true;
  scene.add(corpos, telhas);
  const arvores = [];
  for (let k = 0; arvores.length < 150 && k < 2000; k++) {
    const a = r() * Math.PI * 2, d = Math.sqrt(r()) * 0.9;
    if (d < 0.2) continue;
    const x = LORIEN.x + Math.cos(a) * d, z = LORIEN.z + Math.sin(a) * d * 0.85;
    arvores.push({ x, z, s: 0.7 + r() * 0.6, t: 12.15 + d * 0.8 + r() * 0.25 });
  }
  const copaGeo = new THREE.ConeGeometry(0.06, 0.22, 7); copaGeo.translate(0, 0.11, 0);
  const copas = new THREE.InstancedMesh(copaGeo, new THREE.MeshStandardMaterial({ color: '#D9AE4E', roughness: 0.85 }), arvores.length);
  copas.castShadow = true;
  scene.add(copas);

  // florestas estáticas (Grand'Peur e Fangorn): cones foscos oliva
  const mata = [];
  for (let k = 0; mata.length < 520 && k < 6000; k++) {
    let x, z;
    if (k % 5 === 0) { const a = r() * 6.283, d = Math.sqrt(r()) * 0.6; x = 1.2 + Math.cos(a) * d; z = 3.4 + Math.sin(a) * d * 0.8; }
    else { x = 4.1 + r() * 3.6; z = -5.6 + r() * 4.6; if (fbm(x * 0.9, z * 0.9 + 20) < 0.42) continue; }
    if (alturaCrua(x, z) < 0.25 || rioMask(x, z) > 0.05) continue;
    mata.push({ x, z, s: 0.6 + r() * 0.6 });
  }
  const mataGeo = new THREE.ConeGeometry(0.055, 0.17, 6); mataGeo.translate(0, 0.085, 0);
  const matas = new THREE.InstancedMesh(mataGeo, new THREE.MeshStandardMaterial({ color: '#8E8A62', roughness: 0.95 }), mata.length);
  matas.castShadow = true; matas.receiveShadow = true;
  mata.forEach((k, i) => { matas.setMatrixAt(i, new THREE.Matrix4().compose(new THREE.Vector3(k.x, altura(k.x, k.z) - 0.01, k.z), new THREE.Quaternion(), new THREE.Vector3(k.s, k.s, k.s))); });
  scene.add(matas);

  // pinos
  const matPino = new THREE.MeshStandardMaterial({ color: '#E8505B', roughness: 0.45 });
  const matAgulha = new THREE.MeshStandardMaterial({ color: '#3A3634', roughness: 0.5, metalness: 0.3 });
  const pinos = cues.pinos.map((p) => {
    const g = new THREE.Group();
    const agulha = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 0.5, 8), matAgulha);
    agulha.position.y = 0.25;
    const cabeca = new THREE.Mesh(new THREE.SphereGeometry(0.11, 24, 16), matPino);
    cabeca.position.y = 0.54;
    agulha.castShadow = cabeca.castShadow = true;
    g.add(agulha, cabeca);
    const y0 = altura(p.x, p.z);
    g.position.set(p.x, y0, p.z);
    g.visible = false;
    scene.add(g);
    return { ...p, g, y0 };
  });

  // fios vermelhos (tubos deitados sobre a maquete, revelados progressivamente)
  const matFio = new THREE.MeshStandardMaterial({ color: '#D8404B', roughness: 0.6 });
  const TUB = 220, RAD = 6;
  const fios = cues.fios.map((f) => {
    const p2 = f.pontos.map(([x, z]) => new THREE.Vector3(x, 0, z));
    const curva2 = new THREE.CatmullRomCurve3(p2, false, 'centripetal');
    const amostras = curva2.getSpacedPoints(160).map((v, i, arr) => {
      const u = i / (arr.length - 1);
      const solo = Math.max(alturaCrua(v.x, v.z) + 0.12, altura(v.x, v.z) + 0.05);
      // nas montanhas o fio passa POR DENTRO (Moria, Cirith Ungol): limita a altura e ele some no relevo
      const soloC = Math.min(solo, SLAB + 0.5);
      return new THREE.Vector3(v.x, soloC + 0.09 * Math.sin(Math.PI * u), v.z);
    });
    const curva = new THREE.CatmullRomCurve3(amostras);
    const g = new THREE.TubeGeometry(curva, TUB, 0.022, RAD, false);
    const m = new THREE.Mesh(g, matFio);
    m.castShadow = true;
    g.setDrawRange(0, 0);
    scene.add(m);
    return { ...f, m, g, curva };
  });

  const camera = new THREE.PerspectiveCamera(36, cues.largura / cues.altura, 0.1, 200);
  const tmpM = new THREE.Matrix4(), tmpQ = new THREE.Quaternion(), tmpS = new THREE.Vector3(), tmpP = new THREE.Vector3(), eixoY = new THREE.Vector3(0, 1, 0);

  function update(t) {
    // câmera contínua (nunca para): spline no tempo + deriva lenta
    const p = hermite(cues.camera, t, 'pos'), a = hermite(cues.camera, t, 'alvo');
    camera.position.set(p[0] + 0.25 * Math.sin(t * 0.45), p[1], p[2] + 0.15 * Math.cos(t * 0.38));
    camera.lookAt(a[0], a[1], a[2]);
    camera.updateMatrixWorld();

    const luz = interpTabela(cues.luz, t);
    sol.intensity = 2.0 * luz;
    hemi.intensity = 0.8 * (0.4 + 0.6 * luz);
    const tMordor = smooth(14.2, 15.2, t);
    sol.color.set('#FFE2BE').lerp(new THREE.Color('#FF9C72'), tMordor * 0.6);
    brasa.intensity = 6 * tMordor;
    cratera.material.emissiveIntensity = 2.5 * tMordor;
    cratera.visible = tMordor > 0.01;

    uRealce.value.set(
      interpTabela(cues.realce.comte, t),
      interpTabela(cues.realce.lorien, t),
      interpTabela(cues.realce.mordor, t)
    );

    pinos.forEach((pi) => {
      const pr = (t - pi.t) / 0.6;
      pi.g.visible = t >= pi.t;
      pi.g.position.y = pi.y0 + 2.4 * queda(pr);
    });
    fios.forEach((f) => {
      const u = smooth(f.t0, f.t1, t);
      f.g.setDrawRange(0, Math.floor(u * TUB) * RAD * 6);
    });
    casas.forEach((k, i) => {
      const s = k.s * Math.min(1, Math.max(0, (t - k.t) / 0.35)) ** 0.7;
      tmpQ.setFromAxisAngle(eixoY, k.rot);
      tmpS.set(s || 1e-4, s || 1e-4, s || 1e-4);
      tmpP.set(k.x, altura(k.x, k.z) - 0.01, k.z);
      tmpM.compose(tmpP, tmpQ, tmpS);
      corpos.setMatrixAt(i, tmpM); telhas.setMatrixAt(i, tmpM);
    });
    corpos.instanceMatrix.needsUpdate = telhas.instanceMatrix.needsUpdate = true;
    arvores.forEach((k, i) => {
      const s = k.s * Math.min(1, Math.max(0, (t - k.t) / 0.4));
      tmpQ.identity();
      tmpS.set(s || 1e-4, s || 1e-4, s || 1e-4);
      tmpP.set(k.x, altura(k.x, k.z) - 0.01, k.z);
      tmpM.compose(tmpP, tmpQ, tmpS);
      copas.setMatrixAt(i, tmpM);
    });
    copas.instanceMatrix.needsUpdate = true;
  }

  // posições de tela (px) para as camadas 2D: pinos (cabeça) e rótulos do mapa
  const v = new THREE.Vector3();
  function projetar(w = cues.largura, h = cues.altura) {
    const conv = (x, y, z) => {
      v.set(x, y, z).project(camera);
      return { x: (v.x * 0.5 + 0.5) * w, y: (-v.y * 0.5 + 0.5) * h, ok: v.z < 1 && v.z > -1 };
    };
    return {
      pinos: pinos.map((p) => ({ id: p.id, ...conv(p.x, p.g.position.y + 0.66, p.z) })),
      rotulos: cues.rotulos_mapa.map((r) => ({ nome: r.nome, ...conv(r.x, altura(r.x, r.z) + 0.05, r.z) })),
    };
  }

  function configurarRenderer(renderer) {
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.NoToneMapping;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
  }

  update(0);
  return { scene, camera, update, projetar, configurarRenderer };
}
