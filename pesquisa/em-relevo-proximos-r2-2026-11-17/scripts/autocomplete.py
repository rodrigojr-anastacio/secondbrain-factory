import sys,json,time
sys.path.insert(0,'/home/hermes/workspace/fabrica-youtube/tools')
from keywords import autocomplete
pref={'pt':["e se","e se o brasil","e se a terra","e se o mar","e se o oceano","e se a amazonia","o que aconteceria se","o que aconteceria se a terra","o que aconteceria se o brasil","como seria o brasil se","como seria a terra se","por que o brasil","por que o brasil não tem","por que o mar","por que o oceano","por que o rio","por que a terra","por que o deserto","por que a amazonia","qual o maior","qual o maior rio","qual o lugar mais","o lugar mais","quanto","quanto tempo","quanto do brasil","quanto de agua","quantos","o maior buraco","o que tem no fundo","o que tem debaixo","o que existe no fundo","e se todo o gelo","e se a terra parasse","por que não existe","por que nunca","o brasil já teve","o brasil vai","como o brasil","existe vulcão","o ponto mais","por que o brasil não tem terremoto","por que o brasil não tem vulcão","por que o brasil não tem furacão","por que o brasil não tem tsunami","e se o mar secasse","como seria a terra sem","o que tem debaixo do gelo","e se o amazonas","por que o rio amazonas","por que o pacifico e o atlantico","por que a areia","o maior rio","o maior deserto","o maior vulcão","o maior buraco do","a maior montanha","quanto o mar","quanto tempo a terra","por que o nordeste","por que o sul do brasil","por que são paulo","e se o pantanal","por que o pantanal","e se itaipu","por que a amazônia não","o brasil tem","por que o brasil é tão grande","por que o brasil fala"],
 'en':["what if the earth","what if","why does the ocean","why is the","what happens if","how much water","biggest hole","deepest","why doesn't brazil","why is brazil"],
 'es':["que pasaria si","y si la tierra","por que el oceano","por que brasil","el lugar mas","cuanto"]}
out={}
f=[]
for hl,ps in pref.items():
    for p in ps:
        s=autocomplete(p,hl,f); out[f'{hl}|{p}']=s or []
        print(hl,p,'->',(s or [])[:12],flush=True); time.sleep(1.2)
json.dump(out,open('/home/hermes/workspace/fabrica-youtube/pesquisa/em-relevo-proximos-r2-2026-11-17/autocomplete/sugestoes.json','w'),ensure_ascii=False,indent=1)
print('falhas',f)
