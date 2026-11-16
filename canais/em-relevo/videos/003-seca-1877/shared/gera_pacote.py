# Gera entrega/pacote/youtube.txt (3 títulos pareados às thumbs A/B/C, descrição, capítulos, créditos de fotos/música/SFX, fontes)
# e FONTES-E-LICENCAS.md. Créditos só na descrição (regra do lote); nada na tela.
import json
from pathlib import Path
A = Path(__file__).parent; R = A.parent
c = json.load(open(A / "cues.json")); fotos = {f["arquivo"].replace("ê", "e").replace("ç", "c"): f for f in json.load(open(R / "dl/fotos/fotos.json"))}
caps = (R / "work/capitulos.txt").read_text().strip()
ts = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
usadas = {}
for m in c["midia"]:
    k = m["src"].split("/")[-1]; usadas.setdefault(k, []).append(m["t0"])
cred, lic = [], []
for k, tt in sorted(usadas.items(), key=lambda x: x[1][0]):
    f = fotos[k]; cred.append(f"- {f['credito_tela'].replace('IMAGEM: ', '').replace('FOTO: ', '')} · {f['legenda_tela']}")
    lic.append(f"| {ts(tt[0])} | `{k}` | {f['legenda_tela']} | {f['autor']} | {f['licenca']} | {f['pagina_origem']} |")
(R / "FONTES-E-LICENCAS.md").write_text("# Fontes e licenças: Em Relevo 003 (A Grande Seca de 1877)\n\nFotos usadas no vídeo (créditos só na descrição; nada na tela).\n\n| Entra em | Arquivo | Legenda na tela | Autor | Licença | Página de origem |\n|---|---|---|---|---|---|\n" + "\n".join(lic) +
 "\n\nRegras: CC BY-SA/CC BY só com corte e redimensionamento; as cartes-de-visite de J. A. Corrêa são baixa resolução (221–400 px) e entram pequenas, sem ampliar.\n\nMúsica: Kevin MacLeod (incompetech.com), CC BY 4.0: \"Echoes of Time\", \"Ossuary 6 - Air\", \"Frozen Star\".\nSFX: ver `../longo-02/FONTES-E-LICENCAS.md` (Work With Sounds / Konrad Gutkowski, CC BY 4.0, e demais livres).\nDados: ver `pesquisa/DADOS.md` (NOAA ERSSTv5, GHCN v2, IBGE, OpenStreetMap ODbL, Monitor de Secas/ANA).\n")
titulos = [("A", "Por que quase ninguém fala da seca que matou 500 mil brasileiros?", "thumb-A.jpg · 500 MIL"), ("B", "A seca que mudou o mapa do Brasil", "thumb-B.jpg · MUDOU O MAPA"), ("C", "O El Niño de 1877 vai se repetir em 2026?", "thumb-C.jpg · 1877 = 2026?")]
desc = f"""Fortaleza, 1878: uma cidade de uns 25 mil habitantes recebe mais de 100 mil retirantes que chegam a pé do sertão. Em 10 de dezembro, a varíola mata 1.004 pessoas em um único dia. É a Grande Seca de 1877: as estimativas de mortos chegam a 500 mil (faixa de 150 mil a 500 mil), pelas contas mais altas 5% da população do Império. Neste vídeo, no mapa 3D com relevo real, respondemos 4 perguntas: o que aconteceu, por que não choveu (El Niño no Pacífico e Atlântico Norte mais quente), o que a seca mudou no mapa do Brasil (ferrovias, o primeiro grande açude, a migração para o Acre) e se pode se repetir com o El Niño de 2026.

CAPÍTULOS
{caps}

Observações: a frase "venderei até a última joia da Coroa" atribuída a Dom Pedro II não tem documento que a comprove. O número de mortos é estimativa (ninguém contou direito). Os dados de temperatura do mar anteriores a 1900 são reconstrução estatística (NOAA ERSSTv5, grade de 2°): mostram o padrão de grande escala, não o detalhe local. As rotas de retirantes no mapa são ilustrativas (direção e destino reais; a quantidade não é dado).

FONTES
Agência Senado (Ricardo Westin, 01/10/2021) · Rodolpho Theophilo, "História da Secca do Ceará" · Singh et al. (2018), Journal of Climate · Barboza (2015), Revista Brasileira de História · O Povo · Diário do Nordeste · Instituto do Ceará · FAPESP "Memórias da seca" · Funceme · INMET (Painel El Niño, out/2026) · ANA, Monitor de Secas (set/2026) · ASA/P1MC (cisternas) · NOAA ERSSTv5 e NOAA/CPC · GHCN v2 (chuva de Fortaleza, 1849–2018) · IBGE/SUDENE (semiárido) · OpenStreetMap (rios e trilhos, ODbL) · NOAA ETOPO 2022 e NASA Blue Marble (relevo e satélite).

CRÉDITOS DAS IMAGENS (fotos cortadas/redimensionadas, sem outra alteração)
""" + "\n".join(cred) + """

MÚSICA
Kevin MacLeod (incompetech.com): "Echoes of Time", "Ossuary 6 - Air" e "Frozen Star", licença Creative Commons BY 4.0 (https://creativecommons.org/licenses/by/4.0/).
Efeito de máquina de escrever: "WWS Typewriter", Work With Sounds / Konrad Gutkowski, Wikimedia Commons, CC BY 4.0.

Narração sintética (ElevenLabs) sobre texto e pesquisa do canal.
"""
tags = "grande seca de 1877, seca de 1877, grande seca, Ceará, Fortaleza 1878, retirantes, Dia dos Mil Mortos, varíola, El Niño, El Niño 2026, El Niño 1877, seca no Nordeste, história do Brasil, história do Nordeste, semiárido, Açude do Cedro, Estrada de Ferro de Baturité, Acre, Dom Pedro II, Theophilo, Em Relevo"
txt = "TÍTULOS (3, pareados às thumbs para o 'Testar e comparar')\n" + "\n".join(f"{k}. {t}   ←  {th}" for k, t, th in titulos) + f"\n\nTÍTULO PRINCIPAL (A): {titulos[0][1]}\n\nDESCRIÇÃO\n{desc}\nTAGS\n{tags}\n\nCATEGORIA: Educação (27)\nIdioma do vídeo: português (Brasil) · legendas: legendas.srt\nConteúdo alterado ou sintético: SIM para a voz (narração sintética); mapas e gráficos são animação de dados; fotos reais com corte/redimensionamento.\nNão é para crianças.\nComentário fixado (sugestão): o mapa ilustra as rotas dos retirantes; os números de mortos são estimativas (faixa 150–500 mil).\nLembretes ao publicar: marcar 'Testar e comparar' com as 3 thumbs; sem card de próximo vídeo (regra do Rodrigo 13/11); puxar o vídeo sobre o El Niño 2026 como card/descrição (já publicado).\n"
(R / "entrega/pacote").mkdir(parents=True, exist_ok=True); (R / "entrega/pacote/youtube.txt").write_text(txt)
print("ok", len(usadas), "fotos creditadas")
