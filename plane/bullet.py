import pygame
from config.config import WIDTH, HEIGHT, DEFAULT_SPEED, SPRITE_SIZE
from pong.plane.FlyingObject import FlyingObject
from typing import override

class Bullet(FlyingObject):
    def __init__(self, fig_path: str, x, y, attack:int, renderer):
        super().__init__(fig_path, renderer)
        self.pos = pygame.Vector2(x, y)
        self.rect.center = self.pos
        self.attack = attack
        self.speed = pygame.Vector2(0, -DEFAULT_SPEED * 1.5)
        self.layer = 2

    @override
    def update(self, dt: float):
        self.pos += self.speed * dt
        self.rect.center = self.pos

        # out of screen
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            return False
        if self.rect.right < 0 or self.rect.left > WIDTH:
            return False
        return True
