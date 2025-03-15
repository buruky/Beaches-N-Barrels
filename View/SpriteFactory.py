import copy
import os
import re
from typing import Final
import pygame
from .SpriteSheet import SpriteSheet
from ViewUnits import ViewUnits

class SpriteFactory:
    
    def __init__(self):
        """Loads all sprites and prepares them for use."""
        self.DOLPHIN_STRING:Final = "Dolphin"
        self.BUDDHA_STRING:Final = "Buddha"
        self.ASTRONAUT_STRING:Final = "Astronaut"

        self.current_dir = os.path.dirname(os.path.dirname(__file__))  # Get the directory where the current script is located
        assets_path = os.path.join(self.current_dir, "Assets")
        

        # Load Player Images
        #self.myRawPlayerImage = pygame.image.load(os.path.join(assets_path, 'luffy.png'))
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
        #self.myPlayerImage = pygame.transform.scale(self.myRawPlayerImage, ViewUnits.DEFAULT_SPRITE_DIM)
        #self.myPlayerImage2 = pygame.transform.flip(self.myPlayerImage, True, False)

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
        self.projectileAstronautImage = pygame.transform.scale(self.myRaw3ProjectileImage, (100,100))

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
        elif theName == "Door":
            return self.createDoorSpriteSheet(theId, thePositionX, thePositionY)
        elif theName == "Pirate":
            return self.createPirateSpriteSheet(theId, thePositionX, thePositionY)
        elif theName == "Crab":
            return self.createCrabSpriteSheet(theId, thePositionX, thePositionY)
        elif theName == "ProjectileDolphin":
            return self.createProjectileDolphinSpriteSheet(theId, thePositionX, thePositionY)
        elif theName == "ProjectileBuddha":
            return self.createProjectileBuddhaSpriteSheet(theId, thePositionX, thePositionY)
        elif theName == "ProjectileAstronaut" or theName == "ProjectilePirate":
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
    

    def getAssetList(self,theName:str, theState:str):

        assets_folder = os.path.join(self.current_dir,"Assets/" + theName)  # Assuming 'assets' folder is in the same directory as the script
        
        images = []
        image_files = [f for f in os.listdir(assets_folder) if f.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

        for image_file in image_files:
            if re.search(theState, image_file):
                image_path = os.path.join(assets_folder, image_file)
                image = pygame.image.load(image_path)
                images.append(image)
        return images

    

    def createDolphinSpriteSheet(self, theId, thePositionX, thePositionY):
        """Creates a Dolphin sprite sheet."""
        imageDict = {ViewUnits.DEFAULT_STATE_NAME: self.getAssetList(self.DOLPHIN_STRING, ViewUnits.DEFAULT_STATE_NAME),
                     ViewUnits.DIRECTION_UP: self.getAssetList(self.DOLPHIN_STRING, ViewUnits.DIRECTION_UP),
                     ViewUnits.DIRECTION_DOWN: self.getAssetList(self.DOLPHIN_STRING,ViewUnits.DIRECTION_DOWN),
                     ViewUnits.DIRECTION_LEFT: self.getAssetList(self.DOLPHIN_STRING, ViewUnits.DIRECTION_LEFT),
                     ViewUnits.DIRECTION_RIGHT: self.getAssetList(self.DOLPHIN_STRING, ViewUnits.DIRECTION_RIGHT),
                     }  
        dolphinRect = copy.copy(ViewUnits.DEFAULT_RECT)
        dolphinRect.x = thePositionX
        dolphinRect.y = thePositionY

        return SpriteSheet(theId, self.DOLPHIN_STRING, imageDict, dolphinRect)  
    def createDoorSpriteSheet(self, theId, thePositionX, thePositionY):
        imageDict = {
                     ViewUnits.DIRECTION_UP: self.getAssetList("Door", ViewUnits.DIRECTION_UP),
                     ViewUnits.DIRECTION_DOWN: self.getAssetList("Door",ViewUnits.DIRECTION_DOWN),
                     ViewUnits.DIRECTION_LEFT: self.getAssetList("Door", ViewUnits.DIRECTION_LEFT),
                     ViewUnits.DIRECTION_RIGHT: self.getAssetList("Door", ViewUnits.DIRECTION_RIGHT),
                     }  
        DoorRect = pygame.Rect((thePositionX,thePositionY), (64,64))
        return SpriteSheet(theId, "Door", imageDict, DoorRect)  
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
