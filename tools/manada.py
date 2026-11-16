#!/usr/bin/env python3
"""manada.py: levanta e transcreve "a manada" de um tema (custo zero, sem API paga).

A manada = os vídeos de mais views no YouTube sobre um tema. Serve para comparar
o nosso roteiro com o que já existe (detector de cópia) e escolher outro ângulo.

Uso (rodar de tools/ com tools/.venv/bin/python):
  manada.py buscar <saida_dir> --idioma pt,en "<termo 1>" ["<termo 2>" ...]
            [--por-termo 15] [--top 5] [--min-dur 300] [--max-dur 2400]
      ytsearchN por termo e idioma (--idioma repetível ou lista "pt,en,es"),
      junta, deduplica, completa views/duração, descarta < min-dur (shorts) e > max-dur
      (maratonas/aulas; 0 = sem teto) e
      grava <saida_dir>/manada.json (ordenado por views) + imprime a tabela.
  manada.py transcrever <saida_dir> [--ids id1,id2] [--top 5]
      baixa a legenda (manual > automática, no idioma ORIGINAL do vídeo), converte
      para <saida_dir>/manada-<id>.txt; sem legenda/429 repetido cai no Whisper
      (tools/transcrever.py, lento). Atualiza o manada.json (campos txt, fonte, palavras).
  manada.py vtt2txt <arquivo.vtt> <saida.txt>
      só a conversão vtt -> texto limpo com marcas [m:ss].

Regras: YouTube só via proxy WARP socks5://127.0.0.1:40000 (IP da VPS é bloqueado);
temporários em $HOME/cache/tmp (nunca /tmp, que é RAM).
"""
import argparse, json, os, re, subprocess, sys, tempfile, time, shutil

PROXY = "socks5://127.0.0.1:40000"
NODE = os.path.expanduser("~/.hermes/tools/node-26.12.1-linux-x64/bin/node")
HERE = os.path.dirname(os.path.abspath(__file__))
YTDLP = os.path.join(os.path.dirname(sys.executable), "yt-dlp")
TMPBASE = os.path.expanduser("~/cache/tmp")
os.makedirs(TMPBASE, exist_ok=True)

# Idioma usado para "puxar" a busca (a busca do YouTube não filtra idioma de verdade,
# então anexamos uma região/idioma por meio de --extractor-args e do próprio termo).
MARCA_PAUSA = 7  # segundos entre marcas [m:ss]


def ytdlp(args, timeout=240):
    """Roda yt-dlp com proxy e runtime JS; devolve CompletedProcess."""
    cmd = [YTDLP, "--proxy", PROXY, "--js-runtimes", f"node:{NODE}",
           "--no-warnings", "--ignore-no-formats-error"] + args
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def fmt_ts(s):
    s = int(s)
    return f"{s // 60}:{s % 60:02d}"


# ---------------------------------------------------------------- vtt -> txt
def _ts(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def vtt2txt(vtt_path, out_path, cabecalho=None):
    """Converte vtt (manual ou auto-sub com palavras marcadas) em texto limpo.
    Remove tags <c> e <00:00:00.000>, descarta linhas repetidas consecutivas
    (auto-sub repete cada linha 2-3x) e coloca [m:ss] a cada ~MARCA_PAUSA s."""
    import html
    texto = open(vtt_path, encoding="utf-8", errors="replace").read()
    # varre linha a linha: "-->" abre um cue; as demais linhas pertencem a ele
    # (não dá para separar por linha em branco: auto-sub tem linhas só com espaço)
    ultima = None            # última linha emitida (dedupe consecutivo)
    emitidas = []            # (inicio_s, texto)
    ini = None
    for l in texto.split("\n"):
        if "-->" in l:
            ini = _ts(l.split("-->")[0].strip())
            continue
        if ini is None:
            continue
        l = re.sub(r"<[^>]+>", "", l)
        l = html.unescape(l).replace("\u200b", "")
        l = re.sub(r"\s+", " ", l).strip()
        if not l or l == ultima:
            continue
        emitidas.append((ini, l))
        ultima = l
    saida, buf, t0 = [], [], None
    for ini, l in emitidas:
        if t0 is None:
            t0 = ini
        elif ini - t0 >= MARCA_PAUSA and buf:
            saida.append(f"[{fmt_ts(t0)}] " + " ".join(buf))
            buf, t0 = [], ini
        buf.append(l)
    if buf:
        saida.append(f"[{fmt_ts(t0)}] " + " ".join(buf))
    corpo = "\n".join(saida) + "\n"
    with open(out_path, "w", encoding="utf-8") as f:
        if cabecalho:
            f.write(cabecalho.rstrip("\n") + "\n")
        f.write(corpo)
    return len(corpo.split())


# ------------------------------------------------------------------- buscar
def _entrada(e, idioma):
    return {
        "id": e.get("id"), "titulo": e.get("title"),
        "canal": e.get("channel") or e.get("uploader"),
        "views": e.get("view_count"), "duracao_s": e.get("duration"),
        "data": e.get("upload_date"), "idioma_busca": idioma,
        "url": f"https://www.youtube.com/watch?v={e.get('id')}",
    }


def cmd_buscar(a):
    idiomas = [i.strip() for x in a.idioma for i in x.split(",") if i.strip()]
    achados = {}
    for idi in idiomas:
        for termo in a.termos:
            # lang/região no termo não é confiável; o próprio termo já vem no idioma.
            r = ytdlp(["-J", "--flat-playlist", f"ytsearch{a.por_termo}:{termo}"])
            if r.returncode != 0 or not r.stdout.strip():
                print(f"! busca falhou ({idi}) '{termo}': {r.stderr[-200:]}", file=sys.stderr)
                continue
            for e in json.loads(r.stdout).get("entries", []):
                if not e or not e.get("id"):
                    continue
                n = _entrada(e, idi)
                if e["id"] not in achados:
                    achados[e["id"]] = n
                else:  # mantém o maior view_count conhecido
                    if (n["views"] or 0) > (achados[e["id"]]["views"] or 0):
                        achados[e["id"]]["views"] = n["views"]
            time.sleep(2)
    lista = list(achados.values())
    # completa views/duração/data via -J por vídeo (só nos ~15 melhores candidatos)
    falta = [v for v in lista if v["views"] is None or v["duracao_s"] is None or not v["data"]]
    falta.sort(key=lambda v: -(v["views"] or 0))
    for v in falta[:15] if len(falta) > 15 else falta:
        r = ytdlp(["-J", "--skip-download", v["url"]])
        if r.returncode == 0 and r.stdout.strip():
            j = json.loads(r.stdout)
            v["views"] = j.get("view_count", v["views"])
            v["duracao_s"] = j.get("duration", v["duracao_s"])
            v["data"] = j.get("upload_date", v["data"])
            v["canal"] = j.get("channel") or v["canal"]
            v["titulo"] = j.get("title") or v["titulo"]
        time.sleep(2)
    # descarta shorts/curtos (duração desconhecida também sai se views desconhecidas)
    lista = [v for v in lista if (v["duracao_s"] or 0) >= a.min_dur
             and (not a.max_dur or (v["duracao_s"] or 0) <= a.max_dur)]
    lista.sort(key=lambda v: -(v["views"] or 0))
    os.makedirs(a.saida_dir, exist_ok=True)
    caminho = os.path.join(a.saida_dir, "manada.json")
    json.dump(lista, open(caminho, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(lista)} vídeos >= {a.min_dur}s -> {caminho}")
    for i, v in enumerate(lista[:max(a.top * 3, 15)], 1):
        print(f"{i:2d} {v['id']} {(v['views'] or 0):>11,} {fmt_ts(v['duracao_s'] or 0):>6} "
              f"{(v['data'] or ''):8} {(v['canal'] or '')[:24]:24} {(v['titulo'] or '')[:60]}")


# -------------------------------------------------------------- transcrever
def _baixar_legenda(v, tmp):
    """Tenta legenda manual e depois automática no idioma original. Devolve
    (caminho_vtt, fonte, idioma) ou (None, None, idioma)."""
    r = ytdlp(["-J", "--skip-download", v["url"]])
    if r.returncode != 0 or not r.stdout.strip():
        return None, "erro-info", None
    j = json.loads(r.stdout)
    v["views"] = j.get("view_count", v.get("views"))
    v["canal"] = j.get("channel") or v.get("canal")
    v["titulo"] = j.get("title") or v.get("titulo")
    lang = (j.get("language") or "").split("-")[0] or None
    manuais = list((j.get("subtitles") or {}).keys())
    autos = list((j.get("automatic_captions") or {}).keys())
    if not lang:  # sem idioma declarado: deduz da legenda automática "-orig"
        orig = [k for k in autos if k.endswith("-orig")]
        lang = orig[0].replace("-orig", "").split("-")[0] if orig else (v.get("idioma_busca") or "en")
    v["idioma"] = lang
    # candidatas, em ordem de preferência
    cands = []
    for k in manuais:
        if k.split("-")[0] == lang:
            cands.append(("legenda-manual", k, False))
    for k in (f"{lang}-orig", lang):
        if k in autos:
            cands.append(("legenda-auto", k, True))
    for fonte, k, auto in cands:
        for tent in range(3):
            base = os.path.join(tmp, "s")
            for f in os.listdir(tmp):
                os.remove(os.path.join(tmp, f))
            args = ["--skip-download", "--sub-format", "vtt", "--sub-langs", re.escape(k),
                    "-o", base + ".%(ext)s", v["url"]]
            args.insert(0, "--write-auto-subs" if auto else "--write-subs")
            r = ytdlp(args)
            vtts = [f for f in os.listdir(tmp) if f.endswith(".vtt")]
            if vtts:
                return os.path.join(tmp, vtts[0]), fonte, lang
            if "429" in (r.stderr or ""):
                print(f"  429 em {v['id']}, esperando 30 s...", file=sys.stderr)
                time.sleep(30)
            else:
                break
    return None, None, lang


def cmd_transcrever(a):
    caminho = os.path.join(a.saida_dir, "manada.json")
    lista = json.load(open(caminho, encoding="utf-8"))
    if a.ids:
        ids = [i.strip() for i in a.ids.split(",") if i.strip()]
        alvo = []
        for i in ids:
            v = next((x for x in lista if x["id"] == i), None)
            if not v:  # id fora do manada.json: cria entrada mínima
                v = {"id": i, "url": f"https://www.youtube.com/watch?v={i}", "titulo": None,
                     "canal": None, "views": None, "duracao_s": None, "data": None,
                     "idioma_busca": None}
                lista.append(v)
            alvo.append(v)
    else:
        alvo = lista[:a.top]
    for v in alvo:
        tmp = tempfile.mkdtemp(dir=TMPBASE)
        try:
            vtt, fonte, lang = _baixar_legenda(v, tmp)
            out = os.path.join(a.saida_dir, f"manada-{v['id']}.txt")
            if vtt:
                cab = (f"# {v['id']} | {v.get('canal')} | {v.get('titulo')} | "
                       f"{v.get('views')} views | {lang} | fonte: {fonte}")
                palavras = vtt2txt(vtt, out, cab)
            else:
                print(f"  sem legenda em {v['id']}: Whisper (lento)...", file=sys.stderr)
                fonte = "whisper"
                lang = lang or v.get("idioma_busca") or "en"
                tmp_out = os.path.join(tmp, "w.txt")
                r = subprocess.run([sys.executable, os.path.join(HERE, "transcrever.py"),
                                    v["id"], tmp_out, lang], capture_output=True, text=True,
                                   env={**os.environ, "TMPDIR": TMPBASE})
                if r.returncode != 0 or not os.path.exists(tmp_out):
                    print(f"! falhou {v['id']}: {r.stderr[-300:]}", file=sys.stderr)
                    v["fonte"] = "falhou"
                    continue
                corpo = open(tmp_out, encoding="utf-8").read()
                cab = (f"# {v['id']} | {v.get('canal')} | {v.get('titulo')} | "
                       f"{v.get('views')} views | {lang} | fonte: whisper")
                open(out, "w", encoding="utf-8").write(cab + "\n" + corpo)
                palavras = len(corpo.split())
            v.update({"txt": out, "fonte": fonte, "idioma": lang, "palavras": palavras})
            print(f"{v['id']} {v.get('canal')} | {lang} | {fonte} | {palavras} palavras")
        except Exception as e:  # um vídeo ruim não derruba o lote
            print(f"! erro {v['id']}: {e}", file=sys.stderr)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        json.dump(lista, open(caminho, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        time.sleep(4)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    s = p.add_subparsers(dest="cmd", required=True)
    b = s.add_parser("buscar")
    b.add_argument("saida_dir"); b.add_argument("termos", nargs="+")
    b.add_argument("--idioma", action="append", default=[]); b.add_argument("--por-termo", type=int, default=15)
    b.add_argument("--top", type=int, default=5); b.add_argument("--min-dur", type=int, default=300)
    b.add_argument("--max-dur", type=int, default=2400)
    t = s.add_parser("transcrever")
    t.add_argument("saida_dir"); t.add_argument("--ids"); t.add_argument("--top", type=int, default=5)
    c = s.add_parser("vtt2txt"); c.add_argument("vtt"); c.add_argument("saida")
    a = p.parse_args()
    if a.cmd == "buscar":
        a.idioma = a.idioma or ["pt"]
        cmd_buscar(a)
    elif a.cmd == "transcrever":
        cmd_transcrever(a)
    else:
        print(vtt2txt(a.vtt, a.saida), "palavras")


if __name__ == "__main__":
    main()
