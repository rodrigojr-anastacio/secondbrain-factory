import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { Thumbnail } from './Thumbnail.jsx';
const Root = () => (
  <Composition id="Thumbnail" component={Thumbnail} durationInFrames={1} fps={30} width={1280} height={720} defaultProps={{ variante: 'A' }} />
);
registerRoot(Root);
