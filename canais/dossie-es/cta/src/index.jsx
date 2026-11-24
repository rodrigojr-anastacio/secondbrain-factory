import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { CTA } from './CTA.jsx';
import T from './tempos.json';

const Root = () => (
  <Composition id="CTA" component={CTA} durationInFrames={Math.round(T.dur * T.fps)} fps={T.fps} width={1920} height={1080} defaultProps={{ mudo: false }} />
);
registerRoot(Root);
