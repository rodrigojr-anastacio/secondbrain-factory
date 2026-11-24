"""Roda os lotes do plano-imagens.json pela fal (src/gerar_fal.py, gpt-image-2/edit), um de cada vez (custo por
endpoint não mistura), parando sozinho depois de --minutos (rode de novo: pula o que existe).
Uso (raiz do repo): tools/.venv/bin/python canais/dossie-es/produtos/hq/001/tools/rodar_fal.py [--ordem 1,2] [--lote nome] [--minutos 8]
"""
import argparse, json, os, shlex, subprocess, time
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", "..", "..", ".."))
ap = argparse.ArgumentParser()
ap.add_argument("--ordem"); ap.add_argument("--lote"); ap.add_argument("--minutos", type=float, default=8)
ap.add_argument("--paralelo", default="6"); ap.add_argument("--modelo", default="openai/gpt-image-2/edit")
a = ap.parse_args()
plano = json.load(open(os.path.join(AQUI, "plano-imagens.json")))["lotes"]
t0 = time.time()
for p in plano:
    if a.ordem and str(p["ordem"]) not in a.ordem.split(","):
        continue
    if a.lote and p["lote"] not in a.lote.split(","):
        continue
    cenas = json.load(open(os.path.join(AQUI, os.path.basename(p["cenas"]))))
    saida = os.path.join(RAIZ, "canais/dossie-es/produtos/hq", p["saida"])
    falta = [c["id"] for c in cenas if not os.path.exists(os.path.join(saida, c["id"] + ".jpg"))]
    if not falta:
        continue
    if time.time() - t0 > a.minutos * 60:
        print("TEMPO: parei antes de", p["lote"]); break
    cmd = shlex.split(p["comando"].replace("src/gerar.py", "src/gerar_fal.py").replace("--notas hq001", ""))
    cmd += ["--modelo", a.modelo, "--paralelo", a.paralelo, "--notas", "dossie-hq-001 " + p["lote"]]
    print(">>", p["lote"], len(falta), "faltando", flush=True)
    r = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True)
    print("\n".join(l for l in (r.stdout + r.stderr).splitlines() if "ERRO" in l or "geradas" in l or "Traceback" in l or "Error" in l)[-1500:], flush=True)
