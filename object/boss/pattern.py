import pygame
import math, random
from abc import ABC, abstractmethod
from pong.object.bullet import Bullet
from pong.instance import get_sm
from pong.config.config import *


class BulletPattern(ABC):
    """弹幕模式基类"""
    
    def __init__(self, owner):
        self.owner = owner
        self.timer = 0
        self.finished = False
    
    @abstractmethod
    def update(self, dt: float):
        """更新弹幕，生成子弹直接注册到场景"""
        pass
    
    def reset(self):
        self.timer = 0
        self.finished = False
    
    def _register_bullet(self, bullet):
        """将子弹注册到场景"""
        scene = get_sm().get_scene
        if scene:
            scene.enemy_bullets.append(bullet)


class CirclePattern(BulletPattern):
    """圆形弹幕 - 向四周均匀发射"""
    
    def __init__(self, owner, bullet_count=16, interval=0.8, waves=999, speed=150):
        super().__init__(owner)
        self.bullet_count = bullet_count
        self.interval = interval
        self.waves = waves
        self.speed = speed
        self.current_wave = 0
        self.last_fire = -999  # 确保第一次能立即发射
    
    def update(self, dt: float):
        self.timer += dt
        
        if self.current_wave >= self.waves:
            self.finished = True
            return
        
        if self.timer - self.last_fire >= self.interval:
            self._spawn_circle()
            self.last_fire = self.timer
            self.current_wave += 1
    
    def _spawn_circle(self):
        angle_step = 360 / self.bullet_count
        
        for i in range(self.bullet_count):
            angle = math.radians(i * angle_step)
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            
            bullet = Bullet(
                fig_path='assets/fig/bullet.png',
                x=self.owner.pos.x,
                y=self.owner.pos.y,
                attack=5,
                speed=direction * self.speed,
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.current_wave = 0
        self.last_fire = -999


class SpiralPattern(BulletPattern):
    """螺旋弹幕 - 旋转发射"""
    
    def __init__(self, owner, arms=3, fire_rate=0.05, rotation_speed=90, duration=999, speed=120):
        super().__init__(owner)
        self.arms = arms
        self.fire_rate = fire_rate
        self.rotation_speed = rotation_speed
        self.duration = duration
        self.speed = speed
        self.angle = 0
        self.last_fire = -999
    
    def update(self, dt: float):
        self.timer += dt
        self.angle += self.rotation_speed * dt
        
        if self.timer >= self.duration:
            self.finished = True
            return
        
        if self.timer - self.last_fire >= self.fire_rate:
            self._spawn_spiral()
            self.last_fire = self.timer
    
    def _spawn_spiral(self):
        angle_step = 360 / self.arms
        
        for i in range(self.arms):
            angle = math.radians(self.angle + i * angle_step)
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            
            bullet = Bullet(
                fig_path='assets/fig/bullet.png',
                x=self.owner.pos.x,
                y=self.owner.pos.y,
                attack=3,
                speed=direction * self.speed,
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.angle = 0
        self.last_fire = -999


class AimedPattern(BulletPattern):
    """自机狙 - 朝向玩家发射"""
    
    def __init__(self, owner, bullet_count=5, spread=15, interval=1.0, waves=999, speed=180):
        super().__init__(owner)
        self.bullet_count = bullet_count
        self.spread = spread  # 散布角度
        self.interval = interval
        self.waves = waves
        self.speed = speed
        self.current_wave = 0
        self.last_fire = -999
    
    def update(self, dt: float):
        self.timer += dt
        
        if self.current_wave >= self.waves:
            self.finished = True
            return
        
        if self.timer - self.last_fire >= self.interval:
            self._spawn_aimed()
            self.last_fire = self.timer
            self.current_wave += 1
    
    def _spawn_aimed(self):
        # 获取玩家位置
        scene = get_sm().get_scene
        if not scene or not scene.players:
            return
        
        player = scene.players[0]
        to_player = player.pos - self.owner.pos
        
        if to_player.length() == 0:
            return
        
        base_angle = math.degrees(math.atan2(to_player.y, to_player.x))
        
        # 散布发射
        if self.bullet_count == 1:
            angles = [base_angle]
        else:
            start_angle = base_angle - self.spread * (self.bullet_count - 1) / 2
            angles = [start_angle + i * self.spread for i in range(self.bullet_count)]
        
        for angle in angles:
            rad = math.radians(angle)
            direction = pygame.Vector2(math.cos(rad), math.sin(rad))
            
            bullet = Bullet(
                fig_path='assets/fig/bullet_blue.png',
                x=self.owner.pos.x,
                y=self.owner.pos.y,
                attack=4,
                speed=direction * self.speed,
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.current_wave = 0
        self.last_fire = -999


class RandomSprayPattern(BulletPattern):
    """随机散射弹幕"""
    
    def __init__(self, owner, bullets_per_shot=8, interval=0.3, speed_range=(100, 200)):
        super().__init__(owner)
        self.bullets_per_shot = bullets_per_shot
        self.interval = interval
        self.speed_range = speed_range
        self.last_fire = -999
    
    def update(self, dt: float):
        import random
        self.timer += dt
        
        if self.timer - self.last_fire >= self.interval:
            for _ in range(self.bullets_per_shot):
                angle = random.uniform(0, 360)
                speed = random.uniform(*self.speed_range)
                rad = math.radians(angle)
                direction = pygame.Vector2(math.cos(rad), math.sin(rad))
                
                bullet = Bullet(
                    fig_path='assets/fig/bullet_green.png',
                    x=self.owner.pos.x,
                    y=self.owner.pos.y,
                    attack=3,
                    speed=direction * speed,
                    hitbox_size=BULLET_BOX_SIZE
                )
                self._register_bullet(bullet)
            
            self.last_fire = self.timer
    
    def reset(self):
        super().reset()
        self.last_fire = -999


class WavePattern(BulletPattern):
    """波浪弹幕 - 正弦波形发射"""
    
    def __init__(self, owner, bullet_count=15, interval=0.1, amplitude=50, frequency=3, speed=120):
        super().__init__(owner)
        self.bullet_count = bullet_count
        self.interval = interval
        self.amplitude = amplitude  # 波浪振幅
        self.frequency = frequency  # 波浪频率
        self.speed = speed
        self.current_bullet = 0
        self.last_fire = -999
        self.wave_offset = 0
    
    def update(self, dt: float):
        self.timer += dt
        self.wave_offset += dt * 2  # 波浪随时间移动
        
        if self.current_bullet >= self.bullet_count:
            self.finished = True
            return
        
        if self.timer - self.last_fire >= self.interval:
            self._spawn_wave_bullet()
            self.last_fire = self.timer
            self.current_bullet += 1
    
    def _spawn_wave_bullet(self):
        # X 方向从左到右
        progress = self.current_bullet / self.bullet_count
        x = progress * WIDTH
        
        # Y 方向带正弦偏移
        base_y = self.owner.pos.y
        offset = math.sin(progress * math.pi * self.frequency + self.wave_offset) * self.amplitude
        
        bullet = Bullet(
            fig_path='assets/fig/bullet.png',
            x=x,
            y=base_y + offset,
            attack=4,
            speed=pygame.Vector2(0, self.speed),
            hitbox_size=BULLET_BOX_SIZE
        )
        self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.current_bullet = 0
        self.last_fire = -999


class RingExpandPattern(BulletPattern):
    """扩散环弹幕 - 多层同心圆向外扩散"""
    
    def __init__(self, owner, rings=5, bullets_per_ring=16, ring_interval=0.3, speed=100, speed_increment=20):
        super().__init__(owner)
        self.rings = rings
        self.bullets_per_ring = bullets_per_ring
        self.ring_interval = ring_interval
        self.base_speed = speed
        self.speed_increment = speed_increment  # 每环速度递增
        self.current_ring = 0
        self.last_fire = -999
    
    def update(self, dt: float):
        self.timer += dt
        
        if self.current_ring >= self.rings:
            self.finished = True
            return
        
        if self.timer - self.last_fire >= self.ring_interval:
            self._spawn_ring()
            self.last_fire = self.timer
            self.current_ring += 1
    
    def _spawn_ring(self):
        speed = self.base_speed + self.current_ring * self.speed_increment
        angle_offset = self.current_ring * 10  # 每环旋转一点角度
        
        for i in range(self.bullets_per_ring):
            angle = math.radians(i * 360 / self.bullets_per_ring + angle_offset)
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            
            bullet = Bullet(
                fig_path='assets/fig/bullet.png',
                x=self.owner.pos.x,
                y=self.owner.pos.y,
                attack=4,
                speed=direction * speed,
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.current_ring = 0
        self.last_fire = -999


class CrossPattern(BulletPattern):
    """十字弹幕 - 四个方向发射，逐渐旋转"""
    
    def __init__(self, owner, fire_rate=0.08, rotation_speed=30, bullets_per_arm=1, spread=0, speed=150):
        super().__init__(owner)
        self.fire_rate = fire_rate
        self.rotation_speed = rotation_speed
        self.bullets_per_arm = bullets_per_arm
        self.spread = spread  # 每条臂的散射角度
        self.speed = speed
        self.angle = 0
        self.last_fire = -999
    
    def update(self, dt: float):
        self.timer += dt
        self.angle += self.rotation_speed * dt
        
        if self.timer - self.last_fire >= self.fire_rate:
            self._spawn_cross()
            self.last_fire = self.timer
    
    def _spawn_cross(self):
        for arm in range(4):
            base_angle = self.angle + arm * 90
            
            for i in range(self.bullets_per_arm):
                if self.bullets_per_arm == 1:
                    angle = base_angle
                else:
                    offset = (i - (self.bullets_per_arm - 1) / 2) * self.spread
                    angle = base_angle + offset
                
                rad = math.radians(angle)
                direction = pygame.Vector2(math.cos(rad), math.sin(rad))
                
                bullet = Bullet(
                    fig_path='assets/fig/bullet.png',
                    x=self.owner.pos.x,
                    y=self.owner.pos.y,
                    attack=3,
                    speed=direction * self.speed,
                    hitbox_size=BULLET_BOX_SIZE
                )
                self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.angle = 0
        self.last_fire = -999


class LaserWarningPattern(BulletPattern):
    """激光预警弹幕 - 先显示警告线，然后发射密集子弹"""
    
    def __init__(self, owner, warning_time=1.0, laser_duration=0.5, laser_width=5, speed=400):
        super().__init__(owner)
        self.warning_time = warning_time
        self.laser_duration = laser_duration
        self.laser_width = laser_width
        self.speed = speed
        self.phase = 'warning'  # 'warning' -> 'firing' -> 'done'
        self.target_angle = 0
        self.fire_timer = 0
    
    def update(self, dt: float):
        self.timer += dt
        
        if self.phase == 'warning':
            # 计算朝向玩家的角度
            scene = get_sm().get_scene
            if scene and scene.players:
                player = scene.players[0]
                to_player = player.pos - self.owner.pos
                if to_player.length() > 0:
                    self.target_angle = math.degrees(math.atan2(to_player.y, to_player.x))
            
            if self.timer >= self.warning_time:
                self.phase = 'firing'
                self.fire_timer = 0
        
        elif self.phase == 'firing':
            self.fire_timer += dt
            self._spawn_laser_bullets()
            
            if self.fire_timer >= self.laser_duration:
                self.phase = 'done'
                self.finished = True
    
    def _spawn_laser_bullets(self):
        # 密集发射
        for i in range(self.laser_width):
            offset = (i - (self.laser_width - 1) / 2) * 3
            angle = math.radians(self.target_angle + offset)
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            
            bullet = Bullet(
                fig_path='assets/fig/bullet.png',
                x=self.owner.pos.x,
                y=self.owner.pos.y,
                attack=8,
                speed=direction * self.speed,
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.phase = 'warning'
        self.fire_timer = 0


class BurstPattern(BulletPattern):
    """爆发弹幕 - 短时间内发射大量子弹，然后休息"""
    
    def __init__(self, owner, burst_count=30, burst_duration=0.5, rest_duration=2.0, speed_range=(80, 160)):
        super().__init__(owner)
        self.burst_count = burst_count
        self.burst_duration = burst_duration
        self.rest_duration = rest_duration
        self.speed_range = speed_range
        self.phase = 'burst'
        self.bullets_fired = 0
        self.phase_timer = 0
    
    def update(self, dt: float):
        self.timer += dt
        self.phase_timer += dt
        
        if self.phase == 'burst':
            bullets_to_fire = int(self.phase_timer / self.burst_duration * self.burst_count) - self.bullets_fired
            
            for _ in range(bullets_to_fire):
                self._spawn_burst_bullet()
                self.bullets_fired += 1
            
            if self.phase_timer >= self.burst_duration:
                self.phase = 'rest'
                self.phase_timer = 0
        
        elif self.phase == 'rest':
            if self.phase_timer >= self.rest_duration:
                self.phase = 'burst'
                self.phase_timer = 0
                self.bullets_fired = 0
    
    def _spawn_burst_bullet(self):
        angle = random.uniform(0, 360)
        speed = random.uniform(*self.speed_range)
        rad = math.radians(angle)
        direction = pygame.Vector2(math.cos(rad), math.sin(rad))
        
        bullet = Bullet(
            fig_path='assets/fig/bullet.png',
            x=self.owner.pos.x,
            y=self.owner.pos.y,
            attack=3,
            speed=direction * speed,
            hitbox_size=BULLET_BOX_SIZE
        )
        self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.phase = 'burst'
        self.bullets_fired = 0
        self.phase_timer = 0


class FlowerPattern(BulletPattern):
    """花瓣弹幕 - 类似花朵绽放的图案"""
    
    def __init__(self, owner, petals=6, bullets_per_petal=8, interval=0.8, speed=100, curl=30):
        super().__init__(owner)
        self.petals = petals
        self.bullets_per_petal = bullets_per_petal
        self.interval = interval
        self.speed = speed
        self.curl = curl  # 花瓣弯曲程度
        self.last_fire = -999
        self.rotation = 0
    
    def update(self, dt: float):
        self.timer += dt
        self.rotation += dt * 20
        
        if self.timer - self.last_fire >= self.interval:
            self._spawn_flower()
            self.last_fire = self.timer
    
    def _spawn_flower(self):
        for petal in range(self.petals):
            base_angle = petal * 360 / self.petals + self.rotation
            
            for i in range(self.bullets_per_petal):
                # 花瓣形状：角度随距离弯曲
                progress = i / self.bullets_per_petal
                curl_offset = math.sin(progress * math.pi) * self.curl
                angle = base_angle + curl_offset
                
                speed = self.speed * (0.5 + progress * 0.5)  # 速度递增
                
                rad = math.radians(angle)
                direction = pygame.Vector2(math.cos(rad), math.sin(rad))
                
                bullet = Bullet(
                    fig_path='assets/fig/bullet.png',
                    x=self.owner.pos.x,
                    y=self.owner.pos.y,
                    attack=3,
                    speed=direction * speed,
                    hitbox_size=BULLET_BOX_SIZE
                )
                self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.last_fire = -999
        self.rotation = 0


class StarPattern(BulletPattern):
    """星形弹幕 - 五角星形状"""
    
    def __init__(self, owner, points=5, inner_radius=50, outer_radius=150, interval=1.0, speed=100):
        super().__init__(owner)
        self.points = points
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.interval = interval
        self.speed = speed
        self.last_fire = -999
        self.rotation = 0
    
    def update(self, dt: float):
        self.timer += dt
        self.rotation += dt * 15
        
        if self.timer - self.last_fire >= self.interval:
            self._spawn_star()
            self.last_fire = self.timer
    
    def _spawn_star(self):
        # 生成星形路径上的点
        for i in range(self.points * 2):
            angle = i * 180 / self.points + self.rotation
            
            # 交替使用内外半径
            if i % 2 == 0:
                radius = self.outer_radius
            else:
                radius = self.inner_radius
            
            rad = math.radians(angle - 90)  # 从顶部开始
            start_x = self.owner.pos.x + math.cos(rad) * 10
            start_y = self.owner.pos.y + math.sin(rad) * 10
            
            direction = pygame.Vector2(math.cos(rad), math.sin(rad))
            
            bullet = Bullet(
                fig_path='assets/fig/bullet.png',
                x=start_x,
                y=start_y,
                attack=4,
                speed=direction * self.speed,
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.last_fire = -999
        self.rotation = 0


class CurtainPattern(BulletPattern):
    """弹幕帘 - 从上方落下的密集弹幕墙，保证有安全通道"""
    
    def __init__(self, owner, columns=20, rows=8, row_interval=0.4, speed=150, 
                 gap_width=4, gap_drift=2):
        """
        Args:
            columns: 列数
            rows: 行数
            row_interval: 行间隔时间
            speed: 子弹速度
            gap_width: 安全通道宽度（列数）
            gap_drift: 通道每行最大漂移量（使通道不完全垂直）
        """
        super().__init__(owner)
        self.columns = columns
        self.rows = rows
        self.row_interval = row_interval
        self.speed = speed
        self.gap_width = gap_width
        self.gap_drift = gap_drift
        self.current_row = 0
        self.last_fire = -999
        self.gap_center = 0  # 安全通道中心位置
    
    def update(self, dt: float):
        self.timer += dt
        
        if self.current_row >= self.rows:
            self.finished = True
            return
        
        if self.timer - self.last_fire >= self.row_interval:
            if self.current_row == 0:
                # 第一行：在玩家附近生成安全通道
                self._init_gap_near_player()
            else:
                # 后续行：通道轻微漂移，但保持连续
                self._drift_gap()
            
            self._spawn_curtain_row()
            self.last_fire = self.timer
            self.current_row += 1
    
    def _init_gap_near_player(self):
        """在玩家位置附近初始化安全通道"""
        scene = get_sm().get_scene
        if scene and scene.players:
            player = scene.players[0]
            # 将玩家 X 坐标转换为列索引
            col_width = WIDTH / self.columns
            player_col = int(player.pos.x / col_width)
            # 限制在有效范围内
            half_gap = self.gap_width // 2
            self.gap_center = max(half_gap, min(self.columns - half_gap - 1, player_col))
        else:
            self.gap_center = self.columns // 2
    
    def _drift_gap(self):
        """让安全通道轻微漂移"""
        if self.gap_drift > 0:
            drift = random.randint(-self.gap_drift, self.gap_drift)
            half_gap = self.gap_width // 2
            new_center = self.gap_center + drift
            # 确保通道不会超出边界
            self.gap_center = max(half_gap, min(self.columns - half_gap - 1, new_center))
    
    def _spawn_curtain_row(self):
        col_width = WIDTH / self.columns
        half_gap = self.gap_width // 2
        
        for col in range(self.columns):
            # 检查是否在安全通道内
            if abs(col - self.gap_center) <= half_gap:
                continue
            
            x = col * col_width + col_width / 2
            y = self.owner.pos.y
            
            bullet = Bullet(
                fig_path='assets/fig/bullet.png',
                x=x,
                y=y,
                attack=5,
                speed=pygame.Vector2(0, self.speed),
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.current_row = 0
        self.last_fire = -999
        self.gap_center = 0


class MultiGapCurtainPattern(BulletPattern):
    """多通道弹幕帘 - 多个安全通道，位置保证合理分布"""
    
    def __init__(self, owner, columns=24, rows=6, row_interval=0.35, speed=160,
                 gap_count=2, gap_width=3, min_gap_distance=6):
        """
        Args:
            gap_count: 安全通道数量
            gap_width: 每个通道宽度
            min_gap_distance: 通道之间最小距离
        """
        super().__init__(owner)
        self.columns = columns
        self.rows = rows
        self.row_interval = row_interval
        self.speed = speed
        self.gap_count = gap_count
        self.gap_width = gap_width
        self.min_gap_distance = min_gap_distance
        self.current_row = 0
        self.last_fire = -999
        self.gap_centers = []
    
    def update(self, dt: float):
        self.timer += dt
        
        if self.current_row >= self.rows:
            self.finished = True
            return
        
        if self.timer - self.last_fire >= self.row_interval:
            if self.current_row == 0:
                self._generate_valid_gaps()
            
            self._spawn_curtain_row()
            self.last_fire = self.timer
            self.current_row += 1
    
    def _generate_valid_gaps(self):
        """生成保证不重叠且分布合理的安全通道"""
        half_gap = self.gap_width // 2
        valid_range = range(half_gap, self.columns - half_gap)
        
        # 尝试生成合理的通道位置
        max_attempts = 100
        for _ in range(max_attempts):
            centers = sorted(random.sample(list(valid_range), self.gap_count))
            
            # 检查通道之间距离是否足够
            valid = True
            for i in range(1, len(centers)):
                if centers[i] - centers[i-1] < self.min_gap_distance:
                    valid = False
                    break
            
            if valid:
                self.gap_centers = centers
                return
        
        # 如果随机失败，使用均匀分布
        spacing = self.columns // (self.gap_count + 1)
        self.gap_centers = [spacing * (i + 1) for i in range(self.gap_count)]
    
    def _is_in_gap(self, col: int) -> bool:
        """检查列是否在任意安全通道内"""
        half_gap = self.gap_width // 2
        for center in self.gap_centers:
            if abs(col - center) <= half_gap:
                return True
        return False
    
    def _spawn_curtain_row(self):
        col_width = WIDTH / self.columns
        
        for col in range(self.columns):
            if self._is_in_gap(col):
                continue
            
            x = col * col_width + col_width / 2
            y = self.owner.pos.y
            
            bullet = Bullet(
                fig_path='assets/fig/bullet.png',
                x=x,
                y=y,
                attack=5,
                speed=pygame.Vector2(0, self.speed),
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.current_row = 0
        self.last_fire = -999
        self.gap_centers = []


class BoomerangPattern(BulletPattern):
    """回旋弹幕 - 子弹飞出后会减速并返回"""
    
    def __init__(self, owner, bullet_count=8, interval=1.5, max_distance=300, speed=200):
        super().__init__(owner)
        self.bullet_count = bullet_count
        self.interval = interval
        self.max_distance = max_distance
        self.speed = speed
        self.last_fire = -999
        self.boomerang_bullets = []  # 追踪回旋子弹
    
    def update(self, dt: float):
        self.timer += dt
        
        # 更新回旋子弹
        self._update_boomerangs(dt)
        
        if self.timer - self.last_fire >= self.interval:
            self._spawn_boomerang()
            self.last_fire = self.timer
    
    def _spawn_boomerang(self):
        for i in range(self.bullet_count):
            angle = i * 360 / self.bullet_count
            rad = math.radians(angle)
            direction = pygame.Vector2(math.cos(rad), math.sin(rad))
            
            bullet = Bullet(
                fig_path='assets/fig/bullet.png',
                x=self.owner.pos.x,
                y=self.owner.pos.y,
                attack=4,
                speed=direction * self.speed,
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
            
            # 记录回旋信息
            self.boomerang_bullets.append({
                'bullet': bullet,
                'start_pos': pygame.Vector2(self.owner.pos),
                'direction': direction,
                'phase': 'out',  # 'out' -> 'back'
                'traveled': 0
            })
    
    def _update_boomerangs(self, dt: float):
        for info in self.boomerang_bullets[:]:
            bullet = info['bullet']
            if not bullet.alive:
                self.boomerang_bullets.remove(info)
                continue
            
            if info['phase'] == 'out':
                info['traveled'] += self.speed * dt
                
                # 减速
                slow_factor = 1 - (info['traveled'] / self.max_distance)
                slow_factor = max(0.1, slow_factor)
                bullet.speed = info['direction'] * self.speed * slow_factor
                
                if info['traveled'] >= self.max_distance:
                    info['phase'] = 'back'
            
            elif info['phase'] == 'back':
                # 返回（朝向玩家）
                scene = get_sm().get_scene
                if scene and scene.players:
                    player = scene.players[0]
                    to_player = player.pos - bullet.pos
                    if to_player.length() > 0:
                        bullet.speed = to_player.normalize() * self.speed * 0.8
    
    def reset(self):
        super().reset()
        self.last_fire = -999
        self.boomerang_bullets = []

# ...existing code...

class HeavyHomingPattern(BulletPattern):

    """强力追踪弹 - 发射少量高伤害追踪弹，命中或超时后发射下一波"""
    
    def __init__(self, owner, bullets_per_wave=3, max_lifetime=3.0, cooldown=0.5, 
                 speed=120, turn_speed=150, attack=15):
        super().__init__(owner)
        self.bullets_per_wave = bullets_per_wave
        self.max_lifetime = max_lifetime  # 每波子弹最大存活时间
        self.cooldown = cooldown  # 波次间隔
        self.speed = speed
        self.turn_speed = turn_speed  # 转向速度（度/秒）
        self.attack = attack
        
        self.active_bullets = []  # 当前波次的追踪弹
        self.wave_timer = 0  # 当前波次计时
        self.cooldown_timer = 0  # 冷却计时
        self.phase = 'ready'  # 'ready' -> 'tracking' -> 'cooldown'
    
    def update(self, dt: float):
        self.timer += dt
        
        if self.phase == 'ready':
            self._spawn_wave()
            self.phase = 'tracking'
            self.wave_timer = 0
        
        elif self.phase == 'tracking':
            self.wave_timer += dt
            self._update_tracking(dt)
            
            # 检查是否所有子弹都消失了（命中或超时）
            self.active_bullets = [b for b in self.active_bullets if b['bullet'].alive]
            
            all_hit = len(self.active_bullets) == 0
            timeout = self.wave_timer >= self.max_lifetime
            
            if all_hit or timeout:
                # 超时的子弹强制消失
                if timeout:
                    for info in self.active_bullets:
                        info['bullet'].alive = False
                    self.active_bullets = []
                
                self.phase = 'cooldown'
                self.cooldown_timer = 0
        
        elif self.phase == 'cooldown':
            self.cooldown_timer += dt
            if self.cooldown_timer >= self.cooldown:
                self.phase = 'ready'
    
    def _spawn_wave(self):
        """发射一波追踪弹"""
        scene = get_sm().get_scene
        if not scene or not scene.players:
            return
        
        player = scene.players[0]
        to_player = player.pos - self.owner.pos
        
        if to_player.length() == 0:
            base_angle = 90  # 默认向下
        else:
            base_angle = math.degrees(math.atan2(to_player.y, to_player.x))
        
        # 散开发射
        spread = 30  # 初始散布角度
        for i in range(self.bullets_per_wave):
            if self.bullets_per_wave == 1:
                angle = base_angle
            else:
                offset = (i - (self.bullets_per_wave - 1) / 2) * spread
                angle = base_angle + offset
            
            rad = math.radians(angle)
            direction = pygame.Vector2(math.cos(rad), math.sin(rad))
            
            bullet = Bullet(
                fig_path='assets/fig/tracing_bullet.png',  # 用红色表示强力弹
                x=self.owner.pos.x,
                y=self.owner.pos.y,
                attack=self.attack,
                speed=direction * self.speed,
                hitbox_size=(BULLET_BOX_SIZE[0] * 1.5, BULLET_BOX_SIZE[1] * 1.5),
                target_group= 'player'
            )
            self._register_bullet(bullet)
            
            self.active_bullets.append({
                'bullet': bullet,
                'current_angle': angle
            })
    
    def _update_tracking(self, dt: float):
        """更新追踪弹的方向"""
        scene = get_sm().get_scene
        if not scene or not scene.players:
            return
        
        player = scene.players[0]
        
        for info in self.active_bullets:
            bullet = info['bullet']
            if not bullet.alive:
                continue
            
            # 计算朝向玩家的目标角度
            to_player = player.pos - bullet.pos
            if to_player.length() == 0:
                continue
            
            target_angle = math.degrees(math.atan2(to_player.y, to_player.x))
            current_angle = info['current_angle']
            
            # 计算角度差（处理环绕）
            angle_diff = target_angle - current_angle
            while angle_diff > 180:
                angle_diff -= 360
            while angle_diff < -180:
                angle_diff += 360
            
            # 限制转向速度
            max_turn = self.turn_speed * dt
            if abs(angle_diff) <= max_turn:
                new_angle = target_angle
            elif angle_diff > 0:
                new_angle = current_angle + max_turn
            else:
                new_angle = current_angle - max_turn
            
            info['current_angle'] = new_angle
            
            # 更新子弹速度方向
            rad = math.radians(new_angle)
            direction = pygame.Vector2(math.cos(rad), math.sin(rad))
            bullet.speed = direction * self.speed
    
    def reset(self):
        super().reset()
        # 清理残留子弹
        for info in self.active_bullets:
            info['bullet'].alive = False
        self.active_bullets = []
        self.wave_timer = 0
        self.cooldown_timer = 0
        self.phase = 'ready'

# ...existing code...

class TimeStopPattern(BulletPattern):
    """时间停止弹幕 - 子弹先冻结在空中，然后同时释放"""
    
    def __init__(self, owner, freeze_duration=1.5, bullets_during_freeze=30, release_speed=120):
        super().__init__(owner)
        self.freeze_duration = freeze_duration
        self.bullets_during_freeze = bullets_during_freeze
        self.release_speed = release_speed
        
        self.phase = 'spawn'  # 'spawn' -> 'freeze' -> 'release' -> 'cooldown'
        self.frozen_bullets = []
        self.spawn_timer = 0
        self.spawn_interval = freeze_duration / bullets_during_freeze
        self.freeze_timer = 0
        self.bullets_spawned = 0
    
    def update(self, dt: float):
        self.timer += dt
        
        if self.phase == 'spawn':
            self.spawn_timer += dt
            
            while self.spawn_timer >= self.spawn_interval and self.bullets_spawned < self.bullets_during_freeze:
                self._spawn_frozen_bullet()
                self.spawn_timer -= self.spawn_interval
                self.bullets_spawned += 1
            
            if self.bullets_spawned >= self.bullets_during_freeze:
                self.phase = 'freeze'
                self.freeze_timer = 0
        
        elif self.phase == 'freeze':
            self.freeze_timer += dt
            # 保持子弹静止
            for info in self.frozen_bullets:
                if info['bullet'].alive:
                    info['bullet'].speed = pygame.Vector2(0, 0)
            
            if self.freeze_timer >= 0.5:  # 短暂停顿后释放
                self.phase = 'release'
                self._release_all()
        
        elif self.phase == 'release':
            # 检查子弹是否都飞走了
            self.frozen_bullets = [b for b in self.frozen_bullets if b['bullet'].alive]
            if not self.frozen_bullets:
                self.phase = 'cooldown'
                self.freeze_timer = 0
        
        elif self.phase == 'cooldown':
            self.freeze_timer += dt
            if self.freeze_timer >= 0.5 :
                self.phase = 'spawn'
                self.spawn_timer = 0
                self.bullets_spawned = 0
    
    def _spawn_frozen_bullet(self):
        # 随机位置，但在boss周围
        angle = random.uniform(0, 360)
        distance = random.uniform(30, 100)
        rad = math.radians(angle)
        
        x = self.owner.pos.x + math.cos(rad) * distance
        y = self.owner.pos.y + math.sin(rad) * distance
        
        # 朝向玩家的方向
        scene = get_sm().get_scene
        if scene and scene.players:
            player = scene.players[0]
            direction = player.pos - pygame.Vector2(x, y)
            if direction.length() > 0:
                direction = direction.normalize()
            else:
                direction = pygame.Vector2(0, 1)
        else:
            direction = pygame.Vector2(0, 1)
        
        bullet = Bullet(
            fig_path='assets/fig/bullet_blue.png',
            x=x, y=y,
            attack=5,
            speed=pygame.Vector2(0, 0),  # 初始静止
            hitbox_size=BULLET_BOX_SIZE
        )
        self._register_bullet(bullet)
        
        self.frozen_bullets.append({
            'bullet': bullet,
            'direction': direction
        })
    
    def _release_all(self):
        """释放所有冻结的子弹"""
        for info in self.frozen_bullets:
            if info['bullet'].alive:
                info['bullet'].speed = info['direction'] * self.release_speed
    
    def reset(self):
        super().reset()
        for info in self.frozen_bullets:
            info['bullet'].alive = False
        self.frozen_bullets = []
        self.phase = 'spawn'
        self.spawn_timer = 0
        self.freeze_timer = 0
        self.bullets_spawned = 0


class TimeReversePattern(BulletPattern):
    """时间回溯弹幕 - 子弹飞出后沿原路返回"""
    
    def __init__(self, owner, bullet_count=16, travel_time=1.2, interval=1.5, speed=150):
        super().__init__(owner)
        self.bullet_count = bullet_count
        self.travel_time = travel_time
        self.interval = interval
        self.speed = speed
        self.last_fire = -999
        self.tracked_bullets = []
    
    def update(self, dt: float):
        self.timer += dt
        
        # 更新追踪的子弹
        self._update_tracked(dt)
        
        if self.timer - self.last_fire >= self.interval:
            self._spawn_wave()
            self.last_fire = self.timer
    
    def _spawn_wave(self):
        for i in range(self.bullet_count):
            angle = i * 360 / self.bullet_count
            rad = math.radians(angle)
            direction = pygame.Vector2(math.cos(rad), math.sin(rad))
            
            bullet = Bullet(
                fig_path='assets/fig/bullet.png',
                x=self.owner.pos.x,
                y=self.owner.pos.y,
                attack=4,
                speed=direction * self.speed,
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
            
            self.tracked_bullets.append({
                'bullet': bullet,
                'direction': direction,
                'timer': 0,
                'phase': 'out'  # 'out' -> 'pause' -> 'back'
            })
    
    def _update_tracked(self, dt: float):
        for info in self.tracked_bullets[:]:
            bullet = info['bullet']
            if not bullet.alive:
                self.tracked_bullets.remove(info)
                continue
            
            info['timer'] += dt
            
            if info['phase'] == 'out':
                if info['timer'] >= self.travel_time:
                    info['phase'] = 'pause'
                    info['timer'] = 0
                    bullet.speed = pygame.Vector2(0, 0)
            
            elif info['phase'] == 'pause':
                if info['timer'] >= 0.3:  # 短暂停顿
                    info['phase'] = 'back'
                    bullet.speed = -info['direction'] * self.speed * 1.2  # 返回时稍快
            
            elif info['phase'] == 'back':
                # 返回后自然消失（超出屏幕）
                pass
    
    def reset(self):
        super().reset()
        for info in self.tracked_bullets:
            info['bullet'].alive = False
        self.tracked_bullets = []
        self.last_fire = -999


class SpatialRiftPattern(BulletPattern):
    """空间裂隙弹幕 - 从多个随机点同时发射"""
    
    def __init__(self, owner, rift_count=3, bullets_per_rift=12, interval=0.8, speed=130):
        super().__init__(owner)
        self.rift_count = rift_count
        self.bullets_per_rift = bullets_per_rift
        self.interval = interval
        self.speed = speed
        self.last_fire = -999
        self.rift_positions = []
    
    def update(self, dt: float):
        self.timer += dt
        
        if self.timer - self.last_fire >= self.interval:
            self._update_rifts()
            self._spawn_from_rifts()
            self.last_fire = self.timer
    
    def _update_rifts(self):
        """更新裂隙位置"""
        self.rift_positions = []
        for _ in range(self.rift_count):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(30, 150)
            self.rift_positions.append(pygame.Vector2(x, y))
    
    def _spawn_from_rifts(self):
        for rift_pos in self.rift_positions:
            for i in range(self.bullets_per_rift):
                angle = i * 360 / self.bullets_per_rift + random.uniform(-10, 10)
                rad = math.radians(angle)
                direction = pygame.Vector2(math.cos(rad), math.sin(rad))
                
                bullet = Bullet(
                    fig_path='assets/fig/bullet.png',
                    x=rift_pos.x,
                    y=rift_pos.y,
                    attack=4,
                    speed=direction * self.speed,
                    hitbox_size=BULLET_BOX_SIZE
                )
                self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.last_fire = -999
        self.rift_positions = []


class GravityWellPattern(BulletPattern):
    """引力场弹幕 - 子弹被引力点吸引后再散开"""
    
    def __init__(self, owner, well_x, well_y, bullet_count=24, interval=1.0, 
                 attraction_strength=200, escape_speed=150):
        super().__init__(owner)
        self.well_pos = pygame.Vector2(well_x, well_y)
        self.bullet_count = bullet_count
        self.interval = interval
        self.attraction_strength = attraction_strength
        self.escape_speed = escape_speed
        self.last_fire = -999
        self.tracked_bullets = []
    
    def update(self, dt: float):
        self.timer += dt
        
        # 更新引力效果
        self._update_gravity(dt)
        
        if self.timer - self.last_fire >= self.interval:
            self._spawn_wave()
            self.last_fire = self.timer
    
    def _spawn_wave(self):
        for i in range(self.bullet_count):
            angle = i * 360 / self.bullet_count
            rad = math.radians(angle)
            direction = pygame.Vector2(math.cos(rad), math.sin(rad))
            
            bullet = Bullet(
                fig_path='assets/fig/bullet_green.png',
                x=self.owner.pos.x,
                y=self.owner.pos.y,
                attack=4,
                speed=direction * 80,  # 初始慢速
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
            
            self.tracked_bullets.append({
                'bullet': bullet,
                'phase': 'attract',  # 'attract' -> 'escape'
                'timer': 0
            })
    
    def _update_gravity(self, dt: float):
        for info in self.tracked_bullets[:]:
            bullet = info['bullet']
            if not bullet.alive:
                self.tracked_bullets.remove(info)
                continue
            
            info['timer'] += dt
            
            if info['phase'] == 'attract':
                # 向引力点加速
                to_well = self.well_pos - bullet.pos
                distance = to_well.length()
                
                if distance < 30:  # 到达引力点附近
                    info['phase'] = 'escape'
                    # 向玩家方向散开
                    scene = get_sm().get_scene
                    if scene and scene.players:
                        player = scene.players[0]
                        escape_dir = player.pos - bullet.pos
                        if escape_dir.length() > 0:
                            escape_dir = escape_dir.normalize()
                        else:
                            escape_dir = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                    else:
                        escape_dir = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                    
                    bullet.speed = escape_dir * self.escape_speed
                else:
                    # 施加引力
                    gravity_dir = to_well.normalize()
                    gravity_force = self.attraction_strength / max(distance, 50)
                    bullet.speed += gravity_dir * gravity_force * dt * 60
            
            # escape 阶段子弹自由飞行
    
    def reset(self):
        super().reset()
        for info in self.tracked_bullets:
            info['bullet'].alive = False
        self.tracked_bullets = []
        self.last_fire = -999


class SplitBulletPattern(BulletPattern):
    """分裂弹幕 - 子弹飞行一段时间后分裂"""
    
    def __init__(self, owner, initial_count=8, split_count=4, split_delay=0.8, 
                 interval=1.2, initial_speed=100, split_speed=80):
        super().__init__(owner)
        self.initial_count = initial_count
        self.split_count = split_count
        self.split_delay = split_delay
        self.interval = interval
        self.initial_speed = initial_speed
        self.split_speed = split_speed
        self.last_fire = -999
        self.tracked_bullets = []
    
    def update(self, dt: float):
        self.timer += dt
        
        # 检查分裂
        self._update_splits(dt)
        
        if self.timer - self.last_fire >= self.interval:
            self._spawn_wave()
            self.last_fire = self.timer
    
    def _spawn_wave(self):
        for i in range(self.initial_count):
            angle = i * 360 / self.initial_count
            rad = math.radians(angle)
            direction = pygame.Vector2(math.cos(rad), math.sin(rad))
            
            bullet = Bullet(
                fig_path='assets/fig/bullet.png',
                x=self.owner.pos.x,
                y=self.owner.pos.y,
                attack=5,
                speed=direction * self.initial_speed,
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet)
            
            self.tracked_bullets.append({
                'bullet': bullet,
                'timer': 0,
                'split': False,
                'base_angle': angle
            })
    
    def _update_splits(self, dt: float):
        for info in self.tracked_bullets[:]:
            bullet = info['bullet']
            if not bullet.alive or info['split']:
                if not bullet.alive:
                    self.tracked_bullets.remove(info)
                continue
            
            info['timer'] += dt
            
            if info['timer'] >= self.split_delay:
                info['split'] = True
                # 分裂
                split_pos = bullet.pos.copy()
                base_angle = info['base_angle']
                
                for j in range(self.split_count):
                    split_angle = base_angle + (j - (self.split_count - 1) / 2) * 30
                    rad = math.radians(split_angle)
                    direction = pygame.Vector2(math.cos(rad), math.sin(rad))
                    
                    split_bullet = Bullet(
                        fig_path='assets/fig/bullet_blue.png',
                        x=split_pos.x,
                        y=split_pos.y,
                        attack=3,
                        speed=direction * self.split_speed,
                        hitbox_size=BULLET_BOX_SIZE
                    )
                    self._register_bullet(split_bullet)
                
                # 原子弹消失
                bullet.alive = False
    
    def reset(self):
        super().reset()
        for info in self.tracked_bullets:
            info['bullet'].alive = False
        self.tracked_bullets = []
        self.last_fire = -999


class MirrorPattern(BulletPattern):
    """镜像弹幕 - 屏幕两侧对称发射"""
    
    def __init__(self, owner, bullet_count=10, spread=60, interval=0.7, speed=140):
        super().__init__(owner)
        self.bullet_count = bullet_count
        self.spread = spread
        self.interval = interval
        self.speed = speed
        self.last_fire = -999
    
    def update(self, dt: float):
        self.timer += dt
        
        if self.timer - self.last_fire >= self.interval:
            self._spawn_mirror()
            self.last_fire = self.timer
    
    def _spawn_mirror(self):
        # 左侧发射点
        left_pos = pygame.Vector2(50, random.randint(50, 150))
        # 右侧镜像
        right_pos = pygame.Vector2(WIDTH - 50, left_pos.y)
        
        for i in range(self.bullet_count):
            # 左侧向右下发射
            angle_left = 45 + (i / self.bullet_count - 0.5) * self.spread
            rad_left = math.radians(angle_left)
            dir_left = pygame.Vector2(math.cos(rad_left), math.sin(rad_left))
            
            bullet_left = Bullet(
                fig_path='assets/fig/bullet.png',
                x=left_pos.x, y=left_pos.y,
                attack=4,
                speed=dir_left * self.speed,
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet_left)
            
            # 右侧镜像（向左下）
            angle_right = 135 - (i / self.bullet_count - 0.5) * self.spread
            rad_right = math.radians(angle_right)
            dir_right = pygame.Vector2(math.cos(rad_right), math.sin(rad_right))
            
            bullet_right = Bullet(
                fig_path='assets/fig/bullet_blue.png',
                x=right_pos.x, y=right_pos.y,
                attack=4,
                speed=dir_right * self.speed,
                hitbox_size=BULLET_BOX_SIZE
            )
            self._register_bullet(bullet_right)
    
    def reset(self):
        super().reset()
        self.last_fire = -999


class TeleportBurstPattern(BulletPattern):
    """传送爆发弹幕 - 配合传送移动使用"""
    
    def __init__(self, owner, burst_count=20, teleport_interval=2.0, burst_duration=0.3, speed_range=(100, 200)):
        super().__init__(owner)
        self.burst_count = burst_count
        self.teleport_interval = teleport_interval
        self.burst_duration = burst_duration
        self.speed_range = speed_range
        self.phase_timer = 0
        self.bullets_fired = 0
    
    def update(self, dt: float):
        self.timer += dt
        self.phase_timer += dt
        
        # 在传送间隔的开始时爆发
        if self.phase_timer <= self.burst_duration:
            bullets_to_fire = int(self.phase_timer / self.burst_duration * self.burst_count) - self.bullets_fired
            for _ in range(bullets_to_fire):
                self._spawn_burst()
                self.bullets_fired += 1
        
        if self.phase_timer >= self.teleport_interval:
            self.phase_timer = 0
            self.bullets_fired = 0
    
    def _spawn_burst(self):
        angle = random.uniform(0, 360)
        speed = random.uniform(*self.speed_range)
        rad = math.radians(angle)
        direction = pygame.Vector2(math.cos(rad), math.sin(rad))
        
        bullet = Bullet(
            fig_path='assets/fig/bullet.png',
            x=self.owner.pos.x,
            y=self.owner.pos.y,
            attack=4,
            speed=direction * speed,
            hitbox_size=BULLET_BOX_SIZE
        )
        self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.phase_timer = 0
        self.bullets_fired = 0


class MultiVortexPattern(BulletPattern):
    """多漩涡弹幕 - 多个旋转发射点"""
    
    def __init__(self, owner, vortex_count=3, bullets_per_vortex=4, fire_rate=0.1, rotation_speed=80, speed=100):
        super().__init__(owner)
        self.vortex_count = vortex_count
        self.bullets_per_vortex = bullets_per_vortex
        self.fire_rate = fire_rate
        self.rotation_speed = rotation_speed
        self.speed = speed
        self.angle = 0
        self.last_fire = -999
        self.vortex_offsets = []
        
        # 初始化漩涡位置（围绕boss）
        for i in range(vortex_count):
            angle = i * 360 / vortex_count
            self.vortex_offsets.append(angle)
    
    def update(self, dt: float):
        self.timer += dt
        self.angle += self.rotation_speed * dt
        
        if self.timer - self.last_fire >= self.fire_rate:
            self._spawn_vortex_bullets()
            self.last_fire = self.timer
    
    def _spawn_vortex_bullets(self):
        vortex_distance = 60  # 漩涡中心距boss距离
        
        for i, offset in enumerate(self.vortex_offsets):
            # 漩涡位置绕boss旋转
            vortex_angle = self.angle + offset
            rad = math.radians(vortex_angle)
            vortex_x = self.owner.pos.x + math.cos(rad) * vortex_distance
            vortex_y = self.owner.pos.y + math.sin(rad) * vortex_distance
            
            # 从每个漩涡发射子弹
            for j in range(self.bullets_per_vortex):
                bullet_angle = self.angle * 2 + j * 360 / self.bullets_per_vortex + i * 30
                bullet_rad = math.radians(bullet_angle)
                direction = pygame.Vector2(math.cos(bullet_rad), math.sin(bullet_rad))
                
                bullet = Bullet(
                    fig_path='assets/fig/bullet.png',
                    x=vortex_x,
                    y=vortex_y,
                    attack=3,
                    speed=direction * self.speed,
                    hitbox_size=BULLET_BOX_SIZE
                )
                self._register_bullet(bullet)
    
    def reset(self):
        super().reset()
        self.angle = 0
        self.last_fire = -999
