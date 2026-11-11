// Vários stills de uma composição Remotion com UM navegador só (muito mais rápido que um `npx remotion still` por quadro).
// Usado pelo tools/render_runpod.sh (amostras de referência na VPS e provas no Pod); serve também para a grade do pré-QA.
// Uso: node tools/remotion_stills.cjs <dir remotion> <bundle> <composição> <pasta saída> <gl> <escala> <q1,q2,...>
//   gl: swangle (VPS, CPU) | angle-egl (GPU no Runpod). Saída: <pasta>/<q>.png. Na VPS: ~8 s por still 1080p (3D pesado).
//   Lista "info" no lugar dos quadros: imprime "<fps> <nº de quadros>" da composição.
const path = require('path');
const { createRequire } = require('module');
const [rem, bundle, comp, saida, gl, escala, lista] = process.argv.slice(2);
if (!lista) { console.error('uso: remotion_stills.cjs <dir remotion> <bundle> <composição> <saida> <gl> <escala> <q1,q2,...>'); process.exit(1); }
const r = createRequire(path.resolve(rem, 'package.json'))('@remotion/renderer');
const [bundleAbs, saidaAbs] = [path.resolve(bundle), path.resolve(saida)];
process.chdir(rem); // o Chrome Headless Shell do Remotion fica em <dir remotion>/node_modules/.remotion (sem isso baixa outro no cwd)
(async () => {
  const quadros = lista.split(',').filter(Boolean).map(Number);
  const serveUrl = bundleAbs;
  const chromiumOptions = { gl };
  const browser = await r.openBrowser('chrome', { chromiumOptions });
  const composition = await r.selectComposition({ serveUrl, id: comp, puppeteerInstance: browser, chromiumOptions });
  if (lista === 'info') { console.log(`${composition.fps} ${composition.durationInFrames}`); await browser.close({ silent: true }); return; }
  const t0 = Date.now();
  for (const frame of quadros) {
    await r.renderStill({ composition, serveUrl, frame, output: path.join(saidaAbs, `${frame}.png`), scale: Number(escala),
      puppeteerInstance: browser, chromiumOptions, timeoutInMilliseconds: 240000, overwrite: true, logLevel: 'error' });
  }
  console.log(`${quadros.length} stills em ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  await browser.close({ silent: true });
})().catch((e) => { console.error(e.stack || String(e)); process.exit(1); });
