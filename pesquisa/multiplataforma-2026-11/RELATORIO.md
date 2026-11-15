# Distribuir os vídeos da fábrica em outras plataformas que pagam (15/11/2026)

Pedido do Rodrigo (brief `~/workspace/referencias/BRIEF-pesquisa-multiplataforma.md`). Só pesquisa: nada mudou na fábrica, nenhuma conta criada, custo **US$ 0**. Método: 5 pesquisas web em paralelo (Meta, TikTok, X+Snapchat, Kwai+Dailymotion, YouTube Shorts), 6 consultas yt-dlp via WARP, banco `vida` para custos unitários. Legenda: **[O]** = fonte oficial da plataforma; **[I]** = indício (blog/ferramenta/imprensa, estimativa de terceiro); **NC** = não confirmado. Várias páginas de ajuda (help.x.com, facebook.com/business/help, support.tiktok.com, faq.dailymotion.com) bloqueiam leitura automática; quando o dado veio só de trecho de busca, está marcado.

## Veredito
**Para dinheiro, hoje nenhuma plataforma compensa o tempo do Rodrigo.** Os canais ainda têm centenas de views no YouTube (historia-ptbr 1.097 views em 7 vídeos; dossie-es 830 em 6; Clearance 41; Em Relevo 30; `youtube.metricas_video`, 15/11/2026) e quase todo programa exige 10 mil+ seguidores ou convite. O público pt/es paga centavos por mil views fora do YouTube longo. O único teste que vale agora: **Shorts no próprio YouTube (descoberta, não receita)** e, opcionalmente, **Dailymotion** (sobe o vídeo longo como está, por API). Facebook entra num 2º momento, quando algum canal tiver 20 mil seguidores (Creator Fast Track Brasil).

## 1. Tabela por plataforma

| Plataforma | Programa vigente | Entrada | Brasil? (residência × público) | Por mil views | IA / reaproveitado / cross-post |
|---|---|---|---|---|---|
| **YouTube Shorts** (base) | YPP + pool de Shorts (45% ao criador) [O](https://support.google.com/youtube/answer/12504220) | Hoje: 1.000 insc. + 4.000 h longas/12 m **ou** 10 mi views Shorts/90 d (Shorts não contam nas horas) [O](https://support.google.com/youtube/answer/72851). **A partir de 01/02/2027** para quem entrar depois: 8.000 h ou 20 mi Shorts; e pool de Shorts só com 10 mi views/90 d [O](https://support.google.com/youtube/answer/12843009), anúncio de 10/08/2026 [O](https://blog.youtube/news-and-events/youtube-partner-program-updates-2027-new-opportunities-earn/) | Sim; RPM segue o país do **público** | Shorts: EUA ~US$ 0,33; BR ~0,045; MX ~0,040 [I](https://air.io/en/monetization/what-rpm-can-you-expect-from-shorts-in-2026) (11/11/2026) | Cortar o próprio vídeo não é proibido; "inautêntico" pega slideshow sem narrativa e IA em molde de produção em massa [O](https://support.google.com/youtube/answer/1311392). Rótulo IA só p/ conteúdo realista [O](https://support.google.com/youtube/answer/14328491) |
| **Facebook** | Content Monetization (in-stream + Reels + bônus num programa) [O](https://about.fb.com/br/news/2024/10/monetize-mais-conteudos-com-o-novo-programa-do-facebook/) | **Por convite** (manifestar interesse no painel) [O](https://creators.facebook.com/blog/new-tips-to-help-you-earn-on-facebook-content-monetization) 30/03/2026; números não publicados (blogs: 5–10 mil seguidores + 60–600 mil min/60 d [I]). **Creator Fast Track Brasil** (~04/11/2026): 20 mil seguidores em IG/TikTok/YT + 30 mil views/30 d; 20 Reels/mês por 3 meses; paga US$ 25/mês (até 100 mil seg.) [I](https://socialmediatoday.com/news/facebook-expands-creator-fast-track-program-to-brazil/873821) | Programa unificado no BR: **NC** (lista oficial não abriu). Fast Track: sim | Não publicado. Reels US$ 0,02–0,20; longo US$ 1–5; LatAm 0,50–2 [I](https://vidpros.com/how-much-does-facebook-pay-for-views/) | Desde 13/03/2026: só é original o produzido pelo dono; "narrar o que já está na tela", juntar clipes = não original → desmonetiza e corta alcance [O](https://about.fb.com/br/news/2026/03/recompensando-criadores-originais-no-facebook/). Tirar marca d'água [O](https://creators.facebook.com/blog/combating-unoriginal-content). Rótulo "AI info" obrigatório p/ vídeo/áudio realista [O](https://about.fb.com/news/2024/02/labeling-ai-generated-images-on-facebook-instagram-and-threads/) |
| **Instagram** | Sem pagamento por view no BR; assinaturas (desde 2023) [O](https://about.fb.com/br/news/2023/11/mais-opcoes-para-creators-ganharem-dinheiro-no-facebook-e-no-instagram), presentes [I], bônus de Reels por convite (BR **NC**) | — | Assinaturas sim; bônus NC | Não há RPM | Mesmas regras Meta; Reels até 3 min [I](https://www.socialmediatoday.com/news/instagram-officially-expands-reels-length-to-3-minutes/737766/) |
| **TikTok** | Creator Rewards Program (aberto, por inscrição) [O](https://newsroom.tiktok.com/introducing-the-new-creator-rewards-program?lang=en) 18/03/2024 | 18+, 10 mil seguidores, 100 mil views/30 d, vídeos **> 1 min**, conta pessoal [O] | **Sim, desde 09/2023** [I](https://techcrunch.com/2023/09/13/tiktoks-revamped-creator-fund-expands-beyond-the-us-to-brazil-germany-korea-and-more/); elegibilidade pela **residência**; valor pelo público (EUA vale mais) [I] | EUA US$ 0,50–2 (mediana 0,92) [I](https://ttcalculator.net/blog/q1-2026-tiktok-rpm-report/); BR sem número confiável (centavos) [I]. 1ª mil views de cada vídeo não paga [I] | "Reused material without anything new" fica **fora do For You** (e o Rewards só paga For You) [O](https://www.tiktok.com/community-guidelines/en/integrity-authenticity). Rótulo IA p/ cenas realistas; C2PA auto [I](https://tubefilter.com/2024/05/09/tiktok-transparency-labels-for-generative-ai-content/). Slideshow + voz IA: regra NC, relatos de "unoriginal" [I] |
| **X** | **Original Content Rewards** (substituiu o Revenue Sharing em 09/2026) [I](https://techcrunch.com/2026/08/08/x-replaces-misaligned-revenue-sharing-program-with-original-content-rewards/) | Premium pago + 500 seguidores verificados + 500 mil impressões de verificados/90 d [I] | **Conflito**: fora na estreia (08/2026) [I](https://www.metropoles.com/entretenimento/antigo-twitter-x-exclui-brasileiros-de-novo-programa-de-remuneracao); trecho de busca da página oficial já lista "Brazil" (~07/11/2026) → **NC** | Não publicado; sem relato confiável | Fora do programa: reupload, compilação, **postagem automatizada**. Vídeo de guerra feito com IA sem rótulo = 90 dias sem pagamento [I](https://www.engadget.com/social-media/x-to-require-ai-labels-on-armed-conflict-videos-from-paid-creators-citing-times-of-war-183631400.html) 03/03/2026 |
| **Snapchat** | Monetização unificada (Spotlight + mid-roll em Stories), por convite [O](https://newsroom.snap.com/snapchat-new-creator-monetization) | 50 mil seguidores, 25 posts/mês, + 10 mi views ou 1 mi Spotlight ou 12 mil h/28 d [O] | **Sim** (BR, MX, AR, CO, EUA nas listas) [O](https://help.snapchat.com/hc/en-us/articles/7012298096788) | Spotlight US$ 0,01–0,30; Stories 1,5–3 [I] | Desde 01/08/2026 Spotlight **não recomenda vídeo feito inteiramente por IA** [I](https://thenextweb.com/news/snapchat-spotlight-bans-ai-generated-videos-recommendations); prioridade a câmera do Snap [O](https://newsroom.snap.com/still-spotlight-but-still-real) |
| **Kwai** | Programa de Receita de Anúncios [O](https://www.kwai.com/pt-BR/support/creator-center/introducao-ao-programa-de-receita-de-anuncios) (09/11/2026) | Nível ≥ 6 ou 500 fãs, originais, > 12 posts/30 d, ≥ 1.000 views/post; abertura gradual "a criadores de alta qualidade" [O](https://www.kwai.com/pt-BR/support/creator-center/por-que-nao-tenho-posso-participar-do-programa-de-receita-de-anuncios) | Sim (foco BR/LatAm); en NC | Não publicado; R$ 0,80–3 [I] | Vídeo com #hashtag fora [O]; "vídeos feitos de fotos" e reposts sem pagamento [I](https://www.clip-short.com/pt/guias/monetizacao-do-kwai). Sem API. Reputação ruim (golpes, apostas) [I](https://www.aosfatos.org/noticias/kwai-jogos-ilegais-tarefas-pagas/) |
| **Dailymotion** | Standard Creator: monetização liga com 1.000 views no perfil [O](https://faq.dailymotion.com/hc/en-us/articles/207338747-Earn-revenue-from-video-monetization) (trecho de busca); Premium Creator 50/50 só EUA/UK/ES/IT/FR/BE/CH [O](https://about.dailymotion.com/en/become-premium-creator/) | Vídeo ≥ 1 min; partner terms; pagamento Tipalti, mínimo US$ 100 [O] | Standard: nenhuma página proíbe nem lista países → **NC** | Sem número oficial nem relato confiável | Rótulo IA só transparência [O](https://faq.dailymotion.com/hc/en-us/articles/27351015488530-AI-generated-content-label); sem regra contra reenviar o próprio vídeo; risco = licença do acervo/trilha |

## 2. Evidência real (perfis parecidos)
| Plataforma | Perfil | Números públicos | Leitura |
|---|---|---|---|
| YouTube Shorts | Ciência Todo Dia (pt) | 7,94 mi insc.; mediana dos últimos 40 Shorts 933 mil, máx. 5,5 mi [O: yt-dlp via WARP, 15/11/2026] | Shorts de ciência/clima em pt funcionam (ponte para o Em Relevo) |
| YouTube Shorts | Kings and Generals (história/guerra animada) | 4,22 mi insc.; mediana Shorts 87 mil, máx. 1,1 mi [O: yt-dlp, 15/11] | Em história os Shorts rendem bem menos por inscrito |
| YouTube Shorts | Archive in Minutes (molde do dossie-es) e Genius History (molde do historia-ptbr) | **Sem aba Shorts**; Archive: mediana 29 mil nos últimos 10 longos [O: yt-dlp, 15/11] | Os dois moldes cresceram **sem** Shorts |
| YouTube (canal-clima) | Short do Ciência Todo Dia sobre tornados no Brasil | 794 mil views (`pesquisa/canal-clima-2026-11/RELATORIO.md`, 08/11/2026) | Shorts quentes de clima em pt têm demanda |
| TikTok | Absolute History (en, History Hit/Little Dot) | 780 mil+ seguidores, 4–20 mi views/mês [I: estudo de caso do estúdio, dados 2022–23](https://www.littledotstudios.com/en-gb/case-study-absolute-history) | Funciona com vertical **nativo**, não corte do longo |
| TikTok | @thehistorylegends (en, história/militar) | 634 mil seguidores [I](https://creatordb.app/creatorstats/thehistorylegends/) 07/10/2026 | Nicho guerra en tem público |
| TikTok | "Professor de História" (pt) | 124 mil seguidores [I: Heepsy 06/2026, página 404] | pt de história é pequeno no TikTok |
| Instagram | History Cool Kids (fotos históricas) | ~2,2 mi seguidores [I](https://creatordb.app/creatorstats/historycoolkids/) 04/10/2026 | Foto + legenda, não vídeo narrado |
| Facebook | Página sem rosto de carros (imagem+texto) | 17 mil seg., 50–150 mil views/dia, US$ 180 no 1º mês monetizado [I](https://nichesitegrowth.beehiiv.com/p/my-facebook-page-income-report-1st-month-monetized) 19/03/2026 | Único relato de valor; não é vídeo |
| X | @historyinmemes ("Historic Vids") | ~6 mi seguidores [I, agregador sem data] | Vídeo de acervo viraliza em en |
| Snapchat, Kwai, Dailymotion | — | **NC**: nenhum perfil de história/guerra/mapas com números públicos encontrado | Sinal fraco de nicho |

## 3. Encaixe por canal
| Canal | Melhor aposta | Por quê | Evitar |
|---|---|---|---|
| **lugares-guerra-en** (Clearance, en) | **Shorts** (público EUA: RPM 5–8× o do BR [I]); depois TikTok en e Facebook | Único canal com público de RPM alto fora do YouTube; acervo real de guerra é o tipo que viraliza em en (Historic Vids, thehistorylegends) | Facebook/Meta: acervo de terceiros narrado pode cair em "narrar o que está na tela" (não original). X: Premium + rótulo obrigatório em guerra. Licenças: só domínio público (já é regra da bíblia) |
| **em-relevo** (pt-BR) | **Shorts** quentes de clima (enchente, granizo, calor) | Demanda comprovada em pt (Ciência Todo Dia 794 mil num Short de tornado); mapa 3D é original nosso (passa em qualquer regra de originalidade) | TikTok pt: RPM BR em centavos. Rótulo IA/realista: mapa 3D de evento real pode exigir declaração |
| **historia-ptbr** (pt-BR) | Shorts (só descoberta); Facebook mais tarde (público BR grande no FB) | Bonequinhos = animação não realista (sem rótulo IA obrigatório em YT/Meta/TikTok) | Volume alto de cortes de imagem parada + TTS = "inautêntico" no YT e "unoriginal" no TikTok. Kwai ("vídeos de fotos") |
| **dossie-es** (es) | Shorts com 1 EXPEDIENTE inteiro (1–3 min tem arco próprio) | Capítulos já são unidades curtas; molde Archive cresceu sem Shorts, então é teste, não necessidade | TikTok/Snap/Kwai es: RPM LatAm baixo, IA + TTS mal visto. X: IA em guerra exige rótulo |

## 4. Adaptação e operação
**Formato por plataforma:** Shorts 9:16 até 3 min [I](https://techcrunch.com/2024/10/03/youtube-takes-on-tiktok-with-longer-shorts-templates-trends-and-more); TikTok > 1 min p/ receber, 9:16 nativo; Reels IG até 3 min; Reels FB por API 3–90 s, 9:16 [O](https://developers.facebook.com/docs/video-api/guides/reels-publishing/); Facebook longo horizontal entra no programa unificado (mínimo de duração p/ in-stream em 2026 NC; piso oficial 10 s); Dailymotion horizontal até 2 h, sem adaptar [O](https://developers.dailymotion.com/reference/rate-limiting); Snapchat até 5 min [I].

**O que a fábrica precisaria acrescentar (Hipótese de desenho, não implementado):** uma etapa `cortes-verticais` depois do render: (1) escolher 2–3 trechos de 60–120 s com arco completo (dossie: 1 EXPEDIENTE; historia: um "mas… então…"; Clearance: o documento; Em Relevo: a cena do mapa); (2) reaproveitar o áudio da narração e as imagens já geradas, recompostas em 1080×1920 (imagem 16:9 centralizada com fundo desfocado, ou recorte com pan; Em Relevo re-enquadra a câmera 3D); (3) legenda queimada a partir da `legendas.srt` já existente; (4) render no Runpod; (5) título + "Related video" para o longo.

**Custo estimado por vídeo longo (3 cortes), com nossas ferramentas** (custos unitários de `financas.consumo`, últimos 10 dias):
| Item | Custo |
|---|---|
| Narração, imagens, legendas | US$ 0 (reuso) |
| Render Runpod (3 × ~90 s; média US$ 0,064 por render registrado, US$ 0,34/h) | ~US$ 0,05–0,20 |
| (Opcional) imagens 9:16 novas: ~20 × US$ 0,043 (fal) ou US$ 0 (Codex no historia-ptbr) | US$ 0–0,90 |
| Claude (escolha de trechos + build): cota do Max | US$ 0 direto |
| **Total** | **~US$ 0,05–1,10 por vídeo** (estimativa) |
Em Relevo: re-enquadrar a câmera 3D na vertical custa mais render (~25 min por Short de 45 s na VPS, segundo o relatório do canal-clima; no Runpod, minutos).

**Postagem automática:**
| Via | Requisitos | Risco |
|---|---|---|
| YouTube Data API (`videos.insert`) | OAuth (já temos tokens por canal). Revisão de 04/12/2025 baixou upload para ~100 unidades; desde 02/11/2026 projeto não verificado não sobe mais como privado [O](https://developers.google.com/youtube/v3/revision_history) (conferir antes de usar) | Link "Related video" do Short parece só no Studio [I]. Upload é decisão do Rodrigo (regra da fábrica) |
| Meta Graph (Reels FB / IG Content Publishing) | Página/conta profissional, app Meta com `pages_manage_posts` / `instagram_content_publish`; FB 30 Reels/24 h; IG 50–100/24 h; mídia em URL pública [O](https://developers.facebook.com/docs/instagram-platform/content-publishing/) | Volume repetido bate na regra de duplicado/não original |
| TikTok Content Posting API | App auditado; sem auditoria tudo fica privado (SELF_ONLY); ~15 posts/dia [O](https://developers.tiktok.com/doc/content-sharing-guidelines) 04/08/2026 | **Auditoria veta ferramenta interna** ("utility tools that upload only to accounts you manage") → inviável; só manual (TikTok Studio agenda 10–30 dias [I]) ou Buffer/Metricool (pago) |
| X API v2 | Pay-per-use desde 02/2026: US$ 0,015/post [O](https://docs.x.com/x-api/getting-started/pricing) | "Postagem automatizada" fica fora do Original Content Rewards [I] |
| Dailymotion API | OAuth `video.manage`; 15 vídeos e 10 h/dia [O](https://developers.dailymotion.com/guides/upload/) | Baixo; pede só `video.mp4` + `youtube.txt` |
| Kwai / Snapchat | Kwai sem API [I]; Snap Public Profile API só para parceiros [I](https://developers.snap.com/marketing-api/Public-Profile-API/Introduction) | Manual pelo celular/web |

**Tempo manual (estimativa):** subir 1 corte já pronto com título/legenda copiados de um arquivo: ~2–3 min por plataforma. 16 vídeos/semana × 3 cortes × 1 plataforma ≈ 48 posts ≈ **2 h/semana por plataforma**; com 3 plataformas, ~6 h/semana. Por isso automação ou foco em 1 plataforma é obrigatório.

## 5. Recomendação
**Teste 1 (agora, US$ ~5 no total): YouTube Shorts em 2 canais, 30 dias.**
- Canais: **lugares-guerra-en** (público EUA, RPM alto) e **em-relevo** (demanda de Shorts de clima em pt comprovada).
- Volume: 2 cortes por vídeo longo novo (60–120 s, arco completo, legenda queimada, "Related video" para o longo) ≈ 16 Shorts/canal em 30 dias. Nada em massa (regra de inautêntico).
- Sucesso: ≥ 1 Short ≥ 10 mil views **e** views dos longos do canal acima da mediana dos 30 dias anteriores **ou** +100 inscritos vindos de Shorts (Studio → origem dos inscritos).
- Parada: todos os Shorts < 1 mil views após 30 dias, ou retenção/views dos longos caem.
- Precisa: etapa `cortes-verticais` na esteira (job de dev, Sonnet) e 2–3 min por Short de upload manual (ou upload por API, se o Rodrigo liberar).

**Teste 2 (opcional, US$ 0): Dailymotion com o vídeo longo como está**, 1 canal en (Clearance) ou os 4, 30 dias, por API. Sucesso: perfil chega a 1.000 views e paga algo; parada: < 1.000 views em 30 dias. Antes: o Rodrigo confirmar no Studio se conta brasileira entra na Tipalti/partner terms.

**Depois (gatilho, não agora): Facebook**, quando algum canal tiver **20 mil seguidores** em YT/IG/TikTok e 30 mil views/30 d → Creator Fast Track Brasil (pequeno, US$ 75 garantidos, mas é a porta de entrada ao convite). Começar pelo historia-ptbr ou em-relevo (público BR forte no FB, conteúdo original nosso).

**O que NÃO vale a pena agora e por quê:**
- **Kwai:** exige "original" no sentido de gravado pelo criador, exclui vídeos feitos de fotos e com hashtag, sem API, reputação ruim.
- **Snapchat:** 50 mil seguidores + 25 posts/mês e, desde 08/2026, não recomenda vídeo inteiramente de IA.
- **X:** Premium pago, 500 mil impressões verificadas, Brasil não confirmado, rótulo obrigatório em vídeo de guerra com IA, automação exclui do pagamento.
- **TikTok:** Brasil elegível, mas RPM do público BR/LatAm em centavos; reupload/slideshow com TTS cai em "unoriginal"; API própria não passa na auditoria (tudo manual). Só faz sentido com vertical nativo em en, quando houver um canal en com tração.
- **Instagram:** não paga por view no Brasil; serve só como vitrine para chegar aos 20 mil do Fast Track.
- **Shorts por dinheiro:** RPM BR/MX ~US$ 0,04/mil e, a partir de 02/2027, pool só com 10 mi views/90 d. Shorts valem só como descoberta.

## O que precisa do Rodrigo
1. Aprovar (ou não) o Teste 1: Shorts no Clearance e no Em Relevo por 30 dias → vira job de dev da etapa `cortes-verticais`.
2. Dizer se o upload dos Shorts fica manual (~2–3 min cada) ou se libera upload por API.
3. Dailymotion: se quiser, criar a conta e checar no Studio se conta brasileira consegue aceitar os Partner Terms/Tipalti (conta é decisão dele).

## Ressalvas
- Vários números de 2026 vieram de uma única fonte de imprensa/blog (X Original Content Rewards, Fast Track Brasil, mudança do YPP em 2027, mudança de cota da API do YouTube): conferir na página oficial antes de agir.
- Nenhuma plataforma publica RPM oficial; todas as faixas são estimativas de terceiros.
