import pygame
from pong.UI.UI import HUD

class GameManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init()
        return cls._instance
    
    def _init(self):
        self.objects: list = []
        self.players: list = []
        self.enemies: list = []
        self.bg: pygame.Surface = None
        self.hud: HUD = HUD()
        self.fps: int = 0
    
    def set_bg(self, bg: pygame.Surface):
        self.bg = bg
    
    def register(self, obj, group: str = None):
        self.objects.append(obj)
        if group == 'player':
            self.players.append(obj)
        elif group == 'enemy':
            self.enemies.append(obj)
    
    def update_all(self, dt: float):
        for obj in self.objects:
            obj.update(dt)
        
        # 统一清理所有死亡对象
        dead = [o for o in self.objects if not o.alive]
        for obj in dead:
            self.objects.remove(obj)
            if obj in self.players:
                self.players.remove(obj)
            if obj in self.enemies:
                self.enemies.remove(obj)
                self.players[0].kill_num += 1

    def get_fps(self, dt: float) -> int:
        self.fps = int(1/dt) if dt > 0 else 0
    
    def draw(self, screen: pygame.Surface):
        screen.blit(self.bg, (0, 0))
        for obj in sorted(self.objects, key=lambda o: o.layer):
            obj.draw(screen)

        player = self.players[0] if self.players else None
        self.hud.draw(screen, player,self.fps)

        pygame.display.flip()

# 单例
gm = GameManager()