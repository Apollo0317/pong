from pong.core import BaseScene
from pong.instance import get_sm
from pong.config.config import *
from pong.object.plane import Player, Enemy
import pygame
import time

class StopScene(BaseScene):
    def __init__(self):
        super().__init__()
        # Initialize stop scene specific attributes here

    def handle_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    print("Resuming to Level1 Scene")
                    get_sm().set_scene(resume=True)

    def update(self, dt, events):
        self.handle_input(events, pygame.key.get_pressed())
        pass

    def draw(self, screen: pygame.Surface):
        self.hud._draw_text(screen, 'Game Stop', (WIDTH/2, HEIGHT/2))
        pass