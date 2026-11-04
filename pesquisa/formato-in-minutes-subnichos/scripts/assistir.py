"""Chama tools/watch.py (assistir) gravando os assets nesta pasta (assets/<id>/) em vez de pesquisa/tendencias/.
Obs.: watch.py faz upsert em youtube.assistidos (tabela do watch, não do garimpo)."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
import watch
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for vid in sys.argv[1:]:
    watch.assistir(vid, os.path.join(BASE, "assets"))
