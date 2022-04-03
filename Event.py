from EventType import EventType


class Event:
    def __init__(self, createdTime: float, startTime: float, eventType: EventType):
        """Initialize an event to be added to a future event list

        Args:
            createdTime (float): The time the event was created at
            startTime (float): The time where this event should start at
            eventType (EventType): The type of event
        """
        self.createdTime = createdTime
        self.startTime = startTime
        self.eventType = eventType
    
    def getCreatedTime(self) -> float:
        """Get the time this event was created at

        Returns:
            (float) : The time this event was created at
        """
        return self.createdTime
    
    def getStartTime(self) -> float:
        """Get the time this event should start at

        Returns:
            (float) : The time this event should start at
        """
        return self.startTime
    
    def getEventType(self) -> EventType:
        """Get the type of event this is

        Returns:
             (EventType) : The type of event
        """
        return self.eventType