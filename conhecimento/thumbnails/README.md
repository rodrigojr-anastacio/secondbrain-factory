# Thumbnails publicadas: por que funcionam (ou não) e o CTR medido

**Como atualizar:** ao publicar ou trocar uma thumb, copie (`cp`, nunca mover) a versão **no ar** para esta pasta como `<canal>-<video>.jpg` (**< 500 KB**; se passar, gere um JPEG reduzido com ffmpeg). Registre aqui a data, a origem do arquivo e o CTR. O **CTR não existe na API** (`tools/report.py`): só no YouTube Studio, então peça o número ao Rodrigo e registre com a data. Quem alimenta: **Métricas** (CTR e views), **Tendências** (thumbs das referências em `pesquisa/tendencias/assets/<data>/<id>/thumb.jpg`) e o **feedback do Rodrigo**. Sem dado, marque **Hipótese**. Depois de editar, faça commit descritivo.

Última revisão: 2026-11-04. A versão no ar foi confirmada baixando `i.ytimg.com/vi/<id>/maxresdefault.jpg` via WARP e comparando por SSIM com os arquivos locais (SSIM ≥ 0,98 = mesma arte).

---

## Regras rápidas

**Faça**
- O **nome do lugar gigante** e legível no celular, no máximo 2–3 palavras na arte; o resto vai no título. [estilo.md historia-ptbr]
- Uma **ilustração do lugar que dá para reconhecer na hora**, com contraste limpo e área livre para o texto. [estilo.md historia-ptbr]
- **Texto sempre composto no código** (Libre Caslon + Open Sans 800 no historia-ptbr), nunca escrito pela IA. [BRIEF.md 001; QA.md 001]
- Gere a base em `high`. [estilo.md historia-ptbr; ETAPA3.md 001]
- Gere **3 variações** e suba no "Testar e comparar" do YouTube. [estilo.md historia-ptbr]
- lotr-fr: a cidade nomeada tem de ser **aquela** cidade (fidelidade), com pergunta curta em letras grandes.

**Não faça**
- Texto pequeno em várias linhas (título + subtítulo + lista de nomes): ilegível no celular. Foi o caso da thumb das cidades com CTR de 1,7% (abaixo).
- Pintura real que não representa o lugar (Thomas Cole no lugar de uma cidade da Terra-média).

---

## historia-ptbr-001-egito.jpg
- **Vídeo:** "A história INTEIRA do Egito em 17 minutos" · `g847Td0Plsk` (republicação; o upload original `s-D5Sk7prJI` está indisponível) · `youtube.videos` id 3.
- **Origem:** `canais/historia-ptbr/videos/001-egito/out/thumbnail.jpg` (v2, base em `high`). SSIM 0,996 com a pública (2026-11-04). 274 KB, 1280x720.
- **O que tem:** panorama do Nilo com pirâmides, Esfinge, templos e barcos à esquerda; céu e deserto livres à direita; "EGITO" em serifa preta enorme e "5000 a.C. – 2026" em sans negrito. É a fórmula da referência VQPzrVMHWlg (417 mil views).
- **Por que deve funcionar (Hipótese):** o lugar e o nome são reconhecíveis na hora, o contraste é limpo e a promessa ("5000 anos") está no selo de datas. Ainda não tem a "identidade nossa" pedida no `estilo.md` (personagem-guia, cor de destaque).
- **CTR:** **sem dado** (o Studio não foi consultado). Views: 6 (`youtube.metricas_video`, 2026-11-04).

## historia-ptbr-002-india.jpg
- **Vídeo:** "A HISTÓRIA COMPLETA da Índia em 19 minutos" · `MV5SSjoccqE` · `youtube.videos` id 4 (o banco ainda o marca como `pronto`).
- **Origem:** `canais/historia-ptbr/videos/002-india/thumb-var/final/E-gandhi.jpg`. SSIM 0,984 com a pública (2026-11-04). 247 KB. A thumb do pacote (`out/thumbnail.jpg`, panorama como a do Egito) **não** é a que está no ar.
- **O que tem:** efeito "pop-out": Gandhi em cartoon, grande, à esquerda, saindo de uma moldura com o Taj Mahal ao pôr do sol; fundo laranja-açafrão; "ÍNDIA" em serifa branca com contorno e "3300 a.C. – 2026" em amarelo. Gerada no fal.ai (`thumb-variacoes.json`; `financas.consumo` ids 19 e 20, US$ 0,13). Existe outra variação, `D-imperador.jpg` (imperador mogol).
- **Por que deve funcionar (Hipótese):** rosto famoso e expressivo em primeiro plano, mais a cor de destaque forte. Segue a direção "personagem-guia + cor fixa" do `estilo.md`, mas o traço do Gandhi é diferente dos bonequinhos de cabeça redonda do canal.
- **CTR:** **sem dado**. Views: 17 (`youtube.metricas_video`, 2026-11-04). Não há registro de "Testar e comparar" entre E e D.

## lotr-fr-001-maiores-cidades.jpg (no ar)
- **Vídeo:** "Quelles étaient les plus grandes villes de la Terre du Milieu ?" · `87BdomKxa-M` · `youtube.videos` id 2 · publicado em 2026-11-02.
- **Origem:** `canais/lotr-fr/videos/001-maiores-cidades/thumbs-v2/final/A.jpg` (prompt "A-minas-tirith" em `thumbs-v2.json`, gpt-image-2, gerada em 2026-11-03; `financas.consumo` id 13, US$ 0,50 pelas 3 variações A/B/C). SSIM 0,979 com a pública (2026-11-04). 245 KB.
- **O que tem:** Minas Tirith em pintura a óleo romântica (sete níveis, torre branca, luz dourada) ocupando a esquerda; céu escuro à direita com "LA PLUS GRANDE" em branco e "VILLE ?" enorme em amarelo.
- **Por que deve funcionar (Hipótese):** a cidade mais conhecida da Terra-média, fiel ao livro, mais uma pergunta curta de 2 linhas com contraste alto.
- **CTR:** **sem dado** desde a troca. Views: 11 → 36 → 54 (2026-11-02 → 11-04, `youtube.metricas_video`). Não dá para atribuir a alta à troca sem o CTR do Studio.

## lotr-fr-001-maiores-cidades-v1-substituida.jpg (referência do que não funcionou)
- **Origem:** `canais/lotr-fr/videos/001-maiores-cidades/out/thumbnail.png` (3,2 MB, 1920x1080), reduzida para JPEG 1280x720 (127 KB). Era a thumb do pacote original (2026-11-01).
- **O que tem:** "The Course of Empire: The Consummation" de Thomas Cole (domínio público; `assets_credits.json`), com faixa escura à esquerda e 4 linhas de texto: "LA PLUS GRANDE / VILLE / DE LA TERRE DU MILIEU ? / GONDOLIN · KHAZAD-DÛM · OSGILIATH · ???".
- **CTR medido: 1,7%.** Fonte: o Rodrigo, repassado pelo manager no `~/workspace/referencias/BRIEF-fase1.md` (2026-11-04). Não há registro no banco nem export do Studio, e não sabemos a janela de impressões. Registre a janela quando o Rodrigo confirmar.
- **Por que não funcionou (Hipótese):** o texto é pequeno e em 4 linhas (ilegível na grade do celular); a pintura é uma cidade real/alegórica, não uma cidade de Tolkien, então não comunica "Terra-média"; e o contraste é baixo (paleta bege e marrom). Em 2026-11-03 ela foi trocada pela variação A (acima). Com base nas datas dos arquivos, a troca parece ter sido uma resposta ao CTR baixo.

---

## Pendências de dado
- CTR do Studio para as 3 thumbs no ar (e a janela), com data. Sem isso, toda conclusão acima é Hipótese.
- Registrar se o "Testar e comparar" foi usado (Índia: D × E; cidades: A × B × C) e qual venceu.
