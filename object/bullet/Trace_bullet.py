import pygame
from pong.object.bullet.bullet import Bullet
from pong.instance import get_sm
from pong.config.config import *

class HomingBullet(Bullet):
    """追踪子弹 - 自动追踪最近的敌人"""
    
    def __init__(self, x, y, attack, speed, turn_speed=2, target_group='enemy'):
        super().__init__(
            fig_path='assets/fig/bullet_blue.png',
            x=x, y=y,
            attack=attack,
            speed=speed,
            hitbox_size= BULLET_BOX_SIZE
        )
        self.turn_speed = turn_speed  # 转向速度
        self.target_group = target_group  # 目标组别
        self.minimum_y_speed = 100
    
    def update(self, dt: float):
        target = self._find_nearest_target()
        
        if target:
            # 计算朝向目标的方向
            to_target = target.pos - self.pos
            if to_target.length() > 0:
                desired = to_target.normalize() * self.speed.length()
                # 平滑转向
                self.speed = self.speed.lerp(desired, self.turn_speed * dt)
                if self.target_group == 'enemy':
                    self.speed.y = min(self.speed.y, -self.minimum_y_speed)
                else:
                    self.speed.y = max(self.speed.y, self.minimum_y_speed)
        
        super().update(dt)
    
    def _find_nearest_target(self):
        sm= get_sm()
        if self.target_group == 'enemy':
            targets = sm.get_scene.enemies
        else:
            targets = sm.get_scene.players
        nearest = None
        min_dist = float('inf')
        
        for t in targets:
            if not t.alive:
                continue
            dist = (t.pos - self.pos).length()
            if dist < min_dist:
                min_dist = dist
                nearest = t
        return nearest