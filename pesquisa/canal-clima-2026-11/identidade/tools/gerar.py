"""Gera as bases (sem texto) do logo e da capa do canal "Em Relevo" no fal (nano-banana) e registra o custo.
Uso (de tools/ da fábrica): .venv/bin/python ../pesquisa/canal-clima-2026-11/identidade/tools/gerar.py [ids...]
Cada id gera N variações (base/<id>-<k>.jpg). Pula as que já existem.
"""
import json, os, sys, urllib.request
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from db import tentar  # noqa: E402

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELO, PRECO = "fal-ai/nano-banana", 0.039
ESTILO = ("Handcrafted papercraft diorama look: layered cut paper and matte clay, warm beige paper #E9DCC3 and kraft tan tones, "
          "soft late-afternoon side light with real cast shadows, a single coral red #E8505B accent, deep navy #1F2A44, "
          "documentary, desaturated, subtle paper grain, tactile, 3D render. "
          "Absolutely no text, no letters, no numbers, no words, no labels, no writing, no watermark, no signature, no frame, no border")
LOGO = ("Bold simple iconic emblem for a round YouTube avatar, centered, the subject fills about 70% of the square, generous margin, "
        "plain solid flat deep navy #1F2A44 background filling the whole square edge to edge (no circle, no badge, no vignette), "
        "strong silhouette readable at tiny size, very few details. ")
BASES = {
    "logo-a": (LOGO + "A small square chunk of terrain cut out like a papercraft relief map tile, seen in three-quarter view from above: "
               "stacked beige paper layers forming a mountain with visible contour steps on the sides, a big glossy coral red map pushpin "
               "stuck in the summit, casting a long shadow", 2),
    "logo-b": (LOGO + "Top-down view of concentric topographic contour lines made of stacked layers of cut beige and tan paper, forming "
               "a rounded hill whose layers rise toward the viewer like a paper relief, a single glossy coral red pushpin at the peak", 2),
    "logo-c": (LOGO + "A folded paper map (three panels, accordion folds, blank beige paper with faint terrain shading and thin border lines, no labels) "
               "partly rising into a 3D paper mountain relief in its middle, a large glossy coral red pushpin stuck into it at an angle", 2),
    "capa-a": ("Wide cinematic panoramic view, a large papercraft relief map of a continent coastline made of stacked beige paper layers "
               "on a dark navy ocean, seen from a low oblique angle with long late-afternoon shadows; coral red pushpins connected by thin red "
               "string on the left and right sides, blank polaroid photos pinned at the far edges; the whole central horizontal band is calm, "
               "simple, low-detail flat paper terrain with clean empty space for a title", 2),
    "capa-b": ("Wide cinematic panoramic view of a cork board desk scene seen from above: a big blank beige paper relief map tile in the center "
               "with soft mountains and a coastline, coral red pushpins, red string, a few blank polaroid photos and blank paper notes only along the "
               "far left and far right edges; the center of the image is low-detail and calm, clean empty space for a title", 2),
}
RATIO = {"logo": "1:1", "capa": "16:9"}


def chave():
    for l in open(os.path.expanduser("~/.segredos/fal.env")):
        if l.startswith("FAL_KEY="):
            return l.split("=", 1)[1].strip()


def main():
    ids = sys.argv[1:] or list(BASES)
    key, feitas = chave(), 0
    for i in ids:
        prompt, n = BASES[i]
        faltam = [k for k in range(1, n + 1) if not os.path.exists(os.path.join(AQUI, "base", f"{i}-{k}.jpg"))]
        if not faltam:
            print(i, "já existe"); continue
        corpo = {"prompt": f"{prompt}. {ESTILO}", "num_images": len(faltam), "aspect_ratio": RATIO[i.split('-')[0]],
                 "output_format": "jpeg"}
        req = urllib.request.Request(f"https://fal.run/{MODELO}", data=json.dumps(corpo).encode(), method="POST",
                                     headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                imgs = json.load(r)["images"]
            for k, img in zip(faltam, imgs):
                urllib.request.urlretrieve(img["url"], os.path.join(AQUI, "base", f"{i}-{k}.jpg")); feitas += 1
            print(i, "ok", len(imgs))
        except Exception as e:  # noqa: BLE001
            print(i, "ERRO", str(e)[:200])
    if feitas:
        def reg(con):
            c = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='fal.ai'").fetchone()
            custo = feitas * PRECO
            con.execute("INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, notas)"
                        " VALUES ('youtube','em-relevo','fal.ai','identidade em relevo',%s,'imagens',%s,'USD',%s,%s)",
                        (feitas, custo, custo * float(c[0]) if c else None, f"{MODELO}: logo/capa do canal Em Relevo: " + ",".join(ids)))
        tentar(reg)
    print(f"{feitas} geradas · US$ {feitas * PRECO:.3f}")


if __name__ == "__main__":
    main()
