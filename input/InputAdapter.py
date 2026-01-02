import pygame
from pong.input import CommandType, command


class InputHandler_Keyboard:
    def __init__(self):
        self.prev_keys = {}  # 记录上一帧按键状态

    def translate_input(self, keys, events: list[pygame.event.Event]) -> list[command]:
        """
        Translates raw input into a stream of commands.
        """
        commands = []

        # Movement commands (持续检测，用于游戏内移动)
        direction = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w]
        )
        if direction.length_squared() > 0:
            direction = direction.normalize()
            if keys[pygame.K_m]:
                direction *= 0.5  # Slow movement
            commands.append(command(CommandType.MOVE, direction))

        # Fire commands
        if keys[pygame.K_k]:
            commands.append(command(CommandType.FIRE, "normal"))
        if keys[pygame.K_l]:
            commands.append(command(CommandType.FIRE, "trace"))
        if keys[pygame.K_j]:
            commands.append(command(CommandType.FIRE, "Y"))

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    commands.append(command(CommandType.PAUSE))
                if event.key == pygame.K_SPACE:
                    commands.append(command(CommandType.ENTER))
                if event.key == pygame.K_q:
                    commands.append(command(CommandType.QUIT))
                # 菜单导航（单次触发）
                if event.key == pygame.K_w:
                    commands.append(command(CommandType.MENU_UP))
                if event.key == pygame.K_s:
                    commands.append(command(CommandType.MENU_DOWN))

        return commands


if __name__ == "__main__":
    # Example usage
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    input_handler = InputHandler_Keyboard()

    running = True
    while running:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        commands = input_handler.translate_input(keys, events)
        for cmd in commands:
            print(cmd)

        for event in events:
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

    pygame.quit()