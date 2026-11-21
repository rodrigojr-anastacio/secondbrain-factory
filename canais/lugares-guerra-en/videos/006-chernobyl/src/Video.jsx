import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import './estilo.jsx';
import { KenBurns, Filme, DocGrifo, Numero, Cartela, EntaoAgora, Dupla, Card } from './componentes.jsx';
import { Arquivo, Contador, Datilo, Teletipo, TresRelogios, Mural, Glitch, MapaCh, Overlay } from './ch.jsx';
import timeline from './timeline.json';

const TIPOS = { KenBurns, Filme, DocGrifo, 'Número': Numero, Mapa2D: MapaCh, Cartela, EntaoAgora, Dupla, Card, Arquivo, Contador, Datilo, Teletipo, TresRelogios, Mural, Glitch };

// 006-chernobyl: cortes secos entre planos (tempos do tools/build.py, ancorados nas palavras do Whisper e nos áudios de época);
// régua de horas + contador persistentes por cima (estado em `rl` de cada plano); render mudo + audio/final/mix.wav.
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
    <Overlay planos={timeline.planos} />
  </AbsoluteFill>
);
