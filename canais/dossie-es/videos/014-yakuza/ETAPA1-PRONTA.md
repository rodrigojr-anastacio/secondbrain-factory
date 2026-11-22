# ETAPA1-PRONTA · dossie-es/014-yakuza · id 57 · 21/11/2026

## Pares aprovados (crivo da embalagem r3, 3 de 3; `CRIVO.md`, `embalagem/crivo-r*.md`; registrados em youtube.embalagem_variantes)
| par | título | padrão do título | thumb (padrão) | texto da thumb |
|---|---|---|---|---|
| A | YAKUZA: la mafia que tenía su nombre en la puerta | SIGLA: aposto com lacuna | `objeto-simbolo` (controle): letreiro vertical de madeira arrancado, encostado sob a marca clara na parede creme, 組 composto em código | "YAKUZA" + sello "¿LEGAL?" |
| B | Cómo la Yakuza pasó de trabajar para Japón a ser su enemiga | Cómo + org + verbo + alvo | `numero-estatistica`: "184.000" gigante riscado em vermelho sobre a ilustração de um salão de tatame vazio | "184.000" + "HOY 17.600" |
| C | Japón, 1992: la Yakuza tuvo que esconder su nombre | [Lugar], [año]: aposto | `cena-acao`: homem de terno em contraluz diante de janela clara, rosto na sombra, rasgando ao meio o cartão de visita com o emblema do grupo | "YAKUZA" (rótulo datilografado em tira de papel) |
Histórico: r1 reprovou Thumb B ("só tipografia"), T3 ("Tokio, 1992: la película que la Yakuza no perdonó", caso único) e Thumb C (5 ternos de costas na rua); r2 reprovou a Thumb C (persiana); r3 aprovou.

## Promessa e onde o roteiro a paga
"En Japón, ser yakuza nunca fue delito: durante un siglo la mafia tuvo oficinas con su nombre en la puerta y trabajó a la vista para ministros, gobiernos y empresas, hasta que Japón inventó leyes y contratos para borrarla de la vista; de 184.000 miembros a 17.600."
- Hook N001–N004 (0:00–0:38): Itami atacado (maio/1992) → "Los grupos de la yakuza tenían oficinas, emblema y tarjetas con su nombre. Pertenecer a la yakuza no era delito. Hoy tampoco." (~0:16–0:25) → "Esta es TODA la historia de la Yakuza: la mafia que no se escondía, porque trabajaba para el poder. De ciento ochenta y cuatro mil miembros y asociados… a diecisiete mil seiscientos." (0:25–0:38).
- T2 ("trabajar para Japón"): exp. 1 El Ministro (0:38–1:35), 2 La Celda e 3 La Visita (1:35–3:27); "ser su enemiga": exp. 7 El Letrero (6:10), 11 El Contrato (10:32), 12 La Sentencia (11:18).
- T1/T3 ("nombre en la puerta" / "esconder su nombre"): hook (0:16) e exp. 7 El Letrero (6:10–7:40: 41 de 108 escritórios tiram letreiro e emblema; chefes tiram o nome dos cartões). Obrigação do crivo r3 cumprida: "41 de 108", nunca "todos".

## Ângulo, detector e crivo de ângulo
- Ângulo: "la mafia que no se escondía, porque trabajaba para el poder": a história contada pelos momentos em que o Estado japonês usou a yakuza à vista e pelos papéis com que depois a apagou (o clone Era Span já fazia a versão "tolerância"; ver `ANGULO.md`, "Atualização").
- `SIMILARIDADE.md`: **5/100** (máx. clone Era Span, cobertura 6%).
- `CRIVO-ANGULO.md`: **r1 APROVADO**; 8 de 12 expedientes fora da manada (67%).

## O que a etapa 2 precisa saber
- **3 thumbs, uma por conceito** (A/B/C = T1/T2/T3), prompts-base no `cenas.json` (`thumb-A/B/C`); textos, 組, aba "EXPEDIENTE Nº 014" e números no `src/Thumbnail.jsx`. Condições do crivo r3: Thumb C com rótulo "YAKUZA" ≥ ~12% da altura, fonte datilografada encorpada, e o rasgo **visível** (metades separando, emblema cortado), senão vira "homem segurando papel" (parecido com 012 B/013 B); Thumb A: conferir que a IA não escreveu letras no letreiro; Thumb B: números sobre tira/contorno, nunca vermelho direto sobre ardósia.
- Roteiro 1.878 palavras, ~13:15; 65 blocos; 12 expedientes; **198 imagens novas + 3 thumbs** (custo previsto ~US$ 8,2; teto US$ 12).
- `src/` e `tools/` copiados do 013 (sem `timeline.json`): trocar textos fixos ("NÚREMBERG"/"Nº 013") e os pinos do `labels.jsx`.
- Pronúncias e cuidados de imagem: `ETAPA1.md`, seção Pendências (placas/cartões/emblemas em branco; sem tatuagem; violência de longe).

## Pendências
- Nenhuma que bloqueie. Kaplan & Dubro, Kapur e Maruyama citados com atribuição, sem leitura do original. Reconferir o Supremo no caso Nomura antes de publicar.
