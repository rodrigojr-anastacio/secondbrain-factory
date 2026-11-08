// Mundo 3D "maquete de papel" do longo 01 (clima pt, 08/11/2026). Base: piloto-pt/shared/cena3d.js.
// Novidades: mapa até a Amazônia e os Andes (crista em papel), câmera com cortes secos, névoa e sombra que seguem o alvo,
// várias folhas de satélite (e uma sequência animada), regiões translúcidas, rastros, ciclone, anel de radar,
// supercélula didática (vento em 2 níveis, rolo deitado que fica em pé, torre girando, mesociclone, descida fria, funil)
// e partículas correndo pelas setas. update(t) é puro e determinístico (t em segundos).

function smooth(a, b, x) {
  const t = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
}
export function interpTabela(tab, t) {
  if (!tab || !tab.length) return 0;
  if (t <= tab[0][0]) return tab[0][1];
  for (let i = 1; i < tab.length; i++) {
    if (t <= tab[i][0]) {
      const [t0, v0] = tab[i - 1], [t1, v1] = tab[i];
      return v0 + (v1 - v0) * smooth(0, 1, (t - t0) / Math.max(1e-6, t1 - t0));
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
    return a[campo].map((v, c) => (b[campo][c] - v) / Math.max(1e-6, b.t - a.t));
  };
  const m0 = tang(i), m1 = tang(i + 1);
  const dt = k1.t - k0.t, s = (t - k0.t) / dt;
  const h00 = 2 * s ** 3 - 3 * s ** 2 + 1, h10 = s ** 3 - 2 * s ** 2 + s, h01 = -2 * s ** 3 + 3 * s ** 2, h11 = s ** 3 - s ** 2;
  return k0[campo].map((v, c) => h00 * v + h10 * dt * m0[c] + h01 * k1[campo][c] + h11 * dt * m1[c]);
}
// câmera em segmentos: uma chave com corte=true começa um segmento novo (corte seco, sem interpolar com o anterior)
function segmentos(keys) {
  const segs = [[]];
  keys.forEach((k) => { if (k.corte && segs[segs.length - 1].length) segs.push([]); segs[segs.length - 1].push(k); });
  return segs;
}
function queda(p) {
  if (p <= 0) return 1;
  if (p < 0.55) { const q = p / 0.55; return 1 - q * q; }
  if (p < 0.8) return 0.10 * Math.sin(Math.PI * (p - 0.55) / 0.25);
  if (p < 1) return 0.025 * Math.sin(Math.PI * (p - 0.8) / 0.2);
  return 0;
}
const ALT = 0.32, ALT_BR = 0.10, ALT_PAIS = 0.05;

export function criarMundo(THREE, cues, geo, tex = {}, opts = {}) {
  const scene = new THREE.Scene();
  const fundo = new THREE.Color('#B9A47F'), fundoNoite = new THREE.Color('#2E3446');
  scene.background = fundo.clone();
  scene.fog = new THREE.Fog(fundo.clone(), 30, 70);

  const forma = (anel) => new THREE.Shape(anel.map(([x, z]) => new THREE.Vector2(x, -z)));
  const extrudar = (aneis, alt) => {
    const g = new THREE.ExtrudeGeometry(aneis.map(forma), { depth: alt, bevelEnabled: false, curveSegments: 1 });
    g.rotateX(-Math.PI / 2);
    return g;
  };

  const mesa = new THREE.Mesh(new THREE.PlaneGeometry(600, 600), new THREE.MeshStandardMaterial({ color: '#A88F69', roughness: 1 }));
  mesa.rotation.x = -Math.PI / 2; mesa.position.y = -0.002; mesa.receiveShadow = true;
  scene.add(mesa);

  // vizinhos (outras UFs e países); a Amazônia Legal ganha tom verde-papel quando "amazonia" > 0
  const matBR = [new THREE.MeshStandardMaterial({ color: '#DCCDB0', roughness: 1 }), new THREE.MeshStandardMaterial({ color: '#BFAA86', roughness: 1 })];
  const matAmaz = [new THREE.MeshStandardMaterial({ color: '#DCCDB0', roughness: 1 }), new THREE.MeshStandardMaterial({ color: '#BFAA86', roughness: 1 })];
  const matPais = [new THREE.MeshStandardMaterial({ color: '#CDBC9C', roughness: 1 }), new THREE.MeshStandardMaterial({ color: '#B19C79', roughness: 1 })];
  for (const v of geo.vizinhos) {
    const m = new THREE.Mesh(extrudar([v.anel], v.br ? ALT_BR : ALT_PAIS), v.amaz ? matAmaz : v.br ? matBR : matPais);
    m.receiveShadow = true; m.castShadow = true;
    scene.add(m);
  }
  const corPapelBR = new THREE.Color('#DCCDB0'), corVerde = new THREE.Color('#9DB07A');

  const tons = { PR: '#EEE2CB', SC: '#E9DCC2', RS: '#EBDFC6' };
  for (const [uf, aneis] of Object.entries(geo.estados)) {
    const mats = [new THREE.MeshStandardMaterial({ color: tons[uf], roughness: 0.95 }), new THREE.MeshStandardMaterial({ color: '#C9B48F', roughness: 1 })];
    const m = new THREE.Mesh(extrudar(aneis, ALT), mats);
    m.castShadow = true; m.receiveShadow = true;
    scene.add(m);
  }
  const segs = [];
  for (const anel of geo.mun) for (let i = 1; i < anel.length; i++) segs.push(anel[i - 1][0], ALT + 0.003, anel[i - 1][1], anel[i][0], ALT + 0.003, anel[i][1]);
  const gl = new THREE.BufferGeometry();
  gl.setAttribute('position', new THREE.Float32BufferAttribute(segs, 3));
  scene.add(new THREE.LineSegments(gl, new THREE.LineBasicMaterial({ color: '#9C8662', transparent: true, opacity: 0.6 })));
  const segE = [];
  for (const aneis of Object.values(geo.estados)) for (const anel of aneis) for (let i = 1; i < anel.length; i++) segE.push(anel[i - 1][0], ALT + 0.004, anel[i - 1][1], anel[i][0], ALT + 0.004, anel[i][1]);
  const ge = new THREE.BufferGeometry();
  ge.setAttribute('position', new THREE.Float32BufferAttribute(segE, 3));
  scene.add(new THREE.LineSegments(ge, new THREE.LineBasicMaterial({ color: '#6E5D45', transparent: true, opacity: 0.7 })));

  // crista dos Andes (papel dobrado): perfil triangular ao longo da linha, com picos determinísticos
  const pts = [];
  for (let i = 0; i < geo.andes.length - 1; i++) {
    const [x0, z0, h0] = geo.andes[i], [x1, z1, h1] = geo.andes[i + 1];
    for (let k = 0; k < 8; k++) {
      const u = k / 8, ruido = 0.75 + 0.35 * Math.abs(Math.sin((i * 8 + k) * 2.3)) ;
      pts.push([x0 + (x1 - x0) * u, z0 + (z1 - z0) * u, (h0 + (h1 - h0) * u) * ruido]);
    }
  }
  pts.push(geo.andes[geo.andes.length - 1]);
  const vtx = [], idx = [];
  pts.forEach(([x, z, h], i) => {
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
    let dx = b[0] - a[0], dz = b[1] - a[1]; const L = Math.hypot(dx, dz) || 1; dx /= L; dz /= L;
    const w = 0.9 + 0.5 * h;
    vtx.push(x - dz * w, ALT_PAIS, z + dx * w, x, ALT_PAIS + 1.25 * h, z, x + dz * w, ALT_PAIS, z - dx * w);
    if (i > 0) { const o = (i - 1) * 3, p = i * 3; idx.push(o, p, o + 1, p, p + 1, o + 1, o + 1, p + 1, o + 2, p + 1, p + 2, o + 2); }
  });
  const gAndes = new THREE.BufferGeometry();
  gAndes.setAttribute('position', new THREE.Float32BufferAttribute(vtx, 3)); gAndes.setIndex(idx); gAndes.computeVertexNormals();
  const matAndes = new THREE.MeshStandardMaterial({ color: '#D7C6A3', roughness: 1, flatShading: true, side: THREE.DoubleSide, emissive: '#E8505B', emissiveIntensity: 0 });
  const andes = new THREE.Mesh(gAndes, matAndes); andes.castShadow = true; andes.receiveShadow = true;
  scene.add(andes);

  // municípios: placas coral que sobem e acendem (somem em t2)
  const destaques = cues.destaques.map((d) => {
    const mat = new THREE.MeshStandardMaterial({ color: d.cor || '#E8505B', roughness: 0.6, emissive: d.cor || '#E8505B', emissiveIntensity: 0, transparent: true });
    const m = new THREE.Mesh(extrudar(geo.destaque[d.nome], 0.07), mat);
    m.position.y = ALT; m.castShadow = true; m.visible = false;
    scene.add(m);
    return { ...d, m, mat };
  });

  // regiões translúcidas (corredor, risco, área de chuva): anel + tabela de opacidade
  const regioes = cues.regioes.map((r) => {
    const mat = new THREE.MeshBasicMaterial({ color: r.cor, transparent: true, opacity: 0, depthWrite: false });
    const m = new THREE.Mesh(extrudar([r.anel], 0.01), mat);
    m.position.y = (r.y ?? ALT + 0.09); m.renderOrder = 2;
    scene.add(m);
    return { ...r, m, mat };
  });

  // rastros: faixa coral que se desenha de a para b
  const rastros = cues.rastros.map((r) => {
    const [a, b] = r.pontos, L = Math.hypot(b[0] - a[0], b[1] - a[1]);
    const mat = new THREE.MeshStandardMaterial({ color: '#B8323D', roughness: 0.7, transparent: true, opacity: 0.95 });
    const g = new THREE.BoxGeometry(1, 0.03, r.largura); g.translate(0.5, 0, 0);
    const m = new THREE.Mesh(g, mat);
    m.position.set(a[0], ALT + 0.02, a[1]); m.rotation.y = -Math.atan2(b[1] - a[1], b[0] - a[0]);
    m.visible = false; scene.add(m);
    return { ...r, m, mat, L };
  });

  // folhas de satélite georreferenciadas (cada uma com sua textura; "seq" troca de textura no tempo)
  const folha = (caixa, y) => {
    const g = new THREE.PlaneGeometry(caixa[2] - caixa[0], caixa[3] - caixa[1]); g.rotateX(-Math.PI / 2);
    const mat = new THREE.MeshBasicMaterial({ transparent: true, opacity: 0, depthWrite: false });
    const m = new THREE.Mesh(g, mat); m.position.set((caixa[0] + caixa[2]) / 2, y, (caixa[1] + caixa[3]) / 2); m.renderOrder = 3;
    m.visible = false; scene.add(m);
    return { m, mat };
  };
  const sats = cues.sats.map((s) => {
    const f = folha(s.caixa, s.y ?? ALT + 0.6);
    const lista = (s.imgs || [s.img]).map((k) => { const t = tex[k]; if (t) t.colorSpace = THREE.SRGBColorSpace; return t; });
    f.mat.map = lista[0] || null;
    return { ...s, ...f, lista };
  });

  // luzes (a sombra segue o alvo da câmera)
  const hemi = new THREE.HemisphereLight('#F4EEE4', '#6E5C49', 0.85);
  scene.add(hemi);
  const sol = new THREE.DirectionalLight('#FFE2BE', 2.0);
  sol.castShadow = true;
  sol.shadow.mapSize.set(opts.sombra ?? 1024, opts.sombra ?? 1024);
  sol.shadow.bias = -0.0008; sol.shadow.normalBias = 0.03;
  scene.add(sol); scene.add(sol.target);

  // pinos
  const matAgulha = new THREE.MeshStandardMaterial({ color: '#3A3634', roughness: 0.5, metalness: 0.3 });
  const matsPino = {};
  const pinos = cues.pinos.map((p) => {
    const cor = p.cor || '#E8505B';
    matsPino[cor] = matsPino[cor] || new THREE.MeshStandardMaterial({ color: cor, roughness: 0.45 });
    const g = new THREE.Group();
    const s = (p.pequeno ? 0.65 : 1) * (p.escala || 1);
    const agulha = new THREE.Mesh(new THREE.CylinderGeometry(0.014 * s, 0.014 * s, 0.55 * s, 8), matAgulha);
    agulha.position.y = 0.275 * s;
    const cabeca = new THREE.Mesh(new THREE.SphereGeometry(0.13 * s, 20, 14), matsPino[cor]);
    cabeca.position.y = 0.6 * s;
    agulha.castShadow = cabeca.castShadow = true;
    g.add(agulha, cabeca);
    const y0 = (p.y0 ?? ALT) + 0.07;
    g.position.set(p.x, y0, p.z); g.visible = false;
    scene.add(g);
    return { ...p, g, y0, s };
  });

  const matFio = new THREE.MeshStandardMaterial({ color: '#D8404B', roughness: 0.6 });
  const TUB = 120, RAD = 6;
  const fios = cues.fios.map((f) => {
    const [a, b] = f.pontos;
    const L = Math.hypot(b[0] - a[0], b[1] - a[1]);
    const meio = new THREE.Vector3((a[0] + b[0]) / 2, ALT + 0.62 + 0.15 + 0.08 * L, (a[1] + b[1]) / 2);
    const curva = new THREE.QuadraticBezierCurve3(new THREE.Vector3(a[0], ALT + 0.62, a[1]), meio, new THREE.Vector3(b[0], ALT + 0.62, b[1]));
    const g = new THREE.TubeGeometry(curva, TUB, 0.022 * (f.grosso || 1), RAD, false);
    const m = new THREE.Mesh(g, matFio); m.castShadow = true; g.setDrawRange(0, 0);
    scene.add(m);
    return { ...f, g, m };
  });

  const perfil = [[0.02, 0], [0.05, 0.25], [0.08, 0.6], [0.14, 1.0], [0.26, 1.35], [0.5, 1.6], [0.62, 1.66]].map(([r, y]) => new THREE.Vector2(r, y));
  const funilGeo = new THREE.LatheGeometry(perfil, 18);
  const matFunil = new THREE.MeshStandardMaterial({ color: '#8E8984', roughness: 0.9, transparent: true, opacity: 0.88 });
  const funis = cues.funis.map((f) => {
    const m = new THREE.Mesh(funilGeo, matFunil);
    m.position.set(f.x, ALT + 0.05, f.z); m.castShadow = true; m.visible = false;
    scene.add(m);
    return { ...f, m };
  });

  // setas (tubo revelado + cabeça cônica); fluxo = bolinhas correndo pela curva
  const matBolinha = new THREE.MeshBasicMaterial({ color: '#FFF3E0', transparent: true, opacity: 0.9 });
  const bolinhaGeo = new THREE.SphereGeometry(0.11, 10, 8);
  const setas = cues.setas.map((s) => {
    const curva = new THREE.CatmullRomCurve3(s.pontos.map(([x, z, y]) => new THREE.Vector3(x, y ?? s.y ?? 0.9, z)));
    const r = s.r ?? 0.16;
    const g = new THREE.TubeGeometry(curva, TUB, r, 10, false);
    const mat = new THREE.MeshStandardMaterial({ color: s.cor, roughness: 0.7, transparent: true, opacity: 0.95, emissive: s.cor, emissiveIntensity: 0.05 });
    const m = new THREE.Mesh(g, mat); m.castShadow = true; g.setDrawRange(0, 0);
    const cab = new THREE.Mesh(new THREE.ConeGeometry(r * 2.25, r * 5, 16), mat); cab.castShadow = true; cab.visible = false;
    scene.add(m, cab);
    const bolinhas = [];
    if (s.fluxo) for (let i = 0; i < 14; i++) { const b = new THREE.Mesh(bolinhaGeo, matBolinha); b.scale.setScalar(r / 0.16); b.visible = false; scene.add(b); bolinhas.push(b); }
    return { ...s, curva, g, m, cab, mat, bolinhas };
  });

  const matNuvem = new THREE.MeshStandardMaterial({ color: '#F1ECE4', roughness: 0.95 });
  const esfera = new THREE.SphereGeometry(1, 16, 12);
  const BOLHAS = [[0, 0, 0, 0.55], [0.5, 0.05, 0.1, 0.42], [-0.45, 0.0, -0.05, 0.45], [0.15, 0.38, 0, 0.42], [-0.1, 0.1, 0.4, 0.38], [0.2, 0.0, -0.4, 0.36], [0.05, 0.7, 0.05, 0.3]];
  const nuvens = cues.nuvens.map((n) => {
    const g = new THREE.Group();
    for (const [x, y, z, r] of BOLHAS) {
      const m = new THREE.Mesh(esfera, matNuvem);
      m.position.set(x, y, z); m.scale.setScalar(r); m.castShadow = true;
      g.add(m);
    }
    g.position.set(n.x, ALT + 1.3, n.z); g.visible = false;
    scene.add(g);
    return { ...n, g };
  });

  // ciclone: espiral de bolhas girando no mar
  const ciclones = cues.ciclones.map((c) => {
    const g = new THREE.Group();
    for (let i = 0; i < 40; i++) {
      const a = i * 0.5, r = 0.15 + i * 0.07;
      const m = new THREE.Mesh(esfera, matNuvem);
      m.position.set(Math.cos(a) * r, 0, Math.sin(a) * r); m.scale.setScalar(0.18 + 0.006 * i); m.castShadow = true;
      g.add(m);
    }
    g.position.set(c.x, ALT_PAIS + 0.9, c.z); g.visible = false; scene.add(g);
    return { ...c, g };
  });

  // anel de radar (rotação dentro da tempestade): arco de toro girando
  const matAnel = new THREE.MeshStandardMaterial({ color: '#E8505B', emissive: '#E8505B', emissiveIntensity: 0.4, transparent: true, opacity: 0.9 });
  const aneis = cues.aneis.map((a) => {
    const g = new THREE.Group();
    for (let k = 0; k < 2; k++) {
      const arco = new THREE.Mesh(new THREE.TorusGeometry(a.r, 0.045, 8, 48, Math.PI * 1.3), matAnel);
      arco.rotation.x = -Math.PI / 2; arco.rotation.z = k * Math.PI; g.add(arco);
      const ponta = new THREE.Mesh(new THREE.ConeGeometry(0.11, 0.3, 12), matAnel);
      const ang = Math.PI * 1.3 + k * Math.PI;
      ponta.position.set(Math.cos(ang) * a.r, 0, -Math.sin(ang) * a.r); ponta.rotation.set(0, ang, Math.PI / 2 * 0 ); ponta.rotation.z = -Math.PI / 2; ponta.rotation.y = ang;
      g.add(ponta);
    }
    g.position.set(a.x, ALT + 0.9, a.z); g.visible = false; scene.add(g);
    return { ...a, g };
  });

  // supercélula didática
  let sc = null;
  if (cues.supercelula) {
    const S = cues.supercelula, k = S.escala;
    const g = new THREE.Group(); g.position.set(S.x, ALT, S.z); g.scale.setScalar(k); scene.add(g);
    const matTorre = new THREE.MeshStandardMaterial({ color: '#ECE6DC', roughness: 0.95, transparent: true, opacity: 1 });
    const torre = new THREE.Group();
    const camadas = [[0.5, 0.75], [0.8, 0.7], [1.15, 0.66], [1.5, 0.6], [1.85, 0.56], [2.2, 0.5]];
    camadas.forEach(([y, r], i) => {
      for (let j = 0; j < 6; j++) {
        const a = j / 6 * Math.PI * 2 + i;
        const m = new THREE.Mesh(esfera, matTorre); m.position.set(Math.cos(a) * r * 0.55, y, Math.sin(a) * r * 0.55); m.scale.setScalar(r * 0.62); m.castShadow = true; torre.add(m);
      }
    });
    const bigorna = new THREE.Mesh(new THREE.CylinderGeometry(1.9, 1.2, 0.35, 28), matTorre); bigorna.position.set(0.5, 2.6, 0); bigorna.castShadow = true; torre.add(bigorna);
    const base = new THREE.Mesh(new THREE.CylinderGeometry(1.25, 1.35, 0.25, 28), new THREE.MeshStandardMaterial({ color: '#8C8A88', roughness: 1 }));
    base.position.y = 0.42; torre.add(base);
    torre.position.y = 0.9; g.add(torre);
    // ventos: baixo (laranja, de norte), alto (azul, de oeste, mais forte)
    const seta = (cor, pontos, r) => {
      const curva = new THREE.CatmullRomCurve3(pontos.map((p) => new THREE.Vector3(...p)));
      const gg = new THREE.TubeGeometry(curva, 60, r, 8, false); gg.setDrawRange(0, 0);
      const mat = new THREE.MeshStandardMaterial({ color: cor, roughness: 0.6, transparent: true, opacity: 0.95 });
      const m = new THREE.Mesh(gg, mat); const cab = new THREE.Mesh(new THREE.ConeGeometry(r * 2.4, r * 5, 12), mat); cab.visible = false;
      g.add(m, cab); return { curva, gg, mat, cab };
    };
    const vBaixo = seta('#E07A3A', [[1.2, 0.2, -2.6], [1.0, 0.22, -1.2], [0.9, 0.22, 0.2], [0.8, 0.22, 1.6]], 0.07);
    const vAlto = seta('#4C7FB8', [[-3.2, 3.0, 0.6], [-1.6, 3.05, 0.5], [0.0, 3.1, 0.45], [1.7, 3.1, 0.4], [3.2, 3.1, 0.35]], 0.11);
    const vDesce = seta('#4C7FB8', [[-1.7, 2.9, 1.4], [-1.4, 1.8, 1.2], [-1.0, 0.8, 0.95], [-0.4, 0.3, 0.9], [0.3, 0.25, 1.1]], 0.08);
    const vSobe = seta('#E07A3A', [[0.2, 0.2, 0.0], [0.15, 1.2, 0.0], [0.1, 2.2, 0.0], [0.1, 3.2, 0.0]], 0.09);
    // rolo: cilindro listrado que gira no próprio eixo e depois fica em pé
    const canvas = typeof document !== 'undefined' ? document.createElement('canvas') : null;
    let texRolo = null;
    if (canvas) {
      canvas.width = 256; canvas.height = 64; const c = canvas.getContext('2d');
      for (let i = 0; i < 8; i++) { c.fillStyle = i % 2 ? '#E9DFCF' : '#C0574E'; c.fillRect(i * 32, 0, 32, 64); }
      texRolo = new THREE.CanvasTexture(canvas); texRolo.colorSpace = THREE.SRGBColorSpace;
    }
    const rolo = new THREE.Mesh(new THREE.CylinderGeometry(0.28, 0.28, 2.4, 24, 1, false), new THREE.MeshStandardMaterial({ map: texRolo, roughness: 0.8, transparent: true }));
    rolo.castShadow = true; const roloG = new THREE.Group(); roloG.add(rolo); roloG.position.set(0.3, 1.6, 0); g.add(roloG);
    // mesociclone: anel girando ao redor da torre
    const meso = new THREE.Group();
    for (let j = 0; j < 3; j++) {
      const t = new THREE.Mesh(new THREE.TorusGeometry(0.95 + 0.12 * j, 0.035, 8, 60, Math.PI * 1.5), matAnel); t.rotation.x = -Math.PI / 2; t.rotation.z = j * 2.1; t.position.y = 1.8 + 0.35 * j; meso.add(t);
    }
    g.add(meso);
    const funil = new THREE.Mesh(funilGeo, matFunil); funil.rotation.x = Math.PI; funil.position.set(0.15, 1.32, 0.2); g.add(funil);
    sc = { S, g, torre, matTorre, vBaixo, vAlto, vDesce, vSobe, rolo, roloG, meso, funil };
  }

  const camera = new THREE.PerspectiveCamera(opts.fov ?? 32, cues.largura / cues.altura, 0.1, 400);
  const corSol = new THREE.Color(), corBase = new THREE.Color('#FFE2BE'), corQuente = new THREE.Color('#FF9A62'), corNoite = new THREE.Color('#8FA6D8');
  const camSegs = segmentos(cues.camera);
  const tmp = new THREE.Color();

  const revela = (gg, cab, curva, u, raioSeg, fade, mat) => {
    gg.setDrawRange(0, Math.floor(u * (gg.parameters?.tubularSegments ?? TUB)) * raioSeg * 6);
    mat.opacity = 0.95 * fade;
    cab.visible = u > 0.02 && fade > 0.02;
    const pt = curva.getPointAt(Math.max(0.001, u)), tg = curva.getTangentAt(Math.max(0.001, u));
    cab.position.copy(pt).addScaledVector(tg, 0.15); cab.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), tg);
  };

  function update(t) {
    let seg = camSegs[0];
    for (const s of camSegs) if (s[0].t <= t) seg = s;
    const p = hermite(seg, t, 'pos'), a = hermite(seg, t, 'alvo');
    const tremor = interpTabela(cues.tremor, t);
    camera.position.set(p[0] + 0.22 * Math.sin(t * 0.45) + tremor * 0.08 * Math.sin(t * 61), p[1] + tremor * 0.06 * Math.sin(t * 47), p[2] + 0.14 * Math.cos(t * 0.38));
    camera.lookAt(a[0], a[1], a[2]);
    camera.updateMatrixWorld();
    const dist = Math.hypot(p[0] - a[0], p[1] - a[1], p[2] - a[2]);
    scene.fog.near = dist * 1.35; scene.fog.far = dist * 3.2;
    const sh = Math.max(9, dist * 0.75);
    const scam = sol.shadow.camera; scam.left = -sh; scam.right = sh; scam.top = sh; scam.bottom = -sh; scam.near = 1; scam.far = sh * 5; scam.updateProjectionMatrix();
    sol.target.position.set(a[0], 0, a[2]); sol.position.set(a[0] - sh * 1.0, sh * 0.8, a[2] + sh * 0.45);

    const luz = interpTabela(cues.luz, t), quente = interpTabela(cues.quente, t), noite = interpTabela(cues.noite, t);
    sol.intensity = 2.0 * luz * (1 - 0.55 * noite);
    hemi.intensity = 0.85 * (0.45 + 0.55 * luz) * (1 - 0.35 * noite);
    sol.color.copy(corSol.copy(corBase).lerp(corQuente, quente).lerp(corNoite, noite));
    tmp.copy(fundo).lerp(fundoNoite, noite * 0.8); scene.background.copy(tmp); scene.fog.color.copy(tmp);
    const amaz = interpTabela(cues.amazonia, t);
    matAmaz[0].color.copy(corPapelBR).lerp(corVerde, amaz);
    const and = interpTabela(cues.andes, t);
    matAndes.emissiveIntensity = 0.35 * and; andes.scale.y = 1 + 0.35 * and;

    destaques.forEach((d) => {
      const u = smooth(d.t, d.t + 0.5, t) * (d.t2 ? 1 - smooth(d.t2, d.t2 + 0.6, t) : 1);
      d.m.visible = u > 0.001;
      d.m.scale.y = Math.max(0.001, u);
      d.mat.opacity = Math.min(1, u * 1.5);
      d.mat.emissiveIntensity = 0.35 * Math.max(0, 1 - (t - d.t) / 1.2) + 0.08;
    });
    regioes.forEach((r) => { const o = interpTabela(r.op, t); r.mat.opacity = (r.max ?? 0.32) * o * (r.pulsa ? 0.8 + 0.2 * Math.sin(t * 3) : 1); r.m.visible = o > 0.005; });
    rastros.forEach((r) => {
      const u = smooth(r.t0, r.t1, t), fade = r.t2 ? 1 - smooth(r.t2, r.t2 + 0.6, t) : 1;
      r.m.visible = u > 0.001 && fade > 0.01; r.m.scale.x = Math.max(0.001, u * r.L); r.mat.opacity = 0.95 * fade;
    });
    sats.forEach((s) => {
      const o = interpTabela(s.op, t); s.m.visible = o > 0.005; s.mat.opacity = o;
      if (s.lista.length > 1 && s.m.visible) {
        const i = Math.min(s.lista.length - 1, Math.max(0, Math.floor((t - s.seq[0]) / (s.seq[1] - s.seq[0]) * s.lista.length)));
        if (s.lista[i] && s.mat.map !== s.lista[i]) { s.mat.map = s.lista[i]; s.mat.needsUpdate = true; }
      }
    });
    pinos.forEach((pi) => {
      pi.g.visible = t >= pi.t && !(pi.t2 && t > pi.t2 + 0.4);
      const sai = pi.t2 ? smooth(pi.t2, pi.t2 + 0.4, t) : 0;
      pi.g.position.y = pi.y0 + 2.4 * queda((t - pi.t) / 0.6) + 1.5 * sai;
      pi.g.scale.setScalar(Math.max(0.001, 1 - sai));
    });
    fios.forEach((f) => {
      const fade = f.t2 ? 1 - smooth(f.t2, f.t2 + 0.4, t) : 1;
      f.m.visible = fade > 0.01;
      f.g.setDrawRange(0, Math.floor(smooth(f.t0, f.t1, t) * TUB) * RAD * 6);
    });
    funis.forEach((f) => {
      const s = smooth(f.t0, f.t0 + 0.6, t) * (1 - smooth(f.t1 - 0.6, f.t1, t)) * (f.s || 1);
      f.m.visible = s > 0.01;
      f.m.scale.set(s * 0.75, s * (0.85 + 0.15 * Math.sin(t * 3.1)), s * 0.75);
      f.m.rotation.y = t * 5;
      f.m.position.x = f.x + 0.06 * Math.sin(t * 1.7); f.m.position.z = f.z + 0.05 * Math.cos(t * 1.3);
    });
    setas.forEach((s) => {
      const u = smooth(s.t0, s.t1, t), fade = 1 - smooth(s.t2, s.t2 + 0.8, t);
      const vis = u > 0.001 && fade > 0.01;
      s.m.visible = vis;
      revela(s.g, s.cab, s.curva, u, 10, fade, s.mat);
      const esc = interpTabela(s.engrossa, t) || 0;
      s.m.scale.set(1, 1, 1); if (esc) { s.mat.emissiveIntensity = 0.05 + 0.4 * esc; }
      s.bolinhas.forEach((b, i) => {
        const q = ((t * (s.vel ?? 0.18) + i / s.bolinhas.length) % 1);
        b.visible = vis && u > 0.98 && q < u;
        if (b.visible) b.position.copy(s.curva.getPointAt(q)).add(new THREE.Vector3(0, (s.r ?? 0.16) * 1.1, 0));
      });
    });
    nuvens.forEach((n) => {
      const s = smooth(n.t, n.t + 0.7, t) * (1 - smooth(n.t2, n.t2 + 0.8, t));
      n.g.visible = s > 0.01;
      n.g.scale.setScalar(Math.max(0.001, s * n.s * (1 + 0.03 * Math.sin(t * 2 + n.x))));
      n.g.position.y = (n.y ?? ALT + 1.1) + 0.25 * s;
    });
    ciclones.forEach((c) => {
      const s = smooth(c.t0, c.t0 + 0.8, t) * (1 - smooth(c.t1, c.t1 + 0.8, t));
      c.g.visible = s > 0.01; c.g.scale.setScalar(Math.max(0.001, s * c.s)); c.g.rotation.y = t * 0.9;
    });
    aneis.forEach((a) => {
      const s = smooth(a.t0, a.t0 + 0.5, t) * (1 - smooth(a.t1, a.t1 + 0.5, t));
      a.g.visible = s > 0.01; a.g.scale.setScalar(Math.max(0.001, s)); a.g.rotation.y = t * 3.2;
    });
    if (sc) {
      const S = sc.S;
      const vis = t >= S.t0 - 0.1 && t <= S.t_fim + 0.8;
      sc.g.visible = vis;
      if (vis) {
        const entra = smooth(S.t0, S.t0 + 0.8, t) * (1 - smooth(S.t_fim, S.t_fim + 0.8, t));
        sc.g.scale.setScalar(Math.max(0.001, S.escala * entra));
        const cresce = smooth(S.t_ergue, S.t_ergue + 1.5, t);
        sc.torre.scale.set(0.6 + 0.4 * cresce, 0.35 + 0.65 * cresce, 0.6 + 0.4 * cresce);
        sc.torre.rotation.y = smooth(S.t_gira, S.t_gira + 1, t) * (t - S.t_gira) * 0.9;
        sc.matTorre.opacity = 1 - 0.55 * smooth(S.t_rolo - 0.3, S.t_rolo + 0.3, t) * (1 - smooth(S.t_meso + 1.5, S.t_meso + 2.5, t));
        const fv = 1 - smooth(S.t_descida + 2.2, S.t_descida + 3, t);
        revela(sc.vBaixo.gg, sc.vBaixo.cab, sc.vBaixo.curva, smooth(S.t_baixo, S.t_baixo + 1.0, t), 8, fv, sc.vBaixo.mat);
        revela(sc.vAlto.gg, sc.vAlto.cab, sc.vAlto.curva, smooth(S.t_alto, S.t_alto + 1.0, t), 8, fv, sc.vAlto.mat);
        revela(sc.vSobe.gg, sc.vSobe.cab, sc.vSobe.curva, smooth(S.t_sobe, S.t_sobe + 0.9, t), 8, 1 - smooth(S.t_gira + 2, S.t_gira + 2.8, t), sc.vSobe.mat);
        revela(sc.vDesce.gg, sc.vDesce.cab, sc.vDesce.curva, smooth(S.t_descida, S.t_descida + 1.0, t), 8, 1 - smooth(S.t_fim - 0.6, S.t_fim, t), sc.vDesce.mat);
        const ro = smooth(S.t_rolo, S.t_rolo + 0.6, t) * (1 - smooth(S.t_gira + 0.8, S.t_gira + 1.6, t));
        sc.roloG.visible = ro > 0.01; sc.roloG.scale.setScalar(Math.max(0.001, ro));
        const em = smooth(S.t_ergue, S.t_ergue + 1.4, t);
        sc.roloG.rotation.set(0, 0, Math.PI / 2 * (1 - em)); // deitado (eixo x) -> em pé (eixo y)
        sc.rolo.rotation.y = t * 4;
        const ms = smooth(S.t_meso, S.t_meso + 0.7, t) * (1 - smooth(S.t_fim - 0.6, S.t_fim, t));
        sc.meso.visible = ms > 0.01; sc.meso.scale.setScalar(Math.max(0.001, ms)); sc.meso.rotation.y = t * 2.6;
        const fu = smooth(S.t_funil, S.t_funil + 1.6, t);
        sc.funil.visible = fu > 0.01; sc.funil.scale.set(0.55, 0.78 * Math.max(0.001, fu), 0.55); sc.funil.position.y = 1.32; sc.funil.rotation.y = t * 6;
      }
    }
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
