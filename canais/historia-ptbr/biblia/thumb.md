# Thumbnail: historia-ptbr

Regra de canal: **prevalece** sobre `conhecimento/thumbnails/README.md` (regras gerais e o procedimento de arquivar a thumb no ar). As thumbs publicadas ficam na galeria `conhecimento/thumbnails/historia-ptbr-*.jpg`.

## Estado em 04/11/2026: o padrão atual NÃO está funcionando
- **CTR do Egito e da Índia abaixo de 2%** (Rodrigo, `~/workspace/referencias/BRIEF-historia-003-v2.md`, 04/11/2026; janela não informada). Os dois seguem o mesmo padrão (lugar panorâmico + nome gigante + datas). "O padrão precisa mudar."
- Nenhuma das 3 thumbs do 003 v1 "gera curiosidade de clique" (mesma fonte).
- Em teste: 4 conceitos novos no job `historia-003-v2` (`videos/003-ira/v2-amostras/thumbs/`). **Quando o Rodrigo aprovar um, registre aqui o padrão novo** e o porquê.

## O que manter (vale até haver dado contra)
- Texto **sempre composto no código** (`src/Thumbnail.jsx`), nunca escrito pela IA. Hoje: Libre Caslon 700 + Open Sans 800. [BRIEF.md 001; QA.md 001]
- No máximo 2–3 palavras na arte, legíveis em 320×180; o resto vai no título. [estilo.md antigo]
- Base em qualidade alta (`high` no gpt-image-2) e **3 variações** para o "Testar e comparar".
- Direção do Rodrigo (até o 002): inspirada na referência, mas com **identidade nossa**: personagem-guia (o bonequinho do canal) reagindo ao lugar/época; assinatura de tempo (selo com o período, sempre no mesmo canto e na mesma cor); cor de destaque fixa do canal (amarelo-ouro ou laranja). [estilo.md antigo]
- **Hipótese (04/11):** falta curiosidade (lacuna de informação, conflito, rosto com emoção). Panorama bonito + nome do país não cria pergunta.

## Thumbs no ar (análise movida de `conhecimento/thumbnails/README.md`, 2026-11-04)
### historia-ptbr-001-egito.jpg
- Vídeo: "A história INTEIRA do Egito em 17 minutos" · `g847Td0Plsk` · `youtube.videos` id 3. Origem: `videos/001-egito/out/thumbnail.jpg` (v2, base `high`); SSIM 0,996 com a pública (2026-11-04).
- Tem: panorama do Nilo com pirâmides, Esfinge, templos e barcos à esquerda; céu e deserto livres à direita; "EGITO" em serifa preta enorme e "5000 a.C. – 2026" em sans negrito. É a fórmula da referência VQPzrVMHWlg (417 mil views).
- Não tem a "identidade nossa" (personagem-guia, cor de destaque). **CTR < 2%** (Rodrigo, 04/11). Views: 6 em 2026-11-04.
### historia-ptbr-002-india.jpg
- Vídeo: "A HISTÓRIA COMPLETA da Índia em 19 minutos" · `MV5SSjoccqE` · id 4. Origem: `videos/002-india/thumb-var/final/E-gandhi.jpg`; SSIM 0,984 com a pública. A thumb do pacote (`out/thumbnail.jpg`, panorama) **não** é a que está no ar.
- Tem: "pop-out" com Gandhi em cartoon, grande, à esquerda, saindo de uma moldura com o Taj Mahal ao pôr do sol; fundo laranja-açafrão; "ÍNDIA" em serifa branca com contorno e "3300 a.C. – 2026" em amarelo. fal.ai (`thumb-variacoes.json`; `financas.consumo` ids 19–20, US$ 0,13). Existe a variação `D-imperador.jpg`.
- O traço do Gandhi é diferente dos bonequinhos de cabeça redonda. **CTR < 2%** (Rodrigo, 04/11). Views: 17 em 2026-11-04. Sem registro de "Testar e comparar" D × E.

## Não faça
- Layout "pôster de expediente" (personagem à esquerda + SIGLA gigante + sello rojo + aba de pasta): é do `dossie-es`.
- Pintura a óleo romântica com pergunta: é do `lotr-fr`.
- Texto pequeno em várias linhas.
