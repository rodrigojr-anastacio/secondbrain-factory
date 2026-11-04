"""Confere handles (channels.list forHandle, 1 unidade cada). Sem item = livre."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from trends import yt_client
yt = yt_client()
for h in sys.argv[1:]:
    r = yt.channels().list(part="snippet,statistics", forHandle=h).execute()
    it = r.get("items", [])
    print(h, "LIVRE" if not it else f"OCUPADO: {it[0]['snippet']['title']} ({it[0]['statistics'].get('videoCount')} vídeos)")
