def check_bullet_hits(bullets: list, targets: list):
    """检测子弹与目标的碰撞，返回命中数"""
    hits = 0
    for bullet in bullets:
        if not bullet.alive:
            continue
        for target in targets:
            if not target.alive:
                continue
            if bullet.hitbox.colliderect(target.hitbox):
                target.take_damage(bullet.attack)
                bullet.alive = False
                hits += 1
                break
    return hits
