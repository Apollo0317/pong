import pygame
from pong.config.config import *

class SceneManager:
    def __init__(self, screen: pygame.Surface = None):
        self.current_scene = None
        self.screen = screen
        self.bg= pygame.transform.scale(
            pygame.image.load('assets/fig/bg.png').convert(),
            self.screen.get_size()
        )
        self.prev_scene= None

    def set_scene(self, scene:str=None, keep:bool=False, resume:bool=False):
        """
        Args:
            scene (str): The name of the scene to switch to.
            keep (bool): Whether to keep the current scene in memory. Defaults to False.
        """

        if resume and self.prev_scene is not None:
            self.current_scene= self.prev_scene
            self.prev_scene= None
            print("Resuming previous scene")
            return
        
        if keep:
            self.prev_scene= self.current_scene
            print("Keeping previous scene in memory.")
        
        cur_scene= None
        match scene:
            case 'MainMenuScene':
                from pong.scene.MainMenuScene import MainMenuScene
                cur_scene = MainMenuScene()
                cur_scene.set_bg(self.bg)
            case 'Level1':
                from pong.scene.Level1 import Level1
                cur_scene = Level1()
                cur_scene.set_bg(self.bg)
            case 'StopScene':
                from pong.scene.StopScene import StopScene
                cur_scene = StopScene()
                cur_scene.set_bg(self.bg)
            case _:
                raise ValueError(f"Scene '{scene}' not recognized.")
        self.current_scene = cur_scene
        
        

    @property
    def get_scene(self):
        return self.current_scene
    
    def update(self, dt, events):
        if self.current_scene:
            self.current_scene.update(dt, events)

    def draw(self):
        if self.current_scene:
            self.current_scene.draw(self.screen)