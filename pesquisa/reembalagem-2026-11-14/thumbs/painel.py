"""Painéis de conferência (grade grande + 320x180). Uso: painel.py saida.jpg arq1 arq2 ... [--cel]"""
import sys
from PIL import Image
out=sys.argv[1]; fs=[a for a in sys.argv[2:] if not a.startswith('--')]; cel='--cel' in sys.argv
w,h=(320,180) if cel else (640,360); cols=2 if not cel else 4
rows=(len(fs)+cols-1)//cols; S=Image.new('RGB',(cols*w,rows*h),(20,20,20))
for i,f in enumerate(fs): S.paste(Image.open(f).convert('RGB').resize((w,h),Image.LANCZOS),((i%cols)*w,(i//cols)*h))
S.save(out,quality=88)
