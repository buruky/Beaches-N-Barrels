import pygame
from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
from ViewUnits import ViewUnits
from CustomEvents import CustomEvents

class Projectile(DungeonCharacter):
    def __init__(self, name: str, shooter, attackDamage: int, direction: str, speed: int, positionX: int, positionY: int):
        """Initialize projectile with attributes and ensure position variables are set."""
        super().__init__(attackDamage, direction, positionX, positionY, speed)  # Ensure DungeonCharacter handles these

        # If DungeonCharacter does not define these attributes, we explicitly declare them
        self.damage = attackDamage
        self.shooter = shooter
        self.x = positionX
        self.y = positionY
        self.speed = speed
        self._direction = direction
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
        """Move projectile based on its direction."""
        new_x, new_y = self.x, self.y

        if self._direction == "UP":
            new_y -= self.speed
        elif self._direction == "DOWN":
            new_y += self.speed
        elif self._direction == "LEFT":
            new_x -= self.speed
        elif self._direction == "RIGHT":
            new_x += self.speed

       
        if not self._game_world.check_projectile_collision(self):
            self.x = new_x
            self.y = new_y
            self.rect.topleft = (self.x, self.y)  # Update rect position
            self.update(CustomEvents.CHARACTER_MOVED)
        else:
            self.Dies()  # Remove projectile if it hits something
            self.update(CustomEvents.UPDATE_PROJECTILE)
        # Notify event system about movement


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
        # print(f"{self._name} has been removed!")  # Debugging
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
