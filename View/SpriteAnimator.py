

import pygame
from .SpriteSheet import SpriteSheet
from ViewUnits import ViewUnits

class SpriteAnimator:
    def __init__(self, theName:str, theId:str, thePositionCords:list[int], theSpriteSheet:SpriteSheet):
        self.__myName = theName
        self.__myId = theId
        self.__myRect = pygame.Rect( (thePositionCords[0],thePositionCords[1]), (ViewUnits.DEFAULT_WIDTH, ViewUnits.DEFAULT_HEIGHT) )

        self.__mySpriteSheet = theSpriteSheet

        self.__myCurrentSpriteIndex = 0

        self.__myCurrentState = ViewUnits.DEFAULT_STATE_NAME
    
    # def __init__(self, theName:str, theId:str, thePositionRect:pygame.Rect, theSpriteSheet):
    #     self.__myName = theName
    #     self.__myId = theId
    #     print("inSpriteANimator: ", thePositionRect)
    #     self.__myRect = pygame.Rect(thePositionRect)

    #     self.__mySpriteSheet = theSpriteSheet

    #     self.__myCurrentSpriteIndex = 0

    #     self.__myCurrentState = ViewUnits.DEFAULT_STATE_NAME

    
    def getAllImages(self) -> list:
        """gets all images in map and returns as unsorted list"""
        spriteList = []
        for key in self.__mySprites.keys():
            for sprite in self.__mySprites[key]:
                spriteList.append(sprite)
        return spriteList
    
    def getStateImages(self, theState:str) -> list:
        if theState in self.__mySprites.keys():
            return self.__mySprites[theState]
        raise Exception("SpriteSheet.getActionImages():",
                        "THERE IS NO LIST UNDER THAT STATE!!!") 

    
    

    def cycleSpriteSheet(self) -> None:
        listOfImages = self.__mySprites[self.__myCurrentState]
        numberOfImages = len(listOfImages)
        if numberOfImages == 0:
            raise Exception("SpriteSheet.cycleSpriteSheet(): NO SPRITES TO CYCLE!!!")
        
        #Doesnt't do anything if list has 1

        elif numberOfImages > 1:
            self.__myCurrentSpriteIndex = (self.__myCurrentSpriteIndex + 1) % numberOfImages
        
    def setCurrentState(self, theState:str) -> None:
        if theState in self.__mySprites.keys():
            self.setCurrentState = theState
            self.__myCurrentSpriteIndex = 0
        else:
            raise Exception("SpriteSheet.setCurrentState(): THERE IS NO LIST UNDER THAT STATE!!!")


    def setPosition(self, theNewX: int, theNewY: int) -> None:
        self.__myRect.x = theNewX
        self.__myRect.y = theNewY

    def getImageMap(self) -> SpriteSheet:
        return self.__mySpriteSheet
    
    def getRect(self):
        return self.__myRect
    
    def getId(self):
        return self.__myId
    
    def getCurrentSprite(self):
        # print(self.__myCurrentState)
        # print(self.__myCurrentSpriteIndex)
        return self.__mySpriteSheet.getCurrentSprite(self.__myCurrentState,self.__myCurrentSpriteIndex)
    
    def getName(self):
        return self.__myName
        