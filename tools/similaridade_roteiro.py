#!/usr/bin/env python3
"""Detector de cópia de roteiro (16/11/2026): o nosso roteiro × as transcrições das referências ("a manada").

Por que existe: o historia-ptbr/005-brasil saiu praticamente igual ao History in Minutes (Vug2cLY3nxk) e ao clone
History Easy Guide (sD0cIJ8JMYw), porque a bíblia mandava "remodelar a transcrição (mesma ordem, beats e números)".
Regra nova: FORMA modelada dos canais de sucesso, CONTEÚDO e ÂNGULO nossos. Este script mede o conteúdo.

Uso (da raiz do repo):
  tools/.venv/bin/python tools/similaridade_roteiro.py <pasta-do-video> [--refs a.txt b.vtt ...] [--idioma pt]
        [--saida <pasta-do-video>/SIMILARIDADE.md] [--sem-traducao] [--video <id>]
  - roteiro: <pasta>/blocos.json (ou shared/blocos.json, ou SCRIPT.md/ROTEIRO.md)
  - referências (padrão): <pasta>/ref/*.txt|*.vtt (transcrições; manada-*.txt do tools/manada.py)
  - idioma do roteiro: --idioma, senão o canal.yaml do canal, senão detectado.
  Saída: SIMILARIDADE.md (+ .json) com nota 0–100 por referência, veredito e os trechos parecidos.
  Código de saída: 0 = passa · 2 = atenção (passa, mas o crivo olha os trechos) · 3 = CÓPIA (volta para reescrita).

Como mede (sem embeddings pagos):
  1. Referência em outro idioma é traduzida para o idioma do roteiro pelo Claude Haiku (créditos da API, chave `qa`,
     ~US$ 0,002 por transcrição; cache em ~/cache/similaridade/, então cada referência só é paga uma vez).
  2. Texto normalizado (minúsculas, sem acento, sem palavras vazias, radical = 5 primeiras letras, números por extenso
     convertidos para dígitos quando simples).
  3. Cada bloco do roteiro (2–4 frases) é comparado por TF-IDF com janelas de tamanho parecido da referência:
     - cobertura = % dos blocos do roteiro que têm um "gêmeo" na referência (cosseno ≥ LIMIAR_GEMEO);
     - ordem = dos gêmeos, a fração que aparece na MESMA sequência da referência (maior subsequência crescente);
     - n-gramas = % dos trigramas de radicais do roteiro presentes na referência.
  4. nota = 100 × (0,55 × cobertura + 0,25 × cobertura × ordem + 0,20 × min(1, 4 × trigramas)); vale a MAIOR nota
     entre as referências.
  Calibrado em 16/11/2026 (pesquisa/roteiro-angulo-2026-11/CALIBRAGEM.md): 005-brasil × History in Minutes = 47 e
  × History Easy Guide = 38 (cópias conhecidas); mesmo tema, vídeos independentes = 0–13; tema diferente ≈ 0.
"""
import argparse
import hashlib
import json
import math
import os
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CACHE = Path(os.path.expanduser("~/cache/similaridade"))
sys.path.insert(0, str(RAIZ / "tools"))

# Limites calibrados (ver CALIBRAGEM.md). nota ≥ COPIA → reprova; ≥ ATENCAO → o crivo olha os trechos.
LIMITES = {"ATENCAO": 18, "COPIA": 30}
LIMIAR_GEMEO = 0.30       # cosseno TF-IDF de um bloco com a melhor janela da referência para contar como "gêmeo"
LIMIAR_TRECHO = 0.30      # trechos listados no relatório

VAZIAS = {
    "pt": "a o as os um uma uns umas de do da dos das em no na nos nas por pelo pela pelos pelas para pra com sem e ou mas que se "
          "nao sim ja mais menos muito muita muitos muitas pouco seu sua seus suas ele ela eles elas isso isto esse essa esses essas "
          "este esta estes estas aquele aquela aquilo lhe lhes me te nos voce voces eu tu era foi sao ser estar esta estava tem tinha "
          "ter ha havia vai vao como quando onde quem qual quais ate entao tambem so ainda depois antes entre sobre sob ao aos "
          "num numa todo toda todos todas outro outra outros outras mesmo mesma porque pois aqui ali la cada tudo nada fica ficou",
    "es": "a el la los las un una unos unas de del en por para con sin y o pero que se no si ya mas menos muy mucho mucha muchos "
          "muchas poco su sus lo le les me te nos os yo tu el ella ellos ellas eso esto ese esa esos esas este esta estos estas "
          "aquel aquella era fue son ser estar estaba tiene tenia tener hay habia va van como cuando donde quien cual cuales "
          "hasta entonces tambien solo aun despues antes entre sobre al todo toda todos todas otro otra otros otras mismo misma "
          "porque pues aqui alli cada nada usted ustedes",
    "en": "a an the of in on at by for to with without and or but that this these those it its is are was were be been being "
          "has have had do does did not no yes so as if then than there their they them he she his her him we our you your i "
          "me my what which who whom when where why how all any each every some such only also just more most very much many "
          "into from out up down over under again once here about after before between through during would could should will "
          "can may might must shall one",
}
VAZIAS = {k: set(v.split()) for k, v in VAZIAS.items()}

NUMS = {  # números por extenso mais comuns → dígito (roteiro escreve por extenso, transcrição em dígito)
    "pt": {"um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8,
           "nove": 9, "dez": 10, "vinte": 20, "trinta": 30, "quarenta": 40, "cinquenta": 50, "cem": 100, "cento": 100,
           "duzentos": 200, "trezentos": 300, "quinhentos": 500, "mil": 1000, "milhao": 10**6, "milhoes": 10**6},
    "es": {"uno": 1, "una": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
           "diez": 10, "veinte": 20, "treinta": 30, "cuarenta": 40, "cincuenta": 50, "cien": 100, "ciento": 100,
           "quinientos": 500, "mil": 1000, "millon": 10**6, "millones": 10**6},
    "en": {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
           "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "hundred": 100, "thousand": 1000, "million": 10**6},
}


# ---------------------------------------------------------------- leitura
def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def limpa_tags(s):
    s = re.sub(r"\[[^\]]*\]", " ", s)          # [serious], [break], [0:12]
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def ler_vtt(caminho):
    linhas, ult = [], None
    for ln in Path(caminho).read_text(errors="ignore").splitlines():
        ln = ln.strip()
        if not ln or "-->" in ln or ln.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")) or ln.isdigit():
            continue
        ln = limpa_tags(ln)
        if ln and ln != ult:
            linhas.append(ln)
            ult = ln
    return " ".join(linhas)


def ler_ref(caminho):
    p = Path(caminho)
    if p.suffix == ".vtt":
        return ler_vtt(p)
    txt = p.read_text(errors="ignore")
    txt = "\n".join(l for l in txt.splitlines() if not l.startswith("# "))  # cabeçalho do manada.py
    return limpa_tags(txt)


def ler_roteiro(pasta):
    """Lista de blocos (texto) do roteiro, na ordem."""
    pasta = Path(pasta)
    for cand in (pasta / "blocos.json", pasta / "shared" / "blocos.json"):
        if cand.exists():
            b = json.loads(cand.read_text())
            if isinstance(b, dict):
                b = b.get("blocos") or list(b.values())
            out = []
            for x in b:
                t = (x.get("texto") or x.get("fala") or x.get("text") or "") if isinstance(x, dict) else str(x)
                t = limpa_tags(t)
                if t:
                    out.append(t)
            if out:
                return out, cand
    for nome in ("SCRIPT.md", "ROTEIRO.md"):
        cand = pasta / nome
        if cand.exists():
            pars = [limpa_tags(re.sub(r"^[#>*|\-\s]+", "", p)) for p in re.split(r"\n\s*\n", cand.read_text())]
            return [p for p in pars if len(p.split()) >= 8], cand
    raise SystemExit(f"roteiro não encontrado em {pasta} (blocos.json, shared/blocos.json, SCRIPT.md, ROTEIRO.md)")


def idioma_canal(pasta):
    p = Path(pasta).resolve()
    for anc in [p, *p.parents]:
        y = anc / "canal.yaml"
        if y.exists():
            m = re.search(r"^\s*idioma:\s*['\"]?([a-z]{2})", y.read_text(), re.M)
            if m:
                return m.group(1)
    if "canal-clima" in str(p):
        return "pt"
    return None


def detecta_idioma(txt):
    t = set(re.findall(r"[a-zà-ú]+", txt.lower()[:20000]))
    marc = {"pt": {"não", "você", "também", "então", "uma", "isso", "foi", "quando"},
            "es": {"pero", "también", "entonces", "una", "fue", "cuando", "muy", "esto"},
            "en": {"the", "and", "was", "when", "this", "but", "they", "with"}}
    return max(marc, key=lambda k: len(marc[k] & t))


# ---------------------------------------------------------------- tradução (com cache)
def traduzir(txt, de, para, video=None):
    CACHE.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha1(f"{de}>{para}\n{txt}".encode()).hexdigest()[:16]
    arq = CACHE / f"{h}.{de}-{para}.txt"
    if arq.exists():
        return arq.read_text(), 0.0
    import anthropic_api as A
    nomes = {"pt": "português do Brasil", "es": "espanhol", "en": "inglês", "fr": "francês", "de": "alemão"}
    A.checar_teto("qa", previsto=0.05)
    cli = A.cliente("qa")
    palavras = txt.split()
    partes, out, custo, tokens = [" ".join(palavras[i:i + 2500]) for i in range(0, len(palavras), 2500)], [], 0.0, 0
    for parte in partes:
        r = cli.messages.create(
            model=A.modelo_id("haiku"), max_tokens=8000,
            system=(f"Traduza fielmente para {nomes.get(para, para)} a transcrição abaixo. Mantenha a ordem e o sentido "
                    "frase a frase, sem resumir, sem comentar, sem acrescentar nada. Escreva números e anos em dígitos. "
                    "Responda só com a tradução."),
            messages=[{"role": "user", "content": parte}])
        out.append("".join(b.text for b in r.content if getattr(b, "type", "") == "text"))
        custo += A.custo_usd("haiku", r.usage)
        tokens += A.tokens_total(r.usage)
    trad = "\n".join(out)
    arq.write_text(trad)
    try:
        A.registrar_consumo(custo, "preqa:similaridade-traducao", tokens, notas=f"{de}->{para} {len(palavras)} palavras",
                            video=video)
    except Exception as e:  # noqa: BLE001
        print(f"aviso: custo não registrado ({type(e).__name__})", file=sys.stderr)
    return trad, custo


# ---------------------------------------------------------------- normalização e TF-IDF
def tokens(txt, idioma, com_pos=False):
    """Radicais de conteúdo; com_pos=True devolve também o índice da palavra (split()) de cada radical."""
    vaz, nums = VAZIAS.get(idioma, set()), NUMS.get(idioma, {})
    out, pos = [], []
    for iw, palavra in enumerate(txt.split()):
        for w in re.findall(r"[a-z0-9]+", sem_acento(palavra.lower())):
            if w in nums:
                out.append(str(nums[w])); pos.append(iw)
                continue
            if w in vaz or (len(w) < 3 and not w.isdigit()):
                continue
            out.append(w if w.isdigit() else w[:5]); pos.append(iw)
    return (out, pos) if com_pos else out


def janelas(toks, tam, passo):
    if len(toks) <= tam:
        return [(0, toks)]
    return [(i, toks[i:i + tam]) for i in range(0, len(toks) - tam // 2, passo)]


def tfidf(docs, idf):
    vs = []
    for d in docs:
        c = Counter(d)
        v = {t: (1 + math.log(n)) * idf.get(t, 0) for t, n in c.items()}
        nrm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vs.append({t: x / nrm for t, x in v.items()})
    return vs


def cos(a, b):
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(t, 0.0) for t, x in a.items())


def lis(seq):
    """Tamanho da maior subsequência crescente."""
    import bisect
    caudas = []
    for x in seq:
        i = bisect.bisect_left(caudas, x)
        if i == len(caudas):
            caudas.append(x)
        else:
            caudas[i] = x
    return len(caudas)


def trigramas(toks):
    return {tuple(toks[i:i + 3]) for i in range(len(toks) - 2)}


def comparar(blocos, ref_txt, idioma, idf_extra=None):
    bt = [tokens(b, idioma) for b in blocos]
    rt, rpos = tokens(ref_txt, idioma, com_pos=True)
    tam = max(12, int(sum(len(x) for x in bt) / max(1, len(bt))))
    jan = janelas(rt, tam, max(4, tam // 2))
    docs = bt + [j for _, j in jan]
    df = Counter(t for d in docs for t in set(d))
    n = len(docs)
    idf = {t: math.log((n + 1) / (c + 1)) + 1 for t, c in df.items()}
    vb, vj = tfidf(bt, idf), tfidf([j for _, j in jan], idf)
    melhor = []
    for i, v in enumerate(vb):
        sc = [(cos(v, w), k) for k, w in enumerate(vj)]
        s, k = max(sc) if sc else (0.0, 0)
        melhor.append((s, k))
    gemeos = [(i, k, s) for i, (s, k) in enumerate(melhor) if s >= LIMIAR_GEMEO]
    cob = len(gemeos) / max(1, len(blocos))
    ordem = (lis([k for _, k, _ in gemeos]) / len(gemeos)) if len(gemeos) >= 3 else 0.0
    tri_r = trigramas(rt)
    tri_b = set().union(*[trigramas(x) for x in bt]) if bt else set()
    ng = len(tri_b & tri_r) / max(1, len(tri_b))
    sim_media = sum(s for s, _ in melhor) / max(1, len(melhor))
    trechos = []
    rt_txt_words = ref_txt.split()
    for i, k, s in sorted(gemeos, key=lambda x: -x[2]):
        if s < LIMIAR_TRECHO:
            continue
        a0 = rpos[min(jan[k][0], len(rpos) - 1)] if rpos else 0
        a1 = rpos[min(jan[k][0] + tam - 1, len(rpos) - 1)] + 1 if rpos else 0
        trechos.append({"bloco": i + 1, "cos": round(s, 2), "nosso": blocos[i][:260],
                        "ref": " ".join(rt_txt_words[a0:a1])[:300]})
    return {"cobertura": cob, "ordem": ordem, "ngramas": ng, "sim_media": sim_media, "gemeos": len(gemeos),
            "blocos": len(blocos), "posicoes": [(i + 1, k) for i, k, _ in gemeos], "trechos": trechos[:12]}


def nota_ref(m):
    """0–100. Cobertura pesa mais; ordem só conta multiplicada pela cobertura (poucos gêmeos em ordem não é cópia);
    trigramas literais (texto traduzido/reescrito colado) completam."""
    return round(100 * (0.55 * m["cobertura"] + 0.25 * m["cobertura"] * m["ordem"] + 0.20 * min(1.0, 4 * m["ngramas"])), 1)


def veredito(nota):
    return "CÓPIA" if nota >= LIMITES["COPIA"] else ("atenção" if nota >= LIMITES["ATENCAO"] else "ok")


# ---------------------------------------------------------------- principal
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pasta")
    ap.add_argument("--refs", nargs="*", help="transcrições (.txt/.vtt); padrão <pasta>/ref/*")
    ap.add_argument("--texto", help="compara um texto qualquer (ex.: transcrição de outro canal) no lugar do roteiro da pasta "
                    "(cortado em blocos de ~35 palavras; calibragem)")
    ap.add_argument("--idioma")
    ap.add_argument("--saida")
    ap.add_argument("--sem-traducao", action="store_true", help="não traduz (só refs no mesmo idioma)")
    ap.add_argument("--video", type=int, help="id em youtube.videos (custo da tradução)")
    ap.add_argument("--json-stdout", action="store_true")
    a = ap.parse_args()
    pasta = Path(a.pasta)
    if a.texto:
        w = ler_ref(a.texto).split()
        blocos, fonte = [" ".join(w[i:i + 35]) for i in range(0, len(w), 35)], Path(a.texto)
    else:
        blocos, fonte = ler_roteiro(pasta)
    idioma = a.idioma or idioma_canal(pasta) or detecta_idioma(" ".join(blocos))
    refs = a.refs or sorted(str(p) for p in (pasta / "ref").glob("*") if p.suffix in (".txt", ".vtt")
                            and not p.name.endswith((".pt-orig.vtt",)))
    # mesma referência em .txt e .vtt: fica o .txt
    vistos, lista = set(), []
    for r in refs:
        m = re.search(r"([A-Za-z0-9_-]{11})(?:\.[a-z-]+)?\.(txt|vtt)$", r)
        chave = m.group(1) if m else r
        if chave in vistos:
            continue
        vistos.add(chave)
        lista.append(r)
    if not lista:
        raise SystemExit("nenhuma referência: rode tools/manada.py transcrever ou passe --refs")
    resultados, custo_total = [], 0.0
    for r in lista:
        txt = ler_ref(r)
        if len(txt.split()) < 150:
            continue
        lr = detecta_idioma(txt)
        traduzido = False
        if lr != idioma and not a.sem_traducao:
            txt, c = traduzir(txt, lr, idioma, a.video)
            custo_total += c
            traduzido = True
        m = comparar(blocos, txt, idioma)
        m.update(ref=str(r), idioma_ref=lr, traduzido=traduzido, palavras_ref=len(txt.split()))
        m["nota"] = nota_ref(m)
        m["veredito"] = veredito(m["nota"])
        resultados.append(m)
    resultados.sort(key=lambda x: -x["nota"])
    nota = resultados[0]["nota"] if resultados else 0.0
    ver = veredito(nota)
    # blocos que são gêmeos de 2+ referências = "consenso da manada" no nosso texto
    cont = Counter(i for m in resultados for i, _ in m["posicoes"])
    manada = sorted(i for i, c in cont.items() if c >= 2)
    out = {"pasta": str(pasta), "roteiro": str(fonte), "idioma": idioma, "blocos": len(blocos), "nota": nota,
           "veredito": ver, "limites": LIMITES, "limiar_gemeo": LIMIAR_GEMEO, "custo_traducao_usd": round(custo_total, 4),
           "blocos_consenso_manada": manada, "referencias": resultados}
    saida = Path(a.saida) if a.saida else pasta / "SIMILARIDADE.md"
    saida.parent.mkdir(parents=True, exist_ok=True)
    saida.with_suffix(".json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    L = [f"# Similaridade do roteiro × referências · {pasta}",
         f"Roteiro: `{fonte}` ({len(blocos)} blocos, {idioma}) · gerado por `tools/similaridade_roteiro.py` · "
         f"tradução US$ {custo_total:.3f}",
         "", f"## Nota máxima: **{nota:.0f}/100 → {ver}** (atenção ≥ {LIMITES['ATENCAO']}, cópia ≥ {LIMITES['COPIA']})", "",
         "| Referência | idioma | nota | veredito | cobertura (gêmeos) | ordem | trigramas |", "|---|---|---|---|---|---|---|"]
    for m in resultados:
        L.append(f"| `{Path(m['ref']).name}` | {m['idioma_ref']}{' → ' + idioma if m['traduzido'] else ''} | {m['nota']:.0f} | "
                 f"{m['veredito']} | {m['cobertura']:.0%} ({m['gemeos']}/{m['blocos']}) | {m['ordem']:.0%} | {m['ngramas']:.1%} |")
    L += ["", f"Blocos do nosso roteiro com gêmeo em 2+ referências (consenso da manada): "
          f"{', '.join(map(str, manada)) or 'nenhum'} ({len(manada)}/{len(blocos)} = {len(manada) / max(1, len(blocos)):.0%}).", ""]
    for m in resultados[:2]:
        if not m["trechos"]:
            continue
        L += [f"## Trechos mais parecidos com `{Path(m['ref']).name}`", ""]
        for t in m["trechos"][:8]:
            L += [f"- **bloco {t['bloco']}** (cos {t['cos']}): {t['nosso']}", f"  - ref: {t['ref']}"]
        L.append("")
    L += ["## Como ler", "- **cobertura** = % dos nossos blocos com um gêmeo (mesmo conteúdo) na referência; **ordem** = dos gêmeos, "
          "quantos vêm na mesma sequência da referência; **trigramas** = sequências de 3 radicais iguais (texto colado).",
          "- Cópia = muitos gêmeos **na mesma ordem**. Tema com fatos obrigatórios (datas, nomes) dá alguns gêmeos isolados: normal.",
          "- Acima do limite: o roteiro volta para reescrita com ângulo próprio (skill `roteiro`, crivo de ângulo; máx. 2 rodadas)."]
    saida.write_text("\n".join(L) + "\n")
    if a.json_stdout:
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(f"nota {nota:.0f}/100 → {ver}  ({saida})")
        for m in resultados:
            print(f"  {m['nota']:5.1f} {m['veredito']:8s} cob {m['cobertura']:.0%} ordem {m['ordem']:.0%} tri {m['ngramas']:.1%}"
                  f"  {Path(m['ref']).name}")
    sys.exit({"ok": 0, "atenção": 2, "CÓPIA": 3}[ver])


if __name__ == "__main__":
    main()
