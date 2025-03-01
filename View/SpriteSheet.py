from typing import Final
import pygame
import random

from ViewUnits import ViewUnits

class SpriteSheet:
    """Holds all sprites for charcter and holds which is currently showing for animation """
    
    
    def __init__(self,theId:int, theName:str,
                 theSprites:dict = ViewUnits.DEFAULT_DICT,
                 theRect:pygame.Rect = ViewUnits.DEFAULT_RECT,):
        
        self.__myId = theId
        self.__myName = theName
        self.__mySprites = theSprites
        self.__myCurrentSpriteIndex = 0
        self.__myCurrentState = "IDLE"
        self.__myRect = theRect

    
    
    def getRect(self):
        return self.__myRect
    
    def getAllImages(self) -> list:
        """gets all images in map and returns as unsorted list"""
        spriteList = []
        for key in self.__mySprites.keys():
            for sprite in self.__mySprites[key]:
                spriteList.append(sprite)
        return spriteList
    
    def getActionImages(self, theAction:str) -> list:
        if theAction in self.__mySprites.keys():
            return self.__mySprites[theAction]
        raise Exception("SpriteSheet.getActionImages():",
                        "THERE IS NO LIST UNDER THAT STATE!!!") 

    def getImageMap(self) -> dict:
        return self.__mySprites
    

    def setPosition(self, theNewX: int, theNewY: int) -> None:
        self.__myRect.x = theNewX
        self.__myRect.y = theNewY
    

    def cycleSpriteSheet(self, theIncrement:int) -> None:
        listOfImages = self.__mySprites[self.__myCurrentState]
        numberOfImages = len(listOfImages)
        if numberOfImages == 0:
            raise Exception("SpriteSheet.cycleSpriteSheet(): NO SPRITES TO CYCLE!!!")
        
        #Doesnt't do anything if list has 1

        elif numberOfImages > 1:
            self.__myCurrentSpriteIndex = self.__myCurrentSpriteIndex + theIncrement % numberOfImages
        
    def setCurrentState(self, theState:str) -> None:
        if theState in self.__mySprites.keys():
            self.setCurrentState = theState
            self.__myCurrentSpriteIndex = 0
        else:
            raise Exception("SpriteSheet.setCurrentState(): THERE IS NO LIST UNDER THAT STATE!!!")
    

    def getId(self):
        return self.__myId
    
    def getCurrentSprite(self):
        # print(self.__myCurrentState)
        # print(self.__myCurrentSpriteIndex)
        return self.__mySprites[self.__myCurrentState][self.__myCurrentSpriteIndex]
    
    def getName(self):
        return self.__myName
        