from faster_whisper import WhisperModel
from pathlib import Path
import json
p='/home/hermes/workspace/lotr-pilot/public/assets/narration.wav'
m=WhisperModel('base',device='cpu',compute_type='int8')
segments,info=m.transcribe(p,language='fr',beam_size=5,word_timestamps=True)
rows=[]
for s in segments:
 rows.append({'start':s.start,'end':s.end,'text':s.text.strip(),'words':[{'start':w.start,'end':w.end,'word':w.word} for w in (s.words or [])]})
out=Path('/home/hermes/workspace/lotr-pilot/transcript_timestamps.json')
out.write_text(json.dumps({'language':info.language,'probability':info.language_probability,'segments':rows},ensure_ascii=False,indent=2))
print(json.dumps({'language':info.language,'probability':info.language_probability,'segments':[{'start':x['start'],'end':x['end'],'text':x['text']} for x in rows]},ensure_ascii=False))
