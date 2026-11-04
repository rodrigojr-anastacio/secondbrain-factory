"""Build V2 word-level captions (Remotion Caption shape) + V2 SRT.

Timings come from transcript_timestamps.json (Whisper); every word's text is
taken from script_fr.txt, which is the authority. Neither input is modified.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
script = open(os.path.join(ROOT, 'script_fr.txt'), encoding='utf-8').read()
data = json.load(open(os.path.join(ROOT, 'transcript_timestamps.json'), encoding='utf-8'))

# Script tokens; standalone punctuation is glued to the previous word.
disp = []
for tok in script.split():
    if tok in ('?', '!', ':', ';') and disp:
        disp[-1] += ' ' + tok
    elif tok == '—' and disp:
        disp[-1] += ' —'
    else:
        disp.append(tok)

# Whisper tokens; fragments ("l" + "'ouest", "a" + "-t" + "-il", "?") are merged.
ws = []
for seg in data['segments']:
    for w in seg['words']:
        t = w['word'].strip()
        if ws and (t.startswith("'") or t.startswith('-') or t in ('?', '!')):
            ws[-1]['end'] = w['end']
            ws[-1]['raw'] += t
        else:
            ws.append({'start': w['start'], 'end': w['end'], 'raw': t})

# Whisper heard "Havres Gris" as one word ("Avregris"): split its span in two.
out = []
for w in ws:
    if w['raw'].lower().startswith('avregris'):
        mid = round((w['start'] + w['end']) / 2, 3)
        out.append({'start': w['start'], 'end': mid, 'raw': w['raw'] + ' (1/2)'})
        out.append({'start': mid, 'end': w['end'], 'raw': w['raw'] + ' (2/2)'})
    else:
        out.append(w)
ws = out

if len(ws) != len(disp):
    print('TOKEN COUNT MISMATCH', len(ws), len(disp))
    for a, b in zip(ws, disp):
        print(a['raw'], '|', b)
    sys.exit(1)

def norm(s):
    return ''.join(ch for ch in s.lower().replace('’', "'") if ch.isalnum() or ch in "'-")

captions = []
corrections = []
for i, (w, text) in enumerate(zip(ws, disp)):
    if norm(w['raw']) != norm(text):
        corrections.append(f"{w['start']:6.2f}s  {w['raw']!r} -> {text!r}")
    start_ms = round(w['start'] * 1000)
    end_ms = round(w['end'] * 1000)
    captions.append({
        'text': (' ' if i else '') + text,
        'startMs': start_ms,
        'endMs': end_ms,
        'timestampMs': round((start_ms + end_ms) / 2),
        'confidence': None,
    })

os.makedirs(os.path.join(ROOT, 'src', 'v2'), exist_ok=True)
with open(os.path.join(ROOT, 'src', 'v2', 'captions_fr.json'), 'w', encoding='utf-8') as f:
    json.dump(captions, f, ensure_ascii=False, indent=2)

# Sanity: concatenated caption text == script text (whitespace-normalised).
joined = ''.join(c['text'] for c in captions).replace(' ', ' ')
assert ' '.join(joined.split()) == ' '.join(script.split()), 'caption text differs from script'

# SRT: phrase cues (<= 46 chars), broken at sentence ends / commas.
cues, cur = [], []
for c in captions:
    t = c['text'].strip()
    if cur and len(' '.join(x['text'].strip() for x in cur + [c])) > 46:
        cues.append(cur); cur = []
    cur.append(c)
    if t.endswith(('.', '?', '!')) or (t.endswith((',', '—')) and len(cur) >= 3):
        cues.append(cur); cur = []
if cur:
    cues.append(cur)

def ts(ms):
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02}:{m:02}:{s:02},{ms:03}'

lines = []
for i, cue in enumerate(cues):
    start = cue[0]['startMs']
    end = cue[-1]['endMs'] + 300
    if i + 1 < len(cues):
        end = min(end, cues[i + 1][0]['startMs'] - 20)
    text = ' '.join(x['text'].strip() for x in cue)
    lines.append(f'{i + 1}\n{ts(start)} --> {ts(end)}\n{text}\n')
srt_path = os.path.join(ROOT, 'out', 'lotr-pilot-v2-fr.srt')
assert not os.path.exists(srt_path) or 'v2' in srt_path
with open(srt_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'{len(captions)} caption words, {len(cues)} SRT cues, {len(corrections)} words corrected against script:')
print('\n'.join(corrections))
