# ETAPA 2: produção (voz + imagens + thumb-base) · 003 Irã (youtube.videos id 5)

04/11/2026 · `status = 'producao'` no banco. Mídia (audio/, imagens/, thumb-var/) fica fora do git.

## Voz (Fish, `--por-frase`)
- **102 blocos, 102 mp3**; soma dos mp3 = **839 s = 13:59** (sem as pausas entre blocos do `build.py`, ~+1 min → **~15 min** no vídeo; título "em 15 minutos", confirmar com o áudio montado).
- **Hook (N001–N005): 29,75 s** (meta ≤ 35 s). Desfecho da anedota ("sai o caixão do poeta", fim do N002) em **11,7 s** (meta ≤ 10 s; a melhoria 1 da etapa 1, cortar "carregada de riquezas", ainda vale).
- **Repetição melódica do hook: 0,23** (queda média −4,7 st) contra 0,09 da amostra G. **Não é comparável**: o hook tem só 11 trechos entre pausas (a amostra G tinha 28), então a correlação média é ruidosa, e a queda no fim das frases é maior. Não repeti a tomada (custo é irrisório, mas o número não decide). **Hipótese:** o ouvido do Rodrigo decide; se soar robótico, regravar a referência do clone (ver `amostras-voz/LEIA.md`).
- **Whisper por bloco** (`tools/qa_voz_blocos.py`, saída `qa/voz_blocos.json`): **mín 75,0% (N059), média 95,1%**; 69 blocos ≥ 93%, 45 ≥ 97%; **33 blocos < 93%**, **0 tags faladas**, nenhuma frase faltando.
  - Os 33 são quase todos nome próprio persa/estrangeiro que o Whisper não sabe escrever (Ferdowsi→"ferdose", Shahnameh→"channame", Qadisiya, Nahavand, Khomeini, Mahsa Amini, Mojtaba, Koh-i-Noor, Qajar, Naqsh-e Rostam, Simurgh, xá/xiita→"char/chiita"…), em blocos curtos que amplificam o erro. Não são falha da voz: registrado e seguido (regra da etapa).
  - **Rodada 1 de correção** (3 frases apagadas e regeradas, US$ 0,003): N070 "no Irã" tinha virado "Irak" → corrigido (93,3%). N075 (a voz diz "mil novecentos e cinquenta e três" onde o texto tem "cinquenta e três": improviso inofensivo, mantido). N046 ("uns cinquenta mil dísticos"): regerada 2x, continua <93% por "dísticos"/"Simurgh" (Whisper), aceito.
  - A 1ª leitura do QA deu mín 54% / média 88,6% por **erro do meu comparador**: o Whisper escreve "1971", "2022", "522 a.C." e o texto tem os números por extenso. Corrigi `norm()` (algarismos → palavras, "a.C." → "antes de cristo", descarta "e", xá = shah) e reavaliei as transcrições já salvas, sem retranscrever. **Para a esteira:** o comparador padrão (`compara_voz.py`) deve fazer isso também.
- **Tempos:** hook 14 s; vídeo inteiro 238 s (≈ 0,5 s por frase, serial); Whisper small int8 2 threads nos 102 mp3: 148 s.

## Imagens
- **OpenAI sem crédito** (prova de crédito com I001 em `medium`: "You have no credits remaining"; nada cobrado) → `BLOQUEIO.md` (parcial) e **plano B fal.ai** (`tools/img_fal.py`, `fal-ai/flux/dev`, `canal.yaml` já com `gerador: fal`; o `AVISO-IMAGENS.md` do Rodrigo manda o mesmo). Nenhum reuso para cobrir falta.
- **189/189 em `cenas.json` geradas, 0 faltando** (188 do vídeo + `thumb-base`); lote único, `--paralelo 6`, ~3 min (flux/dev é muito mais rápido que os 25–35 min do gpt-image-2). **2 regeradas** (I030, I106; ver abaixo). Mais **2 variações de thumb** (`thumb-var/thumb-v2-guia.jpg`, `thumb-v3-ciro.jpg`) pelo fal.
- Amostra visual: 12 imagens de capítulos espalhados + 12 de cenas com risco de texto (contact sheets). Estilo coerente (cartoon, contornos grossos, céu azul), lugares e épocas plausíveis, figurino por época ok. **Reprovadas e regeradas (prompt ajustado no `roteiro.py`):** I030 (tablete com letras "TXEE" e marca no canto) e I106 (livro com escrita árabe inventada). Após regerar: sem texto; I106 ainda tem uma assinatura minúscula no canto inferior direito (recortar/enquadrar no render).
- **Ressalvas:** (1) o estilo do flux/dev **destoa** do gpt-image-2 do 002: personagens nem sempre "cabeça branca redonda" (alguns têm rosto realista de desenho animado, como os de I150/I118/I116); (2) a `thumb-base` e as variações saíram em flux/dev, **não em `high`**: se o Rodrigo recarregar a OpenAI, vale regerar a base em `high` (~US$ 0,22 cada); (3) I060 (Cilindro de Ciro) mostra glifos em grade, aceitável como "escrita cuneiforme", mas não é fiel; (4) rótulos dos mapas (`labels.jsx`) ainda precisam ser conferidos contra as imagens (pendência 3 da etapa 1); (5) não abri as 189 uma a uma: ~24 vistas.

## Custo (teto R$ 80 ≈ US$ 13,7)
| Fornecedor | US$ | R$ |
|---|---|---|
| Fish Audio (A/B 0,137 + hook 0,007 + resto 0,173 + correções 0,003) | 0,320 | 1,87 |
| fal.ai (189 + 2 regeradas + 2 thumbs = 193 imagens × 0,025) | 4,825 | 28,24 |
| OpenAI | 0 | 0 |
| **Total ref_id 5** | **5,145** | **30,11** (**38% do teto**) |

## Problemas e improvisos (para o relatório da esteira)
1. OpenAI sem crédito → plano B fal (mudança de estilo; thumb não saiu em `high`).
2. Meu comparador Whisper reprovou 58/102 por números em algarismos; corrigir `norm()` (ver acima) e fazer o mesmo no `compara_voz.py` da esteira. Sem isso, o critério "≥ 93% por bloco" gera falso alarme.
3. Os nomes persas fazem ~30% dos blocos ficarem entre 75% e 93% no Whisper small; o critério por bloco deveria ter lista de exceções (glossário de nomes próprios normalizados) em vez de olho humano.
4. A medida "repetição melódica" não funciona em trechos de ~30 s (poucos trechos): comparar sempre amostras de tamanho parecido (≥ 60 s).
5. `.prompt-*.md`, `cenas-teste.json` e `blocos-hook.json` ficam na pasta (não vão para o commit).

## Melhorias sugeridas
1. `compara_voz.py`/`qa_voz_blocos.py` na esteira com normalização de números e glossário de nomes próprios (um `glossario.json` por canal).
2. Prompts de objetos com inscrição (tablete, livro, cilindro): sempre "no letters, no writing" explícito; flux/dev inventa escrita árabe/latina quando o prompt diz "manuscript/inscription".
3. Para o 004+: decidir antes da etapa 2 qual gerador de imagem vale (custo 5× menor e 10× mais rápido no fal; qualidade/estilo menor): fazer um A/B de 6 cenas gpt-image-2 × flux/dev com o Rodrigo.
