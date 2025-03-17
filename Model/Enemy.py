from abc import ABC
from .DungeonCharacter import DungeonCharacter
from .EventManager import EventManager
from CustomEvents import CustomEvents
from ViewUnits import ViewUnits
import pygame
import random

class Enemy(DungeonCharacter, ABC):
    """Base class for all beach-themed enemies."""
    
    SCREEN_WIDTH = ViewUnits.SCREEN_WIDTH  
    SCREEN_HEIGHT = ViewUnits.SCREEN_HEIGHT  

    def __init__(self, name: str, attackDamage: int, healthPoints: int, speed: int, positionX: int, positionY: int):
        """Initializes an enemy with basic attributes."""
        super().__init__(attackDamage, healthPoints, positionX, positionY, speed)
        self._myAttackDamage = attackDamage
        self._name = name
        self._myHealth = healthPoints
        self._direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self._move_timer = pygame.time.get_ticks()
        from .GameWorld import GameWorld
        self._game_world = GameWorld.getInstance()



    def getRect(self):
        return self._myRect
    def update(self):
        """Updates the enemy's movement and actions."""
        current_time = pygame.time.get_ticks()
        if current_time - self._move_timer > 1000:  # Change direction every 1 sec
            self._direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            self._move_timer = current_time
        self.moveCharacter()

    def getAttackDamage(self):
        return self._myAttackDamage

    def moveCharacter(self):
        """Moves the character based on its current direction."""
        new_x, new_y = self._myPositionX, self._myPositionY

        if self._direction == "UP":
            new_y -= self._mySpeed
        elif self._direction == "DOWN":
            new_y += self._mySpeed
        elif self._direction == "LEFT":
            new_x -= self._mySpeed
        elif self._direction == "RIGHT":
            new_x += self._mySpeed

        # Call helper method to check collision before applying movement
        self._check_collision_and_update_position(new_x, new_y, self)

    def _check_collision_and_update_position(self, new_x, new_y, ignore):
        """Helper method to check for collisions before updating position."""
        new_x = max(0, min(new_x, self.SCREEN_WIDTH - 150))  # Keep inside width
        new_y = max(0, min(new_y, self.SCREEN_HEIGHT - 150))  # Keep inside height

        from .GameWorld import GameWorld
        if not GameWorld.getInstance().check_collision(pygame.Rect(new_x, new_y, 50, 50), ignore):
            self._myPositionX, self._myPositionY = new_x, new_y
            self._post_move_event()

    def takeDamage(self, damage: int):
        self._myHealth -= damage
        if self._myHealth <= 0:
            self.Dies()
            
    def getName(self):
        return self._name
    
    def shoot(self, theEventName: str,angle):
        """Post an event when the projectile moves."""
        event = pygame.event.Event(
                    EventManager.event_types[theEventName],
                    {"shooter": self.getName(),
                    "direction": angle,
                    "damage": self.getAttackDamage(),
                    "positionX": self.getPositionX(),
                    "positionY": self.getPositionY(),
                    "speed": self._mySpeed * 10,
                    "isEnemy": True}   
                )
        pygame.event.post(event)

    def _post_move_event(self):
        """Posts an event when the enemy moves."""
        event = pygame.event.Event(
            EventManager.event_types[CustomEvents.CHARACTER_MOVED],
            {
                "name": self._name,
                "id": id(self),
                "positionX": self._myPositionX,
                "positionY": self._myPositionY
            }
        )
        pygame.event.post(event)

    def get_player_position(self):
        """Returns the player's (x, y) position if available, otherwise None."""
        player = self._game_world.getPlayer()
        return player.getPositionX(), player.getPositionY()



    def Dies(self):
        """Handles enemy death."""
        print(f"{self._name} has been defeated!")
        from .GameWorld import GameWorld
        GameWorld.getInstance().removeEnemy(self)

    def getPositionX(self) -> int:
        return int(self._myPositionX)
    
    def getPositionY(self) -> int:
        return int(self._myPositionY)

    def toString(self):
        return f"{self._name} at ({self._myPositionX}, {self._myPositionY})"

    def to_dict(self):
        """Convert player state to a dictionary for serialization."""
        return {
            "name": self._name,
            "speed": self._mySpeed,
            "health": self._myHealth,
            "direction": self._direction,
            "damage": self._myAttackDamage,
            "positionX": self._myPositionX,
            "positionY": self._myPositionY,

        }
    @classmethod
    def from_dict(cls, data):
        """Reconstruct an Enemy from a dictionary while ensuring movement logic is restored correctly."""
        enemy = cls(
            data["name"],
            data["damage"],
            data["health"],
            data["speed"],      # ✅ Correct order
            data["positionX"],  # ✅ Correct order
            data["positionY"]
        )

        # Restore movement properties
        enemy._direction = data["direction"]
        enemy._move_timer = pygame.time.get_ticks()  # ✅ Reset movement timer

        return enemy
