from .Room import Room
from .EnemyFactory import EnemyFactory
from .DungeonCharacterList import DungeonCharacterList
class RoomFactory():
    def createRoom(theRoomType, theX, theY):
        if theRoomType == "s ":
            RoomFactory.createStartRoom(theRoomType, theX, theY)
        elif theRoomType == "n ":
            RoomFactory.createNormalRoom(theRoomType, theX, theY)

    def createStartRoom(theRoomType:str, theX, theY):
        return Room(theRoomType, theX, theY, DungeonCharacterList())
    
    def createNormalRoom(theRoomType, theX, theY):
        enemylist = EnemyFactory.createNormalTemplate()
        return Room(theRoomType, theX, theY, [])
