import json,re,sys
G={"Geheime Staatspolizei":"Gue-jái-me Shtáats-po-li-tsái","Prinz Albrecht":"Prints Álbrejt","Reichstag":"Ráiksstag","Reich":"Raik","Göring":"Guéring","Himmler":"Jímler","Heydrich":"Jáidrik","Reinhard":"Ráinjart","Heinrich":"Háinrik","Müller":"Míler","Keitel":"Káitel","Wilhelm":"Vílhelm","Eichmann":"Áikman","Klement":"Klémen","Mossad":"Mosád","Würzburg":"Vúrtsburk","Gellately":"Yélatli","Bernburg":"Bérnburk","Benário":"Benario","Prestes":"Préstes","Getúlio":"Jetúlio","Filinto":"Filínto","Lyon":"Lión","Montluc":"Monlúk","Caluire":"Kaluír","Jean Moulin":"Yan Mulán","De Gaulle":"De Gol","Izieu":"Isié","Altmann":"Áltman","Auschwitz":"Áushvits","Draganović":"Draganóvich","Krunoslav":"Krunóslav","Klarsfeld":"Klársfelt","Serge":"Sérj","Beate":"Beáte","Priebke":"Príbke","Erich":"Érik","télex":"téleks","Telex":"Téleks","Hitler":"Hítler"}
G.pop("Hitler")
b=json.load(open("blocos.json"))
ks=sorted(G,key=len,reverse=True)
pat=re.compile("(?<!\\w)("+"|".join(map(re.escape,ks))+")(?!\\w)")
for x in b:
    t=x["texto"]; t=pat.sub(lambda m:G[m.group(1)],t); t=t.replace("—",",")
    x["texto"]=t
json.dump(b,open("blocos-voz.json","w"),ensure_ascii=False,indent=1)
print(len(b))
