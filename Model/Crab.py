from .Enemy import Enemy
import pygame

class Crab(Enemy):
    """A fast but weak enemy that moves side to side."""
    
    def __init__(self, attackDamage: int, healthPoints: int, positionX: int, positionY: int, speed: int):
        super().__init__("Crab", attackDamage, healthPoints, speed, positionX, positionY)
        self._direction = "LEFT"  # Default movement direction

    def moveCharacter(self):
        """Crabs move only LEFT or RIGHT, switching direction when hitting a wall."""
        new_x = self._myPositionX

        # Move in the current direction
        if self._direction == "LEFT":
            new_x -= self._mySpeed
        elif self._direction == "RIGHT":
            new_x += self._mySpeed

        # Check if the crab is hitting a wall
        if new_x <= 0 or new_x >= self.SCREEN_WIDTH - 50:
            self._toggle_direction()  # Flip direction only when hitting a wall
        else:
            # If no wall collision, apply movement normally
            self._check_collision_and_update_position(new_x, self._myPositionY, self)

    def _toggle_direction(self):
        """Switches the Crab's movement direction when hitting a wall."""
        self._direction = "RIGHT" if self._direction == "LEFT" else "LEFT"

    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Crab enemy from a dictionary, restoring its movement state."""
        crab = cls(
            data["damage"],
            data["health"],
            data["positionX"],
            data["positionY"],
            data["speed"]
        )

        # Restore game world reference
        from .GameWorld import GameWorld
        crab._game_world = GameWorld.getInstance()

        # ✅ Restore movement state correctly
        crab._direction = data["direction"]
        crab._move_timer = pygame.time.get_ticks()  # Reset movement timer

        return crab

