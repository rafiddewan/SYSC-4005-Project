from Event import Event
from EventType import EventType
from Inspector import Inspector
from InspectorEvent import InspectorEvent
from Workstation import WorkStation
from Buffer import Buffer
from Component import Component
from typing import List
from RandomNumberGeneration import RandomNumberGeneration

MAX_BUFFER_SIZE = 2


def createBuffers()-> List[Buffer]:
    """
    Creates the buffers for the inspectors and workstations to use.
    Returns:
        List[Buffer]: the list containing all buffers
    """
    buf1 = Buffer(1,MAX_BUFFER_SIZE,Component.C1, "Buffer 1")
    buf2 = Buffer(2,MAX_BUFFER_SIZE,Component.C1, "Buffer 2")
    buf3 = Buffer(3,MAX_BUFFER_SIZE,Component.C1, "Buffer 3")
    buf4 = Buffer(4,MAX_BUFFER_SIZE,Component.C2, "Buffer 4")
    buf5 = Buffer(5,MAX_BUFFER_SIZE,Component.C3, "Buffer 5")
    return [buf1, buf2, buf3, buf4, buf5]


def createInspectors(buffers: List[Buffer], seeds: dict[int]) -> List[Inspector]:
    """
    Initializes the inspectors.
    Args:
            buffers: The list of buffers the inspectors will use
    Returns:
        List[Inspector]: a list containing all inspectors
    """
    gen1 = RandomNumberGeneration(seeds[0], 0.096545)
    ins1 = Inspector(1, 3, [Component.C1], [gen1], "Inspector 1")
    ins1.setBuffer(0, buffers[0])
    ins1.setBuffer(1, buffers[1])
    ins1.setBuffer(2, buffers[2])

    gen2 = RandomNumberGeneration(seeds[100000], 0.064363)
    gen3 = RandomNumberGeneration(seeds[200000], 0.048467)
    ins2 = Inspector(2, 2, [Component.C2, Component.C3], [gen2, gen3], "Inspector 2")
    ins2.setBuffer(0, buffers[3])
    ins2.setBuffer(1, buffers[4])
    return [ins1, ins2]


def createWorkstations(buffers: List[Buffer], seeds: List[int])-> List[WorkStation]:
    """
    Initializes the workstations.
    Args:
            buffers: The list of buffers the workstations will use
    Returns:
        List[Workstation]: a list containing all workstations
    """
    gen1 = RandomNumberGeneration(seeds[300000], 0.217183)
    gen2 = RandomNumberGeneration(seeds[400000], 0.090150)
    gen3 = RandomNumberGeneration(seeds[500000], 0.113688)

    work1 = WorkStation(1, 1, gen1, "Workstation 1")
    work2 = WorkStation(2, 2, gen2, "Workstation 2")
    work3 = WorkStation(3, 2, gen3, "Workstation 3")
    
    work1.setBuffer(0, buffers[0])
    work2.setBuffer(0, buffers[1])
    work2.setBuffer(1, buffers[3])

    work3.setBuffer(0, buffers[2])
    work3.setBuffer(1, buffers[4])
    return [work1, work2, work3]


class Simulation:

    def __init__(self):
        """
        Constructor for a Simulation which will simulate the system.
        """
        self.time = 60
        self.fel = []
        g1 = RandomNumberGeneration(0, 0.0)
        seeds = g1.generateRandomNumberStreams(100000, 6)
        print(seeds)
        self.buffers = createBuffers()
        self.inspectors = createInspectors(self.buffers, seeds)
        self.workstations = createWorkstations(self.buffers, seeds)
        self.addStartingEvents()

    
    def addStartingEvents(self):
        """
        Adds the events that are created at the very start of the simulation. 
        Events to start each inspector and a Simulation Done event
        """
        self.addEventToFEL(InspectorEvent(0, 0, EventType.IS, 1))
        self.addEventToFEL(InspectorEvent(0, 0, EventType.IS, 2))
        self.addEventToFEL(Event(0, self.time, EventType.SD))

    def addEventToFEL(self, event: Event):
        """
        Adds the given event to the future event list and sorts the list based on the start time of the events
        Args:
                event: The event that will be added to the future event list
        """
        self.fel.append(event)
        self.fel.sort(key=lambda e: e.getStartTime()) #sort fel by the start times

    def addEventsToFEL(self, events: List[Event]):
        """
        Adds the given events to the future event list and sorts the list based on the start time of the events
        Args:
                events: The event list that will be added to the future event list
        """
        for event in events:
            self.fel.append(event)
        self.fel.sort(key=lambda x: x.getStartTime()) #sort fel by the start times

    def handleInspectorStarted(self, event:Event) -> List[Event]:
        """
        Handles the logic for when an inspector started event is next.
        Passes the event to all inspectors to handle individually.
        Args:
                event: The event that is to be handled
        Returns:
            List[Event]: a list containing Events from the inspectors
        """
        events = []
        for inspector in self.inspectors:
            newEvent = inspector.handleInspectorStarted(event)
            if newEvent is not None:
                events.append(newEvent)
        return events

    def handleInspectorDone(self, event:Event) -> List[Event]:
        """
        Handles the logic for when an Inspector Done event is next.
        Passes the event to all inspectors and workstations to handle individually.
        Args:
                event: The event that is to be handled
        Returns:
            List[Event]: a list containing Events from the inspectors and workstations
        """
        events = []
        for inspector in self.inspectors:
            newEvent = inspector.handleInspectorDone(event)
            if newEvent is not None:
                events.append(newEvent)
        for workstation in self.workstations:
            newEvent = workstation.handleInspectorDone(event)
            if newEvent is not None:
                events.append(newEvent)
        return events

    def handleWorkstationStarted(self, event:Event) -> List[Event]:
        """
        Handles the logic for when an Workstation Started event is next.
        Passes the event to all inspectors and workstations to handle individually.
        Args:
                event: The event that is to be handled
        Returns:
            List[Event]: a list containing Events from the inspectors and workstations
        """
        events = []
        for workstation in self.workstations:
            newEvent = workstation.handleWorkstationStarted(event)
            if newEvent is not None:
                events.append(newEvent)
        for inspector in self.inspectors:
            newEvent = inspector.handleWorkstationStarted(event)
            if newEvent is not None:
                events.append(newEvent)
        return events

    def handleWorkstationDone(self, event:Event) -> List[Event]:
        """
        Handles the logic for when an Workstation Done event is next.
        Passes the event to all workstations to handle individually.
        Args:
                event: The event that is to be handled
        Returns:
            List[Event]: a list containing Events from the workstations
        """
        events = []
        for workstation in self.workstations:
            newEvent = workstation.handleWorkstationDone(event)
            if newEvent is not None:
                events.append(newEvent)
        return events

    def run(self):
        """
        Handles the logic for running the simulation. 
        Loops over the event list, removing the next element in the Future Event List and passing it to the corresponding handler
        Args:
                event: The event that is to be handled
        Returns:
            List[Event]: a list containing Events from the workstations
        """
        done = False
        while not done:
            event:Event = self.fel.pop(0)
            if event.getEventType() == EventType.IS:
                events = self.handleInspectorStarted(event)
                self.addEventsToFEL(events)
            elif event.getEventType() == EventType.ID:
                events = self.handleInspectorDone(event)
                self.addEventsToFEL(events)
            elif event.getEventType() == EventType.WS:
                events = self.handleWorkstationStarted(event)
                self.addEventsToFEL(events)
            elif event.getEventType() == EventType.WD:
                events = self.handleWorkstationDone(event)
                self.addEventsToFEL(events)
            elif event.getEventType() == EventType.SD:
                done = True
            else:
                raise ValueError("Unidentified EventType received.")
        print("Simulation successfully completed")
        self.printStatistics()

    def printStatistics(self):
        totalArrivals = 0
        totalDepartures = self.workstations[0].getNumProductsCreated() + \
                          (2 * self.workstations[1].getNumProductsCreated()) + \
                          (2 * self.workstations[2].getNumProductsCreated())

        for workstation in self.workstations:
            print(workstation.getTitle() + " is busy " + str((workstation.getMinutesBusy()/self.time) * 100) + "% of the time.")
            print(workstation.getTitle() + " built " + str(workstation.getNumProductsCreated()) + " products.")
            print(workstation.getTitle() + " has a throughput of " + str((workstation.getNumProductsCreated()/self.time) * 100))
        for inspector in self.inspectors:
            print(inspector.getTitle() + " has picked up " + str(inspector.getNumComponentsPickedUp()) + " components")
            print(inspector.getTitle() + " is blocked " + str((inspector.getTimeBlocked()/self.time) * 100) + "% of the time.")
            totalArrivals += inspector.getNumComponentsPickedUp()
        for buffer in self.buffers:
            print(buffer.getTitle() + " has an avg buffer occupancy of ")

        print("Arrival rate: " + str(totalArrivals))
        print("Departure rate: " + str(totalDepartures))


def main():
    sim = Simulation()
    sim.run()


if __name__ == "__main__":
   main()
