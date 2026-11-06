# Identidade visual: História em Minutos (historia-ptbr), 06/11/2026

## Arquivos para subir (YouTube Studio → Personalização → Branding)
| Arquivo | O que é |
|---|---|
| `logo-1.png` | **Recomendado.** Bonequinho do canal abraçando uma ampulheta de areia dourada, fundo ouro #F7C21B. O mais legível a 48 px (cabeça branca + ampulheta) |
| `logo-2.png` | Bonequinho de coroa dourada segurando um pergaminho aberto (com uma ampulheta pequena desenhada), fundo terracota. A 48 px o boneco fica menor |
| `logo-3.png` | Ampulheta com um globo antigo no bulbo de cima e areia dourada caindo; o bonequinho espia acenando por trás. Fundo azul-marinho; a silhueta da ampulheta lê bem pequena, o boneco não |
| `capa-1.png` | Desfile das eras (faraó, imperador indiano, rei persa, imperador chinês, legionário, viking, cavaleiro, navegador, pessoa de hoje) com pirâmides, Taj Mahal, Persépolis, Muralha e Coliseu no horizonte; placa de papiro com o título |
| `capa-2.png` | Livro aberto com o "mundinho da história" (pirâmides, Taj Mahal, templo) saindo das páginas, bonequinhos de várias eras dos dois lados, céu de pôr do sol; título em 2 linhas |
| `previa-logos.jpg` | Os 3 logos em círculo a 300, 98 e 48 px (e 48 px no tema escuro), só para conferência |
| `previa-capas.jpg` | Cada capa como TV (imagem inteira, com a área segura em verde e a faixa do desktop em amarelo), desktop (2560×423), celular (1546×423) e celular real (~360 px) |

- Logos 800×800 (o YouTube corta em círculo), **nenhuma letra**. Capas 2560×1440 PNG (~3–4 MB, < 6 MB); título e tagline só dentro da área segura 1546×423 (o `compor.py` falha se sair).
- Texto composto no código: **"HISTÓRIA EM MINUTOS"** em Libre Caslon 700 tinta escura sobre placa de papiro claro com sombra chapada (o mesmo cartão das placas do vídeo), "MINUTOS" em ouro #F7C21B com contorno; tagline **"A história inteira de cada país, contada em minutos"** em Open Sans 800 numa pílula ouro (a mesma das datas das thumbs).
- Conferido com visão: todos os personagens com cabeça redonda branca, nenhuma letra inventada pela IA (o livro da capa-2 tem só linhas onduladas; o mapa do navegador, só contorno).

## Como refazer
- `tools/gerar.py` gera as bases sem texto em `base/` (fal `google/nano-banana-2.1/edit` com as 3 refs de estilo do `canal.yaml` + `videos/004-china/imagens/I010.jpg`; logos 1:1 em 1K, capas 16:9 em 2K = 2752×1536), 2 tomadas por conceito, pula o que já existe, trava no teto e registra o custo real (uso do endpoint) em `financas.consumo` (`projeto=fabrica`, `ref_tipo=youtube.canal`, notas "identidade historia-ptbr").
- `tools/compor.py` faz os finais e as prévias a partir de `base/` e `fontes/` (Libre Caslon Text e Open Sans, OFL). Grátis. Escolhidas: logo-a-1, logo-b-2, logo-c-1, capa-a-1, capa-b-2 (as outras tomadas ficam em `base/`).
- Aprendizado: no 1:1 o nano-banana-2.1 com refs entrega o ícone já sobre fundo chapado (sem o círculo sobre branco que o nano-banana v1 desenhou no dossie-es) e sem moldura; só precisa de zoom para ocupar o círculo. No 16:9 a capa sai como cena inteira: o título fica na faixa central (onde estão os marcos/céu) e os bonequinhos aparecem do peito para cima no celular. Na tomada capa-a-2 a "pessoa de hoje" saiu com rosto comum (cabelo, sem cabeça redonda): conferir sempre o personagem moderno.

## Custo
10 imagens (6 logos + 4 capas, 2 tomadas cada), **US$ 0,559** (real, uso do endpoint), sem refação.
