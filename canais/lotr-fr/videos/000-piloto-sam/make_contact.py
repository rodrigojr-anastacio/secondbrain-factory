from pathlib import Path
from PIL import Image,ImageDraw
import subprocess
root=Path('/home/hermes/workspace/lotr-pilot/public/assets'); ff='/home/hermes/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg'
items=[('waves.ogv','waves'),('ship_archive.webm','ship archive'),('fog.webm','fog')]
ims=[]
for file,label in items:
 out=root/f'preview_{label}.jpg'
 subprocess.run([ff,'-hide_banner','-loglevel','error','-ss','2','-i',str(root/file),'-frames:v','1','-vf','scale=640:360:force_original_aspect_ratio=decrease,pad=640:360:(ow-iw)/2:(oh-ih)/2',str(out),'-y'],check=True)
 im=Image.open(out).convert('RGB').resize((640,360)); ims.append((label,im))
for file,label in [('hills.jpg','hills'),('book.jpg','book'),('ship_painting.jpg','ship painting')]:
 im=Image.open(root/file).convert('RGB'); im.thumbnail((640,360)); canvas=Image.new('RGB',(640,360),(15,18,25)); canvas.paste(im,((640-im.width)//2,(360-im.height)//2)); ims.append((label,canvas))
sheet=Image.new('RGB',(1280,1080),(8,10,15)); draw=ImageDraw.Draw(sheet)
for i,(label,im) in enumerate(ims):
 x=(i%2)*640; y=(i//2)*360; sheet.paste(im,(x,y)); draw.rectangle((x,y,x+150,y+30),fill=(0,0,0)); draw.text((x+8,y+7),label,fill='white')
sheet.save('/home/hermes/workspace/lotr-pilot/assets_contact_sheet.jpg',quality=92)
print('/home/hermes/workspace/lotr-pilot/assets_contact_sheet.jpg')
