"""Gera dados/tabelas.md (tabelas a/b/c/docs, stats de clones, risco de hit único) e dados/stats.json."""
import json, os, sys, statistics as st
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = json.load(open(os.path.join(BASE, "dados/classes.json"))); M = K["m"]; cls = K["cls"]
U = json.load(open(os.path.join(BASE, "dados/uploads.json")))
import re
N = {re.sub(r"\s+", " ", m["nome"]).strip(): cid for cid, m in M.items()}
A = ["Forgotten Fleet", "Ship Tales", "Insight Ship", "Park Vibes", "Hollow Cairn", "Ivan Old Army", "Earthyphus", "MJ MYSTERY GLOBE", "Curious Britain", "Sterling Map Mysteries", "History Unfolded Films", "Unreal Destinations",
     "Strange World Vault", "Unreachable Places", "Explain By Atish", "Verboten", "TheHiddenBases", "Dann"]
B_EXCL = {"The Generals’ Oath", "ATLAS FILES", "Forgotten Fleet", "Ship Tales", "Insight Ship"}
CW = ["Civil War Fine Print", "The Union And Confederacy", "Shrapnel", "Cloaked History", "Lens History", "Mystery in History", "Nation Of History", "Past in Pictures", "Markets of the Past"]
C = ["IT'S HISTORY", "Yarnhub", "Real Time History", "Mark Felton Productions", "War Stories", "The Operations Room", "Kings and Generals", "Simple History", "Atlas Pro", "Timeline - World History Documentaries", "History Hit",
     "The History Guy: History Deserves to Be Remembered", "Jared Owen", "Battle Guide", "American Battlefield Trust", "WW2 Wayfinder", "The History Underground", "Exploring With Josh", "Places", "Historically", "Warlines",
     "The Generals’ Oath", "WW2 Vellob", "Lost US Towns", "Ambrose Discovery", "Agent Flappy", "Top Fives", "HistoryMarche", "The Intel Report", "Military Heroes", "Frontline Echoes - Harold Warfield", "QUANTARA", "ATLAS FILES", ]
A = [n for n in A if n != "Dann"]
def link(m): return f'[{m["nome"].strip()[:30]}](https://www.youtube.com/channel/{m["id"]})'
def idade(m):
    d = m["idade_d"]; return f'{d} d' if d < 365 else f'{d/365:.1f} a'
def k(n): return f"{n:,}".replace(",", ".")
def lin(m):
    mb = m["melhor"]
    return f'| {link(m)} | {m["primeiro"][:10]} ({idade(m)}) | {m["n_long"]}+{m["n_short"]}{"" if m["completo"] else "+"} | {k(m["views"])} | {k(m["inscritos"]) if m["inscritos"] is not None else "oculto"} | {k(m["views_mes"])} | {k(m["mediana_long"])} | {k(mb[0]) if mb else "-"}: {mb[1][:48] if mb else ""} |'
HEAD = "| Canal | 1º vídeo (idade) | Vídeos (longos+shorts; + = só os 100 mais novos lidos) | Views | Inscritos | Views/mês | Mediana (longos) | Melhor vídeo |\n|---|---|---|---|---|---|---|---|"
def tab(ids, ordem="views"):
    ms = sorted([M[i] for i in ids], key=lambda m: -m[ordem]); return HEAD + "\n" + "\n".join(lin(m) for m in ms)
def tabb(ids):
    ms = sorted([M[i] for i in ids], key=lambda m: -m["views"])
    H = "| Canal | 1º vídeo (idade) | Vídeos | Views | Inscritos | Mediana (longos) | Título-clone (views) | Melhor vídeo do canal |\n|---|---|---|---|---|---|---|---|"
    def l(m):
        w = m["wcopy_ex"][0] if m["wcopy_ex"] else None; mb = m["melhor"]
        return f'| {link(m)} | {m["primeiro"][:10]} ({idade(m)}) | {m["n_long"]}+{m["n_short"]}{"" if m["completo"] else "+"} | {k(m["views"])} | {k(m["inscritos"]) if m["inscritos"] is not None else "oculto"} | {k(m["mediana_long"])} | {w[2] if w else ""} ({k(w[0]) if w else ""}) | {k(mb[0])} |'
    return H + "\n" + "\n".join(l(m) for m in ms)
ids_a = [N[n] for n in A if n in N and n != "Dann"]
ids_b = [cid for cid, c in cls.items() if c == "b_wts" and re.sub(r"\s+", " ", M[cid]["nome"]).strip() not in B_EXCL]
ids_ref = [N["Where They Stood"], N["Civil War Fine Print"]]
ids_cw = [N[n] for n in CW if n in N and n != "Civil War Fine Print"]
ids_c = [N[n] for n in C if n in N]
miss = [n for n in A + CW + C if n not in N]
out = []
out.append("### Referências\n" + tab(ids_ref))
out.append("### (a) Fórmula exata (\"Why can't you visit / What's still under-at / Why is X still there\"), canais com < 1 ano\n" + tab(ids_a))
out.append("### (b1) Clones do Where They Stood (título/ideia do Iwo Jima copiados; 1º vídeo ≥ 09/2026 na maioria)\n" + tabb(ids_b))
out.append("### (b2) Clones e parentes do Civil War Fine Print (ângulo \"documentos / fotos que você não deveria ver\")\n" + tab(ids_cw))
out.append("### (c) Mesmo nicho (guerra/lugares/história militar), outro formato: dá o teto\n" + tab(ids_c, "views_mes"))
S = {}
def grp(ids, nome):
    ms = [M[i] for i in ids]
    S[nome] = {"n": len(ms), "mediana_das_medianas": int(st.median([m["mediana_long"] for m in ms])), "mediana_do_melhor": int(st.median([m["melhor"][0] for m in ms if m["melhor"]])),
               "com_melhor_ge_10k": sum(1 for m in ms if m["melhor"] and m["melhor"][0] >= 10000), "com_melhor_ge_100k": sum(1 for m in ms if m["melhor"] and m["melhor"][0] >= 100000),
               "com_mediana_ge_5k": sum(1 for m in ms if m["mediana_long"] >= 5000), "mediana_inscritos": int(st.median([m["inscritos"] or 0 for m in ms])),
               "soma_views": sum(m["views"] for m in ms), "top1_share_med": round(st.median([m["melhor"][0] / max(m["views"], 1) for m in ms if m["melhor"]]), 2)}
grp(ids_a, "a"); grp(ids_b, "b_wts"); grp(ids_cw, "b_cwfp_e_parentes")
# clones puros do WTS (1º vídeo >= 2026-09-27)
puros = [i for i in ids_b if M[i]["primeiro"] >= "2026-09-27"]; grp(puros, "b_wts_puros")
json.dump({"stats": S, "faltando": miss, "ids": {"a": ids_a, "b": ids_b, "cw": ids_cw, "c": ids_c}}, open(os.path.join(BASE, "dados/stats.json"), "w"), ensure_ascii=False, indent=1)
open(os.path.join(BASE, "dados/tabelas.md"), "w").write("\n\n".join(out))
print(json.dumps(S, indent=1)); print("faltando", miss, "mapeados nas tabelas:", len(set(ids_a + ids_b + ids_cw + ids_c + ids_ref)))
