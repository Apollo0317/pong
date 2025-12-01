import sys
sys.path.append('../')
import pygame
from pong.config.config import *
from pong.plane.player import Player
from pong.plane.enemy import Enemy
from pong.manager.GameManager import gm
import time



def game_init():
    pygame.init()
    screen= pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Pong")
    clock= pygame.time.Clock()
    return screen, clock


def main():
    screen, clock= game_init()

    background= pygame.transform.scale(
        pygame.image.load('assets/fig/bg.png').convert(),
        SCREEN_SIZE
    )

    gm.set_bg(background)

    Player(fig_path='assets/fig/player.png')

    dt= 0

    last_enemy_spawn_time= time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if time.time() - last_enemy_spawn_time >= DEFAULT_ENEMY_SPAWN_INTERVAL * dt:
            Enemy.enemy_generator()
            last_enemy_spawn_time= time.time()

        gm.update_all(dt)
        gm.draw(screen)

        dt= clock.tick(FPS) / 1000  # seconds passed since last frame
        gm.get_fps(dt)



    

    pass

if __name__ == '__main__':
    main()