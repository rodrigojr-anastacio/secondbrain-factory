import { Composition } from 'remotion';
import { Teste } from './Teste';
import cues from '../../shared/cues.json';

export const Root = () => (
  <Composition id="Teste" component={Teste} durationInFrames={cues.duracao * cues.fps}
    fps={cues.fps} width={cues.largura} height={cues.altura} />
);
