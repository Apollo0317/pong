from pong.object.boss.pattern import BulletPattern
from pong.object.boss.movement import Movement, StayMovement


class SpellCard:
    """符卡 - 包含移动模式和弹幕模式"""
    
    def __init__(self, name: str, hp: int, time_limit: float = 60):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.time_limit = time_limit
        self.timer = 0
        self.patterns: list[BulletPattern] = []
        self.movement: Movement = StayMovement()
        self.finished = False
    
    def add_pattern(self, pattern: BulletPattern):
        self.patterns.append(pattern)
        return self  # 链式调用
    
    def set_movement(self, movement: Movement):
        self.movement = movement
        return self
    
    def update(self, dt: float, owner):
        self.timer += dt
        
        # 时间耗尽或血量归零
        if self.timer >= self.time_limit or self.hp <= 0:
            self.finished = True
            return
        
        # 更新移动
        if self.movement:
            self.movement.update(dt, owner)
        
        # 更新弹幕
        for pattern in self.patterns:
            if not pattern.finished:
                pattern.update(dt)
        
        # 所有弹幕结束后循环
        if all(p.finished for p in self.patterns):
            for p in self.patterns:
                p.reset()
    
    def reset(self):
        self.timer = 0
        self.hp = self.max_hp
        self.finished = False
        for p in self.patterns:
            p.reset()