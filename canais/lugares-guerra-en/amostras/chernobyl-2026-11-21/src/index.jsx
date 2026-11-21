import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { Amostra } from './Amostra.jsx';
import timeline from './timeline.json';

const Root = () => (
  <Composition id="Amostra" component={Amostra} durationInFrames={timeline.durationInFrames} fps={timeline.fps} width={1920} height={1080} />
);
registerRoot(Root);
