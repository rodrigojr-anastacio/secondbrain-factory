# Thumbnail: historia-ptbr

Regra de canal: **prevalece** sobre `conhecimento/thumbnails/README.md` (regras gerais e o procedimento de arquivar a thumb no ar). As thumbs publicadas ficam na galeria `conhecimento/thumbnails/historia-ptbr-*.jpg`.

## Estado em 04/11/2026: o padrão atual NÃO está funcionando
- **CTR do Egito e da Índia abaixo de 2%** (Rodrigo, `~/workspace/referencias/BRIEF-historia-003-v2.md`, 04/11/2026; janela não informada). Os dois seguem o mesmo padrão (lugar panorâmico + nome gigante + datas). "O padrão precisa mudar."
- Nenhuma das 3 thumbs do 003 v1 "gera curiosidade de clique" (mesma fonte).
- Em teste: 4 conceitos novos no job `historia-003-v2` (`videos/003-ira/v2-amostras/thumbs/`). **Aprovado em 05/11: o conflito cara a cara (abaixo).**

## Padrão novo aprovado em 05/11/2026: CONFLITO CARA A CARA ("COROA × TURBANTE")
O Rodrigo gostou da pegada da thumb-3 da fase 1 (`videos/003-ira/v2-amostras/thumbs/thumb-3.jpg`). Template (003 v2, `videos/003-ira/v2-thumbs/compose_v2.py`):
- **Dois bonequinhos de cabeça redonda, grandes (do peito para cima), testa contra testa, com emoção forte (raiva, boca aberta gritando)**, um de cada lado; os dois no mesmo traço (no 1º teste o clérigo saía semi-realista).
- **Raio amarelo** entre os rostos; fundo dividido (o mundo de cada lado: azulejos × multidão, penhasco × escudos romanos, poços de petróleo × tanques).
- **Datas em pílula amarela** (Open Sans 800) no topo, ao centro: a lacuna ("1891 · 1979", "260 d.C.", "1953").
- **Duas palavras grandes embaixo** em Libre Caslon 700 sobre degradê escuro: a 1ª em ouro (#F7C21B), "×" branco, a 2ª em branco. O título dá o "história INTEIRA"; a thumb vende o conflito.
- Base: nano-banana-2.1/edit + refs do canal, 2 tomadas por conceito (US$ 0,046 cada), texto composto em PIL (fontes em `videos/003-ira/v2-amostras/thumbs/base/fonts/`).
- Irã v2: 1 COROA × TURBANTE (principal), 2 PÉRSIA × ROMA (Shapur × Valeriano), 3 PETRÓLEO × CIA (Mossadegh × agente). **Hipótese** até o CTR do "Testar e comparar": registre aqui o vencedor e o CTR de cada uma.
- Para o próximo país, escolha 3 pares de conflito do próprio roteiro (personagem × personagem, ou povo × povo).
- China 004 (05/11/2026): 1 **IMPERADOR × MORTE** "210 a.C." (Qin com as pílulas × a morte encapuzada, exército de barro × rios de mercúrio; principal, casa com o hook), 2 **DRAGÃO × CANHONEIRA** "1839" (oficial Qing × capitão britânico com o baú de ópio), 3 **IMPERADOR × MONGOL** "1279". As 6 bases saíram boas na 1ª tomada (US$ 0,046 cada); palavra longa (CANHONEIRA) cabe com a fonte a 86 px, legível a 320 px. **Hipótese** até o "Testar e comparar".

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
