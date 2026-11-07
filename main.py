import math
import os
import random
import sys
import pygame
from player import Player
from graphics import draw_platform, draw_spike, draw_exit
from sprites import load_sprites, draw_tecolote, load_coin, draw_satochi, draw_cadejo_anim, load_exit, draw_portal
from backgrounds import load_backgrounds
from levels_menu import load_level_select_bg, run_level_select
from difficulty_menu import run_difficulty
from sound import load_audio, play, start_music
from controller_server import start_server, get_input, connected, local_ip
from menu import load_menu_bg, run_menu

TILE = 40
WIDTH, HEIGHT = 960, 540
OFFSET_Y = 100

# Símbolos: # plataforma | ^ picos | x picos ocultos | c plataforma que cae
#           $ satoshi | E salida | A Blanqui | B Darky
LEVELS = [
    {
        "nombre": "Nivel 1: Primer paso",
        "dialogo": ["Don Tecolote: Un paso a la vez, compañeros."],
        "mapa": [
            "", "", "", "", "", "",
            "........$$$",
            "........####",
            "AB....$.........$....E..",
            "########################",
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
            "..................###",
            "...............###",
            ".........$$$###",
            ".........###",
            "A.B...###",
            "########################",
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
            "...........###..........",
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
    {  
        "nombre": "Nivel 16: Piso mentiroso",
        "dialogo": ["Don Tecolote: El piso no siempre es piso."],
        "mapa": [
            "........................",
            "....................E...",
            "...................###..",
            "...............####.....",
            "........................",
            "........####............",
            "........................",
            "...###..................",
            "AB.....$.........$......",
            "######x######c##########",
        ],
    },
    {
        "nombre": "Nivel 17: Monedas traicioneras",
        "dialogo": ["Don Tecolote: Cada moneda tiene su precio."],
        "mapa": [
            "........................",
            "......................E.",
            "....................###.",
            "................###.....",
            "........................",
            "............###.........",
            "........###.............",
            "....###.................",
            "AB$.....$........$......",
            "##x######c##############",
        ],
    },
    {
        "nombre": "Nivel 18: Torre engañosa",
        "dialogo": ["Don Tecolote: Cada escalón tiene su trampa."],
        "mapa": [
            "........................",
            "....................E...",
            "...................###..",
            "................c##.....",
            "........................",
            "...........x###.........",
            "........................",
            "......###...............",
            "AB....$.........$......",
            "#####^^^^^##x#####c#####",
        ],
    },
    {
        "nombre": "Nivel 19: Lava en ascenso",
        "dialogo": ["Don Tecolote: La lava sube. Sube más rápido o muere."],
        "lava": True,
        "lava_limit": 380,
        "mapa": [
            "........................",
            "......................E.",
            "....................###.",
            "................###.....",
            "...............x........",
            "............###.........",
            "........###.............",
            "....###.................",
            "AB....$.........x......",
            "######x######x#########",
        ],
    },
    {
        "nombre": "Nivel 20: Espinas del Cadejo",
        "dialogo": ["Don Tecolote: Los picos esconden más de lo que ves."],
        "mapa": [
            "........................",
            "....................E...",
            "...................###..",
            "...............###.....",
            "........................",
            "..........###..........",
            "........................",
            "......###...............",
            "AB...$...x.....$.......",
            "####^^####^^####x#####^#",
        ],
    },
    {
        "nombre": "Nivel 21: Escalera de trampas",
        "dialogo": ["Don Tecolote: Cada escalón puede desaparecer."],
        "mapa": [
            "........................",
            "......................E.",
            "....................###.",
            "................ccc.....",
            "........................",
            "............###.........",
            "........................",
            "........###.............",
            "....###.................",
            "AB...$...........$......",
            "##x#####c###x###########",
        ],
    },
    {
        "nombre": "Nivel 22: Doble trampa",
        "dialogo": ["Don Tecolote: Dos trampas en una sola escalera."],
        "mapa": [
            "........................",
            "....................E...",
            "...................###..",
            "...............###.....",
            "..............x.........",
            "...........###.........",
            "........................",
            "......###...............",
            "AB....x...........$.....",
            "#####^^##x###^###^######",
        ],
    },
    {
        "nombre": "Nivel 23: Suelo ardiente",
        "dialogo": ["Don Tecolote: Cuidado, el suelo arde."],
        "lava": True,
        "lava_limit": 360,
        "mapa": [
            "........................",
            "......................E.",
            "....................###.",
            "................###.....",
            "........................",
            "............###.........",
            "........###.............",
            "....###..........^......",
            "AB....$...........$.....",
            "######^##^####x#########",
        ],
    },
    {
        "nombre": "Nivel 24: Bóveda de satoshis",
        "dialogo": ["Don Tecolote: Ya no hay vuelta atrás."],
        "mapa": [
            "........................",
            "..................E.....",
            "................###....",
            "........................",
            "..........###...........",
            "........................",
            "........c##.............",
            "....###.................",
            "AB....$.......$........",
            "##x#####^##x##c##x######",
        ],
    },
]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SALVACORE")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
small = pygame.font.SysFont(None, 28)

SPRITES = load_sprites()
COIN_IMG = load_coin()
EXIT_IMG = load_exit()
FONDOS = load_backgrounds()
load_audio()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIALOGO_BG = pygame.transform.smoothscale(
    pygame.image.load(os.path.join(BASE_DIR, "assets", "dialogo.png")).convert(),
    (WIDTH, HEIGHT))
WIN_BG = pygame.transform.smoothscale(
    pygame.image.load(os.path.join(BASE_DIR, "assets", "nivel_completado.png")).convert(),
    (WIDTH, HEIGHT))

DIALOG_PANEL = pygame.Rect(100, 322, 753, 95)
text_font = pygame.font.Font(None, 32)
TYPE_SPEED = 0.6
CLICK_FRAMES = 18

GAME_MODE = "normal"
PHONE_ON = False


def quit_game():
    pygame.quit()
    raise SystemExit


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


def wrap_text(text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        test = (cur + " " + word).strip()
        if font.size(test)[0] <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def split_linea(linea):
    if ":" in linea:
        speaker, texto = linea.split(":", 1)
        return speaker.strip(), texto.strip()
    return "", linea.strip()


def draw_dialog_frame(linea, n_chars):
    screen.blit(DIALOGO_BG, (0, 0))
    _, texto = split_linea(linea)
    lines = wrap_text(texto, text_font, DIALOG_PANEL.w - 60)
    line_h = 30
    block_h = len(lines) * line_h
    y = DIALOG_PANEL.centery - block_h // 2 - 8

    count = 0
    for ln in lines:
        visible = ln[:max(0, n_chars - count)]
        count += len(ln) + 1
        if visible:
            s = text_font.render(visible, True, (255, 255, 255))
            screen.blit(s, (DIALOG_PANEL.left + 30, y))
        y += line_h


def show_dialogo(lineas):
    for linea in lineas:
        _, texto = split_linea(linea)
        total_chars = len(texto)
        n = 0.0
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if int(n) < total_chars:
                        n = total_chars
                    else:
                        esperando = False
            if n < total_chars:
                n += TYPE_SPEED
            draw_dialog_frame(linea, int(n))
            pygame.display.flip()
            clock.tick(30)


def troll_map(mapa, semilla):
    rng = random.Random(semilla)
    rows = [list(r) for r in mapa]
    for y, fila in enumerate(rows):
        for x, ch in enumerate(fila):
            if x < 3 or x > len(fila) - 4:
                continue
            below = rows[y + 1][x] if y + 1 < len(rows) and x < len(rows[y + 1]) else "."
            above = rows[y - 1][x] if y > 0 and x < len(rows[y - 1]) else "."
            if ch == "." and below == "#" and above == "." and rng.random() < 0.12:
                fila[x] = "x"
            elif ch == "#" and above == "." and rng.random() < 0.08:
                fila[x] = "c"
    return ["".join(r) for r in rows]


def build_level(mapa, nombre=""):
    if GAME_MODE == "bitcoiner":
        mapa = troll_map(mapa, sum(map(ord, nombre)))
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


def pick_players(players, role):
    blanqui = [p for p in players if p.color == (255, 200, 0)][0]
    darky = [p for p in players if p.color == (0, 180, 255)][0]
    return (blanqui, darky) if role == "A" else (darky, blanqui)


def connect_online(host):
    print("El modo en red no está disponible en esta versión.")
    quit_game()
    rol = {"A": "Blanqui", "B": "Darky"}
    while not net.ready:
        net.poll()
        if net.full:
            print("La partida ya tiene 2 jugadores.")
            quit_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
        screen.fill((20, 20, 40))
        if net.role:
            texto = f"Conectado como {rol[net.role]}. Esperando al otro jugador..."
        else:
            texto = "Conectando..."
        s = font.render(texto, True, (255, 255, 255))
        screen.blit(s, s.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        pygame.display.flip()
        clock.tick(30)
    return net


def phone_input(p):
    if not PHONE_ON:
        return ()
    return get_input("1" if p.color == (255, 200, 0) else "2")


def phone_lobby(ip):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return
        screen.fill((15, 15, 40))
        lineas = [
            ("Abre estos enlaces en los teléfonos (misma red Wi-Fi):", (255, 255, 255)),
            (f"Blanqui:  http://{ip}:8000/p1", (120, 200, 255)),
            (f"Darky:    http://{ip}:8000/p2", (190, 130, 255)),
            ("", (0, 0, 0)),
            (f"Blanqui: {'CONECTADO' if connected('1') else 'esperando...'}", (255, 220, 80)),
            (f"Darky: {'CONECTADO' if connected('2') else 'esperando...'}", (255, 220, 80)),
            ("", (0, 0, 0)),
            ("Pulsa ENTER en la PC para empezar", (180, 180, 180)),
        ]
        y = 120
        for texto, color in lineas:
            if texto:
                s = font.render(texto, True, color)
                screen.blit(s, s.get_rect(center=(WIDTH // 2, y)))
            y += 40
        pygame.display.flip()
        clock.tick(30)


def play_level(nivel, total, fondo, idx=0, net=None):
    platforms, coins, spikes, hidden, falling, players, exit_rect = build_level(nivel["mapa"], nivel["nombre"])
    es_lava = nivel.get("lava", False)
    lava_y = float(HEIGHT)
    danger = spikes + hidden
    score = 0
    taken = set()
    won = False
    sent_won = False
    t = 0
    local = remote = None
    if net:
        local, remote = pick_players(players, net.role)
    active = [local] if net else players

    while True:
        t += 1
        if net:
            net.poll()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if won and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if net is None or net.remote_won >= idx:
                    return score

        gone = set(taken)
        if net:
            gone |= {ci for lv, ci in net.remote_coins if lv == idx}
            s = net.remote_state
            if s and s.get("level") == idx:
                remote.rect.topleft = (s["x"], s["y"])
                remote.facing = s["facing"]
                remote.anim = s["anim"]
                remote.dying = s["dying"]
                remote.howl = s["howl"]
                remote.moving = s["moving"]

        lava_rect = None
        if es_lava:
            if not won and lava_y > nivel["lava_limit"]:
                lava_y = max(nivel["lava_limit"], lava_y - (0.25 if GAME_MODE == "bitcoiner" else 0.15))
            lava_rect = pygame.Rect(0, int(lava_y), WIDTH, HEIGHT)

        if not won:
            for f in falling:
                update_falling(f, players)
            solid = platforms + [f["rect"] for f in falling
                                 if f["estado"] in ("firme", "tiembla")]
            for p in active:
                if p.dying:
                    p.dying -= 1
                    if p.dying == 0:
                        if p.death_by_lava:
                            lava_y = float(HEIGHT)
                            for q in active:
                                q.respawn()
                            for f in falling:
                                reset_falling(f)
                        else:
                            p.respawn()
                    continue
                was_ground = p.on_ground
                p.update(solid, phone_input(p))
                if was_ground and not p.on_ground and p.vel_y < 0:
                    play("jump", 0.6)
                if p.moving and p.on_ground and t % 14 == 0:
                    play("step", 0.35)
                if is_dead(p, danger, lava_rect):
                    p.kill(by_lava=lava_rect is not None and p.rect.colliderect(lava_rect))
                    play("death", 0.7)
                for ci, c in enumerate(coins):
                    if ci not in gone and p.rect.colliderect(c):
                        taken.add(ci)
                        gone.add(ci)
                        score += 1
                        play("coin", 0.6)
                        if net:
                            net.send({"type": "coin", "level": idx, "i": ci})
            if net:
                ready = local.rect.colliderect(exit_rect) and remote.rect.colliderect(exit_rect)
            else:
                ready = all(p.rect.colliderect(exit_rect) for p in players)
            if ready:
                won = True
                play("howl", 0.9)
                for p in players:
                    p.howl = True
                    p.moving = False
                    p.anim = "idle"

        if net:
            net.send({
                "type": "state", "level": idx,
                "x": local.rect.x, "y": local.rect.y,
                "facing": local.facing, "anim": local.anim,
                "dying": local.dying, "howl": local.howl,
                "moving": local.moving,
            })
            if won and not sent_won:
                net.send({"type": "won", "level": idx})
                sent_won = True

        screen.blit(fondo, (0, 0))
        for r in platforms:
            draw_platform(screen, r)
        for f in falling:
            draw_falling(screen, f, t)
        for s_ in spikes:
            draw_spike(screen, s_)
        for ci, c in enumerate(coins):
            if ci not in gone:
                draw_satochi(screen, c, COIN_IMG, t)
        draw_portal(screen, exit_rect, EXIT_IMG, t)        
        if lava_rect is not None:
            draw_lava(screen, int(lava_y), t)
        for p in players:
            draw_cadejo_anim(screen, p, t)

        if won:
            screen.blit(WIN_BG, (0, 0))
            hud = small.render(f"Satoshis: {total + score}", True, (255, 220, 80))
            screen.blit(hud, (20, 20))
            if net and net.remote_won < idx:
                aviso = small.render("Esperando al otro jugador...", True, (255, 255, 255))
                screen.blit(aviso, aviso.get_rect(center=(WIDTH // 2, HEIGHT - 40)))
        else:
            screen.blit(font.render(f"Satoshis: {total + score}", True, (255, 255, 255)), (10, 10))
            screen.blit(small.render(nivel["nombre"], True, (200, 200, 200)), (WIDTH - 340, 14))

        pygame.display.flip()
        clock.tick(60)


def main():
    global GAME_MODE, PHONE_ON
    start_music()
    net = None

    inicio = 0
    if "--phones" in sys.argv:
        start_server()
        PHONE_ON = True
        phone_lobby(local_ip())
    else:
        menu_bg = load_menu_bg((WIDTH, HEIGHT))
        level_bg = load_level_select_bg((WIDTH, HEIGHT))
        while net is None:
            accion = run_menu(screen, clock, menu_bg, font, quit_game)
            if accion == "start":
                break
            if accion == "phones":
                start_server()
                PHONE_ON = True
                phone_lobby(local_ip())
                break
            if accion == "levels":
                elegido = run_level_select(screen, clock, level_bg, quit_game)
                if elegido is not None:
                    inicio = elegido
                    break
            if accion == "difficulty":
                modo = run_difficulty(screen, clock, menu_bg, quit_game)
                if modo:
                    GAME_MODE = modo
                    nombre = "Bitcoiner" if modo == "bitcoiner" else "Normal"
                    show_dialogo([
                        f"Modo elegido: {nombre}",
                        "Ahora pulsa Iniciar juego.",
                    ])

    total = 0
    if inicio == 0:
        intro = [
            "¡Parece que estás en apuros!",
            "La patria te necesita.",
            "Controles: Blanqui W A D  |  Darky flechas",
        ]
        if GAME_MODE == "bitcoiner":
            intro.append("Modo Bitcoiner: prepárate para los trolleos.")
        show_dialogo(intro)
    for i in range(inicio, len(LEVELS)):
        nivel = LEVELS[i]
        show_dialogo(nivel["dialogo"])
        total += play_level(nivel, total, FONDOS[i % len(FONDOS)], idx=i, net=net)
    show_dialogo([
        "Don Tecolote: ¡Libertad! El Salvador escapó del fiat.",
        f"Satoshis totales: {total}",
    ])
    pygame.quit()

if __name__ == "__main__":
    main()
    