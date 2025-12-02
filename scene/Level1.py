from pong.core import BaseScene
from pong.instance import get_sm
from pong.config.config import *
from pong.object.plane import Player
from pong.utils import enemy_generator
import pygame
import time

class Level1(BaseScene):
    def __init__(self):
        super().__init__()
        self.last_spawn_time = time.time()
        # Initialize level-specific attributes here
        self.player= Player('assets/fig/player.png')
        self.register(self.player, group='player')

    def handle_input(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    print("Pausing the game")
                    get_sm().set_scene('StopScene', keep=True)

    def update(self, dt, events):

        if events is None:
            events= []
        self.handle_input(events, pygame.key.get_pressed())
        
        # Update level-specific logic here
        super().update(dt)

        cur_time= time.time()
        if cur_time - self.last_spawn_time > 3:
            enemy_generator()
            self.last_spawn_time= cur_time

        if self.player.hp <= 0:
            print("Player defeated! Returning to Main Menu.")
            get_sm().set_scene('MainMenuScene')



        

    def draw(self, screen: pygame.Surface):
        super().draw(screen)

