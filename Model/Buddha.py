from .Player import Player
from .Abilities import InvincibilityAbility

class Buddha(Player):
    """Buddha hero that can become temporarily invincible."""
    
    def __init__(self):
        super().__init__("Buddha", speed=4, health=151, damage = 50)  # Slower but tankier
        self._canDie = True
        self._ability = InvincibilityAbility(self)
        self.update("HEALTH")


    def takeDamage(self, damage: int):
        if self._canDie: 
            self._myHealth -= damage
            self.update("HEALTH")
            if self._myHealth <= 0:
                self.Dies()