"""Bases fotorrealistas das thumbs cine D/E/F do 013 (21/11/2026). Reusa img_fal.py, mas SEM o estilo graphic novel do canal
(pedido do Rodrigo: estilo pôster de cinema das refs). Custo real pelo uso do endpoint, registrado no vídeo 53.
Uso (de tools/): .venv/bin/python ../canais/dossie-es/videos/013-nuremberg/thumbs-extra/gerar_bases.py <cenas.json> [--modelo M] [--so D1,E1]"""
import argparse, json, os, sys, time
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
import img_fal as F
from db import tentar

X = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser(); ap.add_argument("cenas"); ap.add_argument("--modelo", default="google/nano-banana-2.1")
ap.add_argument("--so", default=""); ap.add_argument("--params", default='{"aspect_ratio":"16:9","resolution":"2K"}')
a = ap.parse_args()
cenas = json.load(open(a.cenas)); so = set(filter(None, a.so.split(",")))
key = F.chave(); u0, s0 = F.uso_endpoint(key, a.modelo), F.saldo(key)
ok = 0
for c in cenas:
    if so and c["id"] not in so: continue
    dest = f"{X}/bases/{c['id']}.jpg"
    if os.path.exists(dest): print("pula", c["id"]); continue
    corpo = {"prompt": c["prompt"], "num_images": 1, **json.loads(a.params)}
    try:
        orig = F.gerar(key, a.modelo, corpo, dest, None); ok += 1; print(c["id"], "ok", orig)
    except Exception as e:  # noqa: BLE001
        print(c["id"], "FALHOU", str(e)[:300])
time.sleep(15)
u1, s1 = F.uso_endpoint(key, a.modelo), F.saldo(key)
if u0 is not None and u1 is not None and u1 > u0: custo, fonte = round(u1 - u0, 4), "uso do endpoint"
elif s0 and s1 and s0 > s1: custo, fonte = round(s0 - s1, 4), "saldo"
else: custo, fonte = ok * 0.15, "estimado"
print(f"{ok} imagens · US$ {custo} ({fonte})")
if ok:
    def reg(con):
        cb = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='fal.ai'").fetchone()
        con.execute("INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
                    " VALUES ('youtube','dossie-es','fal.ai',%s,%s,'imagens',%s,'USD',%s,'youtube.video',53,%s)",
                    (f"imagem {a.modelo}", ok, custo, custo * float(cb[0]) if cb else None, f"thumbs cine 013 {os.path.basename(a.cenas)}; custo {fonte}"))
    tentar(reg)
