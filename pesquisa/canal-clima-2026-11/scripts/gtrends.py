"""Google Trends: interesse ao longo do tempo (12 meses e 5 anos, BR e mundo) via API não oficial do explore, WARP. Grátis.
Saída: dados/gtrends.json"""
import json, os, subprocess, urllib.parse, time
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = "127.0.0.1:40000"; JAR = "/tmp/gt_cookies.txt"
def get(url):
    r = subprocess.run(["curl", "-s", "-m", "30", "--socks5-hostname", P, "-b", JAR, "-c", JAR, "-A", "Mozilla/5.0", url], capture_output=True)
    return r.stdout.decode("utf-8", "replace")
get("https://trends.google.com/trends/?geo=BR")
PROP = os.environ.get("PROP", "")
def interesse(termos, geo, tempo, hl="pt-BR"):
    req = {"comparisonItem": [{"keyword": t, "geo": geo, "time": tempo} for t in termos], "category": 0, "property": PROP}
    txt = get("https://trends.google.com/trends/api/explore?" + urllib.parse.urlencode({"hl": hl, "tz": "180", "req": json.dumps(req)}))
    try:
        ws = json.loads(txt[txt.index("{"):])["widgets"]
    except Exception:
        return {"erro": txt[:200]}
    w = [w for w in ws if w["id"] == "TIMESERIES"][0]
    txt = get("https://trends.google.com/trends/api/widgetdata/multiline?" + urllib.parse.urlencode({"hl": hl, "tz": "180", "req": json.dumps(w["request"]), "token": w["token"]}))
    d = json.loads(txt[txt.index("{"):])["default"]["timelineData"]
    return {"termos": termos, "geo": geo, "tempo": tempo, "serie": [(x["formattedTime"], x["value"]) for x in d]}
CONS = [(["tornado", "ciclone", "enchente", "el niño", "desastre"], "BR", "today 5-y"), (["tornado", "hurricane", "el niño", "flood", "disaster"], "", "today 5-y")] if PROP else [(["tornado", "ciclone", "enchente", "el niño", "granizo"], "BR", "today 5-y"),
        (["tornado", "ciclone", "enchente", "el niño", "granizo"], "BR", "today 12-m"),
        (["tornado", "hurricane", "el niño", "flood", "heat wave"], "", "today 5-y"),
        (["tornado brasil", "tornado santa catarina", "tornado paraná"], "BR", "today 12-m")]
out = []
for t, g, tp in CONS:
    out.append(interesse(t, g, tp)); time.sleep(3)
json.dump(out, open(os.path.join(BASE, "dados", f"gtrends{PROP and '_'+PROP}.json"), "w"), ensure_ascii=False)
for o in out:
    if "erro" in o: print("ERRO", o["erro"][:150]); continue
    print(o["geo"] or "mundo", o["tempo"], o["termos"])
    s = o["serie"]; print("  últimos:", s[-6:]); 
    for i, t in enumerate(o["termos"]):
        vals = [v[i] for _, v in s]; mx = max(vals); print(f"  {t:24} média {sum(vals)/len(vals):5.1f} max {mx} em {s[vals.index(mx)][0]} | último {vals[-1]}")
