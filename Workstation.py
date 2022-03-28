from mailbox import FormatError
from random import randint
from Buffer import Buffer
from Event import Event
from EventType import EventType
from InspectorEvent import InspectorEvent
from WorkstationEvent import WorkstationEvent
import numpy as np

class WorkStation:
    
    def __init__(self, id, numBuffers, randomNumberGenerator):
        """Workstation constructor

        Args:
            id (int): The workstation's id. In our simulation this will either be 1, 2 or 3
            numBuffers (int): The number of buffers assigned to this inspector
            filename (string): Relative Path to the file that contains the workstation's service time data
        """

        self.id = id
        self.buffers = [None] * numBuffers
        self.numProductsCreated = 0
        self.isBusy = False
        self.minutesBusy = 0.0
        self.randomNumberGenerator = randomNumberGenerator

    def getBuffers(self):
        """Get the list of buffers this workstation has

        Returns:
            Buffer[]: The buffers the workstation has
        """

        return self.buffers
    
    def setBuffer(self, index: int, buffer: Buffer):
        """Set a buffer to one of the items in the list of buffers

        Args:
            index (int): Where in the list the buffer should be added to
            buffer (Buffer): Buffer to be added

        Returns:
            bool : True if the buffer was successfully added
        """

        if(index > len(self.buffers) or index < 0):
            raise IndexError(f"Wrong index for the buffer, the max index of the buffer is {len(buffer) - 1}")
        self.buffers[index] = buffer

    def getId(self):
        """
        Gets the id of the workstation

        Returns:
            int: Id of the workstation
        """
        return self.id

    def getIsBusy(self) -> bool:
        """
        Checks if the workstation is busy or not

        Returns:
            bool: True if the workstaiton is busy, False if the workstation is not busy
        """

        return self.isBusy
    
    def getNumProductsCreated(self) -> int:
        """
        Number of products the workstation built

        Returns:
            int: Total number of products build
        """

        return self.numProductsCreated

    def getMinutesBusy(self) -> int:
        """
        Time that the workstation was busy building products

        Returns:
            int: Total time the workstation was busy
        """

        return self.minutesBusy

    def handleInspectorDone(self, event: InspectorEvent) -> Event:
        """
        Handles Inspector Done event

        Goes through each buffer removing a component in order to build a product
        
        Args:
            InspectorEvent: The event where an Inspector is done 
        
        Return:
            WorkstationEvent: Return a Workstation Started Event (WS)
            None: If the workstation is busy
        """

        currentTime = event.getStartTime()
        startEvent = None

        #Create the workstation started event only if the buffers are ready and if the workstation is free
        if self.__buffersAreReady() and not self.getIsBusy():
            startEvent = WorkstationEvent(currentTime, currentTime, EventType.WS, self.getId())
        
        return startEvent

    def handleWorkstationStarted(self, event: WorkstationEvent) -> Event:
        """
        Handles Workstation Started event

        Goes through each buffer removing a component in order to build a product

        Args:
            WorkstationEvent: Creates a workstation event

        Return:
            WorkstationEvent: Returns a Workstation Done (WD) 
        """
        if event.workstationId != self.id:
            return None

        #Set workstation to busy
        self.isBusy = True

        #Generate a random service time for the workstation
        randomServiceTime = self.__generateRandomServiceTime()

        currentTime = event.getStartTime()

        # Remove a component from each buffer in order to build the product
        for buffer in self.buffers:
            if buffer.isEmpty():
                raise ValueError("Buffer is empty it should not be empty")
            else:
                buffer.removeComponent()
                print(f"Workstation {self.id} removed component {buffer.getComponentType()} from Buffer {buffer.getId()} at {currentTime}")
        workStationDone = WorkstationEvent(currentTime, currentTime + randomServiceTime, EventType.WD, self.getId())
        return workStationDone

    def handleWorkstationDone(self, event: WorkstationEvent) -> Event:
        """
        Handles WorkStation Done event

        Frees up workstation, updates the number of products created, and calculates the time it took to build the product

        Args:
            WorkstationEvent: Returns a workstation started event to take next job
        """
        if event.getWorkstationId() != self.getId():
            return None
            
        #Free up workstation now that the product is built
        self.isBusy = False

        #Increment number of products created
        self.numProductsCreated += 1
        
        currentTime = event.getStartTime()
        
        #Calculate how long it took to build the product
        prouductionTime = currentTime - event.getCreatedTime()

        self.minutesBusy += prouductionTime

        startEvent = None

        print(f"Workstation {self.id} finished assembly at {currentTime}")

        #Create the workstation started event only if the buffers are ready and if the workstation is free
        if self.__buffersAreReady() and not self.getIsBusy():
            startEvent = WorkstationEvent(currentTime, currentTime, EventType.WS, self.getId())
        
        return startEvent
        
    def __generateRandomServiceTime(self) -> float:
        """
        Use the random number generator's method to get the next random sequential random number

        Returns:
            float: Amount of time a workstation will take to work on a product
        """

        return self.randomNumberGenerator.generateRandomServiceTime()
    
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