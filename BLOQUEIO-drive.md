# BLOQUEIO: entrega no Drive (rclone precisa de autorização do Rodrigo)

**Por quê:** o conector Google Drive do Claude só aceita conteúdo inline (`textContent` ou `base64Content` escrito pelo próprio modelo). Texto pequeno funcionou (pacote.md subiu). Vídeo de 350 MB e PNGs de 2 MB não cabem: o base64 passaria pelo contexto do modelo (centenas de milhares de tokens por arquivo). Por isso o caminho para binários é o **rclone** (já instalado em `~/.local/bin/rclone`, v1.75), que falta autorizar.

**O que o Rodrigo faz (uma vez, ~2 min), sem colar token no chat:**
1. No Mac: `brew install rclone` (ou baixe em rclone.org).
2. No Mac: `rclone authorize "drive" --drive-scope drive` → abre o navegador, login na conta Google dele. O terminal imprime um bloco `{"access_token":...}`.
3. Na VPS (SSH): `rclone config` → `n` (new remote) → nome **gdrive** → storage **drive** → client_id/secret em branco → scope **1 (drive)** → "Use auto config?" **n** → "Configure as Shared Drive?" **n** → cole o bloco do passo 2 no prompt `config_token>` (digitado no terminal da VPS, não no chat).
4. Teste: `rclone lsd gdrive:Youtube`.
5. Depois: `tools/entregar_drive.sh dossie-es 001-cia` e `tools/entregar_drive.sh dossie-es identidade`.

O token fica em `~/.config/rclone/rclone.conf` (fora do git).
