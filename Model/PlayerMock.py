class PlayerMock:
    def __init__(self):
        self.player_x = 250
        self.player_y = 250
        self.speed = 5

    def movePlayer(self, dx, dy):  # Initial color (Green)
        
        self.player_x += dx * self.speed
        self.player_y += dy * self.speed

    def changeColor(self, theColor):
        self.color = theColor