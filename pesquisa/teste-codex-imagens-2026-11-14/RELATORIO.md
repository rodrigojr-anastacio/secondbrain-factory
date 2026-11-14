# Teste: imagens pelo Codex (ChatGPT Plus) no lugar da fal, 14/11/2026

**Veredito:** adotar **só no historia-ptbr** (Codex primeiro, fal de reserva), depois de um lote-prova de 6 cenas num vídeo real. **dossie-es: ainda não**, falta uma rodada de ajuste de prompt. **Em Relevo: não adotar.**
Gasto pago: **US$ 0** (nada de fal nem de API). 30/30 imagens geradas, 0 recusas.

## Veredito por canal (comparativos ao lado, esquerda = atual, direita = Codex)
| Canal | Nota | Por quê |
|---|---|---|
| historia-ptbr (`comparativo-historia-ptbr.jpg`) | **Adota** | Bonequinhos de cabeça redonda em 10/10, mais fiéis à bíblia que o nano-banana (céu azul, cores chapadas, rostos de ponto; o nano às vezes sai sépia e com figuras de fundo meio realistas). Personagens nomeados (Napoleão, papa × imperador, governador romano) no molde "round-white-head". 0 letras, 0 molduras. Mapa (I109) bonito, mas a geografia é tão livre quanto a do nano. |
| dossie-es (`comparativo-dossie-es.jpg`) | **Ainda não** | Tinta de graphic novel com rostos adultos ok e acabamento acima do nano, mas: (1) paleta mais quente e saturada que o "ardósia/oliva/sépia" da bíblia; (2) **inventa contexto que o prompt não pede**: o mapa "flat scan, completely blank" (I091) veio com conquistadores, astecas e navios; o carimbo "só a mão" (I013) ganhou 3 homens de terno dos anos 40; (3) **sangue**: o cirurgião (I007) veio com avental ensanguentado, maca com ferido e corpo na mesa ao fundo (política do YouTube). Precisa de prompt mais fechado ("only…, no people, muted palette, no blood") e nova amostra. |
| Em Relevo (`comparativo-em-relevo.jpg`) | **Não adota** | Os vídeos não usam imagem de IA (mapa 3D + satélite real + dados); o comparativo é contra o frame real do longo-04. O Codex faz bases lindas e sem texto, mas a **geografia é inventada** (o Ceará de b17 não tem o formato do Ceará; enchente "de União da Vitória" em b12 é uma cidade qualquer). Num canal de mapa com dados e fontes, isso é erro, não estilo. Serve no máximo como fundo de thumb. |

## Como automatizar (resposta 1)
- **Pré-requisito que faltava:** o Codex estava instalado só como binário solto; toda ferramenta falhava ("codex-code-mode-host not found"). Instalei o `codex-code-mode-host` oficial da mesma release (GitHub openai/codex `rust-v0.169.0`, musl x86_64) em `~/.local/bin/` (espaço do usuário, sem sudo). Para desfazer: apagar o arquivo.
- **Comando estável** (`codex_img.py`, protótipo): 1 imagem = 1 `codex exec --skip-git-repo-check -s read-only --json -C <pasta vazia> -` com o pedido "chame o image_gen uma vez, prompt literal". Sem `OPENAI_API_KEY` (o script zera a variável).
- **Onde grava:** `~/.codex/generated_images/<thread_id>/*.png` (o `thread_id` sai no evento `thread.started` do `--json`). O rollout `~/.codex/sessions/AAAA/MM/DD/rollout-*<thread_id>.jsonl` traz status, falha (recusa), prompt revisado e o uso da cota. O script converte para JPEG 1536×864 em `<saida>/<id>.jpg`.
- **Tamanho:** sempre **1672×941** (já é 16:9 e > 1536×864): só reescala, nada se perde.
- **Modelo de fato:** ferramenta interna `image_gen.imagegen`; o C2PA das imagens diz `softwareAgent: ChatGPT / gpt-image` (o mesmo gerador do ChatGPT; a versão exata não é exposta). O agente que a chama é o modelo padrão do Codex.
- **Refs de estilo:** o `image_gen` aceita `referenced_image_paths`; passei as 3 refs do `canal.yaml` do historia-ptbr + `ref_instrucao` (igual ao `img_fal.py`). Funcionou.
- **Prompt literal:** 30/30 com o prompt revisado idêntico ao enviado (a invenção de contexto vem do gerador, não do agente).
- **Tempo:** 28–77 s por imagem (mediana 45 s; ~11 s de geração, o resto é o agente). **Paralelo 3 funciona**: 9–10 imagens em 160–190 s → **~18 s por imagem efetiva**. 200 imagens ≈ 1 h com 3 processos (a fal faz em ~25 min).
- Cada chamada gasta ~34 mil tokens de entrada (88% em cache) e ~250 de saída do agente.

## Cota (resposta 3: não medida; só o que apareceu)
Depois de ~34 execuções (30 imagens + 4 testes), o rollout mostrou: **janela de 5 h em 6%**, **semanal em 1%** (`plan_type: plus`, sem créditos extras). Indicativo grosso (passos de 1%): ~5–6 imagens por 1% da janela de 5 h, ou seja, **algo como 500 imagens por janela**; a semanal não dá para estimar com 1%.
**Como medir de verdade (rodada noturna proposta):** rodar `codex_img.py --paralelo 3` com um lote de ~200 cenas de um vídeo que já existe, gravando depois de cada imagem o `used_percent` primário/secundário do rollout, até 1 janela de 5 h ou até `rate_limit_reached_type` aparecer. Resultado: imagens por janela e por semana. Testar também o modo "lote" (1 `codex exec` gerando 10 imagens), que deve gastar ~10× menos tokens do agente e talvez menos cota.

## Se adotar no historia-ptbr: como ficaria `skills/imagens` (não alterado; o Rodrigo aprova antes)
1. `canal.yaml`: `gerador: codex` com `reserva: fal` (nano-banana-2.1/edit + refs, como hoje).
2. Passo 1 da skill: `tools/img_codex.py` (o protótipo promovido, com trava por pasta e "pula o que existe", como hoje) com `--paralelo 3`; custo US$ 0 em `financas.consumo` (registrar a linha para o histórico, com nota "cota Plus").
3. Se aparecer limite (`rate_limit_reached_type` ou falha repetida), o mesmo processo cai para o `img_fal.py` nas cenas que faltam; o teto do BRIEF continua valendo para a reserva.
4. Lote-prova de 6 cenas antes de cada vídeo (já é regra do canal) e conferência das regras da bíblia (bandeira, letras, anacronismo); as do nano não foram testadas aqui no Codex.
Economia esperada só no historia-ptbr: ~US$ 9 por vídeo (≈ 200 × US$ 0,046), se a cota aguentar o volume.

## Arquivos
`codex_img.py` (gerador), `comparativo.py`, `em-relevo-cenas.json` (prompts do Em Relevo), `imagens/<canal>/` (geradas + `codex_log.jsonl`), `imagens/em-relevo-real/` (frames do longo-04).
