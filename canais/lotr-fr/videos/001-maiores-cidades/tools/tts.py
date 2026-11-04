import sys, json, time, re, numpy as np, soundfile as sf
from kokoro import KPipeline
paras = json.load(open(sys.argv[1], encoding='utf-8'))
outdir, speed = sys.argv[2], float(sys.argv[3])
pipe = KPipeline(lang_code='f', repo_id='hexgrad/Kokoro-82M')
SR = 24000
timing = {}
for pid, text in paras.items():
    sents = [s.strip() for s in re.split(r'(?<=[.?!…])\s+', text) if s.strip()]
    parts, segs, t = [], [], 0.0
    for s in sents:
        a = np.concatenate([x for _, _, x in pipe(s, voice='ff_siwis', speed=speed)])
        # trim leading/trailing near-silence
        idx = np.where(np.abs(a) > 0.01)[0]
        if len(idx): a = a[max(0, idx[0]-240): idx[-1]+1200]
        gap = 0.55 if s.endswith(('?', '…')) else 0.38
        segs.append({'text': s, 'start': round(t, 3), 'end': round(t + len(a)/SR, 3)})
        parts += [a, np.zeros(int(gap*SR), dtype=a.dtype)]
        t += len(a)/SR + gap
    audio = np.concatenate(parts[:-1])
    sf.write(f'{outdir}/{pid}.wav', audio, SR)
    timing[pid] = {'duration': round(len(audio)/SR, 3), 'sentences': segs}
    print(f'{pid}: {len(audio)/SR:.1f}s', flush=True)
json.dump(timing, open(f'{outdir}/../timing.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('TOTAL', sum(v['duration'] for v in timing.values()))
