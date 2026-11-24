# Expedientes Secretos #1: personagens (e1, 24/11/2026)

Fonte única das descrições: `personagens.py` (`DESC`). Nos prompts o personagem entra como token `{CHAVE}` e o
`montar.py` troca pela descrição fixa abaixo, **literal em todo quadro** (técnica que segurou o Juan em 7/7 na v3).
**Regra da v3:** quadro com personagem que tem folha → config com a folha (`visual/visual-<chaves>.yaml`, máx. 2
folhas por quadro); quadro sem nenhum → `visual/visual-sem.yaml` (sem folha), senão o Codex enfia o personagem na cena.
Pessoas reais: figuras históricas mortas, retratadas com respeito; aparência inspirada em fotos de época, não retrato.

## Folhas de personagem
| Chave | Quem | Folha | Gerar na e2? |
|---|---|---|---|
| JUAN | Juan Pujol (GARBO), ~30 | `arte-v2/folha-cor.jpg` | **já existe** |
| ARACELI | Araceli González, esposa, ~27 | `arte-001/folhas/folha-araceli.jpg` | sim |
| HARRIS | Tomás Harris, oficial do MI5, ~35 | `arte-001/folhas/folha-harris.jpg` | sim |
| KUHLENTHAL | Karl-Erich Kühlenthal, Abwehr Madri, ~34 | `arte-001/folhas/folha-kuhlenthal.jpg` | sim (o oficial alto das artes P201/P205 da amostra) |
| HARRIMAN | W. Averell Harriman, embaixador, 53 (1945) | `arte-001/folhas/folha-harriman.jpg` | sim |
| THEREMIN | Léon Theremin, inventor, 49 (1945) | `arte-001/folhas/folha-theremin.jpg` | sim |
| KENNAN | George F. Kennan, embaixador, 48 (1952) | `arte-001/folhas/folha-kennan.jpg` | sim |
| PIONEROS | 5 Pioneiros soviéticos, 10–12 anos | `arte-001/folhas/folha-pioneros.jpg` | sim (folha de grupo) |
| NKVD | agente do NKVD (**fictício, composto**), ~40 | `arte-001/folhas/folha-nkvd.jpg` | sim |
Sem folha (poucos quadros; só a descrição fixa): TECNICO (técnico do Dept. de Estado, sem nome na HQ) e LODGE
(Henry Cabot Lodge Jr., 1960).

## Descrições físicas fixas (vão literais nos prompts)
- **JUAN:** slim Spanish man about 30, oval face, high receding hairline, dark slicked-back hair, thin pencil mustache, thick dark eyebrows, gray double-breasted suit, dark red tie, dark trench coat and trilby hat when outdoors.
- **ARACELI:** Spanish woman about 27, oval face, large dark eyes, dark wavy shoulder-length 1940s hair, red lipstick, dark green fitted 1940s dress with a small brooch, cream coat when outdoors.
- **HARRIS (Tomás):** British-Spanish man about 35, round friendly face, dark wavy hair combed back, dark eyes, clean-shaven, warm smile, brown tweed jacket, open collar or loose dark tie, often a cigarette.
- **KUHLENTHAL:** very tall and thin man about 34, long narrow face, blond hair parted to the side, pale eyes, cold polite smile, civilian dark charcoal suit, no insignia.
- **HARRIMAN:** tall lean American diplomat about 53, long narrow face, dark hair graying at the temples, heavy dark eyebrows, deep-set eyes, serious expression, dark three-piece suit, white shirt, dark tie.
- **THEREMIN:** Russian inventor about 49, slim, thin intelligent face, dark hair combed straight back, high forehead, tired kind eyes, clean-shaven, worn gray work jacket over a white shirt.
- **KENNAN:** slim American diplomat about 48, thin face, high forehead with receding hairline, short neat dark-blond hair, clean-shaven, thoughtful eyes, rimless glasses only when reading, gray suit, dark tie.
- **PIONEROS:** Soviet schoolchildren aged 10 to 12, boys and girls, white shirts and blouses, bright red neckerchiefs, neatly combed hair, girls with braids and white ribbons.
- **NKVD:** fictional Soviet security officer about 40, broad square face, short dark hair, thick dark mustache, small cold eyes, long dark gray overcoat, dark fur hat outdoors.
- **TECNICO:** American embassy technician about 35, compact build, dark hair cut short, headphones around his neck, white shirt with sleeves rolled up, dark trousers.
- **LODGE:** tall handsome American ambassador about 58, strong jaw, wavy graying hair combed back, clean-shaven, dark suit, white pocket square.

## Objeto recorrente (La Cosa)
**O selo:** "a large hand-carved wooden replica of the Great Seal of the United States: a wooden eagle with spread
wings holding a striped shield on its chest, warm polished wood". Aparece como objeto histórico na cena, nunca como
logo do produto. A cápsula: "a small copper cylinder with a thin antenna" sob o bico da águia.

## Prompts das folhas
Em `extras.py` (`FOLHAS`) → `cenas-folhas.json` (paisagem, config sem folha). Conferir cada folha antes de seguir:
mesmo rosto nas 5 vistas, sem texto, roupa da época. Folha ruim = refazer (no máx. 2×) antes de gerar os quadros.
