"""Monta a #1 de "Expedientes Secretos" a partir da fonte única (e1, 24/11/2026).

Entrada (fonte única): roteiro/garbo.py, roteiro/lacosa.py (páginas e quadros), personagens.py (descrições fixas e
folhas), layouts.py (formas dos quadros), extras.py (folhas, capas das histórias, pôster, wallpapers, páginas de texto).
Saída (tudo em 001/):
  ROTEIRO.md                      roteiro quadro a quadro legível (gerado; não edite à mão)
  livro.json                      as ~42 páginas para o `src/diagramar.py --livro` (balões já posicionados)
  cenas-*.json                    prompts só de conteúdo, um arquivo por (lote, orientação, config de personagem)
  visual/visual-*.yaml            config visual de cada lote (estilo v3 + folhas dos personagens do quadro; sem folha
                                  quando não há personagem com folha, regra da v3)
  plano-imagens.json, IMAGENS.md  ordem da e2 (folhas → capas → quadros → pôster → wallpapers), comandos e contagem
Uso (raiz do repo):
  tools/.venv/bin/python canais/dossie-es/produtos/hq/001/montar.py            # gera tudo acima
  tools/.venv/bin/python canais/dossie-es/produtos/hq/001/montar.py --pdf      # + rascunho.pdf (placeholders cinza)
"""
import json
import os
import runpy
import subprocess
import sys
from collections import OrderedDict

AQUI = os.path.dirname(os.path.abspath(__file__))
HQ = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(HQ, "..", "..", "..", ".."))
sys.path.insert(0, AQUI)
import layouts as LY  # noqa: E402
import personagens as PE  # noqa: E402
import extras as EX  # noqa: E402

ARTE = "arte-001"                      # pasta das artes novas (fora do git), relativa a produtos/hq/
FOLHAS_DIR = os.path.join(HQ, ARTE, "folhas")
ESTILO_REFS = [
    "/home/hermes/workspace/fabrica-youtube/canais/dossie-es/produtos/hq/arte-v2/P101.jpg",
    "/home/hermes/workspace/fabrica-youtube/canais/dossie-es/produtos/hq/arte-v2/P102.jpg",
    "videos/015-gru/imagens/I040.jpg",
]
ESTILO_INSTR = ("The first three attached images are STYLE references only: draw in exactly their art style (clean "
                "graphic novel ink illustration, even bold black outlines, large areas of flat matte color, simple "
                "hard-edged cel shadows, cool slate blue, olive and charcoal palette with warm lamp light and deep red "
                "accents); do not copy their content, people or composition. Make the colour slightly richer and the "
                "lighting a bit more dramatic than the references (strong contrast of warm lamp light against cool "
                "blue night, crisp rim light, deep shadows), but keep the same ink line and flat colour; not a glossy "
                "superhero style. ")
ESTILO_PROMPT = ("Clean graphic novel ink illustration, western comic book art, even bold black ink outlines, large flat "
                 "matte color areas with simple hard-edged cel shadows, minimal hatching, no gradients, realistic adult "
                 "proportions and faces, cool slate blue, olive green and charcoal palette with warm lamp light and "
                 "small deep red accents, dramatic lighting, dynamic comic camera angle, no text, no speech balloons, "
                 "no letters, no captions, no panel border, no frame, no swastikas or extremist insignia")
ORDINAL = ["fourth", "fifth", "sixth"]
SLOT_NOME = {
    "A5": ["faixa larga no topo", "largo, calha diagonal", "estreito em pé, calha diagonal", "faixa larga", "faixa baixa"],
    "B5": ["faixa larga no topo", "largo, calha diagonal", "ALTO em pé à direita (2 linhas), calha diagonal",
           "largo embaixo à esquerda, calha diagonal", "faixa baixa"],
    "C4": ["GRANDE no topo", "par, calha diagonal (esq.)", "par, calha diagonal (dir.)", "faixa larga"],
    "D3": ["SPLASH quase página", "par, calha diagonal (esq.)", "par, calha diagonal (dir.)"],
    "E6": ["topo esq.", "topo dir.", "meio esq., calha diagonal", "meio dir., calha diagonal", "baixo largo",
           "baixo estreito em pé"],
    "F1": ["PÁGINA INTEIRA (splash)"],
    "G4": ["faixa larga no topo", "coluna ALTA à esquerda, calha diagonal", "direita cima, calha diagonal",
           "direita baixo, calha diagonal"],
}
FRENTE = 3  # capa, créditos, sumário


def expandir(prompt):
    for k, v in PE.DESC.items():
        prompt = prompt.replace("{%s}" % k, v)
    assert "{" not in prompt, prompt
    return prompt


def combo(chars):
    chars = sorted([c for c in chars if c in PE.FOLHA][:2])  # ordem canônica: menos lotes/configs
    return chars, ("-".join(c.lower() for c in chars) if chars else "sem")


def folha_path(c):
    arq, existe = PE.FOLHA[c]
    return arq if existe else os.path.join(FOLHAS_DIR, arq)


def visual_yaml(chars, nome):
    refs = ESTILO_REFS + [folha_path(c) for c in chars]
    instr = ESTILO_INSTR
    for i, c in enumerate(chars):
        instr += ("The %s attached image is the CHARACTER MODEL SHEET of %s: whenever %s appears, draw them with "
                  "exactly this face, hair, build and clothing; do not copy the sheet layout. "
                  % (ORDINAL[i], PE.DESC[c], c))
    instr += "No panel border, no frame. Scene: "
    txt = ("# Gerado por 001/montar.py (e1 24/11/2026): estilo v3 + folhas de %s\n" % (", ".join(chars) or "nenhum")
           + "refs: %s\nref_instrucao: %s\nestilo_prompt: %s\n" % (json.dumps(refs), json.dumps(instr),
                                                                   json.dumps(ESTILO_PROMPT)))
    os.makedirs(os.path.join(AQUI, "visual"), exist_ok=True)
    with open(os.path.join(AQUI, "visual", "visual-%s.yaml" % nome), "w") as f:
        f.write(txt)
    return "canais/dossie-es/produtos/hq/001/visual/visual-%s.yaml" % nome


# ---------- textos: posição automática (rascunho; a e2 ajusta "pos"/"alvo" olhando a arte) ----------
def posicionar(textos, caixa):
    _, _, w, h = caixa
    estreito = w < 700
    out = []
    lado_y = {"e": 0.18, "d": 0.18, "c": 0.18}
    n_leg = 0
    for t in textos:
        tipo = t[0]
        if tipo in ("legenda", "carta"):
            larg = int(w * 0.9) if estreito else int(min(620, max(320, w * 0.55)))
            if n_leg == 0:
                pos = [0.02, 0.03]
                lado_y["e"] = max(lado_y["e"], 0.30 if h > 900 else 0.42)
                if estreito:
                    lado_y["c"] = lado_y["d"] = lado_y["e"]
            elif n_leg == 1:
                pos = [0.02, 0.80 if h > 700 else 0.72]
            else:
                pos = [0.45, 0.03]
            n_leg += 1
            e = {"tipo": tipo, "pos": pos, "larg": larg, "texto": t[1]}
            if tipo == "carta":
                e["px"] = 30
            out.append(e)
        elif tipo in ("fala", "pensa", "grito"):
            lado = (t[3] if len(t) > 3 else "e") if not estreito else "c"
            x = {"e": 0.25, "d": 0.75, "c": 0.5}[lado]
            y = lado_y[lado]
            lado_y[lado] = min(y + 0.24, 0.85)
            larg = int(w * 0.78) if estreito else int(min(360, max(240, w * 0.36)))
            alvo = [x + (0.06 if lado == "e" else -0.06 if lado == "d" else 0), min(y + min(0.30, 260 / h), 0.95)]
            out.append({"tipo": tipo, "pos": [x, y], "larg": larg, "alvo": alvo, "texto": t[1], "quem": t[2]})
        elif tipo == "sfx":
            out.append({"tipo": "sfx", "pos": [0.80, 0.62], "texto": t[1], "px": 84 if w > 900 else 64, "rot": -8,
                        "cor": "vermelho"})
        else:
            raise ValueError(t)
        if len(t) > 4 and isinstance(t[4], dict):  # ajuste fino (pos/alvo/larg/px/rot) gravado no roteiro
            out[-1].update(t[4])
    return out


def carregar(nome):
    d = runpy.run_path(os.path.join(AQUI, "roteiro", nome + ".py"))
    for pg in d["PAGINAS"]:
        n_slots = len(LY.LAYOUTS[pg["layout"]])
        assert len(pg["quadros"]) == n_slots, (nome, pg["n"], pg["layout"], len(pg["quadros"]))
    return d


def main():
    import glob
    for velho in glob.glob(os.path.join(AQUI, "cenas-*.json")) + glob.glob(os.path.join(AQUI, "visual", "*.yaml")):
        os.remove(velho)  # tudo aqui é gerado: regera do zero
    historias = [carregar("garbo"), carregar("lacosa")]
    ids_novos = {}
    lotes = OrderedDict()          # (grupo, orient, combo) -> [cenas]
    yamls = {}
    paginas_livro = []
    pag_livro = FRENTE
    sumario = []
    contagem = {"quadros": 0, "novos": 0, "reuso": 0, "existentes": 0}
    md = ["# Expedientes Secretos #1: roteiro quadro a quadro (e1, 24/11/2026)", "",
          "Gerado por `montar.py` a partir de `roteiro/garbo.py` e `roteiro/lacosa.py` (fonte única: edite lá e rode de "
          "novo). Espanhol LatAm neutro. Fatos e liberdades em `FATOS.md`; personagens em `PERSONAGENS.md`.", "",
          "Legenda dos quadros: **id** (orientação · slot do layout · personagens com folha) · descrição visual "
          "(pt-BR) · textos. `[existe]` = arte da amostra v3; `[reusa X]` = mesma arte do quadro X com outro recorte.",
          ""]
    for hi, H in enumerate(historias, 1):
        hist = H["HISTORIA"]
        ex = EX.CAPAS[hist]
        pag_livro += 1
        paginas_livro.append(dict(ex["pagina"], tipo="capa_historia", saida="capa-" + hist, img=ex["id"],
                                  placeholder=ex["desc"]))
        sumario.append((H["TITULO"], pag_livro, ex["pagina"]["subtitulo"]))
        md += ["---", "", "## Expediente %d: %s" % (hi, H["TITULO"]), "",
               "**Capa da história** (livro p. %d, `%s`, retrato): %s" % (pag_livro, ex["id"], ex["desc"]), ""]
        cap_atual = None
        for pg in H["PAGINAS"]:
            pag_livro += 1
            if pg["cap"] != cap_atual:
                cap_atual = pg["cap"]
                md += ["### Cap. %d: %s" % (cap_atual, H["CAPITULOS"][cap_atual]), ""]
                sumario.append(("Cap. %d · %s" % (cap_atual, H["CAPITULOS"][cap_atual].capitalize()), pag_livro, None))
            slots = LY.LAYOUTS[pg["layout"]]
            md += ["#### Pág. %d (livro p. %d) · layout %s · %d quadros" % (pg["n"], pag_livro, pg["layout"],
                                                                            len(slots)),
                   "_%s_" % pg.get("nota", ""), ""]
            paineis, textos = [], []
            for q, slot in zip(pg["quadros"], slots):
                contagem["quadros"] += 1
                orient = LY.orientacao(slot)
                cx = LY.caixa(slot)
                chars, cmb = combo(q.get("chars") or [])
                img, arte_dir, marca = q["id"], ARTE, ""
                if q.get("arte"):
                    img, arte_dir, marca = q["arte"], q["arte_dir"], " `[existe %s]`" % q["arte"]
                    contagem["existentes"] += 1
                elif q.get("reusa"):
                    img, marca = q["reusa"], " `[reusa %s]`" % q["reusa"]
                    contagem["reuso"] += 1
                else:
                    assert q.get("prompt"), q["id"]
                    contagem["novos"] += 1
                    grupo = "quadros-" + hist
                    nome_y = cmb
                    if nome_y not in yamls:
                        yamls[nome_y] = visual_yaml(chars, nome_y)
                    lotes.setdefault((grupo, orient, cmb), []).append({"id": q["id"], "prompt": expandir(q["prompt"])})
                    ids_novos[q["id"]] = orient
                painel = dict(slot, img=img, arte_dir=arte_dir, orient=orient, foco=q.get("foco") or [0.5, 0.5],
                              placeholder=q.get("desc", ""))
                paineis.append(painel)
                for t in posicionar(q.get("textos") or [], cx):
                    t["painel"] = img
                    textos.append(t)
                # roteiro legível
                md.append("- **%s** (%s · %s%s)%s · %s" % (
                    q["id"], orient, SLOT_NOME[pg["layout"]][len(paineis) - 1],
                    (" · " + ", ".join(q.get("chars") or [])) if q.get("chars") else "", marca, q.get("desc", "")))
                for t in q.get("textos") or []:
                    if t[0] == "legenda":
                        md.append("  - LEGENDA: %s" % t[1])
                    elif t[0] == "carta":
                        md.append("  - CARTA/DOCUMENTO: %s" % t[1])
                    elif t[0] == "sfx":
                        md.append("  - SFX: %s" % t[1])
                    else:
                        md.append("  - %s%s: %s" % (t[2], {"fala": "", "pensa": " (pensa)", "grito": " (grita)"}[t[0]],
                                                    t[1]))
            # pp. já prontas na amostra v3 (todas as artes existem): textos com a posição original do src/paginas.json
            if pg["quadros"] and all(q.get("arte") for q in pg["quadros"]) and H["HISTORIA"] == "garbo":
                orig = {p["saida"]: p for p in json.load(open(os.path.join(HQ, "src", "paginas.json")))["paginas"]}
                if "pagina-%d" % pg["n"] in orig:
                    textos = orig["pagina-%d" % pg["n"]]["textos"]
            # painéis com a mesma arte (reuso) precisam de chave única para os balões
            vistos = {}
            for p in paineis:
                vistos[p["img"]] = vistos.get(p["img"], 0) + 1
            assert all(v == 1 for v in vistos.values()), ("mesma arte 2x na página", pg["n"], hist)
            md.append("")
            paginas_livro.append({"tipo": "quadros", "saida": "%s-%02d" % (hist, pg["n"]), "estilo": "cor",
                                  "arte": ARTE, "numero": pag_livro,
                                  "cabecalho": "EXPEDIENTES SECRETOS #1  ·  %s  ·  CAP. %d: %s" % (
                                      H["TITULO"], pg["cap"], H["CAPITULOS"][pg["cap"]]),
                                  "paineis": paineis, "textos": textos})
    # reuso: confere que o quadro reusado é gerado
    for H in historias:
        for pg in H["PAGINAS"]:
            for q in pg["quadros"]:
                if q.get("reusa"):
                    assert q["reusa"] in ids_novos, ("reusa inexistente", q["id"], q["reusa"])

    # ---------- livro completo ----------
    fim = EX.paginas_fim(pag_livro)
    livro = {"saida_dir": "001/rascunho", "pdf": "001/rascunho.pdf", "larg_pdf": 1200, "estilo": "cor",
             "paginas": [EX.CAPA_GERAL, EX.CREDITOS, EX.sumario(sumario, pag_livro + 1)] + paginas_livro + fim}
    json.dump(livro, open(os.path.join(AQUI, "livro.json"), "w"), ensure_ascii=False, indent=1)

    # ---------- lotes de imagens ----------
    plano = []
    yamls["sem"] = yamls.get("sem") or visual_yaml([], "sem")

    def lote(ordem, nome, cenas, orient, cmb, saida):
        arq = "cenas-%s.json" % nome
        json.dump(cenas, open(os.path.join(AQUI, arq), "w"), ensure_ascii=False, indent=1)
        tam = "%dx%d" % LY.TAMANHO[orient]
        cmd = ("tools/.venv/bin/python canais/dossie-es/produtos/hq/src/gerar.py --orient %s dossie-es "
               "canais/dossie-es/produtos/hq/001/%s canais/dossie-es/produtos/hq/%s --visual %s --tamanho %s "
               "--sem-fallback --ignorar-portao --prazo-min 8 --notas hq001" % (orient, arq, saida, yamls[cmb], tam))
        plano.append({"ordem": ordem, "lote": nome, "n": len(cenas), "orient": orient, "visual": cmb,
                      "saida": saida, "cenas": "001/" + arq, "comando": cmd})

    # 1 folhas (estilo sem folha; paisagem)
    lote(1, "folhas", [{"id": k, "prompt": v} for k, v in EX.FOLHAS.items()], "paisagem", "sem", ARTE + "/folhas")
    # 2 capas das histórias (retrato)
    for hist, c in EX.CAPAS.items():
        chars, cmb = combo(c.get("chars", []))
        if cmb not in yamls:
            yamls[cmb] = visual_yaml(chars, cmb)
        lote(2, "capa-" + hist, [{"id": c["id"], "prompt": expandir(c["prompt"])}], "retrato", cmb, ARTE)
    # 3 quadros (Garbo antes de La Cosa; dentro, por orientação e config)
    for (grupo, orient, cmb), cenas in lotes.items():
        lote(3, "%s-%s-%s" % (grupo, orient, cmb), cenas, orient, cmb, ARTE)
    # 4 pôster, 5 wallpapers
    for ordem, item in [(4, EX.POSTER)] + [(5, w) for w in EX.WALLPAPERS]:
        chars, cmb = combo(item.get("chars", []))
        if cmb not in yamls:
            yamls[cmb] = visual_yaml(chars, cmb)
        lote(ordem, item["id"].lower(), [{"id": item["id"], "prompt": expandir(item["prompt"])}], item["orient"], cmb,
             ARTE)
    plano.sort(key=lambda p: p["ordem"])
    total = sum(p["n"] for p in plano)
    json.dump({"total_imagens": total, "contagem_quadros": contagem, "lotes": plano},
              open(os.path.join(AQUI, "plano-imagens.json"), "w"), ensure_ascii=False, indent=1)

    nomes = {1: "folhas de personagem", 2: "capas das histórias", 3: "quadros", 4: "pôster", 5: "wallpapers"}
    im = ["# Imagens da etapa 2 (gerado por montar.py)", "",
          "Total a gerar: **%d imagens** (meta ≤ 180). Quadros no livro: %d = %d novos + %d reusos + %d já prontos "
          "(amostra v3). Capa geral (`capa.png`) já existe (job do CTA)." % (
              total, contagem["quadros"], contagem["novos"], contagem["reuso"], contagem["existentes"]), "",
          "| ordem | etapa | imagens |", "|---|---|---|"]
    for o in range(1, 6):
        im.append("| %d | %s | %d |" % (o, nomes[o], sum(p["n"] for p in plano if p["ordem"] == o)))
    im += ["", "## Lotes (rodar nesta ordem; cada comando pula o que já existe)", ""]
    for p in plano:
        im.append("- **%s** (%d, %s, config `%s`) → `%s`" % (p["lote"], p["n"], p["orient"], p["visual"], p["saida"]))
    open(os.path.join(AQUI, "IMAGENS.md"), "w").write("\n".join(im) + "\n")
    md.insert(4, "**Livro:** %d páginas · quadros: %d (%d novos, %d reusos, %d da amostra) · imagens da e2: %d." % (
        len(livro["paginas"]), contagem["quadros"], contagem["novos"], contagem["reuso"], contagem["existentes"],
        total))
    md.insert(5, "")
    open(os.path.join(AQUI, "ROTEIRO.md"), "w").write("\n".join(md) + "\n")
    print("páginas", len(livro["paginas"]), "| quadros", contagem, "| imagens e2", total)

    if "--pdf" in sys.argv:
        subprocess.run([os.path.join(RAIZ, "tools", ".venv", "bin", "python"), os.path.join(HQ, "src", "diagramar.py"),
                        "--livro", os.path.join(AQUI, "livro.json")], check=True)


if __name__ == "__main__":
    main()
