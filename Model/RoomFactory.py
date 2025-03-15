from .Room import Room
from .ItemFactory import ItemFactory
from .EnemyFactory import EnemyFactory
from .DungeonCharacterList import DungeonCharacterList
import random
from .Item import MockItem 
from ViewUnits import ViewUnits

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
        self.k = "k "
        self.b = "b "
        self.__myEnemyFactory = EnemyFactory.getInstance()
        self.__myItemFactory = ItemFactory.getInstance()

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
        elif theRoomType == self.k:
            return self.createKeyRoom(theRoomType, theX, theY)
        elif theRoomType == self.b: 
            return self.createBossRoom(theRoomType, theX, theY)

    def createStartRoom(self, theRoomType: str, theX, theY):
        self.__myEnemyFactory.test_database_connection()
        room = Room(theRoomType, theX, theY, DungeonCharacterList())
        # Add a random number (0-2) of items to the start room.
        self.__myItemFactory.populateRoomItems(room)
        return room

    def createNormalRoom(self, theRoomType, theX, theY):    
        roomType = random.randint(1, 5)  # Generate a random number from 1 to 5
        enemylist = self.__myEnemyFactory.createNormalTemplate(roomType)
        room = Room(theRoomType, theX, theY, enemylist)
        # Add a random number (0-2) of items to a normal room.
        self.__myItemFactory.populateRoomItems(room)
        return room

    def createKeyRoom(self, theRoomType, theX, theY):    
        room = Room(theRoomType, theX, theY, DungeonCharacterList())
        self.__myItemFactory.populateRoomItems(room)
        return room

    def createBossRoom(self, theRoomType, theX, theY):    
        enemylist = self.__myEnemyFactory.createBossTemplate()
        room = Room(theRoomType, theX, theY, enemylist)
        self.__myItemFactory.populateRoomItems(room)
        #print("KEY BOSS")
        return room