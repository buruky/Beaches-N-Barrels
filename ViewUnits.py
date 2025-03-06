from typing import Final

import pygame

class ViewUnits:
    pygame.init()

    # Get the screen resolution
    info = pygame.display.Info()
    SCREEN_WIDTH = info.current_w
    SCREEN_HEIGHT = info.current_h

    # Define the window size as a percentage of the screen
    SCREEN_WIDTH = int(SCREEN_WIDTH * 0.75)   # 75% of screen width
    SCREEN_HEIGHT = int(SCREEN_HEIGHT * 0.85) # 85% of screen height
    DEFAULT_WIDTH = 75
    DEFAULT_HEIGHT = 75

    DEFAULT_POSITION_X:Final = 0
    DEFAULT_POSITION_Y:Final = 0
    DEFAULT_RECT:Final = pygame.Rect((DEFAULT_POSITION_X,
                                      DEFAULT_POSITION_Y),
                                      (DEFAULT_WIDTH,
                                       DEFAULT_HEIGHT ))
    DEFAULT_STATE_NAME = "IDLE"
    DEFAULT_DICT:Final = {DEFAULT_STATE_NAME: []}
    PLAYER_SPRITE_NAME = "PlayerMock"
    ENEMY_SPRITE_NAME = "EnemyMock"
    DEFAULT_SPRITE_DIM = (DEFAULT_WIDTH,DEFAULT_HEIGHT)

    SOUTH_DOOR_CORD =  (SCREEN_WIDTH // 2 - DEFAULT_WIDTH // 2, 0)  # Centered at the top
    WEST_DOOR_CORD = (SCREEN_WIDTH - DEFAULT_WIDTH, SCREEN_HEIGHT // 2 - DEFAULT_HEIGHT // 2)  # Right side
    NORTH_DOOR_CORD = (SCREEN_WIDTH // 2 - DEFAULT_WIDTH // 2, SCREEN_HEIGHT - DEFAULT_HEIGHT)  # Bottom
    EAST_DOOR_CORD =  (0, SCREEN_HEIGHT // 2 - DEFAULT_HEIGHT // 2)  # Left side