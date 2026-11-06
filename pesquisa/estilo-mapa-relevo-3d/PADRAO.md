# Padrão de edição "mapa em relevo 3D com câmera contínua" (referência para o PRÓXIMO CANAL)

**Decisão do Rodrigo (06/11/2026):** o próximo canal novo vai usar esta pegada: **dinâmico, câmera sempre em movimento, nada de vídeo estático só com imagem** (ao contrário do historia-ptbr e do dossie-es, que são slideshow de ilustrações com Ken Burns). Este arquivo **não** é regra do historia-ptbr nem do dossie-es: é a semente da bíblia visual do canal novo (copiar para `canais/<slug>/biblia/visual.md` quando ele nascer, via skill `novo-canal`).

Referência: Instagram @relevo.ia (Willian Cardoso), post `DfWr-P8yEi7` (tornados em Chapecó/Xanxerê, 04/11/2026), 1:48, 1080×1920 vertical, 30 fps, ~213 mil curtidas. Vídeo em `ref/video.mp4` (fora do git); quadros em `quadros/` (`sheet.jpg` 1 fps do vídeo inteiro; `fast.jpg` 23–29 s a 4 fps; `anim.jpg` 7–10 s a 6 fps; `full.jpg` 5 quadros em alta). Análise feita em 06/11/2026 pelo orquestrador (frames + detecção de cena do ffmpeg).

## Mundo visual
- **Mapa em relevo 3D tipo maquete de papel:** estados/municípios extrudados, bordas recortadas, sombra projetada real, luz de fim de tarde. Textura de papel bege; linhas de divisa finas.
- **Objetos 3D estilizados** de textura argila/fosca (tornados, nuvens, casinhas em miniatura como "cidades"); no impacto, as casas voam como blocos.
- **Paleta curta:** bege papel, vermelho-coral (~#E8505B, destaque e áreas afetadas), azul-marinho (etiquetas), preto/cinza. Dessaturado, cara de documentário. Rosa claro = região em alerta.
- **Luz narrativa:** a iluminação muda com o texto ("e à noite…" → mapa escurece, aparecem rachaduras).

## Motion (o diferencial)
- **Câmera nunca para:** dolly/orbit lento e contínuo o vídeo todo. **Sem corte seco**: transição = movimento de câmera (do objeto para a vista do estado; zoom-out que revela território; pan para a próxima cidade). A detecção de cena do ffmpeg só acha "cortes" nos trechos de câmera rápida (23–29 s), ou seja, não há cortes de verdade.
- **Algo novo entra a cada 2–3 s:** número, pino, etiqueta, foto, manchete, área acendendo.
- **Contador rolando** (116 → 211 → 247 → 250 MIL) sincronizado com a fala; "+" quando cresce; unidade em versalete menor ("MIL", "km/h").
- **Áreas acendem uma a uma** em vermelho no ritmo da contagem (4 → 9 → 13 → 23 cidades).
- **Pinos caem com bounce leve**, ligados por **fios vermelhos** (quadro de investigação); etiquetas navy aparecem com pop/scale.
- **Fotos reais como polaroid com tachinha** vermelha, girando levemente ao entrar, com legenda ("CHAPECÓ · SC / FOTO: DIVULGAÇÃO/CBMSC").
- **Manchetes como recorte de papel** com veículo e data ("CNN BRASIL · 04/11"), serifa itálica, palavra-chave sublinhada em vermelho.

## Camadas fixas de tipografia
- **Legenda palavra a palavra em máquina de escrever** com cursor vermelho, numa etiqueta de papel branco no terço inferior (mono).
- **Título/número no topo** em vermelho, sans condensada pesada, enorme; abaixo, **faixa navy** com o contexto em mono caixa-alta ("ENTRE UM TORNADO E OUTRO").
- **Aba de capítulo** pequena no canto superior esquerdo (URGENTE → CHAPECÓ → O APAGÃO → AS VÍTIMAS → O PERIGO NÃO PASSOU → O QUE FAZER).
- **Barra de fontes fixa** no rodapé durante todo o vídeo (credibilidade).

## Ritmo e estrutura
- Hook com número no centro no 1º segundo: "Dois tornados em 18 minutos." + "Isso ainda não acabou."
- ~6 capítulos em 1:48; zero corte, o movimento de câmera segura a atenção.
- Fecho útil e compartilhável: quadro de cortiça com post-its "O QUE FAZER" + CTA "MANDA PRA QUEM MORA NO SUL".

## Como produzir na fábrica (Hipótese, a validar no teste de estilo do canal novo)
- Remotion + `@remotion/three` (three.js/react-three-fiber): mapa por GeoJSON (IBGE/Natural Earth) extrudado, câmera animada por keyframes ligados aos tempos da narração (o `build.py` já tem os tempos reais por bloco). Objetos 3D low-poly simples (primitivas/GLB grátis) em vez de imagens geradas.
- Camadas 2D (legenda máquina de escrever, contador, etiquetas, polaroid, manchete, barra de fontes) em React por cima do canvas 3D.
- **Custo de CPU:** render 3D na VPS de 2 vCPU será bem mais lento que o slideshow; medir no teste (renderizar em partes, um por vez; considerar GPU/render na nuvem se inviável). Imagem paga quase zero (só fotos reais/manchetes, com crédito).
- Fase 1 obrigatória: amostra de ~20 s para o Rodrigo aprovar antes de produzir (regra 7 do orquestrador).
