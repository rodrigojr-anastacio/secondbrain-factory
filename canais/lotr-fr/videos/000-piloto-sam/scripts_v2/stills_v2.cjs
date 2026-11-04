// Render representative V2 stills for review (not the final video).
// Usage: node scripts_v2/stills_v2.cjs 40 150 ...
const path = require('path');
const { bundle } = require('@remotion/bundler');
const { selectComposition, renderStill } = require('@remotion/renderer');

const frames = process.argv.slice(2).map(Number);
(async () => {
  const serveUrl = await bundle({ entryPoint: path.resolve(__dirname, '../src/index.jsx') });
  const composition = await selectComposition({ serveUrl, id: 'LotR1MinPilotV2' });
  console.log('composition', composition.id, composition.width, composition.height, composition.fps, composition.durationInFrames);
  for (const frame of frames) {
    const output = path.resolve(__dirname, `../out/v2-check/frame-${String(frame).padStart(4, '0')}.png`);
    await renderStill({ composition, serveUrl, output, frame });
    console.log('rendered', frame);
  }
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
