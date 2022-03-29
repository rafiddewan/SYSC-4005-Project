from ComponentType import ComponentType


class Buffer:

    def __init__(self, id, maxSize, componentType: ComponentType):
        self.id = id
        self.maxSize = maxSize
        self.size = 0
        self.componentType = componentType
        self.componentList = []
        self.cumulativeOcc = 0
    
    def getSize(self):
        """
        Gets the amount of components in the buffer currently
        Returns: current buffer size

        """
        return self.size
    
    def addComponent(self, component) -> bool:
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

    def removeComponent(self):
        """
        Removes a component from this buffer
        Returns: The next component in the buffer, None if buffer is empty

        """
        if self.size > 0:
            self.size -= 1
            return self.componentList.pop(0)
        return None
    
    def isFull(self):
        """
        If the buffer is full or not
        Returns: True if full

        """
        return self.size == self.maxSize
    
    def isEmpty(self):
        """
        If the buffer is empty or not
        Returns: True if the buffer is empty

        """
        return self.size == 0
        
    def getId(self):
        """
        Gets the id of the buffer
        Returns: The id

        """
        return self.id
    
    def getComponentType(self):
        """
        Get the component type assigned to this buffer
        Returns: The component type

        """
        return self.componentType

    def getCummulativeOcc(self):
        """
        Gets the cumulative buffer occupancy value
        Returns: cumulative occupancy

        """
        return self.cumulativeOcc

    def accumulateOcc(self, timeElapsed):
        """
        Accumulates the buffer occupancy value
        Args:
            timeElapsed: The amount of time elapsed since the last accumulation

        Returns: None

        """
        # print(f"Buffer {self.id} size is: {self.size}")
        self.cumulativeOcc = self.cumulativeOcc + (self.getSize() * timeElapsed)
        # print(f"Buffer {self.id} cumulative occupancy is: {self.cumulativeOcc}")
