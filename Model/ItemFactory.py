import random
from .Item import MockItem, KeyItem
from ViewUnits import ViewUnits
from .Item import MockItem, KeyItem, invincibilityItem, SpeedItem

class ItemFactory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ItemFactory, cls).__new__(cls)
            cls._instance._init_once()
        return cls._instance

    def _init_once(self):
        pass

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def createItem(self, item_type: str, position: tuple):
        """
        Create and return an item instance.
        - For "mock", returns a MockItem.
        - For "key", returns a KeyItem.
        """
        if item_type.lower() == "mock":
            return MockItem(position)
        elif item_type.lower() == "key":
            return KeyItem(position)
        if item_type.lower() == "invince":
            return invincibilityItem(position)
        elif item_type.lower() == "speed":
            return SpeedItem(position)
        else:
            return None

    def createNormalTemplate(self):
        """
        Returns a list of items for a room.
        There is a 30% chance that no items spawn.
        If items do spawn (1-3 items), each item is placed 50 pixels away from a room corner.
        If multiple items spawn, they are placed in different corners.
        """
        items = []
        if random.random() < 0.3:
            return items
        room_width = ViewUnits.SCREEN_WIDTH
        room_height = ViewUnits.SCREEN_HEIGHT
        corners = [
            (50, 50),  # Top-left
            (room_width - 100, 50), 
            (50, room_height - 100), 
            (room_width - 100, room_height - 100) 
        ]
        num_items = random.randint(1, 3)

        if num_items <= len(corners):
            chosen_corners = random.sample(corners, num_items)
        else:
            chosen_corners = [random.choice(corners) for _ in range(num_items)]

        possible_items = ["MockItem", "SpeedItem", "InvincibilityItem"]
        type_mapping = {
            "MockItem": "mock",
            "SpeedItem": "speed",
            "InvincibilityItem": "invince",
        }
    
        for pos in chosen_corners:
            selected_type = random.choice(possible_items)
            item_arg = type_mapping.get(selected_type, "mock")
            items.append(self.createItem(item_arg, pos))
        
        return items

    def createKeyTemplate(self):
        """
        Returns a list with a single key item spawned in one of the four corners,
        positioned 80 pixels away from the corner.
        """
        room_width = ViewUnits.SCREEN_WIDTH
        room_height = ViewUnits.SCREEN_HEIGHT
        offset = 60
        corners = [
            (80, 80),  
            (room_width - 80 - offset, 80),
            (80, room_height - 80 - offset), 
            (room_width - 80 - offset, room_height - 80 - offset)  
        ]
        pos = random.choice(corners)
        return [self.createItem("key", pos)]
    
    def createBossTemplate(self):
        """
        Returns a list with two healing potion items (for boss rooms) spawned in two distinct
        random corners of the room. Each item is positioned exactly 80 pixels away from the corner.
        """
        room_width = ViewUnits.SCREEN_WIDTH
        room_height = ViewUnits.SCREEN_HEIGHT
        potion_size = 50  # Assuming each potion occupies a 50x50 area


        corners = [
            (80, 80),  
            (room_width - 80 - potion_size, 80), 
            (80, room_height - 80 - potion_size), 
            (room_width - 80 - potion_size, room_height - 80 - potion_size)  
        ]
        chosen_corners = random.sample(corners, 2)
        pos = random.choice(corners)
  
        return [self.createItem("heal", pos)]



    def populateRoomItems(self, room):
        """
        Populates a room with items based on its room type.
        Room types:
       """
        room_type = room.getRoomType()
    
        if room_type == "n ":
            for item in self.createNormalTemplate():
                room.add_item(item)
        elif room_type == "k ":
            for item in self.createKeyTemplate():
                room.add_item(item)
        elif room_type == "b ":
            for item in self.createNormalTemplate():
                room.add_item(item)
        else:
            for item in self.createNormalTemplate():
                room.add_item(item)