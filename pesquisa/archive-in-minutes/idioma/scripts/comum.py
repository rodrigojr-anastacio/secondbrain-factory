"""Classificadores compartilhados: idioma do vídeo, tema (organização) e fórmula no título."""
import re
TEMA_RE = {
 "kgb": re.compile(r"\bkgb\b|кгб|كي جي بي|केजीबी", re.I),
 "cia": re.compile(r"\bCIA\b|\bC\.I\.A\b|ЦРУ|цру|سي آي إيه|المخابرات المركزية"),
 "mossad": re.compile(r"mossad|mosad|моссад|موساد|モサド|मोसाद", re.I),
 "stasi": re.compile(r"(?<!alberto )\bstasi\b|штази|シュタージ|شتازي", re.I),
 "gestapo": re.compile(r"gestapo|гестапо|ゲシュタポ|جستابو|غيستابو|गेस्टापो", re.I),
 "ss": re.compile(r"\bSS\b|schutzstaffel|waffen[- ]?ss|\bСС\b"),
 "mi6": re.compile(r"\bmi[- ]?6\b|ми-?6", re.I),
 "fbi": re.compile(r"\bfbi\b|фбр|إف بي آي", re.I),
 "mafia": re.compile(r"mafia|mafie|mafya|cosa nostra|camorra|ndrangheta|мафи|مافيا|マフィア|माफिया", re.I),
 "templarios": re.compile(r"templ[aáeiá]r|templier|templer|тамплиер|tapınak şövalye|فرسان الهيكل|テンプル騎士", re.I),
 "legiao": re.compile(r"l[eé]gi\w* (extranjera|estrangeira|étrangère|etrangere|straniera)|foreign legion|fremdenlegion|legia cudzoziemska|иностранн\w* легион", re.I),
 "cartel": re.compile(r"c[aá]rtel|kartell|kartel|картел|narco", re.I),
}
FORMULA_RE = {
 "en": re.compile(r"\b(entire|complete|whole) history\b", re.I),
 "es": re.compile(r"toda la historia|historia completa|historia entera|historia entera", re.I),
 "pt": re.compile(r"hist[óo]ria (inteira|completa)|toda a hist[óo]ria", re.I),
 "fr": re.compile(r"toute l['’ ]histoire|histoire compl[èe]te|histoire enti[èe]re", re.I),
 "de": re.compile(r"(ganze|komplette|gesamte|vollständige) geschichte", re.I),
 "it": re.compile(r"tutta la storia|storia completa|intera storia|storia intera", re.I),
 "ru": re.compile(r"вся история|полная история", re.I),
 "tr": re.compile(r"tüm tarihi|bütün tarihi|tam tarihi", re.I),
 "pl": re.compile(r"cała historia|pełna historia", re.I),
 "hi": re.compile(r"complete history|पूरा इतिहास|सम्पूर्ण इतिहास|संपूर्ण इतिहास", re.I),
 "ja": re.compile(r"全歴史|完全解説"), "ar": re.compile(r"التاريخ الكامل|تاريخ .* كامل"),
}
MIN_RE = re.compile(r"\d+\s*(minutes?|minutos?|minuten|minuti|minut\w*|min\b|минут\w*|dakika\w*|分|मिनट|دقيقة|دقائق)", re.I)
SW = {
 "en": [" the ", " of ", " and ", "history", " how ", " why ", " what ", " was ", " who ", " secret"],
 "es": ["historia", " el ", " los ", " las ", " del ", "qué", "cómo", "ñ", " por ", " y ", " una ", " más ", "ción"],
 "pt": ["história", " da ", " do ", " dos ", " das ", "ã", "õ", "ç", " não ", " uma ", " em ", " e ", "ção"],
 "fr": ["histoire", " le ", " les ", " du ", " des ", "l'", "l’", " à ", " et ", " une ", " est ", "è", " qui "],
 "de": ["geschichte", " der ", " die ", " das ", " und ", "ü", "ö", "ä", "ß", " ein", " wie ", " ist "],
 "it": ["storia", " della ", " dei ", " delle ", " il ", "perché", " gli ", " di ", " è ", " una ", "zione"],
 "pl": ["historia", " i ", "ł", "ś", "ż", "ą", "ę", " jak ", " nie ", " się "],
 "tr": ["tarih", "ı", "ş", "ğ", " ve ", " bir ", "nın", "nin"],
}
def idioma(v):
    a = (v.get("audio") or v.get("lang") or "")[:2].lower()
    if a and a != "zx": return a
    t = " " + v["titulo"].lower() + " "
    if re.search(r"[Ѐ-ӿ]", t): return "ru"
    if re.search(r"[؀-ۿ]", t): return "ar"
    if re.search(r"[ऀ-ॿ]", t) or " hindi" in t: return "hi"
    if re.search(r"[぀-ヿ]", t): return "ja"
    sc = {k: sum(t.count(w) for w in ws) for k, ws in SW.items()}
    k, s = max(sc.items(), key=lambda x: x[1])
    return k if s > 0 else None
def temas(titulo):
    return [k for k, r in TEMA_RE.items() if r.search(titulo)]
def formula(titulo, lang):
    r = FORMULA_RE.get(lang)
    return bool(r and r.search(titulo))
def em_minutos(titulo):
    return bool(MIN_RE.search(titulo))

FICCAO_RE = re.compile(r"garlasco|chiara poggi|sempio|pel[íi]cula|\bfilme\b|\bmovie\b|film complet|\bresumen\b|\brecap|\bdrama\b|novela|temporada|\bdvd\b|\bm[úu]sic|\blyrics\b|\bletra\b|trailer|gameplay|\bjuego\b|\bjogo\b|\bgame\b|reaction|\breact\b|resumo do filme|filmes?\b|cinema|\bpart(ie)? \d+ du film|fiction|\bgta\b|minecraft|roblox|anime", re.I)
NUCLEO = ["kgb", "cia", "mossad", "stasi", "gestapo", "ss", "mi6"]
def ficcao(titulo, canal=""):
    return bool(FICCAO_RE.search(titulo) or FICCAO_RE.search(canal or ""))
