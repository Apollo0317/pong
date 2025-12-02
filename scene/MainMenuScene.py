import pygame
from pong.core import BaseScene
from pong.instance import get_sm
from pong.UI.UI import HUD
from pong.config.config import *

class MainMenuScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.hud= HUD()
        self.draw_test_msg= False
        # Initialize main menu specific attributes here

    def handle_input(self, events, pressed_keys):
        for event in events:
            if event == pygame.QUIT:
                pygame.quit()

        if pressed_keys[pygame.K_SPACE]:
            get_sm().set_scene('Level1')  # Switch to Level1 scene
            print("Switching to Level1 Scene")

    def update(self, dt: float, events:list[pygame.event.Event]):
        self.handle_input(events, pygame.key.get_pressed())

    def draw(self, screen:pygame.Surface):
        if hasattr(self, 'bg'):
            screen.blit(self.bg, (0, 0))
        # Draw main menu elements here
        font = pygame.font.Font(None, 74)
        text = font.render("Main Menu", True, (255, 255, 255))
        screen.blit(text, (100, 100))

        if self.draw_test_msg:
            test_font = pygame.font.Font(None, 50)
            test_text = test_font.render("Space Key Pressed!", True, (255, 0, 0))
            screen.blit(test_text, (100, 200))