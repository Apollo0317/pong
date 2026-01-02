import pygame
from pong.object.boss import *
from pong.config.config import *


def create_stage2_boss() -> Boss:
    """创建第二关 Boss - 时空守护者"""
    
    boss = Boss(
        fig_path='assets/fig/boss_2.png',
        pos=pygame.Vector2(WIDTH // 2, -50),
        hitbox_size=(64, 64)
    )
    
    # ========== 非符1：入场 - 时间涟漪 ==========
    nonspell1 = SpellCard(name="「Time Ripple」", hp=120, time_limit=30)
    nonspell1.add_pattern(RingExpandPattern(
        boss, rings=999, bullets_per_ring=20, ring_interval=0.8, speed=80, speed_increment=0
    ))
    nonspell1.set_movement(EnterMovement(pygame.Vector2(WIDTH // 2, 100), speed=80))
    
    # ========== 符卡1：时停弹幕 - 子弹先静止再同时启动 ==========
    spell1 = SpellCard(name="时符「时间停止」", hp=150, time_limit=40)
    spell1.add_pattern(TimeStopPattern(
        boss, 
        freeze_duration=1.5,      # 冻结1.5秒
        bullets_during_freeze=40, # 冻结期间发射40发
        release_speed=120         # 释放后速度
    ))
    spell1.set_movement(SinewaveMovement(WIDTH // 2, 120, 0.5))
    
    # ========== 非符2：交错十字 ==========
    nonspell2 = SpellCard(name="「Cross Dimension」", hp=130, time_limit=30)
    nonspell2.add_pattern(CrossPattern(boss, fire_rate=0.06, rotation_speed=45, speed=140))
    nonspell2.add_pattern(CrossPattern(boss, fire_rate=0.06, rotation_speed=-45, speed=140))
    nonspell2.set_movement(WaypointMovement([
        pygame.Vector2(120, 100),
        pygame.Vector2(WIDTH - 120, 100),
    ], speed=100, loop=True))
    
    # ========== 符卡2：时间回溯 - 子弹飞出后倒退回来 ==========
    spell2 = SpellCard(name="时符「时间回溯」", hp=240, time_limit=45)
    spell2.add_pattern(TimeReversePattern(
        boss,
        bullet_count=16,
        travel_time=3.5 ,    # 飞行1.2秒后开始倒退
        interval=1.5,
        speed=150
    ))
    spell2.set_movement(SinewaveMovement(WIDTH // 2, 80, 0.8))
    
    # ========== 非符3：密集追踪 ==========
    nonspell3 = SpellCard(name="「Temporal Hunter」", hp=150, time_limit=30)
    nonspell3.add_pattern(HeavyHomingPattern(
        boss, bullets_per_wave=5, max_lifetime=4.0, cooldown=0.8,
        speed=140, turn_speed=120, attack=10
    ))
    nonspell3.add_pattern(CirclePattern(boss, bullet_count=8, interval=1.5, speed=100))
    nonspell3.set_movement(WaypointMovement([
        pygame.Vector2(100, 80),
        pygame.Vector2(WIDTH // 2, 120),
        pygame.Vector2(WIDTH - 100, 80),
    ], speed=80, loop=True))
    
    # ========== 符卡3：时空裂隙 - 多点同时发射弹幕帘 ==========
    spell3 = SpellCard(name="时符「时空裂隙」", hp=200, time_limit=50)
    spell3.add_pattern(SpatialRiftPattern(
        boss,
        rift_count=3,           # 3个裂隙点
        bullets_per_rift=12,
        interval=0.6,
        speed=130
    ))
    spell3.set_movement(StayMovement())
    
    # ========== 终符：时间悖论 - 混合所有时间技能 ==========
    final_spell = SpellCard(name="终符「时间悖论」", hp=250, time_limit=60)
    final_spell.add_pattern(TimeStopPattern(boss, freeze_duration=1.0, bullets_during_freeze=30, release_speed=100))
    final_spell.add_pattern(SpiralPattern(boss, arms=4, fire_rate=0.08, rotation_speed=60, speed=90))
    final_spell.add_pattern(AimedPattern(boss, bullet_count=3, spread=20, interval=2.0, speed=160))
    final_spell.set_movement(WaypointMovement([
        pygame.Vector2(80, 80),
        pygame.Vector2(WIDTH - 80, 80),
        pygame.Vector2(WIDTH // 2, 150),
    ], speed=60, loop=True))
    
    boss.add_spellcard(nonspell1)
    boss.add_spellcard(spell1)
    #boss.add_spellcard(nonspell2)
    boss.add_spellcard(spell2)
    boss.add_spellcard(nonspell3)
    boss.add_spellcard(spell3)
    boss.add_spellcard(final_spell)
    
    return boss