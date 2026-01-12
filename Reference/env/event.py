from enum import Enum, auto

class EventType(Enum):
    ARRIVAL = auto()
    COMPLETION = auto()

class Event:
    """
    Simple event structure for discrete-event simulation.
    """
    def __init__(self, time: int, event_type: EventType, payload=None):
        self.time = time
        self.type = event_type
        self.payload = payload
