from .Room import Room
from .EnemyFactory import EnemyFactory
class RoomFactory():
    def createRoom(self, theRoomType, theX, theY):
        if theRoomType == "s ":
            self.createStartRoom(theRoomType, theX, theY)
        elif theRoomType == "n ":
            self.createNormalRoom(theRoomType, theX, theY)

    def createStartRoom(self, theRoomType, theX, theY):
        return Room(theRoomType, theX, theY, [])
    
    def createNormalRoom(self, theRoomType, theX, theY):
        enemylist = EnemyFactory.createNormalTemplate()
        return Room(theRoomType, theX, theY, [])
