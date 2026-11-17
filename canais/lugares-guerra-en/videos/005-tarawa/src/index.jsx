import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { Video } from './Video.jsx';
import timeline from './timeline.json';

const Root = () => (
  <Composition id="Video" component={Video} durationInFrames={timeline.durationInFrames} fps={timeline.fps} width={1920} height={1080} />
);
registerRoot(Root);
