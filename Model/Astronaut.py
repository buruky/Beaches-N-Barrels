from .Player import Player
from .Abilities import LowGravityAbility
import pygame

class Astronaut(Player):
    """Astronaut hero that can jump with low gravity effect."""
    
    def __init__(self):
        super().__init__("Astronaut", speed=5, health=175, damage = 50)  # Balanced stats
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
        
        if data.get("ability_active"):
            # Simulate restoring start time by assuming the ability started before saving
            elapsed_time = pygame.time.get_ticks() - (data.get("start_time", pygame.time.get_ticks()))
            
            if elapsed_time < Astronaut._ability.duration:
                Astronaut._ability.active = True
                Astronaut._ability.start_time = pygame.time.get_ticks() - elapsed_time  # ✅ Restore exact start time
            else:
                Astronaut._ability.deactivate()  # ✅ Expired, so deactivate immediately

        Astronaut._ability.update()
        return Astronaut
