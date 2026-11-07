# Thumbs v3: Irã (003), 3 estilos para o "Testar e comparar" (07/11/2026)

Vídeo no ar: "A história INTEIRA do Irã em 18 minutos". Pedido do Rodrigo em 07/11 (`~/workspace/referencias/BRIEF-historia-003-thumbs-v3.md`).

| Arquivo | Estilo | O que é |
|---|---|---|
| `thumb-1-him.jpg` | Pegada History in Minutes, fiel ao print | Panorama claro da Praça Naqsh-e Jahan (Isfahan): Mesquita do Xá com a cúpula azul e minaretes, Lotfollah, Ali Qapu, espelho d'água; sem boneco. Céu livre com "IRÃ" em serifa preta gigante + "4200 a.C. – 2026" (Susa/elamitas, N012, o ano mais antigo do roteiro) |
| `thumb-2-bonecos.jpg` | Bonecos (emoção + objeto do hook) | Dario piscando com sorriso malandro, o cavalo relinchando, os 5 nobres apontando chocados e o cavalariço escondendo a égua com o dedo na boca. "TRAPAÇA?" + "522 a.C." |
| `thumb-3-mapa.jpg` | Mapa-império brilhando | O império aquemênida aceso em ouro do Egito à Índia sobre mapa escuro, Dario de braços abertos "abraçando" o mapa, gregos pequenos e bravos no canto. "METADE DO MUNDO?" + "500 a.C." |

**Por que o 3 (mapa):** o "império gigante aceso no mapa" é o formato que mais puxa clique em história de impérios e cria uma pergunta de escala ("metade do mundo?", N005/N023, estimativa discutida, daí o "?"). É um 3º caminho real: nem panorama nem cena de personagem, e o escuro com ouro destoa do feed claro dos concorrentes.

Não repete os conflitos do v2 (COROA × TURBANTE, PÉRSIA × ROMA, PETRÓLEO × CIA).

## Técnica
- Bases: nano-banana-2.1/edit (fal) com as refs do `canal.yaml`, 2 tomadas por conceito (`cenas-thumbs-v3.json`, `base/`, fora do git). Escolhidas: `t1-him-isfahan-2`, `t2-bonecos-cavalo-1`, `t3-mapa-imperio-2`. Detector de moldura (`dossie-es/.../001-cia/tools/checa_imagens.py`): 0 suspeitas.
- Texto composto em PIL (`compose_v3.py`, fontes de `v2-amostras/thumbs/base/fonts/`). A base do Isfahan tinha pouco céu: o código empurra a cena 110 px para baixo e completa o topo com o degradê do céu (esticar o céu deixou emenda na cúpula; descartado).
- 1280×720, 172–225 KB; `prancha-celular.jpg` mostra a leitura a 320 px.
- Custo: US$ 0,277 (6 bases a US$ 0,046, real pelo uso do endpoint), `financas.consumo` ref_id 5, "thumbs v3 Irã".

Uso: na pasta do vídeo, `../../../../tools/.venv/bin/python entrega/thumbs-v3/compose_v3.py`.
