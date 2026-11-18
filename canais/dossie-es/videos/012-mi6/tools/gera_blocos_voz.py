import json,re
# Glossário só para a VOZ (011 Templarios): nomes em espanhol saem bem; conferir franceses/portugueses depois.
G={}
b=json.load(open("blocos.json"))
ks=sorted(G,key=len,reverse=True)
pat=re.compile("(?<!\\w)(ZZZNONE)(?!\\w)")
for x in b:
    t=x["texto"]; t=pat.sub(lambda m:G[m.group(1)],t); t=t.replace("—",",")
    x["texto"]=t
json.dump(b,open("blocos-voz.json","w"),ensure_ascii=False,indent=1)
print(len(b))
