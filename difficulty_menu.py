import math
import pygame

WIDTH, HEIGHT = 960, 540
CLICK_FRAMES = 18

OPTIONS = [
    ("normal", pygame.Rect(280, 190, 400, 80), "MODO NORMAL",
     "Los niveles tal como fueron diseñados", (50, 120, 60), (140, 255, 160)),
    ("bitcoiner", pygame.Rect(280, 300, 400, 80), "MODO BITCOINER",
     "Trampas ocultas y trolleos", (95, 35, 130), (210, 130, 255)),
]
BTN_BACK = pygame.Rect(30, 460, 180, 50)


def _pulse(color, t):
    k = 0.85 + 0.15 * math.sin(t * 0.15)
    return tuple(min(255, int(c * k)) for c in color)


def _draw_option(screen, fonts, rect, label, desc, base, glow, h, t, flash, click_t):
    label_f, small_f = fonts
    grow = int(h * 14)
    r = rect.inflate(grow, grow // 2)
    pygame.draw.rect(screen, base, r, border_radius=16)
    if h > 0.5:
        pygame.draw.rect(screen, _pulse(glow, t), r, 3, border_radius=16)
    else:
        pygame.draw.rect(screen, (90, 90, 120), r, 2, border_radius=16)
    if flash:
        fx = pygame.Surface(r.size, pygame.SRCALPHA)
        fx.fill((255, 255, 255, int(180 * min(1, click_t / CLICK_FRAMES))))
        screen.blit(fx, r.topleft)
    s1 = label_f.render(label, True, (255, 255, 255))
    screen.blit(s1, s1.get_rect(center=(r.centerx, r.centery - 12)))
    s2 = small_f.render(desc, True, (220, 220, 240))
    screen.blit(s2, s2.get_rect(center=(r.centerx, r.centery + 20)))


def run_difficulty(screen, clock, bg, quit_fn):
    """Devuelve 'normal', 'bitcoiner' o None si se regresa."""
    title_f = pygame.font.Font(None, 60)
    label_f = pygame.font.Font(None, 40)
    small_f = pygame.font.Font(None, 26)
    fonts = (label_f, small_f)
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 25, 170))

    hover = {key: 0.0 for key, *_ in OPTIONS}
    hover["back"] = 0.0
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
                for key, rect, *_ in OPTIONS:
                    if rect.collidepoint(event.pos):
                        clicked = key
                        break
                else:
                    if BTN_BACK.collidepoint(event.pos):
                        clicked = "back"

        if clicked is not None:
            click_t += 1
            if click_t >= CLICK_FRAMES:
                return None if clicked == "back" else clicked

        screen.blit(bg, (0, 0))
        screen.blit(overlay, (0, 0))
        title = title_f.render("AUMENTAR DIFICULTAD", True, (255, 210, 60))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 125)))

        for key, rect, label, desc, base, glow in OPTIONS:
            target = 1.0 if rect.collidepoint(mouse) else 0.0
            hover[key] += (target - hover[key]) * 0.25
            _draw_option(screen, fonts, rect, label, desc, base, glow,
                         hover[key], t, clicked == key, click_t)

        target = 1.0 if BTN_BACK.collidepoint(mouse) else 0.0
        hover["back"] += (target - hover["back"]) * 0.25
        back = BTN_BACK.inflate(int(hover["back"] * 12), int(hover["back"] * 6))
        pygame.draw.rect(screen, (40, 40, 70), back, border_radius=12)
        pygame.draw.rect(screen, (255, 210, 60), back, 2, border_radius=12)
        s = label_f.render("Regresar", True, (255, 255, 255))
        screen.blit(s, s.get_rect(center=back.center))

        pygame.display.flip()
        clock.tick(60)

        