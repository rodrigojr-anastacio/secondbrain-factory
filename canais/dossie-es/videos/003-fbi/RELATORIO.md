# RELATÓRIO · dossie-es/003 · "TODA la historia del FBI en 13 minutos" (youtube.videos id 9)

Job: `~/workspace/referencias/BRIEF-dossie-003.md` (05/11/2026, ~17h40–19h10). Orquestrador: Claude Code (Opus) nesta sessão, que fez a pesquisa, o roteiro e o storyboard. A 2ª leitura nativa foi feita por um subagente Sonnet. Voz, imagens, build e render são comandos determinísticos, todos em primeiro plano. Nenhum outro job rodou ao mesmo tempo. Nada foi publicado nem enviado ao Telegram.

## Entrega (`entrega/` + Google Drive `Youtube/Dossier en Minutos/003-fbi/`)
- `video.mp4`: **13:17**, 1080p30, −15,2 LUFS;
- `thumb-A.jpg` (o diretor com a pasta), `thumb-B.jpg` (o ladrão de Media, "LE ROBARON SUS SECRETOS") e `thumb-C.jpg` (Hoover no fichário, "48 AÑOS DE SECRETOS");
- `pacote.md`: título, título B, descrição com fontes e link da CIA, 15 capítulos, tags, checklist e tradução pt-BR;
- `legendas.srt` (es).
- Também: o 001 (CIA) foi marcado como publicado em `youtube.videos` (id 7, `Qs-TusYCr-o`, 04/11, "La historia COMPLETA de la CIA en 12 minutos") e no `backlog.md`.

QA aprovado (`QA.md`): 0 telas pretas, Whisper com 97,6% de média, hook de 31 s, 183 imagens + 3 thumbs e 2 mapas com pinos no código.

## O roteiro
- **Hook:** o arrombamento do escritório do FBI em Media (Pensilvânia), na noite de Ali × Frazier (08/03/1971). Os concorrentes em en abrem com a morte de Hoover, Dillinger ou o 11-S, e ninguém em es usa o molde. O hook é pago no expediente 10 ("Las Maletas": COINTELPRO, "un agente detrás de cada buzón"), e o cierre volta à fechadura: o caso prescreve sem nenhuma prisão, e os ladrões se revelam em 2014.
- **13 expedientes:** El Memorando, El Fichero, El Director, El Cine, El Espejo, El Servicio, La Reunión, El Programa, La Carta, Las Maletas, El Garaje, La Casa e El Parque, mais "Cierre. La Cerradura".
- **Ângulo América Latina:**
  - o Servicio de Inteligencia Especial do FBI (1940–46) no México, no Brasil, na Argentina e no Chile, que passa à CIA em 1947 (ponte para o 001);
  - as "carpetas" de Porto Rico, com a frase de Louis Freeh em 2000;
  - o caso Camarena em Guadalajara (1985);
  - o alias "Ramón García" do Hanssen.
- **Trinca CIA → Mossad → FBI:** o fecho e a descrição puxam para o vídeo da CIA (`Qs-TusYCr-o`). Sugestão no pacote: tela final com o vídeo da CIA.
- **Neutralidade:** COINTELPRO "según una comisión del Senado"; a carta a King confirmada pela comissão Church; Camarena "según los fiscales"; o laboratório criticado pelo inspetor-geral (1997); o valor pago pelo dossiê do Hanssen "según la prensa". O recorte termina em 2001, com uma única frase atual: o 11-S muda a missão.
- **Números:** 1.830 palavras e 80 blocos. Estimado em 12:57 (WPS 2,38) e medido em 13:17 (+2,6%).

## Custo (financas.consumo, ref_id 9)
| Etapa | Itens | US$ |
|---|---|---|
| Voz completa (80 blocos, por frase) | Fish s2.1-pro (o crédito caiu US$ 0,152, preço do s2.1-pro) | 0,16 |
| Lote (183 cenas + 3 thumbs) | fal nano-banana | 7,36 |
| 8 refeitas | fal | 0,32 |
| **Total direto** | | **7,84**, teto de US$ 10 |
- Não fiz amostra de voz separada: a voz inteira custa US$ 0,16, e o Whisper por bloco faz a checagem.
- Saldo do fal depois do job: ~US$ 74,3; do Fish: ~US$ 48,2.

## Correções de fatos (antes da voz; detalhes em `SOURCES.md`)
1. **Hanssen:** em 1979 ele vendia ao **GRU** (inteligência militar soviética), não à KGB, que só vem em 1985. Dos US$ 1,4 milhão, parte foi depósito em Moscou.
2. **Carta a King:** o pacote foi enviado em novembro de 1964, e Coretta o abriu "semanas depois". "Solo te queda una cosa por hacer" não é o fim da carta: o texto agora diz "dice, entre otras cosas".
3. **COINTELPRO:** Hoover encerrou o programa em abril de 1971, **antes** do processo do jornalista. A ordem do texto foi corrigida.
4. **Cronologia do Hanssen e do 11-S:** a perpétua é de 2002, e os 7 meses vão da prisão até o 11-S.
5. **Atribuições acrescentadas:** "según el FBI" (a maior rede de espiões), "según una comisión del Senado" (o objetivo do COINTELPRO), a autorização de Robert Kennedy para as escutas, Freeh "hablará de…" (era fala dele, não uma admissão formal) e "uno de los hombres más vigilados" (em vez de superlativo).
6. **Números incertos:** agentes do SIS (340–700) viraram "cientos"; os presos em Apalachin, "más de cincuenta"; os ladrões revelados em 2014 (4, 5 ou 7, conforme a fonte), "varios".

## Revisão do espanhol
Um subagente Sonnet leu como editor mexicano e depois espanhol e deu nota 8,5/10. Apliquei ~30 mudanças, entre elas:
- "lo ha vendido" → "lo delató";
- "espiando contra" → "espiando a";
- "quedarse con el mundo" → "hacer espionaje en todo el mundo";
- "por un tiempo" → "de forma interina";
- "control" → "bloquean el camino";
- "puente" → "pasarela";
- "Anna Sage" (grafia certa);
- frases longas divididas.

## Falhas da esteira (o que quebrou, o improviso, a correção sugerida)
1. **Moldura em 26% de novo** (48 de 186), e apareceu um 3º tipo: **margem branca só nas laterais/embaixo**, que o `recorta_moldura.py` não pega (4 imagens).
   - Fiz o `tools/recorta_branco.py`.
   - Correção: juntar os três recortes num só e chamá-lo dentro do `img_fal.py`.
2. **`recorta_moldura.py` reusa o original velho.** Se a imagem é **refeita**, ele recorta a cópia antiga de `imagens-orig/` (`if not o.exists()`) e sobrescreve a nova. Isso custou a regeração do I014 (US$ 0,04).
   - Correção: comparar o mtime ou apagar `imagens-orig/<id>.jpg` sempre que regenerar.
3. **Letreiro inventado em cena nomeada:** o cinema Biograph saiu como "ROXY PALACE".
   - Prompt de lugar real com fachada deve pedir "blank marquee, blank signs".
4. **`qa.sh` conta poucos cortes no 1º minuto** (13 com scene > 0,3) com planos escuros parecidos (o hook noturno). O número real do storyboard é 19,5/min. O detector subestima: não é defeito do vídeo.
5. **Custo de Claude do orquestrador invisível** (mesma falha do 001/002): esta sessão não roda via `claude_run`.

## Pendências para o Rodrigo
- **Ouvir** (timestamps conferidos na `legendas.srt`):
  - 0:08 "Muhammad Ali";
  - 0:23 "del FBI" (confirmar se sai "efe-be-i");
  - 3:57 "Sebold";
  - 4:17 "Fritz Duquesne";
  - 5:45 "Apalachin";
  - 6:35 "COINTELPRO";
  - 11:35 "Hanssen".
- Publicar é decisão sua. O checklist está no `pacote.md` (es, sintético = sim, não é para crianças, 3 thumbs em "Probar y comparar", legenda es, tela final com a CIA).
