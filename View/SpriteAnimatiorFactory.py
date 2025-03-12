#singleton
from collections import defaultdict
import os

import pygame
from .SpriteAnimator import SpriteAnimator
from ViewUnits import ViewUnits

class SpriteAnimatorFactory:
    def __init__(self):
        
        self.__myListOfSpriteSheets = self.__SpriteSheetFactory.getAllAssets()#dictionary name: spriteSheet

    def createSpriteAnimator(self, theName:str, theId: str, thePositionCords:list[int]) -> SpriteAnimator:
        self.createDefaultCharacter()
        #might implement different methods
    def createDefaultCharacter(self, theName:str, theId: str, thePositionCords:list[int]) -> SpriteAnimator:

        for currentName, currentSpriteSheet in self.__myListOfSpriteSheets.items():
            if theName == currentName:
                return SpriteAnimator(theName, theId, thePositionCords, currentSpriteSheet)
        raise Exception("SpriteAnimatorFactory.createDefaultCharacter: NO CHARACTER WITH SPRITESHEET WITH THAT NAME\n",
                        "Name Passed: ",theName,"\n"
                        "Names in List: ", self.__myListOfSpriteSheets.keys())
    


    class __SpriteSheetFactory:
        def  __init__(self):
            pass
        def getAllAssets(self) -> list:
            '''returns list of spriteSheets for all assets in assets folder'''

            allSpriteSheets = defaultdict(list) #name: spriteSheet

            allImageInfo = self.__getAllImageInfo()#hols all image data from Assets [name: state, index, fullFileName]

            for name, info in allImageInfo.items():#iterates through all of the data

                image = self.getImageFromFolder(info[2]) #passes full file name

                if name not in allSpriteSheets.keys():          # if finds unique name makes new spritesheet
                                

                    newMap = ViewUnits.DEFAULT_DICT.copy()
                    #       [State]         [list index]
                    newMap[info[0].upper()][int(info[1])] = image


                    allSpriteSheets.append(self.SpriteSheet(name, newMap))
                else:                                            #if found already creates spriteSheet

                    theAddingSpriteSheet = allSpriteSheets[name]

                    theAddingSpriteSheet.addToMap(info[0], info[1], image)
            
            return allSpriteSheets

        def __getAllImageInfo(self)-> dict:
            """gets all image names from Assets Folder
            [
                [name: state, index/number, fullfileName]
                ...
            ]
            
            """
        def getImageFromFolder(self, theFileName:str) -> pygame.image:
            current_directory = os.path.dirname(__file__)
            path = os.path.join(current_directory, '..', 'Assets', theFileName)
            image = pygame.image.load(path)
            return image

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