import pygame

GRAVITY = 0.6
JUMP = -12
SPEED = 5
DEATH_FRAMES = 45


class Player:
    def __init__(self, x, y, color, keys):
        self.image = pygame.Surface((30, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start = (x, y)
        self.color = color
        self.keys = keys  # (izquierda, derecha, saltar)
        self.sprite = None  # se asigna en build_level
        self.vel_y = 0
        self.on_ground = False
        self.facing = 1
        self.moving = False
        self.anim = "idle"
        self.howl = False
        self.dying = 0
        self.death_total = DEATH_FRAMES
        self.death_by_lava = False

    def kill(self, by_lava=False):
        if not self.dying:
            self.dying = self.death_total
            self.death_by_lava = by_lava
            self.vel_y = 0
            self.anim = "die"

    def respawn(self):
        self.rect.topleft = self.start
        self.vel_y = 0
        self.dying = 0
        self.death_by_lava = False
        self.anim = "idle"

    def update(self, platforms):
        left, right, up = self.keys
        pressed = pygame.key.get_pressed()
        dx = 0
        if pressed[left]:
            dx -= SPEED
        if pressed[right]:
            dx += SPEED
        if pressed[up] and self.on_ground:
            self.vel_y = JUMP
        self.vel_y += GRAVITY

        self.moving = dx != 0
        if dx:
            self.facing = 1 if dx > 0 else -1

        self.rect.x += dx
        for p in platforms:
            if self.rect.colliderect(p):
                if dx > 0:
                    self.rect.right = p.left
                elif dx < 0:
                    self.rect.left = p.right

        self.rect.y += round(self.vel_y)
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vel_y > 0:
                    self.rect.bottom = p.top
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = p.bottom
                self.vel_y = 0

        if not self.on_ground:
            self.anim = "jump"
        elif self.moving:
            self.anim = "walk"
        else:
            self.anim = "idle"