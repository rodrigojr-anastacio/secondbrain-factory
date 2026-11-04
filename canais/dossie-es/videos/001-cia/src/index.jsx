import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { Cia } from './Video.jsx';
import { Thumbnail } from './Thumbnail.jsx';
import timeline from './timeline.json';

const Root = () => (
  <>
    <Composition id="Cia" component={Cia} durationInFrames={timeline.frames} fps={30} width={1920} height={1080} />
    <Composition id="Thumbnail" component={Thumbnail} durationInFrames={1} fps={30} width={1280} height={720} defaultProps={{ variante: 'A' }} />
  </>
);
registerRoot(Root);
