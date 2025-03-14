from .Player import Player
from .Abilities import LowGravityAbility

class Astronaut(Player):
    """Astronaut hero that can jump with low gravity effect."""
    
    def __init__(self):
        super().__init__("Astronaut", speed=5, health=125, damage = 75)  # Balanced stats
        self._ability = LowGravityAbility(self)
    
    def setAbility(self):
        return  LowGravityAbility(self)
        
    
    


    def to_dict(self):
        """Convert Astronaut to a dictionary for serialization, including abilities."""
        data = super().to_dict()  # Get base player data
        data["class"] = self.__class__.__name__  # Store class type
        return data

    
    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Astronaut player from a dictionary, ensuring abilities are restored."""
        Astronaut = cls()
        
        # Restore base player attributes
        Astronaut._myPositionX = data["positionX"]
        Astronaut._myPositionY = data["positionY"]
        Astronaut._direction = data["direction"]
        Astronaut._myHealth = data["health"]
        Astronaut._ability = Astronaut.setAbility()  # Restore first ability
        
        return Astronaut