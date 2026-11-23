"""Gera as artes do mangá pelo Codex (tools/img_codex.py, cota do ChatGPT Plus, US$ 0) com orientação escolhida.

O img_codex.py pede sempre "wide 16:9 landscape"; aqui troco só essa frase da instrução (INSTR) para poder gerar
painéis em pé, capa/pôster e wallpaper de celular. Todo o resto (vagas globais, trava, log, consumo) é o da tool.

Uso (da raiz do repo):
  tools/.venv/bin/python canais/dossie-es/produtos/manga/src/gerar.py --orient retrato \
      dossie-es canais/dossie-es/produtos/manga/src/cenas-retrato.json canais/dossie-es/produtos/manga/arte \
      --visual canais/dossie-es/produtos/manga/src/visual-manga.yaml --tamanho 1024x1536 --sem-fallback
--orient: paisagem (padrão, 16:9) | retrato (2:3 em pé) | quadrado
"""
import os
import sys

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import img_codex  # noqa: E402

FRASES = {
    "paisagem": "The image must be a wide 16:9 landscape. ",
    "retrato": "The image must be a tall 2:3 PORTRAIT (vertical) image, taller than wide. ",
    "quadrado": "The image must be a square 1:1 image. ",
}

orient = "paisagem"
if "--orient" in sys.argv:
    i = sys.argv.index("--orient")
    orient = sys.argv[i + 1]
    del sys.argv[i:i + 2]
img_codex.INSTR = img_codex.INSTR.replace("The image must be a wide 16:9 landscape. ", FRASES[orient])
assert FRASES[orient] in img_codex.INSTR
img_codex.main()
