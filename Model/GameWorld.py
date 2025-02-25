import pygame
from .Floor import Floor
class GameWorld:
    """Singleton class representing the game world with obstacles and enemies."""

    _instance = None  # Stores the single instance

    def __new__(cls):
        """Ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super(GameWorld, cls).__new__(cls)
            cls._instance._init_once()
        return cls._instance

    def _init_once(self):
        """Initialize the game world only once."""
        self.obstacles = [
            pygame.Rect(150, 150, 50, 500),  # Top-left corner
            pygame.Rect(300, 200, 50, 50),  # Near center
            pygame.Rect(500, 100, 50, 50),  # Top-right area
            pygame.Rect(150, 400, 50, 50),  # Left side
            pygame.Rect(400, 500, 50, 50),  # Bottom-center
            pygame.Rect(600, 300, 50, 50),  # Right side
            pygame.Rect(700, 500, 50, 50),  # Bottom-right
            pygame.Rect(250, 350, 50, 50),  # Slightly off-center
            pygame.Rect(350, 450, 50, 50),  # Middle-right
            pygame.Rect(450, 250, 50, 50),  # Randomly placed
        ]
        self.__myFloor = Floor()
        self.currentRoom = self.__myFloor.getStartRoom()
        self.__myFloor.connect_rooms() 
        self.__myFloor.print_dungeon() 
        grid = self.__myFloor.get_dungeon()
             
        self.enemies = []  # List of enemies
        self.player = [] # player
        self.item = []
        self.doors = []

    @classmethod
    def getInstance(cls):
        """Getter for the singleton instance."""
        return cls._instance

    def get_obstacles(self):
        """Return the list of obstacles."""
        return self.obstacles

    def get_enemies(self):
        """Return the list of enemies."""
        return self.enemies

    def add_enemy(self, enemy):
        """Add an enemy to the game world."""
        self.enemies.append(enemy)

    def add_player(self, player):
        """Add an enemy to the game world."""
        self.player.append(player)

    def remove_enemy(self, enemy):
        """Remove an enemy from the game world."""
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def check_collision(self, rect, ignore=None):
        """Check if a given rectangle collides with any obstacle or enemy."""
        for obstacle in self.obstacles:
            if rect.colliderect(obstacle):
                print(f"Collision with obstacle at {obstacle}")  # Debugging
                return True  # Collision detected

        for enemy in self.enemies:
            if enemy != ignore:  # Don't check collision with itself
                enemy_rect = pygame.Rect(enemy.getPositionX(), enemy.getPositionY(), 50, 50)
                if rect.colliderect(enemy_rect):
                    if ignore in self.player:
                        ignore.Dies()
                    print(f"Collision with another enemy at ({enemy.getPositionX()}, {enemy.getPositionY()})")  # Debugging
                    return True
                
        for player in self.player:
            if player != ignore:  # Don't check collision with itself
                my_rect = pygame.Rect(player.getPositionX(), player.getPositionY(), 50, 50)
                if rect.colliderect(my_rect):
                    if ignore in self.enemies:
                        player.Dies()
                    print(f"Collision with the player at ({player.getPositionX()}, {player.getPositionY()})")  # Debugging
                    return True

            return False  # No collision
        