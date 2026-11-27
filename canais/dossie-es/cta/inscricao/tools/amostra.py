#!/usr/bin/env python3
"""Amostra do CTA de inscrição (27/11/2026): ~23 s do 016-mkultra (fim do Expediente 8 "La Silla" → a frase com o botão →
cartão do Expediente 9 "La Selva"), montada pelo MESMO caminho de produção: blocos.json + qa/blocos.json + mix.wav + timeline
do 016 recortada, e depois `inscricao.py montar` (liga o Video.jsx, copia o botão, põe clique/sininho) e, depois do render,
`inscricao.py qa --sem-posicao`.

Uso (raiz do repo): tools/.venv/bin/python canais/dossie-es/cta/inscricao/tools/amostra.py   → pasta de trabalho em
$TMPDIR/cta-inscricao-amostra (nunca /tmp); render e prévia: canais/dossie-es/cta/inscricao/tools/render_amostra.sh
Voz da frase: canais/dossie-es/cta/inscricao/voz/v1/INSCRICAO.mp3 (Fish, config de produção do canal, 1,0×).
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

AQUI = Path(__file__).resolve().parent.parent            # canais/dossie-es/cta/inscricao
V16 = AQUI.parent.parent / "videos/016-mkultra"
W = Path(os.environ.get("TMPDIR", Path.home() / "cache/tmp")) / "cta-inscricao-amostra"
sys.path.insert(0, str(AQUI))
import inscricao as I  # noqa: E402

spec = importlib.util.spec_from_file_location("build016", V16 / "tools/build.py")
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)   # trilha(), sfx(), ducking(), aparar() do canal
SR, FPS = B.SR, B.FPS

T0 = 506.40                     # "Ese mismo mes, un informe…" (2ª frase do N046, último bloco do Expediente 8)
FIM_ORIG = 521.30               # já dentro do Expediente 9 (cartão + "La Selva. Iquitos, Perú…")


def main():
    if W.exists(): shutil.rmtree(W)
    for d in ("src", "public/img", "public/audio", "audio", "qa", "out"): (W / d).mkdir(parents=True)
    q = {b["id"]: b for b in json.load(open(V16 / "qa/blocos.json"))}
    txt = {b["id"]: b["texto"] for b in json.load(open(V16 / "blocos.json"))}
    tl = json.load(open(V16 / "src/timeline.json"))
    S = q["N046"]["fim"]                                   # fim da fala do último bloco do capítulo

    # voz: trecho original + 0,9 s (GAP_IDEIA) + a frase + o resto original (que já tem a pausa de capítulo de 1,5 s)
    voz16 = B.ler_mp3(V16 / "public/audio/voz.wav")
    cta = B.aparar(B.ler_mp3(AQUI / "voz/v1/INSCRICAO.mp3"))
    ref = voz16[int(T0 * SR):int(S * SR)]
    cta *= np.sqrt(np.mean(ref ** 2)) / np.sqrt(np.mean(cta ** 2))            # mesmo volume da narração em volta
    D = B.GAP_IDEIA + len(cta) / SR                                            # tempo inserido em S
    voz = np.concatenate([voz16[int(T0 * SR):int(S * SR)], np.zeros(int(B.GAP_IDEIA * SR)), cta,
                          voz16[int(S * SR):int(FIM_ORIG * SR)]])
    dur = len(voz) / SR
    sh = lambda t: t - T0 if t <= S else t - T0 + D                           # tempo original → amostra
    cta_ini, cta_fim = S - T0 + B.GAP_IDEIA, S - T0 + D

    # timeline: planos do N046 até o meio da pausa, 2 planos de reuso do capítulo durante a frase, depois o 016 deslocado
    shots = []
    for s in tl["shots"]:
        a, z = s["from"] / FPS, (s["from"] + s["dur"]) / FPS
        if z <= T0 or a >= FIM_ORIG: continue
        if s["bloco"] == "N046":
            a, z = max(a, T0), min(z, S + B.GAP_IDEIA / 2)
            if z <= a: continue
            shots.append({**s, "from": round((a - T0) * FPS), "dur": None})
        elif s["bloco"] >= "N047":
            shots.append({**s, "from": round(sh(max(a, T0)) * FPS), "dur": None})
    meio = (cta_ini + cta_fim) / 2
    reuso = [("I126", "chair_room", "detalhe-centro", "push-in leve"), ("I128", "chair_tilt", "médio-dir", "pan dir→esq")]
    k = next(i for i, s in enumerate(shots) if s["bloco"] >= "N047")
    for j, (img, ch, enq, mov) in enumerate(reuso):
        ini = (S - T0 + B.GAP_IDEIA / 2) if j == 0 else meio
        shots.insert(k + j, {"from": round(ini * FPS), "dur": None, "img": img, "chave": ch, "enq": enq, "mov": mov,
                             "nova": False, "bloco": "N002", "trecho": "", "rot": None})
    total = int(np.ceil(dur * FPS))
    for i, s in enumerate(shots):
        s["dur"] = (shots[i + 1]["from"] if i + 1 < len(shots) else total) - s["from"]
        if s["bloco"] == "N046": s["bloco"] = "N001"
        elif s["bloco"] != "N002": s["bloco"] = "N003" if s["bloco"] == "N047" else s["bloco"]
    caps = [{**c, "from": round(sh(c["t"]) * FPS), "t": round(sh(c["t"]), 2), "bloco": "N003"} for c in tl["chapters"] if c["bloco"] == "N047"]
    cards = [{**c, "from": round(sh(c["from"] / FPS) * FPS)} for c in tl["cards"] if T0 * FPS < c["from"] < FIM_ORIG * FPS]
    json.dump({"fps": FPS, "frames": total, "shots": shots, "cards": cards, "chapters": caps},
              open(W / "src/timeline.json", "w"), ensure_ascii=False, indent=0)

    # trilha e SFX do canal (mesmas regras do build.py do 016) + mix em -15 LUFS
    CARD = 100
    carimbos = [(c["from"] + 4 + 16) / FPS for c in caps]
    teclas = []
    for s in shots:
        if s.get("rot"):
            kk = next((c for c in caps if c["from"] + 4 < s["from"] + s["dur"] and c["from"] + 4 + CARD > s["from"]), None)
            ini = max(s["from"], kk["from"] + 4 + CARD) if kk else s["from"]
            teclas.append(((ini + 4) / FPS, len(s["rot"])))
    for c in cards:
        kk = next((ch for ch in caps if ch["from"] + 4 < c["from"] + 90 and ch["from"] + 4 + CARD > c["from"]), None)
        ini = (kk["from"] + 4 + CARD) if kk else c["from"] + 6
        teclas.append(((ini + 4) / FPS, len(c["text"])))
    musica = B.ducking(voz, B.trilha(dur)) + B.sfx(dur, teclas, carimbos)
    B.salvar(W / "public/audio/mix_pre.wav", voz + musica)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(W / "public/audio/mix_pre.wav"), "-af", "loudnorm=I=-15:TP=-1.5:LRA=11",
                    "-ar", str(SR), "-ac", "2", str(W / "public/audio/mix.wav")], check=True)
    (W / "public/audio/mix_pre.wav").unlink()

    # blocos (o mesmo formato da produção) e o áudio da frase, para o `inscricao.py montar` achar o bloco e o clique
    n3_ini = sh(q["N047"]["ini"])
    json.dump([{"id": "N001", "texto": txt["N046"], "ideia": False}, {"id": "N002", "texto": I.TEXTO, "ideia": True},
               {"id": "N003", "texto": txt["N047"], "ideia": False}], open(W / "blocos.json", "w"), ensure_ascii=False, indent=1)
    json.dump([{"id": "N001", "ini": 0.0, "fim": round(S - T0, 3)}, {"id": "N002", "ini": round(cta_ini, 3), "fim": round(cta_fim, 3)},
               {"id": "N003", "ini": round(n3_ini, 3), "fim": round(sh(q["N047"]["fim"]), 3)}], open(W / "qa/blocos.json", "w"), indent=0)
    shutil.copyfile(AQUI / "voz/v1/INSCRICAO.mp3", W / "audio/N002.mp3")

    # projeto Remotion: src do 016 (template do canal), imagens usadas, node_modules do 016
    for f in ("Video.jsx", "labels.jsx", "index.jsx", "Thumbnail.jsx"): shutil.copyfile(V16 / "src" / f, W / "src" / f)
    for s in shots:
        dst = W / "public/img" / f"{s['img']}.jpg"
        if not dst.exists(): dst.hardlink_to(V16 / "imagens" / f"{s['img']}.jpg")
    (W / "node_modules").symlink_to(V16 / "node_modules")
    shutil.copyfile(V16 / "package.json", W / "package.json")
    print(json.dumps({"pasta": str(W), "duracao_s": round(dur, 2), "frase": [round(cta_ini, 2), round(cta_fim, 2)],
                      "planos": len(shots), "frames": total}, ensure_ascii=False))


if __name__ == "__main__":
    main()
