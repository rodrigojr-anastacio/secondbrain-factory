# Storyboard V3 — versión de producción

**Estado:** implementación autorizada por Rodrigo. V1, V2, `script_fr.txt` y `public/assets/narration.wav` quedan preservados. Duración prevista: 61 s (locución de 60,55 s), 1920×1080, 30 fps.

## Enfoque

Hook inmediato: Frodo parte hacia el Oeste; Sam vuelve a casa; a los 102 años, Sam toma esa misma ruta. La voz deja respirar las pausas; los visuales siguen siendo dinámicos, pero sin hacer que cada frase compita con el texto. El montaje combina la foto licenciada de Hobbiton, fan art aprobada mostrada íntegra, fotos de libro y paisaje licenciadas, metraje de barco de dominio público y animación original.

## Beats

| Tiempo | Voz / intención | Imagen y movimiento | Rótulo |
|---|---|---|---|
| 00:00–00:03.8 | « Frodon a pris la mer vers l’Ouest. » Hook visual: la partida de Frodon | Insert breve del navire, corte rápido a la foto real de Bag End/Hobbiton; mapa de fondo | **FRODON PART VERS L’OUEST** |
| 00:03.8–00:07.4 | « Sam, lui, est rentré. À cent deux ans, pourquoi part-il à son tour ? » | Match-cut vers la porte ronde; silueta original de Sam vuelve y el contador marca 102 | **SAM EST RENTRÉ. PUIS IL EST REPARTI.** |
| 00:07.4–00:12 | Rosie, los hijos, el Libro Rojo | Fan art de Sam mostrada completa, intacta y con firma; iconos originales de Rosie/familia/libro | **ROSIE · LEURS ENFANTS · LE LIVRE ROUGE** |
| 00:12–00:14.97 | « Après plus de soixante ans ensemble… » | El Libro Rojo, paso de estaciones y push-in lento sobre la foto de Hobbiton | **UNE VIE ENSEMBLE** |
| 00:14.97–00:19.2 | « …Rosie meurt. » | El movimiento se detiene; jardín vacío, luz se atenúa y música baja antes de la pausa | **PUIS, ROSIE MEURT.** |
| 00:19.2–00:24.2 | « Le 22 septembre, Sam quitte Cul-de-Sac. » | Fecha escrita como **22 SEPTEMBRE 1482**; puerta y camino, plano corto | **IL QUITTE CUL-DE-SAC** |
| 00:24.2–00:28 | « Aux Collines des Tours… » | Mapa esquemático del oeste de Eriador; Comté → Marche de l’Ouest → Collines des Tours | **LA COMTÉ → COLLINES DES TOURS** |
| 00:28–00:32 | « …il confie le Livre à Elanor. » | El Libro pasa de Sam a Elanor; marcador en Emyn Beraid/Collines des Tours | **ELANOR REÇOIT LE LIVRE** |
| 00:32–00:36 | « Selon la tradition familiale… » | El mapa se abre; una ruta discontinua aparece después de las Collines des Tours | **SELON LA TRADITION FAMILIALE** |
| 00:36–00:40 | « …il rejoint les Havres Gris… » | El rótulo **HAVRES GRIS · MITHLOND** junto al golfo de Lhûn, en Lindon | **LINDON · GOLFE DE LHÛN** |
| 00:40–00:44.6 | « …traverse la mer — dernier Porteur de l’Anneau à partir. » | Barco de archivo de dominio público y olas CC0; plano corto, no presentado como imagen de la película | **LE DERNIER PORTEUR À PARTIR** |
| 00:44.6–00:49.6 | « Mais Tolkien ne raconte pas leurs retrouvailles. » | La ruta se pierde en la niebla; página abierta, sin mostrar un reencuentro inventado | **LE TEXTE NE RACONTE PAS LEURS RETROUVAILLES** |
| 00:49.6–00:53.8 | « Deux départs. Une vie entre eux. » | Dos líneas temporales, una larga vida en la Comté entre ambas partidas | **DEUX DÉPARTS. UNE VIE ENTRE EUX.** |
| 00:53.8–00:56.4 | Respiración antes de la pregunta | La música se reduce; horizonte y libro en reposo | **ET VOUS…** |
| 00:56.4–01:01 | « …vous imaginez qu’ils se sont retrouvés ? » | Pregunta final, sin nueva información; fundido lento | **VOUS IMAGINEZ LEURS RETROUVAILLES ?** |

## Geografía canónica

- Mapa esquemático, no a escala, centrado en el noroeste de la Terre du Milieu: La Comté al este; Marche de l’Ouest y Collines des Tours/Emyn Beraid al oeste; Lindon y les Havres Gris/Mithlond en el extremo oriental del golfe de Lhûn.
- Animar dos pasos distintos: Sam deja Bag End y es visto por última vez en las Collines des Tours; la continuación hacia Mithlond se marca con línea discontinua y el rótulo «selon la tradition familiale», no como una ruta detallada confirmada.
- El cruce de Belegaer se muestra en un panel separado: no dibujar Aman/Valinor como una isla vecina en el mapa del noroeste.
- No mostrar el reencuentro entre Sam y Frodo como hecho; el texto no lo narra.

## Voz, música e imágenes

- Locución V3 separada: `public/assets/v3/narration_v3.mp3`, generada a velocidad 0,88; duración medida 60,552 s. El proveedor Edge no admite instrucciones de interpretación emocional; por eso la locución no se presenta como una actuación humana aprobada. Las pausas se preservan y se apoyan con edición y música.
- Música original V3: `public/assets/v3/music_bed_v3.wav`, sin samples ni tema de Howard Shore; motivo folk-cinemático, más perceptible que la cama ambiental V2 y ducking bajo la voz.
- La solicitud de usar cortes de los largometrajes queda sin un archivo de fuente accesible: la descarga del clip oficial de YouTube pidió iniciar sesión. No se sortea ese control; el render usa imágenes licenciadas y animación propia. Si Rodrigo aporta clips autorizados, se pueden insertar en los beats 1, 2, 5 y 11.
- Fan art de Lucie Vergne se muestra completa, sin recortar, retocar ni recolorear; firma visible y crédito/licencia en pantalla y descripción.
