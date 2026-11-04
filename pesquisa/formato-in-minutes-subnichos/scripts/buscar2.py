"""Segunda passada: buscas dirigidas aos subnichos promissores, só vídeos recentes (este ano/este mês, por views).
Reaproveita rodar() de buscar.py. Saída: dados/busca_bruta2.jsonl"""
import json, os, sys, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "scripts"))
import buscar
T = {
 "empresas_marcas": ["coca-cola", "mcdonald's", "nike", "disney", "lego", "ikea", "amazon", "walmart", "starbucks", "nestle",
    "samsung", "sony", "netflix", "boeing", "ford", "porsche", "red bull", "kfc", "nokia", "blockbuster", "kodak", "enron",
    "harley davidson", "uber", "the company", "a company"],
 "tecnologia": ["the internet", "ai", "computers", "the iphone", "google", "microsoft", "nvidia", "social media", "openai",
    "intel", "the smartphone", "video", "cameras", "electricity", "the telephone", "robots", "hacking", "cybersecurity"],
 "financas_economia": ["money", "the stock market", "banking", "bitcoin", "crypto", "the dollar", "gold", "inflation",
    "debt", "the federal reserve", "wall street", "the economy", "taxes", "credit cards", "economic crises"],
 "comida_bebida": ["coffee", "sugar", "chocolate", "beer", "pizza", "the tomato", "salt", "spices", "tea", "wine", "bread",
    "fast food", "the potato", "whiskey", "rice"],
 "guerras_especificas": ["the vietnam war", "ww1", "ww2", "the korean war", "the cold war", "the crusades", "the napoleonic wars",
    "the gulf war", "the falklands war", "the hundred years war", "the american civil war", "the iraq war", "the six day war",
    "the spanish civil war", "the war of 1812", "the yom kippur war", "the iran iraq war"],
 "cidades": ["london", "paris", "new york city", "venice", "istanbul", "tokyo", "berlin", "las vegas", "chicago", "rio de janeiro",
    "sao paulo", "lisbon", "madrid", "barcelona", "amsterdam", "vienna", "moscow", "babylon"],
 "medicina_saude": ["medicine", "surgery", "vaccines", "anesthesia", "the plague", "pandemics", "psychiatry", "dentistry",
    "antibiotics", "cancer treatment", "drugs", "pharmacy"],
 "crime_mafia": ["the mafia", "the cartels", "the yakuza", "the fbi", "alcatraz", "the sicilian mafia", "the triads",
    "the medellin cartel", "piracy", "the cia drug", "scams", "the irish mob"],
 "esportes": ["football", "basketball", "the nba", "the olympics", "the world cup", "boxing", "the ufc", "formula 1",
    "the champions league", "the premier league", "baseball", "tennis", "chess", "the super bowl"],
 "games": ["video games", "nintendo", "playstation", "xbox", "sega", "minecraft", "gta", "pokemon", "call of duty",
    "valve", "atari", "arcade games", "esports"],
 "musica": ["rock and roll", "hip hop", "heavy metal", "jazz", "the beatles", "k-pop", "punk", "electronic music",
    "country music", "reggae", "mtv", "the record industry"],
 "religioes": ["christianity", "islam", "buddhism", "judaism", "the catholic church", "the bible", "the vatican", "the popes",
    "hinduism", "the knights templar"],
 "ciencia_espaco": ["the universe", "the earth", "the space race", "nasa", "physics", "chemistry", "nuclear weapons",
    "the atomic bomb", "evolution", "dinosaurs", "mathematics", "the moon landing"],
 "transporte_engenharia": ["aviation", "cars", "trains", "ships", "submarines", "tanks", "rockets", "the titanic"],
}
SPS = {"ano_views": "CAMSAggF", "mes_views": "CAMSAggE"}
def rodar2(item):
    sub, q, ordem = item
    alvo = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=" + SPS[ordem]
    import subprocess
    cmd = [buscar.YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--flat-playlist", "-J", "--playlist-end", "25", alvo]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if r.returncode != 0: return item, None
    return item, [{k: e.get(k) for k in ("id", "title", "channel", "channel_id", "view_count", "duration")} for e in json.loads(r.stdout).get("entries") or []]
qs = []
for sub, ts in T.items():
    for t in ts:
        qs.append((sub, f"the entire history of {t}", "ano_views"))
for q in ["the entire history of in minutes", "the ENTIRE history of", "entire history of explained", "a história inteira de",
          "a história completa de em minutos", "la historia completa de en minutos", "toda la historia de en minutos",
          "l'histoire complète de en minutes", "die ganze geschichte in minuten", "the complete history of in minutes",
          "the entire history of company", "the entire history of brand", "the entire history of war", "the entire history of city"]:
    qs.append(("generica", q, "mes_views")); qs.append(("generica", q, "ano_views"))
print(len(qs), "consultas", file=sys.stderr)
with open(os.path.join(BASE, "dados/busca_bruta2.jsonl"), "w") as f, ThreadPoolExecutor(4) as ex:
    for (sub, q, ordem), vs in ex.map(rodar2, qs):
        if vs is None: print("ERRO", q, file=sys.stderr); continue
        for i, v in enumerate(vs):
            f.write(json.dumps({"subnicho_busca": sub, "lang": "multi", "q": q, "ordem": ordem, "pos": i, **v}, ensure_ascii=False) + "\n")
