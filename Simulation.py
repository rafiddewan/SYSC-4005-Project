from Event import Event
from EventType import EventType
from Inspector import Inspector
from InspectorEvent import InspectorEvent
from Replication import Replication
from Workstation import WorkStation
from Buffer import Buffer
from ComponentType import ComponentType
from typing import List
from RandomNumberGeneration import RandomNumberGeneration

MAX_BUFFER_SIZE = 2


def createBuffers() -> List[Buffer]:
    """
    Creates the buffers for the inspectors and workstations to use.
    Returns:
        List[Buffer]: the list containing all buffers
    """
    buf1 = Buffer(1, MAX_BUFFER_SIZE, ComponentType.C1)
    buf2 = Buffer(2, MAX_BUFFER_SIZE, ComponentType.C1)
    buf3 = Buffer(3, MAX_BUFFER_SIZE, ComponentType.C1)
    buf4 = Buffer(4, MAX_BUFFER_SIZE, ComponentType.C2)
    buf5 = Buffer(5, MAX_BUFFER_SIZE, ComponentType.C3)
    return [buf1, buf2, buf3, buf4, buf5]


def createInspectors(buffers: List[Buffer], seeds: dict[int]) -> List[Inspector]:
    """
    Initializes the inspectors.
    Args:
            buffers: The list of buffers the inspectors will use
            seeds: A dictionary of the seeds that are being used for the simulation
    Returns:
        List[Inspector]: a list containing all inspectors
    """
    gen1 = RandomNumberGeneration(seeds[0], 0.096545)
    ins1 = Inspector(1, 3, [ComponentType.C1], [gen1])
    ins1.setBuffer(0, buffers[0])
    ins1.setBuffer(1, buffers[1])
    ins1.setBuffer(2, buffers[2])

    gen2 = RandomNumberGeneration(seeds[100000], 0.064363)
    gen3 = RandomNumberGeneration(seeds[200000], 0.048467)
    ins2 = Inspector(2, 2, [ComponentType.C2, ComponentType.C3], [gen2, gen3])
    ins2.setBuffer(0, buffers[3])
    ins2.setBuffer(1, buffers[4])
    return [ins1, ins2]


def createWorkstations(buffers: List[Buffer], seeds: dict[int]) -> List[WorkStation]:
    """
    Initializes the workstations.
    Args:
            buffers: The list of buffers the workstations will use
            seeds: A dictionary of the seeds that are being used for the simulation
    Returns:
        List[Workstation]: a list containing all workstations
    """
    gen1 = RandomNumberGeneration(seeds[300000], 0.217183)
    gen2 = RandomNumberGeneration(seeds[400000], 0.090150)
    gen3 = RandomNumberGeneration(seeds[500000], 0.113688)

    work1 = WorkStation(1, 1, gen1)
    work2 = WorkStation(2, 2, gen2)
    work3 = WorkStation(3, 2, gen3)
    
    work1.setBuffer(0, buffers[0])
    work2.setBuffer(0, buffers[1])
    work2.setBuffer(1, buffers[3])

    work3.setBuffer(0, buffers[2])
    work3.setBuffer(1, buffers[4])
    return [work1, work2, work3]


class Simulation:

    def __init__(self, seeds):
        """
        Constructor for a Simulation which will simulate the system.
        """
        self.time = 15000
        self.warmup = 1000
        self.steadyStateTime = self.time - self.warmup
        self.clock = 0
        self.fel = []
        # self.b = 100000
        # g1 = RandomNumberGeneration(0, 0.0)
        # seeds = g1.generateRandomNumberStreams(self.b, 6)
        # print("Seeds being used: " + str(seeds))
        self.buffers = createBuffers()
        self.inspectors = createInspectors(self.buffers, seeds)
        self.workstations = createWorkstations(self.buffers, seeds)
        self.addStartingEvents()
        self.totalComponentTime = 0
        self.xis = {}


    def addStartingEvents(self):
        """
        Adds the events that are created at the very start of the simulation. 
        Events to start each inspector and a Simulation Done event
        """
        self.addEventToFEL(InspectorEvent(0, 0, EventType.IS, 1))
        self.addEventToFEL(InspectorEvent(0, 0, EventType.IS, 2))
        self.addEventToFEL(Event(0, self.warmup, EventType.SSS))
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

    def addBufferOccupancies(self, timeElapsed):
        """
        Iterates over the buffers and calls a method to accumulate the buffer occupancies
        Args:
            timeElapsed: The amount of time elapsed since the last calculation

        Returns: None
        """
        for buffer in self.buffers:
            buffer.accumulateOcc(timeElapsed)

    def addAverageInSystem(self,timeElapsed):
        for buffer in self.buffers:
            self.totalComponentTime += buffer.getSize() * timeElapsed

        for inspector in self.inspectors:
            self.totalComponentTime += timeElapsed #inspectors always have a component

        for workstation in self.workstations:
            if(workstation.getIsBusy()):
                self.totalComponentTime += workstation.getNumComponents() * timeElapsed

    def setSteadyState(self):
        for buffer in self.buffers:
            buffer.setSteadyState(True)

        for inspector in self.inspectors:
            inspector.setSteadyState(True)

        for workstation in self.workstations:
            workstation.setSteadyState(True)

    def getXis(self):
        return self.xis

    def grabXis(self):
        self.xis[0] = self.inspectors[0].getGenerators()[0].getXi()
        self.xis[100000] = self.inspectors[1].getGenerators()[0].getXi()
        self.xis[200000] = self.inspectors[1].getGenerators()[1].getXi()
        self.xis[300000] = self.workstations[0].getGenerator().getXi()
        self.xis[400000] = self.workstations[1].getGenerator().getXi()
        self.xis[500000] = self.workstations[2].getGenerator().getXi()

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
            #print("----------------------------------------------------------------")
            event:Event = self.fel.pop(0)

            oldClock = self.clock
            newClock = event.getStartTime()
            timeElapsed = newClock - oldClock
            # print(f"Clock value: {self.clock}")
            # print(f"Time elapsed since last event {timeElapsed}")
            self.addBufferOccupancies(timeElapsed)
            self.addAverageInSystem(timeElapsed)
            self.clock = newClock

            if event.getEventType() == EventType.IS:
                # print(
                #     f"Event: {event.getEventType()} Inspector: {event.getInspectorId()} "
                #     f"Created Time: {event.getCreatedTime()} Start Time: {event.getStartTime()}")
                events = self.handleInspectorStarted(event)
                self.addEventsToFEL(events)
            elif event.getEventType() == EventType.ID:
                # print(
                #     f"Event: {event.getEventType()} Inspector: {event.getInspectorId()} "
                #     f"Created Time: {event.getCreatedTime()} Start Time: {event.getStartTime()}")
                events = self.handleInspectorDone(event)
                self.addEventsToFEL(events)
            elif event.getEventType() == EventType.WS:
                # print(
                #     f"Event: {event.getEventType()} Workstation: {event.getWorkstationId()} "
                #     f"Created Time: {event.getCreatedTime()} Start Time: {event.getStartTime()}")
                events = self.handleWorkstationStarted(event)
                self.addEventsToFEL(events)
            elif event.getEventType() == EventType.WD:
                # print(
                #     f"Event: {event.getEventType()} Workstation: {event.getWorkstationId()} "
                #     f"Created Time: {event.getCreatedTime()} Start Time: {event.getStartTime()}")
                events = self.handleWorkstationDone(event)
                self.addEventsToFEL(events)
            elif event.getEventType() == EventType.SSS:
                self.setSteadyState()
            elif event.getEventType() == EventType.SD:
                done = True
            else:
                raise ValueError("Unidentified EventType received.")
        print("Simulation successfully completed")
        self.grabXis()
        # self.printStatistics()

    def printWorkstationStats(self, workstation):
        """
        Print out the statistics of a given workstation
        Args:
            workstation: the given workstation

        Returns: None

        """
        print("Workstation " + str(workstation.getId()) + " is busy " + str(
            (workstation.getMinutesBusy() / self.steadyStateTime) * 100) + "% of the time.")
        print("Workstation " + str(workstation.getId()) + " built " + str(
            workstation.getNumProductsCreated()) + " products.")
        print("Workstation " + str(workstation.getId()) + " has a throughput of " + str(
            (workstation.getNumProductsCreated() / self.steadyStateTime) * 100))

    def printInspectorStats(self, inspector):
        """
        Print out the statistics of a given inspector
        Args:
            inspector: The given inspector

        Returns: None

        """
        print("Inspector " + str(inspector.getId()) + " has picked up " + str(
            inspector.getNumComponentsPickedUp()) + " components")
        print("Inspector " + str(inspector.getId()) + " is blocked " + str(
            (inspector.getTimeBlocked() / self.steadyStateTime) * 100) + "% of the time.")

    def printBufferStats(self, buffer):
        """
        Print out the statistics of a given buffer
        Args:
            buffer: The given buffer

         Returns: None

        """
        print("Buffer " + str(buffer.getId()) + " has an avg buffer occupancy of " + str(
            buffer.getCummulativeOcc() / self.steadyStateTime))
        print("Left over buffer size " + str(buffer.getSize()))

    def printStatistics(self):
        """
        Print out the statistics of the simulation
        Returns: none

        """
        totalArrivals = 0
        totalCompletedCompTime = 0
        totalDepartures = self.workstations[0].getNumProductsCreated() + \
                          (2 * self.workstations[1].getNumProductsCreated()) + \
                          (2 * self.workstations[2].getNumProductsCreated())
        totalLeftInBuffer = 0
        totalLeftOverInspectorDoneEvents = 0
        totalProducts = 0
        totalLeftOverWorkstationDoneEvents = 0
        totalInspectorsBlockedAndHolding = 0

        print(f"\n-----------------------Individual Statistics-----------------------")
        for workstation in self.workstations:
            self.printWorkstationStats(workstation)
            totalProducts += workstation.getNumProductsCreated()
            for comp in workstation.componentsBuilt:
                time = comp.getDepartureTime() - comp.getArrivalTime()
                totalCompletedCompTime += time
        for inspector in self.inspectors:
            self.printInspectorStats(inspector)
            if inspector.isBlocked:
                totalInspectorsBlockedAndHolding += 1
            totalArrivals += inspector.getNumComponentsPickedUp()
        print(f"\n")
        for buffer in self.buffers:
            self.printBufferStats(buffer)
            totalLeftInBuffer += buffer.getSize()

        print(f"\n---------------------------Statistics---------------------------")
        print("Total Throughput: " + str(totalProducts/self.steadyStateTime))
        print(f"\nTotal Arrivals: " + str(totalArrivals))
        print("Total Departures: " + str(totalDepartures))
        print("Left over events: ")
        for event in self.fel:
            print(str(event.getEventType()))
            if event.getEventType() == EventType.ID:
                totalLeftOverInspectorDoneEvents += 1
            if event.getEventType() == EventType.WD:
                totalLeftOverWorkstationDoneEvents += len(self.workstations[event.getWorkstationId() - 1].getBuffers())
        print("Total due to leftover events: " + str(totalLeftOverWorkstationDoneEvents + totalLeftOverInspectorDoneEvents))
        print("Total left in buffers: " + str(totalLeftInBuffer))
        print("Total left due to blocked inspectors: " + str(totalInspectorsBlockedAndHolding))
        print("Does input = output? " +
              str(totalArrivals == (totalDepartures + totalLeftOverInspectorDoneEvents + totalLeftInBuffer +
                                    totalLeftOverWorkstationDoneEvents + totalInspectorsBlockedAndHolding)))
        print(f"\nLittle's law: ")
        print("Arrival Rate: " + str(totalArrivals/self.steadyStateTime))
        print("Average Time in System: " + str(totalCompletedCompTime/totalDepartures))
        print("Arrival Rate * Average Time in System: " + str((totalCompletedCompTime/totalDepartures) * (totalArrivals/self.steadyStateTime)))
        print("Average Number of Components in the System: " + str(self.totalComponentTime/self.steadyStateTime))

    def getStatistics(self):
        replication = Replication()
        totalProducts = 0
        for workstation in self.workstations:
            probabilityWorkstationBusy = (workstation.getMinutesBusy() / self.steadyStateTime) * 100
            replication.addWorkstationBusyProbability(workstation.getId(), probabilityWorkstationBusy)
            totalProducts += workstation.getNumProductsCreated()
        for inspector in self.inspectors:
            probabilityInspectorBlocked = (inspector.getTimeBlocked() / self.steadyStateTime) * 100
            replication.addInspectorBlockedProbability(inspector.getId(), probabilityInspectorBlocked)
        for buffer in self.buffers:
            avgBufferOccup = buffer.getCummulativeOcc() / self.steadyStateTime
            replication.addAvgBufferOccupancy(buffer.getId(), avgBufferOccup)
        throughput = totalProducts/self.steadyStateTime
        replication.setThroughput(throughput)
        return replication
