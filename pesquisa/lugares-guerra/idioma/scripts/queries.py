"""Definição das consultas (grupo, lang, tema, tipo, q, ordem). Grupos: conc (concorrência), dem (demanda en por tema), idi (idioma)."""
TEMAS_EN = {
 "iwo jima": "Iwo Jima", "midway": "Midway Atoll", "corregidor": "Corregidor", "tinian": "Tinian", "bikini": "Bikini Atoll",
 "hashima": "Hashima Battleship Island", "pearl harbor": "Pearl Harbor USS Arizona", "omaha": "Omaha Beach Normandy", "okinawa": "Okinawa battle",
 "peleliu": "Peleliu", "truk": "Truk Lagoon", "kwajalein": "Kwajalein", "wake": "Wake Island", "guadalcanal": "Guadalcanal",
 "alcatraz": "Alcatraz", "johnston": "Johnston Atoll", "diego garcia": "Diego Garcia", "area 51": "Area 51", "cheyenne": "Cheyenne Mountain",
 "camp century": "Camp Century Greenland", "runit": "Runit Dome Enewetak", "pointe du hoc": "Pointe du Hoc", "gettysburg": "Gettysburg",
 "antietam": "Antietam", "fort sumter": "Fort Sumter", "lincoln": "Lincoln assassination", "appomattox": "Appomattox", "andersonville": "Andersonville prison",
 "north brother": "North Brother Island", "fort jefferson": "Fort Jefferson Dry Tortugas", "bastogne": "Bastogne", "hiroshima": "Hiroshima",
 "chernobyl": "Chernobyl", "falklands": "Falklands minefields",
}
def conc():
    qs = []
    A = ["why can't you visit", "why you can't visit this island", "what's still under the water", "what's still buried at the battlefield", "what happened to the real",
         "why is america still digging up", "sealed since 1945", "the island nobody is allowed to visit", "off limits island WW2 today", "abandoned military base today documentary",
         "battlefield today what's left", "why is no one allowed on this island", "what's still inside the tunnels WW2", "why can't americans visit", "the forbidden island",
         "what the war left behind", "unexploded bombs still there today"]
    for q in A:
        qs += [("conc", "en", "a", "formula", q, "relevancia"), ("conc", "en", "a", "formula", q, "data")]
    B = ["Where They Stood", "why can't you visit iwo jima", "what's still at omaha beach", "why is america still digging up normandy", "japanese submarine alaska",
         "why can't you visit island WW2", "iwo jima sealed tunnels", "why can't you visit midway", "why can't you visit tinian"]
    for q in B: qs += [("conc", "en", "b_wts", "clone", q, "data"), ("conc", "en", "b_wts", "clone", q, "relevancia")]
    C = ["Civil War Fine Print", "the pictures of Lincoln's death you weren't supposed to see", "photos you weren't supposed to see", "history fine print documents telegram",
         "declassified documents history explained", "what happened to the man who hosted general lee's surrender", "the telegram that changed history", "civil war documents newspaper ads photographs",
         "civil war untold story documents", "the photograph they tried to hide history"]
    for q in C: qs += [("conc", "en", "b_cwfp", "clone", q, "data"), ("conc", "en", "b_cwfp", "clone", q, "relevancia")]
    D = ["mark felton", "simple history WW2", "the operations room", "yarnhub", "kings and generals", "atlas pro", "ww2 documentary pacific island", "cold war secret base documentary",
         "abandoned military bases", "american history documentary 20 minutes", "history channel pacific war island today", "forgotten battlefield documentary", "military history short documentary 2026",
         "WW2 history channel new 2026", "the history guy", "cold war history documentary 2026", "ghost island war ruins", "WW2 sites today"]
    for q in D: qs += [("conc", "en", "c", "nicho", q, "ano_views"), ("conc", "en", "c", "nicho", q, "relevancia")]
    return qs
def dem():
    qs = []
    for k, t in TEMAS_EN.items():
        qs.append(("dem", "en", k, "why", f"why can't you visit {t}", "relevancia"))
        qs.append(("dem", "en", k, "why", f"why can't you visit {t}", "ano_views"))
        qs.append(("dem", "en", k, "today", f"{t} today", "relevancia"))
        qs.append(("dem", "en", k, "doc", f"{t} documentary", "relevancia"))
        qs.append(("dem", "en", k, "doc", f"{t} documentary", "ano_views"))
    return qs
# idioma: temas nativos (5) + fórmula traduzida (3) + local (3)
IDI = {
 "en": dict(temas=["Iwo Jima", "Pearl Harbor", "Omaha Beach Normandy", "Hiroshima", "Area 51"], formula=["why can't you visit Iwo Jima", "what's still under Pearl Harbor", "why can't you visit Midway Atoll"], local=["Civil War Gettysburg documentary", "Lincoln assassination documentary", "Vietnam War battlefield today"]),
 "es": dict(temas=["Iwo Jima", "Pearl Harbor", "Playa Omaha Normandía", "Hiroshima", "Área 51"], formula=["¿por qué no puedes visitar Iwo Jima?", "qué hay todavía bajo Pearl Harbor", "por qué no se puede visitar la isla de Midway"], local=["islas Malvinas campos minados hoy", "Guerra Civil Española lugares abandonados hoy", "Guerra del Chaco documental"]),
 "pt": dict(temas=["Iwo Jima", "Pearl Harbor", "Praia de Omaha Normandia", "Hiroshima", "Área 51"], formula=["por que você não pode visitar Iwo Jima", "o que ainda existe embaixo de Pearl Harbor", "por que ninguém pode visitar a ilha de Midway"], local=["Monte Castelo FEB Itália hoje", "Guerra do Paraguai documentário", "Canudos guerra lugar hoje"]),
 "fr": dict(temas=["Iwo Jima", "Pearl Harbor", "plage d'Omaha Normandie", "Hiroshima", "Zone 51"], formula=["pourquoi on ne peut pas visiter Iwo Jima", "ce qu'il reste sous Pearl Harbor", "pourquoi l'île de Midway est interdite"], local=["Verdun champ de bataille aujourd'hui", "ligne Maginot aujourd'hui", "zone rouge Verdun interdite"]),
 "de": dict(temas=["Iwo Jima", "Pearl Harbor", "Omaha Beach Normandie", "Hiroshima", "Area 51"], formula=["Warum darf man Iwo Jima nicht besuchen", "was liegt noch unter Pearl Harbor", "Warum darf niemand die Insel Midway betreten"], local=["Atlantikwall heute Dokumentation", "Peenemünde Dokumentation", "Lost Places Zweiter Weltkrieg Bunker"]),
 "it": dict(temas=["Iwo Jima", "Pearl Harbor", "spiaggia di Omaha Normandia", "Hiroshima", "Area 51"], formula=["perché non si può visitare Iwo Jima", "cosa c'è ancora sotto Pearl Harbor"], local=["Linea Gotica oggi documentario"]),
 "ru": dict(temas=["Иводзима", "Перл-Харбор", "Нормандия Омаха", "Хиросима", "Зона 51"], formula=["почему нельзя посетить Иводзиму", "что осталось под Перл-Харбором"], local=[]),
 "pl": dict(temas=["Iwo Jima", "Pearl Harbor", "Normandia Omaha", "Hiroszima", "Strefa 51"], formula=["dlaczego nie można odwiedzić Iwo Jimy", "co zostało pod Pearl Harbor"], local=[]),
 "ja": dict(temas=["硫黄島", "真珠湾", "ノルマンディー オマハビーチ", "広島 原爆", "エリア51"], formula=["硫黄島 なぜ行けない", "真珠湾 今も残る"], local=[]),
 "tr": dict(temas=["Iwo Jima", "Pearl Harbor", "Normandiya Omaha", "Hiroşima"], formula=["Iwo Jima neden ziyaret edilemez"], local=[]),
}
def idi():
    qs = []
    for l, d in IDI.items():
        for t in d["temas"]:
            qs += [("idi", l, t, "tema", t, "relevancia"), ("idi", l, t, "tema", t, "ano_views")]
        for q in d["formula"]: qs += [("idi", l, "formula", "formula", q, "relevancia"), ("idi", l, "formula", "formula", q, "data")]
        for q in d["local"]: qs += [("idi", l, "local", "local", q, "relevancia")]
    return qs
