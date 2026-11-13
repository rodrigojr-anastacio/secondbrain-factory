# Tracado aproximado das ferrovias historicas a partir de trilhos OSM (em uso/abandonados): menor caminho entre estacoes
import json, heapq, math
d = json.load(open("dl/dados/trilhos_osm.json"))
def build(els):
    G = {}
    k = lambda p: (round(p["lon"], 5), round(p["lat"], 5))
    for e in els:
        g = e["geometry"]
        for a, b in zip(g, g[1:]):
            ka, kb = k(a), k(b); w = math.hypot((ka[0]-kb[0])*0.99, ka[1]-kb[1])
            G.setdefault(ka, {})[kb] = w; G.setdefault(kb, {})[ka] = w
    ends = []
    for e in els:
        g = e["geometry"]; ends += [k(g[0]), k(g[-1])]
    ends = list(set(ends))
    for i, a in enumerate(ends):
        for b in ends[i+1:]:
            w = math.hypot(a[0]-b[0], a[1]-b[1])
            if w < TOL and b not in G.get(a, {}): G[a][b] = w + 0.0005; G[b][a] = w + 0.0005
    return G
TOL = 0.004
def near(G, lon, lat): return min(G, key=lambda p: math.hypot(p[0]-lon, p[1]-lat))
def path(G, a, b):
    dist = {a: 0}; prev = {}; pq = [(0, a)]
    while pq:
        dd, u = heapq.heappop(pq)
        if u == b: break
        if dd > dist[u]: continue
        for v, w in G[u].items():
            if dd + w < dist.get(v, 9e9): dist[v] = dd + w; prev[v] = u; heapq.heappush(pq, (dd + w, v))
    if b not in prev and a != b: return None
    out = [b]
    while out[-1] != a: out.append(prev[out[-1]])
    return out[::-1]
def simp(pts, eps):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1e-9
    i, dm = 0, 0
    for j in range(1, len(pts)-1):
        dj = abs(dy*pts[j][0] - dx*pts[j][1] + b[0]*a[1] - b[1]*a[0]) / L
        if dj > dm: i, dm = j, dj
    return simp(pts[:i+1], eps)[:-1] + simp(pts[i:], eps) if dm > eps else [a, b]
res = {}
for nome, seq in {"baturite": [("Fortaleza", -38.5336, -3.7226), ("Parangaba", -38.5658, -3.7766), ("Baturite", -38.8845, -4.3295), ("Quixada", -39.0148, -4.9717), ("Senador Pompeu", -39.3719, -5.5878)],
                  "sobral": [("Camocim", -40.8428, -2.9008), ("Granja", -40.8258, -3.12), ("Sobral", -40.3497, -3.6861)]}.items():
    G = build(d[nome]["elements"])
    # baturite: o ramal para Baturité sai da linha tronco; faz-se caminho Fortaleza->Baturite, e Fortaleza->Quixada->Senador Pompeu separados
    pares = [(0, 2, "Fortaleza-Baturite"), (0, 3, "Fortaleza-Quixada"), (3, 4, "Quixada-Senador Pompeu")] if nome == "baturite" else [(0, 1, "Camocim-Granja"), (1, 2, "Granja-Sobral"), (0, 2, "Camocim-Sobral")]
    for i, j, rot in pares:
        a = near(G, seq[i][1], seq[i][2]); b = near(G, seq[j][1], seq[j][2])
        p = path(G, a, b)
        print(rot, "a", a, "b", b, None if not p else len(p))
        if p: res[rot] = [[round(x, 4), round(y, 4)] for x, y in simp(p, 0.004)]
json.dump(res, open("dl/dados/trilhos_caminhos.json", "w"))
print({k: len(v) for k, v in res.items()})
