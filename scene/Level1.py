from pong.core import BaseScene
from pong.instance import get_sm
from pong.config.config import *
from pong.object.plane import Player
from pong.utils import enemy_generator
from pong.input import command, CommandType
import pygame
import time


class Level1(BaseScene):
    def __init__(self):
        super().__init__()
        self.last_spawn_time = time.time()
        # Initialize level-specific attributes here
        self.player = Player("assets/fig/player.png")
        self.register(self.player, group="player")
        self.change_scene = False
        self.current_commands = []

    def handle_commands(self, commands: list[command]):
        for command in commands:
            if command.command_type == CommandType.PAUSE:
                print("Pausing the game")
                get_sm().set_scene("StopScene", keep=True)
            if command.command_type == CommandType.QUIT:
                pygame.quit()
        self.current_commands = commands

    def update(self, dt, commands: list):
        self.handle_commands(commands)

        # Update level-specific logic here
        super().update(dt)

        cur_time = time.time()
        if cur_time - self.last_spawn_time > 3:
            enemy_generator()
            self.last_spawn_time = cur_time

        if self.player.hp <= 0:
            print("Player defeated!")
            get_sm().set_scene("GameOverScene")

    def draw(self, screen: pygame.Surface):
        super().draw(screen)
