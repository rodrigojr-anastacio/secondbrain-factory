# Thumbs cine D/E/F · dossie-es 013 Núremberg (21/11/2026)

Pedido do Rodrigo: 3 thumbs extras no estilo "pôster de cinema" das refs do filme *Nuremberg* (2025) em `refs/` (40, 41, 42).
**Desvio da bíblia pedido pelo dono** (fotorrealista em vez de graphic novel, sem aba "EXPEDIENTE", rosto de Göring, que o crivo da embalagem tinha reprovado). Status: **Hipótese**, medir no "Testar e comparar".

## Arquivos
- `thumb-D.jpg`, `thumb-E.jpg`, `thumb-F.jpg` (1280×720, 160–210 KB), `prancha.jpg` (atuais A/B/C + D/E/F a 320×180 e 160×90, e D/E/F entre as thumbs de `embalagem/thumbs`)
- `compose.py` (texto no código: "NÚREMBERG" em Cinzel Black, OFL, `pesquisa/reembalagem-2026-11-14/thumbs/fonts/Cinzel.ttf`; degradê creme→dourado, sombra suave, grão, vinheta; limpeza do patch do PM no E)
- `gerar_bases.py` + `cenas-r1.json` / `cenas-r2.json` (prompts), bases em `bases/` (D1/E1/F1 = r1 descartadas; D2/E2/F2 = finais)
- Crivo: `crivo-r1.md`, `crivo-r2.md`

## Modelo e custo
`google/nano-banana-2.1` (texto→imagem, 16:9, 2K = 2752×1536), sem o estilo do canal.yaml. 6 imagens, **US$ 0,414** (real pelo uso do endpoint), registrado em `financas.consumo` com `ref_id` 53. Teto US$ 1,50.

## As 3 thumbs
| thumb | composição | título que casa | crivo r2 |
|---|---|---|---|
| **F** | banco dos réus, Göring de fones na frente (túnica sem insígnias), 2 réus atrás na sombra, título no alto | novo: "Núremberg: el juicio que tuvo que inventar hasta las palabras" (61 car.), ou T3 | **8** · aprovada c/ condição (aplicado: título subiu e foi à esquerda, rosto clareado) |
| **D** | close de Göring à direita, túnica sem insígnias, fones no pescoço, título no alto à esquerda | T1 | **6,5** · aprovada c/ condição (aplicado: título saiu da linha dos olhos; não aplicado: tira de couro atrás do pescoço) |
| **E** | de dentro do banco dos réus, por trás de um réu com fones, rumo à bancada dos juízes; PM de capacete branco | T3 | **6** · aprovada c/ condição (aplicado: patch com bandeira francesa pintado liso, barra preta da base cortada, bordas escurecidas; não aplicado: PM menor) |

r1 → r2: o crivo r1 reprovou o E (cópia elemento a elemento da capa da trilha, ref 42, e cena que não aconteceu: réu de pé com fotógrafos disparando flash) e pediu túnica sem insígnias (é como Göring estava no julgamento; dragonas/golas douradas puxavam o figurino do filme) e título maior (Cinzel Bold espaçada sumia a 160×90).

## Recomendação do crivo
- **F no lugar da B** no "Testar e comparar" (a B, sem texto, é a mais fraca a 160×90), com o título novo; manter A e C. D e F competem entre si (mesmo rosto): só uma no teste. E fica de reserva.
- Pessoa real em cena realista: marcar **"Uso de IA = Sim"** no Studio.
- Risco: o pacote parecer material do filme; se vencer, olhar a retenção dos primeiros 30 s.
- Pendente (fora do escopo deste job, que só podia tocar `thumbs-extra/`): registrar o desvio como Hipótese em `canais/dossie-es/biblia/thumb.md`.

## Drive
`gdrive:Youtube/Dossier en Minutos/013-nuremberg/thumbs-cine/` (thumb-D/E/F + prancha). A pasta do vídeo não existia mais no Drive (o canal aparece vazio para o rclone, scope drive.file); foi criada só `013-nuremberg/thumbs-cine`.
