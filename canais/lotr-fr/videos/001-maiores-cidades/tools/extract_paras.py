import re, json, sys
src = open(sys.argv[1], encoding='utf-8').read()
paras = {}
blocks = re.split(r'\n\*\*(P\d+b?)\*\*[^\n]*\n', src)
# blocks: [pre, id, body, id, body...]
for i in range(1, len(blocks), 2):
    pid, body = blocks[i], blocks[i+1]
    body = body.split('\n---')[0].split('\n## ')[0]
    if pid == 'P18b':
        m = re.search(r"\*Repli[^:]*:\*\s*(.+)", body)
        body = m.group(1)
    body = re.sub(r'\s*\[S-\d+b?\]', '', body)
    lines = [l.strip() for l in body.strip().split('\n') if l.strip()]
    paras[pid] = ' '.join(lines)
json.dump(paras, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in paras.items(): print(k, len(v.split()), v[:90])
print('TOTAL words', sum(len(v.split()) for v in paras.values()))
