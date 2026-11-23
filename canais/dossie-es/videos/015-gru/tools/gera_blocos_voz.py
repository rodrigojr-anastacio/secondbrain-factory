import json,re
# Glossário só para a VOZ (013 Núremberg): nomes em espanhol saem bem; conferir franceses/portugueses depois.
G={"GRU":"ge erre u","KGB":"ka ge be","MI6":"eme i seis","OTAN":"ótan"}
b=json.load(open("blocos.json"))
ks=sorted(G,key=len,reverse=True)
pat=re.compile("(?<!\\w)("+"|".join(map(re.escape,ks))+")(?!\\w)")
for x in b:
    t=x["texto"]; t=pat.sub(lambda m:G[m.group(1)],t); t=t.replace("—",",")
    x["texto"]=t
json.dump(b,open("blocos-voz.json","w"),ensure_ascii=False,indent=1)
print(len(b))
