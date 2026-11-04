# Original ambient bed (no samples): slow modal chord pads + sparse harp-like plucks + drone.
import numpy as np, soundfile as sf, sys
SR = 24000; DUR = float(sys.argv[2]); N = int(SR*DUR)
rng = np.random.default_rng(7)
t = np.arange(N)/SR
def midi(m): return 440*2**((m-69)/12)
# D dorian-ish progression, 10 s per chord
prog = [[50,57,62,65,69],[46,53,58,62,65],[43,50,55,58,62],[45,52,57,61,64],[50,57,62,65,69],[48,55,60,64,67],[46,53,58,62,65],[45,52,57,60,64]]
CH = 10.0
out = np.zeros(N)
nch = int(np.ceil(DUR/CH))+1
for c in range(nch):
    notes = prog[c % len(prog)]
    s0 = int((c*CH-2.5)*SR); L = int((CH+5)*SR)
    a, b = max(0,s0), min(N, s0+L)
    if a >= b: continue
    tt = np.arange(a,b)/SR - c*CH + 2.5
    env = np.clip(tt/3.5,0,1)*np.clip((CH+5-tt)/3.5,0,1)
    env = env**1.5
    seg = np.zeros(b-a)
    for i,m in enumerate(notes):
        f = midi(m)
        for det in (-0.12, 0.0, 0.11):
            ph = rng.uniform(0,2*np.pi)
            fr = f*2**(det/12)
            seg += (np.sin(2*np.pi*fr*tt+ph) + 0.18*np.sin(4*np.pi*fr*tt+ph) + 0.06*np.sin(6*np.pi*fr*tt))*(0.9 if i else 1.3)
    out[a:b] += seg*env*0.03
# drone D2 with slow swell
out += 0.05*np.sin(2*np.pi*midi(38)*t)*(0.6+0.4*np.sin(2*np.pi*t/23))
# plucks
pent = [62,64,65,69,72,74,77,81]
k = 3.0
while k < DUR-3:
    m = pent[rng.integers(len(pent))]; f = midi(m)
    s = int(k*SR); L = int(3.5*SR); e = min(N, s+L); tt = np.arange(e-s)/SR
    out[s:e] += 0.05*np.exp(-tt*1.6)*(np.sin(2*np.pi*f*tt)+0.3*np.sin(4*np.pi*f*tt))*np.clip(tt/0.005,0,1)
    k += rng.choice([1.25,2.5,2.5,3.75,5.0])
# simple reverb: FFT convolve with decaying noise IR
ir_len = int(2.8*SR); ir = rng.standard_normal(ir_len)*np.exp(-np.arange(ir_len)/SR*2.2); ir[0]=0; ir/=np.abs(ir).sum()/6
n2 = 1<<int(np.ceil(np.log2(N+ir_len)))
wet = np.fft.irfft(np.fft.rfft(out,n2)*np.fft.rfft(ir,n2),n2)[:N]
mix = 0.55*out + 0.45*wet
# one-pole lowpass for softness
y = np.empty_like(mix); acc=0.0; al=0.35
# vectorized approx: moving average
kern = np.ones(5)/5; y = np.convolve(mix,kern,'same')
fade = np.clip(t/4,0,1)*np.clip((DUR-t)/5,0,1)
y *= fade; y /= np.abs(y).max()*1.12
L = y; R = np.concatenate([np.zeros(240), y[:-240]])
sf.write(sys.argv[1], np.stack([L,R],1).astype(np.float32), SR)
print('music', DUR)
