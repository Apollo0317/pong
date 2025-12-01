import pygame
from pong.plane.FlyingObject import FlyingObject

class Enemy(FlyingObject):
    def __init__(self, fig_path: str):
        super().__init__(fig_path)