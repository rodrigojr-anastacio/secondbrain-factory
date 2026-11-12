"""Pré-QA visual automático: manda os quadros do pré-QA (stills a cada N s, frames de um mp4 ou uma grade) para um
modelo com visão (Claude Sonnet 5.5 pela API, chave ~/.segredos/anthropic/qa.env) com o checklist de pré-render de
conhecimento/erros-qa.md, e devolve os problemas com timestamp e severidade.

Uso (a partir do repo):
  tools/.venv/bin/python tools/preqa_visual.py <alvo> [--video <id>] [--fps 30] [--intervalo 10] [--modelo sonnet|opus]
      [--saida <pasta>] [--max-quadros 120] [--contexto "texto"]
  <alvo> pode ser:
    - a pasta do vídeo: usa <pasta>/preqa/ (stills do pré-QA, ex.: remotion_stills.cjs → <quadro>.png) se existir;
      senão o mp4 em out/video.mp4 (frames a cada --intervalo s com ffmpeg);
    - uma pasta de stills (<quadro>.png do remotion_stills.cjs: timestamp = quadro ÷ --fps; outros nomes: o nome);
    - um mp4 (frames a cada --intervalo s);
    - uma imagem (grade/contact sheet ou quadro solto).
Saída: PREQA-visual.md na pasta do vídeo (ou em --saida / ao lado do alvo) e PREQA-visual.json.
Código de saída: 0 sem bloqueante · 2 há bloqueante · 1 erro (API, arquivo) · 4 teto mensal do grupo qa (US$ 30).

- Cada lote de até 8 quadros vai numa chamada (quadro a 1280 px de largura, rotulado com o tempo). Antes, sinais
  automáticos grátis (PIL): luminância média < 15 (tela preta) e faixa uniforme colada na borda (≥ 3% da altura/largura,
  ex.: a faixa bege do Em Relevo 002); eles vão como pista ao modelo e aparecem no relatório.
- Se o alvo está dentro de canais/<slug>/, a biblia/visual.md do canal entra como contexto (o que é estilo intencional).
- Custo real em financas.consumo (servico 'preqa-visual', ref_id = --video). Sonnet: ~US$ 0,002 por quadro
  (~US$ 0,15–0,25 por vídeo de 12 min com 1 quadro a cada 10 s).
"""
import argparse
import base64
import glob
import io
import json
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import anthropic_api as A  # noqa: E402

FAB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ERROS_QA = os.path.join(FAB, "conhecimento", "erros-qa.md")
IMG_EXT = (".png", ".jpg", ".jpeg", ".webp")
SEVERIDADES = ["bloqueante", "alto", "medio", "baixo"]

ESQUEMA = {
    "type": "object",
    "properties": {
        "problemas": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "quadro": {"type": "string", "description": "rótulo do quadro exatamente como veio (ex.: Q07)"},
                "categoria": {"type": "string", "description": "fundo/faixa | moldura | texto_inventado | texto_cortado | texto_encavalado | legenda | tela_preta | anacronismo | glifo | valor_errado | elemento_fora | outro"},
                "severidade": {"type": "string", "enum": SEVERIDADES},
                "descricao": {"type": "string", "description": "o que está errado e onde no quadro (curto e concreto)"},
            },
            "required": ["quadro", "categoria", "severidade", "descricao"], "additionalProperties": False}},
        "quadros_ok": {"type": "array", "items": {"type": "string"}, "description": "rótulos dos quadros sem problema"},
    },
    "required": ["problemas", "quadros_ok"], "additionalProperties": False,
}

SISTEMA = """Você faz o pré-QA visual de vídeos faceless do YouTube (mapas 3D, ilustrações de IA, texto na tela, legendas) ANTES do render final.
Recebe quadros rotulados (Q01, Q02… com o tempo no vídeo). Procure defeitos que um espectador veria e que obrigariam a corrigir/re-renderizar.
Use o checklist abaixo (vem da base de erros reais da fábrica). Olhe bordas, cantos, fundo atrás de mapas/globos, cada texto e cada legenda.

Severidade:
- bloqueante: faixa/listra/bloco chapado de cor errada no fundo ou na borda (ex.: faixa bege no topo atrás de um mapa 3D), buraco/emenda no 3D,
  textura sumida, tela preta ou quase preta fora de transição, moldura/margem/faixa preta de imagem de IA, texto inventado/ilegível escrito pela
  IA bem visível (letreiro, mapa, jornal), texto de tela cortado pela borda ou encavalado com outro texto a ponto de atrapalhar a leitura,
  legenda saindo do quadro, glifo "tofu" (quadrado no lugar de símbolo), placeholder.
- alto: mesmo tipo de defeito, porém pequeno/discreto; anacronismo claro (bandeira, uniforme, arquitetura); valor animado claramente errado.
- medio/baixo: estética discutível, legibilidade fraca, detalhe pequeno.
NÃO é defeito: legenda ou texto no meio de uma animação de digitação/entrada (palavra incompleta no fim da linha quando o texto está sendo
revelado), crossfade/transição entre duas cenas, vinheta escura intencional, desfoque de movimento, céu/fundo liso que faz parte da cena,
estilo intencional descrito no contexto do canal, personagem/objeto cortado pela borda como enquadramento normal. Na dúvida entre estilo e defeito, registre como "medio" explicando a dúvida.
Seja específico (onde no quadro, qual texto). Não invente: só o que dá para ver. Cada problema aponta um quadro.
Responda em português do Brasil, só com o JSON do esquema."""


def checklist():
    try:
        s = open(ERROS_QA, encoding="utf-8").read()
        m = re.search(r"## Checklist de pré-render.*?\n(.*?)\n---", s, re.S)
        return m.group(1).strip() if m else s[:4000]
    except OSError:
        return "(conhecimento/erros-qa.md não encontrado)"


def contexto_canal(alvo):
    m = re.search(r"/canais/([^/]+)/", os.path.abspath(alvo) + "/")
    if not m:
        return ""
    v = os.path.join(FAB, "canais", m.group(1), "biblia", "visual.md")
    if os.path.exists(v):
        return f"Canal {m.group(1)} — trecho da bíblia visual (estilo intencional):\n" + open(v, encoding="utf-8").read()[:3500]
    return f"Canal {m.group(1)}."


def mmss(seg):
    seg = int(round(seg))
    return f"{seg // 60}:{seg % 60:02d}"


def frames_do_mp4(mp4, intervalo, tmp, maximo):
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                               capture_output=True, text=True, check=True).stdout.strip() or 0)
    if dur / intervalo > maximo:
        intervalo = dur / maximo
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf", f"fps=1/{intervalo:.3f},scale=1280:-2", "-q:v", "3",
                    os.path.join(tmp, "f%04d.jpg")], check=True)
    fs = sorted(glob.glob(os.path.join(tmp, "f*.jpg")))
    # o filtro fps pega o 1º quadro de cada janela, centrado em ~intervalo/2
    return [(f, (i + 0.5) * intervalo) for i, f in enumerate(fs)], intervalo


def frames_da_pasta(pasta, fps):
    fs = [f for f in glob.glob(os.path.join(pasta, "*")) if f.lower().endswith(IMG_EXT)]
    out = []
    for f in fs:
        nome = os.path.splitext(os.path.basename(f))[0]
        t = int(nome) / fps if nome.isdigit() else None
        out.append((f, t))
    out.sort(key=lambda x: (x[1] is None, x[1] if x[1] is not None else 0, x[0]))
    return out


def sinais_automaticos(caminho):
    """Pistas grátis: luminância média e faixa uniforme colada na borda."""
    from PIL import Image, ImageStat
    im = Image.open(caminho).convert("RGB")
    w, h = im.size
    lum = ImageStat.Stat(im.convert("L")).mean[0]
    sinais = []
    if lum < 15:
        sinais.append(f"luminância média {lum:.0f} (< 15: tela preta?)")
    px = im.resize((min(w, 320), max(1, int(h * min(w, 320) / w)))).load()
    W, H = min(w, 320), max(1, int(h * min(w, 320) / w))

    def linha_uniforme(cores):
        # chapada = sem textura (diferença média entre vizinhos baixa), mesmo com degradê/vinheta suave
        med = [sum(c[i] for c in cores) / len(cores) for i in range(3)]
        desv = max((sum((c[i] - med[i]) ** 2 for c in cores) / len(cores)) ** 0.5 for i in range(3))
        viz = sum(max(abs(cores[j + 1][i] - cores[j][i]) for i in range(3)) for j in range(len(cores) - 1)) / max(len(cores) - 1, 1)
        return viz < 1.5 and desv < 25, med

    for borda in ("topo", "base", "esquerda", "direita"):
        n, cor0 = 0, None
        lim = (H if borda in ("topo", "base") else W) // 3
        for k in range(lim):
            if borda == "topo":
                cores = [px[x, k] for x in range(W)]
            elif borda == "base":
                cores = [px[x, H - 1 - k] for x in range(W)]
            elif borda == "esquerda":
                cores = [px[k, y] for y in range(H)]
            else:
                cores = [px[W - 1 - k, y] for y in range(H)]
            uni, med = linha_uniforme(cores)
            if not uni or (cor0 and max(abs(med[i] - cor0[i]) for i in range(3)) > 18):
                break
            cor0 = cor0 or med
            n += 1
        frac = n / (H if borda in ("topo", "base") else W)
        if frac >= 0.03 and cor0 and sum(cor0) / 3 > 12:  # faixa preta pura de letterbox também aparece (cor ~0); ignora ≤ 12
            sinais.append(f"faixa uniforme na borda {borda}: {frac * 100:.0f}% do quadro, cor RGB({int(cor0[0])},{int(cor0[1])},{int(cor0[2])})")
        elif frac >= 0.03:
            sinais.append(f"faixa preta na borda {borda}: {frac * 100:.0f}% do quadro")
    return sinais


def img_b64(caminho, largura=1280):
    from PIL import Image
    im = Image.open(caminho).convert("RGB")
    if im.width > largura:
        im = im.resize((largura, int(im.height * largura / im.width)))
    if max(im.size) > 1568 and im.height > im.width:  # grade alta
        im.thumbnail((1568, 1568))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=85)
    return base64.b64encode(b.getvalue()).decode()


def analisar(cli, modelo, quadros, contexto, sistema_cache):
    conteudo = []
    for q in quadros:
        rot = f"{q['id']} · t={mmss(q['t'])}" if q["t"] is not None else f"{q['id']} · {q['nome']}"
        if q["sinais"]:
            rot += " · sinais automáticos: " + "; ".join(q["sinais"])
        conteudo.append({"type": "text", "text": rot})
        conteudo.append({"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": img_b64(q["arquivo"])}})
    conteudo.append({"type": "text", "text": "Analise cada quadro acima contra o checklist e responda com o JSON."})
    m = cli.messages.create(model=A.modelo_id(modelo), max_tokens=8000, system=sistema_cache,
                            output_config={"effort": "medium", "format": {"type": "json_schema", "schema": ESQUEMA}},
                            messages=[{"role": "user", "content": conteudo}])
    txt = "".join(c.text for c in m.content if c.type == "text")
    return json.loads(txt), m


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("alvo")
    ap.add_argument("--video", type=int, help="id em youtube.videos (custo vai para o vídeo)")
    ap.add_argument("--fps", type=float, default=30)
    ap.add_argument("--intervalo", type=float, default=10, help="segundos entre frames ao ler um mp4")
    ap.add_argument("--modelo", default="sonnet")
    ap.add_argument("--saida", help="pasta onde gravar PREQA-visual.md")
    ap.add_argument("--max-quadros", type=int, default=120)
    ap.add_argument("--lote", type=int, default=8, help="quadros por chamada")
    ap.add_argument("--contexto", default="", help="texto extra (estilo intencional, o que mudou)")
    ap.add_argument("--incluir-baixo", action="store_true", help="lista também os itens de severidade baixa na tabela")
    a = ap.parse_args()

    alvo = os.path.abspath(a.alvo)
    tmp = tempfile.mkdtemp(prefix="preqa-")
    origem = alvo
    if os.path.isdir(alvo):
        stills = os.path.join(alvo, "preqa")
        mp4 = os.path.join(alvo, "out", "video.mp4")
        if os.path.isdir(stills) and frames_da_pasta(stills, a.fps):
            lista, origem = frames_da_pasta(stills, a.fps), stills
        elif any(f.lower().endswith(IMG_EXT) for f in os.listdir(alvo)):
            lista = frames_da_pasta(alvo, a.fps)
        elif os.path.exists(mp4):
            lista, a.intervalo = frames_do_mp4(mp4, a.intervalo, tmp, a.max_quadros)
            origem = mp4
        else:
            sys.exit(f"nada para analisar em {alvo} (sem preqa/, imagens ou out/video.mp4)")
        saida = a.saida or alvo
    elif alvo.lower().endswith((".mp4", ".mov", ".mkv", ".webm")):
        lista, a.intervalo = frames_do_mp4(alvo, a.intervalo, tmp, a.max_quadros)
        d = os.path.dirname(alvo)
        saida = a.saida or (os.path.dirname(d) if os.path.basename(d) == "out" else d)
    elif alvo.lower().endswith(IMG_EXT):
        lista = [(alvo, None)]
        saida = a.saida or os.path.dirname(alvo)
    else:
        sys.exit(f"alvo não reconhecido: {alvo}")
    if not lista:
        sys.exit("nenhum quadro encontrado")
    if len(lista) > a.max_quadros:
        passo = len(lista) / a.max_quadros
        lista = [lista[int(i * passo)] for i in range(a.max_quadros)]

    quadros = []
    for i, (f, t) in enumerate(lista, 1):
        try:
            s = sinais_automaticos(f)
        except Exception as e:  # noqa: BLE001
            s = [f"(sinais falharam: {type(e).__name__})"]
        quadros.append({"id": f"Q{i:02d}", "arquivo": f, "t": t, "nome": os.path.basename(f), "sinais": s})

    previsto = len(quadros) * (0.01 if "opus" in a.modelo else 0.004)
    try:
        A.checar_teto("qa", previsto=previsto)
    except A.TetoExcedido as e:
        print(f"[preqa_visual] ERRO: {e}", file=sys.stderr)
        sys.exit(4)

    ctx = "\n\n".join(x for x in [contexto_canal(alvo), a.contexto] if x)
    sistema = [{"type": "text", "text": SISTEMA + "\n\n# Checklist de pré-render (conhecimento/erros-qa.md)\n" + checklist()
                + ("\n\n# Contexto do canal/vídeo\n" + ctx if ctx else ""), "cache_control": {"type": "ephemeral"}}]
    cli = A.cliente("qa")
    problemas, oks, custo, tokens, modelo_real, falhas = [], set(), 0.0, 0, None, []
    for k in range(0, len(quadros), a.lote):
        lote = quadros[k:k + a.lote]
        try:
            r, m = analisar(cli, a.modelo, lote, ctx, sistema)
        except Exception as e:  # noqa: BLE001
            falhas.append(f"{lote[0]['id']}–{lote[-1]['id']}: {type(e).__name__}: {str(e)[:200]}")
            print(f"[preqa_visual] lote {lote[0]['id']}–{lote[-1]['id']} falhou: {type(e).__name__}", file=sys.stderr)
            continue
        custo += A.custo_usd(m.model, m.usage)
        tokens += A.tokens_total(m.usage)
        modelo_real = m.model
        ids = {q["id"] for q in lote}
        problemas += [p for p in r.get("problemas", []) if p.get("quadro") in ids]
        oks |= set(r.get("quadros_ok", [])) & ids
        print(f"[preqa_visual] {lote[0]['id']}–{lote[-1]['id']}: {len(r.get('problemas', []))} problema(s)", file=sys.stderr)

    if custo or tokens:
        A.registrar_consumo(custo, "preqa-visual", tokens, "tokens", video=a.video,
                            notas=f"preqa_visual.py {modelo_real}: {len(quadros)} quadros de {os.path.relpath(origem, FAB) if origem.startswith(FAB) else origem}")

    por_id = {q["id"]: q for q in quadros}
    ordem = {s: i for i, s in enumerate(SEVERIDADES)}
    problemas.sort(key=lambda p: (por_id[p["quadro"]]["t"] if por_id[p["quadro"]]["t"] is not None else 0, ordem.get(p["severidade"], 9)))
    n = {s: sum(1 for p in problemas if p["severidade"] == s) for s in SEVERIDADES}
    bloq = n["bloqueante"] > 0

    os.makedirs(saida, exist_ok=True)
    md = [f"# Pré-QA visual automático",
          "",
          f"- Alvo: `{os.path.relpath(origem, FAB) if origem.startswith(FAB) else origem}` · {len(quadros)} quadros"
          + (f" (1 a cada {a.intervalo:.0f} s)" if origem.lower().endswith(".mp4") else "")
          + f" · modelo `{modelo_real or A.modelo_id(a.modelo)}` · custo US$ {custo:.3f} · `tools/preqa_visual.py`",
          f"- Resultado: **{'REPROVADO (há bloqueante)' if bloq else 'sem bloqueante'}** · bloqueante {n['bloqueante']} · alto {n['alto']} · médio {n['medio']} · baixo {n['baixo']}",
          "- Confira cada item no quadro (o modelo erra para os dois lados): falso positivo → anote e siga; defeito real → corrija e refaça os stills do trecho.",
          ""]
    if falhas:
        md += ["**Lotes que falharam (não analisados):** " + "; ".join(falhas), ""]
    if problemas:
        md += ["| Tempo | Quadro | Severidade | Categoria | Problema |", "|---|---|---|---|---|"]
        for p in problemas:
            if p["severidade"] == "baixo" and not a.incluir_baixo:
                continue
            q = por_id[p["quadro"]]
            tempo = mmss(q["t"]) if q["t"] is not None else "—"
            md.append(f"| {tempo} | {p['quadro']} `{q['nome']}` | {p['severidade']} | {p['categoria']} | {p['descricao'].replace('|', '/')} |")
        if n["baixo"] and not a.incluir_baixo:
            md.append(f"\n{n['baixo']} item(ns) de severidade baixa só no PREQA-visual.json (use --incluir-baixo para listar).")
        md.append("")
    sinais = [(q, s) for q in quadros for s in q["sinais"]]
    if sinais:
        md += ["## Sinais automáticos (PIL, sem IA)", ""] + [
            f"- {q['id']} ({mmss(q['t']) if q['t'] is not None else q['nome']}): {s}" for q, s in sinais] + [""]
    md += ["## Quadros", "", ", ".join(f"{q['id']}={mmss(q['t']) if q['t'] is not None else q['nome']}" for q in quadros), ""]
    open(os.path.join(saida, "PREQA-visual.md"), "w", encoding="utf-8").write("\n".join(md))
    json.dump({"alvo": origem, "modelo": modelo_real, "custo_usd": round(custo, 4), "contagem": n, "bloqueante": bloq,
               "problemas": [{**p, "t": por_id[p["quadro"]]["t"], "arquivo": por_id[p["quadro"]]["nome"]} for p in problemas],
               "falhas": falhas, "quadros": [{k: q[k] for k in ("id", "t", "nome", "sinais")} for q in quadros]},
              open(os.path.join(saida, "PREQA-visual.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[preqa_visual] {len(quadros)} quadros · bloqueante {n['bloqueante']} · alto {n['alto']} · médio {n['medio']} · "
          f"baixo {n['baixo']} · US$ {custo:.3f} → {os.path.join(saida, 'PREQA-visual.md')}", file=sys.stderr)
    if falhas and not problemas and not oks:
        sys.exit(1)
    sys.exit(2 if bloq else 0)


if __name__ == "__main__":
    main()
