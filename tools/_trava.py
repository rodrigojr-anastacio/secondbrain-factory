"""Trava por pasta de saída para as tools de geração paga (img_openai.py, img_fal.py).

flock não bloqueante em <pasta>/.img.lock: se outro processo já gera na mesma pasta, avisa e sai (código 3),
em vez de os dois calcularem os mesmos pendentes e pagarem imagens em dobro (anti-padrões nº 3, Índia).
A trava cai sozinha quando o processo termina (inclusive se for morto).
"""
import datetime as dt
import fcntl
import os
import sys


def travar_pasta(pasta, nome=".img.lock"):
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, nome)
    f = open(caminho, "a+")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        f.seek(0)
        dono = f.read().strip() or "?"
        print(f"AVISO: outro processo já está gerando imagens em {pasta} ({dono}). Nada foi gerado. "
              f"Espere ele terminar (ou use --paralelo num processo só).", file=sys.stderr)
        sys.exit(3)
    f.seek(0)
    f.truncate()
    f.write(f"pid={os.getpid()} desde={dt.datetime.now().isoformat(timespec='seconds')}\n")
    f.flush()
    return f  # mantenha a referência viva até o fim do processo
