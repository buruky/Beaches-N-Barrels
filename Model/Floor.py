import random
from typing import Final
from .Room import Room 
from .EventManager import EventManager
from CustomEvents import CustomEvents
from .Door import Door
import pygame

class Floor:
    
    _ROOM_SIZE = 100
    _START_POS:Final = (5,5)
    def __init__(self, theGrid:list[list], theDoorList:list[Door]):
        self.__myGrid = theGrid
        self.__myDoorList = theDoorList
        self.__myStartCord = Floor._START_POS

    def get_dungeon(self) -> list[list]:
        return self.__myGrid  
    
    def getDoorList(self) -> list[Door]:
        return self.__myDoorList
    
    def getStartRoom(self):
        return self.__myGrid[self.__myStartCord[0]][self.__myStartCord[1]]
    
    def print_dungeon(self):
        for row in range(len(self.__myGrid)):
            line = ""
            for col in range(len(self.__myGrid[0])):
                if isinstance(self.__myGrid[row][col], Room):
                    line += str(self.__myGrid[row][col].getRoom())
                else:
                    line += ". "
            print(line)
        print()
   
