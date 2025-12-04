import pygame
from pong.core import BaseScene
from pong.instance import get_sm
from pong.UI.UI import HUD
from pong.config.config import *
from pong.input import command, CommandType


class MainMenuScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.hud = HUD()
        self.draw_test_msg = False
        # Initialize main menu specific attributes here

    def handle_input(self, events, pressed_keys):
        for event in events:
            if event == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    get_sm().set_scene("Level1")  # Switch to Level1 scene

    def handle_commands(self, commands: list[command]):
        for command in commands:
            if command.command_type == CommandType.ENTER:
                get_sm().set_scene("Level1")  # Switch to Level1 scene
            if command.command_type == CommandType.QUIT:
                pygame.quit()

    def update(self, dt, commands: list[command]):
        self.handle_commands(commands)

    def draw(self, screen: pygame.Surface):
        if hasattr(self, "bg"):
            screen.blit(self.bg, (0, 0))
        # Draw main menu elements here
        font = pygame.font.Font(None, 74)
        text = font.render("Main Menu", True, (255, 255, 255))
        screen.blit(text, (100, 100))
