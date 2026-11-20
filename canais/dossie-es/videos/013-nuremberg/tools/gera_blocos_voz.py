import json,re
# Glossário só para a VOZ (012 MI6): nomes em espanhol saem bem; conferir franceses/portugueses depois.
G={"MI6":"eme i seis","MI5":"eme i cinco","BSC":"be ese ce","Estación M":"Estación eme","Ordzhonikidze":"Ordyonikídze","Exocet":"Exoset","Joe K":"Yóu Kéi","Maschwitz":"Máshvits"}
b=json.load(open("blocos.json"))
ks=sorted(G,key=len,reverse=True)
pat=re.compile("(?<!\\w)("+"|".join(map(re.escape,ks))+")(?!\\w)")
for x in b:
    t=x["texto"]; t=pat.sub(lambda m:G[m.group(1)],t); t=t.replace("—",",")
    x["texto"]=t
json.dump(b,open("blocos-voz.json","w"),ensure_ascii=False,indent=1)
print(len(b))
