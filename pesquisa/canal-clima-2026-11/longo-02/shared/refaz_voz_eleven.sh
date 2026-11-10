#!/bin/bash
# Troca a voz provisória (Kokoro) pela final (ElevenLabs v3 "Fernanda") e refaz tudo que depende dela.
# Pré-requisito: chave válida em ~/.segredos/elevenlabs/api_key (ver BLOQUEIO.md). ~11 mil caracteres (saldo do plano: ~32 mil).
# Uso: shared/refaz_voz_eleven.sh  (depois: conferir work/confere_voz_eleven.txt e refazer só os blocos ruins com
#      python3 shared/gera_voz_eleven.py bNN, rodando de novo a partir do passo 2)
set -e
cd "$(dirname "$0")/.."
python3 shared/roteiro.py
python3 shared/gera_voz_eleven.py                                            # 1. voz (só os blocos que faltam)
rm -f shared/slot.json                                                       # o slot é medido na 1ª montagem ElevenLabs
VOZ=eleven ~/workspace/fabrica-youtube/tools/.venv/bin/python shared/monta_audio_v2.py   # 2. montagem, Whisper por bloco, slot
python3 shared/build_cues.py                                                 # 3. storyboard re-sincronizado
~/tts/venv-kokoro/bin/python shared/mix_audio.py
python3 shared/gera_srt.py
REBUNDLE=1 bash shared/render.sh plano | tail -1
bash shared/thumbs.sh
echo "Agora: render de todas as partes (shared/render.sh 0..N-1, uma por vez) e shared/render.sh junta"
