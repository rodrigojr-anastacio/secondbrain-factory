# Em Relevo 005: rios da Região Hidrográfica do Guaíba (OSM, ODbL) -> shared/rios.json
# 1) liga cada trecho ao seguinte pelo nó de foz (OSM orienta a linha na direção da água) e sobe a partir do Guaíba (BFS contra a corrente);
# 2) classifica: 5 principais (Jacuí, Taquari-Antas, Caí, Sinos, Gravataí), afluentes nomeados e o resto; 3) distância à foz (m) por vértice, para a árvore crescer "convergindo".
# Uso: python3 prepara_rios.py   (precisa de dados/rios-osm.json, fora do git)
import json, math, collections
from pathlib import Path
R = Path(__file__).resolve().parent.parent
d = json.load(open(R / "dados/rios-osm.json"))["elements"]
ways = {e["id"]: e for e in d if e.get("geometry") and len(e["geometry"]) > 1}
for w in ways.values(): w["nodes"] = [(p["lon"], p["lat"]) for p in w["geometry"]]   # a saída "out geom" não traz ids de nó: a coordenada exata faz o papel
node_ways = collections.defaultdict(set)
for w in ways.values():
    for n in w["nodes"]: node_ways[n].add(w["id"])
def hav(a, b):
    la = math.radians((a[1] + b[1]) / 2); return math.hypot((a[0] - b[0]) * math.cos(la), a[1] - b[1]) * 111.2
# sementes: trechos nomeados que passam perto da foz no Guaíba (lago a oeste/norte de Porto Alegre) — Jacuí (delta), Sinos, Caí, Gravataí
FOZ = (-51.27, -29.99)
sem = []
for w in ways.values():
    nome = w["tags"].get("name", "")
    if any(k in nome for k in ("Jacuí", "Sinos", "Caí", "Gravataí")) and any(hav((p["lon"], p["lat"]), FOZ) < 14 for p in w["geometry"]): sem.append(w["id"])
print("sementes", len(sem), [ways[i]["tags"].get("name") for i in sem])
dist = {}   # id -> distância (km) da foz até o fim (jusante) do trecho
fila = collections.deque()
for i in sem: dist[i] = 0.0; fila.append(i)
EXCLUI = ("Ibicuí", "Ijuí", "Uruguai", "Camaquã", "Passo Fundo", "Pelotas", "Inhandava", "Apuaê", "Forquilha", "Turvo", "Comandaí", "Piratini")
while fila:
    i = fila.popleft(); w = ways[i]
    L = sum(hav((a["lon"], a["lat"]), (b["lon"], b["lat"])) for a, b in zip(w["geometry"], w["geometry"][1:]))
    for n in w["nodes"]:
        for j in node_ways[n]:
            if j in dist: continue
            v = ways[j]
            if v["nodes"][-1] != n and v["nodes"][0] != n: pass
            if v["nodes"][-1] == n:   # v deságua em w neste nó
                if any(k in v["tags"].get("name", "") for k in EXCLUI): continue
                dist[j] = dist[i] + L; fila.append(j)
print("trechos na bacia", len(dist), "de", len(ways))
def classe(nome):
    for k, c in (("Jacuí", "jacui"), ("Taquari", "taquari"), ("das Antas", "taquari"), ("Caí", "cai"), ("Sinos", "sinos"), ("Gravataí", "gravatai")):
        if k in nome and "Mirim" not in nome and "zinho" not in nome and "Paranhana" not in nome: return c
    return None
out = []
for i, dd in dist.items():
    w = ways[i]; nome = w["tags"].get("name", ""); c = classe(nome)
    pts = [[round(p["lon"], 4), round(p["lat"], 4)] for p in w["geometry"]]
    # simplifica: remove pontos a < 0,012° do anterior
    s = [pts[0]]
    for p in pts[1:-1]:
        if math.hypot(p[0] - s[-1][0], p[1] - s[-1][1]) > 0.012: s.append(p)
    s.append(pts[-1])
    L = sum(hav(a, b) for a, b in zip(pts, pts[1:]))
    out.append({"n": nome, "c": c, "d0": round(dd + L, 1), "d1": round(dd, 1), "p": s})   # d0 = dist. da nascente do trecho, d1 = dist. da foz do trecho
# importância: contar quantos trechos a montante (para engrossar os médios)
cnt = collections.Counter()
for i, dd in dist.items(): pass
ex = {c: sum(1 for o in out if o["c"] == c) for c in ("jacui", "taquari", "cai", "sinos", "gravatai")}
print(ex, "sem classe:", sum(1 for o in out if not o["c"]), "dmax", max(o["d0"] for o in out))
json.dump(out, open(R / "shared/rios.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(len(json.dumps(out)) // 1024, "KB")
