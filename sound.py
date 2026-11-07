import math
import random
from array import array
import pygame

pygame.mixer.pre_init(44100, -16, 1, 512)
RATE = 44100

SFX = {}
MUSIC = None


def _tone(freq, dur, wave="square", vol=0.3, slide=0.0, decay=True):
    n = int(RATE * dur)
    if freq == 0:
        return array("h", [0]) * n
    buf = array("h")
    phase = 0.0
    for i in range(n):
        f = freq + slide * (i / n)
        phase += f / RATE
        frac = phase % 1.0
        if wave == "square":
            s = 1.0 if frac < 0.5 else -1.0
        elif wave == "tri":
            s = 4 * abs(frac - 0.5) - 1
        elif wave == "noise":
            s = random.uniform(-1, 1)
        else:
            s = math.sin(2 * math.pi * frac)
        env = (1 - i / n) if decay else 1.0
        buf.append(int(max(-1, min(1, s * vol * env)) * 32767))
    return buf


def _concat(parts):
    out = array("h")
    for p in parts:
        out.extend(p)
    return out


def _mix(a, b):
    n = max(len(a), len(b))
    out = array("h", [0]) * n
    for i in range(n):
        v = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
        out[i] = max(-32767, min(32767, v))
    return out


def _make_sound(buf):
    return pygame.mixer.Sound(buffer=buf.tobytes())


def load_audio():
    global MUSIC
    if not pygame.mixer.get_init():
        return
    SFX["jump"] = _make_sound(_tone(260, 0.18, "square", 0.2, slide=420))
    SFX["step"] = _make_sound(_tone(90, 0.05, "noise", 0.18))
    SFX["coin"] = _make_sound(_concat([
        _tone(988, 0.07, "square", 0.2, decay=False),
        _tone(1319, 0.18, "square", 0.2),
    ]))
    SFX["howl"] = _make_sound(_tone(350, 1.4, "sine", 0.4, slide=400))
    SFX["death"] = _make_sound(_tone(380, 0.9, "tri", 0.35, slide=-300))

    melodia_notas = [220, 261.63, 329.63, 293.66, 261.63, 246.94, 220, 0,
                     220, 261.63, 329.63, 349.23, 329.63, 293.66, 261.63, 0]
    bajo_notas = [110, 110, 82.41, 82.41, 87.31, 87.31, 110, 110,
                  110, 110, 82.41, 82.41, 87.31, 87.31, 82.41, 82.41]
    melodia = _concat(_tone(f, 0.25, "square", 0.08) for f in melodia_notas)
    bajo = _concat(_tone(f, 0.25, "tri", 0.14, decay=False) for f in bajo_notas)
    MUSIC = _make_sound(_mix(melodia, bajo))
    MUSIC.set_volume(0.35)


def play(nombre, vol=1.0):
    s = SFX.get(nombre)
    if s:
        s.set_volume(vol)
        s.play()


def start_music():
    if MUSIC:
        MUSIC.play(-1)

        