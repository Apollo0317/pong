import pygame
from config.config import *
from pong.plane.FlyingObject import FlyingObject
from typing import override
from pong.plane.bullet import Bullet
import time

class Player(FlyingObject):

    def __init__(self, fig_path, renderer):
        super().__init__(fig_path, renderer)
        self.bullets:list[Bullet]= []
        self.layer= 1
        self.last_fire_time= 0

    def fire(self):
        bullet= Bullet(
            fig_path='assets/fig/bullet.png',
            x= self.pos.x,
            y= self.pos.y - SPRITE_SIZE[1] // 4,
            attack= 10,
            renderer= self.renderer
        )
        self.bullets.append(bullet)
        pass

    @override
    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0,0)

        if keys[pygame.K_w]: direction.y -= 1
        if keys[pygame.K_s]: direction.y += 1
        if keys[pygame.K_a]: direction.x -= 1
        if keys[pygame.K_d]: direction.x += 1
        if keys[pygame.K_k]: 
            if time.time() - self.last_fire_time > FIRE_INTERVAL*dt:
                self.fire()
                self.last_fire_time= time.time()

        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.speed = direction * DEFAULT_SPEED

        self.pos += self.speed * dt
        self.rect.center = self.pos

        # boundary
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > HEIGHT: self.rect.bottom = HEIGHT

        self.pos = pygame.Vector2(self.rect.center)

        #update bullets
        alives= [ bullet.update(dt) for bullet in self.bullets]
        self.bullets= [ bullet for i, bullet in enumerate(self.bullets) if alives[i] ]



        