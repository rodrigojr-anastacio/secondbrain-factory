#!/usr/bin/env python3
"""VTT automático → texto deduplicado com marca de tempo a cada ~30 s. Uso: vtt2txt.py arq.vtt > arq.txt"""
import re, sys
linhas, vistos, ult = [], set(), -999
t = 0
for l in open(sys.argv[1], encoding='utf-8'):
    m = re.match(r'(\d+):(\d+):(\d+)\.\d+ -->', l)
    if m:
        t = int(m[1]) * 3600 + int(m[2]) * 60 + int(m[3]); continue
    l = re.sub(r'<[^>]+>', '', l).strip()
    if not l or l.startswith(('WEBVTT', 'Kind:', 'Language:')) or l in vistos:
        continue
    vistos.add(l)
    if t - ult >= 30:
        linhas.append(f'\n[{t // 60}:{t % 60:02d}] '); ult = t
    linhas.append(l + ' ')
print(''.join(linhas))
