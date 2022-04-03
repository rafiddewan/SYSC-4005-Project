from Event import Event
from EventType import EventType


class WorkstationEvent(Event):
    def __init__(self, createdTime: float, startTime: float, eventType: EventType, workstationId: int):
        """Initialize an inspector event

        Args:
            createdTime (float): The time the event was created at
            startTime (float): The time where this event should start at
            eventType (EventType): The type of event
            workstationId (int): The id of the workstation
        """
        Event.__init__(self, createdTime, startTime, eventType)
        self.workstationId = workstationId
    
    def getWorkstationId(self) -> int:
        """Get the id of the workstation that created this event

        Returns:
            int : Id of the workstaiton
        """
        return self.workstationId
