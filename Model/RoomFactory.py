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
        self.__myEnemyFactory = EnemyFactory.getInstance()

    @classmethod
    def getInstance(cls):
        """Getter for the singleton instance."""
        if cls._instance is None:  # Ensure an instance exists
            cls._instance = cls()  # This triggers __new__()
        return cls._instance

    def createRoom(self, theRoomType, theX, theY):
        if theRoomType == self.s:
            return self.createStartRoom(theRoomType, theX, theY)
        elif theRoomType == self.n:
            return self.createNormalRoom(theRoomType, theX, theY)

    def createStartRoom(self, theRoomType:str, theX, theY):
        return Room(theRoomType, theX, theY, DungeonCharacterList())
    
    def createNormalRoom(self, theRoomType, theX, theY):
        enemylist = self.__myEnemyFactory.createNormalTemplate()
        return Room(theRoomType, theX, theY, enemylist)
