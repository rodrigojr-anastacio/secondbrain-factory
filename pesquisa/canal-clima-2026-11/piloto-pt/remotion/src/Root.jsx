import { Composition } from 'remotion';
import { Piloto } from './Piloto';
import cues from '../../shared/cues.json';

const dur = Math.ceil(cues.duracao * cues.fps);
export const Root = () => (
  <>
    <Composition id="Shorts" component={Piloto} durationInFrames={dur} fps={cues.fps} width={1080} height={1920} defaultProps={{ formato: 'v' }} />
    <Composition id="Longo" component={Piloto} durationInFrames={dur} fps={cues.fps} width={1920} height={1080} defaultProps={{ formato: 'h' }} />
    <Composition id="Capa" component={Piloto} durationInFrames={dur} fps={cues.fps} width={1080} height={1920} defaultProps={{ formato: 'v', capa: true }} />
  </>
);
