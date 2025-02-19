import os
import pygame


class SpriteFactory:
    def __init__(self):

        # Get the current working directory
        current_directory = os.path.dirname(__file__)

        # Build the relative path to the image
        image_path = os.path.join(current_directory, '..', 'Assets', 'luffy.png')  # Move one level up to project_root

        # Load the image using pygame
        self.image = pygame.image.load(image_path)

        self.myCoolImage = pygame.transform.scale(self.image, (50,50))