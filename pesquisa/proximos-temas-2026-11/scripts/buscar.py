"""Busca yt-dlp via WARP (0 cota) dos temas candidatos em pt (historia-ptbr) e es (dossie-es).
Cada consulta em 2 ordens: relevância (ytsearch40) e 'este ano por views' (sp=CAMSAggF). Saída: dados/busca.jsonl"""
import json, os, sys, subprocess, urllib.parse
from concurrent.futures import ThreadPoolExecutor
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
YTDLP = os.path.expanduser("~/workspace/fabrica-youtube/tools/.venv/bin/yt-dlp")
PT = {
 "roma": ["história de roma", "história do império romano", "a história inteira de roma", "história completa do império romano"],
 "japao": ["história do japão", "a história inteira do japão", "história completa do japão"],
 "russia": ["história da rússia", "a história inteira da rússia", "história completa da rússia"],
 "ucrania": ["história da ucrânia", "a história inteira da ucrânia", "história completa da ucrânia"],
 "britanico": ["história do império britânico", "a história inteira da inglaterra", "história completa do reino unido"],
 "grecia": ["história da grécia", "a história inteira da grécia antiga", "história completa da grécia"],
 "otomano": ["história do império otomano", "a história inteira do império otomano", "história completa da turquia"],
 "portugal": ["história de portugal", "a história inteira de portugal", "história completa de portugal"],
 "eua": ["história dos estados unidos", "a história inteira dos estados unidos", "história completa dos eua"],
 "mongois": ["história do império mongol", "a história inteira dos mongóis", "história completa de genghis khan"],
 "israel": ["história de israel", "a história inteira de israel", "história completa de israel e palestina"],
 "alemanha": ["história da alemanha", "a história inteira da alemanha", "história completa da alemanha"],
 "franca": ["história da frança", "a história inteira da frança"],
 "espanha": ["história da espanha", "a história inteira da espanha"],
 "coreia": ["história da coreia", "a história inteira da coreia do norte", "história completa da coreia"],
 "mexico": ["história do méxico", "a história inteira dos astecas", "história completa dos maias"],
 "argentina": ["história da argentina", "a história inteira da argentina"],
 "bizancio": ["história do império bizantino", "a história inteira de bizâncio"],
 "vikings": ["história dos vikings", "a história inteira dos vikings"],
 "mesopotamia": ["história da mesopotâmia", "a história inteira da mesopotâmia"],
 "incas": ["história dos incas", "a história inteira dos incas"],
 "italia": ["história da itália", "a história inteira da itália"],
 "cartago": ["história de cartago", "a história inteira de cartago"],
 "africa": ["história da áfrica", "a história inteira da áfrica"],
}
ES = {
 "kgb": ["historia de la kgb", "toda la historia de la kgb", "la kgb documental"],
 "templarios": ["historia de los templarios", "toda la historia de los templarios", "templarios documental"],
 "inquisicion": ["historia de la inquisición", "toda la historia de la inquisición española", "santa inquisición documental"],
 "masoneria": ["historia de la masonería", "toda la historia de la masonería", "masones documental"],
 "jesuitas": ["historia de los jesuitas", "toda la historia de los jesuitas", "jesuitas documental"],
 "condor": ["operación cóndor historia", "plan cóndor documental", "toda la historia del plan cóndor"],
 "illuminati": ["historia de los illuminati", "illuminati documental historia"],
 "opusdei": ["historia del opus dei", "opus dei documental"],
 "yakuza": ["historia de la yakuza", "yakuza documental"],
 "asesinos": ["la orden de los asesinos historia", "hashashin historia", "secta de los asesinos alamut"],
 "guardiasuiza": ["historia de la guardia suiza", "guardia suiza vaticano documental"],
 "mafiarusa": ["historia de la mafia rusa", "bratva mafia rusa documental"],
 "stasi": ["historia de la stasi", "stasi documental"],
 "gestapo": ["historia de la gestapo"],
 "ss": ["historia de las ss nazis"],
 "kkk": ["historia del ku klux klan", "ku klux klan documental"],
 "eta": ["historia de eta", "eta documental"],
 "hospitalarios": ["historia de la orden de malta", "caballeros hospitalarios historia"],
 "navyseals": ["historia de los navy seals", "fuerzas especiales historia sas"],
 "pinkerton": ["historia de la agencia pinkerton"],
 "camorra": ["historia de la camorra", "ndrangheta documental"],
 "triadas": ["historia de las triadas chinas"],
 "dina": ["historia de la dina chile", "dina pinochet documental"],
 "spetsnaz": ["historia de los spetsnaz", "historia del nkvd"],
 "vaticano": ["servicio secreto del vaticano", "historia de la entidad vaticano espías"],
 "legion": ["historia de la legión extranjera francesa"],
 "rosacruces": ["historia de los rosacruces"],
 "sicarios": ["historia de los sicarios medievales", "historia de los ninjas"],
}
def rodar(item):
    lang, tema, q, ordem = item
    alvo = f"ytsearch40:{q}" if ordem == "relevancia" else "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&sp=CAMSAggF"
    for _ in range(2):
        r = subprocess.run([YTDLP, "--proxy", "socks5://127.0.0.1:40000", "--flat-playlist", "-J", "--playlist-end", "40", alvo], capture_output=True, text=True, timeout=180)
        if not r.returncode: break
    if r.returncode: return item, None
    return item, [{k: e.get(k) for k in ("id", "title", "channel", "channel_id", "view_count", "duration")} for e in json.loads(r.stdout).get("entries") or []]
qs = [("pt", t, q, o) for t, l in PT.items() for q in l for o in ("relevancia", "ano_views")] + \
     [("es", t, q, o) for t, l in ES.items() for q in l for o in ("relevancia", "ano_views")]
print(len(qs), "consultas", file=sys.stderr)
erros = 0
with open(os.path.join(BASE, "dados/busca.jsonl"), "w") as f, ThreadPoolExecutor(4) as ex:
    for (l, t, q, o), vs in ex.map(rodar, qs):
        if vs is None: erros += 1; print("ERRO", q, o, file=sys.stderr); continue
        for i, v in enumerate(vs): f.write(json.dumps({"lang": l, "tema": t, "q": q, "ordem": o, "pos": i, **v}, ensure_ascii=False) + "\n")
print("erros", erros, file=sys.stderr)
