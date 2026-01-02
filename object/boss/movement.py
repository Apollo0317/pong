import pygame
import math
from abc import ABC, abstractmethod
from pong.config.config import *


class Movement(ABC):
    @abstractmethod
    def update(self, dt: float, owner):
        pass


class StayMovement(Movement):
    """静止不动"""
    def update(self, dt: float, owner):
        pass


class SinewaveMovement(Movement):
    """左右正弦移动"""
    
    def __init__(self, center_x: float = None, amplitude: float = 100, frequency: float = 1.5):
        self.center_x = center_x if center_x is not None else WIDTH // 2
        self.amplitude = amplitude
        self.frequency = frequency
        self.timer = 0
    
    def update(self, dt: float, owner):
        self.timer += dt
        owner.pos.x = self.center_x + math.sin(self.timer * self.frequency) * self.amplitude
        owner.rect.center = owner.pos
        owner.hitbox.center = owner.pos


class WaypointMovement(Movement):
    """按路径点移动"""
    
    def __init__(self, waypoints: list[pygame.Vector2], speed: float = 100, loop: bool = True):
        self.waypoints = waypoints
        self.speed = speed
        self.loop = loop
        self.current_index = 0
        self.waiting = False
        self.wait_timer = 0
        self.wait_time = 0.5  # 到达每个点后等待时间
    
    def update(self, dt: float, owner):
        if self.current_index >= len(self.waypoints):
            if self.loop:
                self.current_index = 0
            else:
                return
        
        # 等待时间
        if self.waiting:
            self.wait_timer += dt
            if self.wait_timer >= self.wait_time:
                self.waiting = False
                self.wait_timer = 0
                self.current_index += 1
            return
        
        target = self.waypoints[self.current_index]
        direction = target - owner.pos
        
        if direction.length() < self.speed * dt:
            owner.pos = target.copy()
            self.waiting = True
        else:
            owner.pos += direction.normalize() * self.speed * dt
        
        owner.rect.center = owner.pos
        owner.hitbox.center = owner.pos


class EnterMovement(Movement):
    """入场移动 - 移动到指定位置后停止"""
    
    def __init__(self, target_pos: pygame.Vector2, speed: float = 150):
        self.target_pos = target_pos
        self.speed = speed
        self.arrived = False
    
    def update(self, dt: float, owner):
        if self.arrived:
            return
        
        direction = self.target_pos - owner.pos
        
        if direction.length() < self.speed * dt:
            owner.pos = self.target_pos.copy()
            self.arrived = True
        else:
            owner.pos += direction.normalize() * self.speed * dt
        
        owner.rect.center = owner.pos
        owner.hitbox.center = owner.pos

# ...existing code...

class TeleportMovement(Movement):
    """瞬移移动"""
    
    def __init__(self, positions: list[pygame.Vector2], teleport_interval: float = 2.0):
        self.positions = positions
        self.teleport_interval = teleport_interval
        self.timer = 0
        self.current_index = 0
        self.initialized = False
    
    def update(self, dt: float, owner):
        if not self.initialized:
            owner.pos = self.positions[0].copy()
            owner.rect.center = owner.pos
            owner.hitbox.center = owner.pos
            self.initialized = True
            return
        
        self.timer += dt
        
        if self.timer >= self.teleport_interval:
            self.timer = 0
            self.current_index = (self.current_index + 1) % len(self.positions)
            owner.pos = self.positions[self.current_index].copy()
            owner.rect.center = owner.pos
            owner.hitbox.center = owner.pos