import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { Pilot } from './Video.jsx';
import { PilotV2 } from './v2/VideoV2.jsx';
import { PilotV3 } from './v3/VideoV3.jsx';

const Root = () => (
  <>
  <Composition
    id="LotR1MinPilot"
    component={Pilot}
    durationInFrames={1800}
    fps={30}
    width={1920}
    height={1080}
  />
  <Composition
    id="LotR1MinPilotV2"
    component={PilotV2}
    durationInFrames={1800}
    fps={30}
    width={1920}
    height={1080}
  />
  <Composition
    id="LotR1MinPilotV3"
    component={PilotV3}
    durationInFrames={1830}
    fps={30}
    width={1920}
    height={1080}
  />
  </>
);

registerRoot(Root);
