# Gera entrega/pacote/youtube.txt (3 títulos pareados às thumbs A/B/C, descrição, capítulos, créditos de fotos/música/SFX, fontes)
# e FONTES-E-LICENCAS.md do longo 04 (1983). Créditos só na descrição (regra do lote); nada na tela.
import json
from pathlib import Path
A = Path(__file__).parent; R = A.parent
c = json.load(open(A / "cues.json")); fotos = {f["arquivo"].split("/")[-1].rsplit(".", 1)[0]: f for f in json.load(open(R / "pesquisa/fotos.json"))}
caps = (R / "work/capitulos.txt").read_text().strip()
ts = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
usadas = {}
for m in c["midia"]:
    k = m["src"].split("/")[-1]; usadas.setdefault(k, []).append((m["t0"], m["legenda"]))
for k in ("landsat4-uv-19830804-par.jpg",):
    usadas.setdefault(k, []).append((next(g["t0"] for g in c["graficos4"] if g["tipo"] == "cortina"), "UNIÃO DA VITÓRIA · LANDSAT 4 · 4 AGO 1983"))
cred, lic = [], []
for k, tt in sorted(usadas.items(), key=lambda x: x[1][0][0]):
    if k.startswith("landsat4-uv"):
        autor, licenca, cr, pg = "NASA / USGS (Landsat 4 MSS), processado pela produção", "Domínio público (USGS)", "NASA/USGS Landsat 4 MSS, domínio público, processado pela produção", "https://earthexplorer.usgs.gov/ (cenas LM04_L1TP_221078_19830703 e _19830804)"
    else:
        f = fotos[k.rsplit(".", 1)[0]]; autor, licenca, cr, pg = f["autor"], f["lic"], f["credito"], f["page"]
    cred.append(f"- {cr} · {tt[0][1]}")
    lic.append(f"| {ts(tt[0][0])} | `{k}` | {tt[0][1]} | {autor} | {licenca} | {pg} |")
(R / "FONTES-E-LICENCAS.md").write_text("# Fontes e licenças: Em Relevo 004 (1983, o El Niño que partiu o Brasil ao meio)\n\nFotos/imagens usadas no vídeo (créditos só na descrição; nada na tela além de lugar e ano).\n\n| Entra em | Arquivo | Legenda na tela | Autor | Licença | Página de origem |\n|---|---|---|---|---|---|\n" + "\n".join(lic) +
 "\n\nNão existe foto livre da enchente nem da seca de 1983: o ano é contado com dado, mapa e satélite. Foto de outro ano sempre leva o ano real na legenda. CC BY / CC BY-SA só com corte e redimensionamento.\nPendência: conferir a licença do slide 'Retirantes' (Centro de Memória/Unicamp) na página antes de publicar (FOTOS.md); se houver dúvida, tirar o slide (b20).\n\nMúsica: Kevin MacLeod (incompetech.com), CC BY 4.0: \"Echoes of Time\", \"Ossuary 6 - Air\", \"Frozen Star\".\nSFX: ver `../longo-02/FONTES-E-LICENCAS.md`.\nDados: ver `pesquisa/DADOS.md` e `pesquisa/FATOS.md` (ANA HidroWeb, NOAA/CPC, NOAA ERSSTv5, INMET).\n")
titulos = [("A", "Por que o Brasil teve seca e enchente no mesmo ano?", "thumb-A.jpg · MESMO ANO"), ("B", "O El Niño de 1983 que partiu o Brasil ao meio", "thumb-B.jpg · 1983 (satélite de ago/1983)"), ("C", "E se o El Niño de 1983 voltar em 2026?", "thumb-C.jpg · 1983 → 2026?")]
desc = f"""Julho de 1983: o rio Iguaçu chega a 10,42 metros em União da Vitória (PR) e cobre a cidade. Em Blumenau (SC), o Itajaí-Açu passa dos 15 metros pela terceira vez no ano. A 2.500 quilômetros dali, o sertão do Ceará vive o quinto ano de uma seca que começou em 1979: em agosto, 5 mil flagelados invadem um armazém de comida em Canindé. Foi o mesmo El Niño puxando o Brasil para os dois lados. Neste vídeo, no mapa 3D com relevo real, a gente responde 4 perguntas: o que aconteceu no Sul, o que aconteceu no sertão, por que os dois ao mesmo tempo (o El Niño de 1982-83, o mais forte desde 1950 no índice RONI da NOAA) e o que 1983 diz sobre 2026 (boletim da NOAA de 12/11/2026: cerca de 60% de chance de um El Niño histórico, sem prever enchente nem seca).

CAPÍTULOS
{caps}

Observações: números de Santa Catarina (78 municípios em calamidade, 49 mortos, quase 200 mil desabrigados) são do levantamento da geógrafa Maria Lúcia Herrmann (UFSC); o de Canindé e os 10 milhões de flagelados vêm do Memorial da Democracia; não existe número oficial confiável de mortos pela seca de 1983, por isso o vídeo não cita nenhum. Fotos de outros anos levam o ano na legenda; não há foto livre da enchente nem da seca de 1983. As imagens de satélite de 3 de julho e 4 de agosto de 1983 são do Landsat 4 (USGS), com o mesmo tratamento de cor nas duas datas. A linha do tempo do rio usa a cota diária da ANA (estação 65310000). Trajetos e posição dos rios no mapa são aproximados.

Veja também o vídeo anterior do canal sobre o El Niño de 2026: https://youtu.be/FeSLzHvlkbo

FONTES
ANA HidroWeb (cota diária do Iguaçu em União da Vitória, estação 65310000; chuva de Mombaça, estação 00539001, DNOCS) · Defesa Civil do Paraná, "Enchente de União da Vitória de 1983" · Defesa Civil de Blumenau, "Enchentes registradas" · Herrmann (2001), via Revista Brasileira de Geografia Física · Memorial da Democracia, "País descobre a tragédia da seca" (12/08/1983) · SUDENE, via Revista de Economia Política (SciELO) · NOAA/CPC (índice RONI e boletim ENSO de 12/11/2026) · Kousky e Cavalcanti (1984, INPE) · Grimm et al. (UFPR) · INMET (outubro de 2026) · Funceme · ASA/P1MC (cisternas) · NOAA ERSSTv5 · NOAA ETOPO 2022 e NASA Blue Marble (relevo e satélite) · IBGE / Natural Earth (limites).

CRÉDITOS DAS IMAGENS (fotos cortadas/redimensionadas, sem outra alteração)
""" + "\n".join(cred) + """

MÚSICA
Kevin MacLeod (incompetech.com): "Echoes of Time", "Ossuary 6 - Air" e "Frozen Star", licença Creative Commons BY 4.0 (https://creativecommons.org/licenses/by/4.0/).

Narração sintética (ElevenLabs) sobre texto e pesquisa do canal.
"""
tags = "El Niño 1983, El Niño, El Niño 2026, enchente de 1983, União da Vitória, Blumenau, rio Iguaçu, Itajaí-Açu, seca de 1983, seca no Nordeste, sertão, Mombaça, Canindé, clima do Brasil, Landsat, NOAA, história do clima, Em Relevo"
txt = "TÍTULOS (3, pareados às thumbs para o 'Testar e comparar')\n" + "\n".join(f"{k}. {t}   ←  {th}" for k, t, th in titulos) + f"\n\nTÍTULO PRINCIPAL (A): {titulos[0][1]}\n\nDESCRIÇÃO\n{desc}\nTAGS\n{tags}\n\nCATEGORIA: Educação (27)\nIdioma do vídeo: português (Brasil) · legendas: legendas.srt\nConteúdo alterado ou sintético: SIM para a voz (narração sintética); mapas e gráficos são animação de dados; fotos reais com corte/redimensionamento.\nNão é para crianças.\nLembretes ao publicar: marcar 'Testar e comparar' com as 3 thumbs; sem card de próximo vídeo (regra do Rodrigo 13/11); cartão/descrição puxando o vídeo do El Niño 2026 (FeSLzHvlkbo, já publicado); conferir a licença do slide 'Retirantes' (Unicamp) na página.\n"
(R / "entrega/pacote").mkdir(parents=True, exist_ok=True); (R / "entrega/pacote/youtube.txt").write_text(txt)
print("ok", len(usadas), "imagens creditadas")
