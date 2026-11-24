import json,re
# Glossário só para a VOZ (017 Gulag; sugestões da revisão nativa, ETAPA1.md): nomes que o Fish pode ler mal.
G={"Jlevniuk":"Jlevniúk","Solzhenitsyn":"Solyenítsin","Iordache":"Iordake","Dalstrói":"Dalstróy","Kirovabad":"Kirovabád","Time":"Taim"}
b=json.load(open("blocos.json"))
ks=sorted(G,key=len,reverse=True)
pat=re.compile("(?<!\\w)("+"|".join(map(re.escape,ks))+")(?!\\w)")
for x in b:
    t=x["texto"]; t=pat.sub(lambda m:G[m.group(1)],t); t=t.replace("—",",")
    x["texto"]=t
json.dump(b,open("blocos-voz.json","w"),ensure_ascii=False,indent=1)
print(len(b))
