"""Busca ampla do formato "ENTIRE History of X in N Minutes" em outros nichos, via yt-dlp + WARP (0 unidade de cota).

Uso: tools/.venv/bin/python -I pesquisa/formato-in-minutes-subnichos/scripts/buscar.py
Saída: dados/busca_bruta.jsonl (uma linha por resultado: consulta, subnicho, ordem, vídeo).
"""
import json
import os
import subprocess
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
OUT = os.path.join(BASE, "dados", "busca_bruta.jsonl")
N = 30

TOPICOS = {
    "tecnologia": ["the internet", "apple", "microsoft", "google", "the iphone", "computers", "artificial intelligence",
                   "nvidia", "the smartphone", "social media", "tesla", "spacex"],
    "empresas_marcas": ["coca cola", "mcdonald's", "nike", "disney", "lego", "toyota", "ferrari", "ikea", "amazon",
                        "walmart", "pepsi", "starbucks", "rolex", "adidas"],
    "financas_economia": ["money", "the stock market", "banking", "bitcoin", "the federal reserve", "inflation",
                          "the economy", "wall street", "capitalism"],
    "ciencia_espaco": ["the universe", "physics", "chemistry", "the atom", "the nuclear bomb", "the space race", "nasa",
                       "evolution", "the earth", "mathematics", "astronomy"],
    "medicina_saude": ["medicine", "surgery", "vaccines", "the black death", "pandemics", "anesthesia", "dentistry",
                       "psychiatry", "pharmaceutical industry", "cancer"],
    "crime_mafia": ["the mafia", "the cartels", "the yakuza", "serial killers", "the fbi", "alcatraz", "pablo escobar",
                    "piracy", "the sinaloa cartel", "organized crime", "prisons", "drugs"],
    "esportes": ["football", "soccer", "the nba", "the olympics", "the world cup", "boxing", "the ufc", "formula 1",
                 "wrestling", "real madrid", "the nfl", "tennis"],
    "religioes": ["christianity", "islam", "buddhism", "judaism", "the catholic church", "the vatican", "the popes",
                  "mormons", "the knights templar", "the bible", "hinduism", "the freemasons"],
    "cidades": ["new york", "london", "paris", "istanbul", "tokyo", "las vegas", "berlin", "venice", "jerusalem",
                "constantinople", "dubai", "rio de janeiro"],
    "comida_bebida": ["pizza", "coffee", "sugar", "chocolate", "beer", "sushi", "bread", "salt", "wine", "spices",
                      "fast food"],
    "guerras_especificas": ["the vietnam war", "world war 1", "the korean war", "the hundred years war",
                            "the napoleonic wars", "the crusades", "the american civil war", "the falklands war",
                            "the thirty years war", "the gulf war", "afghanistan war", "the samurai"],
    "games": ["video games", "nintendo", "minecraft", "gta", "pokemon", "playstation", "call of duty", "xbox",
              "sega", "fortnite", "world of warcraft"],
    "musica": ["rock music", "hip hop", "heavy metal", "the beatles", "jazz", "k-pop", "punk", "rap", "eminem",
               "michael jackson"],
    "transporte_engenharia": ["aviation", "cars", "trains", "the titanic", "ships", "the boeing", "skyscrapers",
                              "submarines", "tanks"],
    "mitologia_lendas": ["greek mythology", "norse mythology", "egyptian mythology", "vampires", "the illuminati",
                         "witches"],
    "cultura_pop_midia": ["marvel", "dc comics", "star wars", "anime", "hollywood", "the simpsons", "youtube",
                          "the internet memes", "pixar"],
    "dinastias_familias": ["the rothschilds", "the medici", "the kennedys", "the habsburgs", "the british royal family"],
}

GENERICAS = {
    "en": ["the entire history of", "entire history of in minutes", "the entire history of in 10 minutes",
           "the rise and fall of explained", "explained in 10 minutes history", "complete history of in minutes",
           "the entire history of company", "the entire history of brand", "the entire history of sport",
           "the entire history of science", "the entire history of video game", "the entire history of band",
           "the entire history of food", "the entire history of city", "the entire history of war in minutes",
           "the entire history of religion", "the entire history of crime", "the entire history of medicine"],
    "pt": ["a história inteira de", "a história completa de em minutos", "história completa em minutos",
           "a história inteira da empresa", "a história completa do futebol", "a história completa da igreja",
           "a história completa da máfia", "ascensão e queda de", "história do em 10 minutos"],
    "es": ["la historia completa de en minutos", "toda la historia de en minutos", "la historia entera de",
           "auge y caída de", "historia de en 10 minutos", "la historia completa de la empresa"],
    "fr": ["l'histoire complète de en minutes", "toute l'histoire de en minutes", "l'histoire entière de",
           "l'ascension et la chute de", "l'histoire de en 10 minutes"],
    "de": ["die gesamte geschichte von in minuten", "die komplette geschichte von", "die ganze geschichte von",
           "aufstieg und fall von", "geschichte in 10 minuten"],
}

# filtro de URL do YouTube: este ano + ordenado por views (sp=CAMSAggF)
SP_ANO_VIEWS = "CAMSAggF"


def consultas():
    qs = []
    for sub, tops in TOPICOS.items():
        for t in tops:
            qs.append((sub, "en", f"entire history of {t} in minutes", "relevancia"))
    for lang, gs in GENERICAS.items():
        for g in gs:
            qs.append(("generica", lang, g, "relevancia"))
            qs.append(("generica", lang, g, "ano_views"))
    # versões pt/es para os subnichos (amostra de 3 tópicos por subnicho)
    for sub, tops in TOPICOS.items():
        for t in tops[:2]:
            qs.append((sub, "pt", f"a história inteira de {t} em minutos", "relevancia"))
            qs.append((sub, "es", f"la historia completa de {t} en minutos", "relevancia"))
    # recentes com tração por subnicho (este ano, por views)
    for sub, tops in TOPICOS.items():
        for t in tops[:4]:
            qs.append((sub, "en", f"entire history of {t}", "ano_views"))
    return qs


def rodar(item):
    sub, lang, q, ordem = item
    if ordem == "relevancia":
        alvo = f"ytsearch{N}:{q}"
    else:
        alvo = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=" + SP_ANO_VIEWS
    cmd = [YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--flat-playlist", "-J", "--playlist-end", str(N), alvo]
    for _ in range(2):
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode == 0:
            break
    if r.returncode != 0:
        return item, None, r.stderr[-200:]
    d = json.loads(r.stdout)
    vs = []
    for e in d.get("entries") or []:
        vs.append({k: e.get(k) for k in ("id", "title", "channel", "channel_id", "view_count", "duration")})
    return item, vs, None


def main():
    qs = consultas()
    print(len(qs), "consultas", file=sys.stderr)
    erros = 0
    with open(OUT, "w") as f, ThreadPoolExecutor(4) as ex:
        for (sub, lang, q, ordem), vs, err in ex.map(rodar, qs):
            if vs is None:
                erros += 1
                print("ERRO", q, err, file=sys.stderr)
                continue
            for i, v in enumerate(vs):
                f.write(json.dumps({"subnicho_busca": sub, "lang": lang, "q": q, "ordem": ordem, "pos": i, **v},
                                   ensure_ascii=False) + "\n")
    print("erros:", erros, file=sys.stderr)


if __name__ == "__main__":
    main()
