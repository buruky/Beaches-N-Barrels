from .Player import Player
from .Abilities import SpeedBoostAbility
import pygame


class Dolphin(Player):
    """Dolphin hero that can swim fast temporarily."""
    
    def __init__(self):
        super().__init__("Dolphin", speed=7, health=100, damage = 100)  # Faster base speed, more health
        self._ability = SpeedBoostAbility(self)
    
    def setAbility(self):
        self._ability = SpeedBoostAbility(self)

        return self._ability
    
    def to_dict(self):
        """Convert Dolphin to a dictionary for serialization, including ability state."""
        data = super().to_dict()  # Get base player data
        data["class"] = self.__class__.__name__  # Store class type

        # ✅ Save ability active state & elapsed time
        data["ability_active"] = self._ability.active
        if self._ability.active:
            data["elapsed_time"] = pygame.time.get_ticks() - self._ability.start_time  # ✅ Save elapsed time

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
        if data.get("ability_active"):
            # Simulate restoring start time by assuming the ability started before saving
            elapsed_time = pygame.time.get_ticks() - (data.get("start_time", pygame.time.get_ticks()))
            
            if elapsed_time < dolphin._ability.duration:
                dolphin._ability.active = True
                dolphin._ability.start_time = pygame.time.get_ticks() - elapsed_time  # ✅ Restore exact start time
            else:
                dolphin._ability.deactivate()  # ✅ Expired, so deactivate immediately

        dolphin._ability.update()
        return dolphin
