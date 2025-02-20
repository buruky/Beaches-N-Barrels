import os
import pygame
from .SpriteSheet import SpriteSheet

class SpriteFactory:
    def __init__(self):
        self.listOfSpriteSheets = {}

        # Get the current working directory
        current_directory = os.path.dirname(__file__)

        # Build the relative path to the player and enemy images
        player_image_path = os.path.join(current_directory, '..', 'Assets', 'luffy.png')
        enemy_image_path = os.path.join(current_directory, '..', 'Assets', 'speederman.png')  # New enemy sprite

        # Load images using pygame
        self.player_image = pygame.image.load(player_image_path)
        self.enemy_image = pygame.image.load(enemy_image_path)

        # Resize images
        self.myCoolImage = pygame.transform.scale(self.player_image, (50,50))
        self.myCoolImage2 = pygame.transform.flip(self.myCoolImage, True, False)  # Flipped player sprite

        self.enemyImage = pygame.transform.scale(self.enemy_image, (50,50))
        self.enemyImage2 = pygame.transform.flip(self.enemyImage, True, False)  # Flipped enemy sprite

    def add(self, theSpriteSheet):
        self.listOfSpriteSheets[theSpriteSheet.getName()] = theSpriteSheet

    def Initalize(self):
        # Player Sprites
        playerDict = {
            "IDLE": [self.myCoolImage, self.myCoolImage2]  # Player idle animation
        }

        # Enemy Sprites
        enemyDict = {
            "IDLE": [self.enemyImage2, self.enemyImage]  # Enemy idle animation
        }

        # Add both player and enemy to the sprite list
        self.add(SpriteSheet("PlayerMock", 50, 50, 100, 100, playerDict))
        self.add(SpriteSheet("EnemyMock", 50, 50, 100, 100, enemyDict))