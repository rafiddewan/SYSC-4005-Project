from ComponentType import ComponentType
import typing
class Component:

    def __init__(self, arrivalTime:float, componentType:ComponentType):
        self.arrivalTime = arrivalTime
        self.componentType = componentType
        self.departureTime = None

    def getComponentType(self) -> ComponentType:
        """
        Get the component type of this component
        Returns: 
            ComponentType: a ComponentType representing the component type
        """
        return self.componentType

    def getArrivalTime(self) -> float:
        """
        Get the time this component arrived in the system
        Returns:
            float: the time the component entered the system
        """
        return self.arrivalTime

    def getDepartureTime(self) -> float: 
        """
        Get the time this component left the system
        Returns:
            float: the time the component left the system
        """
        return self.departureTime

    def setDepartureTime(self, departureTime:float):
        """
        Set the time this component left the system
        """
        self.departureTime = departureTime
