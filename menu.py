import math
import os
import pygame

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

# Rectángulos de los botones sobre la imagen (960 x 540)
BUTTONS = [
    ("start", pygame.Rect(320, 282, 320, 64)),
    ("levels", pygame.Rect(320, 358, 320, 64)),
    ("difficulty", pygame.Rect(320, 434, 320, 64)),
]
PHONE_BTN = pygame.Rect(670, 478, 270, 44)
CLICK_FRAMES = 18


def load_menu_bg(size=(960, 540)):
    img = pygame.image.load(os.path.join(ASSETS, "menu.png")).convert()
    return pygame.transform.smoothscale(img, size)


def _draw_button(screen, bg, rect, h, t, clicked, click_t):
    scale = 1 + 0.07 * h
    if clicked:
        scale = 1.07 + 0.05 * min(1, click_t / CLICK_FRAMES)

    if h > 0.02:
        pad_x, pad_y = 16, 12
        glow = pygame.Surface((rect.w + pad_x * 2, rect.h + pad_y * 2), pygame.SRCALPHA)
        alpha = int(h * (150 + 70 * math.sin(t * 0.15)))
        pygame.draw.rect(glow, (255, 220, 90, max(0, min(255, alpha))),
                         glow.get_rect().inflate(-4, -4), 3, border_radius=12)
        screen.blit(glow, (rect.x - pad_x, rect.y - pad_y))

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
            sx = int(-rect.w * 0.4 + phase * rect.w * 1.8)
            pygame.draw.polygon(shine, (255, 255, 255, int(120 * h)),
                                [(sx, 0), (sx + 40, 0), (sx + 20, rect.h), (sx - 20, rect.h)])
        screen.blit(shine, rect.topleft)


def _draw_phone_btn(screen, font, rect, h):
    grow = int(h * 8)
    r = rect.inflate(grow, grow // 2)
    base = (30, 140, 90) if h > 0.5 else (20, 90, 60)
    border = (255, 220, 90) if h > 0.5 else (140, 140, 170)
    pygame.draw.rect(screen, base, r, border_radius=12)
    pygame.draw.rect(screen, border, r, 2, border_radius=12)
    s = font.render("MANDO CON TELÉFONOS", True, (255, 255, 255))
    screen.blit(s, s.get_rect(center=r.center))


def run_menu(screen, clock, bg, font, quit_fn):
    """Devuelve 'start', 'levels', 'difficulty' o 'phones'."""
    hover = {name: 0.0 for name, _ in BUTTONS}
    hover["phones"] = 0.0
    phone_font = pygame.font.Font(None, 28)
    clicked, click_t = None, 0
    t = 0

    while True:
        t += 1
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_fn()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and clicked is None:
                if PHONE_BTN.collidepoint(event.pos):
                    return "phones"
                for name, rect in BUTTONS:
                    if rect.collidepoint(event.pos):
                        clicked = name

        if clicked:
            click_t += 1
            if click_t >= CLICK_FRAMES:
                return clicked

        screen.blit(bg, (0, 0))
        for name, rect in BUTTONS:
            target = 1.0 if rect.collidepoint(mouse) else 0.0
            hover[name] += (target - hover[name]) * 0.25
            _draw_button(screen, bg, rect, hover[name], t, clicked == name, click_t)

        target = 1.0 if PHONE_BTN.collidepoint(mouse) else 0.0
        hover["phones"] += (target - hover["phones"]) * 0.25
        _draw_phone_btn(screen, phone_font, PHONE_BTN, hover["phones"])

        pygame.display.flip()
        clock.tick(60)
        


