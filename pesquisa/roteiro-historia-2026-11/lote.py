"""Transcreve (Whisper, tools/transcrever.py) a seleção e grava transcricoes/<canal>__<id>.txt com cabeçalho."""
import json, os, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__)); T = os.path.expanduser("~/workspace/fabrica-youtube/tools")
SEL = [  # (handle, id, papel, idioma)
 ("Archlang","yV-Cwcy8K6A","C-hit","en"),("Archlang","J1ARuhEH0zI","C-fraco","en"),("Archlang","APoNEKs9d-4","C-fraco","en"),
 ("breakdownwithpaints","cjIvXfkF1S0","C-hit","en"),("breakdownwithpaints","5d-KSO2BVGM","C-fraco","en"),("breakdownwithpaints","J-wZ1HfirTo","C-fraco","en"),
 ("breakdownwithpaints","cHwDK968qCQ","C-fraco-antes","en"),
 ("Kelevins","FnXS0VOhX1I","A-topo","en"),("Kelevins","ngprAYfRrnY","A-topo","en"),("Kelevins","t7zjiFULuUc","A-topo","en"),
 ("Crayon_Capital","HawmGu7oNrc","A-topo","en"),("Crayon_Capital","LuEcoqizj0o","A-topo","en"),("Crayon_Capital","y51JjcymEAY","A-topo","en"),
 ("Inkexplainer96","49_Ph2q6uIM","A-topo","en"),("Inkexplainer96","SD7XyG2wd1k","A-topo","en"),
 ("HistóriaNaMarra","ARDA87ONohc","B-topo","pt"),("HistóriaNaMarra","VAaop-wsneQ","B-topo","pt"),("HistóriaNaMarra","S8yKeHDpgOg","B-topo","pt"),
]
C = json.load(open(f"{D}/canais.json"))
lim = int(sys.argv[1]) if len(sys.argv) > 1 else 99; n = 0
for h, vid, papel, lang in SEL:
    out = f"{D}/transcricoes/{h}__{vid}.txt"
    if os.path.exists(out): continue
    if n >= lim: break
    c = C[h]; v = next(x for x in c["videos"] if x["id"] == vid)
    tmp = f"/tmp/tr_{vid}.txt"
    r = subprocess.run([f"{T}/.venv/bin/python", "transcrever.py", vid, tmp, lang], cwd=T, capture_output=True, text=True)
    if r.returncode: print("ERRO", vid, r.stderr[-300:]); continue
    body = open(tmp).read(); words = sum(len(l.split(" ", 1)[-1].split()) for l in body.splitlines())
    head = (f"# {v['titulo']}\n# id: {vid} | canal: {c['nome']} (@{h}, {c['inscritos']} inscritos) | grupo/papel: {papel}\n"
            f"# views: {v['views']} (Data API, 2026-11-07) | publicado: {v['pub']} ({v['idade_d']} dias) | duração: {v['dur_s']//60}:{v['dur_s']%60:02d}"
            f" | palavras: {words} ({words/(v['dur_s']/60):.0f} ppm) | Whisper small, {lang}\n\n")
    open(out, "w").write(head + body); os.remove(tmp); n += 1
    print("ok", h, vid, words, "palavras", flush=True)
