# Referências visuais (10/11/2026)

**Acesso:** o Instagram exige login (perfil, API web e yt-dlp devolvem a página de login, com WARP ou sem). Os dois perfis publicam os mesmos vídeos no YouTube, então baixei de lá (via WARP) e extraí quadros com ffmpeg. Os arquivos ficaram em `work/refs/`, fora do git.
- **GeoGlobeTales** (@GeoGlobeTales): shorts *How Brazil Got Its Borders* (`_t8ujQL3xnY`), *New Orleans Flooding* (`iaeYlPNeZio`) e *Dingo Fence* (`iZS0b9U9UPs`).
- **HistóriAtenta** (@HistoriAtenta): longo *A História do Brasil em 15 minutos* (`1XrEFw4OcNM`) e shorts *Pangeia* (`lcIyGQ9smZo`) e *Irlanda* (`hUQyNZcNPk4`).

## O que eles fazem
| Item | HistóriAtenta (longo) | GeoGlobeTales |
|---|---|---|
| Terreno | satélite real (Esri World Imagery; o crédito "Tiles © Esri" fica no rodapé o tempo todo), com relevo dos Andes visível pela própria foto | dois modos: **pergaminho** (terra bege com textura de papel, mar verde-azulado com granulado) e **satélite** realista (Delta do Mississippi, Grandes Lagos) |
| Iluminação/sombra | só a do satélite, sem luz 3D; câmera quase de cima | plana; a profundidade vem de **nuvens volumétricas** que passam na frente e servem de transição e de vinheta |
| Relevo exagerado | não (2D) | não (2D); "3D" só nas nuvens e nos bonecos |
| Oceano | azul-petróleo escuro, com a **batimetria** visível (plataforma mais clara) | verde-azulado chapado (pergaminho) ou o azul real do satélite |
| Fronteiras | só a da região em foco: preenchimento **chapado e saturado** (vermelho, verde, bandeira) com **contorno branco** | contorno escuro fino; as regiões de interesse levam cor chapada (laranja/verde) |
| Rótulos | pílula amarela em caixa-alta (título do momento), alfinete vermelho com etiqueta amarela | faixa de papel com o nome; ano grande em serifa |
| Câmera | zoom lento e empurrões curtos entre regiões; corte seco entre eras | zoom e pan contínuos, entrando "através" das nuvens |
| Destaque da região | a região ganha cor forte e o resto continua satélite (mais escuro e menos saturado nas bordas, efeito de vinheta) | o resto fica escondido por nuvens escuras ou segue em tom neutro |
| Fotos | quadro tipo polaroid com legenda manuscrita, ~25–30% da tela, ao lado do alfinete | a foto ou cena **ocupa a tela inteira** por 1–2 s (corte), depois volta ao mapa |

## O que aproveitei
1. **Base real** no lugar do papel liso: satélite (A) ou relevo sombreado gerado de dado real (B, C).
2. **Batimetria visível** no oceano (é o que tira a cara de "chapado").
3. **Foco por vinheta no mundo**: o shader escurece e dessatura o terreno longe do alvo da câmera, então a região de interesse fica viva sem esforço de timeline.
4. **Região destacada = cor chapada drapeada no relevo** (as UFs tingidas do cap. 3 continuam, pintadas sobre o terreno).
5. **Fotos grandes**, como no GeoGlobe: 1240 px (65% da largura) sobre o mapa escurecido, com o crédito legível dentro da foto.
6. Rios (Natural Earth) para o zoom regional não ficar vazio, como os rios em linha azul do GeoGlobe.

Não copiei marca, personagens nem layout de nenhum dos dois; são ideias de linguagem (base real, foco, foto grande).
