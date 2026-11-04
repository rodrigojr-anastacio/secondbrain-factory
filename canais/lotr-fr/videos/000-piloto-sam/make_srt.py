from pathlib import Path
subs=[
(0.00,4.88,'Frodon part vers l’Ouest. Sam, lui, rentre dans la Comté.'),
(5.30,8.96,'Il retrouve Rosie, élève leurs enfants et garde le Livre Rouge.'),
(9.60,15.80,'Des années plus tard, après la mort de Rosie, Sam confie le livre à Elanor et rejoint les Havres Gris.'),
(16.24,17.18,'Pourquoi ?'),
(17.18,21.30,'La tradition de la Comté le présente comme le dernier Porteur de l’Anneau à prendre la mer.'),
(21.78,24.00,'Sam aussi a porté l’Anneau, brièvement.'),
(24.48,28.92,'Son départ fait écho à celui de Frodon — mais le récit ne raconte pas leurs retrouvailles.'),
(28.92,32.26,'Et partir vers Aman ne rend pas un Hobbit immortel.'),
(32.68,36.26,'Tolkien précise que les mortels autorisés à y séjourner'),
(36.58,38.04,'n’y restent que pour un temps limité.'),
(38.56,41.92,'L’Ouest offre la paix et la guérison, pas l’éternité.'),
(42.52,45.14,'Alors, Sam a-t-il revu Frodon ?'),
(45.14,47.28,'Le livre laisse la question ouverte.'),
(47.86,51.68,'Il nous montre seulement Sam qui prend, à son tour, la route de l’Ouest.'),
]
def stamp(seconds):
 ms=round(seconds*1000); h,ms=divmod(ms,3600000); m,ms=divmod(ms,60000); s,ms=divmod(ms,1000)
 return f'{h:02}:{m:02}:{s:02},{ms:03}'
out=[]
for i,(start,end,text) in enumerate(subs,1): out += [str(i),f'{stamp(start)} --> {stamp(end)}',text,'']
Path('out/lotr-pilot-fr.srt').write_text('\n'.join(out),encoding='utf-8')
print('subtitles',len(subs),'saved to out/lotr-pilot-fr.srt')
