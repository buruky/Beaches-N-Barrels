import pygame

from .DungeonCharacter import DungeonCharacter
class SingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
    
class EventManager(metaclass=SingletonMeta):
    """Encapsulates event creation, registration, and dispatching."""
    event_handlers = {}
    event_types = {}

    # def get_event_type(self, name):
    #     """Returns the event ID for a given event name."""
    #     return self.event_types.get(name, None)

    @staticmethod
    def registerEvent( event_name, handler):
        """
        Registers an event type and a handler.
        - If the event type doesn't exist, it creates one dynamically.
        - Adds the handler to the event’s handler list.
        """
        if event_name not in EventManager.event_types:
            event_id = pygame.USEREVENT + len(EventManager.event_types) + 1
            EventManager.event_types[event_name] = event_id
            EventManager.event_handlers[event_id] = []  # Initialize handler list
            
        # Register the handler
        EventManager.event_handlers[EventManager.event_types[event_name]].append(handler)

    def RegisterExistingEvent(theEventName, theEventType: int, theHandler):
        EventManager.event_types[theEventName] = theEventType
        EventManager.event_handlers[theEventType] = []  # Initialize handler list
        EventManager.event_handlers[EventManager.event_types[theEventName]].append(theHandler)


    def dispatch_event( event):
        """Calls the appropriate handler(s) when an event is triggered."""
    
        if event.type in EventManager.event_handlers:
            for handler in EventManager.event_handlers[event.type]:
                handler(event)
        