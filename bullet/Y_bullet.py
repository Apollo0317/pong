import pygame
from pong.bullet.bullet import Bullet
from pong.config.config import *

class YBullet(Bullet):
    """发射后分裂成3颗子弹"""
    
    def __init__(self, x, y, attack, speed, player, split_delay=0.3):
        super().__init__(
            fig_path='assets/fig/bullet_green.png',
            x=x, y=y,
            attack=attack,
            speed=speed
        )
        self.split_delay = split_delay  # 分裂延迟（秒）
        self.timer = 0
        self.has_split = False
        self.children = []  # 分裂出的子弹
        self.player = player  # 引用玩家对象，便于访问属性
    
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
                fig_path='assets/fig/bullet_green.png',
                x=self.pos.x,
                y=self.pos.y,
                attack= 1 ,  # 伤害减半
                speed=direction * base_speed
            )
            self.player.bullets.append(child)
    
    def draw(self, screen):
        super().draw(screen)
        for child in self.children:
            child.draw(screen)