# Proposta v3: HQ colorida "EXPEDIENTES SECRETOS #1" (Dossier en Minutos) · 23/11/2026

Decisão do Rodrigo (23/11, ~19:00–19:20): **HQ ocidental colorida**, não mangá. Estilo-base = a página colorida da v2 (`../manga/pagina-1-estilo-canal.jpg`), que ele aprovou, temperada pelas refs dele (`refs-rodrigo/`, fora do git): cor e luz um pouco mais vivas e diagramação mais dinâmica. Reaproveita a v1 (`../expedientes-pdf/PROPOSTA.md`) e a v2 (`../manga/PROPOSTA.md`) em plataforma, direitos, fontes, código e folha de personagem. **FATO** = tem fonte; **EST.** = estimativa nossa.

## Resumo (10 linhas)
1. **Produto:** *Expedientes Secretos #1*, com 2 histórias inéditas no canal (~16 pp cada), pôster A3 e 6 wallpapers. Sai uma edição nova a cada 4–6 semanas.
2. **Histórias:** *Operación Garbo* (MI5, 1941–44) e ***La Cosa*** (KGB, Moscou 1945–52): o micrófono sem pilhas escondido num brasão de madeira dado de presente ao embaixador dos EUA.
3. **Estilo:** o traço aprovado da v2, com luz quente contra noite fria, 1 painel diagonal ou grande por página e balões brancos em caixa alta. Não virou arte de "super-herói".
4. **A IA segurou cor e personagem:** Juan ficou reconhecível em 7/7 quadros novos. Única falha: 1 quadro botou o Juan onde ele não estava; a correção foi tirar a folha de personagem nos quadros sem ele.
5. **Amostra:** `capa.jpg`, `pagina-1.jpg`, `pagina-2.jpg`, `wallpaper-celular.jpg`, `wallpaper-desktop.jpg` e `amostra.pdf`.
6. **Preço:** **US$ 6,99** de lançamento (US$ 7,99 depois). Combo de 3 edições a US$ 17,99 (EST.).
7. **Venda:** **Hotmart** agora (OXXO, Mercado Pago, e-mail do comprador, área de membros com atualização). Na fase 2, site próprio com Payhip ou Lemon Squeezy e assinatura.
8. **Leads:** landing com **1 wallpaper de celular grátis** em troca do e-mail (o `wallpaper-celular.jpg` serve), ferramenta **Kit** (plano grátis até 10 mil inscritos) e sequência de 4 e-mails em espanhol.
9. **Prazo da #1:** **~5 dias úteis** depois do OK (~175 imagens no Codex, US$ 0, só de dia: qua/qui/sex).
10. **Custo da amostra:** **US$ 0** (9 imagens no Codex; Gemini não foi usada).

---

## 1. Estilo: o que mudou em relação à v2
| | v2 colorida (aprovada) | v3 HQ (esta amostra) |
|---|---|---|
| Traço | tinta + cor chapada + sombra recortada | **igual** (2 quadros aprovados da v2 entram como referência de estilo) |
| Cor e luz | fria e uniforme | mais contraste: **luz quente de abajur e poste contra noite azul**, contraluz, sombras fundas |
| Diagramação | retângulos | **calhas diagonais** (pág. 1: escritório × diplomata; pág. 2: Lisboa × biblioteca × carta) e 1 quadro alto atravessando 2 linhas |
| Texto | balões brancos caixa alta, legendas com barra vermelha | igual (Comic Neue Bold, Bangers, Bebas Neue, Special Elite; tudo OFL/Apache, `src/fontes/LEIA.md`) |
- **Pág. 1:** a da v2 com as mesmas artes, só a calha entre os quadros 2 e 3 virou diagonal e o cabeçalho mudou para "EXPEDIENTES SECRETOS #1". **Pág. 2:** refeita a cores, com as artes novas.
- **Consistência:** a folha de personagem colorida da v2 (`arte-v2/folha-cor.jpg`, a mesma de `folha-personagem.jpg`) vai como 4ª referência, junto com a descrição física fixa. **Regra nova:** em quadros sem o Juan, use `visual-hq-sem-juan.yaml`. Com a folha, o Codex o colocou entre os alemães (`arte/P205-com-juan-errado.jpg`).
- **Configuração:** `src/visual-hq.yaml`, com refs = 2 quadros da v2 + I040 do 015 + folha, e a instrução "colour slightly richer… not a glossy superhero style".

## 2. As 2 histórias
**1. Operación Garbo** (a da v2; escolha já feita). Juan Pujol, catalão, é recusado pelos ingleses, vira espião dos alemães, inventa de Lisboa uma rede de 27 agentes que não existem e, adotado pelo MI5, engana Hitler sobre o Dia D. Recebe a Cruz de Ferro e o MBE. **16 pp:** a sinopse de 28 pp da v2 condensada em 4 capítulos de 4 pp (*El hombre que nadie quería*, *Los 27 fantasmas*, *Araceli*, *La noche más larga* + epílogo em Caracas). Risco de política **baixo** (detalhes na v2 §9).

**2ª história: 2 candidatas (nenhuma aparece nos roteiros 001–015, conferido por grep)**
| | **A. La Cosa (escolhida)** | B. Proyecto Azorian |
|---|---|---|
| O quê | 4/8/1945: os Jovens Pioneiros dão ao embaixador Averell Harriman um Grande Selo dos EUA esculpido em madeira. Ele o pendura no escritório da residência (Spaso House). Dentro, um microfone **sem pilhas nem fios**, inventado por **Léon Theremin** (o do instrumento, preso num laboratório do gulag), que só "acorda" com um feixe de rádio vindo de fora. Ouviu tudo por **7 anos**, até ser achado em 1952. Em 26/5/1960, depois do U-2, Henry Cabot Lodge o mostra na ONU | 1974: a CIA, com Howard Hughes de fachada ("mineração no fundo do mar"), constrói o Glomar Explorer para içar o submarino soviético K-129 de 5 km de profundidade |
| Por que vira HQ | presente de crianças que esconde uma arma; gênio preso; mistério técnico; reviravolta na ONU. Fecha a edição com o tom de "objeto" que o canal já usa | *heist* gigante, mas é técnico e longo |
| Risco de política | **baixo**: sem violência, figuras históricas mortas | **médio**: tripulação morta, enterro no mar |
| Fontes | CIA, "Compromise of the Great Seal"; NSA, "The Thing and I" e Cold War: Great Seal; Crypto Museum (links abaixo) | Polmar & White, *Project Azorian* (2010); FOIA da CIA |
**Por que A:** é KGB, tema de vídeo forte no canal (005-kgb, maior retenção em horas pelo relatório de monetização), contrasta com Garbo (Espanha/MI5 × Moscou/KGB, homem × objeto) e o eixo "presente de crianças → escuta de 7 anos" rende capa e Short. **16 pp:** *El regalo* (1945) · *El prisionero que inventaba* (Theremin) · *Siete años escuchando* · *La Cosa en la ONU* (1960). Fatos a conferir no e1: o local exato do achado (Kennan era o embaixador em 1952) e a data do relatório (1/12/1952).

## 3. Estrutura do PDF (~38 páginas, 6×9 pol.)
1. Capa (`capa.jpg`).
2. Créditos + "ilustraciones generadas con IA" + aviso de liberdades dramáticas.
3. Sumário.
4. **Operación Garbo** (16 pp).
5. Página de transição: "EXPEDIENTE 2".
6. **La Cosa** (16 pp).
7. **"Lo que es real"** (2 pp): fatos × liberdades e fontes das 2 histórias.
8. **Página do pôster:** miniatura + link de download do A3 em alta (o PNG vai no zip).
9. **Página final com CTA:** "¿Qué expediente quieres en el #2?" + link de inscrição na lista (lead) + aviso da próxima edição.
10. Contracapa: "Dossier en Minutos" + QR do canal.

## 4. Pacote e preço
- **Zip:** `Expedientes-Secretos-1.pdf` (~38 pp, ~30–40 MB), `poster-A3.pdf/png` (300 dpi, LANCZOS + nitidez, testado na v2) e **6 wallpapers** (3 de celular 1440×3120 + 3 de desktop 3840×2160).
- **Preço: US$ 6,99 no lançamento** (primeiros 7 dias ou primeiros compradores) e **US$ 7,99** depois. Fica abaixo dos US$ 9,99 do ebook do History in Minutes (FATO, v1), com o dobro de conteúdo da v2.
- **Edições:** #2, #3… a cada 4–6 semanas. Depois de 3 edições, combo a US$ 17,99 (EST.).

## 5. Plataforma
| | **Hotmart (agora)** | Site + Payhip | Site + Lemon Squeezy | Site + Stripe direto |
|---|---|---|---|---|
| Taxa | 9,9% + R$ 2,49 (FATO, relatório) | grátis com 5% + Stripe/PayPal; Plus US$ 29/mês com 2% | 5% + US$ 0,50, processamento incluso | ~3–4% + câmbio |
| LatAm (OXXO, Mercado Pago) | **sim** | não | não | parcial |
| E-mail do comprador | sim (+ integra com o Kit por webhook ou Zapier) | sim | sim | sim |
| Atualização para quem comprou | sim (área de membros: troca o arquivo) | sim (atualiza o arquivo) | sim | você que faz |
| Assinatura | sim (Hotmart tem recorrência) | sim | sim | sim |
| Imposto UE/EUA | Hotmart é revendedora | só parcial (UE/Reino Unido) | merchant of record | é seu problema |
- **Recomendo:** Hotmart agora (o público é ~70% LatAm, FATO do relatório). **Fase 2** (≥ 3 edições e ≥ 1 mil leads): site próprio com **Payhip** para a Espanha e a UE, e assinatura "Expediente del mes" a ~US$ 4,99/mês (EST.). O Lemon Squeezy é bom em imposto, mas o US$ 0,50 fixo pesa em produto de US$ 7, e há relatos de gente saindo depois da compra pela Stripe.

## 6. Funil de leads
- **Ferramenta: Kit** (ex-ConvertKit). O plano grátis vai até **10 mil inscritos** com envio ilimitado, mas só 1 automação (que basta para a sequência) e com a marca do Kit. Tem landing page própria grátis, então nem precisa de site.
  - **Alternativas:** Brevo (até 100 mil contatos, mas 300 e-mails/dia) e MailerLite (o grátis caiu para **250 inscritos** em 16/06/2026, pequeno demais).
- **Landing (1 página, espanhol):** imagem do wallpaper, "Descarga gratis el fondo de pantalla de *Operación Garbo*", campo de e-mail, **checkbox não pré-marcada** de consentimento e link de política.
- **Isca: `wallpaper-celular.jpg` serve.** Funciona no celular (de onde vem quase todo o tráfego do YouTube, EST.), tem a marca discreta e é a arte-chave da #1. Os outros 5 ficam só no pacote pago.
- **Sequência (4 e-mails, espanhol):**
  1. *Día 0:* "Tu fondo de pantalla de Operación Garbo" (link de download + 1 frase sobre o canal).
  2. *Día 2:* "El español que inventó 27 espías" (a história em 150 palavras + a pág. 1 da HQ como imagem).
  3. *Día 4:* "Expedientes Secretos #1 ya está aquí" (capa, o que vem no pacote, preço de lançamento US$ 6,99 por 7 dias).
  4. *Día 7:* "Última oportunidad + ¿qué expediente quieres en el #2?" (resposta vira pauta).
  - Depois: 1 e-mail por vídeo novo + 1 por edição.
- **LGPD/GDPR:** double opt-in (o Kit tem), consentimento explícito e separado para marketing, descadastro em todo e-mail, política de privacidade (modelo grátis), sem comprar lista. Como há público na Espanha/UE, o GDPR vale (FATO).
- **Visão de ecossistema:** a lista é do Rodrigo, não do YouTube. Serve para vender as edições, os PDFs da v1 e produtos de outros canais com o mesmo público.

## 7. CTA nos vídeos
- **Descrição (1ª linha):** `🎁 Fondo de pantalla GRATIS de espías → [landing]  ·  📘 Cómic "Expedientes Secretos #1" → [Hotmart]`
- **Comentário fixado:** *"¿Sabías que unos niños soviéticos le regalaron al embajador de EE. UU. un escudo… con un micrófono dentro? Lo contamos en cómic. Fondo de pantalla gratis en la descripción. ¿Qué expediente quieres en el #2?"*
- **Fala de ~5 s no fecho:** *"Y si quieres un expediente que no está en el canal, el cómic y un fondo de pantalla gratis están en la descripción."* Isso entra na bíblia de roteiro **só se o Rodrigo aprovar**. Hoje nada muda nos vídeos.
- Sem YPP o link não é clicável no Short (v1): no Short, "enlace en el perfil".

## 8. Produção da #1
| Etapa | Quem | Tempo / custo |
|---|---|---|
| e1 (Opus) | checar fatos com fonte das 2 histórias, roteiro página a página (`paginas.json` com textos) e prompts dos quadros | ~3 h, US$ 0 (Max) |
| e2 (Sonnet) | 3 folhas novas (Theremin, Harriman, Kühlenthal), **~160 quadros + capa + 6 wallpapers + pôster ≈ 175 imagens no Codex**, diagramação, QA visual página a página, PDF, zip, Drive | ~6–8 h, **US$ 0** (Gemini só se faltar Codex: ~US$ 0,05/img, teto US$ 3) |
| Rodrigo | ler o PDF (~25 min), criar o produto na Hotmart, conta no Kit (login dele), subir o zip | ~1,5 h |
- **Cota do Codex:** 9 imagens hoje = +3% da janela de 5 h (FATO, log). Então 175 imagens ≈ ~55–60% de uma janela de 5 h (EST.), divididas em 2–3 blocos. **Produzir de dia na qua/qui/sex**, com `fila.sh add … --agora`, para não disputar com a fábrica noturna.
- **Prazo:** ~5 dias úteis depois do OK. Edições seguintes: ~3 dias cada.

## 9. Direitos (o mesmo da v1/v2 + o que é novo)
- Valem v1 §direitos e v2 §9: arte de IA vendável com colofão, nada de selo oficial ou foto de arquivo, texto autoral, liberdades declaradas.
- **Refs do Rodrigo (HQs DC/Marvel e outras):** usadas só para eu entender o gosto dele; **não entram como referência no gerador**, e nenhum prompt cita obra, autor ou personagem. Ficam fora do git.
- **La Cosa:** o brasão é uma réplica do Grande Selo dos EUA, um emblema de governo. Na HQ ele aparece como **objeto histórico na cena** (é o tema), nunca como marca ou logo do produto. Nada de selo da CIA/KGB como arte (FATO, cia.gov, v1).
- Pessoas reais (Harriman, Kennan, Theremin, Lodge, Pujol) são figuras históricas mortas, retratadas sem degradação.

## 10. Métricas (30 dias depois do lançamento)
| Métrica | Onde | Meta EST. |
|---|---|---|
| Cliques nos links da descrição | encurtador com contagem (ou UTM no Hotmart/Kit) | ≥ 2% das views dos vídeos novos |
| Leads (e-mails confirmados) | Kit | ≥ 150 |
| Conversão lead → venda | Hotmart × Kit | ≥ 3% |
| Vendas | Hotmart | ≥ 10 (valida a #2) |
| Respostas "qué expediente quieres" | e-mail + comentários | pauta da #2 |

---

## Arquivos da amostra (prévias jpg ≤ 1 MB; mídia fora do git)
`capa.jpg` · `pagina-1.jpg` · `pagina-2.jpg` · `wallpaper-celular.jpg` (1440×3120) · `wallpaper-desktop.jpg` (3840×2160) · `amostra.pdf` (capa + 2 pp) · PNGs 300 dpi ao lado.
- **Código em `src/`:** `gerar.py` (Codex com orientação), `visual-hq.yaml` / `visual-hq-sem-juan.yaml`, `cenas-*.json`, `paginas.json`, `diagramar.py` (da v2 + painel em polígono), `hq.py` (capa, wallpapers, PDF), `fontes/`.
- **Para refazer:** `tools/.venv/bin/python canais/dossie-es/produtos/hq/src/hq.py`.
- **Custo:** 9 imagens Codex (US$ 0) + 1 refeita (P205) = **US$ 0**. Cota Codex: 5 h em 3%, semana em 14%.

Fontes de La Cosa: [CIA: Compromise of the Great Seal](https://www.cia.gov/stories/story/compromise-of-the-great-seal) · [NSA: Cold War Great Seal](https://www.nsa.gov/History/National-Cryptologic-Museum/Exhibits-Artifacts/Exhibit-View/Article/2718563/cold-war-great-seal/) · [NSA: "The Thing" and I](https://www.nsa.gov/portals/75/documents/news-features/declassified-documents/history-today-articles/10%202018/04OCT2018%20The%20Thing%20and%20I.pdf) · [Crypto Museum](https://cryptomuseum.com/covert/bugs/thing). E-mail e plataformas: [Kit free plan](https://intercom.help/convertkit/en/articles/16627071-the-kit-free-plan) · [MailerLite free plan FAQ](https://www.mailerlite.com/help/free-plan-update-faq) · [Brevo free plan limits](https://help.brevo.com/hc/en-us/articles/208580669) · [Payhip vs Lemon Squeezy](https://www.passivekit.com/payhip-vs-lemonsqueezy/) · [Payhip pricing](https://passivekit.com/payhip-pricing/).

## O que precisa da decisão do Rodrigo
1. **Estilo da amostra:** aprova capa + páginas + wallpaper como padrão da série?
2. **2ª história:** La Cosa (recomendo) ou Azorian.
3. **Nome:** "Expedientes Secretos" (recomendo; já está na v1) ou outro.
4. **Preço:** US$ 6,99 de lançamento → US$ 7,99.
5. **Kit** para os leads (criar a conta é com ele) e OK para a landing com o wallpaper grátis.
6. **Fala de CTA de 5 s** nos vídeos (muda a bíblia de roteiro) sim/não.
7. OK para disparar e1 + e2 da #1 **de dia (qua/qui/sex)**.

## Aprendizados da série (e2 da #1, 24/11/2026)
Fonte: `001/E2-RELATORIO.md`, `financas.consumo` (notas `dossie-hq-001 …`).
- **Gerador de imagem da HQ fora do Codex: `openai/gpt-image-2/edit` na fal** (mesma família do gerador do Codex/ChatGPT), com as refs de estilo da v3 + folha do personagem. Teste de 4 imagens: o `google/nano-banana-2.1/edit` saiu mais "cartum" (traço grosso, menos detalhe) e destoava das págs. 1–2 do Codex; o gpt-image-2 casou sem refazer páginas antigas. Custo real: US$ 0,053 (16:9 1536×864), 0,062 (2:3), 0,073 (1:1) por imagem em `quality: medium`; A3 2336×3296 ≈ US$ 0,12–0,14. 151 imagens pagas, **0 molduras** e 0 textos inventados nas folhas.
- **Folha de personagem antes dos quadros** funcionou: 8/8 aprovadas na 1ª, rostos consistentes nos quadros.
- **Detector de imagem preta** do `img_fal.py` reprova cena escura de propósito ("floating in deep darkness"): escrever "dark slate-blue background with a soft glow".
- **Época:** pedir o modelo do avião pelo formato (U-2 = asas longas e retas de planador), senão sai jato moderno/asa delta.
- **Balões automáticos olhando a arte** (`001/autolayout.py`: rostos por OpenCV Haar, nada fora do quadro, sem sobrepor, ordem de leitura, rabicho até a borda do rosto de quem fala): de ~150 textos, só 7 precisaram de ajuste manual (falante de costas/rosto não detectado). Reaproveitar na #2.
- **Custo no mesmo endpoint em paralelo duplica o lançamento** (o `img_fal.py` mede pelo uso do endpoint): rodar os lotes da HQ um de cada vez (`001/tools/rodar_fal.py`).
