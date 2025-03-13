import os
import re
import pygame

from .SpriteSheet import SpriteSheet
from ViewUnits import ViewUnits


from collections import defaultdict


class SpriteSheetFactory:
    def  __init__(self):
        self.x = 0
        
    def getAllAssets(self,P) -> list:
        '''returns list of spriteSheets for all assets in assets folder'''

        allSpriteSheets = defaultdict(SpriteSheet) #name: spriteSheet

        allImageInfo = self.__getAllImageInfo()#hols all image data from Assets [name: state, index, fullFileName]

        for name, info in allImageInfo.items():#iterates through all of the data
            
            
            
            if len(info) < 3:
                state = "IDLE" 
                index = 0
                fileName = info[1]
            else:
                state = info[0]
                index = info[1]
                fileName = info[2]
                
            image = self.getImageFromFolder(fileName) #passes full file name

            
            if name not in allSpriteSheets.keys():          # if finds unique name makes new spritesheet

                newMap = ViewUnits.DEFAULT_DICT.copy()
            #           [State]     [list index]
                
                newMap[state.upper()] = [None] * 10
                newMap[state.upper()][int(index)] = image


                allSpriteSheets[name] = SpriteSheet(name, newMap)
            else:                                            #if found already creates spriteSheet

                theAddingSpriteSheet = allSpriteSheets[name]

                theAddingSpriteSheet.addToMap(state, index, image)
        
        return allSpriteSheets

    def __getAllImageInfo(self)-> dict:
        """gets all image names from Assets Folder
        """
        """reads asset folder and represent"""
        
        # Specify the directory path
        directory_path = os.path.join(os.path.dirname(__file__), '..', 'Assets')
        # List all the files in the directory and save them as a list of strings
        file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        # Optionally, if you want to join them into a single string
        file_names_str = ', '.join(file_names)
        #spiderman-IDLE-1
        nameToInfo = dict()
        for fileName in file_names:
            #gets rid of .png or .jpg and splits at dashes
            fileContents = fileName.split(".")[0].split("-")
            
            fileContents.append(fileName)
            nameToInfo[fileContents[0]] = fileContents[1::]
        return nameToInfo
    
    def getImageFromFolder(self, theFileName:str) -> pygame.image:
        current_directory = os.path.dirname(__file__)
        path = os.path.join(current_directory, '..', 'Assets', theFileName)
        image = pygame.image.load(path)
        return image


