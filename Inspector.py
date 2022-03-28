import random
from Buffer import Buffer
from Event import Event
from EventType import EventType
from InspectorEvent import InspectorEvent
from Component import Component
from WorkstationEvent import WorkstationEvent
import numpy as np
from RandomNumberGeneration import RandomNumberGeneration


class Inspector:

    def __init__(self, id, numBuffers, componentsToHandle, generators):
        """Initialize an inspector

        Args:
            id (int): The inspector's id. In our simulation this will either be 1 or 2
            numBuffers (int): The number of buffers assigned to this inspector
            componentsToHandle (Component[]): The components the inspector is capable of processing
            seeds (List[int]): Relative path to the file that contains the inspector's cleaning time data
        """
        self.id = id
        self.numBuffers = numBuffers
        self.buffers = [None] * numBuffers  # creates an empty array of length numBuffers
        self.timeBlocked = 0.0
        self.isBlocked = False
        self.blockedStartTime = 0.0
        self.componentsToHandle = componentsToHandle
        self.randomNumberGenerators = {}
        for i in range(len(componentsToHandle)): #populate dict with key as component and value as the random num generator
            self.randomNumberGenerators[componentsToHandle[i]] = generators[i]
        self.currComponent = None
        self.numComponentsPickedUp = 0

    def getBuffers(self):
        """Get the list of buffers this inspector has

        Returns:
            Buffer[]: The buffers the inspector has
        """
        return self.buffers
    
    def setBuffer(self, index: int, buffer: Buffer) -> bool:
        """Set a buffer to one of the items in the list of buffers

        Args:
            index (int): Where in the list the buffer should be added to
            buffer (Buffer): Buffer to be added

        Returns:
            bool : True if the buffer was successfully added
        """
        if 0 <= index < self.numBuffers:
            self.buffers[index] = buffer
            return True
        return False
    
    def getComponentsToHandle(self):
        """Get the list of components handled by this inspector

        Returns:
            Component[]: The components this inspector handles
        """
        self.componentsToHandle

    def getTimeBlocked(self):
        """Get the amount of time this inspector has been blocked

        Returns:
            float: Minutes the inspector has been waiting for a buffer to free up
        """
        return self.timeBlocked

    def getNumComponentsPickedUp(self):
        """Get the amount of components picked up by the inspector

        Returns:
            int: Number of components
        """
        return self.numComponentsPickedUp

    def getId(self):
        return self.id

    def handleInspectorStarted(self, event: InspectorEvent) -> Event:
        """Select a random cleaning time, select a component to clean, create and return an Inspect Done event to be
        added to the FEL

        Args:
            event (InspectorEvent): The current inspector event to be handled

        Raises:
            ValueError: Raises an error if the inspector's components to handle have not been set

        Returns:
            Event: An Inspector Done event to be added to the Simulation's future event list
        """
        if (event.getInspectorId() != self.id) or (self.isBlocked):
            if self.isBlocked: 
                print(f"Inspector {self.id} is blocked")
            return None
        self.currComponent = self.__selectComponentToClean()
        self.numComponentsPickedUp += 1
        cleaningTime = self.__generateRandomCleaningTime()
        currentTime = event.getStartTime()
        if (self.currComponent == None):
            raise ValueError("Inspector is not fully configured for use. Please set the components this inspector should handle.")
        
        print(f"Inspector {self.id} started cleaning {self.currComponent} at {currentTime}")
        doneEvent = InspectorEvent(currentTime, (currentTime + cleaningTime), EventType.ID, self.id)
        return doneEvent
    
    def handleInspectorDone(self, event: InspectorEvent) -> Event:
        """Iterate through the buffers to see if we can add a component to one of them. If we can then create the next
        InspectorStarted event, otherwise set inspector as blocked

        Args:
            event (InspectorEvent): The current inspector event to be handled

        Returns:
            Event: An Inspector Started event to be added to the Simulation's future event list. None if the inspector
            is blocked
        """
        if (event.getInspectorId() != self.id): #not this inspector
            return None

        success = self.__iterateThroughBuffers(self.currComponent)
        currentTime = event.getStartTime()
        if success:
            startEvent = InspectorEvent(currentTime, currentTime, EventType.IS, self.id)
            print(f"Inspector {self.id} finished cleaning {self.currComponent} at {currentTime}")
            return startEvent
        else:
            self.isBlocked = True
            self.blockedStartTime = currentTime
            return None

    def handleWorkstationStarted(self, event: WorkstationEvent) -> Event:
        """If the inspector is blocked, check the buffer if the inspector can become unblocked and create Inspector
        Started event. If the inspector cannot be unblocked, stay blocked.

        Args:
            event (WorkstationEvent): The current workstation started event to be handled

        Returns:
            Event: An Inspector Started event to be added to the Simulation's future event list. None if the inspector
            is blocked
        """
        if self.isBlocked:
            success = self.__iterateThroughBuffers(self.currComponent)
            if success:
                self.isBlocked = False
                currentTime = event.getStartTime()
                self.timeBlocked += currentTime - self.blockedStartTime
                startEvent = InspectorEvent(currentTime, currentTime, EventType.IS, self.id)
                return startEvent
        return None

    def __generateRandomCleaningTime(self) -> float:
        """Use the random number generator's method to get the next random sequential random number

        Returns:
            float: The amount of time the inspector will take to clean the component
        """
        return self.randomNumberGenerators[self.currComponent].generateRandomServiceTime()
    
    def __selectComponentToClean(self) -> Component:
        """If the inspector handles more than one component, randomly select which one to clean.

        Returns:
            Component: The component type to be cleaned
        """
        return random.choice(self.componentsToHandle)
        
    def __iterateThroughBuffers(self, componentType: Component) -> bool:
        """Iterate through the buffers to see if the inspector can add a component to at least one of them.

        Args:
            componentType (Component): The component type to be added to a buffer

        Returns:
            bool: True if the inspector is able to add to the buffer, otherwise False
        """
        success = False
        for buffer in self.buffers:
            if (buffer.getComponentType() == componentType) and not buffer.isFull():
                success = buffer.addComponent()
                if success: 
                    break
        return success
