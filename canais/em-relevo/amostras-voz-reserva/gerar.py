"""Amostras de voz de reserva (Fish) do Em Relevo, 16/11/2026. Mesmo trecho do 005 (hook b01–b04 + transição b20).
Uso: tools/.venv/bin/python canais/em-relevo/amostras-voz-reserva/gerar.py [letra...]
Gera brutos/<letra>-hook.mp3 e brutos/<letra>-trans.mp3 (cache: não regera o que existe) e registra o custo em financas.consumo
(projeto em-relevo, sem ref_id). A chave do Fish é lida por tools/tts_fish.chave() e nunca impressa."""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
FAB = os.path.abspath(os.path.join(AQUI, "../../.."))
sys.path.insert(0, os.path.join(FAB, "tools"))
from tts_fish import chave, credito, gerar, preco  # noqa: E402
from db import tentar  # noqa: E402

VOZES = {  # letra: (id, nome no Fish, modelo)
    "A": ("1573caa3d6444e16a28eab1f094e1416", "Putinha 1", "drama-3"),
    "B": ("8f50c4c145e44ec280fb759b32934890", "Caine (Brazilian Portuguese)", "drama-3"),
    "C": ("e8bccb7beecd46c6a1c64813e0238fa9", "#NATASHA", "drama-3"),
    "D": ("5b5a485751824c1993e210602cee16cb", "Voz feminina", "drama-3"),
    "E": ("0ba1afd27db44eb2b4cb27fd331b93aa", "Narrador de Historias e Ciências", "drama-3"),
}
if os.path.exists(os.path.join(AQUI, "extra.json")):
    VOZES.update({k: tuple(v) for k, v in json.load(open(os.path.join(AQUI, "extra.json"))).items()})

B = {x["id"]: x for x in json.load(open(os.path.join(FAB, "canais/em-relevo/videos/005-enchente-porto-alegre-2024/shared/blocos.json")))}
def limpo(i):
    return " ".join(B[i]["fala"].split())
TEXTOS = {"hook": "\n\n".join(limpo(i) for i in ["b01", "b02", "b03", "b04"]), "trans": limpo("b20")}

def main():
    letras = sys.argv[1:] or list(VOZES)
    key = chave()
    os.makedirs(os.path.join(AQUI, "brutos"), exist_ok=True)
    c0 = credito(key)
    gasto = {}
    try:
        for L in letras:
            vid, nome, modelo = VOZES[L]
            for parte, txt in TEXTOS.items():
                p = os.path.join(AQUI, "brutos", f"{L}-{parte}.mp3")
                if os.path.exists(p):
                    continue
                gerar(key, vid, modelo, 1.0, txt, p)
                gasto[modelo] = gasto.get(modelo, 0) + len(txt.encode())
                print(f"{L} {parte} ok ({nome}, {modelo})", flush=True)
    finally:
        for modelo, n in gasto.items():
            custo = n * preco(modelo) / 1e6
            def reg(con, modelo=modelo, n=n, custo=custo):
                cam = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='Fish Audio'").fetchone()
                con.execute("INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, notas)"
                            " VALUES ('youtube','em-relevo','Fish Audio',%s,%s,'bytes',%s,'USD',%s,%s)",
                            (f"tts {modelo} amostra voz reserva", n, custo, custo * float(cam[0]) if cam else None,
                             "canais/em-relevo/amostras-voz-reserva (16/11/2026)"))
            tentar(reg)
            print(f"{modelo}: {n} bytes · US$ {custo:.4f} registrado")
        print(f"crédito Fish antes {c0} · depois {credito(key)}")

if __name__ == "__main__":
    main()
