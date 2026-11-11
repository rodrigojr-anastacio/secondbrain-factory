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
