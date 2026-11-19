// Rótulos dos mapas (012 Portugal): imagens geradas sem texto; letras feitas no código.
// chave da imagem → [{ t: texto, x, y: fração da imagem, size: px a 1x }]. x entre 0,2 e 0,8 (o pan/zoom corta rótulo na borda).
// escala_pe_pt_es: contornos reais na mesma escala (thumbs/escala.py); PORTUGAL fica abaixo da forma dourada (a faixa é estreita demais para o rótulo).
export const LABELS = {
  escala_pe_pt_es: [
    { t: 'PERNAMBUCO', x: 0.22, y: 0.72, size: 38 },
    { t: 'PORTUGAL', x: 0.42, y: 0.84, size: 38 },
    { t: 'ESPANHA', x: 0.62, y: 0.52, size: 44 },
  ],
};
