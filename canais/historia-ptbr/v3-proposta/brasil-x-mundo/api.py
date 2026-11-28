import json, os, sys, re
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
c=Credentials.from_authorized_user_file(os.path.expanduser("~/.segredos/youtube/tokens/historia-ptbr.json"))
if not c.valid: c.refresh(Request())
yt=build("youtube","v3",credentials=c,cache_discovery=False)
B=json.load(open("busca.json"))
old=json.load(open(os.path.expanduser("~/cache/tmp/v3pesq/vids.json")))
ids=sorted({i for b in B for i in b["ids"]})
vids={}
need=[i for i in ids]
for k in range(0,len(need),50):
    r=yt.videos().list(part="snippet,statistics,contentDetails",id=",".join(need[k:k+50]),maxResults=50).execute()
    for it in r["items"]:
        s=it["snippet"]
        vids[it["id"]]=dict(id=it["id"],titulo=s["title"],canal=s["channelTitle"],cid=s["channelId"],data=s["publishedAt"][:10],
          views=int(it["statistics"].get("viewCount",0)),dur=it["contentDetails"]["duration"],
          lang=s.get("defaultAudioLanguage") or s.get("defaultLanguage") or "")
cids=sorted({v["cid"] for v in vids.values()}); chs={}
for k in range(0,len(cids),50):
    r=yt.channels().list(part="snippet,statistics",id=",".join(cids[k:k+50]),maxResults=50).execute()
    for it in r["items"]:
        chs[it["id"]]=dict(subs=int(it["statistics"].get("subscriberCount",0)),nvid=int(it["statistics"].get("videoCount",0)),criado=it["snippet"]["publishedAt"][:10])
def dur(iso):
    m=re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?",iso); d,h,mi,s=[int(x or 0) for x in m.groups()]
    return d*86400+h*3600+mi*60+s
for v in vids.values():
    v["seg"]=dur(v["dur"]); v.update({k:chs.get(v["cid"],{}).get(k) for k in ["subs","nvid","criado"]})
json.dump(vids,open("vids.json","w"),ensure_ascii=False); print(len(ids),len(vids),len(chs))
