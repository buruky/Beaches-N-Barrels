from typing import Final

import pygame

class ViewUnits:
    pygame.init()  # Initialize pygame to get display info


     # Get actual screen resolution
    info = pygame.display.Info()
    screen_w = info.current_w
    screen_h = info.current_h

    # Set screen dimensions close to 1000x1100 pixels but adapt to the actual resolution
    TARGET_WIDTH = 960  # Approximate target width
    TARGET_HEIGHT = 768  # Approximate target height

    FLOOR_SIDE_LENGTH:Final = 11
    # Ensure the screen size is proportionally close to the target without exceeding real screen
    SCREEN_WIDTH: Final = min(max(TARGET_WIDTH, screen_w // 2), screen_w)  # Adjusted within range
    SCREEN_HEIGHT: Final = min(max(TARGET_HEIGHT, screen_h // 2), screen_h)  # Adjusted within range

    # Define relative sizes as a percentage of the screen
    DEFAULT_HEIGHT: Final = SCREEN_HEIGHT // 10  # 10% of screen height
    DEFAULT_WIDTH: Final = SCREEN_WIDTH // 12  # 8.33% of screen width
    DEFAULT_POSITION_X:Final = 0
    DEFAULT_POSITION_Y:Final = 0
    DEFAULT_RECT:Final = pygame.Rect((DEFAULT_POSITION_X,
                                      DEFAULT_POSITION_Y),
                                      (DEFAULT_WIDTH,
                                       DEFAULT_HEIGHT ))
    DEFAULT_STATE_NAME = "IDLE"
    DEFAULT_DICT:Final = {DEFAULT_STATE_NAME: []}
    PLAYER_SPRITE_NAME:Final = "PlayerMock"
    ENEMY_SPRITE_NAME:Final = "EnemyMock"
    DEFAULT_SPRITE_DIM:Final = (DEFAULT_WIDTH,DEFAULT_HEIGHT)

    SOUTH_DOOR_CORD =  (SCREEN_WIDTH // 2 - DEFAULT_WIDTH // 2, 0)  # Centered at the top
    WEST_DOOR_CORD = (SCREEN_WIDTH - DEFAULT_WIDTH, SCREEN_HEIGHT // 2 - DEFAULT_HEIGHT // 2)  # Right side
    NORTH_DOOR_CORD = (SCREEN_WIDTH // 2 - DEFAULT_WIDTH // 2, SCREEN_HEIGHT - DEFAULT_HEIGHT)  # Bottom
    EAST_DOOR_CORD =  (0, SCREEN_HEIGHT // 2 - DEFAULT_HEIGHT // 2)  # Left side

    DIRECTION_UP:Final = "UP"
    DIRECTION_DOWN:Final = "DOWN"
    DIRECTION_LEFT:Final = "LEFT"
    DIRECTION_RIGHT:Final = "RIGHT"
