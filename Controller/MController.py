from typing import Final
import pygame
import random
from .MModel import MModel
from Model import *
from View import *

COLOR_CHANGE_EVENT = pygame.USEREVENT + 3
class MController:
    
    def __init__(self):
        self.__myModel:Final = MModel()
        self.__myPlayer:Final = PlayerMock()
        self.__myView:Final = MView()
        self.__myIsHoldingClick = False
        self.__mySign = 1#direction?
        self.__myRandomX = random.randint(0, 500)
        self.__myRandomY = random.randint(0, 500)
        self.__myKeyMap:Final = {
            pygame.K_w: "UP",
            pygame.K_s: "DOWN",
            pygame.K_a: "LEFT",
            pygame.K_d: "RIGHT"
        }
        pygame.time.set_timer(COLOR_CHANGE_EVENT, 500)  # Fire event every 500ms (30 ticks @ 60 FPS)
        
    def ControllerTick(self):
        quit = self.__handleEvents()
        self.__handle_keyboard()
        self.__handle_mouse(self.__mySign)
        self.__myModel.update()
        return quit
    
    def __handleEvents(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return False
            # if event.type == COLOR_CHANGE_EVENT:
            #     self.myView.myPlayerSprite.changeColor()#help
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:  # press left or right click
                    self.__myIsHoldingClick = True
                    if event.button == 1: 
                        self.__mySign = 1
                    else:
                        self.__mySign = -1
                
            elif event.type == pygame.MOUSEBUTTONUP:  # release left or right click
                if event.button == 1 or event.button == 3:
                    self.__myRandomX = random.randint(0, 500)
                    self.__myRandomY = random.randint(0, 500)
                    self.__myIsHoldingClick = False
            
            elif event.type == EventManager.PLAYER_MOVED:
                entity = event.dict["PlayerMock"]
                sprite = entity.getSprite()
                self.__myView.update_entity(id(entity), sprite, entity.getPositionX(), entity.getPositionY())

            elif event.type == EventManager.ENEMY_MOVED:
                entity = event.dict["EnemyMock"]
                sprite = entity.getSprite()
                self.__myView.update_entity(id(entity), sprite, entity.getPositionX(), entity.getPositionY())
    def __handle_keyboard(self):
        """Handles keyboard input for moving the player rectangle."""
        keys = pygame.key.get_pressed()
        directions = []
        for key, direction in self.__myKeyMap.items():
            if keys[key]:
                directions.append(direction)
        #Player is handled differntly than other characters due to only one taking input
        self.__myPlayer.moveCharacter(directions)#help
        
    def __handle_mouse(self, theSign: int):
        if self.__myIsHoldingClick:
            if theSign > 0:
                self.__myPlayer.teleportCharacter(self.__myRandomX, self.__myRandomY)
            else:
                self.__myPlayer.teleportCharacter(0,0)

    
    