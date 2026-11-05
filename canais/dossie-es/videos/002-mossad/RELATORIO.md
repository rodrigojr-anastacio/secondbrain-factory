# RELATÓRIO · dossie-es/002 · "TODA la historia del Mossad en 14 minutos" (youtube.videos id 8)

Job: `~/workspace/referencias/BRIEF-dossie-002.md` (05/11/2026, 12:35–14:10), em paralelo com o `historia-003-v2-fase2` (Irã). Orquestrador: Claude Code (Opus) nesta sessão, que fez a pesquisa, o roteiro e o storyboard. A 2ª leitura nativa foi feita por um subagente Sonnet. Voz, imagens, build e render são comandos determinísticos, todos em primeiro plano. Nada foi publicado nem enviado ao Telegram. Nada foi tocado em `canais/historia-ptbr/`.

## Entrega (`entrega/`)
- `video.mp4`: **13:43**, 1080p30, −15,2 LUFS;
- `thumb-A.jpg` (o agente e o MiG), `thumb-B.jpg` ("LO ENCONTRÓ UN CIEGO") e `thumb-C.jpg` ("EL MIG ROBADO");
- `pacote.md`: título, título B, descrição com fontes, 15 capítulos, tags, checklist e tradução pt-BR;
- `legendas.srt` (es).
- **Google Drive: não enviado.** `tools/entregar_drive.py` não existia às 14:05. A entrega fica só na VPS.

QA aprovado (`QA.md`): 0 telas pretas, 26 cortes no 1º minuto e 20,4 por minuto, Whisper com 96,4% de média, 198/198 imagens e 4 mapas com pinos no código.

## O roteiro
- **Hook:** o MiG-21 iraquiano de Munir Redfa (16/08/1966), não Eichmann (o Atlas del Tiempo abre com ele). É pago no expediente 7 (metade do vídeo), e o cierre volta ao avião no museu de Hatzerim, com o número 007.
- **Eichmann contado de outro jeito:** pelo homem quase cego que o achou (Lothar Hermann, Coronel Suárez) e que o Mossad desacreditou. Expedientes "El Ciego" e "La Calle Garibaldi". Também a "thumb B".
- **Ângulo América Latina:** Argentina (Hermann, Eichmann, Resolução 138), Uruguai (Cukurs em Shangrilá), Brasil (São Paulo) e Buenos Aires como base da identidade de Eli Cohen.
- **13 expedientes:** El Instituto, El Ciego, La Calle Garibaldi, Las Cartas, La Casa, El Espía, El MiG, Múnich, El Camarero, El Ángel, El Hotel, La Mano e El Libro, mais "Cierre. El MiG".
- **Neutralidade:** as mortes atribuídas ao Mossad vêm com fonte ("según historiadores y periodistas", "el ataque se atribuye al Mossad", "su entorno siempre lo negó"). Lillehammer e a indenização sem admissão estão no texto. O recorte termina em 1990 e há uma única frase atual: "cumple setenta y seis años, en un Medio Oriente que sigue en conflicto".
- **Números:** 1.954 palavras e 85 blocos. Estimado em 13:50 (WPS 2,38, calibrado no 001) e medido em 13:43 (erro de 1%).

## Custo (financas.consumo, ref_id 8)
| Etapa | Itens | US$ |
|---|---|---|
| Amostra de pronúncia (10 blocos) | Fish | 0,02 |
| Voz completa (85 blocos, por frase, com cache da amostra) | Fish | 0,15 |
| Prova de estilo (4) | fal nano-banana | 0,16 |
| Lote (194) | fal nano-banana | 7,72 |
| 3 refeitas (I143, I155, thumb-C) | fal | 0,12 |
| **Total direto** | | **8,17**, teto de US$ 10 |
- Apaguei uma linha falsa (id 90, US$ 0,05) que o `img_fal.py` gravou numa chamada com **0 imagens geradas**: o custo dele veio da variação do saldo do fal, que incluía o outro job. Ver a falha 3.
- Saldo do fal depois do job: ~US$ 85.

## Tempo (relógio)
| Etapa | Tempo |
|---|---|
| Leitura (brief, mapa, bíblia, 001) | ~5 min |
| Checagem de fatos (12 buscas) | ~5 min |
| `roteiro.py` (texto + 280 planos) + revisão nativa (3 min do subagente) | ~12 min |
| Amostra de voz + Whisper | ~3 min |
| Voz completa + prova de imagem (em paralelo) | ~3 min |
| Lote de 194 imagens (paralelo 8, em ~4 min) + molduras + refeitas | ~12 min |
| Remotion (mapas, thumb, build) | ~8 min |
| **Espera do outro job** | **~22 min medidos (+ até 10 min não medidos)** |
| Render em 5 partes (337 + 316 + 321 + 326 s + parte final) + junção | ~23 min |
| QA, pacote, relatório, bíblia | ~10 min |
| **Total** | **≈ 1h35** |

### Teste de paralelismo (pedido do brief)
- O render do Irã ocupou a CPU de ~13:15 a 13:40. Fiquei 1.313 s (~22 min) em `tools/espera_render.sh` (log em `qa/espera.log`). Os 10 min anteriores (13:15–13:25) são inválidos: o 1º laço usava `pgrep -f "[r]emotion"`, que casava a linha do próprio bash (ela continha "npx remotion still"). Ele nunca terminaria e foi parado.
- Depois disso, os 5 renders não esperaram nada: o outro job não renderizou entre 13:41 e 14:04.
- Imagens e voz rodaram enquanto o Irã renderizava, sem trava (o fal é remoto; o Whisper concorreu pela CPU sem erro).
- **Correção:** usar `pgrep -f "^node .*remotion (render|still)"` e chamar a espera de um script (`tools/espera_render.sh`), nunca na mesma linha que o `npx remotion`. Isso vale para o `playbooks/produzir-video.md`/skill `montagem-render` (regra geral).

## Correções de fatos (antes da voz; detalhes em `SOURCES.md`)
1. "Cinco condenados" em Lillehammer não foi confirmado: o texto diz "varios son condenados" (6 detidos, penas de 1 a 5,5 anos).
2. A família de Redfa: as fontes divergem (levada a Israel × reassentada no Ocidente). O texto diz só "sacar a su familia de Irak", e o cierre não afirma onde nem quando ele morreu.
3. Eli Cohen era da Unidade 188 da inteligência **militar**, que depois passou ao Mossad: o texto diz isso em vez de "agente do Mossad". A data da prisão (18 ou 24/01/1965) virou "en enero".
4. A pista de Hermann: há várias versões de como o Mossad a descartou. O texto diz "según varias versiones".
5. Marwan: o aviso falava em "ao pôr do sol" e o ataque veio às 14h. O texto diz "horas antes de lo previsto"; a morte em 2007 aparece "en circunstancias que nunca se aclararon".
6. Sudão: os números variam de 6 a 7 mil (e até 28 mil, num escopo maior). O texto diz "miles", "según los relatos publicados".
7. Revisão nativa: as cartas-bomba ganharam "según varias fuentes" (Israel nunca as reconheceu), e Zuaiter ganhou "el ataque se atribuye al Mossad".

## Revisão do espanhol
Um subagente Sonnet leu como editor mexicano e depois espanhol e deu nota 8/10. Apliquei 36 mudanças:
- vírgulas antes de "y";
- concordância de tempos ("había construido", "había escrito");
- "cuelgan" → "ahorcan";
- "parlamento" → "Knéset";
- "Revolución de Mayo argentina", para não soar israelense;
- "Oriente Medio" → "Medio Oriente";
- atribuições em temas sensíveis;
- cortes de redundâncias (de 1.974 para 1.954 palavras).
Mantive "coche bomba" (termo-padrão em toda a imprensa hispânica) e "Déjalo en los comentarios" (igual ao 001).

## Falhas da esteira (o que quebrou, o improviso, a correção sugerida)
1. **A Hipótese do "paper grain" caiu.** Sem "subtle paper grain texture", 51 de 198 imagens (26%) saíram com moldura, contra 25% no 001. Agora há dois tipos: papel claro (30) e **faixa preta/letterbox** (21, novo).
   - O `checa_imagens.py` ganhou a detecção da faixa preta, e o `recorta_moldura.py` já recorta as duas.
   - Correção: levar os dois scripts para `tools/` da fábrica e chamá-los dentro do `img_fal.py`. Testar `aspect_ratio` nativo, se o endpoint do nano-banana aceitar, ou o `gpt-image-2` no fal, que venceu a bancada do historia-ptbr.
   - O `canal.yaml` fica **sem** a frase do grão: não fez diferença na moldura e a textura vem do traço.
2. **Laço de espera que casa a si mesmo**: ver "Teste de paralelismo".
3. **`img_fal.py` grava custo com 0 imagens geradas.** Quando todas as imagens "já existiam", ele gravou US$ 0,05 da variação do saldo, que era o gasto de outro job. Correção: não gravar nada quando `geradas == 0` e nunca usar a variação do saldo como custo com jobs em paralelo.
4. **`build.py` só linka `imagens/I*.jpg` em `public/img/`**, e o still das thumbs deu 404. Linkei as `thumb-*.jpg` à mão. Correção: incluir `thumb-*.jpg` no passo 3 do `build.py` do template.
5. **Hook de 40 s**, acima dos 25–35 s da bíblia. A estimativa do `roteiro.py` já mostrava isso e não cortei. Correção: o `roteiro.py` deve avisar quando o hook passar de 35 s.
6. **Custo de Claude do orquestrador invisível** (mesma falha do 001): esta sessão não roda via `claude_run`.

## Pendências para o Rodrigo
- **Ouvir** N012 (~1:45, "se apellida Eichmann") e N028 (~4:32, "Herberts Cukurs"): o Whisper ouviu "se ha pedido a Ekman" e "Cuckooers". Pode ser só a transcrição.
- Publicar é decisão sua. O checklist está no `pacote.md` (es, sintético = sim, não é para crianças, 3 thumbs em "Probar y comparar", legenda es), com a sugestão de moderar comentários (tema Israel/mundo árabe).
- Renomear o canal para **Dossier en Minutos** antes do 1º vídeo continua pendente (vale também para o 001).
- Subir a entrega no Drive quando o `tools/entregar_drive.py` existir: `Youtube/Dossier en Minutos/002-mossad/`.
