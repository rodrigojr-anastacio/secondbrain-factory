# Em Relevo 006: copia (reduzida) as fotos/docs de dl/fotos para remotion/public/fotos/ (≤ 2400 px no lado maior; o Remotion não serve symlink).
from pathlib import Path
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
R = Path(__file__).resolve().parent.parent; SRC = R / "dl/fotos"; DST = R / "remotion/public/fotos"
for f in SRC.rglob("*"):
    if f.suffix.lower() not in (".jpg", ".jpeg", ".png"): continue
    d = DST / f.relative_to(SRC); d.parent.mkdir(parents=True, exist_ok=True)
    im = Image.open(f); im.thumbnail((2400, 2400), Image.LANCZOS)
    if f.suffix.lower() == ".png": im.save(d)
    else: im.convert("RGB").save(d, quality=90)
    print(d.relative_to(R), im.size)
