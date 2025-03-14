import pygame
import math
from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
from ViewUnits import ViewUnits
from CustomEvents import CustomEvents

class Projectile(DungeonCharacter):
    def __init__(self, name: str, shooter, attackDamage: int, angle: float, speed: int, positionX: int, positionY: int):
        """Initialize projectile with attributes and ensure position variables are set."""
        
        # Since DungeonCharacter requires health points, we pass a placeholder value of 1 for the health.
        # Assuming projectiles are not intended to have health.
        super().__init__(attackDamage, 1, positionX, positionY, speed)  # Pass '1' for health points (not relevant for projectiles)
        
        # Now we define the attributes specific to the Projectile class
        self.damage = attackDamage
        self.shooter = shooter
        self.x = positionX
        self.y = positionY
        self.speed = speed
        self.angle = angle  # Store the angle for movement
        self._name = name

        from .GameWorld import GameWorld  # Prevent circular imports
        self._game_world = GameWorld.getInstance()

        # Create a rectangle for positioning and collision handling
        self.rect = pygame.Rect(self.x, self.y, 10, 10)  # Change width & height as needed

        # Immediately start moving the projectile
        self.is_active = True  # Track if the projectile should keep moving
        self.shoot()



    def shoot(self):
        """Moves the projectile continuously after being created."""
        if self.is_active:
            self.moveCharacter()

    def getAttackDamage(self):
        return self.damage
    
    def moveCharacter(self):
        """Move projectile based on its angle or direction."""
        new_x, new_y = self.x, self.y

        # Check if an angle is used (for diagonals or specific direction) or predefined directions
        if self.angle is not None:  # Using angle for movement
            new_x += self.speed * math.cos(self.angle)
            new_y += self.speed * math.sin(self.angle)
        else:
            # Predefined directions (UP, DOWN, LEFT, RIGHT)
            if self._direction == "UP":
                new_y -= self.speed  # Move up (decrease Y)
            elif self._direction == "DOWN":
                new_y += self.speed  # Move down (increase Y)
            elif self._direction == "LEFT":
                new_x -= self.speed  # Move left (decrease X)
            elif self._direction == "RIGHT":
                new_x += self.speed  # Move right (increase X)

        # Check for collisions in the game world
        if not self._game_world.check_projectile_collision(self):
            self.x = new_x
            self.y = new_y
            self.rect.topleft = (self.x, self.y)  # Update rect position
            self.update(CustomEvents.CHARACTER_MOVED)
        else:
            self.Dies()  # Remove projectile if it hits something
            self.update(CustomEvents.UPDATE_PROJECTILE)

    def update(self, theEventName: str):
        """Post an event when the projectile moves."""
        event = pygame.event.Event(
            EventManager.event_types[theEventName],
            {
                "name": self.getName(),
                "positionX": self.getPositionX(),
                "positionY": self.getPositionY(),
                "id": id(self)
            }
        )
        pygame.event.post(event)

    def Dies(self) -> None:
        """Handles when a projectile is removed from the game."""
        self.is_active = False  # Stop movement
        self._game_world.removeProjectile(self)

    def getPositionX(self) -> int:
        """Returns the X coordinate of the projectile."""
        return self.x

    def getPositionY(self) -> int:
        """Returns the Y coordinate of the projectile."""
        return self.y

    def getName(self):
        """Returns the projectile's name."""
        return self._name

    def toString(self) -> str:
        """Returns a string representation of the projectile."""
        return f"{self._name} at ({self.x}, {self.y})"

    def to_dict(self):
        """Convert player state to a dictionary for serialization."""
        return {
            "name": self._name,
            "speed": self._mySpeed,
            "direction": self._direction,
            "damage": self._myAttackDamage,
            "positionX": self._myPositionX,
            "positionY": self._myPositionY,
            # "inventory": [item.to_dict() for item in self.__inventory],  # Convert inventory items if needed
            # "ability_active": self._item_Ability.active if self._item_Ability else None
        }
    @classmethod
    def from_dict(cls, data):
        """Reconstruct a DungeonCharacter from a dictionary. Assumes subclass implementation."""
        return cls(
            data["damage"],
            data["health"],
            data["positionX"],
            data["positionY"],
            data["speed"]
        )
