import math
import pygame


def make_background(w, h):
    """Fondo con degradado nocturno y estrellas. Se crea una sola vez."""
    surf = pygame.Surface((w, h))
    top, bottom = (18, 12, 45), (70, 35, 100)
    for y in range(h):
        k = y / h
        c = tuple(int(top[i] + (bottom[i] - top[i]) * k) for i in range(3))
        pygame.draw.line(surf, c, (0, y), (w, y))
    for i in range(60):
        x = (i * 137) % w
        y = (i * 73) % (h // 2)
        b = 150 + (i * 37) % 105
        pygame.draw.circle(surf, (b, b, b), (x, y), 1 if i % 3 else 2)
    return surf


def draw_platform(surf, r):
    pygame.draw.rect(surf, (55, 60, 85), r, border_radius=6)
    pygame.draw.rect(surf, (110, 120, 160), (r.x, r.y, r.w, 6), border_radius=6)
    pygame.draw.rect(surf, (35, 38, 58), r, 2, border_radius=6)


def draw_spike(surf, r):
    pts = [(r.left, r.bottom), (r.centerx, r.top + 4), (r.right, r.bottom)]
    pygame.draw.polygon(surf, (220, 50, 70), pts)
    pygame.draw.polygon(surf, (255, 140, 150), pts, 2)


def draw_coin(surf, r, t):
    cx, cy = r.center
    radius = int(9 + 1.5 * math.sin(t / 8))
    pygame.draw.circle(surf, (200, 110, 20), (cx, cy), radius + 2)
    pygame.draw.circle(surf, (247, 147, 26), (cx, cy), radius)
    pygame.draw.circle(surf, (255, 220, 120), (cx - 3, cy - 3), 3)


def draw_exit(surf, r, t):
    cx, cy = r.center
    for i in range(3):
        radius = 18 + i * 7 + int(3 * math.sin(t / 10 + i))
        pygame.draw.circle(surf, (0, 255, 150), (cx, cy), radius, 2)
    pygame.draw.circle(surf, (0, 120, 80), (cx, cy), 14)


def draw_player(surf, r, color):
    # Sombra en el suelo
    pygame.draw.ellipse(surf, (10, 10, 20), (r.x - 2, r.bottom - 3, r.w + 4, 6))
    # Cuerpo con borde oscuro
    dark = tuple(max(0, c - 70) for c in color)
    pygame.draw.rect(surf, color, r, border_radius=8)
    pygame.draw.rect(surf, dark, r, 2, border_radius=8)
    # Brillo superior
    light = tuple(min(255, c + 60) for c in color)
    pygame.draw.rect(surf, light, (r.x + 4, r.y + 3, r.w - 8, 6), border_radius=4)
    # Ojos
    for ex in (r.left + 10, r.right - 10):
        pygame.draw.circle(surf, (255, 255, 255), (ex, r.top + 14), 5)
        pygame.draw.circle(surf, (0, 0, 0), (ex + 1, r.top + 15), 2)
