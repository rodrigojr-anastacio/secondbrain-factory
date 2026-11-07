import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { Brasil } from './Video.jsx';
import { Thumbnail } from './Thumbnail.jsx';
import timeline from './timeline.json';

const Root = () => (
  <>
    <Composition id="Brasil" component={Brasil} durationInFrames={timeline.frames} fps={30} width={1920} height={1080} />
    <Composition id="Thumbnail" component={Thumbnail} durationInFrames={1} fps={30} width={1280} height={720} />
  </>
);
registerRoot(Root);
