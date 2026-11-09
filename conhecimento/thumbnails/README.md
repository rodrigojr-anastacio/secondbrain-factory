# Thumbnails: regras gerais e galeria das thumbs no ar

> **Regras gerais. Regra de canal está em `canais/<slug>/biblia/` e sempre prevalece.** O padrão de thumb de cada canal e a análise de cada thumb publicada (com CTR) estão em `canais/<slug>/biblia/thumb.md`. Esta pasta guarda só a **galeria** dos arquivos `.jpg` (o `.gitignore` só libera mídia em `conhecimento/**`) e as regras que valem para qualquer canal.

**Como atualizar:** ao publicar ou trocar uma thumb, copie (`cp`, nunca mover) a versão **no ar** para esta pasta como `<canal>-<video>.jpg` (**< 500 KB**; se passar, gere um JPEG reduzido com ffmpeg) e registre a análise e o CTR no `thumb.md` da bíblia do canal. O **CTR não vem no `tools/report.py`**: o Rodrigo exporta o CSV do Studio (~2x/semana) e o orquestrador grava em `youtube.studio_video` (view `studio_ultimo`); registre com a data e a janela. Sem dado = **Hipótese**. Commit descritivo.

Última revisão: 2026-11-04 (caixinhas por canal: análises movidas para as bíblias). Confirmação da versão no ar: baixar `i.ytimg.com/vi/<id>/maxresdefault.jpg` via WARP e comparar por SSIM com os arquivos locais (SSIM ≥ 0,98 = mesma arte).


> **Lente de apoio (não é regra):** antes de propor, passe a ideia pelas 5 condições de decisão por atalho em `conhecimento/decisao-do-clique.md` (09/11/2026).
---

## Galeria (arquivo → análise)
| Arquivo | Vídeo | Análise e CTR |
|---|---|---|
| `historia-ptbr-001-egito.jpg` | `g847Td0Plsk` | `canais/historia-ptbr/biblia/thumb.md` (Studio 09/11, 28 dias: **CTR 4,02%**, 920 impressões; o "< 2%" de 04/11 era de poucas horas) |
| `historia-ptbr-002-india.jpg` | `MV5SSjoccqE` | `canais/historia-ptbr/biblia/thumb.md` (Studio 09/11, 28 dias: **CTR 3,69%**, 1.273 impressões) |
| `lotr-fr-001-maiores-cidades.jpg` (no ar) | `87BdomKxa-M` | `canais/lotr-fr/biblia/thumb.md` (CTR sem dado) |
| `lotr-fr-001-maiores-cidades-v1-substituida.jpg` | `87BdomKxa-M` (até 03/11) | `canais/lotr-fr/biblia/thumb.md` (CTR 1,7%) |

## Regras gerais
**Faça**
- **Texto sempre composto no código** (`src/Thumbnail.jsx` no Remotion), nunca escrito pela IA. Fonte e cor são da bíblia do canal. [BRIEF.md e QA.md historia-ptbr 001]
- **Legível no celular:** 2–3 palavras grandes na arte; confira numa prévia de 320×180.
- Base em qualidade alta (`high` no gpt-image-2) e **3 variações** para o "Testar e comparar" do YouTube; registre qual venceu.
- **Fidelidade:** o lugar ou personagem nomeado tem de ser **aquele** (nunca um lugar real no lugar de um fictício).
- Cada canal tem um **template reconhecível na grade** (o mesmo layout sempre); o template é da bíblia e não se usa em outro canal.

**Não faça**
- Texto pequeno em várias linhas (título + subtítulo + lista de nomes): ilegível no celular. Caso real: thumb v1 das cidades (lotr-fr), 4 linhas, **CTR 1,7%**. [lotr-fr biblia/thumb.md]
- Pintura ou foto que não representa o lugar nomeado.
- Copiar a composição exata do concorrente.
- **Hipótese (04/11/2026):** thumb "bonita" sem lacuna de curiosidade (panorama + nome) não gera clique: Egito e Índia com CTR < 2%. [BRIEF-historia-003-v2.md]

## Pendências de dado
- CTR do Studio (com a janela) para todas as thumbs no ar; registrar se o "Testar e comparar" foi usado e qual venceu. Sem isso, as conclusões são Hipótese.
