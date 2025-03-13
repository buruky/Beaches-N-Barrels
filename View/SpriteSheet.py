
import pygame


class SpriteSheet:
    def __init__(self, theName:str, theMapOfSprites:dict):
        self.__myName = theName
        self.__myStateToImages = theMapOfSprites
    
    def getName(self):
        return self.__myName
    
    def getMap(self):
        return  self.__myStateToImages.copy()
    
    def addToMap(self, theState:str,theIndex:int ,theImage:pygame.image):
        if theState in self.__myStateToImages.keys():
            self.__myStateToImages[theState] [theIndex] = theImage

        else:
            raise Exception("SpriteAnimator.SpriteSheet.addToMap: NO STATE FOUND IN SPRITESHEET'S MAP\n",
                            "SpriteSheetName: ", self.__myName,"\n",
                            "SpriteSheetStates: ", self.__myStateToImages.keys(),"\n",
                            "State passed: ", theState)
    def getCurrentSprite(self,theWantedState:str, theWantedIndex:int):
        # print(self.__myCurrentState)
        # print(self.__myCurrentSpriteIndex)
        return self.__myStateToImages[theWantedState][theWantedIndex]