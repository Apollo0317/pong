import pygame
from pong.config.config import WIDTH, HEIGHT, DEFAULT_SPEED, SPRITE_SIZE
from pong.renderer import Renderer

class FlyingObject:
    def __init__(self, fig_path: str, renderer: Renderer):
        self.pos = pygame.Vector2(WIDTH // 2, HEIGHT // 2)
        self.speed = pygame.Vector2(0, 0)
        self.image = pygame.transform.scale(
            pygame.image.load(fig_path).convert_alpha(),
            SPRITE_SIZE
        )
        self.rect = self.image.get_rect(center=self.pos)
        self.alive = True
        self.renderer = renderer
        self.renderer.register(self)

    def update(self, dt: float):
        self.pos += self.speed * dt
        self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)



