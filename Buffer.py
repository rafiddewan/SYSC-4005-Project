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
        return self.size
    
    def addComponent(self, component) -> bool:
        if self.size < self.maxSize:
            self.size += 1
            self.componentList.append(component)
            return True
        return False

    def removeComponent(self):
        if self.size > 0:
            self.size -= 1
            return self.componentList.pop(0)
        return None
    
    def isFull(self):
        return self.size == self.maxSize
    
    def isEmpty(self):
        return self.size == 0
        
    def getId(self):
        return self.id
    
    def getComponentType(self):
        return self.componentType

    def getCummulativeOcc(self):
        return self.cumulativeOcc

    def accumulateOcc(self, timeElapsed):
        print(self.size)
        print(timeElapsed)
        self.cumulativeOcc += self.getSize() * timeElapsed
