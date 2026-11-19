# Thumbs extra D/E · dossie-es 012 MI6 (19/11/2026, pedido do Rodrigo)

Prédio do MI6 (SIS Building, Vauxhall Cross, Tâmisa: blocos escalonados creme com vidro verde) + agente de smoking na frente (arquétipo do 007, **sem rosto de ator, sem arma/logo, sem "BOND"/"007"**).

| thumb | composição | texto |
|---|---|---|
| `thumb-D.jpg` | agente de costas no cais à esquerda, prédio ao entardecer do outro lado do rio | carimbo "LO INVENTARON" no céu, aba Nº 012 |
| `thumb-E.jpg` | agente em 3/4 à esquerda, rosto na sombra, ajeitando a abotoadura; prédio grande atrás | idem, carimbo à direita |

**Par sugerido:** T3 "El Complot Nazi que Nunca Existió | Expedientes Secretos del MI6" + **"LO INVENTARON"**.
Por quê: o título diz que o complô *não existiu*; a thumb dá o veredito de *quem* o fez (o prédio e o agente do MI6), sem repetir "MI6" nem "complot". Alternativa: T1 ("…que nadie escribió en Berlín") também fecha com "LO INVENTARON" (quem escreveu, então?). Não use com T2 (repete a ideia de "engañó").

Testes: a 320×180 e 160×90 (`prancha-celular.jpg`, A–E lado a lado) o prédio escalonado, o smoking e o carimbo leem; D e E se diferenciam das A/B/C (únicas com céu e cidade). Texto cor papel sobre carimbo vermelho (mesmo contraste ~6,5:1 aprovado na B).

Observações:
- Base `fal-ai/nano-banana` (mesma das A/B/C), 1344×768 (máximo 16:9 do modelo; as A/B/C também), saída 1280×720 jpg (262 KB e 238 KB).
- 4 tomadas (`bases/`, prompts em `cenas-extra.json`): D1 tinha moldura branca → recortada (`imagens-orig/D1.jpg` é a original); D2 com prédio menos fiel; **E2 descartada: rosto visível parecido com ator real**. Nenhuma letra inventada nem código de cor no canto nas usadas.
- O prédio é de 1994: anacrônico para o caso de 1941 (que foi da BSC em Nova York). Vale como símbolo do serviço; se o crivo pedir fidelidade, a A ("NUEVA YORK") continua sendo a do caso.
- Composição: `compose.py` (PIL; não mexe no `src/` do vídeo). Custo: US$ 0,16 (4 imagens, `--video 51`).
