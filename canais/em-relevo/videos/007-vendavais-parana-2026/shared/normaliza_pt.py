# Normalização para comparar Whisper × roteiro falado (v2): algarismos -> por extenso (pt-BR), km/% -> palavras, "F2"/"F -4" -> "efe dois".
import re, unicodedata
U = "zero um dois três quatro cinco seis sete oito nove dez onze doze treze catorze quinze dezesseis dezessete dezoito dezenove".split()
D = {2: "vinte", 3: "trinta", 4: "quarenta", 5: "cinquenta", 6: "sessenta", 7: "setenta", 8: "oitenta", 9: "noventa"}
C = {1: "cento", 2: "duzentos", 3: "trezentos", 4: "quatrocentos", 5: "quinhentos", 6: "seiscentos", 7: "setecentos", 8: "oitocentos", 9: "novecentos"}
def ext(n):
    if n < 20: return U[n]
    if n < 100: return D[n // 10] + ("" if n % 10 == 0 else " e " + U[n % 10])
    if n == 100: return "cem"
    if n < 1000: return C[n // 100] + ("" if n % 100 == 0 else " e " + ext(n % 100))
    if n < 1000000:
        m, r = divmod(n, 1000); p = "mil" if m == 1 else ext(m) + " mil"
        return p if r == 0 else p + (" e " if r < 100 or r % 100 == 0 else " ") + ext(r)
    return str(n)
def norm(s):
    s = re.sub(r"(\d)\s*\.\s*(\d{3})", r"\1\2", s)                      # 1 .200 / 1.200
    s = re.sub(r"\b[Ff]\s*[A-Za-z]?\s*-?\s*(\d)\b", lambda m: "efe " + U[int(m.group(1))], s)  # F2, F -4, FR2, FS2
    s = re.sub(r"(\d+),(\d+)", lambda m: ext(int(m.group(1))) + " vírgula " + ext(int(m.group(2))), s)
    s = re.sub(r"(\d+)\s*%", lambda m: m.group(1) + " por cento", s)
    s = re.sub(r"\bkm\b", "quilômetros", s)
    s = re.sub(r"\d+", lambda m: ext(int(m.group(0))), s)
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.replace("efe", "efe").replace("éfe", "efe")
    return re.sub(r"[^a-z0-9 ]", " ", s).split()
