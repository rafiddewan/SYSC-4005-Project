from Component import Component
from Event import Event
from EventType import EventType


class InspectorEvent(Event):
    def __init__(self, createdTime: float, startTime: float, eventType: EventType, inspectorId: int,
                 componentType: Component):
        """Initialize an inspector event

        Args:
            createdTime (float): The time the event was created at
            startTime (float): The time where this event should start at
            eventType (EventType): The type of event
            inspectorId (int): The id of the inspector
            componentType (Component): The type of component that the inspector is working with right now
        """
        Event.__init__(self, createdTime, startTime, eventType)
        self.inspectorId = inspectorId
        self.componentType = componentType
    
    def getInspectorId(self):
        """Get the id of the inspector that created this event

        Returns:
            int : Id of the inspector
        """
        return self.inspectorId
    
    def getComponentType(self):
        """Get the component type that the inspector is working with right now

        Returns:
            Component : The component type 
        """
        return self.componentType
