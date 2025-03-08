from .Player import Player
from .Abilities import LowGravityAbility

class Astronaut(Player):
    """Astronaut hero that can jump with low gravity effect."""
    
    def __init__(self):
        super().__init__("Astronaut", speed=5, health=150)  # Balanced stats
        self._ability = LowGravityAbility(self)
