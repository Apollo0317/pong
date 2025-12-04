import pygame
from pong.input import CommandType, command


class InputHandler_Keyboard:
    def __init__(self):
        pass

    @staticmethod
    def translate_input(keys, events: list[pygame.event.Event]) -> list[command]:
        """
        Translates raw input into a stream of commands.
        """
        commands = []

        # Movement commands
        direction = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w]
        )
        if direction.length_squared() > 0:
            direction = direction.normalize()
            commands.append(command(CommandType.MOVE, direction))

        # Fire commands
        if keys[pygame.K_j]:
            commands.append(command(CommandType.FIRE, "Y"))
        if keys[pygame.K_k]:
            commands.append(command(CommandType.FIRE, "normal"))
        if keys[pygame.K_l]:
            commands.append(command(CommandType.FIRE, "trace"))

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    commands.append(command(CommandType.PAUSE))
                if event.key == pygame.K_SPACE:
                    commands.append(command(CommandType.ENTER))
                if event.key == pygame.K_q:
                    commands.append(command(CommandType.QUIT))

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(60)

    pygame.quit()
