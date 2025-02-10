from .DungeonCharacter import DungeonCharacter
class EnemyMock(DungeonCharacter):
    def __init__(self):
        super().__init__(50, 100, 250, 250, 5)#####

        self.direction = None
        self.max_size = 500 
        self.min_size = 10

    def moveCharacter(self, directions):  # Initial color (Green)
        
        dx, dy = 0, 0

        if "LEFT" in directions:
            dx = -1
        if "RIGHT" in directions:
            dx = 1
        if "UP" in directions:
            dy = -1
        if "DOWN" in directions:
            dy = 1

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707

        # Update position
        self._myPositionX += dx * self._mySpeed
        self._myPositionY += dy * self._mySpeed

         # Update direction if moving
        if directions:
            self.direction = directions[-1]  # Last key pressed is priority

    def changeColor(self, theColor):
        self.color = (25,120,0)

    def moveTo(self, num1, num2):
        self._myPositionX = num1
        self._myPositionY = num2
    

    def Dies():
        print("*Dies*")

    

    def getPositionX(self) -> int:
        return self._myPositionX
    
    def getPositionY(self) -> int:
        return self._myPositionY
    
    


    def toString() -> str:
        print("*Strings*")