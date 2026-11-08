# Catálogo dos trechos reais (fonte única: corte + crédito na tela). Formatos: pol = 4:3 960×720 (polaroid), mon = 16:9 960×540
# (câmera/monitor), cel = 9:16 540×960 (celular). crop em frações do quadro de origem (x0, y0, x1, y1). Uso: python3 shared/clipes.py corta
import json, subprocess, sys
from pathlib import Path
R = Path(__file__).parent.parent
C = {}
def c(nome, arq, fmt, legenda, credito, url, ini, crop=(0, 0, 1, 1), ss=0.0, dur=None, rate=1.0):
    C[nome] = dict(arq=arq, fmt=fmt, legenda=legenda, credito=credito, url=url, ini=ini, crop=crop, ss=ss, dur=dur, rate=rate)
YT = "https://www.youtube.com/watch?v="
# --- hook
c("maringa-drone", "dl/clips/gm5vWBbuXyY-102.mp4", "pol", "MARINGÁ · PR · DEPOIS DO TORNADO", "VÍDEO: 7K DRONES · YOUTUBE · 07/11/2026", YT + "gm5vWBbuXyY", 102.0, (0.06, 0, 0.94, 0.86))
c("chapeco-centro", "dl/okd61_o5xks.mp4", "pol", "CHAPECÓ · SC · 04/11, 10H30", "VÍDEO: CÂMERA AO VIVO PORTAL CHAPECÓ · 04/11/2026", YT + "okd61_o5xks", 104.0, (0.12, 0.05, 0.88, 0.84), ss=104.0, dur=7)
c("santo-augusto-rua", "dl/clips/ix8SSbAajAw-12.mp4", "pol", "SANTO AUGUSTO · RS · 07/11, MADRUGADA", "VÍDEO: VAGNER ONUCZAK (MORADOR) · YOUTUBE · 07/11/2026", YT + "ix8SSbAajAw", 12.0, (0.125, 0, 0.875, 1))
# --- dia 1: Maringá
c("maringa-arvore", "dl/clips/2YfBh5M2Bp8-18.mp4", "pol", "MARINGÁ · ÁRVORES PARTIDAS", "VÍDEO: LUNG ARTS · YOUTUBE · 03/11/2026", YT + "2YfBh5M2Bp8", 18.0)
c("maringa-posto", "dl/clips/2YfBh5M2Bp8-24.mp4", "pol", "MARINGÁ · POSTES NO CHÃO", "VÍDEO: LUNG ARTS · YOUTUBE · 03/11/2026", YT + "2YfBh5M2Bp8", 24.0)
c("maringa-limpeza", "dl/clips/2YfBh5M2Bp8-48.mp4", "pol", "MARINGÁ · A LIMPEZA", "VÍDEO: LUNG ARTS · YOUTUBE · 03/11/2026", YT + "2YfBh5M2Bp8", 48.0)
# --- dia 3: 4/11
c("chapeco-predios", "dl/okd61_o5xks.mp4", "mon", "CHAPECÓ · CENTRO · 04/11", "VÍDEO: CÂMERA AO VIVO PORTAL CHAPECÓ · 04/11/2026", YT + "okd61_o5xks", 112.0, (0, 0.03, 1, 0.84), ss=112.0, dur=6)
c("chapeco-aeroporto", "dl/clips/Q8uunz9iwXA-96.mp4", "mon", "AEROPORTO DE CHAPECÓ · 10H30", "VÍDEO: CÂMERA PORTAL CHAPECÓ · YOUTUBE · 04/11/2026", YT + "Q8uunz9iwXA", 96.0, (0, 0.11, 1, 1))
c("chapeco-palmeiras", "dl/clips/cgaVfPKLRAg-408.mp4", "mon", "AEROPORTO · CABECEIRA 30 · 10H31", "VÍDEO: CÂMERA PORTAL CHAPECÓ · YOUTUBE · 04/11/2026", YT + "cgaVfPKLRAg", 408.0, (0, 0, 1, 0.86))
c("chapeco-telhas", "dl/clips/cgaVfPKLRAg-616.mp4", "mon", "CHAPECÓ · TELHAS PELO AR", "VÍDEO: CÂMERA PORTAL CHAPECÓ · YOUTUBE · 04/11/2026", YT + "cgaVfPKLRAg", 616.0, (0, 0, 1, 0.86))
c("xanxere-rodovia", "dl/clips/iF-GPyX20hM-2.mp4", "cel", "XANXERÊ · RODOVIA · 04/11", "VÍDEO: RÁDIO AMIGO DO POVO · YOUTUBE · 04/11/2026", YT + "iF-GPyX20hM", 2.0, (0, 0.17, 1, 1))
c("xanxere-drone", "dl/clips/UMBq-14sHEU-20.mp4", "cel", "XANXERÊ · O RASTRO", "VÍDEO: JOLVANI BUENO · YOUTUBE · 05/11/2026", YT + "UMBq-14sHEU", 20.0)
c("erval-eucalipto", "dl/clips/n5vFxl4TV4w-16.mp4", "pol", "ERVAL GRANDE · RS · 04/11", "VÍDEO: MARCO ANTONIO SILVA · YOUTUBE · 05/11/2026", YT + "n5vFxl4TV4w", 16.0, (0, 0.36, 1, 0.77))
c("rionegrinho-casas", "dl/clips/aMyHsdD9de8-27.mp4", "cel", "RIO NEGRINHO · SC · INTERIOR", "VÍDEO: SIDIONEI MIRANDA · YOUTUBE · 07/11/2026", YT + "aMyHsdD9de8", 27.0)
c("rionegrinho-telhado", "dl/clips/aMyHsdD9de8-75.mp4", "cel", "RIO NEGRINHO · O CONSERTO", "VÍDEO: SIDIONEI MIRANDA · YOUTUBE · 07/11/2026", YT + "aMyHsdD9de8", 75.0)
c("chapeco-claroes", "dl/clips/cgaVfPKLRAg-608.mp4", "mon", "CHAPECÓ · CENTRO · 04/11, MANHÃ", "VÍDEO: CÂMERA PORTAL CHAPECÓ · YOUTUBE · 04/11/2026", YT + "cgaVfPKLRAg", 608.0, (0, 0, 1, 0.86))
# --- é inédito?
c("xanxere2015-funil", "dl/clips/ogO0Q4szoBg-175.mp4", "pol", "XANXERÊ · 20/04/2015", "VÍDEO: ELIAS BORTOLUZZI COLLET · YOUTUBE · 2015", YT + "ogO0Q4szoBg", 175.0)
c("xanxere2015-cctv", "dl/clips/SPahXz2p7aw-96.mp4", "mon", "XANXERÊ · 20/04/2015 · 15H04", "VÍDEO: SAMUEL BIONDO GIORDANI · YOUTUBE · 2015", YT + "SPahXz2p7aw", 96.0)
c("guaraciaba2009", "dl/clips/tpzNZVAMWgY-0.mp4", "pol", "GUARACIABA · SC · SET/2009", "VÍDEO: LANA CARMONA PACHECO · YOUTUBE · 2009", YT + "tpzNZVAMWgY", 0.0)
c("rbi-comercio", "dl/clips/MD80NpRCZUA-9.mp4", "pol", "RIO BONITO DO IGUAÇU · PR · 08/11/2025", "VÍDEO: DRONELOOK · YOUTUBE · 08/11/2025", YT + "MD80NpRCZUA", 9.0, (0, 0.08, 1, 1))
c("rbi-rastro", "dl/clips/MD80NpRCZUA-234.mp4", "pol", "RIO BONITO DO IGUAÇU · O RASTRO", "VÍDEO: DRONELOOK · YOUTUBE · 08/11/2025", YT + "MD80NpRCZUA", 234.0, (0, 0.08, 1, 1))
c("celular-nuvem", "dl/clips/SyxEa6IjJGk-118.mp4", "pol", "QUALQUER UM FILMA O CÉU", "VÍDEO: DE OLHO NO CÉU · YOUTUBE · 2022", YT + "SyxEa6IjJGk", 118.0)
c("dolores2016", "dl/clips/RIIJxV83oRY-75.mp4", "pol", "DOLORES · URUGUAI · 2016", "VÍDEO: SEBASTIÁN MARTÍNEZ · YOUTUBE · 2016", YT + "RIIJxV83oRY", 75.0)
# --- caixa 1
c("prateleira-timelapse", "dl/clips/5stC8FkNuA8-14.mp4", "pol", "FRENTE DE RAJADA · SP", "VÍDEO: PIRACICABA STORMCHASING · CC BY · YOUTUBE", YT + "5stC8FkNuA8", 14.0)
c("mesociclone", "dl/clips/UW5AlqbAS9o-3.mp4", "pol", "MESOCICLONE · A BASE GIRANDO", "VÍDEO: PIRACICABA STORMCHASING · CC BY · YOUTUBE", YT + "UW5AlqbAS9o", 3.0)
c("tail-cloud", "dl/clips/UW5AlqbAS9o-48.mp4", "pol", "A NUVEM SE ESTREITA", "VÍDEO: PIRACICABA STORMCHASING · CC BY · YOUTUBE", YT + "UW5AlqbAS9o", 48.0)
c("funil-maringa2022", "dl/clips/SyxEa6IjJGk-142.mp4", "pol", "NUVEM-FUNIL · PR · 2022", "VÍDEO: DE OLHO NO CÉU · YOUTUBE · 2022", YT + "SyxEa6IjJGk", 142.0)
c("tornado-nssl1973", "dl/clips/_u3qolstr50-44.mp4", "pol", "TORNADO · EUA · 1973", "VÍDEO: NOAA/NSSL · CC BY · YOUTUBE", YT + "_u3qolstr50", 44.0)
# --- caixa 2 e 3
c("prateleira-baixa", "dl/clips/CEXEYDGzMlY-60.mp4", "pol", "TEMPORAL CHEGANDO", "VÍDEO: PIRACICABA STORMCHASING · CC BY · YOUTUBE", YT + "CEXEYDGzMlY", 60.0)
c("rbi-galpao", "dl/clips/MD80NpRCZUA-99.mp4", "pol", "RIO BONITO DO IGUAÇU · F4", "VÍDEO: DRONELOOK · YOUTUBE · 08/11/2025", YT + "MD80NpRCZUA", 99.0, (0, 0.08, 1, 1))
c("rbi-bombeiros", "dl/clips/MD80NpRCZUA-126.mp4", "pol", "UMA CIDADE INTEIRA ATINGIDA", "VÍDEO: DRONELOOK · YOUTUBE · 08/11/2025", YT + "MD80NpRCZUA", 126.0, (0, 0.08, 1, 1))
# --- o que fazer
c("sinal-nuvem", "dl/clips/kFOhAT2QsSc-5.mp4", "pol", "NUVEM BAIXA E ESCURA", "VÍDEO: NOAA/NSSL · CC BY · YOUTUBE", YT + "kFOhAT2QsSc", 5.0)
c("sinal-granizo", "dl/clips/kFOhAT2QsSc-10.mp4", "pol", "GRANIZO GRANDE", "VÍDEO: NOAA/NSSL · CC BY · YOUTUBE", YT + "kFOhAT2QsSc", 10.0)
c("sinal-funil", "dl/clips/SyxEa6IjJGk-40.mp4", "pol", "PAREDE DE NUVENS", "VÍDEO: DE OLHO NO CÉU · YOUTUBE · 2022", YT + "SyxEa6IjJGk", 40.0)

SAIDA = {"pol": (960, 720), "mon": (960, 540), "cel": (540, 960)}
def corta():
    o = R / "remotion/public/clips"; o.mkdir(parents=True, exist_ok=True)
    for nome, k in C.items():
        W, H = SAIDA[k["fmt"]]; x0, y0, x1, y1 = k["crop"]
        # recorte em frações e depois crop central para a proporção do formato
        vf = (f"crop=iw*{x1-x0}:ih*{y1-y0}:iw*{x0}:ih*{y0},"
              f"crop='min(iw,ih*{W}/{H})':'min(ih,iw*{H}/{W})',scale={W}:{H},fps=30,setsar=1")
        cmd = ["ffmpeg", "-v", "error", "-y"] + (["-ss", str(k["ss"])] if k["ss"] else []) + ["-i", str(R / k["arq"])]
        cmd += (["-t", str(k["dur"])] if k["dur"] else []) + ["-an", "-vf", vf, "-c:v", "libx264", "-crf", "20", "-preset", "fast", "-pix_fmt", "yuv420p", str(o / f"{nome}.mp4")]
        subprocess.run(cmd, check=True)
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(o / f"{nome}.mp4")], capture_output=True, text=True).stdout)
        k["duracao"] = round(d, 2); print(nome, k["fmt"], d, flush=True)
    json.dump(C, open(R / "shared/clipes.json", "w"), ensure_ascii=False, indent=1)
if __name__ == "__main__" and sys.argv[1:] == ["corta"]: corta()
