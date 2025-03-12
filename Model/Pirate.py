from .Enemy import Enemy
import random
import pygame

class Pirate(Enemy):
    """A slow but strong enemy that moves toward the player if nearby."""
    
    def __init__(self, attackDamage: int, healthPoints: int, positionX: int, positionY: int, speed: int):
        super().__init__("Pirate", attackDamage, healthPoints, speed, positionX, positionY)
        self.shoot_cooldown = 1000  # 300ms = 0.3 seconds between shots
        self.last_shot_time = 0  # Time of last shot

    def moveCharacter(self):
        """Pirate moves toward the player if close enough, otherwise moves randomly."""
        player_pos = self.get_player_position()

        if player_pos:
            player_x, player_y = player_pos
            distance_x = abs(player_x - self._myPositionX)
            distance_y = abs(player_y - self._myPositionY)

            if distance_x < 300 and distance_y < 300:  # If player is within 300 pixels
                self._move_towards_player(player_x, player_y)
            else:
                self._random_movement()
        else:
            self._random_movement()


    
    def _move_towards_player(self, player_x, player_y):
        """Moves Pirate toward the player's location."""
        current_time = pygame.time.get_ticks()
        new_x, new_y = self._myPositionX, self._myPositionY
        
        if player_x < self._myPositionX:
            new_x -= self._mySpeed  # Move left
        elif player_x > self._myPositionX:
            new_x += self._mySpeed  # Move right

        if player_y < self._myPositionY:
            new_y -= self._mySpeed  # Move up
        elif player_y > self._myPositionY:
            new_y += self._mySpeed  # Move down
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.shoot("SHOOT_PROJECTILE")
            self.last_shot_time = current_time  # Update last shot time

        self._check_collision_and_update_position(new_x, new_y, self)
        
    def _random_movement(self):
        """Moves randomly if the player is too far away."""
        if random.randint(1, 10) == 1:  # Only change direction 10% of the time
            self._direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            

        super().moveCharacter()
