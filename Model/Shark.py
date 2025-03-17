from .Enemy import Enemy
import pygame
import random
import math
from .EventManager import EventManager



class Shark(Enemy):
    """A boss enemy representing a shark with special abilities."""
    
    def __init__(self, attackDamage: int, healthPoints: int, positionX: int, positionY: int, speed: int, shoot_distance: int = 300):
        super().__init__("Shark", attackDamage, healthPoints, speed, positionX, positionY)
        self.shoot_distance = shoot_distance  # Distance for the shark to shoot at the player
        self.special_attack_cooldown = 5000  # Time between special attacks (5 seconds)
        self.last_special_attack_time = 0
        self.last_shot_time = pygame.time.get_ticks()  # Initialize last shot time
        self.shoot_cooldown = 1000  # 1 second cooldown for shooting


        self.is_angry = False  # Track if the shark is in an "angry" state for special attacks
        self.boss_health_threshold = healthPoints * 0.5  # The health threshold at which the shark becomes angrier
        self.maxHealth = self._myHealth
        # event = pygame.event.Event(
        #     EventManager.event_types["BOSS_ROOM"],
        #     {"name": self.getName(),
        #     "health": self._myHealth,
        #     "maxHealth": self.maxHealth
        #     }        
        # )
        # pygame.event.post(event)

    def update(self):
        """Updates the shark's movement and actions."""
        current_time = pygame.time.get_ticks()
        
        # Check for special attack (once the health threshold is crossed)
        if self._myHealth <= self.boss_health_threshold and not self.is_angry:
            self.enter_angry_mode()

        # Perform the special attack if the cooldown allows
        if current_time - self.last_special_attack_time >= self.special_attack_cooldown:
            self.perform_special_attack()
        event = pygame.event.Event(
            EventManager.event_types["BOSS_ROOM"],
            {"name": self.getName(),
            "health": self._myHealth,
            "maxHealth": self.maxHealth,
            "isdead":False
            }        
        )
        pygame.event.post(event)
        
        # Regular movement and shooting at player
        self.moveCharacter()

    def moveCharacter(self):
        """Shark moves towards the player or performs other behaviors."""
        player_pos = self.get_player_position()
        
        if player_pos:
            player_x, player_y = player_pos
            distance = pygame.math.Vector2(player_x - self._myPositionX, player_y - self._myPositionY)
            
            # Move towards the player in the "angry" state
            if self.is_angry:
                self._move_towards_player(player_x, player_y)
            else:
                # Normal random movement behavior
                self._random_movement()

            # Always shoot at the player
            self._shoot_at_player(player_x, player_y)

    def _move_towards_player(self, player_x, player_y):
        """Move towards the player aggressively."""
        direction = pygame.math.Vector2(player_x - self._myPositionX, player_y - self._myPositionY)
        move_vector = direction.normalize() * self._mySpeed  # Move towards player
        new_position = pygame.math.Vector2(self._myPositionX, self._myPositionY) + move_vector
        
        # Check for collisions and update position
        self._check_collision_and_update_position(new_position.x, new_position.y, self)

    def _random_movement(self):
        """Random movement if the player is not within range."""
        if random.randint(1, 10) == 1:  # Only change direction 10% of the time
            self._direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

        super().moveCharacter()  # Call the base class method to handle general movement

    def perform_special_attack(self):
        """Special attack where the shark targets the player aggressively."""
        current_time = pygame.time.get_ticks()
        
        if self.is_angry:
            print(f"{self.getName()} performs a special attack!")
            # You can add special effects, like a charging attack or an area attack
            print("IM MARK THE SHARK AND I AM ANGRY")
            # self.shoot("SPECIAL_SHOOT_PROJECTILE")  # Shoot a special projectile
            self.last_special_attack_time = current_time  # Reset the special attack cooldown

    def enter_angry_mode(self):
        """Change the shark's behavior when it becomes enraged."""
        print(f"{self.getName()} becomes enraged!")
        self.is_angry = True
        self._myAttackDamage *= 2  # Double the attack damage when enraged
        self.shoot_distance = 400  # Increase shooting range when enraged

    def _shoot_at_player(self, player_x, player_y):
        """Shark shoots projectiles at the player."""
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot_time >= self.shoot_cooldown:
            # Calculate direction towards player using math.atan2
            direction_x = player_x - self._myPositionX
            direction_y = player_y - self._myPositionY
            angle = math.atan2(direction_y, direction_x)  # Calculate the angle towards the player
            
            # Post event to create the projectile
            # Shoot in the direction of the player
            self.shoot("SHOOT_PROJECTILE", angle)
            self.last_shot_time = current_time  # Update last shot tim

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
        """Reconstruct a Shark enemy from a dictionary, ensuring it properly tracks the player."""
        Shark = cls(
            data["damage"],
            data["health"],
            data["positionX"],
            data["positionY"],
            data["speed"]
        )

        # Restore game world reference
        from .GameWorld import GameWorld
        Shark._game_world = GameWorld.getInstance()

        # ✅ Restore movement state correctly
        Shark._direction = data["direction"]
        Shark.last_shot_time = pygame.time.get_ticks()  # Reset shot cooldown


        return Shark