import pygame

class Renderer:
    def __init__(self, bg:pygame.Surface):
        self.objects:list = []
        self.bg = bg

    def register(self, obj):
        self.objects.append(obj)

    def unregister(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def draw(self, screen:pygame.Surface):
        screen.blit(self.bg, (0, 0))
        for obj in sorted(self.objects, key=lambda o: o.layer):
            obj.draw(screen)
        pygame.display.flip()
