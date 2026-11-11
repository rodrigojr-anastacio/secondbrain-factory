# Teste de render Remotion com GPU alugada no Runpod (11/11/2026)

Brief: `~/workspace/referencias/BRIEF-teste-render-gpu.md`. Projeto: Em Relevo 002 v2 (`pesquisa/canal-clima-2026-11/longo-02`, composição `LongoV2`, bundle `work/bundle-v2` de 10/11 19:58). `longo-02/` não foi alterado.

## Resultado em uma linha
**Funciona, e a imagem sai igual à da VPS:** o vídeo inteiro (12:10, 21.896 quadros) renderizou em **286 s (4,8 min) contra ~9,8 h na VPS** (~120× mais rápido). O teste custou **US$ 0,30** no total; um vídeo deve custar **~US$ 0,05–0,08 (~R$ 0,30–0,50)** com ~15 min de Pod. Duas ressalvas: (1) o Chrome tem que ser o **Headless Shell** padrão do Remotion, porque no `chrome-for-testing` o 3D some; (2) **a GPU nem sempre sai igual**. Uma 4090 Secure perdeu a textura satélite sem dar erro, por isso o script tem uma **trava de QA por SSIM** antes e depois do render.

## Máquina
| Item | Valor |
|---|---|
| GPU | RTX 3090 24 GB, Community, **US$ 0,22/h** (driver 580.65, ~27 vCPU no cgroup, 54 GB RAM) |
| Imagem | `runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04` (sshd com `PUBLIC_KEY`) + libs do Chrome via apt + Node 26.12.1 enviado da VPS + `npm ci` |
| Chave do truque | env `NVIDIA_DRIVER_CAPABILITIES=all` na criação do Pod: monta `libEGL_nvidia`/GLES/Vulkan no contêiner. O padrão (`compute,utility`) não traz as libs gráficas |
| Render | `npx remotion render … --gl=angle-egl --concurrency=16` (Headless Shell 158) |

## O WebGL usou a GPU de verdade?
Sim.
- Com `chrome-for-testing`, o `chrome://gpu` mostrou "WebGL: Hardware accelerated" e GPU a 100%. **Mas a imagem saiu errada** (ver abaixo).
- Com o Headless Shell (o que ficou), o `chrome://gpu` não abre. As provas: **9,8 GB de memória de vídeo e 33% de uso** durante o render, CPU a ~10%, e velocidade de 0,013 s/quadro (o SwiftShader nos mesmos 27 vCPU levaria segundos por quadro). O script confere a memória da GPU no meio do render e avisa se estiver parada.
- Abordagens que não serviram: `--gl=egl` e `--gl=angle` (erro "Error creating WebGL context") e `--gl=vulkan` (imagem correta, mas o `chrome://gpu` diz WebGL em software, ou seja, caiu no SwiftShader).

## Tempos
| Etapa | Tempo |
|---|---|
| API cria o Pod → RUNNING com IP | 16 s |
| → SSH pronto | 23 s |
| Envio (bundle 111 MB + Node 35 MB, tar por ssh; a imagem não tem rsync) | 54 s |
| Setup (apt das libs do Chrome + `npm ci` + download do Chrome) | ~6 min (o maior custo fixo) |
| Download do mp4 inteiro (421 MB) | 34 s |

### s/quadro, VPS × GPU
VPS = `work/render-v2-tempos.txt` (última passada de cada bloco, `--gl=swangle --concurrency=2`). GPU = 3090, Headless Shell, `angle-egl`.

| Trecho | Quadros | VPS | GPU conc 8 | GPU conc 16 |
|---|---|---|---|---|
| **Pesado** 9:24–10:24 (enchente 2024 + relevo de calor do Pacífico), quadros 16932–18731 | 1.800 | 4.950 s = **2,75 s/q** (blocos de 2,4–4,1 s/q) | 61 s = 0,034 s/q | **31 s = 0,017 s/q** |
| **Leve** 3:18–3:26 (mapa 2D), 5950–6187 | 238 | 313 s = 1,3 s/q | 8 s (quase tudo é abrir o Chrome) | 8 s |
| **Vídeo inteiro** | 21.896 | 35.252 s = **9,8 h** (1,61 s/q) | — | **286 s = 0,013 s/q** |

Com `chrome-for-testing` (descartado) o trecho pesado levou 201 s (conc 8) e 210 s (conc 16). Com a GPU a 100%, mais concorrência não ajudava.

## A imagem ficou igual?
Sim. SSIM contra stills da VPS feitos do **mesmo bundle** (`remotion still --gl=swangle`):

| Quadro | Cena | SSIM GPU × VPS |
|---|---|---|
| 17000 | foto da enchente sobre o mapa satélite | 0,980 |
| 17500 | enchente / mapa | 0,983 |
| 18100 | relevo de calor 3D + caixa das 4 perguntas + legenda | 0,971 |
| 18600 | relevo de calor + gráfico de barras | 0,977 |
| 6000 / 6150 | leve | 0,988 / 0,987 |

Referência: o mp4 da própria VPS contra o still da VPS dá 0,985–0,991. Logo, a diferença que sobra é compressão (crf 18). A PSNR ficou em ~39–40 dB. Conferi lado a lado: texturas, fontes, legendas, relevo e sombras iguais (`comparacao/q*_vps-x-gpu.jpg`). No vídeo inteiro, 9 quadros espalhados contra o `out/video.mp4` deram SSIM de 0,974 a 0,992.

**Problema encontrado (importante):** com `--chrome-mode=chrome-for-testing` a GPU funciona, mas a malha do relevo de calor (OISST) não aparece. No render com concorrência às vezes some também a textura satélite (`comparacao/q18100_vps-x-gpu-chrome-for-testing-ERRADO.jpg`, SSIM 0,47–0,71). Nenhum erro no log. **Hipótese** (sem confirmar): diferença do Chrome completo no buffer da malha atualizada a cada quadro. Regra: **não usar chrome-for-testing** e fazer pré-QA de stills de toda cena 3D antes de confiar num ambiente novo.

## Custo real
- Saldo Runpod pela API: **US$ 40,00 → 39,6981 = US$ 0,302** no total:
  - Pod 3090 da medição (2.538 s × US$ 0,22/h, quase tudo depuração): US$ 0,152 (`financas.consumo` id 183);
  - 5 Pods curtos para validar o script (A5000 Secure a 0,27, 4090 Secure a 0,89, 3090 Community a 0,22): US$ 0,150 (id 184).
  - As duas linhas têm fornecedor Runpod e `ref_id` 17 (Em Relevo 002).
- Destruição conferida pela API no fim: `pods: []`, `networkVolumes: []`, `currentSpendPerHr: 0`.

## Estimativa por vídeo (12 min, igual ao Em Relevo 002)
| | Tempo de Pod | Custo |
|---|---|---|
| 3090 Community (US$ 0,22/h) | ~13 min (boot 0,5 + envio 1 + setup 6 + render 5 + download 0,6) | **~US$ 0,05** |
| 4090 Community (US$ 0,34/h), se faltar 3090 | ~12 min | ~US$ 0,07 |
| VPS hoje | ~10 h de render, sem dinheiro, mas trava a VPS e qualquer refação custa horas | — |

Refazer um trecho (slot, correção de QA) vira questão de minutos, não de horas.

## Receita reprodutível
> **Atualização 11/11 (tarde):** o script virou `tools/render_runpod.sh` (genérico, com conferência densa e render em blocos; ver "Virou padrão" no fim). A descrição abaixo é a da versão do teste.

`render_runpod.sh <dir remotion> <dir bundle> <composição> <saida.mp4> [a-b] [conc]`. O script liga o Pod (lista de GPUs em ordem, Community e depois Secure), envia por tar via ssh, instala, renderiza mudo com `angle-egl`, confere a GPU, traz o mp4 e **destrói o Pod no trap** (em qualquer saída ou erro). A chave vai num arquivo de header temporário (600), fora do código e do log. O áudio é juntado na VPS como no `render_v2.sh junta` (ffmpeg `-c:v copy` + mix).

Travas do script:
- **Prova antes do render:** os quadros `PROVAS` viram stills na VPS (swangle, antes de ligar o Pod) e no Pod. Se algum der SSIM < 0,95, o script aborta sem renderizar.
- **Conferência do mp4:** os mesmos quadros, tirados do mp4 que voltou, são comparados de novo. Abaixo de 0,95 o script sai com código 3.
- **Concorrência** limitada aos vCPU do Pod (a A5000 Secure tinha só 7; o Remotion recusa concorrência maior).
- **Disponibilidade:** tenta Community e depois Secure, a cada 60 s, `TENTA` vezes.

### Validação do script (11/11, 11:07–11:29)
| Rodada | Resultado |
|---|---|
| 1–3 | "There are no instances currently available" em todas as GPUs da lista, Community e Secure → entrou a repetição a cada 60 s |
| A5000 Secure (US$ 0,27/h) | falhou: concorrência 16 > 7 vCPU → entrou o limite de concorrência |
| **4090 Secure (driver 595)** | render saiu, mas **sem a textura satélite e com faixas** (quadro 17000: SSIM 0,89), sem erro nenhum → entrou a trava de QA |
| 3090 Community | o `apt` falhou calado no setup → entrou a repetição com erro visível |
| **4090 Secure (driver 595), 2ª vez** | **passou de ponta a ponta**: SSH 35 s, envio 146 s, setup 216 s, provas com SSIM 0,998 / 0,998 / 0,999, pico de 16 GB na GPU, 240 quadros pesados em ~25 s. mp4 contra a VPS: SSIM 0,974–0,981. Custo ~US$ 0,07 |

A conferência do mp4 dentro do script entrou depois da última rodada e só foi testada à mão (mesmo comando ffmpeg).

**Lição:** a mesma composição saiu certa numa 4090 e errada em outra 4090 do mesmo tipo, nos dois casos sem erro. **Hipótese:** carga/tempo de textura grande em algumas máquinas. Por isso, render na GPU só com a trava de QA ligada e o QA normal do vídeo depois.

## Recomendação
**Adotar** para render de vídeo inteiro e para refações grandes: ~120× mais rápido, centavos por vídeo, imagem igual. Para virar padrão:
1. Rodar o `render_runpod.sh` uma vez com o **vídeo inteiro**, com `PROVAS` nas cenas 3D, e juntar o áudio na VPS. O script já passou de ponta a ponta num trecho.
2. **Disponibilidade:** o estoque com IP público oscila de um minuto para o outro. O script já insiste (`TENTA`); se faltar com frequência, vale aceitar mais modelos.
3. **Imagem própria** (`runpod-build-template`): cortaria os ~6 min de setup para ~1 min.
4. Encaixar na skill `montagem-render` como opção ("render > 10 min → Runpod"), mantendo o pré-QA de stills na VPS e o QA do mp4 que volta. **Precisa da aprovação do Rodrigo:** é gasto recorrente novo, pequeno.
5. Nunca usar `--chrome-mode=chrome-for-testing` (some o 3D) e nunca desligar a trava de QA: GPUs diferentes podem errar sem dar erro.

---

# Virou padrão da fábrica (11/11/2026, tarde)
Brief: `~/workspace/referencias/BRIEF-render-gpu-padrao.md`. Aprovado pelo Rodrigo: **todo render de vídeo vai para o Runpod** (VPS = stills, thumbs, grades do pré-QA, testes de segundos e fallback).

## Rodada completa (vídeo inteiro do Em Relevo 002 v2, `LongoV2`, bundle `work/bundle-v2`)
Resultados em `validacao/` (fora do git): `video_gpu3.mp4` (instalação na imagem base) e `video_gpu4.mp4` (imagem da fábrica), logs `rodada*.log`, SSIM em `ssim_vs_publicado*.txt`, quadros em `quadros/`.

| Rodada | Máquina | Pod | Custo | Resultado |
|---|---|---|---|---|
| 1 (script da manhã) | 4090 Secure US$ 0,89/h | 772 s | US$ 0,19 | **reprovada no olho:** provas 0,997–0,999 e 5 quadros do mp4 ≥ 0,97, mas **trechos sem a textura satélite** (quadros 1700 e 10100: SSIM 0,57 e 0,66 contra o publicado; faixas diagonais e bloco marrom) |
| 2 (conferência densa, limiar 0,97) | A5000 0,27/h | 669 s | US$ 0,05 | falso positivo: quadro 15 (escuro, início) dá 0,9695 sempre; o próprio vídeo publicado dá 0,972 → limiar caiu para **0,95** |
| 3 (instalação) | 3090 0,50/h | 903 s | US$ 0,13 | 12 blocos, 85 amostras, 0 refeitos, SSIM 480p mín. 0,969 |
| 4 (imagem da fábrica) | RTX PRO 4500 0,50/h | 1008 s | US$ 0,14 | idem, mín. 0,970 |
| teste final (trecho 900 q) | 4090 Secure 0,89/h | 262 s | US$ 0,06 | ok, 901/901 quadros |

Rodadas 3 e 4 saíram com código 3 por um **bug meu** na divisão em blocos (o "rabo" foi fundido no bloco errado e o último bloco veio repetido: 23.696 quadros); a conferência de nº de quadros pegou. Os blocos 0–10 cobrem exatamente o vídeo e passaram na conferência; o mp4 foi cortado em 21.896 quadros (`-c:v copy`) e recebeu o áudio. Bug corrigido e retestado (teste final).

**Comparação com `longo-02/out/video.mp4`** (rodadas 3 e 4, iguais entre si):
- duração 729,87 s, 21.896 quadros, 1920×1080 30 fps, AAC 48 kHz mono; loudness -14,0 LUFS, LRA 2,2;
- **áudio idêntico bit a bit** (md5 do áudio decodificado igual ao publicado);
- SSIM de 17 quadros espalhados (mp4 × mp4, 1080p): **0,957–0,991** (1700: 0,966; 10100: 0,960; o vídeo publicado contra o still da VPS dá 0,967–0,99, então a diferença é compressão).

## Por que a conferência mudou (o que a rodada 1 ensinou)
A prova com stills isolados passa até na máquina que erra: o defeito só aparece no render concorrente (**Hipótese:** memória de vídeo/carga de textura com muitas abas; a 4090 da rodada 1 chegou a 21 GB com concorrência 16, a 3090 da manhã usou 9,8 GB). O `tools/render_runpod.sh` agora:
- renderiza em **blocos de 60 s** (`BLOCO_S`) e confere **um quadro a cada 10 s** (`AMOSTRA_S`) de cada bloco contra stills da VPS, em 480p (calibração: bons 0,97–0,99, quadro escuro 0,9695, defeitos 0,52–0,93; limiar `LIMIAR_MP4` 0,95);
- bloco reprovado é **refeito no mesmo Pod** com metade da concorrência (até 2×); reprovação idêntica nas 2 rodadas = diferença estável (não é a GPU) e para;
- concorrência padrão **8** (era 16): pico de 8–11 GB nas cenas 3D;
- stills de referência com **um navegador só** (`tools/remotion_stills.cjs`, ~7 s/still 1080p na VPS; 79 stills = 8–10 min, antes de ligar o Pod) e cache opcional `REFS=<dir>` para refações;
- custo gravado em `financas.consumo` (custo/h × tempo; saldo antes/depois nas notas), Pod destruído no trap e conferido pela API.

## Imagem pronta (só dependências)
- `tools/render-gpu-image/` (Dockerfile Debian 12 + libs Chrome/GL/EGL/Vulkan + ffmpeg + fontes + sshd + Node 26.12.1 + `node_modules` do Remotion 4.0.541 com o Chrome Headless Shell), construída pelo GitHub Actions (`.github/workflows/render-gpu-image.yml`, `GITHUB_TOKEN`, minutos gratuitos, ~1,5 min) em **`ghcr.io/rodrigojr-anastacio/fabrica-render-gpu:latest`** (1,43 GB). **Já nasceu pública** (pull anônimo dá HTTP 200): nenhum passo do Rodrigo.
- Armadilhas do runner (11/11/2026): o GitHub Actions **não resolve `*.ubuntu.com`** (nem no host; o apt do runner só aponta para packages.microsoft.com), por isso a base é Debian (`deb.debian.org` resolve). O log do Actions exige login; o workflow escreve os erros como anotação (`::error::`), que a API pública mostra. A API pública tem limite de 60 consultas/h.
- Projeto com o mesmo `package-lock.json` da imagem (sha256 em `/opt/deps/lock.sha256`) usa o `node_modules` dela; lock diferente roda `npm ci` (5 s) no Pod.

| Tempo até o Pod ficar pronto | SSH | envio | setup | total |
|---|---|---|---|---|
| Teste da manhã (imagem base, apt + npm + Chrome) | 16–35 s | 54–146 s | 216 s – ~6 min | ~5–8 min |
| Imagem base, script novo (rodada 3) | 27 s | 58 s (Node em xz na hora) | 59 s | **144 s** |
| Imagem base + Node em cache (teste final) | 37 s | 26 s | 63 s | **126 s** |
| **Imagem da fábrica** (rodada 4) | 145 s (pull de 1,43 GB num host frio) | 18 s | 4 s | **167 s** |
| Imagem da fábrica, testes seguintes (áudio, MKV, Masones) | 83 s / 136 s / 28 s | 17–57 s* | 4–9 s | **107 / 156 / 94 s** |

\* o Masones envia 379 MB de `public/` e roda `npm ci` (lock diferente).

**Leitura honesta (4 Pods com a imagem, 3 sem):** a instalação já tinha caído de ~6 min para ~2 min (apt mais enxuto, `npm ci` de 5 s, Node pré-comprimido), e o pull da imagem num host que não a tem custa o mesmo que se ganha. Ficou como **padrão** a imagem da fábrica (o script cai sozinho para a base + instalação se ela não estiver acessível) porque tira apt e npm do caminho do Pod (o apt já falhou calado na manhã); o custo de 1 min a mais ou a menos é ~US$ 0,004. **Hipótese:** em hosts que já baixaram a imagem o pull some; medir nos próximos renders e, se não melhorar, voltar o padrão para a base (`IMG=runpod/pytorch:...`).
- Alternativa avaliada e descartada: network volume com as deps (prende o Pod a um datacenter, o que reduz a oferta de GPU que já oscila; US$ 0,07/GB/mês; e as libs do sistema não ficam no volume).

## Tempo e custo reais por vídeo (12 min, com 3D)
- Pod ~15–17 min no total: ~2–3 min até ficar pronto, ~12 min de render + conferência (12 blocos de ~55–65 s com concorrência 8), ~5 s para juntar.
- **US$ 0,06 (3090 Community a 0,22/h) a US$ 0,14 (máquinas a 0,50/h)**; 4090 Secure a 0,89/h ≈ US$ 0,25. VPS antes: ~9,8 h.
- Antes do Pod, ~8–10 min de stills na VPS (grátis; com `REFS` uma refação reaproveita).
- Estoque: em 9 criações, 5 saíram na 1ª tentativa, 3 na 2ª (1 min) e 1 na 6ª (5 min). A lista aceita 3090, A5000, 4090, A4500, A4000, L4, Community e depois Secure; o Runpod já entregou também uma RTX PRO 4500 (passou na prova).

## Testes do caminho dos canais e do áudio
- **Padrão dos canais** (`dossie-es/006-masones`, só leitura, trecho 3000–3899, bundle feito pelo script com `ENTRY=src/index.jsx`, `AUDIO=public/audio/mix.wav`, lock 4.0.539 ≠ imagem → `npm ci` de 2 s): RTX A4500 US$ 0,19/h, Pod 145 s, **US$ 0,008**; prova SSIM 1,000; 900/900 quadros; contra o `out/video.mp4` publicado 0,986–0,990 (crf 18 × 20). Cenas 2D não usam a GPU (pico 2 MiB), e mesmo assim o Pod sai mais rápido que a VPS.
- **Áudio dentro da composição:** (1) passada `--codec=wav` separada levou 5 min no Pod para 30 s (sem `--gl`, caiu em CPU); (2) blocos `h264-mkv` + PCM saíram com SSIM 0,61–0,63 nas amostras no Pod (no VPS o mesmo MKV confere 0,996; causa não investigada). Como **nenhum canal usa** (todos renderizam mudo + `mix.wav`), o caminho foi removido: o script exige `AUDIO=` ou `MUDO=1`.
- Trecho `[a-b]` com `AUDIO`: o áudio começa em a/fps (clipe certo para refação).
- Um teste foi morto pelo `timeout` do meu comando no meio do render: o trap destruiu o Pod e registrou o custo (confirma a destruição em erro).

## Custo desta tarefa
Runpod: **US$ 0,77** em 9 Pods (`financas.consumo` 185–193, `ref_id` 17); saldo pela API **39,6981 → 38,9263 (US$ 0,772)**, igual ao estimado pelo script. Com o teste da manhã (US$ 0,30), a validação inteira custou US$ 1,07. GitHub Actions: 10 builds (9 falhas de rede/pacote até achar o caminho), minutos gratuitos. Teto US$ 2.
