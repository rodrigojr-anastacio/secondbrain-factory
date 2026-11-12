# THUMBS 001-midway (3 conceitos para o "Testar e comparar")

Template: `../../biblia/thumb.md`. Amostras feitas no teste de estilo (12/11/2026): `../../amostras/thumb-A.jpg`, `thumb-B.jpg`, `thumb-C.jpg` (base `openai/gpt-image-2` via fal 1536×864 + texto no Remotion, `../../testes/estilo/src/Thumbnail.jsx`). Prompts em `../../testes/thumb-cenas.json`.

| | Palavras | Imagem | Paga no vídeo |
|---|---|---|---|
| **A** | NO VISITORS / ALLOWED + RESTRICTED | atol em corte: albatrozes e hangar em cima; munição, sala selada e barcaça submersa acesas em ciano embaixo | a visitação suspensa (B03, B16) |
| **B** | 3 MILES / DOWN + RESTRICTED | coluna d'água: o atol lá em cima, o porta-aviões no fundo aceso em ciano, um submersível | os naufrágios a 5.400 m (B19) |
| **C** | THE BIRDS / WON + RESTRICTED | canhão de 5" enferrujado tomado por albatrozes e filhotes, cerca fechada | refúgio de vida selvagem, Wisdom (B15–B18) |

Recomendação: **B** como principal (mais simples, um objeto-herói, contraste máximo; lê em 320×180), A e C no teste. Ajuste fino para a fase 2: o porta-aviões de B tem ilha grande demais para o Kaga/Akagi (pedir "very small island on the starboard side"), e a barcaça de A não é de Midway (trocar por canhão/hangar submerso? ou deixar só a sala selada).

## Finais (12/11/2026)
Arquivos: `thumbs/thumb-A.jpg`, `thumb-B.jpg`, `thumb-C.jpg` (1280x720, 180-355 KB), `thumbs/previa-320.jpg` (as 3 a 320x180: texto legível nas três), `out/thumbnail.jpg` = cópia da B. Código: `thumbs/proj/` (Remotion mini-projeto, `src/Thumbnail.jsx`; node_modules por symlink do teste de estilo; render: `remotion still src/index.jsx Thumbnail ../thumb-X.png --props='{"variante":"X"}'`). Bases sem texto em `thumbs/bases/`, prompts em `thumbs/cenas.json`.

| | Base | O que mudou |
|---|---|---|
| A | regenerada (`bases/A.jpg`) | sem a barcaça: no lugar, um canhão costeiro de 5" enferrujado em cavidade alagada, aceso em ciano (existe em Midway); mantidos munição e sala selada com porta de aço; "no boats, no ships" |
| B | regenerada (`bases/B.jpg`) | porta-aviões com ilha pequena a estibordo (coerente com Akagi/Kaga), sem bandeira ou marcação; texto subiu (top 170 para 110) para não encostar no casco |
| C | mantida (`bases/C.jpg` = T3 do teste) | sem alteração; canhão, albatrozes, cerca fechada, luz ciano na porta |

Conferência: bases 1536x864 sem preto, sem texto, sem insígnia/bandeira. Ressalva: o canhão de A e o de C são parecidos entre si (peças de 5"), mas contextos distintos (submerso x ao sol).

Custo: 2 gerações gpt-image-2 (A, B) = US$ 0,261 (US$ 0,13/imagem, uso real do endpoint; `financas.consumo` ref_id 30). Saldo fal depois: ~US$ 5,96.

Recomendação: **B principal** (um objeto-herói, maior contraste, lê bem em 320x180; paga em B19). A e C para o "Testar e comparar". Fraqueza de B: o navio fica pequeno na prévia; se perder no teste, ampliar o casco na fase 2.
