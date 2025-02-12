import pygame
import random
from .MModel import MModel
from Model import *
from View import *

COLOR_CHANGE_EVENT = pygame.USEREVENT + 3
class MController:
    
    def __init__(self, view):
        self.myModel = MModel()
        self.myCharacterList = self.myModel.myDungeonCharacterList.get_entities()
        self.player = PlayerMock()
        self.myView = view
        self.myKeyMap = {
            pygame.K_w: "UP",
            pygame.K_s: "DOWN",
            pygame.K_a: "LEFT",
            pygame.K_d: "RIGHT"
        }
        self.myIsHoldingClick = False
        self.sign = 1#direction?
        self.myRandomX = random.randint(0, 500)
        self.myRandomY = random.randint(0, 500)
        pygame.time.set_timer(COLOR_CHANGE_EVENT, 500)  # Fire event every 500ms (30 ticks @ 60 FPS)
        
    def ControllerTick(self):
        quit = self.handleEvents()
        self.__handle_keyboard()
        self.__handle_mouse(self.sign)
        self.myModel.update()
        return quit
    
    def handleEvents(self):
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                return False
            if event.type == COLOR_CHANGE_EVENT:
                self.myView.myPlayerSprite.changeColor()#help
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 or event.button == 3:  # press left or right click
                    self.myIsHoldingClick = True
                    if event.button == 1: 
                        self.sign = 1
                    else:
                        self.sign = -1
                
            elif event.type == pygame.MOUSEBUTTONUP:  # release left or right click
                if event.button == 1 or event.button == 3:
                    self.myRandomX = random.randint(0, 500)
                    self.myRandomY = random.randint(0, 500)
                    self.myIsHoldingClick = False
            
            

            elif event.type == EventManager.PLAYER_MOVED:
                entity = event.dict["PlayerMock"]
                sprite = entity.getSprite()
                self.myView.update_entity(id(entity), sprite, entity.getPositionX(), entity.getPositionY())
                print("hi the player has updated bozo")##################################
            elif event.type == EventManager.ENEMY_MOVED:
                entity = event.dict["entity"]
                sprite = entity.getSprite()
                self.myView.update_entity(id(entity), sprite, entity.getPositionX(), entity.getPositionY())
    def __handle_keyboard(self):
        """Handles keyboard input for moving the player rectangle."""
        keys = pygame.key.get_pressed()
        directions = []

        for key, direction in self.myKeyMap.items():
            if keys[key]:
                directions.append(direction)

        #updates both model and view
        
        #MModel adds player as first index to character list
        self.player.moveCharacter(directions)#help
        
    def __handle_mouse(self, sign):
        if self.myIsHoldingClick:
            if sign > 0:
                self.player.teleportCharacter(self.myRandomX, self.myRandomY)
                self.myView.myPlayerSprite.updatePosition(self.myRandomX, self.myRandomY)
            else:
                self.player.teleportCharacter(0,0)
                self.myView.myPlayerSprite.updatePosition(0,0)

    
    