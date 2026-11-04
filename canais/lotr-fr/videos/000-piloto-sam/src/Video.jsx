import React from 'react';
import {
  AbsoluteFill,
  Audio,
  continueRender,
  delayRender,
  Img,
  OffthreadVideo,
  Sequence,
  Easing,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

const FPS = 30;
const W = 1920;
const H = 1080;

const sceneSpecs = [
  { seconds: 5.3, kind: 'video', asset: 'ship_intro.mp4', tint: 'ship', kicker: 'LE DERNIER PORTEUR', title: 'FRODON PART', line: 'ET SAM RESTE' },
  { seconds: 3.7, kind: 'image', asset: 'hills.jpg', tint: 'green', kicker: 'DES ANNÉES PLUS TARD', title: 'LA COMTÉ', line: 'UNE VIE RECOMMENCE' },
  { seconds: 6.8, kind: 'image', asset: 'book.jpg', tint: 'book', kicker: 'LE LIVRE ROUGE', title: 'CONFIE À ELANOR', line: 'UNE DERNIÈRE TRANSMISSION' },
  { seconds: 6.0, kind: 'map', tint: 'map', kicker: 'LA TRADITION DE LA COMTÉ', title: 'LE DERNIER PORTEUR', line: 'LA ROUTE VERS L’OUEST' },
  { seconds: 7.2, kind: 'video', asset: 'waves.mp4', tint: 'ocean', kicker: 'IL A PORTÉ L’ANNEAU', title: 'MÊME BRIÈVEMENT', line: 'COMME FRODON' },
  { seconds: 9.9, kind: 'video', asset: 'fog.mp4', tint: 'mist', kicker: 'AMAN', title: 'PAS L’IMMORTALITÉ', line: 'PAIX ET GUÉRISON' },
  { seconds: 8.3, kind: 'video', asset: 'ship_outro.mp4', tint: 'ship', kicker: 'APRÈS LA MORT DE ROSIE', title: 'IL PART À SON TOUR', line: 'VERS LES HAVRES GRIS' },
  { seconds: 6.5, kind: 'video', asset: 'waves.mp4', tint: 'ocean', kicker: 'UNE QUESTION RESTE', title: 'A-T-IL REVU FRODON ?', line: 'LE TEXTE NE LE MONTRE PAS' },
  { seconds: 6.3, kind: 'video', asset: 'fog.mp4', tint: 'mist', kicker: 'LE DERNIER VOYAGE', title: 'ET VOUS ?', line: 'ILS SE SONT RETROUVÉS ?' },
];
let cursor = 0;
const SCENES = sceneSpecs.map((scene, index) => {
  const duration = Math.round(scene.seconds * FPS);
  const item = { ...scene, index, from: cursor, duration };
  cursor += duration;
  return item;
});

const captions = [
  [0.00, 4.88, 'Frodon part vers l’Ouest. Sam, lui, rentre dans la Comté.'],
  [5.30, 8.96, 'Il retrouve Rosie, élève leurs enfants et garde le Livre Rouge.'],
  [9.60, 15.80, 'Des années plus tard, après la mort de Rosie, Sam confie le livre à Elanor et rejoint les Havres Gris.'],
  [16.24, 17.18, 'Pourquoi ?'],
  [17.18, 21.30, 'La tradition de la Comté le présente comme le dernier Porteur de l’Anneau à prendre la mer.'],
  [21.78, 24.00, 'Sam aussi a porté l’Anneau, brièvement.'],
  [24.48, 28.92, 'Son départ fait écho à celui de Frodon — mais le récit ne raconte pas leurs retrouvailles.'],
  [28.92, 32.26, 'Et partir vers Aman ne rend pas un Hobbit immortel.'],
  [32.68, 36.26, 'Tolkien précise que les mortels autorisés à y séjourner'],
  [36.58, 38.04, 'n’y restent que pour un temps limité.'],
  [38.56, 41.92, 'L’Ouest offre la paix et la guérison, pas l’éternité.'],
  [42.52, 45.14, 'Alors, Sam a-t-il revu Frodon ?'],
  [45.14, 47.28, 'Le livre laisse la question ouverte.'],
  [47.86, 51.68, 'Il nous montre seulement Sam qui prend, à son tour, la route de l’Ouest.'],
].map(([start, end, text]) => ({ start: start * FPS, end: end * FPS, text }));

const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };

function MapArt({ progress }) {
  const dash = 780 * (1 - progress);
  return (
    <AbsoluteFill style={{ background: 'linear-gradient(125deg, #c8b58a 0%, #8b7958 48%, #25343a 100%)' }}>
      <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ position: 'absolute', inset: 0 }}>
        <defs>
          <pattern id="grain" width="42" height="42" patternUnits="userSpaceOnUse">
            <path d="M0 10h42M0 30h42" stroke="rgba(40,30,20,.10)" strokeWidth="1" />
            <circle cx="9" cy="7" r="1.5" fill="rgba(30,20,10,.15)" />
            <circle cx="31" cy="22" r="1" fill="rgba(255,255,255,.16)" />
          </pattern>
          <linearGradient id="routeGold" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0" stopColor="#fff1bc" />
            <stop offset="1" stopColor="#d59d42" />
          </linearGradient>
          <filter id="glow"><feGaussianBlur stdDeviation="8" result="blur" /><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        </defs>
        <rect width={W} height={H} fill="url(#grain)" />
        <path d="M0 815 C240 700 310 840 520 740 S850 690 1000 780 S1320 870 1470 730 S1750 720 1920 650" fill="none" stroke="rgba(248,231,190,.20)" strokeWidth="5" />
        <path d="M180 250 C330 160 440 310 590 230 S900 175 1020 270 S1320 230 1450 315 S1700 280 1820 205" fill="none" stroke="rgba(20,33,34,.22)" strokeWidth="3" />
        <path d="M410 300 C600 390 660 515 840 520 S1030 420 1160 460 S1350 600 1570 575" fill="none" stroke="rgba(20,33,34,.20)" strokeWidth="4" />
        <path d="M315 625 C490 500 640 580 755 540 C900 490 925 410 1080 430 C1250 450 1280 555 1455 500 C1550 470 1625 365 1730 345" fill="none" stroke="rgba(35,28,20,.28)" strokeWidth="5" strokeDasharray="14 15" />
        <path d="M315 625 C490 500 640 580 755 540 C900 490 925 410 1080 430 C1250 450 1280 555 1455 500 C1550 470 1625 365 1730 345" fill="none" stroke="url(#routeGold)" strokeWidth="9" strokeLinecap="round" strokeDasharray="1000" strokeDashoffset={1000 * (1 - progress)} pathLength="1000" filter="url(#glow)" />
        <circle cx="315" cy="625" r="19" fill="#f6dda1" filter="url(#glow)" />
        <circle cx="1730" cy="345" r="19" fill="#f6dda1" filter="url(#glow)" />
        <text x="230" y="710" fill="#f7edcf" fontSize="42" fontFamily="PilotSans, sans-serif" letterSpacing="4">LA COMTÉ</text>
        <text x="1460" y="310" fill="#f7edcf" fontSize="42" fontFamily="PilotSans, sans-serif" letterSpacing="3">HAVRES GRIS</text>
        <text x="1570" y="760" fill="rgba(255,240,200,.78)" fontSize="27" fontFamily="PilotSans, sans-serif" letterSpacing="9">VERS L’OUEST</text>
        <text x="500" y="900" fill="rgba(25,30,30,.55)" fontSize="26" fontFamily="PilotSans, sans-serif" letterSpacing="5">CARTE SCHÉMATIQUE — NON À L’ÉCHELLE</text>
      </svg>
      <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(5,11,13,.18), rgba(5,11,13,.04) 55%, rgba(5,11,13,.45))' }} />
    </AbsoluteFill>
  );
}

function RingGraphic() {
  const frame = useCurrentFrame();
  const rotation = interpolate(frame, [0, 216], [-18, 342], clamp);
  const scale = interpolate(frame, [0, 10, 35, 216], [0.62, 1.08, 1, 0.94], clamp);
  return (
    <div style={{ position: 'absolute', right: 170, top: 265, width: 300, height: 300, transform: `rotate(${rotation}deg) scale(${scale})`, filter: 'drop-shadow(0 0 28px rgba(221,171,82,.62))' }}>
      <svg viewBox="0 0 300 300" width="100%" height="100%">
        <defs><linearGradient id="ringGold" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stopColor="#fff3c6"/><stop offset=".48" stopColor="#c58b35"/><stop offset="1" stopColor="#f7d991"/></linearGradient></defs>
        <ellipse cx="150" cy="150" rx="98" ry="118" fill="none" stroke="url(#ringGold)" strokeWidth="21" />
        <ellipse cx="150" cy="150" rx="70" ry="91" fill="none" stroke="rgba(255,245,215,.44)" strokeWidth="3" />
      </svg>
    </div>
  );
}

function Background({ scene }) {
  const frame = useCurrentFrame();
  const zoom = interpolate(frame, [0, scene.duration], [1.015, scene.kind === 'image' ? 1.13 : 1.07], clamp);
  const drift = interpolate(frame, [0, scene.duration], [-12, 12], clamp);
  const filter = scene.tint === 'ship' ? 'grayscale(1) contrast(1.13) brightness(.77)' : scene.tint === 'book' ? 'sepia(.22) saturate(.9) contrast(1.08)' : scene.tint === 'green' ? 'saturate(.78) contrast(1.08)' : scene.tint === 'mist' ? 'saturate(.72) contrast(1.03)' : 'saturate(.82) contrast(1.06)';
  const style = { width: '100%', height: '100%', objectFit: 'cover', transform: `scale(${zoom}) translateX(${drift}px)`, filter };
  if (scene.kind === 'map') return <MapArt progress={interpolate(frame, [0, scene.duration], [0, 1], clamp)} />;
  if (scene.kind === 'video') return <OffthreadVideo src={staticFile(`assets/${scene.asset}`)} muted volume={0} style={style} />;
  return <Img src={staticFile(`assets/${scene.asset}`)} style={style} />;
}

function SceneText({ scene }) {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const entrance = spring({ frame, fps, config: { damping: 18, stiffness: 155, mass: 0.75 } });
  const exit = interpolate(frame, [scene.duration - 9, scene.duration - 1], [1, 0.7], clamp);
  const y = interpolate(entrance, [0, 1], [46, 0]);
  const titleSize = scene.title.length > 20 ? 82 : scene.title.length > 15 ? 92 : 108;
  return (
    <div style={{ position: 'absolute', left: 128, top: scene.index === 0 ? 215 : 178, maxWidth: 1430, opacity: entrance * exit, transform: `translateY(${y}px)` }}>
      <div style={{ display: 'inline-flex', alignItems: 'center', gap: 18, color: '#f4cf82', fontFamily: 'PilotSans, sans-serif', fontWeight: 700, fontSize: 26, letterSpacing: 7, textTransform: 'uppercase' }}>
        <span style={{ width: 54, height: 3, background: '#d9ad5c', display: 'inline-block' }} />{scene.kicker}
      </div>
      <div style={{ marginTop: 24, color: '#fffaf0', fontFamily: 'PilotSans, sans-serif', fontSize: titleSize, fontWeight: 900, letterSpacing: -3, lineHeight: 0.98, textTransform: 'uppercase', textShadow: '0 8px 30px rgba(0,0,0,.52)', maxWidth: 1400 }}>
        {scene.title}
      </div>
      <div style={{ marginTop: 22, color: 'rgba(255,250,240,.92)', fontFamily: 'PilotSans, sans-serif', fontSize: 34, fontWeight: 600, letterSpacing: 2, textTransform: 'uppercase', textShadow: '0 4px 16px rgba(0,0,0,.65)' }}>
        {scene.line}
      </div>
    </div>
  );
}

function CaptionTrack() {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const caption = captions.find((c) => frame >= c.start && frame <= c.end);
  if (!caption) return null;
  const entrance = spring({ frame: frame - caption.start, fps, config: { damping: 22, stiffness: 180, mass: 0.6 } });
  const opacity = Math.min(1, entrance * interpolate(frame, [caption.end - 5, caption.end], [1, 0], clamp));
  return (
    <div style={{ position: 'absolute', left: 210, right: 210, bottom: 78, display: 'flex', justifyContent: 'center', opacity, transform: `translateY(${interpolate(entrance, [0, 1], [18, 0])}px)` }}>
      <div style={{ maxWidth: 1500, padding: '18px 28px', borderRadius: 12, background: 'rgba(2,8,12,.72)', borderLeft: '4px solid #d9ad5c', color: '#fff', fontFamily: 'PilotSans, sans-serif', fontSize: 35, fontWeight: 500, lineHeight: 1.22, textAlign: 'center', textShadow: '0 2px 7px rgba(0,0,0,.8)' }}>
        {caption.text}
      </div>
    </div>
  );
}

function ProgressBar() {
  const frame = useCurrentFrame();
  const progress = frame / (60 * FPS);
  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 6, background: 'rgba(255,255,255,.14)', zIndex: 20 }}>
      <div style={{ width: `${progress * 100}%`, height: '100%', background: 'linear-gradient(90deg,#c68f3c,#f3d28f)', boxShadow: '0 0 18px rgba(224,177,89,.55)' }} />
    </div>
  );
}

export const Pilot = () => {
  const frame = useCurrentFrame();
  const seconds = frame / FPS;
  const [fontHandle] = React.useState(() => delayRender('Loading bundled font'));
  React.useEffect(() => {
    const fontFaces = [
      new FontFace('PilotSans', `url(${staticFile('assets/DejaVuSans.ttf')})`, { weight: '400' }),
      new FontFace('PilotSans', `url(${staticFile('assets/DejaVuSans-Bold.ttf')})`, { weight: '700' }),
    ];
    Promise.all(fontFaces.map((font) => font.load()))
      .then((loaded) => { loaded.forEach((font) => document.fonts.add(font)); return document.fonts.ready; })
      .then(() => continueRender(fontHandle))
      .catch(() => continueRender(fontHandle));
  }, [fontHandle]);
  return (
    <AbsoluteFill style={{ backgroundColor: '#071115', color: '#fff' }}>
      <style>{`
        @font-face { font-family: 'PilotSans'; src: url("${staticFile('assets/DejaVuSans.ttf')}") format('truetype'); font-weight: 400; font-style: normal; }
        @font-face { font-family: 'PilotSans'; src: url("${staticFile('assets/DejaVuSans-Bold.ttf')}") format('truetype'); font-weight: 700; font-style: normal; }
      `}</style>
      {SCENES.map((scene) => (
        <Sequence key={scene.index} from={scene.from} durationInFrames={scene.duration} layout="none">
          <AbsoluteFill>
            <Background scene={scene} />
            <AbsoluteFill style={{ background: 'linear-gradient(90deg, rgba(3,9,12,.70) 0%, rgba(3,9,12,.36) 56%, rgba(3,9,12,.10) 100%), linear-gradient(0deg, rgba(1,5,8,.72) 0%, rgba(1,5,8,.02) 48%, rgba(1,5,8,.23) 100%)' }} />
            {scene.index === 4 && <RingGraphic />}
            <SceneText scene={scene} />
            <div style={{ position: 'absolute', right: 92, top: 70, fontFamily: 'PilotSans, sans-serif', fontSize: 23, color: 'rgba(255,250,240,.76)', letterSpacing: 4, fontWeight: 700 }}>
              {String(scene.index + 1).padStart(2, '0')} <span style={{ color: '#d9ad5c' }}>/</span> 09
            </div>
          </AbsoluteFill>
        </Sequence>
      ))}
      <Audio src={staticFile('assets/narration.wav')} volume={1} />
      <Audio src={staticFile('assets/ambient.wav')} volume={0.34} />
      <CaptionTrack />
      <ProgressBar />
      {seconds > 53.7 && (
        <div style={{ position: 'absolute', left: 0, right: 0, bottom: 22, textAlign: 'center', fontFamily: 'PilotSans, sans-serif', fontSize: 20, color: 'rgba(255,255,255,.66)', letterSpacing: 3, zIndex: 21 }}>
          UN PILOTE — LE GARDIEN DE VALINOR
        </div>
      )}
    </AbsoluteFill>
  );
};

export const getPilotDurationInFrames = () => SCENES.reduce((sum, scene) => sum + scene.duration, 0);
export const getPilotTimeline = () => SCENES.map(({index, from, duration, seconds, title, asset}) => ({index, from, duration, seconds, title, asset}));
