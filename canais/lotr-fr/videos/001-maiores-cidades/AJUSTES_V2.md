# AJUSTES V2 — vídeo das cidades (pedido do Rodrigo, via manager)

O vídeo `out/cidades-fr.mp4` (8:18) foi aprovado no geral. Roteiro, narração Kokoro, legendas, mapa e thumbnail ficam como estão. Corrigir apenas o que está abaixo e renderizar de novo.

## 1. Imagens fiéis à Terra-média, mantendo o estilo visual
O Rodrigo **gostou do estilo** das imagens atuais: pintura a óleo, paisagem romântica clássica, luz dramática (Thomas Cole, Claude Lorrain, Bierstadt…). Mantenha esse padrão.
O problema é **fidelidade**. Toda imagem precisa representar de forma crível o lugar ou o momento que a narração descreve. Nada de lugares reais reconhecíveis.
- Exemplo do erro: "Minas Tirith" foi ilustrada com o **Mont-Saint-Michel** (William Stanley Haseltine). Isso é inaceitável, ainda mais para o público francês.
- Revise **todas** as cenas (veja `public/img` e o storyboard) e troque toda imagem que mostre um lugar real reconhecível ou que contradiga a descrição de Tolkien. Exemplos: Minas Tirith (cidade branca de sete níveis encostada no Mindolluin, com o esporão de pedra), Gondolin (cidade branca num vale cercado de montanhas), Khazad-dûm (salões subterrâneos com colunas), Osgiliath (cidade sobre o Anduin, com pontes), Nargothrond (fortaleza escavada na rocha junto a um rio), Menegroth (cavernas-palácio na floresta), Umbar, Pelargir, Armenelos.
- **Fontes, em ordem de preferência:**
  1. Ilustrações da Terra-média em estilo pictórico (pintura) encontradas no Google, com o artista creditado no canto e em `description.txt`. O Rodrigo autorizou.
  2. Se não achar uma boa, gerar a imagem (ferramenta de geração de imagem) em estilo de pintura a óleo romântica do século XIX, coerente com as demais, e creditar como "illustration générée".
- Pinturas genéricas de domínio público continuam valendo para cenas de clima ou de transição (mar, tempestade, ruínas sem identidade). Na cena com o nome de uma cidade, a imagem tem que ser daquela cidade.
- Proibido: frames de filme ou série.

## 2. Placar duplicado nas cenas de mapa
Nas cenas de mapa (por exemplo, 3:00 Gondolin e 7:00 Armenelos) aparecem dois quadros empilhados: "LA COURONNE · Gondolin" e, logo abaixo, outro quadro "Gondolin / Estimation". Deixe só o quadro **LA COURONNE**.

## 3. Áudio
Fica como está; o Rodrigo aprovou. Não regere a narração.

## QA antes de entregar
- Contact sheet com uma amostra de **cada cena que nomeia uma cidade**: confirme que a imagem bate com a cidade e que não é um lugar real reconhecível.
- Confirme que não sobrou nenhum placar duplicado.
- Duração continua por volta de 8:18.
- Saídas: sobrescreva `out/cidades-fr.mp4` e `out/cidades-fr-telegram.mp4`; atualize `description.txt` (créditos) e `QA.md`.
