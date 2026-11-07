#!/usr/bin/env python3
"""Checklist mensurável da bíblia de roteiro v2 do historia-ptbr (canais/historia-ptbr/biblia/roteiro.md).

Vale para os vídeos 006 em diante. Nos vídeos 001–005 (bíblia v1, `biblia/roteiro-v1.md`) roda só como
informação (não reprova nada). Não serve para outros canais.

Uso (da raiz do repo ou de qualquer lugar):
    python3 canais/historia-ptbr/tools/checklist_roteiro_v2.py canais/historia-ptbr/videos/006-xxx
    ... --pergunta "Quem escolhe quem governa o Irã?"   (se o SCRIPT.md/BRIEF.md não tiver "Pergunta central:")
    ... --ppm 130     (ritmo para estimar tempos antes da voz; com legendas.srt usa os tempos reais)
    ... --json        (saída em JSON)
Entrada: $V/SCRIPT.md (gerado pelo roteiro.py: "## Hook", "## N. Título", "## Fecho", blocos "**[N001]** texto").
Tempos: se existir $V/out/legendas.srt ou $V/entrega/legendas.srt, usa os tempos reais (alinhamento por contagem de
palavras); senão estima a --ppm (padrão 130, o drama-3 medido no 003/004).
Saída: tabela PASSA/REPROVA/AVISO/MANUAL; código 1 se algum item obrigatório reprovar num vídeo v2.
Origem das métricas: pesquisa/roteiro-historia-2026-11/metricas_texto.py (RELATORIO.md, 07/11/2026).
"""
import argparse, json, re, sys
from pathlib import Path

# Mesmas listas do metricas_texto.py do relatório, com uma diferença: "seu/sua" saíram do "você"
# (em pt, "seu túmulo" quase sempre é dele, não do espectador; o relatório contava os dois).
CONECTIVOS = r"\b(mas|então|só que|porque|aí|e aí|acontece que|o problema)\b"
VOCE = r"\b(você|vocês|imagine|imagina|pense|repare|olhe|tente|te)\b"
GUARDE = r"\bguard(e|a|em)\b"
SUCESSAO = r"^(quem (assumiu|pegou|ficou|subiu|herdou|tomou)|dess[ae] |desse |depois del|o sucessor|o filho de)"
ABRE_DATA = r"^(em (mil|dois|um|\d)|por volta de|no ano|anos depois|séculos depois|no século)"
PROMESSA = r"(no caminho|nos próximos|pelo caminho|você vai ver|vamos ver|neste vídeo)"
FALA = r"[\"“”]|\b(disse|diz|gritou|escreveu|perguntou|respondeu|teria dito)\b[^.?!]*:"
STOP = set("""a o os as um uma uns umas de da do das dos e é em no na nos nas que se por para com como mais
mas foi ser era essa esse isso esta este isto ela ele eles elas seu sua seus suas qual quem quando onde
porque então história inteira tudo todo toda país vez vezes""".split())


def ler_script(v):
    txt = (v / "SCRIPT.md").read_text()
    secoes, atual = [], None
    for linha in txt.splitlines():
        m = re.match(r"^##\s+(.*)", linha)
        if m:
            atual = {"titulo": m[1].strip(), "blocos": []}; secoes.append(atual); continue
        m = re.match(r"^\*\*\[(N\d+)\]\*\*\s*(.*)", linha)
        if m and atual is not None:
            atual["blocos"].append({"id": m[1], "texto": m[2].strip()})
    return txt, [s for s in secoes if s["blocos"]]


def palavras(t): return re.findall(r"[\wÀ-ú'-]+", t)


def ler_srt(v):
    for p in (v / "out/legendas.srt", v / "entrega/legendas.srt"):
        if p.exists():
            cues = []
            for bloco in re.split(r"\n\s*\n", p.read_text().strip()):
                ls = bloco.strip().splitlines()
                m = next((re.match(r"(\d+):(\d+):(\d+)[,.](\d+)\s*-->\s*(\d+):(\d+):(\d+)[,.](\d+)", l) for l in ls if "-->" in l), None)
                if not m: continue
                g = [int(x) for x in m.groups()]
                ini = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000; fim = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
                texto = " ".join(l for l in ls if "-->" not in l and not l.strip().isdigit())
                cues.append((ini, fim, len(palavras(texto))))
            return p, cues
    return None, []


def tempos(secoes, cues, ppm):
    """Início (s) de cada bloco e fim do vídeo. Com srt: palavra k do roteiro ↔ palavra k·(total_srt/total_roteiro) da legenda."""
    blocos = [b for s in secoes for b in s["blocos"]]
    n = [len(palavras(b["texto"])) for b in blocos]; total = sum(n)
    if cues:
        marcas = []  # (índice acumulado de palavra, tempo)
        acc = 0
        for ini, fim, k in cues:
            for j in range(k): marcas.append(ini + (fim - ini) * j / max(1, k))
            acc += k
        escala = len(marcas) / total
        acc, out = 0, {}
        for b, k in zip(blocos, n):
            out[b["id"]] = marcas[min(len(marcas) - 1, int(acc * escala))]; acc += k
        return out, cues[-1][1], "legendas.srt (tempos reais)"
    acc, out = 0, {}
    for b, k in zip(blocos, n):
        out[b["id"]] = acc / ppm * 60; acc += k
    return out, total / ppm * 60, f"estimado a {ppm} ppm (sem voz)"


def fmt(s): return f"{int(s // 60)}:{int(s % 60):02d}"


def chave(t): return {w for w in (x.lower() for x in palavras(t)) if len(w) >= 4 and w not in STOP}


def achar_pergunta(txt, v, arg, hook):
    if arg: return arg, "--pergunta"
    for fonte in (txt, (v / "BRIEF.md").read_text() if (v / "BRIEF.md").exists() else ""):
        m = re.search(r"pergunta central\**:?\**\s*[:\-–]?\s*\**\s*(.+\?)", fonte, re.I)
        if m: return m[1].strip("* "), "declarada no SCRIPT/BRIEF"
    for b in hook["blocos"]:  # 1ª pergunta do hook; se for curta ("Como?"), junta a frase anterior
        frases = re.split(r"(?<=[.!?])\s+", b["texto"])
        for i, f in enumerate(frases):
            if f.endswith("?"):
                p = f if len(palavras(f)) >= 5 or i == 0 else frases[i - 1] + " " + f
                return p, f"automática ({b['id']}; declare 'Pergunta central:' no SCRIPT.md)"
    return None, "não encontrada"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--pergunta"); ap.add_argument("--ppm", type=float, default=130)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    v = Path(a.video).expanduser().resolve()
    m = re.match(r"(\d{3})-", v.name); num = int(m[1]) if m else 0
    v2 = "historia-ptbr" in str(v) and num >= 6
    txt, secoes = ler_script(v)
    hook = next(s for s in secoes if s["titulo"].lower().startswith("hook"))
    fecho = next((s for s in secoes if s["titulo"].lower().startswith("fecho")), None)
    caps = [s for s in secoes if re.match(r"^\d+\.", s["titulo"])]
    srt, cues = ler_srt(v)
    t0, fim, fonte_t = tempos(secoes, cues, a.ppm)
    todos = [b for s in secoes for b in s["blocos"]]
    corpo = " ".join(b["texto"] for b in todos); low = corpo.lower(); W = len(palavras(corpo))
    R = []  # (item, valor, alvo, status, regra nº)

    def item(nome, valor, alvo, ok, regra, tipo="obrig"):
        st = ("PASSA" if ok else "REPROVA") if tipo == "obrig" else ("ok" if ok else "AVISO") if tipo == "aviso" else "MANUAL"
        R.append({"item": nome, "valor": valor, "alvo": alvo, "status": st, "regra": regra})

    # 1. pergunta central cedo
    perg, origem = achar_pergunta(txt, v, a.pergunta, hook)
    kq = chave(perg or "")
    item("Pergunta central declarada (\"Pergunta central:\" no SCRIPT.md)", origem, "declarada",
         not origem.startswith(("automática", "não")), 1)
    t_perg = None
    if perg:
        for b in todos:
            if "?" in b["texto"] and (len(kq & chave(b["texto"])) >= max(1, len(kq) // 2) or perg[:30] in b["texto"]):
                t_perg = t0[b["id"]]; bloco_perg = b["id"]; break
    item("Pergunta central (como pergunta) até ~0:50", f"{fmt(t_perg)} em {bloco_perg}" if t_perg is not None else "não achada",
         "≤ 0:50", t_perg is not None and t_perg <= 50, 1)
    # 2. pergunta volta ≥ 3× fora do hook
    ids_hook = {b["id"] for b in hook["blocos"]}
    voltas = [b["id"] for b in todos if b["id"] not in ids_hook and (
        ("?" in b["texto"] and kq and len(kq & chave(b["texto"])) >= max(2, (len(kq) + 1) // 2))
        or re.search(r"\b(nossa|aquela) pergunta\b|pergunta (do começo|do início|inicial|central|lá do)|a pergunta continua|peça da resposta|parte da resposta", b["texto"].lower()))]
    item("Pergunta volta em voz alta (fora do hook)", f"{len(voltas)}× {voltas[:6]}", "≥ 3 (fecho responde)", len(voltas) >= 3, 2)
    # 3. motor problema→solução→novo problema: conectivos + fim de capítulo com problema
    con = len(re.findall(CONECTIVOS, low)); con100 = 100 * con / W
    item("Conectivos de virada /100 palavras", f"{con100:.2f} ({con})", "≥ 1,5", con100 >= 1.5, 3)
    fins = [c for c in caps if not re.search(CONECTIVOS + r"|problema|\?|precisava|faltava", c["blocos"][-1]["texto"].lower())]
    item("Capítulo fecha com o problema da próxima era", f"{len(caps) - len(fins)}/{len(caps)}" + (f" (sem: {[c['titulo'][:22] for c in fins]})" if fins else ""),
         "todos", not fins, 3)
    suc = [c["titulo"][:28] + ": " + c["blocos"][0]["texto"][:40] for c in caps if re.search(SUCESSAO, c["blocos"][0]["texto"].lower())]
    item("Nenhum capítulo abre com sucessão seca", f"{len(suc)} {suc}", "0", not suc, 3)
    dat = [c["titulo"][:28] for c in caps if re.search(ABRE_DATA, c["blocos"][0]["texto"].lower())]
    item("Capítulo abrindo com data (ficha, não cena)", f"{len(dat)} {dat}", "≤ 2", len(dat) <= 2, 5, "aviso")
    # 4. espectador na cena
    vc = len(re.findall(VOCE, low)); vc100 = 100 * vc / W
    item("\"Você/imagine\" /100 palavras", f"{vc100:.2f} ({vc})", "≥ 1,0", vc100 >= 1.0, 4)
    sem_ponte = [c["titulo"][:24] for c in caps if not re.search(VOCE, " ".join(b["texto"] for b in c["blocos"]).lower())]
    item("Capítulo com ponte para o espectador", f"{len(caps) - len(sem_ponte)}/{len(caps)}", "todos", not sem_ponte, 4)
    # 7. guarde
    g = len(re.findall(GUARDE, low))
    item("\"Guarde isso\" no vídeo", str(g), "≤ 2", g <= 2, 7)
    # 8. hook
    t_cap1 = t0[caps[0]["blocos"][0]["id"]] if caps else 0
    item("Hook até o capítulo 1", fmt(t_cap1), "0:60–1:15", 45 <= t_cap1 <= 75, 8)
    prom = next((b for b in hook["blocos"] if re.search(PROMESSA, b["texto"].lower())), None)
    if prom:
        resto = prom["texto"].split(":", 1)[-1]
        n_it = 1 + len(re.findall(r",\s(?!que\b|e\b)", resto)) + len(re.findall(r"…?\s+e\s+(?=(o|a|os|as|um|uma)\b)", resto))
        item("Promessa em lista", f"~{n_it} itens ({prom['id']})", "≤ 2", n_it <= 2, 8)
    else:
        item("Promessa em lista", "nenhuma", "≤ 2", True, 8)
    # 9. falas de personagem
    f = len(re.findall(FALA, corpo))
    item("Falas curtas de personagem", str(f), "1–2+", f >= 1, 9, "aviso")
    # 10. ritmo
    ppm = W / (fim / 60)
    if cues:
        item("Ritmo (palavras/min com pausas)", f"{ppm:.0f} ppm em {fmt(fim)}", "140–145 (Hipótese)", 138 <= ppm <= 150, 10)
    else:
        item("Ritmo (palavras/min com pausas)", "sem voz ainda", "140–145 (Hipótese)", True, 10, "aviso")
    frases = [s for s in re.split(r"[.!?…]+\s", corpo) if s.strip()]
    item("Palavras por frase (média)", f"{W / len(frases):.1f}", "≤ 12,5; 5–8 nas viradas", W / len(frases) <= 12.5, 10, "aviso")
    item("Palavras no roteiro", str(W), "~2.250 p/ 16 min a 140 ppm", 1900 <= W <= 2400, 10, "aviso")
    # 11. fecho
    if fecho:
        t_f = fim - t0[fecho["blocos"][0]["id"]]
        item("Fecho (do início do Fecho ao fim)", fmt(t_f), "≤ 0:45", t_f <= 45, 11)
    else:
        item("Fecho", "seção 'Fecho' não achada", "≤ 0:45", False, 11)
    # manuais
    item("1 cena (lugar, pessoa, momento) por capítulo antes dos fatos", "ler", "todos", True, 5, "manual")
    item("Humor seco a cada ~40–60 s, sobre o fato", "ler", "~15–20 tiradas", True, 6, "manual")
    item("Teste da troca + fio condutor ≥ 3 capítulos + loops pagos", "ler", "sim", True, 0, "manual")

    reprov = [r for r in R if r["status"] == "REPROVA"]
    res = {"video": v.name, "biblia": "v2" if v2 else "v1 (só informativo)", "pergunta": perg, "pergunta_origem": origem,
           "tempos": fonte_t, "palavras": W, "itens": R, "reprovados": len(reprov), "aprovado": not reprov}
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=1))
    else:
        print(f"Checklist roteiro v2 · {v.name} · bíblia {res['biblia']} · tempos: {fonte_t}")
        print(f"Pergunta central ({origem}): {perg}")
        print(f"{'nº':>3} {'status':8} {'item':52} {'valor':38} alvo")
        for r in R:
            print(f"{r['regra']:>3} {r['status']:8} {r['item'][:52]:52} {str(r['valor'])[:38]:38} {r['alvo']}")
        print(f"\nResultado: {'APROVADO' if not reprov else f'REPROVADO em {len(reprov)} item(ns)'}"
              + ("" if v2 else " — vídeo da v1: resultado só informativo, não bloqueia"))
    sys.exit(1 if (reprov and v2) else 0)


if __name__ == "__main__":
    main()
