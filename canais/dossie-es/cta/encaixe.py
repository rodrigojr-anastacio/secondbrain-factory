"""Encaixe do CTA da HQ "Expedientes Secretos" nos vídeos novos do Dossier en Minutos (24/11/2026).

Usado pelo tools/build.py de cada vídeo (016 em diante) e pelo tools/pacote.py. Regras (brief do Rodrigo, 24/11):
- interruptor: o CTA só entra se existir canais/dossie-es/cta/ATIVO (1ª linha = link da Hotmart). Sem ele, nada muda
  na montagem (timeline, .srt, capítulos e áudio idênticos aos de antes). Quem cria o ATIVO é o orquestrador.
- posição: na troca de capítulo ("EXPEDIENTE N") cujo início fica mais perto de 37,5% da duração (faixa 35–40%),
  nunca nos 2 primeiros minutos nem no último minuto.
- o bloco (cta-hq.mp4, 15 s) entra inteiro entre o fim do bloco anterior e o cartão do capítulo; a voz entra na faixa de
  voz do vídeo (a trilha do vídeo faz ducking sozinha) e os SFX do bloco (cta-sfx.wav) na faixa de efeitos.
Testes: CTA_ATIVO=<arquivo de teste> aponta para outro ATIVO (nunca crie o ATIVO de verdade num teste).
"""
import json
import os
import re
from pathlib import Path

DIR = Path(os.environ.get("CTA_DIR", Path(__file__).resolve().parent))
GAP_ANTES = 0.5          # s de silêncio entre o fim do bloco anterior e o início do CTA
XF = 8                   # quadros de fusão na entrada e na saída do bloco
FAIXA = (0.35, 0.40)
MIN_INI = 120.0          # nunca nos 2 primeiros minutos
MIN_FIM = 60.0           # nem no último minuto


def ativo_path():
    return Path(os.environ.get("CTA_ATIVO", DIR / "ATIVO"))


def carregar():
    """None sem ATIVO; senão o cta.json + link + caminhos absolutos."""
    p = ativo_path()
    if not p.exists():
        return None
    link = next((l.strip() for l in p.read_text().splitlines() if l.strip()), "")
    cfg = json.load(open(DIR / "cta.json"))
    cfg["link"] = link
    cfg["video_abs"] = str(DIR / cfg["arquivos"]["video"])
    cfg["voz_abs"] = str(DIR / cfg["arquivos"]["voz"])
    cfg["sfx_abs"] = str(DIR / cfg["arquivos"]["sfx"])
    return cfg


def escolher(inicios, dur):
    """inicios: [(id_do_bloco, t_ini_s)] dos blocos que abrem capítulo, na montagem SEM CTA. Devolve o id ou None."""
    alvo = sum(FAIXA) / 2
    ok = [(abs(t / dur - alvo), bid, t) for bid, t in inicios if MIN_INI <= t <= dur - MIN_FIM]
    if not ok:
        return None
    return min(ok)[1]


def textos(link=None):
    """(1ª linha da descrição, comentário fixado) de textos.md, com {LINK} trocado pelo link do ATIVO."""
    md = (DIR / "textos.md").read_text()
    def bloco(titulo):
        m = re.search(r"^###\s+" + re.escape(titulo) + r".*?\n```[a-z]*\n(.*?)\n```", md, re.S | re.M)
        return m.group(1).strip() if m else ""
    link = link if link is not None else (carregar() or {}).get("link", "{LINK}")
    return bloco("1ª linha da descrição").replace("{LINK}", link), bloco("Comentário fixado").replace("{LINK}", link)
