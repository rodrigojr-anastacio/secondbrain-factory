"""Demanda por nicho editorial: buscas nativas via yt-dlp + WARP (0 cota).
Ordens: relevancia (all-time), mes_views (sp=CAMSAggE), ano_views (sp=CAMSAggF).
Uso: buscar.py [nicho,...]  -> dados/busca.jsonl (append; pula consultas já feitas)"""
import json, os, sys, subprocess, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
N = 20
# nicho -> {lang: [consultas]}; en com 5 consultas centrais, demais idiomas com 2 nativas
Q = {
 "geo": {"en": ["geopolitics explained", "geography of russia explained", "why borders are so weird", "how geography shapes countries", "border dispute explained map"],
         "es": ["geopolítica explicada", "geografía explicada mapas"], "pt": ["geopolítica explicada", "geografia explicada no mapa"],
         "fr": ["géopolitique expliquée", "géographie expliquée carte"], "de": ["Geopolitik erklärt", "Geographie erklärt Karte"]},
 "desastre": {"en": ["natural disaster documentary", "deadliest disaster explained", "how hurricanes form", "worst flood in history", "volcano eruption documentary"],
              "es": ["desastres naturales documental", "peores desastres de la historia"], "pt": ["desastres naturais documentário", "maiores tragédias da história"],
              "fr": ["catastrophe naturelle documentaire", "pires catastrophes de l'histoire"], "de": ["Naturkatastrophe Doku", "schlimmste Katastrophen der Geschichte"]},
 "espaco": {"en": ["space documentary", "james webb telescope discoveries", "how big is the universe", "mars explained", "apollo moon landing documentary"],
            "es": ["documental del espacio", "el universo explicado"], "pt": ["documentário espaço universo", "o universo explicado"],
            "fr": ["documentaire espace univers", "l'univers expliqué"], "de": ["Weltraum Doku", "Universum erklärt"]},
 "mega": {"en": ["megaprojects explained", "how was it built engineering", "biggest engineering projects", "megastructures documentary", "how does a dam work"],
          "es": ["megaconstrucciones documental", "megaproyectos explicados"], "pt": ["megaconstruções documentário", "megaprojetos explicados"],
          "fr": ["mégastructures documentaire", "méga projets expliqués"], "de": ["Megabauten Doku", "Megaprojekte erklärt"]},
 "guerrafria": {"en": ["cold war documentary", "space race documentary", "cuban missile crisis explained", "history of nuclear weapons", "berlin wall history"],
                "es": ["guerra fría documental", "carrera espacial documental"], "pt": ["guerra fria documentário", "corrida espacial documentário"],
                "fr": ["guerre froide documentaire", "course à l'espace documentaire"], "de": ["Kalter Krieg Doku", "Wettlauf ins All Doku"]},
 "economia": {"en": ["economy explained", "why is this country so rich", "how inflation works explained", "economic collapse explained", "how this company makes money"],
              "es": ["economía explicada", "por qué este país es tan rico"], "pt": ["economia explicada", "por que esse país é tão rico"],
              "fr": ["économie expliquée", "pourquoi ce pays est si riche"], "de": ["Wirtschaft erklärt", "warum ist dieses Land so reich"]},
 "natureza": {"en": ["wildlife documentary", "animal facts documentary", "deadliest animals in the world", "amazon rainforest documentary", "animal migration documentary"],
              "es": ["documental de animales", "animales más peligrosos del mundo"], "pt": ["documentário de animais", "animais mais perigosos do mundo"],
              "fr": ["documentaire animalier", "animaux les plus dangereux du monde"], "de": ["Tierdoku", "gefährlichste Tiere der Welt"]},
 "truecrime": {"en": ["true crime documentary", "unsolved mysteries explained", "disappearance explained documentary", "biggest heist explained", "cold case documentary"],
               "es": ["crimen real documental", "misterios sin resolver"], "pt": ["caso criminal documentário", "mistérios não resolvidos"],
               "fr": ["affaire criminelle documentaire", "mystères non résolus"], "de": ["True Crime Doku", "ungelöste Rätsel"]},
 "cidades": {"en": ["why does this city exist", "why is this city so", "how this city grew", "country explained documentary", "why nobody lives here"],
             "es": ["por qué esta ciudad existe", "por qué nadie vive aquí"], "pt": ["por que essa cidade existe", "por que ninguém mora aqui"],
             "fr": ["pourquoi cette ville existe", "pourquoi personne ne vit ici"], "de": ["warum gibt es diese Stadt", "warum lebt hier niemand"]},
 "militar": {"en": ["aircraft carrier explained", "fighter jet explained", "military documentary", "battleship history documentary", "submarine explained"],
             "es": ["documental militar", "portaaviones explicado"], "pt": ["documentário militar", "porta-aviões explicado"],
             "fr": ["documentaire militaire", "porte-avions expliqué"], "de": ["Militär Doku", "Flugzeugträger erklärt"]},
 "escala": {"en": ["size comparison", "real size of", "scale of the universe", "how deep is the ocean", "how big is"],
            "es": ["comparación de tamaño", "el tamaño real de"], "pt": ["comparação de tamanho", "o tamanho real de"],
            "fr": ["comparaison de taille", "la vraie taille de"], "de": ["Größenvergleich", "wie groß ist wirklich"]},
 "oceano": {"en": ["deep sea documentary", "mariana trench explained", "deep ocean creatures", "titanic wreck explained", "what lies beneath the ocean"],
            "es": ["documental del fondo del mar", "fosa de las marianas explicada"], "pt": ["documentário fundo do mar", "fossa das marianas explicada"],
            "fr": ["documentaire fonds marins", "fosse des mariannes expliquée"], "de": ["Tiefsee Doku", "Marianengraben erklärt"]},
 "acidentes": {"en": ["plane crash explained", "air crash investigation documentary", "industrial disaster explained", "engineering disaster explained", "train crash explained"],
               "es": ["accidente aéreo explicado", "desastre industrial explicado"], "pt": ["acidente aéreo explicado", "desastre industrial explicado"],
               "fr": ["crash aérien expliqué", "catastrophe industrielle expliquée"], "de": ["Flugzeugabsturz erklärt", "Industriekatastrophe erklärt"]},
 "historia20": {"en": ["20th century history documentary", "archival footage history", "what really happened in 1969", "history of the atomic bomb", "great depression explained"],
                "es": ["historia del siglo xx documental", "imágenes de archivo historia"], "pt": ["história do século xx documentário", "imagens de arquivo história"],
                "fr": ["histoire du xxe siècle documentaire", "images d'archives histoire"], "de": ["Geschichte 20. Jahrhundert Doku", "Archivaufnahmen Geschichte"]},
}

# finalistas: mais consultas nativas por idioma (rodada 2)
Q2 = {
 "economia": {"en": ["why is this country so poor", "economic history explained", "currency crisis explained", "resource curse explained"],
              "es": ["por qué este país es pobre", "historia económica explicada", "crisis económica explicada", "maldición de los recursos"],
              "pt": ["por que esse país é pobre", "história econômica explicada", "crise econômica explicada"],
              "fr": ["pourquoi ce pays est pauvre", "histoire économique expliquée", "crise économique expliquée"],
              "de": ["warum ist dieses Land so arm", "Wirtschaftsgeschichte erklärt", "Wirtschaftskrise erklärt"]},
 "mega": {"en": ["how it was built", "why it doesn't collapse engineering", "engineering explained", "how does this bridge work"],
          "es": ["cómo se construyó", "por qué no se cae", "ingeniería explicada", "cómo funciona este puente"],
          "pt": ["como foi construído", "por que não cai", "engenharia explicada"],
          "fr": ["comment a été construit", "ingénierie expliquée", "pourquoi il ne s'effondre pas"],
          "de": ["wie wurde gebaut", "Ingenieurskunst erklärt", "warum stürzt es nicht ein"]},
 "militar": {"en": ["how it actually worked military", "cold war weapons explained", "battleship explained", "nuclear submarine explained"],
             "es": ["cómo funcionaba realmente", "armas de la guerra fría", "acorazado explicado", "submarino nuclear explicado"],
             "pt": ["como funcionava de verdade", "armas da guerra fria", "submarino nuclear explicado"],
             "fr": ["comment ça fonctionnait vraiment", "cuirassé expliqué", "sous-marin nucléaire expliqué"],
             "de": ["wie funktionierte eigentlich", "Schlachtschiff erklärt", "Atom-U-Boot erklärt"]},
 "espaco": {"en": ["what nasa found", "black hole explained", "voyager explained", "solar system explained"],
            "es": ["lo que encontró la nasa", "agujero negro explicado", "sistema solar explicado", "la sonda voyager"],
            "pt": ["o que a nasa encontrou", "buraco negro explicado", "sistema solar explicado"],
            "fr": ["ce que la nasa a trouvé", "trou noir expliqué", "système solaire expliqué"],
            "de": ["was die NASA gefunden hat", "schwarzes Loch erklärt", "Sonnensystem erklärt"]},
}
for n, d in Q2.items():
    for l, lst in d.items():
        Q[n][l] = Q[n][l] + lst
SP = {"relevancia": "", "mes_views": "&sp=CAMSAggE", "ano_views": "&sp=CAMSAggF"}
def rodar(item):
    nicho, lang, q, ordem = item
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + SP[ordem]
    for _ in range(3):
        try:
            r = subprocess.run([YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--extractor-args", f"youtube:lang={lang}", "--flat-playlist", "-J",
                                "--playlist-end", str(N), url], capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            continue
        if r.returncode == 0:
            return item, [{k: e.get(k) for k in ("id", "title", "channel", "channel_id", "view_count", "duration")} for e in json.loads(r.stdout).get("entries") or []]
    return item, None
if __name__ == "__main__":
    nichos = sys.argv[1].split(",") if len(sys.argv) > 1 else list(Q)
    arq = os.path.join(BASE, "dados", "busca.jsonl")
    feitos = set()
    if os.path.exists(arq):
        for l in open(arq):
            r = json.loads(l); feitos.add((r["nicho"], r["lang"], r["q"], r["ordem"]))
    qs = [(n, l, q, o) for n in nichos for l, lst in Q[n].items() for q in lst for o in SP if (n, l, q, o) not in feitos]
    erros = 0
    with ThreadPoolExecutor(6) as ex, open(arq, "a") as f:
        for (nicho, lang, q, ordem), res in ex.map(rodar, qs):
            if res is None:
                erros += 1; print("ERRO", nicho, lang, q, ordem, file=sys.stderr); continue
            for pos, e in enumerate(res):
                f.write(json.dumps({"nicho": nicho, "lang": lang, "q": q, "ordem": ordem, "pos": pos, **e}, ensure_ascii=False) + "\n")
            f.flush()
    print(len(qs), "consultas,", erros, "erros")
