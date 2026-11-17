# Em Relevo 006 (17/11/2026): voz de reserva do canal.yaml (Fish #NATASHA, drama-3), 1 request por bloco, SEM as tags do v3.
# Motivo: a chave da ElevenLabs (~/.segredos/elevenlabs/api_key) voltou 401 "Invalid API key" em 17/11 00:40.
# Brutos em audio/fish-brutos/<id>.mp3 (fora do git); cache por texto; custo em financas.consumo (--video 47).
import json, re, sys, hashlib, types
from pathlib import Path
sys.path.insert(0, str(Path.home() / "workspace/fabrica-youtube/tools"))
import tts_fish as F
A = Path(__file__).parent; OUT = A.parent / "audio/fish-brutos"; (OUT / "cache").mkdir(parents=True, exist_ok=True)
VOZ, MODELO = "e8bccb7beecd46c6a1c64813e0238fa9", "drama-3"
key = F.chave(); c0 = F.credito(key); print("crédito antes", c0, flush=True)
total = 0; so = set(sys.argv[1:])
try:
    for b in json.load(open(A / "blocos.json")):
        if so and b["id"] not in so: continue
        txt = " ".join(l.strip() for l in b["fala_tts"].split("\n") if l.strip()); txt = re.sub(r"\[[^\]]*\]\s*", "", txt).strip()
        h = hashlib.sha1((VOZ + MODELO + txt).encode()).hexdigest()[:12]; p = OUT / "cache" / f"{h}.mp3"
        if not p.exists():
            for t in range(3):
                try: F.gerar(key, VOZ, MODELO, None, txt, str(p)); break
                except Exception as e: print(b["id"], "erro", e, flush=True)
            else: sys.exit("falhou " + b["id"])
            total += len(txt.encode())
        d = OUT / f"{b['id']}.mp3"
        if d.exists() or d.is_symlink(): d.unlink()
        d.hardlink_to(p); print(b["id"], len(txt), flush=True)
finally:
    if total:
        F.registrar_custo(types.SimpleNamespace(canal="em-relevo", video=47, entrada="006-blocos.json"), MODELO, total)
        print("crédito depois", F.credito(key))
