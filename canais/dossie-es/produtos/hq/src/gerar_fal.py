"""Gera as artes da HQ pelo fal (tools/img_fal.py, nano-banana /edit com refs), com a config de um visual/*.yaml do 001.

Decisão do Rodrigo (24/11/2026, ~11:30): a HQ #1 sai pela fal agora, de dia (a janela do Codex é do vídeo da noite).
O img_fal.py lê o bloco `visual` do canal.yaml; aqui troco essa leitura pelo yaml do lote (refs, ref_instrucao,
estilo_prompt) + modelo, aspect_ratio da orientação e tamanho final. Todo o resto (trava por pasta, detector de
imagem preta, custo real por endpoint em financas.consumo) é o da tool.

Uso (da raiz do repo), mesmos argumentos do gerar.py (Codex) + --modelo:
  tools/.venv/bin/python canais/dossie-es/produtos/hq/src/gerar_fal.py --orient quadrado dossie-es <cenas.json> <saida> \
      --visual <visual.yaml> --tamanho 1024x1024 [--modelo google/nano-banana-2.1/edit] [--so A,B] [--teto 15]
Argumentos do Codex sem efeito aqui (--sem-fallback, --ignorar-portao, --prazo-min) são aceitos e ignorados.
"""
import os
import sys

import yaml as _yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import img_fal  # noqa: E402

ASPECTO = {"paisagem": "16:9", "retrato": "2:3", "quadrado": "1:1", "celular": "9:16"}
MODELO_PADRAO = "google/nano-banana-2.1/edit"


def tirar(flag, tem_valor=True, padrao=None):
    if flag not in sys.argv:
        return padrao
    i = sys.argv.index(flag)
    v = sys.argv[i + 1] if tem_valor else True
    del sys.argv[i:i + (2 if tem_valor else 1)]
    return v


orient = tirar("--orient", padrao="paisagem")
visual_arq = tirar("--visual")
tamanho = tirar("--tamanho")
modelo = tirar("--modelo", padrao=MODELO_PADRAO)
resolucao = tirar("--resolucao", padrao="1K")
for f in ("--sem-fallback", "--ignorar-portao"):
    tirar(f, tem_valor=False)
tirar("--prazo-min")

visual = {}
if visual_arq:
    caminho = visual_arq if os.path.isabs(visual_arq) else os.path.join(RAIZ, visual_arq)
    visual = _yaml.safe_load(open(caminho)) or {}
visual = dict(visual)
visual["modelo"] = modelo
if tamanho:
    w, h = (int(x) for x in tamanho.split("x"))
    visual["tamanho"] = {"width": w, "height": h}
params = {"aspect_ratio": ASPECTO[orient]}
qualidade = tirar("--qualidade", padrao="medium")
if "nano-banana-2" in modelo:
    params.update({"resolution": resolucao, "output_format": "jpeg", "thinking_level": "minimal"})
if "gpt-image" in modelo:  # mesma família do gerador do Codex (ChatGPT): casa melhor com as páginas já prontas
    params = {"quality": qualidade, "output_format": "jpeg"}
    if tamanho:
        params["image_size"] = {"width": w, "height": h}
visual["parametros"] = params
img_fal.PRECO_POR_IMAGEM.setdefault(modelo, 0.06)


class _Yaml:
    @staticmethod
    def safe_load(_f):
        return {"visual": visual}


img_fal.yaml = _Yaml
img_fal.main()
