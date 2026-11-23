# ETAPA 1 · historia-ptbr/017-cuba · 22/11/2026 (Opus, lote noturno)
`youtube.videos` id 61 · `biblia_versao='v2'` · status `roteiro` · título no banco = T1.

## O que foi feito
1. **Pesquisa + ângulo** (`BRIEF.md`, `ANGULO.md`): manada de **15 transcrições** via WARP (tema + recorte vizinho "açúcar/dependência"), incluindo o **History in Minutes "The ENTIRE History of Cuba in 19 Minutes"** (`Oo-NkDx-8eA`, recém-publicado). O ângulo da pauta ("por que Cuba sempre dependeu de um único comprador?") **já é a tese** do vídeo pt Riqueza e Ruína (`ALpd58SX-Mc`, 15/11/2026: "trocou um freguês por outro… uma mesada por outra"): mantida a pergunta, trocada a resposta → **"quem compra, manda": o preço garantido e a cláusula** (cada comprador garantiu o preço cobrando uma cláusula: estanco 1717, tarifa 1894, reciprocidade+Platt 1902, cota 1934, alinhamento 1960, volume 1964, rublo de convênio 1972, médicos 2000).
2. **Embalagem** (`EMBALAGEM.md`, `CRIVO.md`): aprovada na **r3**. r1 reprovou T2 ("padrinho" = sugar daddy/mesada da manada; presente absoluto) e Thumb C (ilha diagonal + bandeirinha + colher = composição da thumb do Lucas, 22×, e "exploração"); r2 reprovou o novo T2 ("Por que Cuba trocou os EUA pela URSS?" = um episódio só, iniciativa errada). Pares registrados em `youtube.embalagem_variantes`.
3. **Roteiro** (`roteiro.py` → `SCRIPT.md`, `blocos.json`, `SOURCES.md`): 63 blocos, **2.159 palavras**, ~17:15 estimados (roteiro.py) / ~16:35 a 130 ppm. Checklist v2 **APROVADO** (abaixo).
4. **Detector + crivo de ângulo**: `SIMILARIDADE.md` **2/100** (máx. HistoDarias 2, BBC 2, Riqueza e Ruína 1); `CRIVO-ANGULO.md` **APROVADO na r3** (3º parecer). r1 reprovou: as respostas no meio do vídeo (padaria, "o preço alto era a corda", "prometeu sair do açúcar") repetiam a tese do Riqueza e Ruína, e o trecho 1762 → Arango (1792) repetia o HistoDarias. r2 reprovou: N020 quase literal do Riqueza e Ruína (fazendeiros ocupando o lugar de São Domingos), fecho "escolhia de quem" (tese do Riqueza e Ruína) e o fato de 2002 sem fonte própria. Cota própria: 13 de 20 = 65% (meta 40%).
5. **Storyboard** (`cenas.json`, `STORYBOARD.md`, `storyboard.json`): **325 planos**, **206 imagens** novas, plano médio 3,18 s, 22 cortes no 1º minuto, reuso 36,6% (45,6% depois de 3:00; 0% antes), 19 rótulos, **0 avisos** da validação.

## Promessa e onde é paga (tempos estimados do storyboard)
- Pergunta central: "Por que Cuba sempre dependeu de um país só para comprar o que ela produz?" (N004, **0:46–0:55**).
- "Setecentas mil toneladas ficam **sem comprador**" (Thumb A) em **N002 ~0:18–0:23**; Moscou se oferece para comprar as mesmas (a troca do T2) **~0:24–0:29**; "quase **cinco vezes o preço** do mercado" (Thumb B) **N003 ~0:30–0:35**; "nenhum comprador cobrou só em dinheiro… Espanha, EUA, soviéticos, Venezuela" (T1/T2/T3) **~0:35–0:46**.
- T2 ("o que cobravam?") pago capítulo a capítulo: estanco (cap. 2), crédito/dívida (cap. 3), tarifa (cap. 4), Platt + 20% (cap. 5), cota (cap. 6), cota como arma (cap. 7, **~10:48**, paga o "guarde"), volume fixo (cap. 8), rublo de convênio (cap. 9, **~13:05** desenvolve o "quase cinco vezes"), médicos (cap. 10). Fecho (~16:29): "não mudaram de dono, mudaram de cláusula".
- Thumb C (ilha amarrada) aparece no storyboard como `cuba_tied_rope` (N004 e N060/N063).

## Checklist v2 (saída do `checklist_roteiro_v2.py`, tempos a 130 ppm)
```
Checklist roteiro v2 · 017-cuba · bíblia v2 · tempos: estimado a 130 ppm (sem voz)
Pergunta central (declarada no SCRIPT/BRIEF): Por que Cuba sempre dependeu de um país só para comprar o que ela produz?
 nº status   item                                                 valor                                  alvo
  1 PASSA    Pergunta central declarada ("Pergunta central:" no S declarada no SCRIPT/BRIEF              declarada
  1 PASSA    Pergunta central (como pergunta) até ~0:50           0:44 em N004                           ≤ 0:50
  2 PASSA    Pergunta volta em voz alta (fora do hook)            3× ['N042', 'N049', 'N061']            ≥ 3 (fecho responde)
  3 PASSA    Conectivos de virada /100 palavras                   1.76 (38)                              ≥ 1,5
  3 PASSA    Capítulo fecha com o problema da próxima era         10/10                                  todos
  3 PASSA    Nenhum capítulo abre com sucessão seca               0 []                                   0
  5 ok       Capítulo abrindo com data (ficha, não cena)          0 []                                   ≤ 2
  4 PASSA    "Você/imagine" /100 palavras                         1.11 (24)                              ≥ 1,0
  4 PASSA    Capítulo com ponte para o espectador                 10/10                                  todos
  7 PASSA    "Guarde isso" no vídeo                               1                                      ≤ 2
  8 PASSA    Hook até o capítulo 1                                1:07                                   0:60–1:15
  8 PASSA    Promessa em lista                                    nenhuma                                ≤ 2
  9 ok       Falas curtas de personagem                           2                                      1–2+
 10 ok       Ritmo (palavras/min com pausas)                      sem voz ainda                          140–145 (Hipótese)
 10 AVISO    Palavras por frase (média)                           12.6                                   ≤ 12,5; 5–8 nas viradas
 10 ok       Palavras no roteiro                                  2159                                   ~2.250 p/ 16 min a 140 ppm
 11 PASSA    Fecho (do início do Fecho ao fim)                    0:43                                   ≤ 0:45
  5 MANUAL   1 cena (lugar, pessoa, momento) por capítulo antes d ler                                    todos
  6 MANUAL   Humor seco a cada ~40–60 s, sobre o fato             ler                                    ~15–20 tiradas
  0 MANUAL   Teste da troca + fio condutor ≥ 3 capítulos + loops  ler                                    sim

Resultado: APROVADO
```
Manuais: cena antes dos fatos em todo capítulo (Bayamo 1604; Jesús del Monte 1717; 600 navios 1805; Martí em Washington 1891; tratado de 1902; Roosevelt 9/05/1934; Mikoyan 1960; Moscou 1964; analistas da CIA c. 1983; Caracas 30/10/2000) · humor seco ~1/min ("Tente ganhar fama literária com um sequestro", "vale do mercadinho em Paris", "tente explicar essa vitória a um usineiro de Camagüey"…) · teste da troca ok (cada capítulo nasce da cláusula do anterior) · fio "cláusula" em 7 capítulos · loops pagos (700 mil t → cap. 7 e fecho; "cinco vezes" → cap. 9). Aviso: média de 12,6 palavras/frase (limite 12,5).

## Fio condutor e loops
- Fio: **o comprador e a cláusula** (preço garantido → condição → crise → próximo comprador).
- "Guarde" único: as 700 mil toneladas (hook → N043 → N062).
- Peças da resposta: 1 (N049) o preço garantido vinha amarrado a uma quantidade; 2 (N053) o comprador pagava bem, mas na moeda dele. Fecho: só um gigante garante preço; cada cláusula só deixava uma saída: outro gigante.

## Custo
- Etapa 1: US$ 0 pago (detector: tradução em cache, US$ 0,000).
- Previsto etapa 2: imagens Codex US$ 0 (fallback fal no pior caso 206 × US$ 0,046 ≈ US$ 9,5 → acima do teto de US$ 8: se o Codex cair, gerar no fal só o que faltar e reaproveitar mais); voz drama-3 ~US$ 1; thumbs 3 bases; render Runpod ~US$ 0,2.

## Pendências / avisos para a etapa 2
- Duração: 2.159 palavras ≈ 16:30–17:15 com o ritmo real (016: 2.212 → 17:22). Se passar de 17:30, cortar N015/N019/N044 (fatos de passagem).
- 2026 (N059): a captura de Maduro e o fim do petróleo venezuelano vêm de CRS IN12650 + S&P Global; manter a frase neutra como está.
- Pronúncias no `FALA` do `roteiro.py` (Bayamo, Girón, Jesús del Monte, Camagüey, Mikoyan, Khrushchev, Cienfuegos, Atkins, Eisenhower, Roosevelt, Chávez, Batista): conferir no Whisper.
- Prompts: cenário ancorado em 100% (CUB/ORI/HAV/HAV20/ING/WAS/NYB/MAD/MOS/CAR/SEA) + `NAO_EG` + `SEMBAND` (nenhuma bandeira, nem cubana nem soviética); palmeira só a palma real cubana. Conferir prancha antes do pré-QA (vazamento das refs do Egito, visual.md 011/013).
- Mapas com rótulo no código: `map_florida_cuba` ("150 KM"), `map_guantanamo` ("GUANTÁNAMO"); `map_cuba_caribbean` sem rótulo.
