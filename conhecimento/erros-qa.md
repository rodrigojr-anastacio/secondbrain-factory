# Base de erros pegos no QA (e como não repetir)

> **Regras gerais. Regra de canal está em `canais/<slug>/biblia/` e sempre prevalece.** Esta base junta todo erro que o QA, o pré-QA ou o Rodrigo pegaram, com causa e prevenção. Pedido do Rodrigo (10/11/2026): "uma base de coisas que vamos pegando com o tempo para não errar mais nelas". Detalhes longos de ferramenta/custo ficam em [`anti-padroes.md`](anti-padroes.md); aqui há o resumo e o link.

**Como atualizar (obrigatório):** toda reprovação ou correção de QA vira (a) a seção "Reprovações" no `QA.md` do vídeo e (b) uma entrada aqui, mais recente no topo. Sem isso o QA não está concluído ([`skills/qa/SKILL.md`](../skills/qa/SKILL.md)). Sempre com data e fonte; sem fonte = **Hipótese**.

Modelo de entrada:
```
### AAAA-MM-DD · canal/vídeo · título curto
- **Errado:** … · **Causa raiz:** … · **Detectado por:** QA pós-render | pré-QA | Rodrigo | QA pré-render
- **Custo do erro:** … · **Como evitar:** … · **Regra/checagem criada:** link
- Fonte: …
```

Última revisão: 2026-11-10.

---

## Checklist de pré-render (destilado das entradas abaixo)

Antes de qualquer render > 10 min: stills a cada ~10 s e em toda troca de cena/estilo, em grade ([`montagem-render`](../skills/montagem-render/SKILL.md) passo 4). Em cada quadro, olhe:

1. **Fundo e bordas:** faixa chapada, listra, buraco ou emenda atrás de mapa/globo/relevo; nada de z-fighting (listras no mar); fundo igual em todas as trocas de estilo.
2. **Moldura / margem / faixa preta** nas imagens de IA (detector de bordas + olho); medalhão ou recorte que cortou rosto.
3. **Texto inventado:** letreiros, placas, mapas, calendários, jornais, pergaminhos (IA escreve letra falsa; rótulo vai no código).
4. **Anacronismo e lugar errado:** bandeiras, uniformes, minaretes, caligrafia árabe, cocares, lugar real no lugar de fictício, mapa com país/região errados.
5. **Sobreposição de elementos de tela:** rótulo × placa de capítulo, HUD duplicado, caixa por cima de termômetro/mostrador, objeto atrás do diorama, elemento fora do quadro.
6. **Glifos:** ícones/símbolos (✓ ✗ ▶ ⚠) que a fonte não tem viram "tofu"; placeholders ("10H3X") em legenda.
7. **Valores animados que começam errados** (régua "0,00", contador antes de crescer) e dados que vazam para outro elemento.
8. **Imagem preta** (filtro do fal devolve sem erro): luminância média < 15.
9. **Voz** (antes do render, por bloco): frase faltando, palavra trocada, pergunta sem entonação, nomes estrangeiros testados antes.
10. **Mudou código/estilo no meio?** Refaça a varredura inteira, não só o trecho mexido.

---

## Entradas (mais recente primeiro)

### 2026-11-10 · Em Relevo 002 (El Niño) v2 · fundo atrás do mapa reprovou o render inteiro
- **Errado:** render do vídeo inteiro reprovado no QA: faixa escura chapada no corte do Pacífico e listras verticais sobre o globo; 2ª rodada do bloco 19 em diante. Quadros em `pesquisa/canal-clima-2026-11/longo-02/qa/v2/` (`f091.jpg`, `f127.jpg`, `cmp1.jpg`).
- **Causa raiz:** nas cenas de câmera baixa (diorama, globo, régua) o 3D não cobre o quadro inteiro e aparecia a cor de fundo do canvas `#B9A47F`; no estilo v1 ela era igual ao papel e não se via, no v2 (navy/satélite) virou faixa bege. Correção: fundo do canvas acompanha a paleta do estilo. 48 blocos re-renderizados (~2,3 h). Fonte: `pesquisa/canal-clima-2026-11/longo-02/QA-visual-v2.md` (10/11). **Lição:** ao trocar estilo/paleta, conferir nos stills as cenas com câmera baixa/inclinada, onde aparece o fundo do canvas.
- **Detectado por:** QA pós-render (vídeo inteiro). **Custo do erro:** ~8 h de render descartadas (valor informado pelo Rodrigo, 10/11).
- **Como evitar:** pré-QA com stills a cada ~10 s e em toda troca de estilo teria pego em minutos. **Regra criada:** pré-QA obrigatório em [`montagem-render`](../skills/montagem-render/SKILL.md) e checklist acima (item 1 e 10).
- Fonte: pedido do Rodrigo e `referencias/BRIEF-base-erros-qa.md`, 10/11/2026; `pesquisa/canal-clima-2026-11/longo-02/QA.md` (1ª rodada).

### 2026-11-10 · Em Relevo 002 · defeitos de tela pegos na conferência visual (corrigidos antes do render final)
- **Errado:** relevo do Peru alto demais; listras no mar do Pacífico (z-fighting); diorama baixo; setas de Walker atrás do diorama; termômetro e mostrador por cima da caixa de perguntas; data do relevo vazando para a régua; Sul fora do quadro no mapa de previsão; focos em grade regular; caixa compacta poluindo a tela. Régua de montanhas mostrando "0,00" no 1º segundo (pendência).
- **Causa raiz:** cena 3D nova sem varredura antes; camadas sobrepostas sem ordem de profundidade definida. **Detectado por:** QA, 4 baterias de stills (`work/grade1..5.jpg`). **Custo:** retrabalho de código; sem dinheiro (US$ 0).
- **Como evitar:** conferir grade de stills de toda cena 3D nova e de cada overlay (checklist 1, 5, 7). **Regra:** checklist acima.
- Fonte: `pesquisa/canal-clima-2026-11/longo-02/QA.md`, 10/11/2026.

### 2026-11-08 · Em Relevo 001 (tornados) v2 · voz v3 erra palavra e entonação
- **Errado:** ElevenLabs v3 trocou/inventou palavras ("Santa Augusto", "arrasou", "o Araciaba", "Exposure" no começo) e deixou perguntas sem entonação (b06, b36); hook ficou a 144 pal/min contra 173 no resto.
- **Causa raiz:** o v3 erra palavra às vezes e faz pausas dramáticas nas perguntas/tags. **Detectado por:** Whisper por bloco. **Custo:** retakes de 7 blocos (sem dinheiro além da assinatura).
- **Como evitar:** Whisper por bloco antes de montar e retake do bloco; testar nomes antes (checklist 9). Ritmo do hook: ajuste de `atempo`, sem gastar crédito, mas pede re-render, então decidir antes.
- Fonte: `pesquisa/canal-clima-2026-11/longo-01/QA-v2.md`.

### 2026-11-08 · Em Relevo 001 (tornados) · supercélula 3D e ícones "tofu"
- **Errado:** seta do jato atravessava a câmera e a nuvem estava no chão; ícones ✓ ✗ ▶ □ ⚠ ◀ saíram como "tofu" (a fonte não tem os glifos); legenda de um trecho com placeholder ("10H3X").
- **Causa raiz:** cena 3D sem conferência de câmera; fonte sem glifos; placeholder não substituído. **Detectado por:** conferência de stills antes do render (corrigidos antes). **Custo:** nenhum re-render.
- **Como evitar:** checklist 5 e 6; trocar símbolos por SVG. **Regra:** checklist acima.
- Fonte: `pesquisa/canal-clima-2026-11/longo-01/QA.md`.

### 2026-11-09 · historia-ptbr/006 Roma e 007 Rússia · anacronismos e texto inventado no nano-banana
- **Errado:** Constantinopla com minaretes otomanos (330 e antes de 1453); Santa Sofia em 988 com medalhões de caligrafia árabe; bandeira tricolor francesa e uniformes da Revolução Francesa no Palácio de Inverno de 1917; calendário com "OCTOBER/NOVEMBER"; mapa dos 15 países pintando a Ásia toda; gorro soviético no séc. XV; pergaminho com letras inventadas. 3 refeitas no 006, 7 no 007.
- **Causa raiz:** o modelo associa o lugar nomeado à aparência mais famosa; "no X" no prompt nem sempre vale; nomear "Hagia Sophia" puxa o visual otomano. **Detectado por:** lote-prova de 6 + pranchas do QA. **Custo:** ~US$ 0,05 por imagem refeita.
- **Como evitar:** descrever a época e o que há na cena em vez de nomear o lugar famoso ("Byzantine Christian cathedral… only Christian mosaics"); "only one big drawing… the rest blank" para pergaminho; checar bandeiras e uniformes por época (checklist 3 e 4). **Regra:** [`imagens`](../skills/imagens/SKILL.md) (lote-prova) e checklist; detalhes por canal na `biblia/visual.md`. Aprendizado de prompt por canal é da bíblia (Hipótese de que vale para os outros).
- Fonte: `canais/historia-ptbr/videos/006-roma/QA.md`, `007-russia/QA.md`, 09/11/2026.

### 2026-11-09 · historia-ptbr/006 e 007 · ritmo de fala abaixo do alvo
- **Errado:** 128 ppm (alvo 140–145, que é Hipótese) em 006 (17:27) e 007 (16:44); único item reprovado do checklist v2.
- **Causa raiz:** o drama-3 tem ~23% de silêncio dentro dos blocos; reduzir gaps entre blocos ganha ~1 s/min. **Detectado por:** `checklist_roteiro_v2.py` com tempos reais da legenda. **Custo:** nenhum (não bloqueia o 006/007; desvio anotado).
- **Como evitar:** orçar o texto pelo ritmo real (2.140 palavras → 16:47 no 007, contra 2.230 → 17:29 no 006); o caminho é texto mais curto, não gap. **Regra:** orçamento por ritmo real (já aplicado no 007).
- Fonte: `QA.md` 006 e 007, 09/11/2026.

### 2026-11-09 · dossie-es/005 KGB e 006 Masones · moldura e texto inventado (nano-banana)
- **Errado:** 25–29% das imagens com moldura/faixa (50 no KGB, 58 nos Masones); refeitas: pasta com "PROJECT NIGHTHAWK", avião com "BRITISH AIRWAYS", luz "ON AIR", calendário com dias em inglês, colagem em fundo bege (recorte 64%), moldura enorme (recorte < 60%).
- **Causa raiz:** ver entrada de 04/11 (moldura e `paper grain`). **Detectado por:** detector de moldura + grade de QA antes do render. **Custo:** ~US$ 0,05 por refeita; recorte perde 6–20% da borda.
- **Como evitar:** detector e recorte antes do render (checklist 2 e 3). Falsos positivos (cenas escuras, vinheta intencional) são restaurados à mão.
- Fonte: `canais/dossie-es/videos/005-kgb/QA.md`, `006-masones/QA.md`.

### 2026-11-07 · historia-ptbr/005 Brasil · bandeiras e letras anacrônicas
- **Errado:** 13 imagens refeitas: bandeira francesa tricolor em 1555–1567, bandeira republicana em 1870 e 1888, bandeiras no palanque, placas com letras inventadas ("Lisboa", "BANK", "ORANGE JUICE"), ideogramas falsos, padaria medieval em 1993, reis medievais em volta da moeda do real. Tupis com tiras de penas "de filme" no lote-prova (prompt corrigido para cabelo em cuia e pintura corporal).
- **Causa raiz:** o modelo preenche cena histórica com símbolo genérico. **Detectado por:** lote-prova + pranchas. **Custo:** 13 × ~US$ 0,046. **Como evitar:** checklist 3 e 4; lote-prova de 6 antes do lote. Também: "Ipanema" sumia colado em "jacaré" na voz, e teste de nomes antes do vídeo inteiro pegou.
- Fonte: `canais/historia-ptbr/videos/005-brasil/QA.md`.

### 2026-11-05 · dossie-es/003 FBI e 004 Cosa Nostra · letreiros e mapas errados
- **Errado:** 48 (FBI) e 44 (Cosa Nostra) com moldura/faixa; letreiros inventados ("ROXY PALACE", "LUIGI'S PIZZA"); manchete com letras falsas; mapa da Sicília com uma 2ª Sicília; texto espelhado numa porta; braçadeira vermelha num uniforme; margem branca lateral (nova ferramenta `tools/recorta_branco.py`); recorte que cortou a cabeça do Riina; mapas com pinos no lugar errado (México e Santiago corrigidos depois do 1º still).
- **Causa raiz:** moldura do nano-banana e texto inventado; pinos de mapa no código sem conferência. **Detectado por:** QA antes do render; mapas por grade e still. **Custo:** 8 e 4 refeitas. **Como evitar:** pinos de mapa conferidos com grade e em frame renderizado; checklist 2–4.
- Fonte: `canais/dossie-es/videos/003-fbi/QA.md`, `004-cosa-nostra/QA.md`.

### 2026-11-05 · dossie-es/002 Mossad · imagens refeitas e rótulo de mapa
- **Errado:** medalhão redondo (I155), moldura vertical que o recorte não salvava (I143), bandeira alemã inventada na cauda do MiG (thumb-C); "Egypt" escrito pelo modelo no mapa (coberto pelo rótulo EGIPTO).
- **Causa/detecção:** mesma família (moldura e texto), pego no QA antes do render. **Custo:** 3 refeitas. **Como evitar:** checklist 2 e 3.
- Fonte: `canais/dossie-es/videos/002-mossad/QA.md`.

### 2026-11-05 · historia-ptbr/004 China · anacronismos e fidelidade
- **Errado:** 8 refeitas: letras inventadas (I143, I171), coroa europeia (I148), bandeira tricolor errada em 1911 (I174), salão gótico (I208), astronautas e depois a Terra no céu do lado oculto da Lua (a Chang'e 6 é robótica), túmulo com cara de Egito (I215).
- **Causa raiz:** prompt sem época e sem fato técnico. **Detectado por:** pranchas do QA. **Como evitar:** checklist 3 e 4; para cena técnica, citar o fato no prompt.
- Fonte: `canais/historia-ptbr/videos/004-china/QA.md`.

### 2026-11-04 · dossie-es/001 CIA · moldura, filtro 422 e mapas
- **Errado:** moldura de papel em ~25% das imagens (43 de 171); HTTP 422 do filtro em cenas históricas comuns; mapa das Américas cortando o Chile; letras falsas no mapa do Irã ("CASPARIN SEA").
- **Causa raiz:** `paper grain texture` no estilo (Hipótese); filtro do fal em cenas de tanque/míssil/Torres Gêmeas. **Detectado por:** QA antes do render (uma rodada). **Custo:** recorte sem custo; 4 recusas sem cobrança. **Como evitar:** `checa_imagens.py`/`recorta_moldura.py`; reescrever "de longe e sem impacto"; rótulo de mapa no código.
- Detalhes: [`anti-padroes.md` §3c](anti-padroes.md). Fonte: `canais/dossie-es/videos/001-cia/QA.md`.

### 2026-11-04 · historia-ptbr/003 Irã · molde de roteiro errado (mistura de canais) e imagens fal
- **Errado:** roteiro v1 com capítulos-objeto do Archive; reprovado pelo Rodrigo ("falta conexão entre as partes"; "lendo corrido"). Depois, 1º lote do flux/dev em 1024×576 descartado e identidade do canal perdida ("sumiram os bonequinhos"). Rótulo "PLANALTO IRANIANO" encostava na placa "CAPÍTULO 1" (corrigido antes do render da v1).
- **Causa raiz:** regra de um canal gravada como geral; tamanho padrão baixo do fal; troca de motor sem amostra aprovada. **Detectado por:** Rodrigo (já renderizado). **Custo:** R$ 69,77 diretos da v1 + US$ 4,83 do lote descartado. **Como evitar:** bíblia por canal, amostra antes de trocar motor, 1536×864.
- Detalhes: [`anti-padroes.md` §8 e §3b](anti-padroes.md). **Regra:** bíblias e skill `qa` "segue a bíblia?". Fonte: `AVISO-ROTEIRO.md`, `QA-v1.md` 003.

### 2026-11-04 · historia-ptbr/002 Índia · imagens em dobro, saldo zerado, voz cortada, estereótipo
- **Errado:** 27 imagens geradas em dobro (2 processos na mesma pasta); saldo zerado deixou 2 imagens sem gerar (cobertas com reuso); o Fish cortou "Guarde essa chuva" depois de `[break]`; "Narendra Modi" mal pronunciado; curandeiro de Mehrgarh com cocar de penas (estereótipo, pendente); bandeira do Congresso com a roda de Ashoka.
- **Causa raiz:** sem trava por pasta; saldo não conferido; Fish corta frase curta após `[break]`. **Detectado por:** QA (voz regerada) e BLOQUEIO. **Custo:** ~US$ 1,1 extra. **Como evitar:** trava `.img.lock` (já implementada); conferir saldo; Whisper por bloco.
- Detalhes: [`anti-padroes.md` §3, §4](anti-padroes.md). Fonte: `canais/historia-ptbr/videos/002-india/BLOQUEIO.md`, `QA.md`.

### 2026-11-02 · historia-ptbr/001 Egito · imagens `low` e narração corrida
- **Errado:** 204 imagens em `low` borraram no Ken Burns; narração "robótica e atropelada" (pausa média 0,33 s); bandeiras atuais em cenas de 1922 e 1952.
- **Causa raiz:** economia de custo em imagem; `build.py` encadeando blocos com 0,16 s. **Detectado por:** Rodrigo e QA-v1. **Custo:** refazer 204 imagens (US$ 8,55 contra US$ 1,06 da leva `low`).
- **Como evitar:** `medium` no vídeo e `high` na thumb; pausas 0,35/0,9/1,5 s. Detalhes: [`anti-padroes.md` §1, §2](anti-padroes.md).
- Fonte: `QA-v1.md`, `ETAPA3.md` 001.

### 2026-11-01 · lotr-fr/001 Cidades · lugar real no lugar de fictício
- **Errado:** Minas Tirith ilustrada com o Mont-Saint-Michel ("inaceitável"); cidades desenhadas por código ficaram amadoras; placar duplicado no HUD (corrigido).
- **Causa raiz:** busca de imagem real sem checar o lugar. **Detectado por:** Rodrigo e `out/QA.md`. **Como evitar:** checklist 4; nada desenhado por código.
- Detalhes: [`anti-padroes.md` §5](anti-padroes.md). Fonte: `AJUSTES_V2.md` lotr-fr 001.

### Outros erros de processo (não são de QA de vídeo, ver anti-padroes)
- Job headless morto por tarefa de fundo (§7); render > 10 min por comando (última seção); YAML inválido no `canal.yaml`; saldo do fal divergente. Todos em [`anti-padroes.md`](anti-padroes.md).
