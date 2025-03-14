from .Enemy import Enemy
import random
import pygame
import math

class Seagull(Enemy):
    """A fast, ranged enemy that tries to keep distance from the player and shoots at the player."""
    
    def __init__(self, attackDamage: int, healthPoints: int, positionX: int, positionY: int, speed: int, shoot_distance: int = 300):
        super().__init__("Seagull", attackDamage, healthPoints, speed, positionX, positionY)
        self.shoot_cooldown = 1000  # 1000ms = 1 second between shots
        self.last_shot_time = 0  # Time of last shot
        self.shoot_distance = shoot_distance  # The minimum distance to move away from player
    
    def moveCharacter(self):
        """Seagull moves to maintain distance from the player and shoots projectiles at the player."""
        player_pos = self.get_player_position()
        
        if player_pos:
            player_x, player_y = player_pos
            distance_x = abs(player_x - self._myPositionX)
            distance_y = abs(player_y - self._myPositionY)

            # If the player is too close, move away
            if distance_x < self.shoot_distance and distance_y < self.shoot_distance:
                self._move_away_from_player(player_x, player_y)
            
            # Always shoot at the player, regardless of distance
            self._shoot_at_player(player_x, player_y)
        else:
            self._random_movement()
        self._post_move_event()
    
    def _move_away_from_player(self, player_x, player_y):
        """Move Seagull away from the player to maintain distance."""
        new_x, new_y = self._myPositionX, self._myPositionY
        
        if player_x < self._myPositionX:
            new_x += self._mySpeed  # Move right (away from player)
        elif player_x > self._myPositionX:
            new_x -= self._mySpeed  # Move left (away from player)

        if player_y < self._myPositionY:
            new_y += self._mySpeed  # Move down (away from player)
        elif player_y > self._myPositionY:
            new_y -= self._mySpeed  # Move up (away from player)

        self._check_collision_and_update_position(new_x, new_y, self)

    def _shoot_at_player(self, player_x, player_y):
        """Seagull shoots at the player, regardless of distance."""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_shot_time >= self.shoot_cooldown:

            direction_x = player_x - self._myPositionX
            direction_y = player_y - self._myPositionY
            angle = math.atan2(direction_y, direction_x)
            
            # Shoot in the direction of the player
            self.shoot("SHOOT_PROJECTILE", angle)
            self.last_shot_time = current_time  # Update last shot time

    def _random_movement(self):
        """Moves randomly if the player is too far away."""
        if random.randint(1, 10) == 1:  # Only change direction 10% of the time
            self._direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            
        super().moveCharacter()  # Call the base class method to handle general movement

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
        """Reconstruct a Seagull enemy from a dictionary, ensuring it properly tracks the player."""
        Seagull = cls(
            data["damage"],
            data["health"],
            data["positionX"],
            data["positionY"],
            data["speed"]
        )

        # Restore game world reference
        from .GameWorld import GameWorld
        Seagull._game_world = GameWorld.getInstance()

        # ✅ Restore movement state correctly
        Seagull._direction = data["direction"]
        Seagull.last_shot_time = pygame.time.get_ticks()  # Reset shot cooldown


        return Seagull
