# PUBLICAR.md do longo 02 (pacote do YouTube) a partir de work/capitulos.txt (gera_srt.py) e dl/fotos/fotos.json. Uso: gera_publicar.py
import json
from pathlib import Path
R = Path(__file__).parent.parent
caps = open(R / "work/capitulos.txt").read().strip()
tp = json.load(open(R / "shared/tempos.json")); voz = tp.get("voz", "eleven")
F = {f["arquivo"]: f for f in json.load(open(R / "dl/fotos/fotos.json"))}
c = json.load(open(R / "shared/cues.json"))
usadas = [m["src"].split("/")[-1] for m in c["midia"] if m["src"].startswith("fotos/")] + [it["src"].split("/")[-1] for it in c["cortica"]["itens"] if it["tipo"] == "fotoimg"]
fotos = []
for a in dict.fromkeys(usadas):
    f = F[a]; extra = " (foto recortada)" if "mucum" in a else ""
    fotos.append(f"• {f['legenda_tela'].title()}: {f['autor']} – {f['licenca']}{extra} – {f['pagina_origem']}")
aviso = "" if voz == "eleven" else "\n> ⚠️ **Versão com voz PROVISÓRIA (Kokoro)**: a chave da ElevenLabs deu 401 em 09/11 (ver `BLOQUEIO.md`). Não publicar esta versão; rodar `shared/refaz_voz_eleven.sh` + render. Os capítulos abaixo mudam com a voz final.\n"
md = f"""# PUBLICAR: Em Relevo, vídeo 2 (o Rodrigo publica; nada foi enviado ao YouTube)
{aviso}
**Arquivo:** `out/video.mp4` (1920×1080, 30 fps, AAC −14 LUFS). **Legendas:** `out/legendas.srt` (pt-BR). **Thumbs:** `out/thumb-1.jpg` (É SUPER?), `out/thumb-2.jpg` (CHUVA × FOGO), `out/thumb-3.jpg` (ATÉ QUANDO?) para o "Testar e comparar".
**Publicar:** sexta, **13/11/2026**, depois de atualizar os blocos do boletim da NOAA de 12/11 (`ATUALIZAR-12-11.md`).

## Título
**Super El Niño: o que ele vai fazer com o Brasil neste verão?**
Alternativas:
- O Super El Niño é real? O que os dados de novembro dizem
- El Niño 2026: o que muda na sua região até março
- Fumaça no Norte, enchente no Sul: o El Niño de 2026 no mapa

## Descrição
```
Fumaça fechando escolas em Manaus, mais de meio metro de chuva em um mês no oeste de Santa Catarina e o mar 5,6 °C acima do normal na costa do Peru. É tudo a mesma história: o El Niño de 2026. No mapa 3D, respondemos 4 perguntas: o que é o El Niño, se ele é mesmo "super" (e se vai bater o recorde), o que muda na sua região neste verão e até quando ele dura.

Alertas da Defesa Civil: mande seu CEP por SMS para 40199 (grátis). Emergência: 199 (Defesa Civil) e 193 (Bombeiros).
Vídeo anterior: 7 tornados em 6 dias no Sul do Brasil.

CAPÍTULOS
{caps}

FONTES
• NOAA/CPC: discussão do ENSO de 08/10/2026 (boletim de 12/11/2026 na atualização), índices ONI e RONI, tabela de força do RONI, índices semanais (Niño 1+2 e 3.4)
• NOAA OISST v2.1 (NCEI/PSL): anomalia diária da temperatura do mar (relevo de calor e globo, desenhados pelo Em Relevo)
• IRI/Universidade Columbia (previsões, 19/10/2026) · Bureau of Meteorology da Austrália (27/10/2026) · OMM (03/09/2026) · NOAA PMEL e NOAA Climate.gov (como funciona o El Niño; paleoclima em corais)
• INMET: anomalia recorde para outubro (03/11/2026); destaques de outubro, 581,6 mm em Dionísio Cerqueira (09/11/2026)
• Painel El Niño 2026-2027, Boletim nº 05 (out/2026): INMET, INPE, ANA, Cemaden, SGB, SEDEC e Censipam · MCTI, 06/11/2026
• Prefeitura/Defesa Civil de Manaus (qualidade do ar, 09/10/2026) · Inpe (focos de calor) · ANA (telemetria do rio Negro em Manaus) · Serviço Geológico do Brasil (rio Branco, 04/09/2026)
• Monitor de Secas (ANA), agosto e setembro de 2026
• Defesa Civil do RS e de SC (balanços de 05 e 06/11/2026) · Simepar · Climatempo (levantamento dos 7 tornados)
• Defesa Civil do Paraná (enchente de União da Vitória, 1983) · Defesa Civil de Blumenau (cheia de 09/07/1983)
• World Weather Attribution (enchente do RS, 2024) · Copernicus C3S (outubro de 2026) · Carbon Brief (06/11/2026)
• Ministério da Integração (SMS 40199) · Ministério da Saúde (fumaça e ondas de calor)

IMAGENS (crédito também na tela)
Satélite: NASA GIBS – MODIS Terra (Manaus, 09/10/2026; Sul, 04/11/2026) e NASA JPL MUR (Pacífico, 08/11/2026), domínio público. Rio Branco em Boa Vista: NASA HLS – contém dados Copernicus Sentinel modificados [2025, 2026].
{chr(10).join(fotos)}
Mapa: IBGE e Natural Earth.

MÚSICA
"Echoes of Time", "Ossuary 6 - Air" e "Frozen Star" – Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 4.0 License
http://creativecommons.org/licenses/by/4.0/

Efeitos sonoros: "WWS Typewriter" – Work With Sounds / Konrad Gutkowski (CC BY 4.0, Wikimedia Commons); demais efeitos de domínio público/CC0 ou próprios.

#elnino #superelnino #clima
```

## Tags
El Niño, Super El Niño, El Niño 2026, El Niño 2026 Brasil, El Niño verão, El Niño quando acaba, até quando vai o El Niño, El Niño Sul, El Niño Nordeste seca, El Niño Amazônia, fumaça Manaus, La Niña 2027, NOAA, Inmet, previsão do tempo verão, clima

## Ao publicar
- **Categoria:** Educação. Idioma: português (Brasil). Envie `out/legendas.srt` como legenda pt-BR.
- Playlist "O verão do El Niño" junto com o vídeo 1; card para o vídeo 1 no trecho "a gente fez um vídeo inteiro só sobre isso" (capítulo Sul) e tela final com o vídeo 1. No vídeo 1, card para este no capítulo do El Niño (6:21).
- "Conteúdo alterado ou sintético": **não** (mapa e gráficos são animação de dados; fotos reais sem alteração além de corte; a voz é sintética, mas narra um texto nosso — Hipótese; se preferir, marque "sim").
- Não é para crianças.
- Comentário fixado (sugestão): data do boletim usado + "atualizamos aqui quando a NOAA publicar o próximo".
"""
open(R / "PUBLICAR.md", "w").write(md)
print("ok PUBLICAR.md", len(fotos), "fotos creditadas")
