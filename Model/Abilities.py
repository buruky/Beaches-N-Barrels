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
        self.player._mySpeed *= 1.5 # Double speed

    def deactivate(self):
        self.player._mySpeed /= 1.5 # Restore speed
        super().deactivate()

class HealAbility(Ability):
    """Temporarily increases health."""
    def __init__(self, player):
        super().__init__(player, duration=3000)  # Set specific duration for speed boost

    def activate(self):
         
        if self.player._myHealth + 50 > self.player.getMaxHealth():
            #self.player.setMaxHealth(self.player._myHealth)
            self.player._myHealth = self.player.getMaxHealth()
        else:
            self.player._myHealth += 50 
        self.player.takeDamage(0)

    def deactivate(self):
        # self.player._myHealth -= 50
        self.player.takeDamage(0)

        super().deactivate()


class InvincibilityAbility(Ability):
    """Temporarily makes the player invincible."""
    def __init__(self, player):
        super().__init__(player, duration=6000)  # Set specific duration for speed boost
        #self.tempHealth = self.player._myHealth

    
    def activate(self):
        #self.tempHealth = self.player._myHealth
        #self.tempMax = self.player.maxHealth
        #self.player._myHealth = 9999
        #self.player.maxHealth = 9999
        #self.player.update("HEALTH")
        #self.player._myHealth = self.tempHealth
        #self.player.maxHealth = self.tempMax

        self.player.setCanDie(False)  # Simulating invincibility
        print("invincible")
    def deactivate(self):

        self.player.update("HEALTH")
        self.player.setCanDie(True)
        print("not Invincible")
        super().deactivate()


class Invincibility(Ability):
    """Temporarily makes the player invincible."""
    def __init__(self, player):
        super().__init__(player, duration=2000)  # Set specific duration for speed boost
        self.tempHealth = self.player._myHealth

    
    def activate(self):
        self.player._canDie = False
        self.player.update("HEALTH")
        print("invince")

    def deactivate(self):

        self.player.update("HEALTH")
        self.player._canDie = True
        print("invince stop")
        super().deactivate()

class LowGravityAbility1(Ability):
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

class LowGravityAbility(Ability):
    """Allows the player (Astronaut) to dash a fixed distance in the direction they're facing."""
    def __init__(self, player, duration=100, cooldown = 2200, dash_distance=200):
        """
        duration: How long the dash ability is considered 'active' (in milliseconds).  
        dash_distance: The number of pixels to dash.
        """
        super().__init__(player, duration)
        self.dash_distance = dash_distance
        self.cooldown = cooldown
        self.last_used = -cooldown
        
    def use(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_used < self.cooldown:
            print("Dash ability is cooling down.")
            return  # Cooldown has not elapsed; do nothing.
        # Otherwise, proceed to use dash.
        self.last_used = current_time  # Record the time dash is used.
        super().use()  # This sets active to True and calls activate().

    def activate(self):
        print("Dash Activated!")
        dx, dy = 0, 0
        direction = self.player._direction  
        if direction == "LEFT":
            dx = -self.dash_distance
        elif direction == "RIGHT":
            dx = self.dash_distance
        elif direction == "UP":
            dy = -self.dash_distance
        elif direction == "DOWN":
            dy = self.dash_distance
        new_x = self.player._myPositionX + dx
        new_y = self.player._myPositionY + dy
        new_x = max(0, min(new_x, ViewUnits.SCREEN_WIDTH - ViewUnits.DEFAULT_WIDTH))
        new_y = max(0, min(new_y, ViewUnits.SCREEN_HEIGHT - ViewUnits.DEFAULT_HEIGHT))

        self.player.teleportCharacter(new_x, new_y)
        self.deactivate()

    def deactivate(self):
        print("Dash Ended.")
        super().deactivate()
