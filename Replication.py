class Replication:
    def __init__(self):
        self.throughput = 0
        self.probabilityWorkstationBusy = {}
        self.probabilityInspectorBlocked = {}
        self.avgBufferOccup = {}
    
    def getThorughput(self) -> float:
        return self.throughput
    
    def setThroughput(self, throughput):
        self.throughput = throughput

    def getProbabilityWorkstationBusy(self):
        return self.probabilityWorkstationBusy
    
    def addWorkstationBusyProbability(self, workstationId: int, probability: float):
        self.probabilityWorkstationBusy[workstationId] = probability
    
    def getProbabilityInspectorBlocked(self):
        return self.probabilityInspectorBlocked

    def addInspectorBlockedProbability(self, inspectorId: int, probability: float):
        self.probabilityInspectorBlocked[inspectorId] = probability

    def getAvgBufferOccupancy(self):
        return self.avgBufferOccup
    
    def addAvgBufferOccupancy(self, bufferId:int, avgBufferOccup: float):
        self.avgBufferOccup[bufferId] = avgBufferOccup

    def printStats(self):
        print(f"Throughput: {self.throughput}")
        print(f"Probability Workstations Busy: {self.probabilityWorkstationBusy}")
        print(f"Probability Inspectors Blocked: {self.probabilityInspectorBlocked}")
        print(f"Average Buffer Occupancy: {self.avgBufferOccup}")

    def getReplicationData(self):
        data = []
        data.append(self.throughput)
        for key in self.probabilityWorkstationBusy.keys():
            data.append(self.probabilityWorkstationBusy[key])

        for key in self.probabilityInspectorBlocked.keys():
            data.append(self.probabilityInspectorBlocked[key])

        for key in self.avgBufferOccup.keys():
            data.append(self.avgBufferOccup[key])
        return data