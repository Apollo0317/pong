import pygame
from pong.object.FlyingObject import FlyingObject
from pong.object.boss.SpellCard import SpellCard
from pong.config.config import *

BOSS_SPRITE_SIZE = (256, 256)

class Boss(FlyingObject):
    def __init__(self, fig_path: str, pos: pygame.Vector2, hitbox_size=BOSS_SPRITE_SIZE):
        super().__init__(fig_path, group="enemy", hitbox_size=hitbox_size)
        self.image = pygame.transform.scale(
            self.image, BOSS_SPRITE_SIZE
        )
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = pygame.Rect(0, 0, hitbox_size[0], hitbox_size[1])
        self.hitbox.center = self.rect.center
        self.image = pygame.transform.flip(self.image, False, True)
        self.pos = pos
        self.rect.center = self.pos
        self.hitbox.center = self.pos
        
        self.spellcards: list[SpellCard] = []
        self.current_spell_index = 0
        self.layer = 2
        
        self.invincible = False
        self.invincible_timer = 0
        self.flash_timer = 0  # 无敌闪烁
    
    def add_spellcard(self, spellcard: SpellCard):
        self.spellcards.append(spellcard)
        return self
    
    @property
    def current_spell(self) -> SpellCard:
        if self.current_spell_index < len(self.spellcards):
            return self.spellcards[self.current_spell_index]
        return None
    
    @property
    def hp(self):
        if self.current_spell:
            return self.current_spell.hp
        return 0
    
    @hp.setter
    def hp(self, value):
        if self.current_spell:
            self.current_spell.hp = value
    
    def update(self, dt: float):
        # 无敌时间
        if self.invincible:
            self.invincible_timer -= dt
            self.flash_timer += dt
            if self.invincible_timer <= 0:
                self.invincible = False
                self.flash_timer = 0
        
        spell = self.current_spell
        if spell is None:
            self.alive = False
            print("=== BOSS DEFEATED ===")
            return
        
        # 更新当前符卡
        spell.update(dt, self)
        
        # 符卡结束，切换下一张
        if spell.finished:
            self._next_spellcard()
        
        # 更新位置同步
        self.rect.center = self.pos
        self.hitbox.center = self.pos
    
    def _next_spellcard(self):
        self.current_spell_index += 1
        self.invincible = True
        self.invincible_timer = 2.0  # 2秒无敌
        
        if self.current_spell:
            print(f"=== Spellcard: {self.current_spell.name} ===")
        
        # 清除屏幕上所有敌方子弹
        self._clear_enemy_bullets()
    
    def _clear_enemy_bullets(self):
        """切换符卡时清除所有敌方子弹"""
        from pong.instance import get_sm
        scene = get_sm().get_scene
        if scene:
            for bullet in scene.enemy_bullets:
                bullet.alive = False
    
    def take_damage(self, damage: int):
        """受到伤害"""
        if self.invincible:
            return
        
        if self.current_spell:
            self.current_spell.hp -= damage
            if self.current_spell.hp <= 0:
                self.current_spell.hp = 0
                self.current_spell.finished = True
    
    def draw(self, screen):
        # 无敌时闪烁
        if self.invincible:
            if int(self.flash_timer * 10) % 2 == 0:
                super().draw(screen)
        else:
            super().draw(screen)
        
        # 绘制 Boss 血条
        self._draw_boss_hp_bar(screen)
        
        # 绘制符卡名称
        self._draw_spell_name(screen)
    
    def _draw_boss_hp_bar(self, screen):
        bar_width = WIDTH - 100
        bar_height = 12
        x, y = 50, 20
        
        # 背景
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))
        
        # 当前血量
        if self.current_spell and self.current_spell.max_hp > 0:
            ratio = max(0, self.current_spell.hp / self.current_spell.max_hp)
            color = (255, 50, 50) if ratio > 0.3 else (255, 150, 50)
            pygame.draw.rect(screen, color, (x, y, int(bar_width * ratio), bar_height))
        
        # 边框
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        # 符卡数量指示（星星）
        star_y = y + bar_height + 8
        for i in range(len(self.spellcards)):
            color = (255, 255, 100) if i >= self.current_spell_index else (80, 80, 80)
            pygame.draw.circle(screen, color, (x + i * 25 + 10, star_y), 8)
            pygame.draw.circle(screen, (255, 255, 255), (x + i * 25 + 10, star_y), 8, 1)
    
    def _draw_spell_name(self, screen):
        if self.current_spell and self.current_spell.name:
            # font = pygame.font.Font(None, 28)
            font= pygame.font.Font('/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc', 28)
            text = font.render(self.current_spell.name, True, (255, 255, 255))
            rect = text.get_rect(topright=(WIDTH - 20, 50))
            
            # 背景
            bg_rect = rect.inflate(20, 10)
            pygame.draw.rect(screen, (0, 0, 0, 128), bg_rect)
            pygame.draw.rect(screen, (255, 200, 100), bg_rect, 2)
            
            screen.blit(text, rect)