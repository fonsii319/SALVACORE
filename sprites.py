import os
from collections import deque
import pygame
import math

IMG_PATH = os.path.join(os.path.dirname(__file__), "assets", "trio.png")

# Zonas (x, y, ancho, alto) de cada personaje dentro de trio.png
REGIONS = {
    "blanqui": (30, 180, 460, 565),
    "darky": (555, 175, 460, 565),
    "tecolote": (1080, 118, 415, 632),
}


def _remove_bg(surf, tol=16):
    """Quita el fondo oscuro conectado a las esquinas (transparencia)."""
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


def _scale_h(surf, h):
    w = round(surf.get_width() * h / surf.get_height())
    return pygame.transform.smoothscale(surf, (w, h))


def load_sprites():
    img = pygame.image.load(IMG_PATH)
    sprites = {}
    for name, rect in REGIONS.items():
        r = pygame.Rect(rect)
        crop = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
        crop.blit(img, (0, 0), r)
        crop = _remove_bg(crop)
        if name == "tecolote":
            sprites[name] = _scale_h(crop, 230)
        else:
            sprites[name] = _scale_h(crop, 56)
    return sprites


def draw_cadejo(surf, rect, img):
    shadow = pygame.Rect(rect.x - 4, rect.bottom - 4, rect.w + 8, 8)
    pygame.draw.ellipse(surf, (10, 10, 20), shadow)
    surf.blit(img, img.get_rect(midbottom=(rect.centerx, rect.bottom + 4)))


def draw_tecolote(surf, cx, cy, img):
    surf.blit(img, img.get_rect(midbottom=(cx, cy + 110)))

COIN_PATH = os.path.join(os.path.dirname(__file__), "assets", "satochi.png")


def load_coin(size=28):
    img = pygame.image.load(COIN_PATH).convert_alpha()
    img = _remove_bg(img)
    # scale sin suavizar para mantener el estilo pixel art
    return pygame.transform.scale(img, (size, size))


def draw_satochi(surf, rect, img, t):
    bob = int(2 * math.sin(t / 10))
    center = (rect.centerx, rect.centery + bob)
    glow = pygame.Surface((44, 44), pygame.SRCALPHA)
    pygame.draw.circle(glow, (255, 200, 40, 50), (22, 22), 20)
    surf.blit(glow, glow.get_rect(center=center))
    surf.blit(img, img.get_rect(center=center))
