from Component import Component


class Buffer:

    def __init__(self, id, maxSize, componentType: Component):
        self.id = id
        self.maxSize = maxSize
        self.size = 0
        self.componentType = componentType
    
    def getSize(self):
        return self.size
    
    def addComponent(self) -> bool:
        if self.size < self.maxSize:
            self.size += 1
            return True
        return False

    def removeComponent(self) -> bool:
        if self.size > 0:
            self.size -= 1
            return True
        return False
    
    def isFull(self):
        return self.size == self.maxSize
    
    def isEmpty(self):
        return self.size == 0
        
    def getId(self):
        return self.id
    
    def getComponentType(self):
        return self.componentType
