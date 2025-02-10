from .DungeonCharacter import DungeonCharacter
from typing import Final

class DungeonCharacterList:
    def __init__(self):
        self.__myDungeonCharacterList = []  # Store all game objects
        
    def add_entity(self, theDungeonCharacter):
        """Add an entity to the game."""
        if isinstance(theDungeonCharacter, DungeonCharacter):
            self.__myDungeonCharacterList.append(theDungeonCharacter)

    def update_all(self):
        """Update all entities each frame."""
        for character in self.__myDungeonCharacterList:
            character.update()

    def get_entities(self):
        """Return a list of all entities."""
        return self.__myDungeonCharacterList