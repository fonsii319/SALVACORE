import math
import pygame
from player import Player
from graphics import draw_platform, draw_spike, draw_coin, draw_exit
from sprites import load_sprites, draw_tecolote, load_coin, draw_satochi, draw_cadejo_anim
from backgrounds import load_backgrounds

TILE = 40
WIDTH, HEIGHT = 960, 540
OFFSET_Y = 100

# Símbolos: # plataforma | ^ picos | $ satoshi | E salida | A Cipitío | B Siguanaba
LEVELS = [
    {
        "nombre": "Nivel 1: Primer paso",
        "dialogo": ["Don Tecolote: Un paso a la vez, compañeros."],
        "mapa": [
            "", "", "", "", "", "",
            "........$$$",
            "........####",
            "AB....$.........$$$...E..",
            "###########^^############",
        ],
    },
    {
        "nombre": "Nivel 2: El foso",
        "dialogo": ["Don Tecolote: Cuidado con el foso de picos."],
        "mapa": [
            "", "", "", "", "", "",
            "...$$$.........$$$",
            "...####",
            "A.B..................E..",
            "#########^^##############",
        ],
    },
    {
        "nombre": "Nivel 3: Escaleras",
        "dialogo": ["Don Tecolote: Sube las escaleras sin prisa."],
        "mapa": [
            "", "", "",
            "...................E",
            "...................###",
            "................###.",
            ".........$$$###",
            ".........###",
            "A.B...###",
            "##########^^^^^^^^^^^^^^#####",
        ],
    },
    {
        "nombre": "Nivel 4: Plataformas",
        "dialogo": ["Don Tecolote: Salta de plataforma en plataforma."],
        "mapa": [
            "", "", "", "", "",
            "....$.....$.....$",
            "......................E..",
            "...###...###...###...###",
            "AB",
            "####^^^^^^^^^^^^^^^^^^^^",
        ],
    },
    {
        "nombre": "Nivel 5: Pozo de picos",
        "dialogo": ["Don Tecolote: Los picos no perdonan."],
        "mapa": [
            "", "", "", "", "", "",
            "........$$",
            "..............##",
            "AB....................E.",
            "#######^^^###^^^^#######",
        ],
    },
    {
        "nombre": "Nivel 6: La torre",
        "dialogo": ["Don Tecolote: Sube la torre paso a paso."],
        "mapa": [
            "........................",
            "........................",
            ".......................E",
            "......................##",
            "...................###..",
            "...............###......",
            "........$$..###..........",
            ".......###..............",
            "AB.###..................",
            "########################",
        ],
    },
    {
        "nombre": "Nivel 7: Picos sobre plataformas",
        "dialogo": ["Don Tecolote: Mira bien dónde pisas."],
        "mapa": [
            "", "", "", "", "",
            "........$$$$",
            "......^.^.....^.^.......",
            ".....#####...#####......",
            "AB....................E.",
            "########################",
        ],
    },
    {
        "nombre": "Nivel 8: Plataformas flotantes",
        "dialogo": ["Don Tecolote: Usa las plataformas flotantes."],
        "mapa": [
            "", "", "", "", "",
            ".......$$.......##......",
            "",
            ".......##...##..........",
            "AB...................E..",
            "######^^^^^^^^^^^^######",
        ],
    },
    {
        "nombre": "Nivel 9: Pilares y picos",
        "dialogo": ["Don Tecolote: Pilares y picos, ten cuidado."],
        "mapa": [
            "", "", "", "", "", "......$$",
            "",
            "......##......##........",
            "AB....................E.",
            "#####^^^#####^^^########",
        ],
    },
    {
        "nombre": "Nivel 10: La última prueba",
        "dialogo": ["Don Tecolote: La última prueba de la patria."],
        "mapa": [
            "",
            "",
            ".......................E",
            "..............###.....##",
            "",
            ".........###.......###..",
            "",
            "....###",
            "AB",
            "####^^^^###^^^##^^^^####",
        ],
        
    },
    {
        "nombre": "Nivel 11: Suelo traicionero",
        "dialogo": ["Don Tecolote: No todo lo que pisas es seguro."],
        "mapa": [
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "AB..x.....x.....x.....E.",
            "##########cc############",
            "..........^^............",
        ],
    },
    {
        "nombre": "Nivel 12: Escalera envenenada",
        "dialogo": ["Don Tecolote: Cada escalón esconde una trampa."],
        "mapa": [
            "........................",
            "........................",
            ".......................E",
            "......................##",
            "...................###..",
            "...............###......",
            "..........###..........",
            ".......ccc..............",
            "AB.###..................",
            "######x####x############",
        ],
    },
    {
        "nombre": "Nivel 13: Laberinto de espinas",
        "dialogo": ["Don Tecolote: Salta cada hueco, uno a uno."],
        "mapa": [
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "........................",
            "AB....................E.",
            "##x#c#^#x#c#^#x#c#^#x###",
        ],
    },
    {
        "nombre": "Nivel 14: Lava ascendente",
        "dialogo": ["Don Tecolote: La lava sube. No te quedes quieto."],
        "lava": True,
        "lava_limit": 280,
        "mapa": [
            "........................",
            "........................",
            "........................",
            ".......................E",
            "......................##",
            "..................ccc...",
            "..............###.......",
            ".........###x...........",
            "AB.###..................",
            "###......................",
        ],
    },
    {
        "nombre": "Nivel 15: Prueba del Cadejo",
        "dialogo": ["Don Tecolote: Solo los valientes llegan hasta el final."],
        "mapa": [
            "........................",
            "........................",
            ".......................E",
            "...................###..",
            "...................##...",
            "...............###......",
            "..........###..........",
            ".......###..............",
            "AB.###.........x........",
            "###ccxxccxxccxxccxxccxxcc",
        ],
    },
    
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SAlVACORE")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
small = pygame.font.SysFont(None, 28)
SPRITES = load_sprites()
COIN_IMG = load_coin()
FONDOS = load_backgrounds()

def quit_game():
    pygame.quit()
    raise SystemExit


def show_dialogo(lineas):
    for linea in lineas:
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    esperando = False
            screen.fill((20, 20, 40))
            draw_tecolote(screen, WIDTH // 2, 130, SPRITES["tecolote"])
            screen.blit(font.render(linea, True, (255, 255, 255)), (40, HEIGHT // 2))
            screen.blit(small.render("ENTER para continuar", True, (150, 150, 150)),
                        (40, HEIGHT // 2 + 50))
            pygame.display.flip()
            clock.tick(30)


def make_falling(rect):
    return {"home": rect.copy(), "rect": rect.copy(), "estado": "firme", "timer": 0}


def update_falling(f, players):
    estado = f["estado"]
    if estado == "firme":
        if any(p.on_ground and p.rect.move(0, 1).colliderect(f["rect"]) for p in players):
            f["estado"], f["timer"] = "tiembla", 30
    elif estado == "tiembla":
        f["timer"] -= 1
        if f["timer"] <= 0:
            f["estado"] = "cae"
    elif estado == "cae":
        f["rect"].y += 6
        if f["rect"].top > HEIGHT:
            f["estado"], f["timer"] = "espera", 180
    elif estado == "espera":
        f["timer"] -= 1
        if f["timer"] <= 0:
            f["rect"] = f["home"].copy()
            f["estado"] = "firme"


def reset_falling(f):
    f["rect"] = f["home"].copy()
    f["estado"], f["timer"] = "firme", 0


def draw_falling(surf, f, t):
    if f["estado"] == "espera":
        return
    r = f["rect"].copy()
    if f["estado"] == "tiembla" and (t // 2) % 2:
        r.x += 2
    pygame.draw.rect(surf, (120, 90, 60), r, border_radius=4)
    pygame.draw.rect(surf, (75, 50, 30), r, 2, border_radius=4)
    pygame.draw.line(surf, (60, 40, 25), (r.x + 8, r.y + 6), (r.centerx, r.centery), 2)
    pygame.draw.line(surf, (60, 40, 25), (r.centerx, r.centery), (r.right - 6, r.bottom - 8), 2)


def draw_lava(surf, y, t):
    pygame.draw.rect(surf, (190, 45, 10), (0, y, WIDTH, HEIGHT - y))
    for x in range(-20, WIDTH, 40):
        ondas = int(4 * math.sin((x + t * 3) / 25))
        pygame.draw.circle(surf, (255, 150, 30), (x + 20, y + ondas), 12)


def is_dead(p, danger, lava_rect):
    if p.rect.top > HEIGHT:
        return True
    if any(p.rect.colliderect(d) for d in danger):
        return True
    return lava_rect is not None and p.rect.colliderect(lava_rect)

def build_level(mapa):
    platforms, coins, spikes, hidden, falling = [], [], [], [], []
    players, exit_rect = [], None
    for row, line in enumerate(mapa):
        for col, ch in enumerate(line):
            x, y = col * TILE, row * TILE + OFFSET_Y
            if ch == "#":
                platforms.append(pygame.Rect(x, y, TILE, TILE))
            elif ch == "^":
                spikes.append(pygame.Rect(x, y, TILE, TILE))
            elif ch == "x":
                hidden.append(pygame.Rect(x, y, TILE, TILE))
            elif ch == "c":
                falling.append(make_falling(pygame.Rect(x, y, TILE, TILE)))
            elif ch == "$":
                coins.append(pygame.Rect(x + 12, y + 12, 16, 16))
            elif ch == "E":
                exit_rect = pygame.Rect(x, y, TILE, TILE)
            elif ch == "A":
                p = Player(x, y, (255, 200, 0), (pygame.K_a, pygame.K_d, pygame.K_w))
                p.sprite = SPRITES["blanqui"]
                players.append(p)
            elif ch == "B":
                p = Player(x, y, (0, 180, 255), (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP))
                p.sprite = SPRITES["darky"]
                players.append(p)
    return platforms, coins, spikes, hidden, falling, players, exit_rect

def play_level(nivel, total, fondo):
    platforms, coins, spikes, hidden, falling, players, exit_rect = build_level(nivel["mapa"])
    es_lava = nivel.get("lava", False)
    lava_y = float(HEIGHT)
    danger = spikes + hidden
    score = 0
    won = False
    t = 0

    while True:
        t += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if won and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return score

        lava_rect = None
        if es_lava:
            if not won and lava_y > nivel["lava_limit"]:
                lava_y = max(nivel["lava_limit"], lava_y - 0.15)
            lava_rect = pygame.Rect(0, int(lava_y), WIDTH, HEIGHT)

        if not won:
            for f in falling:
                update_falling(f, players)
            solid = platforms + [f["rect"] for f in falling
                                 if f["estado"] in ("firme", "tiembla")]
            for p in players:
                if p.dying:
                    p.dying -= 1
                    if p.dying == 0:
                        if p.death_by_lava:
                            lava_y = float(HEIGHT)
                            for q in players:
                                q.respawn()
                            for f in falling:
                                reset_falling(f)
                        else:
                            p.respawn()
                    continue
                p.update(solid)
                if is_dead(p, danger, lava_rect):
                    p.kill(by_lava=lava_rect is not None and p.rect.colliderect(lava_rect))
                for c in coins[:]:
                    if p.rect.colliderect(c):
                        coins.remove(c)
                        score += 1
            if all(p.rect.colliderect(exit_rect) for p in players):
                won = True
                for p in players:
                    p.howl = True
                    p.moving = False
                    p.anim = "idle"

        screen.blit(fondo, (0, 0))
        for r in platforms:
            draw_platform(screen, r)
        for f in falling:
            draw_falling(screen, f, t)
        for s in spikes:
            draw_spike(screen, s)
        for c in coins:
            draw_satochi(screen, c, COIN_IMG, t)
        draw_exit(screen, exit_rect, t)
        if lava_rect is not None:
            draw_lava(screen, int(lava_y), t)
        for p in players:
            draw_cadejo_anim(screen, p, t)

        screen.blit(font.render(f"Satoshis: {total + score}", True, (255, 255, 255)), (10, 10))
        screen.blit(small.render(nivel["nombre"], True, (200, 200, 200)), (WIDTH - 340, 14))
        if won:
            screen.blit(font.render("¡Nivel completado!", True, (255, 255, 255)),
                        (WIDTH // 2 - 130, HEIGHT // 2 + 20))
            screen.blit(small.render("ENTER para seguir", True, (150, 150, 150)),
                        (WIDTH // 2 - 90, HEIGHT // 2 + 60))
            draw_tecolote(screen, WIDTH // 2, 130, SPRITES["tecolote"])
        pygame.display.flip()
        clock.tick(60)

def main():
    show_dialogo([
        "Don Tecolote: ¡Parece que estás en apuros!",
        "Don Tecolote: La patria te necesita.",
        "Controles: Blanqui W A D  |  Darky flechas",
    ])
    total = 0
    for i, nivel in enumerate(LEVELS):
        show_dialogo(nivel["dialogo"])
        total += play_level(nivel, total, FONDOS[i % len(FONDOS)])
    show_dialogo([
        "Don Tecolote: ¡Libertad! El Salvador escapó del fiat.",
        f"Satoshis totales: {total}",
    ])
    pygame.quit()


if __name__ == "__main__":
    main()

