from ComponentType import ComponentType
from Event import Event
from EventType import EventType


class InspectorEvent(Event):
    def __init__(self, createdTime: float, startTime: float, eventType: EventType, inspectorId: int):
        """Initialize an inspector event

        Args:
            createdTime (float): The time the event was created at
            startTime (float): The time where this event should start at
            eventType (EventType): The type of event
            inspectorId (int): The id of the inspector
        """
        Event.__init__(self, createdTime, startTime, eventType)
        self.inspectorId = inspectorId
    
    def getInspectorId(self):
        """Get the id of the inspector that created this event

        Returns:
            int : Id of the inspector
        """
        return self.inspectorId