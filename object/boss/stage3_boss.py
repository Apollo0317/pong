import pygame
from pong.object.boss import *
from pong.config.config import *


def create_stage3_boss() -> Boss:
    """创建第三关 Boss - 混沌之主"""
    
    boss = Boss(
        fig_path='assets/fig/boss_3.png',
        pos=pygame.Vector2(WIDTH // 2, -50),
        hitbox_size=(72, 72)
    )
    
    # ========== 非符1：混沌涌动 ==========
    nonspell1 = SpellCard(name="「Chaos Surge」", hp=150, time_limit=30)
    nonspell1.add_pattern(RandomSprayPattern(boss, bullets_per_shot=12, interval=0.25, speed_range=(80, 180)))
    nonspell1.set_movement(EnterMovement(pygame.Vector2(WIDTH // 2, 100), speed=100))
    
    # ========== 符卡1：引力场 - 子弹被某点吸引后散开 ==========
    spell1 = SpellCard(name="重符「引力崩塌」", hp=180, time_limit=45)
    spell1.add_pattern(GravityWellPattern(
        boss,
        well_x=WIDTH // 2,
        well_y=HEIGHT // 2,
        bullet_count=24,
        interval=0.8,
        attraction_strength=200,
        escape_speed=150
    ))
    spell1.set_movement(SinewaveMovement(WIDTH // 2, 100, 0.6))
    
    # ========== 非符2：分裂弹 ==========
    nonspell2 = SpellCard(name="「Splitting Chaos」", hp=160, time_limit=35)
    nonspell2.add_pattern(SplitBulletPattern(
        boss,
        initial_count=8,
        split_count=4,
        split_delay=0.8,
        interval=1.2,
        initial_speed=100,
        split_speed=80
    ))
    nonspell2.set_movement(WaypointMovement([
        pygame.Vector2(150, 100),
        pygame.Vector2(WIDTH - 150, 100),
    ], speed=90, loop=True))
    
    # ========== 符卡2：镜像弹幕 - 屏幕两侧对称发射 ==========
    spell2 = SpellCard(name="幻符「镜像迷宫」", hp=100, time_limit=50)
    spell2.add_pattern(MirrorPattern(
        boss,
        bullet_count=10,
        spread=60,
        interval=0.7,
        speed=140
    ))
    spell2.add_pattern(CirclePattern(boss, bullet_count=16, interval=1.8, speed=90))
    spell2.set_movement(StayMovement())
    
    # ========== 非符3：随机传送攻击 ==========
    nonspell3 = SpellCard(name="「Teleport Strike」", hp=180, time_limit=35)
    nonspell3.add_pattern(TeleportBurstPattern(
        boss,
        burst_count=20,
        teleport_interval=2.0,
        burst_duration=0.3,
        speed_range=(100, 200)
    ))
    nonspell3.set_movement(TeleportMovement(
        positions=[
            pygame.Vector2(100, 80),
            pygame.Vector2(WIDTH - 100, 80),
            pygame.Vector2(WIDTH // 2, 120),
            pygame.Vector2(150, 150),
            pygame.Vector2(WIDTH - 150, 150),
        ],
        teleport_interval=2.0
    ))
    
    # ========== 符卡3：混沌漩涡 - 多个旋转中心 ==========
    spell3 = SpellCard(name="混符「混沌漩涡」", hp=220, time_limit=55)
    spell3.add_pattern(MultiVortexPattern(
        boss,
        vortex_count=3,
        bullets_per_vortex=6,
        fire_rate=0.1,
        rotation_speed=80,
        speed=100
    ))
    spell3.set_movement(SinewaveMovement(WIDTH // 2, 60, 1.2))
    
    # ========== 符卡x：时空裂隙 - 多点同时发射弹幕帘 ==========
    spellx = SpellCard(name="终符「时空裂隙」", hp=200, time_limit=50)
    spellx.add_pattern(SpatialRiftPattern(
        boss,
        rift_count=3,           # 3个裂隙点
        bullets_per_rift=12,
        interval=0.6,
        speed=130
    ))
    spellx.set_movement(StayMovement())

    # ========== 终符：混沌终焉 ==========
    final_spell = SpellCard(name="终符「混沌终焉」", hp=300, time_limit=70)
    final_spell.add_pattern(SplitBulletPattern(boss, initial_count=6, split_count=3, split_delay=0.6, interval=1.5, initial_speed=80, split_speed=100))
    final_spell.add_pattern(SpiralPattern(boss, arms=5, fire_rate=0.1, rotation_speed=50, speed=80))
    final_spell.add_pattern(AimedPattern(boss, bullet_count=5, spread=15, interval=1.8, speed=150))
    final_spell.add_pattern(RandomSprayPattern(boss, bullets_per_shot=5, interval=0.5, speed_range=(60, 120)))
    final_spell.set_movement(WaypointMovement([
        pygame.Vector2(80, 80),
        pygame.Vector2(WIDTH - 80, 120),
        pygame.Vector2(WIDTH // 2, 80),
        pygame.Vector2(80, 120),
        pygame.Vector2(WIDTH - 80, 80),
    ], speed=50, loop=True))
    
    boss.add_spellcard(nonspell1)
    boss.add_spellcard(spell1)
    boss.add_spellcard(nonspell2)
    boss.add_spellcard(spell2)
    boss.add_spellcard(nonspell3)
    # boss.add_spellcard(spell3)
    boss.add_spellcard(spellx)
    boss.add_spellcard(final_spell)

    
    return boss