from typing import Final

import pygame

class ViewUnits:
    SCREEN_HEIGHT:Final = 1000
    SCREEN_WIDTH:Final = 1100

    DEFAULT_HEIGHT:Final = 75
    DEFAULT_WIDTH:Final = 75
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