from .Player import Player
from .Abilities import InvincibilityAbility
import pygame
from .EventManager import EventManager
from CustomEvents import CustomEvents

class Buddha(Player):
    """Buddha hero that can become temporarily invincible."""
    
    def __init__(self):
        super().__init__("Buddha", speed=4, health=150, damage = 50)  # Slower but tankier
        self._canDie = True
        self._ability = InvincibilityAbility(self)
        self.update("HEALTH")
    def takeDamage(self, damage: int):
        if self._canDie: 
            self._myHealth -= damage
            self.update("HEALTH")
            if self._myHealth <= 0:
                self.Dies()
    def setAbility(self):
        self.update("HEALTH")
        self._ability = InvincibilityAbility(self)

        return self._ability
        



    def to_dict(self):
        """Convert Buddha to a dictionary for serialization, including ability state."""
        data = super().to_dict()  # Get base player data
        data["class"] = self.__class__.__name__  # Store class type

        # ✅ Save ability active state & elapsed time
        data["ability_active"] = self._ability.active
        if self._ability.active:
            data["elapsed_time"] = pygame.time.get_ticks() - self._ability.start_time  # ✅ Save elapsed time

        return data


    
    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Buddha player from a dictionary, ensuring abilities are restored correctly."""
        Buddha = cls()
        
        # Restore base player attributes
        Buddha._myPositionX = data["positionX"]
        Buddha._myPositionY = data["positionY"]
        Buddha._direction = data["direction"]
        Buddha._myHealth = data["health"]

        # ✅ Restore ability properly
        Buddha._ability = Buddha.setAbility()  

        # ✅ Fix: Instead of force-activating, check if the ability should still be active
        if data.get("ability_active"):
            # Simulate restoring start time by assuming the ability started before saving
            elapsed_time = pygame.time.get_ticks() - (data.get("start_time", pygame.time.get_ticks()))
            
            if elapsed_time < Buddha._ability.duration:
                Buddha._ability.active = True
                Buddha._ability.start_time = pygame.time.get_ticks() - elapsed_time  # ✅ Restore exact start time
            else:
                Buddha._ability.deactivate()  # ✅ Expired, so deactivate immediately

        Buddha._ability.update()
        return Buddha
