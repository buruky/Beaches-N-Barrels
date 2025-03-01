from typing import Final

import pygame

class ViewUnits:
    SCREEN_HEIGHT:Final = 600
    SCREEN_WIDTH:Final = 800

    DEFAULT_HEIGHT:Final = 50
    DEFAULT_WIDTH:Final = 50
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
    DEFAULT_SPRITE_DIM = (50,50)