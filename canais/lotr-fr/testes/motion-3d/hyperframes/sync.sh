#!/bin/bash
# Copia o que é compartilhado/vendorizado para dentro do projeto (o servidor do Hyperframes só serve esta pasta).
set -e
cd "$(dirname "$0")"
mkdir -p vendor shared fonts
cp node_modules/three/build/three.module.js node_modules/three/build/three.core.js vendor/
cp node_modules/gsap/dist/gsap.min.js vendor/
cp ../shared/cena3d.js ../shared/camadas.js ../shared/cues.json shared/
ln -f ../audio/narracao.wav narracao.wav
for f in ../shared/fonts/*.ttf; do ln -f "$f" fonts/; done
