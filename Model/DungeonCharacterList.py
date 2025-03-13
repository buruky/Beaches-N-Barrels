from .DungeonCharacter import DungeonCharacter
from typing import Final

class DungeonCharacterList:
    def __init__(self):
        self.__myDungeonCharacterList = []  # Store all game objects
        
    def add_entity(self, theDungeonCharacter: DungeonCharacter) -> None:
        """Add an entity to the game."""
        
        self.__myDungeonCharacterList.append(theDungeonCharacter)

    def update_all(self) -> None:
        """Update all entities each frame."""
        for character in self.__myDungeonCharacterList:
            #pass 
            character.update()

    def deleteAllEnemy(self):
        self.__myDungeonCharacterList.clear()
        self.update_all()
    
    def deleteEnemy(self,enemy):
        self.__myDungeonCharacterList.remove(enemy)
        self.update_all()
        
    def get_entities(self):
        """Return a list of all entities."""
        return self.__myDungeonCharacterList
    def to_dict(self):
        """Convert DungeonCharacterList to a dictionary for serialization."""
        return {
            "characters": [character.to_dict() for character in self.__myDungeonCharacterList]
        }
    @classmethod
    def from_dict(cls, data):
        """Reconstruct DungeonCharacterList from a dictionary."""
        from .DungeonCharacter import DungeonCharacter
        
        character_list = cls()  # Create an empty list
        for char_data in data["characters"]:
            character_list.add_entity(DungeonCharacter.from_dict(char_data))  # Restore characters

        return character_list
