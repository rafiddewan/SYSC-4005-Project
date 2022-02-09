from Event import Event
from EventType import EventType


class WorkstationEvent(Event):
    def __init__(self, createdTime: float, startTime: float, eventType: EventType, workstationId: int):
        Event.__init__(self, createdTime, startTime, eventType)
        self.workstationId = workstationId
    
    def getWorkstationId(self) -> int:
        return self.workstationId
