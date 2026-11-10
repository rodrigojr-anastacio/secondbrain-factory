import { Composition } from 'remotion';
import { Longo } from './Longo';
import { Thumb } from './Thumb';
import { LongoV2 } from './LongoV2';
import cues from '../../shared/cues.json';

const dur = Math.ceil(cues.duracao * cues.fps);
export const Root = () => (
  <>
    <Composition id="Longo" component={Longo} durationInFrames={dur} fps={cues.fps} width={1920} height={1080} />
    {/* visual-v2 (amostras para aprovação; não afeta o Longo) */}
    <Composition id="LongoV2" component={LongoV2} durationInFrames={dur} fps={cues.fps} width={1920} height={1080} defaultProps={{ estilo: 'B', fotos: 'grande' }} />
    {[1, 2, 3].map((v) => <Composition key={v} id={`Thumb${v}`} component={Thumb} durationInFrames={1} fps={30} width={1920} height={1080} defaultProps={{ v }} />)}
  </>
);
