import json, os, glob
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = os.path.dirname(BASE)
d = {"gerado": "2026-11-12", "canais_metricas": json.load(open(BASE + "/dados/canais_metricas.json")), "classes": {k: v for k, v in json.load(open(BASE + "/dados/classes.json"))["cls"].items() if v},
     "stats_grupos": json.load(open(BASE + "/dados/stats.json")), "demanda_en": json.load(open(BASE + "/dados/demanda_en.json")), "demanda_idioma": json.load(open(BASE + "/dados/demanda_idioma.json")),
     "buscas": {os.path.basename(f): sum(1 for _ in open(f)) for f in glob.glob(BASE + "/dados/busca_*.jsonl")}, "ref": json.load(open(R + "/dados/ref_videos.json"))}
json.dump(d, open(R + "/dados.json", "w"), ensure_ascii=False)
print(os.path.getsize(R + "/dados.json"))
