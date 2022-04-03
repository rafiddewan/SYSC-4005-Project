from Component import Component
from ComponentType import ComponentType


class Buffer:

    def __init__(self, id: int, maxSize: int, componentType: ComponentType):
        self.id = id
        self.maxSize = maxSize
        self.size = 0
        self.componentType = componentType
        self.componentList = []
        self.cumulativeOcc = 0
        self.isSteadyState = False
    
    def getSize(self) -> int:
        """
        Gets the amount of components in the buffer currently
        Returns: current buffer size

        """
        return self.size
    
    def addComponent(self, component:Component) -> bool:
        """
        Adds a component to this buffer
        Returns: True if there is space to add the component, otherwise false

        """
        # print(f"Adding to buffer {self.id}")
        if self.size < self.maxSize:
            self.size += 1
            self.componentList.append(component)
            return True
        return False

    def removeComponent(self) -> Component:
        """
        Removes a component from this buffer
        Returns: The next component in the buffer, None if buffer is empty

        """
        if self.size > 0:
            self.size -= 1
            return self.componentList.pop(0)
        return None
    
    def isFull(self) -> bool:
        """
        If the buffer is full or not
        Returns: True if full

        """
        return self.size == self.maxSize
    
    def isEmpty(self) -> bool:
        """
        If the buffer is empty or not
        Returns: True if the buffer is empty
        """
        return self.size == 0
        
    def getId(self) -> int:
        """
        Gets the id of the buffer
        Returns: The id
        """
        return self.id
    
    def getComponentType(self) -> ComponentType:
        """
        Get the component type assigned to this buffer
        Returns: The component type
        """
        return self.componentType

    def getCummulativeOcc(self) -> float:
        """
        Gets the cumulative buffer occupancy value
        Returns: cumulative occupancy
        """
        return self.cumulativeOcc

    def accumulateOcc(self, timeElapsed:float):
        """
        Accumulates the buffer occupancy value
        Args:
            timeElapsed: The amount of time elapsed since the last accumulation
        """
        # print(f"Buffer {self.id} size is: {self.size}")
        if self.isSteadyState:
            self.cumulativeOcc = self.cumulativeOcc + (self.getSize() * timeElapsed)
        # print(f"Buffer {self.id} cumulative occupancy is: {self.cumulativeOcc}")

    def setSteadyState(self, steadyState:bool):
        """
        Set if we are in steady state or not
        Args:
            steadyState: True if in steady state
        """
        self.isSteadyState = steadyState
