# Roteiro: dossie-es, ramo "Expediente de ingreso" (teste aprovado 28/11/2026)

Regra do ramo: vale **só** para o vídeo cujo item do backlog tem `RAMO: biblia-ingreso` (ver `README.md`). **Prevalece** sobre `../biblia/roteiro.md` nos assuntos abaixo (estrutura, ponto de vista, hook, fecho, tamanho do recorte). **Todo o resto** do roteiro padrão continua valendo e deve ser lido lá: Forma × Conteúdo (ângulo próprio, `ANGULO.md`, manada, cota ≥ 50%, detector < 30, crivo de ângulo), Tom (presente histórico, seco, atribuição), Idioma (espanhol neutro com tú, 2ª leitura nativa), WPS 2,38, revisão de fatos e as lições dos vídeos 001–017.
Fonte: proposta `../analises/2026-11-28-formato-como-era-vivir.md` §2 (demanda 2026: 897 vídeos medidos, Te lo Pinto "Tu vida en cada rango" 12–23× a mediana; Tercios de Tinta "Así era la vida real de un soldado…" 29×; Historia Militar "¿Qué se sentía ser…?" 15–19×). Decisão do Rodrigo: 28/11/2026 13:45 (formato aprovado como teste) e 13:50 (ramo separado). Tudo aqui é **Hipótese** até ter CTR/retenção dos 3 vídeos do teste (critério na proposta §4c).

---

## A ideia em 1 linha
O espectador recebe a **ficha de entrada** numa organização, **num ano e num lugar exatos**. Cada EXPEDIENTE é uma etapa da vida lá dentro, contada em **2ª pessoa ("tú")** e **provada pelo depoimento/documento de um recluta real**, que é o fio do vídeo.
Diferença para a manada ("Tu vida en cada rango/nivel de…", Te lo Pinto e clones): lá é escada fictícia, genérica, sem data nem fonte; aqui é **uma época + um lugar + um recluta documentado**, em expedientes.

## Esqueleto fixo (hook + 8–10 expedientes + cierre, 11–13 min)
A sequência é **por etapa de vida**, não cronológica da organização. Os 8 expedientes abaixo são obrigatórios e nesta ordem; pode haver 1–2 extras (ex.: "La Familia", "La Guerra") se a fonte der, sem passar de 10.

| # | bloco | o que faz | duração |
|---|---|---|---|
| 0 | **Hook (cena física, 2ª pessoa)** | data + lugar → **tú** numa cena com um **objeto** concreto (o objeto que volta no fecho) → desfecho seco → "Este es el expediente de lo que era formar parte de X" → promessa em 1 linha (ex.: "de la puerta de entrada a las dos únicas salidas"). Sem "hola", sem vinheta, sem pedir inscrição. ≤ 35 s | 20–35 s |
| 1 | **EXPEDIENTE 1: El Reclutamiento** | quem escolhe, por que você, quanto tempo te observam, quem te apresenta | 60–80 s |
| 2 | **EXPEDIENTE 2: La Prueba** | o 1º serviço / o teste de confiança antes de entrar | 60–80 s |
| 3 | **EXPEDIENTE 3: El Juramento** | o rito contado como **objeto**, pelo testemunho do recluta-fio (nunca o objeto/hook do vídeo "TODA la historia" do mesmo tema) | 60–80 s |
| 4 | **EXPEDIENTE 4: Las Reglas** | um **documento real** com as regras, lido contra a vida da época | 60–90 s |
| 5 | **EXPEDIENTE 5: El Dinero** | quanto se ganhava, de onde vinha, números exatos com fonte | 60–80 s |
| 6 | **EXPEDIENTE 6: Un Día Cualquiera** | rotina, casa, família, o que se podia contar à mulher/aos filhos. **O CTA da HQ (~37–40%) cai antes deste bloco** | 60–80 s |
| 7 | **EXPEDIENTE 7: La Falta** | o que acontecia a quem quebrava regra: sugerido por tinta e sombra, **fora de quadro**, sem violência explícita e sem vocabulário de glamour | 60–80 s |
| 8 | **EXPEDIENTE 8: La Salida** | as únicas saídas (prisão/colaboração ou sumir), com o caso real do recluta-fio | 60–90 s |
| — | **Cierre** | volta ao **objeto do hook** + aforismo de 2 frases + 1 frase neutra de presente + "Y tú, ¿habrías dicho que sí? Déjalo en los comentarios." | 30–45 s |

- **CTA de inscrição (~60%, 55–70%)**: a frase fixa de `../cta/inscricao/inscricao.py` (`TEXTO`) como **último bloco do EXPEDIENTE 6 ou 7**, ≥ 2 min do CTA da HQ. Regras e portões idênticos ao padrão: `../biblia/roteiro.md` item 6 e `../cta/inscricao/LEIA.md` (`inscricao.py roteiro $V` APROVADO).
- **Título falado** no começo de cada expediente ("El Reclutamiento.", "La Prueba."…), como no padrão; a cartela visual continua "EXPEDIENTE N: …" (`../biblia/visual.md`).
- **Cada expediente puxa o próximo** (re-hook no fim; o melhor é a frase final já ser o título do próximo), como no padrão.
- **Tamanho:** ~1.650–1.850 palavras (WPS 2,38) → 11–13 min. Hook ≤ 35 s (`HOOK_MAX`).

## O fio: uma época + um lugar + um recluta documentado
- **Um ano ou uma década, e uma cidade/região** no título e no hook (ex.: "Sicilia, 1962"). Nada de atravessar 100 anos: a história inteira é o formato padrão.
- **Um recluta real com depoimento/documento publicado** volta em **todos** os expedientes como prova ("Calderone lo cuenta así: …", "Vitale lo dijo en 1973"). Pode haver um 2º recluta de contraste. Atribuição sempre ao depoimento/sentença/livro (ex.: Antonino Calderone, *Gli uomini del disonore*, 1992, com Pino Arlacchi; Leonardo Vitale, depoimento de 1973).
- Lembre em 1 frase quem era o recluta (ex.: "mafioso confeso") para ele não virar herói (lição do 004).

## Ficha de ingresso na tela (objeto recorrente do ramo)
- Uma **ficha de ingresso** amarelada (máquina de escrever, foto 3×4, carimbos) que **se preenche a cada expediente**: um campo por etapa — **NOMBRE · PADRINO · PRUEBA · JURAMENTO · REGLAS · SUELDO · FALTAS · SALIDA** (adapte os rótulos à organização, sempre em espanhol). Aparece na abertura de cada expediente (junto da cartela "EXPEDIENTE N") com o campo novo sendo datilografado; carimbo **"ACEPTADO"** no fim do Juramento e **"BAJA"** na Salida.
- O roteiro marca no `roteiro.py`/storyboard qual campo e qual texto curto entra em cada expediente (≤ 4 palavras por campo, fatos com fonte). O texto é composto no código (Remotion), nunca pedido à IA de imagem.
- Visual (traço, paleta, pasta parda, carimbos, SFX nas transições): herda de `../biblia/visual.md`.

## Regras novas do ramo (além das do padrão)
1. **"Tú" nunca pratica violência.** Tú entra, observa, jura, recebe, obedece, vê e foge; a violência acontece ao redor, fora de quadro, atribuída a terceiros com fonte. Nada de "ganar respeto matando", "tu primer encargo" com morte, nem tom de glamour (regra do vocabulário de perpetrador do 007/010, aplicada à 2ª pessoa; política do YouTube).
2. **Todo detalhe da vida em 2ª pessoa tem fonte** (depoimento, sentença, documento). Detalhe genérico sem fonte vira "según los arrepentidos…" ou sai. O formato atrai cena de filme (lições do 004 e do 005): peça ao revisor que separe lenda de documento em cada cena do "tú".
3. **Não canibalizar o vídeo "TODA la historia" do mesmo tema:** nenhum objeto, hook ou cena usado no vídeo antigo (ex.: Cosa Nostra 004 usou o santinho de Buscetta, o Restaurante, o Hotel, o Búnker e a Autopista: aqui **nenhum** deles; Buscetta no máximo como nome). Liste no `ANGULO.md` os objetos do vídeo antigo e confira.
4. **Nunca "Tu vida en cada rango/nivel de…"** nem escada de patentes como estrutura (marca do Te lo Pinto, saturada nos clones, que caíram para 1–2 mil views em ~6 semanas). A estrutura é a **ficha de ingresso por etapas**, não a escada.
5. **Sem "TODA la historia"** no hook e no título: a frase-promessa do ramo é **"Este es el expediente de lo que era formar parte de X"**.
6. **Tom continua seco, sem humor** (nada de piada, HUD, "bruxa"): é o Dossier, não o "como era viver" do historia-ptbr.

## O que continua igual ao padrão (leia lá; não copiado aqui)
Carimbos e SFX nas transições, cartelas "EXPEDIENTE N", pasta parda e máquina de escrever (`../biblia/visual.md`); CTA da HQ ~37–40% (`../cta/encaixe.py`); CTA de inscrição ~60% com frase fixa e botão SUSCRÍBETE (`../biblia/roteiro.md` item 6); ângulo América Latina quando houver fato real; atribuição de toda acusação; regra do nome que diz o que é (`../biblia/titulo.md`, 24/11/2026); políticas do YouTube (`../biblia/README.md`); voz (`../biblia/voz.md`).

## Checklist do roteiro (ramo)
- [ ] Hook ≤ 35 s em 2ª pessoa, cena física com objeto, data + lugar, "Este es el expediente de lo que era formar parte de X" + promessa.
- [ ] Os 8 expedientes obrigatórios na ordem (Reclutamiento → Prueba → Juramento → Reglas → Dinero → Un Día Cualquiera → La Falta → La Salida), no máx. 10.
- [ ] Recluta-fio documentado presente em todos os expedientes, com atribuição; época e lugar únicos.
- [ ] "Tú" nunca pratica violência; La Falta sugerida, fora de quadro.
- [ ] Cierre volta ao objeto do hook + "Y tú, ¿habrías dicho que sí?".
- [ ] Ficha de ingresso: campo e texto de cada expediente marcados no storyboard; "ACEPTADO" no Juramento e "BAJA" na Salida.
- [ ] Nenhum objeto/hook/cena do vídeo "TODA la historia" do mesmo tema.
- [ ] Portões do padrão: `ANGULO.md`, detector < 30, `CRIVO-ANGULO.md` APROVADO, revisão nativa + fatos, `inscricao.py roteiro $V` APROVADO.

## Exemplo de hook (proposta §2b, Cosa Nostra; ponto de partida, a pesquisa confirma)
"Catania, 1962. Un hombre que conoces desde niño te presenta a otro con cuatro palabras: 'Questo è la stessa cosa'. Desde ese momento, esas palabras son tu único documento. […] Este es el expediente de lo que era formar parte de la mafia siciliana. Y de las dos únicas maneras de salir." → cierre "Las Cuatro Palabras". Confirmar na fonte (Calderone/Arlacchi) a fórmula exata da apresentação antes de usar.
