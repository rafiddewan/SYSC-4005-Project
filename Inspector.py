import random
from Buffer import Buffer
from Event import Event
from EventType import EventType
from InspectorEvent import InspectorEvent
from Component import Component
from WorkstationEvent import WorkstationEvent
import numpy as np


class Inspector:

    def __init__(self, id, numBuffers, numComponentsToHandle, filename):
        """Initialize an inspector

        Args:
            id (int): The inspector's id. In our simulation this will either be 1 or 2
            numBuffers (int): The number of buffers assigned to this inspector
            numComponentsToHandle (int): The number of components this inspector creates
            filename (string): Relative path to the file that contains the inspector's cleaning time data
        """
        self.id = id
        self.numBuffers = numBuffers
        self.buffers = [None] * numBuffers  # creates an empty array of length numBuffers
        self.timeBlocked = 0
        self.isBlocked = False
        self.fileName = filename
        self.numComponentsToHandle = numComponentsToHandle
        self.componentsToHandle = [None] * numComponentsToHandle # creates an empty array of length numComponentsToHandle
        self.timeData = np.loadtxt(self.fileName) # store all of the sample data from the file

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
        if 0 < index < self.numBuffers:
            self.buffers[index] = buffer
            return True
        return False
    
    def getComponentsToHandle(self):
        """Get the list of components handled by this inspector

        Returns:
            Component[]: The components this inspector handles
        """
        self.componentsToHandle
    
    def setComponentToHandle(self, index: int, component: Component) -> bool:
        """Set a component to one of the items in the list of components to handle

        Args:
            index (int): Where in the list the component should be added to
            component (Component): Component to be added

        Returns:
            [type]: True if component was added
        """
        if 0 < index < self.numComponentsToHandle:
            self.componentsToHandle[index] = component
            return True
        return False

    def getTimeBlocked(self):
        """Get the amount of time this inspector has been blocked

        Returns:
            float: Minutes the inspector has been waiting for a buffer to free up
        """
        return self.timeBlocked

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
        cleaningTime = self.__generateRandomCleaningTime()
        currentTime = event.getStartTime()
        componentType = self.__selectComponentToClean()
        if (componentType == None):
            raise ValueError("Inspector is not fully configured for use. Please set the components this inspector should handle.")

        doneEvent = InspectorEvent(currentTime, (currentTime + cleaningTime), EventType.ID, self.id, componentType)
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
        success = self.__iterateThroughBuffers(event.getComponentType())
        if success:
            currentTime = event.getStartTime()
            startEvent = InspectorEvent(currentTime, currentTime, EventType.IS, self.id, None)
            return startEvent
        else:
            self.isBlocked = True
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
            success = self.__iterateThroughBuffers(event.getComponentType())
            if success:
                self.isBlocked = False
                currentTime = event.getStartTime()
                startEvent = InspectorEvent(currentTime, currentTime, EventType.IS, self.id, None)
                return startEvent
        return None

    def __generateRandomCleaningTime(self) -> float:
        """For deliverable 1, we are not calculating the distribution of the given files so we will randomly
        select a time from the sample data to use.

        Returns:
            float: The amount of time the inspector will take to clean the component
        """
        index = random.randint(0, len(self.timeData)-1)
        return self.timeData[index]
    
    def __selectComponentToClean(self) -> Component:
        """If the inspector handles more than one component, randomly select which one to clean.

        Returns:
            Component: The component type to be cleaned
        """
        if self.numComponentsToHandle == 1:
            return self.componentsToHandle[0]
        else:
            index = random.randint(0, self.numComponentsToHandle - 1)
            return self.componentsToHandle[index]
    
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
