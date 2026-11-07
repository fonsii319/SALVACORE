import os
import pygame

FOLDER = os.path.join(os.path.dirname(__file__), "assets", "fondos")


def _find(i):
    for ext in ("png", "jpg"):
        path = os.path.join(FOLDER, f"fondo_{i:02d}.{ext}")
        if os.path.exists(path):
            return path
    raise FileNotFoundError(f"Falta el fondo fondo_{i:02d}.png en assets/fondos")


def load_backgrounds(total=24, size=(960, 540)):
    fondos = []
    for i in range(1, total + 1):
        img = pygame.image.load(_find(i)).convert()
        fondos.append(pygame.transform.smoothscale(img, size))
    return fondos