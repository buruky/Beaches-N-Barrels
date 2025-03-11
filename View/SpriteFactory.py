import copy
import os
import pygame
from .SpriteSheet import SpriteSheet
from ViewUnits import ViewUnits

class SpriteFactory:
    
    def __init__(self):
        """Loads all sprites and prepares them for use."""
        current_directory = os.path.dirname(__file__)
        assets_path = os.path.join(current_directory, '..', 'Assets')

        # Load Player Images
        self.myRawPlayerImage = pygame.image.load(os.path.join(assets_path, 'luffy.png'))
        self.myRawDolphinImage = pygame.image.load(os.path.join(assets_path, 'Dolphin.png'))  
        self.myRawBuddhaImage = pygame.image.load(os.path.join(assets_path, 'Buddha.jpg'))  # NEW
        self.myRawAstronautImage = pygame.image.load(os.path.join(assets_path, 'Astronaut.jpg'))  # NEW

        # Load Enemy Images
        self.myRawEnemyImage = pygame.image.load(os.path.join(assets_path, 'speederman.png'))
        self.myRawPirateImage = pygame.image.load(os.path.join(assets_path, 'pirate.png'))
        self.myRawCrabImage = pygame.image.load(os.path.join(assets_path, 'crab.png'))

        # Load Projectile Image
        self.myRawProjectileImage = pygame.image.load(os.path.join(assets_path, 'projectileDolphin.png'))
        self.myRaw2ProjectileImage = pygame.image.load(os.path.join(assets_path, 'projectileBuddha.png'))
        self.myRaw3ProjectileImage = pygame.image.load(os.path.join(assets_path, 'projectileAstronaut.png'))

        # Resize and Flip Sprites
        self.myPlayerImage = pygame.transform.scale(self.myRawPlayerImage, ViewUnits.DEFAULT_SPRITE_DIM)
        self.myPlayerImage2 = pygame.transform.flip(self.myPlayerImage, True, False)

        self.dolphinImage = pygame.transform.scale(self.myRawDolphinImage, ViewUnits.DEFAULT_SPRITE_DIM)  
        self.dolphinImage2 = pygame.transform.flip(self.dolphinImage, True, False)  

        self.buddhaImage = pygame.transform.scale(self.myRawBuddhaImage, ViewUnits.DEFAULT_SPRITE_DIM)  # NEW
        self.buddhaImage2 = pygame.transform.flip(self.buddhaImage, True, False)  # NEW

        self.astronautImage = pygame.transform.scale(self.myRawAstronautImage, ViewUnits.DEFAULT_SPRITE_DIM)  # NEW
        self.astronautImage2 = pygame.transform.flip(self.astronautImage, True, False)  # NEW

        self.enemyImage = pygame.transform.scale(self.myRawEnemyImage, ViewUnits.DEFAULT_SPRITE_DIM)
        self.enemyImage2 = pygame.transform.flip(self.enemyImage, True, False)

        self.pirateImage = pygame.transform.scale(self.myRawPirateImage, ViewUnits.DEFAULT_SPRITE_DIM)
        self.pirateImage2 = pygame.transform.flip(self.pirateImage, True, False)

        self.crabImage = pygame.transform.scale(self.myRawCrabImage, ViewUnits.DEFAULT_SPRITE_DIM)
        self.crabImage2 = pygame.transform.flip(self.crabImage, True, False)
        
        # Resize (and optionally flip) the projectile image.
        # Assuming the projectile is symmetric, flipping might not be necessary,
        # but we create two images for consistency.
        self.projectileDolphinImage = pygame.transform.scale(self.myRawProjectileImage, ViewUnits.DEFAULT_SPRITE_DIM)
        self.projectileBuddhaImage = pygame.transform.scale(self.myRaw2ProjectileImage, ViewUnits.DEFAULT_SPRITE_DIM)
        self.projectileAstronautImage = pygame.transform.scale(self.myRaw3ProjectileImage, ViewUnits.DEFAULT_SPRITE_DIM)

        # Initialize the sprite sheets dictionary if needed
        self.listOfSpriteSheets = {}

    def createSpriteSheet(self, theId, theName, thePositionX, thePositionY):
        """Creates a sprite sheet based on the character type."""
        if theName == ViewUnits.PLAYER_SPRITE_NAME:
            return self.createPlayerSpriteSheet(theId, thePositionX, thePositionY)
        elif theName == "Dolphin":
            return self.createDolphinSpriteSheet(theId, thePositionX, thePositionY)  
        elif theName == "Buddha":
            return self.createBuddhaSpriteSheet(theId, thePositionX, thePositionY)  # NEW
        elif theName == "Astronaut":
            return self.createAstronautSpriteSheet(theId, thePositionX, thePositionY)  # NEW
        elif theName == "Pirate":
            return self.createPirateSpriteSheet(theId, thePositionX, thePositionY)
        elif theName == "Crab":
            return self.createCrabSpriteSheet(theId, thePositionX, thePositionY)
        elif theName == "ProjectileDolphin":
            return self.createProjectileDolphinSpriteSheet(theId, thePositionX, thePositionY)
        elif theName == "ProjectileBuddha":
            return self.createProjectileBuddhaSpriteSheet(theId, thePositionX, thePositionY)
        elif theName == "ProjectileAstronaut":
            return self.createProjectileAstronautSpriteSheet(theId, thePositionX, thePositionY)
        else:  # Default to generic enemy
            return self.createEnemySpriteSheet(theId, thePositionX, thePositionY)

    def createPlayerSpriteSheet(self, theId, thePositionX, thePositionY):
        """Creates a player sprite sheet."""
        imageDict = {ViewUnits.DEFAULT_STATE_NAME: [self.myPlayerImage, self.myPlayerImage2]}
        playerRect = copy.copy(ViewUnits.DEFAULT_RECT)
        playerRect.x = thePositionX
        playerRect.y = thePositionY

        return SpriteSheet(theId, ViewUnits.PLAYER_SPRITE_NAME, imageDict, playerRect)

    def createDolphinSpriteSheet(self, theId, thePositionX, thePositionY):
        """Creates a Dolphin sprite sheet."""
        imageDict = {ViewUnits.DEFAULT_STATE_NAME: [self.dolphinImage, self.dolphinImage2]}  
        dolphinRect = copy.copy(ViewUnits.DEFAULT_RECT)
        dolphinRect.x = thePositionX
        dolphinRect.y = thePositionY

        return SpriteSheet(theId, "Dolphin", imageDict, dolphinRect)  

    def createBuddhaSpriteSheet(self, theId, thePositionX, thePositionY):
        """Creates a Buddha sprite sheet."""
        imageDict = {ViewUnits.DEFAULT_STATE_NAME: [self.buddhaImage, self.buddhaImage2]}  
        buddhaRect = copy.copy(ViewUnits.DEFAULT_RECT)
        buddhaRect.x = thePositionX
        buddhaRect.y = thePositionY

        return SpriteSheet(theId, "Buddha", imageDict, buddhaRect)

    def createAstronautSpriteSheet(self, theId, thePositionX, thePositionY):
        """Creates an Astronaut sprite sheet."""
        imageDict = {ViewUnits.DEFAULT_STATE_NAME: [self.astronautImage, self.astronautImage2]}  
        astronautRect = copy.copy(ViewUnits.DEFAULT_RECT)
        astronautRect.x = thePositionX
        astronautRect.y = thePositionY

        return SpriteSheet(theId, "Astronaut", imageDict, astronautRect)

    def createEnemySpriteSheet(self, theId, thePositionX, thePositionY):
        """Creates a generic enemy sprite sheet."""
        imageDict = {ViewUnits.DEFAULT_STATE_NAME: [self.enemyImage2, self.enemyImage]}
        enemyRect = copy.copy(ViewUnits.DEFAULT_RECT)
        enemyRect.x = thePositionX
        enemyRect.y = thePositionY

        return SpriteSheet(theId, ViewUnits.ENEMY_SPRITE_NAME, imageDict, enemyRect)

    def createPirateSpriteSheet(self, theId, thePositionX, thePositionY):
        """Creates a Pirate sprite sheet."""
        imageDict = {ViewUnits.DEFAULT_STATE_NAME: [self.pirateImage2, self.pirateImage]}
        pirateRect = copy.copy(ViewUnits.DEFAULT_RECT)
        pirateRect.x = thePositionX
        pirateRect.y = thePositionY

        return SpriteSheet(theId, "Pirate", imageDict, pirateRect)

    def createCrabSpriteSheet(self, theId, thePositionX, thePositionY):
        """Creates a Crab sprite sheet."""
        imageDict = {ViewUnits.DEFAULT_STATE_NAME: [self.crabImage2, self.crabImage]}
        crabRect = copy.copy(ViewUnits.DEFAULT_RECT)
        crabRect.x = thePositionX
        crabRect.y = thePositionY

        return SpriteSheet(theId, "Crab", imageDict, crabRect)

    def createProjectileDolphinSpriteSheet(self, theId, thePositionX, thePositionY):
        """Creates a Projectile sprite sheet."""
        imageDict = {ViewUnits.DEFAULT_STATE_NAME: [self.projectileDolphinImage, self.projectileDolphinImage]}
        projectileRect = copy.copy(ViewUnits.DEFAULT_RECT)
        projectileRect.x = thePositionX
        projectileRect.y = thePositionY

        return SpriteSheet(theId, "ProjectileDolphin", imageDict, projectileRect)

    def createProjectileAstronautSpriteSheet(self, theId, thePositionX, thePositionY):
        """Creates a Projectile sprite sheet."""
        imageDict = {ViewUnits.DEFAULT_STATE_NAME: [self.projectileAstronautImage, self.projectileAstronautImage]}
        projectileRect = copy.copy(ViewUnits.DEFAULT_RECT)
        projectileRect.x = thePositionX
        projectileRect.y = thePositionY

        return SpriteSheet(theId, "ProjectileAstronaut", imageDict, projectileRect)
    def createProjectileBuddhaSpriteSheet(self, theId, thePositionX, thePositionY):
        """Creates a Projectile sprite sheet."""
        imageDict = {ViewUnits.DEFAULT_STATE_NAME: [self.projectileBuddhaImage, self.projectileBuddhaImage]}
        projectileRect = copy.copy(ViewUnits.DEFAULT_RECT)
        projectileRect.x = thePositionX
        projectileRect.y = thePositionY

        return SpriteSheet(theId, "ProjectileBuddha", imageDict, projectileRect)

    def add(self, theSpriteSheet):
        """Adds a sprite sheet to the internal list."""
        self.listOfSpriteSheets[theSpriteSheet.getName()] = theSpriteSheet
