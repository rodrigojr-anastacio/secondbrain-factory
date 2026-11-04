import React from 'react';
import { AbsoluteFill, Easing, Img, Sequence, interpolate, staticFile, useCurrentFrame } from 'remotion';
import { Audio } from '@remotion/media';
import { loadFont as loadCinzel } from '@remotion/google-fonts/Cinzel';
import { loadFont as loadCormorant } from '@remotion/google-fonts/CormorantGaramond';
import timeline from './timeline.json';
import { MapLayer } from './MapLayer.jsx';

const cinzel = loadCinzel('normal', { weights: ['400', '700'], subsets: ['latin', 'latin-ext'] });
const cormorant = loadCormorant('normal', { weights: ['600', '700'], subsets: ['latin', 'latin-ext'] });
loadCormorant('italic', { weights: ['500', '600'], subsets: ['latin', 'latin-ext'] });
const TITLE = `${cinzel.fontFamily}, serif`;
const BODY = `${cormorant.fontFamily}, serif`;
const FONTS = { title: TITLE, body: BODY };

const GOLD = '#d9a94a';
const CREAM = '#f6ecd6';
const DARK = '#15100a';
const XF = 10; // crossfade frames
const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' };
const EASE = Easing.bezier(0.16, 1, 0.3, 1);
const SOFT = Easing.bezier(0.45, 0, 0.55, 1);
const NO_HUD = ['card', 'recap', 'end'];

const shadow = '0 2px 6px rgba(0,0,0,.85), 0 0 22px rgba(0,0,0,.55)';

// ---------------------------------------------------------------- image shot (Ken Burns)
const ImgShot = ({ shot }) => {
  const f = useCurrentFrame();
  const [z0, z1, x0, y0, x1, y1] = shot.kb;
  const t = interpolate(f, [0, shot.dur + XF], [0, 1], { ...clamp, easing: SOFT });
  const z = z0 + (z1 - z0) * t, fx = x0 + (x1 - x0) * t, fy = y0 + (y1 - y0) * t;
  const filt = `sepia(0.12) saturate(0.95) contrast(1.04)${shot.grade === 'dim' ? ' brightness(0.72)' : ''}`;
  if (shot.contain) {
    return (
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, #2a2016 0%, #120d08 75%)' }}>
        <AbsoluteFill style={{ transform: `scale(${0.9 + (z - 1) * 0.5})`, transformOrigin: `${fx * 100}% ${fy * 100}%`, padding: '60px 0 150px' }}>
          <Img src={staticFile(`img/${shot.img}.jpg`)} style={{ width: '100%', height: '100%', objectFit: 'contain', filter: filt }} />
        </AbsoluteFill>
      </AbsoluteFill>
    );
  }
  return (
    <AbsoluteFill style={{ background: DARK, overflow: 'hidden' }}>
      <Img src={staticFile(`img/${shot.img}.jpg`)}
        style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'cover', objectPosition: `${fx * 100}% ${fy * 100}%`,
          transform: `scale(${z})`, transformOrigin: `${fx * 100}% ${fy * 100}%`, filter: filt }} />
      <AbsoluteFill style={{ background: 'radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,.55) 100%)' }} />
      <AbsoluteFill style={{ background: 'linear-gradient(180deg, rgba(0,0,0,0) 62%, rgba(0,0,0,.55) 100%)' }} />
    </AbsoluteFill>
  );
};

const MapShot = ({ shot }) => (
  <AbsoluteFill style={{ background: '#e6d6b2' }}>
    <Img src={staticFile('img/parchment.jpg')} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }} />
    <MapLayer shot={shot} fonts={FONTS} />
  </AbsoluteFill>
);

const Parchment = ({ children, dark }) => (
  <AbsoluteFill style={{ background: dark ? '#1a130c' : '#e6d6b2' }}>
    {!dark && <Img src={staticFile('img/parchment.jpg')} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }} />}
    {dark && <AbsoluteFill style={{ background: 'radial-gradient(ellipse at center, #3a2b1a 0%, #140e08 80%)' }} />}
    {children}
  </AbsoluteFill>
);

const CardShot = ({ shot }) => {
  const f = useCurrentFrame();
  const a = interpolate(f, [4, 22], [0, 1], { ...clamp, easing: EASE });
  const line = interpolate(f, [8, 40], [0, 1], { ...clamp, easing: EASE });
  return (
    <Parchment dark>
      <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', flexDirection: 'column' }}>
        <div style={{ fontFamily: TITLE, fontSize: 104, color: CREAM, letterSpacing: 10, opacity: a, transform: `translateY(${(1 - a) * 24}px)`, textTransform: 'uppercase' }}>{shot.title}</div>
        <div style={{ width: 520 * line, height: 3, background: GOLD, margin: '26px 0' }} />
        <div style={{ fontFamily: BODY, fontStyle: 'italic', fontSize: 46, color: '#e8d2a0', opacity: a }}>{shot.sub}</div>
      </AbsoluteFill>
    </Parchment>
  );
};

const RecapShot = ({ shot }) => {
  const f = useCurrentFrame();
  const final = shot.final;
  return (
    <Parchment>
      <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'flex-start', paddingTop: final ? 230 : 130, flexDirection: 'column' }}>
        {!final && <div style={{ fontFamily: TITLE, fontSize: 44, letterSpacing: 12, color: '#6b4d1f', marginBottom: 34 }}>LA COURONNE</div>}
        {shot.steps.map((st, i) => {
          const a = interpolate(f, [st.at, st.at + 14], [0, 1], { ...clamp, easing: EASE });
          return (
            <div key={i} style={{ opacity: a, transform: `translateX(${(1 - a) * -40}px)`, display: 'flex', alignItems: 'baseline', gap: 36,
              width: final ? 900 : 1300, justifyContent: final ? 'center' : 'flex-start', borderBottom: '2px solid rgba(80,55,25,.35)', padding: '14px 10px' }}>
              {!final && <div style={{ fontFamily: BODY, fontStyle: 'italic', fontSize: 44, color: '#5b4325', width: 360 }}>{st.a}</div>}
              <div style={{ fontFamily: TITLE, fontSize: final ? 70 : 62, fontWeight: 700, color: st.b === '?' ? '#8e2a1f' : '#2b2219' }}>{final ? st.a : st.b}</div>
            </div>
          );
        })}
      </AbsoluteFill>
    </Parchment>
  );
};

const EndShot = () => {
  const f = useCurrentFrame();
  const a = interpolate(f, [5, 30], [0, 1], { ...clamp, easing: EASE });
  return (
    <Parchment dark>
      <AbsoluteFill style={{ alignItems: 'center', justifyContent: 'center', flexDirection: 'column', opacity: a }}>
        <div style={{ fontFamily: BODY, fontStyle: 'italic', fontSize: 44, color: '#e8d2a0' }}>Quelles étaient les plus grandes villes</div>
        <div style={{ fontFamily: TITLE, fontSize: 84, color: CREAM, letterSpacing: 6, marginTop: 10 }}>DE LA TERRE DU MILIEU ?</div>
        <div style={{ width: 420, height: 3, background: GOLD, margin: '34px 0' }} />
        <div style={{ fontFamily: BODY, fontSize: 30, color: '#cdb98f' }}>Sources et crédits des images dans la description</div>
      </AbsoluteFill>
    </Parchment>
  );
};

// ---------------------------------------------------------------- HUD
const Keyword = ({ shot }) => {
  const f = useCurrentFrame();
  if (!shot.kw) return null;
  // mapa com coroa: LA COURONNE é a única placa
  if (shot.kind === 'map' && shot._hasCrown) return null;
  const [title, sub] = shot.kw;
  const a = interpolate(f, [XF + 2, XF + 18], [0, 1], { ...clamp, easing: EASE });
  const out = interpolate(f, [shot.dur - 8, shot.dur], [1, 0], clamp);
  const op = a * out;
  if (shot.kind === 'map') {
    // opaque cartouche under the scoreboard (map labels are kept out of this corner)
    return (
      <div style={{ position: 'absolute', left: 60, top: shot._hasCrown ? 214 : 56, opacity: op, background: '#1d150d', border: `2px solid ${GOLD}`,
        borderRadius: 6, padding: '14px 26px', boxShadow: '0 6px 18px rgba(0,0,0,.35)', transform: `translateY(${(1 - a) * 12}px)` }}>
        <div style={{ fontFamily: TITLE, fontWeight: 700, fontSize: 40, color: CREAM, letterSpacing: 2 }}>{title}</div>
        {sub && <div style={{ fontFamily: BODY, fontStyle: 'italic', fontSize: 30, color: '#e5c98d' }}>{sub}</div>}
      </div>
    );
  }
  return (
    <div style={{ position: 'absolute', left: 110, bottom: 250, opacity: op, transform: `translateX(${(1 - a) * -30}px)` }}>
      <div style={{ width: 90 * a, height: 3, background: GOLD, marginBottom: 14 }} />
      <div style={{ fontFamily: TITLE, fontWeight: 700, fontSize: 76, color: CREAM, letterSpacing: 3, textShadow: shadow, lineHeight: 1.05 }}>{title}</div>
      {sub && <div style={{ fontFamily: BODY, fontStyle: 'italic', fontWeight: 600, fontSize: 42, color: '#f0d9a4', textShadow: shadow, marginTop: 6 }}>{sub}</div>}
    </div>
  );
};

const Credit = ({ shot }) => {
  const f = useCurrentFrame();
  if (!shot.credit) return null;
  const o = interpolate(f, [shot.dur, shot.dur + 4], [1, 0], clamp);
  return (
    <div style={{ opacity: o, position: 'absolute', right: 34, top: 26, fontFamily: BODY, fontStyle: 'italic', fontSize: 21, fontWeight: 600,
      color: shot.kind === 'map' ? '#4d3b25' : 'rgba(255,246,228,.88)', textShadow: shot.kind === 'map' ? 'none' : '0 1px 4px rgba(0,0,0,.9)' }}>
      {shot.kind === 'map' ? shot.credit : `Art : ${shot.credit}`}
    </div>
  );
};

const Scoreboard = ({ frame, hidden }) => {
  const evs = timeline.crown.filter((c) => c.from <= frame);
  const vis = interpolate(hidden ? 0 : 1, [0, 1], [0, 1]);
  if (!evs.length) return null;
  const cur = evs[evs.length - 1];
  const since = frame - cur.from;
  const a = interpolate(since, [0, 16], [0, 1], { ...clamp, easing: EASE });
  const flash = interpolate(since, [0, 8, 30], [0, 1, 0], clamp);
  return (
    <div style={{ position: 'absolute', left: 60, top: 50, width: 420, opacity: vis, background: '#1d150d', border: `2px solid ${GOLD}`, borderRadius: 6,
      padding: '12px 22px 14px', boxShadow: `0 6px 18px rgba(0,0,0,.4), 0 0 ${30 * flash}px rgba(217,169,74,${0.8 * flash})` }}>
      <div style={{ fontFamily: TITLE, fontSize: 19, letterSpacing: 6, color: GOLD }}>LA COURONNE</div>
      <div style={{ overflow: 'hidden', height: 56 }}>
        <div style={{ transform: `translateY(${(1 - a) * 50}px)`, opacity: a, fontFamily: TITLE, fontWeight: 700, fontSize: 40, color: CREAM, whiteSpace: 'nowrap' }}>{cur.name}</div>
      </div>
      <div style={{ fontFamily: BODY, fontStyle: 'italic', fontSize: 25, color: '#d9c39a' }}>{cur.era} · estimation</div>
    </div>
  );
};

const Captions = ({ frame }) => {
  const c = timeline.captions.find((x) => frame >= x.from && frame < x.to);
  if (!c) return null;
  return (
    <div style={{ position: 'absolute', left: 0, right: 0, bottom: 56, display: 'flex', justifyContent: 'center' }}>
      <div style={{ maxWidth: 1480, background: 'rgba(16,11,6,.84)', borderRadius: 10, padding: '10px 30px 12px', textAlign: 'center',
        fontFamily: BODY, fontWeight: 700, fontSize: 50, lineHeight: 1.18, color: '#fbf3e1' }}>{c.text}</div>
    </div>
  );
};

const KIND = { img: ImgShot, map: MapShot, card: CardShot, recap: RecapShot, end: EndShot };

export const Cidades = () => {
  const frame = useCurrentFrame();
  const shots = timeline.shots;
  const cur = [...shots].reverse().find((s) => s.from <= frame) || shots[0];
  const hasCrown = timeline.crown.some((c) => c.from <= frame);
  const hideHud = NO_HUD.includes(cur.kind);
  return (
    <AbsoluteFill style={{ background: DARK }}>
      {shots.map((s, i) => {
        const C = KIND[s.kind];
        const dur = s.dur + (i < shots.length - 1 ? XF : 0);
        return (
          <Sequence key={i} from={s.from} durationInFrames={dur} premountFor={30}>
            <FadeIn first={i === 0}><C shot={s} /></FadeIn>
          </Sequence>
        );
      })}
      {shots.map((s, i) => (s.kw || s.credit) && (
        <Sequence key={`h${i}`} from={s.from} durationInFrames={s.dur + XF}>
          <HudFade><Keyword shot={{ ...s, _hasCrown: hasCrown }} /><Credit shot={s} /></HudFade>
        </Sequence>
      ))}
      {!hideHud && <Scoreboard frame={frame} />}
      <Captions frame={frame} />
      <Audio src={staticFile('audio/mix.wav')} />
    </AbsoluteFill>
  );
};

const FadeIn = ({ children, first }) => {
  const f = useCurrentFrame();
  const o = first ? interpolate(f, [0, 12], [0, 1], clamp) : interpolate(f, [0, XF], [0, 1], clamp);
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};
const HudFade = ({ children }) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [XF - 2, XF + 4], [0, 1], clamp);
  return <AbsoluteFill style={{ opacity: o }}>{children}</AbsoluteFill>;
};
