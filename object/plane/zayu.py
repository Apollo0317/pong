from pong.object.plane.enemy import Enemy
from typing import override
from pong.object.bullet import Bullet, YBullet, HomingBullet
from pong.config.config import *
from pong.instance import get_sm
import pygame, random

ZAYUA_HEALTH = 20


class ZayYuA(Enemy):
    def __init__(self, pos: pygame.Vector2, hitbox_size: tuple[int, int]):
        fig_path = "assets/fig/zayuA.png"
        super().__init__(fig_path, pos, hitbox_size)

    def fire(self):
        bullet_type = random.choice([HomingBullet])
        bullet = bullet_type(
            x=self.pos.x,
            y=self.pos.y + self.hitbox.height // 2,
            attack=10,
            speed=pygame.Vector2(0, DEFAULT_SPEED / 2),
            target_group="player",
        )
        get_sm().get_scene.enemy_bullets.append(bullet)


class ZayYuB(Enemy):
    def __init__(self, pos: pygame.Vector2, hitbox_size: tuple[int, int]):
        fig_path = "assets/fig/zayuB.png"
        super().__init__(fig_path, pos, hitbox_size)

    def fire(self):
        bullet_type = random.choice([YBullet])
        bullet = bullet_type(
            x=self.pos.x,
            y=self.pos.y + self.hitbox.height // 2,
            attack=15,
            speed=pygame.Vector2(0, DEFAULT_SPEED),
            target_group="player",
        )
        get_sm().get_scene.enemy_bullets.append(bullet)
