import pygame
from config.config import *
from pong.object.FlyingObject import FlyingObject
from pong.utils.collision import check_bullet_hits
from pong.instance import get_sm
from pong.object.bullet import Bullet
import time, random

ENEMY_FIRE_INTERVAL= 60
ENEMY_HEALTH= 20

class Enemy(FlyingObject):

    def __init__(self, fig_path:str, pos:pygame.Vector2, hitbox_size:int= PLANE_BOX_SIZE):
        super().__init__(fig_path, hitbox_size= hitbox_size, group='enemy')
        self.pos= pos
        self.rect.center= self.pos
        self.hitbox.center= self.pos
        self.image= pygame.transform.flip(self.image, False, True)
        self.bullets:list[Bullet]= []
        self.layer= 1
        self.last_fire_time= 0
        self.speed= pygame.Vector2(0, ENEMY_SPEED)
        self.hp= ENEMY_HEALTH

    @staticmethod
    def enemy_generator():
        y=0 # spawn at top
        x= random.randint(0, WIDTH)
        enemy= Enemy(
            fig_path='assets/fig/enemy.png',
            pos= pygame.Vector2(x, y),
            hitbox_size= PLANE_BOX_SIZE
        )

        return enemy

        pass

    def fire(self):
        bullet= Bullet(
            fig_path='assets/fig/bullet.png',
            x= self.pos.x,
            y= self.pos.y + SPRITE_SIZE[1] // 4,
            attack= 5,
            speed= pygame.Vector2(0, DEFAULT_SPEED*2),
            hitbox_size= BULLET_BOX_SIZE
        )
        self.bullets.append(bullet)
        pass

    def is_in_sight(self)->bool:
        if not (0 <= self.pos.x <= WIDTH and 0 <= self.pos.y <= HEIGHT):
            return False
        return True

    def update(self, dt: float):
        super().update(dt)

        self.bullets= [bullet for bullet in self.bullets if bullet.alive]

        #check if bullets collide with player
        check_bullet_hits(self.bullets, get_sm().get_scene.players)

        # fire every interval
        current_time= time.time()
        if current_time - self.last_fire_time >= ENEMY_FIRE_INTERVAL*dt:
            self.fire()
            self.last_fire_time= current_time

        # boundary
        if not self.is_in_sight():
            self.alive= False
            return




        