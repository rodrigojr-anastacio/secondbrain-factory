#!/usr/bin/env python
"""Gera a secao "Itens-chave por tema" do MATERIAL.md a partir de material.json (itens automaticos filtrados)
+ itens notaveis conferidos a mao (IDs do Internet Archive verificados na busca de 12/11/2026).
Uso: tools/.venv/bin/python -I .../secao_temas.py > /tmp/secao.md
"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = json.load(open(os.path.join(BASE, "material.json")))

RUIDO = ["USS Iwo Jima", "USS Gettysburg", "USS Antietam", "USS Peleliu", "USS Corregidor", "Truck", "truck", "NFL", "Grand Princess",
         "Home Movie", "Storms", "Coastal Area 51", "Overlay indexes", "Butterflyfish", "Senior Enlisted", "RIMPAC", "C130 AIRCRAFT",
         "Kiev", "Ptarmigan", "Picnic", "Melissa Hill", "Stevenson Photo", "Loran", "WHPO-", "Records Transfer", "Army-Navy Screen",
         "News Of The Day", "170th Anniversary", "Phal Family", "Tom Mooney", "THOMAS", "Joseph Whitney", "Appomattox Manor",
         "ALERT PRESENTATION", "reenactme", "Prinz Eugen", "Featured Document", "Pfc. Ira", "We All Came Home", "Andersonville Landing",
         "Fort |", "Antietam Bridge", "Pennsylvania, Gettysburg", "Lager-Nordhausen", "Caroline Islands", "Midway Atoll beach",
         "Captain Thomas C. Evans", "Damage Control Drill", "Wake Island Avengers", "Quiet on Kwajalein", "H-052-1", "CMC speaks",
         "Diego Garcia combat", "Combined and joint", "News Parade of the Year", "MacArthur Returns", "Bunkers - Trinity", "Hanford Plant",
         "Fighting Lady\" Outtakes", "Aerial View of Wake"]

ATUAL = {  # existe material ATUAL livre do lugar? (fonte principal)
    "iwo-jima": "sim: DVIDS (cerimonias anuais Reunion of Honor, USMC), GSI Japao (PDL 1.0, credito)",
    "midway": "sim: USFWS (PD) + DVIDS + ISS/NASA; acesso civil fechado = imagens de governo sao quase as unicas",
    "corregidor": "parcial: DVIDS raro (Balikatan); o resto e CC BY / CC BY-SA no Commons",
    "tinian": "sim: DVIDS forte (Forager, Cope North, North Field, poco da bomba)",
    "bikini": "fraco: Landsat (PD), relatorio NPS 1991 dos naufragios (PD); fotos de mergulho atuais sao CC BY-SA/privadas",
    "enewetak": "parcial: DOE/LLNL (Runit Dome), Landsat; DVIDS raro",
    "kwajalein": "sim: DVIDS (Reagan Test Site, US Army Garrison Kwajalein)",
    "johnston": "parcial: USFWS (refugio), DoD/JACADS; pouco recente",
    "wake": "parcial: DVIDS (USAF/PACAF), USFWS; base fechada",
    "truk": "fraco: NOAA/NPS esparso; mergulho = privado",
    "peleliu": "sim: DVIDS (DPAA, obras do porto 2020s)",
    "guadalcanal": "sim: DVIDS (DPAA, aniversarios)",
    "okinawa": "sim: DVIDS muito forte (bases atuais)",
    "pearl-harbor": "sim: NPS + DVIDS muito forte",
    "hashima": "nao (so CC BY/BY-SA de turistas; governo do Japao com credito)",
    "omaha": "sim: DVIDS (aniversarios do Dia D), ABMC",
    "mittelwerk": "fraco: memorial alemao (licencas alemas); quase nada PD",
    "camp-century": "fraco: so imagens NASA/USGS do gelo e estudos (PD)",
    "cheyenne": "parcial: DVIDS (Space Force/NORAD), acesso controlado",
    "area51": "nao (so satelite USGS/Landsat)",
    "nts": "sim: NNSA/DOE (PD), Landsat; visitas guiadas mensais",
    "alcatraz": "sim: NPS (PD) + DVIDS",
    "fort-jefferson": "sim: NPS (PD)",
    "gettysburg": "sim: NPS (PD) + DVIDS (staff rides)",
    "antietam": "sim: NPS (PD)",
    "andersonville": "sim: NPS (PD)",
    "fort-sumter": "sim: NPS (PD)",
    "lincoln": "sim: NPS Ford's Theatre (PD)",
    "appomattox": "sim: NPS (PD)",
    "hanford": "sim: DOE/NPS Manhattan Project NHP (PD)",
    "trinity": "sim: DVIDS / White Sands Missile Range (open house anual)",
    "diego-garcia": "sim: DVIDS forte (base ativa)",
    "aleutians": "parcial: NPS (Aleutian WWII NHA), USFWS (Alaska Maritime NWR)",
    "chernobyl": "nao (nao e EUA)",
}

NOTAVEIS = {  # titulo | URL (IA ids conferidos na busca; filme de governo = PD salvo trechos de terceiros)
    "iwo-jima": [("To the Shores of Iwo Jima (1945, USN/USMC/USCG)", "https://archive.org/details/ToTheShoresOfIwoJima")],
    "peleliu": [("Fury in the Pacific (1945, Army/Navy/USMC)", "https://archive.org/details/MN-5051J")],
    "pearl-harbor": [("December 7th (1943, John Ford/Gregg Toland, versao longa)", "https://archive.org/details/gov.archives.arc.40099.bl")],
    "aleutians": [("Report from the Aleutians (1943, John Huston, Army)", "https://archive.org/details/gov.dod.dimoc.20347")],
    "enewetak": [("Operation Ivy (1952, Ivy Mike) - copia do DOE", "https://archive.org/details/gov.doe.0800012")],
    "trinity": [("Nuclear Test Film - Trinity Shot (1945, DOE)", "https://archive.org/details/gov.doe.0800001")],
    "camp-century": [("The Big Picture: Camp Century (Army)", "https://archive.org/details/big-picture-camp-century")],
    "nts": [("Nuclear Test Film - Operation Teapot (1955, DOE)", "https://archive.org/details/gov.doe.0800017")],
    "johnston": [("Starfish Prime Interim Report by Commander JTF-8 (1962)", "https://archive.org/details/StarfishPrimeInterimReportByCommanderJTF8")],
    "bikini": [("Nuclear Test Film - Project Crossroads (DOE)", "https://archive.org/details/gov.doe.0800002")],
    "tinian": [("The Last Bomb (1945, AAF)", "https://archive.org/details/gov.archives.arc.65631")],
    "corregidor": [("Appointment in Tokyo (1945, Army)", "https://archive.org/details/gov.dod.dimoc.20379")],
    "midway": [("Torpedo Squadron 8 (1942, John Ford, USN)", "https://archive.org/details/torpedo_squadron8")],
}


C = "https://commons.wikimedia.org/wiki/File:"
NOTAVEIS_COMMONS = {  # Commons, PD, conferidos na busca de 12/11/2026 (fonte original no proprio arquivo: LOC, USMC, DoD...)
    "antietam": [("Antietam: Confederate dead by a fence on the Hagerstown road (Gardner, 1862, LOC)", C + "Antietam,_Md._Confederate_dead_by_a_fence_on_the_Hagerstown_road_LOC_cwpb.01097.jpg")],
    "lincoln": [("Execution of the Lincoln assassins (Gardner, 7 jul 1865), 6902x5425", C + "Execution_Lincoln_assassins.jpg")],
    "andersonville": [("Andersonville Prison, July 1864 (LOC), 4024x5367", C + "Andersonville_Prison,_Georgia_in_July_1864._LOC_gvhs01.vhs00039.jpg")],
    "appomattox": [("McLean house, Appomattox, 1865 (LOC), 7500x6311", C + "Appomattox_Court_House,_Virginia._McLean_house_LOC_cwpb.01395.jpg")],
    "fort-jefferson": [("Fort Jefferson, Dry Tortugas (aerea, PD)", C + "Fort-Jefferson_Dry-Tortugas.jpg")],
    "mittelwerk": [("Mittelwerk V-2 complex tunnel (1945)", C + "Mittelwerk_V-2_complex_tunnel.jpg")],
    "truk": [("Japanese shipping under attack in Truk Lagoon, 17 Feb 1944 (Hailstone)", C + "Japanese_shipping_under_attack_in_Truk_Lagoon_during_Operation_Hailstone,_17_February_1944_(80-G-215151).jpg")],
    "hanford": [("Hanford B-Reactor Area, 2 jun 1944", C + "Hanford_B-Reactor_Area_1944.jpg")],
    "cheyenne": [("Cheyenne Mountain 20-ton blast door closing (USAF, 2012)", C + "121025-F-ZZ000-001_Cheyenne_Mountain_20-ton_blast_door_closing.jpg")],
    "area51": [("Area 51, 28 Aug 1968 (satelite, PD)", C + "Area_51_28_August_1968_2.jpg")],
    "johnston": [("Johnston Atoll Chemical Agent Disposal System, Nov 1990", C + "Johnston_Atoll_Chemical_Agent_Disposal_System_Nov_1990.JPEG")],
    "camp-century": [("Camp Century trench construction (1960)", C + "Camp_Century_trench_construction.png"),
                     ("Camp Century revisited - a pictorial view, June 1969 (USACE, PDF)", C + "Camp_Century_revisited-_A_pictorial_view_-_June_1969_-_USACE-p266001coll1-3499.pdf")],
    "okinawa": [("Rubble of the walls of Shuri castle, 1945", C + "Rubble_of_the_walls_of_Shuri_castle,_1945_01.jpg")],
    "nts": [("Grable event, Operation Upshot-Knothole (1953)", C + "Nuclear_artillery_test_Grable_Event_-_Part_of_Operation_Upshot-Knothole.jpg")],
    "wake": [("USMC-17673 (Wake, USMC Archives)", C + "USMC-17673.jpg")],
}

temas = sorted(m["temas"].items(), key=lambda kv: (-kv[1]["nota"], -kv[1]["indice_epoca"]))
for k, r in temas:
    print(f"**{r['nome']}** (nota {r['nota']:g}) - atual livre: {ATUAL.get(k, '?')}")
    itens = [i for i in m["itens_chave_auto"].get(k, []) if not any(x in (str(i.get('titulo')) + ' |') for x in RUIDO)]
    for t, u in NOTAVEIS.get(k, []):
        print(f"- [{t}]({u}) - Internet Archive, filme de governo")
    for t, u in NOTAVEIS_COMMONS.get(k, []):
        print(f"- [{t}]({u}) - Wikimedia Commons, PD")
    for i in itens[:4]:
        extra = []
        if i.get("ano"): extra.append(str(i["ano"]))
        if i.get("resolucao"): extra.append(i["resolucao"])
        lic = i.get("licenca") or (i.get("licenca_declarada") or "").replace("http://creativecommons.org/", "cc/")
        titulo = str(i.get("titulo")).replace("File:", "").replace("[", "(").replace("]", ")")[:90]
        print(f"- [{titulo}]({i['url']}) - {i['fonte']}; {lic}{'; ' + ', '.join(extra) if extra else ''}")
    print()
