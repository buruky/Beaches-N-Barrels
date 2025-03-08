from .Player import Player
from .Abilities import InvincibilityAbility

class Buddha(Player):
    """Buddha hero that can become temporarily invincible."""
    
    def __init__(self):
        super().__init__("Buddha", speed=4, health=200)  # Slower but tankier
        self._ability = InvincibilityAbility(self)
