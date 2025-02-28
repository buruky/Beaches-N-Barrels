from typing import Final
from .EnemyMock import EnemyMock
from .DungeonCharacterList import DungeonCharacterList

class EnemyFactory():
    _DEFAULT_SPEED:Final = 2
    _DEFAULT_HEALTH:Final = 1
    _DEFAULT_ATTACK_DAMAGE:Final = 1
    def createNormalTemplate():
        enemyList = DungeonCharacterList()
        enemy1 = EnemyMock(EnemyFactory._DEFAULT_ATTACK_DAMAGE, 
                           EnemyFactory._DEFAULT_HEALTH,
                           150, #positionX
                           100, #positionY
                           EnemyFactory._DEFAULT_SPEED)
        enemy2 = EnemyMock(EnemyFactory._DEFAULT_ATTACK_DAMAGE, 
                           EnemyFactory._DEFAULT_HEALTH,
                           400, #positionX
                           100, #positionY
                           EnemyFactory._DEFAULT_SPEED)
        enemyList.add_entity(enemy1)
        enemyList.add_entity(enemy2)
        return enemyList
