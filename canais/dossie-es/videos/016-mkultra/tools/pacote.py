#!/usr/bin/env python3
"""Gera out/youtube.txt (+ entrega/pacote/youtube.txt) do 015 GRU. Rodar na pasta do vídeo, depois do render."""
import json, subprocess
from pathlib import Path
V = Path(__file__).resolve().parent.parent
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(V / "out/video.mp4")],
                           capture_output=True, text=True).stdout.strip())
mm, ss = int(dur // 60), int(dur % 60)
var = json.load(open(V / "embalagem/variantes.json"))
cap = json.load(open(V / "qa/capitulos.json"))
def ts(t): return f"{int(t // 60)}:{int(t % 60):02d}"
tit = {"Hook": "Introducción: el uruguayo que no lo era"}
lines = []
for c in cap:
    t = c["title"]
    if t in tit: t = tit[t]
    elif t.startswith("Cierre"): t = "Cierre: El Pasaporte"
    else:
        n, nom = t.split(". ", 1); t = f"Expediente {n}: {nom}"
    lines.append(f"{ts(c['t'])} {t}")
thumbs = {
 "A": "thumb-A.jpg: matrioska abierta (cáscara de empresario de traje blanco y panamá, dentro una muñeca de oficial soviético), «GRU» + sello «GULAG»",
 "B": "thumb-B.jpg: noche en la pista, Putin en primer plano estrecha la mano de un hombre, sello «¿BRASILEÑO?»",
 "C": "thumb-C.jpg: tres pasaportes en abanico vistos desde arriba, ventana de la foto vacía, sello «NUNCA NACIERON»",
}
out = [f"# Pacote de publicación · dossie-es 015 · El GRU (puede ir al aire: según el día que elija Rodrigo; ventana sugerida: lun o mié) · duración {mm}:{ss:02d}", "",
       "## TESTAR E COMPARAR (títulos × thumbs)", "| par | título | padrão do título | thumb | padrão da thumb |", "|---|---|---|---|---|"]
for v in var:
    out.append(f"| {v['letra']} (T{ 'ABC'.index(v['letra'])+1}) | {v['titulo']} | {v['padrao_titulo']} | {thumbs[v['letra']]} | {v['padrao_thumb']} |")
out += ["", "## Descripción",
"Si te gustan estos expedientes, suscríbete, deja tu like y compártelo: abrimos uno nuevo cada semana.", "",
"Bruselas, 1941: un joven empresario uruguayo dirige una empresa de importación y exportación, y su mejor cliente es la organización que construye para el régimen nazi. En los papeles es un hombre de negocios más. Pero su pasaporte se emitió en Nueva York y la persona que lo lleva no es quien dice ser.",
"Esta es la historia completa del GRU, la inteligencia militar rusa, contada a través de los latinoamericanos falsos que, según gobiernos e investigadores, fabricó: un uruguayo, una peruana, dos brasileños.", "",
"Capítulos"] + lines + ["",
"Fuentes",
"- CIA, Kesaris (ed.), The Rote Kapelle (1979); UK National Archives KV 2/2068; Rossiyskaya Gazeta (2004); Volodarsky (2015); Firsov, Klehr y Haynes, Secret Cables of the Comintern.",
"- Rose y Scott, Johnny: A Spy's Life (2010), a través de reseñas de FPA, Project MUSE y MercoPress.",
"- Fursenko y Naftali, One Hell of a Gamble (1997); nota de Dobrynin del 5/11/1962 (Wilson Center); Departamento de Estado de EE. UU. (history.state.gov); CIA Reading Room.",
"- FAS (irp.fas.org), Jamestown Foundation sobre la base de Lourdes; Casa Blanca (17/10/2001).",
"- El Independiente (13/3/2018); The Times; informe de la investigación Dawn Sturgess (4/12/2025).",
"- Bellingcat, The Insider, Der Spiegel y La Repubblica (25/8/2022); Bellingcat y AIVD (16/6/2022); AFP/Moscow Times (29/3/2023).",
"- Departamento de Justicia de EE. UU. (USAO-DC, 24/3/2023); CBS; The New York Times (21/5/2025); Barents Observer (14/12/2023); Bellingcat/VG.",
"- Meduza (1/8/2024); Novaya Gazeta Europe (2/8/2024); Mexico News Daily; NBC (21/9/2024); Irish Times (4/12/2025); RFE/RL; Correio Braziliense.",
"Las acusaciones se atribuyen a sus fuentes; el GRU y los gobiernos citados las niegan o no las han confirmado. Contenido educativo e histórico; sin apología de la violencia.", "",
"## Etiquetas",
"GRU, espionaje, inteligencia militar rusa, espías rusos, historia del GRU, servicios secretos, espías, Rusia, Guerra Fría, KGB, documental, expedientes secretos, identidades falsas, latinoamericanos, historia de espionaje", "",
"## Categoría e idioma", "Educación · español (es)", "",
"## CHECKLIST DE PUBLICACIÓN (para Rodrigo; fuera de la descripción)",
"- Studio → Atributos: Uso de IA = Sí; no es contenido para niños; idioma español.",
"- «Testar e comparar»: subir las 3 miniaturas y los 3 títulos pareados como arriba (thumb-A con título A, thumb-B con B, thumb-C con C); después avisar cuál ganó.",
"- Subir el mp4 1080p de entrega/ (nunca la versión de Telegram) y los subtítulos legendas.srt.",
"- Revisar de oído el nombre «Vincente» y la sigla GRU (ge-erre-u) en la narración."]
txt = "\n".join(out) + "\n"
(V / "out/youtube.txt").write_text(txt)
(V / "entrega/pacote").mkdir(parents=True, exist_ok=True)
(V / "entrega/pacote/youtube.txt").write_text(txt)
print(f"youtube.txt ok, duração {mm}:{ss:02d}")
