import math
import os
import pygame

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
SRC_W, SRC_H = 1024, 576        # tamaño de la imagen original
CLICK_FRAMES = 18
TOTAL_LEVELS = 24
PLAYABLE = 15                   # niveles jugables por ahora

# Centros de los botones en la imagen original (1024 x 576)
COLS = [320, 448, 580, 708]
ROWS = [128, 198, 270, 340, 410, 480]
TILE_W, TILE_H = 84, 70
BACK_SRC = pygame.Rect(30, 508, 165, 46)


def load_level_select_bg(size=(960, 540)):
    img = pygame.image.load(os.path.join(ASSETS, "seleccion_nivel.png")).convert()
    return pygame.transform.smoothscale(img, size)


def _scaled(src, sx, sy):
    return pygame.Rect(round(src.x * sx), round(src.y * sy),
                       round(src.w * sx), round(src.h * sy))


def _build_buttons(sx, sy):
    buttons = []
    for n in range(1, TOTAL_LEVELS + 1):
        row, col = divmod(n - 1, 4)
        src = pygame.Rect(0, 0, TILE_W, TILE_H)
        src.center = (COLS[col], ROWS[row])
        buttons.append((n, _scaled(src, sx, sy)))
    return buttons


def _draw_tile(screen, bg, rect, h, t, clicked, click_t, locked):
    if locked:
        dark = pygame.Surface(rect.size, pygame.SRCALPHA)
        dark.fill((0, 0, 0, 150))
        screen.blit(dark, rect.topleft)
        return

    scale = 1 + 0.07 * h
    if clicked:
        scale = 1.07 + 0.05 * min(1, click_t / CLICK_FRAMES)

    if h > 0.02:
        pad = 10
        glow = pygame.Surface((rect.w + pad * 2, rect.h + pad * 2), pygame.SRCALPHA)
        alpha = int(h * (150 + 70 * math.sin(t * 0.15)))
        pygame.draw.rect(glow, (255, 220, 90, max(0, min(255, alpha))),
                         glow.get_rect().inflate(-4, -4), 3, border_radius=10)
        screen.blit(glow, (rect.x - pad, rect.y - pad))

    if scale > 1.001:
        piece = bg.subsurface(rect).copy()
        big = pygame.transform.smoothscale(piece, (int(rect.w * scale), int(rect.h * scale)))
        screen.blit(big, big.get_rect(center=rect.center))

    if h > 0.02 or clicked:
        shine = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        if clicked:
            flash = min(1, click_t / CLICK_FRAMES)
            shine.fill((255, 255, 255, int(170 * flash)))
        else:
            phase = (t % 50) / 50
            sx_ = int(-rect.w * 0.4 + phase * rect.w * 1.8)
            pygame.draw.polygon(shine, (255, 255, 255, int(120 * h)),
                                [(sx_, 0), (sx_ + 25, 0), (sx_ + 12, rect.h), (sx_ - 12, rect.h)])
        screen.blit(shine, rect.topleft)


def run_level_select(screen, clock, bg, quit_fn):
    """Devuelve el índice (0 a 14) del nivel elegido, o None si se regresa."""
    sx, sy = bg.get_width() / SRC_W, bg.get_height() / SRC_H
    buttons = _build_buttons(sx, sy)
    back = _scaled(BACK_SRC, sx, sy)
    targets = [(n, rect, n <= PLAYABLE) for n, rect in buttons]
    targets.append(("back", back, True))

    hover = {key: 0.0 for key, _, _ in targets}
    clicked, click_t, t = None, 0, 0

    while True:
        t += 1
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_fn()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and clicked is None:
                clicked = "back"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and clicked is None:
                for key, rect, playable in targets:
                    if playable and rect.collidepoint(event.pos):
                        clicked = key
                        break

        if clicked is not None:
            click_t += 1
            if click_t >= CLICK_FRAMES:
                if clicked == "back":
                    return None
                return clicked - 1

        screen.blit(bg, (0, 0))
        for key, rect, playable in targets:
            target = 1.0 if (playable and rect.collidepoint(mouse)) else 0.0
            hover[key] += (target - hover[key]) * 0.25
            _draw_tile(screen, bg, rect, hover[key], t, clicked == key, click_t, not playable)
        pygame.display.flip()
        clock.tick(60)
        