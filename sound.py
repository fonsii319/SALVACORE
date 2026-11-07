import math
import random
from array import array
import pygame

RATE = 44100
pygame.mixer.pre_init(RATE, -16, 1, 512)

TWO_PI = 2 * math.pi
BPM = 88
BARS = 8
SFX = {}
MUSIC = None

# Progresión tenebrosa: Am - F - Dm - E (con Si bemol y Sol sostenido)
BASS = [110, 87.31, 73.42, 82.41, 110, 87.31, 73.42, 82.41]
MELODY = [
    [440, None, 523.25, 440, 392, None, 329.63, None],
    [349.23, None, 440, 523.25, 440, None, 349.23, None],
    [293.66, None, 349.23, 293.66, 233.08, None, 293.66, None],
    [329.63, None, 415.30, 329.63, 246.94, None, 329.63, None],
    [440, 523.25, None, 587.33, 523.25, None, 440, None],
    [349.23, None, 440, None, 392, 349.23, 329.63, None],
    [293.66, None, 233.08, 261.63, 293.66, None, 220, None],
    [329.63, None, 246.94, None, 329.63, 415.30, 329.63, None],
]


def _wave(phase, kind):
    frac = phase % 1.0
    if kind == "square":
        return 1.0 if frac < 0.5 else -1.0
    if kind == "tri":
        return 4 * abs(frac - 0.5) - 1
    return math.sin(TWO_PI * frac)


def _sweep(f0, f1, dur, vol, kind="sine", decay=0.0):
    n = int(RATE * dur)
    out, phase = [], 0.0
    for i in range(n):
        f = f0 + (f1 - f0) * (i / n)
        phase += f / RATE
        out.append(_wave(phase, kind) * vol * math.exp(-decay * i / RATE))
    return out


def _noise(dur, vol, decay):
    n = int(RATE * dur)
    return [random.uniform(-1, 1) * vol * math.exp(-decay * i / RATE) for i in range(n)]


def _pluck(freq, dur, vol, decay=7.0):
    n = int(RATE * min(dur, 5.0 / decay))
    w = TWO_PI * freq / RATE
    out = []
    for i in range(n):
        env = math.exp(-decay * i / RATE)
        s = math.sin(w * i) + 0.35 * math.sin(2 * w * i) + 0.12 * math.sin(3 * w * i)
        out.append(s * env * vol)
    return out


def _kick(vol=0.45, dur=0.22):
    n = int(RATE * dur)
    out, phase = [], 0.0
    for i in range(n):
        t = i / RATE
        phase += (110 * math.exp(-14 * t) + 42) / RATE
        out.append(math.sin(TWO_PI * phase) * math.exp(-12 * t) * vol)
    return out


def _to_sound(samples, peak=0.9):
    m = max(1e-9, max(abs(x) for x in samples))
    k = peak * 32767 / m
    buf = array("h", [int(x * k) for x in samples])
    return pygame.mixer.Sound(buffer=buf.tobytes())


def _add(buf, start, samples):
    # Envuelve al inicio del loop para que las colas de las notas no se corten
    n = len(buf)
    i0 = int(start * RATE)
    for i, v in enumerate(samples):
        buf[(i0 + i) % n] += v


def _build_music():
    beat = 60.0 / BPM
    total = int(RATE * BARS * 4 * beat)
    buf = [0.0] * total

    # Drone oscuro: La y Mi, con respiración lenta
    for i in range(total):
        t = i / RATE
        lfo = 0.6 + 0.4 * math.sin(TWO_PI * 0.25 * t)
        buf[i] += 0.04 * lfo * (math.sin(TWO_PI * 110 * t) + 0.5 * math.sin(TWO_PI * 164.81 * t))

    kick = _kick()
    rim = _noise(0.06, 0.1, 80)

    for bar in range(BARS):
        t0 = bar * 4 * beat
        for k in range(8):
            note = MELODY[bar][k]
            if note:
                start = t0 + k * beat / 2
                _add(buf, start, _pluck(note, 0.9, 0.16))
                _add(buf, start, _pluck(note * 1.004, 0.9, 0.07))  # desafinado leve
        for b in (0, 2):
            _add(buf, t0 + b * beat, _pluck(BASS[bar], 1.2, 0.28, decay=2.5))
            _add(buf, t0 + b * beat, kick)
        for b in (1, 3):
            _add(buf, t0 + b * beat, rim)

    return _to_sound(buf, peak=0.85)


def load_audio():
    global MUSIC
    if not pygame.mixer.get_init():
        return
    SFX["jump"] = _to_sound(_sweep(260, 620, 0.16, 0.25, "square", decay=10))
    SFX["step"] = _to_sound(_noise(0.05, 0.2, 60))
    SFX["coin"] = _to_sound(
        _sweep(988, 988, 0.06, 0.2, "square")
        + _sweep(1319, 1319, 0.18, 0.2, "square", decay=12))
    SFX["howl"] = _to_sound(_sweep(350, 520, 1.4, 0.35, "sine", decay=1.2))
    SFX["death"] = _to_sound(_sweep(380, 90, 0.9, 0.35, "tri", decay=2.5))
    MUSIC = _build_music()
    MUSIC.set_volume(0.45)


def play(nombre, vol=1.0):
    s = SFX.get(nombre)
    if s:
        s.set_volume(vol)
        s.play()


def start_music():
    if MUSIC:
        MUSIC.play(-1)
        
