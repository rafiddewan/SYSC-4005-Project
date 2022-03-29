import csv

class Replication:
    def __init__(self):
        self.throughput = 0
        self.probabilityWorkstationBusy = {}
        self.probabilityInspectorBlocked = {}
        self.avgBufferOccup = {}
        batches = []
    
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
        print(f"\n--------------Batch Stats-----------------")
        for i in range(len(self.batches)):
            print(f"\n----------Batch {i+1}-------------")
            self.batches[i].printStats()

    def getBatches(self):
        return self.batches

    def setBatches(self, batches):
        self.batches = batches

    def writeStatsToCsv(self, filename):
        with open(filename, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)            
            for i  in range(len(self.batches)):
                batch = self.batches[i]
                batchRow = batch.getCsvFormattedStats()
                batchRow.insert(0,str(i+1))
                writer.writerow(batchRow)
