#!/usr/bin/env python3
"""Gera out/youtube.txt (+ entrega/pacote/youtube.txt) do 016 MKUltra. Rodar na pasta do vídeo, depois do render."""
import json, subprocess
from pathlib import Path
V = Path(__file__).resolve().parent.parent
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(V / "out/video.mp4")],
                           capture_output=True, text=True).stdout.strip())
mm, ss = int(dur // 60), int(dur % 60)
var = json.load(open(V / "embalagem/variantes.json"))
cap = json.load(open(V / "qa/capitulos.json"))
def ts(t): return f"{int(t // 60)}:{int(t % 60):02d}"
tit = {"Hook": "Introducción: Huautla, 1956"}
lines = []
for c in cap:
    t = c["title"]
    if t in tit: t = tit[t]
    elif t.startswith("Cierre"): t = "Cierre: Los Niños Santos"
    else:
        n, nom = t.split(". ", 1); t = f"Expediente {n}: {nom}"
    lines.append(f"{ts(c['t'])} {t}")
thumbs = {
 "A": "thumb-A.jpg: cuatro hongos sagrados en pares sobre una hoja de plátano, una vela encendida y un paño bordado mazateco, «MKULTRA»",
 "B": "thumb-B.jpg: perfil de un científico de la CIA con el rostro en la sombra del sombrero, un saco de lona al hombro con «10 LIBRAS», adobe y magueyes",
 "C": "thumb-C.jpg: hoja mecanografiada sobre la bandera de Honduras, «stress» tachado y «deplore» a mano, rótulo «HONDURAS»",
}
out = [f"# Pacote de publicación · dossie-es 016 · MKUltra (puede ir al aire: según el día que elija Rodrigo; ventana sugerida: mié o vie) · duración {mm}:{ss:02d}", "",
       "## TESTAR E COMPARAR (títulos × thumbs)", "| par | título | padrão do título | thumb | padrão da thumb |", "|---|---|---|---|---|"]
for v in var:
    out.append(f"| {v['letra']} (T{ 'ABC'.index(v['letra'])+1}) | {v['titulo'].replace('|', chr(92)+'|')} | {v['padrao_titulo']} | {thumbs[v['letra']]} | {v['padrao_thumb']} |")
out += ["", "## Descripción",
"Si te gustan estos expedientes, suscríbete, deja tu like y compártelo: abrimos uno nuevo cada semana.", "",
"Huautla de Jiménez, Oaxaca, verano de 1956: en la velada de María Sabina, un químico de Delaware mastica los hongos sagrados. Nadie en la casa sabe que el dinero del viaje salió de la CIA.",
"Esta es la historia completa de MKUltra contada por lo que la CIA vino a buscar a América Latina (las semillas de México, los hongos de Huautla, las plantas de la Amazonía) y por lo que dejó (los químicos del mismo servicio técnico para Fidel Castro y un manual en Honduras).", "",
"Capítulos"] + lines + ["",
"Fuentes",
"- John Marks, The Search for the \"Manchurian Candidate\" (1979), caps. 7, 11 y 12; documentos ARTICHOKE de 1952–53; adendo CIA BLUEBIRD/ARTICHOKE (29/1/1975).",
"- Comité Church, Alleged Assassination Plots Involving Foreign Leaders (1975), pp. 71–73; Informe Final, Libro I, pp. 385–422; audiencia del Senado del 3/8/1977; informe del inspector general de la CIA (26/7/1963).",
"- Life, «Seeking the Magic Mushroom» (13/5/1957); Álvaro Estrada, Vida de María Sabina (1976); Albert Hofmann, LSD: My Problem Child.",
"- Manual KUBARK (1963) y Human Resource Exploitation Training Manual – 1983 (National Security Archive, EBB 27/122); Baltimore Sun (11–18/6/1995 y 27/1/1997); Comisionado Nacional de Derechos Humanos de Honduras (1993); Alfred McCoy, A Question of Torture (2006).",
"Las acusaciones se atribuyen a sus fuentes; la CIA y los gobiernos citados las niegan o no las han confirmado. Contenido educativo e histórico; sin apología de la violencia.", "",
"## Etiquetas",
"MKUltra, CIA, historia de MKUltra, control mental, programa secreto de la CIA, María Sabina, Huautla, hongos sagrados, Fidel Castro, Honduras, manual KUBARK, Guerra Fría, servicios secretos, documental, expedientes secretos, América Latina", "",
"## Categoría e idioma", "Educación · español (es)", "",
"## CHECKLIST DE PUBLICACIÓN (para Rodrigo; fuera de la descripción)",
"- Studio → Atributos: Uso de IA = Sí; no es contenido para niños; idioma español.",
"- «Testar e comparar»: subir las 3 miniaturas y los 3 títulos pareados como arriba (thumb-A con título A, thumb-B con B, thumb-C con C); después avisar cuál ganó.",
"- Subir el mp4 1080p de entrega/ (nunca la versión de Telegram) y los subtítulos legendas.srt.",
"- Revisar de oído «Toughkenamon», «Geschickter», «KUBARK» y «fluothane» en la narración (respelling del Fish).",
"- Pendiente: revisión nativa independiente del español y verificar «Cameron en los papeles de 1977» (fuente secundaria)."]
txt = "\n".join(out) + "\n"
(V / "out/youtube.txt").write_text(txt)
(V / "entrega/pacote").mkdir(parents=True, exist_ok=True)
(V / "entrega/pacote/youtube.txt").write_text(txt)
print(f"youtube.txt ok, duração {mm}:{ss:02d}")
