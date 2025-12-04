import pygame
from pong.UI.UI import HUD


class BaseScene:
    def __init__(self):
        self.objects = []
        self.players = []
        self.enemies = []
        self.player_bullets = []  # player collision group
        self.enemy_bullets = []  # enemy collision group
        self.bg = None
        self.hud = HUD()
        self.fps = 0
        self.filter_effienct = 0.8

    def set_bg(self, bg):
        self.bg = bg

    def register(self, obj, group=None):
        self.objects.append(obj)
        if group == "player":
            self.players.append(obj)
        elif group == "enemy":
            self.enemies.append(obj)

    def check_bullet_collision(self):
        from pong.utils import check_bullet_hits

        check_bullet_hits(self.player_bullets, self.enemies)
        check_bullet_hits(self.enemy_bullets, self.players)
        self.player_bullets = [b for b in self.player_bullets if b.alive]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.alive]

    def update(self, dt):
        self.fps = int(
            self.filter_effienct * self.fps + (1 - self.filter_effienct) * (1 / dt)
        )

        # 该方法可被子类覆盖，但通常保留此逻辑
        for obj in self.objects:
            obj.update(dt)

        self.check_bullet_collision()

        dead = [o for o in self.objects if not o.alive]
        for obj in dead:
            self.objects.remove(obj)
            if obj in self.players:
                self.players.remove(obj)
            if obj in self.enemies:
                self.enemies.remove(obj)
                if self.players:
                    self.players[0].kill_num += 1

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))

        for obj in sorted(self.objects, key=lambda o: o.layer):
            obj.draw(screen)

        player = self.players[0] if self.players else None
        self.hud.draw(screen, player, self.fps)

        pygame.display.flip()
