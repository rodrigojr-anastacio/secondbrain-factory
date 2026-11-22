# ETAPA 1 PRONTA · historia-ptbr/016-espanha · 21/11/2026 23:25
`youtube.videos` id 59 · `CRIVO.md` APROVADO (embalagem, **r3**) · `CRIVO-ANGULO.md` APROVADO (**r1**) · `SIMILARIDADE.md` **1/100** (só contra 2 transcrições locais; ver pendência 1).

## Ângulo (1 linha)
A costura: o casamento de 1469 junta coroas e não países; o império de Castela adia a costura, a costura à força (1624–1640, 1707–1717) deixa sempre alguém de fora, até a costura assinada de 1978.

## Os 3 pares aprovados (A = T1, B = T2, C = T3; registrados em `youtube.embalagem_variantes`)
| par | título | padrão do título | thumb (padrão) | texto da thumb |
|---|---|---|---|---|
| A | A Espanha juntou meio mundo. Por que não juntava a si mesma? | afirmação estranha + pergunta | `rosto-emocao`: rei do séc. XVI de manto vermelho (sem rufo), rosto irritado-perplexo, segurando uma pilha alta e torta de 5 coroas diferentes; fundo ocre liso | "REI DAS ESPANHAS" ("ESPANHAS" em ouro) |
| B | Por que a Espanha cobrava ALFÂNDEGA de si mesma até 1841? | pergunta de transformação + número | `conflito-xvy`: fiscal de alfândega castelhano × mercador navarro (boina **escura**, capa com correntes de Navarra), peito para cima, testa contra testa, cancela listrada no meio, fundo em 2 cores lisas | "CASTELA × NAVARRA" |
| C | Espanha: o império que ainda não era um país | [Lugar]: o X que contradiz o esperado | `objeto-simbolo`: coroa partida ao meio e costurada com linha grossa (metade castelo, metade listras), um ponto arrebentando; fundo creme claro, objeto à direita | pílula "1469" |
Prompts-base e referências em `EMBALAGEM.md` (seções Thumb A/B/C). Observações do crivo r3 para a arte: pilha de coroas alta e torta, rosto ≥ 35% da altura e mãos nos lados da pilha (não repetir o gesto do 014-A); boina escura no navarro (vermelha = símbolo carlista); a coroa costurada de C não pode parecer nenhuma coroa da pilha de A.

## Promessa e onde o roteiro a paga
"Por que a Espanha juntou meio mundo antes de conseguir juntar a si mesma?" — N003 (~0:25: coroas × países, lei/**alfândega**/moeda), N004 (~0:41: pergunta), N005 (~0:50: "rei das Espanhas, no plural, uma pilha de coroas" + "última alfândega de dentro só caiu em 1841"). T2: N018 (~3:45, cena da alfândega Castela–Aragão), N049 (~11:19, 1717), N057–N058 (~13:31, o Ebro, 1841). T3: N035 (~7:48, "o império que ainda não era um país"). Fecho N068–N070 responde e volta ao plural. Tempos estimados (126 ppm); conferir na `legendas.srt` (skill `qa`).

## O que a etapa 2 precisa saber
- **3 thumbs, uma por conceito** (A/B/C acima), texto no código; A/B/C = T1/T2/T3 no `youtube.txt`.
- Roteiro e storyboard prontos no `roteiro.py` (`blocos.json` com grafia fonética em `texto` e correta em `tela`; `cenas.json` com 206 imagens; 0 avisos). Setup `src/` e `tools/` copiado do 014 (ajustar `build.py`/`Video.jsx` ao 016: trilha em modo frígio/andaluz, paleta do canal).
- **Antes da voz (pendência 1, obrigatória):** tentar transcrever a manada (`tools/manada.py transcrever ref --ids 90H1JvKT5tI,zlssmpPrJkA,KFe9zlQNuSs,1PAEeroCy9w,rjhIzemLdos,1xmLTdlTLTE,Gwm7eF4NG0A`). Se o YouTube ainda bloquear ("not a bot"), seguir e registrar no ETAPA2 (o crivo de ângulo aprovou com o conferível). Se transcrever: rodar `tools/similaridade_roteiro.py canais/historia-ptbr/videos/016-espanha --video 59`; nota < 18 = segue; 18–29 = registrar os trechos no ETAPA2 e seguir só se forem fatos obrigatórios ditos com palavras nossas; ≥ 30 = parar com `BLOQUEIO.md` ("ângulo") antes de gastar.
- Cartões de data de N055 e N063: mover para o plano da cena datada (ver `ETAPA1.md`).
- Visual: refs do Egito vazam (faraó, turbante, palmeira): os prompts já levam `NAO_EG`; conferir a prancha inteira antes do pré-QA. Bandeira vermelha-amarela atual não pode aparecer antes de 1785 (nem estelada/republicana/franquista).

## Pendências
1. Manada sem transcrição nesta noite (YouTube "not a bot" no WARP de 22:00 a 23:20) — reconferir conforme acima.
2. Humor ~12 tiradas (meta 15–20, Hipótese de dosagem).
