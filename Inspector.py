from Buffer import Buffer
from Event import Event
from EventType import EventType
from InspectorEvent import InspectorEvent
from ComponentType import ComponentType
from WorkstationEvent import WorkstationEvent
from Component import Component
from typing import Dict
from typing import List


class Inspector:

    def __init__(self, id, numBuffers, componentsToHandle, generators, roundRobinPolicy):
        """Initialize an inspector

        Args:
            id (int): The inspector's id. In our simulation this will either be 1 or 2
            numBuffers (int): The number of buffers assigned to this inspector
            componentsToHandle (Component[]): The components the inspector is capable of processing
            generators (List[int]): Number generators to use for each component to handle
            roundRobinPolicy: The operating policy which will be used to deliver components to buffers.
                        If True, uses round robin policy. Otherwise uses the original priority policy
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
        if len(componentsToHandle) > 1:
            self.randomNumberGenerators["choose component"] = generators[len(componentsToHandle)]
        self.currComponentType = None
        self.numComponentsPickedUp = 0
        self.currComponent = None
        self.isSteadyState = False
        self.roundRobinPolicy = roundRobinPolicy
        self.currStartIdx = 0

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
    
    def getComponentsToHandle(self) -> List[Component]:
        """Get the list of components handled by this inspector

        Returns:
            Component[]: The components this inspector handles
        """
        self.componentsToHandle

    def getTimeBlocked(self) -> float:
        """Get the amount of time this inspector has been blocked

        Returns:
            float: Minutes the inspector has been waiting for a buffer to free up
        """
        return self.timeBlocked

    def getNumComponentsPickedUp(self) -> int:
        """Get the amount of components picked up by the inspector

        Returns:
            int: Number of components
        """
        return self.numComponentsPickedUp

    def getId(self)-> int:
        """
        Gets the id of the inspector

        Returns: the id of the inspector

        """
        return self.id

    def getGenerators(self) -> Dict:
        """
        Get the random number generators associated with this inspector
        Returns: Dictionary of random number generators for each component type, key = the component type

        """
        generators = []
        for componentType in self.componentsToHandle:
            generators.append(self.randomNumberGenerators[componentType])
        if self.randomNumberGenerators.get("choose component"):
            generators.append(self.randomNumberGenerators.get("choose component"))
        return generators

    def setSteadyState(self, steadyState:bool):
        """
        Set if we are in steady state or not
        Args:
            steadyState: True if in steady state
        """
        self.isSteadyState = steadyState

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
            # print(f"Inspector {self.id} is blocked, skipping inspector started event")
            return None
        self.currComponentType = self.__selectComponentToClean()
        self.numComponentsPickedUp += 1
        cleaningTime = self.__generateRandomCleaningTime()
        currentTime = event.getStartTime()
        self.currComponent = Component(currentTime, self.currComponentType)
        if (self.currComponentType == None):
            raise ValueError("Inspector is not fully configured for use. Please set the components this inspector should handle.")
        
        # print(f"Inspector {self.id} started cleaning {self.currComponentType} at {currentTime}")
        doneEvent = InspectorEvent(currentTime, (currentTime + cleaningTime), EventType.ID, self.id)
        return doneEvent
    
    def handleInspectorDone(self, event: InspectorEvent) -> Event:
        """
        Iterate through the buffers to see if we can add a component to one of them. If we can then create the next
        InspectorStarted event, otherwise set inspector as blocked

        Args:
            event (InspectorEvent): The current inspector event to be handled

        Returns:
            Event: An Inspector Started event to be added to the Simulation's future event list. None if the inspector
            is blocked
        """
        if (event.getInspectorId() != self.id): #not this inspector
            return None

        success = self.__iterateThroughBuffers(self.currComponentType)
        currentTime = event.getStartTime()
        if success:
            startEvent = InspectorEvent(currentTime, currentTime, EventType.IS, self.id)
            # print(f"Inspector {self.id} finished cleaning {self.currComponentType} at {currentTime}")
            return startEvent
        else:
            self.isBlocked = True
            # print(f"Inspector {self.id} is now blocked due to buffers being full")
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
            success = self.__iterateThroughBuffers(self.currComponentType)
            if success:
                # print(f"Inspector {self.id} is now unblocked")
                self.isBlocked = False
                currentTime = event.getStartTime()
                if self.isSteadyState:
                    self.timeBlocked += currentTime - self.blockedStartTime
                startEvent = InspectorEvent(currentTime, currentTime, EventType.IS, self.id)
                return startEvent
        return None

    def __generateRandomCleaningTime(self) -> float:
        """Use the random number generator's method to get the next random sequential random number

        Returns:
            float: The amount of time the inspector will take to clean the component
        """
        return self.randomNumberGenerators[self.currComponentType].generateRandomServiceTime()
    
    def __selectComponentToClean(self) -> ComponentType:
        """If the inspector handles more than one component, randomly select which one to clean.

        Returns:
            ComponentType: The component type to be cleaned
        """
        if self.randomNumberGenerators.get("choose component"):
            randomNum = self.randomNumberGenerators.get("choose component").lcm()
            return self.componentsToHandle[randomNum % len(self.componentsToHandle)]
        else:
            return self.componentsToHandle[0]
        
    def __iterateThroughBuffers(self, componentType: ComponentType) -> bool:
        """Iterate through the buffers to see if the inspector can add a component to at least one of them.

        Args:
            componentType (ComponentType): The component type to be added to a buffer

        Returns:
            bool: True if the inspector is able to add to the buffer, otherwise False
        """
        success = False
        for i in range(self.numBuffers):
            buffer = self.buffers[(self.currStartIdx + i) % self.numBuffers]
            if (buffer.getComponentType() == componentType) and not buffer.isFull():
                success = buffer.addComponent(self.currComponent)
                if success:
                    # print(f"Inspector {self.id} is adding {componentType} to Buffer {buffer.getId()}")
                    if(self.roundRobinPolicy):
                        self.currStartIdx = (self.currStartIdx + i + 1) % self.numBuffers
                    break
        return success
