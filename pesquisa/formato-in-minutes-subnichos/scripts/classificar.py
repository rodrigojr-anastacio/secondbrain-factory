"""Classifica vídeos no formato por subnicho (palavra-chave no título) e por força do formato."""
import json, os, re, sys, datetime as dt
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, "scripts"))
STRICT = re.compile(r"(entire|complete|whole|full)\s+history\s+of|hist[óo]ria\s+(inteira|completa)\s+d|historia\s+(completa|entera)\s+de|toda\s+la\s+historia\s+de|histoire\s+(compl[èe]te|enti[èe]re)|toute\s+l.histoire|(gesamte|komplette|ganze)\s+geschichte", re.I)
MIN = re.compile(r"\b(in|em|en|in)\s+(\d+|just\s+\d+|ten|five)\s+(min|minutes|minutos|minuten)", re.I)
RISE = re.compile(r"rise\s+and\s+fall|ascens[ãa]o\s+e\s+queda|auge\s+y\s+ca[íi]da|ascension\s+et|aufstieg\s+und\s+fall", re.I)
KW = {
 "tecnologia": r"internet|apple\b|microsoft|google|iphone|computer|artificial intelligence|\bai\b|nvidia|smartphone|social media|tesla|spacex|intel\b|samsung|software|facebook|chatgpt|openai|tech|televis|telephone|radio\b|robot|electricity",
 "empresas_marcas": r"coca|mcdonald|nike|disney|lego|toyota|ferrari|ikea|amazon|walmart|pepsi|starbucks|rolex|adidas|company|brand|corporation|porsche|lamborghini|bmw|mercedes|ford\b|empresa|marca|kfc|burger king|netflix|sony|hermes|louis vuitton|gucci|nestl|heinz|kellogg|red bull|boeing|airbus",
 "financas_economia": r"money|stock market|bank|bitcoin|crypto|federal reserve|\bfed\b|inflation|econom|wall street|capitalism|dinheiro|dinero|argent|geld|gold\b|dollar|tax",
 "ciencia_espaco": r"universe|physics|chemistry|atom|nuclear|space race|nasa|evolution|earth\b|planet|mathemat|astronomy|science|ci[êe]ncia|science|dinosaur|life on|moon|mars|sun\b|universo|univers\b|black hole|ice age|humans|homo sapiens|climate",
 "medicina_saude": r"medicine|surgery|vaccin|black death|plague|pandemic|anesthes|dentist|psychiatr|pharma|cancer|disease|doctor|hospital|virus|medicina|m[ée]decine|drug\b|opioid|smallpox|insulin|antibiotic",
 "crime_mafia": r"mafia|cartel|yakuza|serial killer|fbi\b|alcatraz|escobar|pirac|pirate|organized crime|prison|gang|crime|chapo|cosa nostra|mob\b|heist|narco|triad|hells angels|scam|ponzi",
 "esportes": r"football|soccer|\bnba\b|olympic|world cup|boxing|\bufc\b|formula 1|\bf1\b|wrestling|real madrid|barcelona|\bnfl\b|tennis|futebol|f[úu]tbol|basketball|baseball|\bmlb\b|nhl|hockey|golf|chess|copa|messi|ronaldo|wwe|champions league|premier league|cricket|sport|esporte|deporte",
 "religioes": r"christian|islam|buddh|judaism|catholic|vatican|pope|mormon|templar|bible|hindu|freemason|jesus|church|religi|igreja|iglesia|[ée]glise|quran|muhammad|jews|protestant|orthodox|satan|devil|angels|god\b|deus|dios",
 "cidades": r"new york|london|paris|istanbul|tokyo|las vegas|berlin|venice|jerusalem|constantinople|dubai|rio de janeiro|city|cidade|ciudad|ville\b|stadt|chicago|los angeles|moscow|rome\b|roma\b|singapore|hong kong|amsterdam|babylon|athens|s[ãa]o paulo|mexico city|cairo",
 "comida_bebida": r"pizza|coffee|sugar|chocolate|beer|sushi|bread|\bsalt\b|wine|spice|fast food|food|caf[ée]|comida|cuisine|whisk|vodka|tea\b|burger|cheese|pasta|ramen|rice|cerveja|cerveza",
 "guerras_especificas": r"vietnam war|world war|\bww1\b|\bww2\b|\bwwi\b|korean war|hundred years|napoleon|crusade|civil war|falklands|thirty years|gulf war|afghan|samurai|\bwar\b|guerra|guerre|krieg|battle|batalha|vikings|knights|spartan|army|navy|wwii",
 "games": r"video game|nintendo|minecraft|\bgta\b|pokemon|pok[ée]mon|playstation|call of duty|xbox|sega|fortnite|warcraft|mario|zelda|sonic|halo|roblox|gaming|game|elden|dark souls|final fantasy|resident evil|fnaf|five nights|league of legends|counter-strike|valve|steam",
 "musica": r"rock|hip hop|hip-hop|metal|beatles|jazz|k-pop|kpop|punk|\brap\b|eminem|michael jackson|music|m[úu]sica|musique|musik|band\b|queen\b|elvis|nirvana|taylor swift|drake|kanye|2pac|tupac|beyonc|guitar|disco|funk|samba|reggae",
 "transporte_engenharia": r"aviation|\bcars?\b|train|titanic|\bships?\b|boeing|skyscraper|submarine|tank|airplane|plane|railway|aircraft|automobil|engine|rocket|bridge",
 "mitologia_lendas": r"mytholog|vampire|illuminati|witch|zeus|odin|thor|gods\b|legend|ghost|demon|dragon|atlantis|bigfoot|alien|ufo|conspirac|mitolog",
 "cultura_pop_midia": r"marvel|dc comics|\bdc\b|star wars|anime|hollywood|simpsons|youtube|meme|pixar|spider-man|batman|superman|x-men|naruto|one piece|dragon ball|harry potter|lord of the rings|tolkien|godzilla|cartoon|comics|movie|film|tv show|sitcom|sesame|barbie|mtv|wrestl|tiktok|twitter|reddit|4chan|mrbeast|lore",
 "dinastias_familias": r"rothschild|medici|kennedy|habsburg|royal family|dynasty|dinastia|tudor|romanov|windsor|borgia|family",
}
MANADA = r"empire|kingdom|country|nation|\bkgb\b|\bcia\b|mossad|gestapo|\bss\b|\bmi6\b|stasi|nazi|soviet|ussr|reich|regime|dictator|china|india|russia|japan|egypt|iran|israel|korea|germany|france|britain|england|spain|portugal|brazil|brasil|mexico|ottoman|roman|persia|mongol|byzant|aztec|inca|maya|usa|america|united states|ukraine|poland|italy|greece|turkey|africa|europe|pakistan|ireland|scotland|canada|australia|vietnam\b|cuba|argentina|colombia|venezuela|chile|peru|hitler|stalin|lenin|mao\b|kim jong|north korea|sparta|rome\b|carthag|imp[ée]rio|imperio|empire|pa[íi]s|pays|reino|royaume"
def classificar(t):
    tl = t.lower()
    subs = [s for s, rx in KW.items() if re.search(rx, tl)]
    return subs
def forca(t):
    s, m, r = bool(STRICT.search(t)), bool(MIN.search(t)), bool(RISE.search(t))
    if s and m: return "alto"
    if s or (r and m): return "medio"
    if r or m: return "baixo"
    return "nenhum"
if __name__ == "__main__":
    vids = json.load(open(os.path.join(BASE, "dados/videos_formato.json")))
    hoje = dt.datetime(2026, 11, 4, tzinfo=dt.timezone.utc)
    for v in vids:
        v["subnichos"] = classificar(v["title"]); v["forca_titulo"] = forca(v["title"])
        v["manada"] = bool(re.search(MANADA, v["title"].lower()))
        if v.get("publicado"):
            v["idade_dias"] = (hoje - dt.datetime.fromisoformat(v["publicado"].replace("Z", "+00:00"))).days
    json.dump(vids, open(os.path.join(BASE, "dados/videos_formato.json"), "w"), ensure_ascii=False, indent=0)
    import collections
    c = collections.Counter(); c2 = collections.Counter()
    for v in vids:
        if v["forca_titulo"] in ("alto", "medio") and (v.get("views") or 0) >= 100_000 and (v.get("dur_s") or 0) >= 240:
            for s in v["subnichos"] or ["?"]: c[s] += 1
            if (v.get("idade_dias") or 9999) <= 365:
                for s in v["subnichos"] or ["?"]: c2[s] += 1
    print("≥100k views, título forte/médio, ≥4 min (todas as idades):", c.most_common())
    print("idem, publicados nos últimos 365 dias:", c2.most_common())
