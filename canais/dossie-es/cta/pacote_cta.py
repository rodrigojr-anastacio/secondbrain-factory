#!/usr/bin/env python3
"""Põe o CTA da HQ no pacote de um vídeo do Dossier (24/11/2026), DEPOIS do tools/pacote.py do vídeo.

Uso: ~/workspace/fabrica-youtube/tools/.venv/bin/python canais/dossie-es/cta/pacote_cta.py <pasta do vídeo>
- Sem canais/dossie-es/cta/ATIVO: não faz nada (sai 0).
- Com ATIVO: no out/youtube.txt (e entrega/pacote/youtube.txt, se existir) põe a 1ª linha da descrição (com o link)
  logo abaixo de "## Descripción", acrescenta a seção "## COMENTARIO FIJADO" e um item no checklist; grava também
  out/comentario-fijado.txt. Idempotente (rodar 2× não duplica). Textos: cta/textos.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import encaixe  # noqa: E402

MARCA = "<!-- cta-hq -->"


def aplicar(txt, linha, comentario, link):
    if MARCA in txt:
        return txt
    i = txt.find("## Descripción\n")
    if i < 0:
        raise SystemExit("youtube.txt sem '## Descripción'")
    j = i + len("## Descripción\n")
    txt = txt[:j] + linha + "\n\n" + txt[j:]
    sec = (f"\n{MARCA}\n## COMENTARIO FIJADO (pegar como comentario del canal y fijarlo)\n{comentario}\n")
    k = txt.find("## CHECKLIST")
    txt = (txt[:k] + sec.lstrip("\n") + "\n" + txt[k:]) if k >= 0 else txt.rstrip("\n") + "\n" + sec
    item = f"- [ ] CTA de la HQ: comentario fijado publicado y fijado; enlace de la descripción ({link}) probado."
    k = txt.find("## CHECKLIST")
    if k >= 0:
        fim = txt.find("\n", k) + 1
        txt = txt[:fim] + item + "\n" + txt[fim:]
    else:
        txt = txt.rstrip("\n") + "\n\n## CHECKLIST CTA (para Rodrigo)\n" + item + "\n"
    return txt


def main():
    v = Path(sys.argv[1]).resolve()
    cta = encaixe.carregar()
    if not cta:
        print("sem ATIVO: pacote sem CTA da HQ"); return
    linha, comentario = encaixe.textos(cta["link"])
    for p in (v / "out/youtube.txt", v / "entrega/pacote/youtube.txt"):
        if p.exists():
            p.write_text(aplicar(p.read_text(), linha, comentario, cta["link"]))
            print("CTA da HQ no pacote:", p)
    (v / "out").mkdir(exist_ok=True)
    (v / "out/comentario-fijado.txt").write_text(comentario + "\n")


if __name__ == "__main__":
    main()
