
import os
from typing import Final
import pygame

from ViewUnits import ViewUnits 


class SpriteSheet:
    pygame.init()
    MAX_NUMBER_OF_STATES:Final = 10
    def __init__(self, name:str):
        
        self.__myName = name
        self.__myStates = [""] * SpriteSheet.MAX_NUMBER_OF_STATES
        self.__mySpriteLists = [[None] for _ in range(SpriteSheet.MAX_NUMBER_OF_STATES)]
        self.load()

    def getSpriteMap(self):
        spritemap = dict()
        for i in range(SpriteSheet.MAX_NUMBER_OF_STATES):
            spritemap[self.__myStates[i]] = self.__mySpriteLists[i]
        return spritemap
    
    def getName(self):
        return self.__myName
    def addState(self)
    
    def load(self):
        """reads asset folder and represent"""
        # Specify the directory path
        directory_path = os.path.join(os.path.dirname(__file__), '..', 'Assets')

        # List all the files in the directory and save them as a list of strings
        file_names = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        # Optionally, if you want to join them into a single string
        file_names_str = ', '.join(file_names)
        alreadyMade = set()
        for pictureName in file_names:
            
            if pictureName in alreadyMade:
                 
        print(file_names_str)

    def defaultScalingImage(theName:str, theWidth:int = ViewUnits.DEFAULT_WIDTH, theHeight:int = ViewUnits.DEFAULT_HEIGHT) -> pygame.image:
        
        