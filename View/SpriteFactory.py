import os
import pygame
from .SpriteSheet import SpriteSheet
from ViewUnits import ViewUnits

class SpriteFactory:
    
    def __init__(self):

        # Get the current working directory
        current_directory = os.path.dirname(__file__)

        # Build the relative path to the player and enemy images
        player_image_path = os.path.join(current_directory, '..', 'Assets', 'luffy.png')
        enemy_image_path = os.path.join(current_directory, '..', 'Assets', 'speederman.png')  # New enemy sprite

        # Load images using pygame
        self.myRawPlayerImage = pygame.image.load(player_image_path)
        self.myRawEnemyImage = pygame.image.load(enemy_image_path)

        # Resize images
        self.myPlayerImage = pygame.transform.scale(self.myRawPlayerImage, ViewUnits.DEFAULT_SPRITE_DIM)
        self.myPlayerImage2 = pygame.transform.flip(self.myPlayerImage, True, False)  # Flipped player sprite

        self.enemyImage = pygame.transform.scale(self.myRawEnemyImage, ViewUnits.DEFAULT_SPRITE_DIM)
        self.enemyImage2 = pygame.transform.flip(self.enemyImage, True, False)  # Flipped enemy sprite


    def createSpriteSheet(self,theId, theName, thePositionX, thePositionY):
        if theName == ViewUnits.PLAYER_SPRITE_NAME:
            return self.createPlayerSpriteSheet(theId, thePositionX,thePositionY)
        elif theName == ViewUnits.ENEMY_SPRITE_NAME:
            return self.createEnemySpriteSheet(theId, thePositionX, thePositionY)

    def createPlayerSpriteSheet(self, theId, thePositionX, thePositionY):
        imageDict = dict()
        imageDict[ViewUnits.DEFAULT_STATE_NAME] = [self.myPlayerImage, self.myPlayerImage2]
        """
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
        """
        playerRect = ViewUnits.DEFAULT_RECT
        playerRect.x = thePositionX
        playerRect.y = thePositionY

        return SpriteSheet(theId, ViewUnits.PLAYER_SPRITE_NAME, imageDict, playerRect)
    

    def createEnemySpriteSheet(self, theId, thePositionX, thePositionY):
        imageDict = dict()
        imageDict[ViewUnits.DEFAULT_STATE_NAME] = [self.enemyImage2, self.enemyImage]
        enemyRect = ViewUnits.DEFAULT_RECT
        enemyRect.x = thePositionX
        enemyRect.y = thePositionY

        return SpriteSheet(theId, ViewUnits.ENEMY_SPRITE_NAME, imageDict, enemyRect)
    

    def add(self, theSpriteSheet):
        self.listOfSpriteSheets[theSpriteSheet.getName()] = theSpriteSheet

    