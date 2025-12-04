import pygame
from pong.object.bullet.bullet import Bullet
from pong.instance import get_sm
from pong.config.config import *


class YBullet(Bullet):
    """发射后分裂成3颗子弹"""

    def __init__(self, x, y, attack, speed, split_delay=0.3, target_group="enemy"):
        super().__init__(
            fig_path="assets/fig/bullet_green.png",
            x=x,
            y=y,
            attack=attack,
            speed=speed,
            hitbox_size=BULLET_BOX_SIZE,
        )
        self.split_delay = split_delay  # 分裂延迟（秒）
        self.timer = 0
        self.has_split = False
        self.children = []  # 分裂出的子弹
        self.target_group = target_group

    def update(self, dt: float):
        super().update(dt)
        self.timer += dt

        if not self.has_split and self.timer >= self.split_delay:
            self._split()
            self.has_split = True

    def _split(self):
        """分裂成3颗：左斜、直行、右斜"""
        angles = [-30, 0, 30]  # 角度
        base_speed = self.speed.length()

        for angle in angles:
            direction = self.speed.normalize().rotate(angle)
            child = Bullet(
                fig_path="assets/fig/bullet_green.png",
                x=self.pos.x,
                y=self.pos.y,
                attack=1,  # 伤害减半
                speed=direction * base_speed,
            )
            if self.target_group == "enemy":
                get_sm().get_scene.player_bullets.append(child)
            else:
                get_sm().get_scene.enemy_bullets.append(child)

    def draw(self, screen):
        super().draw(screen)
        for child in self.children:
            child.draw(screen)
