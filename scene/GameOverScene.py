from pong.core import BaseScene
from pong.instance import get_sm
from pong.config.config import *
from pong.input import command, CommandType
import pygame
import time


class GameOverScene(BaseScene):
    def __init__(self):
        super().__init__()
        # Initialize stop scene specific attributes here
        self.current_commands = []

    def handle_commands(self, commands: list[command]):
        for command in commands:
            if command.command_type == CommandType.ENTER:
                get_sm().set_scene("MainMenuScene")
                print("Returning to Main Menu Scene")
            if command.command_type == CommandType.QUIT:
                pygame.quit()

    def update(self, dt, commands: list):
        self.handle_commands(commands)

    def draw(self, screen: pygame.Surface):
        self.hud._draw_game_over(screen)
        pass
