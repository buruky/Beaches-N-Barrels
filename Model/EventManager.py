import pygame

from .DungeonCharacter import DungeonCharacter

class EventManager:
    """Encapsulates event creation, registration, and dispatching."""
    PLAYER_MOVED = pygame.USEREVENT + 1
    ENEMY_MOVED = pygame.USEREVENT + 2

    def __init__(self):
        self.event_handlers = {}
        self.event_types = {
            "ENEMY_MOVED": pygame.USEREVENT + 1,  # Encapsulated event
        }

    def get_event_type(self, name):
        """Returns the event ID for a given event name."""
        return self.event_types.get(name, None)

    def register_event(self, event_type, handler):
        """Registers a function to handle a specific event type."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    def dispatch_event(self, event):
        """Calls the appropriate handler(s) when an event is triggered."""
        if event.type in self.event_handlers:
            for handler in self.event_handlers[event.type]:
                handler(event)
