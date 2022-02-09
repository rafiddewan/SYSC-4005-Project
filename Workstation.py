from random import randint
from tkinter import EventType
from Buffer import Buffer


class WorkStation:
    
    def __init__(self, id, numBuffers, filename):
        self.id = id
        self.buffers = [None] * numBuffers
        self.numProductsCreated = 0
        self.isBusy = False
        self.minutesBusy = 0
        self.serviceTimes = self.__stripServiceTimes(filename)

    def __stripServiceTimes(filename: str):
        serviceTimes = []
        try:
            with open(filename, 'r') as file:
                for line in file:
                    serviceTimes.extend(map(float, line.split()))
        except FileNotFoundError:
            print(f"Cannot find filename: {filename}")
        return serviceTimes 

    def getId(self):
        return self.id
            
    def getBuffers(self):
        return self.buffers

    def setBuffers(self, index: int, buffer: Buffer) -> bool:
        numBuffers = len(self.buffers)

        if(index >= numBuffers or index < 0):
            return False

        self.buffers[index] = buffer
        return True

    def getIsBusy(self) -> bool:
        return self.isBusy
    
    def setIsBusy(self, isBusy: bool):
        self.isBusy = isBusy
    
    def getMinutesBusy(self) -> int:
        return self.minutesBusy
    
    def setMinutesBusy(self, minutesBusy: int):
        self.minutesBusy(minutesBusy)

    def handleInspectorDone(self, event: InspectorEvent) -> Event:
        """
        Handles Inspector Done event

        Goes through each buffer removing a component in order to build a product
        
        Parameters:
            WorkstationEvent: Returns a Product Build (WS) event when 
        
        Return:
            WorkstationEvent: If the workstation is not busy
            None: If the workstation is busy
        """
        currentTime = event.getStartTime()
        startEvent = None

        if self.__buffersAreReady() and not self.getIsBusy():
            startEvent = WorkStationEvent(currentTime, currentTime, EventType.WS, self.getId())
        return startEvent

    def handleWorkstationStarted(self, event: WorkstationEvent) -> event:
        """
        Handles Workstation Started event

        Goes through each buffer removing a component in order to build a product

        Parameter:
            WorkstationEvent: Creates a workstation event
        Return:
            WorkstationEvent: Returns a Product Build (WD) event when 
        """
        randomServiceTime = self.__generateRandomServiceTime()
        currentTime = event.getStartTime()
        self.setIsBusy(True)
        for buffer in self.buffers:
            if buffer.isEmpty():
                raise ValueError("Buffer is empty it should not be empty")
            else:
                buffer.removeComponent()
        productBuilt = WorkstationEvent(currentTime, currentTime + randomServiceTime, EventType.WD, self.getId())

    def handleProductBuilt(self, event: WorkstationEvent) -> event:
        """
        Handles Product Build event

        Frees up workstation, updates the number of products created, and calculates the time it took to build the product

        Parameters:
            WorkstationEvent: Returns a workstation started event to take next job
        """

        #Free up workstation now that the product is built
        self.setIsBusy(False)

        #Increment number of products created
        self.numProductsCreated += 1
        
        currentTime = event.getStartTime()
        
        #Calculate how long it took to build the product
        prouductionTime = currentTime - event.getCreatedTime()


        self.setMinutesBusy(prouductionTime)

        productBuiltEvent = WorkStationEvent(currentTime, currentTime, EventType.WS, self.getId())
        
        return productBuiltEvent
        
    def __generateRandomServiceTime(self) -> float:
        """
        Generates a random service time using the random integer generator from the python random library

        Returns:
            float: Amount of time a workstation will take to work on a product
        """
        index = randint(0, len(self.serviceTimes) -1)
        return self.serviceTimes[index]
    
    def __buffersAreReady(self) -> bool:
        """
        Checks if a workstation has a component from each buffer to pull out from
        
        Returns:
            bool: If the buffers are ready for the workstation to be in motion
        """
        isReady = True
        for buffer in self.buffers:
            if buffer.isEmpty():
                isReady = False
                break
        return isReady