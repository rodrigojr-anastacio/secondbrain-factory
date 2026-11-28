import subprocess, json, os, sys, urllib.parse, concurrent.futures as cf
YTDLP=os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
NODE=os.path.expanduser("~/.hermes/tools/node-26.12.1-linux-x64/bin/node")
T=[l.rstrip("\n").split("\t") for l in open("termos.tsv") if l.strip()]
def run(gt):
    g,t=gt
    url="https://www.youtube.com/results?search_query="+urllib.parse.quote(t)+"&sp=EgIIBQ%253D%253D"
    cmd=[YTDLP,"--proxy","socks5://127.0.0.1:40000","--js-runtimes",f"node:{NODE}","--no-warnings","-J","--flat-playlist","--playlist-end","30",url]
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=240)
        d=json.loads(r.stdout); return g,t,[e.get("id") for e in d.get("entries",[]) if e.get("id")]
    except Exception as e: return g,t,[]
out=[]
with cf.ThreadPoolExecutor(5) as ex:
    for g,t,ids in ex.map(run,T):
        out.append(dict(grupo=g,termo=t,ids=ids)); print(g,t,len(ids),flush=True)
json.dump(out,open("busca.json","w"),ensure_ascii=False)
