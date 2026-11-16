import { Composition } from 'remotion';
import { Longo } from './Longo';
import { Thumb } from './Thumb';
import { LongoV2 } from './LongoV2';
import cues from '../../shared/cues.json';

const dur = Math.ceil(cues.duracao * cues.fps);
export const Root = () => (
  <>
    <Composition id="Longo" component={Longo} durationInFrames={dur} fps={cues.fps} width={1920} height={1080} />
    {/* visual-v2 fase 2: mistura A/B aprovada (shared/estilo_v2.json) + fotos grandes; o Longo (v1) não muda */}
    <Composition id="LongoV2" component={LongoV2} durationInFrames={dur} fps={cues.fps} width={1920} height={1080} defaultProps={{ estilo: 'AB', fotos: 'grande', perf: { seg: 0.3, segLargo: 0.12 } }} />
    {[1, 2, 3].map((v) => <Composition key={v} id={`Thumb${v}`} component={Thumb} durationInFrames={1} fps={30} width={1920} height={1080} defaultProps={{ v }} />)}
  </>
);
