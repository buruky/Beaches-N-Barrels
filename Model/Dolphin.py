from .Player import Player
from .Abilities import SpeedBoostAbility

class Dolphin(Player):
    """Dolphin hero that can swim fast temporarily."""
    
    def __init__(self):
        super().__init__("Dolphin", speed=7, health=120)  # Faster base speed, more health
        self._ability = SpeedBoostAbility(self)