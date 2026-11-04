from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import subprocess
ROOT=Path('/home/hermes/workspace/lotr-pilot'); A=ROOT/'public/assets'; TMP=ROOT/'out/thumbnail_frame.png'; OUT=ROOT/'out/thumbnail-youtube.png'
ff='/home/hermes/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg'
subprocess.run([ff,'-hide_banner','-loglevel','error','-ss','12','-i',str(A/'ship_archive.webm'),'-frames:v','1','-vf','scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,eq=contrast=1.18:brightness=-0.05:saturation=0',str(TMP),'-y'],check=True)
im=Image.open(TMP).convert('RGB').resize((1280,720))
# Cinematic warm wash, then a left-side readable gradient.
warm=Image.new('RGB',im.size,(55,38,17)); im=Image.blend(im,warm,0.13)
overlay=Image.new('RGBA',im.size,(0,0,0,0)); px=overlay.load()
for x in range(im.width):
 alpha=int(210*max(0,1-x/900)**0.82)
 for y in range(im.height): px[x,y]=(3,9,13,alpha)
im=Image.alpha_composite(im.convert('RGBA'),overlay)
# Add a soft ring glow on the right as an original graphic.
glow=Image.new('RGBA',im.size,(0,0,0,0)); gd=ImageDraw.Draw(glow)
gd.ellipse((930,175,1160,535),outline=(211,166,83,155),width=24)
glow=glow.filter(ImageFilter.GaussianBlur(18)); im=Image.alpha_composite(im,glow)
d=ImageDraw.Draw(im)
d.ellipse((930,175,1160,535),outline=(241,207,135,235),width=12)
font_path=str(A/'DejaVuSans-Bold.ttf')
small=ImageFont.truetype(font_path,28); large=ImageFont.truetype(font_path,75)
d.text((78,96),'LE DERNIER PORTEUR',font=small,fill=(236,195,120,255),stroke_width=1,stroke_fill=(0,0,0,180))
for y,text in [(178,'SAM A SUIVI'),(275,'FRODON ?')]:
 d.text((72,y),text,font=large,fill=(255,250,239,255),stroke_width=4,stroke_fill=(0,0,0,220))
# Thin gold underline for a finished thumbnail treatment.
d.rounded_rectangle((78,390,510,398),radius=4,fill=(226,179,92,255))
im.convert('RGB').save(OUT,optimize=True)
print(OUT,OUT.stat().st_size)
