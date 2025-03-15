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
        """Reconstruct DungeonCharacterList from a dictionary while ensuring correct subclass restoration."""
        from .Enemy import Enemy
        from .Pirate import Pirate
        from .BeachBall import BeachBall
        from .Seagull import Seagull
        from .Crab import Crab  # Import all subclasses

        character_list = cls()  # Create an empty list

        for char_data in data["characters"]:
            if char_data["name"] == "Pirate":
                character = Pirate.from_dict(char_data)  # Correctly load Pirate
            elif char_data["name"] == "BeachBall":
                character = BeachBall.from_dict(char_data)  # Correctly load BeachBall
            elif char_data["name"] == "Crab":
                character = Crab.from_dict(char_data)  #  Correctly load Crab
            elif char_data["name"] == "Seagull":
                character = Seagull.from_dict(char_data)  # Correctly load Seagull
            else:
                character = Enemy.from_dict(char_data)  # Default to generic enemy

            character_list.add_entity(character)  # Restore character

        return character_list
