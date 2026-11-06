import pygame

GRAVITY = 0.6
JUMP = -12
SPEED = 5

class Player:
    def __init__(self, x, y, color, keys):
        self.image = pygame.Surface((30, 40))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start = (x, y)
        self.color = color
        self.keys = keys  # (izquierda, derecha, saltar)
        self.vel_y = 0
        self.on_ground = False

    def respawn(self):
        self.rect.topleft = self.start
        self.vel_y = 0

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