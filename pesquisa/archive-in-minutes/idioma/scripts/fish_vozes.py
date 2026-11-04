"""Lista vozes públicas do Fish Audio por idioma (GET /model). Não imprime a chave.
Uso: tools/.venv/bin/python -I pesquisa/archive-in-minutes/idioma/scripts/fish_vozes.py <idioma> [busca] > saida.json"""
import json, os, sys, urllib.parse, urllib.request
key = next(l.split("=", 1)[1].strip() for l in open(os.path.expanduser("~/.segredos/fish.env")) if l.startswith("FISH_API_KEY="))
lang = sys.argv[1]; titulo = sys.argv[2] if len(sys.argv) > 2 else ""
out = []
for sort in ("task_count", "score"):
    q = urllib.parse.urlencode({"page_size": 40, "page_number": 1, "language": lang, "sort_by": sort, "title": titulo})
    req = urllib.request.Request(f"https://api.fish.audio/model?{q}", headers={"Authorization": f"Bearer {key}"})
    for it in json.load(urllib.request.urlopen(req, timeout=60)).get("items", []):
        out.append({"id": it["_id"], "titulo": it.get("title"), "langs": it.get("languages"), "tags": it.get("tags"),
                    "usos": it.get("task_count"), "likes": it.get("like_count"), "desc": (it.get("description") or "")[:160],
                    "amostra": [s.get("audio") for s in (it.get("samples") or [])][:1], "visib": it.get("visibility")})
uniq = {o["id"]: o for o in out}
json.dump(list(uniq.values()), sys.stdout, ensure_ascii=False, indent=1)
