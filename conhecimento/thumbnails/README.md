# Thumbnails: regras gerais e galeria das thumbs no ar

> **Regras gerais. Regra de canal está em `canais/<slug>/biblia/` e sempre prevalece.** O padrão de thumb de cada canal e a análise de cada thumb publicada (com CTR) estão em `canais/<slug>/biblia/thumb.md`. Esta pasta guarda só a **galeria** dos arquivos `.jpg` (o `.gitignore` só libera mídia em `conhecimento/**`) e as regras que valem para qualquer canal.

**Como atualizar:** ao publicar ou trocar uma thumb, copie (`cp`, nunca mover) a versão **no ar** para esta pasta como `<canal>-<video>.jpg` (**< 500 KB**; se passar, gere um JPEG reduzido com ffmpeg) e registre a análise e o CTR no `thumb.md` da bíblia do canal. O **CTR não vem no `tools/report.py`**: o Rodrigo exporta o CSV do Studio (~2x/semana) e o orquestrador grava em `youtube.studio_video` (view `studio_ultimo`); registre com a data e a janela. Sem dado = **Hipótese**. Commit descritivo.

Última revisão: 2026-11-14 (embalagem + crivo; antes, 2026-11-04: caixinhas por canal, análises movidas para as bíblias). Confirmação da versão no ar: baixar `i.ytimg.com/vi/<id>/maxresdefault.jpg` via WARP e comparar por SSIM com os arquivos locais (SSIM ≥ 0,98 = mesma arte).


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

## Embalagem + crivo (14/11/2026)
O conceito de thumb nasce na etapa `embalagem` (skill `embalagem`, antes do roteiro) e passa pelo crivo independente (`skills/embalagem/CRIVO.md`); a skill `thumbnail` só executa a arte do conceito aprovado. Só entra aqui o que apareceu em **2+ canais** na reembalagem de 14/11/2026 (fonte: `pesquisa/reembalagem-2026-11-14/PROPOSTAS.md` (a) e (b), `padroes.md`); o resto fica na bíblia do canal.
- **1 foco e poucos elementos.** Reprovaram na r1 por muitos focos: historia-ptbr (Roma v1 com 8 elementos; Brasil v1 com 3 focos), dossie-es (KGB v1 com 6) e Em Relevo (El Niño com 3 focos; Sul com 6 elementos e o Sul a ~15% da altura). Confira numa maquete 320×180 ao lado do mosaico do tema.
- **A thumb não repete palavra nem ideia do título**; juntos criam a pergunta. Reprovaram: viking + tamanho nos dois (historia-ptbr Rússia v1), "559 a.C. · 2026" = "De Ciro aos aiatolás" (Irã v1), "ROBADO" × "Robaron" e guarda-chuva + "LONDRES 1978" + KGB (dossie-es). Avalie a thumb com **cada** um dos 2 títulos.
- **Lacuna em vez de resposta:** pergunta curta ou sello de uma palavra (historia-ptbr "NADA MUDOU?"; dossie-es "FALSA", "¿QUIÉNES?"; Em Relevo "CULPA DOS ANDES?"). Sello que lê junto com a sigla estraga ("CIA FALSA").
- **Diferenciar da grade do tema, não copiar o que todas fazem** (gap 2): clones de historia-ptbr com líder atual + cidade em chamas + NOME + datas; Em Relevo com o Pacífico inteiro vermelho e o "Sul vermelho + funil". O mosaico do tema (`embalagem/mosaico.jpg`) é obrigatório e é olhado antes de propor.
- **Referências medidas:** ≥ 2 thumbs reais do mesmo padrão, acima da mediana real do canal delas (a mediana de olho errou na r1). Padrão sem prova (ex.: objeto banal sem rosto no dossie-es) fica **Hipótese** de A/B.
- **Fundo, base e texto:** o texto continua composto no código; confira a base da IA de perto (código de cor escrito no canto, gotas vermelhas que parecem sangue, emenda de painel, moldura).
