from .Enemy import Enemy
import random
import pygame

class BeachBall(Enemy):
    """A slow but strong enemy that moves toward the player if nearby and dashes occasionally."""
    
    def __init__(self, attackDamage: int, healthPoints: int, positionX: int, positionY: int, speed: int):
        super().__init__("BeachBall", attackDamage, healthPoints, speed, positionX, positionY)
        self.dash_cooldown = 5000  # Dash cooldown: 5 seconds
        self.last_dash_time = 0  # Time of last dash
        self.steps_before_change = 5  # Number of steps to take in one direction before changing
        self.steps_taken = 0  # Steps taken in the current direction
        self.current_direction = None  # The current direction the BeachBall is moving in

    def moveCharacter(self):
        """Overridden to move the BeachBall in specific patterns."""
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
        """Moves BeachBall toward the player's location."""
        current_time = pygame.time.get_ticks()
        new_x, new_y = self._myPositionX, self._myPositionY

        # Dash if the cooldown has expired
        if current_time - self.last_dash_time >= self.dash_cooldown:
            self._dash_towards_player(player_x, player_y)
            self.last_dash_time = current_time  # Update last dash time
            return  # Skip regular movement for this frame, dash was performed.

        # Ensure movement happens along one axis only (X or Y)
        if abs(player_x - self._myPositionX) > abs(player_y - self._myPositionY):
            # Move left or right (X axis has larger distance)
            if player_x < self._myPositionX:
                new_x -= self._mySpeed  # Move left
                self.current_direction = "LEFT"
            elif player_x > self._myPositionX:
                new_x += self._mySpeed  # Move right
                self.current_direction = "RIGHT"
        else:
            # Move up or down (Y axis has larger distance)
            if player_y < self._myPositionY:
                new_y -= self._mySpeed  # Move up
                self.current_direction = "UP"
            elif player_y > self._myPositionY:
                new_y += self._mySpeed  # Move down
                self.current_direction = "DOWN"

        self.steps_taken += 1  # Increment steps taken in the current direction

        # If we have taken enough steps, change direction
        if self.steps_taken >= self.steps_before_change:
            self._change_direction()

        # Update position after movement and check for collisions
        self._check_collision_and_update_position(new_x, new_y, self)

    def _change_direction(self):
        """Change the direction after taking a set number of steps."""
        # Reset the step counter and randomly choose a new direction
        self.steps_taken = 0

        if self.current_direction == "LEFT":
            self._direction = random.choice(["UP", "DOWN", "RIGHT"])
        elif self.current_direction == "RIGHT":
            self._direction = random.choice(["UP", "DOWN", "LEFT"])
        elif self.current_direction == "UP":
            self._direction = random.choice(["LEFT", "RIGHT", "DOWN"])
        elif self.current_direction == "DOWN":
            self._direction = random.choice(["LEFT", "RIGHT", "UP"])
        
        # Ensuring that the movement stays in cardinal directions
        if self._direction == "LEFT":
            self._myPositionX -= self._mySpeed
        elif self._direction == "RIGHT":
            self._myPositionX += self._mySpeed
        elif self._direction == "UP":
            self._myPositionY -= self._mySpeed
        elif self._direction == "DOWN":
            self._myPositionY += self._mySpeed

    def _random_movement(self):
        """Moves randomly if the player is too far away."""
        if random.randint(1, 10) == 1:  # 10% chance to change direction
            self._direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
            
        # Regular movement logic (in cardinal directions)
        super().moveCharacter()

    def _dash_towards_player(self, player_x, player_y):
        """Performs a dash movement towards the player."""
        dash_distance = self._mySpeed * 3  # Dash 3 times the normal speed
        new_x, new_y = self._myPositionX, self._myPositionY
        
        if abs(player_x - self._myPositionX) > abs(player_y - self._myPositionY):
            # Dash left or right (X axis has larger distance)
            if player_x < self._myPositionX:
                new_x -= dash_distance  # Dash left
            elif player_x > self._myPositionX:
                new_x += dash_distance  # Dash right
        else:
            # Dash up or down (Y axis has larger distance)
            if player_y < self._myPositionY:
                new_y -= dash_distance  # Dash up
            elif player_y > self._myPositionY:
                new_y += dash_distance  # Dash down

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
        """Reconstruct a BeachBall enemy from a dictionary, ensuring it properly tracks the player."""
        BeachBall = cls(
            data["damage"],
            data["health"],
            data["positionX"],
            data["positionY"],
            data["speed"]
        )

        # Restore game world reference
        from .GameWorld import GameWorld
        BeachBall._game_world = GameWorld.getInstance()

        # ✅ Restore movement state correctly
        BeachBall._direction = data["direction"]
        BeachBall.last_shot_time = pygame.time.get_ticks()  # Reset shot cooldown


        return BeachBall
