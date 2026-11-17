import { Composition } from 'remotion';
import { Longo6 } from './Longo6';
import { Thumb } from './Thumb';
import cues from '../../shared/cues.json';

const dur = Math.ceil(cues.duracao * cues.fps);
export const Root = () => (
  <>
    <Composition id="Longo6" component={Longo6} durationInFrames={dur} fps={cues.fps} width={1920} height={1080} />
    {['A', 'B', 'C'].map((v) => <Composition key={v} id={`Thumb${v}`} component={Thumb} durationInFrames={1} fps={30} width={1920} height={1080} defaultProps={{ v }} />)}
  </>
);
