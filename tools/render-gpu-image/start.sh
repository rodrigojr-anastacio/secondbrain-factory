#!/bin/bash
# Entrada do contêiner: põe a chave pública (env PUBLIC_KEY, passada pelo render_runpod.sh) e sobe o sshd.
set -e
mkdir -p /root/.ssh /run/sshd
if [ -n "$PUBLIC_KEY" ]; then echo "$PUBLIC_KEY" > /root/.ssh/authorized_keys; chmod 600 /root/.ssh/authorized_keys; fi
ssh-keygen -A >/dev/null 2>&1
# sessões ssh não herdam o env do contêiner: grava o essencial para os comandos remotos
{ echo "export PATH=/root/node/bin:\$PATH"; env | grep -E '^(NVIDIA_|CUDA_|RUNPOD_POD_ID)' | sed 's/^/export /'; } > /etc/profile.d/render.sh
exec /usr/sbin/sshd -D -e
