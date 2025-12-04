from enum import Enum, auto


class CommandType(Enum):
    MOVE = auto()
    FIRE = auto()
    PAUSE = auto()
    ENTER = auto()
    QUIT = auto()


class command:
    def __init__(self, command_type: CommandType, value=None):
        """
        command is composed of type and associated value (Optional)
        """
        self.command_type = command_type
        self.value = value
        pass

    def __str__(self):
        return f"command(type={self.command_type}, value={self.value})"
