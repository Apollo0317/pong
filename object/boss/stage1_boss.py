import pygame
from pong.object.boss import *
from pong.config.config import *


def create_stage1_boss() -> Boss:
    """创建第一关 Boss"""
    
    boss = Boss(
        fig_path='assets/fig/boss_1.png',  # 使用你现有的图片
        pos=pygame.Vector2(WIDTH // 2, -50),
        hitbox_size=(64, 64)
    )
    
    nonspell1 = SpellCard(name="「Warmup」", hp=100, time_limit=25)
    nonspell1.add_pattern(CirclePattern(boss, bullet_count=12, interval=1.2, speed=120))
    nonspell1.set_movement(EnterMovement(pygame.Vector2(WIDTH // 2, 120), speed=100))
    
    spell1 = SpellCard(name="旋符「三重螺旋」", hp=100, time_limit=35)
    spell1.add_pattern(SpiralPattern(boss, arms=3, fire_rate=0.06, rotation_speed=80, speed=100))
    spell1.set_movement(SinewaveMovement(WIDTH // 2, 80, 1.0))
    
    spell2 = SpellCard(name="「八方鬼缚阵」", hp=120, time_limit=30)
    spell2.add_pattern(HeavyHomingPattern(
        boss,
        bullets_per_wave= 12,
        max_lifetime= 10,
        cooldown= 0.5,
        speed= 200,
        turn_speed= 100,
        attack= 15
    ))
    spell2.add_pattern(CirclePattern(boss, bullet_count=12, interval=1.2, speed=120))
    spell2.set_movement(SinewaveMovement(WIDTH // 2, 100, 0.8))
    
    # spell2 = SpellCard(name="星符「星屑乱舞」", hp=150, time_limit=40)
    # spell2.add_pattern(CirclePattern(boss, bullet_count=20, interval=1.5, speed=80))
    # spell2.add_pattern(RandomSprayPattern(boss, bullets_per_shot=6, interval=0.4, speed_range=(60, 140)))
    # spell2.set_movement(SinewaveMovement(WIDTH // 2, 120, 0.6))

    spell3 = SpellCard(name="水符「弹幕瀑布」", hp=200, time_limit=60)
    spell3.add_pattern(
        MultiGapCurtainPattern(boss)
    )
    spell3.set_movement(EnterMovement(pygame.Vector2(WIDTH // 2, 100), speed=150))
    
    final_spell = SpellCard(name="终符「银河风暴」", hp=200, time_limit=60)
    final_spell.add_pattern(SpiralPattern(boss, arms=5, fire_rate=0.08, rotation_speed=50, speed=90))
    final_spell.add_pattern(AimedPattern(boss, bullet_count=7, spread=8, interval=1.2, speed=140))
    final_spell.set_movement(WaypointMovement([
        pygame.Vector2(100, 80),
        pygame.Vector2(WIDTH - 100, 80),
        pygame.Vector2(WIDTH // 2, 150),
        pygame.Vector2(100, 120),
        pygame.Vector2(WIDTH - 100, 120),
    ], speed=80, loop=True))
    
    boss.add_spellcard(nonspell1)
    boss.add_spellcard(spell1)
    boss.add_spellcard(spell2)
    # boss.add_spellcard(spell3)
    boss.add_spellcard(final_spell)
    
    return boss