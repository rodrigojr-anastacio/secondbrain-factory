import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import './estilo.jsx';
import { KenBurns, Filme, DocGrifo, Numero, Mapa2D, Cartela, EntaoAgora, Card } from './componentes.jsx';
import timeline from './timeline.json';

const TIPOS = { KenBurns, Filme, DocGrifo, 'Número': Numero, Mapa2D, Cartela, EntaoAgora, Card };

// 001-midway: cortes secos entre planos (tempos do tools/build.py, ancorados nas palavras do Whisper); render mudo + audio/final/mix.wav.
export const Video = () => (
  <AbsoluteFill style={{ background: '#111418' }}>
    {timeline.planos.map((p) => {
      const Comp = TIPOS[p.tipo];
      return (
        <Sequence key={p.id} from={p.from_} durationInFrames={p.dur} name={`${p.id} ${p.tipo}`}>
          <Comp p={p} />
        </Sequence>
      );
    })}
  </AbsoluteFill>
);
