import pygame
from ViewUnits import ViewUnits

class UsableItem:
    """
    Base class for usable items. Items can be activated (used) and then become inactive
    until their cooldown expires. Each item has its own cooldown (duration) in milliseconds.
    """
    def __init__(self, name: str, description: str = "", cooldown: int = 3000):
        self.name = name
        self.description = description
        self.cooldown = cooldown  # cooldown duration in milliseconds
        self.active = False
        self.start_time = None  # Time when the item was activated

    def __str__(self):
        return self.name

class MockItem(UsableItem):
    """
    A simple test item that, when used, subtracts 10 health from the player.
    It uses a 3-second cooldown by default.
    """
    def __init__(self, position=None):
        super().__init__("MockItem", "This is a test item for pickup.", cooldown=3000)
        if position is None:
            position = (10, 10)
        self.position = position
        # Create a collision rectangle (50x50) at the given position.
        self.rect = pygame.Rect(position[0], position[1], 50, 50)
