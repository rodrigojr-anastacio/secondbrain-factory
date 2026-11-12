import { loadFont as anton } from '@remotion/google-fonts/Anton';
import { loadFont as plexMono } from '@remotion/google-fonts/IBMPlexMono';
import { loadFont as barlow } from '@remotion/google-fonts/BarlowCondensed';

// Identidade do canal (biblia/visual.md e biblia/thumb.md). Cores medidas nas thumbs do Where They Stood (ANATOMIA.md §4),
// mas a assinatura de vídeo é nossa: legenda "ficha de arquivo" em mono + grifo amarelo no documento.
export const DISPLAY = anton().fontFamily;          // números grandes e texto da thumb
export const MONO = plexMono().fontFamily;          // fichas de fonte/data/lugar ("o carimbo do arquivo")
export const COND = barlow().fontFamily;            // rótulos de mapa e então × agora
export const AMARELO = '#FDD505';
export const CIANO = '#2BCEE2';
export const FERRUGEM = '#C8561E';
export const TINTA = '#111418';
export const PAPEL = '#EDE6D6';
export const GRIFO = 'rgba(255, 225, 77, 0.55)';
