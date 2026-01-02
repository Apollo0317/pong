import pygame
import math
from pong.core import BaseScene
from pong.instance import get_sm
from pong.UI.UI import HUD
from pong.config.config import *
from pong.input import command, CommandType


class MainMenuScene(BaseScene):
    def __init__(self):
        super().__init__()
        self.hud = HUD()
        
        # 菜单选项
        self.menu_items = [
            {"text": "Stage 1 - 初始试炼", "scene": "Level1"},
            {"text": "Stage 2 - 时空守护者", "scene": "Level2"},
            {"text": "Stage 3 - 混沌之主", "scene": "Level3"},
            {"text": "退出游戏", "scene": None},
        ]
        self.selected_index = 0
        
        # 字体
        self._init_fonts()
        
        # 动画
        self.title_offset = 0
        self.title_timer = 0
        self.cursor_blink = 0

    def _init_fonts(self):
        """初始化字体"""
        font_paths = [
            'assets/fonts/SourceHanSansCN-Regular.otf',
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
        ]
        
        self.title_font = None
        self.menu_font = None
        self.hint_font = None
        
        for path in font_paths:
            try:
                self.title_font = pygame.font.Font(path, 56)
                self.menu_font = pygame.font.Font(path, 32)
                self.hint_font = pygame.font.Font(path, 20)
                break
            except:
                continue
        
        if self.title_font is None:
            self.title_font = pygame.font.Font(None, 56)
            self.menu_font = pygame.font.Font(None, 32)
            self.hint_font = pygame.font.Font(None, 20)

    def handle_commands(self, commands: list[command]):
        for cmd in commands:
            # 使用专门的菜单命令
            if cmd.command_type == CommandType.MENU_UP:
                self.selected_index = (self.selected_index - 1) % len(self.menu_items)
            
            if cmd.command_type == CommandType.MENU_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.menu_items)
            
            if cmd.command_type == CommandType.ENTER:
                self._select_current()
            
            if cmd.command_type == CommandType.QUIT:
                pygame.quit()
                exit()

    def _select_current(self):
        """选择当前项"""
        item = self.menu_items[self.selected_index]
        if item["scene"] is None:
            pygame.quit()
            exit()
        else:
            get_sm().set_scene(item["scene"])

    def update(self, dt, commands: list[command]):
        self.handle_commands(commands)
        
        self.title_timer += dt
        self.title_offset = math.sin(self.title_timer * 2) * 5
        self.cursor_blink += dt

    def draw(self, screen: pygame.Surface):
        screen.fill((15, 15, 35))
        self._draw_background_decoration(screen)
        self._draw_title(screen)
        self._draw_menu(screen)
        self._draw_hints(screen)

    def _draw_background_decoration(self, screen: pygame.Surface):
        """绘制背景装饰"""
        import random
        random.seed(42)
        for _ in range(50):
            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)
            brightness = random.randint(100, 255)
            size = random.randint(1, 3)
            flicker = int(math.sin(self.title_timer * random.uniform(1, 3) + random.uniform(0, 6.28)) * 50)
            color = max(0, min(255, brightness + flicker))
            pygame.draw.circle(screen, (color, color, color), (x, y), size)

    def _draw_title(self, screen: pygame.Surface):
        """绘制标题"""
        title_text = "Pong"
        
        # 阴影
        shadow_surface = self.title_font.render(title_text, True, (50, 50, 80))
        shadow_rect = shadow_surface.get_rect(center=(WIDTH // 2 + 3, 83 + self.title_offset))
        screen.blit(shadow_surface, shadow_rect)
        
        # 标题
        title_surface = self.title_font.render(title_text, True, (255, 220, 100))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, 80 + self.title_offset))
        screen.blit(title_surface, title_rect)
        
        # 副标题
        subtitle = "Bullet Hell"
        subtitle_surface = self.hint_font.render(subtitle, True, (150, 150, 200))
        subtitle_rect = subtitle_surface.get_rect(center=(WIDTH // 2, 130))
        screen.blit(subtitle_surface, subtitle_rect)

    def _draw_menu(self, screen: pygame.Surface):
        """绘制菜单选项"""
        menu_start_y = 200
        item_height = 60
        
        for i, item in enumerate(self.menu_items):
            y = menu_start_y + i * item_height
            is_selected = (i == self.selected_index)
            
            if is_selected:
                # 选中背景
                bg_rect = pygame.Rect(WIDTH // 2 - 180, y - 5, 360, 45)
                pygame.draw.rect(screen, (60, 60, 120), bg_rect, border_radius=8)
                pygame.draw.rect(screen, (150, 150, 255), bg_rect, 2, border_radius=8)
                
                # 箭头指示器
                cursor_x = WIDTH // 2 - 200
                if int(self.cursor_blink * 3) % 2 == 0:
                    points = [
                        (cursor_x, y + 15),
                        (cursor_x + 15, y + 22),
                        (cursor_x, y + 29),
                    ]
                    pygame.draw.polygon(screen, (255, 220, 100), points)
                
                text_color = (255, 255, 255)
            else:
                text_color = (150, 150, 180)
            
            text_surface = self.menu_font.render(item["text"], True, text_color)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, y + 17))
            screen.blit(text_surface, text_rect)

    def _draw_hints(self, screen: pygame.Surface):
        """绘制操作提示"""
        hints = ["W/S - 选择", "Space - 确认", "Q - 退出"]
        hint_y = HEIGHT - 80
        
        bg_rect = pygame.Rect(WIDTH // 2 - 150, hint_y - 10, 300, len(hints) * 25 + 20)
        pygame.draw.rect(screen, (30, 30, 60), bg_rect, border_radius=5)
        pygame.draw.rect(screen, (80, 80, 120), bg_rect, 1, border_radius=5)
        
        for i, hint in enumerate(hints):
            hint_surface = self.hint_font.render(hint, True, (120, 120, 150))
            hint_rect = hint_surface.get_rect(center=(WIDTH // 2, hint_y + i * 25 + 10))
            screen.blit(hint_surface, hint_rect)