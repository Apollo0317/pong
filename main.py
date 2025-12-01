import sys
sys.path.append('../')
import pygame
from pong.config.config import SCREEN_SIZE, FPS
from pong.plane.player import Player
from pong.renderer import Renderer



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
    renderer= Renderer(bg=background)
    player= Player(fig_path='assets/fig/player.png', renderer= renderer)

    dt= 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        player.update(dt)
        renderer.draw(screen)

        dt= clock.tick(FPS) / 1000  # seconds passed since last frame



    

    pass

if __name__ == '__main__':
    main()