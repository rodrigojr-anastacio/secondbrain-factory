#!/usr/bin/env bash
# Gera ../amostra.pdf, ../capa.jpg e ../pagina-N.jpg a partir de amostra.html. Grátis.
# Motor: WeasyPrint (BSD) + pypdfium2 para os jpgs, num venv fora do repo:
#   uv venv ~/cache/weasyvenv && VIRTUAL_ENV=~/cache/weasyvenv uv pip install weasyprint pypdfium2 pillow
# (O Chromium headless da VPS trava no --print-to-pdf em 23/11/2026; por isso WeasyPrint.)
set -euo pipefail
cd "$(dirname "$0")"
PY="${PY:-$HOME/cache/weasyvenv/bin/python}"
"$PY" - <<'EOF'
import os, weasyprint, pypdfium2 as pdfium
out = ".."
weasyprint.HTML("amostra.html", base_url=".").write_pdf(f"{out}/amostra.pdf")
pdf = pdfium.PdfDocument(f"{out}/amostra.pdf")
print("amostra.pdf", len(pdf), "páginas", os.path.getsize(f"{out}/amostra.pdf") // 1024, "KB")
for i, page in enumerate(pdf, 1):
    im = page.render(scale=1200 / page.get_width()).to_pil().convert("RGB")  # 1200 px de largura
    name = "capa.jpg" if i == 1 else f"pagina-{i}.jpg"
    q = 86
    while True:
        im.save(f"{out}/{name}", quality=q, optimize=True, progressive=True)
        if os.path.getsize(f"{out}/{name}") <= 1_000_000 or q <= 50: break
        q -= 6
    print(name, im.size, os.path.getsize(f"{out}/{name}") // 1024, "KB")
EOF
