"""Gera as bases (sem texto) do logo e da capa do dossie-es no fal (nano-banana) e registra o custo.
Uso (de tools/ da fábrica): .venv/bin/python ../canais/dossie-es/identidade/tools/gerar.py [ids...]
Pula as bases que já existem em identidade/base/.
"""
import json, os, sys, urllib.request
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from db import tentar  # noqa: E402

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELO, PRECO = "fal-ai/nano-banana", 0.039
ESTILO = ("Graphic novel ink illustration, bold clean black ink outlines, muted desaturated palette of slate blue #2E3A46, "
          "manila folder tan, aged paper #E9DFC9 and charcoal, with a single deep red #B3261E accent, subtle paper grain, "
          "absolutely no text, no letters, no numbers, no words, no writing, no watermark, no signature")
LOGO = ("Bold flat iconic emblem for a round avatar, centered composition with generous margin, the subject fills about 70% of the frame, "
        "plain solid dark slate blue #2E3A46 background, strong silhouette readable at tiny size, very few details. ")
BASES = {
    "logo-a": LOGO + "A closed manila case file folder seen straight on, slightly tilted, with a big round deep red rubber stamp mark "
                     "on its cover (the stamp is an empty ring with a star, no lettering), a paper clip at the top",
    "logo-b": LOGO + "Silhouette head and shoulders of a 1950s secret agent in a fedora hat and trench coat with the collar turned up, "
                     "face hidden in shadow, standing behind an open manila case file folder held at chest height, deep red accent on the hat band",
    "logo-c": LOGO + "A large magnifying glass held over a manila dossier folder, inside the lens a single watchful human eye in black ink, "
                     "a deep red round wax seal on the folder",
    "capa-a": "Wide cinematic panoramic banner, dark slate blue desk seen from above, manila case file folders, typewriter, "
              "black and white photographs (blurred, no faces readable), magnifying glass and a deep red rubber stamp arranged ONLY "
              "along the left and right edges; the whole central horizontal band is empty dark desk surface with soft lamp light, "
              "clean negative space for a title",
    "capa-b": "Wide cinematic panoramic banner, a dim 1950s archive room with endless rows of filing cabinets and stacked manila folders "
              "fading into darkness, a silhouette of an agent in a fedora at the far left, a desk lamp glow at the far right; the center of the "
              "image is a calm, dark, out-of-focus wall area with clean empty space for a title",
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
        dest = os.path.join(AQUI, "base", f"{i}.jpg")
        if os.path.exists(dest):
            print(i, "já existe"); continue
        corpo = {"prompt": f"{BASES[i]}. {ESTILO}", "num_images": 1, "aspect_ratio": RATIO[i.split('-')[0]]}
        req = urllib.request.Request(f"https://fal.run/{MODELO}", data=json.dumps(corpo).encode(), method="POST",
                                     headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                url = json.load(r)["images"][0]["url"]
            urllib.request.urlretrieve(url, dest); feitas += 1; print(i, "ok")
        except Exception as e:  # noqa: BLE001
            print(i, "ERRO", str(e)[:200])
    if feitas:
        def reg(con):
            c = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='fal.ai'").fetchone()
            custo = feitas * PRECO
            con.execute("INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, notas)"
                        " VALUES ('youtube','dossie-es','fal.ai',%s,%s,'imagens',%s,'USD',%s,%s)",
                        (f"imagem {MODELO}", feitas, custo, custo * float(c[0]) if c else None, "identidade do canal (logo/capa): " + ",".join(ids)))
        tentar(reg)
    print(f"{feitas} geradas · US$ {feitas * PRECO:.3f}")


if __name__ == "__main__":
    main()
