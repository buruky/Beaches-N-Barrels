from typing import Final
from .EnemyMock import EnemyMock
from .DungeonCharacterList import DungeonCharacterList

class EnemyFactory():
    _instance = None  # Stores the single instance
    _DEFAULT_SPEED:Final = 2
    _DEFAULT_HEALTH:Final = 1
    _DEFAULT_ATTACK_DAMAGE:Final = 1
    

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
        enemy1 = EnemyMock(EnemyFactory._DEFAULT_ATTACK_DAMAGE, 
                           EnemyFactory._DEFAULT_HEALTH,
                           150, #positionX
                           100, #positionY
                           EnemyFactory._DEFAULT_SPEED)
        # enemy2 = EnemyMock(EnemyFactory._DEFAULT_ATTACK_DAMAGE, 
        #                    EnemyFactory._DEFAULT_HEALTH,
        #                    400, #positionX
        #                    100, #positionY
        #                    EnemyFactory._DEFAULT_SPEED)
        enemyList.add_entity(enemy1)
        #enemyList.add_entity(enemy2)
        return enemyList
