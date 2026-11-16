# Gera entrega/pacote/youtube.txt (padrão de conhecimento/politicas-youtube.md item 5: TÍTULOS A/B/C → DESCRIÇÃO → CAPÍTULOS → FONTES/CRÉDITOS → TAGS → CATEGORIA → CHECKLIST)
# e FONTES-E-LICENCAS.md do longo 05 (enchente de maio/2024 em Porto Alegre). Créditos só na descrição (nada na tela além de lugar e data).
import json
from pathlib import Path
A = Path(__file__).parent; R = A.parent
c = json.load(open(A / "cues.json")); fotos = {Path(f["arquivo"]).stem: f for f in json.load(open(R / "pesquisa/fotos.json"))}
caps = (R / "work/capitulos.txt").read_text().strip()
ts = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
usadas = {}
for m in c["midia"]:
    k = Path(m["src"]).stem.replace("-recorte", ""); usadas.setdefault(k, []).append((m["t0"], m["legenda"]))
cred, lic = [], []
for k, tt in sorted(usadas.items(), key=lambda x: x[1][0][0]):
    f = fotos[k]; cred.append(f"- {f['credito']} · {tt[0][1]}")
    lic.append(f"| {ts(tt[0][0])} | `{k}.jpg` | {tt[0][1]} | {f['autor']} | {f['licenca']} | {f['pagina']} |")
titulos = [("A", "Por que a chuva da SERRA alagou PORTO ALEGRE?", "thumb-A.jpg · 1/3 DO ESTADO? (câmera alta)"),
           ("B", "O LAGO que engoliu PORTO ALEGRE em 2024", "thumb-B.jpg · 1/3 DO ESTADO? (câmera baixa, ponto do Guaíba maior)"),
           ("C", "Por que a água da SERRA foi parar em PORTO ALEGRE?", "thumb-C.jpg · UM TERÇO?")]
cta = "Se você quer entender o clima do Brasil no mapa, inscreva-se no Em Relevo e compartilhe este vídeo com quem tem família no Rio Grande do Sul. Para entender por que o Sul tem um clima tão diferente do resto do país, veja também: https://youtu.be/bG6-E4qjXYc"
desc = f"""{cta}

Em maio de 2024, a chuva mais pesada caiu na serra gaúcha. Quem ficou debaixo d'água foi Porto Alegre, a cerca de 100 quilômetros dali. Neste vídeo, no mapa em relevo, a gente segue o caminho da água: dos rios que nascem na serra e no planalto até o Guaíba, a saída lenta pela Lagoa dos Patos e a defesa da cidade que cedeu.

CAPÍTULOS
{caps}

FONTES
INMET (chuva em Caxias do Sul, Santa Maria e Porto Alegre) · World Weather Attribution (estudo rápido de 03/06/2024) · SGB/ANA (cota do Taquari em Lajeado e revisão da série de 1941) · Sema/ANA (pico do Guaíba, 5 de maio) · Prefeitura de Porto Alegre e DMAE (sistema de proteção contra cheias, casas de bombas, pessoas atingidas) · IPH/UFRGS (bacia do Guaíba, vento e Lagoa dos Patos, artigo na RBRH) · Governo do Rio Grande do Sul (bacia do Guaíba, cota de inundação, balanço da Defesa Civil) · Defesa Civil do RS (alerta por SMS: CEP para 40199). Esquemas (orla, corte do sistema, perfil do relevo, vazão) são ilustrativos e dizem isso na tela; trajetos de água no mapa são aproximados.

CRÉDITOS DAS IMAGENS (cortadas e redimensionadas, sem outra alteração)
""" + "\n".join(cred) + """
- Imagens de satélite: NASA Earth Observatory / Landsat 8 e MODIS (domínio público); "Contains modified Copernicus Sentinel data 2024" (HLS/Sentinel-2).
- Mapa: relevo SRTM / AWS Terrain Tiles, cor NASA Blue Marble, limites IBGE, rios © colaboradores do OpenStreetMap (ODbL, https://www.openstreetmap.org/copyright).

MÚSICA E EFEITOS
Kevin MacLeod (incompetech.com): "Echoes of Time", "Ossuary 6 - Air" e "Frozen Star", licença Creative Commons BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Efeito de máquina de escrever: Work With Sounds / Konrad Gutkowski, Wikimedia Commons, CC BY 4.0. Batida de madeira: stephan, Wikimedia Commons, domínio público.
"""
tags = "enchente Porto Alegre, enchente 2024, enchente Rio Grande do Sul, Guaíba, Lagoa dos Patos, Vale do Taquari, bacia do Guaíba, rios do Rio Grande do Sul, muro da Mauá, casas de bombas, cheia de 1941, chuva na serra gaúcha, clima do Brasil, geografia do Brasil, Em Relevo"
check = """CHECKLIST DE PUBLICAÇÃO (para o Rodrigo; fora da descrição)
- Studio → Atributos → "Uso de IA" = Sim (voz sintética); não é para crianças; idioma português (Brasil); legendas: legendas.srt.
- "Testar e comparar": 3 thumbs (A/B/C) + 3 títulos pareados; mp4 1080p.
- Upload manual (publicação prevista: qua 18/11/2026). Sem card de próximo vídeo (regra de 13/11); o vídeo do clima do Sul (bG6-E4qjXYc) já está publicado e vai na descrição.
- Decisão de risco do Rodrigo: a série de fotos aéreas da Prefeitura de Porto Alegre (PMPA, Wikimedia Commons) tem licença "Attribution only" (NÃO é Creative Commons): exige crédito, que está acima; se preferir zero risco, troque por fotos Stuckert (CC BY-SA 2.0) e satélite.
- Fotos de outros anos levam o ano real na legenda (muro 2016, barra de Rio Grande 2023, Cais Mauá 2026, Mercado Público 1941).
"""
txt = "TÍTULOS (3, pareados às thumbs para o 'Testar e comparar')\n" + "\n".join(f"{k}. {t}   ←  {th}" for k, t, th in titulos) + f"\n\nTÍTULO PRINCIPAL (A): {titulos[0][1]}\n\nDESCRIÇÃO\n{desc}\nTAGS\n{tags}\n\nCATEGORIA: Educação (27)\nIdioma do vídeo: português (Brasil)\n\n{check}"
(R / "entrega/pacote").mkdir(parents=True, exist_ok=True); (R / "entrega/pacote/youtube.txt").write_text(txt)
(R / "FONTES-E-LICENCAS.md").write_text("# Fontes e licenças: Em Relevo 005 (enchente de maio/2024 em Porto Alegre)\n\nFotos usadas no vídeo (créditos só na descrição; na tela, lugar e data).\n\n| Entra em | Arquivo | Legenda na tela | Autor | Licença | Página de origem |\n|---|---|---|---|---|---|\n" + "\n".join(lic) +
 "\n\nCortes feitos pela produção: `hls-sentinel2-...-recorte.jpg` (tira a faixa sem dados do satélite) e `mercado-publico-...-1941-05-recorte.jpg` (tira a marca d'água do site no topo).\n"
 "Mapa: SRTM/AWS Terrain Tiles (relevo), NASA Blue Marble (cor), IBGE (limites), OpenStreetMap (rios, ODbL; `dados/rios-osm.json` → `shared/rios.json`, script `shared/prepara_rios.py`).\n"
 "Música: Kevin MacLeod (CC BY 4.0): Echoes of Time, Ossuary 6 - Air, Frozen Star. SFX: máquina de escrever WWS (CC BY 4.0), toque na madeira (domínio público); o resto sintetizado (`shared/sintetiza_sfx.py`).\n"
 "Dados: `pesquisa/FATOS.md` (INMET, SGB/ANA, DMAE, IPH/UFRGS, WWA, Defesa Civil RS, prefeitura).\n"
 "Pendência (decisão do Rodrigo): a série PMPA tem licença \"Attribution only\" (não CC) no Commons.\n")
print("ok", len(usadas), "imagens creditadas")
