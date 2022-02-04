from Buffer import Buffer

class Inspector:

    def __init__(self, numBuffers):
        self.numBuffers = numBuffers
        self.buffers = [None] * numBuffers #creates an empty array of length numBuffers
        self.timeRemaining = 0
        self.currentComponentType = 0

    def getBuffers(self):
        return self.buffers
    
    def setBuffer(self, index: int, buffer: Buffer) -> bool:
        if(index < self.numBuffers and index > 0):
            self.buffers[index] = buffer
            return True
        return False

    def getTimeRemaining(self) -> int:
        return self.timeRemaining

    def setTimeRemaining(self, timeRemaining: int) -> None:
        self.timeRemaining = timeRemaining
    
    def getCurrentComponentType(self):
        return self.currentComponentType

    def setCurrentComponentType(self, type: int) -> None: #make sure type is from 1-3 when using this
        self.currentComponentType = type
    
    