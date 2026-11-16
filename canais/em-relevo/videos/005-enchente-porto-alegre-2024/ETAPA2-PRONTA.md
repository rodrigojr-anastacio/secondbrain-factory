# ETAPA 2 PRONTA: Em Relevo 005, enchente de maio/2024 (16/11/2026)

`youtube.videos` id 43 → `pronto`. **Duração 9:48 (588,2 s)**, 1920×1080 30 fps, AAC −14,1 LUFS (pico −1,3 dBFS, LRA 2,0), 0 telas pretas, 0 silêncios > 1,5 s, 6 cortes no 1º minuto. Entrega local em `entrega/` (video.mp4, legendas.srt, thumb-A/B/C.jpg, thumbnail.jpg, pacote/youtube.txt). Nada no Drive nem no YouTube.

**Promessa paga (legendas.srt):** frase-âncora "A chuva mais pesada caiu na serra. Quem afundou foi Porto Alegre." em **0:20,6**; "Oficialmente, o Guaíba é um lago" 0:59,5 e "quase 1/3 do Rio Grande do Sul" 1:04,9; "só tem uma saída" 1:07,9; cap. 2 em 3:02 ("todos desembocam no mesmo lago" 3:27); comportas/casas de bombas 6:02–6:15.

- **Voz** ElevenLabs (b01–b06 1,36×, resto 1,1×): 40 blocos, Whisper × roteiro 0,967; divergências = grafia do Whisper.
- **Visual:** LongoV5 (copiado do 004) + terreno novo do RS (SRTM/Terrain Tiles z10 + Blue Marble), **árvore de rios real do OSM** (2.212 trechos, 5 principais grossos, cresce das nascentes à foz), gota, e peças 2D novas (`Novos5.jsx`: maquete da orla, corte do sistema, perfil serra→capital, vazão, 3 cheias, calendário de picos, etapas, WWA, SMS). Esquemas marcados "ilustrativo" na tela.
- **Thumbs** A/B/C (código, US$ 0): conceito aprovado (mapa escuro + árvore ciano + "1/3 DO ESTADO?"); C = "UM TERÇO?". Prévia 320×180 conferida ao lado do mosaico: destaca-se.
- **Pré-QA:** 104 stills + `preqa_visual.py` (2 rodadas): 0 bloqueantes no fim (1ª: cunha preta do Sentinel-2 e 1941 com marca d'água → recortados; medidor, rótulos e cartões reposicionados). Restam "altos" menores de sobreposição momentânea (rótulo ONDE NASCEM OS RIOS × placa de Caxias; medidor).
- **Render Runpod** em 6 partes (≤10 min por comando): SSIM mín. 0,988; 17.646 quadros. O quadro 12015 reprovou a prova em 2 máquinas (4090 Secure), mas passou na conferência densa em outra GPU. Pods destruídos (API: 0). Houve 429 do Runpod (limite por hora) após muitas tentativas.
- **Custo ≈ US$ 0,85** (preqa 0,46 + Runpod ~0,39; voz no plano; teto 3).

## Pendências / para o Rodrigo
- **PMPA "Attribution only"** (não CC): 8 fotos da série da prefeitura; crédito está na descrição. Decisão de risco dele (ou trocar por Stuckert/satélite).
- 1941: foto de 800 px, pequena (cartep), marca d'água cortada.
- Rios do mapa = OSM (aproximado); esquemas fora de escala.
- `ETAPA2` ajustou `mix_audio` (trilha troca em b14/b34) e recriou os SFX (`shared/sintetiza_sfx.py`: os WAV tinham sido apagados pela limpeza).
