"""Métricas por canal a partir de uploads.json + canais_lista.json. Saída: dados/canais_metricas.json e prévia no stdout."""
import json, os, sys, statistics as st, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import F, D, WAR
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(BASE, "dados/canais_lista.json"))); U = json.load(open(os.path.join(BASE, "dados/uploads.json")))
HOJE = dt.date(2026, 11, 12); out = {}
def dias(d): return (HOJE - dt.date.fromisoformat(d)).days
for cid, u in U.items():
    c = C[cid]; vs = u["videos"]; lg = [v for v in vs if v["dur_s"] >= 240]; sh = len(vs) - len(lg)
    prim = min((v["pub"] for v in vs), default=c["criado"]) if u["completo"] else c["criado"]
    idade = max(dias(prim), 1)
    if idade < 365: vm = c["views"] / idade * 30; base = "views/idade"
    else:
        r = [v for v in lg if dias(v["pub"]) <= 90]; vm = sum(v["views"] for v in r) / 3; base = "longos 90d"
    vl = sorted(lg, key=lambda v: -v["views"])
    f = [v for v in lg if F.search(v["titulo"])]; d = [v for v in lg if D.search(v["titulo"])]; w = [v for v in lg if WAR.search(v["titulo"])]
    out[cid] = {"id": cid, "nome": c["nome"], "handle": c["handle"], "criado": c["criado"], "primeiro": prim, "idade_d": idade, "pais": c["pais"], "n_videos": c["n_videos"], "views": c["views"], "inscritos": c["inscritos"],
                "n_long": len(lg), "n_short": sh, "views_mes": int(vm), "base_vm": base, "mediana_long": int(st.median([v["views"] for v in lg])) if lg else 0, "completo": u["completo"],
                "melhor": (vl[0]["views"], vl[0]["titulo"][:70], vl[0]["id"]) if vl else None, "n_formula": len(f), "n_doc": len(d), "n_war": len(w),
                "formula_ex": [(v["views"], v["pub"], v["titulo"][:70], v["id"]) for v in sorted(f, key=lambda v: -v["views"])[:3]], "doc_ex": [(v["views"], v["pub"], v["titulo"][:70], v["id"]) for v in sorted(d, key=lambda v: -v["views"])[:3]],
                "mediana_sem_top": int(st.median([v["views"] for v in vl[1:]])) if len(vl) > 2 else None,
                "posts_30d": sum(dias(v["pub"]) <= 30 for v in vs)}
json.dump(out, open(os.path.join(BASE, "dados/canais_metricas.json"), "w"), ensure_ascii=False, indent=1)
print(len(out))
