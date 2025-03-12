from typing import Final
from .Enemy import Enemy
import random
from .Crab import Crab
from .Pirate import Pirate
from .DungeonCharacterList import DungeonCharacterList
from ViewUnits import ViewUnits

class EnemyFactory():
    _instance = None  # Stores the single instance
    _DEFAULT_SPEED:Final = 2
    _DEFAULT_HEALTH:Final = 50
    _DEFAULT_ATTACK_DAMAGE:Final = 20
    

    def __new__(cls):
        """Ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super(EnemyFactory, cls).__new__(cls)
            cls._instance._init_once()
        return cls._instance
    def _init_once(self):
        pass

    @classmethod
    def getInstance(cls):
        """Getter for the singleton instance."""
        if cls._instance is None:  # Ensure an instance exists
            cls._instance = cls()  # This triggers __new__()
        return cls._instance
    
    def createNormalTemplate(self):
        enemyList = DungeonCharacterList()
        screen_width = ViewUnits.SCREEN_WIDTH - 50
        screen_height = ViewUnits.SCREEN_HEIGHT - 50
        enemy1 = Crab(
            EnemyFactory._DEFAULT_ATTACK_DAMAGE, 
            EnemyFactory._DEFAULT_HEALTH,
            random.randint(0, screen_width),  # Random x position
            random.randint(0, screen_height),  # Random y position
            3
        )
        enemy2 = Pirate(
            EnemyFactory._DEFAULT_ATTACK_DAMAGE, 
            EnemyFactory._DEFAULT_HEALTH + 50,
            random.randint(0, screen_width),  # Random x position
            random.randint(0, screen_height),  # Random y position
            EnemyFactory._DEFAULT_SPEED
        )
        enemyList.add_entity(enemy1)
        enemyList.add_entity(enemy2)
        return enemyList
