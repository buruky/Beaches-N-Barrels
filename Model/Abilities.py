import pygame
import random
from ViewUnits import ViewUnits
class Ability:
    """Base class for all abilities."""
    
    def __init__(self, player, duration=3000):  # Duration in milliseconds
        self.player = player
        self.duration = duration
        self.active = False
        self.start_time = None  # Track when the ability starts

    def use(self):
        """Activates the ability and starts tracking the duration."""
        if not self.active:
            self.active = True
            self.start_time = pygame.time.get_ticks()  # Record activation time
            self.activate()
    def is_active(self):
        return self.active
    def activate(self):
        """Effect of the ability (to be overridden in subclasses)."""
        pass

    def update(self):
        """Checks if the ability duration has expired and deactivates it."""
        if self.active and pygame.time.get_ticks() - self.start_time >= self.duration:
            self.deactivate()

    def deactivate(self):
        """Stops the ability after duration."""
        self.active = False
        # print(f"{self.__class__.__name__} ability ended.")

class SpeedBoostAbility(Ability):
    """Temporarily increases speed."""
    def __init__(self, player):
        super().__init__(player, duration=3000)  # Set specific duration for speed boost

    def activate(self):
        self.player._mySpeed *= 2  # Double speed

    def deactivate(self):
        self.player._mySpeed /= 2  # Restore speed
        super().deactivate()

class HealAbility(Ability):
    """Temporarily increases health."""
    def __init__(self, player):
        super().__init__(player, duration=3000)  # Set specific duration for speed boost

    def activate(self):
        self.player._myHealth += 50  # Increase health by 50
        if self.player._myHealth > self.player.getMaxHealth():
            self.player.setMaxHealth(self.player._myHealth)
        self.player.takeDamage(0)

    def deactivate(self):
        # self.player._myHealth -= 50
        self.player.takeDamage(0)

        super().deactivate()


class InvincibilityAbility(Ability):
    """Temporarily makes the player invincible."""
    def __init__(self, player):
        super().__init__(player, duration=6000)  # Set specific duration for speed boost
        self.tempHealth = self.player._myHealth

    
    def activate(self):
        self.tempHealth = self.player._myHealth
        self.tempMax = self.player.maxHealth
        self.player._myHealth = 9999
        self.player.maxHealth = 9999
        self.player.update("HEALTH")
        self.player._myHealth = self.tempHealth
        self.player.maxHealth = self.tempMax

        self.player._canDie = False  # Simulating invincibility

    def deactivate(self):

        self.player.update("HEALTH")
        self.player._canDie = True
        super().deactivate()

class LowGravityAbility(Ability):
    """Simulates low gravity jumping."""
    def __init__(self, player):
        super().__init__(player, duration=4000)  # Set specific duration for speed boost
    
    def activate(self):
        randX = random.randint(0, ViewUnits.SCREEN_WIDTH)
        randY = random.randint(0, ViewUnits.SCREEN_HEIGHT)
        self.player.teleportCharacter(randX, randY)

    def deactivate(self):
        # self.player._mySpeed /= 0.5
        super().deactivate()
