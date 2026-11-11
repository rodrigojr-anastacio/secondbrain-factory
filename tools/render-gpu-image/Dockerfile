# Imagem de render Remotion em GPU (Runpod), só com DEPENDÊNCIAS: nada de projeto, mídia ou segredo.
# Construída pelo GitHub Actions (.github/workflows/render-gpu-image.yml) → ghcr.io/rodrigojr-anastacio/fabrica-render-gpu
# Usada por tools/render_runpod.sh (IMG=...). Corta o setup do Pod (~4–6 min de apt + npm ci + Chrome) para segundos.
#
# O que tem: Ubuntu 22.04 + libs do Chrome/GL/EGL/Vulkan (as libs NVIDIA vêm do host com NVIDIA_DRIVER_CAPABILITIES=all),
# ffmpeg, fontes, sshd (chave pública pela env PUBLIC_KEY, igual às imagens do Runpod), Node 26.12.1 em /root/node e
# node_modules do Remotion 4.0.541 (+ three/@remotion/three) já com o Chrome Headless Shell em /opt/deps/node_modules.
# Projeto com o mesmo package-lock.json (sha256 em /opt/deps/lock.sha256) usa esse node_modules direto; outro lock roda npm ci.
FROM ubuntu:22.04

ARG NODE_VERSION=26.12.1
ENV DEBIAN_FRONTEND=noninteractive \
    PATH=/root/node/bin:$PATH \
    NVIDIA_DRIVER_CAPABILITIES=all \
    NVIDIA_VISIBLE_DEVICES=all

COPY pacotes.txt /tmp/pacotes.txt
RUN echo 'Acquire::Retries "5";' > /etc/apt/apt.conf.d/80retries \
    && for t in 1 2 3; do apt-get update && apt-get install -y --no-install-recommends $(grep -v '^#' /tmp/pacotes.txt) && break; \
         [ $t = 3 ] && exit 1; sleep 20; done \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /run/sshd /root/.ssh && chmod 700 /root/.ssh \
    && sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin prohibit-password/; s/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

RUN curl -fsSL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz" | tar -xJ -C /root \
    && mv /root/node-v${NODE_VERSION}-linux-x64 /root/node && node --version

WORKDIR /opt/deps
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund --loglevel=error \
    && npx remotion browser ensure \
    && ls node_modules/.remotion \
    && sha256sum package-lock.json | cut -d' ' -f1 > lock.sha256 \
    && npm cache verify >/dev/null

COPY start.sh /start.sh
RUN chmod +x /start.sh
WORKDIR /root
CMD ["/start.sh"]
