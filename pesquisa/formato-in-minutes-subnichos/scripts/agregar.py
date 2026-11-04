"""Agrega a busca bruta: vídeos únicos com título no formato, canais e contagens."""
import json, re, os, sys, collections
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORMATO = re.compile(r"(entire|complete|whole|full)\s+history|in\s+\d+\s+min|em\s+\d+\s+min|en\s+\d+\s+min|in\s+\d+\s+minuten|"
    r"hist[óo]ria\s+(inteira|completa|entera)|toda\s+la\s+historia|histoire\s+(compl[èe]te|enti[èe]re)|toute\s+l.histoire|"
    r"(gesamte|komplette|ganze)\s+geschichte|rise\s+and\s+fall|ascens[ãa]o\s+e\s+queda|auge\s+y\s+ca[íi]da|ascension\s+et\s+(la\s+)?chute|aufstieg\s+und\s+fall", re.I)
vids = {}
for l in (l for fn in ("dados/busca_bruta.jsonl", "dados/busca_bruta2.jsonl") for l in open(os.path.join(BASE, fn))):
    r = json.loads(l)
    if not r.get("id"): continue
    v = vids.setdefault(r["id"], {**{k: r[k] for k in ("id","title","channel","channel_id","view_count","duration")}, "buscas": set()})
    v["buscas"].add((r["subnicho_busca"], r["lang"]))
    if (r.get("view_count") or 0) > (v.get("view_count") or 0): v["view_count"] = r["view_count"]
fmt = {k: v for k, v in vids.items() if v["title"] and FORMATO.search(v["title"])}
print("vídeos únicos", len(vids), "no formato", len(fmt), file=sys.stderr)
canais = collections.defaultdict(list)
for v in fmt.values(): canais[v["channel_id"]].append(v)
print("canais com vídeo no formato", len(canais), file=sys.stderr)
for v in fmt.values(): v["buscas"] = sorted(map(list, v["buscas"]))
json.dump(list(fmt.values()), open(os.path.join(BASE, "dados/videos_formato.json"), "w"), ensure_ascii=False, indent=0)
