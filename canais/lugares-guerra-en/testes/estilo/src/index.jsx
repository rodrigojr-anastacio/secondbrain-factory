import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { Thumbnail } from './Thumbnail.jsx';
import { DocGrifo, EntaoAgora, MapaKenBurns } from './Frames.jsx';

// Teste de estilo do canal lugares-guerra-en (12/11/2026). Fase 1: só amostras (3 thumbs + 3 frames de 8 s).
const Root = () => (
  <>
    <Composition id="Thumbnail" component={Thumbnail} durationInFrames={1} fps={30} width={1280} height={720} defaultProps={{ variante: 'A' }} />
    <Composition id="DocGrifo" component={DocGrifo} durationInFrames={240} fps={30} width={1920} height={1080} />
    <Composition id="EntaoAgora" component={EntaoAgora} durationInFrames={240} fps={30} width={1920} height={1080} />
    <Composition id="MapaKenBurns" component={MapaKenBurns} durationInFrames={240} fps={30} width={1920} height={1080} />
  </>
);
registerRoot(Root);
