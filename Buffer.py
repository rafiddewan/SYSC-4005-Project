from Workstation import WorkStation


class Buffer:

    def __init__(self, workstation: WorkStation):
        self.size = 0
        self.workstation = workstation
    
    def getSize(self):
        return self.size
    
    def addComponent(self):
        self.size +=1
    
    def removeComponent(self):
        self.size -=1
    
    def isFull(self):
        return self.size == 2
    
    def isEmpty(self):
        return self.size == 0
        
    def setWorkstation(self, workstation: WorkStation):
        self.workstation = workstation

    def getWorkstation(self):
        return self.workstation
