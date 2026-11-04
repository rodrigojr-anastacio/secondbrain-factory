"""Create an original, royalty-free 60-second folk-cinematic music bed for V3.

No samples, melodies, or material from the Lord of the Rings films are used.
The score uses a slow D-major/B-minor harmonic palette, soft sustained tones,
and a sparse plucked motif. Narration ducking is applied in Remotion.
"""
import array
import math
import os
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "assets", "v3", "music_bed_v3.wav")
SR = 22050
DURATION = 60.0
N = int(SR * DURATION)
left = [0.0] * N
right = [0.0] * N

# Open voicings: Bm(add9), Gmaj7, D(add9), Asus2, then a softer return.
CHORDS = [
    (73.42, 110.00, 146.83, 220.00),
    (98.00, 123.47, 146.83, 185.00),
    (73.42, 110.00, 146.83, 164.81),
    (55.00, 82.41, 110.00, 146.83),
    (73.42, 110.00, 146.83, 220.00),
    (98.00, 123.47, 146.83, 196.00),
    (73.42, 110.00, 146.83, 185.00),
    (73.42, 110.00, 146.83, 164.81),
]
SEGMENT = DURATION / len(CHORDS)
FADE = 1.7


def smooth_envelope(t, start, end):
    x = min(1.0, max(0.0, (t - start) / FADE), max(0.0, (end - t) / FADE))
    return 0.5 - 0.5 * math.cos(math.pi * x) if x > 0 else 0.0


def dynamics(t):
    # Start spare, warm through the family section, thin under the loss,
    # swell gently for the western journey, then leave the ending unresolved.
    if t < 5:
        return 0.48 + 0.035 * t
    if t < 18:
        return 0.66
    if t < 25:
        return 0.42
    if t < 43:
        return 0.68
    if t < 52:
        return 0.43
    return 0.53


for section, chord in enumerate(CHORDS):
    start = section * SEGMENT
    end = (section + 1) * SEGMENT
    i0 = max(0, int(start * SR))
    i1 = min(N, int(end * SR))
    for voice, freq in enumerate(chord):
        phase_l = 0.29 * voice
        phase_r = phase_l + 0.31
        amp = (0.20, 0.15, 0.12, 0.08)[voice]
        for i in range(i0, i1):
            t = i / SR
            env = smooth_envelope(t, start, end)
            if env <= 0:
                continue
            wobble = 0.92 + 0.08 * math.sin(2 * math.pi * 0.085 * t + voice)
            a = amp * env * wobble * dynamics(t)
            l = math.sin(2 * math.pi * freq * t + phase_l) + 0.12 * math.sin(4 * math.pi * freq * t + phase_l)
            r = math.sin(2 * math.pi * (freq * 1.0015) * t + phase_r) + 0.10 * math.sin(4 * math.pi * freq * t + phase_r)
            left[i] += a * l
            right[i] += a * r

# A simple original plucked-string motif in D major; the long gaps keep it
# lyrical rather than busy. The final notes intentionally avoid a hard cadence.
D4, E4, F4s, A4, B4, D5, E5, F5s = 293.66, 329.63, 369.99, 440.00, 493.88, 587.33, 659.25, 739.99
MELODY = (D5, A4, F4s, B4, A4, D5, E5, B4, F4s, A4, D5, B4, A4, E4, F4s, A4, D5, B4, F4s, E4)
for note_index, freq in enumerate(MELODY):
    onset = 0.9 + note_index * 2.9
    if onset >= DURATION:
        continue
    i0 = int(onset * SR)
    count = min(int(1.9 * SR), N - i0)
    for j in range(count):
        t = j / SR
        envelope = math.exp(-2.7 * t) * min(1.0, t / 0.018)
        phase = 2 * math.pi * freq * t
        tone = (0.74 * math.sin(phase) + 0.20 * math.sin(2.01 * phase + 0.12) + 0.06 * math.sin(3.98 * phase + 0.31))
        gain = 0.18 * envelope * dynamics(onset + t)
        pan = 0.5 + 0.28 * math.sin(note_index * 0.83)
        left[i0 + j] += tone * gain * (1.0 - pan)
        right[i0 + j] += tone * gain * pan

# Gentle fade-in/out and peak-safe stereo PCM export.
for i in range(N):
    t = i / SR
    edge = min(1.0, t / 1.8, (DURATION - t) / 2.4)
    left[i] *= edge
    right[i] *= edge

peak = max(max(abs(x) for x in left), max(abs(x) for x in right)) or 1.0
gain = 0.72 / peak
with wave.open(OUT, "wb") as wav:
    wav.setnchannels(2)
    wav.setsampwidth(2)
    wav.setframerate(SR)
    frames = array.array("h")
    for l, r in zip(left, right):
        frames.append(int(max(-1.0, min(1.0, l * gain)) * 32767))
        frames.append(int(max(-1.0, min(1.0, r * gain)) * 32767))
    wav.writeframes(frames.tobytes())

print(f"Wrote {OUT}: {DURATION:.1f}s stereo, {SR} Hz; peak={20 * math.log10(0.72):.1f} dBFS")
