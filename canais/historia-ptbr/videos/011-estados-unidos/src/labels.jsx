// Rótulos dos mapas (011 Estados Unidos): imagens geradas sem texto; letras feitas no código.
// POSIÇÕES PROVISÓRIAS: conferir em still de cada plano (qa/mapas-stills.jpg); manter x entre 0,2 e 0,8 (o pan/zoom corta rótulo na borda).
// chave da imagem → [{ t: texto, x, y: fração da imagem, size: px a 1x }]
export const LABELS = {
  map_13_colonies: [{ t: '13 COLÔNIAS, 1776', x: 0.62, y: 0.42, size: 34 }],
  map_usa_today: [{ t: 'ESTADOS UNIDOS', x: 0.5, y: 0.5, size: 44 }],
  map_louisiana: [{ t: 'LUISIANA, 1803', x: 0.45, y: 0.5, size: 36 }],
  map_1765: [{ t: 'AS 13 COLÔNIAS', x: 0.6, y: 0.45, size: 30 }],
  map_georgia: [{ t: 'NAÇÃO CHEROKEE', x: 0.5, y: 0.5, size: 30 }],
  map_trail: [{ t: 'NAÇÃO CHEROKEE', x: 0.35, y: 0.5, size: 28 }],
  map_split: [
    { t: 'UNIÃO', x: 0.4, y: 0.3, size: 36 },
    { t: 'CONFEDERAÇÃO', x: 0.5, y: 0.7, size: 36 },
  ],
  map_states_1920: [{ t: 'TENNESSEE', x: 0.62, y: 0.55, size: 30 }],
};
