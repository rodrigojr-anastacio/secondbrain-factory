#!/bin/bash
# OBSOLETO (16/11/2026): era uma cópia do tools/render_runpod.sh sem a espera por render/still da VPS (usada uma vez no
# historia-ptbr/009) e ainda chamava a REST v1 do Runpod, desligada em 16/11/2026. Agora é só um atalho:
exec env ESPERA_VPS=0 "$(dirname "$0")/render_runpod.sh" "$@"
