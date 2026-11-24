import json,re
# Glossário só para a VOZ (016 MKUltra, 24/11/2026): respelling de nomes ingleses/siglas; o texto de tela fica em blocos.json.
G={"MKUltra":"MK Ultra","MKSearch":"MK Sérch","KUBARK":"Kiúbark","Toughkenamon":"Tafkenéimon","Geschickter":"Géshikter","LSD":"ele ese de","fluothane":"fluotén"}
b=json.load(open("blocos.json"))
ks=sorted(G,key=len,reverse=True)
pat=re.compile("(?<!\\w)("+"|".join(map(re.escape,ks))+")(?!\\w)")
for x in b:
    t=x["texto"]; t=pat.sub(lambda m:G[m.group(1)],t); t=t.replace("—",",")
    x["texto"]=t
json.dump(b,open("blocos-voz.json","w"),ensure_ascii=False,indent=1)
print(len(b))
