"""Gera as bases (sem texto) do logo e da capa do historia-ptbr no fal e registra o custo real em financas.consumo.
Motor do canal: google/nano-banana-2.1/edit com as refs de ESTILO do canal.yaml (bonequinhos de cabeça redonda).
Uso (da raiz da fábrica): tools/.venv/bin/python canais/historia-ptbr/identidade/tools/gerar.py [ids...] [--teto 2.0]
Pula as bases que já existem em identidade/base/. Fontes de texto ficam fora: o texto é composto no compor.py.
"""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

import yaml

FAB = os.path.expanduser("~/workspace/fabrica-youtube")
sys.path.insert(0, os.path.join(FAB, "tools"))
from db import tentar  # noqa: E402
from img_fal import chave, data_uri, gerar, saldo, uso_endpoint  # noqa: E402

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANAL = os.path.join(FAB, "canais", "historia-ptbr")
VIS = yaml.safe_load(open(os.path.join(CANAL, "canal.yaml")))["visual"]
MODELO = VIS["modelo"]  # google/nano-banana-2.1/edit
REFS = VIS["refs"] + ["videos/004-china/imagens/I010.jpg"]

SEM_TEXTO = "absolutely no text, no letters, no numbers, no words, no writing, no watermark, no signature, no frame, no border"
LOGO = ("Bold flat iconic emblem for a small round YouTube avatar, centered composition with generous margin, the subject fills about "
        "65% of the frame, plain solid flat background of a single color, strong simple silhouette readable at tiny size, very few "
        "details, thick black outlines, flat bright colors. ")
BONECO = ("the channel mascot: a friendly simple cartoon person with a big round white head, two black dot eyes, a small happy "
          "open smile, simple round body, ")
LOGOS = {
    "logo-a": LOGO + "Background solid warm golden yellow #F7C21B. " + BONECO +
              "wearing a simple brown explorer vest, hugging with both arms a big classic wooden hourglass with golden sand running "
              "down, the hourglass as tall as the mascot",
    "logo-b": LOGO + "Background solid deep terracotta red #B8462B. " + BONECO +
              "wearing a small simple golden crown, holding open in front of him an old unrolled parchment scroll (blank, no writing) "
              "with a tiny hourglass drawn as a simple shape on the side",
    "logo-c": LOGO + "Background solid dark warm navy blue #1F2A44. A big classic hourglass with a wooden frame; inside the top bulb "
              "a tiny antique globe of the world in brown and blue, and golden yellow #F7C21B sand falling into the bottom bulb; "
              "a small round-white-head cartoon mascot with dot eyes peeking from behind the hourglass and waving",
}
ERAS = ("an ancient Egyptian pharaoh with the striped blue and gold headdress, an Indian emperor with a turban and jewels, a Persian king "
        "with a tall crown and flat curled beard shape, a Chinese emperor with a flat black board crown with hanging beads, a Roman "
        "legionary with a red-crested helmet, a Viking with a round shield, a medieval knight, a 1500s explorer with a hat and a map, "
        "and a modern person with a backpack and a phone")
CAPAS = {
    "capa-a": "Wide cinematic panoramic illustration for a channel banner. A long cheerful parade of 9 round-white-head cartoon characters "
              "from different eras walking left to right in ONE single row along a dirt road that crosses the whole width of the image "
              f"exactly in the vertical middle of the picture: {ERAS}. All of them small and full body, same size, evenly spaced. "
              "Far behind them on the horizon, small landmarks in order of time: Egyptian pyramids, the Taj Mahal, the ruins of "
              "Persepolis, the Great Wall of China on green hills, the Colosseum. The top third of the image is a bright clean blue sky "
              "with a few small white clouds; the bottom third is plain warm grassy ground. Warm afternoon light",
    "capa-b": "Wide cinematic panoramic illustration for a channel banner, warm golden sunset light. In the exact center of the image a "
              "huge open antique book lies flat; from its pages rises a small round world of history: Egyptian pyramids, the Taj Mahal, "
              "a Persian palace, a Chinese pagoda and a Roman temple. On the left side and on the right side of the book stand round-"
              f"white-head cartoon characters from different eras, waving and looking at the book: {ERAS}. Background: soft warm "
              "sky gradient from orange to golden yellow with small clouds, clean and simple",
}
BASES = {**{f"{k}-{t}": (v, "1:1", "1K") for k, v in LOGOS.items() for t in (1, 2)},
         **{f"{k}-{t}": (v, "16:9", "2K") for k, v in CAPAS.items() for t in (1, 2)}}


def main():
    args = [a for a in sys.argv[1:]]
    teto = 2.0
    if "--teto" in args:
        i = args.index("--teto"); teto = float(args[i + 1]); del args[i:i + 2]
    ids = args or list(BASES)
    os.makedirs(os.path.join(AQUI, "base"), exist_ok=True)
    pend = [i for i in ids if not os.path.exists(os.path.join(AQUI, "base", f"{i}.jpg"))]
    if not pend:
        print("nada a gerar"); return
    key = chave()
    gasto = 0.0

    def ja_gasto(con):
        r = con.execute("SELECT coalesce(sum(custo),0) FROM financas.consumo WHERE notas LIKE 'identidade historia-ptbr%%'").fetchone()
        return float(r[0])
    gasto = tentar(ja_gasto) or 0.0
    if gasto + 0.09 * len(pend) > teto:
        sys.exit(f"teto: já gasto US$ {gasto:.3f}; {len(pend)} bases (~US$ {0.09 * len(pend):.2f}) passariam de US$ {teto}")
    refs = [data_uri(os.path.join(CANAL, r)) for r in REFS]
    u0, s0 = uso_endpoint(key, MODELO), saldo(key)
    print(f"{MODELO} · {len(pend)} bases · refs {len(refs)} · já gasto US$ {gasto:.3f} · uso endpoint {u0} · saldo {s0}")

    def uma(i):
        prompt, ratio, res = BASES[i]
        corpo = {"prompt": VIS["ref_instrucao"] + prompt + ". " + SEM_TEXTO, "num_images": 1, "image_urls": refs,
                 "aspect_ratio": ratio, "resolution": res, "output_format": "jpeg", "thinking_level": "minimal"}
        try:
            orig = gerar(key, MODELO, corpo, os.path.join(AQUI, "base", f"{i}.jpg"), None)
            print(i, "ok", orig, flush=True); return True
        except Exception as e:  # noqa: BLE001
            print(i, "ERRO", str(e)[:200], flush=True); return False
    with ThreadPoolExecutor(4) as ex:
        ok = sum(ex.map(uma, pend))
    u1 = None
    for _ in range(8):
        time.sleep(10)
        u1 = uso_endpoint(key, MODELO)
        if u0 is not None and u1 is not None and u1 - u0 > 0:
            break
    if u0 is not None and u1 is not None and u1 - u0 > 0:
        custo, fonte = round(u1 - u0, 4), f"real pelo uso do endpoint ({u0:.3f} → {u1:.3f})"
    else:
        custo, fonte = round(ok * 0.06, 4), "estimado"
    print(f"{ok} geradas · US$ {custo:.3f} ({fonte})")
    if ok:
        def reg(con):
            c = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='fal.ai'").fetchone()
            con.execute("INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl,"
                        " ref_tipo, ref_id, notas) VALUES ('youtube','fabrica','fal.ai',%s,%s,'imagens',%s,'USD',%s,'youtube.canal',NULL,%s)",
                        (f"imagem {MODELO}", ok, custo, custo * float(c[0]) if c else None,
                         f"identidade historia-ptbr (logo/capa): {','.join(pend)}; custo {fonte}"))
        tentar(reg)


if __name__ == "__main__":
    main()
