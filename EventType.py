from enum import Enum


class EventType(Enum):
    IS = "Inspect Started"
    ID = "Inspector Done"
    WS = "Workstation Started"
    WD = "Workstation Done"
    SD = "Simulation Done"
