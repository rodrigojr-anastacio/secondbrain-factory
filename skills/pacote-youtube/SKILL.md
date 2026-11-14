---
name: pacote-youtube
description: Use quando o vídeo da fábrica do YouTube estiver renderizado para montar o pacote de publicação em out/ - youtube.txt com 3 títulos, descrição (CTA + resumo + capítulos + fontes/créditos), capítulos em ordem crescente desde 0:00, fontes, créditos, tags e categoria - e o lembrete do que o Rodrigo marca ao publicar (sem menção a IA no texto; padrão de 14/11/2026).
---

# pacote-youtube: out/youtube.txt + checklist de publicação

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`.
Procedimento-base: `playbooks/produzir-video.md` §7. Modelo recomendado: **sonnet** (dentro da etapa `montagem-render`).

## Antes de agir
0. **Primeiro a bíblia do canal** (caixinha): `canais/<slug>/biblia/README.md` (canal-modelo e "o que NÃO fazer aqui") e `biblia/titulo.md` (fórmula do título do canal, título B, nota da descrição). A bíblia **prevalece** sobre `conhecimento/` (só regras gerais). Nunca aplique padrão de outro canal.
1. Regras gerais: `conhecimento/titulos.md` (N = duração) e `conhecimento/roteiros.md` (capítulos fora de ordem já aconteceram).
2. Leia `conhecimento/anti-padroes.md`.
3. Leia `canais/<slug>/canal.yaml` (idioma).
4. Leia `$V/BRIEF.md`, `$V/SOURCES.md`, `$V/qa/capitulos.json` (gerado pelo `build.py`) e `$V/out/legendas.srt`.
5. Modelo: o `out/youtube.txt` do **vídeo anterior do mesmo canal** (fora do git; leia se existir).

## Passos
1. Pegue a duração real: `ffprobe -v error -show_entries format=duration -of csv=p=0 $V/out/video.mp4`. O **N do título** é essa duração arredondada em minutos.
2. Escreva `$V/out/youtube.txt` (e copie para `$V/entrega/pacote/youtube.txt`) no **padrão de 14/11/2026** (`conhecimento/politicas-youtube.md`), no idioma do canal, **nesta ordem**:
   - **TÍTULOS:** 3, de 3 padrões diferentes dentro da fórmula da `biblia/titulo.md`, pareados às thumbs A/B/C (≤ 100 caracteres cada).
   - **DESCRIÇÃO** (o texto que vai no campo do YouTube, nesta ordem): (1) **CTA curto** de inscrever-se, curtir e compartilhar (1–2 linhas, natural); (2) **descrição breve** do vídeo (2–4 linhas, sem repetir o título, sem entregar a resposta; a pergunta do fecho pode entrar aqui); (3) **capítulos** de `qa/capitulos.json`, `M:SS Título`, começando em `0:00`, crescentes, ≥ 3 de ≥ 10 s, cada tempo conferido na `legendas.srt`; (4) **fontes e créditos** (fontes de `SOURCES.md`; acervo, fotos e música com licença; créditos só aqui, nunca na tela).
   - **TAGS:** 10–15, idioma do canal.
   - **CATEGORIA** (Educação) e **idioma** do vídeo.
   - **CHECKLIST DE PUBLICAÇÃO** (para o Rodrigo, **fora da descrição**): Uso de IA = **Sim** (Studio → Atributos), não é para crianças, idioma, 3 thumbs + 3 títulos no "Testar e comparar", mp4 1080p (nunca o do Telegram), legendas `legendas.srt`.
   - **Proibido no arquivo:** qualquer menção a IA, voz sintética ou "conteúdo gerado/alterado" (o Rodrigo declara no campo "Uso de IA"); e, em títulos, descrição e tags, morte/morreu/morto/assassinado/assassinato (es: muerte/murió/muerto/asesinado/asesinato; en: death/died/dead/killed/murdered/assassinated/murder) e sinônimos chocantes (massacre, chacina, "chocante", "perturbador", "nojento"). Rode `grep -n -i` com essas palavras no arquivo antes de fechar.
3. A **Hipótese de título/descrição** novas vão para a bíblia (ver Loop). O checklist do item acima é o lembrete ao Rodrigo; não repita na descrição.
4. Copie também o essencial (título e capítulos) para `$V/ETAPA3.md`, porque `out/` fica fora do git.
5. **Entrega final no Google Drive do Rodrigo** (não no Mac): monte `entrega/` e rode `tools/entregar_drive.sh <canal_slug> <NNN-slug>` → `Youtube/<nome do canal>/<NNN-slug>/` (nome vem do `canal.yaml`; só copia, nunca apaga). Logos/capas: `tools/entregar_drive.sh <canal_slug> identidade`. Usa rclone (remote `gdrive`); se faltar, veja `BLOQUEIO-drive.md`. O conector claude.ai Drive só serve para arquivos de texto pequenos (binário passaria pelo contexto do modelo).

## Critérios de pronto (avaliar)
Valide com um one-liner Python sobre `out/youtube.txt`:
- Capítulos em ordem estritamente crescente, o primeiro `0:00`, o último < duração.
- N do título = duração arredondada (± 1 min); título na fórmula da bíblia do canal e no idioma do canal.
- Título ≤ 100 caracteres; descrição na ordem CTA → resumo → capítulos → fontes/créditos; fontes presentes.
- **0** ocorrências das palavras proibidas em títulos/descrição/tags e **0** menção a IA/voz sintética no `youtube.txt`; checklist do Rodrigo com "Uso de IA = Sim".
- Arquivos do pacote presentes: `out/video.mp4`, `out/thumbnail.jpg` (< 2 MB), `out/legendas.srt`, `out/youtube.txt`.

## Loop de melhoria
1. **Avaliar:** rode a validação e o checklist acima.
2. **Corrigir:** até 2 rodadas; resto = pendência no `ETAPA3.md`.
3. **Registrar:** fórmula de título/descrição nova em **`canais/<slug>/biblia/titulo.md`** como **Hipótese** (o Métricas confirma com views/CTR depois), com **data e fonte**.
4. **Commitar:** `git add $V/ETAPA3.md` (+ conhecimento; `out/` não vai ao git) e
   `git commit -m "<canal>/<NNN>: pacote YouTube (título, N capítulos)"`.
5. Status: `psql -d vida -c "UPDATE youtube.videos SET status='pronto', titulo='<título final>', atualizado_em=now() WHERE id=<id>"` (só depois do QA aprovado). **A publicação é sempre do Rodrigo.**
