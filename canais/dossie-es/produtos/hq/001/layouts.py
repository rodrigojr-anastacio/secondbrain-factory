"""Layouts de página da HQ "Expedientes Secretos #1" (e1, 24/11/2026).

Página 6×9 pol. a 300 dpi = 1800×2700 px; área de quadros x 80..1720, y 130..2610; calha de 30 px.
Cada layout é uma lista de "slots" na ordem de leitura ocidental (esquerda→direita, cima→baixo).
Todo layout tem pelo menos 1 quadro diagonal (poly) ou grande, como na v3 (pág. 1 e 2 da amostra).

Proporção de cada slot (para gerar a arte no tamanho certo): pela caixa envolvente w/h
  > 1.25 → paisagem (1536×864) · < 0.8 → retrato (1024×1536) · senão → quadrado (1024×1024).

| layout | quadros | forma |
|---|---|---|
| A5 | 5 | faixa larga · par com calha diagonal (largo + estreito em pé) · faixa larga · faixa baixa (= pág. 1 da v3) |
| B5 | 5 | faixa larga · 2 à esquerda + 1 alto em pé à direita, calhas diagonais · faixa baixa (= pág. 2 da v3) |
| C4 | 4 | quadro grande no topo · par com calha diagonal · faixa larga |
| D3 | 3 | splash quase quadrado · par com calha diagonal embaixo |
| E6 | 6 | 3 linhas de 2; a do meio com calha diagonal; última = largo + estreito em pé |
| F1 | 1 | página inteira (splash em pé) |
| G4 | 4 | faixa larga · coluna alta à esquerda + 2 à direita, calha diagonal |
"""


def R(x, y, w, h):
    return {"rect": [x, y, w, h]}


def P(*pts):
    return {"poly": [list(p) for p in pts]}


LAYOUTS = {
    "A5": [
        R(80, 130, 1640, 600),
        P((80, 760), (1235, 760), (1150, 1460), (80, 1460)),
        P((1265, 760), (1720, 760), (1720, 1460), (1180, 1460)),
        R(80, 1490, 1640, 620),
        R(80, 2140, 1640, 470),
    ],
    "B5": [
        R(80, 130, 1640, 600),
        P((80, 760), (1300, 760), (1120, 1520), (80, 1520)),
        P((1330, 760), (1720, 760), (1720, 2110), (1010, 2110)),
        P((80, 1550), (1112, 1550), (980, 2110), (80, 2110)),
        R(80, 2140, 1640, 470),
    ],
    "C4": [
        R(80, 130, 1640, 1150),
        P((80, 1310), (900, 1310), (800, 1990), (80, 1990)),
        P((930, 1310), (1720, 1310), (1720, 1990), (830, 1990)),
        R(80, 2020, 1640, 590),
    ],
    "D3": [
        R(80, 130, 1640, 1650),
        P((80, 1810), (880, 1810), (800, 2610), (80, 2610)),
        P((910, 1810), (1720, 1810), (1720, 2610), (830, 2610)),
    ],
    "E6": [
        R(80, 130, 800, 790),
        R(910, 130, 810, 790),
        P((80, 950), (1000, 950), (860, 1750), (80, 1750)),
        P((1030, 950), (1720, 950), (1720, 1750), (890, 1750)),
        R(80, 1780, 1000, 830),
        R(1110, 1780, 610, 830),
    ],
    "F1": [
        R(80, 130, 1640, 2480),
    ],
    "G4": [
        R(80, 130, 1640, 560),
        P((80, 720), (760, 720), (660, 2610), (80, 2610)),
        P((790, 720), (1720, 720), (1720, 1650), (741, 1650)),
        P((743, 1680), (1720, 1680), (1720, 2610), (690, 2610)),
    ],
}

TAMANHO = {"paisagem": (1536, 864), "retrato": (1024, 1536), "quadrado": (1024, 1024)}


def caixa(slot):
    if "rect" in slot:
        return slot["rect"]
    xs = [p[0] for p in slot["poly"]]
    ys = [p[1] for p in slot["poly"]]
    return [min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)]


def orientacao(slot):
    _, _, w, h = caixa(slot)
    r = w / h
    return "paisagem" if r > 1.25 else ("retrato" if r < 0.8 else "quadrado")


if __name__ == "__main__":
    for nome, slots in LAYOUTS.items():
        print(nome, [orientacao(s) for s in slots])
