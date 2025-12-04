import sys

sys.path.append("../")
import pygame
from pong.config.config import *
from pong.object.plane.player import Player
from pong.object.plane.enemy import Enemy
from pong.core import SceneManager
from pong.scene.MainMenuScene import MainMenuScene
from pong.instance import set_sm
from pong.input import InputHandler_Keyboard
import time


def game_init():
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    return screen, clock


def game_clear():
    pass


def main():
    screen, clock = game_init()

    sm = SceneManager(screen=screen)
    set_sm(sm)

    input_handler = InputHandler_Keyboard()

    main_menu_scene = MainMenuScene()

    background = pygame.transform.scale(
        pygame.image.load("assets/fig/bg.png").convert(), SCREEN_SIZE
    )

    main_menu_scene.set_bg(background)

    sm.set_scene("MainMenuScene")

    while True:
        dt = clock.tick(FPS) / 1000

        events = pygame.event.get()
        commands = input_handler.translate_input(pygame.key.get_pressed(), events)

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        sm.update(dt, commands)

        sm.draw()

        pygame.display.flip()

    pass


if __name__ == "__main__":
    main()
