class Replication:
    def __init__(self):
        self.throughput = 0
        self.probabilityWorkstationBusy = {}
        self.probabilityInspectorBlocked = {}
        self.avgBufferOccup = {}
    
    def getThroughput(self) -> float:
        """
        Get throughput
        Returns: 
            float: throughput
        """
        return self.throughput
    
    def setThroughput(self, throughput:float):
        """
        Set throughput
        Args:
            throughput(float): the throughput
        """
        self.throughput = throughput

    def getProbabilityWorkstationBusy(self):
        """
        Get dictionary of workstations and probability they are busy for each
        Returns: Dictionary of workstations ids + probabilities
        """
        return self.probabilityWorkstationBusy
    
    def addWorkstationBusyProbability(self, workstationId: int, probability: float):
        """
        Add a probability for a workstation into the dictionary
        Args:
            workstationId(int): workstation id
            probability(float): probability the workstation is busy
        """
        self.probabilityWorkstationBusy[workstationId] = probability
    
    def getProbabilityInspectorBlocked(self):
        """
        Get dictionary of inspector ids and probability they are blocked for each
        Returns: Dictionary of inspectors and the probability they are blocked

        """
        return self.probabilityInspectorBlocked

    def addInspectorBlockedProbability(self, inspectorId: int, probability: float):
        """
        Add an inpsector the probability that it is blocked
        Args:
            inspectorId(int): Inspector id
            probability(float): probability that the inspector is blocked
        """
        self.probabilityInspectorBlocked[inspectorId] = probability

    def getAvgBufferOccupancy(self):
        """
        Get a dictionary of the average buffer occupancies
        Returns: Dictionary of buffer ids and their avg buffer occupancies

        """
        return self.avgBufferOccup
    
    def addAvgBufferOccupancy(self, bufferId:int, avgBufferOccup: float):
        """
        Add a buffer occupancy into the dictionary
        Args:
            bufferId(int): Buffer id
            avgBufferOccup(float):average buffer occupancy
        """
        self.avgBufferOccup[bufferId] = avgBufferOccup

    def printStats(self):
        """
        Print stats for this replication
        """
        print(f"Throughput: {self.throughput}")
        print(f"Probability Workstations Busy: {self.probabilityWorkstationBusy}")
        print(f"Probability Inspectors Blocked: {self.probabilityInspectorBlocked}")
        print(f"Average Buffer Occupancy: {self.avgBufferOccup}")

    def getReplicationData(self):
        """
        Gets a list of all the quantities of interest for this replication.
        Returns: List of all the quantities of interest for this replication.
        """
        data = []
        data.append(self.throughput)
        for key in self.probabilityWorkstationBusy.keys():
            data.append(self.probabilityWorkstationBusy[key])

        for key in self.probabilityInspectorBlocked.keys():
            data.append(self.probabilityInspectorBlocked[key])

        for key in self.avgBufferOccup.keys():
            data.append(self.avgBufferOccup[key])
        return data