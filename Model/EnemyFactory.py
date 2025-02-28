from typing import Final
from .EnemyMock import EnemyMock
class EnemyFactory():
    _DEFAULT_SPEED:Final = 2
    _DEFAULT_HEALTH:Final = 1
    _DEFAULT_ATTACK_DAMAGE:Final = 1
    def createNormalTemplate():
        enemy1 = EnemyMock(EnemyFactory._DEFAULT_ATTACK_DAMAGE, 
                           EnemyFactory._DEFAULT_HEALTH,
                           100, #positionX
                           100, #positionY
                           EnemyFactory._DEFAULT_SPEED)
        enemy2 = EnemyMock(EnemyFactory._DEFAULT_ATTACK_DAMAGE, 
                           EnemyFactory._DEFAULT_HEALTH,
                           100, #positionX
                           100, #positionY
                           EnemyFactory._DEFAULT_SPEED)
        
        return [enemy1, enemy2]
