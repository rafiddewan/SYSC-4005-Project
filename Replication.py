class Replication:
    def __init__(self, throughput: float, workstationBusy: float, inspectorBlocked:float, avgBufferOccup: float):
        self.throughput = throughput
        self.workstationBusy = workstationBusy
        self.inspectorBlocked = inspectorBlocked
        self.avgBufferOccup = avgBufferOccup
    
    def getThorughput(self) -> float:
        return self.throughput
    
    def setThroughput(self, throughput):
        self.throughput = throughput

    def getWorkstationBusy(self) -> float:
        return self.workstationBusy
    
    def setWorkstationBusy(self, workstationBusy):
        self.workstationBusy = workstationBusy
    
    def getInspectorBlocked(self) -> float:
        return self.inspectorBlocked

    def setInspectorBlocked(self, inspectorBlocked):
        self.inspectorBlocked = inspectorBlocked

    def getAvgBufferOccupancy(self) -> float:
        return self.avgBufferOccup
    
    def setAvgBufferOccupancy(self, avgBufferOccup):
        self.avgBufferOccup = avgBufferOccup