"""Personagens fixos da HQ "Expedientes Secretos #1" (e1, 24/11/2026): fonte única das descrições físicas.

Nos prompts dos quadros o personagem entra como token {CHAVE} (ex.: "{JUAN} sits at a desk"); o montar.py troca pelo
texto de DESC. Assim a mesma descrição vai literal em todo quadro (técnica que segurou o Juan em 7/7 na v3).
FOLHA = arquivo da folha de personagem (gerada na e2 em ../arte-001/folhas/, exceto a do Juan, que já existe).
Regra da v3: quadro sem personagem com folha usa a config SEM folha (senão o Codex enfia o personagem na cena).
Pessoas reais: figuras históricas mortas, desenhadas com respeito; a aparência é inspirada em fotos de época, não retrato.
"""

DESC = {
    # --- Operación Garbo ---
    "JUAN": "JUAN (slim Spanish man about 30, oval face, high receding hairline, dark slicked-back hair, thin pencil "
            "mustache, thick dark eyebrows, gray double-breasted suit, dark red tie, dark trench coat and trilby hat "
            "when outdoors)",
    "ARACELI": "ARACELI (Spanish woman about 27, oval face, large dark eyes, dark wavy shoulder-length 1940s hair, "
               "red lipstick, dark green fitted 1940s dress with a small brooch, cream coat when outdoors)",
    "HARRIS": "TOMAS (British-Spanish man about 35, round friendly face, dark wavy hair combed back, dark eyes, "
              "clean-shaven, warm smile, brown tweed jacket, open collar or loose dark tie, often a cigarette)",
    "KUHLENTHAL": "the German officer KUHLENTHAL (very tall and thin man about 34, long narrow face, blond hair parted "
                  "to the side, pale eyes, cold polite smile, civilian dark charcoal suit, no insignia)",
    # --- La Cosa ---
    "HARRIMAN": "HARRIMAN (tall lean American diplomat about 53, long narrow face, dark hair graying at the temples, "
                "heavy dark eyebrows, deep-set eyes, serious expression, dark three-piece suit, white shirt, dark tie)",
    "THEREMIN": "THEREMIN (Russian inventor about 49, slim, thin intelligent face, dark hair combed straight back, "
                "high forehead, tired kind eyes, clean-shaven, worn gray work jacket over a white shirt)",
    "KENNAN": "KENNAN (slim American diplomat about 48, thin face, high forehead with receding hairline, short neat "
              "dark-blond hair, clean-shaven, thoughtful eyes, rimless glasses only when reading, gray suit, "
              "dark tie)",
    "PIONEROS": "the PIONEERS (a group of Soviet schoolchildren aged 10 to 12, boys and girls, white shirts and "
                "blouses, bright red neckerchiefs tied at the neck, neatly combed hair, girls with braids and white "
                "ribbons)",
    "NKVD": "the NKVD man (fictional Soviet security officer about 40, broad square face, short dark hair, thick "
            "dark mustache, small cold eyes, long dark gray overcoat, dark fur hat outdoors)",
    "TECNICO": "the TECHNICIAN (American embassy technician about 35, compact build, dark hair cut short, "
               "headphones around his neck, white shirt with sleeves rolled up, dark trousers)",
    "LODGE": "LODGE (tall handsome American ambassador about 58, strong jaw, wavy graying hair combed back, "
             "clean-shaven, dark suit, white pocket square)",
}

# chave → (arquivo da folha, já existe?)
FOLHA = {
    "JUAN": ("/home/hermes/workspace/fabrica-youtube/canais/dossie-es/produtos/hq/arte-v2/folha-cor.jpg", True),
    "ARACELI": ("folha-araceli.jpg", False),
    "HARRIS": ("folha-harris.jpg", False),
    "KUHLENTHAL": ("folha-kuhlenthal.jpg", False),
    "HARRIMAN": ("folha-harriman.jpg", False),
    "THEREMIN": ("folha-theremin.jpg", False),
    "KENNAN": ("folha-kennan.jpg", False),
    "PIONEROS": ("folha-pioneros.jpg", False),
    "NKVD": ("folha-nkvd.jpg", False),
}
# sem folha (aparecem em poucos quadros; só a descrição fixa): TECNICO, LODGE
