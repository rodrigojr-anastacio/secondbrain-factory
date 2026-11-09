# Roteiros: regras gerais de escrita e de processo

> **Lente de apoio (não é regra):** antes de propor, passe a ideia pelas 5 condições de decisão por atalho em `conhecimento/decisao-do-clique.md` (09/11/2026).

> **Regras gerais. Regra de canal está em `canais/<slug>/biblia/` e sempre prevalece.** Estrutura, hook, capítulos, transições, fecho, tamanho e tom de cada canal estão em `canais/<slug>/biblia/roteiro.md`. Aqui só entra o que vale para **qualquer** canal.

**Como atualizar:** só aprendizado **comprovadamente geral** (vale em mais de um canal, ou é da ferramenta/processo). Aprendizado de um vídeo vai primeiro para a bíblia do canal dele. Cada entrada leva **data e fonte**; sem dado = **Hipótese**. Commit descritivo.

Última revisão: 2026-11-04 (caixinhas por canal: padrões de formato movidos para as bíblias; ver "O que saiu daqui").

---

## Regras gerais
**Faça**
- **Escreva para a fala:** frases de 4–14 palavras, vírgula onde se respira, "…" só na virada, números por extenso quando o TTS ler mal, tag de tom só onde a emoção muda. No A/B de 04/11, o texto reescrito para a fala reduziu a "musiquinha repetida" entre frases (repetição melódica 0,14 → 0,10) mais que qualquer parâmetro do Fish. [`canais/historia-ptbr/videos/003-ira/amostras-voz/LEIA.md`] Atenção: escrever para a fala **não** é escrever em fichas; a costura entre as partes é regra de cada bíblia.
- **Modele a referência, não copie:** mesma técnica, ritmo e beats, texto próprio no idioma do canal. Nunca traduza o texto de um concorrente. [BRIEF.md historia-ptbr 001; playbooks/produzir-video.md]
- **Estude a referência pela transcrição completa** (não só o hook) com `tools/transcrever.py`, nos vídeos do **canal-modelo da bíblia** (não de outro canal-modelo). [estudo de 04/11/2026]
- **Abra loops e pague todos**; todo loop aberto no hook tem payoff marcado no roteiro. [ETAPA1.md historia-ptbr 001; SCRIPT_FR.md lotr-fr 001]
- `roteiro.py` é a **fonte única**: gera `SCRIPT.md`, `blocos.json`, `cenas.json`, `STORYBOARD.md` e `storyboard.json` e valida as regras de reuso. Edite lá, nunca nos gerados. [ETAPA1.md historia-ptbr 001]
- Marque no `roteiro.py` os blocos que **abrem ideia nova** (`IDEIA` → `"ideia": true`) para o `build.py` dar a pausa certa. [ETAPA3.md historia-ptbr 001]
- Fato com fonte em `SOURCES.md`; estimativa dita como estimativa; fato não confirmado vai como `[PENDENTE]` com versão alternativa. Não trave por isso. [playbooks/produzir-video.md]
- **Estime a duração pelas palavras com o ritmo medido da voz do canal** (está na bíblia). Com o Fish por frase, ~140–143 palavras/min em pt-BR e es (historia-ptbr 003: 2.137 palavras = 15:18, ~140; dossie-es 001: 1.686 palavras = 11:46, ~143). Nos dois, o `roteiro.py` errou a estimativa em 2–5%: calibre o WPS com o último vídeo do canal. [ETAPA3.md historia-ptbr 003; RELATORIO.md dossie-es 001]

**Não faça**
- **Não aplique a estrutura de um canal em outro.** Erro de 04/11/2026: os capítulos-objeto do Archive in Minutes (molde do `dossie-es`) foram gravados aqui como regra e usados no Irã do `historia-ptbr`; o Rodrigo reprovou ("não tem cara de história, falta conexão entre as partes"). [`~/workspace/referencias/BRIEF-historia-003-v2.md`; `conhecimento/anti-padroes.md` §8]
- Não ponha capítulos fora de ordem na descrição: o YouTube exige ordem crescente a partir de 0:00 (no `out/description.txt` das cidades, "6:38" veio antes de "6:23"). [lotr-fr 001]

---

## Como medir (para qualquer canal)
- Retenção: `tools/report.py <canal> --retencao <ID>` (o Analytics atrasa 1–3 dias). Anote a retenção aos 30 s e 60 s (hook) e as quedas por capítulo; o resultado vai para a bíblia do canal.
- Duração × palavras: registre na tabela "Tamanho" da bíblia (palavras, blocos, duração final) a cada vídeo.

## O que saiu daqui em 2026-11-04 (e para onde foi)
- Estrutura do historia-ptbr até o 002 (hook + 8–9 capítulos, fio condutor, loops "guarde isso", tamanho 2.250–2.300 palavras, remodelar transcrição, ritmo HiM 195 ppm × nosso 135, evidências por vídeo) → `canais/historia-ptbr/biblia/roteiro.md`.
- "Estrutura nova do historia-ptbr a partir do 003" (capítulos-objeto falados, fim que é o título do próximo, CTA no meio, fecho que volta ao começo, narração no presente, rótulo em 1 de 2 planos) → **revogada no historia-ptbr**; é o molde Archive e foi para `canais/dossie-es/biblia/roteiro.md` (e o texto na tela para `canais/dossie-es/biblia/visual.md`).
- Linha "CIA dossie-es 001" da tabela de evidências (1.686 palavras, 11:46) e os "Aprendizados do piloto 001" do `canais/dossie-es/estilo.md` → `canais/dossie-es/biblia/roteiro.md`, `voz.md` e `visual.md`.
- Retenção do lotr-fr por duração e o fio condutor "la couronne" → `canais/lotr-fr/biblia/roteiro.md` e `titulo.md`.
