#!/usr/bin/env python3
"""Amostras de voz v2 do 003 (Fish Audio, clone do historia-ptbr), com custo registrado em financas.consumo.

Uso (de qualquer pasta):
  ~/workspace/fabrica-youtube/tools/.venv/bin/python gerar.py <arquivo_texto> <saida.mp3> --modelo <m>
        [--tecnica bloco|paragrafo|unico] [--direcao "[...]"] [--pausa-tag "[pause]"] [--pausa-tag-curta "[short pause]"] [--sem-tags]
        [--velocidade 1.0] [--temperature 0.7] [--top-p 0.7] [--language pt-BR] [--extra '{"chave": valor}']
        [--gap 0.35] [--gap-ideia 0.9] [--video 5] [--take 1]

Texto: parágrafos separados por linha em branco (um bloco por parágrafo); linhas que começam com "#" são comentário.
  Parágrafo que começa com "§ " abre ideia nova (gap --gap-ideia antes dele; os outros levam --gap).
  As tags [..] do texto vão para a API como estão (s2.1-pro e drama-3 usam a mesma sintaxe de colchetes;
  o drama-3 aceita também pares <emphasis>…</emphasis>, <slow>, <soft>, <whisper>, <stress>, <fast>, <forceful>).
Técnicas:
  bloco      1 chamada por parágrafo; aparo o silêncio e junto com --gap / --gap-ideia (técnica "A" do 003).
  paragrafo  1 chamada por ideia (junta os parágrafos até o próximo "§"); --gap-ideia entre ideias.
  unico      1 chamada com o trecho todo (o Fish corta em chunks e condiciona no anterior);
             antes de parágrafo com § entra --pausa-tag e entre os outros --pausa-tag-curta (padrão: nada;
             ex.: "[pause]" / "[short pause]" no drama-3). Parágrafos vão separados por quebra de linha.
--direcao: texto (ex.: "[contando uma lenda, calmo e curioso]") posto no início de cada chamada (no unico, só no início).
Cache: <saida>.partes/<hash>.mp3 (rodar de novo com o mesmo texto e parâmetros não cobra); --take N força nova tomada.
Saída: <saida.mp3> (192 kbps, 44,1 kHz mono) + <saida>.json (parâmetros, chamadas, bytes, custo).
Custo: bytes UTF-8 enviados × preço do modelo; 1 linha em financas.consumo (ref_tipo 'youtube.video', ref_id --video,
notas 'v2 amostras voz'). Também mostra o crédito do Fish antes/depois (GET /wallet/self/api-credit), que confirma
o modelo cobrado (o Fish NÃO dá erro com header de modelo errado: cai em s2.1-pro calado).
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

import numpy as np

TOOLS = Path(__file__).resolve().parents[6] / "tools"
sys.path.insert(0, str(TOOLS))
from tts_fish import chave, ler, aparar, SR  # noqa: E402  (só leitura; não altera o tts_fish.py)
from db import tentar  # noqa: E402

VOZ = "48613fc675f84984981683d92266e543"  # clone do historia-ptbr (canal.yaml)
PROMO_DRAMA3_ATE = dt.datetime(2026, 11, 12, 17, 0, tzinfo=dt.timezone.utc)


def preco(modelo):
    """US$ por milhão de bytes UTF-8 (docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits, 04/11/2026)."""
    if modelo == "drama-3":
        return 10.0 if dt.datetime.now(dt.timezone.utc) < PROMO_DRAMA3_ATE else 50.0
    tabela = {"s2.1-pro": 15.0, "s2-pro": 15.0, "s2.1-pro-free": 0.0}
    if modelo not in tabela:
        sys.exit(f"Modelo {modelo!r} sem preço cadastrado (e o Fish cairia calado em s2.1-pro). Válidos: drama-3, {', '.join(tabela)}")
    return tabela[modelo]


def ler_texto(arq):
    linhas = [l for l in open(arq, encoding="utf-8").read().splitlines() if not l.lstrip().startswith("#")]
    pars = [p.strip() for p in re.split(r"\n\s*\n", "\n".join(linhas)) if p.strip()]
    out = []
    for i, p in enumerate(pars):
        ideia = p.startswith("§")
        out.append({"texto": " ".join(p.lstrip("§").split()), "ideia": ideia and i > 0})
    return out


TAG = re.compile(r"\[[^\]]*\]\s*")


def credito(key):
    try:
        r = urllib.request.urlopen(urllib.request.Request("https://api.fish.audio/wallet/self/api-credit",
                                                          headers={"Authorization": f"Bearer {key}"}), timeout=30)
        return float(json.loads(r.read())["credit"])
    except Exception:
        return None


def tts(key, modelo, texto, destino, corpo_extra):
    corpo = {"text": texto, "reference_id": VOZ, "format": "mp3", "mp3_bitrate": 192}
    corpo.update(corpo_extra)
    req = urllib.request.Request("https://api.fish.audio/v1/tts", data=json.dumps(corpo).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "model": modelo})
    with urllib.request.urlopen(req, timeout=600) as r:
        dados = r.read()
    Path(destino).write_bytes(dados)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("texto")
    ap.add_argument("saida")
    ap.add_argument("--modelo", required=True)
    ap.add_argument("--tecnica", choices=["bloco", "paragrafo", "unico"], default="bloco")
    ap.add_argument("--direcao", default="", help='direção posta no início de cada chamada, ex.: "[calmo, contando uma lenda]"')
    ap.add_argument("--pausa-tag", default="", help='no unico: tag antes de parágrafo com § (ex.: "[pause]")')
    ap.add_argument("--pausa-tag-curta", default="", help='no unico/paragrafo: tag entre parágrafos do mesmo assunto (ex.: "[short pause]")')
    ap.add_argument("--sem-tags", action="store_true", help="remove as tags [..] do texto")
    ap.add_argument("--velocidade", type=float, default=1.0)
    ap.add_argument("--temperature", type=float)
    ap.add_argument("--top-p", type=float)
    ap.add_argument("--language", help="BCP-47 só para normalização (ex.: pt-BR)")
    ap.add_argument("--extra", default="{}", help="JSON com outros campos da API (ex.: '{\"condition_on_previous_chunks\": true}')")
    ap.add_argument("--gap", type=float, default=0.35, help="s entre parágrafos do mesmo assunto")
    ap.add_argument("--gap-ideia", type=float, default=0.9, help="s antes de parágrafo com §")
    ap.add_argument("--video", type=int, default=5)
    ap.add_argument("--take", type=int, default=1)
    a = ap.parse_args()

    pr = preco(a.modelo)
    pars = ler_texto(a.texto)
    if a.sem_tags:
        for p in pars:
            p["texto"] = TAG.sub("", p["texto"]).strip()
    sep = f" {a.pausa_tag_curta} " if a.pausa_tag_curta else " "
    # chamadas: (texto, gap_antes)
    if a.tecnica == "bloco":
        chamadas = [(p["texto"], (a.gap_ideia if p["ideia"] else a.gap) if i else 0.0) for i, p in enumerate(pars)]
    elif a.tecnica == "paragrafo":
        grupos = []
        for p in pars:
            if not grupos or p["ideia"]:
                grupos.append([])
            grupos[-1].append(p["texto"])
        chamadas = [(sep.join(g), a.gap_ideia if i else 0.0) for i, g in enumerate(grupos)]
    else:
        txt = ""
        for i, p in enumerate(pars):
            tag = a.pausa_tag if p["ideia"] else a.pausa_tag_curta
            txt += ((("\n\n" if p["ideia"] else "\n") + (f"{tag} " if tag else "")) if i else "") + p["texto"]
        chamadas = [(txt, 0.0)]
    if a.direcao:
        chamadas = [(f"{a.direcao} {t}", g) for t, g in chamadas]

    corpo_extra = json.loads(a.extra)
    if a.velocidade != 1.0:
        corpo_extra.setdefault("prosody", {})["speed"] = a.velocidade
    for k, v in (("temperature", a.temperature), ("top_p", a.top_p), ("language", a.language)):
        if v is not None:
            corpo_extra[k] = v

    saida = Path(a.saida).resolve()
    cache = saida.with_suffix(".partes")
    cache.mkdir(parents=True, exist_ok=True)
    key = chave()
    cred0 = credito(key)
    total_bytes, registro, partes = 0, [], []
    try:
        for i, (t, gap) in enumerate(chamadas):
            h = hashlib.sha1(json.dumps([a.modelo, VOZ, corpo_extra, t, a.take], sort_keys=True).encode()).hexdigest()[:12]
            mp3 = cache / f"{i:02d}-{h}.mp3"
            novo = not mp3.exists()
            if novo:
                tts(key, a.modelo, t, mp3, corpo_extra)
                total_bytes += len(t.encode("utf-8"))
            x = ler(str(mp3))
            if a.tecnica != "unico":
                x = aparar(x)
            partes += ([np.zeros(int(gap * SR), dtype=np.float32)] if gap else []) + [x]
            registro.append({"texto": t, "gap_antes_s": gap, "mp3": mp3.name, "gerado_agora": novo, "dur_s": round(len(x) / SR, 2)})
            print(f"{i:02d} {'gerado' if novo else 'cache '} {len(x) / SR:5.1f} s  {t[:70]}")
    finally:
        custo = total_bytes * pr / 1e6
        if total_bytes:
            def reg(con):
                c = con.execute("SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor='Fish Audio'").fetchone()
                con.execute(
                    "INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)"
                    " VALUES ('youtube', 'historia-ptbr', 'Fish Audio', %s, %s, 'bytes', %s, 'USD', %s, 'youtube.video', %s, 'v2 amostras voz')",
                    (f"tts {a.modelo}", total_bytes, custo, custo * float(c[0]) if c else None, a.video))
            tentar(reg)
        print(f"\n{total_bytes} bytes novos · US$ {custo:.4f} ({a.modelo}, US$ {pr:g}/M bytes)"
              + (" · registrado em financas.consumo" if total_bytes else " · nada cobrado (cache)"))

    y = np.concatenate([np.zeros(int(0.25 * SR), dtype=np.float32)] + partes + [np.zeros(int(0.5 * SR), dtype=np.float32)])
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "pipe:0",
                    "-b:a", "192k", str(saida)], input=y.astype(np.float32).tobytes(), check=True)
    cred1 = credito(key)
    info = {"saida": saida.name, "texto": os.path.basename(a.texto), "modelo": a.modelo, "voz": VOZ, "tecnica": a.tecnica,
            "direcao": a.direcao, "pausa_tag": a.pausa_tag, "pausa_tag_curta": a.pausa_tag_curta, "sem_tags": a.sem_tags, "api_extra": corpo_extra,
            "gap": a.gap, "gap_ideia": a.gap_ideia, "take": a.take, "dur_s": round(len(y) / SR, 1),
            "bytes_novos": total_bytes, "custo_usd": round(custo, 5), "preco_por_mi_bytes": pr,
            "credito_fish_antes": cred0, "credito_fish_depois": cred1, "gerado_em": dt.datetime.now().isoformat(timespec="seconds"),
            "chamadas": registro}
    json.dump(info, open(saida.with_suffix(".json"), "w"), ensure_ascii=False, indent=1)
    print(f"→ {saida} ({len(y) / SR:.1f} s)" + (f" · crédito Fish {cred0:.6f} → {cred1:.6f} (pode atrasar)" if cred0 and cred1 else ""))


if __name__ == "__main__":
    main()
