#!/usr/bin/env python
"""Junta contagens.json + candidatos_brutos.json + commons_buscas.json em material.json, calcula a nota
automatica (0-5) de "material farto e livre" e imprime a tabela em Markdown.
Rode depois de contar.py, candidatos.py, commons_busca.py e itens_chave.py; os .json intermediarios podem ser apagados.

Nota automatica (antes do ajuste manual, que fica em AJUSTE com o motivo):
  epoca  = fotos NARA online + 10 x filmes NARA online + fotos NHHC + 2 x arquivos do Commons vindos da LoC
           >= 3000: 3 | >= 1000: 2.5 | >= 500: 2 | >= 200: 1.5 | >= 50: 1 | senao 0.5
  atual  = arquivos do Commons vindos do DVIDS + arquivos nas categorias do Commons (diretos + 1 nivel)
           >= 2000: 2 | >= 800: 1.5 | >= 300: 1 | >= 100: 0.5 | senao 0
"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda n: os.path.join(BASE, n)  # noqa: E731

AJUSTE = {
    "hashima": (-0.5, "material de epoca e japones (sem PD automatico); quase nada em arquivo dos EUA; hoje so CC BY/BY-SA; nao e lugar de guerra americano"),
    "enewetak": (+0.5, "filmes DOE/AEC de Ivy Mike (gov.doe.*, PD) + fotos DOE do Runit Dome; contagem por frase subestima"),
    "chernobyl": (-3, "nao e EUA; material sovietico/ucraniano sem PD claro; so contraste"),
    "area51": (-1.5, "quase sem material oficial liberado (fotos CIA/USGS esparsas); contagem do IA/NHHC e ruido"),
    "camp-century": (+0.5, "pouco volume, mas o filme do Exercito 'Camp Century' / The Big Picture e fotos do Army sao PD e unicos"),
    "mittelwerk": (-0.5, "fotos NARA vem do campo Dora/Nordhausen (tema sensivel, atrocidade); interior da fabrica: pouco"),
    "nts": (0, "22 mil fotos NNSA/DOE no NARA (series 434/326) + filmes do DOE no IA: material imenso"),
    "trinity": (+1, "pouco no NARA por frase, mas LANL/DOE/Army: fotos e filme Trinity PD e muito conhecidos; open house anual (fotos DVIDS/White Sands)"),
    "midway": (+0.5, "filme de John Ford (PD) + 80-G em ~6000 px + fotos USFWS PD do lugar hoje (hangar, baterias, pistas)"),
    "bikini": (+0.5, "filmes oficiais de Crossroads (PD) e 1.268 imagens no Smithsonian; hoje: Landsat PD + relatorio NPS 1991 dos naufragios"),
    "tinian": (+0.5, "509th/Enola Gay (PD) + DVIDS forte em North Field hoje (Forager, Cope North)"),
    "corregidor": (-0.5, "periodo bom, mas o 'hoje' e quase todo CC BY / CC BY-SA no Commons; DVIDS fraco (o proxy pega nomes de unidades)"),
    "diego-garcia": (-1, "3.800 fotos DVIDS de base ativa, mas pouca historia de guerra em arquivo; acesso de imagem da base e controlado"),
    "pearl-harbor": (0, "o maior acervo; o difícil e ser original"),
    "omaha": (0, "IWM e agencias dominam a iconografia famosa (Capa = Magnum, NAO); NARA/Signal Corps/USCG suficientes"),
}


def pts_epoca(v):
    return 3 if v >= 3000 else 2.5 if v >= 1000 else 2 if v >= 500 else 1.5 if v >= 200 else 1 if v >= 50 else 0.5


def pts_atual(v):
    return 2 if v >= 2000 else 1.5 if v >= 800 else 1 if v >= 300 else 0.5 if v >= 100 else 0


def main():
    # sem os intermediarios, recalcula a partir do proprio material.json
    cont = json.load(open(P("contagens.json"))) if os.path.exists(P("contagens.json")) else json.load(open(P("material.json")))["temas"]
    out = {"gerado_em": None, "metodo": __doc__, "temas": {}}
    for k, r in cont.items():
        n = r.get("nara", {})
        epoca = n.get("fotos", 0) + 10 * n.get("filmes", 0) + r.get("nhhc_fotos", 0) + 2 * r.get("commons_loc", 0)
        atual = r.get("commons_dvids", 0) + r.get("commons_cats_total", 0)
        auto = min(5, pts_epoca(epoca) + pts_atual(atual))
        aj, motivo = AJUSTE.get(k, (0, ""))
        nota = max(0, min(5, auto + aj))
        r.update({"indice_epoca": epoca, "indice_atual": atual, "nota_auto": auto, "ajuste": aj,
                  "ajuste_motivo": motivo, "nota": nota})
        out["temas"][k] = r
    for nome, chave in [("candidatos_brutos.json", "candidatos_brutos"), ("commons_buscas.json", "commons_buscas"), ("itens_chave.json", "itens_chave_auto")]:
        if os.path.exists(P(nome)):
            out[chave] = json.load(open(P(nome)))
    import time
    out["gerado_em"] = time.strftime("%Y-%m-%d %H:%M")
    if os.path.exists(P("material.json")):  # preserva blocos acrescentados a mao (ex.: licencas)
        velho = json.load(open(P("material.json")))
        for kk in velho:
            if kk not in out or (kk in ("candidatos_brutos", "commons_buscas", "itens_chave_auto") and not os.path.exists(P({"candidatos_brutos": "candidatos_brutos.json", "commons_buscas": "commons_buscas.json", "itens_chave_auto": "itens_chave.json"}[kk]))):
                out[kk] = velho[kk]
    json.dump(out, open(P("material.json"), "w"), ensure_ascii=False, indent=1)
    linhas = sorted(out["temas"].items(), key=lambda kv: (-kv[1]["nota"], -kv[1]["indice_epoca"]))
    print("| # | Tema | Nota | NARA fotos | NARA filmes | NHHC fotos | IA filmes | Commons cat. | Commons DVIDS | Commons LoC | Ajuste |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for i, (k, r) in enumerate(linhas, 1):
        n = r.get("nara", {})
        print(f"| {i} | {r['nome']} | **{r['nota']:g}** | {n.get('fotos', '-')} | {n.get('filmes', '-')} | {r.get('nhhc_fotos', '-')} | "
              f"{r.get('ia_movies', '-')} | {r.get('commons_cats_total', '-')} | {r.get('commons_dvids', '-')} | {r.get('commons_loc', '-')} | "
              f"{(f'{r['ajuste']:+g}: ' + r['ajuste_motivo']) if r['ajuste'] else ''} |")


if __name__ == "__main__":
    main()
