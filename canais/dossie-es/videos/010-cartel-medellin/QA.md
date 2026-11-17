# QA · dossie-es 010 El Cártel de Medellín (16/11/2026)
| Item | Resultado |
|---|---|
| Render | 14:04,9 (844,9 s), 1920×1080 30 fps H.264+AAC, −15,2 LUFS, pico −3,1 dBFS, 0 telas pretas, 0 silêncios > 1,5 s; Runpod em 5 faixas, SSIM mín 0,992; título "en 14 Minutos" confere |
| Voz | Fish s2.1-pro por frase, US$ 0,18, 80 blocos; Whisper média 98,7%; abaixo de 93% só por grafia (Turbay→"Turbey", "es Jairo"); "MAS" como sigla saía "emaz" → respelling "Más" em `blocos-voz.json` (N013 regerado, 93,1%); nenhuma tag falada |
| Promessa (EMBALAGEM) | frase-âncora "Esta es TODA la historia del Cártel de Medellín. Y de la guerra… por una sola palabra: extradición" em **0:25,6** (`legendas.srt`); Exp. 1 "El Tratado" 0:34; reféns (Exp. 8–9) 7:52–10:03, "rescatarla" 9:20; "El Artículo" 10:55 com o texto exato («Se prohíbe la extradición de colombianos por nacimiento») 11:09 |
| Thumbs | A = algemas + MEDELLÍN + sello INTOCABLES (objeto-simbolo); B = folha com tarja + ART. 35 (documento-evidencia); C = fazenda + helicópteros + ¿RESCATE? (cena-acao). Três diferentes, A/B/C = T1/T2/T3, legíveis a 320×180. A refeita 1× (algemas maiores); B com zoom na folha (sem mesa/livro vermelho) |
| 6b/6c | `SIMILARIDADE.md` 11/100 (< 30, roteiro não mudou); `CRIVO-ANGULO.md` aprovado r2 |
| Imagens | 204 (nano-banana); 47 com moldura/faixa recortadas, 4 refeitas por recorte ruim, 10 refeitas pelo pré-QA (texto inventado, uniformes europeus, bandeira); I070 refeita por filtro do fal (422) |
| Pré-QA | 113 stills: 0 bloqueantes, 10 "alto" → corrigidos (restam textos pequenos de fundo e bandeiras genéricas, severidade baixa/média); I092 mantém sombra escura no batente da porta (intencional) |
| Custo | fal 8,76 + Fish 0,18 + Runpod 0,61 + API 0,29 ≈ **US$ 9,84** (teto 12) |
Incidentes: (1) 1º render preso no upload do bundle (167 MB em 18 min, Pod ligado): abortado, Pod destruído; bundle com stubs de áudio de 1 s (100 MB em vez de 409 MB; o render é mudo). (2) Bundle e `refs` ficaram velhos após refazer imagens: cópia para o bundle e novo render das 4 faixas (render v1 em `out/partes-v1/`). Pendência menor: nenhuma que bloqueie.
