"""Teste do pôster gerado direto em 4K na Gemini API (tools/img_gemini.py com proporção 2:3 e imagem nativa, sem reescala).
Custo registrado pela própria tool em financas.consumo. Uso (da raiz do repo):
  tools/.venv/bin/python canais/dossie-es/produtos/manga/src/gemini_4k.py dossie-es <cenas.json> <saida> --so K01 \
      --visual canais/dossie-es/produtos/manga/src/visual-manga-4k.yaml --teto 0.6 --paralelo 1
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "..", "tools"))
import img_gemini  # noqa: E402

_corpo = img_gemini.corpo


def corpo(modelo, texto, refs_inline, params):
    c = _corpo(modelo, texto, refs_inline, params)
    c["generationConfig"]["imageConfig"]["aspectRatio"] = "2:3"
    return c


def salvar(im, destino, tam):  # guarda o tamanho nativo (é o que se quer medir)
    print("tamanho nativo:", im.size, flush=True)
    im.save(destino, "JPEG", quality=95)


img_gemini.corpo = corpo
img_gemini.salvar = salvar
img_gemini.main()
