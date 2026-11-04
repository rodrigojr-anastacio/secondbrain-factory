"""Gera as tabelas markdown do NOTAS.md a partir de dados/resumo_idiomas.json e dados/sugestoes.json (stdout)."""
import json, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(BASE, "dados/resumo_idiomas.json")))
S = json.load(open(os.path.join(BASE, "dados/sugestoes.json")))
NOME = {"kgb": "KGB", "cia": "CIA", "mossad": "Mossad", "stasi": "Stasi", "gestapo": "Gestapo", "ss": "SS", "mi6": "MI6", "fbi": "FBI", "mafia": "Máfia",
        "templarios": "Templários", "legiao": "Legião Estrangeira", "cartel": "Cartel"}
def k(n):
    if n >= 1_000_000: return f"{n/1e6:.2f} mi".replace(".", ",")
    if n >= 1000: return f"{n/1e3:.1f} mil".replace(".", ",")
    return str(n)
def cut(s, n=55): return (s or "")[:n].replace("|", "/")
print("## Comparativo geral [O]\n")
print("| Idioma | C4 mediana do top-1 | C4 mediana da mediana top-10 | C4 soma top-10 | C4 vídeos 2026 > 100 mil | C4 > 1 mi | Núcleo-7 mediana top-10 | Núcleo-7 2026 > 100 mil | 12 temas 2026 > 100 mil | > 1 mi | Autocomplete \"história da X\" (soma 8 orgs) | Canais do molde exato | Clones desde 09/2026 | Mediana dos clones | Molde com mediana > 5 mil |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for l, x in R.items():
    d, c = x["demanda"], x["concorrencia"]
    sug = sum((S[l][o]["n_hist"] or 0) for o in S[l] if not o.startswith("extra"))
    n7 = d["nucleo7_mediana_top10mediana"] if l in ("en", "es", "pt", "fr", "de", "it") else "—"
    n7a = d["nucleo7_ano_gt100k"] if l in ("en", "es", "pt", "fr", "de", "it") else "—"
    a12 = d["todos12_ano_gt100k"] if l in ("en", "es", "pt", "fr", "de", "it") else "—"
    a12m = d["todos12_ano_gt1m"] if l in ("en", "es", "pt", "fr", "de", "it") else "—"
    print(f"| {l} | {k(d['c4_mediana_top1'])} | {k(d['c4_mediana_top10mediana'])} | {k(d['c4_soma_top10'])} | {d['c4_ano_gt100k']} | {d['c4_ano_gt1m']} | "
          f"{k(n7) if n7 != '—' else n7} | {n7a} | {a12} | {a12m} | {sug} | {c['n_molde_exato']} | {c['n_clones_desde_09_2026']} | {c['mediana_das_medianas_formula_org_clones']} | {c['n_molde_exato_mediana_gt5k']} |")
for l, x in R.items():
    d, c = x["demanda"], x["concorrencia"]
    print(f"\n### TABELAS {l}\n")
    print("Demanda por tema [O] (vídeos ≥ 4 min no idioma, título original cita o tema; amostra das buscas, não o universo)\n")
    print("| Tema | Vídeos | Top-1 all-time | Mediana top-10 | Top-1 de 2026 | 2026 > 100 mil | 2026 > 1 mi | Top de 2026 (canal) |")
    print("|---|---|---|---|---|---|---|---|")
    for t, y in d["por_tema"].items():
        print(f"| {NOME[t]} | {y['n']} | {k(y['top1'])} | {k(y['top10_mediana'])} | {k(y['ano_top1'])} | {y['ano_gt100k']} | {y['ano_gt1m']} | {cut(y['ano_top1_titulo'], 50)} ({cut(y['ano_top1_canal'], 25)}) |")
    print(f"\nPaís dos canais (% das views do top-20 de cada tema) [O]: " + ", ".join(f"{p} {v}%" for p, v in d["paises_dos_canais_pct_views_top20"].items()))
    print("\nTeto (maiores canais no núcleo-7, outro formato) [O]: " + "; ".join(f"{t['canal']} ({t['pais'] or '?'}, {k(t['inscritos'] or 0)} inscritos)" for t in d["teto_canais"][:5]))
    print("\nConcorrência: molde exato (\"história INTEIRA/COMPLETA de <organização> em N minutos\", ≥ 40% dos vídeos na fórmula) [O]\n")
    if c["canais_molde_exato"]:
        print("| Canal | País | 1º vídeo | Vídeos | Inscritos | Mediana (fórmula+org) | Mediana longos ≥ 7 d | Melhor vídeo |")
        print("|---|---|---|---|---|---|---|---|")
        for r in c["canais_molde_exato"][:15]:
            ini = r["inicio"] + ("" if r["primeiro_video_confirmado"] else " (criação)")
            print(f"| [{cut(r['nome'], 30)}]({r['link']}) | {r['pais'] or '?'} | {ini} | {r['n_videos']} | {k(r['inscritos'])} | {k(r['mediana_formula_org'])} | {k(r['mediana_longos_7d'])} | {k(r['melhor']['views'])}: {cut(r['melhor']['titulo'], 50)} |")
        if len(c["canais_molde_exato"]) > 15: print(f"| … mais {len(c['canais_molde_exato']) - 15} canais (ver JSON) | | | | | | | |")
    else:
        print("Nenhum.")
    if c["formula_org_outro_molde"]:
        print("\nFórmula com organização, outro molde (sem \"N minutos\", para dormir, longo ou só 1 vídeo) [O]: " + "; ".join(
            f"{cut(r['nome'], 28)} ({r['pais'] or '?'}, {k(r['inscritos'])} insc.; {k(r['melhor']['views'])} em \"{cut(r['melhor']['titulo'], 45)}\")" for r in c["formula_org_outro_molde"][:6]))
    if c["formula_outros_temas_top"]:
        print("\nFórmula com outros temas (países, cidades, desenhos) [O]: " + "; ".join(
            f"{cut(r['nome'], 28)} ({r['inicio']}, mediana {k(r['mediana_longos'])}, melhor {k(r['melhor']['views'])})" for r in c["formula_outros_temas_top"][:5]))
