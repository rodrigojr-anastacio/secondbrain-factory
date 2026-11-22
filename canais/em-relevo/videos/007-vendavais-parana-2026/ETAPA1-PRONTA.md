# ETAPA 1 PRONTA: Em Relevo 007, vendavais no Paraná de 20/11/2026 (22/11/2026)

`youtube.videos` **id 58** (em-relevo, nº 7, status `roteiro`, título = T1). Pasta: `canais/em-relevo/videos/007-vendavais-parana-2026/`. **Aguarda aprovação do Rodrigo** (`APROVACAO.md`); este job **não** enfileira a etapa 2 (o orquestrador enfileira depois do OK; produção prevista para a noite de 22/11). Custo da etapa 1 em dinheiro: **US$ 0** (Data API ~60 unidades, `search.list` 0; detector sem tradução; Whisper local).

## Ângulo (1 linha)
**O rastro de uma tarde:** a reta das rajadas de 14 estações do Simepar (Capanema 13h45 → Cornélio Procópio 20h15, ~430 km, ~70 km/h, r² 0,98) + satélite GOES-19 + relevo do Paraná em escada → por que o temporal entra pelo oeste, o mesmo lado de Rio Bonito do Iguaçu 2025. `ANGULO.md` (provisório: transcrições barradas pelo YouTube no WARP em 21/11; 2–3 transcritas depois por Whisper).

## Embalagem aprovada (crivo r3, 3 de 3)
| par | título | padrão do título | thumb (padrão) | texto |
|---|---|---|---|---|
| **A** | **Por que o temporal entra pelo OESTE do PARANÁ?** (46) | Por que [LUGAR] [anomalia]? (controle) | `mapa-lugar`: o Paraná em bloco 3D claro visto de sul, cor subindo do verde (oeste) ao marrom (leste), seta coral entrando pela ponta oeste | "PELO LADO BAIXO?" (tarja navy, embaixo à direita) |
| **B** | **O temporal que atravessou o PARANÁ em 6 horas e meia** (52) | O/A [coisa] que [faz algo] | `documento-evidencia`: GOES-19 canal 13 de 20/11 (um quadro só, 22–23 UTC), faixa laranja cruzando o contorno do PR | "13H45" em Capanema · "20H15" em Cornélio Procópio |
| **C** | **RIO BONITO 2025, FOZ 2026: por que o temporal vem pelo mesmo lado?** (66) | Contraste A × B + por que | `cena-acao`: foto CC0 (DPU, 18/11/2025) do madeiramento de um telhado em Rio Bonito do Iguaçu | (nenhum) |
Histórico: r1 0/3 (A "POR AQUI?" repetia o título; B 2ª referência era live e horas desencontradas; C vendia o "mês dos 3 temporais", fórmula de clone, notícia no título, foto de TV) → r2 1/3 (B ok; A "LADEIRA ABAIXO?" contradizia a seta; C aéreo de entulho = tragédia/textura) → r3 3/3. `embalagem/crivo-r1..r3.md`, `EMBALAGEM-r1/r2.md`. Registrado em `youtube.embalagem_variantes` (A/B/C = mapa-lugar, documento-evidencia, cena-acao).

**Promessa:** no mapa, o caminho do temporal de 20/11 (Capanema 13h45 → Cornélio Procópio 20h15) e por que os temporais entram pelo oeste do Paraná, o mesmo lado de Rio Bonito do Iguaçu em 2025.
**Onde o roteiro paga** (tempos estimados; hook a ~1,36×):
- frase-âncora no **b04 (~0:32–0:38)**: "Por que o temporal entra pelo oeste do Paraná, de novo pelo mesmo lado? A resposta está no mapa." (b01–b03: Capanema 81,7 → Cornélio 98,3, 423 km, 6 h 30, dois tornados, Rio Bonito 2025).
- reta das estações **b05–b06 (~0:38–1:04)** e exceções Paranaguá/Cambará **b07 (~1:04–1:16)**; "atravessou o Paraná em 6 horas e meia" no **b09 (~1:32)** (paga T2).
- "pelo oeste": cap. 2 (b14–b19, ~2:25–4:00) e cap. 3 (b20–b28, ~4:00–6:05), com a resposta à Thumb A no b26 ("a ladeira não puxa a tempestade").
- "mesmo lado" (T3): cap. 4 **b29–b35 (~6:05–7:50)**, as duas linhas no mesmo mapa (b33) e o que "mesmo lado" quer dizer (b34).
- Resposta b41–b43; fecho útil b44–b45 (SMS 40199; árvores e postes); CTA b46 (001 `bG6-E4qjXYc`; sem próximo vídeo).

## Roteiro e portões
- `shared/roteiro.py` → `shared/blocos.json` (**46 blocos, 1.661 palavras, 9.048 caracteres** no TTS, **~9:55**); leitura em `SCRIPT.md`/`ROTEIRO.md`; fatos em `pesquisa/FATOS.md` (+ `FATOS-bruto.md` com URL de tudo); bloco → fonte e cota em `SOURCES.md` (~80% dos blocos de conteúdo fora da manada; meta 40%).
- **Detector de cópia: 14/100** (`SIMILARIDADE.md`; maior = o nosso 001, por fatos repetidos de Rio Bonito; manada 2–3/100; nenhum bloco com gêmeo em 2+ referências).
- **Crivo de ângulo: r1 APROVADO** (7 de 7; cota 23/30 = 77%; condição do item 6: reconferir E2–E7 em fonte primária antes da voz) → recomendações aplicadas (b31 sem a largura do 001; b35 troca Maringá F2, abertura do 001, pelos 15 tornados do ano; b42 sem causalidade do relevo; "porta" uma vez só). `roteiro-crivo/crivo-angulo-r1.md`, `CRIVO-ANGULO.md`.
- Storyboard: `STORYBOARD.md`, `shared/storyboard.py` → `shared/storyboard.json`, `shared/cenas.json` (zero IA; 10 mídias reais; ~153 eventos visuais, ~16/min).

## O que a etapa 2 precisa saber
1. **Reconferir antes da voz** (AEN/Simepar devem publicar 22–24/11): rajadas e horas (E4), tornados F1 (E2), 353.849 (E5), boletim da Defesa Civil (E6), números de Foz/Londrina (E7). O que não confirmar: "segundo o Simepar" ou sai. Se o Simepar publicar lista de rajadas diferente, **refazer a reta** (N1) e, se a hora final mudar, ajustar T2 ("6 horas e meia") e os rótulos da Thumb B **antes** do pacote.
2. **Altitudes** (b21–b22, b25): gerar o perfil SRTM oeste → leste (N4) e conferir Curitiba ~930, Guarapuava > 1.000, Cascavel ~780, Foz ~160 (sede; o crivo r3 lembrou que ~120 m é o leito do rio). Pico Paraná 1.877 m (IBGE).
3. **GOES-19:** baixar o NetCDF ABI-L2-CMIPF canal 13 de 20/11 12–23 UTC do bucket público `s3://noaa-goes19` e reprojetar para lon/lat; conferir que às 9h (12 UTC) o aglomerado está mesmo **a oeste do Paraná** (b15 afirma). O STAR (jpg em `dl/goes19/`) só guarda ~10 dias e já está baixado.
4. **Voz ElevenLabs** (Fernanda, `eleven_v3`) ou reserva Fish #NATASHA drama-3, `--video 58`. ~9.000 caracteres. Hook = b01–b04 (marcha 1). Conferir na `legendas.srt` que a frase-âncora termina **≤ 0:40**. **Pronúncia:** Capanema, Cornélio Procópio, Manoel Ribas, Rio Bonito do Iguaçu, Quedas do Iguaçu, Cantagalo, Candói, Entre Rios, Guarapuava, Paranaguá, Cambará, Ubiratã, Cerro Azul, Simepar ("si-me-PAR"), Copel ("co-PÉL"), GOES ("gôs"), NOAA ("NOA"), TRMM (letra por letra), UFSM (letra por letra), "F1" ("éfe um"), "40199" (por extenso no `fala_tts`).
5. **Thumbs A/B/C, uma por conceito** (`Thumb.jsx`, US$ 0): A = bloco 3D do PR (câmera sul-sudoeste para esconder o litoral atrás da serra; prévia `embalagem/previa-a-r3-1280.jpg`); B = GOES reprojetado, **um quadro só**, contorno do PR em branco, rótulos presos às cidades (prévia `previa-b-r3-1280.jpg`); C = `dl/fotos/dpu/rb-telhado-54944696133-orig.jpg`, recorte mais alto, legenda neutra "RIO BONITO DO IGUAÇU · 18/11/2025" (nunca "telhado arrancado"). Prévia 320 ao lado de `embalagem/mosaico.jpg` e `vizinhas-em-relevo.jpg`.
6. **Pacote:** A = T1, B = T2, C = T3 com o padrão de cada par no `youtube.txt`; regravar `variantes.json` + `embalagem_variantes.py registrar`. Créditos: NOAA/NESDIS (GOES-19), NASA GPM IMERG, Copernicus Sentinel-2 (via Commons), DPU (CC0), Ari Dias/AEN (CC0), Copel/AEN (CC0), Defesa Civil/AEN, Simepar, Copel, Defesa Civil PR, UFSM (Lopes & Nascimento 2025), Zipser et al. 2006, Velasco & Fritsch 1987, SRTM/Terrain Tiles, IBGE, trilha Kevin MacLeod (CC BY 4.0). Sem "morte" em título/descrição/tags.
7. Render só no Runpod (`tools/render_runpod.sh`, em partes), pré-QA visual antes; nada em `/tmp`. **Teto US$ 3.** Entrega no Drive (`tools/entregar_drive.sh em-relevo 007-vendavais-parana-2026`).

## Pendências (não bloqueiam)
- Transcrições da manada incompletas (bloqueio do YouTube no WARP); antes da voz, rodar `tools/manada.py transcrever` nos que faltarem e repetir `tools/similaridade_roteiro.py` (se passar de 18, voltar ao crivo de ângulo).
- `watch.py` da referência não rodou (mesmo bloqueio).
- Velasco & Fritsch (b17) citado pelo abstract; Zipser (b16) pelo abstract + release da NASA.
- Fotos de 20/11 com licença livre ainda não existem; o vídeo usa fotos CC0 de 07/11 com a data certa na legenda.
