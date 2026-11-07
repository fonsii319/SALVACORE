import math
import os
from collections import deque
import pygame

ASSETS = os.path.join(os.path.dirname(__file__), "assets")
TRIO_PATH = os.path.join(ASSETS, "trio.png")
COIN_PATH = os.path.join(ASSETS, "satochi.png")
CADEJOS_PATH = os.path.join(ASSETS, "cadejos.png")

TECOLOTE_REGION = (1080, 118, 415, 632)
CADEJO_SCALE = 0.5

# (y inicial, alto, columnas x, ancho) de cada animación en cadejos.png
CADEJO_ROWS = {
    "blanqui": {
        "idle": (56, 118, [462, 612, 757, 902], 145),
        "walk": (216, 105, [462, 612, 757, 902], 145),
        "run": (360, 95, [462, 612, 757, 902], 145),
        "die": (380, 78, [1145, 1318, 1495], 150),
    },
    "darky": {
        "idle": (515, 118, [462, 612, 757, 902], 145),
        "walk": (668, 110, [462, 612, 757, 902], 145),
        "run": (824, 100, [462, 612, 757, 902], 145),
        "die": (845, 82, [1145, 1318, 1495], 150),
    },
}


def _remove_bg(surf, tol=12):
    w, h = surf.get_size()
    bg = surf.get_at((0, 0))
    seen = set()
    q = deque()
    for pos in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        q.append(pos)
        seen.add(pos)
    while q:
        x, y = q.popleft()
        c = surf.get_at((x, y))
        if abs(c.r - bg.r) + abs(c.g - bg.g) + abs(c.b - bg.b) > tol * 3:
            continue
        surf.set_at((x, y), (0, 0, 0, 0))
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in seen:
                seen.add((nx, ny))
                q.append((nx, ny))
    return surf


def _scale(surf, s):
    w, h = surf.get_size()
    return pygame.transform.smoothscale(surf, (max(1, round(w * s)), max(1, round(h * s))))


def _scale_h(surf, h):
    return _scale(surf, h / surf.get_height())


def _load_cadejo(img, rows):
    frames = {}
    for anim, (y0, h, xs, w) in rows.items():
        lista = []
        for x in xs:
            crop = pygame.Surface((w, h), pygame.SRCALPHA)
            crop.blit(img, (0, 0), pygame.Rect(x, y0, w, h))
            crop = _remove_bg(crop)
            box = crop.get_bounding_rect()
            if box.w and box.h:
                lista.append(_scale(crop.subsurface(box).copy(), CADEJO_SCALE))
        frames[anim] = lista
    return frames


def load_sprites():
    sprites = {}

    trio = pygame.image.load(TRIO_PATH)
    r = pygame.Rect(TECOLOTE_REGION)
    crop = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
    crop.blit(trio, (0, 0), r)
    sprites["tecolote"] = _scale_h(_remove_bg(crop), 230)

    cad = pygame.image.load(CADEJOS_PATH)
    for nombre, rows in CADEJO_ROWS.items():
        sprites[nombre] = _load_cadejo(cad, rows)
    return sprites


def load_coin(size=28):
    img = pygame.image.load(COIN_PATH).convert_alpha()
    img = pygame.transform.smoothscale(img, (128, 128))
    img = _remove_bg(img)
    return pygame.transform.scale(img, (size, size))


def draw_satochi(surf, rect, img, t):
    bob = int(2 * math.sin(t / 10))
    center = (rect.centerx, rect.centery + bob)
    glow = pygame.Surface((44, 44), pygame.SRCALPHA)
    pygame.draw.circle(glow, (255, 200, 40, 50), (22, 22), 20)
    surf.blit(glow, glow.get_rect(center=center))
    surf.blit(img, img.get_rect(center=center))


def draw_tecolote(surf, cx, cy, img):
    surf.blit(img, img.get_rect(midbottom=(cx, cy + 110)))


def draw_howl(surf, pos, facing, t):
    hx = pos.centerx + 18 * facing
    hy = pos.top + 16
    grosor_extra = (t // 6) % 2 * 3
    for i in range(3):
        r = 12 + i * 8 + grosor_extra
        if facing > 0:
            inicio, fin = -0.6, 0.6
        else:
            inicio, fin = math.pi - 0.6, math.pi + 0.6
        pygame.draw.arc(surf, (230, 240, 255), (hx - r, hy - r, 2 * r, 2 * r), inicio, fin, 2)


def draw_cadejo_anim(surf, p, t):
    sheet = p.sprite
    if p.dying:
        frames = sheet["die"]
        prog = 1 - p.dying / p.death_total
        frame = frames[min(len(frames) - 1, int(prog * len(frames)))]
    elif p.anim == "jump":
        frame = sheet["run"][1]
    elif p.anim == "walk":
        frame = sheet["walk"][(t // 6) % len(sheet["walk"])]
    else:
        frame = sheet["idle"][(t // 14) % len(sheet["idle"])]

    if p.facing < 0:
        frame = pygame.transform.flip(frame, True, False)

    pos = frame.get_rect(midbottom=(p.rect.centerx, p.rect.bottom + 4))
    shadow = pygame.Rect(pos.x + 6, p.rect.bottom - 4, pos.w - 12, 8)
    pygame.draw.ellipse(surf, (10, 10, 20), shadow)
    surf.blit(frame, pos)

    if p.howl:
        draw_howl(surf, pos, p.facing, t)