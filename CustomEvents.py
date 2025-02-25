from typing import Final


class CustomEvents:
    """Holds all custom event names """
    QUIT:Final = "QUIT"
    CHARACTER_MOVED:Final = "CHARACTER_MOVED"
    CHARACTER_STOPPED:Final = "CHARACTER_STOPPED"
    MOUSE_BUTTON_DOWN:Final = "MOUSE_BUTTON_DOWN"
    MOUSE_BUTTON_UP:Final = "MOUSE_BUTTON_DOWN"
    COLLISIONS:Final = "COLLISION"
    PLAYER_DIED:Final = "PLAYER_DIED"
    CHANGED_ROOM:Final = "CHANGED_ROOM"