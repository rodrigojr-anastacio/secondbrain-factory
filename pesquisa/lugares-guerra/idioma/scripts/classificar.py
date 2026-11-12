"""Classifica canais mapeados em a / b_wts / b_cwfp / c. Saída: dados/classes.json"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import F, D, WAR
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(BASE, "dados/canais_metricas.json"))); U = json.load(open(os.path.join(BASE, "dados/uploads.json")))
WTS_PLACE = re.compile(r"iwo|midway|wake island|tinian|omaha|normandy|peleliu|corregidor|okinawa|pearl harbor|guadalcanal|bikini|d-day|uss arizona", re.I)
CW = re.compile(r"supposed to see|lincoln.{0,40}(death|assassin|photo|picture)|lee.?s surrender|appomattox|fine print", re.I)
cls = {}
for cid, m in M.items():
    vs = [v for v in U[cid]["videos"] if v["dur_s"] >= 240]
    fw = [v for v in vs if F.search(v["titulo"]) and (WAR.search(v["titulo"]) or WTS_PLACE.search(v["titulo"]))]
    wcopy = [v for v in vs if F.search(v["titulo"]) and WTS_PLACE.search(v["titulo"])]
    ccopy = [v for v in vs if CW.search(v["titulo"]) and D.search(v["titulo"])]
    m["wcopy_ex"] = [(v["views"], v["pub"], v["titulo"][:75], v["id"]) for v in sorted(wcopy, key=lambda v: -v["views"])[:2]]; m["n_fw"] = len(fw); m["n_wcopy"] = len(wcopy); m["n_ccopy"] = len(ccopy)
    m["fw_ex"] = [(v["views"], v["pub"], v["titulo"][:75], v["id"]) for v in sorted(fw, key=lambda v: -v["views"])[:2]]
    m["cc_ex"] = [(v["views"], v["pub"], v["titulo"][:75], v["id"]) for v in sorted(ccopy, key=lambda v: -v["views"])[:2]]
    young = m["idade_d"] < 365
    c = None
    if cid == "UCUt7wPSxHRObHObdAW-26JQ" or cid == "UCE1gBqF9TF6JswS0zsxdGTg": c = "ref"
    elif m["nome"] in ("The Union And Confederacy", "Shrapnel") : c = "b_cwfp"
    elif young and m["primeiro"] >= "2026-09-20" and m["n_wcopy"] >= 1: c = "b_wts"
    elif young and m["n_wcopy"] >= 1: c = "b_wts"
    elif young and m["n_fw"] >= 2: c = "a"
    elif young and m["n_formula"] >= 3: c = "a_geral"
    cls[cid] = c
json.dump({"cls": cls, "m": M}, open(os.path.join(BASE, "dados/classes.json"), "w"), ensure_ascii=False)
import collections; print(collections.Counter(cls.values()))
for k in ("b_wts", "b_cwfp", "a", "a_geral"):
    print("==", k)
    for cid, c in cls.items():
        if c == k: m = M[cid]; print(m["nome"][:30], m["primeiro"], m["n_long"], f'{m["views"]:,}', m["n_fw"], m["n_wcopy"], m["fw_ex"][0][2] if m["fw_ex"] else "")
