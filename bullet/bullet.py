import pygame
from config.config import *
from pong.plane.FlyingObject import FlyingObject

class Bullet(FlyingObject):
    def __init__(self, fig_path: str, x, y, attack:int, speed:pygame.Vector2, hitbox_size= BULLET_BOX_SIZE):
        super().__init__(fig_path, hitbox_size= hitbox_size)
        self.pos = pygame.Vector2(x, y)
        self.rect.center = self.pos
        self.attack = attack
        self.speed = speed
        self.layer = 2

    def is_in_sight(self)->bool:
        if not (0 <= self.pos.x <= WIDTH and 0 <= self.pos.y <= HEIGHT):
            return False
        return True
    
    def update(self, dt: float):
        super().update(dt)

        # out of screen
        if not self.is_in_sight():
            self.alive= False
