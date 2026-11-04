import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { Cidades } from './Video.jsx';
import timeline from './timeline.json';
import { Thumbnail } from './Thumbnail.jsx';

const Root = () => (
  <>
  <Composition id="CidadesFR" component={Cidades} durationInFrames={timeline.frames} fps={30} width={1920} height={1080} />
  <Composition id="Thumbnail" component={Thumbnail} durationInFrames={1} fps={30} width={1920} height={1080} />
  </>
);
registerRoot(Root);
