#!/usr/bin/env python
"""Aplica a reavaliação do backlog do Dossier (bolha da Cosa Nostra, 24/11/2026) SÓ via tools/rotinas/backlog.py.
Fonte: pesquisa/backlog-dossie-bolha-2026-11-24/<tema>/manada.json (manada.py buscar, via WARP) + youtube.studio_video (24/11)."""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path.home() / "workspace/fabrica-youtube"
D = REPO / "pesquisa/backlog-dossie-bolha-2026-11-24"
PY = str(REPO / "tools/.venv/bin/python")
BK = str(REPO / "tools/rotinas/backlog.py")
HOJE = "2026-11-24"
STUDIO = {"tipo": "nosso", "fonte": "youtube.studio_video (export 24/11, 28 dias)",
          "link": "psql: select * from youtube.studio_video where canal_slug='dossie-es' and exportado_em='2026-11-24'",
          "numero": "Cosa Nostra 26.370 views (52% do canal), 87.184 impressões; KGB 11.550; SS 7.428; 70–87% das views vêm de sugeridos",
          "data": HOJE}


def manada(slug, n=4, ids=None):
    vs = json.loads((D / slug / "manada.json").read_text())
    if ids:
        vs = [v for v in vs if v["id"] in ids]
    out = []
    for v in vs[:n]:
        dt = v["data"]
        out.append({"id": v["id"], "canal": v["canal"], "views": v["views"], "data": f"{dt[:4]}-{dt[4:6]}-{dt[6:]}",
                    "faz": "pelo título: " + v["titulo"][:110]})
    return out


def busca(slug, numero, n=2):
    vs = json.loads((D / slug / "manada.json").read_text())
    ev = [{"tipo": "busca", "fonte": f"manada.py buscar (yt-dlp via WARP), pesquisa/backlog-dossie-bolha-2026-11-24/{slug}",
           "link": vs[0]["url"], "numero": numero, "data": HOJE}]
    return ev + [STUDIO]


def run(*args):
    r = subprocess.run([PY, BK, *args], capture_output=True, text=True)
    print(" ".join(a if len(a) < 60 else a[:57] + "…" for a in args[:4]), "->", (r.stdout + r.stderr).strip()[-300:])
    if r.returncode:
        sys.exit(r.returncode)
    return r.stdout


NOVOS = [
    dict(slug="ndrangheta", tema="La 'Ndrangheta (la mafia de Calabria)", d=9, e=10, u=7,
         titulo="TODA la historia de la 'Ndrangheta en N minutos",
         angulo="Recorte: a 'Ndrangheta como ORGANIZAÇÃO de sangue (as 'ndrine são famílias, por isso quase não há arrependidos) que trocou os sequestros pela cocaína e virou a máfia mais rica; ponte LatAm: os brokers na Colômbia e nos portos do Brasil. Hook fora da manada: Roma, novembro de 1973: o jornal Il Messaggero recebe um envelope com uma orelha humana, a de John Paul Getty III, sequestrado por calabreses [conferir]. Expedientes possíveis: La Oreja, El Santuario (Polsi), El Cumpleaños (Duisburg 2007), El Puerto (Gioia Tauro), El Juicio (Rinascita Scott). A manada abre em Calábria/San Luca e 'la mafia más poderosa' (Nova Lectio, Historias Vivas, Show Me the World).",
         riscos="Não usar a lenda dos 3 cavaleiros (fica no item mafia-origen-aragon) nem a Pizza Connection/Falcone do 004-cosa-nostra. Clone Era Span já usou o molde na 'Ndrangheta (r2 20/11): conferir na embalagem.",
         busca=("ndrangheta", "es: Historias Vivas 1.488.667 (2024), Show Me the World 1.001.441, La Huella 199.434 (08/2025); it: Nova Lectio 1.957.708 em 2 meses (09/2026); en Best Documentary 343.635 (07/2026). Sem clone 'toda la historia… en minutos' em es no topo")),
    dict(slug="mafia-rusa", tema="La Mafia rusa (los vory v zakone y la Bratva)", d=8, e=10, u=6,
         titulo="TODA la historia de la Mafia rusa en N minutos",
         angulo="Recorte: os vory v zakone (ladrones en ley) como ORGANIZAÇÃO com código, tatuagens e 'coroação', nascidos nas prisões soviéticas, que no colapso de 1991 viram a Bratva global (Brighton Beach, Espanha, América Latina). É a ponte exata Cosa Nostra × KGB. Hook fora da manada: o código das tatuagens lido como dossiê (estrelas nos joelhos = 'não me ajoelho diante de ninguém') [conferir]. A manada faz biografias (Mogilevich, Solonik, Ivankov: Cruzada Hostil 450 mil/328 mil/89 mil) ou 'tu vida en cada nivel' (Mr Sticky 446 mil).",
         riscos="Não repetir capítulos do 017-gulag (Gulag em si) nem do 005-kgb; vory entram pelo código e pela virada de 1991. Pessoas vivas (Mogilevich): só fatos de fonte.",
         busca=("bratva", "es: Cruzada Hostil 'Mogilevich' 450.668, Mr Sticky 'Mafia rusa' 446.428 (06/2026), Cruzada Hostil 'Solonik' 328.104; nenhum vídeo 'historia completa' no molde em es")),
    dict(slug="ratlines-odessa", tema="ODESSA y las rutas de las ratas (la red que sacó a los nazis hacia Sudamérica)", d=9, e=8, u=6,
         titulo="ODESSA: la red que llevó a los nazis a Sudamérica",
         angulo="Recorte: a fuga como REDE (bispo Alois Hudal em Roma, padre Draganović em San Girolamo, passaportes da Cruz Vermelha, a DAIE de Perón em Buenos Aires) e a ODESSA como mito × arquivo (Wiesenthal, o romance de Forsyth de 1972, o que os documentos provam). Hook fora da manada: Buenos Aires, anos 1990: o jornalista Uki Goñi descobre que parte dos arquivos de imigração da época tinha sido destruída [conferir; alternativa: carta de Hudal a Perón pedindo vistos]. A manada pergunta '¿por qué huyeron a Argentina?' em panorama (Historia con Jiven 1,5 mi, Armapedia 1,4 mi, Hispanoria 217 mil em 10/2026).",
         riscos="Canibalização: o 007-ss já tem Mengele/Helmut Gregor, Rauff, Barbie e Priebke (exp. 13–14) e o 002-mossad tem Eichmann. Protagonistas aqui são os que montaram a rede, não os fugitivos famosos. Nazismo = cuidado com anúncio (sem suástica na thumb).",
         busca=("ratlines", "es: Historia con Jiven 1.524.738, Armapedia 1.372.425 (02/2025), El Mapa de Sebas 276.481, Hispanoria 217.416 (17/10/2026); público do canal MX/AR/CO/ES. Guerra en Tinta (clone de estética?) 378 views em 17/11/2026")),
    dict(slug="outfit-chicago", tema="El Outfit de Chicago (la mafia de Al Capone)", d=8, e=8, u=5,
         titulo="TODA la historia de la mafia de Chicago en N minutos",
         angulo="Recorte: o Outfit como ORGANIZAÇÃO que durou 70 anos além de Capone (Torrio → Capone → Nitti → Accardo/Giancana; extorsão de Hollywood em 1943, cassinos de Las Vegas, o caso Spilotro). Hook fora da manada: Chicago, 1931: o que derruba Capone é um livro-caixa achado numa batida e decifrado por agentes do Tesouro (Frank Wilson) [conferir]. A manada é biografia de Capone abrindo no Massacre de São Valentim (Fusgo 2,6 mi, PERSONAJES 1,1 mi).",
         riscos="Não repetir Nova York/Luciano/Lei Seca do 004-cosa-nostra (exp. 4); o foco é Chicago e o pós-Capone. Capone como personagem, não como título-biografia.",
         busca=("clones-capone", "es: Fusgo 'La Historia Completa De Al Capone' 2.577.252, PERSONAJES 1.125.226 (01/2025), Cruzada Hostil 'Giancana' 94.143; pt: Planeta Novo 1.076.543 (08/2025)")),
    dict(slug="camorra", tema="La Camorra (la mafia de Nápoles)", d=6, e=9, u=5,
         titulo="TODA la historia de la Camorra en N minutos",
         angulo="Recorte: a Camorra como sistema SEM chefe (clãs que se partem e guerreiam), da Nápoles espanhola a Gomorra e Scampia. Hook fora da manada: Irpinia, 23/11/1980: o terremoto; o dinheiro da reconstrução vira a guerra entre a Nuova Camorra Organizzata de Raffaele Cutolo e a Nuova Famiglia [conferir]. A manada: Cruzada Hostil 'hidra de mil cabezas' (36 mil), Investigations 'Baby Camorra' (en, 546 mil).",
         riscos="Não usar a lenda dos 3 cavaleiros (item mafia-origen-aragon). Demanda em es menor que a da 'Ndrangheta: ir depois dela.",
         busca=("camorra", "es: Cruzada Hostil 36.495 (10/2025); en: Investigations 'Baby Camorra' 546.081 (06/2026); pt/it 2 vídeos novos em 20/11/2026 (tema se mexendo)")),
    dict(slug="triadas", tema="Las Tríadas chinas", d=6, e=8, u=4,
         titulo="TODA la historia de las Tríadas chinas en N minutos",
         angulo="Recorte: das sociedades secretas anti-Qing (juramento de sangue, códigos numéricos 489/438/426) aos sindicatos de Hong Kong e às Chinatowns da América. Hook fora da manada: Kowloon, a cidade murada: dezenas de milhares de pessoas em 2,6 hectares quase sem polícia, demolida em 1993 [conferir]. A manada: Mega Hampa 'La Mafia China' (San Francisco, 1,2 mi, 2018), Insider 'cómo operan' (55 mil), Cruzada Hostil (49 mil).",
         riscos="Vizinho do 014-yakuza (mesma família asiática): não colar na semana da Yakuza.",
         busca=("triadas", "es: Mega Hampa 1.247.570 (2018), Insider Español 55.270, Cruzada Hostil 49.357 (04/2025); sem clone no molde")),
    dict(slug="murder-inc", tema="Murder Inc. (los sicarios del Sindicato y la mafia judía de Nueva York)", d=5, e=8, u=4,
         titulo="Murder Inc.: la empresa de asesinatos de la mafia",
         angulo="Recorte: o braço armado do Sindicato nacional (Lepke Buchalter, Albert Anastasia, Bugsy Siegel) e a aliança judaico-italiana que o criou. Hook fora da manada: Coney Island, 12/11/1941: Abe Reles, testemunha do Estado sob guarda policial, cai da janela do Half Moon Hotel [conferir]. A manada é en (Michael Franzese 1,7 mi, 'Jewish Mafia').",
         riscos="Lansky e Havana já estão no 004-cosa-nostra (exp. 6): não repetir. Demanda em es fraca: é o reserva da família máfia.",
         busca=("murderinc", "en: Michael Franzese 'Jewish Mafia' 1.676.731, Bloodletters 'Meyer Lansky' 707.853; em es quase nada (demanda incerta)")),
]

REAVAL = [
    (50, 5, 9, 7, "bolha Cosa Nostra 24/11: sugestão de espectador do próprio público da Cosa Nostra (engajamento) e adjacência máxima; demanda em es baixa (El Camarote 5 mil, Alter Historia 7 mil, Suso Lopez 11 mil), título de curiosidade '¿La Mafia nació en España?' compensa. Lenda dos 3 cavaleiros fica só aqui.",
     busca("garduna", "es: Suso Lopez 'La garduña' 11.184, Alter Historia 7.323, El Camarote 'primera mafia española' 5.145 (11/2025): pouca oferta e pouca busca")),
    (46, 6, 7, 4, "bolha Cosa Nostra 24/11: serviços secretos da Guerra Fria ficam na órbita (KGB/CIA), mas longe do núcleo máfia → KGB → SS; encaixe 9 → 7. Mantém pelo público do Cone Sul.", [STUDIO]),
    (24, 8, 3, 4, "bolha Cosa Nostra 24/11: família religiosa fora da bolha (Inquisición 773 views/2.180 impressões, Masones 461/2.568, Templarios 116/455: CTR bom, quase sem impressões); encaixe 5 → 3. Não descartado: demanda em es alta; volta se a família religiosa ganhar impressões.", [STUDIO]),
]

if __name__ == "__main__":
    ids = {}
    for t in NOVOS:
        out = run("add", "--canal", "dossie-es", "--tema", t["tema"], "--slug", t["slug"], "--angulo", t["angulo"],
                  "--titulo", t["titulo"], "--riscos", t["riscos"], "--demanda", str(t["d"]), "--encaixe", str(t["e"]),
                  "--urgencia", str(t["u"]), "--evidencias", json.dumps(busca(*t["busca"]), ensure_ascii=False),
                  "--motivo", "bolha Cosa Nostra 24/11/2026 (BRIEF-dossie-backlog-bolha-cosa-nostra): tema vizinho da Cosa Nostra/KGB/SS; pesquisa em pesquisa/backlog-dossie-bolha-2026-11-24")
    import psycopg
    with psycopg.connect("dbname=vida") as con:
        for slug, i in con.execute("select slug,id from youtube.backlog where canal_slug='dossie-es'"):
            ids[slug] = i
    src = {t["slug"]: t["busca"][0] for t in NOVOS}
    for t in NOVOS:
        run("angulo", str(ids[t["slug"]]), "--angulo", t["angulo"], "--manada", json.dumps(manada(src[t["slug"]]), ensure_ascii=False),
            "--motivo", "ângulo fora da manada 24/11/2026 (bolha Cosa Nostra)")
    with psycopg.connect("dbname=vida") as con:
        atuais = {i: e for i, e in con.execute("select id, evidencias from youtube.backlog where canal_slug='dossie-es'")}
    for i, d, e, u, m, ev in REAVAL:
        ev = (atuais.get(i) or []) + ev   # nota --evidencias substitui: preserva as antigas
        run("nota", str(i), "--demanda", str(d), "--encaixe", str(e), "--urgencia", str(u), "--motivo", m,
            "--evidencias", json.dumps(ev, ensure_ascii=False))
    run("angulo", "50", "--angulo", "Mito × história: a lenda dos três cavaleiros espanhóis (Osso, Mastrosso, Carcagnosso) que teriam fundado Mafia, 'Ndrangheta e Camorra, e a Garduña de Toledo, contra o que os arquivos comprovam (a Garduña provavelmente é invenção do séc. XIX; a Coroa de Aragão dominou Sicília e Nápoles de verdade). Hook: a própria lenda como ela é jurada nos rituais calabreses [conferir]. Título de curiosidade: '¿La Mafia nació en España?'.",
        "--manada", json.dumps(manada("garduna", ids={"p16llAhT5mc", "jJAJ_fhEXGo", "9nBGwPkytNQ", "qc4IGJZsdEo"}), ensure_ascii=False),
        "--motivo", "ângulo fora da manada 24/11/2026: a manada conta a Garduña como fato ('la primera mafia'); nós contamos mito × arquivo")
