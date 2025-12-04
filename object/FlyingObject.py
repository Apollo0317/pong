import pygame
from pong.config.config import *
from pong.instance import get_sm
from typing import Optional
from pong.input import command


class FlyingObject:
    def __init__(self, fig_path: str, hitbox_size=PLANE_BOX_SIZE, group: str = None):
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.speed = pygame.Vector2(0, 0)
        self.image = pygame.transform.scale(
            pygame.image.load(fig_path).convert_alpha(), SPRITE_SIZE
        )
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = pygame.Rect(0, 0, hitbox_size[0], hitbox_size[1])
        self.hitbox.center = self.rect.center
        self.alive = True
        get_sm().get_scene.register(obj=self, group=group)

    def update(self, dt: float):
        self.pos += self.speed * dt
        self.rect.center = self.pos
        self.hitbox.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def take_damage(self, damage: int):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            self.hp = 0
