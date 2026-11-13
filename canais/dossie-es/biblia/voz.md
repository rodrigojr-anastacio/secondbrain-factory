# Voz: dossie-es

Regra de canal: **prevalece** sobre `conhecimento/anti-padroes.md`. Configuração em `../canal.yaml` (`voz`).

## Voz do canal
- Fish `s2.1-pro`, **por frase** (`tools/tts_fish.py --por-frase`), velocidade 1.0. Voz `ac594943984a47e7a827416eb263c7b1` ("Dio Historias", neutra, documental), **escolhida pelo Rodrigo em 2026-11-04** (BRIEF-dossie-001). Alternativas em `../testes/voz/LEIA.md`.
- Masculina, acento **neutro** (nem mexicano marcado nem espanhol), documental, seca. Tags: `[serious]` e `[slightly dramatic]`. [canal.yaml]
- Referência Archive [O/I]: narrador masculino neutro, grave e constante; provavelmente TTS de alta qualidade ou clone (sem respiração audível, ritmo regular). [LEVANTAMENTO §2e]

## Pronúncia
- Medido no piloto CIA (04/11): "CIA" sai como "sía" (uso latino); "OSS", "U dos", "PB Success" e "MK Ultra" saem bem. Números sempre por extenso no texto. Whisper 97,8%. Ritmo ~143 ppm (ver `roteiro.md`). [`videos/001-cia/RELATORIO.md`]
- Medido no 002 Mossad (05/11): Whisper 96,4%. "Mossad", "MiG veintiuno", "cero cero siete", "Knéset", "Yom Kipur" saem bem; nomes hebraicos/árabes/letões saem aceitáveis, mas o Whisper grafa mal (Shiloaj, Zamir, Marwan, Cukurs, Hatzerim): conferir de ouvido, não regerar. [`videos/002-mossad/QA.md`]
- Medido no 004 Cosa Nostra (05/11): Whisper 96,5%. Nomes italianos saem à espanhola ("Buscetta" → "Buseta", "Schifani" → "Shifani" ok, "Riina" → "Rina"); aceitável em es, conferir de ouvido, não regerar. [`videos/004-cosa-nostra/QA.md`]
- Medido no 005 KGB (09/11): Whisper 97,2%. "KGB", "NKVD", "GPU" saem bem ("OGPU" sai "o-ge-pe-u"); nomes russos com "zh" (Dzerzhinski, Yezhov, Zhivkov) e "Cheká" saem aceitáveis à espanhola; o Whisper grafa "Checa", "Lubianca", "Jezov": conferir de ouvido, não regerar. [`videos/005-kgb/QA.md`]
- Medido no 006 Masones (09/11): Whisper 97,2%. Nomes ingleses (Mainwaring, Sayer, Wirt, Vaughan), "In eminenti", "Jakim Boor/Jakín" e "Sáenz" saem aceitáveis; o Whisper ouve "logias" como "lojas" e "la masonería" como "l'amazonería" (junção): conferir de ouvido, não regerar. **Modelo cobrado:** a API do Fish não expõe histórico de uso (testados 7 endpoints `wallet/self/*`, 404/401); com outro job no Fish, concilie a queda do crédito com as linhas de `financas.consumo` dos dois jobs no período (006: queda 0,333 = 0,178 s2.1-pro + ~0,152 drama-3 da Rússia; se fosse drama-3 seriam ~0,27). [`videos/006-masones/RELATORIO.md`]
- Medido no 007 SS (13/11): Whisper 95,6%. **"SS" escrito como sigla sai certo** (teste: "las SS" e "las ese ese" deram o mesmo áudio, 2,4 s; "S S" com espaço saiu "Sur, Sur": nunca separe). O Whisper grafa "SS/SA" como "s s", "ses", "la csa", e nomes alemães à espanhola (Röhm "Rom", Einsatzgruppen "ansas grupen", Wannsee "Juan c", Priebke "Priepke"): conferir de ouvido, não regerar. Ouviu "September" no início de um bloco ("Septiembre de 1939"): conferir. [`videos/007-ss/QA.md`]
- Siglas como no uso latino ("la ce-i-a", "el ka-ge-be", "el efe-be-i"); confira na 1ª amostra do roteiro.
- Números por extenso quando o Fish ler mal; datas "27 de junio de 1954".
- **Whisper por bloco ≥ 95%** depois da voz; nomes próprios conferidos à parte. [estilo.md de 04/11]
- Medido no 008 Inquisición (13/11): Whisper 97,9% (média; 8 blocos < 93%, todos grafia). Respelling do Fish funcionou ('Ometóch-tsin', 'Tescóco', 'Sugarra-múrdi', 'Yorénte', 'Ripóy', 'Tulús'); o Whisper ouviu 'Gui' como 'Guy' e 'Zumárraga' ('Sumárraga') quebrado em 'su ma raga': conferir de ouvido. Aspas «» e algarismo romano por extenso saem bem. Custo da voz de 14 min: US$ 0,18. [`videos/008-inquisicion/QA.md`]

## Não faça
- Vozes que imitam pessoas reais (dubladores, políticos, Iker Jiménez) nem a voz de TikTok mais usada (`locutor k`).
- O clone pt-BR do Rodrigo (é do `historia-ptbr`) ou tom caloroso de contador de história.
