import pygame
from ViewUnits import ViewUnits

class UsableItem:
    """
    Base class for usable items. Items can be activated (used) and then become inactive
    until their cooldown expires. Each item has its own cooldown (duration) in milliseconds.
    """
    def __init__(self, name: str, description: str = "", cooldown: int = 3000):
        self._name = name
        self._description = description
        self._cooldown = cooldown  # cooldown duration in milliseconds
        self._active = False
        self._start_time = None  # Time when the item was activated
   
    def getName(self):
        return self._name
    
    def to_dict(self):
        """Convert player state to a dictionary for serialization."""
        data = {
            "name": self._name,
            "description": self._description,
            "cooldown": self._cooldown,
            "active": self._active,
            "start_time": self._start_time,
            "class": self.__class__.__name__  # Store class type for deserialization
        }
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Reconstruct a Player object from a dictionary."""
        required_keys = ["name", "description", "cooldown", "active", "start_time"]
        for key in required_keys:
            if key not in data:
                raise ValueError(f"Missing key in saved data: {key}")
            
        item = cls(data["name"],
                   data["description"],
                   data["cooldown"]
                   )
        
        # Restore additional attributes
        item._active = data.get("active", False)  # Default to False if missing
        item._start_time = data.get("start_time", None)  # Default to None if missing

        return item
    
    def __str__(self):
        return self._name

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
   
    def to_dict(self):
        """Convert item to dictionary including position data."""
        data = super().to_dict()  # Get parent class dictionary
        data["position"] = tuple(self.position)  # Ensure it's stored as a tuple
        data["class"] = self.__class__.__name__  # Store class type for deserialization
        return data


    @classmethod
    def from_dict(cls, data):
        """Reconstruct a MockItem from dictionary, ensuring position is properly restored."""
        position = tuple(data.get("position", (10, 10)))  # Ensure it's a tuple
        item = cls(position=position)

        # Restore optional state fields
        item._active = data.get("active", False)  # Default to inactive
        item._start_time = data.get("start_time", None)  # Default to None

        # Restore correct collision rectangle at the right position
        item.rect = pygame.Rect(position[0], position[1], 50, 50)

        return item
    
class KeyItem(UsableItem):
    """
    A simple test item that, when used, subtracts 10 health from the player.
    It uses a 3-second cooldown by default.
    """
    def __init__(self, position=None):
        super().__init__("KeyItem", "This is a test item for pickup.", cooldown=3000)
        if position is None:
            position = (10, 10)
        self.position = position
        # Create a collision rectangle (50x50) at the given position.
        self.rect = pygame.Rect(position[0], position[1], 50, 50)

    
    def __str__(self):
        return "MockItem"
