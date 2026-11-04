# Bancada de modelos de imagem (fal.ai), historia-ptbr/003, 04/11/2026

## Pergunta do Rodrigo: "usou os mesmos prompts?"
**Sim.** O 003 usou o mesmo `estilo_prompt` do Egito e da Índia (o histórico do `canal.yaml` no git mostra o mesmo texto desde o primeiro commit). Os prompts de cena seguem o mesmo padrão: descrição concreta + estilo anexado pela tool.
**O que mudou foi o modelo.** Egito e Índia saíram no gpt-image-2 `medium` (OpenAI, 1536×1024). O 003 saiu no `fal-ai/flux/dev` (1536×864), porque a OpenAI estava sem crédito. O flux/dev ignora "round white heads, dot eyes" e desenha um cartoon genérico com rosto realista. É por isso que os bonequinhos sumiram. Comparação lado a lado: `diagnostico-gpt-vs-flux.jpg`.

## Descoberta principal
**O gpt-image-2 existe dentro do fal** (`openai/gpt-image-2` e `openai/gpt-image-2/edit`), e é cobrado no crédito do fal. Dá para voltar ao estilo dos bonequinhos sem recarregar a OpenAI. No fal, o `medium` a 1536×864 sai por **US$ 0,04/img**, contra ~US$ 0,055 na OpenAI direto.

## Bancada: 12 configurações × 2 cenas
- Cenas: **I002** (caravana com camelos e condutor sob o portão, com gente) e **I007** (ruínas de Persépolis ao pôr do sol, cenário).
- Grades: `grade-1.jpg` e `grade-2.jpg`. A referência gpt-image-2 do Egito e da Índia fica no topo de cada uma.
- Prompts exatos de cada modelo: `prompts.json`. Resoluções e tempos: `resultados.json`. Script: `bench.py`.
- Os modelos de edição receberam I041 do Egito e I041 da Índia como referência de estilo.

Notas de 0 a 5, dadas olhando as grades:

| Configuração | Endpoint | US$/img | Resolução | Bonequinho | Cena | Sem texto | Nota |
|---|---|---|---|---|---|---|---|
| gpt-image-2 medium | openai/gpt-image-2 | 0,040 | 1536×864 | 5 | 5 | 5 | **5,0** |
| gpt-image-2 edit low (+refs) | openai/gpt-image-2/edit | 0,020 | 1536×864 | 5 | 5 | 5 | **4,8** |
| gpt-image-2 low | openai/gpt-image-2 | 0,006 | 1536×864 | 4,5 | 5 | 5 | 4,5 (*) |
| nano-banana 2.1 edit (+refs) | google/nano-banana-2.1/edit | 0,044 | 1376×768 | 4,5 | 4,5 | 5 | **4,4** |
| nano-banana edit (+refs) | fal-ai/nano-banana/edit | 0,040 | 1344×768 | 4 | 4 | 5 | 4,0 |
| recraft v4 style | recraft/v4/style/text-to-image | 0,037 | 1344×768 | 3,5 | 4 | 5 | 3,7 |
| kontext pro multi (+refs) | fal-ai/flux-pro/kontext/multi | 0,040 | 1392×752 | 4 | 3 (Persépolis genérica) | 5 | 3,5 |
| seedream 4.5 edit (+refs) | fal-ai/bytedance/seedream/v4.5/edit | 0,040 | 3416×1920 | 3 | 4 | 5 | 3,4 |
| seedream 4 t2i | fal-ai/bytedance/seedream/v4/text-to-image | 0,030 | 1536×864 | 3 (palito, cabeça grande) | 4 | 5 | 3,3 |
| gpt-image-1-mini medium | fal-ai/gpt-image-1-mini | 0,015 | 1536×1024 | 2,5 | 3,5 | 5 | 3,0 |
| z-image turbo | fal-ai/z-image/turbo | 0,007 | 1536×864 | 2 (bonecos sem rosto) | 3 | 5 | 2,5 |
| ideogram v3 turbo (style ref) | fal-ai/ideogram/v3 | 0,030 | 1312×736 | 0 (rostos de desenho animado comum) | 3 | 5 | 1,5 |

(*) O `low` é tentador pelo preço, mas o canal já reprovou o `low` em 02/11 porque borra no Ken Burns. Só vale com teste de zoom em 1080p.

Nenhum modelo pôs texto inventado nessas 2 cenas. O problema de letras falsas no 003 apareceu nos **mapas**, e eles devem continuar sem texto, com rótulos no código.

## Recomendação (o Rodrigo aprova o vencedor)
1. **`openai/gpt-image-2` medium no fal, US$ 0,04/img: o vencedor.** É o mesmo modelo do Egito e da Índia, com o mesmo estilo, sem precisar de referência e já em 1536×864. Para ~190 imagens, dá ~US$ 7,60.
2. **`openai/gpt-image-2/edit` low + 2 refs do canal, US$ 0,02/img.** Fica muito perto do 1, pela metade do preço, e as referências travam a identidade. Precisa de teste de Ken Burns em 1080p antes, porque é qualidade `low`.
3. **`google/nano-banana-2.1/edit` + refs, US$ 0,044/img.** É a melhor alternativa fora da OpenAI e serve de plano B se o gpt-image-2 sair do fal. Sai em 1376×768, um pouco abaixo de 1536.

**Conclusão: só o gpt-image-2 resolve de verdade, mas não precisa de crédito na OpenAI, porque ele está no fal.** O `flux/dev` deve sair do canal.

## Não testados
- `flux-2-klein-9b-edit` e `qwen-image-edit-2511` foram pulados porque o saldo **real** do fal acabou (ver abaixo).
- `fal-ai/nano-banana-pro` (US$ 0,15/img) ficou de fora pelo preço.
- O restante do catálogo (213 geradores/editores) está em `catalogo/CATALOGO.md`, com o preço estimado a 1536×864.

## Custo e saldo
- Bancada: **US$ 0,70** em 12 linhas de `financas.consumo` (ids 59 e 62–72, ref_id 5).
- **Alerta:** o saldo ao vivo do fal (`api.fal.ai/v1/account/billing`) estava em **US$ 0,67** em 04/11 ~19h55, mas `financas.saldo_pre_pago` mostra US$ 4,43. Faltam ~US$ 3,8 de consumo não lançado no banco. O suspeito é o `img_fal.py`, que registra US$ 0,025 fixo em vez de cobrar por MP; o outro job (dossie) também gera no fal.
- A FASE 2 (~190 imagens no gpt-image-2 medium, ~US$ 7,60) **precisa de recarga do fal**.
