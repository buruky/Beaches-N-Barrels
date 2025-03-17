import random
from .Item import MockItem, KeyItem, invincibilityItem, SpeedItem
from ViewUnits import ViewUnits

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
        Returns a list of mock items (3-5) created at random positions.
        """
        items = []
        num_items = random.randint(1, 3)
        if num_items == 1:
            pos = (ViewUnits.SCREEN_WIDTH /2,
                   ViewUnits.SCREEN_HEIGHT /2)
            items.append(self.createItem("mock", pos))
        if num_items == 2:
            pos = (ViewUnits.SCREEN_WIDTH /2,
                   ViewUnits.SCREEN_HEIGHT - 50)
            items.append(self.createItem("speed", pos))
        if num_items == 3:
            pos = (ViewUnits.SCREEN_WIDTH /2,
                   ViewUnits.SCREEN_HEIGHT /2)
            items.append(self.createItem("speed", pos))
        
        for _ in range(random.randint(1, 3)):
            pos = (random.randint(0, ViewUnits.SCREEN_WIDTH - 50),
                    random.randint(0, ViewUnits.SCREEN_HEIGHT - 50))
            items.append(self.createItem("mock", pos))
            items.append(self.createItem("speed", pos))
            items.append(self.createItem("invince", pos))
          
        
        return items

    def createKeyTemplate(self):
        """
        Returns a list with a single key item at a fixed position.
        """
        pos = (ViewUnits.SCREEN_WIDTH // 2 + 199, ViewUnits.SCREEN_HEIGHT // 2 + 199)
        return [self.createItem("key", pos)]

    def populateRoomItems(self, room):
        """
        Populates a room with items based on its room type.
        Room types:
          - "s " : Start room gets several mock items.
          - "n " : Normal room gets items from the normal template.
          - "k " : Key room gets items from the key template.
          - "b " : Boss room gets several mock items.
        """
        room_type = room.getRoomType()

        if room_type == "s ":
            """
            for _ in range(random.randint(3, 5)):
                pos = (random.randint(0, ViewUnits.SCREEN_WIDTH - 50),
                       random.randint(0, ViewUnits.SCREEN_HEIGHT - 50))
                room.add_item(self.createItem("mock", pos))
                """
        elif room_type == "n ":
            for item in self.createNormalTemplate():
                room.add_item(item)
        elif room_type == "k ":
            for item in self.createKeyTemplate():
                room.add_item(item)
        elif room_type == "b ":
            """
            for _ in range(random.randint(3, 5)):
                pos = (random.randint(0, ViewUnits.SCREEN_WIDTH - 50),
                       random.randint(0, ViewUnits.SCREEN_HEIGHT - 50))
                room.add_item(self.createItem("mock", pos))
                """
        else:
            # For unknown types, you might choose a default behavior.
            for item in self.createNormalTemplate():
                room.add_item(item)