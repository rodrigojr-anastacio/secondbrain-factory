"""Grava em youtube.garimpo_canais os canais analisados neste levantamento (formula, decisao, notas)."""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/workspace/fabrica-youtube/tools"))
from db import conectar
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
C = json.load(open(os.path.join(BASE, "dados", "canais_nicho.json")))
N = "nichos-editorial-2026-11: "
D = {  # id: (formula, decisao, notas)
 "UCdyNZcgs1ZcFFM1cy4g04og": ("en: economia de notícia 'WTF just happened to <país>?' com gráficos editoriais (tipo Economist) + fotos, 20 min", "investir", "referência do nicho #1 economia com dados; 3,1 mi views/mês em ~26 dias, mediana longos 605 mil"),
 "UCK9xNYXhp2zL4_SIkd1AIEA": ("en: 'Why did X get rich but Y never did?' mapa animado ilustrado + placar, 12 min", "investir", "nicho #1; 1,8 mi no 1º hit (US × América Latina); mapa 100% motion, sem footage"),
 "UCEPS4Oc-5EqlOp8IlfUhUZQ": ("en: geografia econômica/migração 'Why do X…?' mapas + stock, 10 min", "testar", "nicho #1; 1,2 mi no hit; tema politicamente sensível"),
 "UCdYuVMwhxFLc-87sulUbIBg": ("en: 'Why <país> is sitting on…' stock footage + mapa satélite + gráficos, 15 min", "testar", "nicho #1/geo; mediana L90 169 mil; formato editorial exato (stock + motion)"),
 "UCZ4AMrDcNrfy3X6nsU8-rPg": ("en: 'Why everyone is leaving <país>' economia explicada, stock + gráficos", "testar", "teto do nicho #1 (dono antigo, 4,3 mi/mês)"),
 "UCsGmo5M9LX8GJ-6CsT8xDpw": ("es: '¿Qué hay debajo de <estrutura>? (y por qué no se cae)' foto de arquivo creditada + esquema 3D + trecho de documento técnico, 13 min", "investir", "MODELO do nicho #2 engenharia; 12 vídeos, mediana 113 mil, 1,6 mi/mês; o formato editorial mais próximo do que faríamos"),
 "UCMOqf8ab-42UUQIdVoKwjlQ": ("en: engenharia civil explicada com maquete/apresentador, 19 min", "testar", "teto do nicho #2 (mediana 1,7 mi)"),
 "UCILe99sw_kJ4NvcFrnrlq9w": ("es: megaestruturas (túnel, ponte) documental, 23 min", "descartar", "nicho #2; 2,6 mi/mês mas parou (0 longos em 90 d); fonte de imagem incerta"),
 "UCG76lqEyDxxARvenKCoOAvQ": ("es: 'Cómo <monumento> tiene X sin Y' imagens de IA fotorrealistas, 22 min", "descartar", "nicho #2; 2,7 mi/mês com IA; mostra demanda es, não o nosso formato"),
 "UC7t63g5TYdhbE8t1Ti-Wa6g": ("en: 'How a <máquina militar> actually worked' filmes de treinamento da Marinha + diagramas de manual (domínio público), 25 min", "investir", "MODELO do nicho #3; canal de 1 mês, 175 mil no hit, mediana 28 mil; prova do arquivo público em escala"),
 "UCI0YUL57yQ03GmfBYmIw5Ng": ("en: 'How <país> quietly built <navio>' IA fotorrealista + cartões motion, 21 min", "testar", "nicho #3; 1,1 mi no hit em 1 mês; usa IA, não arquivo"),
 "UCO4gtSa3rpOutrZ45-OjYyA": ("en: 'Every US <classe> ever built' catálogo, 25 min", "descartar", "nicho #3; mediana L90 1,9 mil: catálogo cansa"),
 "UCBMpOoAvVl9T2V6ZavXl9vw": ("en: filmagem de arquivo restaurada/colorizada 4K com legendas, 14 min", "testar", "nicho #3/séc. XX; 1,2 mi no hit; arquivo PD, pouca narração (risco reutilizado)"),
 "UC1ZBQ-F-yktYD4m5AzM6pww": ("en: aviação/naval em 3D próprio de alto nível, 42 min", "testar", "teto do nicho #3 (mediana 6,4 mi), 1 vídeo/trimestre"),
 "UCQVKHQydcoIVN6Xfx3-72MQ": ("es: espaço 'James Webb acaba de ver…' imagens NASA/ESA + CGI, 16 min", "testar", "4º colocado (espaço es); 105 mil inscritos desde fev/2026, mediana L90 288 mil"),
 "UC5q902RpdLkzhzmm8kGvQXg": ("es: espaço/escala '¿Cuánto se tarda en…?' 13 min", "testar", "espaço es; mediana L90 312 mil"),
 "UCdZhRs4wM7SgVXoP9WSW2yA": ("en: 'What really happened inside <voo>' reconstrução 3D branca minimalista + gráficos de dados", "descartar", "acidentes: corrida do ouro do Learjet (6+ canais criados em out/2026); efêmero e com tema de morte"),
 "UCfDPwaVu8uF1_C4_uy6ntVw": ("en: reconstrução 3D de acidente aéreo", "descartar", "acidentes: clone da onda Learjet out/2026"),
 "UCoZ6gJoTzo1ptnhrbFtWTSw": ("es: 'Accidente aéreo … segundo a segundo' 3D", "descartar", "acidentes es: mediana 7 mil fora do hit"),
 "UCXIkr0SRTnZO4_QpZozvCCA": ("en: animações oficiais de acidentes industriais (governo dos EUA, domínio público)", "testar", "fonte de MATERIAL (CSB, PD), não concorrente; mediana 589 mil"),
 "UCTngalO3jl5I3Op885eurfw": ("en: oceano profundo com imagens de IA", "descartar", "oceano: 1 hit de 949 mil, mediana 1,3 mil; IA"),
 "UCe9imMhDp6Kn3dn75mzUUZw": ("en: documentário de natureza longo (76 min) com footage de origem não declarada", "descartar", "natureza: material livre insuficiente; risco reutilizado"),
 "UCLNUQhd4SfWog0b4TAqtjkw": ("pt: 'Por que NINGUÉM mora em <lugar>?' mapa, 13 min", "testar", "cidades/geo pt; 5,1 mi/mês em 18 dias; subnicho que o Em Relevo pode absorver"),
}
con = conectar(); cur = con.cursor(); n = 0
for cid, (f, d, notas) in D.items():
    c = C.get(cid, {})
    cur.execute("""INSERT INTO youtube.garimpo_canais (channel_id, titulo, url, pais, criado, primeiro_video, formula, decisao, notas)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                   ON CONFLICT (channel_id) DO UPDATE SET formula=EXCLUDED.formula, decisao=EXCLUDED.decisao,
                     notas=coalesce(youtube.garimpo_canais.notas||' | ','')||EXCLUDED.notas, ultima_vez=now(),
                     primeiro_video=coalesce(youtube.garimpo_canais.primeiro_video, EXCLUDED.primeiro_video)""",
                (cid, c.get("nome"), f"https://www.youtube.com/channel/{cid}", c.get("pais"), c.get("criado"), c.get("primeiro_video"), f, d, N + notas))
    n += 1
con.commit(); print(n, "canais gravados")
