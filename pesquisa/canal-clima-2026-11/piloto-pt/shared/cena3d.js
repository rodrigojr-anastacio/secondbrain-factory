// Mundo 3D "maquete de papel" do Sul do Brasil (PR/SC/RS extrudados a partir da malha do IBGE).
// three.js puro: recebe o THREE de quem chama, update(t) determinístico (t em segundos) e projetar() para as camadas 2D.
// Base: canais/lotr-fr/testes/motion-3d/shared/cena3d.js (teste de motion, 06/11/2026). Piloto clima pt, 08/11/2026.

function smooth(a, b, x) {
  const t = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
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
function queda(p) {
  if (p <= 0) return 1;
  if (p < 0.55) { const q = p / 0.55; return 1 - q * q; }
  if (p < 0.8) return 0.10 * Math.sin(Math.PI * (p - 0.55) / 0.25);
  if (p < 1) return 0.025 * Math.sin(Math.PI * (p - 0.8) / 0.2);
  return 0;
}
const ALT = 0.32;      // altura dos estados do Sul (papel grosso)
const ALT_BR = 0.10;   // outros estados do Brasil
const ALT_PAIS = 0.05; // países vizinhos

export function criarMundo(THREE, cues, geo, opts = {}) {
  const scene = new THREE.Scene();
  const fundo = new THREE.Color('#B9A47F');
  scene.background = fundo;
  scene.fog = new THREE.Fog(fundo, 30, 70);

  const forma = (anel) => new THREE.Shape(anel.map(([x, z]) => new THREE.Vector2(x, -z)));
  const extrudar = (aneis, alt) => {
    const g = new THREE.ExtrudeGeometry(aneis.map(forma), { depth: alt, bevelEnabled: false, curveSegments: 1 });
    g.rotateX(-Math.PI / 2);
    return g;
  };

  // mesa
  const mesa = new THREE.Mesh(new THREE.PlaneGeometry(300, 300), new THREE.MeshStandardMaterial({ color: '#A88F69', roughness: 1 }));
  mesa.rotation.x = -Math.PI / 2; mesa.position.y = -0.002; mesa.receiveShadow = true;
  scene.add(mesa);

  // vizinhos (Brasil e países): papel mais baixo e mais escuro
  const matBR = [new THREE.MeshStandardMaterial({ color: '#DCCDB0', roughness: 1 }), new THREE.MeshStandardMaterial({ color: '#BFAA86', roughness: 1 })];
  const matPais = [new THREE.MeshStandardMaterial({ color: '#CDBC9C', roughness: 1 }), new THREE.MeshStandardMaterial({ color: '#B19C79', roughness: 1 })];
  for (const v of geo.vizinhos) {
    const m = new THREE.Mesh(extrudar([v.anel], v.br ? ALT_BR : ALT_PAIS), v.br ? matBR : matPais);
    m.receiveShadow = true; m.castShadow = true;
    scene.add(m);
  }

  // estados do Sul
  const tons = { PR: '#EEE2CB', SC: '#E9DCC2', RS: '#EBDFC6' };
  const estados = {};
  for (const [uf, aneis] of Object.entries(geo.estados)) {
    const mats = [new THREE.MeshStandardMaterial({ color: tons[uf], roughness: 0.95 }), new THREE.MeshStandardMaterial({ color: '#C9B48F', roughness: 1 })];
    const m = new THREE.Mesh(extrudar(aneis, ALT), mats);
    m.castShadow = true; m.receiveShadow = true;
    scene.add(m);
    estados[uf] = m;
  }

  // divisas municipais (linhas finas sobre o papel)
  const segs = [];
  for (const anel of geo.mun) for (let i = 1; i < anel.length; i++) segs.push(anel[i - 1][0], ALT + 0.003, anel[i - 1][1], anel[i][0], ALT + 0.003, anel[i][1]);
  const gl = new THREE.BufferGeometry();
  gl.setAttribute('position', new THREE.Float32BufferAttribute(segs, 3));
  const matLinha = new THREE.LineBasicMaterial({ color: '#9C8662', transparent: true, opacity: 0.6 });
  scene.add(new THREE.LineSegments(gl, matLinha));
  // contorno dos estados (mais forte)
  const segE = [];
  for (const aneis of Object.values(geo.estados)) for (const anel of aneis) for (let i = 1; i < anel.length; i++) segE.push(anel[i - 1][0], ALT + 0.004, anel[i - 1][1], anel[i][0], ALT + 0.004, anel[i][1]);
  const ge = new THREE.BufferGeometry();
  ge.setAttribute('position', new THREE.Float32BufferAttribute(segE, 3));
  scene.add(new THREE.LineSegments(ge, new THREE.LineBasicMaterial({ color: '#6E5D45', transparent: true, opacity: 0.7 })));

  // municípios atingidos: placas coral que sobem e acendem
  const destaques = cues.destaques.map((d) => {
    const mat = new THREE.MeshStandardMaterial({ color: '#E8505B', roughness: 0.6, emissive: '#E8505B', emissiveIntensity: 0 });
    const m = new THREE.Mesh(extrudar(geo.destaque[d.nome], 0.07), mat);
    m.position.y = ALT; m.castShadow = true; m.visible = false;
    scene.add(m);
    return { ...d, m, mat };
  });

  // corredor de tempestades (faixa translúcida)
  const matCorr = new THREE.MeshBasicMaterial({ color: '#E8505B', transparent: true, opacity: 0, depthWrite: false });
  const corr = new THREE.Mesh(extrudar([cues.corredor.anel], 0.01), matCorr);
  corr.position.y = ALT + 0.09; corr.renderOrder = 2;
  scene.add(corr);

  // satélite GOES (folha translúcida georreferenciada sobre a maquete)
  let sat = null;
  if (opts.texturaSat) {
    const b = cues.satelite.caixa; // [x0, z0, x1, z1]
    const g = new THREE.PlaneGeometry(b[2] - b[0], b[3] - b[1]);
    g.rotateX(-Math.PI / 2);
    opts.texturaSat.colorSpace = THREE.SRGBColorSpace;
    const mat = new THREE.MeshBasicMaterial({ map: opts.texturaSat, transparent: true, opacity: 0, depthWrite: false });
    sat = new THREE.Mesh(g, mat);
    sat.position.set((b[0] + b[2]) / 2, ALT + 0.6, (b[1] + b[3]) / 2);
    sat.renderOrder = 3;
    scene.add(sat);
  }

  // luzes
  const hemi = new THREE.HemisphereLight('#F4EEE4', '#6E5C49', 0.85);
  scene.add(hemi);
  const sol = new THREE.DirectionalLight('#FFE2BE', 2.0);
  sol.castShadow = true;
  sol.shadow.mapSize.set(opts.sombra ?? 1024, opts.sombra ?? 1024);
  const sc = sol.shadow.camera; sc.left = -14; sc.right = 14; sc.top = 14; sc.bottom = -14; sc.near = 1; sc.far = 70;
  sol.shadow.bias = -0.0008; sol.shadow.normalBias = 0.03;
  sol.position.set(-14, 11, 6); sol.target.position.set(-1, 0, 1);
  scene.add(sol); scene.add(sol.target);

  const alturaEm = () => ALT;

  // pinos
  const matPino = new THREE.MeshStandardMaterial({ color: '#E8505B', roughness: 0.45 });
  const matAgulha = new THREE.MeshStandardMaterial({ color: '#3A3634', roughness: 0.5, metalness: 0.3 });
  const pinos = cues.pinos.map((p) => {
    const g = new THREE.Group();
    const s = p.pequeno ? 0.65 : 1;
    const agulha = new THREE.Mesh(new THREE.CylinderGeometry(0.014 * s, 0.014 * s, 0.55 * s, 8), matAgulha);
    agulha.position.y = 0.275 * s;
    const cabeca = new THREE.Mesh(new THREE.SphereGeometry(0.13 * s, 20, 14), matPino);
    cabeca.position.y = 0.6 * s;
    agulha.castShadow = cabeca.castShadow = true;
    g.add(agulha, cabeca);
    const y0 = alturaEm(p.x, p.z) + 0.07;
    g.position.set(p.x, y0, p.z);
    g.visible = false;
    scene.add(g);
    return { ...p, g, y0, s };
  });

  // fios vermelhos entre os pinos
  const matFio = new THREE.MeshStandardMaterial({ color: '#D8404B', roughness: 0.6 });
  const TUB = 120, RAD = 6;
  const fios = cues.fios.map((f) => {
    const [a, b] = f.pontos;
    const meio = new THREE.Vector3((a[0] + b[0]) / 2, ALT + 0.75, (a[1] + b[1]) / 2);
    const curva = new THREE.QuadraticBezierCurve3(new THREE.Vector3(a[0], ALT + 0.62, a[1]), meio, new THREE.Vector3(b[0], ALT + 0.62, b[1]));
    const g = new THREE.TubeGeometry(curva, TUB, 0.022, RAD, false);
    const m = new THREE.Mesh(g, matFio);
    m.castShadow = true;
    g.setDrawRange(0, 0);
    scene.add(m);
    return { ...f, g };
  });

  // funis de tornado (argila cinza, giram)
  const perfil = [[0.02, 0], [0.05, 0.25], [0.08, 0.6], [0.14, 1.0], [0.26, 1.35], [0.5, 1.6], [0.62, 1.66]].map(([r, y]) => new THREE.Vector2(r, y));
  const funilGeo = new THREE.LatheGeometry(perfil, 18);
  const matFunil = new THREE.MeshStandardMaterial({ color: '#8E8984', roughness: 0.9, transparent: true, opacity: 0.88 });
  const funis = cues.funis.map((f) => {
    const m = new THREE.Mesh(funilGeo, matFunil);
    m.position.set(f.x, ALT + 0.05, f.z);
    m.castShadow = true; m.visible = false;
    scene.add(m);
    return { ...f, m };
  });

  // setas de massas de ar (tubo revelado + cabeça cônica)
  const setas = cues.setas.map((s) => {
    const curva = new THREE.CatmullRomCurve3(s.pontos.map(([x, z]) => new THREE.Vector3(x, s.y ?? 0.9, z)));
    const g = new THREE.TubeGeometry(curva, TUB, 0.16, 10, false);
    const mat = new THREE.MeshStandardMaterial({ color: s.cor, roughness: 0.7, transparent: true, opacity: 0.95 });
    const m = new THREE.Mesh(g, mat); m.castShadow = true; g.setDrawRange(0, 0);
    const cab = new THREE.Mesh(new THREE.ConeGeometry(0.36, 0.8, 16), mat); cab.castShadow = true; cab.visible = false;
    scene.add(m, cab);
    return { ...s, curva, g, cab, mat };
  });

  // supercélulas: nuvens de argila (esferas agrupadas)
  const matNuvem = new THREE.MeshStandardMaterial({ color: '#F1ECE4', roughness: 0.95 });
  const esfera = new THREE.SphereGeometry(1, 16, 12);
  const nuvens = cues.nuvens.map((n) => {
    const g = new THREE.Group();
    const bolhas = [[0, 0, 0, 0.55], [0.5, 0.05, 0.1, 0.42], [-0.45, 0.0, -0.05, 0.45], [0.15, 0.38, 0, 0.42], [-0.1, 0.1, 0.4, 0.38], [0.2, 0.0, -0.4, 0.36], [0.05, 0.7, 0.05, 0.3]];
    for (const [x, y, z, r] of bolhas) {
      const m = new THREE.Mesh(esfera, matNuvem);
      m.position.set(x, y, z); m.scale.setScalar(r); m.castShadow = true;
      g.add(m);
    }
    g.position.set(n.x, ALT + 1.3, n.z); g.visible = false;
    scene.add(g);
    return { ...n, g };
  });

  const camera = new THREE.PerspectiveCamera(opts.fov ?? 32, cues.largura / cues.altura, 0.1, 200);
  const corSol = new THREE.Color(), corBase = new THREE.Color('#FFE2BE'), corQuente = new THREE.Color('#FF9A62');
  const DIST = opts.dist ?? 1;

  function update(t) {
    const p = hermite(cues.camera, t, 'pos'), a = hermite(cues.camera, t, 'alvo');
    if (opts.offV) { const o = hermite(cues.camera, t, 'offV'); a[0] += o[0]; a[2] += o[1]; p[0] += o[0]; p[2] += o[1]; }
    // formato vertical: afasta a câmera do alvo (mesmo enquadramento central)
    const px = a[0] + (p[0] - a[0]) * DIST, py = a[1] + (p[1] - a[1]) * DIST, pz = a[2] + (p[2] - a[2]) * DIST;
    camera.position.set(px + 0.22 * Math.sin(t * 0.45), py, pz + 0.14 * Math.cos(t * 0.38));
    camera.lookAt(a[0], a[1], a[2]);
    camera.updateMatrixWorld();

    const luz = interpTabela(cues.luz, t), quente = interpTabela(cues.quente, t);
    sol.intensity = 2.0 * luz;
    hemi.intensity = 0.85 * (0.45 + 0.55 * luz);
    sol.color.copy(corSol.copy(corBase).lerp(corQuente, quente));

    destaques.forEach((d) => {
      const u = smooth(d.t, d.t + 0.5, t);
      d.m.visible = u > 0.001;
      d.m.scale.y = Math.max(0.001, u);
      d.mat.emissiveIntensity = 0.35 * Math.max(0, 1 - (t - d.t) / 1.2) + 0.08;
    });
    matCorr.opacity = 0.32 * interpTabela(cues.corredor.op, t);
    if (sat) sat.material.opacity = interpTabela(cues.satelite.op, t);

    pinos.forEach((pi) => {
      pi.g.visible = t >= pi.t;
      pi.g.position.y = pi.y0 + 2.4 * queda((t - pi.t) / 0.6);
    });
    fios.forEach((f) => f.g.setDrawRange(0, Math.floor(smooth(f.t0, f.t1, t) * TUB) * RAD * 6));
    funis.forEach((f) => {
      const s = smooth(f.t0, f.t0 + 0.6, t) * (1 - smooth(f.t1 - 0.6, f.t1, t));
      f.m.visible = s > 0.01;
      f.m.scale.set(s * 0.75, s * (0.85 + 0.15 * Math.sin(t * 3.1)), s * 0.75);
      f.m.rotation.y = t * 5;
      f.m.position.x = f.x + 0.06 * Math.sin(t * 1.7); f.m.position.z = f.z + 0.05 * Math.cos(t * 1.3);
    });
    setas.forEach((s) => {
      const u = smooth(s.t0, s.t1, t), fade = 1 - smooth(s.t2, s.t2 + 0.8, t);
      s.g.setDrawRange(0, Math.floor(u * TUB) * 10 * 6);
      s.mat.opacity = 0.95 * fade;
      s.cab.visible = u > 0.02 && fade > 0.02;
      const pt = s.curva.getPointAt(Math.max(0.001, u)), tg = s.curva.getTangentAt(Math.max(0.001, u));
      s.cab.position.copy(pt).addScaledVector(tg, 0.3);
      s.cab.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), tg);
    });
    nuvens.forEach((n) => {
      const s = smooth(n.t, n.t + 0.7, t) * (1 - smooth(n.t2, n.t2 + 0.8, t));
      n.g.visible = s > 0.01;
      n.g.scale.setScalar(Math.max(0.001, s * n.s * (1 + 0.03 * Math.sin(t * 2 + n.x))));
      n.g.position.y = ALT + 1.1 + 0.25 * s;
    });
  }

  const v = new THREE.Vector3();
  function projetar(w = cues.largura, h = cues.altura) {
    const conv = (x, y, z) => {
      v.set(x, y, z).project(camera);
      return { x: (v.x * 0.5 + 0.5) * w, y: (-v.y * 0.5 + 0.5) * h, ok: v.z < 1 && v.z > -1 };
    };
    return {
      pinos: pinos.map((p) => ({ id: p.id, ...conv(p.x, p.g.position.y + 0.72 * p.s, p.z) })),
      rotulos: cues.rotulos_mapa.map((r) => ({ ...r, ...conv(r.x, r.y ?? ALT + 0.02, r.z) })),
    };
  }

  function configurarRenderer(renderer) {
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFShadowMap;
    renderer.toneMapping = THREE.NoToneMapping;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
  }

  update(0);
  return { scene, camera, update, projetar, configurarRenderer };
}
