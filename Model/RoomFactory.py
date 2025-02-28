from .Room import Room
from .EnemyFactory import EnemyFactory
from .DungeonCharacterList import DungeonCharacterList
class RoomFactory():
    _instance = None  # Stores the single instance

    def __new__(cls):
        """Ensure only one instance is created."""
        if cls._instance is None:
            cls._instance = super(RoomFactory, cls).__new__(cls)
            cls._instance._init_once()
        return cls._instance
    def _init_once(self):
        self.s = "s "
        self.n = "n "

    def createRoom(self, theRoomType, theX, theY):
        if theRoomType == self.s:
            return self.createNormalRoom(theRoomType, theX, theY)
        elif theRoomType == self.n:
            return self.createNormalRoom(theRoomType, theX, theY)

    def createStartRoom(self, theRoomType:str, theX, theY):
        return Room(theRoomType, theX, theY, DungeonCharacterList())
    
    def createNormalRoom(self, theRoomType, theX, theY):
        enemylist = EnemyFactory.createNormalTemplate()
        return Room(theRoomType, theX, theY, enemylist)
