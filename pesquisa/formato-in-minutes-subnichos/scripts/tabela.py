"""Gera a tabela markdown de canais por subnicho (dados/canais_tabela.md) a partir de dados/canais_detalhe.json."""
import json, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(BASE, "dados/canais_detalhe.json")))
# semelhança do formato (título + visual + duração), avaliada à mão a partir de títulos, thumbs e frames
SIM = {"CEOzoned": "alto", "Built On You": "alto", "Michael Girdley": "baixo", "Crayon Capital": "médio", "FINAiUS": "médio",
 "Raphael H. Alves": "médio", "Casual Economics": "médio", "Problema de Rico - Clube do Valor": "médio (título alto; apresentador)", "Historia Del Comercio": "médio",
 "FooDiscover": "médio", "Smart Code Studios": "alto", "SciMath ": "médio", "Интернетович": "médio", "Bub Explains": "baixo",
 "Unsolved Concept": "baixo", "Your T V": "baixo", "Unknown Frequencies": "alto", "Chronofold": "alto", "Agent Flappy": "médio",
 "Historia en Minutos": "alto", "Majestic Studios": "alto", "Geschichte. Lebt.": "alto", "Geschichte Ewig": "alto",
 "ZeitreiseGeschichte": "alto", "Zeitspiegel": "alto", "América Restaurada": "médio", "O Reconstrutor": "médio", "Живые Руины": "médio",
 "Chronopolis": "alto", "Thomas Relives History": "médio", "timewarp cities": "médio", "Ancient Human Explains": "alto",
 "Reconstruindo Histórias": "médio", "Bible Origins": "baixo", "Historias de Tiempos Bíblicos": "médio", "Crayon History": "alto",
 "A História do Cristianismo": "alto", "Más Allá De Los Versos": "médio", "Mystères du Coran": "médio", "Historia Explicada": "alto",
 "Señor Mafia": "alto", "20 Minute Professor": "alto", "Historiador de Medianoche": "baixo", "Iso Jack": "médio",
 "Football ALL STARS ": "baixo", "SoccerJM": "médio", "CRG Explains": "médio", "Porão do OrdJogos": "médio", "NeverKnowsBest": "baixo",
 "TragicRoyals ": "médio", "Old Money Dynasty": "baixo", "Wallace": "médio", "Turtoon": "baixo", "Alexcalibur01": "baixo",
 "Mark The Hammer": "baixo", "Archive in Minutes": "alto", "Ruínas Vivas": "alto", "Curioso Mercado": "baixo",
 "Vozes do Brasil Antigo": "médio", "Origem Do Sabor": "médio", "Paraná no Tempo": "médio"}
ADS = {"Problema de Rico - Clube do Valor": True, "CEOzoned": True, "Built On You": False, "Unknown Frequencies": True, "Geschichte. Lebt.": True, "Historia en Minutos": True, "Ruínas Vivas": True, "Archive in Minutes": True}
LANG = {"Geschichte. Lebt.": "de", "Geschichte Ewig": "de", "ZeitreiseGeschichte": "de", "Zeitspiegel": "de", "Historia en Minutos": "es",
 "Historia Del Comercio": "es", "América Restaurada": "es", "Chronopolis": "es", "Historias de Tiempos Bíblicos": "es", "Más Allá De Los Versos": "es",
 "Historia Explicada": "es", "Señor Mafia": "es", "Historiador de Medianoche": "es", "O Reconstrutor": "pt", "Reconstruindo Histórias": "pt",
 "A História do Cristianismo": "pt", "Raphael H. Alves": "pt/en", "Problema de Rico - Clube do Valor": "pt", "Porão do OrdJogos": "pt",
 "SoccerJM": "pt", "Ruínas Vivas": "pt", "Curioso Mercado": "pt", "Vozes do Brasil Antigo": "pt", "Origem Do Sabor": "pt", "Paraná no Tempo": "pt",
 "Mystères du Coran": "fr", "Живые Руины": "ru/en", "Интернетович": "ru/en", "Michael Girdley": "en/de", "Turtoon": "fr/en"}
def k(n):
    return f"{n/1e6:.2f} mi".replace(".", ",") if n >= 1e6 else (f"{n/1e3:.0f} mil" if n >= 1e3 else str(n))
def monet(o):
    ok = o["inscritos"] >= 1000 and o["horas_12m_estim"] >= 4000
    if not ok: return "não elegível"
    if ADS.get(o["nome"]) or o["inscritos"] >= 100_000: return "provável"
    return "elegível, não confirmado"
ordem = ["empresas_negocios", "tecnologia_ciencia", "financas_economia", "comida_commodities", "guerras_especificas", "cidades_regioes",
         "religioes", "crime_drogas", "esportes", "games", "dinastias_familias", "cultura_pop_lore", "musica", "manada_referencia"]
out = []
for sub in ordem:
    xs = sorted([o for o in d if o["subnicho"] == sub], key=lambda o: -o["views_mes_recente_90d"])
    if not xs: continue
    out.append(f"\n#### {sub}\n")
    out.append("| Canal | Idioma | Idade (1º vídeo) | Vídeos (longos/formato) | Views | Inscritos | Views/mês vida [I] | Views/mês recente 90d [I] | Últimos 30 d (vídeos · views) | Mediana no formato | Monetização [I] | Semelhança | Melhor vídeo [O] |")
    out.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for o in xs:
        t = o["top3"][0] if o["top3"] else None
        ida = f"{o['idade_dias']} d" + ("" if o["lista_completa"] else " (criação)")
        out.append(f"| [{o['nome'].strip()}](https://www.youtube.com/channel/{o['id']}) | {LANG.get(o['nome'], 'en')} | {ida} | {o['n_videos']} ({o['n_longos']}/{o['n_formato']}) | {k(o['views'])} | {k(o['inscritos'])} | {k(o['views_mes_vida'])} | {k(o['views_mes_recente_90d'])} | {o['videos_30d']} · {k(o['views_videos_30d'])} | {k(o['mediana_views_formato'])} | {monet(o)} | {SIM.get(o['nome'], '?')} | " + (f"{t[3]} — {k(t[0])} ({t[1]} d, {t[2]} min)" if t else "") + " |")
open(os.path.join(BASE, "dados/canais_tabela.md"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
