from typing import Final
import pygame
import random
from .MModel import MModel
from Model.Dolphin import Dolphin
from Model import *
from View import *
from CustomEvents import CustomEvents
from View.TitleScreen import TitleScreen

class MController:
    
    def __init__(self):
        
        
        self.__myView:Final = MView()
        self.__InitalizeEvents()

        self.__myIsRunning = True
         # Show title screen before starting the game
        title_screen = TitleScreen(self.__myView.screen)
        title_screen.run()  # Display title screen before game starts
        self.__myWorld = GameWorld.getInstance()
        # self.__myModel:Final = MModel() 
        self.__myPlayer:Final = Dolphin()
        self.__myWorld.setPlayer(self.__myPlayer)
        
        self.__myIsHoldingClick = False
        self.__mySign = 1 
        self.__myKeyMap:Final = {
            pygame.K_w: "UP",
            pygame.K_s: "DOWN",
            pygame.K_a: "LEFT",
            pygame.K_d: "RIGHT"
        }
        #pygame.time.set_timer(COLOR_CHANGE_EVENT, 500)  # Fire event every 500ms (30 ticks @ 60 FPS)
        


    def ControllerTick(self):

        self.__handleEvents()
        self.__handle_keyboard()
        self.__handle_mouse(self.__mySign)
        self.__myWorld.tick()
        
        if self.__myPlayer._ability:
            self.__myPlayer._ability.update()
        
        return self.__myIsRunning
    
    def __InitalizeEvents(self):
        """Intializes all events with name and method to call when event is dispatched"""

        """Events that pygame posts for us"""
        EventManager.RegisterExistingEvent(CustomEvents.QUIT,pygame.QUIT, self.__quitGame)
        EventManager.RegisterExistingEvent(CustomEvents.MOUSE_BUTTON_DOWN,pygame.MOUSEBUTTONDOWN, self.__mouseButtonDown)
        EventManager.RegisterExistingEvent(CustomEvents.MOUSE_BUTTON_UP,pygame.MOUSEBUTTONUP, self.__mouseButtonUp)

        """Events that are posted manually"""
        EventManager.registerEvent(CustomEvents.CHARACTER_MOVED, self.__myView.update_entity)
        EventManager.registerEvent(CustomEvents.CHARACTER_STOPPED, self.__myView.update_entity)
        EventManager.registerEvent(CustomEvents.PLAYER_DIED, self.__handle_character_death)
        EventManager.registerEvent(CustomEvents.CHANGED_ROOM, self.__myView.updateRoom)


    def __handle_character_death(self, event):
        """Displays 'Game Over' on the screen when the player dies."""
        self.__myView.display_game_over()
        self.__myIsRunning = False  # Stop the game loop

    def __quitGame(self, event) -> bool:
        self.__myIsRunning = False  # Properly stop the game loop
        return self.__myIsRunning
    
    
    def __handleEvents(self):
        for event in pygame.event.get():
            EventManager.dispatch_event(event) 
            
    def __handle_keyboard(self):
        """Handles keyboard input for moving the player rectangle."""
        keys = pygame.key.get_pressed()
        directions = []
        if keys[pygame.K_e]:  # Press 'E' to activate ability
            print("Player Used Ability")
            self.__myPlayer.activate_ability()
            
        for key, direction in self.__myKeyMap.items():
            if keys[key]:
                directions.append(direction)
        #Player is handled differntly than other characters due to only one taking input
        if len(directions) > 0:
            self.__myPlayer.moveCharacter(directions)#help

    def __mouseButtonUp(self, theEvent):
        if theEvent.button == 1 or theEvent.button == 3:
            self.__myIsHoldingClick = False

    def __mouseButtonDown(self, theEvent):
        if theEvent.button == 1 or theEvent.button == 3:  # press left or right click
            self.__myIsHoldingClick = True
            if theEvent.button == 1: 
                self.__mySign = 1
            else:
                self.__mySign = -1

    def __handle_mouse(self, theSign: int):
        # if self.__myIsHoldingClick:
        #     if theSign > 0:
            #     # event = pygame.event.Event(
            #     #     EventManager.event_types[CustomEvents.CHANGED_ROOM],
            #     #     {
            #     #         "roomName": "s ",
            #     #         "direction": None
            #     #     }
            #     # )
            #     # pygame.event.post(event)
            #     # randX = random.randint(0, 500)
            #     # randY = random.randint(0, 500)
            #     # self.__myPlayer.teleportCharacter(randX, randY)
            # else:
            #     self.__myWorld.go()
        pass
    
    