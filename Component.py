from ComponentType import ComponentType
import typing
class Component:

    def __init__(self, arrivalTime:float, componentType:ComponentType):
        self.arrivalTime = arrivalTime
        self.componentType = componentType
        self.departureTime = None

    def getComponentType(self) -> ComponentType:
        return self.componentType

    def getArrivalTime(self) -> float:
        return self.arrivalTime

    def getDepartureTime(self) -> float: 
        return self.departureTime

    def setDepartureTime(self, departureTime:float):
        self.departureTime = departureTime
