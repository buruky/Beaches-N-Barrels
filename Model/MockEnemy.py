class MockEnemy:
    """
    A simplified enemy mock for testing, with no dependency on GameWorld, events, or rendering.
    """

    def __init__(self, name="MockEnemy", attackDamage=10, healthPoints=100, speed=1, positionX=50, positionY=50):
        """
        Initializes the mock enemy with basic attributes.

        :param name: Enemy name (for identification).
        :param attackDamage: Damage the enemy can deal.
        :param healthPoints: Starting health.
        :param speed: Movement speed (not used here).
        :param positionX: Starting X coordinate.
        :param positionY: Starting Y coordinate.
        """
        self._name = name
        self._myAttackDamage = attackDamage
        self._myHealth = healthPoints
        self._mySpeed = speed
        self._myPositionX = positionX
        self._myPositionY = positionY
        self._direction = "RIGHT"
        self._is_dead = False

    def takeDamage(self, damage: int):
        """
        Apply damage to the enemy. If health reaches 0 or below, mark as dead.

        :param damage: Damage to subtract from health.
        """
        self._myHealth -= damage
        if self._myHealth <= 0:
            self.Dies()

    def Dies(self):
        """Mark the mock enemy as dead."""
        self._is_dead = True

    def getAttackDamage(self):
        return self._myAttackDamage

    def getHealth(self):
        return self._myHealth

    def isDead(self):
        return self._is_dead

    def getName(self):
        return self._name

    def getPositionX(self):
        return self._myPositionX

    def getPositionY(self):
        return self._myPositionY

    def moveCharacter(self):
        """
        Simulate movement by adjusting position based on direction.
        Useful for unit testing movement logic.
        """
        if self._direction == "LEFT":
            self._myPositionX -= self._mySpeed
        elif self._direction == "RIGHT":
            self._myPositionX += self._mySpeed
        elif self._direction == "UP":
            self._myPositionY -= self._mySpeed
        elif self._direction == "DOWN":
            self._myPositionY += self._mySpeed

    def setDirection(self, direction: str):
        self._direction = direction