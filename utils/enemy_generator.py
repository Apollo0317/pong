from pong.config.config import *
from pong.object.bullet import Bullet, YBullet, HomingBullet
import random
import pygame

ZayYuA_PROB= 0.5
ZayYuB_PROB= 0.5

def enemy_generator():

    from pong.object.plane import ZayYuA, ZayYuB

    y=0 # spawn at top
    x= random.randint(0, WIDTH)

    enemy_type= random.choices(
        population= [ZayYuA, ZayYuB],
        weights= [ZayYuA_PROB, ZayYuB_PROB],
        k=1
    )[0]

    enemy_type(
        pos= pygame.Vector2(x, y),
        hitbox_size= PLANE_BOX_SIZE
    )
