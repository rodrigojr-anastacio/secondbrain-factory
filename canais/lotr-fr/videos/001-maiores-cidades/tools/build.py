# Builds the master timeline (src/timeline.json), captions (out/cidades-fr.srt),
# the narration+music mix (public/audio/mix.wav) and STORYBOARD.md.
# Run with ~/tts/venv-kokoro/bin/python (numpy + soundfile).
import json, re, sys, os, subprocess
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(__file__))
from storyboard import S, CARDS, CROWN

FPS, SR = 30, 24000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
timing = json.load(open('audio/timing.json', encoding='utf-8'))
order = list(timing.keys())
credits = json.load(open('assets_credits.json', encoding='utf-8'))

LEAD, GAP, CARD, TAIL = 0.8, 0.85, 2.6, 5.5
start, t = {}, LEAD
cards = []
for pid in order:
    if pid in CARDS:
        cards.append({'from': t + 0.1, 'dur': CARD - 0.2, 'title': CARDS[pid][0], 'sub': CARDS[pid][1]})
        t += CARD
    start[pid] = t
    t += timing[pid]['duration'] + GAP
total = t - GAP + TAIL
frames = int(round(total * FPS))

# ---------- shots
shots = []
for pid, si, off, kind, p in S:
    at = start[pid] + timing[pid]['sentences'][si]['start'] + off - 0.12
    shots.append({'t': max(0, at), 'kind': kind, 'pid': pid, **p})
shots.sort(key=lambda s: s['t'])
shots[0]['t'] = 0
# insert era cards as their own shots
for c in cards:
    shots.append({'t': c['from'] - 0.1, 'kind': 'card', 'title': c['title'], 'sub': c['sub']})
shots.sort(key=lambda s: s['t'])
end_t = start[order[-1]] + timing[order[-1]]['duration'] + 0.6
shots.append({'t': end_t, 'kind': 'end'})
for i, s in enumerate(shots):
    nxt = shots[i + 1]['t'] if i + 1 < len(shots) else total
    s['from'] = int(round(s['t'] * FPS)); s['dur'] = int(round(nxt * FPS)) - s['from']
    if s.get('img'):
        c = credits[s['img']]
        artist = re.sub(r'\s*\(.*?\)\s*$', '', c['artist']).strip()
        artist = {'National Park Service Digital Image Archives': 'U.S. National Park Service'}.get(artist, artist)
        lic = 'domaine public' if c['license'].lower() in ('public domain', 'cc0', 'no restrictions') else c['license']
        s['credit'] = f"{artist} · {lic}"
    if s['kind'] == 'map':
        s['credit'] = 'Carte schématique originale · pas à l’échelle'

for s in shots:
    if s['kind'] == 'recap':
        if s.get('final'):
            s['steps'] = [{'at': int(a * FPS) + 6, 'a': x, 'b': y} for a, x, y in s['steps']]
        else:
            s['steps'] = [{'at': max(6, int(round((start[s['pid']] + timing[s['pid']]['sentences'][k]['start'] - s['t']) * FPS))), 'a': x, 'b': y} for k, x, y in s['steps']]
# crown timeline
crown = []
for s in shots:
    if 'crown' in s and s['crown']:
        crown.append({'from': s['from'], 'name': CROWN[s['crown']][0], 'era': CROWN[s['crown']][1]})

# ---------- captions: split sentences into ≤ 2-line cues
def chunks(text, maxc=84):
    if len(text) <= maxc: return [text]
    words, out, cur = text.split(), [], ''
    # prefer breaks after punctuation near the middle
    parts = re.split(r'(?<=[,:;])\s+', text)
    if all(len(x) <= maxc for x in parts) and len(parts) > 1:
        res, cur = [], ''
        for x in parts:
            if cur and len(cur) + 1 + len(x) > maxc: res.append(cur); cur = x
            else: cur = (cur + ' ' + x).strip()
        res.append(cur); return res
    for w in words:
        if cur and len(cur) + 1 + len(w) > maxc: out.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    out.append(cur); return out

caps = []
for pid in order:
    for s in timing[pid]['sentences']:
        a, b = start[pid] + s['start'], start[pid] + s['end']
        cs = chunks(s['text']); tot = sum(len(c) for c in cs); x = a
        for c in cs:
            d = (b - a) * len(c) / tot
            caps.append({'text': c, 'start': round(x, 3), 'end': round(x + d, 3)}); x += d
for i, c in enumerate(caps):  # hold briefly into the pause, never into the next cue
    nxt = caps[i + 1]['start'] if i + 1 < len(caps) else c['end'] + 1
    c['end'] = round(min(c['end'] + 0.25, nxt - 0.04), 3)

def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
def wrap2(t, n=44):
    if len(t) <= n: return t
    best = min((abs(i - len(t) / 2), i) for i, ch in enumerate(t) if ch == ' ')[1]
    return t[:best] + '\n' + t[best + 1:]
os.makedirs('out', exist_ok=True)
with open('out/cidades-fr.srt', 'w', encoding='utf-8') as f:
    for i, c in enumerate(caps, 1):
        f.write(f"{i}\n{ts(c['start'])} --> {ts(c['end'])}\n{wrap2(c['text'])}\n\n")

json.dump({'fps': FPS, 'frames': frames, 'shots': shots, 'crown': crown,
           'captions': [{'from': int(round(c['start'] * FPS)), 'to': int(round(c['end'] * FPS)), 'text': c['text']} for c in caps]},
          open('src/timeline.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# ---------- audio mix: narration + original music bed with ducking
N = int(total * SR)
voice = np.zeros(N, np.float32)
for pid in order:
    a, sr = sf.read(f'audio/paras/{pid}.wav', dtype='float32'); assert sr == SR
    i = int(start[pid] * SR); voice[i:i + len(a)] += a[:N - i]
music_path = 'audio/music.wav'
if not os.path.exists(music_path) or abs(sf.info(music_path).duration - total) > 0.5:
    subprocess.run([sys.executable, 'tools/make_music.py', music_path, str(total)], check=True)
mus, sr = sf.read(music_path, dtype='float32'); mus = mus[:N]
if len(mus) < N: mus = np.pad(mus, ((0, N - len(mus)), (0, 0)))
# ducking envelope from voice activity (paragraph-level: duck while a paragraph is playing)
act = np.zeros(N, np.float32)
for pid in order:
    i = int(start[pid] * SR); j = i + int(timing[pid]['duration'] * SR); act[i:j] = 1
k = int(0.5 * SR); ker = np.ones(k, np.float32) / k
act = np.convolve(act, ker, 'same')
gain = 0.30 - (0.30 - 0.085) * np.clip(act, 0, 1)   # music ~-10.5 dB in gaps, ~-21 dB under voice
mix = mus * gain[:, None] + voice[:, None] * 0.92
peak = np.abs(mix).max()
if peak > 0.97: mix *= 0.97 / peak
os.makedirs('public/audio', exist_ok=True)
sf.write('audio/mix_raw.wav', mix, SR)
subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', 'audio/mix_raw.wav', '-af',
                'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '48000', 'public/audio/mix.wav'], check=True)

# ---------- STORYBOARD.md
def fmt(x): return f'{int(x // 60)}:{x % 60:04.1f}'
with open('STORYBOARD.md', 'w', encoding='utf-8') as f:
    f.write(f'# STORYBOARD — généré par tools/build.py\n\nDurée totale : {fmt(total)} ({frames} frames @30 fps).\n\n')
    f.write('| # | Début | Durée | Type | Visuel | Texte à l’écran | Crédit |\n|---|---|---|---|---|---|---|\n')
    for i, s in enumerate(shots, 1):
        vis = s.get('img') or (('carte ' + s.get('view', '')) if s['kind'] == 'map' else s['kind'])
        kw = ' / '.join(x for x in (s.get('kw') or ()) if x) if s.get('kw') else (s.get('title', '') if s['kind'] == 'card' else '')
        if s.get('crown'): kw += f" · couronne → {CROWN[s['crown']][0]}"
        f.write(f"| {i} | {fmt(s['from'] / FPS)} | {s['dur'] / FPS:.1f}s | {s['kind']} | {vis} | {kw} | {s.get('credit', '')} |\n")
print(f'total {total:.2f}s frames {frames} shots {len(shots)} caps {len(caps)}')
long = [(round(s['from'] / FPS, 1), round(s['dur'] / FPS, 1), s.get('img') or s['kind']) for s in shots if s['dur'] / FPS > 9]
print('shots >9s:', long)
