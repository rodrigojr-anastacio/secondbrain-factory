import { Composition } from 'remotion';
import { Thumb } from './Thumb';
import { LongoV3 } from './LongoV3';
import cues from '../../shared/cues.json';

const dur = Math.ceil(cues.duracao * cues.fps);
export const Root = () => (
  <>
    {/* visual-v2 fase 2: mistura A/B aprovada (shared/estilo_v2.json) + fotos grandes; o Longo (v1) não muda */}
    <Composition id="LongoV3" component={LongoV3} durationInFrames={dur} fps={cues.fps} width={1920} height={1080} defaultProps={{ estilo: 'AB', fotos: 'grande', perf: { seg: 0.3, segLargo: 0.12 } }} />
    {["A", "B", "C"].map((v) => <Composition key={v} id={`Thumb${v}`} component={Thumb} durationInFrames={1} fps={30} width={1920} height={1080} defaultProps={{ v }} />)}
  </>
);
