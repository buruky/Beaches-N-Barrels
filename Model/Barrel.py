import random
import pygame
from .Enemy import Enemy
from .EventManager import EventManager


class Barrel(Enemy):
    """A miniboss enemy that runs away from the player and dashes at the player every few seconds."""
    
    def __init__(self, attackDamage: int, healthPoints: int, positionX: int, positionY: int, speed: int):
        super().__init__("Barrel", attackDamage, healthPoints, speed, positionX, positionY)
        self.dash_cooldown = 5000  # Cooldown between dashes (5 seconds)
        self.dash_duration = 1100  # Duration of the dash (2 seconds)
        self.last_dash_time = 0  # Time of last dash
        self.dash_end_time = 0  # Time when the dash ends
        self.maxHealth = self._myHealth
        self.is_dashing = False  # Track if the barrel is in the middle of a dash
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])  # Random direction for movement

    def moveCharacter(self):
        """Move the BarrelGuard away from the player and dash occasionally."""
        current_time = pygame.time.get_ticks()
        event = pygame.event.Event(
            EventManager.event_types["BOSS_ROOM"],
            {"name": self.getName(),
            "health": self._myHealth,
            "maxHealth": self.maxHealth,
            "isdead":False
            }        
        )
        pygame.event.post(event)
        # Get player position
        player_pos = self.get_player_position()

        if player_pos:
            player_x, player_y = player_pos
            
            # Check if the barrel should dash (cooldown + not currently dashing)
            if current_time - self.last_dash_time >= self.dash_cooldown and not self.is_dashing:
                self._dash_towards_player(player_x, player_y)
                self.last_dash_time = current_time  # Reset dash cooldown
                self.dash_end_time = current_time + self.dash_duration  # Set when dash should end
                self.is_dashing = True  # Set flag to prevent immediate fleeing after dash

            elif self.is_dashing and current_time < self.dash_end_time:
                # Continue dashing, prevent other movement during dash
                self._dash_towards_player(player_x, player_y)

                return  # Skip further movement logic while dashing

            elif self.is_dashing and current_time >= self.dash_end_time:
                # Reset the dashing state after the dash duration ends
                self.is_dashing = False

            # Only allow the barrel to move away or move randomly if it's not dashing
            if not self.is_dashing:
                distance_x = abs(player_x - self._myPositionX)
                distance_y = abs(player_y - self._myPositionY)

                # Run away from the player if they are too close
                if distance_x < 300 and distance_y < 300:  # Player is too close, run away
                    self._move_away_from_player(player_x, player_y)
                else:
                    # Move randomly if player is not close
                    self._random_movement()

    def _move_away_from_player(self, player_x, player_y):
        """Move the BarrelGuard away from the player to keep distance."""
        new_x, new_y = self._myPositionX, self._myPositionY
        
        if player_x < self._myPositionX:
            new_x += self._mySpeed + 1  # Move right (away from player)
        elif player_x > self._myPositionX:
            new_x -= self._mySpeed + 1 # Move left (away from player)

        if player_y < self._myPositionY:
            new_y += self._mySpeed + 1 # Move down (away from player)
        elif player_y > self._myPositionY:
            new_y -= self._mySpeed + 1 # Move up (away from player)

        self._check_collision_and_update_position(new_x, new_y, self)
    def Dies(self):
        """Handles enemy death."""
        print(f"{self._name} has been defeated!")
        event = pygame.event.Event(
            EventManager.event_types["BOSS_ROOM"],
            {"name": self.getName(),
            "health": self._myHealth,
            "maxHealth": self.maxHealth,
            "isdead": True
            }        
        )
        pygame.event.post(event)
        from .GameWorld import GameWorld
        GameWorld.getInstance().removeEnemy(self)

    def _random_movement(self):
        """Random movement if the player is not too close."""
        if random.randint(1, 10) == 1:  # 10% chance to change direction
            self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

        if self.direction == "UP":
            self._myPositionY -= self._mySpeed
        elif self.direction == "DOWN":
            self._myPositionY += self._mySpeed
        elif self.direction == "LEFT":
            self._myPositionX -= self._mySpeed
        elif self.direction == "RIGHT":
            self._myPositionX += self._mySpeed

        # Update position and check for collisions
        self._check_collision_and_update_position(self._myPositionX, self._myPositionY, self)

    def _dash_towards_player(self, player_x, player_y):
        """Perform a dash towards the player."""
        dash_distance = self._mySpeed * 3  # Dash 3 times the normal speed
        
        # Calculate the direction towards the player
        direction = pygame.math.Vector2(player_x - self._myPositionX, player_y - self._myPositionY)
        
        # Normalize the direction to get a unit vector (so that it has a magnitude of 1)
        direction.normalize_ip()  # Normalize the vector in-place

        # Update the position after the dash (move in the direction of the player)
        new_x = self._myPositionX + direction.x * dash_distance
        new_y = self._myPositionY + direction.y * dash_distance
        
        # Debugging output to verify dash position
        print(f"Dash towards player: new_x={new_x}, new_y={new_y}")

        # Update position after dash and check for collisions
        self._check_collision_and_update_position(new_x, new_y, self)

    def to_dict(self):
        """Convert enemy state to a dictionary for serialization."""
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
        """Reconstruct a Barrel enemy from a dictionary, ensuring it properly tracks the player."""
        Barrel = cls(
            data["damage"],
            data["health"],
            data["positionX"],
            data["positionY"],
            data["speed"]
        )

        # Restore game world reference
        from .GameWorld import GameWorld
        Barrel._game_world = GameWorld.getInstance()

        # ✅ Restore movement state correctly
        Barrel._direction = data["direction"]
        Barrel.last_shot_time = pygame.time.get_ticks()  # Reset shot cooldown

        return Barrel
