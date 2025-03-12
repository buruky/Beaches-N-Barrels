
import pygame


class SpriteSheet:
    def __init__(self, theName:str, theMapOfSprites:dict):
        self.__myName = theName
        self.__myStateToImages = theMapOfSprites
    
    def __getName(self):
        return self.__myName
    
    def __getMap(self):
        return  self.__myStateToImages.copy()
    
    def addToMap(self, theState:str,theIndex:int ,theImage:pygame.image):
        if theState in self.__myStateToImages.keys():
            self.__myStateToImages[theState] [theIndex] = theImage

        else:
            raise Exception("SpriteAnimator.SpriteSheet.addToMap: NO STATE FOUND IN SPRITESHEET'S MAP\n",
                            "SpriteSheetName: ", self.__myName,"\n",
                            "SpriteSheetStates: ", self.__myStateToImages.keys(),"\n",
                            "State passed: ", theState)