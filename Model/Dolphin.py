from .Player import Player
from .Abilities import SpeedBoostAbility

class Dolphin(Player):
    """Dolphin hero that can swim fast temporarily."""
    
    def __init__(self):
        super().__init__("Dolphin", speed=7, health=100, damage = 40)  # Faster base speed, more health
        self._ability = SpeedBoostAbility(self)
    
    def setAbility(self):
        return SpeedBoostAbility(self)
    
    def to_dict(self):
        """Convert Dolphin to a dictionary for serialization, including abilities."""
        data = super().to_dict()  # Get base player data
        data["class"] = self.__class__.__name__  # Store class type
        return data

    
    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Dolphin player from a dictionary, ensuring abilities are restored."""
        dolphin = cls()
        
        # Restore base player attributes
        dolphin._myPositionX = data["positionX"]
        dolphin._myPositionY = data["positionY"]
        dolphin._direction = data["direction"]
        dolphin._myHealth = data["health"]
        dolphin._ability = dolphin.setAbility()  # Restore first ability
        
        return dolphin

