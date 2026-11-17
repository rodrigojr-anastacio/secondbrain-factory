# Em Relevo 006: legendas.srt + capítulos + entrega/pacote/youtube.txt (títulos A/B/C pareados às thumbs, descrição, fontes, créditos, tags) + FONTES-E-LICENCAS.md
# + embalagem/variantes.json. Padrão de conhecimento/politicas-youtube.md. Uso: python3 shared/gera_pacote6.py <duracao_do_video_em_s>
import json, sys, subprocess
from pathlib import Path
A = Path(__file__).parent; R = A.parent
dur = float(sys.argv[1]) if len(sys.argv) > 1 else json.load(open(A / "cues.json"))["duracao"]
c = json.load(open(A / "cues.json")); tp = json.load(open(A / "tempos.json"))["blocos"]
ts = lambda t: f"{int(t // 60)}:{int(t % 60):02d}"
# --- SRT (cartões da legenda)
cartoes, cur = [], []
for p in c["palavras"]:
    if p == "|":
        if cur: cartoes.append(cur); cur = []
    else: cur.append(p)
if cur: cartoes.append(cur)
fins = [f["e"] for b in tp for f in b["frases"]]
def fim_frase(t): return min((e for e in fins if e >= t - 0.05), default=t + 2)
def sr(t): h, r = divmod(t, 3600); m, s = divmod(r, 60); return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)) % 1000:03d}"
out = []; fim_ant = 0
for i, cd in enumerate(cartoes):
    t0 = cd[0][1]; prox = cartoes[i + 1][0][1] if i + 1 < len(cartoes) else t0 + 3
    t1 = min(prox - 0.02, fim_frase(cd[-1][1]) + 0.25); a = max(fim_ant + 0.01, t0 - 0.05); b = max(t1, a + 0.6); fim_ant = b
    out.append(f"{i+1}\n{sr(a)} --> {sr(b)}\n{' '.join(w for w, _ in cd)}\n")
(R / "entrega/pacote").mkdir(parents=True, exist_ok=True); (R / "out").mkdir(exist_ok=True)
open(R / "out/legendas.srt", "w").write("\n".join(out))
# --- capítulos
mapa = [("BERTIOGA", "Hook: 683 mm num dia"), ("O MAPA", "O mapa: a pergunta"), ("1 · A PAREDE", "1 · A parede"), ("2 · A CHUVA", "2 · A chuva que a serra fabrica"),
        ("3 · A CASCA", "3 · A casca da serra"), ("4 · 1967", "4 · 1967: o caminho até a cidade"), ("5 · 2023", "5 · 2023: a mesma receita"), ("A RESPOSTA", "A resposta")]
caps = []
for cp in c["capitulos"]:
    nome = next((v for k, v in mapa if cp["nome"].startswith(k)), None)
    if nome and nome not in [x[1] for x in caps]: caps.append((0.0 if not caps else cp["t"], nome))
caps_txt = "\n".join(f"{ts(t)} {n}" for t, n in caps)
# --- pacote
titulos = [("A", "Por que a SERRA DO MAR desaba sobre o LITORAL?", "Por que [LUGAR] [anomalia]? (controle)", "mapa-lugar", "bloco 3D do relevo (parede cortada de lado) + seta até a cidade + \"UMA PAREDE?\""),
           ("B", "CARAGUATATUBA 1967, SÃO SEBASTIÃO 2023: por que a serra repete?", "Contraste A × B + por que", "antes-depois", "Landsat 29/10/2022 × 26/02/2023, tela dividida + \"UMA NOITE\""),
           ("C", "A CASCA de terra que faz a SERRA DO MAR desabar", "O/A [coisa concreta] que [faz algo]", "cena-acao", "foto real do solo exposto mordendo o asfalto (Ubatuba, 19/02/2023), sem texto")]
bloco = "TESTAR E COMPARAR (3 pares título + thumb; \"Testar e comparar\" do Studio)\n" + "\n".join(f"{k}. {t}\n   padrão do título: {pt}\n   thumb-{k}.jpg · padrão da thumb: {pth} · {cn}" for k, t, pt, pth, cn in titulos)
cta = "Se você tem família no litoral norte de São Paulo, manda este vídeo para ela. E se inscreva no Em Relevo para entender o clima do Brasil no mapa. Para ver outro desastre brasileiro explicado no mapa: https://youtu.be/I5KpDKy6r3E"
desc = f"""{cta}

Na madrugada de 19 de fevereiro de 2023, choveu 683 mm em 24 horas em Bertioga e 627 mm em São Sebastião; em Caraguatatuba, a poucos quilômetros, foram 234 mm. Neste vídeo, no mapa em relevo, a gente mostra por que a Serra do Mar desce sobre o litoral: uma parede de quase 700 metros a menos de 6 km do mar, um temporal preso numa faixa estreita e uma casca de terra de 1 a 2,5 metros quase sem coesão. A mesma receita em Caraguatatuba (1967, carta de declividades da geógrafa Olga Cruz) e em São Sebastião (2023, Landsat antes e depois). Não é previsão: é o mapa de onde a serra cede.

CAPÍTULOS
{caps_txt}

FONTES
CEMADEN (acumulados de 18–19/02/2023) · INMET · NASA GPM IMERG (estimativa de chuva por satélite, quadrados de ~10 km) · IAG-USP (frente fria e ciclone) · Olga Cruz, "Contribuição ao estudo das massas de movimentos gravitacionais da Serra do Mar", Revista Brasileira de Geografia 37(2), 1975 (IBGE) · estudo da USP de 2017 (cicatrizes × granito) · SGB/CPRM (carta de suscetibilidade, Caraguatatuba) · IBGE (Censo 2022 e 2010) · NASA Earth Observatory (deslizamentos em São Paulo) · Defesa Civil (alertas por SMS: CEP para 40199). Detalhes: pesquisa/FATOS.md.

CRÉDITOS DAS IMAGENS (cortadas e redimensionadas, sem outra alteração)
- Imagens de satélite: NASA Earth Observatory (Allison Nussbaum), dados USGS Landsat 8 e 9, domínio público.
- Carta de declividades: Olga Cruz, Revista Brasileira de Geografia 37(2), 1975, IBGE (CC BY 4.0).
- Encosta na estrada em Ubatuba (19/02/2023): Defesa Civil de Ubatuba / Governo do Estado de São Paulo (CC BY 2.0).
- Vista aérea de São Sebastião (23/02/2023): Governo do Estado de São Paulo (CC BY 2.0).
- Serra do Mar vista da Rodovia dos Tamoios: Themium, Wikimedia Commons (CC0).
- Chuva: NASA GPM IMERG (GES DISC), domínio público.
- Mapa: relevo SRTM / AWS Terrain Tiles, máscara terra-mar NASA GIBS (OpenStreetMap, ODbL, https://www.openstreetmap.org/copyright). Cores, blocos e cicatrizes do mapa são ilustrativos.

MÚSICA E EFEITOS
Kevin MacLeod (incompetech.com): "Echoes of Time", "Ossuary 6 - Air" e "Frozen Star", licença Creative Commons BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Efeito de máquina de escrever: Work With Sounds / Konrad Gutkowski, Wikimedia Commons (CC BY 4.0); toque na madeira (domínio público); demais efeitos sintetizados.
"""
tags = "Serra do Mar, Caraguatatuba, São Sebastião, deslizamento, deslizamento de terra, Caraguatatuba 1967, São Sebastião 2023, litoral norte de São Paulo, chuva no litoral norte, Bertioga, Ubatuba, encostas, geografia do Brasil, relevo, clima do Brasil, Defesa Civil, alerta SMS 40199, Olga Cruz, Landsat"
check = """CHECKLIST DE PUBLICAÇÃO (para o Rodrigo; fora da descrição)
- Studio → Atributos → "Uso de IA" = Sim (voz sintética); não é para crianças; idioma português (Brasil); legendas: legendas.srt.
- "Testar e comparar": 3 thumbs (A/B/C) + 3 títulos pareados (bloco no topo); mp4 1080p.
- Upload manual; janela sugerida: qua 18/11 ou sex 20/11/2026 (decisão do Rodrigo). Sem card de próximo vídeo; o vídeo da seca de 1877 (I5KpDKy6r3E) já está publicado e vai na descrição.
- Voz: Fish #NATASHA (reserva), porque a chave da ElevenLabs voltou 401 na noite de 16→17/11; se preferir a Fernanda, regravar a voz (plano ElevenLabs) e remontar.
- Carta do SGB: NÃO reproduzida no vídeo (PDF de 34 MB não convertido); no b32 o vídeo mostra a declividade > 40% do SRTM com legenda honesta. O texto do b32 foi trocado para a versão segura do brief.
- Esquemas (fratura, cicatrizes, casca, faixa de chuva) levam o selo ILUSTRATIVO na tela. Cores/relevo do mapa são sintéticos a partir do SRTM (não são foto de satélite).
- Descrição e tags sem "morte/morreu/vítimas fatais"; a narração diz "sessenta e cinco pessoas morreram" (b37): decisão editorial já aprovada na etapa 1.
"""
txt = bloco + f"\n\nTÍTULO PRINCIPAL (A): {titulos[0][1]}\n\nDESCRIÇÃO\n{desc}\nTAGS\n{tags}\n\nCATEGORIA: Educação (27)\nIdioma: português (Brasil)\nDuração: {ts(dur)}\n\n{check}"
(R / "entrega/pacote/youtube.txt").write_text(txt)
vs = [{"letra": k, "titulo": t, "padrao_titulo": pt, "padrao_thumb": pth, "thumb_conceito": cn, "thumb_texto": {"A": "UMA PAREDE?", "B": "UMA NOITE", "C": ""}[k], "thumb_arquivo": f"entrega/thumb-{k}.jpg"} for k, t, pt, pth, cn in titulos]
json.dump(vs, open(R / "embalagem/variantes.json", "w"), ensure_ascii=False, indent=1)
(R / "FONTES-E-LICENCAS.md").write_text("# Fontes e licenças: Em Relevo 006\n\nVer `pesquisa/FOTOS.md` (arquivo → autor → licença → URL) e a seção CRÉDITOS de `entrega/pacote/youtube.txt`.\nMapa: SRTM/AWS Terrain Tiles + máscara NASA GIBS (`shared/gera_assets6.py`); chuva NASA GPM IMERG; música Kevin MacLeod (CC BY 4.0); SFX do 005.\n")
print(len(out), "legendas;"); print(caps_txt)
