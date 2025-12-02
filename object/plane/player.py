from pong.core.FlyingObject import FlyingObject
from pong.object.bullet import YBullet, HomingBullet, Bullet
from pong.instance import get_sm
from pong.utils.collision import check_bullet_hits
from pong.config.config import *
import pygame
import time

PLAYER_HITBOX_SIZE= (16, 16)

class Player(FlyingObject):
    def __init__(self, fig_path):
        super().__init__(fig_path, group='player', hitbox_size= PLAYER_HITBOX_SIZE)
        self.speed_length= DEFAULT_SPEED * 1.5
        self.bullets = []
        self.hp = DEFAULT_HEALTH
        self.last_fire_time = 0
        self.hit_num = 0
        self.kill_num = 0
        self.layer= 1

    def update(self, dt: float):
        self._handle_input(dt)
        super().update(dt)
        
        self.bullets = [b for b in self.bullets if b.alive]
        self.hit_num += check_bullet_hits(self.bullets, get_sm().get_scene.enemies)
        
        self._clamp_to_screen()

    def _handle_input(self, dt: float):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w]
        )
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.speed = direction * self.speed_length
        
        if time.time() - self.last_fire_time > 2*FIRE_INTERVAL*dt:
            if keys[pygame.K_j]:
                self.fire(type='Y')
            elif keys[pygame.K_k]:
                self.fire(type='normal')
            elif keys[pygame.K_l]:
                self.fire(type='trace')
            else:
                return
            self.last_fire_time = time.time()

    def _clamp_to_screen(self):
        self.pos.x = max(self.hitbox.width // 2, min(WIDTH - self.hitbox.width // 2, self.pos.x))
        self.pos.y = max(self.hitbox.height // 2, min(HEIGHT - self.hitbox.height // 2, self.pos.y))
        self.rect.center = self.pos
        self.hitbox.center = self.pos
    
    def fire(self, type='normal'):
        if type == 'Y':
            bullet = YBullet(
                x=self.pos.x,
                y=self.pos.y - SPRITE_SIZE[1] // 4,
                attack=10,
                speed=pygame.Vector2(0, -DEFAULT_SPEED),
                player=self
            )
        elif type == 'normal':
            bullet= Bullet(
                fig_path='assets/fig/bullet.png',
                x= self.pos.x,
                y= self.pos.y - SPRITE_SIZE[1] // 4,
                attack= 5,
                speed= pygame.Vector2(0, -DEFAULT_SPEED),
                hitbox_size= BULLET_BOX_SIZE
            )
        elif type == 'trace':
            bullet= HomingBullet(
                x= self.pos.x,
                y= self.pos.y - SPRITE_SIZE[1] // 4,
                attack= 8,
                speed= pygame.Vector2(0, -DEFAULT_SPEED/2),
                target_group= 'enemy'
            )
        self.bullets.append(bullet)
        pass