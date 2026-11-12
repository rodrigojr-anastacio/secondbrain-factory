import json
L = ["en", "es", "pt", "fr", "de", "it", "pl", "ja", "ru", "tr"]
D = dict(en=10, es=6, pt=4.5, fr=2, de=1.5, it=1.5, pl=1.5, ja=7, ru=4, tr=0.5)
C = dict(en=3, es=7, pt=8, fr=10, de=9, it=9, pl=9, ja=7, ru=8, tr=9)
R = dict(en=10, es=4, pt=2.5, fr=6, de=8, it=6, pl=3, ja=7, ru=0, tr=2)
V = dict(en=9, es=8, pt=10, fr=5, de=3, it=4, pl=3, ja=2, ru=3, tr=2)
K = dict(en=6, es=6, pt=6, fr=6, de=3, it=6, pl=6, ja=5, ru=2, tr=5)
def nota(l, w): return round(sum(a * b[l] for a, b in zip(w, (D, C, R, V, K))), 2)
W0 = (.30, .25, .20, .15, .10); W1 = (.2,) * 5; W2 = (.20, .25, .30, .15, .10)
out = {}
for l in L:
    trava = "RPM" if R[l] <= 1 else ("concorrência" if C[l] <= 2 else "")
    out[l] = dict(D=D[l], C=C[l], R=R[l], V=V[l], K=K[l], base=nota(l, W0), iguais=nota(l, W1), rpm30=nota(l, W2), trava=trava)
json.dump(out, open("dados/matriz.json", "w"), indent=1)
for l, v in sorted(out.items(), key=lambda x: -x[1]["base"]): print(l, v)
# se C(en)=2 (trava)
