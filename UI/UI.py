import pygame
from pong.config.config import *

class HUD:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)  # None 使用默认字体，36 是字号
        # 或使用自定义字体：
        # self.font = pygame.font.Font('assets/fonts/pixel.ttf', 36)
        
        self.text_color = (255, 255, 255)  # 白色
        self.shadow_color = (0, 0, 0)      # 黑色阴影
    
    def draw(self, screen, player, fps):
        if player is None or not player.alive:
            self._draw_game_over(screen)
            return
        
        # 血量
        hp_text = f"HP: {player.hp}"
        self._draw_text(screen, hp_text, (10, 10))
        
        # 击杀数
        kills_text = f"Kills: {player.kill_num}"
        self._draw_text(screen, kills_text, (10, 50))

        # FPS
        fps_text = f"FPS: {fps}"
        self._draw_text(screen, fps_text, (WIDTH - 150, 10))
        
        # 可选：绘制血条
        self._draw_health_bar(screen, player)
    
    def _draw_text(self, screen, text: str, pos: tuple):
        # 绘制阴影（偏移1像素）
        shadow = self.font.render(text, True, self.shadow_color)
        screen.blit(shadow, (pos[0] + 1, pos[1] + 1))
        
        # 绘制文本
        surface = self.font.render(text, True, self.text_color)
        screen.blit(surface, pos)
    
    def _draw_health_bar(self, screen, player):
        bar_width = 100
        bar_height = 20
        x, y = 10, 90
        
        # 背景（灰色）
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
        
        # 当前血量（绿色->红色）
        hp_ratio = player.hp / DEFAULT_HEALTH
        color = (int(255 * (1 - hp_ratio)), int(255 * hp_ratio), 0)
        pygame.draw.rect(screen, color, (x, y, bar_width * hp_ratio, bar_height))
        
        # 边框
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
    
    def _draw_game_over(self, screen):
        text = "GAME OVER"
        surface = self.font.render(text, True, (255, 0, 0))
        rect = surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(surface, rect)